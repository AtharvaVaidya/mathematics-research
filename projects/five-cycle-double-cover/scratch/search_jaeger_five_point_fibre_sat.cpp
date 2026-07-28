// Search fixed three-tree multiplicity fibres for an Oum pair labelling
// supported on at most five of the eight coordinate points.

#define JAEGER_FIXED_FIBRE_NO_MAIN
#include "search_jaeger_fixed_fibre_sat.cpp"

namespace {

Encoding encode_five_point_good(const Graph& graph) {
  Encoding result = encode(graph, true);
  Formula& formula = result.formula;
  std::array<std::array<int, 2>, 28> pairs{};
  int pair_count = 0;
  for (int first = 0; first < 8; ++first) {
    for (int second = first + 1; second < 8; ++second) {
      pairs[pair_count++] = {first, second};
    }
  }
  std::array<int, 8> used{};
  for (int point = 0; point < 8; ++point) {
    used[point] = formula.variable();
    std::vector<int> containing{-used[point]};
    for (int edge = 0; edge < graph.m(); ++edge) {
      for (int pair = 0; pair < 28; ++pair) {
        if (pairs[pair][0] != point && pairs[pair][1] != point) continue;
        formula.clause({-result.label[edge][pair], used[point]});
        containing.push_back(result.label[edge][pair]);
      }
    }
    formula.clause(containing);
  }
  // Forbid every six-point set from being entirely used.
  for (int omitted_first = 0; omitted_first < 8; ++omitted_first) {
    for (int omitted_second = omitted_first + 1;
         omitted_second < 8; ++omitted_second) {
      std::vector<int> row;
      for (int point = 0; point < 8; ++point) {
        if (point == omitted_first || point == omitted_second) continue;
        row.push_back(-used[point]);
      }
      formula.clause(row);
    }
  }
  return result;
}

void print_defect_five(const std::vector<int>& multiplicity) {
  std::cout << '[';
  bool first = true;
  for (std::size_t edge = 0; edge < multiplicity.size(); ++edge) {
    if (multiplicity[edge] == 2) continue;
    if (!first) std::cout << ',';
    first = false;
    std::cout << '[' << edge << ',' << multiplicity[edge] << ']';
  }
  std::cout << ']';
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: search_jaeger_five_point_fibre_sat GRAPH6\n";
    return 64;
  }
  const std::string graph6 = argv[1];
  const Graph graph = parse_graph6(graph6);
  if (!is_cubic_connected(graph) || !is_bridgeless(graph)) return 3;

  const Encoding feasibility_encoding = encode(graph, false);
  const Encoding five_encoding = encode_five_point_good(graph);
  Incremental feasibility(feasibility_encoding.formula);
  Incremental five(five_encoding.formula);
  std::vector<int> multiplicity(graph.m(), 2);
  uint64_t patterns = 0;
  uint64_t feasible = 0;
  uint64_t successful = 0;

  const auto audit = [&](char type) {
    ++patterns;
    const int feasible_status =
        feasibility.solve(feasibility_encoding, multiplicity);
    assert(feasible_status == 10 || feasible_status == 20);
    if (feasible_status == 20) return false;
    ++feasible;
    const int five_status = five.solve(five_encoding, multiplicity);
    assert(five_status == 10 || five_status == 20);
    if (five_status == 10) {
      ++successful;
      verify_good_model(graph, five_encoding, five, multiplicity);
      return false;
    }
    const auto trees = extract_trees(feasibility_encoding, feasibility);
    std::cout << "{\"status\":\"NO_FIVE_POINT_GOOD_REPRESENTATIVE\","
              << "\"graph6\":\"" << graph6
              << "\",\"vertices\":" << graph.n
              << ",\"edges\":" << graph.m()
              << ",\"type\":\"" << type << "\",\"defect\":";
    print_defect_five(multiplicity);
    std::cout << ",\"feasible_tree_masks\":["
              << trees[0] << ',' << trees[1] << ',' << trees[2]
              << "],\"patterns_tested\":" << patterns
              << ",\"feasible_patterns\":" << feasible << "}\n";
    return true;
  };

  for (int first = 0; first < graph.m(); ++first) {
    multiplicity[first] = 1;
    for (int second = first + 1; second < graph.m(); ++second) {
      multiplicity[second] = 1;
      for (int third = second + 1; third < graph.m(); ++third) {
        multiplicity[third] = 1;
        if (audit('A')) return 2;
        multiplicity[third] = 2;
      }
      multiplicity[second] = 2;
    }
    multiplicity[first] = 2;
  }
  for (int zero = 0; zero < graph.m(); ++zero) {
    multiplicity[zero] = 0;
    for (int one = 0; one < graph.m(); ++one) {
      if (one == zero) continue;
      multiplicity[one] = 1;
      if (audit('B')) return 2;
      multiplicity[one] = 2;
    }
    multiplicity[zero] = 2;
  }

  std::cout << "{\"status\":\"GRAPH_DONE\",\"graph6\":\""
            << graph6 << "\",\"vertices\":" << graph.n
            << ",\"edges\":" << graph.m()
            << ",\"patterns\":" << patterns
            << ",\"feasible_fibres\":" << feasible
            << ",\"five_point_good_fibres\":" << successful
            << ",\"failures\":0}\n";
  return 0;
}
