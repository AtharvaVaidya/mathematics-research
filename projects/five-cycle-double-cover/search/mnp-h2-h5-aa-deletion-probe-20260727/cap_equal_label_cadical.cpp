#include <cadical.hpp>

#include <algorithm>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

struct Graph {
  int vertices = 0;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::vector<int>> incident;
};

Graph parse_graph6(const std::string& record) {
  if (record.empty()) {
    throw std::runtime_error("empty graph6 record");
  }
  Graph graph;
  std::size_t data_position = 1;
  if (static_cast<unsigned char>(record[0]) == 126) {
    if (record.size() < 4 || static_cast<unsigned char>(record[1]) == 126) {
      throw std::runtime_error("unsupported graph6 order header");
    }
    for (int position = 1; position <= 3; ++position) {
      const int value = static_cast<unsigned char>(record[position]) - 63;
      if (value < 0 || value >= 64) {
        throw std::runtime_error("bad graph6 order header");
      }
      graph.vertices = 64 * graph.vertices + value;
    }
    data_position = 4;
  } else {
    graph.vertices = static_cast<unsigned char>(record[0]) - 63;
  }
  if (graph.vertices < 0 || graph.vertices > 258047) {
    throw std::runtime_error("bad graph order");
  }

  std::vector<int> bits;
  for (std::size_t position = data_position; position < record.size();
       ++position) {
    const int value = static_cast<unsigned char>(record[position]) - 63;
    if (value < 0 || value >= 64) {
      throw std::runtime_error("bad graph6 character");
    }
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }

  std::size_t cursor = 0;
  for (int right = 1; right < graph.vertices; ++right) {
    for (int left = 0; left < right; ++left) {
      if (cursor >= bits.size()) {
        throw std::runtime_error("short graph6 record");
      }
      if (bits[cursor]) {
        graph.edges.emplace_back(left, right);
      }
      ++cursor;
    }
  }
  if (graph.edges.size() * 2 !=
      static_cast<std::size_t>(3 * graph.vertices)) {
    throw std::runtime_error("input is not cubic");
  }

  graph.incident.assign(graph.vertices, {});
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    const auto [left, right] = graph.edges[edge];
    graph.incident[left].push_back(edge);
    graph.incident[right].push_back(edge);
  }
  if (std::any_of(graph.incident.begin(), graph.incident.end(),
                  [](const auto& row) { return row.size() != 3; })) {
    throw std::runtime_error("input is not cubic");
  }
  return graph;
}

std::vector<int> d5_values() {
  std::vector<int> result;
  for (int value = 0; value < 32; ++value) {
    if (std::popcount(static_cast<unsigned>(value)) == 2) {
      result.push_back(value);
    }
  }
  if (result.size() != 10) {
    throw std::runtime_error("D5 construction failed");
  }
  return result;
}

int variable(int edge, int label) { return 1 + 10 * edge + label; }

class EqualLabelSolver {
 public:
  explicit EqualLabelSolver(const Graph& graph)
      : graph_(graph), values_(d5_values()) {
    for (int edge = 0; edge < static_cast<int>(graph_.edges.size()); ++edge) {
      for (int label = 0; label < 10; ++label) {
        solver_.add(variable(edge, label));
      }
      solver_.add(0);
      for (int left = 0; left < 10; ++left) {
        for (int right = left + 1; right < 10; ++right) {
          solver_.add(-variable(edge, left));
          solver_.add(-variable(edge, right));
          solver_.add(0);
        }
      }
    }

    for (const auto& edges : graph_.incident) {
      for (int left = 0; left < 10; ++left) {
        for (int right = 0; right < 10; ++right) {
          const int target_value = values_[left] ^ values_[right];
          const auto found =
              std::find(values_.begin(), values_.end(), target_value);
          solver_.add(-variable(edges[0], left));
          solver_.add(-variable(edges[1], right));
          if (found != values_.end()) {
            const int forced = static_cast<int>(found - values_.begin());
            solver_.add(variable(edges[2], forced));
          }
          solver_.add(0);
        }
      }
    }
  }

  bool solve_equal(int first, int second) {
    // By the global S5 symmetry, equality in any D5 label is equivalent
    // to assigning both prescribed edges the representative label 0011.
    solver_.assume(variable(first, 0));
    solver_.assume(variable(second, 0));
    const int result = solver_.solve();
    if (result == 10) {
      return true;
    }
    if (result == 20) {
      return false;
    }
    throw std::runtime_error("CaDiCaL returned UNKNOWN");
  }

  std::string model() {
    std::string result;
    result.reserve(graph_.edges.size());
    for (int edge = 0; edge < static_cast<int>(graph_.edges.size()); ++edge) {
      int selected = -1;
      for (int label = 0; label < 10; ++label) {
        if (solver_.val(variable(edge, label)) > 0) {
          if (selected >= 0) {
            throw std::runtime_error("model gives two labels to one edge");
          }
          selected = label;
        }
      }
      if (selected < 0) {
        throw std::runtime_error("model leaves an edge unlabelled");
      }
      result.push_back(static_cast<char>('0' + selected));
    }
    return result;
  }

 private:
  const Graph& graph_;
  std::vector<int> values_;
  CaDiCaL::Solver solver_;
};

}  // namespace

int main(int argc, char** argv) {
  std::uint64_t progress = 0;
  for (int index = 1; index < argc; ++index) {
    const std::string option = argv[index];
    if (option == "--progress" && index + 1 < argc) {
      progress = std::strtoull(argv[++index], nullptr, 10);
    } else {
      std::cerr << "usage: cap_equal_label_cadical [--progress N]\n";
      return 2;
    }
  }

  std::uint64_t graphs = 0;
  std::uint64_t queries = 0;
  std::uint64_t sat = 0;
  std::uint64_t pairs = 0;
  std::string record;
  while (std::getline(std::cin, record)) {
    if (record.empty()) {
      continue;
    }
    try {
      const Graph graph = parse_graph6(record);
      EqualLabelSolver solver(graph);
      ++graphs;
      std::vector<std::pair<int, int>> independent_pairs;
      for (int first = 0; first < static_cast<int>(graph.edges.size());
           ++first) {
        const auto [a, b] = graph.edges[first];
        for (int second = first + 1;
             second < static_cast<int>(graph.edges.size()); ++second) {
          const auto [c, d] = graph.edges[second];
          if (a == c || a == d || b == c || b == d) {
            continue;
          }
          independent_pairs.emplace_back(first, second);
        }
      }

      pairs += independent_pairs.size();
      std::vector<bool> covered(independent_pairs.size(), false);
      std::size_t covered_count = 0;
      std::uint64_t certificates = 0;
      while (covered_count != independent_pairs.size()) {
        const auto next = std::find(covered.begin(), covered.end(), false);
        const std::size_t pivot =
            static_cast<std::size_t>(next - covered.begin());
        const auto [first, second] = independent_pairs[pivot];
        ++queries;
        if (!solver.solve_equal(first, second)) {
          std::cerr << "UNSAT graph=" << graphs << " first=" << first
                    << " second=" << second << '\n';
          return 4;
        }
        ++sat;
        ++certificates;
        const std::string model = solver.model();
        std::size_t newly_covered = 0;
        for (std::size_t index = 0; index < independent_pairs.size();
             ++index) {
          if (covered[index]) {
            continue;
          }
          const auto [left, right] = independent_pairs[index];
          if (model[left] == model[right]) {
            covered[index] = true;
            ++covered_count;
            ++newly_covered;
          }
        }
        if (newly_covered == 0) {
          throw std::runtime_error("SAT model does not cover its pivot pair");
        }
        std::cout << graphs << '\t' << certificates << '\t' << first << '\t'
                  << second << '\t' << newly_covered << '\t' << model
                  << '\n';
        if (progress != 0 && certificates % progress == 0) {
          std::cerr << "progress graph=" << graphs
                    << " certificates=" << certificates
                    << " covered=" << covered_count
                    << " pairs=" << independent_pairs.size() << '\n';
        }
      }
      std::cerr << "GRAPH graph=" << graphs
                << " vertices=" << graph.vertices
                << " edges=" << graph.edges.size()
                << " pairs=" << independent_pairs.size()
                << " certificates=" << certificates << '\n';
    } catch (const std::exception& error) {
      std::cerr << "ERROR graph=" << (graphs + 1)
                << " message=" << error.what() << '\n';
      return 3;
    }
  }

  std::cerr << "SUMMARY implementation=cadical mode=cap-equal-label"
            << " graphs=" << graphs << " queries=" << queries
            << " sat=" << sat << " unsat=" << (queries - sat)
            << " pairs=" << pairs << '\n';
  return 0;
}
