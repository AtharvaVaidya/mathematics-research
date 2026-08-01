// Search the following strengthening of the Jaeger star-fibre parity target:
//
//   K(T_0) intersection K(T_1) is contained in the graphic-matroid
//   closure of K(T_2).
//
// Since K(T_2) is a forest, this says that the endpoints of every edge in
// K(T_0) intersection K(T_1) lie in one K(T_2)-component.  It implies the
// required quotient parity, but is not known to be necessary.
//
// Build:
//   clang++ -O3 -std=c++20 -I/opt/homebrew/include \
//     scratch/search_jaeger_star_kernel_closure_sat.cpp \
//     /opt/homebrew/lib/libcadical.a -o /tmp/search_star_kernel_closure

#define JAEGER_FIXED_FIBRE_NO_MAIN
#include "search_jaeger_fixed_fibre_sat.cpp"

namespace {

Graph parse_graph6_closure(std::string record) {
  while (!record.empty() &&
         (record.back() == '\n' || record.back() == '\r')) {
    record.pop_back();
  }
  const std::string header = ">>graph6<<";
  if (record.rfind(header, 0) == 0) record.erase(0, header.size());
  if (record.empty() || record[0] == '~') {
    throw std::runtime_error("only short graph6 records are supported");
  }
  Graph graph;
  graph.n = static_cast<unsigned char>(record[0]) - 63;
  if (graph.n < 1 || graph.n > 62) {
    throw std::runtime_error("short graph6 order must be at most 62");
  }
  const int bit_count = graph.n * (graph.n - 1) / 2;
  std::vector<int> bits;
  for (std::size_t i = 1; i < record.size(); ++i) {
    const int chunk = static_cast<unsigned char>(record[i]) - 63;
    if (chunk < 0 || chunk >= 64) throw std::runtime_error("bad graph6 byte");
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((chunk >> shift) & 1);
    }
  }
  if (static_cast<int>(bits.size()) < bit_count) {
    throw std::runtime_error("truncated graph6 record");
  }
  int cursor = 0;
  for (int v = 1; v < graph.n; ++v) {
    for (int u = 0; u < v; ++u) {
      if (bits[cursor]) graph.edges.push_back({u, v});
      ++cursor;
    }
  }
  graph.incidence.assign(graph.n, {});
  for (int edge = 0; edge < graph.m(); ++edge) {
    graph.incidence[graph.edges[edge][0]].push_back(edge);
    graph.incidence[graph.edges[edge][1]].push_back(edge);
  }
  return graph;
}

void xor4_even(
    Formula& formula, const int a, const int b, const int c, const int d) {
  const std::array<int, 4> variables{a, b, c, d};
  for (int assignment = 0; assignment < 16; ++assignment) {
    if ((__builtin_popcount(static_cast<unsigned>(assignment)) & 1) == 0) {
      continue;
    }
    std::vector<int> forbidden;
    for (int bit = 0; bit < 4; ++bit) {
      forbidden.push_back(
          (assignment & (1 << bit)) ? -variables[bit] : variables[bit]);
    }
    formula.clause(forbidden);
  }
}

Encoding encode_kernel_closure(const Graph& graph) {
  Encoding result = encode(graph, false);
  Formula& formula = result.formula;
  const int m = graph.m();

  // Fundamental completions F_i=E-K_i.
  result.completion.resize(m);
  for (int edge = 0; edge < m; ++edge) {
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      result.completion[edge][coordinate] = formula.variable();
      formula.clause(
          {result.tree[edge][coordinate],
           result.completion[edge][coordinate]});
    }
    formula.clause(
        {result.completion[edge][0],
         result.completion[edge][1],
         result.completion[edge][2]});
  }
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      xor3_even(
          formula,
          result.completion[graph.incidence[vertex][0]][coordinate],
          result.completion[graph.incidence[vertex][1]][coordinate],
          result.completion[graph.incidence[vertex][2]][coordinate]);
    }
  }

  // For every target edge e, pure[e] iff e belongs to K_0 cap K_1.
  // If pure[e], a parity path y[e,*] inside K_2 joins its endpoints.
  // A subset of a forest has boundary {u,v} iff it is the unique u-v path,
  // so these commodity equations encode exactly e in cl(K_2).
  for (int target = 0; target < m; ++target) {
    const int pure = formula.variable();
    const int f0 = result.completion[target][0];
    const int f1 = result.completion[target][1];
    formula.clause({-pure, -f0});
    formula.clause({-pure, -f1});
    formula.clause({pure, f0, f1});

    std::vector<int> path(m);
    for (int edge = 0; edge < m; ++edge) {
      path[edge] = formula.variable();
      formula.clause({-path[edge], -result.completion[edge][2]});
    }
    const int left = graph.edges[target][0];
    const int right = graph.edges[target][1];
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      const auto& row = graph.incidence[vertex];
      if (vertex == left || vertex == right) {
        xor4_even(
            formula, path[row[0]], path[row[1]], path[row[2]], pure);
      } else {
        xor3_even(formula, path[row[0]], path[row[1]], path[row[2]]);
      }
    }
  }
  return result;
}

bool verify_closure_model(
    const Graph& graph, const Encoding& encoding, Incremental& solver,
    const std::vector<int>& multiplicity) {
  std::vector<std::array<bool, 3>> trees(graph.m());
  std::vector<std::array<bool, 3>> kernels(graph.m());
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    std::vector<int> parent(graph.n);
    std::iota(parent.begin(), parent.end(), 0);
    const auto find = [&](int vertex, const auto& self) -> int {
      if (parent[vertex] == vertex) return vertex;
      return parent[vertex] = self(parent[vertex], self);
    };
    int selected = 0;
    for (int edge = 0; edge < graph.m(); ++edge) {
      trees[edge][coordinate] =
          solver.solver.val(encoding.tree[edge][coordinate]) > 0;
      kernels[edge][coordinate] =
          solver.solver.val(encoding.completion[edge][coordinate]) <= 0;
      if (!trees[edge][coordinate]) continue;
      ++selected;
      int a = find(graph.edges[edge][0], find);
      int b = find(graph.edges[edge][1], find);
      if (a == b) return false;
      parent[a] = b;
    }
    if (selected != graph.n - 1) return false;
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      int kernel_degree = 0;
      for (const int edge : graph.incidence[vertex]) {
        kernel_degree += kernels[edge][coordinate];
      }
      if ((kernel_degree & 1) == 0) return false;
    }
  }
  for (int edge = 0; edge < graph.m(); ++edge) {
    int count = 0;
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      count += trees[edge][coordinate];
      if (kernels[edge][coordinate] && !trees[edge][coordinate]) return false;
    }
    if (count != multiplicity[edge]) return false;
  }

  std::vector<int> parent(graph.n);
  std::iota(parent.begin(), parent.end(), 0);
  const auto find = [&](int vertex, const auto& self) -> int {
    if (parent[vertex] == vertex) return vertex;
    return parent[vertex] = self(parent[vertex], self);
  };
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (!kernels[edge][2]) continue;
    int a = find(graph.edges[edge][0], find);
    int b = find(graph.edges[edge][1], find);
    if (a == b) return false;
    parent[a] = b;
  }
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (!(kernels[edge][0] && kernels[edge][1])) continue;
    if (find(graph.edges[edge][0], find) !=
        find(graph.edges[edge][1], find)) {
      return false;
    }
  }
  return true;
}

}  // namespace

int main(int argc, char** argv) {
  const std::string mode = argc >= 2 ? argv[1] : "stars";
  const bool emit_witnesses =
      mode == "stars-witnesses" || mode == "all-type-ab-witnesses";
  const bool all_type_ab =
      mode == "all-type-ab" || mode == "all-type-ab-witnesses";
  if (mode != "stars" && mode != "stars-witnesses" &&
      mode != "all-type-ab" && mode != "all-type-ab-witnesses") {
    throw std::runtime_error(
        "mode must be stars, stars-witnesses, all-type-ab, "
        "or all-type-ab-witnesses");
  }
  std::string graph6;
  while (std::getline(std::cin, graph6)) {
    if (graph6.empty()) continue;
    const Graph graph = parse_graph6_closure(graph6);
    if (graph.n % 2 || graph.m() != 3 * graph.n / 2) {
      std::cout << "{\"graph6\":\"" << graph6
                << "\",\"status\":\"SKIPPED_NOT_CUBIC\"}\n";
      continue;
    }
    const Encoding feasibility_encoding = encode(graph, false);
    const Encoding encoding = encode_kernel_closure(graph);
    Incremental feasibility_solver(feasibility_encoding.formula);
    Incremental solver(encoding.formula);
    uint64_t patterns = 0;
    uint64_t feasible_patterns = 0;
    uint64_t closure_patterns = 0;
    uint64_t connected_third_kernel_roots = 0;

    const auto test_multiplicity = [&](
        const std::vector<int>& multiplicity, const char* kind,
        const std::vector<int>& defect_edges) {
      ++patterns;
      const int feasible_status =
          feasibility_solver.solve(feasibility_encoding, multiplicity);
      if (feasible_status == 20) return;
      if (feasible_status != 10) {
        throw std::runtime_error("feasibility solver returned nonterminal status");
      }
      ++feasible_patterns;
      const int status = solver.solve(encoding, multiplicity);
      if (status == 10) {
        if (!verify_closure_model(
                graph, encoding, solver, multiplicity)) {
          throw std::runtime_error("SAT model failed direct closure check");
        }
        int third_kernel_size = 0;
        for (int edge = 0; edge < graph.m(); ++edge) {
          third_kernel_size +=
              solver.solver.val(encoding.completion[edge][2]) <= 0;
        }
        connected_third_kernel_roots +=
            third_kernel_size == graph.n - 1;
        ++closure_patterns;
        if (emit_witnesses) {
          std::cout << "{\"status\":\"CLOSURE_WITNESS\","
                    << "\"graph6\":\"" << graph6 << "\","
                    << "\"kind\":\"" << kind << "\","
                    << "\"defect_edges\":[";
          for (std::size_t index = 0; index < defect_edges.size(); ++index) {
            if (index) std::cout << ',';
            std::cout << defect_edges[index];
          }
          std::cout << "],\"trees\":[";
          for (int coordinate = 0; coordinate < 3; ++coordinate) {
            if (coordinate) std::cout << ',';
            std::cout << '[';
            bool first = true;
            for (int edge = 0; edge < graph.m(); ++edge) {
              if (solver.solver.val(
                      encoding.tree[edge][coordinate]) <= 0) {
                continue;
              }
              if (!first) std::cout << ',';
              first = false;
              std::cout << edge;
            }
            std::cout << ']';
          }
          std::cout << "]}\n";
        }
      } else if (status != 20) {
        throw std::runtime_error("solver returned nonterminal status");
      } else {
        std::cout << "{\"status\":\"CLOSURE_FAILURE\","
                  << "\"graph6\":\"" << graph6 << "\","
                  << "\"kind\":\"" << kind << "\","
                  << "\"defect_edges\":[";
        for (std::size_t index = 0; index < defect_edges.size(); ++index) {
          if (index) std::cout << ',';
          std::cout << defect_edges[index];
        }
        std::cout << "]}\n";
      }
    };

    if (!all_type_ab) {
      for (int root = 0; root < graph.n; ++root) {
        std::vector<int> multiplicity(graph.m(), 2);
        for (const int edge : graph.incidence[root]) multiplicity[edge] = 1;
        test_multiplicity(
            multiplicity, "star", std::vector<int>{root});
      }
    } else {
      for (int first = 0; first < graph.m(); ++first) {
        for (int second = first + 1; second < graph.m(); ++second) {
          for (int third = second + 1; third < graph.m(); ++third) {
            std::vector<int> multiplicity(graph.m(), 2);
            multiplicity[first] = 1;
            multiplicity[second] = 1;
            multiplicity[third] = 1;
            test_multiplicity(
                multiplicity, "type_a",
                std::vector<int>{first, second, third});
          }
        }
      }
      for (int zero = 0; zero < graph.m(); ++zero) {
        for (int one = 0; one < graph.m(); ++one) {
          if (zero == one) continue;
          std::vector<int> multiplicity(graph.m(), 2);
          multiplicity[zero] = 0;
          multiplicity[one] = 1;
          test_multiplicity(
              multiplicity, "type_b", std::vector<int>{zero, one});
        }
      }
    }
    std::cout << "{\"graph6\":\"" << graph6
              << "\",\"vertices\":" << graph.n
              << ",\"mode\":\"" << mode << "\""
              << ",\"patterns\":" << patterns
              << ",\"feasible_patterns\":" << feasible_patterns
              << ",\"closure_patterns\":" << closure_patterns
              << ",\"connected_third_kernel_models\":"
              << connected_third_kernel_roots
              << ",\"failures\":"
              << (feasible_patterns - closure_patterns)
              << "}\n";
  }
}
