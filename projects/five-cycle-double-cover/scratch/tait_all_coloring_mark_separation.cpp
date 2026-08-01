// Search connected simple cubic graph6 rows for edge matchings that remain
// separated in every proper 3-edge-colouring.
//
// A pair of edges conflicts if it is adjacent, or if some proper
// 3-edge-colouring puts both on one bichromatic circuit.  Thus an
// independent set of size s in the accumulated conflict graph is exactly
// an s-edge matching separated in every bichromatic circuit of every
// proper 3-edge-colouring.
//
// Build:
//   c++ -O3 -std=c++17 scratch/tait_all_coloring_mark_separation.cpp \
//       -o scratch/tait_all_coloring_mark_separation
//
// Example:
//   geng -cq -d3 -D3 18 27:27 |
//     scratch/tait_all_coloring_mark_separation --target 4

#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using std::array;
using std::bitset;
using std::cerr;
using std::cin;
using std::cout;
using std::pair;
using std::string;
using std::vector;

struct Graph {
  int n = 0;
  vector<pair<int, int>> edges;
  vector<vector<int>> incident;
};

static Graph parse_graph6(const string &row) {
  if (row.empty() || row[0] == ':' || row[0] == '>') {
    throw std::runtime_error("unsupported graph6 row");
  }
  vector<int> values;
  values.reserve(row.size());
  for (unsigned char byte : row) {
    const int value = static_cast<int>(byte) - 63;
    if (value < 0 || value > 63) {
      throw std::runtime_error("invalid graph6 byte");
    }
    values.push_back(value);
  }
  int n = 0;
  int header_length = 0;
  if (values[0] <= 62) {
    n = values[0];
    header_length = 1;
  } else if (values.size() >= 4 && values[1] <= 62) {
    n = (values[1] << 12) | (values[2] << 6) | values[3];
    header_length = 4;
  } else if (values.size() >= 8 && values[1] == 63) {
    const uint64_t wide_order =
        (static_cast<uint64_t>(values[2]) << 30) |
        (static_cast<uint64_t>(values[3]) << 24) |
        (static_cast<uint64_t>(values[4]) << 18) |
        (static_cast<uint64_t>(values[5]) << 12) |
        (static_cast<uint64_t>(values[6]) << 6) |
        static_cast<uint64_t>(values[7]);
    if (wide_order > static_cast<uint64_t>(std::numeric_limits<int>::max())) {
      throw std::runtime_error("graph order exceeds implementation limit");
    }
    n = static_cast<int>(wide_order);
    header_length = 8;
  } else {
    throw std::runtime_error("truncated graph6 header");
  }
  Graph g;
  g.n = n;
  g.incident.assign(n, {});
  int bit_index = 0;
  for (int v = 1; v < n; ++v) {
    for (int u = 0; u < v; ++u, ++bit_index) {
      const int byte_index = header_length + bit_index / 6;
      if (byte_index >= static_cast<int>(row.size())) {
        throw std::runtime_error("truncated graph6 row");
      }
      const int value = values[byte_index];
      const int bit = (value >> (5 - bit_index % 6)) & 1;
      if (bit) {
        const int e = static_cast<int>(g.edges.size());
        g.edges.push_back({u, v});
        g.incident[u].push_back(e);
        g.incident[v].push_back(e);
      }
    }
  }
  return g;
}

struct ColouringSearch {
  static constexpr int kMaximumEdges = 128;
  const Graph &g;
  const int m;
  vector<int> colour;
  vector<unsigned> used;
  vector<bitset<kMaximumEdges>> conflict;
  vector<char> required;
  bool required_conflict = false;
  bool track_one_extension = false;
  bool track_ten_factor_profiles = false;
  bitset<kMaximumEdges> possible_extension;
  bool no_required_extension = false;
  uint64_t colourings = 0;
  uint64_t colourings_with_two_ten_factors = 0;
  uint64_t colourings_with_three_ten_factors = 0;

  explicit ColouringSearch(const Graph &graph,
                           const vector<int> &required_edges = {},
                           bool track_single_extension = false,
                           bool track_ten_factors = false)
      : g(graph), m(static_cast<int>(graph.edges.size())),
        colour(m, -1), used(graph.n, 0), conflict(m, 0),
        required(m, 0), track_one_extension(track_single_extension),
        track_ten_factor_profiles(track_ten_factors) {
    if (m > kMaximumEdges) {
      throw std::runtime_error("at most 128 edges are supported");
    }
    for (int e = 0; e < m; ++e) {
      const auto [u, v] = g.edges[e];
      for (int f : g.incident[u]) {
        if (f != e) conflict[e].set(f);
      }
      for (int f : g.incident[v]) {
        if (f != e) conflict[e].set(f);
      }
    }
    for (int e : required_edges) required[e] = 1;
    for (int e : required_edges) {
      for (int f : required_edges) {
        if (e != f && conflict[e].test(f)) required_conflict = true;
      }
    }
    if (track_one_extension) {
      for (int e = 0; e < m; ++e) {
        if (required[e]) continue;
        bool okay = true;
        for (int f : required_edges) okay &= !conflict[e].test(f);
        if (okay) possible_extension.set(e);
      }
      no_required_extension = possible_extension.none();
    }
  }

  bool assign(int e, int c) {
    if (colour[e] != -1) return colour[e] == c;
    const auto [u, v] = g.edges[e];
    const unsigned bit = 1U << c;
    if ((used[u] & bit) || (used[v] & bit)) return false;
    colour[e] = c;
    used[u] |= bit;
    used[v] |= bit;
    return true;
  }

  void unassign(int e, int c) {
    const auto [u, v] = g.edges[e];
    colour[e] = -1;
    used[u] &= ~(1U << c);
    used[v] &= ~(1U << c);
  }

  void record() {
    ++colourings;
    array<bool, 3> ten_factor = {true, true, true};
    for (int omitted = 0; omitted < 3; ++omitted) {
      vector<char> seen_edge(m, 0);
      for (int start = 0; start < m; ++start) {
        if (colour[start] == omitted || seen_edge[start]) continue;
        vector<int> component;
        vector<int> stack = {start};
        seen_edge[start] = 1;
        while (!stack.empty()) {
          const int e = stack.back();
          stack.pop_back();
          component.push_back(e);
          const auto [u, v] = g.edges[e];
          for (int x : {u, v}) {
            for (int f : g.incident[x]) {
              if (colour[f] != omitted && !seen_edge[f]) {
                seen_edge[f] = 1;
                stack.push_back(f);
              }
            }
          }
        }
        if (component.size() != 10) ten_factor[omitted] = false;
        bitset<kMaximumEdges> mask;
        for (int e : component) mask.set(e);
        int required_count = 0;
        for (int e : component) required_count += required[e];
        if (required_count > 1) required_conflict = true;
        if (track_one_extension && required_count == 1) {
          possible_extension &= ~mask;
          no_required_extension = possible_extension.none();
        }
        for (int e : component) {
          conflict[e] |= mask;
          conflict[e].reset(e);
        }
      }
    }
    if (track_ten_factor_profiles) {
      const int count =
          static_cast<int>(ten_factor[0]) +
          static_cast<int>(ten_factor[1]) +
          static_cast<int>(ten_factor[2]);
      if (count >= 2) ++colourings_with_two_ten_factors;
      if (count == 3) ++colourings_with_three_ten_factors;
    }
  }

  void recurse(int assigned) {
    if (required_conflict || no_required_extension) return;
    if (assigned == m) {
      record();
      return;
    }
    int best = -1;
    unsigned best_allowed = 0;
    int best_count = 4;
    for (int e = 0; e < m; ++e) {
      if (colour[e] != -1) continue;
      const auto [u, v] = g.edges[e];
      const unsigned allowed = 7U & ~(used[u] | used[v]);
      const int count = __builtin_popcount(allowed);
      if (count == 0) return;
      if (count < best_count) {
        best = e;
        best_allowed = allowed;
        best_count = count;
        if (count == 1) break;
      }
    }
    for (int c = 0; c < 3; ++c) {
      if (!(best_allowed & (1U << c))) continue;
      if (assign(best, c)) {
        recurse(assigned + 1);
        unassign(best, c);
        if (required_conflict || no_required_extension) return;
      }
    }
  }

  void run_modulo_global_colour_permutation() {
    if (g.n == 0 || g.incident[0].size() != 3) return;
    // Each labelled colouring has a unique global colour permutation for
    // which the three edge objects at vertex 0 receive 0,1,2 in this order.
    int assigned = 0;
    for (int c = 0; c < 3; ++c) {
      const int e = g.incident[0][c];
      if (!assign(e, c)) return;
      ++assigned;
    }
    recurse(assigned);
  }
};

static bool independent_extension(
                                  const vector<bitset<ColouringSearch::kMaximumEdges>>
                                      &conflict,
                                  int target, int next,
                                  vector<int> &chosen) {
  if (static_cast<int>(chosen.size()) == target) return true;
  const int m = static_cast<int>(conflict.size());
  const int need = target - static_cast<int>(chosen.size());
  for (int e = next; e + need <= m; ++e) {
    if (std::find(chosen.begin(), chosen.end(), e) != chosen.end()) continue;
    bool okay = true;
    for (int f : chosen) {
      if (conflict[e].test(f)) {
        okay = false;
        break;
      }
    }
    if (!okay) continue;
    chosen.push_back(e);
    if (independent_extension(conflict, target, e + 1, chosen)) return true;
    chosen.pop_back();
  }
  return false;
}

static int subdivided_girth(const Graph &g, const vector<int> &marks) {
  vector<int> mark_position(g.edges.size(), -1);
  for (int i = 0; i < static_cast<int>(marks.size()); ++i) {
    mark_position[marks[i]] = i;
  }
  const int order = g.n + static_cast<int>(marks.size());
  vector<vector<int>> adjacency(order);
  for (int e = 0; e < static_cast<int>(g.edges.size()); ++e) {
    const auto [u, v] = g.edges[e];
    if (mark_position[e] == -1) {
      adjacency[u].push_back(v);
      adjacency[v].push_back(u);
    } else {
      const int w = g.n + mark_position[e];
      adjacency[u].push_back(w);
      adjacency[w].push_back(u);
      adjacency[v].push_back(w);
      adjacency[w].push_back(v);
    }
  }
  int answer = order + 1;
  for (int root = 0; root < order; ++root) {
    vector<int> distance(order, -1);
    vector<int> parent(order, -1);
    vector<int> queue = {root};
    distance[root] = 0;
    for (int head = 0; head < static_cast<int>(queue.size()); ++head) {
      const int v = queue[head];
      for (int w : adjacency[v]) {
        if (distance[w] == -1) {
          distance[w] = distance[v] + 1;
          parent[w] = v;
          queue.push_back(w);
        } else if (parent[v] != w) {
          answer = std::min(answer, distance[v] + distance[w] + 1);
        }
      }
    }
  }
  return answer;
}

static bool packs_even_marked_circuits(
    const Graph &g, const vector<int> &marks) {
  using EdgeMask = bitset<ColouringSearch::kMaximumEdges>;
  const int m = static_cast<int>(g.edges.size());
  vector<int> parent(g.n, -1);
  vector<int> parent_edge(g.n, -1);
  vector<int> depth(g.n, 0);
  vector<char> tree_edge(m, 0);
  vector<int> queue = {0};
  parent[0] = 0;
  for (int head = 0; head < static_cast<int>(queue.size()); ++head) {
    const int v = queue[head];
    for (int e : g.incident[v]) {
      const auto [x, y] = g.edges[e];
      const int w = x ^ y ^ v;
      if (parent[w] == -1) {
        parent[w] = v;
        parent_edge[w] = e;
        depth[w] = depth[v] + 1;
        tree_edge[e] = 1;
        queue.push_back(w);
      }
    }
  }
  if (static_cast<int>(queue.size()) != g.n) return false;
  vector<EdgeMask> basis;
  for (int e = 0; e < m; ++e) {
    if (tree_edge[e]) continue;
    auto [u, v] = g.edges[e];
    EdgeMask cycle;
    cycle.set(e);
    while (depth[u] > depth[v]) {
      cycle.flip(parent_edge[u]);
      u = parent[u];
    }
    while (depth[v] > depth[u]) {
      cycle.flip(parent_edge[v]);
      v = parent[v];
    }
    while (u != v) {
      cycle.flip(parent_edge[u]);
      cycle.flip(parent_edge[v]);
      u = parent[u];
      v = parent[v];
    }
    basis.push_back(cycle);
  }
  EdgeMask mark_mask;
  for (int e : marks) mark_mask.set(e);
  const int dimension = static_cast<int>(basis.size());
  if (dimension >= 63) {
    throw std::runtime_error("cycle-space enumeration overflow");
  }
  vector<uint64_t> equations;
  for (int e : marks) {
    uint64_t row = uint64_t{1} << dimension;
    for (int i = 0; i < dimension; ++i) {
      if (basis[i].test(e)) row |= uint64_t{1} << i;
    }
    equations.push_back(row);
  }
  vector<int> pivot_columns;
  int rank = 0;
  for (int column = 0; column < dimension; ++column) {
    int pivot = -1;
    for (int row = rank; row < static_cast<int>(equations.size()); ++row) {
      if ((equations[row] >> column) & 1U) {
        pivot = row;
        break;
      }
    }
    if (pivot == -1) continue;
    std::swap(equations[rank], equations[pivot]);
    for (int row = 0; row < static_cast<int>(equations.size()); ++row) {
      if (row != rank && ((equations[row] >> column) & 1U)) {
        equations[row] ^= equations[rank];
      }
    }
    pivot_columns.push_back(column);
    ++rank;
  }
  const uint64_t variable_mask =
      dimension == 64 ? ~uint64_t{0} : ((uint64_t{1} << dimension) - 1);
  for (uint64_t row : equations) {
    if (!(row & variable_mask) && ((row >> dimension) & 1U)) return false;
  }
  vector<char> is_pivot(dimension, 0);
  uint64_t particular_coefficients = 0;
  for (int row = 0; row < rank; ++row) {
    const int pivot = pivot_columns[row];
    is_pivot[pivot] = 1;
    if ((equations[row] >> dimension) & 1U) {
      particular_coefficients |= uint64_t{1} << pivot;
    }
  }
  vector<uint64_t> null_coefficients;
  for (int free_column = 0; free_column < dimension; ++free_column) {
    if (is_pivot[free_column]) continue;
    uint64_t vector = uint64_t{1} << free_column;
    for (int row = 0; row < rank; ++row) {
      if ((equations[row] >> free_column) & 1U) {
        vector |= uint64_t{1} << pivot_columns[row];
      }
    }
    null_coefficients.push_back(vector);
  }
  auto edge_cycle = [&](uint64_t coefficients) {
    EdgeMask cycle;
    for (int i = 0; i < dimension; ++i) {
      if ((coefficients >> i) & 1U) cycle ^= basis[i];
    }
    return cycle;
  };
  const EdgeMask particular_cycle = edge_cycle(particular_coefficients);
  vector<EdgeMask> null_cycles;
  for (uint64_t coefficients : null_coefficients) {
    null_cycles.push_back(edge_cycle(coefficients));
  }
  const uint64_t combinations = uint64_t{1} << null_cycles.size();
  for (uint64_t choice = 0; choice < combinations; ++choice) {
    EdgeMask cycle = particular_cycle;
    for (int i = 0; i < static_cast<int>(null_cycles.size()); ++i) {
      if ((choice >> i) & 1U) cycle ^= null_cycles[i];
    }
    if ((cycle & mark_mask) != mark_mask) {
      throw std::runtime_error("affine marked-cycle solve failed");
    }
    vector<int> component(g.n, -1);
    int component_count = 0;
    for (int root = 0; root < g.n; ++root) {
      bool active = false;
      for (int e : g.incident[root]) active |= cycle.test(e);
      if (!active || component[root] != -1) continue;
      vector<int> stack = {root};
      component[root] = component_count;
      while (!stack.empty()) {
        const int v = stack.back();
        stack.pop_back();
        for (int e : g.incident[v]) {
          if (!cycle.test(e)) continue;
          const auto [x, y] = g.edges[e];
          const int w = x ^ y ^ v;
          if (component[w] == -1) {
            component[w] = component_count;
            stack.push_back(w);
          }
        }
      }
      ++component_count;
    }
    vector<int> mark_count(component_count, 0);
    for (int e : marks) {
      const auto [u, v] = g.edges[e];
      if (component[u] == -1 || component[u] != component[v]) {
        throw std::runtime_error("selected marked cycle is malformed");
      }
      ++mark_count[component[u]];
    }
    bool even = true;
    for (int count : mark_count) even &= count % 2 == 0;
    if (even) return true;
  }
  return false;
}

// If H is a suppressed core from one component of G-M, lifting a connected
// cyclic shore X of H back to G gives a cut with one extra matching edge
// for every marked edge wholly inside X.  Cyclic 4-edge-connectivity of G
// therefore forces
//
//   |delta_H(X)| + |marks contained in H[X]| >= 4.
//
// A violating connected shore has boundary at most three.  It appears as a
// connected component after deleting some set of at most three edges, so
// the finite check below is exact.  Repeated shores are harmless.
static bool satisfies_marked_cyclic_four(
    const Graph &g, const vector<int> &marks) {
  const int m = static_cast<int>(g.edges.size());
  vector<char> marked(m, 0);
  for (int e : marks) marked[e] = 1;

  auto inspect_removed = [&](const array<int, 3> &skip, int skip_count) {
    vector<int> component(g.n, -1);
    int component_count = 0;
    for (int root = 0; root < g.n; ++root) {
      if (component[root] != -1) continue;
      vector<int> stack = {root};
      component[root] = component_count;
      while (!stack.empty()) {
        const int v = stack.back();
        stack.pop_back();
        for (int e : g.incident[v]) {
          bool removed = false;
          for (int i = 0; i < skip_count; ++i) removed |= e == skip[i];
          if (removed) continue;
          const auto [x, y] = g.edges[e];
          const int w = x ^ y ^ v;
          if (component[w] == -1) {
            component[w] = component_count;
            stack.push_back(w);
          }
        }
      }
      ++component_count;
    }
    if (component_count == 1) return true;

    vector<int> vertices(component_count, 0);
    vector<int> internal_edges(component_count, 0);
    vector<int> internal_marks(component_count, 0);
    vector<int> boundary(component_count, 0);
    for (int v = 0; v < g.n; ++v) ++vertices[component[v]];
    for (int e = 0; e < m; ++e) {
      const auto [u, v] = g.edges[e];
      if (component[u] == component[v]) {
        ++internal_edges[component[u]];
        if (marked[e]) ++internal_marks[component[u]];
      } else {
        ++boundary[component[u]];
        ++boundary[component[v]];
      }
    }
    for (int i = 0; i < component_count; ++i) {
      const bool cyclic = internal_edges[i] >= vertices[i];
      if (cyclic && boundary[i] + internal_marks[i] < 4) return false;
    }
    return true;
  };

  array<int, 3> skip = {-1, -1, -1};
  for (int e = 0; e < m; ++e) {
    skip[0] = e;
    if (!inspect_removed(skip, 1)) return false;
  }
  for (int e = 0; e < m; ++e) {
    for (int f = e + 1; f < m; ++f) {
      skip[0] = e;
      skip[1] = f;
      if (!inspect_removed(skip, 2)) return false;
    }
  }
  for (int e = 0; e < m; ++e) {
    for (int f = e + 1; f < m; ++f) {
      for (int h = f + 1; h < m; ++h) {
        skip[0] = e;
        skip[1] = f;
        skip[2] = h;
        if (!inspect_removed(skip, 3)) return false;
      }
    }
  }
  return true;
}

static bool independent_extension_filtered(
    const vector<bitset<ColouringSearch::kMaximumEdges>> &conflict,
    int target, int next,
    vector<int> &chosen, const Graph &g, int minimum_girth,
    bool require_nonpacking, bool require_marked_cyclic_four) {
  if (static_cast<int>(chosen.size()) == target) {
    if (minimum_girth && subdivided_girth(g, chosen) < minimum_girth) {
      return false;
    }
    if (require_nonpacking && packs_even_marked_circuits(g, chosen)) {
      return false;
    }
    if (require_marked_cyclic_four &&
        !satisfies_marked_cyclic_four(g, chosen)) {
      return false;
    }
    return true;
  }
  const int m = static_cast<int>(conflict.size());
  const int need = target - static_cast<int>(chosen.size());
  for (int e = next; e + need <= m; ++e) {
    bool okay = true;
    for (int f : chosen) {
      if (conflict[e].test(f)) {
        okay = false;
        break;
      }
    }
    if (!okay) continue;
    chosen.push_back(e);
    if (independent_extension_filtered(
            conflict, target, e + 1, chosen, g, minimum_girth,
            require_nonpacking, require_marked_cyclic_four)) {
      return true;
    }
    chosen.pop_back();
  }
  return false;
}

static bool has_edge_cut_below_three(const Graph &g) {
  const int m = static_cast<int>(g.edges.size());
  auto disconnected = [&](int skip_a, int skip_b) {
    vector<char> seen(g.n, 0);
    vector<int> stack = {0};
    seen[0] = 1;
    while (!stack.empty()) {
      const int v = stack.back();
      stack.pop_back();
      for (int e : g.incident[v]) {
        if (e == skip_a || e == skip_b) continue;
        const auto [x, y] = g.edges[e];
        const int w = x ^ y ^ v;
        if (!seen[w]) {
          seen[w] = 1;
          stack.push_back(w);
        }
      }
    }
    return std::find(seen.begin(), seen.end(), 0) != seen.end();
  };
  for (int e = 0; e < m; ++e) {
    if (disconnected(e, -1)) return true;
  }
  for (int e = 0; e < m; ++e) {
    for (int f = e + 1; f < m; ++f) {
      if (disconnected(e, f)) return true;
    }
  }
  return false;
}

static bool has_cyclic_cut_below_four(const Graph &g) {
  const int m = static_cast<int>(g.edges.size());
  auto cyclic_cut = [&](const array<int, 3> &skip, int skip_count) {
    vector<int> component(g.n, -1);
    int component_count = 0;
    for (int root = 0; root < g.n; ++root) {
      if (component[root] != -1) continue;
      vector<int> stack = {root};
      component[root] = component_count;
      while (!stack.empty()) {
        const int v = stack.back();
        stack.pop_back();
        for (int e : g.incident[v]) {
          bool removed = false;
          for (int i = 0; i < skip_count; ++i) removed |= e == skip[i];
          if (removed) continue;
          const auto [x, y] = g.edges[e];
          const int w = x ^ y ^ v;
          if (component[w] == -1) {
            component[w] = component_count;
            stack.push_back(w);
          }
        }
      }
      ++component_count;
    }
    if (component_count == 1) return false;
    vector<int> vertices(component_count, 0);
    vector<int> edges(component_count, 0);
    for (int v = 0; v < g.n; ++v) ++vertices[component[v]];
    for (int e = 0; e < m; ++e) {
      bool removed = false;
      for (int i = 0; i < skip_count; ++i) removed |= e == skip[i];
      if (removed) continue;
      const auto [u, v] = g.edges[e];
      if (component[u] == component[v]) ++edges[component[u]];
    }
    int cyclic_components = 0;
    for (int i = 0; i < component_count; ++i) {
      cyclic_components += edges[i] >= vertices[i];
    }
    return cyclic_components >= 2;
  };
  array<int, 3> skip = {-1, -1, -1};
  for (int e = 0; e < m; ++e) {
    skip[0] = e;
    if (cyclic_cut(skip, 1)) return true;
  }
  for (int e = 0; e < m; ++e) {
    for (int f = e + 1; f < m; ++f) {
      skip[0] = e;
      skip[1] = f;
      if (cyclic_cut(skip, 2)) return true;
    }
  }
  for (int e = 0; e < m; ++e) {
    for (int f = e + 1; f < m; ++f) {
      for (int h = f + 1; h < m; ++h) {
        skip[0] = e;
        skip[1] = f;
        skip[2] = h;
        if (cyclic_cut(skip, 3)) return true;
      }
    }
  }
  return false;
}

int main(int argc, char **argv) {
  int target = 4;
  uint64_t limit = 0;
  uint64_t progress = 1000;
  bool require_edge_three = false;
  bool require_cyclic_four = false;
  int minimum_subdivided_girth = 0;
  bool require_nonpacking = false;
  bool require_marked_cyclic_four = false;
  bool stop_after_first = false;
  bool report_ten_factor_profiles = false;
  vector<pair<int, int>> required_edge_ends;
  for (int i = 1; i < argc; ++i) {
    const string arg = argv[i];
    if (arg == "--target" && i + 1 < argc) {
      target = std::atoi(argv[++i]);
    } else if (arg == "--limit" && i + 1 < argc) {
      limit = std::strtoull(argv[++i], nullptr, 10);
    } else if (arg == "--progress" && i + 1 < argc) {
      progress = std::strtoull(argv[++i], nullptr, 10);
    } else if (arg == "--min-edge-connectivity" && i + 1 < argc) {
      require_edge_three = std::atoi(argv[++i]) >= 3;
    } else if (arg == "--cyclic-edge-connectivity" && i + 1 < argc) {
      require_cyclic_four = std::atoi(argv[++i]) >= 4;
    } else if (arg == "--min-subdivided-girth" && i + 1 < argc) {
      minimum_subdivided_girth = std::atoi(argv[++i]);
    } else if (arg == "--require-nonpacking") {
      require_nonpacking = true;
    } else if (arg == "--marked-cyclic-connectivity" && i + 1 < argc) {
      require_marked_cyclic_four = std::atoi(argv[++i]) >= 4;
    } else if (arg == "--stop-after-first") {
      stop_after_first = true;
    } else if (arg == "--report-ten-factor-profiles") {
      report_ten_factor_profiles = true;
    } else if (arg == "--required-edge-ends" && i + 1 < argc) {
      std::stringstream entries(argv[++i]);
      string entry;
      while (std::getline(entries, entry, ',')) {
        const auto dash = entry.find('-');
        if (dash == string::npos) {
          cerr << "bad required edge endpoint pair: " << entry << "\n";
          return 2;
        }
        int u = std::atoi(entry.substr(0, dash).c_str());
        int v = std::atoi(entry.substr(dash + 1).c_str());
        if (u > v) std::swap(u, v);
        required_edge_ends.push_back({u, v});
      }
    } else {
      cerr << "usage: " << argv[0]
           << " [--target s] [--limit graph_rows]"
              " [--progress row_interval]"
              " [--min-edge-connectivity 3]"
              " [--cyclic-edge-connectivity 4]"
              " [--min-subdivided-girth g]"
              " [--require-nonpacking]"
              " [--marked-cyclic-connectivity 4]"
              " [--required-edge-ends u-v,x-y,...]"
              " [--report-ten-factor-profiles]"
              " [--stop-after-first]\n";
      return 2;
    }
  }

  string row;
  uint64_t rows = 0;
  uint64_t tait = 0;
  uint64_t witnesses = 0;
  uint64_t total_colourings = 0;
  uint64_t total_colourings_with_two_ten_factors = 0;
  uint64_t total_colourings_with_three_ten_factors = 0;
  while (std::getline(cin, row)) {
    if (row.empty() || row.rfind(">>", 0) == 0) continue;
    if (limit && rows >= limit) break;
    ++rows;
    Graph g;
    try {
      g = parse_graph6(row);
    } catch (const std::exception &error) {
      cerr << "parse error at row " << rows << ": " << error.what() << "\n";
      return 2;
    }
    bool cubic = true;
    for (const auto &inc : g.incident) cubic &= inc.size() == 3;
    if (!cubic) {
      cerr << "noncubic row " << rows << "\n";
      return 2;
    }
    vector<int> required_edges;
    bool required_present = true;
    for (const auto &required_end : required_edge_ends) {
      auto found = std::find(g.edges.begin(), g.edges.end(), required_end);
      if (found == g.edges.end()) {
        required_present = false;
        break;
      }
      required_edges.push_back(
          static_cast<int>(std::distance(g.edges.begin(), found)));
    }
    if (!required_present) continue;
    ColouringSearch search(
        g, required_edges,
        !required_edges.empty() &&
            target == static_cast<int>(required_edges.size()) + 1,
        report_ten_factor_profiles);
    search.run_modulo_global_colour_permutation();
    total_colourings += search.colourings;
    total_colourings_with_two_ten_factors +=
        search.colourings_with_two_ten_factors;
    total_colourings_with_three_ten_factors +=
        search.colourings_with_three_ten_factors;
    if (search.colourings == 0 || search.required_conflict ||
        search.no_required_extension) {
      continue;
    }
    ++tait;
    vector<int> chosen = required_edges;
    const bool found =
        (minimum_subdivided_girth || require_nonpacking ||
         require_marked_cyclic_four)
            ? independent_extension_filtered(
                  search.conflict, target, 0, chosen, g,
                  minimum_subdivided_girth, require_nonpacking,
                  require_marked_cyclic_four)
            : independent_extension(search.conflict, target, 0, chosen);
    if (found) {
      if (require_edge_three && has_edge_cut_below_three(g)) continue;
      if (require_cyclic_four && has_cyclic_cut_below_four(g)) continue;
      ++witnesses;
      cout << "{\"row\":" << rows << ",\"graph6\":\"" << row
           << "\",\"order\":" << g.n
           << ",\"colourings_mod_s3\":" << search.colourings
           << ",\"marks\":[";
      for (int i = 0; i < target; ++i) {
        if (i) cout << ",";
        cout << chosen[i];
      }
      cout << "],\"mark_edges\":[";
      for (int i = 0; i < target; ++i) {
        if (i) cout << ",";
        const auto [u, v] = g.edges[chosen[i]];
        cout << "[" << u << "," << v << "]";
      }
      cout << "]}\n";
      if (stop_after_first) {
        cerr << "STOP rows=" << rows << " tait=" << tait
             << " colourings=" << total_colourings
             << " witnesses=" << witnesses << " target=" << target << "\n";
        return 0;
      }
    }
    if (progress && rows % progress == 0) {
      cerr << "rows=" << rows << " tait=" << tait
           << " colourings=" << total_colourings
           << " witnesses=" << witnesses << "\n";
    }
  }
  cerr << "FINAL rows=" << rows << " tait=" << tait
       << " colourings=" << total_colourings
       << " witnesses=" << witnesses << " target=" << target;
  if (report_ten_factor_profiles) {
    cerr << " colourings_with_at_least_two_C10_factors="
         << total_colourings_with_two_ten_factors
         << " colourings_with_three_C10_factors="
         << total_colourings_with_three_ten_factors;
  }
  cerr << "\n";
  return 0;
}
