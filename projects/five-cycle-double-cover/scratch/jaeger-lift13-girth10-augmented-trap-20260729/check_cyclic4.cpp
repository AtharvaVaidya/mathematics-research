#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <iterator>
#include <numeric>
#include <regex>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

class DisjointSets {
 public:
  explicit DisjointSets(int order) : parent_(order) {
    std::iota(parent_.begin(), parent_.end(), 0);
  }

  int Find(int item) {
    while (parent_[item] != item) {
      parent_[item] = parent_[parent_[item]];
      item = parent_[item];
    }
    return item;
  }

  void Unite(int first, int second) {
    first = Find(first);
    second = Find(second);
    if (first != second) parent_[first] = second;
  }

 private:
  std::vector<int> parent_;
};

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: check_cyclic4 GRAPH.json\n";
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
  const std::regex edge_pattern("\\\"u\\\":([0-9]+),\\\"v\\\":([0-9]+)");
  std::vector<std::pair<int, int>> edges;
  for (std::sregex_iterator match(text.begin(), text.end(), edge_pattern), end;
       match != end; ++match) {
    edges.emplace_back(std::stoi((*match)[1]), std::stoi((*match)[2]));
  }
  if (edges.size() != 195) {
    std::cerr << "expected 195 edges\n";
    return 1;
  }

  constexpr int kOrder = 130;
  long long three_edge_cuts = 0;
  long long cyclic_three_edge_cuts = 0;
  for (int first = 0; first < 195; ++first) {
    for (int second = first + 1; second < 195; ++second) {
      for (int third = second + 1; third < 195; ++third) {
        DisjointSets components(kOrder);
        for (int edge = 0; edge < 195; ++edge) {
          if (edge != first && edge != second && edge != third) {
            components.Unite(edges[edge].first, edges[edge].second);
          }
        }
        std::unordered_map<int, int> vertex_count;
        std::unordered_map<int, int> internal_edge_count;
        for (int vertex = 0; vertex < kOrder; ++vertex) {
          ++vertex_count[components.Find(vertex)];
        }
        if (vertex_count.size() == 1) continue;
        ++three_edge_cuts;
        for (int edge = 0; edge < 195; ++edge) {
          if (edge != first && edge != second && edge != third) {
            ++internal_edge_count[components.Find(edges[edge].first)];
          }
        }
        int cyclic_components = 0;
        for (const auto& [root, vertices] : vertex_count) {
          if (internal_edge_count[root] >= vertices) ++cyclic_components;
        }
        if (cyclic_components >= 2) ++cyclic_three_edge_cuts;
      }
    }
  }
  std::cout << "three_edge_cuts=" << three_edge_cuts
            << " cyclic_three_edge_cuts=" << cyclic_three_edge_cuts << '\n';
  return cyclic_three_edge_cuts == 0 ? 0 : 1;
}
