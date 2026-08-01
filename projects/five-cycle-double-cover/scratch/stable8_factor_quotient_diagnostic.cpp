// Exact factor-quotient diagnostic for the retained order-60 stable-eight core.
//
// This program is intentionally self-contained.  It:
//   * reconstructs the graph from graph6 and verifies a fixed all-c-mark
//     Tait colouring;
//   * expands the first terminal pairing and builds the lifted ac 2-factor;
//   * contracts that factor and counts every ordered pair of edge-disjoint
//     quotient T-joins;
//   * tests exact simultaneous liftability through the cyclic factor ports;
//   * mines a smallest globally realizable local interlacing obstruction;
//   * independently enumerates all 2^23 binary core cycles containing the
//     eight marks and checks the even-marked-component criterion; and
//   * enumerates all Tait colourings with all marks fixed to c.
//
// The output is a finite diagnostic, not a five-cycle-double-cover result.

#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <regex>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

using std::array;
using std::bitset;
using std::map;
using std::pair;
using std::string;
using std::tuple;
using std::uint64_t;
using std::vector;

namespace {

constexpr int CORE_N = 60;
constexpr int CORE_M = 90;
constexpr int QUOTIENT_M = 30;
constexpr int MAX_FACTORS = 8;

const string GRAPH6 =
    "{??????O@?B?D?EGGSAK?H_?HG?Ao@A_??????????????C?G?C???M???B_???["
    "???????????????????O?C??C????B_????M?????[_???????????????????????"
    "C??_???O?????B_?????B_?????@q?????????????????????????????C???G???"
    "C???????M???????B_???????[_??????????????????????????????????O????G"
    "???C????????B_????????M?????????[";

const array<pair<int, int>, 8> MARKS = {{
    {3, 11}, {6, 15}, {7, 18}, {22, 26},
    {30, 34}, {38, 42}, {46, 50}, {54, 58},
}};

// Produced deterministically by the exact DSATUR routine in
// tools/marked_core_exact_pair_search.py followed, in mark order, by the
// unique bichromatic Kempe switch that changes each remaining mark to c.
// Colours are 1=a, 2=b, 3=c.
const array<int, CORE_M> ALL_C_COLOURS = {{
    3,2,1,1,3,2,3,2,1,3,1,2,2,1,3,2,1,3,2,3,1,1,3,2,3,1,2,2,3,2,
    1,1,3,1,3,2,3,2,1,1,3,2,2,3,1,3,2,1,2,3,1,1,3,2,2,1,3,2,1,1,
    3,2,2,3,1,1,3,2,3,1,1,3,2,2,3,1,1,2,3,3,2,2,3,1,1,3,2,2,1,3,
}};

const array<pair<int, int>, 4> FIRST_PAIRING = {{
    {0, 1}, {2, 3}, {4, 5}, {6, 7},
}};

struct CoreEdge {
    int u;
    int v;
    int colour;
};

struct QuotientEdge {
    int factor_u;
    int factor_v;
    int core_edge;
    int core_u;
    int core_v;
};

struct Factor {
    vector<int> core_vertices;
    vector<int> core_factor_edges;
    int mark_index = -1;
    int terminal = -1;
    // One entry for each vertex of the lifted factor circuit.  An old core
    // vertex carries the id of its incident b-edge; the new terminal is -1.
    vector<int> cyclic_ports;
    vector<int> nonloops;
    vector<int> loops;
};

struct LocalEvaluation {
    bool parity_ok = false;
    bool obstruction = false;
    array<int, 4> state_class_counts = {{0, 0, 0, 0}};
    vector<int> demand_one_positions;
    vector<int> demand_two_positions;
};

struct LocalTable {
    vector<int> nonloops;
    vector<int> loops;
    vector<array<uint64_t, 2>> counts;
    vector<array<int, 2>> witness_loop_code;
};

struct BranchMessage {
    vector<int> vertices;
    int vertex_mask = 0;
    vector<int> boundary_edges;
    vector<int> variable_edges;
    vector<array<uint64_t, 1 << MAX_FACTORS>> counts;
    vector<array<int64_t, 1 << MAX_FACTORS>> witness_variable_code;
};

void require(bool condition, const string& message) {
    if (!condition) {
        throw std::runtime_error(message);
    }
}

uint64_t pow3(int exponent) {
    uint64_t value = 1;
    for (int i = 0; i < exponent; ++i) {
        value *= 3;
    }
    return value;
}

vector<int> ternary_digits(uint64_t code, int width) {
    vector<int> result(width, 0);
    for (int index = 0; index < width; ++index) {
        result[index] = static_cast<int>(code % 3);
        code /= 3;
    }
    return result;
}

string json_escape(const string& text) {
    std::ostringstream out;
    for (char character : text) {
        switch (character) {
            case '\\': out << "\\\\"; break;
            case '"': out << "\\\""; break;
            case '\n': out << "\\n"; break;
            case '\r': out << "\\r"; break;
            case '\t': out << "\\t"; break;
            default: out << character;
        }
    }
    return out.str();
}

vector<pair<int, int>> decode_graph6(const string& text) {
    require(!text.empty(), "empty graph6");
    vector<int> values;
    for (char character : text) {
        values.push_back(static_cast<unsigned char>(character) - 63);
    }
    require(values[0] == CORE_N, "unexpected graph6 order");
    vector<int> bits;
    for (std::size_t index = 1; index < values.size(); ++index) {
        require(values[index] >= 0 && values[index] < 64, "invalid graph6");
        for (int shift = 5; shift >= 0; --shift) {
            bits.push_back((values[index] >> shift) & 1);
        }
    }
    vector<pair<int, int>> edges;
    int position = 0;
    for (int upper = 1; upper < CORE_N; ++upper) {
        for (int lower = 0; lower < upper; ++lower) {
            require(position < static_cast<int>(bits.size()), "short graph6");
            if (bits[position]) {
                edges.push_back({lower, upper});
            }
            ++position;
        }
    }
    std::sort(edges.begin(), edges.end());
    require(edges.size() == CORE_M, "unexpected core edge count");
    return edges;
}

int other_end(const CoreEdge& edge, int vertex) {
    require(edge.u == vertex || edge.v == vertex, "nonincident edge");
    return edge.u == vertex ? edge.v : edge.u;
}

vector<CoreEdge> build_core() {
    vector<pair<int, int>> ends = decode_graph6(GRAPH6);
    vector<CoreEdge> edges;
    for (int edge = 0; edge < CORE_M; ++edge) {
        edges.push_back({ends[edge].first, ends[edge].second, ALL_C_COLOURS[edge]});
    }
    vector<array<int, 4>> colour_degree(CORE_N);
    for (auto& row : colour_degree) {
        row.fill(0);
    }
    for (const auto& edge : edges) {
        require(1 <= edge.colour && edge.colour <= 3, "invalid colour");
        ++colour_degree[edge.u][edge.colour];
        ++colour_degree[edge.v][edge.colour];
    }
    for (int vertex = 0; vertex < CORE_N; ++vertex) {
        for (int colour = 1; colour <= 3; ++colour) {
            require(colour_degree[vertex][colour] == 1,
                    "fixed edge colouring is not proper");
        }
    }
    for (const auto& mark : MARKS) {
        auto iterator = std::lower_bound(
            ends.begin(), ends.end(), pair<int, int>{std::min(mark.first, mark.second),
                                                     std::max(mark.first, mark.second)});
        require(iterator != ends.end() && *iterator == mark, "missing mark");
        int edge = static_cast<int>(iterator - ends.begin());
        require(edges[edge].colour == 3, "a mark is not coloured c");
    }
    return edges;
}

vector<int> mark_edge_ids(const vector<CoreEdge>& edges) {
    vector<int> ids;
    for (const auto& mark : MARKS) {
        int found = -1;
        for (int edge = 0; edge < CORE_M; ++edge) {
            if (pair<int, int>{edges[edge].u, edges[edge].v} == mark) {
                found = edge;
                break;
            }
        }
        require(found >= 0, "mark edge lookup failed");
        ids.push_back(found);
    }
    return ids;
}

struct QuotientConstruction {
    vector<Factor> factors;
    vector<QuotientEdge> quotient_edges;
    vector<int> vertex_factor;
    vector<int> vertex_b_edge;
    vector<int> mark_ids;
};

struct AmbientValidation {
    int vertices = 0;
    int edges = 0;
    int graph_minus_matching_edges = 0;
    int lifted_factor_edges = 0;
    bool simple = false;
    bool cubic = false;
    bool connected = false;
    bool matching_is_matching = false;
    bool lifted_factor_is_spanning_two_factor = false;
};

AmbientValidation validate_ambient_expansion(
    const vector<CoreEdge>& edges,
    const QuotientConstruction& construction
) {
    std::set<pair<int, int>> ambient_set;
    std::set<int> mark_set(
        construction.mark_ids.begin(), construction.mark_ids.end());
    std::set<pair<int, int>> pairing_set;
    for (int edge = 0; edge < CORE_M; ++edge) {
        if (!mark_set.count(edge)) {
            ambient_set.insert({edges[edge].u, edges[edge].v});
        }
    }
    for (int mark = 0; mark < 8; ++mark) {
        int edge = construction.mark_ids[mark];
        int terminal = CORE_N + mark;
        ambient_set.insert({
            std::min(edges[edge].u, terminal),
            std::max(edges[edge].u, terminal),
        });
        ambient_set.insert({
            std::min(edges[edge].v, terminal),
            std::max(edges[edge].v, terminal),
        });
    }
    for (const auto& pair_row : FIRST_PAIRING) {
        pair<int, int> pairing_edge = {
            CORE_N + pair_row.first,
            CORE_N + pair_row.second,
        };
        pairing_set.insert(pairing_edge);
        ambient_set.insert(pairing_edge);
    }
    vector<pair<int, int>> ambient_edges(ambient_set.begin(), ambient_set.end());
    vector<vector<int>> adjacency(CORE_N + 8);
    for (int edge = 0; edge < static_cast<int>(ambient_edges.size()); ++edge) {
        adjacency[ambient_edges[edge].first].push_back(edge);
        adjacency[ambient_edges[edge].second].push_back(edge);
    }
    bool cubic = std::all_of(
        adjacency.begin(), adjacency.end(),
        [](const vector<int>& row) { return row.size() == 3; });
    vector<int> seen(CORE_N + 8, 0);
    std::queue<int> queue;
    queue.push(0);
    seen[0] = 1;
    while (!queue.empty()) {
        int vertex = queue.front();
        queue.pop();
        for (int edge : adjacency[vertex]) {
            int other = ambient_edges[edge].first == vertex
                ? ambient_edges[edge].second
                : ambient_edges[edge].first;
            if (!seen[other]) {
                seen[other] = 1;
                queue.push(other);
            }
        }
    }

    std::set<pair<int, int>> lifted_factor;
    for (int edge = 0; edge < CORE_M; ++edge) {
        if (edges[edge].colour != 1 && edges[edge].colour != 3) {
            continue;
        }
        auto mark_iterator =
            std::find(construction.mark_ids.begin(),
                      construction.mark_ids.end(), edge);
        if (mark_iterator == construction.mark_ids.end()) {
            lifted_factor.insert({edges[edge].u, edges[edge].v});
        } else {
            int mark = static_cast<int>(
                mark_iterator - construction.mark_ids.begin());
            int terminal = CORE_N + mark;
            lifted_factor.insert({
                std::min(edges[edge].u, terminal),
                std::max(edges[edge].u, terminal),
            });
            lifted_factor.insert({
                std::min(edges[edge].v, terminal),
                std::max(edges[edge].v, terminal),
            });
        }
    }
    vector<int> factor_degree(CORE_N + 8, 0);
    for (const auto& edge : lifted_factor) {
        ++factor_degree[edge.first];
        ++factor_degree[edge.second];
    }
    bool two_factor = std::all_of(
        factor_degree.begin(), factor_degree.end(),
        [](int degree) { return degree == 2; });

    AmbientValidation result;
    result.vertices = CORE_N + 8;
    result.edges = static_cast<int>(ambient_edges.size());
    result.graph_minus_matching_edges =
        result.edges - static_cast<int>(pairing_set.size());
    result.lifted_factor_edges = static_cast<int>(lifted_factor.size());
    result.simple = ambient_set.size() == 102 &&
        std::all_of(
            ambient_edges.begin(), ambient_edges.end(),
            [](const pair<int, int>& edge) { return edge.first != edge.second; });
    result.cubic = cubic;
    result.connected =
        std::all_of(seen.begin(), seen.end(), [](int value) { return value; });
    std::set<int> paired_terminals;
    for (const auto& edge : pairing_set) {
        paired_terminals.insert(edge.first);
        paired_terminals.insert(edge.second);
    }
    result.matching_is_matching =
        pairing_set.size() == 4 && paired_terminals.size() == 8;
    result.lifted_factor_is_spanning_two_factor = two_factor;
    require(result.edges == 102, "bad ambient edge count");
    require(result.graph_minus_matching_edges == 98, "bad G-M edge count");
    require(result.lifted_factor_edges == 68, "bad lifted factor edge count");
    require(result.simple && result.cubic && result.connected,
            "ambient expansion premise failed");
    require(result.matching_is_matching, "pairing edges are not a matching");
    require(result.lifted_factor_is_spanning_two_factor,
            "lifted ac system is not a spanning 2-factor of G-M");
    return result;
}

QuotientConstruction build_quotient(const vector<CoreEdge>& edges) {
    vector<vector<int>> factor_incidence(CORE_N);
    vector<int> vertex_b_edge(CORE_N, -1);
    for (int edge = 0; edge < CORE_M; ++edge) {
        if (edges[edge].colour == 1 || edges[edge].colour == 3) {
            factor_incidence[edges[edge].u].push_back(edge);
            factor_incidence[edges[edge].v].push_back(edge);
        } else {
            require(vertex_b_edge[edges[edge].u] == -1 &&
                    vertex_b_edge[edges[edge].v] == -1,
                    "duplicate b-edge at vertex");
            vertex_b_edge[edges[edge].u] = edge;
            vertex_b_edge[edges[edge].v] = edge;
        }
    }
    for (int vertex = 0; vertex < CORE_N; ++vertex) {
        require(factor_incidence[vertex].size() == 2, "ac factor is not degree two");
        require(vertex_b_edge[vertex] >= 0, "missing b-edge");
    }

    vector<int> vertex_factor(CORE_N, -1);
    vector<Factor> factors;
    for (int start = 0; start < CORE_N; ++start) {
        if (vertex_factor[start] >= 0) {
            continue;
        }
        Factor factor;
        int current = start;
        int previous_edge = -1;
        while (true) {
            require(vertex_factor[current] == -1 || current == start,
                    "factor traversal repeated a vertex");
            if (current == start && !factor.core_vertices.empty()) {
                break;
            }
            vertex_factor[current] = static_cast<int>(factors.size());
            factor.core_vertices.push_back(current);
            int next_edge;
            if (previous_edge == -1) {
                next_edge = std::min(factor_incidence[current][0],
                                     factor_incidence[current][1]);
            } else {
                next_edge = factor_incidence[current][0] == previous_edge
                    ? factor_incidence[current][1]
                    : factor_incidence[current][0];
            }
            factor.core_factor_edges.push_back(next_edge);
            int next = other_end(edges[next_edge], current);
            previous_edge = next_edge;
            current = next;
        }
        require(factor.core_vertices.size() == factor.core_factor_edges.size(),
                "factor order mismatch");
        factors.push_back(factor);
    }
    require(factors.size() == 8, "expected exactly eight ac factor circuits");

    vector<QuotientEdge> quotient_edges;
    vector<int> core_b_to_quotient(CORE_M, -1);
    for (int edge = 0; edge < CORE_M; ++edge) {
        if (edges[edge].colour != 2) {
            continue;
        }
        core_b_to_quotient[edge] = static_cast<int>(quotient_edges.size());
        quotient_edges.push_back({
            vertex_factor[edges[edge].u],
            vertex_factor[edges[edge].v],
            edge,
            edges[edge].u,
            edges[edge].v,
        });
    }
    require(quotient_edges.size() == QUOTIENT_M, "unexpected quotient edge count");

    vector<int> marks = mark_edge_ids(edges);
    for (int mark = 0; mark < 8; ++mark) {
        int factor_id = vertex_factor[edges[marks[mark]].u];
        require(vertex_factor[edges[marks[mark]].v] == factor_id,
                "mark is not in one factor");
        require(factors[factor_id].mark_index == -1,
                "two marks lie on one ac factor circuit");
        factors[factor_id].mark_index = mark;
        factors[factor_id].terminal = CORE_N + mark;
    }
    for (auto& factor : factors) {
        require(factor.mark_index >= 0, "unmarked ac factor circuit");
        for (std::size_t position = 0; position < factor.core_vertices.size();
             ++position) {
            int vertex = factor.core_vertices[position];
            int b_edge = vertex_b_edge[vertex];
            int qedge = core_b_to_quotient[b_edge];
            require(qedge >= 0, "b-edge quotient lookup failed");
            factor.cyclic_ports.push_back(qedge);
            int factor_edge = factor.core_factor_edges[position];
            if (factor_edge == marks[factor.mark_index]) {
                factor.cyclic_ports.push_back(-1);
            }
        }
        require(factor.cyclic_ports.size() == factor.core_vertices.size() + 1,
                "the lifted factor should contain one terminal");
    }

    for (int factor_id = 0; factor_id < static_cast<int>(factors.size());
         ++factor_id) {
        for (int qedge = 0; qedge < QUOTIENT_M; ++qedge) {
            const auto& edge = quotient_edges[qedge];
            if (edge.factor_u == factor_id && edge.factor_v == factor_id) {
                factors[factor_id].loops.push_back(qedge);
            } else if (edge.factor_u == factor_id || edge.factor_v == factor_id) {
                factors[factor_id].nonloops.push_back(qedge);
            }
        }
        std::sort(factors[factor_id].loops.begin(), factors[factor_id].loops.end());
        std::sort(factors[factor_id].nonloops.begin(),
                  factors[factor_id].nonloops.end());
    }

    return {factors, quotient_edges, vertex_factor, vertex_b_edge, marks};
}

LocalEvaluation evaluate_local(
    const Factor& factor,
    const vector<int>& quotient_states
) {
    LocalEvaluation result;
    int length = static_cast<int>(factor.cyclic_ports.size());
    vector<int> demand_one(length, 0);
    vector<int> demand_two(length, 0);
    for (int position = 0; position < length; ++position) {
        int qedge = factor.cyclic_ports[position];
        if (qedge < 0) {
            demand_one[position] = 1;
            demand_two[position] = 1;
        } else {
            demand_one[position] = quotient_states[qedge] == 1;
            demand_two[position] = quotient_states[qedge] == 2;
        }
        if (demand_one[position]) {
            result.demand_one_positions.push_back(position);
        }
        if (demand_two[position]) {
            result.demand_two_positions.push_back(position);
        }
    }
    int parity_one = std::accumulate(demand_one.begin(), demand_one.end(), 0) & 1;
    int parity_two = std::accumulate(demand_two.begin(), demand_two.end(), 0) & 1;
    if (parity_one || parity_two) {
        return result;
    }
    result.parity_ok = true;

    vector<int> path_one(length, 0);
    vector<int> path_two(length, 0);
    // Fix the last cycle edge absent.  The complementary solution is the
    // other possible parity path on the circuit.
    path_one[length - 1] = 0;
    path_two[length - 1] = 0;
    for (int position = 0; position + 1 < length; ++position) {
        int previous_one = position == 0 ? path_one[length - 1]
                                         : path_one[position - 1];
        int previous_two = position == 0 ? path_two[length - 1]
                                         : path_two[position - 1];
        path_one[position] = previous_one ^ demand_one[position];
        path_two[position] = previous_two ^ demand_two[position];
    }
    require((path_one[length - 2] ^ path_one[length - 1]) ==
                demand_one[length - 1],
            "join-one parity-path closure failed");
    require((path_two[length - 2] ^ path_two[length - 1]) ==
                demand_two[length - 1],
            "join-two parity-path closure failed");

    for (int edge = 0; edge < length; ++edge) {
        int state_class = 2 * path_one[edge] + path_two[edge];
        ++result.state_class_counts[state_class];
    }
    result.obstruction = std::all_of(
        result.state_class_counts.begin(),
        result.state_class_counts.end(),
        [](int count) { return count > 0; });
    return result;
}

LocalTable build_local_table(
    int factor_id,
    const QuotientConstruction& construction
) {
    const Factor& factor = construction.factors[factor_id];
    LocalTable table;
    table.nonloops = factor.nonloops;
    table.loops = factor.loops;
    uint64_t nonloop_count = pow3(static_cast<int>(table.nonloops.size()));
    uint64_t loop_count = pow3(static_cast<int>(table.loops.size()));
    table.counts.resize(nonloop_count, array<uint64_t, 2>{{0, 0}});
    table.witness_loop_code.resize(nonloop_count, array<int, 2>{{-1, -1}});
    vector<int> states(QUOTIENT_M, 0);
    for (uint64_t nonloop_code = 0; nonloop_code < nonloop_count;
         ++nonloop_code) {
        vector<int> nonloop_digits =
            ternary_digits(nonloop_code, static_cast<int>(table.nonloops.size()));
        for (int index = 0; index < static_cast<int>(table.nonloops.size());
             ++index) {
            states[table.nonloops[index]] = nonloop_digits[index];
        }
        for (uint64_t loop_code = 0; loop_code < loop_count; ++loop_code) {
            vector<int> loop_digits =
                ternary_digits(loop_code, static_cast<int>(table.loops.size()));
            for (int index = 0; index < static_cast<int>(table.loops.size());
                 ++index) {
                states[table.loops[index]] = loop_digits[index];
            }
            LocalEvaluation evaluation =
                evaluate_local(construction.factors[factor_id], states);
            if (!evaluation.parity_ok) {
                continue;
            }
            int obstruction = evaluation.obstruction ? 1 : 0;
            ++table.counts[nonloop_code][obstruction];
            if (table.witness_loop_code[nonloop_code][obstruction] < 0) {
                table.witness_loop_code[nonloop_code][obstruction] =
                    static_cast<int>(loop_code);
            }
        }
    }
    return table;
}

uint64_t local_nonloop_code(
    const LocalTable& table,
    const vector<int>& states
) {
    uint64_t code = 0;
    uint64_t place = 1;
    for (int qedge : table.nonloops) {
        code += place * states[qedge];
        place *= 3;
    }
    return code;
}

vector<vector<int>> components_without_central(
    int central,
    const QuotientConstruction& construction
) {
    int factor_count = static_cast<int>(construction.factors.size());
    vector<vector<int>> adjacency(factor_count);
    for (const auto& edge : construction.quotient_edges) {
        if (edge.factor_u == edge.factor_v ||
            edge.factor_u == central || edge.factor_v == central) {
            continue;
        }
        adjacency[edge.factor_u].push_back(edge.factor_v);
        adjacency[edge.factor_v].push_back(edge.factor_u);
    }
    vector<int> seen(factor_count, 0);
    seen[central] = 1;
    vector<vector<int>> result;
    for (int root = 0; root < factor_count; ++root) {
        if (seen[root]) {
            continue;
        }
        vector<int> component;
        std::queue<int> queue;
        queue.push(root);
        seen[root] = 1;
        while (!queue.empty()) {
            int vertex = queue.front();
            queue.pop();
            component.push_back(vertex);
            for (int other : adjacency[vertex]) {
                if (!seen[other]) {
                    seen[other] = 1;
                    queue.push(other);
                }
            }
        }
        std::sort(component.begin(), component.end());
        result.push_back(component);
    }
    std::sort(result.begin(), result.end());
    return result;
}

BranchMessage build_branch_message(
    int central,
    const vector<int>& branch_vertices,
    const QuotientConstruction& construction,
    const vector<LocalTable>& local_tables
) {
    BranchMessage message;
    message.vertices = branch_vertices;
    std::set<int> branch_set(branch_vertices.begin(), branch_vertices.end());
    for (int vertex : branch_vertices) {
        message.vertex_mask |= 1 << vertex;
    }
    for (int qedge = 0; qedge < QUOTIENT_M; ++qedge) {
        const auto& edge = construction.quotient_edges[qedge];
        bool in_u = branch_set.count(edge.factor_u);
        bool in_v = branch_set.count(edge.factor_v);
        if ((edge.factor_u == central && in_v) ||
            (edge.factor_v == central && in_u)) {
            message.boundary_edges.push_back(qedge);
            message.variable_edges.push_back(qedge);
        } else if (in_u && in_v && edge.factor_u != edge.factor_v) {
            message.variable_edges.push_back(qedge);
        }
    }
    std::sort(message.boundary_edges.begin(), message.boundary_edges.end());
    std::sort(message.variable_edges.begin(), message.variable_edges.end());
    message.variable_edges.erase(
        std::unique(message.variable_edges.begin(), message.variable_edges.end()),
        message.variable_edges.end());

    uint64_t boundary_count =
        pow3(static_cast<int>(message.boundary_edges.size()));
    uint64_t variable_count =
        pow3(static_cast<int>(message.variable_edges.size()));
    message.counts.resize(boundary_count);
    message.witness_variable_code.resize(boundary_count);
    for (uint64_t code = 0; code < boundary_count; ++code) {
        message.counts[code].fill(0);
        message.witness_variable_code[code].fill(-1);
    }

    vector<int> states(QUOTIENT_M, 0);
    for (uint64_t variable_code = 0; variable_code < variable_count;
         ++variable_code) {
        vector<int> digits = ternary_digits(
            variable_code, static_cast<int>(message.variable_edges.size()));
        for (int index = 0; index < static_cast<int>(message.variable_edges.size());
             ++index) {
            states[message.variable_edges[index]] = digits[index];
        }
        uint64_t boundary_code = 0;
        uint64_t place = 1;
        for (int qedge : message.boundary_edges) {
            boundary_code += place * states[qedge];
            place *= 3;
        }

        array<uint64_t, 1 << MAX_FACTORS> distribution{};
        distribution.fill(0);
        distribution[0] = 1;
        for (int vertex : branch_vertices) {
            uint64_t code = local_nonloop_code(local_tables[vertex], states);
            array<uint64_t, 1 << MAX_FACTORS> next{};
            next.fill(0);
            for (int mask = 0; mask < (1 << MAX_FACTORS); ++mask) {
                if (!distribution[mask]) {
                    continue;
                }
                for (int obstruction = 0; obstruction <= 1; ++obstruction) {
                    uint64_t count =
                        local_tables[vertex].counts[code][obstruction];
                    if (!count) {
                        continue;
                    }
                    int next_mask = mask |
                        (obstruction ? (1 << vertex) : 0);
                    next[next_mask] += distribution[mask] * count;
                }
            }
            distribution = next;
        }
        for (int mask = 0; mask < (1 << MAX_FACTORS); ++mask) {
            if (!distribution[mask]) {
                continue;
            }
            message.counts[boundary_code][mask] += distribution[mask];
            if (message.witness_variable_code[boundary_code][mask] < 0) {
                message.witness_variable_code[boundary_code][mask] =
                    static_cast<int64_t>(variable_code);
            }
        }
    }
    return message;
}

uint64_t boundary_code_for(
    const BranchMessage& message,
    const vector<int>& states
) {
    uint64_t code = 0;
    uint64_t place = 1;
    for (int qedge : message.boundary_edges) {
        code += place * states[qedge];
        place *= 3;
    }
    return code;
}

void fill_branch_witness(
    const BranchMessage& message,
    int branch_mask,
    uint64_t boundary_code,
    const vector<LocalTable>& local_tables,
    vector<int>& states
) {
    int64_t variable_code =
        message.witness_variable_code[boundary_code][branch_mask];
    require(variable_code >= 0, "missing branch witness");
    vector<int> digits = ternary_digits(
        static_cast<uint64_t>(variable_code),
        static_cast<int>(message.variable_edges.size()));
    for (int index = 0; index < static_cast<int>(message.variable_edges.size());
         ++index) {
        int qedge = message.variable_edges[index];
        if (std::find(message.boundary_edges.begin(),
                      message.boundary_edges.end(), qedge) !=
                message.boundary_edges.end()) {
            require(states[qedge] == digits[index],
                    "branch witness disagrees on boundary");
        }
        states[qedge] = digits[index];
    }
    for (int vertex : message.vertices) {
        uint64_t nonloop_code =
            local_nonloop_code(local_tables[vertex], states);
        int obstruction = (branch_mask >> vertex) & 1;
        int loop_code =
            local_tables[vertex].witness_loop_code[nonloop_code][obstruction];
        require(loop_code >= 0, "missing local loop witness");
        vector<int> loop_digits = ternary_digits(
            static_cast<uint64_t>(loop_code),
            static_cast<int>(local_tables[vertex].loops.size()));
        for (int index = 0;
             index < static_cast<int>(local_tables[vertex].loops.size());
             ++index) {
            states[local_tables[vertex].loops[index]] = loop_digits[index];
        }
    }
}

struct QuotientCountResult {
    int central = -1;
    vector<BranchMessage> branches;
    array<uint64_t, 1 << MAX_FACTORS> obstruction_histogram{};
    array<vector<int>, 1 << MAX_FACTORS> witnesses;
};

QuotientCountResult count_quotient_pairs(
    const QuotientConstruction& construction
) {
    QuotientCountResult result;
    int central = 0;
    for (int factor = 1;
         factor < static_cast<int>(construction.factors.size()); ++factor) {
        if (construction.factors[factor].nonloops.size() >
            construction.factors[central].nonloops.size()) {
            central = factor;
        }
    }
    result.central = central;
    require(construction.factors[central].loops.empty(),
            "diagnostic expects a loopless maximum-degree central factor");

    vector<LocalTable> local_tables(construction.factors.size());
    for (int factor = 0; factor < static_cast<int>(construction.factors.size());
         ++factor) {
        if (factor != central) {
            local_tables[factor] = build_local_table(factor, construction);
        }
    }
    vector<vector<int>> branch_vertices =
        components_without_central(central, construction);
    for (const auto& vertices : branch_vertices) {
        result.branches.push_back(
            build_branch_message(
                central, vertices, construction, local_tables));
    }

    result.obstruction_histogram.fill(0);
    vector<int> central_edges = construction.factors[central].nonloops;
    uint64_t central_count = pow3(static_cast<int>(central_edges.size()));
    vector<int> states(QUOTIENT_M, 0);
    for (uint64_t central_code = 0; central_code < central_count;
         ++central_code) {
        vector<int> digits =
            ternary_digits(central_code, static_cast<int>(central_edges.size()));
        for (int index = 0; index < static_cast<int>(central_edges.size());
             ++index) {
            states[central_edges[index]] = digits[index];
        }
        LocalEvaluation central_evaluation =
            evaluate_local(construction.factors[central], states);
        if (!central_evaluation.parity_ok) {
            continue;
        }
        int central_mask =
            central_evaluation.obstruction ? (1 << central) : 0;

        vector<pair<int, uint64_t>> distribution = {{central_mask, 1}};
        vector<uint64_t> boundary_codes;
        for (const auto& branch : result.branches) {
            uint64_t boundary_code = boundary_code_for(branch, states);
            boundary_codes.push_back(boundary_code);
            vector<pair<int, uint64_t>> next;
            for (const auto& current : distribution) {
                for (int branch_mask = 0;
                     branch_mask < (1 << MAX_FACTORS); ++branch_mask) {
                    uint64_t count =
                        branch.counts[boundary_code][branch_mask];
                    if (!count) {
                        continue;
                    }
                    next.push_back({
                        current.first | branch_mask,
                        current.second * count,
                    });
                }
            }
            // Branch masks occupy disjoint vertex sets, so identical masks
            // can only arise from loop-state multiplicities already summed in
            // the message.  Coalesce defensively.
            map<int, uint64_t> coalesced;
            for (const auto& row : next) {
                coalesced[row.first] += row.second;
            }
            distribution.clear();
            for (const auto& row : coalesced) {
                distribution.push_back(row);
            }
        }
        for (const auto& row : distribution) {
            int mask = row.first;
            result.obstruction_histogram[mask] += row.second;
            if (result.witnesses[mask].empty()) {
                vector<int> witness = states;
                for (std::size_t index = 0; index < result.branches.size();
                     ++index) {
                    int branch_mask = mask & result.branches[index].vertex_mask;
                    fill_branch_witness(
                        result.branches[index],
                        branch_mask,
                        boundary_codes[index],
                        local_tables,
                        witness);
                }
                for (int factor = 0;
                     factor < static_cast<int>(construction.factors.size());
                     ++factor) {
                    LocalEvaluation check =
                        evaluate_local(construction.factors[factor], witness);
                    require(check.parity_ok, "stored witness violates quotient parity");
                    require(check.obstruction == (((mask >> factor) & 1) != 0),
                            "stored witness obstruction mask mismatch");
                }
                result.witnesses[mask] = witness;
            }
        }
    }
    return result;
}

string marked_profile_key(vector<int> counts) {
    std::sort(counts.begin(), counts.end());
    std::ostringstream out;
    for (std::size_t index = 0; index < counts.size(); ++index) {
        if (index) {
            out << "+";
        }
        out << counts[index];
    }
    return out.str();
}

struct DirectCycleResult {
    int equation_rank = 0;
    int dimension = 0;
    uint64_t enumerated = 0;
    uint64_t even_component_cycles = 0;
    map<string, uint64_t> marked_component_profiles;
};

struct IndependentQuotientPairResult {
    int equation_rank = 0;
    int affine_dimension = 0;
    uint64_t first_joins_enumerated = 0;
    uint64_t first_joins_with_t_even_complement = 0;
    uint64_t ordered_pairs = 0;
    map<int, uint64_t> complement_cycle_dimension_histogram;
};

IndependentQuotientPairResult independent_quotient_pair_count(
    const QuotientConstruction& construction
) {
    constexpr int VARIABLES = QUOTIENT_M;
    constexpr int RHS = QUOTIENT_M;
    vector<bitset<QUOTIENT_M + 1>> rows;
    for (int vertex = 0; vertex < MAX_FACTORS; ++vertex) {
        bitset<QUOTIENT_M + 1> row;
        for (int edge = 0; edge < QUOTIENT_M; ++edge) {
            int u = construction.quotient_edges[edge].factor_u;
            int v = construction.quotient_edges[edge].factor_v;
            // A quotient loop has two incidences and is zero in the binary
            // boundary operator.
            if (u != v && (u == vertex || v == vertex)) {
                row.flip(edge);
            }
        }
        row.set(RHS);  // every quotient vertex contains one terminal
        rows.push_back(row);
    }
    vector<int> pivots;
    int rank = 0;
    for (int column = 0; column < VARIABLES; ++column) {
        int selected = -1;
        for (int row = rank; row < static_cast<int>(rows.size()); ++row) {
            if (rows[row].test(column)) {
                selected = row;
                break;
            }
        }
        if (selected < 0) {
            continue;
        }
        std::swap(rows[rank], rows[selected]);
        for (int row = 0; row < static_cast<int>(rows.size()); ++row) {
            if (row != rank && rows[row].test(column)) {
                rows[row] ^= rows[rank];
            }
        }
        pivots.push_back(column);
        ++rank;
    }
    for (int row = rank; row < static_cast<int>(rows.size()); ++row) {
        bitset<QUOTIENT_M + 1> coefficients = rows[row];
        bool rhs = coefficients.test(RHS);
        coefficients.reset(RHS);
        require(coefficients.any() || !rhs,
                "quotient T-join equations are inconsistent");
    }
    vector<int> is_pivot(VARIABLES, 0);
    for (int pivot : pivots) {
        is_pivot[pivot] = 1;
    }
    vector<int> free_columns;
    for (int column = 0; column < VARIABLES; ++column) {
        if (!is_pivot[column]) {
            free_columns.push_back(column);
        }
    }
    require(free_columns.size() == 23,
            "unexpected quotient T-join affine dimension");
    bitset<QUOTIENT_M> current;
    for (int row = 0; row < rank; ++row) {
        if (rows[row].test(RHS)) {
            current.set(pivots[row]);
        }
    }
    vector<bitset<QUOTIENT_M>> null_basis;
    for (int free_column : free_columns) {
        bitset<QUOTIENT_M> vector;
        vector.set(free_column);
        for (int row = 0; row < rank; ++row) {
            if (rows[row].test(free_column)) {
                vector.set(pivots[row]);
            }
        }
        null_basis.push_back(vector);
    }

    IndependentQuotientPairResult result;
    result.equation_rank = rank;
    result.affine_dimension = static_cast<int>(free_columns.size());
    result.first_joins_enumerated = uint64_t{1} << result.affine_dimension;
    for (uint64_t assignment = 0;
         assignment < result.first_joins_enumerated; ++assignment) {
        if (assignment) {
            current ^= null_basis[__builtin_ctzll(assignment)];
        }
        array<int, MAX_FACTORS> parent;
        std::iota(parent.begin(), parent.end(), 0);
        auto find = [&](int vertex) {
            int root = vertex;
            while (parent[root] != root) {
                root = parent[root];
            }
            while (parent[vertex] != vertex) {
                int next = parent[vertex];
                parent[vertex] = root;
                vertex = next;
            }
            return root;
        };
        auto unite = [&](int first, int second) {
            int root_first = find(first);
            int root_second = find(second);
            if (root_first != root_second) {
                parent[root_second] = root_first;
            }
        };
        int remaining_edges = 0;
        for (int edge = 0; edge < QUOTIENT_M; ++edge) {
            if (current.test(edge)) {
                continue;
            }
            ++remaining_edges;
            int u = construction.quotient_edges[edge].factor_u;
            int v = construction.quotient_edges[edge].factor_v;
            if (u != v) {
                unite(u, v);
            }
        }
        array<int, MAX_FACTORS> component_sizes{};
        component_sizes.fill(0);
        for (int vertex = 0; vertex < MAX_FACTORS; ++vertex) {
            ++component_sizes[find(vertex)];
        }
        bool t_even = true;
        int components = 0;
        for (int root = 0; root < MAX_FACTORS; ++root) {
            if (!component_sizes[root]) {
                continue;
            }
            ++components;
            if (component_sizes[root] & 1) {
                t_even = false;
            }
        }
        if (!t_even) {
            continue;
        }
        ++result.first_joins_with_t_even_complement;
        int cycle_dimension = remaining_edges - MAX_FACTORS + components;
        require(cycle_dimension >= 0 && cycle_dimension < 63,
                "bad complement cycle dimension");
        ++result.complement_cycle_dimension_histogram[cycle_dimension];
        result.ordered_pairs += uint64_t{1} << cycle_dimension;
    }
    return result;
}

DirectCycleResult direct_cycle_enumeration(
    const vector<CoreEdge>& edges,
    const vector<int>& marks
) {
    constexpr int VARIABLES = CORE_M;
    constexpr int RHS = CORE_M;
    vector<bitset<CORE_M + 1>> rows;
    vector<vector<int>> incidence(CORE_N);
    for (int edge = 0; edge < CORE_M; ++edge) {
        incidence[edges[edge].u].push_back(edge);
        incidence[edges[edge].v].push_back(edge);
    }
    for (int vertex = 0; vertex < CORE_N; ++vertex) {
        bitset<CORE_M + 1> row;
        for (int edge : incidence[vertex]) {
            row.set(edge);
        }
        rows.push_back(row);
    }
    for (int mark : marks) {
        bitset<CORE_M + 1> row;
        row.set(mark);
        row.set(RHS);
        rows.push_back(row);
    }

    vector<int> pivots;
    int rank = 0;
    for (int column = 0; column < VARIABLES; ++column) {
        int selected = -1;
        for (int row = rank; row < static_cast<int>(rows.size()); ++row) {
            if (rows[row].test(column)) {
                selected = row;
                break;
            }
        }
        if (selected < 0) {
            continue;
        }
        std::swap(rows[rank], rows[selected]);
        for (int row = 0; row < static_cast<int>(rows.size()); ++row) {
            if (row != rank && rows[row].test(column)) {
                rows[row] ^= rows[rank];
            }
        }
        pivots.push_back(column);
        ++rank;
    }
    for (int row = rank; row < static_cast<int>(rows.size()); ++row) {
        bitset<CORE_M + 1> coefficients = rows[row];
        bool rhs = coefficients.test(RHS);
        coefficients.reset(RHS);
        require(coefficients.any() || !rhs, "inconsistent all-mark cycle system");
    }

    vector<int> is_pivot(VARIABLES, 0);
    for (int pivot : pivots) {
        is_pivot[pivot] = 1;
    }
    vector<int> free_columns;
    for (int column = 0; column < VARIABLES; ++column) {
        if (!is_pivot[column]) {
            free_columns.push_back(column);
        }
    }
    require(free_columns.size() == 23, "unexpected all-mark cycle dimension");

    bitset<CORE_M> current;
    for (int row = 0; row < rank; ++row) {
        if (rows[row].test(RHS)) {
            current.set(pivots[row]);
        }
    }
    vector<bitset<CORE_M>> null_basis;
    for (int free_column : free_columns) {
        bitset<CORE_M> vector;
        vector.set(free_column);
        for (int row = 0; row < rank; ++row) {
            if (rows[row].test(free_column)) {
                vector.set(pivots[row]);
            }
        }
        null_basis.push_back(vector);
    }

    std::set<int> mark_set(marks.begin(), marks.end());
    DirectCycleResult result;
    result.equation_rank = rank;
    result.dimension = static_cast<int>(free_columns.size());
    result.enumerated = uint64_t{1} << result.dimension;
    vector<int> visited(CORE_N, 0);
    for (uint64_t assignment = 0; assignment < result.enumerated; ++assignment) {
        if (assignment) {
            int toggled = __builtin_ctzll(assignment);
            current ^= null_basis[toggled];
        }
        std::fill(visited.begin(), visited.end(), 0);
        vector<int> marked_counts;
        bool all_even = true;
        for (int root = 0; root < CORE_N; ++root) {
            if (visited[root]) {
                continue;
            }
            int selected_degree = 0;
            for (int edge : incidence[root]) {
                selected_degree += current.test(edge);
            }
            require(selected_degree == 0 || selected_degree == 2,
                    "enumerated vector is not Eulerian");
            if (!selected_degree) {
                visited[root] = 1;
                continue;
            }
            int mark_count = 0;
            int current_vertex = root;
            int previous_edge = -1;
            while (true) {
                visited[current_vertex] = 1;
                int next_edge = -1;
                for (int edge : incidence[current_vertex]) {
                    if (edge != previous_edge && current.test(edge)) {
                        next_edge = edge;
                        break;
                    }
                }
                require(next_edge >= 0, "cycle traversal got stuck");
                if (mark_set.count(next_edge)) {
                    ++mark_count;
                }
                int next_vertex = other_end(edges[next_edge], current_vertex);
                previous_edge = next_edge;
                current_vertex = next_vertex;
                if (current_vertex == root) {
                    break;
                }
                require(!visited[current_vertex], "selected component is not a circuit");
            }
            if (mark_count) {
                marked_counts.push_back(mark_count);
                if (mark_count & 1) {
                    all_even = false;
                }
            }
        }
        require(std::accumulate(marked_counts.begin(), marked_counts.end(), 0) == 8,
                "selected cycle lost a mark");
        ++result.marked_component_profiles[marked_profile_key(marked_counts)];
        if (all_even) {
            ++result.even_component_cycles;
        }
    }
    return result;
}

struct AllCColouringResult {
    uint64_t fixed_mark_perfect_matchings = 0;
    uint64_t raw_all_c_colourings = 0;
    uint64_t modulo_ab_swap = 0;
    map<string, uint64_t> ab_factor_profiles;
};

void enumerate_fixed_mark_matchings_recursive(
    const vector<CoreEdge>& edges,
    const vector<vector<int>>& adjacency_edges,
    vector<int>& unmatched,
    vector<int>& selected,
    const std::set<int>& fixed_marks,
    AllCColouringResult& result
) {
    int chosen_vertex = -1;
    int best_options = 100;
    for (int vertex = 0; vertex < CORE_N; ++vertex) {
        if (!unmatched[vertex]) {
            continue;
        }
        int options = 0;
        for (int edge : adjacency_edges[vertex]) {
            int other = other_end(edges[edge], vertex);
            options += unmatched[other];
        }
        if (options < best_options) {
            best_options = options;
            chosen_vertex = vertex;
        }
    }
    if (chosen_vertex < 0) {
        ++result.fixed_mark_perfect_matchings;
        std::set<int> matching = fixed_marks;
        matching.insert(selected.begin(), selected.end());
        vector<int> seen(CORE_N, 0);
        vector<int> cycle_lengths;
        for (int root = 0; root < CORE_N; ++root) {
            if (seen[root]) {
                continue;
            }
            int length = 0;
            int current = root;
            int previous_edge = -1;
            while (true) {
                seen[current] = 1;
                ++length;
                int next_edge = -1;
                for (int edge : adjacency_edges[current]) {
                    if (!matching.count(edge) && edge != previous_edge) {
                        next_edge = edge;
                        break;
                    }
                }
                require(next_edge >= 0, "matching complement traversal failed");
                int next = other_end(edges[next_edge], current);
                previous_edge = next_edge;
                current = next;
                if (current == root) {
                    break;
                }
                require(!seen[current], "matching complement is not a 2-factor");
            }
            cycle_lengths.push_back(length);
        }
        if (std::all_of(cycle_lengths.begin(), cycle_lengths.end(),
                        [](int length) { return length % 2 == 0; })) {
            std::sort(cycle_lengths.begin(), cycle_lengths.end());
            std::ostringstream key;
            for (std::size_t index = 0; index < cycle_lengths.size(); ++index) {
                if (index) {
                    key << "+";
                }
                key << cycle_lengths[index];
            }
            ++result.ab_factor_profiles[key.str()];
            uint64_t colourings = uint64_t{1} << cycle_lengths.size();
            result.raw_all_c_colourings += colourings;
            result.modulo_ab_swap += colourings / 2;
        }
        return;
    }
    if (best_options == 0) {
        return;
    }
    unmatched[chosen_vertex] = 0;
    for (int edge : adjacency_edges[chosen_vertex]) {
        int other = other_end(edges[edge], chosen_vertex);
        if (!unmatched[other]) {
            continue;
        }
        unmatched[other] = 0;
        selected.push_back(edge);
        enumerate_fixed_mark_matchings_recursive(
            edges, adjacency_edges, unmatched, selected, fixed_marks, result);
        selected.pop_back();
        unmatched[other] = 1;
    }
    unmatched[chosen_vertex] = 1;
}

AllCColouringResult enumerate_all_c_colourings(
    const vector<CoreEdge>& edges,
    const vector<int>& marks
) {
    vector<vector<int>> adjacency_edges(CORE_N);
    for (int edge = 0; edge < CORE_M; ++edge) {
        adjacency_edges[edges[edge].u].push_back(edge);
        adjacency_edges[edges[edge].v].push_back(edge);
    }
    vector<int> unmatched(CORE_N, 1);
    for (int mark : marks) {
        unmatched[edges[mark].u] = 0;
        unmatched[edges[mark].v] = 0;
    }
    vector<int> selected;
    AllCColouringResult result;
    enumerate_fixed_mark_matchings_recursive(
        edges,
        adjacency_edges,
        unmatched,
        selected,
        std::set<int>(marks.begin(), marks.end()),
        result);
    return result;
}

struct PairedCutStatus {
    int pairing_count = -1;
    int surviving_pairings = -1;
};

PairedCutStatus read_paired_cut_status(const string& path) {
    std::ifstream input(path);
    require(input.good(), "could not read paired-cut result");
    std::ostringstream buffer;
    buffer << input.rdbuf();
    string text = buffer.str();
    auto extract = [&](const string& key) {
        std::regex pattern("\"" + key + "\"\\s*:\\s*([0-9]+)");
        std::smatch match;
        require(std::regex_search(text, match, pattern),
                "missing key in paired-cut result: " + key);
        return std::stoi(match[1].str());
    };
    require(text.find("stable8-paired-cyclic-cut-check-v1") != string::npos,
            "unexpected paired-cut schema");
    return {extract("pairing_count"), extract("surviving_pairings")};
}

string vector_json(const vector<int>& values) {
    std::ostringstream out;
    out << "[";
    for (std::size_t index = 0; index < values.size(); ++index) {
        if (index) {
            out << ",";
        }
        out << values[index];
    }
    out << "]";
    return out.str();
}

string pair_vector_json(const vector<pair<int, int>>& values) {
    std::ostringstream out;
    out << "[";
    for (std::size_t index = 0; index < values.size(); ++index) {
        if (index) {
            out << ",";
        }
        out << "[" << values[index].first << "," << values[index].second << "]";
    }
    out << "]";
    return out.str();
}

string render_report(
    const QuotientConstruction& construction,
    const AmbientValidation& ambient,
    const QuotientCountResult& quotient_result,
    const IndependentQuotientPairResult& independent_quotient_result,
    const DirectCycleResult& direct_result,
    const AllCColouringResult& colouring_result,
    const PairedCutStatus& paired_cut
) {
    uint64_t quotient_pairs = std::accumulate(
        quotient_result.obstruction_histogram.begin(),
        quotient_result.obstruction_histogram.end(),
        uint64_t{0});
    uint64_t liftable_pairs = quotient_result.obstruction_histogram[0];
    require(quotient_pairs == independent_quotient_result.ordered_pairs,
            "two quotient-pair counters disagree");
    require(liftable_pairs == direct_result.even_component_cycles,
            "factor-quotient and direct nonpacking tests disagree");

    int best_factor = -1;
    int best_mask = -1;
    int best_length = 1000000;
    for (int mask = 1; mask < (1 << MAX_FACTORS); ++mask) {
        if (!quotient_result.obstruction_histogram[mask]) {
            continue;
        }
        for (int factor = 0; factor < MAX_FACTORS; ++factor) {
            if (!((mask >> factor) & 1)) {
                continue;
            }
            int length =
                static_cast<int>(construction.factors[factor].cyclic_ports.size());
            if (std::tie(length, factor, mask) <
                std::tie(best_length, best_factor, best_mask)) {
                best_length = length;
                best_factor = factor;
                best_mask = mask;
            }
        }
    }
    require(best_factor >= 0, "no local obstruction mined");
    const vector<int>& obstruction_witness =
        quotient_result.witnesses[best_mask];
    LocalEvaluation smallest = evaluate_local(
        construction.factors[best_factor], obstruction_witness);
    require(smallest.parity_ok && smallest.obstruction,
            "smallest obstruction witness failed");

    vector<int> join_one;
    vector<int> join_two;
    for (int qedge = 0; qedge < QUOTIENT_M; ++qedge) {
        if (obstruction_witness[qedge] == 1) {
            join_one.push_back(qedge);
        } else if (obstruction_witness[qedge] == 2) {
            join_two.push_back(qedge);
        }
    }

    std::ostringstream out;
    out << "{\n";
    out << "  \"schema\": \"stable8-factor-quotient-diagnostic-v1\",\n";
    out << "  \"classification\": \"EXACT_FINITE_DIAGNOSTIC_NONPACKING_CONFIRMED\",\n";
    out << "  \"warning\": \"This concerns one retained marked core, one all-c Tait colouring, and the first terminal pairing. It is not a five-CDC counterexample or a universal theorem.\",\n";
    out << "  \"core\": {\n";
    out << "    \"graph6\": \"" << json_escape(GRAPH6) << "\",\n";
    out << "    \"vertices\": 60,\n";
    out << "    \"edges\": 90,\n";
    out << "    \"marks\": " << pair_vector_json(
        vector<pair<int, int>>(MARKS.begin(), MARKS.end())) << ",\n";
    out << "    \"mark_edge_ids\": " << vector_json(construction.mark_ids) << ",\n";
    out << "    \"all_c_colours_by_edge\": " << vector_json(
        vector<int>(ALL_C_COLOURS.begin(), ALL_C_COLOURS.end())) << "\n";
    out << "  },\n";
    out << "  \"ambient_expansion\": {\n";
    out << "    \"vertices\": " << ambient.vertices << ",\n";
    out << "    \"edges\": " << ambient.edges << ",\n";
    out << "    \"pairing_by_mark_index\": " << pair_vector_json(
        vector<pair<int, int>>(FIRST_PAIRING.begin(), FIRST_PAIRING.end()))
        << ",\n";
    out << "    \"matching_edges\": [[60,61],[62,63],[64,65],[66,67]],\n";
    out << "    \"graph_minus_matching_edges\": "
        << ambient.graph_minus_matching_edges << ",\n";
    out << "    \"simple\": " << (ambient.simple ? "true" : "false") << ",\n";
    out << "    \"cubic\": " << (ambient.cubic ? "true" : "false") << ",\n";
    out << "    \"connected\": " << (ambient.connected ? "true" : "false")
        << ",\n";
    out << "    \"matching_is_matching\": "
        << (ambient.matching_is_matching ? "true" : "false") << ",\n";
    out << "    \"lifted_factor_edges\": " << ambient.lifted_factor_edges
        << ",\n";
    out << "    \"lifted_factor_is_spanning_two_factor\": "
        << (ambient.lifted_factor_is_spanning_two_factor ? "true" : "false")
        << "\n";
    out << "  },\n";
    out << "  \"lifted_ac_factor\": {\n";
    out << "    \"components\": " << construction.factors.size() << ",\n";
    out << "    \"core_cycle_lengths\": [";
    for (int factor = 0; factor < MAX_FACTORS; ++factor) {
        if (factor) out << ",";
        out << construction.factors[factor].core_vertices.size();
    }
    out << "],\n";
    out << "    \"lifted_cycle_lengths\": [";
    for (int factor = 0; factor < MAX_FACTORS; ++factor) {
        if (factor) out << ",";
        out << construction.factors[factor].cyclic_ports.size();
    }
    out << "],\n";
    out << "    \"one_terminal_per_component\": true\n";
    out << "  },\n";
    out << "  \"quotient\": {\n";
    out << "    \"vertices\": " << construction.factors.size() << ",\n";
    out << "    \"edges\": " << construction.quotient_edges.size() << ",\n";
    out << "    \"loops\": ";
    int loops = 0;
    for (const auto& edge : construction.quotient_edges) {
        loops += edge.factor_u == edge.factor_v;
    }
    out << loops << ",\n";
    out << "    \"terminal_vertices\": [0,1,2,3,4,5,6,7],\n";
    out << "    \"edge_rows\": [\n";
    for (int qedge = 0; qedge < QUOTIENT_M; ++qedge) {
        const auto& edge = construction.quotient_edges[qedge];
        out << "      {\"id\":" << qedge
            << ",\"ends\":[" << edge.factor_u << "," << edge.factor_v << "]"
            << ",\"core_edge_id\":" << edge.core_edge
            << ",\"core_ends\":[" << edge.core_u << "," << edge.core_v << "]}";
        out << (qedge + 1 == QUOTIENT_M ? "\n" : ",\n");
    }
    out << "    ]\n";
    out << "  },\n";
    out << "  \"quotient_t_join_pairs\": {\n";
    out << "    \"ordered_edge_disjoint_pairs\": " << quotient_pairs << ",\n";
    out << "    \"unordered_edge_disjoint_pairs\": " << quotient_pairs / 2 << ",\n";
    out << "    \"ordered_exactly_liftable_pairs\": " << liftable_pairs << ",\n";
    out << "    \"independent_first_t_joins_enumerated\": "
        << independent_quotient_result.first_joins_enumerated << ",\n";
    out << "    \"independent_first_t_joins_with_t_even_complement\": "
        << independent_quotient_result.first_joins_with_t_even_complement
        << ",\n";
    out << "    \"independent_ordered_pair_count\": "
        << independent_quotient_result.ordered_pairs << ",\n";
    out << "    \"independent_complement_cycle_dimension_histogram\": {";
    bool first_dimension = true;
    for (const auto& row :
         independent_quotient_result.complement_cycle_dimension_histogram) {
        if (!first_dimension) out << ",";
        first_dimension = false;
        out << "\n      \"" << row.first << "\": " << row.second;
    }
    if (!first_dimension) out << "\n    ";
    out << "},\n";
    out << "    \"obstruction_mask_histogram\": {";
    bool first_histogram = true;
    for (int mask = 0; mask < (1 << MAX_FACTORS); ++mask) {
        uint64_t count = quotient_result.obstruction_histogram[mask];
        if (!count) continue;
        if (!first_histogram) out << ",";
        first_histogram = false;
        out << "\n      \"" << mask << "\": " << count;
    }
    if (!first_histogram) out << "\n    ";
    out << "}\n";
    out << "  },\n";
    out << "  \"smallest_local_interlacing_obstruction\": {\n";
    out << "    \"lifted_cycle_length\": " << best_length << ",\n";
    out << "    \"factor_vertex\": " << best_factor << ",\n";
    out << "    \"global_obstruction_mask\": " << best_mask << ",\n";
    out << "    \"global_mask_pair_count\": "
        << quotient_result.obstruction_histogram[best_mask] << ",\n";
    out << "    \"state_class_counts_00_01_10_11\": ["
        << smallest.state_class_counts[0] << ","
        << smallest.state_class_counts[1] << ","
        << smallest.state_class_counts[2] << ","
        << smallest.state_class_counts[3] << "],\n";
    out << "    \"cyclic_port_quotient_edges_minus_one_is_terminal\": "
        << vector_json(construction.factors[best_factor].cyclic_ports) << ",\n";
    auto terminal_position = std::find(
        construction.factors[best_factor].cyclic_ports.begin(),
        construction.factors[best_factor].cyclic_ports.end(), -1);
    require(terminal_position !=
                construction.factors[best_factor].cyclic_ports.end(),
            "smallest obstruction factor lost its terminal");
    out << "    \"terminal_position\": "
        << (terminal_position -
            construction.factors[best_factor].cyclic_ports.begin())
        << ",\n";
    out << "    \"join_one_demand_positions\": "
        << vector_json(smallest.demand_one_positions) << ",\n";
    out << "    \"join_two_demand_positions\": "
        << vector_json(smallest.demand_two_positions) << ",\n";
    out << "    \"ordered_quotient_join_one_edges\": "
        << vector_json(join_one) << ",\n";
    out << "    \"ordered_quotient_join_two_edges\": "
        << vector_json(join_two) << ",\n";
    out << "    \"interpretation\": \"All four joint parity-path states occur around this circuit, so every choice of complementary local parity paths makes the two lifts share an edge.\"\n";
    out << "  },\n";
    out << "  \"direct_all_mark_cycle_check\": {\n";
    out << "    \"equation_rank\": " << direct_result.equation_rank << ",\n";
    out << "    \"affine_dimension\": " << direct_result.dimension << ",\n";
    out << "    \"cycles_enumerated\": " << direct_result.enumerated << ",\n";
    out << "    \"even_marked_component_cycles\": "
        << direct_result.even_component_cycles << ",\n";
    out << "    \"marked_component_profile_histogram\": {";
    bool first_profile = true;
    for (const auto& row : direct_result.marked_component_profiles) {
        if (!first_profile) out << ",";
        first_profile = false;
        out << "\n      \"" << row.first << "\": " << row.second;
    }
    if (!first_profile) out << "\n    ";
    out << "}\n";
    out << "  },\n";
    out << "  \"equivalence_check\": {\n";
    out << "    \"factor_quotient_liftable\": " << liftable_pairs << ",\n";
    out << "    \"direct_even_component_cycles\": "
        << direct_result.even_component_cycles << ",\n";
    out << "    \"exact_match\": true,\n";
    out << "    \"nonpacking_confirmed\": true\n";
    out << "  },\n";
    out << "  \"alternate_scope\": {\n";
    out << "    \"fixed_mark_c_perfect_matchings\": "
        << colouring_result.fixed_mark_perfect_matchings << ",\n";
    out << "    \"raw_all_c_tait_colourings\": "
        << colouring_result.raw_all_c_colourings << ",\n";
    out << "    \"all_c_colourings_modulo_ab_swap\": "
        << colouring_result.modulo_ab_swap << ",\n";
    out << "    \"ab_factor_profile_histogram\": {";
    bool first_ab = true;
    for (const auto& row : colouring_result.ab_factor_profiles) {
        if (!first_ab) out << ",";
        first_ab = false;
        out << "\n      \"" << row.first << "\": " << row.second;
    }
    if (!first_ab) out << "\n    ";
    out << "},\n";
    out << "    \"pairings_checked_by_paired_cut_audit\": "
        << paired_cut.pairing_count << ",\n";
    out << "    \"paired_cut_qualified_pairings\": "
        << paired_cut.surviving_pairings << ",\n";
    out << "    \"qualified_alternate_colouring_pairing_tests\": 0,\n";
    out << "    \"reason\": \"The retained exact paired-cut audit has no surviving pairing, so there is no paired-cut-qualified alternate pairing/colouring case on this core.\"\n";
    out << "  }\n";
    out << "}\n";
    return out.str();
}

}  // namespace

int main(int argc, char** argv) {
    try {
        string output_path =
            "scratch/stable8-factor-quotient-diagnostic-result.json";
        string paired_cut_path = "scratch/stable8-paired-cut-result.json";
        for (int index = 1; index < argc; ++index) {
            string argument = argv[index];
            if (argument == "--output" && index + 1 < argc) {
                output_path = argv[++index];
            } else if (argument == "--paired-cut-result" && index + 1 < argc) {
                paired_cut_path = argv[++index];
            } else {
                throw std::runtime_error("unknown or incomplete argument: " + argument);
            }
        }
        vector<CoreEdge> core = build_core();
        QuotientConstruction construction = build_quotient(core);
        AmbientValidation ambient =
            validate_ambient_expansion(core, construction);
        QuotientCountResult quotient_result = count_quotient_pairs(construction);
        IndependentQuotientPairResult independent_quotient_result =
            independent_quotient_pair_count(construction);
        DirectCycleResult direct_result =
            direct_cycle_enumeration(core, construction.mark_ids);
        AllCColouringResult colouring_result =
            enumerate_all_c_colourings(core, construction.mark_ids);
        PairedCutStatus paired_cut = read_paired_cut_status(paired_cut_path);
        require(paired_cut.pairing_count == 105, "unexpected pairing count");
        require(paired_cut.surviving_pairings == 0,
                "a paired-cut-qualified alternate case exists");
        string report = render_report(
            construction,
            ambient,
            quotient_result,
            independent_quotient_result,
            direct_result,
            colouring_result,
            paired_cut);
        std::ofstream output(output_path);
        require(output.good(), "could not open output");
        output << report;
        output.close();
        std::cout << report;
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << "\n";
        return 1;
    }
}
