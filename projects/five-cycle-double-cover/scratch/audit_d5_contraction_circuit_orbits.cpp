// Exhaustive generalized factor-circuit orbit audit for edge contractions.
//
// Input: graph6 rows of simple biconnected cubic graphs.
// For every edge uv, contract uv to a degree-four vertex with the inherited
// u-side/v-side 2+2 split.  Enumerate D5 flows modulo global S5, generate
// switches on every nonempty Eulerian subgraph of every factor Y_ij, and
// check that each orbit contains a state whose side xor has weight two.
//
// This is a finite audit, not a proof of the universal statement.

#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

using State = std::string;

static const std::array<unsigned char, 10> LABELS = {
    3, 5, 9, 17, 6, 10, 18, 12, 20, 24
};

struct CubicGraph {
    int n = 0;
    std::vector<std::pair<int, int>> edges;
    std::vector<std::array<int, 3>> incidence;
};

struct ContractedGraph {
    int n = 0;
    std::vector<std::pair<int, int>> edges;
    std::vector<std::vector<int>> incidence;
    std::array<int, 2> u_side = {-1, -1};
    std::array<int, 2> v_side = {-1, -1};
    int w = -1;
};

static bool is_label(unsigned char value) {
    return std::find(LABELS.begin(), LABELS.end(), value) != LABELS.end();
}

static CubicGraph decode_graph6(const std::string& row) {
    if (row.empty() || row[0] == '~') {
        throw std::runtime_error("only short graph6 rows are supported");
    }
    CubicGraph graph;
    graph.n = static_cast<unsigned char>(row[0]) - 63;
    std::vector<int> bits;
    for (std::size_t i = 1; i < row.size(); ++i) {
        const int value = static_cast<unsigned char>(row[i]) - 63;
        if (value < 0 || value >= 64) throw std::runtime_error("bad graph6 byte");
        for (int shift = 5; shift >= 0; --shift) {
            bits.push_back((value >> shift) & 1);
        }
    }
    int cursor = 0;
    for (int right = 1; right < graph.n; ++right) {
        for (int left = 0; left < right; ++left) {
            if (bits.at(cursor)) graph.edges.emplace_back(left, right);
            ++cursor;
        }
    }
    std::vector<std::vector<int>> rows(graph.n);
    for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
        const auto [left, right] = graph.edges[edge];
        rows[left].push_back(edge);
        rows[right].push_back(edge);
    }
    graph.incidence.resize(graph.n);
    for (int vertex = 0; vertex < graph.n; ++vertex) {
        if (rows[vertex].size() != 3) throw std::runtime_error("input is not cubic");
        graph.incidence[vertex] = {rows[vertex][0], rows[vertex][1], rows[vertex][2]};
    }
    return graph;
}

static ContractedGraph contract_edge(const CubicGraph& graph, int root) {
    const auto [u, v] = graph.edges.at(root);
    std::vector<int> vertex_map(graph.n, -1);
    vertex_map[u] = 0;
    vertex_map[v] = 0;
    int next = 1;
    for (int vertex = 0; vertex < graph.n; ++vertex) {
        if (vertex != u && vertex != v) vertex_map[vertex] = next++;
    }

    ContractedGraph answer;
    answer.n = graph.n - 1;
    answer.w = 0;
    int u_count = 0;
    int v_count = 0;
    for (int old_edge = 0;
         old_edge < static_cast<int>(graph.edges.size());
         ++old_edge) {
        if (old_edge == root) continue;
        const auto [old_left, old_right] = graph.edges[old_edge];
        const int edge = static_cast<int>(answer.edges.size());
        answer.edges.emplace_back(vertex_map[old_left], vertex_map[old_right]);
        if (old_left == u || old_right == u) {
            if (u_count >= 2) throw std::runtime_error("too many u-side edges");
            answer.u_side[u_count++] = edge;
        }
        if (old_left == v || old_right == v) {
            if (v_count >= 2) throw std::runtime_error("too many v-side edges");
            answer.v_side[v_count++] = edge;
        }
    }
    if (u_count != 2 || v_count != 2) throw std::runtime_error("bad 2+2 split");
    answer.incidence.assign(answer.n, {});
    for (int edge = 0; edge < static_cast<int>(answer.edges.size()); ++edge) {
        const auto [left, right] = answer.edges[edge];
        if (left == right) throw std::runtime_error("unexpected contraction loop");
        answer.incidence[left].push_back(edge);
        answer.incidence[right].push_back(edge);
    }
    for (int vertex = 0; vertex < answer.n; ++vertex) {
        const int expected = vertex == answer.w ? 4 : 3;
        if (static_cast<int>(answer.incidence[vertex].size()) != expected) {
            throw std::runtime_error("wrong contracted degree");
        }
    }
    return answer;
}

static std::vector<std::array<int, 5>> all_permutations() {
    std::array<int, 5> current = {0, 1, 2, 3, 4};
    std::vector<std::array<int, 5>> answer;
    do {
        answer.push_back(current);
    } while (std::next_permutation(current.begin(), current.end()));
    return answer;
}

static unsigned char permute_label(
    unsigned char label,
    const std::array<int, 5>& permutation
) {
    unsigned char answer = 0;
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
        if ((label >> coordinate) & 1) {
            answer |= static_cast<unsigned char>(1 << permutation[coordinate]);
        }
    }
    return answer;
}

struct DSU {
    std::vector<int> parent;
    explicit DSU(int n) : parent(n) {
        std::iota(parent.begin(), parent.end(), 0);
    }
    int find(int value) {
        if (parent[value] != value) parent[value] = find(parent[value]);
        return parent[value];
    }
    bool join(int left, int right) {
        left = find(left);
        right = find(right);
        if (left == right) return false;
        parent[right] = left;
        return true;
    }
};

struct Auditor {
    ContractedGraph graph;
    std::vector<std::array<int, 5>> permutations;
    std::array<std::array<unsigned char, 32>, 120> permuted{};

    explicit Auditor(ContractedGraph input)
        : graph(std::move(input)), permutations(all_permutations()) {
        for (int p = 0; p < 120; ++p) {
            for (unsigned char label : LABELS) {
                permuted[p][label] = permute_label(label, permutations[p]);
            }
        }
    }

    State canonical(const State& state) const {
        State best;
        bool initial = true;
        for (int p = 0; p < 120; ++p) {
            State candidate(state.size(), '\0');
            for (int edge = 0; edge < static_cast<int>(state.size()); ++edge) {
                candidate[edge] = static_cast<char>(
                    permuted[p][static_cast<unsigned char>(state[edge])]
                );
            }
            if (initial || candidate < best) {
                initial = false;
                best = std::move(candidate);
            }
        }
        return best;
    }

    bool assign(
        State& state,
        int edge,
        unsigned char label,
        std::vector<int>& changed
    ) const {
        if (state[edge]) return static_cast<unsigned char>(state[edge]) == label;
        if (!is_label(label)) return false;
        state[edge] = static_cast<char>(label);
        changed.push_back(edge);
        std::vector<int> pending = {
            graph.edges[edge].first,
            graph.edges[edge].second
        };
        while (!pending.empty()) {
            const int vertex = pending.back();
            pending.pop_back();
            int unassigned = 0;
            int missing = -1;
            unsigned char total = 0;
            for (int item : graph.incidence[vertex]) {
                if (state[item]) {
                    total ^= static_cast<unsigned char>(state[item]);
                } else {
                    ++unassigned;
                    missing = item;
                }
            }
            if (unassigned > 1) continue;
            if (unassigned == 0) {
                if (total) return false;
                continue;
            }
            if (!is_label(total)) return false;
            state[missing] = static_cast<char>(total);
            changed.push_back(missing);
            pending.push_back(graph.edges[missing].first);
            pending.push_back(graph.edges[missing].second);
        }
        return true;
    }

    void enumerate_visit(
        State& state,
        std::unordered_set<State>& answers
    ) const {
        int edge = -1;
        for (int index = 0; index < static_cast<int>(state.size()); ++index) {
            if (!state[index]) {
                edge = index;
                break;
            }
        }
        if (edge < 0) {
            answers.insert(canonical(state));
            return;
        }
        const bool empty = std::all_of(
            state.begin(),
            state.end(),
            [](char value) { return value == 0; }
        );
        const int choices = empty ? 1 : 10;
        for (int index = 0; index < choices; ++index) {
            std::vector<int> changed;
            if (assign(state, edge, LABELS[index], changed)) {
                enumerate_visit(state, answers);
            }
            for (auto iterator = changed.rbegin(); iterator != changed.rend(); ++iterator) {
                state[*iterator] = 0;
            }
        }
    }

    std::unordered_set<State> enumerate_flows() const {
        State state(graph.edges.size(), '\0');
        std::unordered_set<State> answer;
        enumerate_visit(state, answer);
        return answer;
    }

    uint32_t active_mask(const State& state, unsigned char pair) const {
        uint32_t mask = 0;
        for (int edge = 0; edge < static_cast<int>(state.size()); ++edge) {
            if ((__builtin_popcount(
                    static_cast<unsigned char>(state[edge]) & pair
                ) & 1) != 0) {
                mask |= uint32_t(1) << edge;
            }
        }
        return mask;
    }

    std::vector<uint32_t> cycle_basis(uint32_t active) const {
        DSU dsu(graph.n);
        std::vector<std::vector<std::pair<int, int>>> tree(graph.n);
        std::vector<int> chords;
        uint32_t copy = active;
        while (copy) {
            const int edge = __builtin_ctz(copy);
            copy &= copy - 1;
            const auto [left, right] = graph.edges[edge];
            if (dsu.join(left, right)) {
                tree[left].emplace_back(right, edge);
                tree[right].emplace_back(left, edge);
            } else {
                chords.push_back(edge);
            }
        }

        std::vector<uint32_t> basis;
        for (int chord : chords) {
            const auto [source, target] = graph.edges[chord];
            std::vector<int> parent_vertex(graph.n, -1);
            std::vector<int> parent_edge(graph.n, -1);
            std::queue<int> queue;
            parent_vertex[source] = source;
            queue.push(source);
            while (!queue.empty() && parent_vertex[target] < 0) {
                const int vertex = queue.front();
                queue.pop();
                for (const auto [other, edge] : tree[vertex]) {
                    if (parent_vertex[other] < 0) {
                        parent_vertex[other] = vertex;
                        parent_edge[other] = edge;
                        queue.push(other);
                    }
                }
            }
            if (parent_vertex[target] < 0) {
                throw std::runtime_error("chord endpoints disconnected in forest");
            }
            uint32_t cycle = uint32_t(1) << chord;
            int vertex = target;
            while (vertex != source) {
                cycle |= uint32_t(1) << parent_edge[vertex];
                vertex = parent_vertex[vertex];
            }
            basis.push_back(cycle);
        }
        return basis;
    }

    std::vector<uint32_t> even_masks(uint32_t active) const {
        const auto basis = cycle_basis(active);
        if (basis.size() >= 20) throw std::runtime_error("unexpected cycle rank");
        std::vector<uint32_t> answer;
        answer.reserve((std::size_t(1) << basis.size()) - 1);
        for (std::size_t selection = 1;
             selection < (std::size_t(1) << basis.size());
             ++selection) {
            uint32_t mask = 0;
            for (int index = 0; index < static_cast<int>(basis.size()); ++index) {
                if ((selection >> index) & 1) mask ^= basis[index];
            }
            answer.push_back(mask);
        }
        return answer;
    }

    State switched(
        const State& state,
        unsigned char pair,
        uint32_t mask
    ) const {
        State answer = state;
        uint32_t copy = mask;
        while (copy) {
            const int edge = __builtin_ctz(copy);
            copy &= copy - 1;
            answer[edge] = static_cast<char>(
                static_cast<unsigned char>(answer[edge]) ^ pair
            );
            if (!is_label(static_cast<unsigned char>(answer[edge]))) {
                throw std::runtime_error("switch left D5");
            }
        }
        return canonical(answer);
    }

    bool good(const State& state) const {
        const unsigned char value =
            static_cast<unsigned char>(state[graph.u_side[0]]) ^
            static_cast<unsigned char>(state[graph.u_side[1]]);
        return __builtin_popcount(value) == 2;
    }

    struct Result {
        int flows = 0;
        int orbits = 0;
        int bad_starting_flows = 0;
        int bad_only_orbits = 0;
        int maximum_orbit = 0;
        int maximum_distance_to_good = 0;
        State failure;
    };

    Result run() const {
        const auto all_flows = enumerate_flows();
        std::vector<State> states(all_flows.begin(), all_flows.end());
        std::sort(states.begin(), states.end());
        std::unordered_map<State, int> index;
        index.reserve(states.size() * 2);
        for (int i = 0; i < static_cast<int>(states.size()); ++i) {
            index.emplace(states[i], i);
        }
        Result result;
        result.flows = static_cast<int>(all_flows.size());
        std::vector<std::vector<int>> adjacency(states.size());
        for (int i = 0; i < static_cast<int>(states.size()); ++i) {
            const State& state = states[i];
            if (!good(state)) ++result.bad_starting_flows;
            for (unsigned char pair : LABELS) {
                const uint32_t active = active_mask(state, pair);
                for (uint32_t mask : even_masks(active)) {
                    const State other = switched(state, pair, mask);
                    const auto found = index.find(other);
                    if (found == index.end()) {
                        throw std::runtime_error("switch neighbour missing");
                    }
                    if (found->second != i) adjacency[i].push_back(found->second);
                }
            }
            std::sort(adjacency[i].begin(), adjacency[i].end());
            adjacency[i].erase(
                std::unique(adjacency[i].begin(), adjacency[i].end()),
                adjacency[i].end()
            );
        }

        for (int i = 0; i < static_cast<int>(states.size()); ++i) {
            for (int other : adjacency[i]) {
                if (!std::binary_search(
                        adjacency[other].begin(),
                        adjacency[other].end(),
                        i
                    )) {
                    throw std::runtime_error("switch adjacency is not symmetric");
                }
            }
        }

        std::vector<unsigned char> component_seen(states.size(), 0);
        std::vector<int> component_queue;
        for (int start = 0; start < static_cast<int>(states.size()); ++start) {
            if (component_seen[start]) continue;
            component_queue.clear();
            component_queue.push_back(start);
            component_seen[start] = 1;
            bool has_good = false;
            for (std::size_t cursor = 0;
                 cursor < component_queue.size();
                 ++cursor) {
                const int current = component_queue[cursor];
                has_good = has_good || good(states[current]);
                for (int other : adjacency[current]) {
                    if (!component_seen[other]) {
                        component_seen[other] = 1;
                        component_queue.push_back(other);
                    }
                }
            }
            ++result.orbits;
            result.maximum_orbit = std::max(
                result.maximum_orbit,
                static_cast<int>(component_queue.size())
            );
            if (!has_good) {
                ++result.bad_only_orbits;
                if (result.failure.empty()) result.failure = states[start];
            }
        }

        std::vector<int> distance(states.size(), -1);
        std::queue<int> distance_queue;
        for (int i = 0; i < static_cast<int>(states.size()); ++i) {
            if (good(states[i])) {
                distance[i] = 0;
                distance_queue.push(i);
            }
        }
        while (!distance_queue.empty()) {
            const int current = distance_queue.front();
            distance_queue.pop();
            for (int other : adjacency[current]) {
                if (distance[other] < 0) {
                    distance[other] = distance[current] + 1;
                    distance_queue.push(other);
                }
            }
        }
        for (int i = 0; i < static_cast<int>(states.size()); ++i) {
            if (distance[i] < 0) {
                if (result.failure.empty()) result.failure = states[i];
            } else {
                result.maximum_distance_to_good = std::max(
                    result.maximum_distance_to_good,
                    distance[i]
                );
            }
        }
        return result;
    }
};

static std::string state_text(const State& state) {
    std::string answer;
    for (int edge = 0; edge < static_cast<int>(state.size()); ++edge) {
        if (edge) answer.push_back(',');
        const unsigned char label = static_cast<unsigned char>(state[edge]);
        for (int coordinate = 0; coordinate < 5; ++coordinate) {
            if ((label >> coordinate) & 1) {
                answer.push_back(static_cast<char>('0' + coordinate));
            }
        }
    }
    return answer;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: audit_d5_contraction_circuit_orbits INPUT.g6\n";
        return 2;
    }
    std::ifstream input(argv[1]);
    if (!input) {
        std::cerr << "cannot open input\n";
        return 2;
    }

    long long graph_count = 0;
    long long contractions = 0;
    long long flows = 0;
    long long orbits = 0;
    long long bad_starting_flows = 0;
    int maximum_flows = 0;
    int maximum_orbit = 0;
    int maximum_distance_to_good = 0;
    std::string row;
    while (std::getline(input, row)) {
        if (row.empty() || row.rfind(">>", 0) == 0) continue;
        const CubicGraph graph = decode_graph6(row);
        ++graph_count;
        for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
            const Auditor auditor(contract_edge(graph, edge));
            const auto result = auditor.run();
            ++contractions;
            flows += result.flows;
            orbits += result.orbits;
            bad_starting_flows += result.bad_starting_flows;
            maximum_flows = std::max(maximum_flows, result.flows);
            maximum_orbit = std::max(maximum_orbit, result.maximum_orbit);
            maximum_distance_to_good = std::max(
                maximum_distance_to_good,
                result.maximum_distance_to_good
            );
            if (result.bad_only_orbits) {
                std::cout
                    << "FAIL graph6=" << row
                    << " edge=" << edge
                    << " endpoints=" << graph.edges[edge].first
                    << "," << graph.edges[edge].second
                    << " flows=" << result.flows
                    << " orbits=" << result.orbits
                    << " bad_only_orbits=" << result.bad_only_orbits
                    << " maximum_distance_to_good="
                    << result.maximum_distance_to_good
                    << " witness=" << state_text(result.failure)
                    << "\n";
                return 1;
            }
        }
        if ((graph_count % 100) == 0) {
            std::cerr
                << "progress graphs=" << graph_count
                << " contractions=" << contractions
                << " flows=" << flows
                << "\n";
        }
    }
    std::cout
        << "PASS graphs=" << graph_count
        << " contractions=" << contractions
        << " normalized_flows=" << flows
        << " generalized_orbits=" << orbits
        << " bad_starting_flows=" << bad_starting_flows
        << " maximum_flows_per_contraction=" << maximum_flows
        << " maximum_orbit=" << maximum_orbit
        << " maximum_distance_to_good=" << maximum_distance_to_good
        << "\n";
    return 0;
}
