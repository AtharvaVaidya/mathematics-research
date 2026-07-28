#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// Exact direct FiveCDC screen for simple cubic graph6 records.
//
// Base variable x(e,i), 0 <= i < 5, is 5*e+i+1.  Every edge has exactly
// two true coordinates.  For every vertex and coordinate, the incident
// variables have even XOR.  Parity is converted to CNF with the same
// left-associated XOR gates as verifier_a/core.py.  Returned SAT models are
// checked directly against the original exact-two/parity semantics before
// they are printed.  An UNSAT result is deliberately labelled uncertified:
// a counterexample requires a separately emitted and independently checked
// LRAT.

namespace {

struct Graph {
  int n = 0;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::vector<int>> incident;
};

std::pair<int, std::size_t> graph6_order(const std::string &row) {
  if (row.empty()) throw std::runtime_error("empty graph6 record");
  auto value = [&](std::size_t i) {
    if (i >= row.size()) throw std::runtime_error("truncated graph6 order");
    const int x = static_cast<unsigned char>(row[i]) - 63;
    if (x < 0 || x > 63) throw std::runtime_error("invalid graph6 byte");
    return x;
  };
  if (value(0) != 63) return {value(0), 1};
  if (value(1) != 63) {
    const int n = (value(1) << 12) | (value(2) << 6) | value(3);
    if (n < 63) throw std::runtime_error("noncanonical graph6 order");
    return {n, 4};
  }
  std::uint64_t n = 0;
  for (std::size_t i = 2; i < 8; ++i) n = (n << 6) | value(i);
  if (n < 258048 || n > static_cast<std::uint64_t>(INT32_MAX))
    throw std::runtime_error("unsupported graph6 order");
  return {static_cast<int>(n), 8};
}

Graph parse_graph6(std::string row) {
  constexpr const char *header = ">>graph6<<";
  if (row.rfind(header, 0) == 0) row.erase(0, 10);
  const auto [n, offset] = graph6_order(row);
  const std::uint64_t bit_count =
      static_cast<std::uint64_t>(n) * (n - 1) / 2;
  const std::uint64_t data_count = (bit_count + 5) / 6;
  if (row.size() != offset + data_count)
    throw std::runtime_error("graph6 length mismatch");

  Graph graph;
  graph.n = n;
  graph.incident.resize(n);
  std::uint64_t cursor = 0;
  for (int v = 1; v < n; ++v) {
    for (int u = 0; u < v; ++u, ++cursor) {
      const int chunk =
          static_cast<unsigned char>(row[offset + cursor / 6]) - 63;
      const int bit = (chunk >> (5 - cursor % 6)) & 1;
      if (bit) {
        const int edge = static_cast<int>(graph.edges.size());
        graph.edges.push_back({u, v});
        graph.incident[u].push_back(edge);
        graph.incident[v].push_back(edge);
      }
    }
  }
  for (std::uint64_t at = bit_count; at < data_count * 6; ++at) {
    const int chunk =
        static_cast<unsigned char>(row[offset + at / 6]) - 63;
    if ((chunk >> (5 - at % 6)) & 1)
      throw std::runtime_error("nonzero graph6 padding");
  }
  for (const auto &row_incident : graph.incident)
    if (row_incident.size() != 3)
      throw std::runtime_error("graph is not cubic");
  return graph;
}

void check_connected_bridgeless(const Graph &graph) {
  std::vector<int> discovery(graph.n, -1), low(graph.n, -1);
  int tick = 0;
  std::vector<int> bridges;
  auto dfs = [&](auto &&self, int vertex, int parent_edge) -> void {
    discovery[vertex] = low[vertex] = tick++;
    for (int edge : graph.incident[vertex]) {
      if (edge == parent_edge) continue;
      const auto [u, v] = graph.edges[edge];
      const int other = u == vertex ? v : u;
      if (discovery[other] < 0) {
        self(self, other, edge);
        low[vertex] = std::min(low[vertex], low[other]);
        if (low[other] > discovery[vertex]) bridges.push_back(edge);
      } else {
        low[vertex] = std::min(low[vertex], discovery[other]);
      }
    }
  };
  if (!graph.n) throw std::runtime_error("empty graph");
  dfs(dfs, 0, -1);
  if (std::find(discovery.begin(), discovery.end(), -1) != discovery.end())
    throw std::runtime_error("graph is disconnected");
  if (!bridges.empty()) throw std::runtime_error("graph has a bridge");
}

int xvar(int edge, int coordinate) { return 5 * edge + coordinate + 1; }

void clause(CaDiCaL::Solver &solver, std::initializer_list<int> literals) {
  for (int literal : literals) solver.add(literal);
  solver.add(0);
}

void xor_gate(CaDiCaL::Solver &solver, int left, int right, int output) {
  clause(solver, {left, right, -output});
  clause(solver, {-left, -right, -output});
  clause(solver, {left, -right, output});
  clause(solver, {-left, right, output});
}

struct Result {
  int status = 0;
  int variables = 0;
  std::vector<unsigned char> labels;
  double seconds = 0.0;
};

Result solve(const Graph &graph) {
  CaDiCaL::Solver solver;
  const int base_variables = 5 * static_cast<int>(graph.edges.size());
  int next_variable = base_variables + 1;

  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    // At most two.
    for (int a = 0; a < 5; ++a)
      for (int b = a + 1; b < 5; ++b)
        for (int c = b + 1; c < 5; ++c)
          clause(solver, {-xvar(edge, a), -xvar(edge, b), -xvar(edge, c)});
    // At least two: every four-variable subset has a true variable.
    for (int omitted = 0; omitted < 5; ++omitted) {
      for (int coordinate = 0; coordinate < 5; ++coordinate)
        if (coordinate != omitted) solver.add(xvar(edge, coordinate));
      solver.add(0);
    }
  }

  for (int vertex = 0; vertex < graph.n; ++vertex) {
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
      int accumulator = xvar(graph.incident[vertex][0], coordinate);
      for (std::size_t step = 1; step < graph.incident[vertex].size(); ++step) {
        const int output = next_variable++;
        xor_gate(solver, accumulator,
                 xvar(graph.incident[vertex][step], coordinate), output);
        accumulator = output;
      }
      clause(solver, {-accumulator});
    }
  }

  const auto started = std::chrono::steady_clock::now();
  const int status = solver.solve();
  const auto stopped = std::chrono::steady_clock::now();
  Result result;
  result.status = status;
  result.variables = next_variable - 1;
  result.seconds =
      std::chrono::duration<double>(stopped - started).count();
  if (status != 10) return result;

  result.labels.resize(graph.edges.size());
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    unsigned char mask = 0;
    for (int coordinate = 0; coordinate < 5; ++coordinate)
      if (solver.val(xvar(edge, coordinate)) > 0)
        mask |= static_cast<unsigned char>(1U << coordinate);
    if (__builtin_popcount(mask) != 2)
      throw std::runtime_error("solver model fails exact-two semantics");
    result.labels[edge] = mask;
  }
  for (int vertex = 0; vertex < graph.n; ++vertex)
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
      int parity = 0;
      for (int edge : graph.incident[vertex])
        parity ^= (result.labels[edge] >> coordinate) & 1;
      if (parity)
        throw std::runtime_error("solver model fails vertex parity semantics");
    }
  return result;
}

std::string json_escape(const std::string &text) {
  std::string out;
  for (unsigned char ch : text) {
    if (ch == '"' || ch == '\\') out.push_back('\\');
    out.push_back(static_cast<char>(ch));
  }
  return out;
}

}  // namespace

int main() {
  std::string row;
  std::uint64_t index = 0;
  std::uint64_t sat = 0, uncertified_unsat = 0;
  double total_seconds = 0.0;
  while (std::getline(std::cin, row)) {
    if (row.empty() || row[0] == '#') continue;
    ++index;
    try {
      const Graph graph = parse_graph6(row);
      check_connected_bridgeless(graph);
      const Result result = solve(graph);
      total_seconds += result.seconds;
      std::cout << "{\"index\":" << index << ",\"graph6\":\""
                << json_escape(row) << "\",\"vertices\":" << graph.n
                << ",\"edges\":" << graph.edges.size()
                << ",\"variables\":" << result.variables
                << ",\"solve_seconds\":" << result.seconds;
      if (result.status == 10) {
        ++sat;
        std::cout << ",\"status\":\"SAT_SEMANTIC_CHECK\",\"labels\":[";
        for (std::size_t edge = 0; edge < result.labels.size(); ++edge) {
          if (edge) std::cout << ',';
          std::cout << static_cast<int>(result.labels[edge]);
        }
        std::cout << "]}";
      } else if (result.status == 20) {
        ++uncertified_unsat;
        std::cout << ",\"status\":\"UNSAT_UNCERTIFIED\"}";
      } else {
        std::cout << ",\"status\":\"UNKNOWN\"}";
      }
      std::cout << '\n';
    } catch (const std::exception &error) {
      std::cout << "{\"index\":" << index << ",\"graph6\":\""
                << json_escape(row) << "\",\"status\":\"ERROR\",\"error\":\""
                << json_escape(error.what()) << "\"}\n";
    }
  }
  std::cerr << "rows=" << index << " sat=" << sat
            << " unsat_uncertified=" << uncertified_unsat
            << " solve_seconds=" << total_seconds << '\n';
  return uncertified_unsat ? 1 : 0;
}
