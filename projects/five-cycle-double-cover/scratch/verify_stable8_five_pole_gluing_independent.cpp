#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <bit>
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

constexpr std::array<std::pair<int, int>, 8> MARKS = {{
    {3, 11}, {6, 15}, {7, 18}, {22, 26},
    {30, 34}, {38, 42}, {46, 50}, {54, 58},
}};

constexpr std::array<int, 10> LABELS =
    {3, 5, 9, 17, 6, 10, 18, 12, 20, 24};

struct Graph {
  int vertices;
  std::vector<std::pair<int, int>> edges;
};

Graph parse_graph6(const std::string &record) {
  if (record.empty() || record[0] == '~')
    throw std::runtime_error("unsupported graph6 header");
  Graph graph{static_cast<unsigned char>(record[0]) - 63, {}};
  std::vector<int> bits;
  for (std::size_t position = 1; position < record.size(); ++position) {
    const int byte = static_cast<unsigned char>(record[position]) - 63;
    if (byte < 0 || byte >= 64) throw std::runtime_error("bad graph6 byte");
    for (int shift = 5; shift >= 0; --shift)
      bits.push_back((byte >> shift) & 1);
  }
  std::size_t cursor = 0;
  for (int high = 1; high < graph.vertices; ++high)
    for (int low = 0; low < high; ++low) {
      if (cursor >= bits.size()) throw std::runtime_error("short graph6");
      if (bits[cursor]) graph.edges.emplace_back(low, high);
      ++cursor;
    }
  return graph;
}

void clause(Solver &solver, const std::vector<int> &literals) {
  for (int literal : literals) solver.add(literal);
  solver.add(0);
}

int variable(int edge, int coordinate) {
  return 5 * edge + coordinate + 1;
}

void exact_two(Solver &solver, int edge) {
  for (int first = 0; first < 5; ++first)
    for (int second = first + 1; second < 5; ++second)
      for (int third = second + 1; third < 5; ++third)
        clause(solver, {-variable(edge, first), -variable(edge, second),
                        -variable(edge, third)});
  for (int omitted = 0; omitted < 5; ++omitted) {
    std::vector<int> literals;
    for (int coordinate = 0; coordinate < 5; ++coordinate)
      if (coordinate != omitted)
        literals.push_back(variable(edge, coordinate));
    clause(solver, literals);
  }
}

void even_three(Solver &solver, int first, int second, int third,
                int coordinate) {
  const int a = variable(first, coordinate);
  const int b = variable(second, coordinate);
  const int c = variable(third, coordinate);
  clause(solver, {-a, b, c});
  clause(solver, {a, -b, c});
  clause(solver, {a, b, -c});
  clause(solver, {-a, -b, -c});
}

std::uint32_t canonical(const std::array<int, 5> &word) {
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

std::map<std::uint32_t, std::array<int, 5>> representatives() {
  std::map<std::uint32_t, std::array<int, 5>> result;
  for (int a : LABELS)
    for (int b : LABELS)
      for (int c : LABELS)
        for (int d : LABELS)
          for (int e : LABELS) {
            if ((a ^ b ^ c ^ d ^ e) != 0) continue;
            const std::array<int, 5> word = {a, b, c, d, e};
            result.emplace(canonical(word), word);
          }
  if (result.size() != 62) throw std::runtime_error("orbit count mismatch");
  return result;
}

struct Pole {
  std::array<int, 5> subset;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::array<int, 3>> incidence;
};

Pole make_pole(const Graph &core, const std::array<int, 5> &subset) {
  std::map<std::pair<int, int>, int> positions;
  for (int index = 0; index < 5; ++index)
    positions[MARKS[subset[index]]] = index;
  Pole pole{subset, {}, std::vector<std::array<int, 3>>(65)};
  for (const auto &edge : core.edges) {
    const auto found = positions.find(edge);
    if (found == positions.end()) {
      pole.edges.push_back(edge);
    } else {
      const int terminal = 60 + found->second;
      pole.edges.emplace_back(edge.first, terminal);
      pole.edges.emplace_back(edge.second, terminal);
    }
  }
  for (int index = 0; index < 5; ++index)
    pole.edges.emplace_back(60 + index, 65 + index);
  if (pole.edges.size() != 100) throw std::runtime_error("edge mismatch");
  std::vector<std::vector<int>> rows(65);
  for (int edge = 0; edge < 100; ++edge) {
    const auto [left, right] = pole.edges[edge];
    if (left < 65) rows[left].push_back(edge);
    if (right < 65) rows[right].push_back(edge);
  }
  for (int vertex = 0; vertex < 65; ++vertex) {
    if (rows[vertex].size() != 3) throw std::runtime_error("degree mismatch");
    pole.incidence[vertex] =
        {rows[vertex][0], rows[vertex][1], rows[vertex][2]};
  }
  return pole;
}

std::set<std::uint32_t> certify_58(
    const Pole &pole,
    const std::map<std::uint32_t, std::array<int, 5>> &orbits) {
  Solver solver;
  solver.set("quiet", 1);
  for (int edge = 0; edge < 100; ++edge) exact_two(solver, edge);
  for (const auto &row : pole.incidence)
    for (int coordinate = 0; coordinate < 5; ++coordinate)
      even_three(solver, row[0], row[1], row[2], coordinate);

  std::set<std::uint32_t> certified;
  for (const auto &[key, word] : orbits) {
    for (int position = 0; position < 5; ++position)
      for (int coordinate = 0; coordinate < 5; ++coordinate)
        solver.assume(
            (word[position] & (1 << coordinate))
                ? variable(95 + position, coordinate)
                : -variable(95 + position, coordinate));
    const int result = solver.solve();
    if (result == 20) continue;
    if (result != 10) throw std::runtime_error("solver returned UNKNOWN");

    std::array<int, 100> labels{};
    for (int edge = 0; edge < 100; ++edge) {
      labels[edge] = 0;
      for (int coordinate = 0; coordinate < 5; ++coordinate)
        if (solver.val(variable(edge, coordinate)) > 0)
          labels[edge] |= 1 << coordinate;
      if (std::popcount(static_cast<unsigned>(labels[edge])) != 2)
        throw std::runtime_error("SAT model violates exact-two semantics");
    }
    for (const auto &row : pole.incidence)
      if ((labels[row[0]] ^ labels[row[1]] ^ labels[row[2]]) != 0)
        throw std::runtime_error("SAT model violates vertex xor semantics");
    for (int position = 0; position < 5; ++position)
      if (labels[95 + position] != word[position])
        throw std::runtime_error("SAT model violates boundary assumptions");
    certified.insert(key);
    if (certified.size() == 58) break;
  }
  if (certified.size() != 58)
    throw std::runtime_error("pole has fewer than 58 certified states");
  return certified;
}

std::uint32_t permute_positions(
    std::uint32_t key, const std::array<int, 5> &permutation) {
  std::array<int, 5> word{};
  for (int position = 0; position < 5; ++position)
    word[position] = (key >> (5 * permutation[position])) & 31;
  return canonical(word);
}

}  // namespace

int main() {
  try {
    const Graph core = parse_graph6(CORE_GRAPH6);
    if (core.vertices != 60 || core.edges.size() != 90)
      throw std::runtime_error("core mismatch");
    const std::set<std::pair<int, int>> core_edges(
        core.edges.begin(), core.edges.end());
    for (const auto &mark : MARKS)
      if (!core_edges.count(mark)) throw std::runtime_error("missing mark");
    const auto orbits = representatives();

    std::vector<std::set<std::uint32_t>> relations;
    for (int a = 0; a < 8; ++a)
      for (int b = a + 1; b < 8; ++b)
        for (int c = b + 1; c < 8; ++c)
          for (int d = c + 1; d < 8; ++d)
            for (int e = d + 1; e < 8; ++e) {
              const std::array<int, 5> subset = {a, b, c, d, e};
              relations.push_back(
                  certify_58(make_pole(core, subset), orbits));
              std::cout << "pole";
              for (int index : subset) std::cout << ' ' << index;
              std::cout << " certified_states 58\n";
            }

    std::uint64_t tests = 0;
    for (std::size_t first = 0; first < relations.size(); ++first)
      for (std::size_t second = first; second < relations.size(); ++second) {
        std::array<int, 5> permutation = {0, 1, 2, 3, 4};
        do {
          ++tests;
          bool common = false;
          for (std::uint32_t key : relations[second])
            if (relations[first].count(
                    permute_positions(key, permutation))) {
              common = true;
              break;
            }
          if (!common)
            throw std::runtime_error("58-state subsets failed to intersect");
        } while (std::next_permutation(permutation.begin(),
                                        permutation.end()));
      }
    if (tests != 191520) throw std::runtime_error("test count mismatch");
    std::cout << "PASS poles 56 certified_lower_bound 58 universe 62 "
                 "pair_permutation_tests "
              << tests << " incompatible 0\n";
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "ERROR " << error.what() << '\n';
    return 2;
  }
}
