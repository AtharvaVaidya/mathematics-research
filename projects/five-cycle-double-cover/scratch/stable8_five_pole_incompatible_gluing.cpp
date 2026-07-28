#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using CaDiCaL::Solver;

namespace {

constexpr const char *CORE_GRAPH6 =
    "{??????O@?B?D?EGGSAK?H_?HG?Ao@A_??????????????C?G?C???M???B_???"
    "[???????????????????O?C??C????B_????M?????[_???????????????????????"
    "C??_???O?????B_?????B_?????@q?????????????????????????????C???G???"
    "C???????M???????B_???????[_??????????????????????????????????O????"
    "G???C????????B_????????M?????????[";

// Keep the marks separately so a parser mismatch fails before any SAT claim
// is made.
constexpr std::array<std::pair<int, int>, 8> MARKS = {{
    {3, 11}, {6, 15}, {7, 18}, {22, 26},
    {30, 34}, {38, 42}, {46, 50}, {54, 58},
}};

struct Graph {
  int vertices = 0;
  std::vector<std::pair<int, int>> edges;
};

Graph parse_graph6(const std::string &record) {
  if (record.empty() || static_cast<unsigned char>(record[0]) == 126)
    throw std::runtime_error("unsupported graph6 header");
  Graph graph;
  graph.vertices = static_cast<unsigned char>(record[0]) - 63;
  if (graph.vertices < 0 || graph.vertices > 62)
    throw std::runtime_error("unsupported graph6 order");
  std::vector<int> bits;
  for (std::size_t index = 1; index < record.size(); ++index) {
    int value = static_cast<unsigned char>(record[index]) - 63;
    if (value < 0 || value > 63)
      throw std::runtime_error("invalid graph6 byte");
    for (int shift = 5; shift >= 0; --shift)
      bits.push_back((value >> shift) & 1);
  }
  std::size_t cursor = 0;
  for (int right = 1; right < graph.vertices; ++right) {
    for (int left = 0; left < right; ++left) {
      if (cursor >= bits.size()) throw std::runtime_error("short graph6");
      if (bits[cursor]) graph.edges.emplace_back(left, right);
      ++cursor;
    }
  }
  return graph;
}

void add_clause(Solver &solver, const std::vector<int> &clause) {
  for (int literal : clause) solver.add(literal);
  solver.add(0);
}

void add_exactly_two(Solver &solver, const std::array<int, 5> &x) {
  for (int i = 0; i < 5; ++i)
    for (int j = i + 1; j < 5; ++j)
      for (int k = j + 1; k < 5; ++k)
        add_clause(solver, {-x[i], -x[j], -x[k]});
  for (int omitted = 0; omitted < 5; ++omitted) {
    std::vector<int> clause;
    for (int i = 0; i < 5; ++i)
      if (i != omitted) clause.push_back(x[i]);
    add_clause(solver, clause);
  }
}

void add_even_three(Solver &solver, int a, int b, int c) {
  add_clause(solver, {a, b, -c});
  add_clause(solver, {a, -b, c});
  add_clause(solver, {-a, b, c});
  add_clause(solver, {-a, -b, -c});
}

std::uint32_t canonical_key(const std::array<int, 5> &word) {
  std::array<int, 5> permutation = {0, 1, 2, 3, 4};
  std::uint32_t best = UINT32_MAX;
  do {
    std::uint32_t key = 0;
    for (int position = 0; position < 5; ++position) {
      int transformed = 0;
      for (int color = 0; color < 5; ++color)
        if (word[position] & (1 << color))
          transformed |= 1 << permutation[color];
      key |= static_cast<std::uint32_t>(transformed) << (5 * position);
    }
    best = std::min(best, key);
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  return best;
}

std::array<int, 5> unpack(std::uint32_t key) {
  std::array<int, 5> word{};
  for (int position = 0; position < 5; ++position)
    word[position] = (key >> (5 * position)) & 31;
  return word;
}

std::uint32_t permute_positions(
    std::uint32_t key, const std::array<int, 5> &permutation) {
  const auto word = unpack(key);
  std::array<int, 5> transformed{};
  for (int position = 0; position < 5; ++position)
    transformed[position] = word[permutation[position]];
  return canonical_key(transformed);
}

std::map<std::uint32_t, std::array<int, 5>> boundary_orbits() {
  constexpr std::array<int, 10> PAIRS =
      {3, 5, 9, 17, 6, 10, 18, 12, 20, 24};
  std::map<std::uint32_t, std::array<int, 5>> result;
  for (int a : PAIRS)
    for (int b : PAIRS)
      for (int c : PAIRS)
        for (int d : PAIRS)
          for (int e : PAIRS) {
            if ((a ^ b ^ c ^ d ^ e) != 0) continue;
            std::array<int, 5> word = {a, b, c, d, e};
            result.emplace(canonical_key(word), word);
          }
  if (result.size() != 62)
    throw std::runtime_error("five-boundary orbit count is not 62");
  return result;
}

struct Pole {
  std::array<int, 5> mark_indices{};
  std::vector<std::pair<int, int>> proper_edges;
  std::array<int, 5> terminals{};
  std::set<std::uint32_t> relation;
};

Pole classify(const Graph &core, const std::array<int, 5> &selected,
              const std::map<std::uint32_t, std::array<int, 5>> &orbits) {
  Pole pole;
  pole.mark_indices = selected;
  std::map<std::pair<int, int>, int> selected_position;
  for (int position = 0; position < 5; ++position) {
    auto edge = MARKS[selected[position]];
    if (edge.first > edge.second) std::swap(edge.first, edge.second);
    selected_position[edge] = position;
    pole.terminals[position] = core.vertices + position;
  }
  for (auto edge : core.edges) {
    if (edge.first > edge.second) std::swap(edge.first, edge.second);
    auto found = selected_position.find(edge);
    if (found == selected_position.end()) {
      pole.proper_edges.push_back(edge);
    } else {
      const int terminal = core.vertices + found->second;
      pole.proper_edges.emplace_back(edge.first, terminal);
      pole.proper_edges.emplace_back(edge.second, terminal);
    }
  }
  if (pole.proper_edges.size() != 95)
    throw std::runtime_error("unexpected pole edge count");

  const int vertices = core.vertices + 5;
  const int proper_count = pole.proper_edges.size();
  const int total_edges = proper_count + 5;
  std::vector<std::vector<int>> incidence(vertices);
  for (int edge_id = 0; edge_id < proper_count; ++edge_id) {
    const auto [left, right] = pole.proper_edges[edge_id];
    incidence[left].push_back(edge_id);
    incidence[right].push_back(edge_id);
  }
  for (int position = 0; position < 5; ++position)
    incidence[pole.terminals[position]].push_back(proper_count + position);
  for (const auto &row : incidence)
    if (row.size() != 3) throw std::runtime_error("pole is not cubic");

  Solver solver;
  solver.set("quiet", 1);
  for (int edge_id = 0; edge_id < total_edges; ++edge_id) {
    std::array<int, 5> variables{};
    for (int coordinate = 0; coordinate < 5; ++coordinate)
      variables[coordinate] = 5 * edge_id + coordinate + 1;
    add_exactly_two(solver, variables);
  }
  for (const auto &row : incidence)
    for (int coordinate = 0; coordinate < 5; ++coordinate)
      add_even_three(solver, 5 * row[0] + coordinate + 1,
                     5 * row[1] + coordinate + 1,
                     5 * row[2] + coordinate + 1);

  for (const auto &[key, word] : orbits) {
    for (int position = 0; position < 5; ++position) {
      const int edge_id = proper_count + position;
      for (int coordinate = 0; coordinate < 5; ++coordinate) {
        const int variable = 5 * edge_id + coordinate + 1;
        solver.assume((word[position] & (1 << coordinate)) ? variable
                                                            : -variable);
      }
    }
    const int result = solver.solve();
    if (result == 10)
      pole.relation.insert(key);
    else if (result != 20)
      throw std::runtime_error("SAT solver returned UNKNOWN");
  }
  return pole;
}

}  // namespace

int main() {
  try {
    Graph core = parse_graph6(CORE_GRAPH6);
    if (core.vertices != 60 || core.edges.size() != 90)
      throw std::runtime_error("core graph6 literal mismatch");
    std::set<std::pair<int, int>> edge_set(core.edges.begin(),
                                           core.edges.end());
    for (auto edge : MARKS) {
      if (edge.first > edge.second) std::swap(edge.first, edge.second);
      if (!edge_set.count(edge)) throw std::runtime_error("mark absent");
    }

    const auto orbits = boundary_orbits();
    std::vector<Pole> poles;
    for (int a = 0; a < 8; ++a)
      for (int b = a + 1; b < 8; ++b)
        for (int c = b + 1; c < 8; ++c)
          for (int d = c + 1; d < 8; ++d)
            for (int e = d + 1; e < 8; ++e) {
              std::array<int, 5> selected = {a, b, c, d, e};
              poles.push_back(classify(core, selected, orbits));
              std::cout << "pole";
              for (int index : selected) std::cout << ' ' << index;
              std::cout << " states " << poles.back().relation.size()
                        << '\n';
            }

    std::array<int, 5> permutation = {0, 1, 2, 3, 4};
    std::uint64_t tests = 0;
    for (int first = 0; first < static_cast<int>(poles.size()); ++first) {
      for (int second = first; second < static_cast<int>(poles.size());
           ++second) {
        permutation = {0, 1, 2, 3, 4};
        do {
          ++tests;
          bool intersects = false;
          for (std::uint32_t key : poles[second].relation) {
            if (poles[first].relation.count(
                    permute_positions(key, permutation))) {
              intersects = true;
              break;
            }
          }
          if (!intersects) {
            std::cout << "INCOMPATIBLE first " << first << " second "
                      << second << " permutation";
            for (int value : permutation) std::cout << ' ' << value;
            std::cout << '\n';
            return 1;
          }
        } while (std::next_permutation(permutation.begin(),
                                        permutation.end()));
      }
    }
    std::cout << "PASS poles " << poles.size() << " pair_permutation_tests "
              << tests << " incompatible 0\n";
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "ERROR " << error.what() << '\n';
    return 2;
  }
}
