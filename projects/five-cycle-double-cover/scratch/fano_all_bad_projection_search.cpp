// Exact classifier/search for seven uncleanable Fano projection cycles.
//
// Usage:
//   c++ -O3 -std=c++20 scratch/fano_all_bad_projection_search.cpp -o /tmp/fano
//   /tmp/fano file1.g6 [file2.g6 ...]
//
// Graphs must be connected simple cubic graph6 rows of order below 42
// (hence fewer than 64 edges).  For every binary cycle h, this directly
// checks the two-cycle normal form over all unordered binary-cycle pairs
// p,q.  It then tests whether the bad projections contain the seven
// nonzero members of a covering 3-dimensional cycle subspace.

#include <algorithm>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

using Mask = std::uint64_t;

struct Graph {
  int order;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::vector<std::pair<int, int>>> adjacency;
};

Graph decode_graph6(std::string row) {
  while (!row.empty() && (row.back() == '\n' || row.back() == '\r')) {
    row.pop_back();
  }
  const std::string header = ">>graph6<<";
  if (row.starts_with(header)) row = row.substr(header.size());
  if (row.empty() || static_cast<unsigned char>(row[0]) >= 126) {
    throw std::runtime_error("only graph6 orders below 63 are supported");
  }
  const int order = static_cast<unsigned char>(row[0]) - 63;
  std::vector<int> bits;
  for (std::size_t index = 1; index < row.size(); ++index) {
    const int value = static_cast<unsigned char>(row[index]) - 63;
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }
  Graph graph{order, {}, std::vector<std::vector<std::pair<int, int>>>(order)};
  std::size_t position = 0;
  for (int second = 1; second < order; ++second) {
    for (int first = 0; first < second; ++first) {
      if (position >= bits.size()) throw std::runtime_error("truncated graph6");
      if (bits[position]) {
        const int edge = static_cast<int>(graph.edges.size());
        graph.edges.emplace_back(first, second);
        graph.adjacency[first].emplace_back(second, edge);
        graph.adjacency[second].emplace_back(first, edge);
      }
      ++position;
    }
  }
  if (graph.edges.size() >= 64) {
    throw std::runtime_error("this exact implementation needs fewer than 64 edges");
  }
  for (const auto &row_adjacency : graph.adjacency) {
    if (row_adjacency.size() != 3) throw std::runtime_error("graph is not cubic");
  }
  return graph;
}

std::vector<Mask> cycle_basis(const Graph &graph) {
  std::vector<int> parent(graph.order, -1), parent_edge(graph.order, -1);
  std::vector<bool> tree_edge(graph.edges.size(), false);
  std::queue<int> queue;
  parent[0] = 0;
  queue.push(0);
  while (!queue.empty()) {
    const int vertex = queue.front();
    queue.pop();
    for (const auto &[neighbor, edge] : graph.adjacency[vertex]) {
      if (parent[neighbor] < 0) {
        parent[neighbor] = vertex;
        parent_edge[neighbor] = edge;
        tree_edge[edge] = true;
        queue.push(neighbor);
      }
    }
  }
  if (std::ranges::find(parent, -1) != parent.end()) {
    throw std::runtime_error("graph is disconnected");
  }

  auto tree_path = [&](int first, int second) {
    std::vector<Mask> prefix(graph.order, 0);
    std::vector<bool> on_first_path(graph.order, false);
    Mask mask = 0;
    int vertex = first;
    while (true) {
      on_first_path[vertex] = true;
      prefix[vertex] = mask;
      if (vertex == 0) break;
      mask ^= Mask{1} << parent_edge[vertex];
      vertex = parent[vertex];
    }
    mask = 0;
    vertex = second;
    while (!on_first_path[vertex]) {
      mask ^= Mask{1} << parent_edge[vertex];
      vertex = parent[vertex];
    }
    return mask ^ prefix[vertex];
  };

  std::vector<Mask> basis;
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    if (!tree_edge[edge]) {
      const auto [first, second] = graph.edges[edge];
      basis.push_back((Mask{1} << edge) ^ tree_path(first, second));
    }
  }
  if (basis.size() != graph.edges.size() - graph.order + 1) {
    throw std::runtime_error("wrong cycle-space dimension");
  }
  return basis;
}

std::vector<Mask> enumerate_cycles(const std::vector<Mask> &basis) {
  std::vector<Mask> cycles{0};
  for (const Mask vector : basis) {
    const std::size_t old_size = cycles.size();
    cycles.reserve(2 * old_size);
    for (std::size_t index = 0; index < old_size; ++index) {
      cycles.push_back(cycles[index] ^ vector);
    }
  }
  std::ranges::sort(cycles, [](Mask first, Mask second) {
    const int first_weight = std::popcount(first);
    const int second_weight = std::popcount(second);
    if (first_weight != second_weight) return first_weight > second_weight;
    return first < second;
  });
  return cycles;
}

std::vector<Mask> factor_cut_masks(const Graph &graph, Mask factor) {
  std::vector<int> component(graph.order, -1);
  int component_count = 0;
  for (int root = 0; root < graph.order; ++root) {
    if (component[root] >= 0) continue;
    std::queue<int> queue;
    component[root] = component_count;
    queue.push(root);
    while (!queue.empty()) {
      const int vertex = queue.front();
      queue.pop();
      for (const auto &[neighbor, edge] : graph.adjacency[vertex]) {
        if (((factor >> edge) & 1) && component[neighbor] < 0) {
          component[neighbor] = component_count;
          queue.push(neighbor);
        }
      }
    }
    ++component_count;
  }
  std::vector<Mask> cuts(component_count, 0);
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    const auto [first, second] = graph.edges[edge];
    if (component[first] != component[second]) {
      cuts[component[first]] |= Mask{1} << edge;
      cuts[component[second]] |= Mask{1} << edge;
    }
  }
  return cuts;
}

struct ProjectionClass {
  bool liftable;
  bool clean;
};

ProjectionClass classify_projection(
    const Graph &graph,
    const std::vector<Mask> &cycles,
    Mask projection,
    Mask all_edges) {
  const Mask factor = all_edges ^ projection;
  const std::vector<Mask> cuts = factor_cut_masks(graph, factor);
  bool liftable = false;
  for (std::size_t first_index = 0; first_index < cycles.size(); ++first_index) {
    const Mask first = cycles[first_index];
    const Mask missing = factor & ~first;
    for (std::size_t second_index = first_index;
         second_index < cycles.size(); ++second_index) {
      const Mask second = cycles[second_index];
      if (missing & ~second) continue;
      liftable = true;
      const Mask product = first & second;
      bool clean = true;
      for (const Mask cut : cuts) {
        if (std::popcount(product & cut) & 1) {
          clean = false;
          break;
        }
      }
      if (clean) return {true, true};
    }
  }
  return {liftable, false};
}

int binary_rank(std::vector<Mask> vectors) {
  std::vector<Mask> pivots(64, 0);
  int rank = 0;
  for (Mask vector : vectors) {
    while (vector) {
      const int pivot = 63 - std::countl_zero(vector);
      if (!pivots[pivot]) {
        pivots[pivot] = vector;
        ++rank;
        break;
      }
      vector ^= pivots[pivot];
    }
  }
  return rank;
}

bool tait_backtrack(
    const Graph &graph,
    std::vector<int> &colors,
    std::vector<int> &used,
    int colored_count) {
  if (colored_count == static_cast<int>(graph.edges.size())) return true;
  int best_edge = -1;
  int best_allowed = 0;
  int best_count = 4;
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    if (colors[edge] >= 0) continue;
    const auto [first, second] = graph.edges[edge];
    const int allowed = 7 & ~used[first] & ~used[second];
    const int count = std::popcount(static_cast<unsigned>(allowed));
    if (!count) return false;
    if (count < best_count) {
      best_count = count;
      best_edge = edge;
      best_allowed = allowed;
      if (count == 1) break;
    }
  }
  const auto [first, second] = graph.edges[best_edge];
  for (int choices = best_allowed; choices; choices &= choices - 1) {
    const int bit = choices & -choices;
    const int color = std::countr_zero(static_cast<unsigned>(bit));
    colors[best_edge] = color;
    used[first] |= bit;
    used[second] |= bit;
    if (tait_backtrack(graph, colors, used, colored_count + 1)) return true;
    used[first] ^= bit;
    used[second] ^= bit;
    colors[best_edge] = -1;
  }
  return false;
}

bool is_tait_colorable(const Graph &graph) {
  std::vector<int> colors(graph.edges.size(), -1);
  std::vector<int> used(graph.order, 0);
  // Break the global S_3 color symmetry at one vertex.
  const int vertex = 0;
  int colored = 0;
  for (int color = 0; color < 3; ++color) {
    const int edge = graph.adjacency[vertex][color].second;
    const auto [first, second] = graph.edges[edge];
    colors[edge] = color;
    used[first] |= 1 << color;
    used[second] |= 1 << color;
    ++colored;
  }
  return tait_backtrack(graph, colors, used, colored);
}

bool is_bridgeless(const Graph &graph) {
  for (int omitted = 0; omitted < static_cast<int>(graph.edges.size());
       ++omitted) {
    std::vector<bool> seen(graph.order, false);
    std::queue<int> queue;
    seen[0] = true;
    queue.push(0);
    while (!queue.empty()) {
      const int vertex = queue.front();
      queue.pop();
      for (const auto &[neighbor, edge] : graph.adjacency[vertex]) {
        if (edge != omitted && !seen[neighbor]) {
          seen[neighbor] = true;
          queue.push(neighbor);
        }
      }
    }
    if (std::ranges::find(seen, false) != seen.end()) return false;
  }
  return true;
}

bool find_all_bad_subspace(
    const std::vector<Mask> &bad,
    const std::unordered_set<Mask> &bad_set,
    Mask all_edges,
    std::vector<Mask> *witness) {
  for (std::size_t first_index = 0; first_index < bad.size(); ++first_index) {
    const Mask first = bad[first_index];
    if (!first) continue;
    for (std::size_t second_index = first_index + 1;
         second_index < bad.size(); ++second_index) {
      const Mask second = bad[second_index];
      if (!second || first == second) continue;
      for (std::size_t third_index = second_index + 1;
           third_index < bad.size(); ++third_index) {
        const Mask third = bad[third_index];
        if (!third || third == (first ^ second)) continue;
        std::vector<Mask> span{
            first,
            second,
            third,
            first ^ second,
            first ^ third,
            second ^ third,
            first ^ second ^ third,
        };
        bool all_bad = true;
        for (const Mask value : span) {
          if (!value || !bad_set.contains(value)) {
            all_bad = false;
            break;
          }
        }
        if (!all_bad || (first | second | third) != all_edges) continue;
        std::ranges::sort(span);
        span.erase(std::unique(span.begin(), span.end()), span.end());
        if (span.size() != 7) continue;
        *witness = span;
        return true;
      }
    }
  }
  return false;
}

int maximum_bad_intersection_from_bad_triples(
    const std::vector<Mask> &bad,
    const std::unordered_set<Mask> &bad_set,
    Mask all_edges,
    std::vector<Mask> *maximum_witness) {
  int maximum = 0;
  for (std::size_t first_index = 0; first_index < bad.size(); ++first_index) {
    const Mask first = bad[first_index];
    if (!first) continue;
    for (std::size_t second_index = first_index + 1;
         second_index < bad.size(); ++second_index) {
      const Mask second = bad[second_index];
      if (!second || first == second) continue;
      for (std::size_t third_index = second_index + 1;
           third_index < bad.size(); ++third_index) {
        const Mask third = bad[third_index];
        if (!third || third == (first ^ second)) continue;
        if ((first | second | third) != all_edges) continue;
        const Mask span[] = {
            first,
            second,
            third,
            first ^ second,
            first ^ third,
            second ^ third,
            first ^ second ^ third,
        };
        int count = 0;
        for (const Mask value : span) count += bad_set.contains(value);
        if (count > maximum) {
          maximum = count;
          maximum_witness->assign(std::begin(span), std::end(span));
          std::ranges::sort(*maximum_witness);
        }
      }
    }
  }
  return maximum;
}

void audit_graph(const std::string &source, int row_index, const std::string &row) {
  const Graph graph = decode_graph6(row);
  if (!is_bridgeless(graph)) {
    std::cout << "{\"source\":\"" << source << "\",\"row\":" << row_index
              << ",\"order\":" << graph.order
              << ",\"bridgeless\":false,\"skipped\":true}" << std::endl;
    return;
  }
  const std::vector<Mask> basis = cycle_basis(graph);
  const std::vector<Mask> cycles = enumerate_cycles(basis);
  const Mask all_edges =
      graph.edges.size() == 64 ? ~Mask{0}
                               : ((Mask{1} << graph.edges.size()) - 1);
  const bool tait_colorable = is_tait_colorable(graph);
  if (tait_colorable) {
    std::cout << "{\"source\":\"" << source << "\",\"row\":" << row_index
              << ",\"order\":" << graph.order
              << ",\"cycles\":" << cycles.size()
              << ",\"bad\":0,\"liftable_bad\":0,"
                 "\"liftable_bad_rank\":0,"
                 "\"all_seven_obstruction\":false}"
              << std::endl;
    return;
  }
  std::vector<Mask> bad, liftable_bad;
  std::unordered_set<Mask> bad_set;
  for (const Mask projection : cycles) {
    // The Tait case was already removed.  A lift of projection zero is
    // exactly a nowhere-zero F_2^2-flow, so zero is immediately unliftable.
    const ProjectionClass result =
        projection == 0
            ? ProjectionClass{false, false}
            : classify_projection(graph, cycles, projection, all_edges);
    if (!result.clean) {
      bad.push_back(projection);
      bad_set.insert(projection);
      if (result.liftable) liftable_bad.push_back(projection);
    }
  }
  std::vector<Mask> witness;
  const bool obstruction =
      find_all_bad_subspace(bad, bad_set, all_edges, &witness);
  const int maximum_bad_from_triples =
      maximum_bad_intersection_from_bad_triples(
          bad, bad_set, all_edges, &witness);
  std::cout << "{\"source\":\"" << source << "\",\"row\":" << row_index
            << ",\"order\":" << graph.order
            << ",\"cycles\":" << cycles.size()
            << ",\"bad\":" << bad.size()
            << ",\"liftable_bad\":" << liftable_bad.size()
            << ",\"liftable_bad_rank\":" << binary_rank(liftable_bad)
            << ",\"max_bad_in_covering_space_from_bad_triples\":"
            << maximum_bad_from_triples << ",\"max_witness_hex\":[";
  for (std::size_t index = 0; index < witness.size(); ++index) {
    if (index) std::cout << ',';
    std::cout << "\"0x" << std::hex << witness[index] << std::dec << "\"";
  }
  std::cout << "],\"all_seven_obstruction\":"
            << (obstruction ? "true" : "false") << "}" << std::endl;
  if (obstruction) {
    std::cerr << "all-seven obstruction:";
    for (const Mask value : witness) std::cerr << " 0x" << std::hex << value;
    std::cerr << std::dec << std::endl;
  }
}

int main(int argc, char **argv) {
  if (argc < 2) {
    std::cerr << "usage: " << argv[0] << " FILE.g6 [FILE.g6 ...]" << std::endl;
    return 1;
  }
  try {
    for (int argument = 1; argument < argc; ++argument) {
      std::ifstream stream(argv[argument]);
      if (!stream) throw std::runtime_error("cannot open input");
      std::string row;
      int row_index = 0;
      while (std::getline(stream, row)) {
        if (!row.empty()) audit_graph(argv[argument], row_index, row);
        ++row_index;
      }
    }
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << std::endl;
    return 1;
  }
  return 0;
}
