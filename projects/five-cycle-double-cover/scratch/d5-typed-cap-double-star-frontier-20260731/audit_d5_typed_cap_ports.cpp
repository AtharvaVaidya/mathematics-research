#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
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

Graph decode_graph6(const std::string& row) {
    Graph graph;
    graph.n = static_cast<unsigned char>(row.at(0)) - 63;
    std::vector<int> bits;
    for (std::size_t i = 1; i < row.size(); ++i) {
        int value = static_cast<unsigned char>(row[i]) - 63;
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
    for (int e = 0; e < static_cast<int>(graph.edges.size()); ++e) {
        rows[graph.edges[e].first].push_back(e);
        rows[graph.edges[e].second].push_back(e);
    }
    graph.incidence.resize(graph.n);
    for (int v = 0; v < graph.n; ++v) {
        if (rows[v].size() != 3) throw std::runtime_error("noncubic");
        graph.incidence[v] = {rows[v][0], rows[v][1], rows[v][2]};
    }
    return graph;
}

bool is_label(unsigned char value) {
    return std::find(LABELS.begin(), LABELS.end(), value) != LABELS.end();
}

std::vector<std::array<int, 5>> all_permutations() {
    std::array<int, 5> p = {0, 1, 2, 3, 4};
    std::vector<std::array<int, 5>> answer;
    do answer.push_back(p); while (std::next_permutation(p.begin(), p.end()));
    return answer;
}

unsigned char permute_label(unsigned char label, const std::array<int, 5>& p) {
    unsigned char answer = 0;
    for (int i = 0; i < 5; ++i) if ((label >> i) & 1) answer |= 1 << p[i];
    return answer;
}

struct Audit {
    Graph graph;
    std::vector<std::array<int, 5>> permutations = all_permutations();
    std::array<std::array<unsigned char, 32>, 120> permuted{};

    explicit Audit(Graph g) : graph(std::move(g)) {
        for (int p = 0; p < 120; ++p)
            for (auto label : LABELS) permuted[p][label] = permute_label(label, permutations[p]);
    }

    State canonical(const State& state) const {
        State best;
        bool first = true;
        for (int p = 0; p < 120; ++p) {
            State candidate(state.size(), '\0');
            for (int e = 0; e < static_cast<int>(state.size()); ++e)
                candidate[e] = static_cast<char>(permuted[p][static_cast<unsigned char>(state[e])]);
            if (first || candidate < best) { best = candidate; first = false; }
        }
        return best;
    }

    bool assign(State& state, int edge, unsigned char label, std::vector<int>& trail) const {
        if (state[edge]) return static_cast<unsigned char>(state[edge]) == label;
        if (!is_label(label)) return false;
        state[edge] = static_cast<char>(label);
        trail.push_back(edge);
        std::vector<int> queue = {graph.edges[edge].first, graph.edges[edge].second};
        while (!queue.empty()) {
            int v = queue.back(); queue.pop_back();
            int count = 0, missing = -1;
            unsigned char value = 0;
            for (int e : graph.incidence[v]) {
                if (state[e]) { ++count; value ^= static_cast<unsigned char>(state[e]); }
                else missing = e;
            }
            if (count < 2) continue;
            if (count == 3) { if (value) return false; continue; }
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
        for (int e = 0; e < static_cast<int>(state.size()); ++e) if (!state[e]) { edge = e; break; }
        if (edge < 0) { answers.insert(canonical(state)); return; }
        bool empty = std::all_of(state.begin(), state.end(), [](char c) { return c == 0; });
        int choices = empty ? 1 : 10;
        for (int i = 0; i < choices; ++i) {
            std::vector<int> trail;
            if (assign(state, edge, LABELS[i], trail)) enumerate_visit(state, answers);
            for (auto it = trail.rbegin(); it != trail.rend(); ++it) state[*it] = 0;
        }
    }

    std::unordered_set<State> flows() const {
        State state(graph.edges.size(), '\0');
        std::unordered_set<State> answer;
        enumerate_visit(state, answer);
        return answer;
    }

    std::vector<std::vector<int>> components(const State& state, unsigned char pair) const {
        std::vector<unsigned char> active(graph.edges.size(), 0), seen(graph.edges.size(), 0);
        for (int e = 0; e < static_cast<int>(graph.edges.size()); ++e)
            active[e] = (__builtin_popcount(static_cast<unsigned char>(state[e]) & pair) == 1);
        std::vector<std::vector<int>> answer;
        for (int start = 0; start < static_cast<int>(graph.edges.size()); ++start) {
            if (!active[start] || seen[start]) continue;
            std::vector<int> stack = {start}, component;
            seen[start] = 1;
            while (!stack.empty()) {
                int e = stack.back(); stack.pop_back(); component.push_back(e);
                for (int v : {graph.edges[e].first, graph.edges[e].second})
                    for (int f : graph.incidence[v]) if (active[f] && !seen[f]) { seen[f] = 1; stack.push_back(f); }
            }
            answer.push_back(component);
        }
        return answer;
    }

    // Bits 2*p+mode, p=01,02,12 in the local incidence order; mode 0 internal, 1 external.
    std::map<std::pair<int,int>, int> typed_masks(const std::unordered_set<State>& all) const {
        std::map<std::pair<int,int>, int> masks;
        for (int z = 0; z < graph.n; ++z)
            for (int root = 0; root < static_cast<int>(graph.edges.size()); ++root)
                if (graph.edges[root].first != z && graph.edges[root].second != z) masks[{z,root}] = 0;
        for (const State& state : all) {
            for (unsigned char pair : LABELS) {
                for (const auto& component : components(state, pair)) {
                    std::vector<unsigned char> in(graph.edges.size(), 0);
                    for (int e : component) in[e] = 1;
                    for (int z = 0; z < graph.n; ++z) {
                        std::vector<int> slots;
                        int inactive = -1;
                        for (int i = 0; i < 3; ++i) {
                            int e = graph.incidence[z][i];
                            if (in[e]) slots.push_back(i); else inactive = i;
                        }
                        if (slots.size() != 2) continue;
                        int physical = -1;
                        if (slots == std::vector<int>({0,1})) physical = 0;
                        if (slots == std::vector<int>({0,2})) physical = 1;
                        if (slots == std::vector<int>({1,2})) physical = 2;
                        if (physical < 0 || inactive < 0) throw std::runtime_error("bad slots");
                        int mode = pair == static_cast<unsigned char>(state[graph.incidence[z][inactive]]) ? 0 : 1;
                        for (int root : component) {
                            if (graph.edges[root].first == z || graph.edges[root].second == z) continue;
                            masks[{z,root}] |= 1 << (2 * physical + mode);
                        }
                    }
                }
            }
        }
        return masks;
    }
};

bool covers_ports(int mask) {
    bool p01 = mask & 0x03, p02 = mask & 0x0c, p12 = mask & 0x30;
    return (p01 || p02) && (p01 || p12) && (p02 || p12);
}

bool contains_double_star(int mask) {
    const bool pair01 = (mask & 0x03) == 0x03;
    const bool pair02 = (mask & 0x0c) == 0x0c;
    const bool pair12 = (mask & 0x30) == 0x30;
    return (pair01 && pair02) || (pair01 && pair12) || (pair02 && pair12);
}

std::string bits6(int mask) {
    std::string s;
    for (int i = 0; i < 6; ++i) if ((mask >> i) & 1) s += (s.empty() ? "" : ",") + std::to_string(i);
    return s;
}

int main() {
    std::string row;
    long long graphs = 0, interfaces = 0, covered = 0, double_star = 0;
    std::set<int> masks;
    while (std::cin >> row) {
        if (!row.empty() && row[0] == '>') continue;
        Graph graph = decode_graph6(row);
        Audit audit(graph);
        auto all = audit.flows();
        auto local = audit.typed_masks(all);
        for (const auto& [key, mask] : local) {
            ++interfaces;
            masks.insert(mask);
            if (covers_ports(mask)) ++covered;
            if (contains_double_star(mask)) ++double_star;
        }
        ++graphs;
        std::cerr << "graph " << graphs << " flows " << all.size() << " masks " << masks.size() << "\n";
    }
    std::cout << "graphs=" << graphs << " interfaces=" << interfaces
              << " covered=" << covered << " double_star=" << double_star
              << " distinct=" << masks.size() << "\n";
    for (int mask : masks) {
        std::cout << mask << " " << bits6(mask)
                  << " cover=" << covers_ports(mask)
                  << " double_star=" << contains_double_star(mask) << "\n";
    }
    std::vector<int> cv;
    for (int mask : masks) if (covers_ports(mask)) cv.push_back(mask);
    for (int a : cv) for (int b : cv) if ((a & b) == 0) {
        std::cout << "DISJOINT " << a << " " << b << "\n";
        return 2;
    }
    if (double_star != interfaces) {
        std::cout << "DOUBLE_STAR_FAILURE\n";
        return 3;
    }
    std::cout << "NO_DISJOINT_COVERED_MASKS\n";
}
