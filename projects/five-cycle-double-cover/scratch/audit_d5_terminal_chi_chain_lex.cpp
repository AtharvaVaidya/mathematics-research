// Exact audit of the lexicographic (surface chi, -component-chain distance)
// target on terminal surface-chi plateaus.

#define D5_CHAIN_POTENTIAL_LIBRARY
#include "audit_d5_root_component_chain_potential.cpp"
#undef D5_CHAIN_POTENTIAL_LIBRARY

#include <unordered_map>

struct LexResult {
    int flows = 0;
    long long terminal_chi_plateaus = 0;
    long long terminal_chi_distance_plateaus = 0;
    int maximum_distance = 0;
    bool failure = false;
    State failure_state;
    int failure_root = -1;
    int failure_target = -1;
    int failure_chi = 0;
    int failure_distance = 0;
    int failure_chi_plateau_size = 0;
    int failure_distance_plateau_size = 0;
};

static int surface_chi(const Auditor& auditor, const State& state) {
    int coordinate_components = 0;
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
        uint32_t mask = 0;
        for (int edge = 0; edge < static_cast<int>(state.size()); ++edge) {
            const unsigned char label =
                static_cast<unsigned char>(state[edge]);
            if ((label >> coordinate) & 1) {
                mask |= uint32_t(1) << edge;
            }
        }
        coordinate_components +=
            static_cast<int>(auditor.component_masks(mask).size());
    }
    return coordinate_components
        - static_cast<int>(auditor.graph.edges.size())
        + auditor.graph.n;
}

static LexResult audit_lex(const Auditor& auditor) {
    auto flow_set = auditor.enumerate_flows();
    std::vector<State> states(flow_set.begin(), flow_set.end());
    std::sort(states.begin(), states.end());
    std::unordered_map<State, int> index;
    index.reserve(states.size() * 2);
    for (int state = 0; state < static_cast<int>(states.size()); ++state) {
        index.emplace(states[state], state);
    }

    std::vector<std::vector<int>> adjacency(states.size());
    for (int state = 0; state < static_cast<int>(states.size()); ++state) {
        for (int first = 0; first < 5; ++first) {
            for (int second = first + 1; second < 5; ++second) {
                const uint32_t active =
                    auditor.active_mask(states[state], first, second);
                for (uint32_t component : auditor.component_masks(active)) {
                    const State other =
                        auditor.switched(
                            states[state], first, second, component
                        );
                    const int target = index.at(other);
                    if (target != state) adjacency[state].push_back(target);
                }
            }
        }
        std::sort(adjacency[state].begin(), adjacency[state].end());
        adjacency[state].erase(
            std::unique(
                adjacency[state].begin(), adjacency[state].end()
            ),
            adjacency[state].end()
        );
    }

    std::vector<int> chi(states.size());
    std::vector<std::vector<unsigned char>> distances;
    distances.reserve(states.size());
    LexResult result;
    result.flows = static_cast<int>(states.size());
    for (int state = 0; state < static_cast<int>(states.size()); ++state) {
        chi[state] = surface_chi(auditor, states[state]);
        distances.push_back(chain_distances(auditor, states[state]));
        for (unsigned char distance : distances.back()) {
            result.maximum_distance = std::max(
                result.maximum_distance, static_cast<int>(distance)
            );
        }
    }

    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    const int pair_count = edge_count * (edge_count - 1) / 2;
    std::vector<unsigned char> chi_seen(states.size(), 0);
    std::vector<unsigned char> distance_seen(states.size(), 0);
    std::vector<unsigned char> in_chi_plateau(states.size(), 0);
    std::vector<int> queue;

    for (int start = 0; start < static_cast<int>(states.size()); ++start) {
        if (chi_seen[start]) continue;
        const int chi_level = chi[start];
        queue.clear();
        queue.push_back(start);
        chi_seen[start] = 1;
        bool terminal = true;
        for (std::size_t cursor = 0; cursor < queue.size(); ++cursor) {
            const int current = queue[cursor];
            for (int other : adjacency[current]) {
                if (chi[other] > chi_level) terminal = false;
                if (chi[other] == chi_level && !chi_seen[other]) {
                    chi_seen[other] = 1;
                    queue.push_back(other);
                }
            }
        }
        if (!terminal) continue;
        ++result.terminal_chi_plateaus;
        const std::vector<int> chi_plateau = queue;
        for (int state : chi_plateau) in_chi_plateau[state] = 1;

        for (int pair = 0; pair < pair_count; ++pair) {
            for (int state : chi_plateau) distance_seen[state] = 0;
            for (int distance_start : chi_plateau) {
                const int level = distances[distance_start][pair];
                if (level <= 1 || distance_seen[distance_start]) continue;
                ++result.terminal_chi_distance_plateaus;
                queue.clear();
                queue.push_back(distance_start);
                distance_seen[distance_start] = 1;
                bool descent = false;
                for (
                    std::size_t cursor = 0;
                    cursor < queue.size();
                    ++cursor
                ) {
                    const int current = queue[cursor];
                    for (int other : adjacency[current]) {
                        if (!in_chi_plateau[other]) continue;
                        const int other_level = distances[other][pair];
                        if (other_level < level) descent = true;
                        if (
                            other_level == level
                            && !distance_seen[other]
                        ) {
                            distance_seen[other] = 1;
                            queue.push_back(other);
                        }
                    }
                }
                if (!descent && !result.failure) {
                    result.failure = true;
                    result.failure_state = states[distance_start];
                    result.failure_chi = chi_level;
                    result.failure_distance = level;
                    result.failure_chi_plateau_size =
                        static_cast<int>(chi_plateau.size());
                    result.failure_distance_plateau_size =
                        static_cast<int>(queue.size());
                    for (int left = 0; left < edge_count; ++left) {
                        for (
                            int right = left + 1;
                            right < edge_count;
                            ++right
                        ) {
                            if (
                                Auditor::pair_index(
                                    edge_count, left, right
                                ) == pair
                            ) {
                                result.failure_root = left;
                                result.failure_target = right;
                            }
                        }
                    }
                }
            }
        }
        for (int state : chi_plateau) in_chi_plateau[state] = 0;
    }
    return result;
}

int main() {
    std::string graph6;
    int graphs = 0;
    long long flows = 0;
    long long chi_plateaus = 0;
    long long distance_plateaus = 0;
    int maximum_distance = 0;
    int failures = 0;
    while (std::getline(std::cin, graph6)) {
        if (graph6.empty()) continue;
        ++graphs;
        const Graph graph = decode_graph6(graph6);
        const Auditor auditor(graph);
        const LexResult result = audit_lex(auditor);
        flows += result.flows;
        chi_plateaus += result.terminal_chi_plateaus;
        distance_plateaus += result.terminal_chi_distance_plateaus;
        maximum_distance =
            std::max(maximum_distance, result.maximum_distance);
        failures += result.failure;
        std::cout
            << "{\"status\":\"GRAPH_DONE\",\"index\":" << graphs
            << ",\"graph6\":\"" << json_escape(graph6) << "\""
            << ",\"vertices\":" << graph.n
            << ",\"flows_mod_s5\":" << result.flows
            << ",\"terminal_chi_plateaus\":"
            << result.terminal_chi_plateaus
            << ",\"terminal_chi_distance_plateaus\":"
            << result.terminal_chi_distance_plateaus
            << ",\"maximum_distance\":" << result.maximum_distance
            << ",\"lex_failures\":" << static_cast<int>(result.failure);
        if (result.failure) {
            std::cout
                << ",\"first_failure\":{\"state_hex\":\""
                << state_hex(result.failure_state)
                << "\",\"roots\":[" << result.failure_root << ','
                << result.failure_target << "]"
                << ",\"chi\":" << result.failure_chi
                << ",\"distance\":" << result.failure_distance
                << ",\"chi_plateau_size\":"
                << result.failure_chi_plateau_size
                << ",\"distance_plateau_size\":"
                << result.failure_distance_plateau_size << '}';
        } else {
            std::cout << ",\"first_failure\":null";
        }
        std::cout << "}\n";
        std::cout.flush();
        if (result.failure) break;
    }
    std::cout
        << "{\"status\":\"SUMMARY\",\"graphs\":" << graphs
        << ",\"flows_mod_s5\":" << flows
        << ",\"terminal_chi_plateaus\":" << chi_plateaus
        << ",\"terminal_chi_distance_plateaus\":"
        << distance_plateaus
        << ",\"maximum_distance\":" << maximum_distance
        << ",\"lex_failures\":" << failures << "}\n";
    return failures ? 1 : 0;
}
