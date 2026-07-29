// Exhaust a literal Jaeger star state's complete same-d_min component.
//
// This is a search/audit program, not an independent certificate checker.
// It shares the exact graph, tree, odd-kernel, profile, and reciprocal-
// exchange semantics of search_jaeger_star_symmetric_local_traps.cpp.
//
// Build:
//   clang++ -O3 -std=c++20 -I/opt/homebrew/include \
//     scratch/audit_jaeger_plateau_component_literal.cpp \
//     /opt/homebrew/lib/libcadical.a -o /tmp/audit_jaeger_plateau
//
// Usage:
//   audit_jaeger_plateau GRAPH6 ROOT SPOKE0 SPOKE1 SPOKE2 MASK0 MASK1 MASK2

#define JAEGER_SYMMETRIC_LOCAL_TRAPS_NO_MAIN
#include "search_jaeger_star_symmetric_local_traps.cpp"

#include <map>
#include <unordered_map>

namespace {

RootModel literal_model(
    const Graph& graph,
    int root,
    const std::array<int, 3>& spokes,
    const StarState& state) {
  RootModel model;
  model.spoke = spokes;
  if (std::set<int>(spokes.begin(), spokes.end()) !=
      std::set<int>(
          graph.incidence[root].begin(), graph.incidence[root].end())) {
    throw std::runtime_error("literal spokes are not the root incidence");
  }
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (std::find(spokes.begin(), spokes.end(), edge) == spokes.end()) {
      model.internal.push_back(edge);
    }
  }
  if (model.internal.size() >= 64) {
    throw std::runtime_error("too many internal edges for literal masks");
  }
  model.all_internal =
      (WideMask{1} << static_cast<int>(model.internal.size())) - 1;
  model.initial = state;
  if ((state.omitted[0] ^ state.omitted[1] ^ state.omitted[2]) !=
          model.all_internal ||
      (state.omitted[0] & state.omitted[1]) ||
      (state.omitted[0] & state.omitted[2]) ||
      (state.omitted[1] & state.omitted[2])) {
    throw std::runtime_error("literal omitted masks do not partition");
  }
  const auto trees = trees_of(model, state);
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    if (!is_tree_wide(graph, trees[coordinate])) {
      throw std::runtime_error("literal state does not contain three trees");
    }
  }
  return model;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 9 && argc != 10) {
    throw std::runtime_error(
        "usage: GRAPH6 ROOT SPOKE0 SPOKE1 SPOKE2 MASK0 MASK1 MASK2 "
        "[first-exit]");
  }
  const bool stop_at_first_lower =
      argc == 10 && std::string(argv[9]) == "first-exit";
  const std::string graph6 = argv[1];
  const Graph graph = parse_graph6_local(graph6);
  const int root = std::atoi(argv[2]);
  const std::array<int, 3> spokes{
      std::atoi(argv[3]), std::atoi(argv[4]), std::atoi(argv[5])};
  StarState start;
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    start.omitted[coordinate] =
        std::strtoull(argv[6 + coordinate], nullptr, 10);
  }
  const RootModel model = literal_model(graph, root, spokes, start);
  const auto start_profile = profile_of(graph, model, start);
  const int level = minimum_score(start_profile);

  std::unordered_map<StarState, int, StarStateHash> distance;
  std::unordered_map<StarState, StarState, StarStateHash> parent;
  std::unordered_map<StarState, int, StarStateHash> boundary_score;
  std::deque<StarState> queue;
  distance.emplace(start, 0);
  queue.push_back(start);

  std::uint64_t candidate_exchanges = 0;
  std::uint64_t legal_exchanges = 0;
  std::uint64_t neutral_arcs = 0;
  std::uint64_t lower_arcs = 0;
  std::uint64_t higher_arcs = 0;
  int minimum_escape_distance = std::numeric_limits<int>::max();
  StarState first_escape;
  StarState first_escape_parent;
  std::map<int, std::uint64_t> boundary_score_histogram;
  std::map<int, std::uint64_t> distance_histogram;

  while (!queue.empty()) {
    const StarState current = queue.front();
    queue.pop_front();
    const int current_distance = distance.at(current);
    ++distance_histogram[current_distance];
    if ((distance.size() % 100000) == 0) {
      std::cerr << "plateau_states=" << distance.size()
                << " queue=" << queue.size()
                << " boundary_states=" << boundary_score.size() << '\n';
    }
    for (int first = 0; first < 3; ++first) {
      for (int second = first + 1; second < 3; ++second) {
        candidate_exchanges +=
            static_cast<std::uint64_t>(
                __builtin_popcountll(current.omitted[first])) *
            __builtin_popcountll(current.omitted[second]);
      }
    }
    const auto next = neighbours(graph, model, current);
    legal_exchanges += next.size();
    for (const StarState& other : next) {
      const auto known_plateau = distance.find(other);
      if (known_plateau != distance.end()) {
        ++neutral_arcs;
        continue;
      }
      int other_score;
      const auto known_boundary = boundary_score.find(other);
      if (known_boundary != boundary_score.end()) {
        other_score = known_boundary->second;
      } else {
        other_score = minimum_score(profile_of(graph, model, other));
      }
      if (other_score == level) {
        ++neutral_arcs;
        if (known_boundary != boundary_score.end()) {
          throw std::runtime_error("boundary cache contains a plateau state");
        }
        {
          distance.emplace(other, current_distance + 1);
          parent.emplace(other, current);
          queue.push_back(other);
        }
      } else {
        if (known_boundary == boundary_score.end()) {
          boundary_score.emplace(other, other_score);
        }
        ++boundary_score_histogram[other_score];
        if (other_score < level) {
          ++lower_arcs;
          if (current_distance + 1 < minimum_escape_distance) {
            minimum_escape_distance = current_distance + 1;
            first_escape = other;
            first_escape_parent = current;
          }
        } else {
          ++higher_arcs;
        }
      }
    }
    if (stop_at_first_lower && lower_arcs) {
      queue.clear();
      break;
    }
  }

  std::vector<StarState> escape_path;
  if (minimum_escape_distance != std::numeric_limits<int>::max()) {
    escape_path.push_back(first_escape);
    StarState cursor = first_escape_parent;
    escape_path.push_back(cursor);
    while (!(cursor == start)) {
      cursor = parent.at(cursor);
      escape_path.push_back(cursor);
    }
    std::reverse(escape_path.begin(), escape_path.end());
  }

  std::cout << "{\"graph6\":\"" << json_escape(graph6) << "\","
            << "\"root\":" << root << ",\"spokes\":["
            << spokes[0] << ',' << spokes[1] << ',' << spokes[2] << "],"
            << "\"start_omitted\":["
            << start.omitted[0] << ',' << start.omitted[1] << ','
            << start.omitted[2] << "],\"start_profile\":";
  print_profile(start_profile);
  std::cout << ",\"level\":" << level
            << ",\"component_states\":" << distance.size()
            << ",\"candidate_exchanges\":" << candidate_exchanges
            << ",\"legal_exchange_arcs\":" << legal_exchanges
            << ",\"neutral_arcs\":" << neutral_arcs
            << ",\"lower_boundary_arcs\":" << lower_arcs
            << ",\"higher_boundary_arcs\":" << higher_arcs
            << ",\"component_complete\":"
            << (stop_at_first_lower ? "false" : "true")
            << ",\"minimum_escape_distance\":";
  if (minimum_escape_distance == std::numeric_limits<int>::max()) {
    std::cout << "null";
  } else {
    std::cout << minimum_escape_distance;
  }
  std::cout << ",\"distance_histogram\":{";
  bool first_output = true;
  for (const auto& [key, value] : distance_histogram) {
    if (!first_output) std::cout << ',';
    first_output = false;
    std::cout << '"' << key << "\":" << value;
  }
  std::cout << "},\"boundary_score_histogram\":{";
  first_output = true;
  for (const auto& [key, value] : boundary_score_histogram) {
    if (!first_output) std::cout << ',';
    first_output = false;
    std::cout << '"' << key << "\":" << value;
  }
  std::cout << "},\"escape_path\":[";
  for (int index = 0; index < static_cast<int>(escape_path.size()); ++index) {
    if (index) std::cout << ',';
    const auto path_profile =
        profile_of(graph, model, escape_path[index]);
    std::cout << "{\"omitted\":["
              << escape_path[index].omitted[0] << ','
              << escape_path[index].omitted[1] << ','
              << escape_path[index].omitted[2] << "],\"profile\":";
    print_profile(path_profile);
    std::cout << '}';
  }
  std::cout << "]}\n";
}
