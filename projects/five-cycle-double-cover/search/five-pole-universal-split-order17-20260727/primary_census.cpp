#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// Diagnostic exact census for the following rooted five-pole state.
//
// Choose two of the five ordered semiedges.  Give both the label 01, and
// give the other three semiedges the labels 23, 24, 34.  The labels form
// a doubled K_2 on one colour pair and a triangle on the complementary
// three colours.  The S_5 orbit is independent of the order in which the
// three triangle labels are put on the remaining boundary positions.
//
// For every graph6 record on stdin, this program builds the full D_5
// edge-labelling CSP once and tests all ten choices of the doubled
// boundary positions by SAT assumptions.  It does not trust a positive
// aggregate as a universal theorem and it does not emit UNSAT
// certificates; any failure is a candidate requiring certificate replay.

using Edge = std::pair<int, int>;

static const std::array<int, 10> D5 = {
    3, 5, 9, 17, 6, 10, 18, 12, 20, 24,
};

static int label_index(int mask) {
  const auto found = std::find(D5.begin(), D5.end(), mask);
  return found == D5.end() ? -1 : int(found - D5.begin());
}

static int variable(int edge, int label) {
  return 1 + 10 * edge + label;
}

static std::pair<int, std::vector<Edge>> parse_graph6(
    const std::string& record) {
  if (record.empty()) throw std::runtime_error("empty graph6 record");
  const int order = int((unsigned char)record[0]) - 63;
  if (order < 0 || order > 62)
    throw std::runtime_error("only short graph6 orders are supported");

  std::vector<int> bits;
  for (size_t index = 1; index < record.size(); ++index) {
    const int value = int((unsigned char)record[index]) - 63;
    if (value < 0 || value > 63)
      throw std::runtime_error("invalid graph6 character");
    for (int shift = 5; shift >= 0; --shift)
      bits.push_back((value >> shift) & 1);
  }

  const size_t required = size_t(order) * size_t(order - 1) / 2;
  if (bits.size() < required)
    throw std::runtime_error("short graph6 payload");

  std::vector<Edge> edges;
  size_t cursor = 0;
  for (int right = 1; right < order; ++right)
    for (int left = 0; left < right; ++left) {
      if (bits[cursor]) edges.emplace_back(left, right);
      ++cursor;
    }
  for (; cursor < bits.size(); ++cursor)
    if (bits[cursor])
      throw std::runtime_error("nonzero graph6 padding");
  return {order, edges};
}

static void exactly_one(CaDiCaL::Solver& solver, int edge) {
  for (int label = 0; label < 10; ++label)
    solver.add(variable(edge, label));
  solver.add(0);
  for (int left = 0; left < 10; ++left)
    for (int right = left + 1; right < 10; ++right) {
      solver.add(-variable(edge, left));
      solver.add(-variable(edge, right));
      solver.add(0);
    }
}

static std::array<int, 5> split_boundary(
    int first_position, int second_position) {
  std::array<int, 5> boundary = {-1, -1, -1, -1, -1};
  boundary[first_position] = 3;   // 01
  boundary[second_position] = 3;  // 01
  const std::array<int, 3> triangle = {12, 20, 24};  // 23, 24, 34
  int cursor = 0;
  for (int position = 0; position < 5; ++position)
    if (boundary[position] < 0)
      boundary[position] = triangle[cursor++];
  return boundary;
}

static std::pair<int, int> test_record(const std::string& record) {
  const auto [order, proper_edges] = parse_graph6(record);
  std::vector<std::vector<int>> incident(order);
  for (int edge = 0; edge < int(proper_edges.size()); ++edge) {
    const auto [left, right] = proper_edges[edge];
    incident[left].push_back(edge);
    incident[right].push_back(edge);
  }

  std::vector<int> terminals;
  for (int vertex = 0; vertex < order; ++vertex) {
    if (incident[vertex].size() == 2)
      terminals.push_back(vertex);
    else if (incident[vertex].size() != 3)
      throw std::runtime_error("record is not a cubic five-pole core");
  }
  if (terminals.size() != 5)
    throw std::runtime_error("record does not have five terminals");

  const int first_boundary = int(proper_edges.size());
  for (int position = 0; position < 5; ++position)
    incident[terminals[position]].push_back(first_boundary + position);
  const int total_edges = first_boundary + 5;

  CaDiCaL::Solver solver;
  for (int edge = 0; edge < total_edges; ++edge)
    exactly_one(solver, edge);

  // At a completed cubic vertex, two labels force the third.  Three
  // weight-two masks xor to zero exactly when they are a K_5 triangle.
  for (const auto& row : incident) {
    if (row.size() != 3)
      throw std::runtime_error("bad completed incidence row");
    for (int left = 0; left < 10; ++left)
      for (int middle = 0; middle < 10; ++middle) {
        const int forced = label_index(D5[left] ^ D5[middle]);
        solver.add(-variable(row[0], left));
        solver.add(-variable(row[1], middle));
        if (forced >= 0)
          solver.add(variable(row[2], forced));
        solver.add(0);
      }
  }

  int tested = 0;
  for (int first = 0; first < 5; ++first)
    for (int second = first + 1; second < 5; ++second) {
      const auto boundary = split_boundary(first, second);
      for (int position = 0; position < 5; ++position) {
        const int label = label_index(boundary[position]);
        if (label < 0) throw std::runtime_error("bad target label");
        solver.assume(variable(first_boundary + position, label));
      }
      const int result = solver.solve();
      ++tested;
      if (result == 20)
        return {first, second};
      if (result != 10)
        throw std::runtime_error("SAT solver returned UNKNOWN");
    }
  if (tested != 10)
    throw std::runtime_error("wrong target count");
  return {-1, -1};
}

int main() {
  std::string record;
  unsigned long long records = 0;
  unsigned long long target_checks = 0;
  while (std::getline(std::cin, record)) {
    if (record.empty()) continue;
    try {
      const auto failure = test_record(record);
      ++records;
      if (failure.first >= 0) {
        std::cout << "FAIL\t" << record << '\t'
                  << failure.first << '\t' << failure.second << '\n';
        return 1;
      }
      target_checks += 10;
    } catch (const std::exception& error) {
      std::cout << "ERROR\t" << record << '\t' << error.what() << '\n';
      return 2;
    }
  }
  std::cout << "PASS\trecords\t" << records
            << "\ttarget_checks\t" << target_checks << '\n';
  return 0;
}
