// Exact all-seven projection search with a linear inner cleanability test.
//
// For fixed projection h and first binary cycle p, the second cycle q is
// represented by its cycle-basis coefficients.  Both the coverage equations
// q_e=1 on (E\h)\p and the component-defect equations
//   |q & p & delta(W)| = 0
// are linear in those coefficients.  Gaussian elimination therefore replaces
// the quadratic enumeration of all (p,q) pairs in the older checker.
//
// Usage:
//   c++ -O3 -std=c++20 scratch/fano_all_bad_projection_search_linear.cpp -o /tmp/fano-linear
//   /tmp/fano-linear input.g6 [...]
//
// This is an exact classifier, not a Five-CDC solver.

#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <ranges>
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
    throw std::runtime_error("this implementation needs fewer than 64 edges");
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
  if (basis.size() >= 63) throw std::runtime_error("basis too large");
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

bool consistent_system(
    const std::vector<Mask> &equations,
    int variables) {
  // Bits [0,variables) are coefficients and bit variables is the RHS.
  std::array<Mask, 63> pivots{};
  const Mask variable_mask = (Mask{1} << variables) - 1;
  for (Mask row : equations) {
    while (row & variable_mask) {
      const int pivot = 63 - std::countl_zero(row & variable_mask);
      if (!pivots[pivot]) {
        pivots[pivot] = row;
        row = 0;
        break;
      }
      row ^= pivots[pivot];
    }
    if (row == (Mask{1} << variables)) return false;
  }
  return true;
}

bool projection_clean(
    const Graph &graph,
    const std::vector<Mask> &basis,
    const std::vector<Mask> &cycles,
    const std::vector<Mask> &edge_coefficients,
    Mask projection,
    Mask all_edges) {
  const Mask factor = all_edges ^ projection;
  const std::vector<Mask> cuts = factor_cut_masks(graph, factor);
  const int dimension = static_cast<int>(basis.size());
  const Mask rhs_one = Mask{1} << dimension;
  std::vector<Mask> equations;
  equations.reserve(graph.edges.size() + cuts.size());

  for (const Mask first : cycles) {
    equations.clear();
    Mask missing = factor & ~first;
    while (missing) {
      const int edge = std::countr_zero(missing);
      missing &= missing - 1;
      equations.push_back(edge_coefficients[edge] | rhs_one);
    }
    for (const Mask cut : cuts) {
      Mask trace = first & cut;
      Mask equation = 0;
      while (trace) {
        const int edge = std::countr_zero(trace);
        trace &= trace - 1;
        equation ^= edge_coefficients[edge];
      }
      if (equation) equations.push_back(equation);
    }
    if (consistent_system(equations, dimension)) return true;
  }
  return false;
}

bool tait_backtrack(
    const Graph &graph,
    std::vector<int> &colors,
    std::vector<int> &used,
    int colored_count) {
  if (colored_count == static_cast<int>(graph.edges.size())) return true;
  int best_edge = -1, best_allowed = 0, best_count = 4;
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    if (colors[edge] >= 0) continue;
    const auto [first, second] = graph.edges[edge];
    const int allowed = 7 & ~used[first] & ~used[second];
    const int count = std::popcount(static_cast<unsigned>(allowed));
    if (!count) return false;
    if (count < best_count) {
      best_edge = edge;
      best_allowed = allowed;
      best_count = count;
      if (count == 1) break;
    }
  }
  const auto [first, second] = graph.edges[best_edge];
  for (int choices = best_allowed; choices; choices &= choices - 1) {
    const int bit = choices & -choices;
    colors[best_edge] = std::countr_zero(static_cast<unsigned>(bit));
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
  int colored = 0;
  for (int color = 0; color < 3; ++color) {
    const int edge = graph.adjacency[0][color].second;
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

int binary_rank(const std::vector<Mask> &vectors) {
  std::array<Mask, 64> pivots{};
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
      if (!bad_set.contains(first ^ second)) continue;
      for (std::size_t third_index = second_index + 1;
           third_index < bad.size(); ++third_index) {
        const Mask third = bad[third_index];
        if (!third || third == (first ^ second)) continue;
        const Mask span[] = {
            first,
            second,
            third,
            first ^ second,
            first ^ third,
            second ^ third,
            first ^ second ^ third,
        };
        bool all_bad = true;
        Mask cover = 0;
        for (const Mask value : span) {
          all_bad &= value && bad_set.contains(value);
          cover |= value;
        }
        if (!all_bad || cover != all_edges) continue;
        witness->assign(std::begin(span), std::end(span));
        std::ranges::sort(*witness);
        return true;
      }
    }
  }
  return false;
}

int closest_covering_space(
    const std::vector<Mask> &bad,
    const std::unordered_set<Mask> &bad_set,
    Mask all_edges,
    std::vector<Mask> *witness) {
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
          witness->assign(std::begin(span), std::end(span));
          std::ranges::sort(*witness);
          // The caller has already ruled out seven.  Six is therefore
          // the largest possible value and permits an exact early exit.
          if (maximum == 6) return maximum;
        }
      }
    }
  }
  return maximum;
}

void audit_graph(
    const std::string &source,
    int row_index,
    const std::string &row,
    bool compute_closest) {
  const Graph graph = decode_graph6(row);
  if (!is_bridgeless(graph)) return;
  const std::vector<Mask> basis = cycle_basis(graph);
  const std::vector<Mask> cycles = enumerate_cycles(basis);
  const Mask all_edges = (Mask{1} << graph.edges.size()) - 1;
  if (is_tait_colorable(graph)) {
    std::cout << "{\"source\":\"" << source << "\",\"row\":" << row_index
              << ",\"order\":" << graph.order
              << ",\"cycles\":" << cycles.size()
              << ",\"bad\":0,\"all_seven_obstruction\":false}" << std::endl;
    return;
  }

  std::vector<Mask> edge_coefficients(graph.edges.size(), 0);
  for (int coordinate = 0; coordinate < static_cast<int>(basis.size());
       ++coordinate) {
    Mask support = basis[coordinate];
    while (support) {
      const int edge = std::countr_zero(support);
      support &= support - 1;
      edge_coefficients[edge] |= Mask{1} << coordinate;
    }
  }

  std::vector<Mask> bad{0};
  std::unordered_set<Mask> bad_set{0};
  for (const Mask projection : cycles) {
    if (!projection) continue;
    if (!projection_clean(
            graph, basis, cycles, edge_coefficients, projection, all_edges)) {
      bad.push_back(projection);
      bad_set.insert(projection);
    }
  }
  std::vector<Mask> witness;
  const bool obstruction =
      find_all_bad_subspace(bad, bad_set, all_edges, &witness);
  std::vector<Mask> closest_witness;
  const int closest =
      obstruction
          ? 7
          : (compute_closest
                 ? closest_covering_space(
                       bad, bad_set, all_edges, &closest_witness)
                 : -1);
  std::cout << "{\"source\":\"" << source << "\",\"row\":" << row_index
            << ",\"order\":" << graph.order
            << ",\"cycles\":" << cycles.size()
            << ",\"bad\":" << bad.size()
            << ",\"bad_rank\":" << binary_rank(bad)
            << ",\"all_seven_obstruction\":"
            << (obstruction ? "true" : "false")
            << ",\"max_bad_in_covering_space\":" << closest
            << ",\"witness_hex\":[";
  const std::vector<Mask> &displayed_witness =
      obstruction ? witness : closest_witness;
  for (std::size_t index = 0; index < displayed_witness.size(); ++index) {
    if (index) std::cout << ',';
    std::cout << "\"0x" << std::hex << displayed_witness[index] << std::dec
              << "\"";
  }
  std::cout << "],\"witness_profiles\":[";
  for (std::size_t index = 0; index < displayed_witness.size(); ++index) {
    if (index) std::cout << ',';
    const Mask projection = displayed_witness[index];
    const Mask factor = all_edges ^ projection;
    const int components =
        static_cast<int>(factor_cut_masks(graph, factor).size());
    const int factor_cycle_rank =
        std::popcount(factor) - graph.order + components;
    bool matching = std::popcount(factor) * 2 == graph.order;
    if (matching) {
      for (int vertex = 0; vertex < graph.order; ++vertex) {
        int degree = 0;
        for (const auto &[neighbor, edge] : graph.adjacency[vertex]) {
          (void)neighbor;
          degree += (factor >> edge) & 1;
        }
        matching &= degree == 1;
      }
    }
    std::cout << "{\"h\":\"0x" << std::hex << projection << std::dec
              << "\",\"bad\":" << (bad_set.contains(projection) ? "true" : "false")
              << ",\"factor_edges\":" << std::popcount(factor)
              << ",\"factor_components\":" << components
              << ",\"factor_cycle_rank\":" << factor_cycle_rank
              << ",\"factor_matching\":" << (matching ? "true" : "false")
              << "}";
  }
  std::cout << "]}" << std::endl;
}

int main(int argc, char **argv) {
  if (argc < 2) {
    std::cerr << "usage: fano-linear [--closest] FILE.g6 [...]" << std::endl;
    return 1;
  }
  try {
    const bool compute_closest = std::string(argv[1]) == "--closest";
    const int first_argument = compute_closest ? 2 : 1;
    if (first_argument == argc) throw std::runtime_error("missing input file");
    for (int argument = first_argument; argument < argc; ++argument) {
      std::ifstream stream(argv[argument]);
      if (!stream) throw std::runtime_error("cannot open input");
      std::string row;
      int row_index = 0;
      while (std::getline(stream, row)) {
        if (!row.empty()) {
          audit_graph(
              argv[argument], row_index, row, compute_closest);
        }
        ++row_index;
      }
    }
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << std::endl;
    return 1;
  }
}
