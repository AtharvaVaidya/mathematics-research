// Independent replay of the universal four-edge-separation screen.
//
// This implementation deliberately does not reuse the producer's
// edge-colouring recursion.  It enumerates perfect matchings.  For each
// perfect matching M, the complementary two-factor can be split into the
// other two colour classes exactly when every component is even.  All
// independent alternating choices are enumerated.  Every Tait colouring
// modulo a global S3 colour permutation is visited six times: three choices
// for M and two orders for the complementary colour classes.
//
// Build:
//   c++ -O3 -std=c++17 scratch/verify_order22_separation_via_matchings.cpp \
//       -o scratch/verify_order22_separation_via_matchings
//
// Complete order-22 replay:
//   for r in 0 1 2 3; do
//     geng -cq -d3 -D3 22 "$r/4" |
//       scratch/verify_order22_separation_via_matchings \
//         --target 4 --stop-after-first --progress 250000
//   done

#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int kMaximumEdges = 64;

struct Graph {
  int n = 0;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::array<int, 3>> incident;
};

Graph parse_graph6(const std::string &line) {
  if (line.empty() || line[0] == ':' || line[0] == '>') {
    throw std::runtime_error("unsupported graph6 record");
  }
  const int n = static_cast<unsigned char>(line[0]) - 63;
  if (n < 0 || n > 62) {
    throw std::runtime_error("only short graph6 headers are supported");
  }
  Graph graph;
  graph.n = n;
  std::vector<std::vector<int>> temporary(n);
  int bit = 0;
  for (int v = 1; v < n; ++v) {
    for (int u = 0; u < v; ++u, ++bit) {
      const int index = 1 + bit / 6;
      if (index >= static_cast<int>(line.size())) {
        throw std::runtime_error("truncated graph6 record");
      }
      const int value = static_cast<unsigned char>(line[index]) - 63;
      if (value < 0 || value > 63) {
        throw std::runtime_error("invalid graph6 byte");
      }
      if ((value >> (5 - bit % 6)) & 1) {
        const int edge = static_cast<int>(graph.edges.size());
        graph.edges.push_back({u, v});
        temporary[u].push_back(edge);
        temporary[v].push_back(edge);
      }
    }
  }
  if (graph.edges.size() > kMaximumEdges) {
    throw std::runtime_error("edge limit exceeded");
  }
  graph.incident.resize(n);
  for (int v = 0; v < n; ++v) {
    if (temporary[v].size() != 3) {
      throw std::runtime_error("input is not cubic");
    }
    for (int i = 0; i < 3; ++i) graph.incident[v][i] = temporary[v][i];
  }
  return graph;
}

struct MatchingReplay {
  const Graph &graph;
  const int edge_count;
  std::vector<std::bitset<kMaximumEdges>> conflict;
  uint64_t colouring_visits = 0;
  uint64_t perfect_matchings = 0;

  explicit MatchingReplay(const Graph &input)
      : graph(input), edge_count(static_cast<int>(input.edges.size())),
        conflict(edge_count) {
    for (int edge = 0; edge < edge_count; ++edge) {
      const auto [u, v] = graph.edges[edge];
      for (int adjacent : graph.incident[u]) {
        if (adjacent != edge) conflict[edge].set(adjacent);
      }
      for (int adjacent : graph.incident[v]) {
        if (adjacent != edge) conflict[edge].set(adjacent);
      }
    }
  }

  void add_factor_conflicts(const std::vector<int> &colour, int omitted) {
    std::vector<char> seen(edge_count, 0);
    for (int start = 0; start < edge_count; ++start) {
      if (colour[start] == omitted || seen[start]) continue;
      std::bitset<kMaximumEdges> component;
      std::vector<int> stack = {start};
      seen[start] = 1;
      while (!stack.empty()) {
        const int edge = stack.back();
        stack.pop_back();
        component.set(edge);
        const auto [u, v] = graph.edges[edge];
        for (const int vertex : {u, v}) {
          for (int next : graph.incident[vertex]) {
            if (colour[next] == omitted || seen[next]) continue;
            seen[next] = 1;
            stack.push_back(next);
          }
        }
      }
      for (int edge = 0; edge < edge_count; ++edge) {
        if (!component.test(edge)) continue;
        conflict[edge] |= component;
        conflict[edge].reset(edge);
      }
    }
  }

  void record_colouring(uint64_t matching,
                        const std::vector<std::vector<int>> &cycles,
                        uint64_t orientation) {
    std::vector<int> colour(edge_count, -1);
    for (int edge = 0; edge < edge_count; ++edge) {
      if ((matching >> edge) & 1ULL) colour[edge] = 0;
    }
    for (int index = 0; index < static_cast<int>(cycles.size()); ++index) {
      int next_colour = ((orientation >> index) & 1ULL) ? 1 : 2;
      for (int edge : cycles[index]) {
        colour[edge] = next_colour;
        next_colour = 3 - next_colour;
      }
    }
    for (int edge = 0; edge < edge_count; ++edge) {
      if (colour[edge] < 0) {
        throw std::runtime_error("incomplete reconstructed colouring");
      }
    }
    ++colouring_visits;
    for (int omitted = 0; omitted < 3; ++omitted) {
      add_factor_conflicts(colour, omitted);
    }
  }

  void process_matching(uint64_t matching) {
    ++perfect_matchings;
    std::vector<char> seen(edge_count, 0);
    std::vector<std::vector<int>> cycles;
    for (int start = 0; start < edge_count; ++start) {
      if ((matching >> start) & 1ULL || seen[start]) continue;
      std::vector<int> cycle;
      int edge = start;
      int previous_vertex = -1;
      while (true) {
        if (seen[edge]) {
          if (edge != start) {
            throw std::runtime_error("malformed complementary two-factor");
          }
          break;
        }
        seen[edge] = 1;
        cycle.push_back(edge);
        const auto [u, v] = graph.edges[edge];
        const int next_vertex =
            previous_vertex == -1 ? v : (u == previous_vertex ? v : u);
        int next_edge = -1;
        for (int candidate : graph.incident[next_vertex]) {
          if (candidate == edge || ((matching >> candidate) & 1ULL)) continue;
          next_edge = candidate;
          break;
        }
        if (next_edge == -1) {
          throw std::runtime_error("complement is not two-regular");
        }
        previous_vertex = next_vertex;
        edge = next_edge;
      }
      if (cycle.size() % 2 != 0) return;
      cycles.push_back(std::move(cycle));
    }
    if (cycles.size() >= 63) {
      throw std::runtime_error("too many complementary cycles");
    }
    const uint64_t choices = 1ULL << cycles.size();
    for (uint64_t choice = 0; choice < choices; ++choice) {
      record_colouring(matching, cycles, choice);
    }
  }

  void enumerate_matchings(uint64_t matched_vertices, uint64_t matching) {
    const uint64_t full =
        graph.n == 64 ? ~uint64_t{0} : ((1ULL << graph.n) - 1);
    if (matched_vertices == full) {
      process_matching(matching);
      return;
    }
    int vertex = 0;
    while ((matched_vertices >> vertex) & 1ULL) ++vertex;
    for (int edge : graph.incident[vertex]) {
      const auto [u, v] = graph.edges[edge];
      const int other = u ^ v ^ vertex;
      if ((matched_vertices >> other) & 1ULL) continue;
      enumerate_matchings(matched_vertices | (1ULL << vertex) |
                                               (1ULL << other),
                          matching | (1ULL << edge));
    }
  }

  void run() { enumerate_matchings(0, 0); }
};

bool find_independent(
    const std::vector<std::bitset<kMaximumEdges>> &conflict, int target,
    int next, std::vector<int> &chosen) {
  if (static_cast<int>(chosen.size()) == target) return true;
  const int edge_count = static_cast<int>(conflict.size());
  const int need = target - static_cast<int>(chosen.size());
  for (int edge = next; edge + need <= edge_count; ++edge) {
    bool allowed = true;
    for (int previous : chosen) {
      if (conflict[edge].test(previous)) {
        allowed = false;
        break;
      }
    }
    if (!allowed) continue;
    chosen.push_back(edge);
    if (find_independent(conflict, target, edge + 1, chosen)) return true;
    chosen.pop_back();
  }
  return false;
}

}  // namespace

int main(int argc, char **argv) {
  int target = 4;
  uint64_t progress = 250000;
  bool stop_after_first = false;
  for (int i = 1; i < argc; ++i) {
    const std::string argument = argv[i];
    if (argument == "--target" && i + 1 < argc) {
      target = std::atoi(argv[++i]);
    } else if (argument == "--progress" && i + 1 < argc) {
      progress = std::strtoull(argv[++i], nullptr, 10);
    } else if (argument == "--stop-after-first") {
      stop_after_first = true;
    } else {
      std::cerr << "usage: " << argv[0]
                << " [--target n] [--progress n] [--stop-after-first]\n";
      return 2;
    }
  }

  uint64_t rows = 0;
  uint64_t tait = 0;
  uint64_t witnesses = 0;
  uint64_t colouring_visits = 0;
  uint64_t perfect_matchings = 0;
  std::string line;
  while (std::getline(std::cin, line)) {
    if (line.empty() || line.rfind(">>", 0) == 0) continue;
    ++rows;
    Graph graph;
    try {
      graph = parse_graph6(line);
      MatchingReplay replay(graph);
      replay.run();
      colouring_visits += replay.colouring_visits;
      perfect_matchings += replay.perfect_matchings;
      if (replay.colouring_visits == 0) continue;
      if (replay.colouring_visits % 6 != 0) {
        throw std::runtime_error("colouring visit count is not divisible by 6");
      }
      ++tait;
      std::vector<int> chosen;
      if (find_independent(replay.conflict, target, 0, chosen)) {
        ++witnesses;
        std::cout << "{\"row\":" << rows << ",\"graph6\":\"" << line
                  << "\",\"order\":" << graph.n << ",\"marks\":[";
        for (int i = 0; i < target; ++i) {
          if (i) std::cout << ",";
          std::cout << chosen[i];
        }
        std::cout << "]}\n";
        if (stop_after_first) {
          std::cerr << "STOP rows=" << rows << " tait=" << tait
                    << " colourings_mod_s3=" << colouring_visits / 6
                    << " perfect_matchings=" << perfect_matchings
                    << " witnesses=" << witnesses << "\n";
          return 0;
        }
      }
    } catch (const std::exception &error) {
      std::cerr << "error at row " << rows << ": " << error.what() << "\n";
      return 2;
    }
    if (progress && rows % progress == 0) {
      std::cerr << "rows=" << rows << " tait=" << tait
                << " colourings_mod_s3=" << colouring_visits / 6
                << " perfect_matchings=" << perfect_matchings
                << " witnesses=" << witnesses << "\n";
    }
  }
  if (colouring_visits % 6 != 0) {
    std::cerr << "global colouring visit count is not divisible by 6\n";
    return 2;
  }
  std::cerr << "FINAL rows=" << rows << " tait=" << tait
            << " colourings_mod_s3=" << colouring_visits / 6
            << " perfect_matchings=" << perfect_matchings
            << " witnesses=" << witnesses << " target=" << target << "\n";
  return 0;
}
