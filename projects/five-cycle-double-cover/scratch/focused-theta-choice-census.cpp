// Exact classifier for the focused prescribed-root theta-choice question.
//
// For each independent edge pair R in a simple cubic graph G:
//   H = G - V(R).
// If H has a perfect matching, classify def0.
// Otherwise the proved deficiency lemma gives def(H)=2.  Enumerate maximum
// near-perfect matchings P of H until G-(R union P) is bridgeless.  In the
// two-branch core dichotomy, bridgeless is exactly theta; exhausting every
// P without one is exactly all-dumbbell.
//
// No SAT solver or project classifier is called.

#include <algorithm>
#include <cstdint>
#include <fstream>
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
};

static Graph parse_graph6(const std::string& text, int expected_order) {
  if (text.empty() || static_cast<unsigned char>(text[0]) >= 126) {
    throw std::runtime_error("expected short graph6");
  }
  Graph graph;
  graph.n = static_cast<unsigned char>(text[0]) - 63;
  if (graph.n != expected_order) {
    throw std::runtime_error("graph6 order mismatch");
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
        throw std::runtime_error("truncated graph6");
      }
      if (bits[cursor]) {
        graph.edges.emplace_back(low, high);
      }
      ++cursor;
    }
  }
  if (static_cast<int>(graph.edges.size()) * 2 != 3 * graph.n) {
    throw std::runtime_error("graph is not cubic-size");
  }
  graph.adj.assign(graph.n, {});
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    const auto [u, v] = graph.edges[edge];
    if (u == v) {
      throw std::runtime_error("loop in simple corpus");
    }
    graph.adj[u].emplace_back(v, edge);
    graph.adj[v].emplace_back(u, edge);
  }
  for (const auto& row : graph.adj) {
    if (row.size() != 3) {
      throw std::runtime_error("graph is not cubic");
    }
  }
  return graph;
}

class Classifier {
 public:
  explicit Classifier(const Graph& graph)
      : graph_(graph),
        all_vertices_((uint32_t{1} << graph.n) - 1),
        in_matching_(graph.edges.size(), false) {
    perfect_cache_.reserve(1 << 16);
    perfect_cache_[0] = true;
  }

  struct Counts {
    uint64_t pairs = 0;
    uint64_t def0 = 0;
    uint64_t def2_theta = 0;
    uint64_t def2_all_dumbbell = 0;
    uint64_t def2_boundary6 = 0;
    uint64_t def2_boundary8 = 0;
    uint64_t near_matchings_checked = 0;
  };

  Counts classify_all(std::string* first_witness) {
    Counts counts;
    for (int first = 0; first < static_cast<int>(graph_.edges.size());
         ++first) {
      const auto [a, b] = graph_.edges[first];
      for (int second = first + 1;
           second < static_cast<int>(graph_.edges.size()); ++second) {
        const auto [c, d] = graph_.edges[second];
        if (a == c || a == d || b == c || b == d) {
          continue;
        }
        ++counts.pairs;
        const uint32_t roots =
            (uint32_t{1} << a) | (uint32_t{1} << b) |
            (uint32_t{1} << c) | (uint32_t{1} << d);
        const uint32_t h_vertices = all_vertices_ & ~roots;
        if (has_perfect_matching(h_vertices)) {
          ++counts.def0;
          continue;
        }
        int internal_u_edges = 0;
        for (const auto [u, v] : graph_.edges) {
          if (((roots >> u) & 1U) && ((roots >> v) & 1U)) {
            ++internal_u_edges;
          }
        }
        const int boundary_u = 12 - 2 * internal_u_edges;
        if (boundary_u == 6) {
          ++counts.def2_boundary6;
        } else if (boundary_u == 8) {
          ++counts.def2_boundary8;
        } else {
          throw std::runtime_error(
              "deficiency-two root has unexpected U-boundary");
        }
        root_first_ = first;
        root_second_ = second;
        in_matching_[first] = true;
        in_matching_[second] = true;
        bool theta = false;
        for (int exposed_first = 0;
             exposed_first < graph_.n && !theta; ++exposed_first) {
          if (!((h_vertices >> exposed_first) & 1U)) {
            continue;
          }
          for (int exposed_second = exposed_first + 1;
               exposed_second < graph_.n && !theta; ++exposed_second) {
            if (!((h_vertices >> exposed_second) & 1U)) {
              continue;
            }
            const uint32_t remaining =
                h_vertices & ~(uint32_t{1} << exposed_first) &
                ~(uint32_t{1} << exposed_second);
            if (!has_perfect_matching(remaining)) {
              continue;
            }
            theta = enumerate_perfect_matchings(
                remaining, &counts.near_matchings_checked);
          }
        }
        in_matching_[first] = false;
        in_matching_[second] = false;
        if (theta) {
          ++counts.def2_theta;
        } else {
          ++counts.def2_all_dumbbell;
          if (first_witness != nullptr && first_witness->empty()) {
            *first_witness =
                std::to_string(first) + "," + std::to_string(second);
          }
        }
      }
    }
    return counts;
  }

 private:
  const Graph& graph_;
  uint32_t all_vertices_;
  std::unordered_map<uint32_t, bool> perfect_cache_;
  std::vector<bool> in_matching_;
  int root_first_ = -1;
  int root_second_ = -1;

  bool has_perfect_matching(uint32_t vertices) {
    const auto known = perfect_cache_.find(vertices);
    if (known != perfect_cache_.end()) {
      return known->second;
    }
    if (__builtin_popcount(vertices) & 1) {
      perfect_cache_[vertices] = false;
      return false;
    }
    int chosen = -1;
    int chosen_degree = 4;
    for (int vertex = 0; vertex < graph_.n; ++vertex) {
      if (!((vertices >> vertex) & 1U)) {
        continue;
      }
      int degree = 0;
      for (const auto [neighbour, edge] : graph_.adj[vertex]) {
        (void)edge;
        degree += (vertices >> neighbour) & 1U;
      }
      if (degree < chosen_degree) {
        chosen_degree = degree;
        chosen = vertex;
      }
    }
    if (chosen < 0 || chosen_degree == 0) {
      perfect_cache_[vertices] = false;
      return false;
    }
    const uint32_t without_chosen = vertices & ~(uint32_t{1} << chosen);
    for (const auto [neighbour, edge] : graph_.adj[chosen]) {
      (void)edge;
      if (!((without_chosen >> neighbour) & 1U)) {
        continue;
      }
      const uint32_t reduced =
          without_chosen & ~(uint32_t{1} << neighbour);
      if (has_perfect_matching(reduced)) {
        perfect_cache_[vertices] = true;
        return true;
      }
    }
    perfect_cache_[vertices] = false;
    return false;
  }

  bool enumerate_perfect_matchings(uint32_t vertices, uint64_t* checked) {
    if (vertices == 0) {
      ++(*checked);
      return complement_is_bridgeless();
    }
    int chosen = -1;
    int chosen_degree = 4;
    for (int vertex = 0; vertex < graph_.n; ++vertex) {
      if (!((vertices >> vertex) & 1U)) {
        continue;
      }
      int degree = 0;
      for (const auto [neighbour, edge] : graph_.adj[vertex]) {
        (void)edge;
        degree += (vertices >> neighbour) & 1U;
      }
      if (degree < chosen_degree) {
        chosen_degree = degree;
        chosen = vertex;
      }
    }
    if (chosen < 0 || chosen_degree == 0) {
      return false;
    }
    const uint32_t without_chosen = vertices & ~(uint32_t{1} << chosen);
    for (const auto [neighbour, edge] : graph_.adj[chosen]) {
      if (!((without_chosen >> neighbour) & 1U)) {
        continue;
      }
      const uint32_t reduced =
          without_chosen & ~(uint32_t{1} << neighbour);
      if (!has_perfect_matching(reduced)) {
        continue;
      }
      in_matching_[edge] = true;
      if (enumerate_perfect_matchings(reduced, checked)) {
        in_matching_[edge] = false;
        return true;
      }
      in_matching_[edge] = false;
    }
    return false;
  }

  bool complement_is_bridgeless() const {
    std::vector<int> discovery(graph_.n, -1);
    std::vector<int> low(graph_.n, -1);
    int timer = 0;
    bool has_bridge = false;
    const auto visit = [&](const auto& self, int vertex,
                           int parent_edge) -> void {
      discovery[vertex] = low[vertex] = timer++;
      for (const auto [neighbour, edge] : graph_.adj[vertex]) {
        if (in_matching_[edge]) {
          continue;
        }
        if (edge == parent_edge) {
          continue;
        }
        if (discovery[neighbour] < 0) {
          self(self, neighbour, edge);
          low[vertex] = std::min(low[vertex], low[neighbour]);
          if (low[neighbour] > discovery[vertex]) {
            has_bridge = true;
          }
        } else {
          low[vertex] = std::min(low[vertex], discovery[neighbour]);
        }
      }
    };
    for (int vertex = 0; vertex < graph_.n; ++vertex) {
      if (discovery[vertex] < 0) {
        visit(visit, vertex, -1);
      }
    }
    return !has_bridge;
  }
};

static std::vector<std::string> read_rows(const std::string& path) {
  std::ifstream input(path);
  if (!input) {
    throw std::runtime_error("cannot open " + path);
  }
  std::vector<std::string> rows;
  std::string line;
  while (std::getline(input, line)) {
    if (!line.empty()) {
      rows.push_back(line);
    }
  }
  return rows;
}

int main(int argc, char** argv) {
  if (argc != 3) {
    std::cerr << "usage: focused-theta-choice-census ORDER CORPUS.g6\n";
    return 2;
  }
  const int order = std::stoi(argv[1]);
  const auto rows = read_rows(argv[2]);
  Classifier::Counts total;
  std::string first_witness;
  for (std::size_t index = 0; index < rows.size(); ++index) {
    const Graph graph = parse_graph6(rows[index], order);
    Classifier classifier(graph);
    std::string witness;
    const auto counts = classifier.classify_all(&witness);
    total.pairs += counts.pairs;
    total.def0 += counts.def0;
    total.def2_theta += counts.def2_theta;
    total.def2_all_dumbbell += counts.def2_all_dumbbell;
    total.def2_boundary6 += counts.def2_boundary6;
    total.def2_boundary8 += counts.def2_boundary8;
    total.near_matchings_checked += counts.near_matchings_checked;
    if (!witness.empty() && first_witness.empty()) {
      first_witness =
          std::to_string(index) + ":" + witness + ":" + rows[index];
    }
    if ((index + 1) % 100 == 0 || index + 1 == rows.size()) {
      std::cerr << "PROGRESS order=" << order
                << " graphs=" << (index + 1)
                << " pairs=" << total.pairs
                << " def0=" << total.def0
                << " def2_theta=" << total.def2_theta
                << " all_dumbbell=" << total.def2_all_dumbbell
                << " boundary6=" << total.def2_boundary6
                << " boundary8=" << total.def2_boundary8
                << " near_checked=" << total.near_matchings_checked
                << "\n";
    }
  }
  std::cout << "{"
            << "\"order\":" << order << ","
            << "\"graphs\":" << rows.size() << ","
            << "\"pairs\":" << total.pairs << ","
            << "\"def0\":" << total.def0 << ","
            << "\"def2_theta\":" << total.def2_theta << ","
            << "\"def2_all_dumbbell\":" << total.def2_all_dumbbell << ","
            << "\"def2_boundary6\":" << total.def2_boundary6 << ","
            << "\"def2_boundary8\":" << total.def2_boundary8 << ","
            << "\"near_matchings_checked\":"
            << total.near_matchings_checked << ","
            << "\"first_witness\":\"" << first_witness << "\""
            << "}\n";
  return 0;
}
