#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

struct Pole {
  int vertices = 0;
  int internal_edges = 0;
  std::vector<int> ports;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::vector<int>> incident;
};

Pole read_pole(const std::string &path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open pole file");
  Pole pole;
  int port_count = 0;
  input >> pole.vertices >> pole.internal_edges >> port_count;
  if (!input || pole.vertices <= 0 || pole.internal_edges < 0 ||
      port_count != 6)
    throw std::runtime_error("invalid pole header");
  pole.ports.resize(port_count);
  for (int &port : pole.ports) input >> port;
  pole.incident.resize(pole.vertices);
  for (int edge = 0; edge < pole.internal_edges; ++edge) {
    int left = -1, right = -1;
    input >> left >> right;
    if (!input || left < 0 || left >= pole.vertices || right < 0 ||
        right >= pole.vertices || left == right)
      throw std::runtime_error("invalid pole edge");
    pole.edges.push_back({left, right});
    pole.incident[left].push_back(edge);
    pole.incident[right].push_back(edge);
  }
  std::string trailing;
  if (input >> trailing) throw std::runtime_error("trailing pole input");
  for (int port = 0; port < port_count; ++port) {
    const int vertex = pole.ports[port];
    if (vertex < 0 || vertex >= pole.vertices)
      throw std::runtime_error("invalid port vertex");
    pole.incident[vertex].push_back(pole.internal_edges + port);
  }
  for (const auto &row : pole.incident)
    if (row.size() != 3)
      throw std::runtime_error("completed pole is not cubic");
  return pole;
}

std::vector<std::array<int, 6>> read_representatives(
    const std::string &path) {
  // The Python generator emits compact JSON.  To keep this producer free of
  // a JSON dependency, scan all integers following the "representatives"
  // key and group them into rows of six.
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open representative file");
  std::string text((std::istreambuf_iterator<char>(input)),
                   std::istreambuf_iterator<char>());
  const std::string key = "\"representatives\":[";
  const auto start = text.find(key);
  if (start == std::string::npos)
    throw std::runtime_error("representatives key not found");
  std::vector<int> values;
  long long value = 0;
  bool in_number = false;
  int depth = 1;
  for (std::size_t at = start + key.size(); at < text.size(); ++at) {
    const char ch = text[at];
    if (ch >= '0' && ch <= '9') {
      value = 10 * value + (ch - '0');
      in_number = true;
    } else if (in_number) {
      values.push_back(static_cast<int>(value));
      value = 0;
      in_number = false;
    }
    if (ch == '[') ++depth;
    if (ch == ']' && --depth == 0) break;
  }
  if (values.size() % 6)
    throw std::runtime_error("representative integer count is not a multiple of six");
  std::vector<std::array<int, 6>> rows(values.size() / 6);
  for (std::size_t row = 0; row < rows.size(); ++row)
    for (int position = 0; position < 6; ++position)
      rows[row][position] = values[6 * row + position];
  if (rows.size() != 571)
    throw std::runtime_error("expected 571 S5 representatives");
  return rows;
}

int xvar(int edge, int coordinate) { return 5 * edge + coordinate + 1; }

void clause(CaDiCaL::Solver &solver,
            std::initializer_list<int> literals) {
  for (int literal : literals) solver.add(literal);
  solver.add(0);
}

void xor_gate(CaDiCaL::Solver &solver, int left, int right, int output) {
  clause(solver, {left, right, -output});
  clause(solver, {-left, -right, -output});
  clause(solver, {left, -right, output});
  clause(solver, {-left, right, output});
}

void add_formula(CaDiCaL::Solver &solver, const Pole &pole,
                 int &last_variable) {
  const int edges = pole.internal_edges + 6;
  last_variable = 5 * edges;
  for (int edge = 0; edge < edges; ++edge) {
    for (int a = 0; a < 5; ++a)
      for (int b = a + 1; b < 5; ++b)
        for (int c = b + 1; c < 5; ++c)
          clause(solver, {-xvar(edge, a), -xvar(edge, b), -xvar(edge, c)});
    for (int omitted = 0; omitted < 5; ++omitted) {
      for (int coordinate = 0; coordinate < 5; ++coordinate)
        if (coordinate != omitted) solver.add(xvar(edge, coordinate));
      solver.add(0);
    }
  }
  for (int vertex = 0; vertex < pole.vertices; ++vertex) {
    for (int coordinate = 0; coordinate < 5; ++coordinate) {
      int accumulator = xvar(pole.incident[vertex][0], coordinate);
      for (std::size_t step = 1; step < pole.incident[vertex].size(); ++step) {
        const int output = ++last_variable;
        xor_gate(solver, accumulator,
                 xvar(pole.incident[vertex][step], coordinate), output);
        accumulator = output;
      }
      clause(solver, {-accumulator});
    }
  }
}

std::vector<unsigned char> extract_model(CaDiCaL::Solver &solver,
                                         const Pole &pole) {
  const int edges = pole.internal_edges + 6;
  std::vector<unsigned char> labels(edges);
  for (int edge = 0; edge < edges; ++edge) {
    unsigned char mask = 0;
    for (int coordinate = 0; coordinate < 5; ++coordinate)
      if (solver.val(xvar(edge, coordinate)) > 0)
        mask |= static_cast<unsigned char>(1U << coordinate);
    if (__builtin_popcount(mask) != 2)
      throw std::runtime_error("model violates exact-two");
    labels[edge] = mask;
  }
  for (int vertex = 0; vertex < pole.vertices; ++vertex) {
    unsigned char total = 0;
    for (int edge : pole.incident[vertex]) total ^= labels[edge];
    if (total)
      throw std::runtime_error("model violates a vertex xor");
  }
  return labels;
}

}  // namespace

int main(int argc, char **argv) {
  if (argc != 3) {
    std::cerr << "usage: enumerate_f10_boundary POLE.txt REPS.json\n";
    return 2;
  }
  try {
    const Pole pole = read_pole(argv[1]);
    const auto representatives = read_representatives(argv[2]);
    CaDiCaL::Solver solver;
    int variables = 0;
    add_formula(solver, pole, variables);
    int sat = 0, unsat = 0;
    double seconds = 0.0;
    for (std::size_t row = 0; row < representatives.size(); ++row) {
      const auto &word = representatives[row];
      for (int port = 0; port < 6; ++port)
        for (int coordinate = 0; coordinate < 5; ++coordinate) {
          const int variable = xvar(pole.internal_edges + port, coordinate);
          solver.assume((word[port] >> coordinate) & 1 ? variable : -variable);
        }
      const auto started = std::chrono::steady_clock::now();
      const int status = solver.solve();
      const auto stopped = std::chrono::steady_clock::now();
      seconds += std::chrono::duration<double>(stopped - started).count();
      std::cout << "{\"orbit\":" << row << ",\"boundary\":[";
      for (int port = 0; port < 6; ++port) {
        if (port) std::cout << ',';
        std::cout << word[port];
      }
      if (status == 10) {
        ++sat;
        const auto labels = extract_model(solver, pole);
        for (int port = 0; port < 6; ++port)
          if (labels[pole.internal_edges + port] != word[port])
            throw std::runtime_error("model violates boundary assumptions");
        std::cout << "],\"status\":\"SAT_SEMANTIC_CHECK\",\"labels\":[";
        for (std::size_t edge = 0; edge < labels.size(); ++edge) {
          if (edge) std::cout << ',';
          std::cout << static_cast<int>(labels[edge]);
        }
        std::cout << "]}\n";
      } else if (status == 20) {
        ++unsat;
        std::cout << "],\"status\":\"UNSAT_UNCERTIFIED\"}\n";
      } else {
        throw std::runtime_error("solver returned UNKNOWN");
      }
    }
    std::cerr << "representatives=" << representatives.size()
              << " sat=" << sat << " unsat_uncertified=" << unsat
              << " variables=" << variables
              << " solve_seconds=" << seconds << '\n';
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "ERROR " << error.what() << '\n';
    return 1;
  }
}
