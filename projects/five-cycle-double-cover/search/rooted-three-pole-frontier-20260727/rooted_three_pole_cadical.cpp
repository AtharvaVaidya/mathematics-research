#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

struct Graph {
  int vertices = 0;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::vector<int>> proper_incidence;
  std::vector<std::array<int, 3>> cubic_incidence;
};

Graph decode_graph6(const std::string& record) {
  if (record.empty() || static_cast<unsigned char>(record.front()) == 126) {
    throw std::runtime_error("only short graph6 records are supported");
  }
  Graph graph;
  graph.vertices = static_cast<unsigned char>(record.front()) - 63;
  if (graph.vertices < 1 || graph.vertices > 62) {
    throw std::runtime_error("invalid graph order");
  }

  std::vector<unsigned char> payload;
  for (std::size_t position = 1; position < record.size(); ++position) {
    const int value = static_cast<unsigned char>(record[position]) - 63;
    if (value < 0 || value > 63) {
      throw std::runtime_error("invalid graph6 payload");
    }
    payload.push_back(static_cast<unsigned char>(value));
  }

  graph.proper_incidence.resize(graph.vertices);
  std::size_t bit = 0;
  for (int right = 1; right < graph.vertices; ++right) {
    for (int left = 0; left < right; ++left, ++bit) {
      if (bit / 6 >= payload.size()) {
        throw std::runtime_error("truncated graph6 payload");
      }
      if ((payload[bit / 6] >> (5 - bit % 6)) & 1U) {
        const int edge = static_cast<int>(graph.edges.size());
        graph.edges.emplace_back(left, right);
        graph.proper_incidence[left].push_back(edge);
        graph.proper_incidence[right].push_back(edge);
      }
    }
  }

  std::vector<int> terminals;
  for (int vertex = 0; vertex < graph.vertices; ++vertex) {
    const auto degree = graph.proper_incidence[vertex].size();
    if (degree == 2) {
      terminals.push_back(vertex);
    } else if (degree != 3) {
      throw std::runtime_error("input degrees are not two/three");
    }
  }
  if (terminals.size() != 3) {
    throw std::runtime_error("expected exactly three degree-two terminals");
  }

  graph.cubic_incidence.reserve(graph.vertices);
  const int first_boundary = static_cast<int>(graph.edges.size());
  std::vector<int> terminal_position(graph.vertices, -1);
  for (int position = 0; position < 3; ++position) {
    terminal_position[terminals[position]] = position;
  }
  for (int vertex = 0; vertex < graph.vertices; ++vertex) {
    auto row = graph.proper_incidence[vertex];
    if (terminal_position[vertex] >= 0) {
      row.push_back(first_boundary + terminal_position[vertex]);
    }
    if (row.size() != 3) {
      throw std::runtime_error("failed to cubicize the incidence");
    }
    graph.cubic_incidence.push_back({row[0], row[1], row[2]});
  }
  return graph;
}

std::array<int, 10> labels() {
  std::array<int, 10> result{};
  int cursor = 0;
  for (int value = 0; value < 32; ++value) {
    if (std::popcount(static_cast<unsigned>(value)) == 2) {
      result[cursor++] = value;
    }
  }
  if (cursor != 10) {
    throw std::runtime_error("failed to construct D5");
  }
  return result;
}

std::array<int, 32> inverse_labels(const std::array<int, 10>& values) {
  std::array<int, 32> inverse{};
  inverse.fill(-1);
  for (int label = 0; label < 10; ++label) {
    inverse[values[label]] = label;
  }
  return inverse;
}

int orbit_of(int value) {
  switch (value) {
    case 0b00011:
      return 0;
    case 0b00101:
      return 1;
    case 0b00110:
      return 2;
    case 0b01001:
    case 0b10001:
      return 3;
    case 0b01010:
    case 0b10010:
      return 4;
    case 0b01100:
    case 0b10100:
      return 5;
    case 0b11000:
      return 6;
    default:
      throw std::runtime_error("label outside D5");
  }
}

class RootedSat {
 public:
  explicit RootedSat(const Graph& graph)
      : graph_(graph), values_(labels()), inverse_(inverse_labels(values_)) {
    const int edge_count = static_cast<int>(graph_.edges.size()) + 3;
    for (int edge = 0; edge < edge_count; ++edge) {
      for (int label = 0; label < 10; ++label) {
        solver_.add(variable(edge, label));
      }
      solver_.add(0);
      for (int first = 0; first < 10; ++first) {
        for (int second = first + 1; second < 10; ++second) {
          solver_.add(-variable(edge, first));
          solver_.add(-variable(edge, second));
          solver_.add(0);
        }
      }
    }

    for (const auto& incident : graph_.cubic_incidence) {
      for (int first = 0; first < 10; ++first) {
        for (int second = 0; second < 10; ++second) {
          solver_.add(-variable(incident[0], first));
          solver_.add(-variable(incident[1], second));
          const int third = inverse_[values_[first] ^ values_[second]];
          if (third >= 0) {
            solver_.add(variable(incident[2], third));
          }
          solver_.add(0);
        }
      }
    }

    const int first_boundary = static_cast<int>(graph_.edges.size());
    fix(first_boundary + 0, inverse_[0b00011]);
    fix(first_boundary + 1, inverse_[0b00101]);
    fix(first_boundary + 2, inverse_[0b00110]);
  }

  bool solve(int root, int label) {
    solver_.assume(variable(root, label));
    const int result = solver_.solve();
    if (result == 10) {
      return true;
    }
    if (result == 20) {
      return false;
    }
    throw std::runtime_error("CaDiCaL returned UNKNOWN");
  }

  const std::array<int, 10>& values() const { return values_; }

 private:
  static int variable(int edge, int label) { return 1 + 10 * edge + label; }

  void fix(int edge, int label) {
    if (label < 0) {
      throw std::runtime_error("invalid fixed boundary label");
    }
    solver_.add(variable(edge, label));
    solver_.add(0);
  }

  const Graph& graph_;
  std::array<int, 10> values_;
  std::array<int, 32> inverse_;
  CaDiCaL::Solver solver_;
};

bool bridge_without_semiedges(const Graph& graph, int removed) {
  const int start = graph.edges[removed].first;
  std::vector<bool> reached(graph.vertices, false);
  std::vector<int> stack = {start};
  reached[start] = true;
  while (!stack.empty()) {
    const int vertex = stack.back();
    stack.pop_back();
    for (int edge : graph.proper_incidence[vertex]) {
      if (edge == removed) {
        continue;
      }
      const auto [left, right] = graph.edges[edge];
      const int other = left == vertex ? right : left;
      if (!reached[other]) {
        reached[other] = true;
        stack.push_back(other);
      }
    }
  }
  return std::find(reached.begin(), reached.end(), false) != reached.end();
}

int main(int argc, char** argv) {
  bool all = false;
  if (argc == 2 && std::string(argv[1]) == "--all") {
    all = true;
  } else if (argc != 1) {
    std::cerr << "usage: rooted_three_pole_cadical [--all]\n";
    return 2;
  }

  std::uint64_t graphs = 0;
  std::uint64_t roots = 0;
  std::uint64_t singleton = 0;
  std::uint64_t singleton_nonbridge = 0;
  std::map<int, std::uint64_t> size_profile;
  std::string record;
  while (std::getline(std::cin, record)) {
    if (record.empty()) {
      continue;
    }
    try {
      const Graph graph = decode_graph6(record);
      RootedSat solver(graph);
      ++graphs;
      for (int root = 0; root < static_cast<int>(graph.edges.size()); ++root) {
        unsigned mask = 0;
        std::array<int, 7> orbit_decision{};
        orbit_decision.fill(-1);
        for (int label = 0; label < 10; ++label) {
          const int decision = solver.solve(root, label) ? 1 : 0;
          const int orbit = orbit_of(solver.values()[label]);
          if (orbit_decision[orbit] >= 0 &&
              orbit_decision[orbit] != decision) {
            throw std::runtime_error("stabilizer orbit decisions disagree");
          }
          orbit_decision[orbit] = decision;
          if (decision) {
            mask |= 1U << orbit;
          }
        }
        const bool bridge = bridge_without_semiedges(graph, root);
        const int size = std::popcount(mask);
        ++roots;
        ++size_profile[size];
        if (size == 1) {
          ++singleton;
          singleton_nonbridge += !bridge;
        }
        if (all || (size == 1 && !bridge)) {
          std::cout << record << '\t' << root << '\t' << std::hex << mask
                    << std::dec << '\t' << (bridge ? 1 : 0) << '\n';
        }
      }
    } catch (const std::exception& error) {
      std::cerr << "ERROR record=" << record << " message=" << error.what()
                << '\n';
      return 3;
    }
  }

  std::cerr << "SUMMARY graphs=" << graphs << " roots=" << roots
            << " singleton=" << singleton
            << " singleton_nonbridge=" << singleton_nonbridge
            << " size_profile=";
  bool first = true;
  for (const auto& [size, count] : size_profile) {
    if (!first) {
      std::cerr << ',';
    }
    first = false;
    std::cerr << size << ':' << count;
  }
  std::cerr << '\n';
  return 0;
}
