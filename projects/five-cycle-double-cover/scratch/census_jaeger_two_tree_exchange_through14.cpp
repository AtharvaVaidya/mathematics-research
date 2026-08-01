// Exact census of coordinated two-tree escape from every obstructed literal
// Jaeger tree triple in connected simple bridgeless cubic graphs through
// order 14.
//
// The flow/potential classification is computed directly for every graph;
// it does not reuse the frozen 12-vertex all-flow report.

#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace {

constexpr int MAX_N = 14;
constexpr int MAX_M = 21;
std::ostream* OUTPUT = &std::cout;
bool REQUIRE_DIRECTION_THINNING = false;

struct Graph {
  int n = 0;
  std::vector<std::array<int, 2>> edges;
  std::vector<std::vector<int>> incidence;
  int m() const { return static_cast<int>(edges.size()); }
};

Graph parse_graph6(std::string record) {
  while (!record.empty() &&
         (record.back() == '\n' || record.back() == '\r')) {
    record.pop_back();
  }
  const std::string header = ">>graph6<<";
  if (record.rfind(header, 0) == 0) record.erase(0, header.size());
  if (record.empty() || record[0] == '~') {
    throw std::runtime_error("only short graph6 records are supported");
  }
  Graph graph;
  graph.n = static_cast<unsigned char>(record[0]) - 63;
  if (graph.n < 1 || graph.n > MAX_N) {
    throw std::runtime_error("graph order outside audit range");
  }
  const int bit_count = graph.n * (graph.n - 1) / 2;
  std::vector<int> bits;
  for (std::size_t i = 1; i < record.size(); ++i) {
    const int chunk = static_cast<unsigned char>(record[i]) - 63;
    if (chunk < 0 || chunk >= 64) throw std::runtime_error("bad graph6 byte");
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((chunk >> shift) & 1);
    }
  }
  if (static_cast<int>(bits.size()) < bit_count) {
    throw std::runtime_error("truncated graph6 record");
  }
  int cursor = 0;
  for (int v = 1; v < graph.n; ++v) {
    for (int u = 0; u < v; ++u) {
      if (bits[cursor]) graph.edges.push_back({u, v});
      ++cursor;
    }
  }
  if (graph.m() > MAX_M) throw std::runtime_error("too many edges");
  graph.incidence.assign(graph.n, {});
  for (int e = 0; e < graph.m(); ++e) {
    graph.incidence[graph.edges[e][0]].push_back(e);
    graph.incidence[graph.edges[e][1]].push_back(e);
  }
  return graph;
}

bool is_cubic_connected(const Graph& graph) {
  if (!std::all_of(
          graph.incidence.begin(), graph.incidence.end(),
          [](const auto& row) { return row.size() == 3; })) {
    return false;
  }
  std::vector<char> seen(graph.n, false);
  std::vector<int> queue{0};
  seen[0] = true;
  for (std::size_t q = 0; q < queue.size(); ++q) {
    const int vertex = queue[q];
    for (const int edge : graph.incidence[vertex]) {
      const int other =
          graph.edges[edge][0] ^ graph.edges[edge][1] ^ vertex;
      if (!seen[other]) {
        seen[other] = true;
        queue.push_back(other);
      }
    }
  }
  return std::all_of(seen.begin(), seen.end(), [](char x) { return x; });
}

bool is_bridgeless(const Graph& graph) {
  for (int removed = 0; removed < graph.m(); ++removed) {
    std::vector<char> seen(graph.n, false);
    std::vector<int> queue{0};
    seen[0] = true;
    for (std::size_t q = 0; q < queue.size(); ++q) {
      const int vertex = queue[q];
      for (const int edge : graph.incidence[vertex]) {
        if (edge == removed) continue;
        const int other =
            graph.edges[edge][0] ^ graph.edges[edge][1] ^ vertex;
        if (!seen[other]) {
          seen[other] = true;
          queue.push_back(other);
        }
      }
    }
    if (!std::all_of(seen.begin(), seen.end(), [](char x) { return x; })) {
      return false;
    }
  }
  return true;
}

struct Dsu {
  std::array<int, MAX_N> parent{};
  explicit Dsu(int n) { std::iota(parent.begin(), parent.begin() + n, 0); }
  int find(int x) {
    while (parent[x] != x) {
      parent[x] = parent[parent[x]];
      x = parent[x];
    }
    return x;
  }
};

bool is_forest(const Graph& graph, uint32_t mask) {
  Dsu dsu(graph.n);
  for (int e = 0; e < graph.m(); ++e) {
    if (!(mask & (uint32_t{1} << e))) continue;
    int a = dsu.find(graph.edges[e][0]);
    int b = dsu.find(graph.edges[e][1]);
    if (a == b) return false;
    dsu.parent[a] = b;
  }
  return true;
}

bool is_tree(const Graph& graph, uint32_t mask) {
  return __builtin_popcount(mask) == graph.n - 1 &&
         is_forest(graph, mask);
}

uint32_t fundamental_completion(const Graph& graph, uint32_t tree) {
  assert(is_tree(graph, tree));
  std::vector<std::vector<std::array<int, 2>>> adjacency(graph.n);
  for (int e = 0; e < graph.m(); ++e) {
    if (!(tree & (uint32_t{1} << e))) continue;
    const int a = graph.edges[e][0], b = graph.edges[e][1];
    adjacency[a].push_back({b, e});
    adjacency[b].push_back({a, e});
  }
  uint32_t answer = 0;
  for (int chord = 0; chord < graph.m(); ++chord) {
    if (tree & (uint32_t{1} << chord)) continue;
    const int start = graph.edges[chord][0];
    const int finish = graph.edges[chord][1];
    std::array<int, MAX_N> previous_vertex;
    std::array<int, MAX_N> previous_edge;
    previous_vertex.fill(-2);
    previous_edge.fill(-1);
    previous_vertex[start] = -1;
    std::vector<int> queue{start};
    for (std::size_t q = 0; q < queue.size(); ++q) {
      const int vertex = queue[q];
      if (vertex == finish) break;
      for (const auto row : adjacency[vertex]) {
        if (previous_vertex[row[0]] != -2) continue;
        previous_vertex[row[0]] = vertex;
        previous_edge[row[0]] = row[1];
        queue.push_back(row[0]);
      }
    }
    assert(previous_vertex[finish] != -2);
    uint32_t circuit = uint32_t{1} << chord;
    for (int vertex = finish; vertex != start;
         vertex = previous_vertex[vertex]) {
      circuit ^= uint32_t{1} << previous_edge[vertex];
    }
    answer ^= circuit;
  }
  return answer;
}

std::vector<uint32_t> binary_cycles(const Graph& graph) {
  uint32_t tree = 0;
  Dsu dsu(graph.n);
  for (int e = 0; e < graph.m(); ++e) {
    int a = dsu.find(graph.edges[e][0]);
    int b = dsu.find(graph.edges[e][1]);
    if (a == b) continue;
    dsu.parent[a] = b;
    tree |= uint32_t{1} << e;
  }
  assert(is_tree(graph, tree));
  std::vector<uint32_t> basis;
  for (int chord = 0; chord < graph.m(); ++chord) {
    if (tree & (uint32_t{1} << chord)) continue;
    // Rebuild the tree path; this avoids relying on any cycle-space library.
    std::vector<std::vector<std::array<int, 2>>> adjacency(graph.n);
    for (int e = 0; e < graph.m(); ++e) {
      if (!(tree & (uint32_t{1} << e))) continue;
      const int a = graph.edges[e][0], b = graph.edges[e][1];
      adjacency[a].push_back({b, e});
      adjacency[b].push_back({a, e});
    }
    const int start = graph.edges[chord][0];
    const int finish = graph.edges[chord][1];
    std::array<int, MAX_N> pv;
    std::array<int, MAX_N> pe;
    pv.fill(-2);
    pe.fill(-1);
    pv[start] = -1;
    std::vector<int> queue{start};
    for (std::size_t q = 0; q < queue.size(); ++q) {
      for (const auto row : adjacency[queue[q]]) {
        if (pv[row[0]] != -2) continue;
        pv[row[0]] = queue[q];
        pe[row[0]] = row[1];
        queue.push_back(row[0]);
      }
    }
    uint32_t circuit = uint32_t{1} << chord;
    for (int vertex = finish; vertex != start; vertex = pv[vertex]) {
      circuit ^= uint32_t{1} << pe[vertex];
    }
    assert(circuit & (uint32_t{1} << chord));
    basis.push_back(circuit);
  }
  const int dimension = graph.m() - graph.n + 1;
  assert(static_cast<int>(basis.size()) == dimension);
  std::vector<uint32_t> cycles(1 << dimension, 0);
  for (int word = 1; word < (1 << dimension); ++word) {
    const int bit = __builtin_ctz(word);
    cycles[word] = cycles[word ^ (1 << bit)] ^ basis[bit];
  }
  return cycles;
}

uint64_t encode_flow(
    const std::array<uint32_t, 3>& supports, int edge_count) {
  uint64_t code = 0;
  for (int e = 0; e < edge_count; ++e) {
    const uint64_t value =
        ((supports[0] >> e) & 1U) |
        (((supports[1] >> e) & 1U) << 1U) |
        (((supports[2] >> e) & 1U) << 2U);
    code |= value << (3 * e);
  }
  return code;
}

int flow_value(uint64_t flow, int edge) {
  return (flow >> (3 * edge)) & 7U;
}

uint64_t transform_flow(
    uint64_t flow, int edge_count, const std::array<int, 8>& table) {
  uint64_t answer = 0;
  for (int e = 0; e < edge_count; ++e) {
    answer |= uint64_t(table[flow_value(flow, e)]) << (3 * e);
  }
  return answer;
}

std::vector<std::array<int, 8>> gl3_tables() {
  std::vector<std::array<int, 8>> result;
  for (int a = 1; a < 8; ++a) {
    for (int b = 1; b < 8; ++b) {
      if (a == b) continue;
      for (int c = 1; c < 8; ++c) {
        if (c == a || c == b || c == (a ^ b)) continue;
        std::array<int, 8> table{};
        for (int x = 1; x < 8; ++x) {
          table[x] = ((x & 1) ? a : 0) ^
                     ((x & 2) ? b : 0) ^
                     ((x & 4) ? c : 0);
        }
        result.push_back(table);
      }
    }
  }
  assert(result.size() == 168);
  return result;
}

uint64_t normalize_flow(const Graph& graph, uint64_t flow) {
  const int e0 = graph.incidence[0][0];
  const int e1 = graph.incidence[0][1];
  const int a = flow_value(flow, e0);
  const int b = flow_value(flow, e1);
  assert(a != 0 && b != 0 && a != b);
  uint64_t best = ~uint64_t{0};
  for (int c = 1; c < 8; ++c) {
    if (c == a || c == b || c == (a ^ b)) continue;
    std::array<int, 8> table{};
    for (int source = 0; source < 8; ++source) {
      bool found = false;
      for (int word = 0; word < 8; ++word) {
        const int rebuilt = ((word & 1) ? a : 0) ^
                            ((word & 2) ? b : 0) ^
                            ((word & 4) ? c : 0);
        if (rebuilt == source) {
          table[source] = word;
          found = true;
          break;
        }
      }
      assert(found);
    }
    best = std::min(best, transform_flow(flow, graph.m(), table));
  }
  return best;
}

std::vector<uint64_t> flow_orbits(const Graph& graph) {
  const auto cycles = binary_cycles(graph);
  const auto root = graph.incidence[0];
  assert(root.size() == 3);
  std::array<std::vector<uint32_t>, 3> buckets;
  constexpr std::array<std::array<int, 3>, 3> patterns = {{
      {{1, 0, 1}}, {{0, 1, 1}}, {{0, 0, 0}},
  }};
  for (int row = 0; row < 3; ++row) {
    for (const uint32_t cycle : cycles) {
      bool matches = true;
      for (int j = 0; j < 3; ++j) {
        if (static_cast<int>((cycle >> root[j]) & 1U) !=
            patterns[row][j]) {
          matches = false;
        }
      }
      if (matches) buckets[row].push_back(cycle);
    }
  }
  const uint32_t all_edges =
      (uint32_t{1} << graph.m()) - uint32_t{1};
  std::unordered_set<uint64_t> seen;
  for (const uint32_t first : buckets[0]) {
    for (const uint32_t second : buckets[1]) {
      const uint32_t partial = first | second;
      for (const uint32_t third : buckets[2]) {
        if ((partial | third) != all_edges) continue;
        const uint64_t flow =
            encode_flow({first, second, third}, graph.m());
        seen.insert(normalize_flow(graph, flow));
      }
    }
  }
  std::vector<uint64_t> result(seen.begin(), seen.end());
  std::sort(result.begin(), result.end());
  return result;
}

struct Row {
  uint64_t mask;
  int rhs;
};

std::map<int, Row> rref(std::vector<Row> rows) {
  std::map<int, Row> pivots;
  for (Row row : rows) {
    while (row.mask) {
      const int pivot = 63 - __builtin_clzll(row.mask);
      const auto found = pivots.find(pivot);
      if (found == pivots.end()) {
        pivots.emplace(pivot, row);
        break;
      }
      row.mask ^= found->second.mask;
      row.rhs ^= found->second.rhs;
    }
    assert(row.mask || row.rhs == 0);
  }
  return pivots;
}

uint64_t potential_assignment(
    const std::map<int, Row>& pivots,
    const std::vector<int>& free_variables,
    uint64_t free_bits) {
  uint64_t assignment = 0;
  for (std::size_t i = 0; i < free_variables.size(); ++i) {
    if (free_bits & (uint64_t{1} << i)) {
      assignment |= uint64_t{1} << free_variables[i];
    }
  }
  for (const auto& [pivot, row] : pivots) {
    const uint64_t lower = row.mask & ((uint64_t{1} << pivot) - 1);
    const int value = (__builtin_popcountll(lower & assignment) & 1) ^
                      row.rhs;
    if (value) assignment |= uint64_t{1} << pivot;
  }
  return assignment;
}

int pair_index(int a, int b) {
  if (a > b) std::swap(a, b);
  assert(0 <= a && a < b && b < 8);
  int index = 0;
  for (int left = 0; left < 8; ++left) {
    for (int right = left + 1; right < 8; ++right) {
      if (left == a && right == b) return index;
      ++index;
    }
  }
  std::abort();
}

bool packing_exists(uint32_t used) {
  std::vector<std::array<int, 2>> missing;
  for (int a = 0; a < 8; ++a) {
    for (int b = a + 1; b < 8; ++b) {
      if (!(used & (uint32_t{1} << pair_index(a, b)))) {
        missing.push_back({a, b});
      }
    }
  }
  for (std::size_t i = 0; i < missing.size(); ++i) {
    for (std::size_t j = i + 1; j < missing.size(); ++j) {
      const int mask2 = (1 << missing[i][0]) | (1 << missing[i][1]) |
                        (1 << missing[j][0]) | (1 << missing[j][1]);
      if (__builtin_popcount(mask2) != 4) continue;
      for (std::size_t k = j + 1; k < missing.size(); ++k) {
        const int mask3 =
            mask2 | (1 << missing[k][0]) | (1 << missing[k][1]);
        if (__builtin_popcount(mask3) == 6) return true;
      }
    }
  }
  for (int a = 0; a < 8; ++a) {
    for (int b = a + 1; b < 8; ++b) {
      for (int c = b + 1; c < 8; ++c) {
        const uint32_t triangle =
            (uint32_t{1} << pair_index(a, b)) |
            (uint32_t{1} << pair_index(a, c)) |
            (uint32_t{1} << pair_index(b, c));
        if (used & triangle) continue;
        const int vertices = (1 << a) | (1 << b) | (1 << c);
        for (const auto edge : missing) {
          if (!(vertices & (1 << edge[0])) &&
              !(vertices & (1 << edge[1]))) {
            return true;
          }
        }
      }
    }
  }
  for (int a = 0; a < 8; ++a) {
    for (int b = a + 1; b < 8; ++b) {
      for (int c = b + 1; c < 8; ++c) {
        for (int d = c + 1; d < 8; ++d) {
          const std::array<int, 4> vertices = {a, b, c, d};
          bool clique = true;
          for (int i = 0; i < 4; ++i) {
            for (int j = i + 1; j < 4; ++j) {
              if (used &
                  (uint32_t{1} <<
                   pair_index(vertices[i], vertices[j]))) {
                clique = false;
              }
            }
          }
          if (clique) return true;
        }
      }
    }
  }
  return false;
}

bool flow_is_successful(const Graph& graph, uint64_t flow) {
  std::vector<Row> rows;
  for (int edge = 0; edge < graph.m(); ++edge) {
    const int u = graph.edges[edge][0], v = graph.edges[edge][1];
    const int u_other = *std::find_if(
        graph.incidence[u].begin(), graph.incidence[u].end(),
        [&](int e) { return e != edge; });
    const int v_other = *std::find_if(
        graph.incidence[v].begin(), graph.incidence[v].end(),
        [&](int e) { return e != edge; });
    const int difference =
        flow_value(flow, u_other) ^ flow_value(flow, v_other);
    const int value = flow_value(flow, edge);
    std::vector<int> orthogonal;
    for (int functional = 1; functional < 8; ++functional) {
      if ((__builtin_popcount(functional & value) & 1) == 0) {
        orthogonal.push_back(functional);
      }
    }
    assert(orthogonal.size() == 3);
    for (int row_index = 0; row_index < 2; ++row_index) {
      const int functional = orthogonal[row_index];
      uint64_t mask = 0;
      for (const int vertex : {u, v}) {
        for (int bit = 0; bit < 3; ++bit) {
          if (functional & (1 << bit)) {
            mask ^= uint64_t{1} << (3 * vertex + bit);
          }
        }
      }
      rows.push_back(
          {mask, __builtin_popcount(functional & difference) & 1});
    }
  }
  for (int bit = 0; bit < 3; ++bit) {
    rows.push_back({uint64_t{1} << bit, 0});
  }
  const auto pivots = rref(rows);
  std::vector<int> free_variables;
  for (int variable = 0; variable < 3 * graph.n; ++variable) {
    if (!pivots.count(variable)) free_variables.push_back(variable);
  }
  assert(free_variables.size() < 63);
  const uint64_t solution_count =
      uint64_t{1} << free_variables.size();
  for (uint64_t free_bits = 0; free_bits < solution_count; ++free_bits) {
    const uint64_t assignment =
        potential_assignment(pivots, free_variables, free_bits);
    std::array<int, MAX_N> potential{};
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      for (int bit = 0; bit < 3; ++bit) {
        potential[vertex] |=
            ((assignment >> (3 * vertex + bit)) & 1U) << bit;
      }
    }
    uint32_t used = 0;
    for (int edge = 0; edge < graph.m(); ++edge) {
      const int u = graph.edges[edge][0];
      const int u_other = *std::find_if(
          graph.incidence[u].begin(), graph.incidence[u].end(),
          [&](int e) { return e != edge; });
      const int first = potential[u] ^ flow_value(flow, u_other);
      const int second = first ^ flow_value(flow, edge);
      assert(first != second);
      used |= uint32_t{1} << pair_index(first, second);
    }
    if (packing_exists(used)) return true;
  }
  return false;
}

int vector_rank(std::array<int, 3> values) {
  std::array<int, 3> basis{};
  int size = 0;
  for (int value : values) {
    for (int i = 0; i < size; ++i) {
      value = std::min(value, value ^ basis[i]);
    }
    if (value) {
      basis[size++] = value;
      std::sort(basis.begin(), basis.begin() + size, std::greater<int>());
    }
  }
  return size;
}

struct Tree {
  uint32_t mask;
  uint32_t completion;
};

struct Exchange {
  uint32_t mask;
  uint32_t completion;
};

struct GraphResult {
  uint64_t flow_orbits = 0;
  uint64_t bad_flow_orbits = 0;
  uint64_t bad_support_types = 0;
  uint64_t spanning_trees = 0;
  uint64_t raw_tree_products = 0;
  uint64_t literal_states = 0;
  uint64_t successful_states = 0;
  bool failure = false;
  std::array<uint32_t, 3> failure_supports{};
  std::array<uint32_t, 3> failure_trees{};
};

GraphResult audit_graph(const Graph& graph) {
  GraphResult result;
  const auto orbits = flow_orbits(graph);
  result.flow_orbits = orbits.size();
  std::vector<uint64_t> bad_orbits;
  for (const uint64_t flow : orbits) {
    const bool success = flow_is_successful(graph, flow);
    if (!success) bad_orbits.push_back(flow);
  }
  result.bad_flow_orbits = bad_orbits.size();
  if (bad_orbits.empty()) return result;
  std::unordered_set<uint64_t> bad_labelled;
  const auto tables = gl3_tables();
  bad_labelled.reserve(bad_orbits.size() * tables.size() * 2);
  for (const uint64_t flow : bad_orbits) {
    for (const auto& table : tables) {
      bad_labelled.insert(transform_flow(flow, graph.m(), table));
    }
  }

  std::vector<Tree> trees;
  std::unordered_map<uint32_t, std::vector<int>> by_completion;
  const uint32_t universe = uint32_t{1} << graph.m();
  for (uint32_t mask = 0; mask < universe; ++mask) {
    if (!is_tree(graph, mask)) continue;
    const uint32_t completion = fundamental_completion(graph, mask);
    const int id = trees.size();
    trees.push_back({mask, completion});
    by_completion[completion].push_back(id);
  }
  result.spanning_trees = trees.size();
  std::vector<std::vector<Exchange>> exchanges(trees.size());
  for (std::size_t id = 0; id < trees.size(); ++id) {
    const uint32_t tree = trees[id].mask;
    for (int removed = 0; removed < graph.m(); ++removed) {
      if (!(tree & (uint32_t{1} << removed))) continue;
      for (int added = 0; added < graph.m(); ++added) {
        if (tree & (uint32_t{1} << added)) continue;
        const uint32_t changed =
            tree ^ (uint32_t{1} << removed) ^ (uint32_t{1} << added);
        if (!is_tree(graph, changed)) continue;
        exchanges[id].push_back(
            {changed, fundamental_completion(graph, changed)});
      }
    }
  }

  std::set<std::array<uint32_t, 3>> support_types;
  for (const uint64_t flow : bad_orbits) {
    std::vector<int> forest_functionals;
    for (int functional = 1; functional < 8; ++functional) {
      uint32_t zero = 0;
      for (int edge = 0; edge < graph.m(); ++edge) {
        if ((__builtin_popcount(functional & flow_value(flow, edge)) & 1) ==
            0) {
          zero |= uint32_t{1} << edge;
        }
      }
      if (is_forest(graph, zero)) {
        forest_functionals.push_back(functional);
      }
    }
    for (std::size_t i = 0; i < forest_functionals.size(); ++i) {
      for (std::size_t j = i + 1; j < forest_functionals.size(); ++j) {
        for (std::size_t k = j + 1; k < forest_functionals.size(); ++k) {
          const std::array<int, 3> functionals = {
              forest_functionals[i],
              forest_functionals[j],
              forest_functionals[k],
          };
          if (vector_rank(functionals) != 3) continue;
          std::array<uint32_t, 3> supports{};
          for (int coordinate = 0; coordinate < 3; ++coordinate) {
            for (int edge = 0; edge < graph.m(); ++edge) {
              if (__builtin_popcount(
                      functionals[coordinate] &
                      flow_value(flow, edge)) &
                  1) {
                supports[coordinate] |= uint32_t{1} << edge;
              }
            }
          }
          std::sort(supports.begin(), supports.end());
          assert(by_completion.count(supports[0]));
          assert(by_completion.count(supports[1]));
          assert(by_completion.count(supports[2]));
          support_types.insert(supports);
        }
      }
    }
  }
  result.bad_support_types = support_types.size();

  constexpr std::array<std::array<int, 3>, 3> pairs = {{
      {{0, 1, 2}}, {{0, 2, 1}}, {{1, 2, 0}},
  }};
  const std::vector<std::array<uint32_t, 3>> support_rows(
      support_types.begin(), support_types.end());
  uint64_t raw_tree_products = 0;
  uint64_t literal_states = 0;
  uint64_t successful_states = 0;
#ifdef _OPENMP
#pragma omp parallel for schedule(dynamic, 1) \
    reduction(+ : raw_tree_products, literal_states, successful_states)
#endif
  for (std::int64_t support_index = 0;
       support_index < static_cast<std::int64_t>(support_rows.size());
       ++support_index) {
    const auto& supports = support_rows[support_index];
    const auto& first = by_completion.at(supports[0]);
    const auto& second = by_completion.at(supports[1]);
    const auto& third = by_completion.at(supports[2]);
    raw_tree_products +=
        uint64_t(first.size()) * second.size() * third.size();
    std::unordered_map<uint32_t, std::vector<int>> admissible_third_cache;
    const auto& admissible_third = [&](uint32_t mask)
        -> const std::vector<int>& {
      auto found = admissible_third_cache.find(mask);
      if (found != admissible_third_cache.end()) return found->second;
      std::vector<int> ids;
      for (const int id : third) {
        if (!(mask & trees[id].mask)) ids.push_back(id);
      }
      return admissible_third_cache.emplace(mask, std::move(ids))
          .first->second;
    };
    for (const int id0 : first) {
      for (const int id1 : second) {
        if (supports[0] == supports[1] && id0 > id1) continue;
        const uint32_t intersection =
            trees[id0].mask & trees[id1].mask;
        for (const int id2 : admissible_third(intersection)) {
          if (supports[1] == supports[2] && id1 > id2) continue;
          ++literal_states;
          const std::array<int, 3> ids = {id0, id1, id2};
          bool escaped = false;
          for (const auto pair : pairs) {
            const int i = pair[0], j = pair[1], k = pair[2];
            for (const Exchange& left : exchanges[ids[i]]) {
              if (escaped) break;
              for (const Exchange& right : exchanges[ids[j]]) {
                if (left.mask & right.mask & trees[ids[k]].mask) continue;
                std::array<uint32_t, 3> changed = supports;
                changed[i] = left.completion;
                changed[j] = right.completion;
                const uint64_t flow =
                    encode_flow(changed, graph.m());
                bool escaped_here = false;
                if (REQUIRE_DIRECTION_THINNING) {
                  std::array<int, 8> counts{};
                  for (int edge = 0; edge < graph.m(); ++edge) {
                    ++counts[flow_value(flow, edge)];
                  }
                  escaped_here = std::any_of(
                      counts.begin() + 1,
                      counts.end(),
                      [](int count) { return count <= 1; });
                } else {
                  escaped_here = !bad_labelled.count(flow);
                }
                if (escaped_here) {
                  escaped = true;
                  break;
                }
              }
            }
          }
          if (!escaped) {
#ifdef _OPENMP
#pragma omp critical
#endif
            {
              if (!result.failure) {
                result.failure = true;
                result.failure_supports = supports;
                result.failure_trees = {
                    trees[id0].mask, trees[id1].mask, trees[id2].mask};
              }
            }
            continue;
          }
          ++successful_states;
        }
      }
    }
  }
  result.raw_tree_products = raw_tree_products;
  result.literal_states = literal_states;
  result.successful_states = successful_states;
  return result;
}

void print_graph_row(
    const std::string& graph6, const Graph& graph,
    const GraphResult& row) {
  *OUTPUT << "{\"status\":\"GRAPH_DONE\",\"graph6\":\"" << graph6
            << "\",\"vertices\":" << graph.n
            << ",\"edges\":" << graph.m()
            << ",\"flow_orbits\":" << row.flow_orbits
            << ",\"bad_flow_orbits\":" << row.bad_flow_orbits
            << ",\"bad_support_types_mod_coordinate_permutation\":"
            << row.bad_support_types
            << ",\"spanning_trees\":" << row.spanning_trees
            << ",\"raw_tree_products\":" << row.raw_tree_products
            << ",\"literal_states_mod_coordinate_permutation\":"
            << row.literal_states
            << ",\"successful_states\":" << row.successful_states
            << ",\"failure\":" << (row.failure ? "true" : "false");
  if (row.failure) {
    *OUTPUT << ",\"failure_support_masks\":["
              << row.failure_supports[0] << ','
              << row.failure_supports[1] << ','
              << row.failure_supports[2] << "],\"failure_tree_masks\":["
              << row.failure_trees[0] << ',' << row.failure_trees[1]
              << ',' << row.failure_trees[2] << ']';
  }
  *OUTPUT << "}\n";
}

}  // namespace

int main(int argc, char** argv) {
  if (argc == 3 && std::string(argv[1]) == "--thin") {
    REQUIRE_DIRECTION_THINNING = true;
    const std::string graph6 = argv[2];
    const Graph graph = parse_graph6(graph6);
    if (!is_cubic_connected(graph) || !is_bridgeless(graph)) {
      std::cerr << "graph is not connected, cubic, and bridgeless\n";
      return 3;
    }
    const GraphResult row = audit_graph(graph);
    print_graph_row(graph6, graph, row);
    return row.failure ? 2 : 0;
  }
  if (argc == 2) {
    const std::string graph6 = argv[1];
    const Graph graph = parse_graph6(graph6);
    if (!is_cubic_connected(graph) || !is_bridgeless(graph)) {
      std::cerr << "graph is not connected, cubic, and bridgeless\n";
      return 3;
    }
    const GraphResult row = audit_graph(graph);
    print_graph_row(graph6, graph, row);
    return row.failure ? 2 : 0;
  }
  std::ofstream output_file;
  std::string geng = "/opt/homebrew/bin/geng";
  int first_order = 4;
  int last_order = 14;
  int residue = -1;
  int modulus = -1;
  if (argc >= 3 && std::string(argv[1]) == "--output") {
    output_file.open(argv[2]);
    if (!output_file) throw std::runtime_error("could not open output path");
    OUTPUT = &output_file;
    if (argc >= 4) geng = argv[3];
  } else if (argc >= 7 && std::string(argv[1]) == "--shard") {
    output_file.open(argv[2]);
    if (!output_file) throw std::runtime_error("could not open output path");
    OUTPUT = &output_file;
    first_order = last_order = std::stoi(argv[3]);
    residue = std::stoi(argv[4]);
    modulus = std::stoi(argv[5]);
    if (argc >= 7) geng = argv[6];
    if (residue < 0 || modulus <= residue) {
      throw std::runtime_error("invalid geng residue/modulus");
    }
  } else if (argc != 1) {
    throw std::runtime_error(
        "expected GRAPH6, --output PATH [GENG], or "
        "--shard PATH ORDER RES MOD GENG");
  }
  uint64_t generated = 0;
  uint64_t bridgeless = 0;
  uint64_t flow_orbits_total = 0;
  uint64_t bad_flow_orbits_total = 0;
  uint64_t bad_support_types_total = 0;
  uint64_t literal_states_total = 0;
  uint64_t successful_states_total = 0;
  for (int order = first_order; order <= last_order; order += 2) {
    const int edge_count = 3 * order / 2;
    std::string command =
        geng + " -cq -d3 -D3 " + std::to_string(order) + " " +
        std::to_string(edge_count) + ":" + std::to_string(edge_count);
    if (residue >= 0) {
      command += " " + std::to_string(residue) + "/" +
                 std::to_string(modulus);
    }
    FILE* pipe = popen(command.c_str(), "r");
    if (!pipe) throw std::runtime_error("could not start geng");
    std::array<char, 4096> buffer{};
    while (fgets(buffer.data(), buffer.size(), pipe)) {
      std::string graph6(buffer.data());
      while (!graph6.empty() &&
             (graph6.back() == '\n' || graph6.back() == '\r')) {
        graph6.pop_back();
      }
      ++generated;
      const Graph graph = parse_graph6(graph6);
      assert(is_cubic_connected(graph));
      if (!is_bridgeless(graph)) continue;
      ++bridgeless;
      const GraphResult row = audit_graph(graph);
      print_graph_row(graph6, graph, row);
      flow_orbits_total += row.flow_orbits;
      bad_flow_orbits_total += row.bad_flow_orbits;
      bad_support_types_total += row.bad_support_types;
      literal_states_total += row.literal_states;
      successful_states_total += row.successful_states;
      if (row.failure) {
        pclose(pipe);
        return 2;
      }
    }
    const int status = pclose(pipe);
    if (status != 0) throw std::runtime_error("geng failed");
  }
  *OUTPUT
      << "{\"status\":\"FINITE_PASS_THROUGH_ORDER_14\","
      << "\"generated_graphs\":" << generated << ','
      << "\"bridgeless_graphs\":" << bridgeless << ','
      << "\"first_order\":" << first_order << ','
      << "\"last_order\":" << last_order << ','
      << "\"residue\":" << residue << ','
      << "\"modulus\":" << modulus << ','
      << "\"flow_orbits\":" << flow_orbits_total << ','
      << "\"bad_flow_orbits\":" << bad_flow_orbits_total << ','
      << "\"bad_support_types_mod_coordinate_permutation\":"
      << bad_support_types_total << ','
      << "\"literal_states_mod_coordinate_permutation\":"
      << literal_states_total << ','
      << "\"successful_states\":" << successful_states_total << "}\n";
  return 0;
}
