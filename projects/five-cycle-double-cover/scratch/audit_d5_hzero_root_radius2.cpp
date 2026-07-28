// Targeted audit of the surviving H=0 radius-two root-transition lemma.
//
// For every normalized D5 flow, every ordered saturated disjoint root pair,
// and both oriented line triangles at the first root, retain the all-bad
// lifts with K1=K3.  From either endpoint, test every length-one and
// length-two sequence of factor-component switches containing exactly one
// root.  Stop with a literal witness if no rescue exists.

#define main d5_root_orbit_audit_unused_main
#include "audit_d5_root_kempe_orbits.cpp"
#undef main

#include <bit>
#include <tuple>

struct HZeroCounts {
    long long flows = 0;
    long long saturated_bad_ordered_roots = 0;
    long long hzero_loops = 0;
    long long nonempty_support = 0;
    long long radius_one = 0;
    long long radius_two = 0;
    long long failures = 0;
};

static State raw_switched(
    const State& state,
    int first,
    int second,
    uint32_t component
) {
    State answer = state;
    for (int edge = 0; edge < static_cast<int>(state.size()); ++edge) {
        if ((component >> edge) & 1) {
            answer[edge] = static_cast<char>(
                Auditor::transpose_label(
                    static_cast<unsigned char>(state[edge]), first, second
                )
            );
        }
    }
    return answer;
}

static uint32_t root_component(
    const Auditor& auditor,
    const State& state,
    int first,
    int second,
    int root
) {
    for (uint32_t component :
         auditor.component_masks(auditor.active_mask(state, first, second))) {
        if ((component >> root) & 1) return component;
    }
    throw std::runtime_error("active root has no factor component");
}

static bool root_good(
    const Auditor& auditor,
    const State& state,
    int first_root,
    int second_root
) {
    for (int first = 0; first < 5; ++first) {
        for (int second = first + 1; second < 5; ++second) {
            for (uint32_t component :
                 auditor.component_masks(
                     auditor.active_mask(state, first, second)
                 )) {
                if (
                    ((component >> first_root) & 1)
                    && ((component >> second_root) & 1)
                ) return true;
            }
        }
    }
    return false;
}

struct Move {
    State state;
    int root;
    int first;
    int second;
    uint32_t component;
};

static std::vector<Move> root_moves(
    const Auditor& auditor,
    const State& state,
    int first_root,
    int second_root
) {
    std::vector<Move> answer;
    for (int root : {first_root, second_root}) {
        const unsigned char label =
            static_cast<unsigned char>(state[root]);
        for (int first = 0; first < 5; ++first) {
            for (int second = first + 1; second < 5; ++second) {
                const unsigned char pair =
                    static_cast<unsigned char>(
                        (1 << first) | (1 << second)
                    );
                if (std::popcount(
                        static_cast<unsigned int>(label & pair)
                    ) != 1) continue;
                const uint32_t component =
                    root_component(auditor, state, first, second, root);
                const int other =
                    root == first_root ? second_root : first_root;
                if ((component >> other) & 1) {
                    throw std::runtime_error(
                        "root-bad state has common root component"
                    );
                }
                answer.push_back({
                    raw_switched(state, first, second, component),
                    root,
                    first,
                    second,
                    component,
                });
            }
        }
    }
    if (answer.size() != 12) {
        throw std::runtime_error("root-bad state does not have 12 moves");
    }
    return answer;
}

static int rescue_radius(
    const Auditor& auditor,
    const State& state,
    int first_root,
    int second_root
) {
    const auto first_layer =
        root_moves(auditor, state, first_root, second_root);
    for (const Move& move : first_layer) {
        if (root_good(
                auditor, move.state, first_root, second_root
            )) return 1;
    }
    for (const Move& move : first_layer) {
        const auto second_layer =
            root_moves(auditor, move.state, first_root, second_root);
        for (const Move& last : second_layer) {
            if (root_good(
                    auditor, last.state, first_root, second_root
                )) return 2;
        }
    }
    return 3;
}

static std::array<int, 2> coordinates(unsigned char label) {
    std::array<int, 2> answer = {-1, -1};
    int cursor = 0;
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
        if ((label >> coordinate) & 1) answer[cursor++] = coordinate;
    }
    if (cursor != 2) throw std::runtime_error("non-weight-two label");
    return answer;
}

static std::string edge_list(uint32_t mask, int edge_count) {
    std::string answer = "[";
    bool first = true;
    for (int edge = 0; edge < edge_count; ++edge) {
        if (!((mask >> edge) & 1)) continue;
        if (!first) answer += ",";
        answer += std::to_string(edge);
        first = false;
    }
    answer += "]";
    return answer;
}

static bool audit_graph(
    const std::string& graph6,
    int graph_index,
    HZeroCounts& counts
) {
    Graph graph = decode_graph6(graph6);
    Auditor auditor(graph);
    auto flow_set = auditor.enumerate_flows();
    std::vector<State> states(flow_set.begin(), flow_set.end());
    std::sort(states.begin(), states.end());
    counts.flows += static_cast<long long>(states.size());
    const int edge_count = static_cast<int>(graph.edges.size());

    for (const State& initial : states) {
        unsigned char used = 0;
        for (unsigned char label : initial) used |= label;
        if (used != 31) continue;

        for (int first_root = 0; first_root < edge_count; ++first_root) {
            for (int second_root = 0;
                 second_root < edge_count;
                 ++second_root) {
                if (first_root == second_root) continue;
                const unsigned char first_label =
                    static_cast<unsigned char>(initial[first_root]);
                const unsigned char second_label =
                    static_cast<unsigned char>(initial[second_root]);
                if (first_label & second_label) continue;
                if (root_good(
                        auditor, initial, first_root, second_root
                    )) continue;
                ++counts.saturated_bad_ordered_roots;

                const auto first_coordinates = coordinates(first_label);
                const auto second_coordinates = coordinates(second_label);
                int hole = -1;
                for (int coordinate = 0; coordinate < 5; ++coordinate) {
                    if (
                        coordinate != first_coordinates[0]
                        && coordinate != first_coordinates[1]
                        && coordinate != second_coordinates[0]
                        && coordinate != second_coordinates[1]
                    ) {
                        hole = coordinate;
                    }
                }
                if (hole < 0) throw std::runtime_error("missing hole");

                for (int orientation = 0; orientation < 2; ++orientation) {
                    const int a = first_coordinates[orientation];
                    const int b = first_coordinates[1 - orientation];
                    const std::array<std::array<int, 2>, 3> line = {{
                        {std::min(b, hole), std::max(b, hole)},
                        {std::min(a, b), std::max(a, b)},
                        {std::min(a, hole), std::max(a, hole)},
                    }};
                    State state = initial;
                    std::array<uint32_t, 3> circuits{};
                    bool rescued = false;
                    for (int step = 0; step < 3; ++step) {
                        const int left = line[step][0];
                        const int right = line[step][1];
                        circuits[step] = root_component(
                            auditor, state, left, right, first_root
                        );
                        if ((circuits[step] >> second_root) & 1) {
                            rescued = true;
                            break;
                        }
                        state = raw_switched(
                            state, left, right, circuits[step]
                        );
                        if (root_good(
                                auditor, state, first_root, second_root
                            )) {
                            rescued = true;
                            break;
                        }
                    }
                    if (rescued) continue;
                    if (circuits[0] != circuits[2]) continue;

                    ++counts.hzero_loops;
                    const uint32_t support = circuits[0] ^ circuits[1];
                    if (support) ++counts.nonempty_support;

                    const int radius = std::min(
                        rescue_radius(
                            auditor, initial, first_root, second_root
                        ),
                        rescue_radius(
                            auditor, state, first_root, second_root
                        )
                    );
                    if (radius == 1) {
                        ++counts.radius_one;
                    } else if (radius == 2) {
                        ++counts.radius_two;
                    } else {
                        ++counts.failures;
                        std::cout
                            << "{\"status\":\"COUNTEREXAMPLE\""
                            << ",\"graph_index\":" << graph_index
                            << ",\"graph6\":\"" << json_escape(graph6)
                            << "\",\"state_hex\":\""
                            << state_hex(initial) << "\""
                            << ",\"roots\":[" << first_root << ","
                            << second_root << "]"
                            << ",\"line\":[[" << line[0][0] << ","
                            << line[0][1] << "],[" << line[1][0] << ","
                            << line[1][1] << "],[" << line[2][0] << ","
                            << line[2][1] << "]]"
                            << ",\"K1\":" << edge_list(
                                circuits[0], edge_count
                            )
                            << ",\"K2\":" << edge_list(
                                circuits[1], edge_count
                            )
                            << ",\"Z\":" << edge_list(
                                support, edge_count
                            )
                            << "}\n";
                        return false;
                    }
                }
            }
        }
    }

    std::cout
        << "{\"status\":\"GRAPH_DONE\",\"graph_index\":" << graph_index
        << ",\"graph6\":\"" << json_escape(graph6)
        << "\",\"flows_mod_s5\":" << states.size()
        << ",\"hzero_loops_total\":" << counts.hzero_loops
        << ",\"radius_one_total\":" << counts.radius_one
        << ",\"radius_two_total\":" << counts.radius_two
        << "}\n";
    return true;
}

int main() {
    std::string graph6;
    int graph_index = 0;
    HZeroCounts counts;
    while (std::getline(std::cin, graph6)) {
        if (graph6.empty()) continue;
        ++graph_index;
        if (!audit_graph(graph6, graph_index, counts)) return 1;
    }
    std::cout
        << "{\"status\":\"PASS\",\"graphs\":" << graph_index
        << ",\"flows_mod_s5\":" << counts.flows
        << ",\"saturated_bad_ordered_roots\":"
        << counts.saturated_bad_ordered_roots
        << ",\"hzero_loops\":" << counts.hzero_loops
        << ",\"nonempty_support\":" << counts.nonempty_support
        << ",\"radius_one\":" << counts.radius_one
        << ",\"radius_two\":" << counts.radius_two
        << ",\"failures\":" << counts.failures << "}\n";
    return counts.failures ? 1 : 0;
}
