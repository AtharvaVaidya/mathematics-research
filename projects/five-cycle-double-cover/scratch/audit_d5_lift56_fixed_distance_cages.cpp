// Search the frozen 56-vertex terminal plateau for a fixed-distance cage.
//
// This is a focused extension of audit_d5_lift56_equal_chi_plateau.cpp.
// It reconstructs the same complete terminal plateau, stores its neutral
// adjacency graph, and tests all root pairs {75,e}.  A failure is a connected
// component of states of one fixed factor-chain distance d>1 with no incident
// neutral edge to smaller distance.

#define main d5_lift56_original_main
#include "audit_d5_lift56_equal_chi_plateau.cpp"
#undef main

#include <bitset>
#include <unordered_map>

using EdgeMask84 = std::bitset<84>;

static std::vector<EdgeMask84> all_factor_masks(
    const Graph& graph,
    const State& state
) {
    std::vector<EdgeMask84> answer;
    for (int first = 0; first < 5; ++first) {
        for (int second = first + 1; second < 5; ++second) {
            for (const auto& component :
                 factor_components(graph, state, first, second)) {
                EdgeMask84 mask;
                for (int edge : component) mask.set(edge);
                answer.push_back(mask);
            }
        }
    }
    return answer;
}

static std::array<unsigned char, 84> distances_from_edge_75(
    const Graph& graph,
    const State& state
) {
    const auto factors = all_factor_masks(graph, state);
    const int count = static_cast<int>(factors.size());
    std::vector<int> distance(count, -1);
    std::queue<int> queue;
    for (int index = 0; index < count; ++index) {
        if (factors[index].test(75)) {
            distance[index] = 1;
            queue.push(index);
        }
    }
    while (!queue.empty()) {
        const int current = queue.front();
        queue.pop();
        for (int other = 0; other < count; ++other) {
            if (distance[other] >= 0) continue;
            if ((factors[current] & factors[other]).none()) continue;
            distance[other] = distance[current] + 1;
            queue.push(other);
        }
    }

    std::array<unsigned char, 84> answer{};
    answer.fill(255);
    for (int edge = 0; edge < 84; ++edge) {
        int best = 255;
        for (int index = 0; index < count; ++index) {
            if (factors[index].test(edge)) {
                best = std::min(best, distance[index]);
            }
        }
        if (best < 0 || best == 255) {
            throw std::runtime_error("factor-component hypergraph disconnected");
        }
        answer[edge] = static_cast<unsigned char>(best);
    }
    return answer;
}

int main() {
    auto [graph, initial] = construct_second_lift();
    if (!valid_graph(graph) || !valid_flow(graph, initial)) {
        throw std::runtime_error("invalid lifted graph or flow");
    }
    apply_seed_escape(initial);
    if (surface_chi(graph, initial) != -8) {
        throw std::runtime_error("wrong terminal seed");
    }

    Canonicalizer canonicalize;
    initial = canonicalize(initial);
    const int plateau_chi = surface_chi(graph, initial);

    std::vector<State> states = {initial};
    std::unordered_map<State, int> index;
    index.emplace(initial, 0);
    std::vector<std::vector<int>> adjacency(1);

    for (std::size_t head = 0; head < states.size(); ++head) {
        const State state = states[head];
        for (int first = 0; first < 5; ++first) {
            for (int second = first + 1; second < 5; ++second) {
                for (const auto& component :
                     factor_components(graph, state, first, second)) {
                    State other = switched(
                        state, first, second, component
                    );
                    const int delta =
                        surface_chi(graph, other) - plateau_chi;
                    if (delta > 0) {
                        throw std::runtime_error(
                            "positive exit from claimed terminal plateau"
                        );
                    }
                    if (delta != 0) continue;
                    other = canonicalize(other);
                    auto [where, inserted] = index.emplace(
                        other, static_cast<int>(states.size())
                    );
                    if (inserted) {
                        states.push_back(other);
                        adjacency.emplace_back();
                    }
                    adjacency[head].push_back(where->second);
                }
            }
        }
        std::sort(adjacency[head].begin(), adjacency[head].end());
        adjacency[head].erase(
            std::unique(adjacency[head].begin(), adjacency[head].end()),
            adjacency[head].end()
        );
    }
    if (states.size() != 55652) {
        throw std::runtime_error("wrong terminal plateau size");
    }

    std::vector<std::array<unsigned char, 84>> distances(states.size());
    for (std::size_t state = 0; state < states.size(); ++state) {
        distances[state] = distances_from_edge_75(graph, states[state]);
    }

    long long subplateaus = 0;
    int failures = 0;
    std::vector<unsigned char> seen(states.size());
    std::vector<int> queue;
    for (int target = 0; target < 84; ++target) {
        if (target == 75) continue;
        std::fill(seen.begin(), seen.end(), 0);
        for (int start = 0; start < static_cast<int>(states.size()); ++start) {
            const int level = distances[start][target];
            if (level <= 1 || seen[start]) continue;
            ++subplateaus;
            bool descent = false;
            queue.clear();
            queue.push_back(start);
            seen[start] = 1;
            for (std::size_t head = 0; head < queue.size(); ++head) {
                const int current = queue[head];
                for (int other : adjacency[current]) {
                    const int other_level = distances[other][target];
                    if (other_level < level) descent = true;
                    if (other_level == level && !seen[other]) {
                        seen[other] = 1;
                        queue.push_back(other);
                    }
                }
            }
            if (!descent) {
                ++failures;
                std::cout
                    << "FIXED_DISTANCE_CAGE"
                    << " root=75 target=" << target
                    << " distance=" << level
                    << " states=" << queue.size()
                    << " representative=" << start
                    << "\nstate_hex ";
                print_state_hex(states[start]);
                return 1;
            }
        }
    }

    long long undirected_neutral_edges = 0;
    for (const auto& row : adjacency) {
        undirected_neutral_edges += row.size();
    }
    undirected_neutral_edges /= 2;
    std::cout
        << "PASS_FIXED_DISTANCE_ROOT75"
        << " states=" << states.size()
        << " neutral_edges=" << undirected_neutral_edges
        << " root_pairs=83"
        << " fixed_distance_subplateaus=" << subplateaus
        << " failures=" << failures
        << "\n";
    return 0;
}
