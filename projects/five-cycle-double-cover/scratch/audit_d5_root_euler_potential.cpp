// Complete C++ audit of the chi-maximal surface-state conjecture.

#define main d5_root_orbit_audit_unused_main
#include "audit_d5_root_kempe_orbits.cpp"
#undef main

#include <unordered_map>

struct EulerResult {
    int flows = 0;
    int orbits = 0;
    int chi_minimum = 0;
    int chi_maximum = 0;
    int maximum_chi_components_in_one_orbit = 0;
    int union_failures = 0;
    int component_failures = 0;
    State first_failure_state;
    int first_failure_root = -1;
    int first_failure_target = -1;
    int first_failure_chi = 0;
};

static int euler_characteristic(const Auditor& auditor, const State& state) {
    int primal_vertices = 0;
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
        uint32_t mask = 0;
        for (int edge = 0; edge < static_cast<int>(state.size()); ++edge) {
            const unsigned char label =
                static_cast<unsigned char>(state[edge]);
            if ((label >> coordinate) & 1) mask |= uint32_t(1) << edge;
        }
        primal_vertices +=
            static_cast<int>(auditor.component_masks(mask).size());
    }
    return primal_vertices
        - static_cast<int>(auditor.graph.edges.size())
        + auditor.graph.n;
}

static std::vector<State> distinct_neighbours(
    const Auditor& auditor,
    const State& state
) {
    std::vector<State> answer;
    for (int first = 0; first < 5; ++first) {
        for (int second = first + 1; second < 5; ++second) {
            const uint32_t active = auditor.active_mask(state, first, second);
            for (uint32_t component : auditor.component_masks(active)) {
                State other =
                    auditor.switched(state, first, second, component);
                if (other != state) answer.push_back(std::move(other));
            }
        }
    }
    std::sort(answer.begin(), answer.end());
    answer.erase(std::unique(answer.begin(), answer.end()), answer.end());
    return answer;
}

static void add_component_root_pairs(
    int edge_count,
    uint32_t component,
    std::vector<uint64_t>& rescued
) {
    std::vector<int> edges;
    while (component) {
        const int edge = __builtin_ctz(component);
        component &= component - 1;
        edges.push_back(edge);
    }
    for (int first = 0; first < static_cast<int>(edges.size()); ++first) {
        for (int second = first + 1;
             second < static_cast<int>(edges.size());
             ++second) {
            const int pair = Auditor::pair_index(
                edge_count,
                edges[first],
                edges[second]
            );
            rescued[pair / 64] |= uint64_t(1) << (pair % 64);
        }
    }
}

static bool all_pairs_rescued(
    const std::vector<uint64_t>& rescued,
    int pair_count
) {
    for (int pair = 0; pair < pair_count; ++pair) {
        if (!((rescued[pair / 64] >> (pair % 64)) & 1)) return false;
    }
    return true;
}

static std::pair<int, int> first_missing_pair(
    const std::vector<uint64_t>& rescued,
    int edge_count
) {
    for (int first = 0; first < edge_count; ++first) {
        for (int second = first + 1; second < edge_count; ++second) {
            const int pair =
                Auditor::pair_index(edge_count, first, second);
            if (!((rescued[pair / 64] >> (pair % 64)) & 1)) {
                return {first, second};
            }
        }
    }
    return {-1, -1};
}

static EulerResult audit_euler(const Auditor& auditor) {
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
        for (State& other : distinct_neighbours(auditor, states[state])) {
            auto found = index.find(other);
            if (found == index.end()) {
                throw std::runtime_error("Kempe neighbour absent");
            }
            adjacency[state].push_back(found->second);
        }
    }

    std::vector<int> chi;
    chi.reserve(states.size());
    for (const State& state : states) {
        chi.push_back(euler_characteristic(auditor, state));
    }
    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    const int pair_count = edge_count * (edge_count - 1) / 2;
    const int words = (pair_count + 63) / 64;
    std::vector<std::vector<uint64_t>> successes(
        states.size(),
        std::vector<uint64_t>(words, 0)
    );
    for (int state = 0; state < static_cast<int>(states.size()); ++state) {
        for (int first = 0; first < 5; ++first) {
            for (int second = first + 1; second < 5; ++second) {
                const uint32_t active =
                    auditor.active_mask(states[state], first, second);
                for (uint32_t component : auditor.component_masks(active)) {
                    add_component_root_pairs(
                        edge_count,
                        component,
                        successes[state]
                    );
                }
            }
        }
    }

    EulerResult result;
    result.flows = static_cast<int>(states.size());
    result.chi_minimum = *std::min_element(chi.begin(), chi.end());
    result.chi_maximum = *std::max_element(chi.begin(), chi.end());
    std::vector<unsigned char> orbit_seen(states.size(), 0);
    std::vector<unsigned char> maximum_seen(states.size(), 0);
    std::queue<int> queue;
    for (int initial = 0; initial < static_cast<int>(states.size()); ++initial) {
        if (orbit_seen[initial]) continue;
        ++result.orbits;
        std::vector<int> orbit = {initial};
        orbit_seen[initial] = 1;
        queue.push(initial);
        while (!queue.empty()) {
            const int current = queue.front();
            queue.pop();
            for (int other : adjacency[current]) {
                if (!orbit_seen[other]) {
                    orbit_seen[other] = 1;
                    orbit.push_back(other);
                    queue.push(other);
                }
            }
        }
        int maximum = chi[initial];
        for (int state : orbit) maximum = std::max(maximum, chi[state]);
        std::vector<uint64_t> union_rescued(words, 0);
        for (int state : orbit) {
            if (chi[state] != maximum) continue;
            for (int word = 0; word < words; ++word) {
                union_rescued[word] |= successes[state][word];
            }
        }
        if (!all_pairs_rescued(union_rescued, pair_count)) {
            ++result.union_failures;
            if (result.first_failure_root < 0) {
                auto missing =
                    first_missing_pair(union_rescued, edge_count);
                result.first_failure_state = states[initial];
                result.first_failure_root = missing.first;
                result.first_failure_target = missing.second;
                result.first_failure_chi = maximum;
            }
        }

        for (int state : orbit) maximum_seen[state] = 0;
        int components = 0;
        for (int start : orbit) {
            if (chi[start] != maximum || maximum_seen[start]) continue;
            ++components;
            std::vector<uint64_t> rescued(words, 0);
            maximum_seen[start] = 1;
            queue.push(start);
            while (!queue.empty()) {
                const int current = queue.front();
                queue.pop();
                for (int word = 0; word < words; ++word) {
                    rescued[word] |= successes[current][word];
                }
                for (int other : adjacency[current]) {
                    if (chi[other] == maximum && !maximum_seen[other]) {
                        maximum_seen[other] = 1;
                        queue.push(other);
                    }
                }
            }
            if (!all_pairs_rescued(rescued, pair_count)) {
                ++result.component_failures;
                if (result.first_failure_root < 0) {
                    auto missing = first_missing_pair(rescued, edge_count);
                    result.first_failure_state = states[start];
                    result.first_failure_root = missing.first;
                    result.first_failure_target = missing.second;
                    result.first_failure_chi = maximum;
                }
            }
        }
        result.maximum_chi_components_in_one_orbit = std::max(
            result.maximum_chi_components_in_one_orbit,
            components
        );
    }
    return result;
}

int main(int argc, char** argv) {
    std::ostream* output = &std::cout;
    std::ofstream file;
    if (argc == 3 && std::string(argv[1]) == "--output") {
        file.open(argv[2]);
        if (!file) throw std::runtime_error("cannot open output");
        output = &file;
    } else if (argc != 1) {
        throw std::runtime_error(
            "usage: audit_d5_root_euler_potential [--output FILE]"
        );
    }

    std::string row;
    int graphs = 0;
    long long flows = 0;
    long long orbits = 0;
    int union_failures = 0;
    int component_failures = 0;
    int maximum_components = 0;
    while (std::getline(std::cin, row)) {
        if (row.empty()) continue;
        ++graphs;
        Graph graph = decode_graph6(row);
        Auditor auditor(graph);
        EulerResult result = audit_euler(auditor);
        flows += result.flows;
        orbits += result.orbits;
        union_failures += result.union_failures;
        component_failures += result.component_failures;
        maximum_components = std::max(
            maximum_components,
            result.maximum_chi_components_in_one_orbit
        );
        *output
            << "{\"status\":\"GRAPH_DONE\",\"index\":" << graphs
            << ",\"graph6\":\"" << json_escape(row) << "\""
            << ",\"vertices\":" << graph.n
            << ",\"edges\":" << graph.edges.size()
            << ",\"flows_mod_s5\":" << result.flows
            << ",\"kempe_orbits_mod_s5\":" << result.orbits
            << ",\"chi_range\":[" << result.chi_minimum << ","
            << result.chi_maximum << "]"
            << ",\"maximum_chi_components_in_one_orbit\":"
            << result.maximum_chi_components_in_one_orbit
            << ",\"chi_maximum_union_failures\":"
            << result.union_failures
            << ",\"chi_maximum_component_failures\":"
            << result.component_failures;
        if (result.first_failure_root >= 0) {
            *output
                << ",\"first_failure\":{\"state_hex\":\""
                << state_hex(result.first_failure_state)
                << "\",\"roots\":[" << result.first_failure_root << ","
                << result.first_failure_target << "],\"chi\":"
                << result.first_failure_chi << "}";
        } else {
            *output << ",\"first_failure\":null";
        }
        *output << "}\n";
        output->flush();
    }
    *output
        << "{\"status\":\"SUMMARY\",\"graphs\":" << graphs
        << ",\"flows_mod_s5\":" << flows
        << ",\"kempe_orbits_mod_s5\":" << orbits
        << ",\"maximum_chi_components_in_one_orbit\":"
        << maximum_components
        << ",\"chi_maximum_union_failures\":" << union_failures
        << ",\"chi_maximum_component_failures\":" << component_failures
        << "}\n";
    return (union_failures || component_failures) ? 1 : 0;
}
