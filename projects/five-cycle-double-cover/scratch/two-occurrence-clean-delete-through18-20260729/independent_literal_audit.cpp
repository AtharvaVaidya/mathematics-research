// Independent literal endpoint-set audit of the support-18 census.
//
// This implementation does not use the alternating bilinear form.  It
// constructs the two translated K4 edges at the ends of every interaction
// edge and compares their two-point masks literally.

#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

struct Instance {
    std::string label;
    int vertices;
    std::vector<std::pair<int, int>> ends;
    std::vector<std::vector<int>> incidence;
};

static Instance build(const std::string& label, const int vertices,
                      const std::vector<std::pair<int, int>>& pair_types,
                      const std::vector<int>& multiplicities) {
    Instance answer{label, vertices, {}, std::vector<std::vector<int>>(vertices)};
    for (std::size_t type = 0; type < pair_types.size(); ++type) {
        for (int copy = 0; copy < multiplicities[type]; ++copy) {
            answer.ends.push_back(pair_types[type]);
        }
    }
    for (int edge = 0; edge < static_cast<int>(answer.ends.size()); ++edge) {
        const auto [u, v] = answer.ends[edge];
        answer.incidence[u].push_back(edge);
        answer.incidence[v].push_back(edge);
    }
    return answer;
}

static std::vector<std::vector<int>> unoriented_rotations(
    const std::vector<int>& incidence) {
    std::vector<std::vector<int>> answer;
    const int anchor = *std::min_element(incidence.begin(), incidence.end());
    std::vector<int> tail;
    for (const int edge : incidence) {
        if (edge != anchor) tail.push_back(edge);
    }
    std::sort(tail.begin(), tail.end());
    do {
        std::vector<int> candidate{anchor};
        candidate.insert(candidate.end(), tail.begin(), tail.end());
        std::vector<int> reverse{anchor};
        reverse.insert(reverse.end(), tail.rbegin(), tail.rend());
        if (candidate <= reverse) answer.push_back(std::move(candidate));
    } while (std::next_permutation(tail.begin(), tail.end()));
    return answer;
}

struct Labeling {
    std::array<unsigned char, 9> value{};
    std::array<std::array<std::uint64_t, 2>, 9> literal_masks{};
};

static std::vector<Labeling> labelings(const Instance& instance) {
    const int edge_count = static_cast<int>(instance.ends.size());
    assert(1 <= edge_count && edge_count <= 9);
    const int assignments = 1 << (2 * (instance.vertices - 1));
    std::vector<Labeling> answer;
    int tail_codes = 1;
    for (int edge = 1; edge < edge_count; ++edge) tail_codes *= 3;
    for (int code = 0; code < tail_codes; ++code) {
        int rest = code;
        Labeling labeling;
        labeling.value[0] = 1;
        for (int edge = 1; edge < edge_count; ++edge) {
            labeling.value[edge] = 1 + rest % 3;
            rest /= 3;
        }
        bool balanced = true;
        for (int vertex = 0; vertex < instance.vertices; ++vertex) {
            int sum = 0;
            for (const int edge : instance.incidence[vertex]) {
                sum ^= labeling.value[edge];
            }
            balanced = balanced && sum == 0;
        }
        if (!balanced) continue;

        for (int edge = 0; edge < edge_count; ++edge) {
            labeling.literal_masks[edge] = {0, 0};
            const auto [u, v] = instance.ends[edge];
            const int step = labeling.value[edge];
            for (int assignment = 0; assignment < assignments; ++assignment) {
                const int shift_u = u == 0 ? 0 :
                    ((assignment >> (2 * (u - 1))) & 3);
                const int shift_v = v == 0 ? 0 :
                    ((assignment >> (2 * (v - 1))) & 3);
                // The prefix-dependent endpoints are inserted during the
                // state census.  Here 0 means equal origins and 1 means the
                // other coset of span(step); use representatives 0 and the
                // least point outside {0,step}.
                const int pair_u = (1 << shift_u) |
                                   (1 << (shift_u ^ step));
                const int pair_v = (1 << shift_v) |
                                   (1 << (shift_v ^ step));
                const int coset = pair_u == pair_v ? 0 : 1;
                labeling.literal_masks[edge][coset] |=
                    std::uint64_t{1} << assignment;
            }
        }
        answer.push_back(labeling);
    }
    return answer;
}

struct Expected {
    std::uint64_t states;
    std::uint64_t clean;
    std::uint64_t delete_only;
    std::uint64_t minimum_goal;
    std::uint64_t maximum_goal;
};

static void audit(const Instance& instance, const Expected expected) {
    const int edge_count = static_cast<int>(instance.ends.size());
    const auto flows = labelings(instance);
    std::vector<std::vector<std::vector<int>>> rotations(instance.vertices);
    for (int vertex = 0; vertex < instance.vertices; ++vertex) {
        rotations[vertex] = unoriented_rotations(instance.incidence[vertex]);
    }
    std::array<const std::vector<int>*, 4> orders{};
    std::uint64_t states = 0;
    std::uint64_t clean_states = 0;
    std::uint64_t delete_only_states = 0;
    std::uint64_t no_goal_states = 0;
    std::uint64_t minimum_goal = UINT64_MAX;
    std::uint64_t maximum_goal = 0;

    std::function<void(int)> recurse = [&](const int vertex) {
        if (vertex < instance.vertices) {
            for (const auto& order : rotations[vertex]) {
                orders[vertex] = &order;
                recurse(vertex + 1);
            }
            return;
        }
        ++states;
        std::uint64_t clean_flows = 0;
        std::uint64_t deleting_flows = 0;
        std::uint64_t goal_flows = 0;
        for (const auto& flow : flows) {
            std::array<std::array<unsigned char, 9>, 4> prefix{};
            bool deletes = false;
            for (int v = 0; v < instance.vertices; ++v) {
                int point = 0;
                int visited = 0;
                for (const int edge : *orders[v]) {
                    prefix[v][edge] = point;
                    visited |= 1 << point;
                    point ^= flow.value[edge];
                }
                assert(point == 0);
                deletes = deletes || visited != 15;
            }

            const int assignment_count =
                1 << (2 * (instance.vertices - 1));
            std::uint64_t possible = assignment_count == 64
                ? ~std::uint64_t{0}
                : (std::uint64_t{1} << assignment_count) - 1;
            for (int edge = 0; edge < edge_count && possible; ++edge) {
                const auto [u, v] = instance.ends[edge];
                const int step = flow.value[edge];
                const int pair_u = (1 << prefix[u][edge]) |
                    (1 << (prefix[u][edge] ^ step));
                const int pair_v = (1 << prefix[v][edge]) |
                    (1 << (prefix[v][edge] ^ step));
                // There are exactly two parallel K4 edges for a fixed step.
                const int required_coset = pair_u == pair_v ? 0 : 1;
                possible &= flow.literal_masks[edge][required_coset];
            }
            const bool clean = possible != 0;
            clean_flows += clean;
            deleting_flows += deletes;
            goal_flows += clean || deletes;
        }
        minimum_goal = std::min(minimum_goal, goal_flows);
        maximum_goal = std::max(maximum_goal, goal_flows);
        if (clean_flows) {
            ++clean_states;
        } else if (deleting_flows) {
            ++delete_only_states;
        } else {
            ++no_goal_states;
        }
    };
    recurse(0);

    assert(states == expected.states);
    assert(clean_states == expected.clean);
    assert(delete_only_states == expected.delete_only);
    assert(no_goal_states == 0);
    assert(minimum_goal == expected.minimum_goal);
    assert(maximum_goal == expected.maximum_goal);
    std::cout << "AUDIT " << instance.label
              << " normalized_flows=" << flows.size()
              << " states=" << states
              << " clean_states=" << clean_states
              << " delete_only_states=" << delete_only_states
              << " no_goal_states=" << no_goal_states
              << " min_goal_flows=" << minimum_goal
              << " max_goal_flows=" << maximum_goal << "\n";
}

int main() {
    const std::vector<std::pair<int, int>> tri_pairs{
        {0, 1}, {0, 2}, {1, 2}};
    audit(build("T(3,2,2)", 3, tri_pairs, {3, 2, 2}),
          {432, 432, 0, 38, 46});
    audit(build("T(3,3,2)", 3, tri_pairs, {3, 3, 2}),
          {8640, 8640, 0, 102, 134});
    audit(build("T(4,3,1)", 3, tri_pairs, {4, 3, 1}),
          {12960, 12744, 216, 120, 140});
    audit(build("T(5,2,2)", 3, tri_pairs, {5, 2, 2}),
          {388800, 388800, 0, 324, 424});
    audit(build("T(4,4,1)", 3, tri_pairs, {4, 4, 1}),
          {362880, 356256, 6624, 300, 400});
    audit(build("T(4,3,2)", 3, tri_pairs, {4, 3, 2}),
          {259200, 259200, 0, 276, 406});

    const std::vector<std::pair<int, int>> quad_pairs{
        {0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}};
    const std::array<std::vector<int>, 7> profiles{{
        {0, 1, 3, 3, 1, 1}, {0, 1, 3, 3, 2, 0},
        {0, 1, 3, 4, 1, 0}, {0, 2, 2, 2, 2, 1},
        {0, 2, 2, 2, 3, 0}, {1, 1, 2, 2, 1, 2},
        {1, 1, 2, 3, 1, 1}}};
    const std::array<Expected, 7> expected{{
        {1296, 1296, 0, 94, 98}, {1296, 1296, 0, 94, 98},
        {1296, 1188, 108, 132, 140}, {1296, 1296, 0, 98, 104},
        {1296, 1296, 0, 104, 110}, {1296, 1296, 0, 100, 106},
        {1296, 1296, 0, 100, 112}}};
    for (int k = 0; k < 7; ++k) {
        std::string label = "Q(";
        for (int j = 0; j < 6; ++j) {
            if (j) label += ",";
            label += std::to_string(profiles[k][j]);
        }
        label += ")";
        audit(build(label, 4, quad_pairs, profiles[k]), expected[k]);
    }
    std::cout << "PASS independent literal endpoint-set audit\n";
}
