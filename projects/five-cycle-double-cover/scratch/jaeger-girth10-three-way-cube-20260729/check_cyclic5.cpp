#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <iterator>
#include <regex>
#include <set>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int kOrder = 130;
constexpr int kEdges = 195;

struct ComponentData {
  int components;
  int cyclic_components;
};

ComponentData Classify(
    const std::array<std::vector<std::pair<int, int>>, kOrder>& adjacency,
    const std::vector<std::pair<int, int>>& edges,
    const std::array<int, 4>& cut,
    int cut_size) {
  std::array<int, kOrder> component;
  component.fill(-1);
  int count = 0;
  for (int source = 0; source < kOrder; ++source) {
    if (component[source] >= 0) continue;
    component[source] = count;
    std::vector<int> stack{source};
    while (!stack.empty()) {
      const int vertex = stack.back();
      stack.pop_back();
      for (const auto [other, edge] : adjacency[vertex]) {
        bool removed = false;
        for (int index = 0; index < cut_size; ++index) {
          if (edge == cut[index]) removed = true;
        }
        if (!removed && component[other] < 0) {
          component[other] = count;
          stack.push_back(other);
        }
      }
    }
    ++count;
  }
  std::vector<int> vertices(count);
  std::vector<int> internal_edges(count);
  for (int vertex = 0; vertex < kOrder; ++vertex) {
    ++vertices[component[vertex]];
  }
  for (int edge = 0; edge < kEdges; ++edge) {
    bool removed = false;
    for (int index = 0; index < cut_size; ++index) {
      if (edge == cut[index]) removed = true;
    }
    if (!removed &&
        component[edges[edge].first] == component[edges[edge].second]) {
      ++internal_edges[component[edges[edge].first]];
    }
  }
  int cyclic = 0;
  for (int index = 0; index < count; ++index) {
    if (internal_edges[index] >= vertices[index]) ++cyclic;
  }
  return {count, cyclic};
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: check_cyclic5 GRAPH.json\n";
    return 2;
  }
  std::ifstream input(argv[1]);
  if (!input) {
    std::cerr << "cannot read graph\n";
    return 2;
  }
  const std::string text(
      (std::istreambuf_iterator<char>(input)),
      std::istreambuf_iterator<char>());
  const std::regex edge_pattern(
      "\\\"u\\\":([0-9]+),\\\"v\\\":([0-9]+)");
  std::vector<std::pair<int, int>> edges;
  for (std::sregex_iterator match(
           text.begin(), text.end(), edge_pattern), end;
       match != end; ++match) {
    edges.emplace_back(
        std::stoi((*match)[1]), std::stoi((*match)[2]));
  }
  if (edges.size() != kEdges) {
    std::cerr << "expected 195 edges\n";
    return 1;
  }

  std::array<std::vector<std::pair<int, int>>, kOrder> adjacency;
  for (int edge = 0; edge < kEdges; ++edge) {
    const auto [left, right] = edges[edge];
    adjacency[left].push_back({right, edge});
    adjacency[right].push_back({left, edge});
  }

  long long triples = 0;
  long long three_edge_cuts = 0;
  long long cyclic_three_edge_cuts = 0;
  long long bridge_occurrences = 0;
  std::set<std::array<int, 4>> four_edge_cuts;
  std::array<int, kOrder> discovery;
  std::array<int, kOrder> low;
  std::array<char, kEdges> deleted;

  for (int first = 0; first < kEdges; ++first) {
    for (int second = first + 1; second < kEdges; ++second) {
      for (int third = second + 1; third < kEdges; ++third) {
        ++triples;
        deleted.fill(0);
        deleted[first] = deleted[second] = deleted[third] = 1;
        discovery.fill(-1);
        int timer = 0;
        int depth_first_roots = 0;
        std::vector<int> bridges;
        const auto visit = [&](auto&& self, int vertex, int parent_edge)
            -> void {
          discovery[vertex] = low[vertex] = timer++;
          for (const auto [other, edge] : adjacency[vertex]) {
            if (deleted[edge] || edge == parent_edge) continue;
            if (discovery[other] >= 0) {
              low[vertex] = std::min(
                  low[vertex], discovery[other]);
            } else {
              self(self, other, edge);
              low[vertex] = std::min(low[vertex], low[other]);
              if (low[other] > discovery[vertex]) {
                bridges.push_back(edge);
              }
            }
          }
        };
        for (int vertex = 0; vertex < kOrder; ++vertex) {
          if (discovery[vertex] < 0) {
            ++depth_first_roots;
            visit(visit, vertex, -1);
          }
        }

        const std::array<int, 4> triple{
            first, second, third, -1};
        if (depth_first_roots > 1) {
          ++three_edge_cuts;
          const ComponentData data = Classify(
              adjacency, edges, triple, 3);
          if (data.cyclic_components >= 2) {
            ++cyclic_three_edge_cuts;
          }
        }

        for (const int fourth : bridges) {
          ++bridge_occurrences;
          std::array<int, 4> cut{
              first, second, third, fourth};
          std::sort(cut.begin(), cut.end());
          if (!four_edge_cuts.insert(cut).second) continue;
          const ComponentData data = Classify(
              adjacency, edges, cut, 4);
          if (data.cyclic_components >= 2) {
            std::cout << "FAIL cyclic_four_cut";
            for (const int edge : cut) std::cout << ' ' << edge;
            std::cout << '\n';
            return 1;
          }
        }
      }
    }
  }

  std::cout
      << "PASS triples=" << triples
      << " three_edge_cuts=" << three_edge_cuts
      << " cyclic_three_edge_cuts=" << cyclic_three_edge_cuts
      << " bridge_occurrences=" << bridge_occurrences
      << " distinct_four_edge_cuts=" << four_edge_cuts.size()
      << " cyclic_four_edge_cuts=0\n";
  return cyclic_three_edge_cuts == 0 ? 0 : 1;
}
