#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <queue>
#include <random>
#include <set>
#include <stdexcept>
#include <utility>
#include <vector>

using CaDiCaL::Solver;

namespace {

struct Graph {
  int vertices = 0;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::vector<int>> incidence;
};

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

Graph random_graph(int blocks, std::mt19937_64 &random) {
  Graph graph;
  graph.vertices = 5 * blocks;
  graph.incidence.resize(graph.vertices);
  for (int block = 0; block < blocks; ++block) {
    for (int offset = 0; offset < 5; ++offset) {
      int left = 5 * block + offset;
      int right = 5 * block + (offset + 1) % 5;
      if (left > right) std::swap(left, right);
      graph.edges.emplace_back(left, right);
    }
  }

  std::vector<int> unmatched(graph.vertices);
  std::iota(unmatched.begin(), unmatched.end(), 0);
  for (int restart = 0;; ++restart) {
    if (restart > 10000) throw std::runtime_error("matching restart limit");
    std::shuffle(unmatched.begin(), unmatched.end(), random);
    std::vector<std::pair<int, int>> matching;
    std::vector<char> used(graph.vertices, false);
    bool failed = false;
    for (int position = 0; position < graph.vertices; ++position) {
      int left = unmatched[position];
      if (used[left]) continue;
      int choice = -1;
      for (int scan = position + 1; scan < graph.vertices; ++scan) {
        int right = unmatched[scan];
        if (!used[right] && left / 5 != right / 5) {
          choice = right;
          break;
        }
      }
      if (choice < 0) {
        failed = true;
        break;
      }
      used[left] = used[choice] = true;
      if (left > choice) std::swap(left, choice);
      matching.emplace_back(left, choice);
    }
    if (!failed && matching.size() * 2 == static_cast<std::size_t>(
                                                graph.vertices)) {
      graph.edges.insert(graph.edges.end(), matching.begin(), matching.end());
      break;
    }
  }

  std::sort(graph.edges.begin(), graph.edges.end());
  for (int edge_id = 0; edge_id < static_cast<int>(graph.edges.size());
       ++edge_id) {
    auto [left, right] = graph.edges[edge_id];
    graph.incidence[left].push_back(edge_id);
    graph.incidence[right].push_back(edge_id);
  }
  for (const auto &row : graph.incidence)
    if (row.size() != 3) throw std::runtime_error("noncubic construction");
  return graph;
}

Graph random_complete_coordinate_cover(int coordinates,
                                       std::mt19937_64 &random) {
  if (coordinates < 4 || coordinates > 8)
    throw std::runtime_error("coordinate count must lie from 4 through 8");
  std::vector<std::array<int, 3>> triangles;
  for (int first = 0; first < coordinates; ++first)
    for (int second = first + 1; second < coordinates; ++second)
      for (int third = second + 1; third < coordinates; ++third)
        triangles.push_back({first, second, third});

  Graph graph;
  graph.vertices = 2 * triangles.size();
  graph.incidence.resize(graph.vertices);
  std::vector<std::vector<int>> sockets(coordinates * coordinates);
  for (int copy = 0; copy < 2; ++copy) {
    for (int triangle_id = 0;
         triangle_id < static_cast<int>(triangles.size()); ++triangle_id) {
      const int vertex = copy * triangles.size() + triangle_id;
      const auto triangle = triangles[triangle_id];
      for (int left_index = 0; left_index < 3; ++left_index)
        for (int right_index = left_index + 1; right_index < 3;
             ++right_index) {
          const int left = triangle[left_index];
          const int right = triangle[right_index];
          sockets[left * coordinates + right].push_back(vertex);
        }
    }
  }

  for (int construction_restart = 0;; ++construction_restart) {
    if (construction_restart > 10000)
      throw std::runtime_error("coordinate-cover restart limit");
    graph.edges.clear();
    std::set<std::pair<int, int>> used_pairs;
    bool failed = false;
    for (int left = 0; left < coordinates && !failed; ++left) {
      for (int right = left + 1; right < coordinates && !failed; ++right) {
        auto row = sockets[left * coordinates + right];
        bool row_done = false;
        for (int row_restart = 0; row_restart < 1000 && !row_done;
             ++row_restart) {
          std::shuffle(row.begin(), row.end(), random);
          std::vector<std::pair<int, int>> proposed;
          bool valid = true;
          for (int position = 0; position < static_cast<int>(row.size());
               position += 2) {
            int first = row[position], second = row[position + 1];
            if (first > second) std::swap(first, second);
            if (first == second || used_pairs.count({first, second})) {
              valid = false;
              break;
            }
            proposed.emplace_back(first, second);
          }
          if (!valid) continue;
          for (auto edge : proposed) {
            used_pairs.insert(edge);
            graph.edges.push_back(edge);
          }
          row_done = true;
        }
        if (!row_done) failed = true;
      }
    }
    if (!failed) break;
  }

  std::sort(graph.edges.begin(), graph.edges.end());
  graph.incidence.assign(graph.vertices, {});
  for (int edge_id = 0; edge_id < static_cast<int>(graph.edges.size());
       ++edge_id) {
    auto [left, right] = graph.edges[edge_id];
    graph.incidence[left].push_back(edge_id);
    graph.incidence[right].push_back(edge_id);
  }
  for (const auto &row : graph.incidence)
    if (row.size() != 3)
      throw std::runtime_error("coordinate-cover graph is not cubic");
  return graph;
}

bool connected_and_bridgeless(const Graph &graph) {
  int timer = 0;
  std::vector<int> discovery(graph.vertices, -1), low(graph.vertices, -1);
  bool bridge = false;
  int seen = 0;
  auto visit = [&](auto &&self, int vertex, int parent_edge) -> void {
    discovery[vertex] = low[vertex] = timer++;
    ++seen;
    for (int edge_id : graph.incidence[vertex]) {
      if (edge_id == parent_edge) continue;
      const auto [left, right] = graph.edges[edge_id];
      const int other = left == vertex ? right : left;
      if (discovery[other] < 0) {
        self(self, other, edge_id);
        low[vertex] = std::min(low[vertex], low[other]);
        if (low[other] > discovery[vertex]) bridge = true;
      } else {
        low[vertex] = std::min(low[vertex], discovery[other]);
      }
    }
  };
  visit(visit, 0, -1);
  return seen == graph.vertices && !bridge;
}

bool tait_colorable(const Graph &graph) {
  Solver solver;
  solver.set("quiet", 1);
  const int edge_count = graph.edges.size();
  auto variable = [edge_count](int color, int edge_id) {
    return color * edge_count + edge_id + 1;
  };
  for (int edge_id = 0; edge_id < edge_count; ++edge_id) {
    add_clause(solver, {variable(0, edge_id), variable(1, edge_id),
                        variable(2, edge_id)});
    for (int first = 0; first < 3; ++first)
      for (int second = first + 1; second < 3; ++second)
        add_clause(solver, {-variable(first, edge_id),
                            -variable(second, edge_id)});
  }
  for (const auto &row : graph.incidence) {
    for (int color = 0; color < 3; ++color) {
      add_clause(solver, {variable(color, row[0]), variable(color, row[1]),
                          variable(color, row[2])});
      for (int first = 0; first < 3; ++first)
        for (int second = first + 1; second < 3; ++second)
          add_clause(solver, {-variable(color, row[first]),
                              -variable(color, row[second])});
    }
  }
  // Global color symmetry.
  add_clause(solver, {variable(0, 0)});
  return solver.solve() == 10;
}

bool fivecdc(const Graph &graph, std::vector<int> *model_labels) {
  Solver solver;
  solver.set("quiet", 1);
  const int edge_count = graph.edges.size();
  for (int edge_id = 0; edge_id < edge_count; ++edge_id) {
    std::array<int, 5> variables{};
    for (int coordinate = 0; coordinate < 5; ++coordinate)
      variables[coordinate] = 5 * edge_id + coordinate + 1;
    add_exactly_two(solver, variables);
  }
  for (const auto &row : graph.incidence)
    for (int coordinate = 0; coordinate < 5; ++coordinate)
      add_even_three(solver, 5 * row[0] + coordinate + 1,
                     5 * row[1] + coordinate + 1,
                     5 * row[2] + coordinate + 1);
  // Global S5 symmetry: the first edge can be labelled 01.
  add_clause(solver, {1});
  add_clause(solver, {2});
  add_clause(solver, {-3});
  add_clause(solver, {-4});
  add_clause(solver, {-5});
  const int result = solver.solve();
  if (result == 10 && model_labels) {
    model_labels->clear();
    for (int edge_id = 0; edge_id < edge_count; ++edge_id) {
      int label = 0;
      for (int coordinate = 0; coordinate < 5; ++coordinate)
        if (solver.val(5 * edge_id + coordinate + 1) > 0)
          label |= 1 << coordinate;
      model_labels->push_back(label);
    }
    for (int label : *model_labels)
      if (__builtin_popcount(static_cast<unsigned>(label)) != 2)
        throw std::runtime_error("FiveCDC model violates edge weight two");
    for (const auto &row : graph.incidence) {
      const int parity = (*model_labels)[row[0]] ^
                         (*model_labels)[row[1]] ^
                         (*model_labels)[row[2]];
      if (parity != 0)
        throw std::runtime_error("FiveCDC model violates vertex parity");
    }
  }
  if (result != 10 && result != 20)
    throw std::runtime_error("FiveCDC solver returned UNKNOWN");
  return result == 10;
}

void print_graph(const Graph &graph, const std::string &family,
                 std::uint64_t seed, std::uint64_t sample) {
  std::cout << "CANDIDATE family " << family << " seed " << seed
            << " sample " << sample << " vertices " << graph.vertices
            << " edges " << graph.edges.size() << '\n';
  for (int edge_id = 0; edge_id < static_cast<int>(graph.edges.size());
       ++edge_id)
    std::cout << edge_id << ' ' << graph.edges[edge_id].first << ' '
              << graph.edges[edge_id].second << '\n';
}

}  // namespace

int main(int argc, char **argv) {
  try {
    if (argc != 5) {
      std::cerr
          << "usage: random-search (BLOCKS|K7|K8) SAMPLES SEED "
             "PROGRESS_INTERVAL\n";
      return 2;
    }
    const std::string family = argv[1];
    int blocks = 0, coordinates = 0;
    if (family.size() >= 2 && family[0] == 'K') {
      coordinates = std::stoi(family.substr(1));
    } else {
      blocks = std::stoi(family);
    }
    const std::uint64_t samples = std::stoull(argv[2]);
    const std::uint64_t seed = std::stoull(argv[3]);
    const std::uint64_t progress = std::stoull(argv[4]);
    if (!coordinates && (blocks < 2 || blocks % 2))
      throw std::runtime_error("BLOCKS must be positive and even");
    std::mt19937_64 random(seed);
    std::uint64_t bridgeless = 0, snarks = 0, sat = 0;
    for (std::uint64_t sample = 0; sample < samples; ++sample) {
      Graph graph = coordinates
                        ? random_complete_coordinate_cover(coordinates, random)
                        : random_graph(blocks, random);
      if (!connected_and_bridgeless(graph)) continue;
      ++bridgeless;
      if (tait_colorable(graph)) continue;
      ++snarks;
      std::vector<int> labels;
      if (!fivecdc(graph, &labels)) {
        print_graph(graph, family, seed, sample);
        return 1;
      }
      ++sat;
      if (progress && (sample + 1) % progress == 0)
        std::cerr << "progress " << (sample + 1) << " bridgeless "
                  << bridgeless << " snarks " << snarks << " sat " << sat
                  << '\n';
    }
    std::cout << "PASS family " << family << " samples " << samples
              << " seed " << seed << " bridgeless " << bridgeless
              << " snarks " << snarks << " fivecdc_sat " << sat << '\n';
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "ERROR " << error.what() << '\n';
    return 2;
  }
}
