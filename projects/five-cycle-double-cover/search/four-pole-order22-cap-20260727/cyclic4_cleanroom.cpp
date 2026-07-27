// Independently classify cubic graph6 rows by cyclic 4-edge-connectivity.
//
// This implementation does not use cycle-space column signatures.  For each
// edge and each edge pair it runs a fresh Tarjan bridge search after deleting
// those edges.  A bridge after deleting one edge witnesses a 2-edge cut; a
// bridge after deleting two edges witnesses a 3-edge cut.  Vertex-star
// 3-cuts are ignored, since they are the only non-cyclic 3-cuts in a cubic
// graph.

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

struct Graph {
  int vertices = 0;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::vector<std::pair<int, int>>> adjacency;
  std::vector<std::uint64_t> stars;
};

Graph parse_graph6(const std::string& record) {
  if (record.empty() || static_cast<unsigned char>(record[0]) == 126) {
    throw std::runtime_error("only short graph6 records are supported");
  }
  Graph graph;
  graph.vertices = static_cast<unsigned char>(record[0]) - 63;
  if (graph.vertices != 22) {
    throw std::runtime_error("expected order 22");
  }
  std::vector<int> bits;
  for (std::size_t position = 1; position < record.size(); ++position) {
    const int value = static_cast<unsigned char>(record[position]) - 63;
    if (value < 0 || value >= 64) {
      throw std::runtime_error("bad graph6 character");
    }
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }
  const int needed = graph.vertices * (graph.vertices - 1) / 2;
  if (static_cast<int>(bits.size()) < needed) {
    throw std::runtime_error("short graph6 record");
  }
  if (std::any_of(bits.begin() + needed, bits.end(),
                  [](int bit) { return bit != 0; })) {
    throw std::runtime_error("nonzero graph6 padding");
  }
  int cursor = 0;
  for (int right = 1; right < graph.vertices; ++right) {
    for (int left = 0; left < right; ++left) {
      if (bits[cursor]) {
        graph.edges.emplace_back(left, right);
      }
      ++cursor;
    }
  }
  if (graph.edges.size() != 33) {
    throw std::runtime_error("expected 33 edges");
  }
  graph.adjacency.assign(graph.vertices, {});
  graph.stars.assign(graph.vertices, 0);
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    const auto [left, right] = graph.edges[edge];
    graph.adjacency[left].emplace_back(right, edge);
    graph.adjacency[right].emplace_back(left, edge);
    graph.stars[left] |= std::uint64_t{1} << edge;
    graph.stars[right] |= std::uint64_t{1} << edge;
  }
  for (const auto& row : graph.adjacency) {
    if (row.size() != 3) {
      throw std::runtime_error("input is not cubic");
    }
  }
  return graph;
}

class BridgeSearch {
 public:
  explicit BridgeSearch(const Graph& graph)
      : graph_(graph),
        discovery_(graph.vertices),
        low_(graph.vertices),
        bridges_() {}

  const std::vector<int>& after_deleting(std::uint64_t removed) {
    std::fill(discovery_.begin(), discovery_.end(), -1);
    std::fill(low_.begin(), low_.end(), -1);
    bridges_.clear();
    time_ = 0;
    dfs(0, -1, removed);
    if (std::any_of(discovery_.begin(), discovery_.end(),
                    [](int value) { return value < 0; })) {
      disconnected_ = true;
    } else {
      disconnected_ = false;
    }
    return bridges_;
  }

  bool disconnected() const { return disconnected_; }

 private:
  void dfs(int vertex, int parent_edge, std::uint64_t removed) {
    discovery_[vertex] = low_[vertex] = time_++;
    for (const auto [other, edge] : graph_.adjacency[vertex]) {
      if ((removed >> edge) & 1U) {
        continue;
      }
      if (edge == parent_edge) {
        continue;
      }
      if (discovery_[other] < 0) {
        dfs(other, edge, removed);
        low_[vertex] = std::min(low_[vertex], low_[other]);
        if (low_[other] > discovery_[vertex]) {
          bridges_.push_back(edge);
        }
      } else {
        low_[vertex] = std::min(low_[vertex], discovery_[other]);
      }
    }
  }

  const Graph& graph_;
  std::vector<int> discovery_;
  std::vector<int> low_;
  std::vector<int> bridges_;
  int time_ = 0;
  bool disconnected_ = false;
};

bool is_vertex_star(const Graph& graph, std::uint64_t cut) {
  return std::find(graph.stars.begin(), graph.stars.end(), cut) !=
         graph.stars.end();
}

enum class Classification {
  kBridge,
  kTwoCut,
  kNontrivialThreeCut,
  kCyclicallyFour,
};

Classification classify(const Graph& graph) {
  BridgeSearch search(graph);
  const int edges = static_cast<int>(graph.edges.size());

  // The retained hard corpus is supposed to be bridgeless, but verify it.
  const auto& original_bridges = search.after_deleting(0);
  if (search.disconnected() || !original_bridges.empty()) {
    return Classification::kBridge;
  }

  // If G-e has a bridge f, then {e,f} is a 2-edge cut.
  for (int first = 0; first < edges; ++first) {
    const auto& bridges =
        search.after_deleting(std::uint64_t{1} << first);
    if (search.disconnected()) {
      return Classification::kBridge;
    }
    if (!bridges.empty()) {
      return Classification::kTwoCut;
    }
  }

  // If G-{e,f} has a bridge g, then {e,f,g} is a 3-edge cut.
  // Ignore exactly the 22 vertex stars; every other cubic 3-cut is cyclic.
  for (int first = 0; first < edges; ++first) {
    for (int second = first + 1; second < edges; ++second) {
      const std::uint64_t removed =
          (std::uint64_t{1} << first) | (std::uint64_t{1} << second);
      const auto& bridges = search.after_deleting(removed);
      if (search.disconnected()) {
        throw std::runtime_error(
            "pair deletion disconnected after 2-cuts were excluded");
      }
      for (const int third : bridges) {
        const std::uint64_t cut = removed | (std::uint64_t{1} << third);
        if (!is_vertex_star(graph, cut)) {
          return Classification::kNontrivialThreeCut;
        }
      }
    }
  }
  return Classification::kCyclicallyFour;
}

int main() {
  std::uint64_t rows = 0;
  std::array<std::uint64_t, 4> counts{};
  std::string record;
  while (std::getline(std::cin, record)) {
    if (record.empty()) {
      continue;
    }
    ++rows;
    try {
      const Graph graph = parse_graph6(record);
      const Classification result = classify(graph);
      ++counts[static_cast<int>(result)];
      if (result == Classification::kCyclicallyFour) {
        std::cout << record << '\n';
      }
    } catch (const std::exception& error) {
      std::cerr << "ERROR row=" << rows << " message=" << error.what()
                << '\n';
      return 3;
    }
  }
  std::cerr << "SUMMARY rows=" << rows << " bridges=" << counts[0]
            << " two_cut=" << counts[1]
            << " nontrivial_three_cut=" << counts[2]
            << " cyclically_four=" << counts[3] << '\n';
  return 0;
}
