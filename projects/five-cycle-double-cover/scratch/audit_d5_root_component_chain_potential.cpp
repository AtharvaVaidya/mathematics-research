// Exact C++ audit of the root component-chain distance potential.
//
// This deliberately reuses only the already cross-checked D5-flow enumerator
// and Kempe-move primitives from audit_d5_root_kempe_orbits.cpp.  The metric
// construction and equal-level plateau test below are independent of the
// Python implementation in audit_d5_root_component_chain_potential.py.

#define main d5_root_orbit_audit_unused_main
#include "audit_d5_root_kempe_orbits.cpp"
#undef main

#include <unordered_map>

struct ChainPotentialResult {
    int flows = 0;
    long long plateaus = 0;
    long long state_root_tests = 0;
    int maximum_distance = 0;
    int maximum_equal_moves_before_descent = 0;
    State maximum_depth_state;
    int maximum_depth_root = -1;
    int maximum_depth_target = -1;
    bool failure = false;
    State failure_state;
    int failure_root = -1;
    int failure_target = -1;
    int failure_distance = -1;
    int failure_plateau_size = 0;
    std::vector<int> failure_boundary_distances;
};

struct TargetOrbitResult {
    int states = 0;
    long long plateaus = 0;
    int maximum_distance = 0;
    int maximum_equal_moves_before_descent = 0;
    std::vector<int> level_counts;
    bool failure = false;
    State failure_state;
    int failure_distance = -1;
    int failure_plateau_size = 0;
    std::vector<int> failure_boundary_distances;
};

static std::vector<unsigned char> chain_distances(
    const Auditor& auditor,
    const State& state
) {
    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    const int pair_count = edge_count * (edge_count - 1) / 2;
    std::vector<uint32_t> neighbours(edge_count, 0);

    for (int first = 0; first < 5; ++first) {
        for (int second = first + 1; second < 5; ++second) {
            const uint32_t active = auditor.active_mask(state, first, second);
            for (uint32_t component : auditor.component_masks(active)) {
                uint32_t copy = component;
                while (copy) {
                    const int edge = __builtin_ctz(copy);
                    copy &= copy - 1;
                    neighbours[edge] |= component;
                }
            }
        }
    }

    std::vector<unsigned char> answer(pair_count, 255);
    for (int root = 0; root < edge_count; ++root) {
        uint32_t visited = uint32_t(1) << root;
        uint32_t frontier = visited;
        int distance = 0;
        while (frontier) {
            uint32_t next = 0;
            uint32_t copy = frontier;
            while (copy) {
                const int edge = __builtin_ctz(copy);
                copy &= copy - 1;
                next |= neighbours[edge];
            }
            next &= ~visited;
            if (!next) break;
            ++distance;
            copy = next;
            while (copy) {
                const int target = __builtin_ctz(copy);
                copy &= copy - 1;
                const int left = std::min(root, target);
                const int right = std::max(root, target);
                answer[Auditor::pair_index(edge_count, left, right)] =
                    static_cast<unsigned char>(distance);
            }
            visited |= next;
            frontier = next;
        }
        const uint32_t all =
            edge_count == 32 ? ~uint32_t(0) : (uint32_t(1) << edge_count) - 1;
        if (visited != all) {
            throw std::runtime_error("factor-component hypergraph disconnected");
        }
    }
    return answer;
}

static ChainPotentialResult audit_chain_potential(const Auditor& auditor) {
    auto flow_set = auditor.enumerate_flows();
    std::vector<State> states(flow_set.begin(), flow_set.end());
    std::sort(states.begin(), states.end());
    std::unordered_map<State, int> index;
    index.reserve(states.size() * 2);
    for (int i = 0; i < static_cast<int>(states.size()); ++i) {
        index.emplace(states[i], i);
    }

    std::vector<std::vector<int>> adjacency(states.size());
    for (int i = 0; i < static_cast<int>(states.size()); ++i) {
        for (int first = 0; first < 5; ++first) {
            for (int second = first + 1; second < 5; ++second) {
                const uint32_t active =
                    auditor.active_mask(states[i], first, second);
                for (uint32_t component : auditor.component_masks(active)) {
                    State other =
                        auditor.switched(states[i], first, second, component);
                    auto found = index.find(other);
                    if (found == index.end()) {
                        throw std::runtime_error("Kempe neighbour absent");
                    }
                    if (found->second != i) adjacency[i].push_back(found->second);
                }
            }
        }
        std::sort(adjacency[i].begin(), adjacency[i].end());
        adjacency[i].erase(
            std::unique(adjacency[i].begin(), adjacency[i].end()),
            adjacency[i].end()
        );
    }

    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    const int pair_count = edge_count * (edge_count - 1) / 2;
    std::vector<std::vector<unsigned char>> distances;
    distances.reserve(states.size());
    ChainPotentialResult result;
    result.flows = static_cast<int>(states.size());
    for (const State& state : states) {
        distances.push_back(chain_distances(auditor, state));
        for (unsigned char value : distances.back()) {
            if (value == 255) throw std::runtime_error("unset chain distance");
            result.maximum_distance =
                std::max(result.maximum_distance, static_cast<int>(value));
        }
    }
    result.state_root_tests =
        static_cast<long long>(states.size()) * pair_count;

    std::vector<unsigned char> seen(states.size(), 0);
    std::vector<int> queue;
    for (int pair = 0; pair < pair_count; ++pair) {
        std::fill(seen.begin(), seen.end(), 0);
        for (int start = 0; start < static_cast<int>(states.size()); ++start) {
            const int level = distances[start][pair];
            if (level <= 1 || seen[start]) continue;
            ++result.plateaus;
            queue.clear();
            queue.push_back(start);
            seen[start] = 1;
            bool has_descent = false;
            std::vector<int> boundary_distances;
            for (std::size_t cursor = 0; cursor < queue.size(); ++cursor) {
                const int current = queue[cursor];
                for (int other : adjacency[current]) {
                    const int other_level = distances[other][pair];
                    if (other_level < level) has_descent = true;
                    if (other_level != level) {
                        boundary_distances.push_back(other_level);
                    } else if (!seen[other]) {
                        seen[other] = 1;
                        queue.push_back(other);
                    }
                }
            }
            if (!has_descent && !result.failure) {
                result.failure = true;
                result.failure_state = states[start];
                result.failure_distance = level;
                result.failure_plateau_size = static_cast<int>(queue.size());
                std::sort(boundary_distances.begin(), boundary_distances.end());
                boundary_distances.erase(
                    std::unique(
                        boundary_distances.begin(),
                        boundary_distances.end()
                    ),
                    boundary_distances.end()
                );
                result.failure_boundary_distances =
                    std::move(boundary_distances);
                for (int left = 0; left < edge_count; ++left) {
                    for (int right = left + 1; right < edge_count; ++right) {
                        if (Auditor::pair_index(edge_count, left, right) == pair) {
                            result.failure_root = left;
                            result.failure_target = right;
                        }
                    }
                }
            }
        }
        // One multi-source BFS per level gives every state's exact distance
        // inside its equal-level plateau to a state with a lower neighbour.
        // This is equivalent to the earlier per-plateau BFS but avoids
        // rebuilding membership tables for every component.
        for (int level = 2; level <= result.maximum_distance; ++level) {
            std::vector<int> descent_distance(states.size(), -1);
            std::queue<int> descent_queue;
            for (int current = 0;
                 current < static_cast<int>(states.size());
                 ++current) {
                if (distances[current][pair] != level) continue;
                if (std::any_of(
                        adjacency[current].begin(),
                        adjacency[current].end(),
                        [&](int other) {
                            return distances[other][pair] < level;
                        }
                    )) {
                    descent_distance[current] = 0;
                    descent_queue.push(current);
                }
            }
            while (!descent_queue.empty()) {
                const int current = descent_queue.front();
                descent_queue.pop();
                if (descent_distance[current] >
                    result.maximum_equal_moves_before_descent) {
                    result.maximum_equal_moves_before_descent =
                        descent_distance[current];
                    result.maximum_depth_state = states[current];
                    for (int left = 0; left < edge_count; ++left) {
                        for (int right = left + 1;
                             right < edge_count;
                             ++right) {
                            if (Auditor::pair_index(
                                    edge_count,
                                    left,
                                    right
                                ) == pair) {
                                result.maximum_depth_root = left;
                                result.maximum_depth_target = right;
                            }
                        }
                    }
                }
                for (int other : adjacency[current]) {
                    if (distances[other][pair] == level &&
                        descent_distance[other] < 0) {
                        descent_distance[other] =
                            descent_distance[current] + 1;
                        descent_queue.push(other);
                    }
                }
            }
        }
    }
    return result;
}

static std::vector<State> kempe_neighbours(
    const Auditor& auditor,
    const State& state
) {
    std::vector<State> answer;
    for (int first = 0; first < 5; ++first) {
        for (int second = first + 1; second < 5; ++second) {
            const uint32_t active = auditor.active_mask(state, first, second);
            for (uint32_t component : auditor.component_masks(active)) {
                State other = auditor.switched(state, first, second, component);
                if (other != state) answer.push_back(std::move(other));
            }
        }
    }
    std::sort(answer.begin(), answer.end());
    answer.erase(std::unique(answer.begin(), answer.end()), answer.end());
    return answer;
}

static TargetOrbitResult audit_target_orbit(
    const Auditor& auditor,
    State initial,
    int root,
    int target
) {
    initial = auditor.canonical(initial);
    std::vector<State> states = {initial};
    std::unordered_map<State, int> index = {{initial, 0}};
    std::vector<std::vector<int>> adjacency(1);
    for (std::size_t cursor = 0; cursor < states.size(); ++cursor) {
        std::vector<State> next = kempe_neighbours(auditor, states[cursor]);
        adjacency.resize(states.size());
        for (State& other : next) {
            auto [position, inserted] =
                index.emplace(other, static_cast<int>(states.size()));
            if (inserted) {
                states.push_back(other);
                adjacency.emplace_back();
            }
            adjacency[cursor].push_back(position->second);
        }
        if ((cursor + 1) % 100000 == 0) {
            std::cerr << "TARGET_PROGRESS states_processed=" << (cursor + 1)
                      << " states_discovered=" << states.size() << "\n";
        }
    }

    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    const int pair =
        Auditor::pair_index(
            edge_count,
            std::min(root, target),
            std::max(root, target)
        );
    std::vector<unsigned char> level(states.size(), 255);
    TargetOrbitResult result;
    result.states = static_cast<int>(states.size());
    for (int i = 0; i < static_cast<int>(states.size()); ++i) {
        level[i] = chain_distances(auditor, states[i])[pair];
        result.maximum_distance =
            std::max(result.maximum_distance, static_cast<int>(level[i]));
    }
    result.level_counts.assign(result.maximum_distance + 1, 0);
    for (unsigned char value : level) ++result.level_counts[value];

    std::vector<unsigned char> seen(states.size(), 0);
    std::vector<int> queue;
    for (int start = 0; start < static_cast<int>(states.size()); ++start) {
        if (level[start] <= 1 || seen[start]) continue;
        ++result.plateaus;
        queue.clear();
        queue.push_back(start);
        seen[start] = 1;
        bool has_descent = false;
        std::vector<int> boundary_distances;
        for (std::size_t cursor = 0; cursor < queue.size(); ++cursor) {
            const int current = queue[cursor];
            for (int other : adjacency[current]) {
                const int other_level = level[other];
                if (other_level < level[start]) has_descent = true;
                if (other_level != level[start]) {
                    boundary_distances.push_back(other_level);
                } else if (!seen[other]) {
                    seen[other] = 1;
                    queue.push_back(other);
                }
            }
        }
        if (!has_descent && !result.failure) {
            result.failure = true;
            result.failure_state = states[start];
            result.failure_distance = level[start];
            result.failure_plateau_size = static_cast<int>(queue.size());
            std::sort(boundary_distances.begin(), boundary_distances.end());
            boundary_distances.erase(
                std::unique(
                    boundary_distances.begin(),
                    boundary_distances.end()
                ),
                boundary_distances.end()
            );
            result.failure_boundary_distances =
                std::move(boundary_distances);
        } else if (has_descent) {
            std::unordered_set<int> in_plateau(queue.begin(), queue.end());
            std::unordered_map<int, int> descent_distance;
            std::queue<int> descent_queue;
            for (int current : queue) {
                if (std::any_of(
                        adjacency[current].begin(),
                        adjacency[current].end(),
                        [&](int other) {
                            return level[other] < level[start];
                        }
                    )) {
                    descent_distance.emplace(current, 0);
                    descent_queue.push(current);
                }
            }
            while (!descent_queue.empty()) {
                const int current = descent_queue.front();
                descent_queue.pop();
                result.maximum_equal_moves_before_descent = std::max(
                    result.maximum_equal_moves_before_descent,
                    descent_distance[current]
                );
                for (int other : adjacency[current]) {
                    if (in_plateau.count(other) &&
                        !descent_distance.count(other)) {
                        descent_distance.emplace(
                            other,
                            descent_distance.at(current) + 1
                        );
                        descent_queue.push(other);
                    }
                }
            }
        }
    }
    return result;
}

static State parse_state_hex(const std::string& text, int edge_count) {
    if (static_cast<int>(text.size()) != 2 * edge_count) {
        throw std::runtime_error("state hex has wrong length");
    }
    State state(edge_count, '\0');
    auto digit = [](char c) -> int {
        if (c >= '0' && c <= '9') return c - '0';
        if (c >= 'a' && c <= 'f') return c - 'a' + 10;
        if (c >= 'A' && c <= 'F') return c - 'A' + 10;
        throw std::runtime_error("bad hex digit");
    };
    for (int edge = 0; edge < edge_count; ++edge) {
        state[edge] = static_cast<char>(
            16 * digit(text[2 * edge]) + digit(text[2 * edge + 1])
        );
        if (!is_label(static_cast<unsigned char>(state[edge]))) {
            throw std::runtime_error("state hex contains a non-D5 label");
        }
    }
    return state;
}

int main(int argc, char** argv) {
    if (argc == 6 && std::string(argv[1]) == "--target") {
        const std::string graph6 = argv[2];
        Graph graph = decode_graph6(graph6);
        Auditor auditor(graph);
        State state = parse_state_hex(argv[3], graph.edges.size());
        const int root = std::stoi(argv[4]);
        const int target = std::stoi(argv[5]);
        if (root < 0 || target < 0 ||
            root >= static_cast<int>(graph.edges.size()) ||
            target >= static_cast<int>(graph.edges.size()) ||
            root == target) {
            throw std::runtime_error("invalid target roots");
        }
        TargetOrbitResult result =
            audit_target_orbit(auditor, state, root, target);
        std::cout
            << "{\"status\":\"TARGET_ORBIT\",\"graph6\":\""
            << json_escape(graph6) << "\",\"roots\":[" << root << ","
            << target << "],\"states_mod_s5\":" << result.states
            << ",\"plateaus_checked\":" << result.plateaus
            << ",\"maximum_distance\":" << result.maximum_distance
            << ",\"maximum_equal_moves_before_descent\":"
            << result.maximum_equal_moves_before_descent
            << ",\"level_counts\":[";
        for (std::size_t i = 0; i < result.level_counts.size(); ++i) {
            if (i) std::cout << ",";
            std::cout << result.level_counts[i];
        }
        std::cout << "],\"failure\":" << (result.failure ? "true" : "false");
        if (result.failure) {
            std::cout
                << ",\"first_failure\":{\"state_hex\":\""
                << state_hex(result.failure_state)
                << "\",\"distance\":" << result.failure_distance
                << ",\"plateau_size\":" << result.failure_plateau_size
                << ",\"boundary_distances\":[";
            for (std::size_t i = 0;
                 i < result.failure_boundary_distances.size();
                 ++i) {
                if (i) std::cout << ",";
                std::cout << result.failure_boundary_distances[i];
            }
            std::cout << "]}";
        } else {
            std::cout << ",\"first_failure\":null";
        }
        std::cout << "}\n";
        return result.failure ? 1 : 0;
    }
    std::ofstream output_file;
    std::streambuf* original_output = nullptr;
    if (argc == 3 && std::string(argv[1]) == "--output") {
        output_file.open(argv[2]);
        if (!output_file) throw std::runtime_error("cannot open output file");
        original_output = std::cout.rdbuf(output_file.rdbuf());
        argc = 1;
    }
    if (argc != 1) {
        throw std::runtime_error(
            "usage: audit_d5_root_component_chain_potential "
            "[--output FILE | --target GRAPH6 STATE_HEX ROOT TARGET]"
        );
    }
    std::string row;
    int graphs = 0;
    long long flows = 0;
    long long plateaus = 0;
    long long tests = 0;
    int maximum_distance = 0;
    int maximum_equal_moves_before_descent = 0;
    int failures = 0;
    while (std::getline(std::cin, row)) {
        if (row.empty()) continue;
        ++graphs;
        Graph graph = decode_graph6(row);
        Auditor auditor(graph);
        ChainPotentialResult result = audit_chain_potential(auditor);
        flows += result.flows;
        plateaus += result.plateaus;
        tests += result.state_root_tests;
        maximum_distance = std::max(maximum_distance, result.maximum_distance);
        maximum_equal_moves_before_descent = std::max(
            maximum_equal_moves_before_descent,
            result.maximum_equal_moves_before_descent
        );
        if (result.failure) ++failures;
        std::cout
            << "{\"status\":\"GRAPH_DONE\",\"index\":" << graphs
            << ",\"graph6\":\"" << json_escape(row) << "\""
            << ",\"vertices\":" << graph.n
            << ",\"edges\":" << graph.edges.size()
            << ",\"flows_mod_s5\":" << result.flows
            << ",\"state_root_pair_tests\":" << result.state_root_tests
            << ",\"plateaus_checked\":" << result.plateaus
            << ",\"maximum_distance\":" << result.maximum_distance
            << ",\"maximum_equal_moves_before_descent\":"
            << result.maximum_equal_moves_before_descent
            << ",\"maximum_depth_witness\":";
        if (result.maximum_depth_root >= 0) {
            std::cout
                << "{\"state_hex\":\""
                << state_hex(result.maximum_depth_state)
                << "\",\"roots\":[" << result.maximum_depth_root << ","
                << result.maximum_depth_target << "]}";
        } else {
            std::cout << "null";
        }
        std::cout
            << ",\"failure\":" << (result.failure ? "true" : "false");
        if (result.failure) {
            std::cout
                << ",\"first_failure\":{\"state_hex\":\""
                << state_hex(result.failure_state)
                << "\",\"roots\":[" << result.failure_root << ","
                << result.failure_target << "]"
                << ",\"distance\":" << result.failure_distance
                << ",\"plateau_size\":" << result.failure_plateau_size
                << ",\"boundary_distances\":[";
            for (std::size_t i = 0;
                 i < result.failure_boundary_distances.size();
                 ++i) {
                if (i) std::cout << ",";
                std::cout << result.failure_boundary_distances[i];
            }
            std::cout << "]}";
        } else {
            std::cout << ",\"first_failure\":null";
        }
        std::cout << "}\n";
        std::cout.flush();
    }
    std::cout
        << "{\"status\":\"SUMMARY\",\"graphs\":" << graphs
        << ",\"flows_mod_s5\":" << flows
        << ",\"state_root_pair_tests\":" << tests
        << ",\"plateaus_checked\":" << plateaus
        << ",\"maximum_distance\":" << maximum_distance
        << ",\"maximum_equal_moves_before_descent\":"
        << maximum_equal_moves_before_descent
        << ",\"failures\":" << failures << "}\n";
    std::cout.flush();
    if (original_output) std::cout.rdbuf(original_output);
    return failures ? 1 : 0;
}
