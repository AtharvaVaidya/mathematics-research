#define main rooted_orbit_base_main
#include "../audit_d5_root_kempe_orbits.cpp"
#undef main

#include <map>

struct ExternalResult {
    int flows = 0;
    int orbits = 0;
    long long interfaces = 0;
    long long orbit_union_failures = 0;
    long long orbit_simultaneous_failures = 0;
    long long all_flow_simultaneous_failures = 0;
    std::map<int, long long> external_masks;
    State first_union_failure;
    int first_union_cap = -1;
    int first_union_root = -1;
    int first_union_mask = -1;
    State first_simultaneous_failure;
    int first_simultaneous_cap = -1;
    int first_simultaneous_root = -1;
};

ExternalResult audit_external(const Auditor& auditor) {
    const int n = auditor.graph.n;
    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    if (edge_count > 31) throw std::runtime_error("uint32 component limit");
    auto all_flows = auditor.enumerate_flows();
    auto unseen = all_flows;
    ExternalResult result;
    result.flows = static_cast<int>(all_flows.size());
    std::vector<unsigned char> all_flow_simultaneous(n * edge_count, 0);

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
                        if (!all_flows.count(other)) throw std::runtime_error("Kempe neighbour absent");
                        if (orbit.insert(other).second) queue.push(other);
                    }
                }
            }
        }
        for (const State& state : orbit) unseen.erase(state);
        ++result.orbits;

        std::vector<unsigned char> masks(n * edge_count, 0);
        std::vector<unsigned char> simultaneous(n * edge_count, 0);
        for (const State& state : orbit) {
            std::vector<unsigned char> current(n * edge_count, 0);
            for (int first = 0; first < 5; ++first) {
                for (int second = first + 1; second < 5; ++second) {
                    const unsigned char pair = static_cast<unsigned char>((1 << first) | (1 << second));
                    uint32_t active = auditor.active_mask(state, first, second);
                    for (uint32_t component : auditor.component_masks(active)) {
                        for (int cap = 0; cap < n; ++cap) {
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
                            if (pair & inactive_label) throw std::runtime_error("bad typed mode");
                            int physical = -1;
                            if (slots[0] == 0 && slots[1] == 1) physical = 0;
                            if (slots[0] == 0 && slots[1] == 2) physical = 1;
                            if (slots[0] == 1 && slots[1] == 2) physical = 2;
                            if (physical < 0) throw std::runtime_error("bad physical pair");
                            uint32_t copy = component;
                            while (copy) {
                                int root = __builtin_ctz(copy);
                                copy &= copy - 1;
                                auto [left, right] = auditor.graph.edges[root];
                                if (left != cap && right != cap) {
                                    current[cap * edge_count + root] |= static_cast<unsigned char>(1 << physical);
                                }
                            }
                        }
                    }
                }
            }
            for (int index = 0; index < n * edge_count; ++index) {
                masks[index] |= current[index];
                if (__builtin_popcount(static_cast<unsigned>(current[index])) >= 2) {
                    simultaneous[index] = 1;
                    all_flow_simultaneous[index] = 1;
                }
            }
        }

        for (int cap = 0; cap < n; ++cap) {
            for (int root = 0; root < edge_count; ++root) {
                auto [left, right] = auditor.graph.edges[root];
                if (left == cap || right == cap) continue;
                int mask = masks[cap * edge_count + root];
                ++result.interfaces;
                ++result.external_masks[mask];
                if (__builtin_popcount(static_cast<unsigned>(mask)) < 2) {
                    ++result.orbit_union_failures;
                    if (result.first_union_cap < 0) {
                        result.first_union_failure = initial;
                        result.first_union_cap = cap;
                        result.first_union_root = root;
                        result.first_union_mask = mask;
                    }
                }
                if (!simultaneous[cap * edge_count + root]) {
                    ++result.orbit_simultaneous_failures;
                    if (result.first_simultaneous_cap < 0) {
                        result.first_simultaneous_failure = initial;
                        result.first_simultaneous_cap = cap;
                        result.first_simultaneous_root = root;
                    }
                }
            }
        }
    }
    for (int cap = 0; cap < n; ++cap) {
        for (int root = 0; root < edge_count; ++root) {
            auto [left, right] = auditor.graph.edges[root];
            if (left != cap && right != cap && !all_flow_simultaneous[cap * edge_count + root]) {
                ++result.all_flow_simultaneous_failures;
            }
        }
    }
    return result;
}

int main() {
    std::string row;
    int graphs = 0;
    long long flows = 0;
    long long orbits = 0;
    long long interfaces = 0;
    long long orbit_union_failures = 0;
    long long orbit_simultaneous_failures = 0;
    long long all_flow_simultaneous_failures = 0;
    std::map<int, long long> masks;
    bool printed_union_failure = false;
    bool printed_simultaneous_failure = false;
    while (std::getline(std::cin, row)) {
        if (row.empty() || row[0] == '>') continue;
        Graph graph = decode_graph6(row);
        if (graph.n != 14) throw std::runtime_error("order 14 required");
        Auditor auditor(graph);
        ExternalResult result = audit_external(auditor);
        ++graphs;
        flows += result.flows;
        orbits += result.orbits;
        interfaces += result.interfaces;
        orbit_union_failures += result.orbit_union_failures;
        orbit_simultaneous_failures += result.orbit_simultaneous_failures;
        all_flow_simultaneous_failures += result.all_flow_simultaneous_failures;
        for (const auto& [mask, count] : result.external_masks) masks[mask] += count;
        std::cerr << "graph=" << graphs << " flows=" << result.flows
                  << " orbits=" << result.orbits
                  << " orbit_union_failures=" << result.orbit_union_failures
                  << " orbit_simultaneous_failures=" << result.orbit_simultaneous_failures
                  << " all_flow_simultaneous_failures=" << result.all_flow_simultaneous_failures << "\n";
        if (result.first_union_cap >= 0 && !printed_union_failure) {
            std::cout << "FIRST_ORBIT_UNION_FAILURE graph=" << graphs << " graph6=" << row
                      << " cap=" << result.first_union_cap << " root=" << result.first_union_root
                      << " external_mask=" << result.first_union_mask
                      << " initial_hex=" << state_hex(result.first_union_failure) << "\n";
            printed_union_failure = true;
        }
        if (result.first_simultaneous_cap >= 0 && !printed_simultaneous_failure) {
            std::cout << "FIRST_ORBIT_SIMULTANEOUS_FAILURE graph=" << graphs << " graph6=" << row
                      << " cap=" << result.first_simultaneous_cap
                      << " root=" << result.first_simultaneous_root
                      << " initial_hex=" << state_hex(result.first_simultaneous_failure) << "\n";
            printed_simultaneous_failure = true;
        }
    }
    std::cout << "ORDER14 graphs=" << graphs << " flows_mod_s5=" << flows
              << " kempe_orbits_mod_s5=" << orbits
              << " orbit_interfaces=" << interfaces
              << " orbit_union_failures=" << orbit_union_failures
              << " orbit_simultaneous_failures=" << orbit_simultaneous_failures
              << " all_flow_simultaneous_failures=" << all_flow_simultaneous_failures
              << " masks=";
    bool first = true;
    for (const auto& [mask, count] : masks) {
        if (!first) std::cout << ",";
        first = false;
        std::cout << mask << ":" << count;
    }
    std::cout << " PASS\n";
    return all_flow_simultaneous_failures ? 1 : 0;
}
