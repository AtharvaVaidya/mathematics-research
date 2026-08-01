// Fast exact audit of the local closed-or-two-neutral strengthening.

#define main d5_root_orbit_audit_unused_main
#include "audit_d5_root_kempe_orbits.cpp"
#undef main

#include <array>
#include <map>
#include <sstream>

static int local_surface_chi(const Auditor& auditor, const State& state) {
    int coordinate_components = 0;
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
        uint32_t mask = 0;
        for (int edge = 0; edge < static_cast<int>(state.size()); ++edge) {
            if (
                (static_cast<unsigned char>(state[edge]) >> coordinate) & 1
            ) {
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

struct ClosedResult {
    int flows = 0;
    long long triples = 0;
    long long no_closed = 0;
    long long strengthening_failures = 0;
    long long boundary_two_nonzero_failures = 0;
    long long minimum_boundary_failures = 0;
    std::map<std::string, long long> feature_histogram;
    std::map<std::string, long long> switch_feature_histogram;
    bool has_first_failure = false;
    State failure_state;
    int failure_vertex = -1;
    int failure_first_edge = -1;
    int failure_second_edge = -1;
    bool has_first_minimum_boundary_failure = false;
    State minimum_boundary_failure_state;
    int minimum_boundary_failure_vertex = -1;
    int minimum_boundary_failure_first_edge = -1;
    int minimum_boundary_failure_second_edge = -1;
};

static ClosedResult audit_closed_or_all_neutral(const Auditor& auditor) {
    const auto flow_set = auditor.enumerate_flows();
    ClosedResult result;
    result.flows = static_cast<int>(flow_set.size());
    const int edge_count = static_cast<int>(auditor.graph.edges.size());
    std::vector<std::vector<int>> incidence(auditor.graph.n);
    for (int edge = 0; edge < edge_count; ++edge) {
        incidence[auditor.graph.edges[edge].first].push_back(edge);
        incidence[auditor.graph.edges[edge].second].push_back(edge);
    }
    for (const auto& row : incidence) {
        if (row.size() != 3) throw std::runtime_error("graph is not cubic");
    }

    for (const State& state : flow_set) {
        const int old_chi = local_surface_chi(auditor, state);
        std::array<std::vector<uint32_t>, 10> through_component;
        std::array<std::vector<int>, 10> through_delta;
        std::array<std::vector<unsigned char>, 10> through_closed;
        std::array<std::vector<int>, 10> through_boundary_size;
        std::array<std::vector<uint32_t>, 10> through_vertices;
        for (int pair = 0; pair < 10; ++pair) {
            through_component[pair].assign(edge_count, 0);
            through_delta[pair].assign(edge_count, 0);
            through_closed[pair].assign(edge_count, 0);
            through_boundary_size[pair].assign(edge_count, 0);
            through_vertices[pair].assign(edge_count, 0);
        }
        int pair_index = 0;
        for (int first = 0; first < 5; ++first) {
            for (int second = first + 1; second < 5; ++second) {
                const uint32_t active =
                    auditor.active_mask(state, first, second);
                const unsigned char pair_label =
                    static_cast<unsigned char>(
                        (1 << first) | (1 << second)
                    );
                for (uint32_t component : auditor.component_masks(active)) {
                    uint32_t vertices = 0;
                    uint32_t copy = component;
                    while (copy) {
                        const int edge = __builtin_ctz(copy);
                        copy &= copy - 1;
                        const auto [left, right] = auditor.graph.edges[edge];
                        vertices |= (uint32_t(1) << left);
                        vertices |= (uint32_t(1) << right);
                    }
                    bool closed = true;
                    int boundary_size = 0;
                    for (int edge = 0; edge < edge_count; ++edge) {
                        if (
                            static_cast<unsigned char>(state[edge])
                            != pair_label
                        ) {
                            continue;
                        }
                        const auto [left, right] = auditor.graph.edges[edge];
                        if (
                            ((vertices >> left) & 1)
                            != ((vertices >> right) & 1)
                        ) {
                            closed = false;
                            ++boundary_size;
                        }
                    }
                    const State switched =
                        auditor.switched(state, first, second, component);
                    const int delta =
                        local_surface_chi(auditor, switched) - old_chi;
                    copy = component;
                    while (copy) {
                        const int edge = __builtin_ctz(copy);
                        copy &= copy - 1;
                        through_component[pair_index][edge] = component;
                        through_delta[pair_index][edge] = delta;
                        through_closed[pair_index][edge] =
                            static_cast<unsigned char>(closed);
                        through_boundary_size[pair_index][edge] =
                            boundary_size;
                        through_vertices[pair_index][edge] = vertices;
                    }
                }
                ++pair_index;
            }
        }

        for (int vertex = 0; vertex < auditor.graph.n; ++vertex) {
            const auto& row = incidence[vertex];
            for (int left = 0; left < 3; ++left) {
                for (int right = left + 1; right < 3; ++right) {
                    const int first_edge = row[left];
                    const int second_edge = row[right];
                    int common = 0;
                    bool has_closed = false;
                    int zero_count = 0;
                    std::vector<int> deltas;
                    std::vector<int> boundary_sizes;
                    std::vector<uint32_t> supports;
                    for (int pair = 0; pair < 10; ++pair) {
                        const uint32_t component =
                            through_component[pair][first_edge];
                        if (
                            !component
                            || !((component >> second_edge) & 1)
                        ) {
                            continue;
                        }
                        ++common;
                        has_closed =
                            has_closed || through_closed[pair][first_edge];
                        if (through_delta[pair][first_edge] == 0) {
                            ++zero_count;
                        }
                        deltas.push_back(through_delta[pair][first_edge]);
                        const int boundary_size =
                            through_boundary_size[pair][first_edge];
                        const int delta = through_delta[pair][first_edge];
                        boundary_sizes.push_back(boundary_size);
                        supports.push_back(
                            through_vertices[pair][first_edge]
                        );
                        if (boundary_size == 2 && delta != 0) {
                            ++result.boundary_two_nonzero_failures;
                        }
                        std::ostringstream switch_feature;
                        switch_feature
                            << "boundary_size=" << boundary_size
                            << ";delta=" << delta;
                        ++result.switch_feature_histogram[
                            switch_feature.str()
                        ];
                    }
                    if (common != 3) {
                        throw std::runtime_error(
                            "local pair does not have three common factors"
                        );
                    }
                    ++result.triples;
                    std::sort(deltas.begin(), deltas.end());
                    std::sort(
                        boundary_sizes.begin(), boundary_sizes.end()
                    );
                    std::sort(supports.begin(), supports.end());
                    const int distinct_supports = static_cast<int>(
                        std::unique(supports.begin(), supports.end())
                        - supports.begin()
                    );
                    std::ostringstream feature;
                    feature << "boundary_sizes=";
                    for (int index = 0; index < 3; ++index) {
                        if (index) feature << ",";
                        feature << boundary_sizes[index];
                    }
                    feature << ";deltas=";
                    for (int index = 0; index < 3; ++index) {
                        if (index) feature << ",";
                        feature << deltas[index];
                    }
                    feature << ";distinct_supports=" << distinct_supports;
                    ++result.feature_histogram[feature.str()];
                    if (boundary_sizes.front() > 2) {
                        ++result.minimum_boundary_failures;
                        if (!result.has_first_minimum_boundary_failure) {
                            result.has_first_minimum_boundary_failure = true;
                            result.minimum_boundary_failure_state = state;
                            result.minimum_boundary_failure_vertex = vertex;
                            result.minimum_boundary_failure_first_edge =
                                first_edge;
                            result.minimum_boundary_failure_second_edge =
                                second_edge;
                        }
                    }
                    if (!has_closed) ++result.no_closed;
                    if (has_closed || zero_count >= 2) continue;
                    ++result.strengthening_failures;
                    if (!result.has_first_failure) {
                        result.has_first_failure = true;
                        result.failure_state = state;
                        result.failure_vertex = vertex;
                        result.failure_first_edge = first_edge;
                        result.failure_second_edge = second_edge;
                    }
                }
            }
        }
    }
    return result;
}

int main() {
    std::string record;
    long long graph_count = 0;
    long long flow_count = 0;
    long long triple_count = 0;
    long long no_closed_count = 0;
    long long failure_count = 0;
    long long boundary_two_nonzero_count = 0;
    long long minimum_boundary_failure_count = 0;
    std::map<std::string, long long> feature_histogram;
    std::map<std::string, long long> switch_feature_histogram;
    while (std::cin >> record) {
        Auditor auditor(decode_graph6(record));
        const ClosedResult result = audit_closed_or_all_neutral(auditor);
        ++graph_count;
        flow_count += result.flows;
        triple_count += result.triples;
        no_closed_count += result.no_closed;
        failure_count += result.strengthening_failures;
        boundary_two_nonzero_count +=
            result.boundary_two_nonzero_failures;
        minimum_boundary_failure_count +=
            result.minimum_boundary_failures;
        for (const auto& [key, count] : result.feature_histogram) {
            feature_histogram[key] += count;
        }
        for (const auto& [key, count] : result.switch_feature_histogram) {
            switch_feature_histogram[key] += count;
        }
        std::cout
            << "{\"status\":\"GRAPH_DONE\",\"index\":" << graph_count
            << ",\"graph6\":\"" << json_escape(record) << "\""
            << ",\"vertices\":" << auditor.graph.n
            << ",\"flows_mod_s5\":" << result.flows
            << ",\"local_edge_pair_triples\":" << result.triples
            << ",\"no_closed_candidate\":" << result.no_closed
            << ",\"no_closed_fewer_than_two_neutral_failures\":"
            << result.strengthening_failures
            << ",\"boundary_two_nonzero_failures\":"
            << result.boundary_two_nonzero_failures
            << ",\"minimum_boundary_at_most_two_failures\":"
            << result.minimum_boundary_failures;
        if (result.has_first_failure) {
            std::cout
                << ",\"first_failure\":{\"state_labels_hex\":\""
                << state_hex(result.failure_state) << "\""
                << ",\"vertex\":" << result.failure_vertex
                << ",\"edge_pair\":["
                << result.failure_first_edge << ","
                << result.failure_second_edge << "]}";
        } else {
            std::cout << ",\"first_failure\":null";
        }
        if (result.has_first_minimum_boundary_failure) {
            std::cout
                << ",\"first_minimum_boundary_failure\":{"
                << "\"state_labels_hex\":\""
                << state_hex(result.minimum_boundary_failure_state) << "\""
                << ",\"vertex\":" << result.minimum_boundary_failure_vertex
                << ",\"edge_pair\":["
                << result.minimum_boundary_failure_first_edge << ","
                << result.minimum_boundary_failure_second_edge << "]}";
        } else {
            std::cout
                << ",\"first_minimum_boundary_failure\":null";
        }
        std::cout << "}\n";
    }
    std::cout
        << "{\"status\":\"SUMMARY\",\"graphs\":" << graph_count
        << ",\"flows_mod_s5\":" << flow_count
        << ",\"local_edge_pair_triples\":" << triple_count
        << ",\"no_closed_candidate\":" << no_closed_count
        << ",\"no_closed_fewer_than_two_neutral_failures\":"
        << failure_count
        << ",\"boundary_two_nonzero_failures\":"
        << boundary_two_nonzero_count
        << ",\"minimum_boundary_at_most_two_failures\":"
        << minimum_boundary_failure_count
        << ",\"feature_histogram\":{";
    bool first_feature = true;
    for (const auto& [key, count] : feature_histogram) {
        if (!first_feature) std::cout << ",";
        first_feature = false;
        std::cout << "\"" << json_escape(key) << "\":" << count;
    }
    std::cout << "},\"switch_feature_histogram\":{";
    bool first_switch_feature = true;
    for (const auto& [key, count] : switch_feature_histogram) {
        if (!first_switch_feature) std::cout << ",";
        first_switch_feature = false;
        std::cout << "\"" << json_escape(key) << "\":" << count;
    }
    std::cout << "}}\n";
}
