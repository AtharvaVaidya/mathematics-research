#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

using State = std::string;

struct Graph {
    int n = 0;
    std::vector<std::pair<int, int>> edges;
    std::vector<std::array<int, 3>> incidence;
};

static const std::array<unsigned char, 10> LABELS = {
    3, 5, 9, 17, 6, 10, 18, 12, 20, 24
};

std::string json_escape(const std::string& value) {
    std::string answer;
    for (unsigned char c : value) {
        if (c == '\\' || c == '"') answer.push_back('\\');
        answer.push_back(static_cast<char>(c));
    }
    return answer;
}

Graph decode_graph6(const std::string& row) {
    if (row.empty() || row[0] == '~') throw std::runtime_error("short graph6 required");
    Graph graph;
    graph.n = static_cast<unsigned char>(row[0]) - 63;
    std::vector<int> bits;
    for (std::size_t i = 1; i < row.size(); ++i) {
        int value = static_cast<unsigned char>(row[i]) - 63;
        if (value < 0 || value >= 64) throw std::runtime_error("bad graph6 byte");
        for (int shift = 5; shift >= 0; --shift) bits.push_back((value >> shift) & 1);
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
        auto [u, v] = graph.edges[edge];
        rows[u].push_back(edge);
        rows[v].push_back(edge);
    }
    graph.incidence.resize(graph.n);
    for (int vertex = 0; vertex < graph.n; ++vertex) {
        if (rows[vertex].size() != 3) throw std::runtime_error("graph is not cubic");
        graph.incidence[vertex] = {rows[vertex][0], rows[vertex][1], rows[vertex][2]};
    }
    return graph;
}

bool is_label(unsigned char value) {
    return std::find(LABELS.begin(), LABELS.end(), value) != LABELS.end();
}

std::vector<std::array<int, 5>> all_permutations() {
    std::array<int, 5> current = {0, 1, 2, 3, 4};
    std::vector<std::array<int, 5>> answer;
    do {
        answer.push_back(current);
    } while (std::next_permutation(current.begin(), current.end()));
    return answer;
}

unsigned char permute_label(unsigned char label, const std::array<int, 5>& permutation) {
    unsigned char answer = 0;
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
        if ((label >> coordinate) & 1) answer |= static_cast<unsigned char>(1 << permutation[coordinate]);
    }
    return answer;
}

struct Auditor {
    Graph graph;
    std::vector<std::array<int, 5>> permutations;
    std::array<std::array<unsigned char, 32>, 120> permuted{};

    explicit Auditor(Graph input) : graph(std::move(input)), permutations(all_permutations()) {
        if (permutations.size() != 120) throw std::runtime_error("wrong S5 size");
        for (int p = 0; p < 120; ++p) {
            for (unsigned char label : LABELS) {
                permuted[p][label] = permute_label(label, permutations[p]);
            }
        }
    }

    State canonical(const State& state) const {
        State best;
        bool first = true;
        for (int p = 0; p < 120; ++p) {
            State candidate(state.size(), '\0');
            for (int edge = 0; edge < static_cast<int>(state.size()); ++edge) {
                candidate[edge] = static_cast<char>(
                    permuted[p][static_cast<unsigned char>(state[edge])]
                );
            }
            if (first || candidate < best) {
                best = std::move(candidate);
                first = false;
            }
        }
        return best;
    }

    bool assign(
        State& state,
        int edge,
        unsigned char label,
        std::vector<int>& trail
    ) const {
        if (state[edge]) return static_cast<unsigned char>(state[edge]) == label;
        if (!is_label(label)) return false;
        state[edge] = static_cast<char>(label);
        trail.push_back(edge);
        std::vector<int> queue = {graph.edges[edge].first, graph.edges[edge].second};
        while (!queue.empty()) {
            int vertex = queue.back();
            queue.pop_back();
            const auto& row = graph.incidence[vertex];
            int count = 0;
            int missing = -1;
            unsigned char value = 0;
            for (int item : row) {
                if (state[item]) {
                    ++count;
                    value ^= static_cast<unsigned char>(state[item]);
                } else {
                    missing = item;
                }
            }
            if (count < 2) continue;
            if (count == 3) {
                if (value != 0) return false;
                continue;
            }
            if (!is_label(value)) return false;
            state[missing] = static_cast<char>(value);
            trail.push_back(missing);
            queue.push_back(graph.edges[missing].first);
            queue.push_back(graph.edges[missing].second);
        }
        return true;
    }

    void enumerate_visit(State& state, std::unordered_set<State>& answers) const {
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
        bool empty = std::all_of(state.begin(), state.end(), [](char c) { return c == 0; });
        int choices = empty ? 1 : 10;
        for (int index = 0; index < choices; ++index) {
            std::vector<int> trail;
            if (assign(state, edge, LABELS[index], trail)) enumerate_visit(state, answers);
            for (auto iterator = trail.rbegin(); iterator != trail.rend(); ++iterator) {
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

    uint32_t active_mask(const State& state, int first, int second) const {
        uint32_t mask = 0;
        for (int edge = 0; edge < static_cast<int>(state.size()); ++edge) {
            unsigned char label = static_cast<unsigned char>(state[edge]);
            if (((label >> first) & 1) ^ ((label >> second) & 1)) mask |= uint32_t(1) << edge;
        }
        return mask;
    }

    std::vector<uint32_t> component_masks(uint32_t mask) const {
        uint32_t unseen = mask;
        std::vector<uint32_t> answer;
        while (unseen) {
            int first_edge = __builtin_ctz(unseen);
            unseen &= ~(uint32_t(1) << first_edge);
            std::vector<int> stack = {first_edge};
            uint32_t component = 0;
            while (!stack.empty()) {
                int edge = stack.back();
                stack.pop_back();
                component |= uint32_t(1) << edge;
                for (int vertex : {graph.edges[edge].first, graph.edges[edge].second}) {
                    for (int other : graph.incidence[vertex]) {
                        uint32_t bit = uint32_t(1) << other;
                        if (unseen & bit) {
                            unseen &= ~bit;
                            stack.push_back(other);
                        }
                    }
                }
            }
            answer.push_back(component);
        }
        return answer;
    }

    static unsigned char transpose_label(unsigned char label, int first, int second) {
        if (((label >> first) & 1) == ((label >> second) & 1)) return label;
        return label ^ static_cast<unsigned char>((1 << first) | (1 << second));
    }

    State switched(
        const State& state,
        int first,
        int second,
        uint32_t component
    ) const {
        State answer = state;
        for (int edge = 0; edge < static_cast<int>(state.size()); ++edge) {
            if ((component >> edge) & 1) {
                answer[edge] = static_cast<char>(
                    transpose_label(static_cast<unsigned char>(state[edge]), first, second)
                );
            }
        }
        return canonical(answer);
    }

    static int pair_index(int edge_count, int first, int second) {
        int answer = 0;
        for (int left = 0; left < first; ++left) answer += edge_count - left - 1;
        return answer + second - first - 1;
    }

    struct Result {
        int flows = 0;
        int orbits = 0;
        long long orbit_root_tests = 0;
        int failures = 0;
        State first_failure_state;
        int first_root = -1;
        int second_root = -1;
        int maximum_orbit = 0;
    };

    Result run() const {
        auto all_flows = enumerate_flows();
        auto unseen = all_flows;
        Result result;
        result.flows = static_cast<int>(all_flows.size());
        int edge_count = static_cast<int>(graph.edges.size());
        int root_pairs = edge_count * (edge_count - 1) / 2;
        while (!unseen.empty()) {
            State initial = *unseen.begin();
            std::unordered_set<State> orbit = {initial};
            std::queue<State> queue;
            queue.push(initial);
            std::vector<unsigned char> rescued(root_pairs, 0);
            int rescued_count = 0;
            while (!queue.empty()) {
                State state = queue.front();
                queue.pop();
                for (int first = 0; first < 5; ++first) {
                    for (int second = first + 1; second < 5; ++second) {
                        uint32_t mask = active_mask(state, first, second);
                        for (uint32_t component : component_masks(mask)) {
                            std::vector<int> edges;
                            uint32_t copy = component;
                            while (copy) {
                                int edge = __builtin_ctz(copy);
                                copy &= copy - 1;
                                edges.push_back(edge);
                            }
                            if (rescued_count < root_pairs) {
                                for (int i = 0; i < static_cast<int>(edges.size()); ++i) {
                                    for (int j = i + 1; j < static_cast<int>(edges.size()); ++j) {
                                        int index = pair_index(edge_count, edges[i], edges[j]);
                                        if (!rescued[index]) {
                                            rescued[index] = 1;
                                            ++rescued_count;
                                        }
                                    }
                                }
                            }
                            State other = switched(state, first, second, component);
                            if (!all_flows.count(other)) throw std::runtime_error("Kempe neighbour absent");
                            if (orbit.insert(other).second) queue.push(other);
                        }
                    }
                }
            }
            for (const State& state : orbit) unseen.erase(state);
            ++result.orbits;
            result.orbit_root_tests += root_pairs;
            result.maximum_orbit = std::max(result.maximum_orbit, static_cast<int>(orbit.size()));
            if (rescued_count != root_pairs) {
                ++result.failures;
                if (result.first_root < 0) {
                    result.first_failure_state = initial;
                    for (int first = 0; first < edge_count; ++first) {
                        for (int second = first + 1; second < edge_count; ++second) {
                            int index = pair_index(edge_count, first, second);
                            if (!rescued[index]) {
                                result.first_root = first;
                                result.second_root = second;
                                break;
                            }
                        }
                        if (result.first_root >= 0) break;
                    }
                }
            }
        }
        return result;
    }
};

std::string state_hex(const State& state) {
    static const char* digits = "0123456789abcdef";
    std::string answer;
    for (unsigned char value : state) {
        answer.push_back(digits[value >> 4]);
        answer.push_back(digits[value & 15]);
    }
    return answer;
}

int main(int argc, char** argv) {
    std::ostream* output = &std::cout;
    std::ofstream file;
    if (argc == 3 && std::string(argv[1]) == "--output") {
        file.open(argv[2]);
        if (!file) throw std::runtime_error("cannot open output");
        output = &file;
    } else if (argc != 1) {
        throw std::runtime_error("usage: audit_d5_root_kempe_orbits [--output FILE]");
    }

    std::string row;
    int graphs = 0;
    long long flows = 0;
    long long orbits = 0;
    long long tests = 0;
    int failures = 0;
    while (std::getline(std::cin, row)) {
        if (row.empty()) continue;
        ++graphs;
        Graph graph = decode_graph6(row);
        Auditor auditor(graph);
        Auditor::Result result = auditor.run();
        flows += result.flows;
        orbits += result.orbits;
        tests += result.orbit_root_tests;
        failures += result.failures;
        *output
            << "{\"status\":\"GRAPH_DONE\",\"index\":" << graphs
            << ",\"graph6\":\"" << json_escape(row) << "\""
            << ",\"vertices\":" << graph.n
            << ",\"edges\":" << graph.edges.size()
            << ",\"flows_mod_s5\":" << result.flows
            << ",\"kempe_orbits_mod_s5\":" << result.orbits
            << ",\"orbit_root_pair_tests\":" << result.orbit_root_tests
            << ",\"maximum_orbit\":" << result.maximum_orbit
            << ",\"failed_orbits\":" << result.failures;
        if (result.first_root >= 0) {
            *output
                << ",\"first_failure\":{\"state_hex\":\""
                << state_hex(result.first_failure_state)
                << "\",\"roots\":[" << result.first_root << "," << result.second_root << "]}";
        } else {
            *output << ",\"first_failure\":null";
        }
        *output << "}\n";
        output->flush();
    }
    *output
        << "{\"status\":\"SUMMARY\",\"graphs\":" << graphs
        << ",\"flows_mod_s5\":" << flows
        << ",\"kempe_orbits_mod_s5\":" << orbits
        << ",\"orbit_root_pair_tests\":" << tests
        << ",\"failed_orbits\":" << failures << "}\n";
    return failures ? 1 : 0;
}
