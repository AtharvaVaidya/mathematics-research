// Exploratory exact-neighbour search for local traps of the sorted
// seven-plane defect profile.  This is deliberately a thin wrapper around
// search_jaeger_star_symmetric_local_traps.cpp so that the graph, tree,
// odd-kernel, profile, and exchange semantics are shared verbatim.
//
// A SORTED_STRICT_TRAP is a counterexample to the proposed refinement
// "every positive state has an exchange that lexicographically decreases
// its sorted seven-plane profile."  It is not a counterexample to the
// same-minimum-level component theorem or to FiveCDC.

#define JAEGER_SYMMETRIC_LOCAL_TRAPS_NO_MAIN
#include "search_jaeger_star_symmetric_local_traps.cpp"

namespace {

std::array<int, 7> sorted_profile_of(
    const Graph& graph, const RootModel& model, const StarState& state) {
  auto profile = profile_of(graph, model, state);
  std::sort(profile.begin(), profile.end());
  return profile;
}

void print_state_json(
    const std::string& status,
    const std::string& graph6,
    int root,
    const RootModel& model,
    const StarState& state,
    const std::array<int, 7>& profile,
    int lower,
    int equal,
    int higher) {
  std::cout << "{\"status\":\"" << status << "\","
            << "\"graph6\":\"" << json_escape(graph6) << "\","
            << "\"root\":" << root << ','
            << "\"spokes\":[" << model.spoke[0] << ','
            << model.spoke[1] << ',' << model.spoke[2] << "],"
            << "\"omitted\":[" << state.omitted[0] << ','
            << state.omitted[1] << ',' << state.omitted[2] << "],"
            << "\"sorted_profile\":";
  print_profile(profile);
  std::cout << ",\"lower\":" << lower << ",\"equal\":" << equal
            << ",\"higher\":" << higher << "}\n";
}

}  // namespace

int main(int argc, char** argv) {
  const int steps = argc >= 2 ? std::atoi(argv[1]) : 10000;
  const std::uint64_t seed =
      argc >= 3 ? std::strtoull(argv[2], nullptr, 10) : 1;
  const int requested_root = argc >= 4 ? std::atoi(argv[3]) : 0;
  const std::string mode = argc >= 5 ? argv[4] : "sorted";
  if (mode != "sorted" && mode != "min-sum") {
    throw std::runtime_error("mode must be sorted or min-sum");
  }
  std::mt19937_64 random(seed);

  std::string graph6;
  while (std::getline(std::cin, graph6)) {
    if (graph6.empty()) continue;
    const Graph graph = parse_graph6_local(graph6);
    if (!is_cubic_connected(graph) || !is_bridgeless(graph) ||
        graph.m() > 63) {
      continue;
    }
    const int first_root = requested_root < 0 ? 0 : requested_root;
    const int last_root =
        requested_root < 0 ? graph.n : requested_root + 1;
    for (int root = first_root; root < last_root; ++root) {
      RootModel model;
      try {
        model = feasible_root_model(graph, root);
      } catch (const std::runtime_error&) {
        continue;
      }
      StarState state = model.initial;
      std::unordered_set<StarState, StarStateHash> seen;
      for (int step = 0; step < steps; ++step) {
        if (seen.insert(state).second) {
          auto profile = sorted_profile_of(graph, model, state);
          if (mode == "min-sum") {
            profile[1] = std::accumulate(
                profile.begin(), profile.end(), 0);
            std::fill(profile.begin() + 2, profile.end(), 0);
          }
          const auto next = neighbours(graph, model, state);
          int lower = 0;
          int equal = 0;
          int higher = 0;
          for (const auto& neighbour : next) {
            auto candidate =
                sorted_profile_of(graph, model, neighbour);
            if (mode == "min-sum") {
              candidate[1] = std::accumulate(
                  candidate.begin(), candidate.end(), 0);
              std::fill(candidate.begin() + 2, candidate.end(), 0);
            }
            lower += candidate < profile;
            equal += candidate == profile;
            higher += candidate > profile;
          }
          if (profile[0] > 0 && lower == 0) {
            print_state_json(
                "SORTED_STRICT_TRAP", graph6, root, model, state,
                profile, lower, equal, higher);
            // Diagnose the exact distinction between the failed sorted
            // one-step potential and the surviving d_min plateau claim.
            const int minimum = profile[0];
            std::unordered_set<StarState, StarStateHash> plateau_seen;
            std::deque<std::pair<StarState, int>> queue;
            plateau_seen.insert(state);
            queue.emplace_back(state, 0);
            bool escaped = false;
            int escape_distance = -1;
            while (!queue.empty() && !escaped) {
              const auto [current, distance] = queue.front();
              queue.pop_front();
              for (const auto& neighbour :
                   neighbours(graph, model, current)) {
                const int candidate_minimum = minimum_score(
                    profile_of(graph, model, neighbour));
                if (candidate_minimum < minimum) {
                  escaped = true;
                  escape_distance = distance + 1;
                  break;
                }
                if (candidate_minimum == minimum &&
                    plateau_seen.insert(neighbour).second) {
                  queue.emplace_back(neighbour, distance + 1);
                }
              }
            }
            std::cout << "{\"status\":\"D_MIN_PLATEAU_DIAGNOSIS\","
                      << "\"escaped\":"
                      << (escaped ? "true" : "false") << ','
                      << "\"escape_distance\":" << escape_distance << ','
                      << "\"states_seen\":" << plateau_seen.size()
                      << "}\n";
            return 1;
          }
        }
        const auto next = neighbours(graph, model, state);
        if (next.empty()) {
          throw std::runtime_error("isolated packing state");
        }
        if ((random() & 3ULL) == 0) {
          state = next[random() % next.size()];
        } else {
          auto best = sorted_profile_of(graph, model, next[0]);
          if (mode == "min-sum") {
            best[1] = std::accumulate(best.begin(), best.end(), 0);
            std::fill(best.begin() + 2, best.end(), 0);
          }
          std::vector<int> best_indices{0};
          for (int index = 1; index < static_cast<int>(next.size());
               ++index) {
            auto candidate =
                sorted_profile_of(graph, model, next[index]);
            if (mode == "min-sum") {
              candidate[1] = std::accumulate(
                  candidate.begin(), candidate.end(), 0);
              std::fill(candidate.begin() + 2, candidate.end(), 0);
            }
            // Bias toward a local minimum of the candidate potential.  The
            // purpose of this wrapper is to find a positive sink, not to
            // spend time at high-defect states.
            if (candidate < best) {
              best = candidate;
              best_indices.clear();
            }
            if (candidate == best) best_indices.push_back(index);
          }
          state = next[best_indices[random() % best_indices.size()]];
        }
      }
      std::cout << "{\"status\":\"ROOT_DONE\",\"graph6\":\""
                << json_escape(graph6) << "\",\"root\":" << root
                << ",\"distinct_states\":" << seen.size() << "}\n";
    }
  }
  return 0;
}
