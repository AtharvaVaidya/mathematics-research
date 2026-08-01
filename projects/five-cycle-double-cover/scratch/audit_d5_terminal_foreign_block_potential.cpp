// Audit the lexicographic (factor distance, foreign-block count) target.

#define D5_CHAIN_POTENTIAL_LIBRARY
#include "audit_d5_root_component_chain_potential.cpp"
#undef D5_CHAIN_POTENTIAL_LIBRARY

#include <limits>

struct FactorRecord {
    int first;
    int second;
    uint32_t mask;
};

static int block_surface_chi(const Auditor& auditor, const State& state) {
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

static std::vector<FactorRecord> factor_records(
    const Auditor& auditor,
    const State& state
) {
    std::vector<FactorRecord> answer;
    for (int first = 0; first < 5; ++first) {
        for (int second = first + 1; second < 5; ++second) {
            for (uint32_t component : auditor.component_masks(
                    auditor.active_mask(state, first, second)
                )) {
                if (component) answer.push_back({first, second, component});
            }
        }
    }
    return answer;
}

static std::vector<int> circuit_order(
    const Auditor& auditor,
    uint32_t component,
    int root
) {
    std::vector<std::vector<int>> incidence(auditor.graph.n);
    uint32_t copy = component;
    while (copy) {
        const int edge = __builtin_ctz(copy);
        copy &= copy - 1;
        auto [left, right] = auditor.graph.edges[edge];
        incidence[left].push_back(edge);
        incidence[right].push_back(edge);
    }
    for (const auto& row : incidence) {
        if (!row.empty() && row.size() != 2) {
            throw std::runtime_error("factor component is not a circuit");
        }
    }
    int vertex = auditor.graph.edges[root].second;
    int previous = root;
    std::vector<int> answer = {root};
    while (true) {
        const auto& row = incidence[vertex];
        const int edge = row[0] != previous ? row[0] : row[1];
        if (edge == root) return answer;
        answer.push_back(edge);
        auto [left, right] = auditor.graph.edges[edge];
        vertex = left ^ right ^ vertex;
        previous = edge;
    }
}

static int orientation_block_count(
    const std::vector<int>& order,
    bool reverse,
    int component_h,
    int component_d,
    const std::vector<int>& q_component_by_edge
) {
    int count = 0;
    int previous_foreign = -1;
    const int size = static_cast<int>(order.size());
    for (int step = 1; step < size; ++step) {
        const int position = reverse ? size - step : step;
        const int component = q_component_by_edge[order[position]];
        if (component == component_d) return count;
        if (component < 0 || component == component_h) {
            previous_foreign = -1;
        } else if (component != previous_foreign) {
            ++count;
            previous_foreign = component;
        }
    }
    throw std::runtime_error("D not encountered on C");
}

static unsigned char ordered_foreign_block_potential(
    const Auditor& auditor,
    const std::vector<FactorRecord>& factors,
    int root,
    int target,
    int rooted_distance
) {
    if (rooted_distance <= 1) return 255;
    const int factor_count = static_cast<int>(factors.size());
    std::vector<std::vector<int>> adjacency(factor_count);
    for (int left = 0; left < factor_count; ++left) {
        for (int right = left + 1; right < factor_count; ++right) {
            if (factors[left].mask & factors[right].mask) {
                adjacency[left].push_back(right);
                adjacency[right].push_back(left);
            }
        }
    }
    std::vector<int> node_distance(factor_count, -1);
    std::queue<int> queue;
    for (int node = 0; node < factor_count; ++node) {
        if ((factors[node].mask >> target) & 1) {
            node_distance[node] = 1;
            queue.push(node);
        }
    }
    while (!queue.empty()) {
        const int current = queue.front();
        queue.pop();
        for (int other : adjacency[current]) {
            if (node_distance[other] < 0) {
                node_distance[other] = node_distance[current] + 1;
                queue.push(other);
            }
        }
    }

    int best = 254;  // Temporary sentinel: no eligible root component.
    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    for (int first_node = 0; first_node < factor_count; ++first_node) {
        const auto& first_factor = factors[first_node];
        if (!((first_factor.mask >> root) & 1) ||
            node_distance[first_node] != rooted_distance) {
            continue;
        }
        const std::vector<int> order =
            circuit_order(auditor, first_factor.mask, root);
        for (int second_node : adjacency[first_node]) {
            const auto& second_factor = factors[second_node];
            if (node_distance[second_node] != rooted_distance - 1) continue;
            const unsigned int first_pair_mask =
                (1u << first_factor.first) |
                (1u << first_factor.second);
            const unsigned int second_pair_mask =
                (1u << second_factor.first) |
                (1u << second_factor.second);
            if (__builtin_popcount(first_pair_mask & second_pair_mask) != 1) {
                continue;
            }

            std::vector<int> q_nodes;
            int component_h = -1;
            int component_d = -1;
            for (int node = 0; node < factor_count; ++node) {
                if (factors[node].first == second_factor.first &&
                    factors[node].second == second_factor.second) {
                    const int position = static_cast<int>(q_nodes.size());
                    q_nodes.push_back(node);
                    if ((factors[node].mask >> root) & 1) {
                        component_h = position;
                    }
                    if (node == second_node) component_d = position;
                }
            }
            if (component_h < 0 || component_h == component_d) continue;
            std::vector<int> by_edge(edge_count, -1);
            for (int position = 0;
                 position < static_cast<int>(q_nodes.size());
                 ++position) {
                uint32_t copy = factors[q_nodes[position]].mask;
                while (copy) {
                    const int edge = __builtin_ctz(copy);
                    copy &= copy - 1;
                    by_edge[edge] = position;
                }
            }
            const int forward = orientation_block_count(
                order, false, component_h, component_d, by_edge
            );
            const int backward = orientation_block_count(
                order, true, component_h, component_d, by_edge
            );
            best = std::min(best, std::min(forward, backward));
        }
    }
    // b*=0 means that the shared-coordinate obstruction is absent.  It is
    // not a success state: the fixed-(d,b*) plateau audit below still
    // requires an incident neutral move to smaller d when d>1.
    return static_cast<unsigned char>(best == 254 ? 0 : best);
}

static std::vector<unsigned char> foreign_block_potentials(
    const Auditor& auditor,
    const State& state,
    const std::vector<unsigned char>& distances,
    bool allow_endpoint_reversal
) {
    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    const int root_pair_count = edge_count * (edge_count - 1) / 2;
    const std::vector<FactorRecord> factors =
        factor_records(auditor, state);
    std::vector<unsigned char> answer(root_pair_count, 255);
    for (int root = 0; root < edge_count; ++root) {
        for (int target = root + 1; target < edge_count; ++target) {
            const int pair =
                Auditor::pair_index(edge_count, root, target);
            const int distance = distances[pair];
            if (distance <= 1) continue;
            unsigned char value = ordered_foreign_block_potential(
                auditor, factors, root, target, distance
            );
            if (allow_endpoint_reversal) {
                value = std::min(
                    value,
                    ordered_foreign_block_potential(
                        auditor, factors, target, root, distance
                    )
                );
            }
            answer[pair] = value;
        }
    }
    return answer;
}

struct BlockAuditResult {
    int flows = 0;
    long long terminal_plateaus = 0;
    long long metric_subplateaus = 0;
    bool failure = false;
    State failure_state;
    int failure_root = -1;
    int failure_target = -1;
    int failure_distance = -1;
    int failure_blocks = -1;
    int failure_subplateau_size = 0;
};

static BlockAuditResult audit_block_potential(
    const Auditor& auditor,
    bool allow_endpoint_reversal
) {
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
                for (uint32_t component : auditor.component_masks(
                        auditor.active_mask(states[state], first, second)
                    )) {
                    State other = auditor.switched(
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
    std::vector<int> chis(states.size());
    std::vector<std::vector<unsigned char>> distances(states.size());
    std::vector<std::vector<unsigned char>> blocks(states.size());
    for (int state = 0; state < static_cast<int>(states.size()); ++state) {
        chis[state] = block_surface_chi(auditor, states[state]);
        distances[state] = chain_distances(auditor, states[state]);
        blocks[state] = foreign_block_potentials(
            auditor,
            states[state],
            distances[state],
            allow_endpoint_reversal
        );
    }

    BlockAuditResult result;
    result.flows = static_cast<int>(states.size());
    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    const int root_pair_count = edge_count * (edge_count - 1) / 2;
    std::vector<unsigned char> chi_seen(states.size(), 0);
    std::vector<unsigned char> in_plateau(states.size(), 0);
    std::vector<unsigned char> metric_seen(states.size(), 0);
    std::vector<int> queue;

    for (int start = 0; start < static_cast<int>(states.size()); ++start) {
        if (chi_seen[start]) continue;
        const int level = chis[start];
        queue.clear();
        queue.push_back(start);
        chi_seen[start] = 1;
        bool terminal = true;
        for (std::size_t cursor = 0; cursor < queue.size(); ++cursor) {
            const int current = queue[cursor];
            for (int other : adjacency[current]) {
                if (chis[other] > level) terminal = false;
                if (chis[other] == level && !chi_seen[other]) {
                    chi_seen[other] = 1;
                    queue.push_back(other);
                }
            }
        }
        if (!terminal) continue;
        ++result.terminal_plateaus;
        const std::vector<int> plateau = queue;
        for (int state : plateau) in_plateau[state] = 1;

        for (int pair = 0; pair < root_pair_count; ++pair) {
            for (int state : plateau) metric_seen[state] = 0;
            for (int metric_start : plateau) {
                const int distance_level = distances[metric_start][pair];
                const int block_level = blocks[metric_start][pair];
                if (distance_level <= 1 || metric_seen[metric_start]) continue;
                ++result.metric_subplateaus;
                queue.clear();
                queue.push_back(metric_start);
                metric_seen[metric_start] = 1;
                bool descent = false;
                for (std::size_t cursor = 0; cursor < queue.size(); ++cursor) {
                    const int current = queue[cursor];
                    for (int other : adjacency[current]) {
                        if (!in_plateau[other]) continue;
                        const int other_distance = distances[other][pair];
                        const int other_blocks = blocks[other][pair];
                        if (
                            other_distance < distance_level ||
                            (
                                other_distance == distance_level &&
                                other_blocks < block_level
                            )
                        ) {
                            descent = true;
                        }
                        if (
                            other_distance == distance_level &&
                            other_blocks == block_level &&
                            !metric_seen[other]
                        ) {
                            metric_seen[other] = 1;
                            queue.push_back(other);
                        }
                    }
                }
                if (!descent && !result.failure) {
                    result.failure = true;
                    result.failure_state = states[metric_start];
                    result.failure_distance = distance_level;
                    result.failure_blocks = block_level;
                    result.failure_subplateau_size =
                        static_cast<int>(queue.size());
                    for (int left = 0; left < edge_count; ++left) {
                        for (int right = left + 1;
                             right < edge_count;
                             ++right) {
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
        for (int state : plateau) in_plateau[state] = 0;
    }
    return result;
}

int main(int argc, char** argv) {
    bool reverse = false;
    if (argc == 2 && std::string(argv[1]) == "--endpoint-reversal") {
        reverse = true;
    } else if (argc != 1) {
        std::cerr << "usage: " << argv[0] << " [--endpoint-reversal]\n";
        return 2;
    }
    std::string graph6;
    int graphs = 0;
    long long flows = 0;
    long long terminal_plateaus = 0;
    long long metric_subplateaus = 0;
    int failures = 0;
    while (std::getline(std::cin, graph6)) {
        if (graph6.empty()) continue;
        ++graphs;
        const Auditor auditor(decode_graph6(graph6));
        const BlockAuditResult result =
            audit_block_potential(auditor, reverse);
        flows += result.flows;
        terminal_plateaus += result.terminal_plateaus;
        metric_subplateaus += result.metric_subplateaus;
        failures += result.failure;
        std::cout
            << "{\"status\":\"GRAPH_DONE\",\"index\":" << graphs
            << ",\"graph6\":\"" << json_escape(graph6) << "\""
            << ",\"flows_mod_s5\":" << result.flows
            << ",\"terminal_plateaus\":" << result.terminal_plateaus
            << ",\"metric_subplateaus\":" << result.metric_subplateaus
            << ",\"failure\":" << static_cast<int>(result.failure);
        if (result.failure) {
            std::cout
                << ",\"first_failure\":{\"state_hex\":\""
                << state_hex(result.failure_state) << "\""
                << ",\"roots\":[" << result.failure_root << ','
                << result.failure_target << "]"
                << ",\"distance\":" << result.failure_distance
                << ",\"blocks\":" << result.failure_blocks
                << ",\"subplateau_size\":"
                << result.failure_subplateau_size << '}';
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
        << ",\"terminal_plateaus\":" << terminal_plateaus
        << ",\"metric_subplateaus\":" << metric_subplateaus
        << ",\"failures\":" << failures
        << ",\"endpoint_reversal\":" << static_cast<int>(reverse)
        << "}\n";
    return failures ? 1 : 0;
}
