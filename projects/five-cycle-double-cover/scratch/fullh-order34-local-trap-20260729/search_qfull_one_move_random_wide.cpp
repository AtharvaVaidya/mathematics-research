// Deterministic random search for an all-fail flow with no successful
// full-H cycle neighbour.  The filename is retained from the earlier
// parity-selector experiment; the terminal condition here is nonzero mask.

#define SIX_POINT_PARITY_NO_MAIN
#include "search_six_point_star_perpacking_parity.cpp"
#undef SIX_POINT_PARITY_NO_MAIN

#include <random>

std::vector<uint64_t> wide64_cycle_basis(const Graph& graph) {
  assert(graph.n <= 63 && graph.m() <= 63);
  std::vector<int> parent(graph.n, -1);
  std::vector<int> parent_edge(graph.n, -1);
  std::vector<int> depth(graph.n);
  parent[0] = 0;
  std::vector<int> stack{0};
  while (!stack.empty()) {
    const int vertex = stack.back();
    stack.pop_back();
    for (const int edge : graph.incidence[vertex]) {
      const auto [left, right] = graph.edges[edge];
      const int other = left == vertex ? right : left;
      if (parent[other] >= 0) continue;
      parent[other] = vertex;
      parent_edge[other] = edge;
      depth[other] = depth[vertex] + 1;
      stack.push_back(other);
    }
  }
  assert(std::all_of(parent.begin(), parent.end(),
                     [](int value) { return value >= 0; }));
  std::set<int> tree_edges(parent_edge.begin() + 1, parent_edge.end());
  std::vector<uint64_t> basis;
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (tree_edges.count(edge)) continue;
    auto [left, right] = graph.edges[edge];
    uint64_t cycle = uint64_t{1} << edge;
    while (depth[left] > depth[right]) {
      cycle ^= uint64_t{1} << parent_edge[left];
      left = parent[left];
    }
    while (depth[right] > depth[left]) {
      cycle ^= uint64_t{1} << parent_edge[right];
      right = parent[right];
    }
    while (left != right) {
      cycle ^= uint64_t{1} << parent_edge[left];
      left = parent[left];
      cycle ^= uint64_t{1} << parent_edge[right];
      right = parent[right];
    }
    basis.push_back(cycle);
  }
  assert(static_cast<int>(basis.size()) == graph.m() - graph.n + 1);
  return basis;
}

std::vector<uint64_t> wide64_cycles(
    const std::vector<uint64_t>& basis) {
  std::vector<uint64_t> cycles{0};
  for (const uint64_t value : basis) {
    const std::size_t old_size = cycles.size();
    for (std::size_t index = 0; index < old_size; ++index) {
      cycles.push_back(cycles[index] ^ value);
    }
  }
  std::sort(cycles.begin(), cycles.end());
  return cycles;
}

bool random_wide_has_success(
    const Graph& graph, const DirectFlow& flow) {
  constexpr std::array<int, 7> planes = {
      0x0f, 0x33, 0x55, 0x69, 0x99, 0xa5, 0xc3};
  for (const int plane : planes) {
    if (full_h_circuit_switch_soluble(graph, flow, plane)) return true;
  }
  return false;
}

int random_wide_span_rank(const Graph& graph, const DirectFlow& flow) {
  std::array<int, 3> basis{};
  int rank = 0;
  for (int edge = 0; edge < graph.m(); ++edge) {
    int value = flow[edge];
    for (int index = 0; index < rank; ++index) {
      value = std::min(value, value ^ basis[index]);
    }
    if (!value) continue;
    basis[rank++] = value;
    std::sort(
        basis.begin(), basis.begin() + rank, std::greater<int>());
  }
  return rank;
}

#ifndef FULLH_RANDOM_WIDE_NO_MAIN
int main(int argc, char** argv) {
  if (argc != 4) return 64;
  const Graph graph = parse_graph6(argv[1]);
  if (!is_cubic_connected(graph) || !is_bridgeless(graph)) return 3;
  const int target_samples = std::stoi(argv[2]);
  std::mt19937_64 generator(std::stoull(argv[3]));
  const auto basis = wide64_cycle_basis(graph);
  const auto cycles = wide64_cycles(basis);
  const uint64_t coordinate_mask =
      (uint64_t{1} << basis.size()) - 1;
  const uint64_t universe =
      (uint64_t{1} << graph.m()) - 1;

  int samples = 0;
  int allfail = 0;
  int escaped = 0;
  uint64_t neighbour_tests = 0;
  std::optional<DirectFlow> first_trap;
  while (samples < target_samples) {
    std::array<uint64_t, 3> supports{};
    for (int bit = 0; bit < 3; ++bit) {
      const uint64_t coefficients = generator() & coordinate_mask;
      for (int index = 0;
           index < static_cast<int>(basis.size()); ++index) {
        if ((coefficients >> index) & 1U) {
          supports[bit] ^= basis[index];
        }
      }
    }
    if ((supports[0] | supports[1] | supports[2]) != universe) {
      continue;
    }
    DirectFlow flow{};
    for (int edge = 0; edge < graph.m(); ++edge) {
      flow[edge] =
          ((supports[0] >> edge) & 1U)
          | (((supports[1] >> edge) & 1U) << 1U)
          | (((supports[2] >> edge) & 1U) << 2U);
      assert(flow[edge]);
    }
    if (random_wide_span_rank(graph, flow) != 3) continue;
    ++samples;
    if (random_wide_has_success(graph, flow)) continue;
    ++allfail;

    bool found = false;
    for (const uint64_t cycle : cycles) {
      if (!cycle) continue;
      for (int increment = 1; increment < 8; ++increment) {
        ++neighbour_tests;
        DirectFlow changed = flow;
        bool legal = true;
        for (int edge = 0; edge < graph.m(); ++edge) {
          if (!((cycle >> edge) & 1U)) continue;
          changed[edge] ^= increment;
          if (!changed[edge]) {
            legal = false;
            break;
          }
        }
        if (!legal) continue;
        if (random_wide_has_success(graph, changed)) {
          found = true;
          break;
        }
      }
      if (found) break;
    }
    if (found) {
      ++escaped;
    } else {
      first_trap = flow;
      break;
    }
  }

  std::cout << "{\"schema\":\"fullh-allfail-random-one-move-wide-v1\""
            << ",\"graph6\":\"" << argv[1] << "\""
            << ",\"vertices\":" << graph.n
            << ",\"samples\":" << samples
            << ",\"allfail_samples\":" << allfail
            << ",\"allfail_with_success_neighbour\":" << escaped
            << ",\"neighbour_tests\":" << neighbour_tests
            << ",\"trap_found\":" << (first_trap ? "true" : "false");
  if (first_trap) {
    std::cout << ",\"first_trap_flow\":";
    print_direct_flow_word(graph, *first_trap);
  }
  std::cout << "}\n";
}
#endif
