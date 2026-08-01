// Exact SAT search for an all-bad fixed-multiplicity fibre of three
// spanning trees in a simple cubic graph.
//
// A fibre is "good" if it contains three spanning trees whose fundamental
// completions are the three coordinates of an eight-point pair-labelled
// double cover with a five-colourable coordinate co-occurrence graph.
//
// Build:
//   clang++ -O3 -std=c++20 -I/opt/homebrew/include \
//     scratch/search_jaeger_fixed_fibre_sat.cpp \
//     /opt/homebrew/lib/libcadical.a -o /tmp/search_jaeger_fixed_fibre_sat
//
// Usage:
//   /tmp/search_jaeger_fixed_fibre_sat GRAPH6

#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

#define main frozen_coordinated_census_unused_main
#include "census_jaeger_two_tree_exchange_through14.cpp"
#undef main

namespace {

struct Formula {
  int variables = 0;
  std::vector<std::vector<int>> clauses;

  int variable() { return ++variables; }

  void clause(std::initializer_list<int> literals) {
    clauses.emplace_back(literals);
  }

  void clause(const std::vector<int>& literals) {
    clauses.push_back(literals);
  }

  void conditional_clause(int selector, std::initializer_list<int> literals) {
    std::vector<int> row;
    row.reserve(literals.size() + 1);
    row.push_back(-selector);
    row.insert(row.end(), literals.begin(), literals.end());
    clauses.push_back(std::move(row));
  }
};

void exactly_one(Formula& formula, const std::vector<int>& variables) {
  formula.clause(variables);
  for (std::size_t i = 0; i < variables.size(); ++i) {
    for (std::size_t j = i + 1; j < variables.size(); ++j) {
      formula.clause({-variables[i], -variables[j]});
    }
  }
}

void xor3_even(Formula& formula, int a, int b, int c) {
  formula.clause({-a, -b, -c});
  formula.clause({-a, b, c});
  formula.clause({a, -b, c});
  formula.clause({a, b, -c});
}

struct Encoding {
  Formula formula;
  std::vector<std::array<int, 3>> tree;
  std::vector<std::array<int, 3>> selector;
  std::vector<std::array<int, 3>> completion;
  std::vector<std::array<int, 28>> label;
  std::vector<std::array<int, 8>> incidence;
  std::array<std::array<int, 5>, 8> colour{};
  std::vector<std::array<int, 8>> flow_value;
  std::array<int, 8> thin_direction{};
};

Encoding encode(const Graph& graph, bool require_good) {
  Encoding result;
  Formula& formula = result.formula;
  const int n = graph.n;
  const int m = graph.m();

  result.tree.resize(m);
  result.selector.resize(m);
  for (int edge = 0; edge < m; ++edge) {
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      result.tree[edge][coordinate] = formula.variable();
      result.selector[edge][coordinate] = formula.variable();
    }
  }

  // A selected edge set is a spanning tree.  Every non-root vertex chooses
  // one incident parent edge.  Unary levels strictly decrease towards the
  // root, excluding directed cycles.  An undirected edge is selected iff
  // exactly one endpoint uses it as its parent edge.
  std::vector<std::vector<std::array<int, 3>>> parent(
      3, std::vector<std::array<int, 3>>(n));
  std::vector<std::vector<std::vector<int>>> level(
      3, std::vector<std::vector<int>>(n, std::vector<int>(n)));
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    for (int vertex = 0; vertex < n; ++vertex) {
      for (int slot = 0; slot < 3; ++slot) {
        parent[coordinate][vertex][slot] = formula.variable();
      }
      for (int depth = 0; depth < n; ++depth) {
        level[coordinate][vertex][depth] = formula.variable();
      }
      exactly_one(formula, level[coordinate][vertex]);
    }
    formula.clause({level[coordinate][0][0]});
    for (int depth = 1; depth < n; ++depth) {
      formula.clause({-level[coordinate][0][depth]});
    }
    for (int slot = 0; slot < 3; ++slot) {
      formula.clause({-parent[coordinate][0][slot]});
    }
    for (int vertex = 1; vertex < n; ++vertex) {
      formula.clause({-level[coordinate][vertex][0]});
      exactly_one(
          formula,
          {parent[coordinate][vertex][0],
           parent[coordinate][vertex][1],
           parent[coordinate][vertex][2]});
    }

    for (int edge = 0; edge < m; ++edge) {
      const int u = graph.edges[edge][0];
      const int v = graph.edges[edge][1];
      const int u_slot = std::find(
          graph.incidence[u].begin(), graph.incidence[u].end(), edge) -
          graph.incidence[u].begin();
      const int v_slot = std::find(
          graph.incidence[v].begin(), graph.incidence[v].end(), edge) -
          graph.incidence[v].begin();
      assert(u_slot < 3 && v_slot < 3);
      const int pu = parent[coordinate][u][u_slot];
      const int pv = parent[coordinate][v][v_slot];
      const int selected = result.tree[edge][coordinate];
      formula.clause({-pu, selected});
      formula.clause({-pv, selected});
      formula.clause({-selected, pu, pv});
      formula.clause({-pu, -pv});

      for (const auto [child, other, parent_variable] :
           {std::array<int, 3>{u, v, pu},
            std::array<int, 3>{v, u, pv}}) {
        for (int child_depth = 0; child_depth < n; ++child_depth) {
          for (int other_depth = child_depth;
               other_depth < n; ++other_depth) {
            formula.clause(
                {-parent_variable,
                 -level[coordinate][child][child_depth],
                 -level[coordinate][other][other_depth]});
          }
        }
      }
    }
  }

  // Conditional exact multiplicity constraints.  A solve call assumes
  // exactly one selector for each edge.
  for (int edge = 0; edge < m; ++edge) {
    const int a = result.tree[edge][0];
    const int b = result.tree[edge][1];
    const int c = result.tree[edge][2];
    const int zero = result.selector[edge][0];
    const int one = result.selector[edge][1];
    const int two = result.selector[edge][2];
    formula.conditional_clause(zero, {-a});
    formula.conditional_clause(zero, {-b});
    formula.conditional_clause(zero, {-c});
    formula.conditional_clause(one, {a, b, c});
    formula.conditional_clause(one, {-a, -b});
    formula.conditional_clause(one, {-a, -c});
    formula.conditional_clause(one, {-b, -c});
    formula.conditional_clause(two, {a, b});
    formula.conditional_clause(two, {a, c});
    formula.conditional_clause(two, {b, c});
    formula.conditional_clause(two, {-a, -b, -c});
  }

  if (!require_good) return result;

  // The fundamental completion F(T) is the unique Eulerian edge set
  // containing every cotree edge.  These two conditions encode it without
  // expanding fundamental circuits.
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
    for (int vertex = 0; vertex < n; ++vertex) {
      xor3_even(
          formula,
          result.completion[graph.incidence[vertex][0]][coordinate],
          result.completion[graph.incidence[vertex][1]][coordinate],
          result.completion[graph.incidence[vertex][2]][coordinate]);
    }
  }

  result.label.resize(m);
  result.incidence.resize(m);
  std::array<std::array<int, 2>, 28> pairs{};
  int pair_count = 0;
  for (int first = 0; first < 8; ++first) {
    for (int second = first + 1; second < 8; ++second) {
      pairs[pair_count++] = {first, second};
    }
  }
  assert(pair_count == 28);

  for (int edge = 0; edge < m; ++edge) {
    std::vector<int> choices;
    for (int pair = 0; pair < 28; ++pair) {
      result.label[edge][pair] = formula.variable();
      choices.push_back(result.label[edge][pair]);
    }
    exactly_one(formula, choices);
    for (int point = 0; point < 8; ++point) {
      result.incidence[edge][point] = formula.variable();
      std::vector<int> containing;
      containing.push_back(-result.incidence[edge][point]);
      for (int pair = 0; pair < 28; ++pair) {
        if (pairs[pair][0] != point && pairs[pair][1] != point) continue;
        formula.clause(
            {-result.label[edge][pair], result.incidence[edge][point]});
        containing.push_back(result.label[edge][pair]);
      }
      formula.clause(containing);
    }
    for (int pair = 0; pair < 28; ++pair) {
      const int value = pairs[pair][0] ^ pairs[pair][1];
      for (int bit = 0; bit < 3; ++bit) {
        const int flow_bit = result.completion[edge][bit];
        formula.clause(
            {-result.label[edge][pair],
             (value & (1 << bit)) ? flow_bit : -flow_bit});
      }
    }
  }

  // Coordinate parity is exactly the eight-coordinate double-cover
  // condition.  Together with pair xor = completion flow, it is equivalent
  // to existence of an Oum-compatible potential.
  for (int vertex = 0; vertex < n; ++vertex) {
    for (int point = 0; point < 8; ++point) {
      xor3_even(
          formula,
          result.incidence[graph.incidence[vertex][0]][point],
          result.incidence[graph.incidence[vertex][1]][point],
          result.incidence[graph.incidence[vertex][2]][point]);
    }
  }

  for (int point = 0; point < 8; ++point) {
    std::vector<int> choices;
    for (int shade = 0; shade < 5; ++shade) {
      result.colour[point][shade] = formula.variable();
      choices.push_back(result.colour[point][shade]);
    }
    exactly_one(formula, choices);
  }
  for (int edge = 0; edge < m; ++edge) {
    for (int pair = 0; pair < 28; ++pair) {
      const int first = pairs[pair][0];
      const int second = pairs[pair][1];
      for (int shade = 0; shade < 5; ++shade) {
        formula.clause(
            {-result.label[edge][pair],
             -result.colour[first][shade],
             -result.colour[second][shade]});
      }
    }
  }
  return result;
}

Encoding encode_direction_thinning(const Graph& graph) {
  Encoding result = encode(graph, false);
  Formula& formula = result.formula;
  const int m = graph.m();
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

  result.flow_value.resize(m);
  for (int edge = 0; edge < m; ++edge) {
    for (int value = 1; value < 8; ++value) {
      const int equal = formula.variable();
      result.flow_value[edge][value] = equal;
      std::vector<int> reverse{equal};
      for (int bit = 0; bit < 3; ++bit) {
        const int variable = result.completion[edge][bit];
        const bool one = value & (1 << bit);
        formula.clause({-equal, one ? variable : -variable});
        reverse.push_back(one ? -variable : variable);
      }
      formula.clause(reverse);
    }
  }
  std::vector<int> directions;
  for (int value = 1; value < 8; ++value) {
    result.thin_direction[value] = formula.variable();
    directions.push_back(result.thin_direction[value]);
    for (int first = 0; first < m; ++first) {
      for (int second = first + 1; second < m; ++second) {
        formula.clause(
            {-result.thin_direction[value],
             -result.flow_value[first][value],
             -result.flow_value[second][value]});
      }
    }
  }
  exactly_one(formula, directions);
  return result;
}

struct Incremental {
  CaDiCaL::Solver solver;
  explicit Incremental(const Formula& formula) {
    for (const auto& clause : formula.clauses) {
      for (const int literal : clause) solver.add(literal);
      solver.add(0);
    }
  }

  int solve(
      const Encoding& encoding, const std::vector<int>& multiplicity) {
    for (std::size_t edge = 0; edge < multiplicity.size(); ++edge) {
      for (int value = 0; value < 3; ++value) {
        const int selector = encoding.selector[edge][value];
        solver.assume(
            value == multiplicity[edge] ? selector : -selector);
      }
    }
    return solver.solve();
  }
};

std::array<uint32_t, 3> extract_trees(
    const Encoding& encoding, Incremental& incremental) {
  std::array<uint32_t, 3> answer{};
  for (std::size_t edge = 0; edge < encoding.tree.size(); ++edge) {
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      if (incremental.solver.val(encoding.tree[edge][coordinate]) > 0) {
        answer[coordinate] |= uint32_t{1} << edge;
      }
    }
  }
  return answer;
}

uint64_t verify_good_model(
    const Graph& graph, const Encoding& encoding,
    Incremental& incremental, const std::vector<int>& multiplicity) {
  const auto trees = extract_trees(encoding, incremental);
  std::array<uint32_t, 3> completions{};
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    assert(is_tree(graph, trees[coordinate]));
    completions[coordinate] =
        fundamental_completion(graph, trees[coordinate]);
  }
  for (int edge = 0; edge < graph.m(); ++edge) {
    int membership = 0;
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      membership += (trees[coordinate] >> edge) & 1U;
      const bool encoded =
          incremental.solver.val(
              encoding.completion[edge][coordinate]) > 0;
      const bool direct = (completions[coordinate] >> edge) & 1U;
      assert(encoded == direct);
    }
    assert(membership == multiplicity[edge]);
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
    int flow_value = 0;
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      flow_value |=
          ((completions[coordinate] >> edge) & 1U) << coordinate;
    }
    assert(
        (pairs[labels[edge]][0] ^ pairs[labels[edge]][1]) ==
        flow_value);
  }

  for (int vertex = 0; vertex < graph.n; ++vertex) {
    for (int point = 0; point < 8; ++point) {
      int degree = 0;
      for (const int edge : graph.incidence[vertex]) {
        degree +=
            pairs[labels[edge]][0] == point ||
            pairs[labels[edge]][1] == point;
      }
      assert((degree & 1) == 0);
    }
  }
  std::array<int, 8> colours{};
  for (int point = 0; point < 8; ++point) {
    colours[point] = -1;
    for (int shade = 0; shade < 5; ++shade) {
      if (incremental.solver.val(encoding.colour[point][shade]) <= 0) {
        continue;
      }
      assert(colours[point] == -1);
      colours[point] = shade;
    }
    assert(colours[point] >= 0);
  }
  for (int edge = 0; edge < graph.m(); ++edge) {
    assert(
        colours[pairs[labels[edge]][0]] !=
        colours[pairs[labels[edge]][1]]);
  }

  // Deterministic FNV-1a digest of the directly checked certificate.
  uint64_t digest = 1469598103934665603ULL;
  auto mix = [&](uint64_t value) {
    digest ^= value;
    digest *= 1099511628211ULL;
  };
  for (const uint32_t tree : trees) mix(tree);
  for (const uint32_t completion : completions) mix(completion);
  for (const int label : labels) mix(label);
  for (const int colour : colours) mix(colour);
  return digest;
}

void print_pattern(const std::vector<int>& multiplicity) {
  bool first = true;
  std::cout << '[';
  for (std::size_t edge = 0; edge < multiplicity.size(); ++edge) {
    if (multiplicity[edge] == 2) continue;
    if (!first) std::cout << ',';
    first = false;
    std::cout << '[' << edge << ',' << multiplicity[edge] << ']';
  }
  std::cout << ']';
}

}  // namespace

#ifndef JAEGER_FIXED_FIBRE_NO_MAIN
int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: search_jaeger_fixed_fibre_sat GRAPH6\n";
    return 64;
  }
  const std::string graph6 = argv[1];
  const Graph graph = parse_graph6(graph6);
  if (!is_cubic_connected(graph) || !is_bridgeless(graph)) return 3;

  const Encoding feasibility_encoding = encode(graph, false);
  const Encoding good_encoding = encode(graph, true);
  Incremental feasibility(feasibility_encoding.formula);
  Incremental good(good_encoding.formula);

  uint64_t patterns = 0;
  uint64_t feasible = 0;
  uint64_t good_fibres = 0;
  uint64_t type_a_feasible = 0;
  uint64_t type_b_feasible = 0;
  uint64_t certificate_digest = 1469598103934665603ULL;
  std::vector<int> multiplicity(graph.m(), 2);

  const auto audit = [&](char type) -> bool {
    ++patterns;
    const int feasible_status =
        feasibility.solve(feasibility_encoding, multiplicity);
    assert(feasible_status == 10 || feasible_status == 20);
    if (feasible_status == 20) return false;
    ++feasible;
    if (type == 'A') ++type_a_feasible;
    else ++type_b_feasible;
    const int good_status = good.solve(good_encoding, multiplicity);
    assert(good_status == 10 || good_status == 20);
    if (good_status == 10) {
      ++good_fibres;
      certificate_digest ^=
          verify_good_model(
              graph, good_encoding, good, multiplicity);
      certificate_digest *= 1099511628211ULL;
      return false;
    }
    const auto trees = extract_trees(feasibility_encoding, feasibility);
    std::cout << "{\"status\":\"ALL_BAD_FIBRE\",\"graph6\":\""
              << graph6 << "\",\"vertices\":" << graph.n
              << ",\"edges\":" << graph.m()
              << ",\"type\":\"" << type << "\",\"defect\":";
    print_pattern(multiplicity);
    std::cout << ",\"feasible_tree_masks\":["
              << trees[0] << ',' << trees[1] << ',' << trees[2]
              << "],\"patterns_tested\":" << patterns
              << ",\"feasible_patterns\":" << feasible << "}\n";
    return true;
  };

  // Type A: three distinct multiplicity-one edges.
  for (int a = 0; a < graph.m(); ++a) {
    multiplicity[a] = 1;
    for (int b = a + 1; b < graph.m(); ++b) {
      multiplicity[b] = 1;
      for (int c = b + 1; c < graph.m(); ++c) {
        multiplicity[c] = 1;
        if (audit('A')) return 2;
        multiplicity[c] = 2;
      }
      multiplicity[b] = 2;
    }
    multiplicity[a] = 2;
  }

  // Type B: one multiplicity-zero edge and a distinct multiplicity-one edge.
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
            << ",\"type_a_feasible\":" << type_a_feasible
            << ",\"type_b_feasible\":" << type_b_feasible
            << ",\"good_fibres\":" << good_fibres
            << ",\"all_bad_fibres\":0"
            << ",\"checked_certificate_digest_fnv1a64\":"
            << certificate_digest
            << ",\"feasibility_variables\":"
            << feasibility_encoding.formula.variables
            << ",\"feasibility_clauses\":"
            << feasibility_encoding.formula.clauses.size()
            << ",\"good_variables\":" << good_encoding.formula.variables
            << ",\"good_clauses\":" << good_encoding.formula.clauses.size()
            << "}\n";
  return 0;
}
#endif
