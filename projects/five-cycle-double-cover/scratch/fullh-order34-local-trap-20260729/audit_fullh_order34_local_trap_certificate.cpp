// Complete semantic certificate for the first order-34 all-fail local trap.

#define FULLH_RANDOM_WIDE_NO_MAIN
#include "search_qfull_one_move_random_wide.cpp"
#undef FULLH_RANDOM_WIDE_NO_MAIN

constexpr const char* TRAP_GRAPH6 =
    "ahc?GC@?G?_`_?C?g?G?@@?C?GGC?G?GCG?@??CG@??_??@G??@????_???"
    "GA??@????C???@G?_??G???@C????H??_@?G";

constexpr std::array<unsigned char, 51> TRAP_FLOW = {
    2,5,2,1,6,6,2,4,2,5,4,2,3,4,6,7,2,
    5,2,6,7,4,4,3,6,7,7,1,3,6,6,5,3,7,
    5,2,3,6,1,7,1,5,7,4,2,3,2,1,5,6,3,
};

constexpr std::array<std::array<int, 2>, 51> FIVE_CDC_LABELS = {{
    {2,4},{4,5},{3,4},{3,4},{1,4},{4,5},{2,4},{2,3},{1,3},
    {1,4},{3,5},{4,5},{2,3},{1,3},{3,5},{2,5},{1,5},{1,2},
    {3,4},{1,3},{1,5},{1,4},{2,5},{4,5},{3,4},{2,4},{1,3},
    {2,3},{2,3},{1,2},{1,2},{1,3},{2,3},{3,5},{3,4},{4,5},
    {2,4},{3,4},{2,3},{2,4},{2,5},{2,3},{3,4},{3,5},{3,4},
    {4,5},{3,4},{3,5},{2,5},{2,4},{4,5},
}};

int trap_success_mask(const Graph& graph, const DirectFlow& flow) {
  constexpr std::array<int, 7> planes = {
      0x0f, 0x33, 0x55, 0x69, 0x99, 0xa5, 0xc3};
  int mask = 0;
  for (int index = 0; index < 7; ++index) {
    if (full_h_circuit_switch_soluble(graph, flow, planes[index])) {
      mask |= 1 << index;
    }
  }
  return mask;
}

bool three_edge_colourable(
    const Graph& graph, std::vector<int> colours, uint64_t& nodes) {
  ++nodes;
  while (true) {
    bool changed = false;
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      int used = 0;
      int uncoloured = -1;
      int uncoloured_count = 0;
      for (const int edge : graph.incidence[vertex]) {
        if (colours[edge] < 0) {
          uncoloured = edge;
          ++uncoloured_count;
        } else {
          const int bit = 1 << colours[edge];
          if (used & bit) return false;
          used |= bit;
        }
      }
      if (!uncoloured_count) {
        if (used != 7) return false;
      } else if (uncoloured_count == 1) {
        const int available = 7 ^ used;
        if (__builtin_popcount(available) != 1) return false;
        const int colour = __builtin_ctz(available);
        if (colours[uncoloured] >= 0 &&
            colours[uncoloured] != colour) {
          return false;
        }
        if (colours[uncoloured] < 0) {
          colours[uncoloured] = colour;
          changed = true;
        }
      }
    }
    if (!changed) break;
  }

  int chosen = -1;
  int chosen_available = 0;
  int chosen_count = 4;
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (colours[edge] >= 0) continue;
    int available = 7;
    for (const int vertex : graph.edges[edge]) {
      for (const int adjacent : graph.incidence[vertex]) {
        if (colours[adjacent] >= 0) {
          available &= ~(1 << colours[adjacent]);
        }
      }
    }
    const int count = __builtin_popcount(available);
    if (!count) return false;
    if (count < chosen_count) {
      chosen = edge;
      chosen_available = available;
      chosen_count = count;
    }
  }
  if (chosen < 0) return true;
  for (int colour = 0; colour < 3; ++colour) {
    if (!(chosen_available & (1 << colour))) continue;
    auto branch = colours;
    branch[chosen] = colour;
    if (three_edge_colourable(graph, std::move(branch), nodes)) {
      return true;
    }
  }
  return false;
}

bool is_simple(const Graph& graph) {
  std::set<std::array<int, 2>> seen;
  for (auto edge : graph.edges) {
    if (edge[0] == edge[1]) return false;
    if (edge[0] > edge[1]) std::swap(edge[0], edge[1]);
    if (!seen.insert(edge).second) return false;
  }
  return true;
}

int graph_girth(const Graph& graph) {
  int answer = graph.n + 1;
  for (int start = 0; start < graph.n; ++start) {
    std::vector<int> distance(graph.n, -1);
    std::vector<int> parent_edge(graph.n, -1);
    std::queue<int> queue;
    distance[start] = 0;
    queue.push(start);
    while (!queue.empty()) {
      const int vertex = queue.front();
      queue.pop();
      for (const int edge : graph.incidence[vertex]) {
        const int other =
            graph.edges[edge][0] ^ graph.edges[edge][1] ^ vertex;
        if (distance[other] < 0) {
          distance[other] = distance[vertex] + 1;
          parent_edge[other] = edge;
          queue.push(other);
        } else if (parent_edge[vertex] != edge) {
          answer = std::min(
              answer, distance[vertex] + distance[other] + 1);
        }
      }
    }
  }
  return answer;
}

bool has_cyclic_separation(
    const Graph& graph, const std::vector<int>& removed) {
  std::vector<char> is_removed(graph.m(), false);
  for (const int edge : removed) is_removed[edge] = true;
  std::vector<int> component(graph.n, -1);
  int components = 0;
  for (int start = 0; start < graph.n; ++start) {
    if (component[start] >= 0) continue;
    std::queue<int> queue;
    component[start] = components;
    queue.push(start);
    while (!queue.empty()) {
      const int vertex = queue.front();
      queue.pop();
      for (const int edge : graph.incidence[vertex]) {
        if (is_removed[edge]) continue;
        const int other =
            graph.edges[edge][0] ^ graph.edges[edge][1] ^ vertex;
        if (component[other] < 0) {
          component[other] = components;
          queue.push(other);
        }
      }
    }
    ++components;
  }
  std::vector<int> vertices(components);
  std::vector<int> edges(components);
  for (const int value : component) ++vertices[value];
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (is_removed[edge]) continue;
    const auto [left, right] = graph.edges[edge];
    assert(component[left] == component[right]);
    ++edges[component[left]];
  }
  int cyclic_components = 0;
  for (int index = 0; index < components; ++index) {
    if (edges[index] >= vertices[index]) ++cyclic_components;
  }
  return cyclic_components >= 2;
}

bool find_cyclic_cut(
    const Graph& graph, int target_size, int first,
    std::vector<int>& chosen) {
  if (static_cast<int>(chosen.size()) == target_size) {
    return has_cyclic_separation(graph, chosen);
  }
  const int still_needed = target_size - static_cast<int>(chosen.size());
  for (int edge = first; edge <= graph.m() - still_needed; ++edge) {
    chosen.push_back(edge);
    if (find_cyclic_cut(graph, target_size, edge + 1, chosen)) return true;
    chosen.pop_back();
  }
  return false;
}

int cyclic_edge_connectivity_through_four(
    const Graph& graph, std::vector<int>& witness) {
  for (int size = 1; size <= 4; ++size) {
    witness.clear();
    if (find_cyclic_cut(graph, size, 0, witness)) return size;
  }
  witness.clear();
  return 5;
}

bool five_cdc_labels_valid(const Graph& graph) {
  for (int edge = 0; edge < graph.m(); ++edge) {
    const auto [first, second] = FIVE_CDC_LABELS[edge];
    if (first < 1 || second > 5 || first >= second) return false;
  }
  for (int vertex = 0; vertex < graph.n; ++vertex) {
    for (int index = 1; index <= 5; ++index) {
      int degree = 0;
      for (const int edge : graph.incidence[vertex]) {
        degree ^= FIVE_CDC_LABELS[edge][0] == index;
        degree ^= FIVE_CDC_LABELS[edge][1] == index;
      }
      if (degree) return false;
    }
  }
  return true;
}

DirectFlow apply_move(
    const Graph& graph, const DirectFlow& flow,
    uint64_t cycle, int increment, bool& legal) {
  DirectFlow changed = flow;
  legal = true;
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (!((cycle >> edge) & 1U)) continue;
    changed[edge] ^= increment;
    if (!changed[edge]) legal = false;
  }
  return changed;
}

void print_flow_json(const Graph& graph, const DirectFlow& flow) {
  std::cout << '[';
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (edge) std::cout << ',';
    std::cout << static_cast<int>(flow[edge]);
  }
  std::cout << ']';
}

int main() {
  const Graph graph = parse_graph6(TRAP_GRAPH6);
  assert(graph.n == 34 && graph.m() == 51);
  assert(is_simple(graph));
  assert(is_cubic_connected(graph));
  assert(is_bridgeless(graph));
  const int girth = graph_girth(graph);
  assert(girth == 5);
  std::vector<int> cyclic_cut;
  const int cyclic_connectivity =
      cyclic_edge_connectivity_through_four(graph, cyclic_cut);
  assert(cyclic_connectivity == 4);
  assert(cyclic_cut.size() == 4);
  assert(five_cdc_labels_valid(graph));

  DirectFlow flow{};
  for (int edge = 0; edge < graph.m(); ++edge) {
    flow[edge] = TRAP_FLOW[edge];
  }
  for (int vertex = 0; vertex < graph.n; ++vertex) {
    int sum = 0;
    for (const int edge : graph.incidence[vertex]) sum ^= flow[edge];
    assert(sum == 0);
  }
  assert(random_wide_span_rank(graph, flow) == 3);
  assert(trap_success_mask(graph, flow) == 0);

  uint64_t colouring_nodes = 0;
  const bool tait = three_edge_colourable(
      graph, std::vector<int>(graph.m(), -1), colouring_nodes);
  assert(!tait);

  const auto basis = wide64_cycle_basis(graph);
  const auto cycles = wide64_cycles(basis);
  assert(basis.size() == 18);
  assert(cycles.size() == (uint64_t{1} << 18));
  for (const uint64_t cycle : cycles) {
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      int degree = 0;
      for (const int edge : graph.incidence[vertex]) {
        degree ^= (cycle >> edge) & 1U;
      }
      assert(degree == 0);
    }
  }

  uint64_t legal_moves = 0;
  std::array<uint64_t, 8> legal_by_increment{};
  uint64_t neighbour_checksum = 1469598103934665603ULL;
  struct Move {
    uint64_t cycle = 0;
    int increment = 0;
    DirectFlow flow{};
  };
  std::vector<Move> neighbours;
  for (const uint64_t cycle : cycles) {
    if (!cycle) continue;
    for (int increment = 1; increment < 8; ++increment) {
      bool legal = false;
      DirectFlow changed =
          apply_move(graph, flow, cycle, increment, legal);
      if (!legal) continue;
      ++legal_moves;
      ++legal_by_increment[increment];
      assert(trap_success_mask(graph, changed) == 0);
      neighbours.push_back({cycle, increment, changed});
      for (int edge = 0; edge < graph.m(); ++edge) {
        neighbour_checksum ^= changed[edge];
        neighbour_checksum *= 1099511628211ULL;
      }
      neighbour_checksum ^= cycle;
      neighbour_checksum *= 1099511628211ULL;
      neighbour_checksum ^= increment;
      neighbour_checksum *= 1099511628211ULL;
    }
  }
  assert(neighbours.size() == legal_moves);

  bool distance_two_found = false;
  uint64_t second_move_tests = 0;
  Move first_escape_move;
  uint64_t second_escape_cycle = 0;
  int second_escape_increment = 0;
  DirectFlow escape_flow{};
  int escape_success_mask = 0;
  for (const Move& first_move : neighbours) {
    for (const uint64_t cycle : cycles) {
      if (!cycle) continue;
      for (int increment = 1; increment < 8; ++increment) {
        ++second_move_tests;
        bool legal = false;
        DirectFlow changed = apply_move(
            graph, first_move.flow, cycle, increment, legal);
        if (!legal) continue;
        const int mask = trap_success_mask(graph, changed);
        if (!mask) continue;
        first_escape_move = first_move;
        second_escape_cycle = cycle;
        second_escape_increment = increment;
        escape_flow = changed;
        escape_success_mask = mask;
        distance_two_found = true;
        break;
      }
      if (distance_two_found) break;
    }
    if (distance_two_found) break;
  }
  assert(distance_two_found);

  std::cout
      << "{\"schema\":\"fullh-order34-local-trap-certificate-v1\""
      << ",\"graph6\":\"" << TRAP_GRAPH6 << "\""
      << ",\"vertices\":" << graph.n
      << ",\"edges\":" << graph.m()
      << ",\"simple_cubic_connected_bridgeless\":true"
      << ",\"girth\":" << girth
      << ",\"cyclic_edge_connectivity\":" << cyclic_connectivity
      << ",\"cyclic_cut_witness\":[";
  for (std::size_t index = 0; index < cyclic_cut.size(); ++index) {
    if (index) std::cout << ',';
    std::cout << cyclic_cut[index];
  }
  std::cout << "]"
      << ",\"three_edge_colourable\":false"
      << ",\"three_edge_colour_search_nodes\":" << colouring_nodes
      << ",\"flow_rank\":3"
      << ",\"trap_flow\":";
  print_flow_json(graph, flow);
  std::cout
      << ",\"initial_success_mask\":0"
      << ",\"cycle_dimension\":" << basis.size()
      << ",\"cycle_count\":" << cycles.size()
      << ",\"legal_moves\":" << legal_moves
      << ",\"legal_by_increment\":[";
  for (int increment = 1; increment < 8; ++increment) {
    if (increment > 1) std::cout << ',';
    std::cout << legal_by_increment[increment];
  }
  std::cout << "]"
            << ",\"successful_neighbours\":0"
            << ",\"neighbour_checksum_fnv64\":\""
            << std::hex << std::setw(16) << std::setfill('0')
            << neighbour_checksum << std::dec << "\""
            << ",\"shortest_success_distance\":2"
            << ",\"distance_two_search_tests\":" << second_move_tests
            << ",\"escape_first_cycle\":" << first_escape_move.cycle
            << ",\"escape_first_increment\":"
            << first_escape_move.increment
            << ",\"escape_middle_flow\":";
  print_flow_json(graph, first_escape_move.flow);
  std::cout << ",\"escape_second_cycle\":" << second_escape_cycle
            << ",\"escape_second_increment\":"
            << second_escape_increment
            << ",\"escape_final_flow\":";
  print_flow_json(graph, escape_flow);
  std::cout << ",\"escape_final_success_mask\":" << escape_success_mask
            << ",\"five_cdc_labels_valid\":true"
            << ",\"five_cdc_edge_labels\":[";
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (edge) std::cout << ',';
    std::cout << '[' << FIVE_CDC_LABELS[edge][0] << ','
              << FIVE_CDC_LABELS[edge][1] << ']';
  }
  std::cout << "]}\n";
}
