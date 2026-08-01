#define main typed_cap_original_main
#include "../d5-typed-cap-double-star-frontier-20260731/audit_d5_typed_cap_ports.cpp"
#undef main

#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <string>

// Complete exact census of the all-flow simultaneous property.  For every
// proper rooted interface (z,r), some one D5 flow must have external root
// factors whose physical two-port pairs cover all three ports of z.

int main() {
    std::string row;
    long long graph_count = 0;
    long long flow_count = 0;
    long long interface_count = 0;
    long long witnessed_count = 0;
    while (std::cin >> row) {
        if (!row.empty() && row[0] == '>') continue;
        Graph graph = decode_graph6(row);
        Audit audit(graph);
        const auto all = audit.flows();
        flow_count += static_cast<long long>(all.size());

        const int m = static_cast<int>(graph.edges.size());
        std::vector<unsigned char> witnessed(graph.n * m, 0);
        std::vector<unsigned char> proper(graph.n * m, 0);
        for (int z = 0; z < graph.n; ++z) {
            for (int root = 0; root < m; ++root) {
                if (graph.edges[root].first == z || graph.edges[root].second == z) continue;
                proper[z * m + root] = 1;
                ++interface_count;
            }
        }

        for (const State& state : all) {
            std::vector<unsigned char> external_ports(graph.n * m, 0);
            for (unsigned char pair : LABELS) {
                for (const auto& component : audit.components(state, pair)) {
                    std::vector<unsigned char> in(m, 0);
                    for (int edge : component) in[edge] = 1;
                    for (int z = 0; z < graph.n; ++z) {
                        std::vector<int> slots;
                        int inactive = -1;
                        for (int slot = 0; slot < 3; ++slot) {
                            const int edge = graph.incidence[z][slot];
                            if (in[edge]) slots.push_back(slot);
                            else inactive = slot;
                        }
                        if (slots.size() != 2) continue;
                        const unsigned char inactive_label = static_cast<unsigned char>(
                            state[graph.incidence[z][inactive]]);
                        if (pair == inactive_label) continue;
                        if (pair & inactive_label)
                            throw std::runtime_error("invalid inactive factor relation");
                        const unsigned char port_bits = static_cast<unsigned char>(
                            (1 << slots[0]) | (1 << slots[1]));
                        for (int root : component) {
                            if (proper[z * m + root])
                                external_ports[z * m + root] |= port_bits;
                        }
                    }
                }
            }
            for (int index = 0; index < graph.n * m; ++index) {
                if (external_ports[index] == 7) witnessed[index] = 1;
            }
        }

        for (int index = 0; index < graph.n * m; ++index) {
            if (!proper[index]) continue;
            if (witnessed[index]) {
                ++witnessed_count;
            } else {
                const int z = index / m;
                const int root = index % m;
                std::cout << "FAIL graph=" << graph_count
                          << " z=" << z << " root=" << root << "\n";
            }
        }
        ++graph_count;
    }
    std::cout << "SIMULTANEOUS graphs=" << graph_count
              << " flows=" << flow_count
              << " interfaces=" << interface_count
              << " witnessed=" << witnessed_count << "\n";
    if (witnessed_count != interface_count) return 2;
    std::cout << "PASS\n";
    return 0;
}
