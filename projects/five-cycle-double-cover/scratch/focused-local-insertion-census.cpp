// Exact test of a restricted theta-witness construction.
//
// For each independent root pair {r1,r2} with G-V(r1,r2) deficient,
// search in both orientations.  In the orientation (keep,insert), take
// a perfect matching M containing keep.  If insert=ab is not in M,
// write ax,by for the two M-edges at a,b and set
//
//                  N = M - {ax,by} + {ab}.
//
// Then N is a near-perfect matching containing both roots.  The test
// succeeds exactly when some such N has bridgeless complement.  This is
// strictly more restrictive than the full focused-theta census.

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
  std::vector<std::vector<std::pair<int, int>>> adj;
};

static Graph parse_graph6(const std::string& text, int expected_order) {
  if (text.empty() || static_cast<unsigned char>(text[0]) >= 126) {
    throw std::runtime_error("expected short graph6");
  }
  Graph g;
  g.n = static_cast<unsigned char>(text[0]) - 63;
  if (g.n != expected_order) {
    throw std::runtime_error("graph6 order mismatch");
  }
  std::vector<int> bits;
  for (std::size_t i = 1; i < text.size(); ++i) {
    const int value = static_cast<unsigned char>(text[i]) - 63;
    if (value < 0 || value >= 64) {
      throw std::runtime_error("bad graph6 byte");
    }
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }
  std::size_t cursor = 0;
  for (int high = 1; high < g.n; ++high) {
    for (int low = 0; low < high; ++low) {
      if (cursor >= bits.size()) {
        throw std::runtime_error("truncated graph6");
      }
      if (bits[cursor++]) {
        g.edges.emplace_back(low, high);
      }
    }
  }
  if (static_cast<int>(g.edges.size()) * 2 != 3 * g.n) {
    throw std::runtime_error("not cubic-size");
  }
  g.adj.assign(g.n, {});
  for (int edge = 0; edge < static_cast<int>(g.edges.size()); ++edge) {
    const auto [u, v] = g.edges[edge];
    g.adj[u].emplace_back(v, edge);
    g.adj[v].emplace_back(u, edge);
  }
  for (const auto& row : g.adj) {
    if (row.size() != 3) {
      throw std::runtime_error("not simple cubic");
    }
  }
  return g;
}

class LocalInsertionTest {
 public:
  explicit LocalInsertionTest(const Graph& graph)
      : g_(graph),
        all_((uint32_t{1} << graph.n) - 1),
        chosen_(graph.edges.size(), false) {
    perfect_[0] = true;
  }

  bool has_perfect(uint32_t vertices) {
    const auto known = perfect_.find(vertices);
    if (known != perfect_.end()) {
      return known->second;
    }
    if (__builtin_popcount(vertices) & 1) {
      return perfect_[vertices] = false;
    }
    int vertex = -1;
    int degree = 4;
    for (int v = 0; v < g_.n; ++v) {
      if (!((vertices >> v) & 1U)) {
        continue;
      }
      int local = 0;
      for (const auto [w, edge] : g_.adj[v]) {
        (void)edge;
        local += (vertices >> w) & 1U;
      }
      if (local < degree) {
        degree = local;
        vertex = v;
      }
    }
    if (vertex < 0 || degree == 0) {
      return perfect_[vertices] = false;
    }
    const uint32_t rest = vertices & ~(uint32_t{1} << vertex);
    for (const auto [w, edge] : g_.adj[vertex]) {
      (void)edge;
      if (((rest >> w) & 1U) &&
          has_perfect(rest & ~(uint32_t{1} << w))) {
        return perfect_[vertices] = true;
      }
    }
    return perfect_[vertices] = false;
  }

  bool pair_has_local_witness(int first, int second) {
    return orientation_has_witness(first, second) ||
           orientation_has_witness(second, first);
  }

 private:
  const Graph& g_;
  uint32_t all_;
  std::unordered_map<uint32_t, bool> perfect_;
  std::vector<bool> chosen_;
  int inserted_ = -1;
  int removed_first_ = -1;
  int removed_second_ = -1;

  bool orientation_has_witness(int kept, int inserted) {
    const auto [p, q] = g_.edges[kept];
    const auto [a, b] = g_.edges[inserted];
    if (p == a || p == b || q == a || q == b) {
      throw std::runtime_error("roots are not independent");
    }
    for (const auto [x, ax] : g_.adj[a]) {
      if (ax == inserted) {
        continue;
      }
      for (const auto [y, by] : g_.adj[b]) {
        if (by == inserted || x == y) {
          continue;
        }
        const uint32_t covered =
            (uint32_t{1} << p) | (uint32_t{1} << q) |
            (uint32_t{1} << a) | (uint32_t{1} << b) |
            (uint32_t{1} << x) | (uint32_t{1} << y);
        if (__builtin_popcount(covered) != 6) {
          continue;
        }
        const uint32_t remaining = all_ & ~covered;
        if (!has_perfect(remaining)) {
          continue;
        }
        chosen_[kept] = true;
        chosen_[ax] = true;
        chosen_[by] = true;
        inserted_ = inserted;
        removed_first_ = ax;
        removed_second_ = by;
        if (enumerate_completions(remaining)) {
          chosen_[kept] = false;
          chosen_[ax] = false;
          chosen_[by] = false;
          return true;
        }
        chosen_[kept] = false;
        chosen_[ax] = false;
        chosen_[by] = false;
      }
    }
    return false;
  }

  bool enumerate_completions(uint32_t vertices) {
    if (vertices == 0) {
      chosen_[removed_first_] = false;
      chosen_[removed_second_] = false;
      chosen_[inserted_] = true;
      const bool answer = complement_is_bridgeless();
      chosen_[inserted_] = false;
      chosen_[removed_first_] = true;
      chosen_[removed_second_] = true;
      return answer;
    }
    int vertex = -1;
    int degree = 4;
    for (int v = 0; v < g_.n; ++v) {
      if (!((vertices >> v) & 1U)) {
        continue;
      }
      int local = 0;
      for (const auto [w, edge] : g_.adj[v]) {
        (void)edge;
        local += (vertices >> w) & 1U;
      }
      if (local < degree) {
        degree = local;
        vertex = v;
      }
    }
    if (vertex < 0 || degree == 0) {
      return false;
    }
    const uint32_t rest = vertices & ~(uint32_t{1} << vertex);
    for (const auto [w, edge] : g_.adj[vertex]) {
      if (!((rest >> w) & 1U)) {
        continue;
      }
      const uint32_t reduced = rest & ~(uint32_t{1} << w);
      if (!has_perfect(reduced)) {
        continue;
      }
      chosen_[edge] = true;
      if (enumerate_completions(reduced)) {
        chosen_[edge] = false;
        return true;
      }
      chosen_[edge] = false;
    }
    return false;
  }

  bool complement_is_bridgeless() const {
    std::vector<int> discovery(g_.n, -1);
    std::vector<int> low(g_.n, -1);
    int timer = 0;
    bool bridge = false;
    const auto visit = [&](const auto& self, int vertex,
                           int parent_edge) -> void {
      discovery[vertex] = low[vertex] = timer++;
      for (const auto [w, edge] : g_.adj[vertex]) {
        if (chosen_[edge] || edge == parent_edge) {
          continue;
        }
        if (discovery[w] < 0) {
          self(self, w, edge);
          low[vertex] = std::min(low[vertex], low[w]);
          if (low[w] > discovery[vertex]) {
            bridge = true;
          }
        } else {
          low[vertex] = std::min(low[vertex], discovery[w]);
        }
      }
    };
    for (int v = 0; v < g_.n; ++v) {
      if (discovery[v] < 0) {
        visit(visit, v, -1);
      }
    }
    return !bridge;
  }
};

int main(int argc, char** argv) {
  if (argc != 3) {
    std::cerr << "usage: focused-local-insertion-census ORDER CORPUS.g6\n";
    return 2;
  }
  const int order = std::stoi(argv[1]);
  std::ifstream input(argv[2]);
  if (!input) {
    throw std::runtime_error("cannot open corpus");
  }
  uint64_t graphs = 0;
  uint64_t pairs = 0;
  uint64_t deficient = 0;
  uint64_t local = 0;
  uint64_t singleton = 0;
  uint64_t singleton_local = 0;
  std::string first_failure;
  std::string first_singleton_failure;
  std::string row;
  while (std::getline(input, row)) {
    if (row.empty()) {
      continue;
    }
    const Graph g = parse_graph6(row, order);
    LocalInsertionTest test(g);
    const uint32_t all = (uint32_t{1} << order) - 1;
    for (int first = 0; first < static_cast<int>(g.edges.size()); ++first) {
      const auto [a, b] = g.edges[first];
      for (int second = first + 1;
           second < static_cast<int>(g.edges.size()); ++second) {
        const auto [c, d] = g.edges[second];
        if (a == c || a == d || b == c || b == d) {
          continue;
        }
        ++pairs;
        const uint32_t roots =
            (uint32_t{1} << a) | (uint32_t{1} << b) |
            (uint32_t{1} << c) | (uint32_t{1} << d);
        if (test.has_perfect(all & ~roots)) {
          continue;
        }
        ++deficient;
        const bool local_witness =
            test.pair_has_local_witness(first, second);
        if (local_witness) {
          ++local;
        } else if (first_failure.empty()) {
          first_failure = std::to_string(graphs) + ":" +
                          std::to_string(first) + "," +
                          std::to_string(second) + ":" + row;
        }
        uint32_t d_set = 0;
        const uint32_t h_vertices = all & ~roots;
        for (int v = 0; v < order; ++v) {
          if (!((h_vertices >> v) & 1U)) {
            continue;
          }
          for (int w = v + 1; w < order; ++w) {
            if (!((h_vertices >> w) & 1U)) {
              continue;
            }
            const uint32_t remainder =
                h_vertices & ~(uint32_t{1} << v) &
                ~(uint32_t{1} << w);
            if (test.has_perfect(remainder)) {
              d_set |= (uint32_t{1} << v);
              d_set |= (uint32_t{1} << w);
            }
          }
        }
        uint32_t a_set = 0;
        bool d_independent = true;
        for (const auto [u, v] : g.edges) {
          const bool u_in_d = (d_set >> u) & 1U;
          const bool v_in_d = (d_set >> v) & 1U;
          if (u_in_d && v_in_d) {
            d_independent = false;
          } else if (u_in_d && ((h_vertices >> v) & 1U)) {
            a_set |= uint32_t{1} << v;
          } else if (v_in_d && ((h_vertices >> u) & 1U)) {
            a_set |= uint32_t{1} << u;
          }
        }
        a_set &= ~d_set;
        const uint32_t c_set = h_vertices & ~d_set & ~a_set;
        if (d_independent && c_set == 0) {
          ++singleton;
          if (local_witness) {
            ++singleton_local;
          } else if (first_singleton_failure.empty()) {
            first_singleton_failure =
                std::to_string(graphs) + ":" +
                std::to_string(first) + "," +
                std::to_string(second) + ":" + row;
          }
        }
      }
    }
    ++graphs;
    if (graphs % 100 == 0) {
      std::cerr << "PROGRESS graphs=" << graphs
                << " deficient=" << deficient
                << " local=" << local
                << " singleton=" << singleton
                << " singleton_local=" << singleton_local
                << " failures=" << (deficient - local) << "\n";
    }
  }
  std::cout << "{\"order\":" << order
            << ",\"graphs\":" << graphs
            << ",\"pairs\":" << pairs
            << ",\"deficient\":" << deficient
            << ",\"local_witness\":" << local
            << ",\"local_failure\":" << (deficient - local)
            << ",\"singleton\":" << singleton
            << ",\"singleton_local_witness\":" << singleton_local
            << ",\"singleton_local_failure\":"
            << (singleton - singleton_local)
            << ",\"first_failure\":\"" << first_failure
            << "\",\"first_singleton_failure\":\""
            << first_singleton_failure << "\"}\n";
}
