// Randomized exact-neighbour search for strict local minima of the symmetric
// seven-Fano-plane defect in Jaeger vertex-star fibres.
//
// A reported STRICT_TRAP is a rigorous counterexample to the proposed
// same-level descent theorem: every reciprocal exchange incident with the
// displayed positive state has strictly larger d_min.  A clean run is only
// exploratory because states are sampled by random walk.
//
// Build:
//   clang++ -O3 -std=c++20 -I/opt/homebrew/include \
//     scratch/search_jaeger_star_symmetric_local_traps.cpp \
//     /opt/homebrew/lib/libcadical.a -o /tmp/search_symmetric_local_traps
//
// Usage:
//   search_symmetric_local_traps [steps-per-root] [seed] [root]
//       [level|kernel] < graph6-stream
//
// Omit root (or pass -1) to inspect every root.  A fixed root is useful for
// broad randomized scans of large canonical snark collections.  The default
// `level` replay follows every same-d_min exchange.  The stronger `kernel`
// replay follows only exchanges preserving all three odd kernels and asks
// whether that neutral realization component exposes a descending exchange.

#define JAEGER_FIXED_FIBRE_NO_MAIN
#include "search_jaeger_fixed_fibre_sat.cpp"

#include <deque>
#include <limits>
#include <random>
#include <unordered_set>

namespace {

using WideMask = std::uint64_t;

Graph parse_graph6_local(std::string record) {
  const std::string header = ">>graph6<<";
  if (record.rfind(header, 0) == 0) record.erase(0, header.size());
  if (record.empty() || record[0] == '~') {
    throw std::runtime_error("only short graph6 records are supported");
  }
  Graph graph;
  graph.n = static_cast<unsigned char>(record[0]) - 63;
  if (graph.n < 1 || graph.n > 42) {
    throw std::runtime_error("graph order outside local-search range");
  }
  std::vector<int> bits;
  for (std::size_t index = 1; index < record.size(); ++index) {
    const int value = static_cast<unsigned char>(record[index]) - 63;
    if (value < 0 || value >= 64) throw std::runtime_error("bad graph6 byte");
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }
  int cursor = 0;
  for (int right = 1; right < graph.n; ++right) {
    for (int left = 0; left < right; ++left) {
      if (bits.at(cursor)) graph.edges.push_back({left, right});
      ++cursor;
    }
  }
  graph.incidence.assign(graph.n, {});
  for (int edge = 0; edge < graph.m(); ++edge) {
    graph.incidence[graph.edges[edge][0]].push_back(edge);
    graph.incidence[graph.edges[edge][1]].push_back(edge);
  }
  return graph;
}

bool is_tree_wide(const Graph& graph, WideMask tree) {
  if (__builtin_popcountll(tree) != graph.n - 1) return false;
  std::vector<int> parent(graph.n);
  std::iota(parent.begin(), parent.end(), 0);
  const auto find = [&](int vertex, const auto& self) -> int {
    if (parent[vertex] == vertex) return vertex;
    return parent[vertex] = self(parent[vertex], self);
  };
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (!((tree >> edge) & 1ULL)) continue;
    int left = find(graph.edges[edge][0], find);
    int right = find(graph.edges[edge][1], find);
    if (left == right) return false;
    parent[left] = right;
  }
  return true;
}

WideMask odd_kernel_wide(const Graph& graph, WideMask tree) {
  std::vector<std::vector<std::pair<int, int>>> adjacency(graph.n);
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (!((tree >> edge) & 1ULL)) continue;
    const int left = graph.edges[edge][0];
    const int right = graph.edges[edge][1];
    adjacency[left].emplace_back(right, edge);
    adjacency[right].emplace_back(left, edge);
  }
  std::vector<int> parent(graph.n, -1);
  std::vector<int> parent_edge(graph.n, -1);
  std::vector<int> traversal{0};
  parent[0] = 0;
  for (std::size_t cursor = 0; cursor < traversal.size(); ++cursor) {
    const int vertex = traversal[cursor];
    for (const auto [other, edge] : adjacency[vertex]) {
      if (parent[other] >= 0) continue;
      parent[other] = vertex;
      parent_edge[other] = edge;
      traversal.push_back(other);
    }
  }
  if (static_cast<int>(traversal.size()) != graph.n) {
    throw std::runtime_error("odd kernel received a disconnected tree");
  }
  std::vector<int> size(graph.n, 1);
  WideMask answer = 0;
  for (int cursor = graph.n - 1; cursor >= 1; --cursor) {
    const int vertex = traversal[cursor];
    if (size[vertex] & 1) answer |= 1ULL << parent_edge[vertex];
    size[parent[vertex]] += size[vertex];
  }
  return answer;
}

std::array<int, 7> exact_profile(
    const Graph& graph, const std::array<WideMask, 3>& kernels) {
  std::vector<unsigned char> flow(graph.m(), 0);
  for (int edge = 0; edge < graph.m(); ++edge) {
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      if (!((kernels[coordinate] >> edge) & 1ULL)) {
        flow[edge] |= 1 << coordinate;
      }
    }
    if (flow[edge] == 0) {
      throw std::runtime_error("zero edge in derived flow");
    }
  }
  std::vector<unsigned char> normal(graph.n, 0);
  for (int vertex = 0; vertex < graph.n; ++vertex) {
    for (int candidate = 1; candidate < 8; ++candidate) {
      bool annihilates = true;
      for (const int edge : graph.incidence[vertex]) {
        annihilates &=
            (__builtin_popcount(candidate & flow[edge]) & 1) == 0;
      }
      if (!annihilates) continue;
      if (normal[vertex]) {
        throw std::runtime_error("nonunique incident-plane normal");
      }
      normal[vertex] = candidate;
    }
    if (!normal[vertex]) {
      throw std::runtime_error("missing incident-plane normal");
    }
  }

  std::array<int, 7> profile{};
  for (int functional = 1; functional < 8; ++functional) {
    std::vector<int> parent(graph.n);
    std::iota(parent.begin(), parent.end(), 0);
    const auto find = [&](int vertex, const auto& self) -> int {
      if (parent[vertex] == vertex) return vertex;
      return parent[vertex] = self(parent[vertex], self);
    };
    std::vector<int> degree(graph.n, 0);
    for (int edge = 0; edge < graph.m(); ++edge) {
      if (__builtin_popcount(functional & flow[edge]) & 1) continue;
      const int left = graph.edges[edge][0];
      const int right = graph.edges[edge][1];
      ++degree[left];
      ++degree[right];
      int first = find(left, find);
      int second = find(right, find);
      if (first != second) parent[first] = second;
    }
    const int transverse = 1 << __builtin_ctz(functional);
    std::vector<unsigned char> parity(graph.n, 0);
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      if (degree[vertex] != 1 && degree[vertex] != 3) {
        throw std::runtime_error("zero-plane degree is not one or three");
      }
      if (degree[vertex] == 1) {
        parity[find(vertex, find)] ^=
            __builtin_popcount(
                (normal[vertex] ^ functional) & transverse) &
            1;
      }
    }
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      if (find(vertex, find) == vertex && parity[vertex]) {
        ++profile[functional - 1];
      }
    }
  }
  return profile;
}

int minimum_score(const std::array<int, 7>& profile) {
  return *std::min_element(profile.begin(), profile.end());
}

struct StarState {
  std::array<WideMask, 3> omitted{};

  bool operator==(const StarState& other) const {
    return omitted == other.omitted;
  }
};

struct StarStateHash {
  std::size_t operator()(const StarState& state) const {
    std::uint64_t value = 1469598103934665603ULL;
    for (const WideMask mask : state.omitted) {
      value ^= mask;
      value *= 1099511628211ULL;
      value ^= mask >> 32;
      value *= 1099511628211ULL;
    }
    return static_cast<std::size_t>(value);
  }
};

struct RootModel {
  std::vector<int> internal;
  std::array<int, 3> spoke{};
  WideMask all_internal = 0;
  StarState initial;
};

RootModel feasible_root_model(const Graph& graph, int root) {
  if (graph.m() > 63) throw std::runtime_error("too many edges");
  const Encoding encoding = encode(graph, false);
  Incremental solver(encoding.formula);
  std::vector<int> multiplicity(graph.m(), 2);
  for (const int edge : graph.incidence[root]) multiplicity[edge] = 1;
  if (solver.solve(encoding, multiplicity) != 10) {
    throw std::runtime_error("vertex-star fibre is infeasible");
  }
  // The fixed-fibre source predates this randomized frontier and exposes a
  // 32-bit convenience extractor.  Reconstruct the SAT model directly here
  // so that the local search remains exact for every cubic graph with at
  // most 42 vertices (and hence at most 63 edges).
  std::array<WideMask, 3> tree_model{};
  for (int edge = 0; edge < graph.m(); ++edge) {
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      if (solver.solver.val(encoding.tree[edge][coordinate]) > 0) {
        tree_model[coordinate] |= WideMask{1} << edge;
      }
    }
  }
  RootModel model;
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (multiplicity[edge] == 2) model.internal.push_back(edge);
  }
  const int internal_count = model.internal.size();
  model.all_internal = (1ULL << internal_count) - 1;
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    int spoke = -1;
    for (const int edge : graph.incidence[root]) {
      if ((tree_model[coordinate] >> edge) & 1ULL) {
        if (spoke >= 0) throw std::runtime_error("two spokes in one tree");
        spoke = edge;
      }
    }
    if (spoke < 0) throw std::runtime_error("tree has no spoke");
    model.spoke[coordinate] = spoke;
    for (int local = 0; local < internal_count; ++local) {
      if (!((tree_model[coordinate] >> model.internal[local]) & 1ULL)) {
        model.initial.omitted[coordinate] |= 1ULL << local;
      }
    }
  }
  if ((model.initial.omitted[0] ^ model.initial.omitted[1] ^
       model.initial.omitted[2]) != model.all_internal) {
    throw std::runtime_error("omitted classes do not partition");
  }
  return model;
}

std::array<WideMask, 3> trees_of(
    const RootModel& model, const StarState& state) {
  std::array<WideMask, 3> trees{};
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    trees[coordinate] |= 1ULL << model.spoke[coordinate];
    WideMask present = model.all_internal ^ state.omitted[coordinate];
    while (present) {
      const int local = __builtin_ctzll(present);
      present &= present - 1;
      trees[coordinate] |= 1ULL << model.internal[local];
    }
  }
  return trees;
}

std::array<int, 7> profile_of(
    const Graph& graph, const RootModel& model, const StarState& state) {
  const auto trees = trees_of(model, state);
  std::array<WideMask, 3> kernels{};
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    if (!is_tree_wide(graph, trees[coordinate])) {
      throw std::runtime_error("invalid state tree");
    }
    kernels[coordinate] = odd_kernel_wide(graph, trees[coordinate]);
  }
  return exact_profile(graph, kernels);
}

std::array<WideMask, 3> kernels_of(
    const Graph& graph, const RootModel& model, const StarState& state) {
  const auto trees = trees_of(model, state);
  std::array<WideMask, 3> kernels{};
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    if (!is_tree_wide(graph, trees[coordinate])) {
      throw std::runtime_error("invalid state tree");
    }
    kernels[coordinate] = odd_kernel_wide(graph, trees[coordinate]);
  }
  return kernels;
}

std::vector<StarState> neighbours(
    const Graph& graph, const RootModel& model, const StarState& state) {
  std::vector<StarState> answer;
  for (int first = 0; first < 3; ++first) {
    for (int second = first + 1; second < 3; ++second) {
      WideMask first_edges = state.omitted[first];
      while (first_edges) {
        const int a = __builtin_ctzll(first_edges);
        first_edges &= first_edges - 1;
        WideMask second_edges = state.omitted[second];
        while (second_edges) {
          const int b = __builtin_ctzll(second_edges);
          second_edges &= second_edges - 1;
          StarState changed = state;
          const WideMask toggle = (1ULL << a) | (1ULL << b);
          changed.omitted[first] ^= toggle;
          changed.omitted[second] ^= toggle;
          const auto changed_trees = trees_of(model, changed);
          if (is_tree_wide(graph, changed_trees[first]) &&
              is_tree_wide(graph, changed_trees[second])) {
            answer.push_back(changed);
          }
        }
      }
    }
  }
  return answer;
}

void print_profile(const std::array<int, 7>& profile) {
  std::cout << '[';
  for (int index = 0; index < 7; ++index) {
    if (index) std::cout << ',';
    std::cout << profile[index];
  }
  std::cout << ']';
}

std::string json_escape(const std::string& text) {
  std::string answer;
  answer.reserve(text.size() + 4);
  for (const char character : text) {
    if (character == '\\' || character == '"') answer.push_back('\\');
    answer.push_back(character);
  }
  return answer;
}

}  // namespace

int main(int argc, char** argv) {
  const int steps = argc >= 2 ? std::atoi(argv[1]) : 10000;
  const std::uint64_t seed =
      argc >= 3 ? std::strtoull(argv[2], nullptr, 10) : 1;
  const int requested_root = argc >= 4 ? std::atoi(argv[3]) : -1;
  const std::string replay_mode = argc >= 5 ? argv[4] : "level";
  if (replay_mode != "level" && replay_mode != "kernel") {
    throw std::runtime_error("replay mode must be level or kernel");
  }
  std::mt19937_64 random(seed);
  std::string graph6;
  int graph_index = 0;
  std::uint64_t sampled_states = 0;
  while (std::getline(std::cin, graph6)) {
    if (graph6.empty()) continue;
    const Graph graph = parse_graph6_local(graph6);
    if (!is_cubic_connected(graph) || !is_bridgeless(graph) ||
        graph.m() > 63) {
      ++graph_index;
      continue;
    }
    const int first_root = requested_root < 0 ? 0 : requested_root;
    const int last_root = requested_root < 0 ? graph.n : requested_root + 1;
    if (first_root < 0 || last_root > graph.n) {
      throw std::runtime_error("requested root is outside the graph");
    }
    for (int root = first_root; root < last_root; ++root) {
      RootModel model = feasible_root_model(graph, root);
      StarState state = model.initial;
      std::unordered_set<StarState, StarStateHash> seen;
      std::unordered_set<StarState, StarStateHash> escaped_plateau_states;
      std::uint64_t positive_sampled = 0;
      std::uint64_t plateau_replays = 0;
      std::size_t largest_replayed_plateau = 0;
      int largest_escape_distance = 0;
      int smallest_neutral_degree = std::numeric_limits<int>::max();
      StarState smallest_neutral_witness;
      std::array<int, 7> smallest_neutral_profile{};
      StarState largest_plateau_witness;
      std::array<int, 7> largest_plateau_profile{};
      int largest_plateau_score = 0;
      for (int step = 0; step < steps; ++step) {
        if (seen.insert(state).second) {
          ++sampled_states;
          const auto profile = profile_of(graph, model, state);
          const int score = minimum_score(profile);
          positive_sampled += score > 0;
          const auto next = neighbours(graph, model, state);
          int lower = 0;
          int equal = 0;
          int higher = 0;
          std::vector<int> next_scores;
          next_scores.reserve(next.size());
          for (const auto& neighbour : next) {
            const int neighbour_score =
                minimum_score(profile_of(graph, model, neighbour));
            next_scores.push_back(neighbour_score);
            lower += neighbour_score < score;
            equal += neighbour_score == score;
            higher += neighbour_score > score;
          }
          if (score > 0 && lower == 0 && equal == 0) {
            std::cout << "{\"status\":\"STRICT_TRAP\","
                      << "\"graph_index\":" << graph_index << ','
                      << "\"graph6\":\"" << json_escape(graph6) << "\","
                      << "\"root\":" << root << ','
                      << "\"step\":" << step << ','
                      << "\"score\":" << score << ','
                      << "\"profile\":";
            print_profile(profile);
            std::cout << ",\"omitted\":["
                      << state.omitted[0] << ','
                      << state.omitted[1] << ','
                      << state.omitted[2] << "],"
                      << "\"legal_neighbours\":" << next.size() << ','
                      << "\"higher_neighbours\":" << higher << "}\n";
            return 1;
          }
          if (score > 0 && lower == 0 &&
              equal < smallest_neutral_degree) {
            smallest_neutral_degree = equal;
            smallest_neutral_witness = state;
            smallest_neutral_profile = profile;
          }
          if (score > 0 && lower == 0 && equal > 0 &&
              !escaped_plateau_states.contains(state)) {
            ++plateau_replays;
            constexpr std::size_t plateau_limit = 100000;
            const auto initial_kernels =
                replay_mode == "kernel"
                    ? kernels_of(graph, model, state)
                    : std::array<WideMask, 3>{};
            std::unordered_set<StarState, StarStateHash> plateau_seen;
            std::deque<std::pair<StarState, int>> queue;
            plateau_seen.insert(state);
            queue.emplace_back(state, 0);
            bool escaped = false;
            bool truncated = false;
            int escape_distance = -1;
            while (!queue.empty() && !escaped) {
              const StarState current = queue.front().first;
              const int distance = queue.front().second;
              queue.pop_front();
              for (const StarState& neighbour :
                   neighbours(graph, model, current)) {
                const int neighbour_score =
                    minimum_score(profile_of(graph, model, neighbour));
                if (neighbour_score < score) {
                  escaped = true;
                  escape_distance = distance + 1;
                  break;
                }
                const bool replay_neighbour =
                    replay_mode == "level"
                        ? neighbour_score == score
                        : kernels_of(graph, model, neighbour) ==
                              initial_kernels;
                if (replay_neighbour &&
                    plateau_seen.insert(neighbour).second) {
                  queue.emplace_back(neighbour, distance + 1);
                  if (plateau_seen.size() > plateau_limit) {
                    truncated = true;
                    break;
                  }
                }
              }
              if (truncated) break;
            }
            if (!escaped && !truncated) {
              std::cout << "{\"status\":\""
                        << (replay_mode == "level"
                                ? "PLATEAU_TRAP"
                                : "KERNEL_EXPOSURE_TRAP")
                        << "\","
                        << "\"graph_index\":" << graph_index << ','
                        << "\"graph6\":\"" << json_escape(graph6) << "\","
                        << "\"root\":" << root << ','
                        << "\"step\":" << step << ','
                        << "\"score\":" << score << ','
                        << "\"profile\":";
              print_profile(profile);
              std::cout << ",\"omitted\":["
                        << state.omitted[0] << ','
                        << state.omitted[1] << ','
                        << state.omitted[2] << "],"
                        << "\"same_level_component_size\":"
                        << plateau_seen.size() << "}\n";
              return 1;
            }
            if (plateau_seen.size() > largest_replayed_plateau) {
              largest_replayed_plateau = plateau_seen.size();
              largest_plateau_witness = state;
              largest_plateau_profile = profile;
              largest_plateau_score = score;
            }
            largest_escape_distance =
                std::max(largest_escape_distance, escape_distance);
            if (escaped) {
              escaped_plateau_states.insert(
                  plateau_seen.begin(), plateau_seen.end());
            }
          }
        }
        auto next = neighbours(graph, model, state);
        if (next.empty()) throw std::runtime_error("isolated packing state");
        // Bias half the steps toward larger d_min to spend more time near
        // potential positive traps; otherwise retain an ordinary random walk.
        if ((random() & 1ULL) == 0) {
          state = next[random() % next.size()];
        } else {
          int best = -1;
          std::vector<int> best_indices;
          for (int index = 0; index < static_cast<int>(next.size()); ++index) {
            const int candidate =
                minimum_score(profile_of(graph, model, next[index]));
            if (candidate > best) {
              best = candidate;
              best_indices.clear();
            }
            if (candidate == best) best_indices.push_back(index);
          }
          state = next[best_indices[random() % best_indices.size()]];
        }
      }
      std::cout << "{\"status\":\"ROOT_DONE\","
                << "\"graph_index\":" << graph_index << ','
                << "\"graph6\":\"" << json_escape(graph6) << "\","
                << "\"root\":" << root << ','
                << "\"spokes\":[" << model.spoke[0] << ','
                << model.spoke[1] << ',' << model.spoke[2] << "],"
                << "\"replay_mode\":\"" << replay_mode << "\","
                << "\"steps\":" << steps << ','
                << "\"distinct_states\":" << seen.size() << ','
                << "\"positive_sampled\":" << positive_sampled << ','
                << "\"plateau_replays\":" << plateau_replays << ','
                << "\"largest_replayed_plateau\":"
                << largest_replayed_plateau << ','
                << "\"largest_escape_distance\":"
                << largest_escape_distance;
      if (smallest_neutral_degree != std::numeric_limits<int>::max()) {
        std::cout << ",\"smallest_neutral_degree\":"
                  << smallest_neutral_degree
                  << ",\"smallest_neutral_profile\":";
        print_profile(smallest_neutral_profile);
        std::cout << ",\"smallest_neutral_omitted\":["
                  << smallest_neutral_witness.omitted[0] << ','
                  << smallest_neutral_witness.omitted[1] << ','
                  << smallest_neutral_witness.omitted[2] << ']';
      }
      if (largest_replayed_plateau) {
        std::cout << ",\"largest_plateau_witness_score\":"
                  << largest_plateau_score
                  << ",\"largest_plateau_witness_profile\":";
        print_profile(largest_plateau_profile);
        std::cout << ",\"largest_plateau_witness_omitted\":["
                  << largest_plateau_witness.omitted[0] << ','
                  << largest_plateau_witness.omitted[1] << ','
                  << largest_plateau_witness.omitted[2] << ']';
      }
      std::cout << "}\n";
    }
    ++graph_index;
  }
  std::cerr << "sampled distinct states " << sampled_states << '\n';
  return 0;
}
