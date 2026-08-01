// Exact census for the near-perfect-matching oddness question on five-poles.
//
// Input: short graph6 records.  The retained objects are connected simple
// graphs with exactly five degree-two vertices and every other vertex of
// degree three.  For every retained factor-critical graph Q and every
// degree-two terminal q, enumerate near-perfect matchings of Q-q until a
// complement with at most one odd circuit is found, or exhaust them all.
//
// A graph with a bad terminal is additionally checked for the local
// cyclic-four condition needed when Q is a shore in a cyclically
// four-edge-connected cubic completion: no vertex set X contained in Q
// may contain a circuit while
//
//   |delta_completion(X)| = 3|X| - 2|E(Q[X])| <= 3.
//
// The program proves only a finite census.  It is deliberately independent
// of the Python counterexample checker in
// scratch/audit_factor_critical_ear_forest.py.

#include <algorithm>
#include <bit>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

struct Graph {
  int n = 0;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::vector<std::pair<int, int>>> adj;  // neighbour, edge
  std::vector<int> terminals;
};

static Graph parse_graph6(const std::string& text) {
  if (text.empty() || static_cast<unsigned char>(text[0]) >= 126) {
    throw std::runtime_error("expected a nonempty short graph6 record");
  }
  Graph graph;
  graph.n = static_cast<unsigned char>(text[0]) - 63;
  if (graph.n < 1 || graph.n > 62) {
    throw std::runtime_error("unsupported graph order");
  }
  std::vector<int> bits;
  for (std::size_t index = 1; index < text.size(); ++index) {
    const int value = static_cast<unsigned char>(text[index]) - 63;
    if (value < 0 || value >= 64) {
      throw std::runtime_error("bad graph6 byte");
    }
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }
  std::size_t cursor = 0;
  for (int high = 1; high < graph.n; ++high) {
    for (int low = 0; low < high; ++low) {
      if (cursor >= bits.size()) {
        throw std::runtime_error("truncated graph6 record");
      }
      if (bits[cursor]) {
        graph.edges.emplace_back(low, high);
      }
      ++cursor;
    }
  }
  graph.adj.assign(graph.n, {});
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    const auto [left, right] = graph.edges[edge];
    graph.adj[left].emplace_back(right, edge);
    graph.adj[right].emplace_back(left, edge);
  }
  for (int vertex = 0; vertex < graph.n; ++vertex) {
    const auto degree = graph.adj[vertex].size();
    if (degree == 2) {
      graph.terminals.push_back(vertex);
    } else if (degree != 3) {
      throw std::runtime_error("graph does not have degree profile 2/3");
    }
  }
  if (graph.terminals.size() != 5) {
    throw std::runtime_error("graph does not have five degree-two terminals");
  }
  return graph;
}

static bool connected(const Graph& graph) {
  std::uint64_t reached = 1;
  std::uint64_t frontier = 1;
  while (frontier != 0) {
    const std::uint64_t bit = frontier & -frontier;
    frontier ^= bit;
    const int vertex = std::countr_zero(bit);
    for (const auto [other, edge] : graph.adj[vertex]) {
      (void)edge;
      const std::uint64_t other_bit = std::uint64_t{1} << other;
      if ((reached & other_bit) == 0) {
        reached |= other_bit;
        frontier |= other_bit;
      }
    }
  }
  return std::popcount(reached) == graph.n;
}

static bool has_bridge(const Graph& graph) {
  std::vector<int> discovery(graph.n, -1);
  std::vector<int> low(graph.n, -1);
  int timer = 0;
  bool bridge = false;
  const auto visit = [&](const auto& self, int vertex,
                         int parent_edge) -> void {
    discovery[vertex] = low[vertex] = timer++;
    for (const auto [other, edge] : graph.adj[vertex]) {
      if (edge == parent_edge) {
        continue;
      }
      if (discovery[other] < 0) {
        self(self, other, edge);
        low[vertex] = std::min(low[vertex], low[other]);
        if (low[other] > discovery[vertex]) {
          bridge = true;
        }
      } else {
        low[vertex] = std::min(low[vertex], discovery[other]);
      }
    }
  };
  visit(visit, 0, -1);
  return bridge;
}

class MatchingAudit {
 public:
  explicit MatchingAudit(const Graph& graph)
      : graph_(graph), selected_(graph.edges.size(), false) {
    perfect_cache_[0] = true;
  }

  bool factor_critical() {
    const std::uint64_t all = (std::uint64_t{1} << graph_.n) - 1;
    for (int vertex = 0; vertex < graph_.n; ++vertex) {
      if (!has_perfect(all ^ (std::uint64_t{1} << vertex))) {
        return false;
      }
    }
    return true;
  }

  bool terminal_has_odd_bound_witness(int exposed, int maximum_odd_circuits) {
    const std::uint64_t vertices =
        ((std::uint64_t{1} << graph_.n) - 1) ^
        (std::uint64_t{1} << exposed);
    maximum_odd_circuits_ = maximum_odd_circuits;
    return enumerate_until_good(vertices);
  }

  std::uint64_t near_matchings_examined() const {
    return near_matchings_examined_;
  }

 private:
  const Graph& graph_;
  std::unordered_map<std::uint64_t, bool> perfect_cache_;
  std::vector<bool> selected_;
  std::uint64_t near_matchings_examined_ = 0;
  int maximum_odd_circuits_ = 0;

  bool has_perfect(std::uint64_t vertices) {
    const auto known = perfect_cache_.find(vertices);
    if (known != perfect_cache_.end()) {
      return known->second;
    }
    if (std::popcount(vertices) % 2 != 0) {
      return perfect_cache_[vertices] = false;
    }
    int chosen = -1;
    int chosen_degree = 4;
    for (int vertex = 0; vertex < graph_.n; ++vertex) {
      if (((vertices >> vertex) & 1U) == 0) {
        continue;
      }
      int degree = 0;
      for (const auto [other, edge] : graph_.adj[vertex]) {
        (void)edge;
        degree += (vertices >> other) & 1U;
      }
      if (degree < chosen_degree) {
        chosen = vertex;
        chosen_degree = degree;
      }
    }
    if (chosen < 0 || chosen_degree == 0) {
      return perfect_cache_[vertices] = false;
    }
    const std::uint64_t without_chosen =
        vertices ^ (std::uint64_t{1} << chosen);
    for (const auto [other, edge] : graph_.adj[chosen]) {
      (void)edge;
      if (((without_chosen >> other) & 1U) == 0) {
        continue;
      }
      if (has_perfect(without_chosen ^
                      (std::uint64_t{1} << other))) {
        return perfect_cache_[vertices] = true;
      }
    }
    return perfect_cache_[vertices] = false;
  }

  bool enumerate_until_good(std::uint64_t vertices) {
    if (vertices == 0) {
      ++near_matchings_examined_;
      return odd_circuit_count() <= maximum_odd_circuits_;
    }
    int chosen = -1;
    int chosen_degree = 4;
    for (int vertex = 0; vertex < graph_.n; ++vertex) {
      if (((vertices >> vertex) & 1U) == 0) {
        continue;
      }
      int degree = 0;
      for (const auto [other, edge] : graph_.adj[vertex]) {
        (void)edge;
        degree += (vertices >> other) & 1U;
      }
      if (degree < chosen_degree) {
        chosen = vertex;
        chosen_degree = degree;
      }
    }
    if (chosen < 0 || chosen_degree == 0) {
      return false;
    }
    const std::uint64_t without_chosen =
        vertices ^ (std::uint64_t{1} << chosen);
    for (const auto [other, edge] : graph_.adj[chosen]) {
      if (((without_chosen >> other) & 1U) == 0) {
        continue;
      }
      const std::uint64_t reduced =
          without_chosen ^ (std::uint64_t{1} << other);
      if (!has_perfect(reduced)) {
        continue;
      }
      selected_[edge] = true;
      if (enumerate_until_good(reduced)) {
        selected_[edge] = false;
        return true;
      }
      selected_[edge] = false;
    }
    return false;
  }

  int odd_circuit_count() const {
    std::uint64_t seen = 0;
    int odd_circuits = 0;
    for (int start = 0; start < graph_.n; ++start) {
      const std::uint64_t start_bit = std::uint64_t{1} << start;
      if ((seen & start_bit) != 0) {
        continue;
      }
      std::uint64_t component = start_bit;
      std::uint64_t frontier = start_bit;
      int degree_sum = 0;
      while (frontier != 0) {
        const std::uint64_t bit = frontier & -frontier;
        frontier ^= bit;
        const int vertex = std::countr_zero(bit);
        for (const auto [other, edge] : graph_.adj[vertex]) {
          if (selected_[edge]) {
            continue;
          }
          ++degree_sum;
          const std::uint64_t other_bit = std::uint64_t{1} << other;
          if ((component & other_bit) == 0) {
            component |= other_bit;
            frontier |= other_bit;
          }
        }
      }
      seen |= component;
      const int vertices = std::popcount(component);
      const int edges = degree_sum / 2;
      if (edges == vertices && vertices % 2 == 1) {
        ++odd_circuits;
      }
    }
    return odd_circuits;
  }
};

static bool contains_circuit(const Graph& graph, std::uint64_t vertices,
                             int internal_edges) {
  std::uint64_t unseen = vertices;
  int components = 0;
  while (unseen != 0) {
    ++components;
    const std::uint64_t first = unseen & -unseen;
    std::uint64_t reached = first;
    std::uint64_t frontier = first;
    while (frontier != 0) {
      const std::uint64_t bit = frontier & -frontier;
      frontier ^= bit;
      const int vertex = std::countr_zero(bit);
      for (const auto [other, edge] : graph.adj[vertex]) {
        (void)edge;
        const std::uint64_t other_bit = std::uint64_t{1} << other;
        if ((vertices & other_bit) != 0 &&
            (reached & other_bit) == 0) {
          reached |= other_bit;
          frontier |= other_bit;
        }
      }
    }
    unseen &= ~reached;
  }
  return internal_edges >= std::popcount(vertices) - components + 1;
}

static bool locally_cyclic_four_admissible(const Graph& graph) {
  if (graph.n >= 63) {
    throw std::runtime_error("subset audit requires order below 63");
  }
  const std::uint64_t full = (std::uint64_t{1} << graph.n) - 1;
  for (std::uint64_t vertices = 1; vertices != full; ++vertices) {
    int internal_edges = 0;
    for (const auto [left, right] : graph.edges) {
      internal_edges +=
          ((vertices >> left) & 1U) && ((vertices >> right) & 1U);
    }
    const int completed_cut =
        3 * std::popcount(vertices) - 2 * internal_edges;
    if (completed_cut <= 3 &&
        contains_circuit(graph, vertices, internal_edges)) {
      return false;
    }
  }
  return true;
}

static std::string json_escape(const std::string& value) {
  std::string result;
  for (const char character : value) {
    if (character == '\\' || character == '"') {
      result.push_back('\\');
    }
    result.push_back(character);
  }
  return result;
}

int main() {
  try {
    std::uint64_t input_graphs = 0;
    std::uint64_t connected_graphs = 0;
    std::uint64_t internally_bridgeless = 0;
    std::uint64_t factor_critical_graphs = 0;
    std::uint64_t terminal_checks = 0;
    std::uint64_t one_odd_bound_failure_instances = 0;
    std::uint64_t graphs_with_one_odd_bound_failure = 0;
    std::uint64_t one_odd_failure_graphs_locally_cyclic_four = 0;
    std::uint64_t one_odd_failure_graphs_locally_with_at_least_two = 0;
    std::uint64_t corrected_bad_terminal_instances = 0;
    std::uint64_t graphs_with_corrected_bad_terminal = 0;
    std::uint64_t corrected_bad_graphs_locally_cyclic_four = 0;
    std::uint64_t corrected_bad_graphs_locally_with_at_least_two = 0;
    std::uint64_t near_matchings_examined = 0;
    std::string first_one_odd_bound_failure;
    std::string first_one_odd_failure_locally_cyclic_four;
    std::string first_corrected_bad_terminal;
    std::string first_corrected_bad_locally_cyclic_four;
    std::string row;
    while (std::getline(std::cin, row)) {
      if (row.empty() || row[0] == '>') {
        continue;
      }
      ++input_graphs;
      const Graph graph = parse_graph6(row);
      if (!connected(graph)) {
        continue;
      }
      ++connected_graphs;
      if (has_bridge(graph)) {
        continue;
      }
      ++internally_bridgeless;
      MatchingAudit audit(graph);
      if (!audit.factor_critical()) {
        continue;
      }
      ++factor_critical_graphs;
      int one_odd_failures = 0;
      int corrected_bad_terminals = 0;
      std::string one_odd_failure_list;
      std::string corrected_bad_terminal_list;
      for (const int terminal : graph.terminals) {
        ++terminal_checks;
        if (!audit.terminal_has_odd_bound_witness(terminal, 1)) {
          ++one_odd_failures;
          ++one_odd_bound_failure_instances;
          if (first_one_odd_bound_failure.empty()) {
            first_one_odd_bound_failure =
                row + ":" + std::to_string(terminal);
          }
          if (!one_odd_failure_list.empty()) {
            one_odd_failure_list.push_back(',');
          }
          one_odd_failure_list += std::to_string(terminal);
          if (!audit.terminal_has_odd_bound_witness(terminal, 2)) {
            ++corrected_bad_terminals;
            ++corrected_bad_terminal_instances;
            if (first_corrected_bad_terminal.empty()) {
              first_corrected_bad_terminal =
                  row + ":" + std::to_string(terminal);
            }
            if (!corrected_bad_terminal_list.empty()) {
              corrected_bad_terminal_list.push_back(',');
            }
            corrected_bad_terminal_list += std::to_string(terminal);
          }
        }
      }
      near_matchings_examined += audit.near_matchings_examined();
      if (one_odd_failures > 0) {
        ++graphs_with_one_odd_bound_failure;
        const bool local = locally_cyclic_four_admissible(graph);
        if (local) {
          ++one_odd_failure_graphs_locally_cyclic_four;
          if (one_odd_failures >= 2) {
            ++one_odd_failure_graphs_locally_with_at_least_two;
          }
          if (first_one_odd_failure_locally_cyclic_four.empty()) {
            first_one_odd_failure_locally_cyclic_four =
                row + ":" + one_odd_failure_list;
          }
        }
        if (corrected_bad_terminals > 0) {
          ++graphs_with_corrected_bad_terminal;
          if (local) {
            ++corrected_bad_graphs_locally_cyclic_four;
            if (corrected_bad_terminals >= 2) {
              ++corrected_bad_graphs_locally_with_at_least_two;
            }
            if (first_corrected_bad_locally_cyclic_four.empty()) {
              first_corrected_bad_locally_cyclic_four =
                  row + ":" + corrected_bad_terminal_list;
            }
          }
        }
      }
      if (input_graphs % 100000 == 0) {
        std::cerr << "PROGRESS input=" << input_graphs
                  << " factor_critical=" << factor_critical_graphs
                  << " one_odd_failures="
                  << graphs_with_one_odd_bound_failure
                  << " corrected_bad="
                  << graphs_with_corrected_bad_terminal << '\n';
      }
    }
    std::cout
        << "{\"schema\":\"factor-critical-five-pole-oddness-census-v2\","
        << "\"classification\":\"EXACT FINITE CENSUS\","
        << "\"input_graphs\":" << input_graphs << ','
        << "\"connected\":" << connected_graphs << ','
        << "\"internally_bridgeless\":" << internally_bridgeless << ','
        << "\"factor_critical\":" << factor_critical_graphs << ','
        << "\"terminal_checks\":" << terminal_checks << ','
        << "\"near_matchings_examined\":" << near_matchings_examined << ','
        << "\"one_odd_bound_failure_instances\":"
        << one_odd_bound_failure_instances << ','
        << "\"graphs_with_one_odd_bound_failure\":"
        << graphs_with_one_odd_bound_failure << ','
        << "\"one_odd_failure_graphs_locally_cyclic_four\":"
        << one_odd_failure_graphs_locally_cyclic_four << ','
        << "\"one_odd_failure_graphs_locally_cyclic_four_with_at_least_two_terminals\":"
        << one_odd_failure_graphs_locally_with_at_least_two << ','
        << "\"corrected_bad_terminal_instances\":"
        << corrected_bad_terminal_instances << ','
        << "\"graphs_with_corrected_bad_terminal\":"
        << graphs_with_corrected_bad_terminal << ','
        << "\"corrected_bad_graphs_locally_cyclic_four\":"
        << corrected_bad_graphs_locally_cyclic_four << ','
        << "\"corrected_bad_graphs_locally_cyclic_four_with_at_least_two_terminals\":"
        << corrected_bad_graphs_locally_with_at_least_two << ','
        << "\"first_one_odd_bound_failure\":\""
        << json_escape(first_one_odd_bound_failure) << "\","
        << "\"first_one_odd_failure_locally_cyclic_four\":\""
        << json_escape(first_one_odd_failure_locally_cyclic_four) << "\","
        << "\"first_corrected_bad_terminal\":\""
        << json_escape(first_corrected_bad_terminal) << "\","
        << "\"first_corrected_bad_locally_cyclic_four\":\""
        << json_escape(first_corrected_bad_locally_cyclic_four) << "\"}\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR " << error.what() << '\n';
    return 3;
  }
}
