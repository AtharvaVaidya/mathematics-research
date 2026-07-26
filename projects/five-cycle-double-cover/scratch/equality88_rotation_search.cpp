// Heuristic search for an abstract equality-case rotation countermodel.
//
// The fixed incidence multigraph is the explicit 8-by-8 row/column-sum-five
// matrix below.  One diagonal edge in each row is marked.  Rotations and
// twist bits are mutated by deterministic simulated annealing.  A score is
// the number of the 256 all-mark selectors whose selected circuits all have
// even marked parity.

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <set>
#include <tuple>
#include <utility>
#include <vector>

using std::array;
using std::pair;
using std::vector;

namespace {

struct State {
    array<array<int, 5>, 8> rotation_a{};
    array<array<int, 5>, 8> rotation_b{};
    array<int, 40> twist{};
};

struct Evaluation {
    int good = 0;
    bool simple = false;
    array<int, 256> profile_code{};
};

const array<array<int, 8>, 8> INCIDENCE = {{
    {{2,0,1,2,0,0,0,0}},
    {{0,1,1,0,1,2,0,0}},
    {{0,2,1,0,0,0,2,0}},
    {{0,0,0,2,1,0,0,2}},
    {{1,0,1,0,1,0,1,1}},
    {{1,0,1,0,1,2,0,0}},
    {{0,2,0,0,0,0,2,1}},
    {{1,0,0,1,1,1,0,1}},
}};

vector<pair<int, int>> incidence_edges() {
    vector<pair<int, int>> result;
    array<array<int, 8>, 8> remaining = INCIDENCE;
    // The first eight edge objects are the distinguished marked matching.
    for (int index = 0; index < 8; ++index) {
        if (remaining[index][index] <= 0) {
            throw std::runtime_error("missing marked diagonal edge");
        }
        result.push_back({index, index});
        --remaining[index][index];
    }
    for (int a = 0; a < 8; ++a) {
        for (int b = 0; b < 8; ++b) {
            for (int copy = 0; copy < remaining[a][b]; ++copy) {
                result.push_back({a, b});
            }
        }
    }
    if (result.size() != 40) {
        throw std::runtime_error("bad incidence edge count");
    }
    return result;
}

pair<int, int> edge_ends(int edge) {
    static const vector<pair<int, int>> edges = incidence_edges();
    return edges.at(edge);
}

struct CubicEdge {
    int u;
    int v;
    int type;  // 0=c, 1=a, 2=b
    int owner;
};

vector<CubicEdge> build(const State& state) {
    vector<CubicEdge> edges;
    for (int edge = 0; edge < 40; ++edge) {
        edges.push_back({2 * edge, 2 * edge + 1, 0, edge});
    }
    for (int a = 0; a < 8; ++a) {
        for (int position = 0; position < 5; ++position) {
            int edge = state.rotation_a[a][position];
            int next = state.rotation_a[a][(position + 1) % 5];
            edges.push_back({2 * edge + 1, 2 * next, 1, a});
        }
    }
    for (int b = 0; b < 8; ++b) {
        for (int position = 0; position < 5; ++position) {
            int edge = state.rotation_b[b][position];
            int next = state.rotation_b[b][(position + 1) % 5];
            edges.push_back({
                2 * edge + (1 - state.twist[edge]),
                2 * next + state.twist[next],
                2,
                b,
            });
        }
    }
    return edges;
}

Evaluation evaluate(const State& state) {
    vector<CubicEdge> edges = build(state);
    std::set<pair<int, int>> unique;
    bool simple = true;
    for (const auto& edge : edges) {
        pair<int, int> ends = {std::min(edge.u, edge.v), std::max(edge.u, edge.v)};
        if (edge.u == edge.v || !unique.insert(ends).second) {
            simple = false;
        }
    }
    Evaluation result;
    result.simple = simple;
    for (int selector = 0; selector < 256; ++selector) {
        array<vector<pair<int, int>>, 80> adjacency;
        for (int index = 0; index < 120; ++index) {
            const auto& edge = edges[index];
            bool selected = false;
            if (edge.type == 1) {
                selected = (selector >> edge.owner) & 1;
            } else if (edge.type == 2) {
                selected = !((selector >> edge.owner) & 1);
            } else {
                auto [a, b] = edge_ends(edge.owner);
                int y = !((selector >> b) & 1);
                selected = ((selector >> a) & 1) ^ y;
            }
            if (selected) {
                adjacency[edge.u].push_back({edge.v, index});
                adjacency[edge.v].push_back({edge.u, index});
            }
        }
        array<int, 80> seen{};
        vector<int> mark_counts;
        bool good = true;
        for (int root = 0; root < 80; ++root) {
            if (seen[root] || adjacency[root].empty()) continue;
            vector<int> stack = {root};
            seen[root] = 1;
            int twice_marks = 0;
            while (!stack.empty()) {
                int vertex = stack.back();
                stack.pop_back();
                for (const auto& [other, edge_index] : adjacency[vertex]) {
                    if (edges[edge_index].type == 0 &&
                        edges[edge_index].owner < 8) {
                        ++twice_marks;
                    }
                    if (!seen[other]) {
                        seen[other] = 1;
                        stack.push_back(other);
                    }
                }
            }
            int marks = twice_marks / 2;
            if (marks) mark_counts.push_back(marks);
            if (marks & 1) good = false;
        }
        if (good) ++result.good;
        std::sort(mark_counts.begin(), mark_counts.end());
        int code = 0;
        for (int value : mark_counts) code = 9 * code + value;
        result.profile_code[selector] = code;
    }
    return result;
}

State random_state(std::mt19937_64& rng) {
    State state;
    vector<pair<int, int>> ends = incidence_edges();
    for (int a = 0; a < 8; ++a) {
        vector<int> incident;
        for (int edge = 0; edge < 40; ++edge) {
            if (ends[edge].first == a) incident.push_back(edge);
        }
        if (incident.size() != 5) throw std::runtime_error("bad A degree");
        std::shuffle(incident.begin(), incident.end(), rng);
        std::copy(incident.begin(), incident.end(), state.rotation_a[a].begin());
    }
    for (int b = 0; b < 8; ++b) {
        vector<int> incident;
        for (int edge = 0; edge < 40; ++edge) {
            if (ends[edge].second == b) incident.push_back(edge);
        }
        if (incident.size() != 5) throw std::runtime_error("bad B degree");
        std::shuffle(incident.begin(), incident.end(), rng);
        std::copy(incident.begin(), incident.end(), state.rotation_b[b].begin());
    }
    for (int edge = 0; edge < 40; ++edge) state.twist[edge] = rng() & 1;
    return state;
}

void mutate(State& state, std::mt19937_64& rng) {
    int kind = rng() % 3;
    if (kind == 0) {
        int a = rng() % 8;
        int first = rng() % 5;
        int second = rng() % 5;
        std::swap(state.rotation_a[a][first], state.rotation_a[a][second]);
    } else if (kind == 1) {
        int b = rng() % 8;
        int first = rng() % 5;
        int second = rng() % 5;
        std::swap(state.rotation_b[b][first], state.rotation_b[b][second]);
    } else {
        state.twist[rng() % 40] ^= 1;
    }
}

void print_state(const State& state, const Evaluation& evaluation, int iteration) {
    std::cout << "BEST iteration=" << iteration << " good=" << evaluation.good
              << " simple=" << evaluation.simple << "\n";
    std::cout << "A=";
    for (int a = 0; a < 8; ++a) {
        if (a) std::cout << ";";
        for (int value : state.rotation_a[a]) std::cout << value << ",";
    }
    std::cout << "\nB=";
    for (int b = 0; b < 8; ++b) {
        if (b) std::cout << ";";
        for (int value : state.rotation_b[b]) std::cout << value << ",";
    }
    std::cout << "\ntau=";
    for (int value : state.twist) std::cout << value;
    std::cout << "\n";
}

}  // namespace

int main(int argc, char** argv) {
    int iterations = argc > 1 ? std::stoi(argv[1]) : 200000;
    uint64_t seed = argc > 2 ? std::stoull(argv[2]) : 20260726;
    std::mt19937_64 rng(seed);
    State current = random_state(rng);
    Evaluation current_evaluation = evaluate(current);
    State best = current;
    Evaluation best_evaluation = current_evaluation;
    print_state(best, best_evaluation, 0);
    for (int iteration = 1; iteration <= iterations; ++iteration) {
        State candidate = current;
        mutate(candidate, rng);
        Evaluation candidate_evaluation = evaluate(candidate);
        int current_score = current_evaluation.good + (current_evaluation.simple ? 0 : 32);
        int candidate_score = candidate_evaluation.good + (candidate_evaluation.simple ? 0 : 32);
        double temperature = 8.0 * std::exp(-5.0 * iteration / iterations) + 0.05;
        bool accept = candidate_score <= current_score;
        if (!accept) {
            double probability =
                std::exp((current_score - candidate_score) / temperature);
            accept = std::generate_canonical<double, 53>(rng) < probability;
        }
        if (accept) {
            current = candidate;
            current_evaluation = candidate_evaluation;
        }
        if (candidate_evaluation.simple &&
            candidate_evaluation.good < best_evaluation.good) {
            best = candidate;
            best_evaluation = candidate_evaluation;
            print_state(best, best_evaluation, iteration);
            if (best_evaluation.good == 0) return 0;
        }
        if (iteration % 20000 == 0) {
            current = random_state(rng);
            current_evaluation = evaluate(current);
        }
    }
    print_state(best, best_evaluation, iterations);
    return best_evaluation.good == 0 ? 0 : 2;
}
