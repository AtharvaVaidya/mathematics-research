// Independent exhaustive counter for the 16-vertex kernel-closure no-go.
//
// This program uses no SAT solver.  Deleting the root turns a star-fibre
// packing into a partition of the 21 remaining edges into three cographic
// bases A_i: the complement of each A_i is a spanning tree on 15 vertices.
// It enumerates those partitions exactly, restores the three root spokes in
// every possible bijection, computes the odd-side forests K(T_i), and counts
// both the closure strengthening and the exact component-parity criterion.
//
// Build:
//   clang++ -O3 -std=c++20 \
//     scratch/count_jaeger_star_kernel_closure_countermodel_16v.cpp \
//     -o /tmp/count_star_kernel_closure_16v

#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr int n = 16;
constexpr int m = 24;
constexpr int root = 13;
constexpr std::array<std::array<int, 2>, m> edges{{
    {0, 6}, {0, 9}, {0, 10},
    {1, 7}, {1, 10}, {1, 11},
    {2, 8}, {2, 12}, {2, 15},
    {3, 9}, {3, 13}, {3, 14},
    {4, 10}, {4, 13}, {4, 15},
    {5, 11}, {5, 12}, {5, 13},
    {6, 9}, {6, 12},
    {7, 11}, {7, 14},
    {8, 14}, {8, 15},
}};
constexpr std::array<int, 3> spokes{{10, 13, 17}};
constexpr std::array<int, 21> nonroot{{
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12,
    14, 15, 16, 18, 19, 20, 21, 22, 23,
}};
constexpr uint32_t all_nonroot = (uint32_t{1} << 21) - 1;

struct DSU {
  std::array<int, n> parent{};
  DSU() { std::iota(parent.begin(), parent.end(), 0); }
  int find(int vertex) {
    if (parent[vertex] == vertex) return vertex;
    return parent[vertex] = find(parent[vertex]);
  }
  bool join(int left, int right) {
    left = find(left);
    right = find(right);
    if (left == right) return false;
    parent[left] = right;
    return true;
  }
};

bool cotree_base(const uint32_t omitted) {
  assert(std::popcount(omitted) == 7);
  DSU dsu;
  int selected = 0;
  for (int local = 0; local < 21; ++local) {
    if (omitted & (uint32_t{1} << local)) continue;
    const int edge = nonroot[local];
    if (!dsu.join(edges[edge][0], edges[edge][1])) return false;
    ++selected;
  }
  if (selected != 14) return false;
  int representative = -1;
  for (int vertex = 0; vertex < n; ++vertex) {
    if (vertex == root) continue;
    if (representative < 0) representative = dsu.find(vertex);
    if (dsu.find(vertex) != representative) return false;
  }
  return true;
}

uint32_t odd_kernel(const uint32_t omitted, const int spoke) {
  std::array<std::vector<std::pair<int, int>>, n> adjacency;
  for (int local = 0; local < 21; ++local) {
    if (omitted & (uint32_t{1} << local)) continue;
    const int edge = nonroot[local];
    const auto [left, right] = edges[edge];
    adjacency[left].push_back({right, edge});
    adjacency[right].push_back({left, edge});
  }
  {
    const auto [left, right] = edges[spoke];
    adjacency[left].push_back({right, spoke});
    adjacency[right].push_back({left, spoke});
  }
  std::array<int, n> parent;
  std::array<int, n> parent_edge;
  parent.fill(-2);
  parent_edge.fill(-1);
  parent[0] = -1;
  std::array<int, n> order{};
  int order_size = 1;
  for (int cursor = 0; cursor < order_size; ++cursor) {
    const int vertex = order[cursor];
    for (const auto [other, edge] : adjacency[vertex]) {
      if (parent[other] != -2) continue;
      parent[other] = vertex;
      parent_edge[other] = edge;
      order[order_size++] = other;
    }
  }
  assert(order_size == n);
  std::array<int, n> size;
  size.fill(1);
  uint32_t answer = 0;
  for (int cursor = n - 1; cursor > 0; --cursor) {
    const int vertex = order[cursor];
    if (size[vertex] & 1) {
      answer |= uint32_t{1} << parent_edge[vertex];
    }
    size[parent[vertex]] += size[vertex];
  }
  return answer;
}

std::pair<int, int> scores(const std::array<uint32_t, 3>& kernel) {
  int closure_coordinates = 0;
  int parity_coordinates = 0;
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    DSU dsu;
    for (int edge = 0; edge < m; ++edge) {
      if (kernel[coordinate] & (uint32_t{1} << edge)) {
        assert(dsu.join(edges[edge][0], edges[edge][1]));
      }
    }
    const int first = (coordinate + 1) % 3;
    const int second = (coordinate + 2) % 3;
    const uint32_t common = kernel[first] & kernel[second];
    bool closure_good = true;
    std::array<int, n> boundary{};
    for (int edge = 0; edge < m; ++edge) {
      if (!(common & (uint32_t{1} << edge))) continue;
      const int left = dsu.find(edges[edge][0]);
      const int right = dsu.find(edges[edge][1]);
      if (left == right) continue;
      closure_good = false;
      boundary[left] ^= 1;
      boundary[right] ^= 1;
    }
    closure_coordinates += closure_good;
    parity_coordinates += std::none_of(
        boundary.begin(), boundary.end(), [](const int bit) {
          return bit != 0;
        });
  }
  return {closure_coordinates, parity_coordinates};
}

}  // namespace

int main() {
  std::vector<uint32_t> bases;
  for (uint32_t mask = 0; mask <= all_nonroot; ++mask) {
    if (std::popcount(mask) == 7 && cotree_base(mask)) {
      bases.push_back(mask);
    }
  }
  std::unordered_set<uint32_t> base_set(bases.begin(), bases.end());
  assert(bases.size() == 16200);

  std::unordered_map<uint32_t, std::array<uint32_t, 3>> kernels;
  kernels.reserve(bases.size());
  for (const uint32_t base : bases) {
    std::array<uint32_t, 3> row{};
    for (int slot = 0; slot < 3; ++slot) {
      row[slot] = odd_kernel(base, spokes[slot]);
    }
    kernels.emplace(base, row);
  }

  uint64_t unordered_partitions = 0;
  std::map<std::pair<int, int>, uint64_t> histogram;
  for (const uint32_t first : bases) {
    // Edge zero belongs to exactly one part, selecting it canonically.
    if (!(first & 1)) continue;
    const uint32_t remaining = all_nonroot ^ first;
    for (uint32_t second = remaining; second;
         second = (second - 1) & remaining) {
      if (std::popcount(second) != 7) continue;
      const uint32_t third = remaining ^ second;
      if (second >= third) continue;
      if (!base_set.contains(second) || !base_set.contains(third)) continue;
      ++unordered_partitions;
      const std::array<uint32_t, 3> parts{{first, second, third}};
      std::array<int, 3> spoke_permutation{{0, 1, 2}};
      do {
        std::array<uint32_t, 3> state{};
        for (int coordinate = 0; coordinate < 3; ++coordinate) {
          state[coordinate] =
              kernels.at(parts[coordinate])[spoke_permutation[coordinate]];
        }
        // The fixed part ordering represents all six coordinate orderings;
        // the score pair is invariant under a simultaneous permutation.
        histogram[scores(state)] += 6;
      } while (std::next_permutation(
          spoke_permutation.begin(), spoke_permutation.end()));
    }
  }

  uint64_t total = 0;
  uint64_t closure_good = 0;
  uint64_t parity_good = 0;
  for (const auto& [score, count] : histogram) {
    total += count;
    if (score.first > 0) closure_good += count;
    if (score.second > 0) parity_good += count;
  }
  assert(total == 36 * unordered_partitions);
  assert(unordered_partitions == 158976);
  assert(total == 5723136);
  assert(closure_good == 0);
  assert(parity_good == 40464);
  assert(histogram.size() == 2);
  assert(histogram.at({0, 0}) == 5682672);
  assert(histogram.at({0, 1}) == 40464);

  std::cout << "PASS\n";
  std::cout << "cographic_bases=" << bases.size() << '\n';
  std::cout << "unordered_base_partitions=" << unordered_partitions << '\n';
  std::cout << "ordered_star_packings=" << total << '\n';
  std::cout << "closure_good_packings=" << closure_good << '\n';
  std::cout << "component_parity_good_packings=" << parity_good << '\n';
  std::cout << "histogram=(closure_coordinates,parity_coordinates):";
  for (const auto& [score, count] : histogram) {
    std::cout << " (" << score.first << ',' << score.second
              << ")=" << count;
  }
  std::cout << '\n';
}
