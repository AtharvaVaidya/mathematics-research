// Semantic checker for canonical expanded graphs at D5 macro frontier 2.
//
// Reads graph6 graphs from stdin.  Independently verifies that each graph is
// simple, connected, bridgeless, and cubic.  It then solves both the Tait
// three-edge-colouring formula and the standard FiveCDC formula.  Every SAT
// model is checked directly against graph incidence before it is counted.

#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Edges = std::vector<std::pair<int,int>>;

static std::pair<int, Edges> parse_graph6(const std::string &line) {
  if (line.empty() || static_cast<unsigned char>(line[0]) < 63)
    throw std::runtime_error("bad graph6 line");
  int vertices = static_cast<unsigned char>(line[0]) - 63;
  if (vertices > 62) throw std::runtime_error("long graph6 not implemented");
  Edges edges;
  int character = 1;
  int remaining = 0;
  int value = 0;
  auto bit = [&]() {
    if (!remaining) {
      if (character >= static_cast<int>(line.size()))
        throw std::runtime_error("truncated graph6");
      value = static_cast<unsigned char>(line[character++]) - 63;
      if (value < 0 || value >= 64)
        throw std::runtime_error("bad graph6 character");
      remaining = 6;
    }
    int answer = (value >> (--remaining)) & 1;
    return answer;
  };
  for (int right = 1; right < vertices; ++right)
    for (int left = 0; left < right; ++left)
      if (bit()) edges.push_back({left, right});
  return {vertices, edges};
}

static bool connected_without(
    int vertices, const Edges &edges, int skipped) {
  std::vector<char> seen(vertices, false);
  std::vector<int> stack = {0};
  seen[0] = true;
  while (!stack.empty()) {
    int current = stack.back();
    stack.pop_back();
    for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
      if (edge == skipped) continue;
      auto [left, right] = edges[edge];
      int other = -1;
      if (left == current) other = right;
      if (right == current) other = left;
      if (other >= 0 && !seen[other]) {
        seen[other] = true;
        stack.push_back(other);
      }
    }
  }
  return std::count(seen.begin(), seen.end(), true) == vertices;
}

static std::vector<std::vector<int>> validate_graph(
    int vertices, const Edges &edges) {
  if (vertices <= 0) throw std::runtime_error("empty graph");
  std::vector<std::vector<int>> incident(vertices);
  std::vector<std::vector<char>> adjacent(
      vertices, std::vector<char>(vertices, false));
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    auto [left, right] = edges[edge];
    if (left < 0 || left >= vertices || right < 0 || right >= vertices ||
        left == right || adjacent[left][right])
      throw std::runtime_error("graph is not simple");
    adjacent[left][right] = adjacent[right][left] = true;
    incident[left].push_back(edge);
    incident[right].push_back(edge);
  }
  for (const auto &row : incident)
    if (row.size() != 3) throw std::runtime_error("graph is not cubic");
  if (!connected_without(vertices, edges, -1))
    throw std::runtime_error("graph is disconnected");
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge)
    if (!connected_without(vertices, edges, edge))
      throw std::runtime_error("graph has a bridge");
  return incident;
}

static void clause(
    CaDiCaL::Solver &solver, std::initializer_list<int> literals) {
  for (int literal : literals) solver.add(literal);
  solver.add(0);
}

static bool tait_sat(
    const Edges &edges, const std::vector<std::vector<int>> &incident) {
  CaDiCaL::Solver solver;
  auto x = [](int edge, int color) { return 3 * edge + color + 1; };
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    clause(solver, {x(edge,0), x(edge,1), x(edge,2)});
    clause(solver, {-x(edge,0), -x(edge,1)});
    clause(solver, {-x(edge,0), -x(edge,2)});
    clause(solver, {-x(edge,1), -x(edge,2)});
  }
  for (const auto &row : incident)
    for (int color = 0; color < 3; ++color) {
      clause(solver, {x(row[0],color),x(row[1],color),x(row[2],color)});
      clause(solver, {-x(row[0],color),-x(row[1],color)});
      clause(solver, {-x(row[0],color),-x(row[2],color)});
      clause(solver, {-x(row[1],color),-x(row[2],color)});
    }
  int result = solver.solve();
  if (result == 20) return false;
  if (result != 10) throw std::runtime_error("Tait solver returned UNKNOWN");
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    int count = 0;
    for (int color = 0; color < 3; ++color)
      count += solver.val(x(edge, color)) > 0;
    if (count != 1) throw std::runtime_error("bad Tait edge model");
  }
  for (const auto &row : incident)
    for (int color = 0; color < 3; ++color) {
      int count = 0;
      for (int edge : row) count += solver.val(x(edge, color)) > 0;
      if (count != 1) throw std::runtime_error("bad Tait vertex model");
    }
  return true;
}

static bool fivecdc_sat(
    const Edges &edges,
    const std::vector<std::vector<int>> &incident,
    std::vector<int> *witness = nullptr) {
  CaDiCaL::Solver solver;
  auto x = [](int edge, int coordinate) {
    return 5 * edge + coordinate + 1;
  };
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    for (int a = 0; a < 5; ++a)
      for (int b = a + 1; b < 5; ++b)
        for (int c = b + 1; c < 5; ++c)
          clause(solver, {-x(edge,a), -x(edge,b), -x(edge,c)});
    for (int omitted = 0; omitted < 5; ++omitted) {
      for (int coordinate = 0; coordinate < 5; ++coordinate)
        if (coordinate != omitted) solver.add(x(edge, coordinate));
      solver.add(0);
    }
  }
  for (const auto &row : incident)
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
      int a = x(row[0], coordinate);
      int b = x(row[1], coordinate);
      int c = x(row[2], coordinate);
      clause(solver, {-a,-b,-c});
      clause(solver, {-a, b, c});
      clause(solver, { a,-b, c});
      clause(solver, { a, b,-c});
    }
  int result = solver.solve();
  if (result == 20) return false;
  if (result != 10)
    throw std::runtime_error("FiveCDC solver returned UNKNOWN");
  std::vector<int> labels(edges.size(), 0);
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    int count = 0;
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
      bool present = solver.val(x(edge, coordinate)) > 0;
      count += present;
      if (present) labels[edge] |= 1 << coordinate;
    }
    if (count != 2) throw std::runtime_error("bad FiveCDC edge model");
  }
  for (const auto &row : incident)
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
      int parity = 0;
      for (int edge : row)
        parity ^= solver.val(x(edge, coordinate)) > 0;
      if (parity) throw std::runtime_error("bad FiveCDC parity model");
    }
  if (witness) *witness = std::move(labels);
  return true;
}

int main(int argc, char **argv) {
  bool emit_nontait =
      argc == 2 && std::string(argv[1]) == "--emit-nontait";
  if (argc > 2 || (argc == 2 && !emit_nontait)) {
    std::cerr << "usage: check_d5_frontier2_graphs [--emit-nontait]\n";
    return 2;
  }
  uint64_t graphs = 0;
  uint64_t tait = 0;
  uint64_t fivecdc = 0;
  uint64_t non_tait_fivecdc = 0;
  std::string line;
  while (std::getline(std::cin, line)) {
    if (line.empty() || line.rfind(">>", 0) == 0) continue;
    auto [vertices, edges] = parse_graph6(line);
    auto incident = validate_graph(vertices, edges);
    bool has_tait = tait_sat(edges, incident);
    std::vector<int> labels;
    bool has_fivecdc = fivecdc_sat(edges, incident, &labels);
    ++graphs;
    tait += has_tait;
    fivecdc += has_fivecdc;
    non_tait_fivecdc += !has_tait && has_fivecdc;
    if (!has_fivecdc) {
      std::cout << "{\"classification\":\"FIVECDC_UNSAT_CANDIDATE\","
                << "\"index\":" << graphs << ",\"graph6\":\"" << line
                << "\"}\n";
      return 20;
    }
    if (emit_nontait && !has_tait) {
      std::cerr << "{\"canonical_index\":" << graphs
                << ",\"graph6\":\"" << line
                << "\",\"fivecdc_label_masks\":[";
      for (int edge = 0; edge < static_cast<int>(labels.size()); ++edge) {
        if (edge) std::cerr << ",";
        std::cerr << labels[edge];
      }
      std::cerr << "]}\n";
    }
  }
  std::cout << "{\"classification\":\"ALL_FIVECDC_SAT\","
            << "\"graphs\":" << graphs << ",\"tait\":" << tait
            << ",\"non_tait\":" << (graphs - tait)
            << ",\"fivecdc\":" << fivecdc
            << ",\"non_tait_fivecdc\":" << non_tait_fivecdc << "}\n";
  return 0;
}
