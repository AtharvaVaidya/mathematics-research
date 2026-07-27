#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

constexpr std::uint16_t kAllLabels = (1U << 10) - 1;

struct Graph {
  int vertices = 0;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::array<int, 3>> incident;
  std::vector<int> terminals;
};

std::array<int, 10> d_values() {
  std::array<int, 10> result{};
  int cursor = 0;
  for (int value = 0; value < 32; ++value) {
    if (std::popcount(static_cast<unsigned>(value)) == 2) {
      result[cursor++] = value;
    }
  }
  if (cursor != 10) {
    throw std::runtime_error("D5 construction failed");
  }
  return result;
}

std::array<int, 32> label_indices(const std::array<int, 10>& values) {
  std::array<int, 32> result{};
  result.fill(-1);
  for (int label = 0; label < 10; ++label) {
    result[values[label]] = label;
  }
  return result;
}

Graph parse_graph6(const std::string& record) {
  if (record.empty() || static_cast<unsigned char>(record[0]) == 126) {
    throw std::runtime_error("only short graph6 records are supported");
  }
  Graph graph;
  graph.vertices = static_cast<unsigned char>(record[0]) - 63;
  if (graph.vertices < 0 || graph.vertices > 62) {
    throw std::runtime_error("bad graph order");
  }
  std::vector<int> bits;
  for (std::size_t position = 1; position < record.size(); ++position) {
    const int value = static_cast<unsigned char>(record[position]) - 63;
    if (value < 0 || value >= 64) {
      throw std::runtime_error("bad graph6 character");
    }
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }
  std::vector<std::vector<int>> incidence(graph.vertices);
  std::size_t cursor = 0;
  for (int right = 1; right < graph.vertices; ++right) {
    for (int left = 0; left < right; ++left) {
      if (cursor >= bits.size()) {
        throw std::runtime_error("short graph6 record");
      }
      if (bits[cursor]) {
        const int edge = static_cast<int>(graph.edges.size());
        graph.edges.emplace_back(left, right);
        incidence[left].push_back(edge);
        incidence[right].push_back(edge);
      }
      ++cursor;
    }
  }
  for (int vertex = 0; vertex < graph.vertices; ++vertex) {
    if (incidence[vertex].size() == 2) {
      graph.terminals.push_back(vertex);
    } else if (incidence[vertex].size() != 3) {
      throw std::runtime_error("input is not degree two/three");
    }
  }
  if (graph.terminals.size() != 3) {
    throw std::runtime_error("expected three terminals");
  }
  const int first_boundary = static_cast<int>(graph.edges.size());
  for (int position = 0; position < 3; ++position) {
    incidence[graph.terminals[position]].push_back(first_boundary + position);
  }
  graph.incident.reserve(graph.vertices);
  for (const auto& row : incidence) {
    if (row.size() != 3) {
      throw std::runtime_error("bad cubic incidence");
    }
    graph.incident.push_back({row[0], row[1], row[2]});
  }
  return graph;
}

class RootedCsp {
 public:
  explicit RootedCsp(const Graph& graph)
      : graph_(graph),
        values_(d_values()),
        label_index_(label_indices(values_)) {}

  bool solve(int root, int root_label) const {
    const int first_boundary = static_cast<int>(graph_.edges.size());
    std::vector<std::uint16_t> domains(first_boundary + 3, kAllLabels);
    domains[first_boundary + 0] = 1U << label_index_[0b00011];
    domains[first_boundary + 1] = 1U << label_index_[0b00101];
    domains[first_boundary + 2] = 1U << label_index_[0b00110];
    domains[root] = 1U << root_label;
    return search(std::move(domains));
  }

 private:
  std::uint16_t supported(std::uint16_t own, std::uint16_t other1,
                          std::uint16_t other2) const {
    std::uint16_t result = 0;
    for (int first = 0; first < 10; ++first) {
      if (!((own >> first) & 1U)) {
        continue;
      }
      for (int second = 0; second < 10; ++second) {
        if (!((other1 >> second) & 1U)) {
          continue;
        }
        const int third = label_index_[values_[first] ^ values_[second]];
        if (third >= 0 && ((other2 >> third) & 1U)) {
          result |= 1U << first;
          break;
        }
      }
    }
    return result;
  }

  bool propagate(std::vector<std::uint16_t>& domains) const {
    bool changed = true;
    while (changed) {
      changed = false;
      for (const auto& edges : graph_.incident) {
        const auto first =
            supported(domains[edges[0]], domains[edges[1]], domains[edges[2]]);
        const auto second =
            supported(domains[edges[1]], domains[edges[0]], domains[edges[2]]);
        const auto third =
            supported(domains[edges[2]], domains[edges[0]], domains[edges[1]]);
        if (first == 0 || second == 0 || third == 0) {
          return false;
        }
        if (first != domains[edges[0]]) {
          domains[edges[0]] = first;
          changed = true;
        }
        if (second != domains[edges[1]]) {
          domains[edges[1]] = second;
          changed = true;
        }
        if (third != domains[edges[2]]) {
          domains[edges[2]] = third;
          changed = true;
        }
      }
    }
    return true;
  }

  bool search(std::vector<std::uint16_t> domains) const {
    if (!propagate(domains)) {
      return false;
    }
    int edge = -1;
    int size = 11;
    for (int candidate = 0; candidate < static_cast<int>(domains.size());
         ++candidate) {
      const int candidate_size = std::popcount(domains[candidate]);
      if (candidate_size > 1 && candidate_size < size) {
        edge = candidate;
        size = candidate_size;
      }
    }
    if (edge < 0) {
      return true;
    }
    std::uint16_t choices = domains[edge];
    while (choices != 0) {
      const std::uint16_t bit =
          static_cast<std::uint16_t>(choices & -choices);
      choices = static_cast<std::uint16_t>(choices - bit);
      auto child = domains;
      child[edge] = bit;
      if (search(std::move(child))) {
        return true;
      }
    }
    return false;
  }

  const Graph& graph_;
  std::array<int, 10> values_;
  std::array<int, 32> label_index_;
};

bool is_bridge(const Graph& graph, int removed) {
  const auto [start, ignored] = graph.edges[removed];
  static_cast<void>(ignored);
  std::vector<bool> reached(graph.vertices, false);
  reached[start] = true;
  std::vector<int> stack = {start};
  while (!stack.empty()) {
    const int vertex = stack.back();
    stack.pop_back();
    for (int edge : graph.incident[vertex]) {
      if (edge >= static_cast<int>(graph.edges.size()) || edge == removed) {
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

int root_orbit(int value) {
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
      throw std::runtime_error("root label outside D5");
  }
}

int main(int argc, char** argv) {
  bool all = false;
  if (argc == 2 && std::string(argv[1]) == "--all") {
    all = true;
  } else if (argc != 1) {
    std::cerr << "usage: rooted_three_pole_csp [--all]\n";
    return 2;
  }

  const auto values = d_values();
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
      const Graph graph = parse_graph6(record);
      const RootedCsp solver(graph);
      ++graphs;
      for (int root = 0; root < static_cast<int>(graph.edges.size()); ++root) {
        unsigned mask = 0;
        std::array<int, 7> decisions{};
        decisions.fill(-1);
        for (int label = 0; label < 10; ++label) {
          const int orbit = root_orbit(values[label]);
          const int result = solver.solve(root, label) ? 1 : 0;
          if (decisions[orbit] >= 0 && decisions[orbit] != result) {
            throw std::runtime_error("stabilizer orbit decisions disagree");
          }
          decisions[orbit] = result;
          if (result) {
            mask |= 1U << orbit;
          }
        }
        const bool bridge = is_bridge(graph, root);
        const int size = std::popcount(mask);
        ++roots;
        ++size_profile[size];
        if (size == 1) {
          ++singleton;
          if (!bridge) {
            ++singleton_nonbridge;
          }
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
