#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Edge = std::pair<int, int>;

static void add_clause(CaDiCaL::Solver &solver,
                       std::initializer_list<int> literals) {
  for (int literal : literals) solver.add(literal);
  solver.add(0);
}

static std::string graph6_from_state(const std::string &path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open state file");
  std::string line;
  bool first = true;
  while (std::getline(input, line)) {
    if (first && !line.empty() && line[0] == '~') return line;
    first = false;
    if (line.rfind("graph6=", 0) == 0) return line.substr(7);
  }
  throw std::runtime_error("state has no graph6 line");
}

static std::pair<int, std::vector<Edge>> decode_graph6(const std::string &s) {
  std::size_t position = 0;
  int n = 0;
  if (s.empty()) throw std::runtime_error("empty graph6");
  if (static_cast<unsigned char>(s[position]) != 126) {
    n = static_cast<unsigned char>(s[position++]) - 63;
  } else {
    ++position;
    if (position >= s.size()) throw std::runtime_error("truncated graph6");
    if (static_cast<unsigned char>(s[position]) != 126) {
      if (position + 3 > s.size()) throw std::runtime_error("truncated graph6");
      n = ((static_cast<unsigned char>(s[position]) - 63) << 12) |
          ((static_cast<unsigned char>(s[position + 1]) - 63) << 6) |
          (static_cast<unsigned char>(s[position + 2]) - 63);
      position += 3;
    } else {
      ++position;
      if (position + 6 > s.size()) throw std::runtime_error("truncated graph6");
      for (int k = 0; k < 6; ++k)
        n = (n << 6) | (static_cast<unsigned char>(s[position++]) - 63);
    }
  }
  std::vector<Edge> edges;
  int bit_position = 6;
  unsigned char word = 0;
  for (int right = 1; right < n; ++right) {
    for (int left = 0; left < right; ++left) {
      if (bit_position == 6) {
        if (position >= s.size()) throw std::runtime_error("truncated data");
        word = static_cast<unsigned char>(s[position++]) - 63;
        if (word > 63) throw std::runtime_error("bad graph6 character");
        bit_position = 0;
      }
      if ((word >> (5 - bit_position)) & 1) edges.emplace_back(left, right);
      ++bit_position;
    }
  }
  std::sort(edges.begin(), edges.end());
  return {n, edges};
}

int main(int argc, char **argv) {
  if (argc != 3) {
    std::cerr << "usage: find_fivecdc STATE OUTPUT\n";
    return 2;
  }
  try {
    const std::string graph6 = graph6_from_state(argv[1]);
    auto [n, edges] = decode_graph6(graph6);
    const int m = static_cast<int>(edges.size());
    std::vector<std::vector<int>> incident(n);
    for (int edge = 0; edge < m; ++edge) {
      const auto [u, v] = edges[edge];
      incident[u].push_back(edge);
      incident[v].push_back(edge);
    }
    if (n != 144 || m != 216)
      throw std::runtime_error("unexpected graph order or size");
    for (const auto &row : incident)
      if (row.size() != 3) throw std::runtime_error("graph is not cubic");

    CaDiCaL::Solver solver;
    solver.set("quiet", 1);
    auto variable = [m](int edge, int cycle) {
      return 1 + edge * 5 + cycle;
    };

    // Exactly two of the five cycles contain each edge.
    for (int edge = 0; edge < m; ++edge) {
      for (int a = 0; a < 5; ++a)
        for (int b = a + 1; b < 5; ++b)
          for (int c = b + 1; c < 5; ++c)
            add_clause(solver, {-variable(edge, a), -variable(edge, b),
                                -variable(edge, c)});
      for (int omitted = 0; omitted < 5; ++omitted) {
        for (int cycle = 0; cycle < 5; ++cycle)
          if (cycle != omitted) solver.add(variable(edge, cycle));
        solver.add(0);
      }
    }

    // A cubic vertex has even degree in a cycle iff its three incidence
    // bits have even parity.  The four clauses forbid 001, 010, 100, 111.
    for (int vertex = 0; vertex < n; ++vertex) {
      for (int cycle = 0; cycle < 5; ++cycle) {
        const int a = variable(incident[vertex][0], cycle);
        const int b = variable(incident[vertex][1], cycle);
        const int c = variable(incident[vertex][2], cycle);
        add_clause(solver, {a, b, -c});
        add_clause(solver, {a, -b, c});
        add_clause(solver, {-a, b, c});
        add_clause(solver, {-a, -b, -c});
      }
    }

    const int result = solver.solve();
    if (result != 10) {
      std::cerr << "solver result " << result << "\n";
      return result == 20 ? 20 : 1;
    }

    std::array<std::vector<int>, 5> cycles;
    for (int edge = 0; edge < m; ++edge)
      for (int cycle = 0; cycle < 5; ++cycle)
        if (solver.val(variable(edge, cycle)) > 0)
          cycles[cycle].push_back(edge);

    std::ofstream output(argv[2]);
    if (!output) throw std::runtime_error("cannot open output file");
    output << "FIVECDC-WITNESS-V1\n";
    output << "graph6=" << graph6 << "\n";
    output << "n=" << n << "\n";
    output << "m=" << m << "\n";
    output << "edge_order=lexicographic_zero_based\n";
    output << "edges=";
    for (int edge = 0; edge < m; ++edge) {
      if (edge) output << ',';
      output << edges[edge].first << '-' << edges[edge].second;
    }
    output << "\n";
    for (int cycle = 0; cycle < 5; ++cycle) {
      output << 'C' << cycle + 1 << '=';
      for (std::size_t k = 0; k < cycles[cycle].size(); ++k) {
        if (k) output << ',';
        output << cycles[cycle][k];
      }
      output << "\n";
    }
    std::cout << "SAT n=" << n << " m=" << m;
    for (int cycle = 0; cycle < 5; ++cycle)
      std::cout << " |C" << cycle + 1 << "|=" << cycles[cycle].size();
    std::cout << "\n";
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << "\n";
    return 1;
  }
}
