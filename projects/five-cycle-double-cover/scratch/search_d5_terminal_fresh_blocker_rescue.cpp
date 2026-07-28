// Test whether every positive cyclic-block obstruction in a terminal
// chi plateau has an immediate neutral fresh-coordinate switch lowering
// the exact factor-chain distance.

#define D5_CYCLIC_BLOCK_LIBRARY
#include "search_d5_terminal_cyclic_block_obstruction.cpp"
#undef D5_CYCLIC_BLOCK_LIBRARY

int main() {
    std::string record;
    long long graphs = 0;
    long long flows = 0;
    long long positive_blocker_tests = 0;
    long long fresh_rescues = 0;
    while (std::getline(std::cin, record)) {
        if (record.empty()) continue;
        ++graphs;
        const Auditor auditor(decode_graph6(record));
        const auto flow_set = auditor.enumerate_flows();
        std::vector<State> states(flow_set.begin(), flow_set.end());
        std::sort(states.begin(), states.end());
        flows += states.size();

        std::unordered_map<State, int> index;
        index.reserve(states.size() * 2);
        for (int state = 0; state < static_cast<int>(states.size()); ++state) {
            index.emplace(states[state], state);
        }
        std::vector<std::vector<int>> adjacency(states.size());
        std::vector<int> chi(states.size());
        for (int state = 0; state < static_cast<int>(states.size()); ++state) {
            chi[state] = surface_chi(auditor, states[state]);
            for (const Factor& factor : all_factors(auditor, states[state])) {
                const State other = auditor.switched(
                    states[state],
                    factor.first,
                    factor.second,
                    factor.mask
                );
                const int target = index.at(other);
                if (target != state) adjacency[state].push_back(target);
            }
            std::sort(adjacency[state].begin(), adjacency[state].end());
            adjacency[state].erase(
                std::unique(
                    adjacency[state].begin(), adjacency[state].end()
                ),
                adjacency[state].end()
            );
        }

        std::vector<unsigned char> seen(states.size(), 0);
        std::vector<int> queue;
        for (int start = 0; start < static_cast<int>(states.size()); ++start) {
            if (seen[start]) continue;
            queue.clear();
            queue.push_back(start);
            seen[start] = 1;
            bool terminal = true;
            for (std::size_t cursor = 0; cursor < queue.size(); ++cursor) {
                const int current = queue[cursor];
                for (int other : adjacency[current]) {
                    if (chi[other] > chi[start]) terminal = false;
                    if (chi[other] == chi[start] && !seen[other]) {
                        seen[other] = 1;
                        queue.push_back(other);
                    }
                }
            }
            if (!terminal) continue;

            for (int state_index : queue) {
                const State& state = states[state_index];
                const FactorContext context =
                    build_factor_context(auditor, state);
                int used_coordinates = 0;
                for (unsigned char raw : state) {
                    used_coordinates |= static_cast<unsigned char>(raw);
                }
                const int edge_count =
                    static_cast<int>(auditor.graph.edges.size());
                for (int root = 0; root < edge_count; ++root) {
                    for (int target = 0; target < edge_count; ++target) {
                        if (root == target) continue;
                        const PotentialWitness before =
                            oriented_potential(
                                auditor, context, root, target
                            );
                        if (
                            before.distance <= 1
                            || before.blocker == INT_MAX
                            || before.blocker == 0
                        ) continue;
                        ++positive_blocker_tests;

                        bool rescued = false;
                        int rescue_x = -1;
                        int rescue_z = -1;
                        uint32_t rescue_component = 0;
                        for (int z = 0; z < 5 && !rescued; ++z) {
                            if ((used_coordinates >> z) & 1) continue;
                            for (int x = 0; x < 5 && !rescued; ++x) {
                                if (x == z) continue;
                                const uint32_t active =
                                    auditor.active_mask(state, x, z);
                                for (uint32_t component :
                                     auditor.component_masks(active)) {
                                    const State other = auditor.switched(
                                        state, x, z, component
                                    );
                                    if (
                                        surface_chi(auditor, other)
                                        != chi[state_index]
                                    ) {
                                        throw std::runtime_error(
                                            "fresh component switch not neutral"
                                        );
                                    }
                                    const FactorContext other_context =
                                        build_factor_context(auditor, other);
                                    const PotentialWitness after =
                                        oriented_potential(
                                            auditor,
                                            other_context,
                                            root,
                                            target
                                        );
                                    if (after.distance < before.distance) {
                                        rescued = true;
                                        rescue_x = x;
                                        rescue_z = z;
                                        rescue_component = component;
                                        break;
                                    }
                                }
                            }
                        }
                        if (rescued) {
                            ++fresh_rescues;
                            continue;
                        }

                        std::cout
                            << "{\"status\":\"FRESH_RESCUE_FAILURE\""
                            << ",\"graph6\":\"" << json_escape(record)
                            << "\",\"state_hex\":\""
                            << state_hex(state) << "\""
                            << ",\"chi\":" << chi[state_index]
                            << ",\"root\":" << root
                            << ",\"target\":" << target
                            << ",\"distance\":" << before.distance
                            << ",\"blocker\":" << before.blocker
                            << ",\"used_coordinate_mask\":"
                            << used_coordinates
                            << ",\"P\":[" << before.p_first << ','
                            << before.p_second << ']'
                            << ",\"Q\":[" << before.q_first << ','
                            << before.q_second << ']'
                            << ",\"C\":" << before.circuit
                            << ",\"H\":" << before.root_component
                            << ",\"D\":" << before.target_component
                            << ",\"checked_rescue\":[" << rescue_x << ','
                            << rescue_z << ',' << rescue_component << "]}\n";
                        return 1;
                    }
                }
            }
        }
        std::cerr << "GRAPH_DONE " << graphs << ' ' << record
                  << " flows=" << states.size() << "\n";
    }
    std::cout
        << "{\"status\":\"PASS\",\"graphs\":" << graphs
        << ",\"flows\":" << flows
        << ",\"positive_blocker_tests\":" << positive_blocker_tests
        << ",\"fresh_rescues\":" << fresh_rescues << "}\n";
    return 0;
}
