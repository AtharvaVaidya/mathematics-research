// Compute the exact maximum number of root-component Kempe switches needed
// to rescue a pair of root edges, or exhibit a root pair that is never
// rescued by root-component switches alone.
//
// A move is admissible for roots r,s when its switched factor component
// contains exactly one of r,s.  If the current state is root-bad, this is
// precisely a Kempe switch on the factor component through one root.
//
// This audits a reconfiguration lemma stronger than the full rooted-orbit
// claim.  A failure here is not a FiveCDC counterexample because a remote
// component switch may still rescue the roots.

#define main d5_root_orbit_audit_unused_main
#include "audit_d5_root_kempe_orbits.cpp"
#undef main

#include <unordered_map>

struct RootMoveDistance {
    int target;
    uint32_t component;
};

static std::vector<uint64_t> pair_mask_for_component(
    int edges,
    uint32_t component
) {
    const int pairs = edges * (edges - 1) / 2;
    std::vector<uint64_t> answer((pairs + 63) / 64, 0);
    for (int first = 0; first < edges; ++first) {
        for (int second = first + 1; second < edges; ++second) {
            if (
                ((component >> first) & 1)
                == ((component >> second) & 1)
            ) {
                continue;
            }
            const int index = Auditor::pair_index(edges, first, second);
            answer[index / 64] |= uint64_t(1) << (index % 64);
        }
    }
    return answer;
}

static std::vector<uint64_t> successful_pair_mask(
    const Auditor& auditor,
    const State& state
) {
    const int edges = static_cast<int>(auditor.graph.edges.size());
    const int pairs = edges * (edges - 1) / 2;
    std::vector<uint64_t> answer((pairs + 63) / 64, 0);
    for (int first = 0; first < 5; ++first) {
        for (int second = first + 1; second < 5; ++second) {
            const uint32_t active =
                auditor.active_mask(state, first, second);
            for (uint32_t component : auditor.component_masks(active)) {
                std::vector<int> members;
                uint32_t copy = component;
                while (copy) {
                    const int edge = __builtin_ctz(copy);
                    copy &= copy - 1;
                    members.push_back(edge);
                }
                for (int left = 0;
                     left < static_cast<int>(members.size());
                     ++left) {
                    for (int right = left + 1;
                         right < static_cast<int>(members.size());
                         ++right) {
                        const int pair = Auditor::pair_index(
                            edges, members[left], members[right]
                        );
                        answer[pair / 64] |= uint64_t(1) << (pair % 64);
                    }
                }
            }
        }
    }
    return answer;
}

static std::pair<int, int> decode_pair(int edges, int wanted) {
    int cursor = 0;
    for (int first = 0; first < edges; ++first) {
        for (int second = first + 1; second < edges; ++second) {
            if (cursor++ == wanted) return {first, second};
        }
    }
    throw std::runtime_error("pair index out of range");
}

static bool audit_graph(
    const std::string& graph6,
    int graph_index,
    int depth_limit
) {
    Graph graph = decode_graph6(graph6);
    Auditor auditor(graph);
    auto flow_set = auditor.enumerate_flows();
    std::vector<State> states(flow_set.begin(), flow_set.end());
    std::sort(states.begin(), states.end());

    std::unordered_map<State, int> index;
    index.reserve(states.size() * 2);
    for (int state = 0; state < static_cast<int>(states.size()); ++state) {
        index.emplace(states[state], state);
    }

    const int edges = static_cast<int>(graph.edges.size());
    const int pairs = edges * (edges - 1) / 2;
    const int words = (pairs + 63) / 64;
    const uint64_t final_word_mask =
        pairs % 64 == 0 ? ~uint64_t(0)
                        : (uint64_t(1) << (pairs % 64)) - 1;

    std::vector<std::vector<uint64_t>> base(states.size());
    std::vector<std::vector<RootMoveDistance>> moves(states.size());
    std::unordered_map<uint32_t, std::vector<uint64_t>> pair_masks;

    for (int state = 0; state < static_cast<int>(states.size()); ++state) {
        base[state] = successful_pair_mask(auditor, states[state]);
        for (int first = 0; first < 5; ++first) {
            for (int second = first + 1; second < 5; ++second) {
                const uint32_t active =
                    auditor.active_mask(states[state], first, second);
                for (uint32_t component : auditor.component_masks(active)) {
                    const State other = auditor.switched(
                        states[state], first, second, component
                    );
                    const auto found = index.find(other);
                    if (found == index.end()) {
                        throw std::runtime_error("Kempe neighbour absent");
                    }
                    moves[state].push_back({found->second, component});
                    if (!pair_masks.count(component)) {
                        pair_masks.emplace(
                            component,
                            pair_mask_for_component(edges, component)
                        );
                    }
                }
            }
        }
    }

    std::vector<std::vector<uint64_t>> reached = base;
    int maximum_distance = 0;
    int maximum_witness_state = -1;
    int maximum_witness_pair = -1;
    long long initially_bad = 0;
    for (const auto& row : base) {
        for (int word = 0; word < words; ++word) {
            const uint64_t mask =
                word + 1 == words ? final_word_mask : ~uint64_t(0);
            initially_bad += __builtin_popcountll((~row[word]) & mask);
        }
    }

    bool complete = false;
    bool fixed = false;
    for (int depth = 0; depth <= depth_limit; ++depth) {
        complete = true;
        for (const auto& row : reached) {
            for (int word = 0; word < words; ++word) {
                const uint64_t mask =
                    word + 1 == words ? final_word_mask : ~uint64_t(0);
                if ((row[word] & mask) != mask) complete = false;
            }
        }
        if (complete) {
            maximum_distance = depth;
            break;
        }
        if (depth == depth_limit) break;

        auto next = reached;
        bool changed = false;
        int iteration_witness_state = -1;
        int iteration_witness_pair = -1;
        for (int state = 0; state < static_cast<int>(states.size()); ++state) {
            for (const RootMoveDistance& move : moves[state]) {
                const auto& allowed = pair_masks.at(move.component);
                for (int word = 0; word < words; ++word) {
                    const uint64_t addition =
                        allowed[word] & reached[move.target][word];
                    const uint64_t enlarged = next[state][word] | addition;
                    const uint64_t newly_reached =
                        enlarged & ~next[state][word];
                    if (newly_reached && iteration_witness_state < 0) {
                        iteration_witness_state = state;
                        iteration_witness_pair =
                            word * 64 + __builtin_ctzll(newly_reached);
                    }
                    changed = changed || enlarged != next[state][word];
                    next[state][word] = enlarged;
                }
            }
        }
        reached.swap(next);
        if (iteration_witness_state >= 0) {
            maximum_witness_state = iteration_witness_state;
            maximum_witness_pair = iteration_witness_pair;
        }
        if (!changed) {
            fixed = true;
            maximum_distance = depth;
            break;
        }
    }

    if (!complete) {
        for (int state = 0; state < static_cast<int>(states.size()); ++state) {
            for (int pair = 0; pair < pairs; ++pair) {
                if ((reached[state][pair / 64] >> (pair % 64)) & 1) {
                    continue;
                }
                const auto [root, target] = decode_pair(edges, pair);
                std::cout
                    << "{\"status\":\""
                    << (fixed ? "ROOT_LOCAL_COUNTEREXAMPLE"
                              : "DEPTH_LIMIT")
                    << "\",\"graph_index\":" << graph_index
                    << ",\"graph6\":\"" << json_escape(graph6)
                    << "\",\"vertices\":" << graph.n
                    << ",\"edges\":" << edges
                    << ",\"flows_mod_s5\":" << states.size()
                    << ",\"depth_reached\":" << maximum_distance
                    << ",\"state_hex\":\"" << state_hex(states[state])
                    << "\",\"roots\":[" << root << ',' << target << "]}\n";
                return false;
            }
        }
    }

    std::cout
        << "{\"status\":\"GRAPH_DONE\",\"graph_index\":" << graph_index
        << ",\"graph6\":\"" << json_escape(graph6)
        << "\",\"flows_mod_s5\":" << states.size()
        << ",\"initially_bad_state_root_pairs\":" << initially_bad
        << ",\"maximum_root_switch_distance\":" << maximum_distance;
    if (maximum_witness_state >= 0) {
        const auto [root, target] =
            decode_pair(edges, maximum_witness_pair);
        std::cout
            << ",\"maximum_witness\":{\"state_hex\":\""
            << state_hex(states[maximum_witness_state])
            << "\",\"roots\":[" << root << ',' << target << "]}";
    } else {
        std::cout << ",\"maximum_witness\":null";
    }
    std::cout << "}\n";
    return true;
}

int main(int argc, char** argv) {
    int depth_limit = 64;
    if (argc == 3 && std::string(argv[1]) == "--depth") {
        depth_limit = std::stoi(argv[2]);
    } else if (argc != 1) {
        throw std::runtime_error(
            "usage: audit_d5_root_switch_distance [--depth N]"
        );
    }

    std::string graph6;
    int graph_index = 0;
    while (std::getline(std::cin, graph6)) {
        if (graph6.empty()) continue;
        ++graph_index;
        if (!audit_graph(graph6, graph_index, depth_limit)) return 1;
    }
    std::cout
        << "{\"status\":\"PASS\",\"graphs\":" << graph_index << "}\n";
    return 0;
}
