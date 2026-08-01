#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// Exact diagnostic for a prescribed strengthening of standard FiveCDC.
//
// For every vertex v and every edge e whose endpoints lie outside the
// closed neighbourhood of v, ask for a
// D_5-labeling in which e has label 01 and the three edges at v, in their
// increasing edge-id order, have labels 23, 24, 34.  Global permutations
// fixing {0,1} act as all permutations of {2,3,4}, so fixing this one
// ordering loses no solutions.  Equivalently, e belongs to exactly the
// two Eulerian members of the cover that avoid v.
//
// The distance restriction makes the three neighbours of v and the two
// endpoints of e five distinct degree-two terminals after deleting v and
// e, exactly matching the terminal-distinct five-pole convention.
//
// A FAIL row refutes only this prescribed vertex-edge strengthening.  It
// is not a FiveCDC counterexample unless the unrestricted D_5 formula is
// also UNSAT and that UNSAT result has an independently checked proof.

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
  size_t cursor = 0;
  int order = 0;
  const int first = int((unsigned char)record[cursor++]) - 63;
  if (first < 0 || first > 63)
    throw std::runtime_error("invalid graph6 header");
  if (first < 63) {
    order = first;
  } else {
    if (record.size() < 4 || record[cursor] == '~')
      throw std::runtime_error("large graph6 headers are unsupported");
    order = 0;
    for (int index = 0; index < 3; ++index) {
      const int value = int((unsigned char)record[cursor++]) - 63;
      if (value < 0 || value > 63)
        throw std::runtime_error("invalid graph6 order");
      order = (order << 6) | value;
    }
  }
  if (order < 0 || order > 258047)
    throw std::runtime_error("unsupported graph6 order");

  std::vector<int> bits;
  for (; cursor < record.size(); ++cursor) {
    const int value = int((unsigned char)record[cursor]) - 63;
    if (value < 0 || value > 63)
      throw std::runtime_error("invalid graph6 character");
    for (int shift = 5; shift >= 0; --shift)
      bits.push_back((value >> shift) & 1);
  }

  const size_t required = size_t(order) * size_t(order - 1) / 2;
  if (bits.size() < required)
    throw std::runtime_error("short graph6 payload");

  std::vector<Edge> edges;
  size_t bit = 0;
  for (int right = 1; right < order; ++right)
    for (int left = 0; left < right; ++left) {
      if (bits[bit]) edges.emplace_back(left, right);
      ++bit;
    }
  for (; bit < bits.size(); ++bit)
    if (bits[bit])
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

static std::pair<int, int> test_record(const std::string& record,
                                      unsigned long long& checks) {
  const auto [order, edges] = parse_graph6(record);
  std::vector<std::vector<int>> incident(order);
  for (int edge = 0; edge < int(edges.size()); ++edge) {
    const auto [left, right] = edges[edge];
    if (left == right) throw std::runtime_error("loop");
    incident[left].push_back(edge);
    incident[right].push_back(edge);
  }
  for (auto& row : incident) {
    std::sort(row.begin(), row.end());
    if (row.size() != 3)
      throw std::runtime_error("record is not cubic");
  }

  CaDiCaL::Solver solver;
  for (int edge = 0; edge < int(edges.size()); ++edge)
    exactly_one(solver, edge);

  for (const auto& row : incident)
    for (int left = 0; left < 10; ++left)
      for (int middle = 0; middle < 10; ++middle) {
        const int forced = label_index(D5[left] ^ D5[middle]);
        solver.add(-variable(row[0], left));
        solver.add(-variable(row[1], middle));
        if (forced >= 0)
          solver.add(variable(row[2], forced));
        solver.add(0);
      }

  const int edge_label = label_index(3);  // 01
  const std::array<int, 3> vertex_labels = {
      label_index(12),  // 23
      label_index(20),  // 24
      label_index(24),  // 34
  };
  if (edge_label < 0 || *std::min_element(vertex_labels.begin(),
                                          vertex_labels.end()) < 0)
    throw std::runtime_error("bad prescribed labels");

  for (int vertex = 0; vertex < order; ++vertex)
    for (int edge = 0; edge < int(edges.size()); ++edge) {
      const auto [left, right] = edges[edge];
      if (left == vertex || right == vertex) continue;
      bool endpoint_is_neighbour = false;
      for (int root_edge : incident[vertex]) {
        const auto [root_left, root_right] = edges[root_edge];
        const int neighbour =
            root_left == vertex ? root_right : root_left;
        if (left == neighbour || right == neighbour) {
          endpoint_is_neighbour = true;
          break;
        }
      }
      if (endpoint_is_neighbour) continue;
      solver.assume(variable(edge, edge_label));
      for (int position = 0; position < 3; ++position)
        solver.assume(variable(incident[vertex][position],
                               vertex_labels[position]));
      const int result = solver.solve();
      ++checks;
      if (result == 20) return {vertex, edge};
      if (result != 10)
        throw std::runtime_error("SAT solver returned UNKNOWN");
    }
  return {-1, -1};
}

int main() {
  std::string record;
  unsigned long long records = 0;
  unsigned long long checks = 0;
  while (std::getline(std::cin, record)) {
    if (record.empty()) continue;
    try {
      const auto failure = test_record(record, checks);
      ++records;
      if (failure.first >= 0) {
        std::cout << "FAIL\t" << record << '\t'
                  << failure.first << '\t' << failure.second
                  << "\tchecks\t" << checks << '\n';
        return 1;
      }
    } catch (const std::exception& error) {
      std::cout << "ERROR\t" << record << '\t' << error.what() << '\n';
      return 2;
    }
  }
  std::cout << "PASS\trecords\t" << records
            << "\ttarget_checks\t" << checks << '\n';
  return 0;
}
