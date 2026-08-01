// Exact SAT audit of the two proof-friendly fixed-multiplicity fibres.
//
// For every vertex v, test the type-A fibre whose three multiplicity-one
// edges are delta(v).  For every ordered adjacent pair (e0,e1), test the
// type-B fibre in which e0 has multiplicity zero and e1 multiplicity one.
// A reported ALL_BAD_SPECIAL_FIBRE is a countermodel to the corresponding
// proposed selection lemma, not a counterexample to FiveCDC.
//
// Build:
//   clang++ -O3 -std=c++20 -I/opt/homebrew/include \
//     scratch/search_jaeger_special_fibres_sat.cpp \
//     /opt/homebrew/lib/libcadical.a -o /tmp/search_jaeger_special_fibres_sat

#define JAEGER_FIXED_FIBRE_NO_MAIN
#include "search_jaeger_fixed_fibre_sat.cpp"

namespace {

Graph parse_graph6_special(std::string record) {
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
    throw std::runtime_error(
        "special audit supports short graph6 orders at most 62");
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

uint64_t verify_good_model_dynamic(
    const Graph& graph, const Encoding& encoding,
    Incremental& incremental, const std::vector<int>& multiplicity) {
  uint64_t digest = 1469598103934665603ULL;
  auto mix = [&](uint64_t value) {
    digest ^= value;
    digest *= 1099511628211ULL;
  };
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    std::vector<int> parent(graph.n);
    std::iota(parent.begin(), parent.end(), 0);
    const auto find = [&](int x, const auto& self) -> int {
      if (parent[x] == x) return x;
      return parent[x] = self(parent[x], self);
    };
    int selected_count = 0;
    for (int edge = 0; edge < graph.m(); ++edge) {
      if (incremental.solver.val(
              encoding.tree[edge][coordinate]) <= 0) {
        continue;
      }
      ++selected_count;
      int a = find(graph.edges[edge][0], find);
      int b = find(graph.edges[edge][1], find);
      assert(a != b);
      parent[a] = b;
      mix(1000 + 3 * edge + coordinate);
    }
    assert(selected_count == graph.n - 1);
  }
  for (int edge = 0; edge < graph.m(); ++edge) {
    int membership = 0;
    int flow = 0;
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      const bool in_tree =
          incremental.solver.val(encoding.tree[edge][coordinate]) > 0;
      const bool in_completion =
          incremental.solver.val(
              encoding.completion[edge][coordinate]) > 0;
      membership += in_tree;
      assert(in_tree || in_completion);
      flow |= static_cast<int>(in_completion) << coordinate;
    }
    assert(membership == multiplicity[edge]);
    assert(flow != 0);
    mix(2000 + 8 * edge + flow);
  }
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      int parity = 0;
      for (const int edge : graph.incidence[vertex]) {
        parity ^= incremental.solver.val(
            encoding.completion[edge][coordinate]) > 0;
      }
      assert(parity == 0);
    }
  }
  std::array<std::array<int, 2>, 28> pairs{};
  int pair_count = 0;
  for (int first = 0; first < 8; ++first) {
    for (int second = first + 1; second < 8; ++second) {
      pairs[pair_count++] = {first, second};
    }
  }
  std::vector<int> labels(graph.m(), -1);
  for (int edge = 0; edge < graph.m(); ++edge) {
    for (int pair = 0; pair < 28; ++pair) {
      if (incremental.solver.val(encoding.label[edge][pair]) <= 0) continue;
      assert(labels[edge] == -1);
      labels[edge] = pair;
    }
    assert(labels[edge] >= 0);
    int flow = 0;
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      flow |=
          static_cast<int>(
              incremental.solver.val(
                  encoding.completion[edge][coordinate]) > 0)
          << coordinate;
    }
    assert(
        (pairs[labels[edge]][0] ^ pairs[labels[edge]][1]) == flow);
    mix(3000 + 28 * edge + labels[edge]);
  }
  for (int vertex = 0; vertex < graph.n; ++vertex) {
    for (int point = 0; point < 8; ++point) {
      int parity = 0;
      for (const int edge : graph.incidence[vertex]) {
        parity ^=
            pairs[labels[edge]][0] == point ||
            pairs[labels[edge]][1] == point;
      }
      assert(parity == 0);
    }
  }
  std::array<int, 8> colours{};
  for (int point = 0; point < 8; ++point) {
    colours[point] = -1;
    for (int shade = 0; shade < 5; ++shade) {
      if (incremental.solver.val(
              encoding.colour[point][shade]) <= 0) {
        continue;
      }
      assert(colours[point] == -1);
      colours[point] = shade;
    }
    assert(colours[point] >= 0);
    mix(4000 + 5 * point + colours[point]);
  }
  for (const int label : labels) {
    assert(colours[pairs[label][0]] != colours[pairs[label][1]]);
  }
  return digest;
}

uint64_t verify_thin_model_dynamic(
    const Graph& graph, const Encoding& encoding,
    Incremental& incremental, const std::vector<int>& multiplicity) {
  uint64_t digest = 1469598103934665603ULL;
  std::array<int, 8> counts{};
  for (int edge = 0; edge < graph.m(); ++edge) {
    int membership = 0;
    int flow = 0;
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      const bool in_tree =
          incremental.solver.val(encoding.tree[edge][coordinate]) > 0;
      const bool in_completion =
          incremental.solver.val(
              encoding.completion[edge][coordinate]) > 0;
      membership += in_tree;
      assert(in_tree || in_completion);
      flow |= static_cast<int>(in_completion) << coordinate;
    }
    assert(membership == multiplicity[edge]);
    assert(flow != 0);
    ++counts[flow];
    digest ^= 8 * edge + flow;
    digest *= 1099511628211ULL;
  }
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      int parity = 0;
      for (const int edge : graph.incidence[vertex]) {
        parity ^= incremental.solver.val(
            encoding.completion[edge][coordinate]) > 0;
      }
      assert(parity == 0);
    }
  }
  int selected = 0;
  for (int value = 1; value < 8; ++value) {
    if (incremental.solver.val(encoding.thin_direction[value]) <= 0) {
      continue;
    }
    assert(selected == 0);
    selected = value;
  }
  assert(
      (selected == 3 || selected == 5 || selected == 6 || selected == 7) &&
      counts[selected] <= 1);
  return digest;
}

void print_good_model_fields(
    const Graph& graph, const Encoding& encoding, Incremental& incremental) {
  std::array<std::array<int, 2>, 28> pairs{};
  int pair_count = 0;
  for (int first = 0; first < 8; ++first) {
    for (int second = first + 1; second < 8; ++second) {
      pairs[pair_count++] = {first, second};
    }
  }
  std::cout << "\"model_trees\":[";
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    if (coordinate) std::cout << ',';
    std::cout << '[';
    bool first = true;
    for (int edge = 0; edge < graph.m(); ++edge) {
      if (incremental.solver.val(
              encoding.tree[edge][coordinate]) <= 0) continue;
      if (!first) std::cout << ',';
      first = false;
      std::cout << edge;
    }
    std::cout << ']';
  }
  std::cout << "],\"flow_values\":[";
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (edge) std::cout << ',';
    int flow = 0;
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      flow |=
          static_cast<int>(
              incremental.solver.val(
                  encoding.completion[edge][coordinate]) > 0)
          << coordinate;
    }
    std::cout << flow;
  }
  std::cout << "],\"pair_labels\":[";
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (edge) std::cout << ',';
    int label = -1;
    for (int pair = 0; pair < 28; ++pair) {
      if (incremental.solver.val(encoding.label[edge][pair]) > 0) {
        label = pair;
      }
    }
    assert(label >= 0);
    std::cout << '[' << pairs[label][0] << ',' << pairs[label][1] << ']';
  }
  std::cout << "],\"colours\":[";
  for (int point = 0; point < 8; ++point) {
    if (point) std::cout << ',';
    int colour = -1;
    for (int shade = 0; shade < 5; ++shade) {
      if (incremental.solver.val(
              encoding.colour[point][shade]) > 0) {
        colour = shade;
      }
    }
    assert(colour >= 0);
    std::cout << colour;
  }
  std::cout << ']';
}

void print_good_model(
    const Graph& graph, const Encoding& encoding, Incremental& incremental) {
  std::cout << '{';
  print_good_model_fields(graph, encoding, incremental);
  std::cout << "}\n";
}

void require_at_most_six_points(Encoding& encoding) {
  Formula& formula = encoding.formula;
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
    std::vector<int> reverse{-used[point]};
    for (int edge = 0; edge < static_cast<int>(encoding.label.size());
         ++edge) {
      for (int pair = 0; pair < 28; ++pair) {
        if (pairs[pair][0] != point && pairs[pair][1] != point) continue;
        formula.clause({-encoding.label[edge][pair], used[point]});
        reverse.push_back(encoding.label[edge][pair]);
      }
    }
    formula.clause(reverse);
  }
  for (int omitted = 0; omitted < 8; ++omitted) {
    std::vector<int> not_all_other_points;
    for (int point = 0; point < 8; ++point) {
      if (point != omitted) not_all_other_points.push_back(-used[point]);
    }
    formula.clause(not_all_other_points);
  }
}

void require_at_most_five_points(Encoding& encoding) {
  Formula& formula = encoding.formula;
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
    std::vector<int> reverse{-used[point]};
    for (int edge = 0; edge < static_cast<int>(encoding.label.size());
         ++edge) {
      for (int pair = 0; pair < 28; ++pair) {
        if (pairs[pair][0] != point && pairs[pair][1] != point) continue;
        formula.clause({-encoding.label[edge][pair], used[point]});
        reverse.push_back(encoding.label[edge][pair]);
      }
    }
    formula.clause(reverse);
  }
  for (int a = 0; a < 8; ++a) {
    for (int b = a + 1; b < 8; ++b) {
      std::vector<int> not_all_six;
      for (int point = 0; point < 8; ++point) {
        if (point != a && point != b) not_all_six.push_back(-used[point]);
      }
      formula.clause(not_all_six);
    }
  }
}

void require_canonical_coordinate_five_points(Encoding& encoding) {
  // By translating every pair label, a five-set whose special direction
  // plane is ker(bit 2) may be normalized to {0,4,5,6,7}; equivalently
  // the missing points are {1,2,3}.  Translation preserves pair
  // differences and every vertex parity constraint.
  for (int edge = 0; edge < static_cast<int>(encoding.label.size()); ++edge) {
    for (const int point : {1, 2, 3}) {
      encoding.formula.clause({-encoding.incidence[edge][point]});
    }
  }
}

bool test_special(
    const Graph& graph,
    const std::string& graph6,
    const Encoding& feasibility_encoding,
    const Encoding& good_encoding,
    Incremental& feasibility,
    Incremental& good,
    const char* kind,
    const std::vector<int>& defect_edges,
    std::vector<int>& multiplicity,
    uint64_t& tested,
    uint64_t& feasible_count,
    uint64_t& digest,
    bool thinning,
    bool emit_witness) {
  ++tested;
  const int feasible_status =
      feasibility.solve(feasibility_encoding, multiplicity);
  assert(feasible_status == 10 || feasible_status == 20);
  if (feasible_status == 20) {
    std::cout << "{\"status\":\"INFEASIBLE_SPECIAL_FIBRE\",\"kind\":\""
              << kind << "\",\"graph6\":\"" << graph6
              << "\",\"defect_edges\":[";
    for (std::size_t i = 0; i < defect_edges.size(); ++i) {
      if (i) std::cout << ',';
      std::cout << defect_edges[i];
    }
    std::cout << "]}\n";
    return false;
  }
  ++feasible_count;
  const int good_status = good.solve(good_encoding, multiplicity);
  assert(good_status == 10 || good_status == 20);
  if (good_status == 10) {
    digest ^=
        thinning
            ? verify_thin_model_dynamic(
                  graph, good_encoding, good, multiplicity)
            : verify_good_model_dynamic(
                  graph, good_encoding, good, multiplicity);
    digest *= 1099511628211ULL;
    if (emit_witness) {
      std::cout << "{\"status\":\"SUPPORTED_SPECIAL_FIBRE\","
                << "\"kind\":\"" << kind << "\",\"graph6\":\""
                << graph6 << "\",\"vertices\":" << graph.n
                << ",\"defect_edges\":[";
      for (std::size_t i = 0; i < defect_edges.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << defect_edges[i];
      }
      std::cout << "],";
      print_good_model_fields(graph, good_encoding, good);
      std::cout << "}\n";
    }
    return false;
  }
  std::cout << "{\"status\":\"ALL_BAD_SPECIAL_FIBRE\",\"kind\":\""
            << kind << "\",\"graph6\":\"" << graph6
            << "\",\"vertices\":" << graph.n
            << ",\"defect_edges\":[";
  for (std::size_t i = 0; i < defect_edges.size(); ++i) {
    if (i) std::cout << ',';
    std::cout << defect_edges[i];
  }
  std::cout << "],\"feasible_trees\":[";
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    if (coordinate) std::cout << ',';
    std::cout << '[';
    bool first = true;
    for (int edge = 0; edge < graph.m(); ++edge) {
      if (feasibility.solver.val(
              feasibility_encoding.tree[edge][coordinate]) <= 0) {
        continue;
      }
      if (!first) std::cout << ',';
      first = false;
      std::cout << edge;
    }
    std::cout << ']';
  }
  std::cout << "]}\n";
  return true;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc < 2 || argc > 3) {
    std::cerr
        << "usage: search_jaeger_special_fibres_sat GRAPH6 "
           "[star-only|star-thin|all-good|all-six|star-six|all-five|"
           "star-five|star-five-coordinate|"
           "star-five-coordinate-witnesses|inspect-star0]\n";
    return 64;
  }
  const std::string mode = argc == 3 ? argv[2] : "";
  const bool all_good =
      mode == "all-good" || mode == "all-six" || mode == "all-five";
  const bool six_point = mode == "all-six" || mode == "star-six";
  const bool five_point = mode == "all-five" || mode == "star-five";
  const bool coordinate_five_point =
      mode == "star-five-coordinate" ||
      mode == "star-five-coordinate-witnesses";
  const bool emit_witnesses =
      mode == "star-five-coordinate-witnesses";
  const bool inspect_star0 = mode == "inspect-star0";
  const bool star_only =
      mode == "star-only" || mode == "star-thin" || all_good ||
      mode == "star-six" || mode == "star-five" ||
      coordinate_five_point || inspect_star0;
  const bool star_thin = mode == "star-thin";
  if (argc == 3 && !star_only) return 64;
  const std::string graph6 = argv[1];
  const Graph graph = parse_graph6_special(graph6);
  if (!is_cubic_connected(graph) || !is_bridgeless(graph)) return 3;

  const Encoding feasibility_encoding = encode(graph, false);
  Encoding good_encoding =
      star_thin ? encode_direction_thinning(graph) : encode(graph, true);
  if (six_point) require_at_most_six_points(good_encoding);
  if (five_point) require_at_most_five_points(good_encoding);
  if (coordinate_five_point) {
    require_canonical_coordinate_five_points(good_encoding);
  }
  if (star_thin) {
    for (const int value : {1, 2, 4}) {
      good_encoding.formula.clause(
          {-good_encoding.thin_direction[value]});
    }
  }
  Incremental feasibility(feasibility_encoding.formula);
  Incremental good(good_encoding.formula);
  std::vector<int> multiplicity(graph.m(), 2);
  uint64_t tested = 0;
  uint64_t feasible_count = 0;
  uint64_t digest = 1469598103934665603ULL;

  if (inspect_star0) {
    const std::vector<int> defect(
        graph.incidence[0].begin(), graph.incidence[0].end());
    for (const int edge : defect) multiplicity[edge] = 1;
    assert(good.solve(good_encoding, multiplicity) == 10);
    verify_good_model_dynamic(
        graph, good_encoding, good, multiplicity);
    print_good_model(graph, good_encoding, good);
    return 0;
  }

  if (all_good) {
    for (int a = 0; a < graph.m(); ++a) {
      multiplicity[a] = 1;
      for (int b = a + 1; b < graph.m(); ++b) {
        multiplicity[b] = 1;
        for (int c = b + 1; c < graph.m(); ++c) {
          multiplicity[c] = 1;
          if (test_special(
                  graph, graph6, feasibility_encoding, good_encoding,
                  feasibility, good, "A_ANY", {a, b, c}, multiplicity,
                  tested, feasible_count, digest, false, false)) {
            return 2;
          }
          multiplicity[c] = 2;
        }
        multiplicity[b] = 2;
      }
      multiplicity[a] = 2;
    }
    for (int zero = 0; zero < graph.m(); ++zero) {
      multiplicity[zero] = 0;
      for (int one = 0; one < graph.m(); ++one) {
        if (one == zero) continue;
        multiplicity[one] = 1;
        if (test_special(
                graph, graph6, feasibility_encoding, good_encoding,
                feasibility, good, "B_ANY", {zero, one}, multiplicity,
                tested, feasible_count, digest, false, false)) {
          return 2;
        }
        multiplicity[one] = 2;
      }
      multiplicity[zero] = 2;
    }
    std::cout << "{\"status\":\"GRAPH_DONE\",\"graph6\":\""
              << graph6 << "\",\"vertices\":" << graph.n
              << ",\"special_fibres_tested\":" << tested
              << ",\"feasible_special_fibres\":" << feasible_count
              << ",\"all_bad_special_fibres\":0"
              << ",\"checked_certificate_digest_fnv1a64\":" << digest
              << "}\n";
    return 0;
  }

  for (int vertex = 0; vertex < graph.n; ++vertex) {
    std::vector<int> defect(
        graph.incidence[vertex].begin(), graph.incidence[vertex].end());
    for (const int edge : defect) multiplicity[edge] = 1;
    if (test_special(
            graph, graph6, feasibility_encoding, good_encoding, feasibility, good,
            "A_STAR", defect, multiplicity, tested, feasible_count, digest,
            star_thin, emit_witnesses)) {
      return 2;
    }
    for (const int edge : defect) multiplicity[edge] = 2;
  }

  for (int zero = 0; !star_only && zero < graph.m(); ++zero) {
    const int u = graph.edges[zero][0];
    const int v = graph.edges[zero][1];
    for (const int endpoint : {u, v}) {
      for (const int one : graph.incidence[endpoint]) {
        if (one == zero) continue;
        multiplicity[zero] = 0;
        multiplicity[one] = 1;
        if (test_special(
                graph, graph6, feasibility_encoding, good_encoding, feasibility, good,
                "B_ADJACENT", {zero, one}, multiplicity, tested,
                feasible_count, digest, false, false)) {
          return 2;
        }
        multiplicity[zero] = 2;
        multiplicity[one] = 2;
      }
    }
  }

  std::cout << "{\"status\":\"GRAPH_DONE\",\"graph6\":\""
            << graph6 << "\",\"vertices\":" << graph.n
            << ",\"special_fibres_tested\":" << tested
            << ",\"feasible_special_fibres\":" << feasible_count
            << ",\"all_bad_special_fibres\":0"
            << ",\"checked_certificate_digest_fnv1a64\":" << digest
            << "}\n";
  return 0;
}
