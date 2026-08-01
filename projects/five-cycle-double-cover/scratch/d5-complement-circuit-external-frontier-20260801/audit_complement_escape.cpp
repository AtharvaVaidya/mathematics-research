#define main rooted_orbit_base_main
#include "../audit_d5_root_kempe_orbits.cpp"
#undef main

#include <map>
#include <set>

struct EscapeResult {
    int flows = 0;
    int orbits = 0;
    long long orbit_interfaces = 0;
    long long bad_orbit_interfaces = 0;
    long long one_complement_rescues = 0;
    long long one_complement_failures = 0;
    long long support_avoids_root_and_cap = 0;
    std::map<int, long long> rescue_lengths;
    State first_before;
    State first_after;
    int first_cap = -1;
    int first_root = -1;
    int first_missing = -1;
    uint32_t first_cycle = 0;
};

static void cycle_dfs(
    const Graph& graph,
    int start,
    int vertex,
    int parent_edge,
    uint32_t visited_vertices,
    uint32_t path_edges,
    std::set<uint32_t>& answer
) {
    for (int edge : graph.incidence[vertex]) {
        if (edge == parent_edge) continue;
        auto [left, right] = graph.edges[edge];
        int next = left == vertex ? right : left;
        if (next == start) {
            if (__builtin_popcount(path_edges) >= 2) {
                answer.insert(path_edges | (uint32_t(1) << edge));
            }
            continue;
        }
        // Requiring start to be the least vertex gives one finite search
        // rooted at the canonical least vertex of each simple circuit.
        if (next < start || ((visited_vertices >> next) & 1)) continue;
        cycle_dfs(
            graph,
            start,
            next,
            edge,
            visited_vertices | (uint32_t(1) << next),
            path_edges | (uint32_t(1) << edge),
            answer
        );
    }
}

static std::vector<uint32_t> simple_cycles(const Graph& graph) {
    if (graph.n > 31 || graph.edges.size() > 31) {
        throw std::runtime_error("32-bit circuit enumerator limit");
    }
    std::set<uint32_t> unique;
    for (int start = 0; start < graph.n; ++start) {
        cycle_dfs(
            graph,
            start,
            start,
            -1,
            uint32_t(1) << start,
            0,
            unique
        );
    }
    return std::vector<uint32_t>(unique.begin(), unique.end());
}

static unsigned char fixed_external_mask(
    const Auditor& auditor,
    const State& state,
    int cap,
    int root
) {
    unsigned char result = 0;
    for (int first = 0; first < 5; ++first) {
        for (int second = first + 1; second < 5; ++second) {
            const unsigned char pair = static_cast<unsigned char>(
                (1 << first) | (1 << second)
            );
            uint32_t active = auditor.active_mask(state, first, second);
            for (uint32_t component : auditor.component_masks(active)) {
                if (!((component >> root) & 1)) continue;
                int slots[2] = {-1, -1};
                int count = 0;
                int inactive = -1;
                for (int slot = 0; slot < 3; ++slot) {
                    int edge = auditor.graph.incidence[cap][slot];
                    if ((component >> edge) & 1) {
                        if (count < 2) slots[count] = slot;
                        ++count;
                    } else {
                        inactive = slot;
                    }
                }
                if (count != 2 || inactive < 0) continue;
                unsigned char inactive_label = static_cast<unsigned char>(
                    state[auditor.graph.incidence[cap][inactive]]
                );
                if (pair == inactive_label) continue;
                if (pair & inactive_label) {
                    throw std::runtime_error("invalid typed state");
                }
                int physical = -1;
                if (slots[0] == 0 && slots[1] == 1) physical = 0;
                if (slots[0] == 0 && slots[1] == 2) physical = 1;
                if (slots[0] == 1 && slots[1] == 2) physical = 2;
                if (physical < 0) throw std::runtime_error("invalid cap slots");
                result |= static_cast<unsigned char>(1 << physical);
            }
        }
    }
    return result;
}

static State complement_translate(
    const Auditor& auditor,
    const State& state,
    int missing,
    uint32_t circuit
) {
    const unsigned char shift = static_cast<unsigned char>(31 ^ (1 << missing));
    State answer = state;
    for (int edge = 0; edge < static_cast<int>(state.size()); ++edge) {
        if (!((circuit >> edge) & 1)) continue;
        unsigned char label = static_cast<unsigned char>(state[edge]);
        if ((label >> missing) & 1) {
            throw std::runtime_error("illegal complement translation");
        }
        unsigned char translated = label ^ shift;
        if (!is_label(translated)) throw std::runtime_error("bad translated label");
        answer[edge] = static_cast<char>(translated);
    }
    return auditor.canonical(answer);
}

static bool circuit_avoids_coordinate(
    const State& state,
    uint32_t circuit,
    int coordinate
) {
    while (circuit) {
        int edge = __builtin_ctz(circuit);
        circuit &= circuit - 1;
        if ((static_cast<unsigned char>(state[edge]) >> coordinate) & 1) return false;
    }
    return true;
}

static EscapeResult audit_graph(const Auditor& auditor) {
    const int n = auditor.graph.n;
    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    auto all_flows = auditor.enumerate_flows();
    auto unseen = all_flows;
    const auto circuits = simple_cycles(auditor.graph);
    EscapeResult result;
    result.flows = static_cast<int>(all_flows.size());

    while (!unseen.empty()) {
        State initial = *unseen.begin();
        std::unordered_set<State> orbit = {initial};
        std::queue<State> queue;
        queue.push(initial);
        while (!queue.empty()) {
            State state = queue.front();
            queue.pop();
            for (int first = 0; first < 5; ++first) {
                for (int second = first + 1; second < 5; ++second) {
                    uint32_t active = auditor.active_mask(state, first, second);
                    for (uint32_t component : auditor.component_masks(active)) {
                        State other = auditor.switched(state, first, second, component);
                        if (!all_flows.count(other)) {
                            throw std::runtime_error("Kempe neighbour absent");
                        }
                        if (orbit.insert(other).second) queue.push(other);
                    }
                }
            }
        }
        for (const State& state : orbit) unseen.erase(state);
        ++result.orbits;

        for (int cap = 0; cap < n; ++cap) {
            for (int root = 0; root < edge_count; ++root) {
                auto [left, right] = auditor.graph.edges[root];
                if (left == cap || right == cap) continue;
                ++result.orbit_interfaces;
                bool orbit_good = false;
                for (const State& state : orbit) {
                    if (__builtin_popcount(
                            static_cast<unsigned>(fixed_external_mask(auditor, state, cap, root))
                        ) >= 2) {
                        orbit_good = true;
                        break;
                    }
                }
                if (orbit_good) continue;
                ++result.bad_orbit_interfaces;

                bool rescued = false;
                bool has_disjoint_rescue = false;
                int best_length = edge_count + 1;
                State best_before;
                State best_after;
                int best_missing = -1;
                uint32_t best_circuit = 0;
                for (const State& state : orbit) {
                    for (int missing = 0; missing < 5; ++missing) {
                        for (uint32_t circuit : circuits) {
                            if (!circuit_avoids_coordinate(state, circuit, missing)) continue;
                            State other = complement_translate(auditor, state, missing, circuit);
                            if (!all_flows.count(other)) {
                                throw std::runtime_error("complement neighbour absent");
                            }
                            if (__builtin_popcount(static_cast<unsigned>(
                                    fixed_external_mask(auditor, other, cap, root)
                                )) < 2) {
                                continue;
                            }
                            int length = __builtin_popcount(circuit);
                            uint32_t forbidden = uint32_t(1) << root;
                            for (int edge : auditor.graph.incidence[cap]) {
                                forbidden |= uint32_t(1) << edge;
                            }
                            if ((circuit & forbidden) == 0) {
                                has_disjoint_rescue = true;
                            }
                            if (!rescued || length < best_length ||
                                (length == best_length && circuit < best_circuit)) {
                                rescued = true;
                                best_length = length;
                                best_before = state;
                                best_after = other;
                                best_missing = missing;
                                best_circuit = circuit;
                            }
                        }
                    }
                }
                if (!rescued) {
                    ++result.one_complement_failures;
                    continue;
                }
                ++result.one_complement_rescues;
                ++result.rescue_lengths[best_length];
                if (has_disjoint_rescue) ++result.support_avoids_root_and_cap;
                if (result.first_cap < 0) {
                    result.first_before = best_before;
                    result.first_after = best_after;
                    result.first_cap = cap;
                    result.first_root = root;
                    result.first_missing = best_missing;
                    result.first_cycle = best_circuit;
                }
            }
        }
    }
    return result;
}

int main(int argc, char** argv) {
    if (argc != 3 || std::string(argv[1]) != "--expect-failures") {
        throw std::runtime_error("usage: audit_complement_escape --expect-failures N");
    }
    int expected_failures = std::stoi(argv[2]);
    std::string row;
    int graphs = 0;
    long long flows = 0;
    long long orbits = 0;
    long long interfaces = 0;
    long long bad = 0;
    long long rescued = 0;
    long long failures = 0;
    long long disjoint = 0;
    std::map<int, long long> lengths;
    bool printed = false;
    while (std::getline(std::cin, row)) {
        if (row.empty() || row[0] == '>') continue;
        Graph graph = decode_graph6(row);
        Auditor auditor(graph);
        EscapeResult result = audit_graph(auditor);
        ++graphs;
        flows += result.flows;
        orbits += result.orbits;
        interfaces += result.orbit_interfaces;
        bad += result.bad_orbit_interfaces;
        rescued += result.one_complement_rescues;
        failures += result.one_complement_failures;
        disjoint += result.support_avoids_root_and_cap;
        for (auto [length, count] : result.rescue_lengths) lengths[length] += count;
        std::cerr << "graph=" << graphs
                  << " flows=" << result.flows
                  << " orbits=" << result.orbits
                  << " bad=" << result.bad_orbit_interfaces
                  << " rescued=" << result.one_complement_rescues
                  << " failures=" << result.one_complement_failures << "\n";
        if (!printed && result.first_cap >= 0) {
            std::cout << "FIRST_ESCAPE graph=" << graphs
                      << " graph6=" << row
                      << " cap=" << result.first_cap
                      << " root=" << result.first_root
                      << " missing=" << result.first_missing
                      << " cycle_mask=" << result.first_cycle
                      << " before_hex=" << state_hex(result.first_before)
                      << " after_hex=" << state_hex(result.first_after) << "\n";
            printed = true;
        }
    }
    std::cout << "SUMMARY graphs=" << graphs
              << " flows_mod_s5=" << flows
              << " kempe_orbits_mod_s5=" << orbits
              << " orbit_interfaces=" << interfaces
              << " bad_orbit_interfaces=" << bad
              << " one_complement_rescues=" << rescued
              << " one_complement_failures=" << failures
              << " expected_failures=" << expected_failures
              << " support_avoids_root_and_cap=" << disjoint
              << " lengths=";
    bool first = true;
    for (auto [length, count] : lengths) {
        if (!first) std::cout << ",";
        first = false;
        std::cout << length << ":" << count;
    }
    std::cout << (failures == expected_failures ? " PASS\n" : " FAIL\n");
    return failures == expected_failures ? 0 : 1;
}
