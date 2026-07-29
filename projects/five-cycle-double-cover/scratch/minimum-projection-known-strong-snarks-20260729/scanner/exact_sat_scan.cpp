#if defined(__clang__)
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wreturn-type"
#elif defined(__GNUC__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#endif
#define main fano_all_bad_projection_search_linear_main
#include "fano_all_bad_projection_search_linear.cpp"
#undef main
#if defined(__clang__)
#pragma clang diagnostic pop
#elif defined(__GNUC__)
#pragma GCC diagnostic pop
#endif

#include <cadical.hpp>
#include <functional>

struct Cnf {
  CaDiCaL::Solver solver;
  int variables;

  explicit Cnf(int initial_variables) : variables(initial_variables) {}

  void clause(std::initializer_list<int> literals) {
    for (const int literal : literals) solver.add(literal);
    solver.add(0);
  }

  int fresh() { return ++variables; }

  int xor_gate(int first, int second) {
    const int output = fresh();
    clause({first, second, -output});
    clause({first, -second, output});
    clause({-first, second, output});
    clause({-first, -second, -output});
    return output;
  }

  void even(const std::vector<int> &inputs) {
    if (inputs.empty()) return;
    if (inputs.size() == 1) {
      clause({-inputs[0]});
      return;
    }
    int parity = xor_gate(inputs[0], inputs[1]);
    for (std::size_t index = 2; index < inputs.size(); ++index) {
      parity = xor_gate(parity, inputs[index]);
    }
    clause({-parity});
  }
};

void add_cycle_constraints(
    Cnf &cnf,
    const Graph &graph,
    const std::vector<int> &variables) {
  for (const auto &incident : graph.adjacency) {
    const int first = variables[incident[0].second];
    const int second = variables[incident[1].second];
    const int third = variables[incident[2].second];
    cnf.clause({first, second, -third});
    cnf.clause({first, -second, third});
    cnf.clause({-first, second, third});
    cnf.clause({-first, -second, -third});
  }
}

bool projection_sat(
    const Graph &graph,
    Mask projection,
    Mask all_edges,
    bool require_clean) {
  const int edge_count = static_cast<int>(graph.edges.size());
  std::vector<int> first(edge_count), second(edge_count);
  for (int edge = 0; edge < edge_count; ++edge) {
    first[edge] = edge + 1;
    second[edge] = edge_count + edge + 1;
  }
  Cnf cnf(2 * edge_count);
  add_cycle_constraints(cnf, graph, first);
  add_cycle_constraints(cnf, graph, second);

  const Mask factor = all_edges ^ projection;
  Mask uncovered = factor;
  while (uncovered) {
    const int edge = std::countr_zero(uncovered);
    uncovered &= uncovered - 1;
    cnf.clause({first[edge], second[edge]});
  }

  if (require_clean) {
    for (const Mask cut : factor_cut_masks(graph, factor)) {
      std::vector<int> products;
      Mask boundary = cut;
      while (boundary) {
        const int edge = std::countr_zero(boundary);
        boundary &= boundary - 1;
        const int product = cnf.fresh();
        cnf.clause({-product, first[edge]});
        cnf.clause({-product, second[edge]});
        cnf.clause({product, -first[edge], -second[edge]});
        products.push_back(product);
      }
      cnf.even(products);
    }
  }
  const int result = cnf.solver.solve();
  if (result != 10 && result != 20) {
    throw std::runtime_error("CaDiCaL returned an indeterminate result");
  }
  return result == 10;
}

std::vector<std::vector<Mask>> cycles_by_weight(
    const std::vector<Mask> &basis,
    int edge_count) {
  std::vector<std::vector<Mask>> output(edge_count + 1);
  const std::size_t count = std::size_t{1} << basis.size();
  Mask cycle = 0;
  output[0].push_back(0);
  for (std::size_t index = 1; index < count; ++index) {
    cycle ^= basis[std::countr_zero(index)];
    output[std::popcount(cycle)].push_back(cycle);
  }
  return output;
}

std::vector<std::vector<Mask>> bounded_cycles_by_weight(
    const Graph &graph,
    int limit) {
  struct Circuit {
    Mask edges;
    Mask vertices;
    int size;
  };
  std::unordered_set<Mask> seen;
  for (int root = 0; root < graph.order; ++root) {
    std::function<void(int, int, Mask, Mask)> search =
        [&](int vertex, int vertex_count, Mask edge_mask, Mask vertex_mask) {
          for (const auto &[neighbor, edge] : graph.adjacency[vertex]) {
            if (neighbor == root) {
              if (vertex_count >= 3) {
                const Mask circuit = edge_mask ^ (Mask{1} << edge);
                if (std::popcount(circuit) <= limit) seen.insert(circuit);
              }
              continue;
            }
            if (neighbor < root ||
                ((vertex_mask >> neighbor) & 1) ||
                vertex_count >= limit) {
              continue;
            }
            search(
                neighbor,
                vertex_count + 1,
                edge_mask ^ (Mask{1} << edge),
                vertex_mask | (Mask{1} << neighbor));
          }
        };
    search(root, 1, 0, Mask{1} << root);
  }

  std::vector<Circuit> circuits;
  circuits.reserve(seen.size());
  for (const Mask circuit : seen) {
    Mask vertices = 0;
    Mask edges = circuit;
    while (edges) {
      const int edge = std::countr_zero(edges);
      edges &= edges - 1;
      vertices |= Mask{1} << graph.edges[edge].first;
      vertices |= Mask{1} << graph.edges[edge].second;
    }
    circuits.push_back({circuit, vertices, std::popcount(circuit)});
  }
  std::ranges::sort(
      circuits,
      [](const Circuit &first, const Circuit &second) {
        return first.edges < second.edges;
      });

  std::vector<std::vector<Mask>> output(graph.edges.size() + 1);
  std::function<void(std::size_t, Mask, Mask, int)> combine =
      [&](std::size_t start, Mask edge_mask, Mask vertex_mask, int size) {
        for (std::size_t index = start; index < circuits.size(); ++index) {
          const Circuit &circuit = circuits[index];
          if ((vertex_mask & circuit.vertices) ||
              size + circuit.size > limit) {
            continue;
          }
          const Mask combined_edges = edge_mask | circuit.edges;
          const Mask combined_vertices = vertex_mask | circuit.vertices;
          const int combined_size = size + circuit.size;
          output[combined_size].push_back(combined_edges);
          combine(
              index + 1,
              combined_edges,
              combined_vertices,
              combined_size);
        }
      };
  combine(0, 0, 0, 0);
  return output;
}

std::string json_escape_sat(const std::string &value) {
  std::string result;
  for (const char character : value) {
    if (character == '\\' || character == '"') result.push_back('\\');
    result.push_back(character);
  }
  return result;
}

int main(int argc, char **argv) {
  if (argc != 2) {
    std::cerr << "usage: exact-sat-scan FILE.g6" << std::endl;
    return 1;
  }
  try {
    std::ifstream stream(argv[1]);
    if (!stream) throw std::runtime_error("cannot open input");
    std::string row;
    int row_index = 0;
    while (std::getline(stream, row)) {
      if (row.empty()) {
        ++row_index;
        continue;
      }
      const Graph graph = decode_graph6(row);
      const std::vector<Mask> basis = cycle_basis(graph);
      const Mask all_edges = (Mask{1} << graph.edges.size()) - 1;

      int minimum = -1;
      int extendable_count = 0;
      const int bounded_limit =
          std::min(12, static_cast<int>(graph.edges.size()));
      std::vector<std::vector<Mask>> projections =
          bounded_cycles_by_weight(graph, bounded_limit);
      int first_weight = 1;
      int last_weight = bounded_limit;
      while (true) {
        for (int weight = first_weight; weight <= last_weight; ++weight) {
          for (const Mask projection : projections[weight]) {
            if (projection_sat(graph, projection, all_edges, true)) {
              minimum = weight;
              ++extendable_count;
              continue;
            }
            if (projection_sat(graph, projection, all_edges, false)) {
              std::cout << "{\"row\":" << row_index
                        << ",\"graph6\":\"" << json_escape_sat(row)
                        << "\",\"minimum\":" << weight
                        << ",\"minimum_extendable_so_far\":"
                        << (extendable_count + 1)
                        << ",\"bad_minimum\":1"
                        << ",\"bad_hex\":[\"0x" << std::hex << projection
                        << std::dec << "\"]"
                        << ",\"extendable_check\":true"
                        << ",\"cleanable_check\":false}"
                        << std::endl;
              return 2;
            }
          }
          if (minimum >= 0) break;
        }
        if (minimum >= 0) break;
        projections = cycles_by_weight(basis, graph.edges.size());
        first_weight = bounded_limit + 1;
        last_weight = static_cast<int>(graph.edges.size());
      }
      std::cout << "{\"row\":" << row_index
                << ",\"graph6\":\"" << json_escape_sat(row)
                << "\",\"minimum\":" << minimum
                << ",\"minimum_extendable\":" << extendable_count
                << ",\"bad_minimum\":0,\"bad_hex\":[]}"
                << std::endl;
      ++row_index;
    }
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << std::endl;
    return 1;
  }
}
