// Exact terminal-chi census for the lexicographic pair
// (factor-chain distance, cyclic foreign-Q-block potential).
//
// For each ordered root pair, b*=0 means either an eligible shortest
// first-pair choice has no foreign blocker, or no eligible shared-pair
// root-Q choice exists.  The latter means only that this particular
// obstruction is absent, not that the roots are good.  The audit
// exhausts every fixed-(d,b*) subplateau and requires a neutral exit
// to lexicographically smaller (d,b*).

#define main d5_root_orbit_audit_unused_main
#include "audit_d5_root_kempe_orbits.cpp"
#undef main

#include <climits>
#include <tuple>
#include <unordered_map>

struct Factor {
    int first;
    int second;
    uint32_t mask;
};

struct FactorContext {
    std::vector<Factor> rows;
    std::vector<std::vector<int>> adjacency;
    std::vector<std::vector<int>> target_distance;
};

struct PotentialWitness {
    int distance = INT_MAX;
    int blocker = INT_MAX;
    int root = -1;
    int target = -1;
    int p_first = -1;
    int p_second = -1;
    int q_first = -1;
    int q_second = -1;
    uint32_t circuit = 0;
    uint32_t root_component = 0;
    uint32_t target_component = 0;
    std::array<int, 2> first_blocker = {-1, -1};
    std::array<int, 2> join_edge = {-1, -1};
    std::vector<std::tuple<int, int, uint32_t>> candidates;
};

static std::vector<Factor> all_factors(
    const Auditor& auditor,
    const State& state
) {
    std::vector<Factor> answer;
    for (int first = 0; first < 5; ++first) {
        for (int second = first + 1; second < 5; ++second) {
            const uint32_t active =
                auditor.active_mask(state, first, second);
            for (uint32_t component : auditor.component_masks(active)) {
                answer.push_back({first, second, component});
            }
        }
    }
    return answer;
}

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

static std::vector<int> circuit_order(
    const Auditor& auditor,
    uint32_t circuit,
    int root
) {
    auto neighbours = [&](int edge) {
        std::vector<int> answer;
        for (int vertex :
             {auditor.graph.edges[edge].first,
              auditor.graph.edges[edge].second}) {
            for (int other : auditor.graph.incidence[vertex]) {
                if (other != edge && ((circuit >> other) & 1)) {
                    answer.push_back(other);
                }
            }
        }
        std::sort(answer.begin(), answer.end());
        answer.erase(std::unique(answer.begin(), answer.end()), answer.end());
        if (answer.size() != 2) {
            throw std::runtime_error("factor component is not a circuit");
        }
        return answer;
    };

    std::vector<int> answer = {root};
    int previous = root;
    int current = neighbours(root).front();
    while (current != root) {
        answer.push_back(current);
        const std::vector<int> adjacent = neighbours(current);
        const int following =
            adjacent[0] == previous ? adjacent[1] : adjacent[0];
        previous = current;
        current = following;
    }
    if (answer.size() != static_cast<std::size_t>(__builtin_popcount(circuit))) {
        throw std::runtime_error("bad circuit traversal");
    }
    return answer;
}

static FactorContext build_factor_context(
    const Auditor& auditor,
    const State& state
) {
    FactorContext context;
    context.rows = all_factors(auditor, state);
    const int count = static_cast<int>(context.rows.size());
    context.adjacency.resize(count);
    for (int left = 0; left < count; ++left) {
        for (int right = left + 1; right < count; ++right) {
            if (context.rows[left].mask & context.rows[right].mask) {
                context.adjacency[left].push_back(right);
                context.adjacency[right].push_back(left);
            }
        }
    }
    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    context.target_distance.assign(
        edge_count, std::vector<int>(count, INT_MAX)
    );
    for (int target = 0; target < edge_count; ++target) {
        std::queue<int> queue;
        for (int index = 0; index < count; ++index) {
            if ((context.rows[index].mask >> target) & 1) {
                context.target_distance[target][index] = 1;
                queue.push(index);
            }
        }
        while (!queue.empty()) {
            const int current = queue.front();
            queue.pop();
            for (int other : context.adjacency[current]) {
                if (context.target_distance[target][other] == INT_MAX) {
                    context.target_distance[target][other] =
                        context.target_distance[target][current] + 1;
                    queue.push(other);
                }
            }
        }
    }
    return context;
}

static PotentialWitness oriented_potential(
    const Auditor& auditor,
    const FactorContext& context,
    int root,
    int target
) {
    const std::vector<Factor>& rows = context.rows;
    const std::vector<std::vector<int>>& adjacency = context.adjacency;
    const std::vector<int>& target_distance =
        context.target_distance[target];
    const int count = static_cast<int>(rows.size());
    PotentialWitness best;
    for (int index = 0; index < count; ++index) {
        if ((rows[index].mask >> root) & 1) {
            best.distance = std::min(best.distance, target_distance[index]);
        }
    }
    best.root = root;
    best.target = target;
    if (best.distance <= 1 || best.distance == INT_MAX) return best;

    for (int first = 0; first < count; ++first) {
        if (!((rows[first].mask >> root) & 1)) continue;
        for (int second : adjacency[first]) {
            if (1 + target_distance[second] != best.distance) continue;
            const Factor& p = rows[first];
            const Factor& q = rows[second];
            const int overlap =
                (p.first == q.first) + (p.first == q.second)
                + (p.second == q.first) + (p.second == q.second);
            if (overlap != 1) continue;

            int root_q = -1;
            for (int index = 0; index < count; ++index) {
                if (
                    rows[index].first == q.first
                    && rows[index].second == q.second
                    && ((rows[index].mask >> root) & 1)
                ) {
                    if (root_q >= 0) {
                        throw std::runtime_error("two root Q-components");
                    }
                    root_q = index;
                }
            }
            if (root_q < 0 || root_q == second) continue;

            std::vector<int> owner(auditor.graph.edges.size(), -1);
            for (int index = 0; index < count; ++index) {
                if (
                    rows[index].first != q.first
                    || rows[index].second != q.second
                ) continue;
                uint32_t copy = rows[index].mask & p.mask;
                while (copy) {
                    const int edge = __builtin_ctz(copy);
                    copy &= copy - 1;
                    if (owner[edge] >= 0) {
                        throw std::runtime_error("two Q owners");
                    }
                    owner[edge] = index;
                }
            }

            const std::vector<int> order =
                circuit_order(auditor, p.mask, root);
            const int n = static_cast<int>(order.size());
            std::array<int, 2> blocker_count = {0, 0};
            std::array<int, 2> first_blocker = {-1, -1};
            std::array<int, 2> join_edge = {-1, -1};
            for (int orientation = 0; orientation < 2; ++orientation) {
                const int step = orientation == 0 ? 1 : -1;
                int cursor = step;
                while (owner[order[(cursor % n + n) % n]] == root_q) {
                    cursor += step;
                    if (std::abs(cursor) > n) {
                        throw std::runtime_error("root Q fills P circuit");
                    }
                }
                int previous_owner = -2;
                while (std::abs(cursor) <= n) {
                    const int edge = order[(cursor % n + n) % n];
                    const int current_owner = owner[edge];
                    if (current_owner != previous_owner) {
                        if (current_owner == second) {
                            join_edge[orientation] = edge;
                            break;
                        }
                        if (current_owner >= 0 && current_owner != root_q) {
                            if (first_blocker[orientation] < 0) {
                                first_blocker[orientation] = current_owner;
                            }
                            ++blocker_count[orientation];
                        }
                    }
                    previous_owner = current_owner;
                    cursor += step;
                }
                if (join_edge[orientation] < 0) {
                    throw std::runtime_error("D absent from P circuit");
                }
            }
            const int blocker = std::min(blocker_count[0], blocker_count[1]);
            if (blocker <= best.blocker) {
                if (blocker < best.blocker) {
                    best.candidates.clear();
                }
                best.candidates.emplace_back(
                    q.first, q.second, rows[root_q].mask
                );
                for (int orientation = 0; orientation < 2; ++orientation) {
                    if (first_blocker[orientation] >= 0) {
                        best.candidates.emplace_back(
                            q.first,
                            q.second,
                            rows[first_blocker[orientation]].mask
                        );
                    }
                }
            }
            if (blocker < best.blocker) {
                best.blocker = blocker;
                best.p_first = p.first;
                best.p_second = p.second;
                best.q_first = q.first;
                best.q_second = q.second;
                best.circuit = p.mask;
                best.root_component = rows[root_q].mask;
                best.target_component = q.mask;
                for (int orientation = 0; orientation < 2; ++orientation) {
                    best.first_blocker[orientation] =
                        first_blocker[orientation] < 0
                        ? -1
                        : rows[first_blocker[orientation]].mask;
                    best.join_edge[orientation] = join_edge[orientation];
                }
            }
        }
    }
    std::sort(best.candidates.begin(), best.candidates.end());
    best.candidates.erase(
        std::unique(best.candidates.begin(), best.candidates.end()),
        best.candidates.end()
    );
    return best;
}

#ifndef D5_CYCLIC_BLOCK_LIBRARY
int main() {
    std::string record;
    long long graphs = 0;
    long long flows = 0;
    long long terminal_states = 0;
    long long oriented_root_tests = 0;
    long long applicable = 0;
    long long positive_blocker_tests = 0;
    long long fixed_distance_blocker_plateaus = 0;
    int maximum_blocker = 0;
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
            terminal_states += queue.size();
            // Exhaust every fixed-(distance,effective-blocker) component
            // inside this terminal equal-chi plateau and require a neutral
            // boundary edge with lexicographically smaller (d,mu*).
            const int edge_count =
                static_cast<int>(auditor.graph.edges.size());
            const int ordered_pairs = edge_count * edge_count;
            std::vector<std::vector<unsigned char>> distance_level(
                queue.size(),
                std::vector<unsigned char>(ordered_pairs, 0)
            );
            std::vector<std::vector<unsigned char>> blocker_level(
                queue.size(),
                std::vector<unsigned char>(ordered_pairs, 0)
            );
            std::vector<FactorContext> factor_contexts;
            factor_contexts.reserve(queue.size());
            for (int state : queue) {
                factor_contexts.push_back(
                    build_factor_context(auditor, states[state])
                );
            }
            std::vector<int> global_to_local(states.size(), -1);
            for (int local = 0;
                 local < static_cast<int>(queue.size());
                 ++local) {
                global_to_local[queue[local]] = local;
                for (int root = 0; root < edge_count; ++root) {
                    for (int target = 0; target < edge_count; ++target) {
                        if (root == target) continue;
                        const PotentialWitness metric =
                            oriented_potential(
                                auditor,
                                factor_contexts[local],
                                root,
                                target
                            );
                        ++oriented_root_tests;
                        if (
                            metric.distance > 1
                            && metric.blocker != INT_MAX
                        ) {
                            ++applicable;
                            maximum_blocker =
                                std::max(
                                    maximum_blocker,
                                    metric.blocker
                                );
                            if (metric.blocker > 0) {
                                ++positive_blocker_tests;
                            }
                        }
                        const int position = root * edge_count + target;
                        distance_level[local][position] =
                            static_cast<unsigned char>(metric.distance);
                        blocker_level[local][position] =
                            static_cast<unsigned char>(
                                metric.blocker == INT_MAX
                                ? 0
                                : metric.blocker
                            );
                    }
                }
            }

            std::vector<unsigned char> fixed_seen(queue.size(), 0);
            std::vector<int> fixed_queue;
            for (int root = 0; root < edge_count; ++root) {
                for (int target = 0; target < edge_count; ++target) {
                    if (root == target) continue;
                    std::fill(
                        fixed_seen.begin(), fixed_seen.end(), 0
                    );
                    const int position = root * edge_count + target;
                    for (int fixed_start = 0;
                         fixed_start < static_cast<int>(queue.size());
                         ++fixed_start) {
                        const int level_d =
                            distance_level[fixed_start][position];
                        const int level_mu =
                            blocker_level[fixed_start][position];
                        if (level_d <= 1 || fixed_seen[fixed_start]) {
                            continue;
                        }
                        ++fixed_distance_blocker_plateaus;
                        fixed_queue.clear();
                        fixed_queue.push_back(fixed_start);
                        fixed_seen[fixed_start] = 1;
                        bool descent = false;
                        for (std::size_t cursor = 0;
                             cursor < fixed_queue.size();
                             ++cursor) {
                            const int local = fixed_queue[cursor];
                            const int current = queue[local];
                            for (int other : adjacency[current]) {
                                const int other_local =
                                    global_to_local[other];
                                if (other_local < 0) continue;
                                const int other_d =
                                    distance_level[other_local][position];
                                const int other_mu =
                                    blocker_level[other_local][position];
                                if (
                                    other_d < level_d
                                    || (
                                        other_d == level_d
                                        && other_mu < level_mu
                                    )
                                ) {
                                    descent = true;
                                }
                                if (
                                    other_d == level_d
                                    && other_mu == level_mu
                                    && !fixed_seen[other_local]
                                ) {
                                    fixed_seen[other_local] = 1;
                                    fixed_queue.push_back(other_local);
                                }
                            }
                        }
                        if (!descent) {
                            const int failure_state =
                                queue[fixed_start];
                            const PotentialWitness witness =
                                oriented_potential(
                                    auditor,
                                    factor_contexts[fixed_start],
                                    root,
                                    target
                                );
                            std::cout
                                << "{\"status\":\"LEX_PLATEAU_FAILURE\""
                                << ",\"graph6\":\""
                                << json_escape(record)
                                << "\",\"state_hex\":\""
                                << state_hex(states[failure_state])
                                << "\",\"chi\":" << chi[failure_state]
                                << ",\"root\":" << root
                                << ",\"target\":" << target
                                << ",\"distance\":" << level_d
                                << ",\"blocker\":" << level_mu
                                << ",\"chi_plateau_size\":"
                                << queue.size()
                                << ",\"fixed_plateau_size\":"
                                << fixed_queue.size()
                                << ",\"P\":[" << witness.p_first << ','
                                << witness.p_second << ']'
                                << ",\"Q\":[" << witness.q_first << ','
                                << witness.q_second << ']'
                                << ",\"C\":" << witness.circuit
                                << ",\"H\":"
                                << witness.root_component
                                << ",\"D\":"
                                << witness.target_component
                                << "}\n";
                            return 1;
                        }
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
        << ",\"terminal_states\":" << terminal_states
        << ",\"oriented_root_tests\":" << oriented_root_tests
        << ",\"applicable\":" << applicable
        << ",\"positive_blocker_tests\":" << positive_blocker_tests
        << ",\"fixed_distance_blocker_plateaus\":"
        << fixed_distance_blocker_plateaus
        << ",\"maximum_blocker\":" << maximum_blocker << "}\n";
    return 0;
}
#endif
