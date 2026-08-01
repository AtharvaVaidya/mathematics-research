#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <regex>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using CaDiCaL::Solver;

static void add_clause(Solver &solver, std::initializer_list<int> clause) {
  for (int literal : clause) solver.add(literal);
  solver.add(0);
}

static void xor_even_three(Solver &solver, int first, int second, int third) {
  add_clause(solver, {first, second, -third});
  add_clause(solver, {first, -second, third});
  add_clause(solver, {-first, second, third});
  add_clause(solver, {-first, -second, -third});
}

static std::vector<std::pair<int, int>> read_edges(const std::string &path) {
  std::ifstream input(path);
  std::stringstream buffer;
  buffer << input.rdbuf();
  const std::string text = buffer.str();
  std::regex pattern(R"("u":\s*([0-9]+),\s*"v":\s*([0-9]+))");
  std::vector<std::pair<int, int>> edges;
  for (std::sregex_iterator it(text.begin(), text.end(), pattern), end;
       it != end; ++it) {
    edges.emplace_back(std::stoi((*it)[1]), std::stoi((*it)[2]));
  }
  return edges;
}

static std::array<int, 4> parse_support(const std::string &line) {
  std::istringstream input(line);
  std::array<int, 4> support;
  for (int &edge : support) {
    if (!(input >> edge)) throw std::runtime_error("short support row");
  }
  int extra;
  if (input >> extra) throw std::runtime_error("long support row");
  if (!std::is_sorted(support.begin(), support.end()) ||
      std::adjacent_find(support.begin(), support.end()) != support.end()) {
    throw std::runtime_error("support is not a sorted set");
  }
  return support;
}

static bool contains(const std::array<int, 4> &support, int edge) {
  return std::binary_search(support.begin(), support.end(), edge);
}

static std::vector<unsigned char> packing_cycle(
    const std::vector<std::pair<int, int>> &edges, int vertices,
    const std::array<int, 4> &support) {
  const int edge_count = static_cast<int>(edges.size());
  std::vector<std::vector<int>> incidence(vertices);
  std::vector<unsigned char> terminal(vertices);
  Solver solver;
  for (int edge = 0; edge < edge_count; ++edge) {
    auto [first, second] = edges[edge];
    if (contains(support, edge)) {
      if (terminal[first] || terminal[second])
        throw std::runtime_error("support is not a matching");
      terminal[first] = terminal[second] = 1;
    } else {
      incidence[first].push_back(edge);
      incidence[second].push_back(edge);
      add_clause(solver, {-(edge + 1), -(edge_count + edge + 1)});
    }
  }
  for (int vertex = 0; vertex < vertices; ++vertex) {
    const auto &row = incidence[vertex];
    if (terminal[vertex]) {
      if (row.size() != 2) throw std::runtime_error("bad terminal degree");
      const int red_first = row[0] + 1;
      const int red_second = row[1] + 1;
      const int blue_first = edge_count + row[0] + 1;
      const int blue_second = edge_count + row[1] + 1;
      add_clause(solver, {red_first, red_second});
      add_clause(solver, {-red_first, -red_second});
      add_clause(solver, {blue_first, blue_second});
      add_clause(solver, {-blue_first, -blue_second});
    } else {
      if (row.size() != 3) throw std::runtime_error("bad internal degree");
      xor_even_three(solver, row[0] + 1, row[1] + 1, row[2] + 1);
      xor_even_three(solver, edge_count + row[0] + 1,
                     edge_count + row[1] + 1,
                     edge_count + row[2] + 1);
    }
  }
  if (solver.solve() != 10) throw std::runtime_error("nonpacking support");
  std::vector<unsigned char> cycle((edge_count + 7) / 8);
  for (int edge = 0; edge < edge_count; ++edge) {
    if (contains(support, edge)) continue;
    const bool red = solver.val(edge + 1) > 0;
    const bool blue = solver.val(edge_count + edge + 1) > 0;
    if (red || blue) cycle[edge / 8] |= 1u << (edge % 8);
  }
  return cycle;
}

static void verify_cycle(
    const std::vector<std::pair<int, int>> &edges, int vertices,
    const std::array<int, 4> &support,
    const std::vector<unsigned char> &cycle) {
  const int edge_count = static_cast<int>(edges.size());
  std::vector<unsigned char> terminal(vertices);
  std::vector<std::vector<int>> selected(vertices);
  for (int edge : support) {
    if (edge < 0 || edge >= edge_count)
      throw std::runtime_error("out-of-range support edge");
    auto [first, second] = edges[edge];
    if (terminal[first] || terminal[second])
      throw std::runtime_error("support is not a matching");
    terminal[first] = terminal[second] = 1;
    if ((cycle[edge / 8] >> (edge % 8)) & 1u)
      throw std::runtime_error("cycle uses support edge");
  }
  for (int edge = 0; edge < edge_count; ++edge) {
    if (!((cycle[edge / 8] >> (edge % 8)) & 1u)) continue;
    auto [first, second] = edges[edge];
    selected[first].push_back(second);
    selected[second].push_back(first);
  }
  for (int vertex = 0; vertex < vertices; ++vertex) {
    const std::size_t degree = selected[vertex].size();
    if (terminal[vertex] ? degree != 2 : !(degree == 0 || degree == 2))
      throw std::runtime_error("witness is not a cycle through terminals");
  }
  std::vector<unsigned char> seen(vertices);
  for (int root = 0; root < vertices; ++root) {
    if (selected[root].empty() || seen[root]) continue;
    int terminal_count = 0;
    std::queue<int> todo;
    todo.push(root);
    seen[root] = 1;
    while (!todo.empty()) {
      const int vertex = todo.front();
      todo.pop();
      terminal_count += terminal[vertex];
      for (int neighbour : selected[vertex]) {
        if (seen[neighbour]) continue;
        seen[neighbour] = 1;
        todo.push(neighbour);
      }
    }
    if (terminal_count & 1)
      throw std::runtime_error("odd-marked circuit component");
  }
}

int main(int argc, char **argv) {
  if (argc != 7) {
    std::cerr << "usage: generate graph.json vertices supports start count output\n";
    return 2;
  }
  const auto edges = read_edges(argv[1]);
  const int vertices = std::stoi(argv[2]);
  const std::string support_path = argv[3];
  const std::uint64_t start = std::stoull(argv[4]);
  const std::uint64_t count = std::stoull(argv[5]);
  const std::string output_path = argv[6];
  if (edges.empty()) throw std::runtime_error("no graph edges");

  std::ifstream supports(support_path);
  std::string line;
  for (std::uint64_t index = 0; index < start; ++index) {
    if (!std::getline(supports, line))
      throw std::runtime_error("start exceeds corpus");
  }
  std::ofstream output(output_path, std::ios::binary);
  for (std::uint64_t offset = 0; offset < count; ++offset) {
    if (!std::getline(supports, line))
      throw std::runtime_error("count exceeds corpus");
    const auto support = parse_support(line);
    const auto cycle = packing_cycle(edges, vertices, support);
    verify_cycle(edges, vertices, support, cycle);
    output.write(reinterpret_cast<const char *>(cycle.data()), cycle.size());
    if (!output) throw std::runtime_error("witness write failed");
    if ((offset + 1) % 100000 == 0)
      std::cerr << "start " << start << " checked " << (offset + 1) << '\n';
  }
  std::cout << "WROTE start " << start << " count " << count
            << " bytes_per_row " << ((edges.size() + 7) / 8) << '\n';
}
