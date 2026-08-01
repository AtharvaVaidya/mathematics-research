// Exact witness-producing census for the whole-fibre square-local statement
// on simple 3-edge-connected cubic graphs of order 14.
//
// Generate the canonical input with:
//
//   geng -cq -d3 -D3 14 |
//     ./search_jaeger_star_square_existential_order14 > witnesses.tsv
//
// Every W row is a positive certificate for one labelled
// (graph, root, independent edge pair) instance.  The separate Python
// checker validates both completeness of the instance list and every tree,
// odd-kernel defect, and square-local lift from first principles.
//
// Coordinates are quotiented soundly: the three root spokes are sorted and
// tree i is required to contain root spoke i.  Any ordered star packing has
// exactly one coordinate permutation with that property, while exact-good
// status and square-local liftability are invariant under coordinate
// permutation.

#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

using Mask = std::uint32_t;

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
  constexpr const char* header = ">>graph6<<";
  if (record.rfind(header, 0) == 0) record.erase(0, 10);
  if (record.empty() || record[0] == '~') {
    throw std::runtime_error("only short graph6 records are supported");
  }
  Graph graph;
  graph.n = static_cast<unsigned char>(record[0]) - 63;
  if (graph.n != 14) throw std::runtime_error("expected order 14");
  std::vector<int> bits;
  for (std::size_t i = 1; i < record.size(); ++i) {
    const int value = static_cast<unsigned char>(record[i]) - 63;
    if (value < 0 || value >= 64) throw std::runtime_error("bad graph6");
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }
  const int needed = graph.n * (graph.n - 1) / 2;
  if (static_cast<int>(bits.size()) < needed) {
    throw std::runtime_error("truncated graph6");
  }
  int cursor = 0;
  for (int right = 1; right < graph.n; ++right) {
    for (int left = 0; left < right; ++left) {
      if (bits[cursor]) graph.edges.push_back({left, right});
      ++cursor;
    }
  }
  graph.incidence.assign(graph.n, {});
  for (int edge = 0; edge < graph.m(); ++edge) {
    for (const int vertex : graph.edges[edge]) {
      graph.incidence[vertex].push_back(edge);
    }
  }
  if (graph.m() != 21 ||
      !std::all_of(graph.incidence.begin(), graph.incidence.end(),
                   [](const auto& row) { return row.size() == 3; })) {
    throw std::runtime_error("input is not cubic");
  }
  return graph;
}

struct Dsu {
  std::vector<int> parent;
  explicit Dsu(int n) : parent(n) {
    std::iota(parent.begin(), parent.end(), 0);
  }
  int find(int x) {
    while (parent[x] != x) {
      parent[x] = parent[parent[x]];
      x = parent[x];
    }
    return x;
  }
  bool join(int first, int second) {
    first = find(first);
    second = find(second);
    if (first == second) return false;
    parent[first] = second;
    return true;
  }
};

bool connected_avoiding(
    const Graph& graph, int removed_first, int removed_second) {
  std::vector<char> seen(graph.n, false);
  std::vector<int> queue{0};
  seen[0] = true;
  for (std::size_t cursor = 0; cursor < queue.size(); ++cursor) {
    const int vertex = queue[cursor];
    for (const int edge : graph.incidence[vertex]) {
      if (edge == removed_first || edge == removed_second) continue;
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

bool is_three_edge_connected(const Graph& graph) {
  for (int first = 0; first < graph.m(); ++first) {
    if (!connected_avoiding(graph, first, -1)) return false;
    for (int second = first + 1; second < graph.m(); ++second) {
      if (!connected_avoiding(graph, first, second)) return false;
    }
  }
  return true;
}

bool is_tree(const Graph& graph, Mask selected) {
  if (std::popcount(selected) != graph.n - 1) return false;
  Dsu dsu(graph.n);
  for (int edge = 0; edge < graph.m(); ++edge) {
    if ((selected >> edge) & 1U) {
      if (!dsu.join(graph.edges[edge][0], graph.edges[edge][1])) {
        return false;
      }
    }
  }
  return true;
}

Mask odd_kernel(const Graph& graph, Mask tree) {
  if (!is_tree(graph, tree)) {
    throw std::runtime_error("odd_kernel received a non-tree");
  }
  std::vector<std::vector<std::array<int, 2>>> adjacency(graph.n);
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (!((tree >> edge) & 1U)) continue;
    const int left = graph.edges[edge][0];
    const int right = graph.edges[edge][1];
    adjacency[left].push_back({right, edge});
    adjacency[right].push_back({left, edge});
  }
  std::vector<int> parent(graph.n, -1);
  std::vector<int> parent_edge(graph.n, -1);
  std::vector<int> order{0};
  parent[0] = 0;
  for (std::size_t cursor = 0; cursor < order.size(); ++cursor) {
    const int vertex = order[cursor];
    for (const auto [other, edge] : adjacency[vertex]) {
      if (parent[other] != -1) continue;
      parent[other] = vertex;
      parent_edge[other] = edge;
      order.push_back(other);
    }
  }
  std::vector<int> size(graph.n, 1);
  Mask answer = 0;
  for (int cursor = graph.n - 1; cursor >= 1; --cursor) {
    const int vertex = order[cursor];
    if (size[vertex] & 1) answer |= Mask{1} << parent_edge[vertex];
    size[parent[vertex]] += size[vertex];
  }
  return answer;
}

std::array<int, 3> defect_profile(
    const Graph& graph, const std::array<Mask, 3>& state) {
  std::array<Mask, 3> kernels{};
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    kernels[coordinate] = odd_kernel(graph, state[coordinate]);
  }
  std::array<int, 3> result{};
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    const int first = (coordinate + 1) % 3;
    const int second = (coordinate + 2) % 3;
    const Mask pure = kernels[first] & kernels[second];
    Dsu dsu(graph.n);
    for (int edge = 0; edge < graph.m(); ++edge) {
      if ((kernels[coordinate] >> edge) & 1U) {
        dsu.join(graph.edges[edge][0], graph.edges[edge][1]);
      }
    }
    std::vector<unsigned char> parity(graph.n, 0);
    for (int edge = 0; edge < graph.m(); ++edge) {
      if (!((pure >> edge) & 1U)) continue;
      const int left = dsu.find(graph.edges[edge][0]);
      const int right = dsu.find(graph.edges[edge][1]);
      if (left != right) {
        parity[left] ^= 1;
        parity[right] ^= 1;
      }
    }
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      if (dsu.find(vertex) == vertex && parity[vertex]) ++result[coordinate];
    }
  }
  return result;
}

bool exact_good(const Graph& graph, const std::array<Mask, 3>& state) {
  const auto profile = defect_profile(graph, state);
  return std::find(profile.begin(), profile.end(), 0) != profile.end();
}

std::vector<std::array<int, 2>> eligible_pairs(
    const Graph& graph, int root) {
  std::vector<std::array<int, 2>> result;
  for (int first = 0; first < graph.m(); ++first) {
    const auto first_edge = graph.edges[first];
    if (first_edge[0] == root || first_edge[1] == root) continue;
    for (int second = first + 1; second < graph.m(); ++second) {
      const auto second_edge = graph.edges[second];
      if (second_edge[0] == root || second_edge[1] == root) continue;
      std::array<int, 4> ends{
          first_edge[0], first_edge[1], second_edge[0], second_edge[1]};
      std::sort(ends.begin(), ends.end());
      if (std::adjacent_find(ends.begin(), ends.end()) == ends.end()) {
        result.push_back({first, second});
      }
    }
  }
  return result;
}

struct LiftResult {
  bool found = false;
  std::array<Mask, 3> state{};
};

LiftResult good_local_lift(
    const Graph& down, const std::array<Mask, 3>& state,
    const std::array<int, 2>& removed_pair) {
  const int first_removed = removed_pair[0];
  const int second_removed = removed_pair[1];
  Graph up;
  up.n = down.n + 4;
  std::array<int, 21> down_to_up{};
  down_to_up.fill(-1);
  for (int edge = 0; edge < down.m(); ++edge) {
    if (edge == first_removed || edge == second_removed) continue;
    down_to_up[edge] = up.m();
    up.edges.push_back(down.edges[edge]);
  }
  const auto [A, C] = down.edges[first_removed];
  const auto [B, D] = down.edges[second_removed];
  const int a = down.n;
  const int b = down.n + 1;
  const int c = down.n + 2;
  const int d = down.n + 3;
  const std::array<std::array<int, 2>, 8> gadget{{
      {A, a}, {B, b}, {C, c}, {D, d},
      {a, b}, {b, c}, {c, d}, {d, a},
  }};
  const int local_offset = up.m();
  up.edges.insert(up.edges.end(), gadget.begin(), gadget.end());
  up.incidence.assign(up.n, {});
  for (int edge = 0; edge < up.m(); ++edge) {
    for (const int vertex : up.edges[edge]) {
      up.incidence[vertex].push_back(edge);
    }
  }

  std::array<Mask, 3> outside{};
  std::array<std::vector<std::pair<unsigned, Mask>>, 3> options;
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    for (int edge = 0; edge < down.m(); ++edge) {
      if (down_to_up[edge] >= 0 && ((state[coordinate] >> edge) & 1U)) {
        outside[coordinate] |= Mask{1} << down_to_up[edge];
      }
    }
    const int required_local = up.n - 1 - std::popcount(outside[coordinate]);
    for (unsigned local = 0; local < 256; ++local) {
      if (std::popcount(local) != required_local) continue;
      const Mask lifted = outside[coordinate] |
          (static_cast<Mask>(local) << local_offset);
      if (is_tree(up, lifted)) {
        options[coordinate].push_back({255U ^ local, lifted});
      }
    }
  }

  std::array<Mask, 256> third_tree{};
  std::array<unsigned char, 256> has_third{};
  for (const auto [omitted, tree] : options[2]) {
    third_tree[omitted] = tree;
    has_third[omitted] = 1;
  }
  for (const auto [omitted_zero, tree_zero] : options[0]) {
    for (const auto [omitted_one, tree_one] : options[1]) {
      if (omitted_zero & omitted_one) continue;
      const unsigned omitted_two = 255U ^ omitted_zero ^ omitted_one;
      if (!has_third[omitted_two]) continue;
      const std::array<Mask, 3> lifted{
          tree_zero, tree_one, third_tree[omitted_two]};
      if (exact_good(up, lifted)) return {true, lifted};
    }
  }
  return {};
}

std::vector<Mask> omission_options(
    const Graph& graph, Mask internal, int root_spoke) {
  std::vector<Mask> result;
  std::vector<int> internal_edges;
  for (int edge = 0; edge < graph.m(); ++edge) {
    if ((internal >> edge) & 1U) internal_edges.push_back(edge);
  }
  if (internal_edges.size() != 18) {
    throw std::runtime_error("wrong number of nonroot edges");
  }
  for (unsigned word = 0; word < (1U << 18); ++word) {
    if (std::popcount(word) != 6) continue;
    Mask omitted = 0;
    for (int slot = 0; slot < 18; ++slot) {
      if ((word >> slot) & 1U) {
        omitted |= Mask{1} << internal_edges[slot];
      }
    }
    const Mask tree = (internal ^ omitted) | (Mask{1} << root_spoke);
    if (is_tree(graph, tree)) result.push_back(omitted);
  }
  return result;
}

struct RootTotals {
  std::uint64_t states = 0;
  std::uint64_t good_states = 0;
  std::uint64_t lift_attempts = 0;
  std::uint64_t witnesses = 0;
};

RootTotals solve_root(
    const Graph& graph, const std::string& record, int graph_index, int root) {
  RootTotals totals;
  std::array<int, 3> spokes{};
  std::copy(
      graph.incidence[root].begin(), graph.incidence[root].end(),
      spokes.begin());
  std::sort(spokes.begin(), spokes.end());
  Mask internal = (Mask{1} << graph.m()) - 1;
  for (const int spoke : spokes) internal ^= Mask{1} << spoke;

  std::array<std::vector<Mask>, 3> options;
  std::array<std::unordered_set<Mask>, 3> lookup;
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    options[coordinate] =
        omission_options(graph, internal, spokes[coordinate]);
    lookup[coordinate].insert(
        options[coordinate].begin(), options[coordinate].end());
  }

  const auto pairs = eligible_pairs(graph, root);
  std::vector<unsigned char> resolved(pairs.size(), 0);
  std::size_t unresolved = pairs.size();
  for (const Mask omitted_zero : options[0]) {
    for (const Mask omitted_one : options[1]) {
      if (omitted_zero & omitted_one) continue;
      const Mask omitted_two = internal ^ omitted_zero ^ omitted_one;
      if (!lookup[2].contains(omitted_two)) continue;
      ++totals.states;
      const std::array<Mask, 3> state{{
          (internal ^ omitted_zero) | (Mask{1} << spokes[0]),
          (internal ^ omitted_one) | (Mask{1} << spokes[1]),
          (internal ^ omitted_two) | (Mask{1} << spokes[2]),
      }};
      if (!exact_good(graph, state)) continue;
      ++totals.good_states;
      for (std::size_t pair_index = 0; pair_index < pairs.size();
           ++pair_index) {
        if (resolved[pair_index]) continue;
        ++totals.lift_attempts;
        const LiftResult lifted =
            good_local_lift(graph, state, pairs[pair_index]);
        if (!lifted.found) continue;
        resolved[pair_index] = 1;
        --unresolved;
        ++totals.witnesses;
        std::cout
            << "W\t" << graph_index << '\t' << record << '\t' << root
            << '\t' << pairs[pair_index][0] << '\t'
            << pairs[pair_index][1]
            << '\t' << state[0] << '\t' << state[1] << '\t' << state[2]
            << '\t' << lifted.state[0] << '\t' << lifted.state[1]
            << '\t' << lifted.state[2] << '\n';
      }
      if (unresolved == 0) return totals;
    }
  }
  std::cerr
      << "FAIL graph_index=" << graph_index << " record=" << record
      << " root=" << root << " unresolved=" << unresolved
      << " states=" << totals.states << " good=" << totals.good_states
      << '\n';
  std::exit(2);
}

}  // namespace

int main(int argc, char** argv) {
  int start = 0;
  int end = 509;
  if (argc >= 2) start = std::stoi(argv[1]);
  if (argc >= 3) end = std::stoi(argv[2]);
  if (start < 0 || end < start || end > 509) {
    std::cerr << "usage: search [start_graph_index [end_graph_index]]\n";
    return 1;
  }
  std::uint64_t records = 0;
  std::uint64_t retained = 0;
  std::uint64_t roots = 0;
  std::uint64_t pairs = 0;
  std::uint64_t states = 0;
  std::uint64_t good_states = 0;
  std::uint64_t lift_attempts = 0;
  std::string record;
  while (std::cin >> record) {
    const int graph_index = static_cast<int>(records++);
    const Graph graph = parse_graph6(record);
    if (graph_index < start || graph_index >= end) continue;
    if (!is_three_edge_connected(graph)) continue;
    ++retained;
    for (int root = 0; root < graph.n; ++root) {
      const RootTotals result =
          solve_root(graph, record, graph_index, root);
      ++roots;
      pairs += result.witnesses;
      states += result.states;
      good_states += result.good_states;
      lift_attempts += result.lift_attempts;
    }
    std::cerr
        << "PASS_GRAPH index=" << graph_index << " record=" << record
        << " roots=" << graph.n << " cumulative_pairs=" << pairs
        << " cumulative_states=" << states
        << " cumulative_good=" << good_states
        << " cumulative_attempts=" << lift_attempts << '\n';
  }
  if (records != 509) {
    std::cerr << "expected 509 canonical records, received " << records
              << '\n';
    return 1;
  }
  std::cerr
      << "PASS_SHARD start=" << start << " end=" << end
      << " retained=" << retained << " roots=" << roots
      << " witnesses=" << pairs << " states=" << states
      << " good_states=" << good_states
      << " lift_attempts=" << lift_attempts << '\n';
  return 0;
}
