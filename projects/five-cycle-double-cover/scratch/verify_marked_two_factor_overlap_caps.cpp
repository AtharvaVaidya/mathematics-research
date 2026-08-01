#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <set>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

// Exact finite checker for the local union of two marked bichromatic factor
// circuits.  It verifies the cap tables for excesses x,y in {0,...,4}.

struct Edge {
    int u;
    int v;
    int kind;   // 0 = common connection, 1 = A residual path, 2 = B path
    int index;  // index within its kind
};

static void require(bool condition, const std::string& message) {
    if (!condition) {
        std::cerr << "verification failure: " << message << "\n";
        std::exit(1);
    }
}

static void compositions_rec(
    int total, int parts, std::vector<int>& prefix,
    std::vector<std::vector<int>>& output
) {
    if (parts == 1) {
        prefix.push_back(total);
        output.push_back(prefix);
        prefix.pop_back();
        return;
    }
    for (int first = 1; first <= total - parts + 1; ++first) {
        prefix.push_back(first);
        compositions_rec(total - first, parts - 1, prefix, output);
        prefix.pop_back();
    }
}

static std::vector<std::vector<int>> residual_weights(
    int half_length, int overlap, bool diagonal
) {
    std::vector<std::vector<int>> compositions;
    std::vector<int> prefix;
    compositions_rec(half_length, overlap, prefix, compositions);

    std::set<std::vector<int>> unique;
    for (const auto& gaps : compositions) {
        if (diagonal) {
            std::vector<int> weights;
            for (int gap : gaps) weights.push_back(2 * gap - 1);
            unique.insert(weights);
        } else {
            // The private marked c-edge lies strictly inside one gap.  Its
            // subdivision adds one to that residual path.
            for (int marked_gap = 0; marked_gap < overlap; ++marked_gap) {
                if (gaps[marked_gap] < 2) continue;
                std::vector<int> weights;
                for (int index = 0; index < overlap; ++index) {
                    weights.push_back(
                        2 * gaps[index] - 1 + (index == marked_gap ? 1 : 0)
                    );
                }
                unique.insert(weights);
            }
        }
    }
    return {unique.begin(), unique.end()};
}

static std::vector<Edge> make_kernel(
    int overlap, bool diagonal, const std::vector<int>& permutation,
    int orientation_mask
) {
    std::vector<Edge> edges;
    for (int edge = 0; edge < overlap; ++edge) {
        edges.push_back({2 * edge, 2 * edge + 1, 0, edge});
    }
    for (int edge = 0; edge < overlap; ++edge) {
        edges.push_back(
            {2 * edge + 1, 2 * ((edge + 1) % overlap), 1, edge}
        );
    }
    for (int position = 0; position < overlap; ++position) {
        int current = permutation[position];
        int following = permutation[(position + 1) % overlap];
        bool current_reverse = (orientation_mask >> current) & 1;
        bool following_reverse = (orientation_mask >> following) & 1;
        int exit = 2 * current + (current_reverse ? 0 : 1);
        int entry = 2 * following + (following_reverse ? 1 : 0);
        edges.push_back({exit, entry, 2, position});
    }
    return edges;
}

static void cycles_dfs(
    int start, int current, const std::vector<Edge>& edges,
    const std::vector<std::vector<int>>& incidence,
    std::vector<bool>& used_vertices, std::uint64_t edge_mask,
    int edge_count, std::set<std::uint64_t>& cycles
) {
    for (int edge_id : incidence[current]) {
        if ((edge_mask >> edge_id) & 1ULL) continue;
        const Edge& edge = edges[edge_id];
        int following = edge.u == current ? edge.v : edge.u;
        if (following == start) {
            // Two distinct parallel kernel edges are a legitimate
            // topological cycle after their paths are expanded.
            if (edge_count >= 1) {
                cycles.insert(edge_mask | (1ULL << edge_id));
            }
            continue;
        }
        if (following < start || used_vertices[following]) continue;
        used_vertices[following] = true;
        cycles_dfs(
            start, following, edges, incidence, used_vertices,
            edge_mask | (1ULL << edge_id), edge_count + 1, cycles
        );
        used_vertices[following] = false;
    }
}

static std::vector<std::uint64_t> all_cycles(
    int vertex_count, const std::vector<Edge>& edges
) {
    std::vector<std::vector<int>> incidence(vertex_count);
    for (int edge_id = 0; edge_id < static_cast<int>(edges.size()); ++edge_id) {
        incidence[edges[edge_id].u].push_back(edge_id);
        incidence[edges[edge_id].v].push_back(edge_id);
    }
    std::set<std::uint64_t> unique;
    std::vector<bool> used(vertex_count, false);
    for (int start = 0; start < vertex_count; ++start) {
        used[start] = true;
        cycles_dfs(start, start, edges, incidence, used, 0, 0, unique);
        used[start] = false;
    }
    std::vector<std::uint64_t> result(unique.begin(), unique.end());
    std::sort(
        result.begin(), result.end(),
        [](std::uint64_t left, std::uint64_t right) {
            int left_size = __builtin_popcountll(left);
            int right_size = __builtin_popcountll(right);
            if (left_size != right_size) return left_size < right_size;
            return left < right;
        }
    );
    return result;
}

static bool weights_have_girth_ten(
    const std::vector<Edge>& edges,
    const std::vector<std::uint64_t>& cycles,
    bool diagonal,
    const std::vector<int>& a_weights,
    const std::vector<int>& b_weights
) {
    for (std::uint64_t cycle : cycles) {
        int length = 0;
        for (int edge_id = 0; edge_id < static_cast<int>(edges.size()); ++edge_id) {
            if (!((cycle >> edge_id) & 1ULL)) continue;
            const Edge& edge = edges[edge_id];
            if (edge.kind == 0) {
                length += diagonal && edge.index == 0 ? 2 : 1;
            } else if (edge.kind == 1) {
                length += a_weights[edge.index];
            } else {
                length += b_weights[edge.index];
            }
            if (length >= 10) break;
        }
        if (length < 10) return false;
    }
    return true;
}

struct Witness {
    bool found = false;
    std::vector<int> a_weights;
    std::vector<int> b_weights;
    std::vector<int> permutation;
    int orientation_mask = 0;
};

static Witness feasible(int x, int y, int overlap, bool diagonal) {
    int a = 5 + x;
    int b = 5 + y;
    if (overlap < 1 || overlap > std::min(a, b)) return {};
    if (!diagonal && overlap >= std::min(a, b)) return {};

    auto a_sequences = residual_weights(a, overlap, diagonal);
    auto b_sequences = residual_weights(b, overlap, diagonal);
    if (a_sequences.empty() || b_sequences.empty()) return {};

    std::vector<int> tail;
    for (int edge = 1; edge < overlap; ++edge) tail.push_back(edge);
    do {
        std::vector<int> permutation = {0};
        permutation.insert(permutation.end(), tail.begin(), tail.end());
        // Fix the orientation of common edge 0.  Reflection of the canonical
        // A cycle swaps it, and every reflected A weight sequence is present.
        for (int mask = 0; mask < (1 << overlap); mask += 2) {
            auto edges = make_kernel(overlap, diagonal, permutation, mask);
            auto cycles = all_cycles(2 * overlap, edges);
            for (const auto& a_weights : a_sequences) {
                for (const auto& b_weights : b_sequences) {
                    if (weights_have_girth_ten(
                            edges, cycles, diagonal, a_weights, b_weights
                        )) {
                        return {
                            true, a_weights, b_weights, permutation, mask
                        };
                    }
                }
            }
        }
    } while (std::next_permutation(tail.begin(), tail.end()));
    return {};
}

static int elementary_cap(int x, int y, bool diagonal) {
    int cap = x + y + 1;
    if (!diagonal && x + y >= 2) {
        // If equality held, the symmetric difference would have total
        // length 20 and any three common unit edges force a short circuit.
        cap = x + y;
    }
    cap = std::min(cap, 5 + std::min(x, y) - (diagonal ? 0 : 1));
    return cap;
}

static bool irregular_moore_excludes(
    int x, int y, int overlap, bool diagonal
) {
    // The expanded union has n vertices and n+overlap edges.  Its minimum
    // degree is two.  The even-girth-10 irregular Moore bound is
    //
    //   n >= 2 sum_{i=0}^4 (d-1)^i,
    //   d = 2(n+overlap)/n.
    //
    // Compare exactly after multiplying by n^4.
    std::int64_t n =
        (diagonal ? 21 : 22) + 2 * (x + y) - 2 * overlap;
    require(n > 0, "nonpositive expanded-union order");
    std::int64_t numerator = n + 2 * overlap;  // n(d-1)
    std::int64_t right = 0;
    for (int exponent = 0; exponent <= 4; ++exponent) {
        std::int64_t term = 1;
        for (int count = 0; count < exponent; ++count) {
            term *= numerator;
        }
        for (int count = exponent; count < 4; ++count) {
            term *= n;
        }
        right += 2 * term;
    }
    std::int64_t left = n * n * n * n * n;
    return left < right;
}

int main() {
    const std::array<std::array<int, 5>, 5> expected_offdiagonal = {{
        {{1, 2, 2, 2, 2}},
        {{2, 2, 2, 3, 3}},
        {{2, 2, 3, 3, 4}},
        {{2, 3, 3, 3, 4}},
        {{2, 3, 4, 4, 4}},
    }};
    const std::array<std::array<int, 5>, 5> expected_diagonal = {{
        {{1, 1, 2, 2, 2}},
        {{1, 2, 2, 2, 3}},
        {{2, 2, 2, 3, 3}},
        {{2, 2, 3, 3, 4}},
        {{2, 3, 3, 4, 4}},
    }};

    int exact_search_decisions = 0;
    int moore_exclusions = 0;
    for (bool diagonal : {false, true}) {
        std::cout << (diagonal ? "diagonal" : "offdiagonal") << "\n";
        for (int x = 0; x <= 4; ++x) {
            for (int y = 0; y <= 4; ++y) {
                int cap = elementary_cap(x, y, diagonal);
                int maximum = 0;
                Witness saved;
                for (int overlap = 1; overlap <= cap; ++overlap) {
                    if (overlap <= 6) {
                        Witness witness = feasible(x, y, overlap, diagonal);
                        ++exact_search_decisions;
                        if (witness.found) {
                            maximum = overlap;
                            saved = std::move(witness);
                        }
                    } else {
                        require(
                            irregular_moore_excludes(
                                x, y, overlap, diagonal
                            ),
                            "claimed high-multiplicity Moore exclusion failed"
                        );
                        ++moore_exclusions;
                    }
                }
                int expected = diagonal
                    ? expected_diagonal[x][y]
                    : expected_offdiagonal[x][y];
                require(
                    maximum == expected,
                    "computed cap differs from retained table"
                );
                std::cout << maximum << (y == 4 ? '\n' : ' ');
                if (saved.found) {
                    std::cerr
                        << (diagonal ? "D" : "O")
                        << " x=" << x << " y=" << y << " m=" << maximum
                        << " A=";
                    for (int value : saved.a_weights) std::cerr << value << ",";
                    std::cerr << " B=";
                    for (int value : saved.b_weights) std::cerr << value << ",";
                    std::cerr << " perm=";
                    for (int value : saved.permutation) std::cerr << value << ",";
                    std::cerr << " mask=" << saved.orientation_mask << "\n";
                }
            }
        }
    }
    std::cout << "marked two-factor overlap cap census: PASS\n";
    std::cout << "exact_search_decisions=" << exact_search_decisions << "\n";
    std::cout << "irregular_moore_exclusions=" << moore_exclusions << "\n";
}
