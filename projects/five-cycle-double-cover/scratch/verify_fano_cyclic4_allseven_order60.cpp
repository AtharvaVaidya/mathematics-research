// Solver-independent checker for the cyclically-4 order-60 all-seven
// fixed-flow obstruction.
//
// This checks an auxiliary counterexample: one nowhere-zero F_2^3-flow
// whose seven functional projections are all uncleanable.  The same graph
// has a checked standard FiveCDC, so this is not a FiveCDC counterexample.
//
// For each of two order-32 deleted-edge four-poles and each functional, the
// checker enumerates all 2^17 binary pole cycles p.  With p fixed, coverage
// and every closed-component defect equation are linear in the second pole
// cycle q, so binary Gaussian elimination is an exact exhaustive decision.

#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <queue>
#include <ranges>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

using Mask = std::uint64_t;

namespace {

constexpr const char *BASE_GRAPH6 =
    "_??G@EOGG?GB_AO_g_?CP_??C??O????[O?CA?AG??CA??@???A?O??C???????"
    "G????g???@W???E????@c";
constexpr std::array<int, 48> BASE_FLOW{
    3, 6, 2, 7, 5, 7, 2, 7, 5, 2, 1, 7, 2, 4, 6, 5,
    6, 6, 5, 3, 6, 5, 5, 5, 6, 3, 6, 3, 6, 3, 5, 6,
    3, 2, 4, 4, 1, 1, 6, 7, 2, 3, 1, 2, 6, 6, 2, 4,
};
constexpr std::array<int, 8> TRANSFORM_A{0, 4, 3, 7, 1, 5, 2, 6};
constexpr std::array<int, 8> TRANSFORM_B{0, 7, 3, 4, 5, 2, 6, 1};
constexpr int DELETED_EDGE_A = 2;
constexpr int DELETED_EDGE_B = 6;
constexpr std::array<std::pair<int, int>, 4> PORT_PAIRING{{
    {0, 2},
    {1, 0},
    {2, 3},
    {3, 1},
}};
constexpr const char *LABELED_GRAPH6 =
    "{??K`C?O[@G@P??Go??G?A????w_?_O@C??GC??G??@????G??????C???@O???"
    "J???B????BG?G???????????C?G???????????????@???????????G_???????A??"
    "A@?????_G????@AG????AG??????DC????A???????@???????O????????F?????"
    "C?C?????A?G_??????@??????_?@????????G?????@???????@????????????_??"
    "??????I????????@W????????W?????????X";
constexpr const char *CANONICAL_GRAPH6 =
    "{s?GO?@?O????@????W?G?A_?K???G?A???_??E???A???C???????B???G_??@O?"
    "??_????O??????????K????I??O??????@_????GO????@G????AO??????????C??"
    "?????CG?????OO@????W??_???@G?O????W?G????o?I?????????????@?AC?????"
    "????_?G??_??O????C??????G?_?_?????G????????_??????GO_??????C__????"
    "???CO???????@@???????A?g???????CC";
constexpr std::array<int, 90> FIVECDC_LABELS{
    3, 20, 5, 20, 17, 9, 5, 12, 12, 9, 12, 5, 5, 6, 5,
    3, 24, 5, 10, 9, 17, 24, 12, 20, 9, 17, 24, 18, 9, 17,
    3, 18, 24, 10, 24, 24, 10, 18, 9, 17, 10, 18, 24, 9, 9,
    6, 6, 10, 9, 6, 3, 5, 12, 20, 18, 10, 24, 17, 3, 3,
    17, 18, 5, 5, 10, 17, 9, 24, 20, 12, 12, 20, 24, 18, 18,
    10, 24, 3, 3, 24, 17, 9, 18, 10, 24, 9, 17, 10, 18, 24,
};

struct Graph {
  int vertices = 0;
  std::vector<std::pair<int, int>> edges;
  std::vector<int> values;
};

struct Pole {
  std::vector<int> retained;
  std::vector<std::pair<int, int>> proper_edges;
  std::vector<int> proper_values;
  std::vector<std::pair<int, int>> ports;  // retained old vertex, value
};

Graph parse_graph6(const std::string &record) {
  if (record.empty() || static_cast<unsigned char>(record[0]) >= 126)
    throw std::runtime_error("only short graph6 records are supported");
  Graph graph;
  graph.vertices = static_cast<unsigned char>(record[0]) - 63;
  std::vector<int> bits;
  for (std::size_t index = 1; index < record.size(); ++index) {
    const int value = static_cast<unsigned char>(record[index]) - 63;
    if (value < 0 || value > 63)
      throw std::runtime_error("invalid graph6 byte");
    for (int shift = 5; shift >= 0; --shift)
      bits.push_back((value >> shift) & 1);
  }
  std::size_t position = 0;
  for (int second = 1; second < graph.vertices; ++second)
    for (int first = 0; first < second; ++first) {
      if (position >= bits.size())
        throw std::runtime_error("truncated graph6 row");
      if (bits[position]) graph.edges.emplace_back(first, second);
      ++position;
    }
  for (; position < bits.size(); ++position)
    if (bits[position]) throw std::runtime_error("nonzero graph6 padding");
  return graph;
}

std::string encode_graph6(const Graph &graph) {
  if (graph.vertices > 62)
    throw std::runtime_error("only short graph6 records are supported");
  std::set<std::pair<int, int>> edge_set(graph.edges.begin(), graph.edges.end());
  std::vector<int> bits;
  for (int second = 1; second < graph.vertices; ++second)
    for (int first = 0; first < second; ++first)
      bits.push_back(edge_set.contains({first, second}));
  while (bits.size() % 6) bits.push_back(0);
  std::string answer(1, static_cast<char>(graph.vertices + 63));
  for (std::size_t offset = 0; offset < bits.size(); offset += 6) {
    int value = 0;
    for (int index = 0; index < 6; ++index)
      value |= bits[offset + index] << (5 - index);
    answer.push_back(static_cast<char>(value + 63));
  }
  return answer;
}

std::vector<std::vector<int>> incidence(const Graph &graph) {
  std::vector<std::vector<int>> rows(graph.vertices);
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    const auto [first, second] = graph.edges[edge];
    rows[first].push_back(edge);
    rows[second].push_back(edge);
  }
  return rows;
}

void validate_flow_graph(const Graph &graph) {
  if (graph.edges.size() != graph.values.size())
    throw std::runtime_error("edge/value length mismatch");
  if (std::set<std::pair<int, int>>(
          graph.edges.begin(), graph.edges.end()).size() != graph.edges.size())
    throw std::runtime_error("parallel edge");
  const auto rows = incidence(graph);
  for (const auto &row : rows) {
    if (row.size() != 3) throw std::runtime_error("graph is not cubic");
    int total = 0;
    for (const int edge : row) {
      const int value = graph.values[edge];
      if (value < 1 || value > 7)
        throw std::runtime_error("zero/invalid flow value");
      total ^= value;
    }
    if (total) throw std::runtime_error("flow conservation failed");
  }
}

Pole make_pole(const Graph &base, int deleted_edge) {
  const auto deleted_endpoints = base.edges.at(deleted_edge);
  const std::set<int> deleted{
      deleted_endpoints.first,
      deleted_endpoints.second,
  };
  Pole pole;
  for (int vertex = 0; vertex < base.vertices; ++vertex)
    if (!deleted.contains(vertex)) pole.retained.push_back(vertex);
  for (int edge = 0; edge < static_cast<int>(base.edges.size()); ++edge) {
    const auto [first, second] = base.edges[edge];
    const int value = base.values[edge];
    const bool first_deleted = deleted.contains(first);
    const bool second_deleted = deleted.contains(second);
    if (first_deleted && second_deleted) continue;
    if (first_deleted) {
      pole.ports.emplace_back(second, value);
    } else if (second_deleted) {
      pole.ports.emplace_back(first, value);
    } else {
      pole.proper_edges.emplace_back(first, second);
      pole.proper_values.push_back(value);
    }
  }
  std::ranges::sort(pole.ports);
  if (pole.retained.size() != 30 || pole.proper_edges.size() != 43 ||
      pole.ports.size() != 4)
    throw std::runtime_error("unexpected pole size");
  return pole;
}

std::vector<Mask> binary_nullspace(
    std::vector<Mask> rows,
    int columns) {
  std::vector<int> pivots;
  int rank = 0;
  for (int column = 0; column < columns; ++column) {
    int pivot = -1;
    for (int row = rank; row < static_cast<int>(rows.size()); ++row)
      if ((rows[row] >> column) & 1) {
        pivot = row;
        break;
      }
    if (pivot < 0) continue;
    std::swap(rows[rank], rows[pivot]);
    for (int row = 0; row < static_cast<int>(rows.size()); ++row)
      if (row != rank && ((rows[row] >> column) & 1))
        rows[row] ^= rows[rank];
    pivots.push_back(column);
    ++rank;
  }
  rows.resize(rank);
  std::set<int> pivot_set(pivots.begin(), pivots.end());
  std::vector<Mask> basis;
  for (int free = 0; free < columns; ++free) {
    if (pivot_set.contains(free)) continue;
    Mask vector = Mask{1} << free;
    for (int row = 0; row < rank; ++row)
      if ((rows[row] >> free) & 1)
        vector |= Mask{1} << pivots[row];
    basis.push_back(vector);
  }
  return basis;
}

struct PoleSpace {
  std::vector<Mask> basis;
  std::vector<Mask> cycles;
  std::vector<Mask> edge_coefficients;
};

PoleSpace pole_space(const Pole &pole) {
  const int edge_count =
      static_cast<int>(pole.proper_edges.size() + pole.ports.size());
  std::vector<int> vertex_index(32, -1);
  for (int index = 0; index < static_cast<int>(pole.retained.size()); ++index)
    vertex_index[pole.retained[index]] = index;
  std::vector<Mask> rows(pole.retained.size(), 0);
  for (int edge = 0; edge < static_cast<int>(pole.proper_edges.size()); ++edge) {
    const auto [first, second] = pole.proper_edges[edge];
    rows[vertex_index[first]] |= Mask{1} << edge;
    rows[vertex_index[second]] |= Mask{1} << edge;
  }
  const int offset = static_cast<int>(pole.proper_edges.size());
  for (int port = 0; port < static_cast<int>(pole.ports.size()); ++port)
    rows[vertex_index[pole.ports[port].first]] |= Mask{1} << (offset + port);
  for (const Mask row : rows)
    if (std::popcount(row) != 3)
      throw std::runtime_error("pole incidence is not cubic");

  PoleSpace result;
  result.basis = binary_nullspace(rows, edge_count);
  if (result.basis.size() != 17)
    throw std::runtime_error("unexpected pole cycle dimension");
  result.cycles = {0};
  for (const Mask vector : result.basis) {
    const std::size_t old_size = result.cycles.size();
    result.cycles.reserve(2 * old_size);
    for (std::size_t index = 0; index < old_size; ++index)
      result.cycles.push_back(result.cycles[index] ^ vector);
  }
  std::ranges::sort(result.cycles, [](Mask first, Mask second) {
    const int first_weight = std::popcount(first);
    const int second_weight = std::popcount(second);
    if (first_weight != second_weight) return first_weight > second_weight;
    return first < second;
  });
  result.edge_coefficients.assign(edge_count, 0);
  for (int coordinate = 0;
       coordinate < static_cast<int>(result.basis.size());
       ++coordinate) {
    Mask support = result.basis[coordinate];
    while (support) {
      const int edge = std::countr_zero(support);
      support &= support - 1;
      result.edge_coefficients[edge] |= Mask{1} << coordinate;
    }
  }
  return result;
}

int dot(int first, int second) {
  return std::popcount(static_cast<unsigned>(first & second)) & 1;
}

std::vector<Mask> closed_factor_cuts(
    const Pole &pole,
    const std::vector<int> &values,
    int functional,
    Mask *factor_out) {
  const int proper_count = static_cast<int>(pole.proper_edges.size());
  const int edge_count = proper_count + static_cast<int>(pole.ports.size());
  if (values.size() != static_cast<std::size_t>(edge_count))
    throw std::runtime_error("wrong transformed pole value count");
  Mask factor = 0;
  for (int edge = 0; edge < edge_count; ++edge)
    if (!dot(functional, values[edge])) factor |= Mask{1} << edge;
  *factor_out = factor;

  std::vector<int> vertex_index(32, -1);
  for (int index = 0; index < static_cast<int>(pole.retained.size()); ++index)
    vertex_index[pole.retained[index]] = index;
  std::vector<std::vector<int>> adjacency(pole.retained.size());
  for (int edge = 0; edge < proper_count; ++edge) {
    if (!((factor >> edge) & 1)) continue;
    const auto [first, second] = pole.proper_edges[edge];
    const int left = vertex_index[first];
    const int right = vertex_index[second];
    adjacency[left].push_back(right);
    adjacency[right].push_back(left);
  }
  std::vector<int> component(pole.retained.size(), -1);
  int component_count = 0;
  for (int root = 0; root < static_cast<int>(pole.retained.size()); ++root) {
    if (component[root] >= 0) continue;
    std::queue<int> queue;
    component[root] = component_count;
    queue.push(root);
    while (!queue.empty()) {
      const int vertex = queue.front();
      queue.pop();
      for (const int neighbor : adjacency[vertex])
        if (component[neighbor] < 0) {
          component[neighbor] = component_count;
          queue.push(neighbor);
        }
    }
    ++component_count;
  }

  std::vector<Mask> cuts;
  for (int selected = 0; selected < component_count; ++selected) {
    bool open = false;
    for (int port = 0; port < static_cast<int>(pole.ports.size()); ++port) {
      const int edge = proper_count + port;
      const int vertex = vertex_index[pole.ports[port].first];
      if (((factor >> edge) & 1) && component[vertex] == selected)
        open = true;
    }
    if (open) continue;
    Mask cut = 0;
    for (int edge = 0; edge < proper_count; ++edge) {
      const auto [first, second] = pole.proper_edges[edge];
      if ((component[vertex_index[first]] == selected) !=
          (component[vertex_index[second]] == selected))
        cut |= Mask{1} << edge;
    }
    for (int port = 0; port < static_cast<int>(pole.ports.size()); ++port)
      if (component[vertex_index[pole.ports[port].first]] == selected)
        cut |= Mask{1} << (proper_count + port);
    cuts.push_back(cut);
  }
  return cuts;
}

bool consistent_system(
    const std::vector<Mask> &equations,
    int variables) {
  std::array<Mask, 63> pivots{};
  const Mask variable_mask = (Mask{1} << variables) - 1;
  for (Mask row : equations) {
    while (row & variable_mask) {
      const int pivot = 63 - std::countl_zero(row & variable_mask);
      if (!pivots[pivot]) {
        pivots[pivot] = row;
        row = 0;
        break;
      }
      row ^= pivots[pivot];
    }
    if (row == (Mask{1} << variables)) return false;
  }
  return true;
}

bool local_cleanable(
    const Pole &pole,
    const PoleSpace &space,
    const std::vector<int> &values,
    int functional) {
  Mask factor = 0;
  const std::vector<Mask> cuts =
      closed_factor_cuts(pole, values, functional, &factor);
  const int dimension = static_cast<int>(space.basis.size());
  const Mask rhs_one = Mask{1} << dimension;
  std::vector<Mask> equations;
  equations.reserve(values.size() + cuts.size());
  for (const Mask first : space.cycles) {
    equations.clear();
    Mask missing = factor & ~first;
    while (missing) {
      const int edge = std::countr_zero(missing);
      missing &= missing - 1;
      equations.push_back(space.edge_coefficients[edge] | rhs_one);
    }
    for (const Mask cut : cuts) {
      Mask trace = first & cut;
      Mask equation = 0;
      while (trace) {
        const int edge = std::countr_zero(trace);
        trace &= trace - 1;
        equation ^= space.edge_coefficients[edge];
      }
      if (equation) equations.push_back(equation);
    }
    if (consistent_system(equations, dimension)) return true;
  }
  return false;
}

std::vector<int> transformed_values(
    const Pole &pole,
    const std::array<int, 8> &transform) {
  std::vector<int> values;
  for (const int value : pole.proper_values)
    values.push_back(transform[value]);
  for (const auto &[vertex, value] : pole.ports) {
    (void)vertex;
    values.push_back(transform[value]);
  }
  return values;
}

Graph build_order60(
    const Pole &first,
    const Pole &second) {
  std::array<std::vector<int>, 2> maps;
  maps[0].assign(32, -1);
  maps[1].assign(32, -1);
  for (int index = 0; index < static_cast<int>(first.retained.size()); ++index)
    maps[0][first.retained[index]] = index;
  for (int index = 0; index < static_cast<int>(second.retained.size()); ++index)
    maps[1][second.retained[index]] = 30 + index;

  std::vector<std::tuple<std::pair<int, int>, int>> rows;
  const std::array<const Pole *, 2> poles{&first, &second};
  const std::array<const std::array<int, 8> *, 2> transforms{
      &TRANSFORM_A,
      &TRANSFORM_B,
  };
  for (int block = 0; block < 2; ++block) {
    const Pole &pole = *poles[block];
    for (int edge = 0; edge < static_cast<int>(pole.proper_edges.size()); ++edge) {
      const auto [old_first, old_second] = pole.proper_edges[edge];
      int first_vertex = maps[block][old_first];
      int second_vertex = maps[block][old_second];
      if (first_vertex > second_vertex) std::swap(first_vertex, second_vertex);
      rows.push_back({
          {first_vertex, second_vertex},
          (*transforms[block])[pole.proper_values[edge]],
      });
    }
  }
  for (const auto [first_port, second_port] : PORT_PAIRING) {
    const auto [old_first, first_value] = first.ports[first_port];
    const auto [old_second, second_value] = second.ports[second_port];
    const int transformed_first = TRANSFORM_A[first_value];
    const int transformed_second = TRANSFORM_B[second_value];
    if (transformed_first != transformed_second)
      throw std::runtime_error("connector values disagree");
    int first_vertex = maps[0][old_first];
    int second_vertex = maps[1][old_second];
    if (first_vertex > second_vertex) std::swap(first_vertex, second_vertex);
    rows.push_back({
        {first_vertex, second_vertex},
        transformed_first,
    });
  }
  std::ranges::sort(rows, [](const auto &first, const auto &second) {
    const auto first_edge = std::get<0>(first);
    const auto second_edge = std::get<0>(second);
    return std::pair{first_edge.second, first_edge.first} <
           std::pair{second_edge.second, second_edge.first};
  });
  Graph graph;
  graph.vertices = 60;
  for (const auto &[edge, value] : rows) {
    graph.edges.push_back(edge);
    graph.values.push_back(value);
  }
  return graph;
}

bool component_has_cycle(
    const Graph &graph,
    const std::vector<int> &component,
    const std::set<int> &omitted) {
  std::vector<bool> selected(graph.vertices, false);
  for (const int vertex : component) selected[vertex] = true;
  int edges = 0;
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    if (omitted.contains(edge)) continue;
    const auto [first, second] = graph.edges[edge];
    edges += selected[first] && selected[second];
  }
  return edges >= static_cast<int>(component.size());
}

bool cyclic_edge_connectivity_at_least_four(const Graph &graph) {
  const auto rows = incidence(graph);
  for (int size = 1; size <= 3; ++size) {
    std::vector<int> combination(size);
    std::iota(combination.begin(), combination.end(), 0);
    while (true) {
      const std::set<int> omitted(combination.begin(), combination.end());
      std::vector<bool> seen(graph.vertices, false);
      int cyclic_components = 0;
      for (int root = 0; root < graph.vertices; ++root) {
        if (seen[root]) continue;
        std::vector<int> component{root};
        seen[root] = true;
        for (std::size_t at = 0; at < component.size(); ++at) {
          const int vertex = component[at];
          for (const int edge : rows[vertex]) {
            if (omitted.contains(edge)) continue;
            const auto [first, second] = graph.edges[edge];
            const int neighbor = first == vertex ? second : first;
            if (!seen[neighbor]) {
              seen[neighbor] = true;
              component.push_back(neighbor);
            }
          }
        }
        cyclic_components += component_has_cycle(graph, component, omitted);
      }
      if (cyclic_components >= 2) return false;

      int index = size - 1;
      while (index >= 0 &&
             combination[index] ==
                 static_cast<int>(graph.edges.size()) - size + index)
        --index;
      if (index < 0) break;
      ++combination[index];
      for (int next = index + 1; next < size; ++next)
        combination[next] = combination[next - 1] + 1;
    }
  }
  return true;
}

void check_fivecdc(const Graph &graph) {
  if (graph.edges.size() != FIVECDC_LABELS.size())
    throw std::runtime_error("wrong FiveCDC label count");
  for (const int label : FIVECDC_LABELS)
    if (std::popcount(static_cast<unsigned>(label)) != 2)
      throw std::runtime_error("FiveCDC edge label does not have weight two");
  const auto rows = incidence(graph);
  for (const auto &row : rows) {
    int parity = 0;
    for (const int edge : row) parity ^= FIVECDC_LABELS[edge];
    if (parity) throw std::runtime_error("FiveCDC vertex parity failed");
  }
}

}  // namespace

int main() {
  try {
    Graph base = parse_graph6(BASE_GRAPH6);
    base.values.assign(BASE_FLOW.begin(), BASE_FLOW.end());
    if (base.vertices != 32 || base.edges.size() != 48)
      throw std::runtime_error("wrong base graph size");
    validate_flow_graph(base);

    const Pole pole_a = make_pole(base, DELETED_EDGE_A);
    const Pole pole_b = make_pole(base, DELETED_EDGE_B);
    const PoleSpace space_a = pole_space(pole_a);
    const PoleSpace space_b = pole_space(pole_b);
    const std::vector<int> values_a = transformed_values(pole_a, TRANSFORM_A);
    const std::vector<int> values_b = transformed_values(pole_b, TRANSFORM_B);

    std::vector<int> bad_a, bad_b;
    for (int functional = 1; functional <= 7; ++functional) {
      if (!local_cleanable(pole_a, space_a, values_a, functional))
        bad_a.push_back(functional);
      if (!local_cleanable(pole_b, space_b, values_b, functional))
        bad_b.push_back(functional);
    }
    if (bad_a != std::vector<int>({5, 6, 7}))
      throw std::runtime_error("unexpected first local profile");
    if (bad_b != std::vector<int>({1, 2, 3, 4, 5}))
      throw std::runtime_error("unexpected second local profile");
    std::set<int> union_bad(bad_a.begin(), bad_a.end());
    union_bad.insert(bad_b.begin(), bad_b.end());
    if (union_bad != std::set<int>({1, 2, 3, 4, 5, 6, 7}))
      throw std::runtime_error("local profiles do not cover all functionals");

    const Graph graph = build_order60(pole_a, pole_b);
    validate_flow_graph(graph);
    if (encode_graph6(graph) != LABELED_GRAPH6)
      throw std::runtime_error("labeled graph6 mismatch");
    if (!cyclic_edge_connectivity_at_least_four(graph))
      throw std::runtime_error("graph has a cyclic edge cut of size at most 3");
    check_fivecdc(graph);

    std::cout
        << "{\"schema\":\"fano-cyclic4-allseven-order60-check-v1\""
        << ",\"order\":60,\"edges\":90"
        << ",\"labeled_graph6\":\"" << LABELED_GRAPH6 << "\""
        << ",\"canonical_graph6\":\"" << CANONICAL_GRAPH6 << "\""
        << ",\"pole_cycle_dimension\":17"
        << ",\"pole_cycle_count\":131072"
        << ",\"first_local_bad\":[5,6,7]"
        << ",\"second_local_bad\":[1,2,3,4,5]"
        << ",\"all_seven_blocked\":true"
        << ",\"cyclic_edge_connectivity_at_least_four\":true"
        << ",\"standard_fivecdc_witness\":true"
        << ",\"fivecdc_counterexample\":false"
        << ",\"solver_independent\":true}"
        << std::endl;
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "FAIL: " << error.what() << std::endl;
    return 1;
  }
}
