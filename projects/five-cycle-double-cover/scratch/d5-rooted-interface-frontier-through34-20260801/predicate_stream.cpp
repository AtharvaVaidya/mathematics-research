#define main typed_cap_original_main
#include "../d5-typed-cap-double-star-frontier-20260731/audit_d5_typed_cap_ports.cpp"
#undef main

#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <unordered_set>

namespace {

std::string state_hex(const State& state) {
    std::ostringstream out;
    out << std::hex << std::setfill('0');
    for (unsigned char value : state) out << std::setw(2) << static_cast<int>(value);
    return out.str();
}

struct StreamingSearch {
    Audit audit;
    const int n;
    const int m;
    std::vector<unsigned char> proper;
    std::vector<unsigned char> aggregate_masks;
    std::vector<unsigned char> aggregate_external_ports;
    std::vector<unsigned char> double_star_good;
    std::vector<unsigned char> aggregate_good;
    std::vector<unsigned char> simultaneous_good;
    std::vector<std::array<int, 6>> bit_provider;
    std::vector<int> simultaneous_provider;
    std::vector<State> all_states;
    std::vector<State> certificate_states;
    long long proper_count = 0;
    long long double_star_count = 0;
    long long aggregate_count = 0;
    long long simultaneous_count = 0;
    long long raw_leaves = 0;
    long long flows_mod_s5 = 0;
    std::unordered_set<State> seen;

    explicit StreamingSearch(Graph graph)
        : audit(std::move(graph)), n(audit.graph.n),
          m(static_cast<int>(audit.graph.edges.size())),
          proper(n * m, 0), aggregate_masks(n * m, 0),
          aggregate_external_ports(n * m, 0), double_star_good(n * m, 0),
          aggregate_good(n * m, 0), simultaneous_good(n * m, 0),
          bit_provider(n * m), simultaneous_provider(n * m, -1) {
        for (auto& providers : bit_provider) providers.fill(-1);
        for (int z = 0; z < n; ++z) {
            for (int root = 0; root < m; ++root) {
                if (audit.graph.edges[root].first == z ||
                    audit.graph.edges[root].second == z) continue;
                proper[z * m + root] = 1;
                ++proper_count;
            }
        }
    }

    bool done() const {
        return double_star_count == proper_count &&
               aggregate_count == proper_count &&
               simultaneous_count == proper_count;
    }

    // The first assigned edge is fixed to label 01.  Quotient only by the
    // stabilizer of 01 so that no orbit representative is lost.
    State canonical_fixed_first(const State& state) const {
        State best;
        bool first = true;
        for (int p = 0; p < 120; ++p) {
            if (audit.permuted[p][LABELS[0]] != LABELS[0]) continue;
            State candidate(state.size(), '\0');
            for (int e = 0; e < static_cast<int>(state.size()); ++e) {
                candidate[e] = static_cast<char>(
                    audit.permuted[p][static_cast<unsigned char>(state[e])]);
            }
            if (first || candidate < best) {
                best = candidate;
                first = false;
            }
        }
        return best;
    }

    void process(const State& state, int state_index) {
        std::vector<unsigned char> external_ports(n * m, 0);
        std::vector<unsigned char> typed_masks(n * m, 0);

        for (unsigned char pair : LABELS) {
            for (const auto& component : audit.components(state, pair)) {
                std::vector<unsigned char> in(m, 0);
                for (int edge : component) in[edge] = 1;

                for (int z = 0; z < n; ++z) {
                    int slots[2] = {-1, -1};
                    int slot_count = 0;
                    int inactive = -1;
                    for (int slot = 0; slot < 3; ++slot) {
                        int edge = audit.graph.incidence[z][slot];
                        if (in[edge]) {
                            if (slot_count < 2) slots[slot_count] = slot;
                            ++slot_count;
                        } else {
                            inactive = slot;
                        }
                    }
                    if (slot_count != 2) continue;

                    unsigned char inactive_label = static_cast<unsigned char>(
                        state[audit.graph.incidence[z][inactive]]);
                    if (pair != inactive_label && (pair & inactive_label)) {
                        throw std::runtime_error("invalid inactive relation");
                    }

                    int physical = -1;
                    if (slots[0] == 0 && slots[1] == 1) physical = 0;
                    if (slots[0] == 0 && slots[1] == 2) physical = 1;
                    if (slots[0] == 1 && slots[1] == 2) physical = 2;
                    if (physical < 0) throw std::runtime_error("invalid port pair");
                    const int mode = pair == inactive_label ? 0 : 1;
                    const unsigned char physical_bits = static_cast<unsigned char>(
                        (1 << slots[0]) | (1 << slots[1]));

                    for (int root : component) {
                        const int index = z * m + root;
                        if (!proper[index]) continue;
                        typed_masks[index] |= static_cast<unsigned char>(
                            1 << (2 * physical + mode));
                        if (mode) external_ports[index] |= physical_bits;
                    }
                }
            }
        }

        for (int index = 0; index < n * m; ++index) {
            if (!proper[index]) continue;

            for (int bit = 0; bit < 6; ++bit) {
                if ((typed_masks[index] >> bit) & 1 &&
                    bit_provider[index][bit] < 0) {
                    bit_provider[index][bit] = state_index;
                }
            }
            aggregate_masks[index] |= typed_masks[index];
            aggregate_external_ports[index] |= external_ports[index];

            if (!double_star_good[index] &&
                contains_double_star(aggregate_masks[index])) {
                double_star_good[index] = 1;
                ++double_star_count;
            }
            if (!aggregate_good[index] &&
                aggregate_external_ports[index] == 7) {
                aggregate_good[index] = 1;
                ++aggregate_count;
            }
            if (!simultaneous_good[index] && external_ports[index] == 7) {
                simultaneous_good[index] = 1;
                ++simultaneous_count;
                simultaneous_provider[index] = state_index;
            }
        }
    }

    void build_certificate() {
        if (!done()) return;
        std::set<int> used;
        const std::array<std::array<int, 2>, 3> choices = {{{0, 1}, {0, 2}, {1, 2}}};
        for (int index = 0; index < n * m; ++index) {
            if (!proper[index]) continue;
            if (simultaneous_provider[index] < 0) {
                throw std::runtime_error("missing simultaneous provider");
            }
            used.insert(simultaneous_provider[index]);
            bool found = false;
            for (const auto& choice : choices) {
                bool available = true;
                for (int physical : choice) {
                    for (int mode = 0; mode < 2; ++mode) {
                        available &= bit_provider[index][2 * physical + mode] >= 0;
                    }
                }
                if (!available) continue;
                for (int physical : choice) {
                    for (int mode = 0; mode < 2; ++mode) {
                        used.insert(bit_provider[index][2 * physical + mode]);
                    }
                }
                found = true;
                break;
            }
            if (!found) throw std::runtime_error("missing double-star providers");
        }
        for (int state_index : used) certificate_states.push_back(all_states[state_index]);
    }

    void visit(State& state) {
        if (done()) return;

        // A frontier-first edge choice makes xor propagation effective.
        int edge = -1;
        int best_score = -1;
        for (int e = 0; e < m; ++e) {
            if (state[e]) continue;
            int score = 0;
            for (int vertex : {audit.graph.edges[e].first,
                               audit.graph.edges[e].second}) {
                for (int incident : audit.graph.incidence[vertex]) {
                    score += state[incident] != 0;
                }
            }
            if (score > best_score) {
                edge = e;
                best_score = score;
            }
        }

        if (edge < 0) {
            ++raw_leaves;
            State canonical = canonical_fixed_first(state);
            if (seen.insert(canonical).second) {
                ++flows_mod_s5;
                all_states.push_back(canonical);
                process(canonical, static_cast<int>(all_states.size()) - 1);
            }
            return;
        }

        const bool empty = std::all_of(
            state.begin(), state.end(), [](char value) { return value == 0; });
        const int choices = empty ? 1 : 10;
        for (int i = 0; i < choices && !done(); ++i) {
            std::vector<int> trail;
            if (audit.assign(state, edge, LABELS[i], trail)) visit(state);
            for (auto it = trail.rbegin(); it != trail.rend(); ++it) {
                state[*it] = 0;
            }
        }
    }

    void run() {
        State state(m, '\0');
        visit(state);
        build_certificate();
    }
};

} // namespace

int main(int argc, char** argv) {
    if (argc != 3 || std::string(argv[1]) != "--witnesses") {
        std::cerr << "usage: predicate_stream --witnesses OUTPUT.tsv\n";
        return 64;
    }
    std::ofstream certificate(argv[2]);
    if (!certificate) {
        std::cerr << "cannot open witness output\n";
        return 74;
    }
    certificate << "D5_ROOTED_INTERFACE_WITNESSES_V1\n";

    std::string row;
    long long graphs = 0;
    long long interfaces = 0;
    long long double_star = 0;
    long long aggregate = 0;
    long long simultaneous = 0;
    long long raw = 0;
    long long unique = 0;
    long long witness_states = 0;
    long long max_unique = 0;

    while (std::cin >> row) {
        if (!row.empty() && row[0] == '>') continue;
        StreamingSearch search(decode_graph6(row));
        search.run();
        ++graphs;
        interfaces += search.proper_count;
        double_star += search.double_star_count;
        aggregate += search.aggregate_count;
        simultaneous += search.simultaneous_count;
        raw += search.raw_leaves;
        unique += search.flows_mod_s5;
        witness_states += static_cast<long long>(search.certificate_states.size());
        max_unique = std::max(max_unique, search.flows_mod_s5);

        certificate << "G\t" << graphs << "\t" << row << "\t"
                    << search.n << "\t" << search.m << "\t"
                    << search.proper_count << "\t"
                    << search.certificate_states.size() << "\n";
        for (const State& state : search.certificate_states) {
            certificate << "F\t" << state_hex(state) << "\n";
        }

        if (!search.done()) {
            for (int index = 0; index < search.n * search.m; ++index) {
                if (!search.proper[index]) continue;
                if (search.double_star_good[index] &&
                    search.aggregate_good[index] &&
                    search.simultaneous_good[index]) continue;
                std::cout << "FAIL graph6=" << row
                          << " z=" << index / search.m
                          << " root=" << index % search.m
                          << " typed_mask="
                          << static_cast<int>(search.aggregate_masks[index])
                          << " external_ports="
                          << static_cast<int>(
                                 search.aggregate_external_ports[index])
                          << " double_star="
                          << static_cast<int>(search.double_star_good[index])
                          << " aggregate="
                          << static_cast<int>(search.aggregate_good[index])
                          << " simultaneous="
                          << static_cast<int>(search.simultaneous_good[index])
                          << "\n";
            }
        }
    }

    std::cout << "STREAM graphs=" << graphs
              << " raw_leaves=" << raw
              << " flows_mod_s5_until_cover=" << unique
              << " max_flows_graph=" << max_unique
              << " witness_states=" << witness_states
              << " interfaces=" << interfaces
              << " double_star=" << double_star
              << " aggregate_external=" << aggregate
              << " simultaneous_external=" << simultaneous << "\n";
    return interfaces == double_star && interfaces == aggregate &&
                   interfaces == simultaneous
               ? 0
               : 2;
}
