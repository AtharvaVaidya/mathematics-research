// Exact support-18 census for loopless two-occurrence interaction states.
//
// Compile:
//   c++ -std=c++17 -O3 verify_support18.cpp -o verify_support18
//
// This checker uses the alternating-form translation equations.  Every
// interaction edge is distinctly labelled.  Cyclic orders are quotiented
// only by rotation and reversal, so no unproved graph-isomorphism reduction
// enters the state count.

#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <numeric>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

struct Graph {
    std::string name;
    int n = 0;
    std::vector<std::pair<int, int>> edges;
    std::vector<std::vector<int>> star;
};

static int B(const int x, const int y) {
    return ((x & 1) & ((y >> 1) & 1)) ^
           (((x >> 1) & 1) & (y & 1));
}

static Graph triangle(const std::array<int, 3>& p) {
    Graph g;
    g.name = "T(" + std::to_string(p[0]) + "," +
             std::to_string(p[1]) + "," + std::to_string(p[2]) + ")";
    g.n = 3;
    const std::array<std::pair<int, int>, 3> pairs{
        std::pair<int, int>{0, 1}, {0, 2}, {1, 2}};
    for (int k = 0; k < 3; ++k) {
        for (int j = 0; j < p[k]; ++j) g.edges.push_back(pairs[k]);
    }
    g.star.resize(g.n);
    for (int e = 0; e < static_cast<int>(g.edges.size()); ++e) {
        const auto [u, v] = g.edges[e];
        g.star[u].push_back(e);
        g.star[v].push_back(e);
    }
    return g;
}

static Graph four_vertex(const std::array<int, 6>& p) {
    Graph g;
    g.name = "Q(";
    for (int k = 0; k < 6; ++k) {
        if (k) g.name += ",";
        g.name += std::to_string(p[k]);
    }
    g.name += ")";
    g.n = 4;
    const std::array<std::pair<int, int>, 6> pairs{
        std::pair<int, int>{0, 1}, {0, 2}, {0, 3},
        {1, 2}, {1, 3}, {2, 3}};
    for (int k = 0; k < 6; ++k) {
        for (int j = 0; j < p[k]; ++j) g.edges.push_back(pairs[k]);
    }
    g.star.resize(g.n);
    for (int e = 0; e < static_cast<int>(g.edges.size()); ++e) {
        const auto [u, v] = g.edges[e];
        g.star[u].push_back(e);
        g.star[v].push_back(e);
    }
    return g;
}

static std::vector<std::vector<int>> cyclic_orders(
    const std::vector<int>& star) {
    assert(star.size() >= 2);
    const int anchor = *std::min_element(star.begin(), star.end());
    std::vector<int> tail;
    for (const int e : star) {
        if (e != anchor) tail.push_back(e);
    }
    std::sort(tail.begin(), tail.end());
    std::vector<std::vector<int>> result;
    do {
        std::vector<int> reversed(tail.rbegin(), tail.rend());
        if (tail <= reversed) {
            std::vector<int> order{anchor};
            order.insert(order.end(), tail.begin(), tail.end());
            result.push_back(std::move(order));
        }
    } while (std::next_permutation(tail.begin(), tail.end()));
    return result;
}

struct Flow {
    std::vector<unsigned char> value;
    std::vector<std::array<std::uint64_t, 2>> clean_mask;
};

static std::vector<Flow> normalized_flows(const Graph& g) {
    const int m = static_cast<int>(g.edges.size());
    assert(1 <= m && m <= 9);
    std::uint64_t codes = 1;
    for (int e = 1; e < m; ++e) codes *= 3;
    const int translations = 1 << (2 * (g.n - 1));
    assert(translations <= 64);
    std::vector<Flow> flows;
    for (std::uint64_t code = 0; code < codes; ++code) {
        auto row = code;
        std::vector<unsigned char> value(m);
        value[0] = 1;  // global GL(2,2) normalization
        for (int e = 1; e < m; ++e) {
            value[e] = static_cast<unsigned char>(1 + row % 3);
            row /= 3;
        }
        bool closes = true;
        for (int v = 0; v < g.n; ++v) {
            int sum = 0;
            for (const int e : g.star[v]) sum ^= value[e];
            if (sum) {
                closes = false;
                break;
            }
        }
        if (!closes) continue;

        Flow f;
        f.value = std::move(value);
        f.clean_mask.resize(m);
        for (int e = 0; e < m; ++e) {
            f.clean_mask[e] = {0, 0};
            const auto [u, v] = g.edges[e];
            for (int assignment = 0; assignment < translations;
                 ++assignment) {
                const int xu = u == 0 ? 0 :
                    ((assignment >> (2 * (u - 1))) & 3);
                const int xv = v == 0 ? 0 :
                    ((assignment >> (2 * (v - 1))) & 3);
                const int lhs = B(xu ^ xv, f.value[e]);
                f.clean_mask[e][lhs] |= (std::uint64_t{1} << assignment);
            }
        }
        flows.push_back(std::move(f));
    }
    return flows;
}

struct Totals {
    std::uint64_t states = 0;
    std::uint64_t clean_states = 0;
    std::uint64_t delete_only_states = 0;
    std::uint64_t no_goal_states = 0;
    std::uint64_t state_hash = 1469598103934665603ULL;
    std::uint64_t min_goal_flows = UINT64_MAX;
    std::uint64_t max_goal_flows = 0;
};

struct Expected {
    std::uint64_t states;
    std::uint64_t clean_states;
    std::uint64_t delete_only_states;
    std::uint64_t min_goal_flows;
    std::uint64_t max_goal_flows;
    std::uint64_t state_hash;
};

static void assert_expected(const Totals& actual, const Expected& expected) {
    assert(actual.states == expected.states);
    assert(actual.clean_states == expected.clean_states);
    assert(actual.delete_only_states == expected.delete_only_states);
    assert(actual.no_goal_states == 0);
    assert(actual.min_goal_flows == expected.min_goal_flows);
    assert(actual.max_goal_flows == expected.max_goal_flows);
    assert(actual.state_hash == expected.state_hash);
}

static void hash_word(std::uint64_t& hash, std::uint64_t word) {
    for (int k = 0; k < 8; ++k) {
        hash ^= (word >> (8 * k)) & 255;
        hash *= 1099511628211ULL;
    }
}

static Totals census(const Graph& g) {
    const int m = static_cast<int>(g.edges.size());
    assert(1 <= m && m <= 9);
    std::vector<std::vector<std::vector<int>>> choices(g.n);
    std::uint64_t expected_states = 1;
    for (int v = 0; v < g.n; ++v) {
        choices[v] = cyclic_orders(g.star[v]);
        expected_states *= choices[v].size();
    }
    const auto flows = normalized_flows(g);
    Totals totals;
    std::vector<const std::vector<int>*> order(g.n);

    std::function<void(int)> visit = [&](const int vertex) {
        if (vertex != g.n) {
            for (const auto& candidate : choices[vertex]) {
                order[vertex] = &candidate;
                visit(vertex + 1);
            }
            return;
        }

        ++totals.states;
        std::uint64_t clean_flow_count = 0;
        std::uint64_t delete_flow_count = 0;
        std::uint64_t goal_flow_count = 0;
        for (const Flow& f : flows) {
            std::vector<std::vector<unsigned char>> prefix(
                g.n, std::vector<unsigned char>(m, 0));
            bool deletes = false;
            for (int v = 0; v < g.n; ++v) {
                int point = 0;
                int used = 0;
                for (const int e : *order[v]) {
                    prefix[v][e] = static_cast<unsigned char>(point);
                    used |= 1 << point;
                    point ^= f.value[e];
                }
                assert(point == 0);
                deletes = deletes || used != 15;
            }

            const int translations = 1 << (2 * (g.n - 1));
            std::uint64_t possible = translations == 64
                ? ~std::uint64_t{0}
                : ((std::uint64_t{1} << translations) - 1);
            for (int e = 0; e < m && possible; ++e) {
                const auto [u, v] = g.edges[e];
                const int rhs = B(prefix[u][e] ^ prefix[v][e],
                                  f.value[e]);
                possible &= f.clean_mask[e][rhs];
            }
            const bool clean = possible != 0;
            clean_flow_count += clean;
            delete_flow_count += deletes;
            goal_flow_count += clean || deletes;
        }
        totals.min_goal_flows =
            std::min(totals.min_goal_flows, goal_flow_count);
        totals.max_goal_flows =
            std::max(totals.max_goal_flows, goal_flow_count);
        if (clean_flow_count) {
            ++totals.clean_states;
        } else if (delete_flow_count) {
            ++totals.delete_only_states;
        } else {
            ++totals.no_goal_states;
        }
        hash_word(totals.state_hash, clean_flow_count);
        hash_word(totals.state_hash, delete_flow_count);
        hash_word(totals.state_hash, goal_flow_count);
    };
    visit(0);
    assert(totals.states == expected_states);
    std::cout << "PROFILE " << g.name << " degrees=";
    for (int v = 0; v < g.n; ++v) {
        if (v) std::cout << ",";
        std::cout << g.star[v].size();
    }
    std::cout << " normalized_flows=" << flows.size()
              << " states=" << totals.states
              << " clean_states=" << totals.clean_states
              << " delete_only_states=" << totals.delete_only_states
              << " no_goal_states=" << totals.no_goal_states
              << " min_goal_flows=" << totals.min_goal_flows
              << " max_goal_flows=" << totals.max_goal_flows
              << " state_hash=" << totals.state_hash << "\n";
    return totals;
}

int main() {
    const std::array<std::array<int, 3>, 6> triangles{{
        {3, 2, 2}, {3, 3, 2}, {4, 3, 1},
        {5, 2, 2}, {4, 4, 1}, {4, 3, 2}}};
    const std::array<std::array<int, 6>, 7> four_profiles{{
        {0, 1, 3, 3, 1, 1},
        {0, 1, 3, 3, 2, 0},
        {0, 1, 3, 4, 1, 0},
        {0, 2, 2, 2, 2, 1},
        {0, 2, 2, 2, 3, 0},
        {1, 1, 2, 2, 1, 2},
        {1, 1, 2, 3, 1, 1},
    }};
    const std::array<Expected, 6> triangle_expected{{
        {432, 432, 0, 38, 46, 7734768525698043395ULL},
        {8640, 8640, 0, 102, 134, 16669557602520969091ULL},
        {12960, 12744, 216, 120, 140, 4450252855536875651ULL},
        {388800, 388800, 0, 324, 424, 8632190210730346291ULL},
        {362880, 356256, 6624, 300, 400, 18043442683196809347ULL},
        {259200, 259200, 0, 276, 406, 10787898853228982803ULL},
    }};
    const std::array<Expected, 7> four_expected{{
        {1296, 1296, 0, 94, 98, 2096642095894169731ULL},
        {1296, 1296, 0, 94, 98, 11920414838350612611ULL},
        {1296, 1188, 108, 132, 140, 1351608326859010691ULL},
        {1296, 1296, 0, 98, 104, 4373726890615436675ULL},
        {1296, 1296, 0, 104, 110, 3542109076517088387ULL},
        {1296, 1296, 0, 100, 106, 12882566383929938947ULL},
        {1296, 1296, 0, 100, 112, 3256834280484815107ULL},
    }};

    std::uint64_t total_states = 0;
    std::uint64_t new_layer_states = 0;
    std::uint64_t total_no_goal = 0;
    for (int k = 0; k < static_cast<int>(triangles.size()); ++k) {
        const auto& p = triangles[k];
        const auto answer = census(triangle(p));
        assert_expected(answer, triangle_expected[k]);
        total_states += answer.states;
        if (k >= 3) new_layer_states += answer.states;
        total_no_goal += answer.no_goal_states;
    }
    for (int k = 0; k < static_cast<int>(four_profiles.size()); ++k) {
        const auto answer = census(four_vertex(four_profiles[k]));
        assert_expected(answer, four_expected[k]);
        total_states += answer.states;
        new_layer_states += answer.states;
        total_no_goal += answer.no_goal_states;
    }
    std::cout << "TOTAL new_layer_states=" << new_layer_states
              << " through18_states=" << total_states
              << " no_goal_states=" << total_no_goal << "\n";
    assert(total_no_goal == 0);
    std::cout << "PASS exact support-18 census\n";
}
