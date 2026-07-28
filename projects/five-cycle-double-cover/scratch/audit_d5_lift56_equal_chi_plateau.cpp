// Exhaust the equal-chi Kempe component of the 56-vertex second lift.
//
// This is standalone: it decodes the literal 28-vertex graph6 witness,
// constructs the voltage-{18,36} two-lift, applies the certified
// neutral-then-positive escape to reach chi -8, quotients states by the
// global S5 action, and searches the entire equal-chi component for a
// positive exit.  If exhaustive, it also reports neutral-hypergraph
// connectivity and root-pair coverage throughout the plateau.

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <map>
#include <numeric>
#include <queue>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

using State = std::string;

struct Graph {
    int n = 0;
    std::vector<std::pair<int, int>> edges;
    std::vector<std::vector<int>> incidence;
};

static const std::string BASE_GRAPH6 =
    "[???????????_?O?D??g?__H@?PB??c_?aA?COO?@S??Ag?AE??@H??P?_?AGO??";

static const std::array<unsigned char, 42> BASE_LABELS = {
    0x03, 0x09, 0x0a, 0x03, 0x09, 0x0a, 0x0c,
    0x14, 0x18, 0x0c, 0x14, 0x18, 0x14, 0x12,
    0x06, 0x14, 0x12, 0x06, 0x11, 0x18, 0x09,
    0x11, 0x18, 0x09, 0x0c, 0x18, 0x14, 0x0c,
    0x18, 0x14, 0x0a, 0x06, 0x0c, 0x0a, 0x06,
    0x0c, 0x11, 0x12, 0x11, 0x12, 0x18, 0x18,
};

Graph decode_base() {
    Graph graph;
    graph.n = static_cast<unsigned char>(BASE_GRAPH6[0]) - 63;
    std::vector<int> bits;
    for (std::size_t index = 1; index < BASE_GRAPH6.size(); ++index) {
        const int value =
            static_cast<unsigned char>(BASE_GRAPH6[index]) - 63;
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
    std::sort(graph.edges.begin(), graph.edges.end());
    return graph;
}

void build_incidence(Graph& graph) {
    graph.incidence.assign(graph.n, {});
    for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
        const auto [left, right] = graph.edges[edge];
        graph.incidence[left].push_back(edge);
        graph.incidence[right].push_back(edge);
    }
}

std::pair<Graph, State> construct_second_lift() {
    const Graph base = decode_base();
    if (base.n != 28 || base.edges.size() != 42) {
        throw std::runtime_error("wrong base graph");
    }
    Graph lift;
    lift.n = 2 * base.n;
    State state;
    for (int edge = 0; edge < 42; ++edge) {
        const auto [left, right] = base.edges[edge];
        const int voltage = edge == 18 || edge == 36;
        for (int sheet = 0; sheet < 2; ++sheet) {
            lift.edges.emplace_back(
                2 * left + sheet,
                2 * right + (sheet ^ voltage)
            );
            state.push_back(static_cast<char>(BASE_LABELS[edge]));
        }
    }
    build_incidence(lift);
    return {lift, state};
}

bool graph_connected_without_edge(const Graph& graph, int omitted) {
    std::vector<unsigned char> seen(graph.n, 0);
    std::queue<int> queue;
    seen[0] = 1;
    queue.push(0);
    while (!queue.empty()) {
        const int vertex = queue.front();
        queue.pop();
        for (int edge : graph.incidence[vertex]) {
            if (edge == omitted) continue;
            const auto [left, right] = graph.edges[edge];
            const int other = left == vertex ? right : left;
            if (!seen[other]) {
                seen[other] = 1;
                queue.push(other);
            }
        }
    }
    return std::all_of(seen.begin(), seen.end(), [](unsigned char value) {
        return value != 0;
    });
}

bool valid_graph(const Graph& graph) {
    if (graph.edges.size() != 3 * graph.n / 2) return false;
    std::unordered_set<std::uint64_t> unique;
    for (const auto& [left, right] : graph.edges) {
        if (left == right) return false;
        const int low = std::min(left, right);
        const int high = std::max(left, right);
        unique.insert(
            (static_cast<std::uint64_t>(low) << 32)
            | static_cast<std::uint32_t>(high)
        );
    }
    if (unique.size() != graph.edges.size()) return false;
    for (const auto& row : graph.incidence) {
        if (row.size() != 3) return false;
    }
    if (!graph_connected_without_edge(graph, -1)) return false;
    for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
        if (!graph_connected_without_edge(graph, edge)) return false;
    }
    return true;
}

bool valid_flow(const Graph& graph, const State& state) {
    if (state.size() != graph.edges.size()) return false;
    for (unsigned char label : state) {
        if (__builtin_popcount(static_cast<unsigned int>(label)) != 2) {
            return false;
        }
    }
    for (const auto& row : graph.incidence) {
        unsigned char value = 0;
        for (int edge : row) {
            value ^= static_cast<unsigned char>(state[edge]);
        }
        if (value != 0) return false;
    }
    return true;
}

unsigned char transpose_label(
    unsigned char label, int first, int second
) {
    const int first_bit = (label >> first) & 1;
    const int second_bit = (label >> second) & 1;
    if (first_bit == second_bit) return label;
    return static_cast<unsigned char>(
        label ^ (1 << first) ^ (1 << second)
    );
}

State switched(
    const State& state,
    int first,
    int second,
    const std::vector<int>& component
) {
    State answer = state;
    for (int edge : component) {
        answer[edge] = static_cast<char>(
            transpose_label(
                static_cast<unsigned char>(answer[edge]), first, second
            )
        );
    }
    return answer;
}

std::vector<std::vector<int>> factor_components(
    const Graph& graph,
    const State& state,
    int first,
    int second
) {
    const int edge_count = static_cast<int>(graph.edges.size());
    std::vector<unsigned char> active(edge_count, 0);
    for (int edge = 0; edge < edge_count; ++edge) {
        const unsigned char label =
            static_cast<unsigned char>(state[edge]);
        active[edge] = static_cast<unsigned char>(
            ((label >> first) & 1) ^ ((label >> second) & 1)
        );
    }
    std::vector<std::vector<int>> answer;
    for (int seed = 0; seed < edge_count; ++seed) {
        if (!active[seed]) continue;
        active[seed] = 0;
        std::vector<int> component = {seed};
        std::queue<int> queue;
        queue.push(graph.edges[seed].first);
        queue.push(graph.edges[seed].second);
        std::vector<unsigned char> seen_vertex(graph.n, 0);
        seen_vertex[graph.edges[seed].first] = 1;
        seen_vertex[graph.edges[seed].second] = 1;
        while (!queue.empty()) {
            const int vertex = queue.front();
            queue.pop();
            for (int edge : graph.incidence[vertex]) {
                if (!active[edge]) continue;
                active[edge] = 0;
                component.push_back(edge);
                for (int endpoint : {
                    graph.edges[edge].first,
                    graph.edges[edge].second,
                }) {
                    if (!seen_vertex[endpoint]) {
                        seen_vertex[endpoint] = 1;
                        queue.push(endpoint);
                    }
                }
            }
        }
        std::sort(component.begin(), component.end());
        answer.push_back(std::move(component));
    }
    return answer;
}

struct Dsu {
    std::vector<int> parent;
    explicit Dsu(int n) : parent(n) {
        std::iota(parent.begin(), parent.end(), 0);
    }
    int find(int value) {
        if (parent[value] == value) return value;
        return parent[value] = find(parent[value]);
    }
    void join(int left, int right) {
        left = find(left);
        right = find(right);
        if (left != right) parent[right] = left;
    }
};

int coordinate_components(
    const Graph& graph, const State& state, int coordinate
) {
    Dsu dsu(graph.n);
    std::vector<unsigned char> used(graph.n, 0);
    for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
        const unsigned char label =
            static_cast<unsigned char>(state[edge]);
        if (!((label >> coordinate) & 1)) continue;
        const auto [left, right] = graph.edges[edge];
        used[left] = used[right] = 1;
        dsu.join(left, right);
    }
    std::unordered_set<int> roots;
    for (int vertex = 0; vertex < graph.n; ++vertex) {
        if (used[vertex]) roots.insert(dsu.find(vertex));
    }
    return static_cast<int>(roots.size());
}

int surface_chi(const Graph& graph, const State& state) {
    int circuits = 0;
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
        circuits += coordinate_components(graph, state, coordinate);
    }
    return circuits
        - static_cast<int>(graph.edges.size())
        + graph.n;
}

struct Canonicalizer {
    std::vector<std::array<unsigned char, 32>> maps;

    Canonicalizer() {
        std::array<int, 5> permutation = {0, 1, 2, 3, 4};
        do {
            std::array<unsigned char, 32> row{};
            for (int label = 0; label < 32; ++label) {
                unsigned char image = 0;
                for (int coordinate = 0; coordinate < 5; ++coordinate) {
                    if ((label >> coordinate) & 1) {
                        image |= static_cast<unsigned char>(
                            1 << permutation[coordinate]
                        );
                    }
                }
                row[label] = image;
            }
            maps.push_back(row);
        } while (std::next_permutation(
            permutation.begin(), permutation.end()
        ));
    }

    State operator()(const State& state) const {
        State best;
        bool first_candidate = true;
        for (const auto& row : maps) {
            State candidate(state.size(), '\0');
            for (std::size_t edge = 0; edge < state.size(); ++edge) {
                candidate[edge] = static_cast<char>(
                    row[static_cast<unsigned char>(state[edge])]
                );
            }
            if (first_candidate || candidate < best) {
                best = std::move(candidate);
                first_candidate = false;
            }
        }
        return best;
    }
};

void apply_seed_escape(State& state) {
    const std::vector<int> first = {
        12, 14, 18, 20, 24, 26, 30, 32, 48, 52, 54, 58,
    };
    const std::vector<int> second = {
        13, 15, 19, 21, 25, 27, 31, 33, 49, 53, 55, 59,
    };
    state = switched(state, 3, 4, first);
    state = switched(state, 3, 4, second);
}

bool contains_component(
    const std::vector<std::vector<int>>& components,
    const std::vector<int>& target
) {
    return std::find(components.begin(), components.end(), target)
        != components.end();
}

void print_state_hex(const State& state) {
    std::ios old_state(nullptr);
    old_state.copyfmt(std::cout);
    for (std::size_t edge = 0; edge < state.size(); ++edge) {
        if (edge) std::cout << " ";
        std::cout
            << std::hex << std::setfill('0') << std::setw(2)
            << static_cast<int>(
                static_cast<unsigned char>(state[edge])
            );
    }
    std::cout.copyfmt(old_state);
    std::cout << "\n";
}

int main() {
    auto [graph, initial] = construct_second_lift();
    if (graph.n != 56 || graph.edges.size() != 84) {
        throw std::runtime_error("wrong lift size");
    }
    if (!valid_graph(graph) || !valid_flow(graph, initial)) {
        throw std::runtime_error("invalid lifted graph or flow");
    }
    if (surface_chi(graph, initial) != -10) {
        throw std::runtime_error("wrong local-maximum chi");
    }
    std::map<int, int> ascent_delta_histogram;
    Dsu ascent_neutral_dsu(84);
    for (int first = 0; first < 5; ++first) {
        for (int second = first + 1; second < 5; ++second) {
            for (const auto& component : factor_components(
                graph, initial, first, second
            )) {
                const State other =
                    switched(initial, first, second, component);
                const int delta = surface_chi(graph, other) + 10;
                ++ascent_delta_histogram[delta];
                if (delta == 0) {
                    for (
                        std::size_t index = 1;
                        index < component.size();
                        ++index
                    ) {
                        ascent_neutral_dsu.join(
                            component[0], component[index]
                        );
                    }
                }
            }
        }
    }
    const std::map<int, int> expected_ascent_histogram = {
        {-3, 2}, {-2, 24}, {-1, 2}, {0, 20},
    };
    if (ascent_delta_histogram != expected_ascent_histogram) {
        throw std::runtime_error("wrong local-maximum delta histogram");
    }
    int ascent_neutral_classes = 0;
    for (int edge = 0; edge < 84; ++edge) {
        if (ascent_neutral_dsu.find(edge) == edge) {
            ++ascent_neutral_classes;
        }
    }
    if (ascent_neutral_classes != 8) {
        throw std::runtime_error("wrong ascent neutral-class count");
    }
    const std::vector<int> first_seed = {
        12, 14, 18, 20, 24, 26, 30, 32, 48, 52, 54, 58,
    };
    const std::vector<int> second_seed = {
        13, 15, 19, 21, 25, 27, 31, 33, 49, 53, 55, 59,
    };
    if (!contains_component(
        factor_components(graph, initial, 3, 4), first_seed
    )) {
        throw std::runtime_error("first seed is not a factor component");
    }
    State middle = switched(initial, 3, 4, first_seed);
    if (!valid_flow(graph, middle) || surface_chi(graph, middle) != -10) {
        throw std::runtime_error("first seed is not neutral");
    }
    if (!contains_component(
        factor_components(graph, middle, 3, 4), second_seed
    )) {
        throw std::runtime_error("second seed is not a factor component");
    }
    State escaped = switched(middle, 3, 4, second_seed);
    if (!valid_flow(graph, escaped) || surface_chi(graph, escaped) != -8) {
        throw std::runtime_error("second seed is not a +2 escape");
    }
    initial = std::move(escaped);
    if (surface_chi(graph, initial) != -8) {
        throw std::runtime_error("wrong seed chi");
    }

    Canonicalizer canonicalize;
    initial = canonicalize(initial);
    const int plateau_chi = surface_chi(graph, initial);
    std::unordered_set<State> seen;
    std::vector<State> queue;
    seen.insert(initial);
    queue.push_back(initial);

    long long directed_neutral_moves = 0;
    long long disconnected_neutral_states = 0;
    std::array<std::array<unsigned char, 84>, 84> root_covered{};
    State first_disconnected_state;

    for (std::size_t head = 0; head < queue.size(); ++head) {
        const State state = queue[head];
        Dsu neutral_dsu(84);
        bool has_neutral = false;
        for (int first = 0; first < 5; ++first) {
            for (int second = first + 1; second < 5; ++second) {
                for (const auto& component : factor_components(
                    graph, state, first, second
                )) {
                    for (std::size_t left = 0; left < component.size(); ++left) {
                        for (
                            std::size_t right = left + 1;
                            right < component.size();
                            ++right
                        ) {
                            root_covered[component[left]][component[right]] = 1;
                            root_covered[component[right]][component[left]] = 1;
                        }
                    }
                    const State other =
                        switched(state, first, second, component);
                    const int delta = surface_chi(graph, other) - plateau_chi;
                    if (delta > 0) {
                        std::cout
                            << "POSITIVE_EXIT\n"
                            << "plateau_chi " << plateau_chi << "\n"
                            << "states_seen " << seen.size() << "\n"
                            << "state_index " << head << "\n"
                            << "pair " << first << " " << second << "\n"
                            << "delta " << delta << "\n"
                            << "component";
                        for (int edge : component) std::cout << " " << edge;
                        std::cout << "\n";
                        return 0;
                    }
                    if (delta != 0) continue;
                    ++directed_neutral_moves;
                    has_neutral = true;
                    for (std::size_t index = 1; index < component.size(); ++index) {
                        neutral_dsu.join(component[0], component[index]);
                    }
                    State canonical = canonicalize(other);
                    if (seen.insert(canonical).second) {
                        queue.push_back(std::move(canonical));
                    }
                }
            }
        }
        int neutral_classes = 0;
        for (int edge = 0; edge < 84; ++edge) {
            if (neutral_dsu.find(edge) == edge) ++neutral_classes;
        }
        if (!has_neutral) neutral_classes = 84;
        if (neutral_classes > 1) {
            ++disconnected_neutral_states;
            if (first_disconnected_state.empty()) {
                first_disconnected_state = state;
            }
        }
        if ((head + 1) % 100000 == 0) {
            std::cerr
                << "processed=" << (head + 1)
                << " discovered=" << queue.size()
                << " disconnected=" << disconnected_neutral_states
                << "\n";
        }
    }

    long long uncovered_pairs = 0;
    for (int left = 0; left < 84; ++left) {
        for (int right = left + 1; right < 84; ++right) {
            if (!root_covered[left][right]) ++uncovered_pairs;
        }
    }
    std::cout
        << "EXHAUSTED_TERMINAL_PLATEAU\n"
        << "ascent_local_chi -10\n"
        << "ascent_local_delta_histogram -3:2 -2:24 -1:2 0:20\n"
        << "ascent_local_neutral_classes 8\n"
        << "ascent_step_1 pair=34 delta=0 component="
        << "12,14,18,20,24,26,30,32,48,52,54,58\n"
        << "ascent_step_2 pair=34 delta=2 component="
        << "13,15,19,21,25,27,31,33,49,53,55,59\n"
        << "plateau_chi " << plateau_chi << "\n"
        << "states_mod_s5 " << seen.size() << "\n"
        << "directed_neutral_moves " << directed_neutral_moves << "\n"
        << "states_with_disconnected_neutral_hypergraph "
        << disconnected_neutral_states << "\n"
        << "uncovered_root_pairs " << uncovered_pairs << "\n";

    if (first_disconnected_state.empty()) {
        throw std::runtime_error("expected a disconnected neutral state");
    }
    Dsu witness_dsu(84);
    std::map<int, int> witness_delta_histogram;
    int witness_neutral_components = 0;
    for (int first = 0; first < 5; ++first) {
        for (int second = first + 1; second < 5; ++second) {
            for (const auto& component : factor_components(
                graph, first_disconnected_state, first, second
            )) {
                const State other = switched(
                    first_disconnected_state,
                    first,
                    second,
                    component
                );
                const int delta =
                    surface_chi(graph, other) - plateau_chi;
                ++witness_delta_histogram[delta];
                if (delta != 0) continue;
                ++witness_neutral_components;
                for (std::size_t index = 1; index < component.size(); ++index) {
                    witness_dsu.join(component[0], component[index]);
                }
            }
        }
    }
    std::map<int, std::vector<int>> witness_classes;
    for (int edge = 0; edge < 84; ++edge) {
        witness_classes[witness_dsu.find(edge)].push_back(edge);
    }
    std::cout << "first_disconnected_state_hex ";
    print_state_hex(first_disconnected_state);
    std::cout << "first_disconnected_delta_histogram";
    for (const auto& [delta, count] : witness_delta_histogram) {
        std::cout << " " << delta << ":" << count;
    }
    std::cout
        << "\nfirst_disconnected_neutral_components "
        << witness_neutral_components
        << "\nfirst_disconnected_neutral_classes "
        << witness_classes.size()
        << "\n";
    int class_index = 0;
    for (const auto& [root, edges] : witness_classes) {
        static_cast<void>(root);
        std::cout << "class_" << class_index++;
        for (int edge : edges) std::cout << " " << edge;
        std::cout << "\n";
    }
    return 0;
}
