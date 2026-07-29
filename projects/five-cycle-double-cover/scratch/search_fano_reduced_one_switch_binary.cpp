#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <cstdint>
#include <functional>
#include <fstream>
#include <iostream>
#include <random>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

struct Key {
  std::uint64_t lo = 0;
  std::uint64_t hi = 0;
  bool operator==(const Key&) const = default;
};

struct KeyHash {
  std::size_t operator()(const Key& key) const {
    return std::hash<std::uint64_t>{}(key.lo) ^
           (std::hash<std::uint64_t>{}(key.hi) << 1);
  }
};

void add_clause(CaDiCaL::Solver& solver,
                const std::vector<int>& clause) {
  for (const int literal : clause) solver.add(literal);
  solver.add(0);
}

void add_xor(CaDiCaL::Solver& solver,
             const std::vector<int>& variables, int target) {
  std::vector<int> reduced;
  for (const int literal : variables) {
    if (literal > 0) {
      reduced.push_back(literal);
    } else {
      reduced.push_back(-literal);
      target ^= 1;
    }
  }
  const int assignments = 1 << reduced.size();
  for (int assignment = 0; assignment < assignments; ++assignment) {
    if ((__builtin_popcount(static_cast<unsigned>(assignment)) & 1) ==
        target) {
      continue;
    }
    std::vector<int> clause;
    for (int bit = 0; bit < static_cast<int>(reduced.size()); ++bit) {
      clause.push_back((assignment >> bit) & 1 ? -reduced[bit]
                                               : reduced[bit]);
    }
    add_clause(solver, clause);
  }
}

bool selected(const Key& key, const int edge) {
  return edge < 64 ? ((key.lo >> edge) & 1)
                   : ((key.hi >> (edge - 64)) & 1);
}

void insert(Key& key, const int edge) {
  if (edge < 64) {
    key.lo |= std::uint64_t{1} << edge;
  } else {
    key.hi |= std::uint64_t{1} << (edge - 64);
  }
}

void erase(Key& key, const int edge) {
  if (edge < 64) {
    key.lo &= ~(std::uint64_t{1} << edge);
  } else {
    key.hi &= ~(std::uint64_t{1} << (edge - 64));
  }
}

struct Graph {
  int vertices = 0;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::vector<int>> incidence;
  std::vector<Key> cycle_basis;
};

Graph decode_graph6(const std::string& record) {
  if (record.empty() || static_cast<unsigned char>(record[0]) < 63) {
    throw std::runtime_error("unsupported graph6 record");
  }
  const int n = static_cast<unsigned char>(record[0]) - 63;
  if (n > 62) throw std::runtime_error("large graph6 unsupported");
  std::vector<int> bits;
  for (std::size_t index = 1; index < record.size(); ++index) {
    const int value = static_cast<unsigned char>(record[index]) - 63;
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }
  Graph graph;
  graph.vertices = n;
  graph.incidence.resize(n);
  int cursor = 0;
  for (int right = 1; right < n; ++right) {
    for (int left = 0; left < right; ++left) {
      if (cursor >= static_cast<int>(bits.size())) {
        throw std::runtime_error("truncated graph6");
      }
      if (bits[cursor++]) {
        const int edge = graph.edges.size();
        graph.edges.emplace_back(left, right);
        graph.incidence[left].push_back(edge);
        graph.incidence[right].push_back(edge);
      }
    }
  }
  if (graph.edges.size() > 128) {
    throw std::runtime_error("more than 128 edges unsupported");
  }
  for (const auto& row : graph.incidence) {
    if (row.size() != 3) throw std::runtime_error("graph not cubic");
  }

  std::vector<int> parent(n, -1), parent_edge(n, -1), depth(n, 0);
  parent[0] = 0;
  std::vector<int> stack = {0};
  while (!stack.empty()) {
    const int vertex = stack.back();
    stack.pop_back();
    for (const int edge : graph.incidence[vertex]) {
      const auto [u, v] = graph.edges[edge];
      const int other = u ^ v ^ vertex;
      if (parent[other] >= 0) continue;
      parent[other] = vertex;
      parent_edge[other] = edge;
      depth[other] = depth[vertex] + 1;
      stack.push_back(other);
    }
  }
  if (std::find(parent.begin(), parent.end(), -1) != parent.end()) {
    throw std::runtime_error("graph disconnected");
  }
  std::vector<bool> tree(graph.edges.size(), false);
  for (int vertex = 1; vertex < n; ++vertex) tree[parent_edge[vertex]] = true;
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    if (tree[edge]) continue;
    Key cycle;
    insert(cycle, edge);
    auto [left0, right0] = graph.edges[edge];
    int left = left0, right = right0;
    while (depth[left] > depth[right]) {
      insert(cycle, parent_edge[left]);
      left = parent[left];
    }
    while (depth[right] > depth[left]) {
      insert(cycle, parent_edge[right]);
      right = parent[right];
    }
    while (left != right) {
      insert(cycle, parent_edge[left]);
      left = parent[left];
      insert(cycle, parent_edge[right]);
      right = parent[right];
    }
    graph.cycle_basis.push_back(cycle);
  }
  return graph;
}

struct PackingOracle {
  const Graph& graph;
  std::unordered_map<Key, bool, KeyHash> cache;

  explicit PackingOracle(const Graph& graph_) : graph(graph_) {}

  bool packs(const Key matching) {
    const auto known = cache.find(matching);
    if (known != cache.end()) return known->second;
    const int m = graph.edges.size();
    std::vector<int> terminal(graph.vertices, 0);
    for (int edge = 0; edge < m; ++edge) {
      if (!selected(matching, edge)) continue;
      terminal[graph.edges[edge].first] ^= 1;
      terminal[graph.edges[edge].second] ^= 1;
    }
    CaDiCaL::Solver solver;
    for (int edge = 0; edge < m; ++edge) {
      if (!selected(matching, edge)) {
        add_clause(solver, {-(edge + 1), -(m + edge + 1)});
      }
    }
    for (int vertex = 0; vertex < graph.vertices; ++vertex) {
      std::vector<int> red, blue;
      for (const int edge : graph.incidence[vertex]) {
        if (!selected(matching, edge)) {
          red.push_back(edge + 1);
          blue.push_back(m + edge + 1);
        }
      }
      add_xor(solver, red, terminal[vertex]);
      add_xor(solver, blue, terminal[vertex]);
    }
    const bool answer = solver.solve() == 10;
    cache.emplace(matching, answer);
    return answer;
  }
};

std::array<Key, 7> classes(const std::vector<int>& flow) {
  std::array<Key, 7> result{};
  for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
    insert(result[flow[edge] - 1], edge);
  }
  return result;
}

bool good(const std::vector<int>& flow, PackingOracle& oracle) {
  for (const Key matching : classes(flow)) {
    if (oracle.packs(matching)) return true;
  }
  return false;
}

int dot_bit(const int functional, const int value) {
  return __builtin_parity(
      static_cast<unsigned>(functional & value));
}

int husek_samal_defect(const Graph& graph,
                       const std::vector<int>& flow,
                       const int functional) {
  // Components of the kernel side K_mu={e:mu(f(e))=0}.
  std::vector<int> component(graph.vertices, -1);
  int component_count = 0;
  for (int root = 0; root < graph.vertices; ++root) {
    if (component[root] >= 0) continue;
    component[root] = component_count++;
    std::vector<int> stack = {root};
    while (!stack.empty()) {
      const int vertex = stack.back();
      stack.pop_back();
      for (const int edge : graph.incidence[vertex]) {
        if (dot_bit(functional, flow[edge])) continue;
        const auto [u, v] = graph.edges[edge];
        const int other = u ^ v ^ vertex;
        if (component[other] < 0) {
          component[other] = component[root];
          stack.push_back(other);
        }
      }
    }
  }
  int affine_value = 0;
  for (int value = 1; value <= 7; ++value) {
    if (dot_bit(functional, value)) {
      affine_value = value;
      break;
    }
  }
  if (!affine_value) {
    throw std::runtime_error("zero functional in H-S defect");
  }
  std::vector<int> odd(component_count, 0);
  for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
    if (flow[edge] != affine_value) continue;
    const auto [u, v] = graph.edges[edge];
    odd[component[u]] ^= 1;
    odd[component[v]] ^= 1;
  }
  return std::count(odd.begin(), odd.end(), 1);
}

std::array<int, 7> husek_samal_profile(
    const Graph& graph, const std::vector<int>& flow) {
  std::array<int, 7> result{};
  for (int functional = 1; functional <= 7; ++functional) {
    result[functional - 1] =
        husek_samal_defect(graph, flow, functional);
  }
  return result;
}

bool husek_samal_good(const Graph& graph,
                      const std::vector<int>& flow) {
  const auto profile = husek_samal_profile(graph, flow);
  return std::find(profile.begin(), profile.end(), 0) != profile.end();
}

std::vector<int> support_components(
    const Graph& graph, const std::vector<int>& flow,
    const int functional) {
  std::vector<int> component(graph.vertices, -1);
  int count = 0;
  for (int start = 0; start < graph.vertices; ++start) {
    if (component[start] >= 0) continue;
    component[start] = count++;
    std::vector<int> stack = {start};
    while (!stack.empty()) {
      const int vertex = stack.back();
      stack.pop_back();
      for (const int edge : graph.incidence[vertex]) {
        if (!dot_bit(functional, flow[edge])) continue;
        const auto [u, v] = graph.edges[edge];
        const int other = u ^ v ^ vertex;
        if (component[other] < 0) {
          component[other] = component[start];
          stack.push_back(other);
        }
      }
    }
  }
  return component;
}

// Counts APX witnesses directly from the affine-complement components.
// A nonzero functional mu with mu(s)=0 defines U=ker(mu).  Equal unordered
// endpoint-component pairs are equivalent to a circuit meeting U precisely
// in the selected two s-edges.  The packing test is exact.
int affine_packing_pair_count(
    const Graph& graph, const std::vector<int>& flow,
    PackingOracle& oracle, int* witness_s = nullptr,
    int* witness_mu = nullptr, int* witness_p = nullptr,
    int* witness_q = nullptr) {
  const auto value_classes = classes(flow);
  int count = 0;
  for (int s = 1; s <= 7; ++s) {
    std::vector<int> same;
    for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
      if (flow[edge] == s) same.push_back(edge);
    }
    for (int mu = 1; mu <= 7; ++mu) {
      if (dot_bit(mu, s)) continue;
      const std::vector<int> component =
          support_components(graph, flow, mu);
      std::vector<std::array<int, 2>> type(same.size());
      for (int index = 0; index < static_cast<int>(same.size()); ++index) {
        const auto [u, v] = graph.edges[same[index]];
        type[index] = {component[u], component[v]};
        if (type[index][1] < type[index][0]) {
          std::swap(type[index][0], type[index][1]);
        }
      }
      for (int left = 0; left < static_cast<int>(same.size()); ++left) {
        for (int right = 0; right < left; ++right) {
          if (type[left] != type[right]) continue;
          Key reduced = value_classes[s - 1];
          erase(reduced, same[left]);
          erase(reduced, same[right]);
          if (!oracle.packs(reduced)) continue;
          if (!count && witness_s) {
            *witness_s = s;
            *witness_mu = mu;
            *witness_p = same[right];
            *witness_q = same[left];
          }
          ++count;
        }
      }
    }
  }
  return count;
}

std::vector<Key> all_circuits(const Graph& graph) {
  std::vector<Key> result;
  std::vector<bool> used(graph.vertices, false);
  std::vector<int> path;
  std::function<void(int, int, Key)> visit =
      [&](const int start, const int vertex, const Key support) {
        for (const int edge : graph.incidence[vertex]) {
          const auto [u, v] = graph.edges[edge];
          const int other = u ^ v ^ vertex;
          if (other == start) {
            if (path.size() >= 3 && path[1] < vertex) {
              Key circuit = support;
              insert(circuit, edge);
              result.push_back(circuit);
            }
            continue;
          }
          if (other < start || used[other]) continue;
          used[other] = true;
          path.push_back(other);
          Key next = support;
          insert(next, edge);
          visit(start, other, next);
          path.pop_back();
          used[other] = false;
        }
      };
  for (int start = 0; start < graph.vertices; ++start) {
    used[start] = true;
    path = {start};
    visit(start, start, Key{});
    used[start] = false;
  }
  return result;
}

bool connected_circuit_repair(
    const Graph& graph, const std::vector<Key>& circuits,
    const std::vector<int>& flow, PackingOracle& oracle,
    int* repair_value, Key* repair_circuit, std::uint64_t* tested) {
  const auto initial_classes = classes(flow);
  for (int t = 1; t <= 7; ++t) {
    for (const Key circuit : circuits) {
      if ((circuit.lo & initial_classes[t - 1].lo) ||
          (circuit.hi & initial_classes[t - 1].hi)) {
        continue;
      }
      ++*tested;
      std::vector<int> switched = flow;
      for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
        if (selected(circuit, edge)) switched[edge] ^= t;
      }
      if (good(switched, oracle)) {
        *repair_value = t;
        *repair_circuit = circuit;
        return true;
      }
    }
  }
  return false;
}

bool connected_circuit_repair_stream(
    const Graph& graph, const std::vector<int>& flow, PackingOracle& oracle,
    int* repair_value, Key* repair_circuit, std::uint64_t* tested,
    std::uint64_t* circuits_seen) {
  const auto initial_classes = classes(flow);
  std::vector<bool> used(graph.vertices, false);
  std::vector<int> path;
  for (int t = 1; t <= 7; ++t) {
    bool found = false;
    std::function<void(int, int, Key)> visit =
        [&](const int start, const int vertex, const Key support) {
          if (found) return;
          for (const int edge : graph.incidence[vertex]) {
            const auto [u, v] = graph.edges[edge];
            const int other = u ^ v ^ vertex;
            if (other == start) {
              if (path.size() < 3 || path[1] >= vertex) continue;
              Key circuit = support;
              insert(circuit, edge);
              ++*circuits_seen;
              if ((circuit.lo & initial_classes[t - 1].lo) ||
                  (circuit.hi & initial_classes[t - 1].hi)) {
                continue;
              }
              ++*tested;
              std::vector<int> switched = flow;
              for (int item = 0;
                   item < static_cast<int>(flow.size()); ++item) {
                if (selected(circuit, item)) switched[item] ^= t;
              }
              if (good(switched, oracle)) {
                *repair_value = t;
                *repair_circuit = circuit;
                found = true;
              }
              continue;
            }
            if (other < start || used[other]) continue;
            used[other] = true;
            path.push_back(other);
            Key next = support;
            insert(next, edge);
            visit(start, other, next);
            path.pop_back();
            used[other] = false;
            if (found) return;
          }
        };
    for (int start = 0; start < graph.vertices && !found; ++start) {
      used[start] = true;
      path = {start};
      visit(start, start, Key{});
      used[start] = false;
    }
    if (found) return true;
  }
  return false;
}

std::vector<int> switched_flow(const std::vector<int>& flow,
                               Key circuit, int value);

bool husek_samal_circuit_repair_stream(
    const Graph& graph, const std::vector<int>& flow,
    int* repair_value, Key* repair_circuit, std::uint64_t* tested,
    std::uint64_t* circuits_seen) {
  const auto initial_classes = classes(flow);
  std::vector<bool> used(graph.vertices, false);
  std::vector<int> path;
  for (int t = 1; t <= 7; ++t) {
    bool found = false;
    std::function<void(int, int, Key)> visit =
        [&](const int start, const int vertex, const Key support) {
          if (found) return;
          for (const int edge : graph.incidence[vertex]) {
            const auto [u, v] = graph.edges[edge];
            const int other = u ^ v ^ vertex;
            if (other == start) {
              if (path.size() < 3 || path[1] >= vertex) continue;
              Key circuit = support;
              insert(circuit, edge);
              ++*circuits_seen;
              if ((circuit.lo & initial_classes[t - 1].lo) ||
                  (circuit.hi & initial_classes[t - 1].hi)) {
                continue;
              }
              ++*tested;
              const std::vector<int> candidate =
                  switched_flow(flow, circuit, t);
              if (husek_samal_good(graph, candidate)) {
                *repair_value = t;
                *repair_circuit = circuit;
                found = true;
              }
              continue;
            }
            if (other < start || used[other]) continue;
            used[other] = true;
            path.push_back(other);
            Key next = support;
            insert(next, edge);
            visit(start, other, next);
            path.pop_back();
            used[other] = false;
            if (found) return;
          }
        };
    for (int start = 0; start < graph.vertices && !found; ++start) {
      used[start] = true;
      path = {start};
      visit(start, start, Key{});
      used[start] = false;
    }
    if (found) return true;
  }
  return false;
}

struct FlowSwitch {
  int value = 0;
  Key circuit;
};

std::vector<FlowSwitch> legal_flow_switches(
    const Graph& graph, const std::vector<Key>& circuits,
    const std::vector<int>& flow) {
  const auto value_classes = classes(flow);
  std::vector<FlowSwitch> result;
  for (int value = 1; value <= 7; ++value) {
    for (const Key circuit : circuits) {
      if ((circuit.lo & value_classes[value - 1].lo) ||
          (circuit.hi & value_classes[value - 1].hi)) {
        continue;
      }
      result.push_back({value, circuit});
    }
  }
  return result;
}

bool husek_samal_radius_two_repair(
    const Graph& graph, const std::vector<Key>& circuits,
    const std::vector<int>& flow, FlowSwitch* first_repair,
    FlowSwitch* second_repair, std::uint64_t* first_neighbors,
    std::uint64_t* second_neighbors) {
  const std::vector<FlowSwitch> first_moves =
      legal_flow_switches(graph, circuits, flow);
  for (const FlowSwitch& first : first_moves) {
    ++*first_neighbors;
    const std::vector<int> after_first =
        switched_flow(flow, first.circuit, first.value);
    if (husek_samal_good(graph, after_first)) {
      *first_repair = first;
      *second_repair = FlowSwitch{};
      return true;
    }
    const std::vector<FlowSwitch> second_moves =
        legal_flow_switches(graph, circuits, after_first);
    for (const FlowSwitch& second : second_moves) {
      ++*second_neighbors;
      const std::vector<int> after_second =
          switched_flow(after_first, second.circuit, second.value);
      if (husek_samal_good(graph, after_second)) {
        *first_repair = first;
        *second_repair = second;
        return true;
      }
    }
  }
  return false;
}

const std::array<std::array<int, 3>, 40> kCompositionSignatures = {{
    {{1,2,3}},{{1,2,3}},{{1,2,3}},{{1,2,3}},{{1,2,3}},
    {{1,2,3}},{{1,2,3}},{{1,2,3}},{{1,2,3}},{{1,2,3}},
    {{1,6,7}},{{3,4,7}},{{3,5,6}},{{2,5,7}},{{1,6,7}},
    {{2,4,6}},{{3,5,6}},{{1,4,5}},{{1,2,3}},{{2,4,6}},
    {{1,6,7}},{{3,4,7}},{{3,5,6}},{{2,5,7}},{{1,6,7}},
    {{2,4,6}},{{3,5,6}},{{1,4,5}},{{1,2,3}},{{2,4,6}},
    {{1,6,7}},{{3,4,7}},{{3,5,6}},{{2,5,7}},{{1,6,7}},
    {{2,4,6}},{{3,5,6}},{{1,4,5}},{{1,2,3}},{{2,4,6}}
}};

struct LabeledEdge {
  std::array<int, 2> endpoints;
  int value;
};

const std::array<LabeledEdge, 60> kCompositionEdges = {{
  {{{0,1}},1},{{{10,13}},7},{{{10,16}},6},{{{10,17}},1},
  {{{11,14}},7},{{{11,16}},3},{{{11,17}},4},{{{12,15}},6},
  {{{12,17}},5},{{{12,18}},3},{{{13,16}},5},{{{14,18}},1},
  {{{14,19}},6},{{{15,18}},2},{{{15,19}},4},{{{0,13}},2},
  {{{2,19}},2},{{{0,3}},3},{{{2,3}},1},{{{4,5}},3},
  {{{4,6}},1},{{{20,23}},7},{{{20,26}},6},{{{20,27}},1},
  {{{21,24}},7},{{{21,26}},3},{{{21,27}},4},{{{22,25}},6},
  {{{22,27}},5},{{{22,28}},3},{{{23,26}},5},{{{24,28}},1},
  {{{24,29}},6},{{{25,28}},2},{{{25,29}},4},{{{5,23}},2},
  {{{6,29}},2},{{{30,33}},7},{{{30,36}},6},{{{30,37}},1},
  {{{31,34}},7},{{{31,36}},3},{{{31,37}},4},{{{32,35}},6},
  {{{32,37}},5},{{{32,38}},3},{{{33,36}},5},{{{34,38}},1},
  {{{34,39}},6},{{{35,38}},2},{{{35,39}},4},{{{1,33}},2},
  {{{7,39}},2},{{{6,7}},3},{{{1,8}},3},{{{4,8}},2},
  {{{5,8}},1},{{{2,9}},3},{{{3,9}},2},{{{7,9}},1}
}};

bool perturbed_composition_graph(std::mt19937_64& random,
                                 const int switches, Graph* graph,
                                 std::vector<int>* flow) {
  std::vector<LabeledEdge> labeled(
      kCompositionEdges.begin(), kCompositionEdges.end());
  for (int step = 0; step < switches; ++step) {
    bool changed = false;
    for (int attempt = 0; attempt < 1000 && !changed; ++attempt) {
      const int first = random() % labeled.size();
      std::vector<int> same;
      for (int edge = 0; edge < static_cast<int>(labeled.size()); ++edge) {
        if (edge != first &&
            labeled[edge].value == labeled[first].value) {
          same.push_back(edge);
        }
      }
      const int second = same[random() % same.size()];
      const auto [a, b] = labeled[first].endpoints;
      const auto [c, d] = labeled[second].endpoints;
      std::array<int, 2> new_first, new_second;
      if (random() & 1) {
        new_first = {a, c};
        new_second = {b, d};
      } else {
        new_first = {a, d};
        new_second = {b, c};
      }
      if (new_first[0] == new_first[1] ||
          new_second[0] == new_second[1]) {
        continue;
      }
      auto normalized = [](std::array<int, 2> edge) {
        if (edge[1] < edge[0]) std::swap(edge[0], edge[1]);
        return edge;
      };
      new_first = normalized(new_first);
      new_second = normalized(new_second);
      bool duplicate = new_first == new_second;
      for (int edge = 0; edge < static_cast<int>(labeled.size()); ++edge) {
        if (edge == first || edge == second) continue;
        const auto old = normalized(labeled[edge].endpoints);
        duplicate |= old == new_first || old == new_second;
      }
      if (duplicate) continue;
      labeled[first].endpoints = new_first;
      labeled[second].endpoints = new_second;
      changed = true;
    }
    if (!changed) return false;
  }
  graph->vertices = 40;
  graph->edges.clear();
  graph->incidence.assign(40, {});
  flow->clear();
  for (const LabeledEdge& edge : labeled) {
    const int index = graph->edges.size();
    graph->edges.emplace_back(edge.endpoints[0], edge.endpoints[1]);
    graph->incidence[edge.endpoints[0]].push_back(index);
    graph->incidence[edge.endpoints[1]].push_back(index);
    flow->push_back(edge.value);
  }
  return true;
}

bool random_signature_graph(std::mt19937_64& random, Graph* graph,
                            std::vector<int>* flow) {
  std::array<std::vector<int>, 8> endpoints;
  for (int vertex = 0; vertex < 40; ++vertex) {
    for (const int value : kCompositionSignatures[vertex]) {
      endpoints[value].push_back(vertex);
    }
  }
  graph->vertices = 40;
  graph->edges.clear();
  graph->incidence.assign(40, {});
  flow->clear();
  std::array<std::array<bool, 40>, 40> adjacent{};
  for (int value = 1; value <= 7; ++value) {
    std::shuffle(endpoints[value].begin(), endpoints[value].end(), random);
    for (int index = 0; index < static_cast<int>(endpoints[value].size());
         index += 2) {
      const int u = endpoints[value][index];
      const int v = endpoints[value][index + 1];
      if (u == v || adjacent[u][v]) return false;
      adjacent[u][v] = adjacent[v][u] = true;
      const int edge = graph->edges.size();
      graph->edges.emplace_back(u, v);
      graph->incidence[u].push_back(edge);
      graph->incidence[v].push_back(edge);
      flow->push_back(value);
    }
  }
  return graph->edges.size() == 60;
}

bool connected_after_removal(const Graph& graph,
                             const std::array<int, 3>& removed,
                             const int removed_count,
                             int* cyclic_components) {
  std::vector<int> component(graph.vertices, -1);
  int count = 0;
  *cyclic_components = 0;
  for (int start = 0; start < graph.vertices; ++start) {
    if (component[start] >= 0) continue;
    component[start] = count;
    std::vector<int> queue = {start};
    int edges_twice = 0;
    for (std::size_t cursor = 0; cursor < queue.size(); ++cursor) {
      const int vertex = queue[cursor];
      for (const int edge : graph.incidence[vertex]) {
        bool deleted = false;
        for (int item = 0; item < removed_count; ++item) {
          deleted |= edge == removed[item];
        }
        if (deleted) continue;
        ++edges_twice;
        const auto [u, v] = graph.edges[edge];
        const int other = u ^ v ^ vertex;
        if (component[other] < 0) {
          component[other] = count;
          queue.push_back(other);
        }
      }
    }
    if (edges_twice / 2 >= static_cast<int>(queue.size())) {
      ++*cyclic_components;
    }
    ++count;
  }
  return count == 1;
}

bool cyclically_four(const Graph& graph, const bool require_girth_five) {
  // Every edge must have distance at least four between its endpoints
  // after deletion: equivalently, there is no circuit of length <= 4.
  for (int forbidden = 0;
       require_girth_five &&
       forbidden < static_cast<int>(graph.edges.size()); ++forbidden) {
    const auto [source, target] = graph.edges[forbidden];
    std::vector<int> distance(graph.vertices, -1);
    distance[source] = 0;
    std::vector<int> queue = {source};
    for (std::size_t cursor = 0; cursor < queue.size(); ++cursor) {
      const int vertex = queue[cursor];
      if (distance[vertex] >= 3) continue;
      for (const int edge : graph.incidence[vertex]) {
        if (edge == forbidden) continue;
        const auto [u, v] = graph.edges[edge];
        const int other = u ^ v ^ vertex;
        if (distance[other] < 0) {
          distance[other] = distance[vertex] + 1;
          queue.push_back(other);
        }
      }
    }
    if (distance[target] >= 0 && distance[target] <= 3) return false;
  }
  const int m = graph.edges.size();
  for (int a = 0; a < m; ++a) {
    for (int b = -1; b < a; ++b) {
      for (int c = -1; c < b; ++c) {
        std::array<int, 3> removed = {a, b, c};
        const int count = 1 + (b >= 0) + (c >= 0);
        std::array<int, 3> normalized{};
        int cursor = 0;
        for (const int edge : removed) {
          if (edge >= 0) normalized[cursor++] = edge;
        }
        int cyclic_components = 0;
        connected_after_removal(
            graph, normalized, count, &cyclic_components);
        if (cyclic_components >= 2) return false;
      }
    }
  }
  return true;
}

bool clean_suppressed_core(const Graph& graph,
                           const std::vector<int>& flow, const int t) {
  std::vector<int> degree(graph.vertices, 0);
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    if (flow[edge] == t) continue;
    ++degree[graph.edges[edge].first];
    ++degree[graph.edges[edge].second];
  }
  std::vector<int> branch_index(graph.vertices, -1);
  int branches = 0;
  for (int vertex = 0; vertex < graph.vertices; ++vertex) {
    if (degree[vertex] == 3) branch_index[vertex] = branches++;
  }
  // A connected all-degree-two complement is one circuit.
  if (!branches) {
    std::vector<bool> seen(graph.vertices, false);
    std::vector<int> stack = {0};
    seen[0] = true;
    while (!stack.empty()) {
      const int vertex = stack.back();
      stack.pop_back();
      for (const int edge : graph.incidence[vertex]) {
        if (flow[edge] == t) continue;
        const auto [u, v] = graph.edges[edge];
        const int other = u ^ v ^ vertex;
        if (!seen[other]) {
          seen[other] = true;
          stack.push_back(other);
        }
      }
    }
    return std::find(seen.begin(), seen.end(), false) == seen.end();
  }
  std::vector<bool> used(graph.edges.size(), false);
  std::vector<std::pair<int, int>> core_edges;
  for (int start = 0; start < graph.vertices; ++start) {
    if (branch_index[start] < 0) continue;
    for (const int first_edge : graph.incidence[start]) {
      if (flow[first_edge] == t || used[first_edge]) continue;
      int edge = first_edge;
      int vertex = start;
      while (true) {
        used[edge] = true;
        const auto [u, v] = graph.edges[edge];
        const int other = u ^ v ^ vertex;
        vertex = other;
        if (branch_index[vertex] >= 0) {
          core_edges.emplace_back(
              branch_index[start], branch_index[vertex]);
          break;
        }
        int next = -1;
        for (const int candidate : graph.incidence[vertex]) {
          if (flow[candidate] != t && candidate != edge) {
            next = candidate;
            break;
          }
        }
        if (next < 0) return false;
        edge = next;
      }
    }
  }
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    if (flow[edge] != t && !used[edge]) return false;
  }
  auto components_after = [&](const int removed_a,
                              const int removed_b) {
    std::vector<std::vector<int>> adjacency(branches);
    for (int edge = 0; edge < static_cast<int>(core_edges.size()); ++edge) {
      if (edge == removed_a || edge == removed_b) continue;
      const auto [u, v] = core_edges[edge];
      adjacency[u].push_back(v);
      adjacency[v].push_back(u);
    }
    std::vector<bool> seen(branches, false);
    int components = 0;
    for (int start = 0; start < branches; ++start) {
      if (seen[start]) continue;
      ++components;
      seen[start] = true;
      std::vector<int> stack = {start};
      while (!stack.empty()) {
        const int vertex = stack.back();
        stack.pop_back();
        for (const int other : adjacency[vertex]) {
          if (!seen[other]) {
            seen[other] = true;
            stack.push_back(other);
          }
        }
      }
    }
    return components;
  };
  if (components_after(-1, -1) != 1) return false;
  for (int first = 0; first < static_cast<int>(core_edges.size()); ++first) {
    if (components_after(first, -1) != 1) return false;
    for (int second = 0; second < first; ++second) {
      if (components_after(first, second) != 1) return false;
    }
  }
  return true;
}

int rewire_search(const int samples, const std::uint64_t seed,
                  const int stop_after, const bool require_girth_five) {
  std::mt19937_64 random(seed);
  std::uint64_t generated = 0, simple = 0, premise = 0, bad = 0;
  for (int sample = 0; sample < samples; ++sample) {
    ++generated;
    Graph graph;
    std::vector<int> flow;
    if (!random_signature_graph(random, &graph, &flow)) continue;
    ++simple;
    if (!cyclically_four(graph, require_girth_five)) continue;
    ++premise;
    PackingOracle oracle(graph);
    if (good(flow, oracle)) continue;
    ++bad;
    int repair_value = 0;
    Key repair_circuit;
    std::uint64_t tested = 0, seen = 0;
    const bool repair = connected_circuit_repair_stream(
        graph, flow, oracle, &repair_value, &repair_circuit, &tested, &seen);
    std::cout << "{\"status\":\"REWIRED_BAD\",\"sample\":" << sample
              << ",\"connected_repair\":" << (repair ? "true" : "false")
              << ",\"repair_value\":" << repair_value
              << ",\"circuits_seen\":" << seen
              << ",\"legal_circuits_tested\":" << tested << ",\"edges\":[";
    for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
      if (edge) std::cout << ',';
      std::cout << '[' << graph.edges[edge].first << ','
                << graph.edges[edge].second << ',' << flow[edge] << ']';
    }
    std::cout << "],\"repair_circuit\":[";
    bool comma = false;
    for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
      if (!selected(repair_circuit, edge)) continue;
      if (comma) std::cout << ',';
      comma = true;
      std::cout << edge;
    }
    std::cout << "]}" << std::endl;
    if (!repair) {
      std::cerr << "generated=" << generated << " simple=" << simple
                << " premise=" << premise << " bad=" << bad << std::endl;
      return 3;
    }
    if (stop_after > 0 && bad >= static_cast<std::uint64_t>(stop_after)) {
      break;
    }
  }
  std::cout << "{\"status\":\"REWIRE_DONE\",\"generated\":" << generated
            << ",\"simple\":" << simple << ",\"premise\":" << premise
            << ",\"bad\":" << bad << "}" << std::endl;
  return 0;
}

int husek_samal_rewire_search(const int samples,
                              const std::uint64_t seed,
                              const bool require_girth_five) {
  std::mt19937_64 random(seed);
  std::uint64_t generated = 0, simple = 0, premise = 0, bad = 0;
  std::uint64_t legal_tested = 0, circuits_seen = 0;
  std::uint64_t maximum_tested = 0;
  for (int sample = 0; sample < samples; ++sample) {
    ++generated;
    Graph graph;
    std::vector<int> flow;
    if (!random_signature_graph(random, &graph, &flow)) continue;
    ++simple;
    if (!cyclically_four(graph, require_girth_five)) continue;
    ++premise;
    const auto initial_profile = husek_samal_profile(graph, flow);
    if (std::find(initial_profile.begin(), initial_profile.end(), 0) !=
        initial_profile.end()) {
      continue;
    }
    ++bad;
    int repair_value = 0;
    Key repair_circuit;
    std::uint64_t tested = 0, seen = 0;
    const bool repair = husek_samal_circuit_repair_stream(
        graph, flow, &repair_value, &repair_circuit, &tested, &seen);
    legal_tested += tested;
    circuits_seen += seen;
    maximum_tested = std::max(maximum_tested, tested);
    if (!repair) {
      std::cout << "{\"status\":\"HS_REWIRE_COUNTERMODEL\","
                << "\"sample\":" << sample
                << ",\"require_girth_five\":"
                << (require_girth_five ? "true" : "false")
                << ",\"initial_profile\":[";
      for (int index = 0; index < 7; ++index) {
        if (index) std::cout << ',';
        std::cout << initial_profile[index];
      }
      std::cout << "],\"circuits_seen\":" << seen
                << ",\"legal_switches_tested\":" << tested
                << ",\"edges\":[";
      for (int edge = 0; edge < static_cast<int>(graph.edges.size());
           ++edge) {
        if (edge) std::cout << ',';
        std::cout << '[' << graph.edges[edge].first << ','
                  << graph.edges[edge].second << ',' << flow[edge] << ']';
      }
      std::cout << "]}" << std::endl;
      return 3;
    }
  }
  std::cout << "{\"status\":\"HS_REWIRE_DONE\",\"generated\":"
            << generated << ",\"simple\":" << simple
            << ",\"premise\":" << premise << ",\"hs_bad\":" << bad
            << ",\"require_girth_five\":"
            << (require_girth_five ? "true" : "false")
            << ",\"circuits_seen_before_repairs\":" << circuits_seen
            << ",\"legal_switches_tested_before_repairs\":"
            << legal_tested
            << ",\"maximum_legal_switches_before_repair\":"
            << maximum_tested << "}" << std::endl;
  return 0;
}

int apx_rewire_search(const int samples, const std::uint64_t seed,
                      const int stop_after,
                      const bool require_girth_five) {
  std::mt19937_64 random(seed);
  std::uint64_t generated = 0, simple = 0, premise = 0, bad = 0;
  int minimum_score = 1 << 30;
  for (int sample = 0; sample < samples; ++sample) {
    ++generated;
    Graph graph;
    std::vector<int> flow;
    if (!random_signature_graph(random, &graph, &flow)) continue;
    ++simple;
    if (!cyclically_four(graph, require_girth_five)) continue;
    ++premise;
    PackingOracle oracle(graph);
    if (good(flow, oracle)) continue;
    ++bad;
    const int score = affine_packing_pair_count(graph, flow, oracle);
    if (score < minimum_score) {
      minimum_score = score;
      std::cerr << "sample=" << sample << " bad=" << bad
                << " best_apx=" << minimum_score
                << " cache=" << oracle.cache.size() << std::endl;
    }
    if (!score) {
      std::cout << "{\"status\":\"APX_REWIRE_COUNTERMODEL\",\"sample\":"
                << sample << ",\"edges\":[";
      for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
        if (edge) std::cout << ',';
        std::cout << '[' << graph.edges[edge].first << ','
                  << graph.edges[edge].second << ',' << flow[edge] << ']';
      }
      std::cout << "]}" << std::endl;
      return 3;
    }
    if (stop_after > 0 && bad >= static_cast<std::uint64_t>(stop_after)) {
      break;
    }
  }
  std::cout << "{\"status\":\"APX_REWIRE_DONE\",\"generated\":"
            << generated << ",\"simple\":" << simple
            << ",\"premise\":" << premise << ",\"bad\":" << bad
            << ",\"minimum_apx_witness_count\":"
            << (minimum_score == (1 << 30) ? -1 : minimum_score)
            << "}" << std::endl;
  return 0;
}

int perturb_search(const int samples, const std::uint64_t seed,
                   const int switches) {
  std::mt19937_64 random(seed);
  std::uint64_t premise = 0, bad = 0;
  std::uint64_t maximum_tested = 0;
  for (int sample = 0; sample < samples; ++sample) {
    Graph graph;
    std::vector<int> flow;
    if (!perturbed_composition_graph(
            random, switches, &graph, &flow)) continue;
    if (!cyclically_four(graph, false)) continue;
    ++premise;
    PackingOracle oracle(graph);
    if (good(flow, oracle)) continue;
    ++bad;
    int repair_value = 0;
    Key repair_circuit;
    std::uint64_t tested = 0, seen = 0;
    const bool repair = connected_circuit_repair_stream(
        graph, flow, oracle, &repair_value, &repair_circuit, &tested, &seen);
    maximum_tested = std::max(maximum_tested, tested);
    if (!repair) {
      std::cout << "{\"status\":\"PERTURB_COUNTERMODEL\",\"sample\":"
                << sample << ",\"switches\":" << switches
                << ",\"circuits_seen\":" << seen
                << ",\"legal_circuits_tested\":" << tested
                << ",\"edges\":[";
      for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
        if (edge) std::cout << ',';
        std::cout << '[' << graph.edges[edge].first << ','
                  << graph.edges[edge].second << ',' << flow[edge] << ']';
      }
      std::cout << "]}" << std::endl;
      return 3;
    }
  }
  std::cout << "{\"status\":\"PERTURB_DONE\",\"samples\":" << samples
            << ",\"switches\":" << switches << ",\"premise\":" << premise
            << ",\"bad\":" << bad
            << ",\"maximum_legal_circuits_tested_before_repair\":"
            << maximum_tested << "}" << std::endl;
  return 0;
}

std::vector<int> switched_flow(const std::vector<int>& flow,
                               const Key circuit, const int value) {
  std::vector<int> result = flow;
  for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
    if (selected(circuit, edge)) result[edge] ^= value;
  }
  return result;
}

std::vector<int> random_flow(const Graph& graph, std::mt19937_64& random,
                             std::uint64_t* trials);

int sampled_repair_score(const std::vector<int>& flow,
                         const std::vector<Key>& circuits,
                         PackingOracle& oracle, std::mt19937_64& random,
                         const int trials) {
  int repairs = 0;
  for (int trial = 0; trial < trials; ++trial) {
    const Key circuit = circuits[random() % circuits.size()];
    std::array<bool, 8> present{};
    for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
      if (selected(circuit, edge)) present[flow[edge]] = true;
    }
    std::vector<int> values;
    for (int value = 1; value <= 7; ++value) {
      if (!present[value]) values.push_back(value);
    }
    if (values.empty()) {
      --trial;
      continue;
    }
    const int value = values[random() % values.size()];
    repairs += good(switched_flow(flow, circuit, value), oracle);
  }
  return repairs;
}

int hill_search(const std::string& path, const int iterations,
                const std::uint64_t seed, const int score_trials) {
  std::ifstream input(path);
  std::string record;
  if (!input || !std::getline(input, record)) {
    throw std::runtime_error("cannot read hill graph");
  }
  Graph graph = decode_graph6(record);
  const std::vector<Key> circuits = all_circuits(graph);
  PackingOracle oracle(graph);
  std::mt19937_64 random(seed);
  std::uint64_t flow_trials = 0;
  std::vector<int> current;
  do {
    current = random_flow(graph, random, &flow_trials);
  } while (good(current, oracle));
  int current_score = sampled_repair_score(
      current, circuits, oracle, random, score_trials);
  std::vector<int> best = current;
  int best_score = current_score;
  for (int iteration = 0; iteration < iterations; ++iteration) {
    std::vector<int> candidate;
    bool found_bad_neighbor = false;
    for (int attempt = 0; attempt < 1000 && !found_bad_neighbor; ++attempt) {
      const Key circuit = circuits[random() % circuits.size()];
      std::array<bool, 8> present{};
      for (int edge = 0; edge < static_cast<int>(current.size()); ++edge) {
        if (selected(circuit, edge)) present[current[edge]] = true;
      }
      std::vector<int> values;
      for (int value = 1; value <= 7; ++value) {
        if (!present[value]) values.push_back(value);
      }
      if (values.empty()) continue;
      candidate = switched_flow(
          current, circuit, values[random() % values.size()]);
      found_bad_neighbor = !good(candidate, oracle);
    }
    if (!found_bad_neighbor) break;
    const int candidate_score = sampled_repair_score(
        candidate, circuits, oracle, random, score_trials);
    if (candidate_score <= current_score || random() % 20 == 0) {
      current = std::move(candidate);
      current_score = candidate_score;
    }
    if (current_score < best_score) {
      best = current;
      best_score = current_score;
      std::cerr << "iteration=" << iteration
                << " best_score=" << best_score
                << " cache=" << oracle.cache.size() << std::endl;
    }
  }
  int repair_value = 0;
  Key repair_circuit;
  std::uint64_t tested = 0;
  const bool repair = connected_circuit_repair(
      graph, circuits, best, oracle, &repair_value, &repair_circuit, &tested);
  std::cout << "{\"status\":\"HILL_DONE\",\"graph6\":\"" << record
            << "\",\"vertices\":" << graph.vertices
            << ",\"circuits\":" << circuits.size()
            << ",\"iterations\":" << iterations
            << ",\"score_trials\":" << score_trials
            << ",\"best_sampled_repairs\":" << best_score
            << ",\"connected_repair\":" << (repair ? "true" : "false")
            << ",\"exact_legal_circuits_tested\":" << tested
            << ",\"repair_value\":" << repair_value << ",\"flow\":[";
  for (int edge = 0; edge < static_cast<int>(best.size()); ++edge) {
    if (edge) std::cout << ',';
    std::cout << best[edge];
  }
  std::cout << "]}" << std::endl;
  return repair ? 0 : 3;
}

int apx_hill_search(const std::string& path, const int iterations,
                    const std::uint64_t seed, const int restarts) {
  std::ifstream input(path);
  std::string record;
  if (!input || !std::getline(input, record)) {
    throw std::runtime_error("cannot read APX hill graph");
  }
  Graph graph = decode_graph6(record);
  const std::vector<Key> circuits = all_circuits(graph);
  PackingOracle oracle(graph);
  std::mt19937_64 random(seed);
  std::uint64_t flow_trials = 0;
  int global_best = 1 << 30;
  std::vector<int> best;
  for (int restart = 0; restart < restarts; ++restart) {
    std::vector<int> current;
    do {
      current = random_flow(graph, random, &flow_trials);
    } while (good(current, oracle));
    int current_score =
        affine_packing_pair_count(graph, current, oracle);
    if (current_score < global_best) {
      global_best = current_score;
      best = current;
      std::cerr << "restart=" << restart
                << " best_apx=" << global_best
                << " cache=" << oracle.cache.size() << std::endl;
    }
    for (int iteration = 0;
         iteration < iterations && global_best; ++iteration) {
      std::vector<int> candidate;
      bool found_bad_neighbor = false;
      for (int attempt = 0; attempt < 1000 && !found_bad_neighbor;
           ++attempt) {
        const Key circuit = circuits[random() % circuits.size()];
        std::array<bool, 8> present{};
        for (int edge = 0; edge < static_cast<int>(current.size()); ++edge) {
          if (selected(circuit, edge)) present[current[edge]] = true;
        }
        std::vector<int> values;
        for (int value = 1; value <= 7; ++value) {
          if (!present[value]) values.push_back(value);
        }
        if (values.empty()) continue;
        candidate = switched_flow(
            current, circuit, values[random() % values.size()]);
        found_bad_neighbor = !good(candidate, oracle);
      }
      if (!found_bad_neighbor) break;
      const int candidate_score =
          affine_packing_pair_count(graph, candidate, oracle);
      if (candidate_score <= current_score || random() % 50 == 0) {
        current = std::move(candidate);
        current_score = candidate_score;
      }
      if (current_score < global_best) {
        global_best = current_score;
        best = current;
        std::cerr << "restart=" << restart
                  << " iteration=" << iteration
                  << " best_apx=" << global_best
                  << " cache=" << oracle.cache.size() << std::endl;
      }
    }
    if (!global_best) break;
  }
  int witness_s = 0, witness_mu = 0;
  int witness_p = -1, witness_q = -1;
  const int checked_score = affine_packing_pair_count(
      graph, best, oracle, &witness_s, &witness_mu,
      &witness_p, &witness_q);
  if (checked_score != global_best) {
    throw std::runtime_error("APX score replay mismatch");
  }
  std::cout << "{\"status\":\"APX_HILL_DONE\",\"graph6\":\"" << record
            << "\",\"vertices\":" << graph.vertices
            << ",\"circuits\":" << circuits.size()
            << ",\"iterations_per_restart\":" << iterations
            << ",\"restarts\":" << restarts
            << ",\"best_apx_witness_count\":" << global_best
            << ",\"witness_s\":" << witness_s
            << ",\"witness_mu\":" << witness_mu
            << ",\"witness_pair\":[" << witness_p << ',' << witness_q
            << "],\"flow\":[";
  for (int edge = 0; edge < static_cast<int>(best.size()); ++edge) {
    if (edge) std::cout << ',';
    std::cout << best[edge];
  }
  std::cout << "]}" << std::endl;
  return global_best ? 0 : 3;
}

int apx_neighborhood_search(const std::string& path,
                            const int rounds,
                            const std::uint64_t seed) {
  std::ifstream input(path);
  std::string record, flow_line;
  if (!input || !std::getline(input, record) ||
      !std::getline(input, flow_line)) {
    throw std::runtime_error("cannot read APX state");
  }
  Graph graph = decode_graph6(record);
  std::vector<int> current;
  std::stringstream parser(flow_line);
  std::string item;
  while (std::getline(parser, item, ',')) {
    current.push_back(std::stoi(item));
  }
  if (current.size() != graph.edges.size()) {
    throw std::runtime_error("APX state has wrong flow length");
  }
  const std::vector<Key> circuits = all_circuits(graph);
  PackingOracle oracle(graph);
  if (good(current, oracle)) {
    throw std::runtime_error("APX state is not bad");
  }
  std::mt19937_64 random(seed);
  int current_score =
      affine_packing_pair_count(graph, current, oracle);
  std::vector<int> best = current;
  int best_score = current_score;
  for (int round = 0; round < rounds && best_score; ++round) {
    std::vector<std::pair<Key, int>> moves;
    for (const Key circuit : circuits) {
      std::array<bool, 8> present{};
      for (int edge = 0; edge < static_cast<int>(current.size()); ++edge) {
        if (selected(circuit, edge)) present[current[edge]] = true;
      }
      for (int value = 1; value <= 7; ++value) {
        if (!present[value]) moves.emplace_back(circuit, value);
      }
    }
    std::shuffle(moves.begin(), moves.end(), random);
    int round_best = 1 << 30;
    std::vector<int> next;
    std::uint64_t bad_neighbors = 0;
    for (const auto& [circuit, value] : moves) {
      std::vector<int> candidate =
          switched_flow(current, circuit, value);
      if (good(candidate, oracle)) continue;
      ++bad_neighbors;
      const int score =
          affine_packing_pair_count(graph, candidate, oracle);
      if (score < round_best) {
        round_best = score;
        next = std::move(candidate);
      }
      if (!round_best) break;
    }
    std::cerr << "round=" << round << " current=" << current_score
              << " round_best=" << round_best
              << " bad_neighbors=" << bad_neighbors
              << " cache=" << oracle.cache.size() << std::endl;
    if (next.empty()) break;
    current = std::move(next);
    current_score = round_best;
    if (current_score < best_score) {
      best_score = current_score;
      best = current;
    }
    if (current_score >= best_score && current_score > 1) {
      // The full neighbourhood is expensive; move to its best state but
      // stop once no strict improvement of a non-minimal score is found.
      break;
    }
  }
  std::cout << "{\"status\":\"APX_NEIGHBORHOOD_DONE\",\"graph6\":\""
            << record << "\",\"vertices\":" << graph.vertices
            << ",\"rounds\":" << rounds
            << ",\"best_apx_witness_count\":" << best_score
            << ",\"flow\":[";
  for (int edge = 0; edge < static_cast<int>(best.size()); ++edge) {
    if (edge) std::cout << ',';
    std::cout << best[edge];
  }
  std::cout << "]}" << std::endl;
  return best_score ? 0 : 3;
}

int circuit_repair_audit(const std::string& path,
                         const bool stop_at_first) {
  std::ifstream input(path);
  std::string record, flow_line;
  if (!input || !std::getline(input, record) ||
      !std::getline(input, flow_line)) {
    throw std::runtime_error("cannot read circuit-audit state");
  }
  Graph graph = decode_graph6(record);
  std::vector<int> flow;
  std::stringstream parser(flow_line);
  std::string item;
  while (std::getline(parser, item, ',')) {
    flow.push_back(std::stoi(item));
  }
  if (flow.size() != graph.edges.size()) {
    throw std::runtime_error("circuit-audit flow has wrong length");
  }
  const std::vector<Key> circuits = all_circuits(graph);
  PackingOracle oracle(graph);
  if (good(flow, oracle)) {
    throw std::runtime_error("circuit-audit state is not bad");
  }
  const auto initial_classes = classes(flow);
  std::uint64_t legal = 0, repairs = 0;
  int first_value = 0;
  Key first_circuit;
  for (int value = 1; value <= 7; ++value) {
    for (const Key circuit : circuits) {
      if ((circuit.lo & initial_classes[value - 1].lo) ||
          (circuit.hi & initial_classes[value - 1].hi)) {
        continue;
      }
      ++legal;
      if (good(switched_flow(flow, circuit, value), oracle)) {
        ++repairs;
        if (!first_value) {
          first_value = value;
          first_circuit = circuit;
        }
        if (stop_at_first) break;
      }
    }
    if (stop_at_first && first_value) break;
  }
  std::cout << "{\"status\":\"CIRCUIT_REPAIR_AUDIT\","
            << "\"graph6\":\"" << record << "\",\"vertices\":"
            << graph.vertices << ",\"circuits\":" << circuits.size()
            << ",\"legal_switches_tested\":" << legal
            << ",\"good_switches\":" << repairs
            << ",\"complete\":" << (stop_at_first ? "false" : "true")
            << ",\"first_value\":" << first_value
            << ",\"first_circuit\":[";
  bool comma = false;
  for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
    if (!selected(first_circuit, edge)) continue;
    if (comma) std::cout << ',';
    comma = true;
    std::cout << edge;
  }
  std::cout << "]}" << std::endl;
  return 0;
}

int husek_samal_circuit_audit(const std::string& path,
                              const bool stop_at_first) {
  std::ifstream input(path);
  std::string record, flow_line;
  if (!input || !std::getline(input, record) ||
      !std::getline(input, flow_line)) {
    throw std::runtime_error("cannot read H-S circuit-audit state");
  }
  Graph graph = decode_graph6(record);
  std::vector<int> flow;
  std::stringstream parser(flow_line);
  std::string item;
  while (std::getline(parser, item, ',')) {
    flow.push_back(std::stoi(item));
  }
  if (flow.size() != graph.edges.size()) {
    throw std::runtime_error("H-S state has wrong flow length");
  }
  const auto initial_profile = husek_samal_profile(graph, flow);
  if (std::find(initial_profile.begin(), initial_profile.end(), 0) !=
      initial_profile.end()) {
    throw std::runtime_error("H-S state is already good");
  }
  const std::vector<Key> circuits = all_circuits(graph);
  const auto initial_classes = classes(flow);
  std::uint64_t legal = 0, repairs = 0;
  int first_value = 0;
  Key first_circuit;
  std::array<int, 7> first_profile{};
  for (int value = 1; value <= 7; ++value) {
    for (const Key circuit : circuits) {
      if ((circuit.lo & initial_classes[value - 1].lo) ||
          (circuit.hi & initial_classes[value - 1].hi)) {
        continue;
      }
      ++legal;
      const std::vector<int> candidate =
          switched_flow(flow, circuit, value);
      const auto candidate_profile =
          husek_samal_profile(graph, candidate);
      if (std::find(candidate_profile.begin(), candidate_profile.end(), 0) !=
          candidate_profile.end()) {
        ++repairs;
        if (!first_value) {
          first_value = value;
          first_circuit = circuit;
          first_profile = candidate_profile;
        }
        if (stop_at_first) break;
      }
    }
    if (stop_at_first && first_value) break;
  }
  std::cout << "{\"status\":\"HS_CIRCUIT_AUDIT\","
            << "\"graph6\":\"" << record << "\",\"vertices\":"
            << graph.vertices << ",\"circuits\":" << circuits.size()
            << ",\"initial_profile\":[";
  for (int index = 0; index < 7; ++index) {
    if (index) std::cout << ',';
    std::cout << initial_profile[index];
  }
  std::cout << "],\"legal_switches_tested\":" << legal
            << ",\"good_switches\":" << repairs
            << ",\"complete\":" << (stop_at_first ? "false" : "true")
            << ",\"first_value\":" << first_value
            << ",\"first_profile\":[";
  for (int index = 0; index < 7; ++index) {
    if (index) std::cout << ',';
    std::cout << first_profile[index];
  }
  std::cout << "],\"first_circuit\":[";
  bool comma = false;
  for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
    if (!selected(first_circuit, edge)) continue;
    if (comma) std::cout << ',';
    comma = true;
    std::cout << edge;
  }
  std::cout << "]}" << std::endl;
  return repairs ? 0 : 3;
}

// Search a stronger operation than the target lemma: X may be any binary
// cycle, possibly disconnected.  SAT therefore disproves nothing; UNSAT
// for all (t,b) pairs certifies no connected-circuit repair.
bool binary_cycle_repair(const Graph& graph, const std::vector<int>& flow,
                         const int t, const int b,
                         std::vector<int>* switched_edges) {
  if (t == b) return false;
  const int m = graph.edges.size();
  CaDiCaL::Solver solver;
  const auto x = [m](int edge) { return edge + 1; };
  const auto red = [m](int edge) { return m + edge + 1; };
  const auto blue = [m](int edge) { return 2 * m + edge + 1; };

  for (int edge = 0; edge < m; ++edge) {
    if (flow[edge] == t) add_clause(solver, {-x(edge)});
    add_clause(solver, {-red(edge), -blue(edge)});
    if (flow[edge] == b) {
      // m'_b = not x.
      add_clause(solver, {x(edge), -red(edge)});
      add_clause(solver, {x(edge), -blue(edge)});
    } else if (flow[edge] == (b ^ t)) {
      // m'_b = x.
      add_clause(solver, {-x(edge), -red(edge)});
      add_clause(solver, {-x(edge), -blue(edge)});
    }
  }
  for (int vertex = 0; vertex < graph.vertices; ++vertex) {
    std::vector<int> parity_x, parity_red, parity_blue;
    int target = 0;
    for (const int edge : graph.incidence[vertex]) {
      parity_x.push_back(x(edge));
      parity_red.push_back(red(edge));
      parity_blue.push_back(blue(edge));
      if (flow[edge] == b) {
        // Terminal contribution not(x): move x to the left and 1 right.
        parity_red.push_back(x(edge));
        parity_blue.push_back(x(edge));
        target ^= 1;
      } else if (flow[edge] == (b ^ t)) {
        parity_red.push_back(x(edge));
        parity_blue.push_back(x(edge));
      }
    }
    add_xor(solver, parity_x, 0);
    add_xor(solver, parity_red, target);
    add_xor(solver, parity_blue, target);
  }
  if (solver.solve() != 10) return false;
  if (switched_edges) {
    switched_edges->clear();
    for (int edge = 0; edge < m; ++edge) {
      if (solver.val(x(edge)) > 0) switched_edges->push_back(edge);
    }
  }
  return true;
}

Key random_cycle(const Graph& graph, std::mt19937_64& random) {
  Key result;
  for (const Key basis : graph.cycle_basis) {
    if (random() & 1) {
      result.lo ^= basis.lo;
      result.hi ^= basis.hi;
    }
  }
  return result;
}

std::vector<int> random_flow(const Graph& graph, std::mt19937_64& random,
                             std::uint64_t* trials) {
  const int m = graph.edges.size();
  while (true) {
    ++*trials;
    const Key a = random_cycle(graph, random);
    const Key b = random_cycle(graph, random);
    const Key c = random_cycle(graph, random);
    std::vector<int> flow(m);
    bool nowhere_zero = true;
    for (int edge = 0; edge < m; ++edge) {
      flow[edge] = selected(a, edge) | (selected(b, edge) << 1) |
                   (selected(c, edge) << 2);
      if (!flow[edge]) {
        nowhere_zero = false;
        break;
      }
    }
    if (nowhere_zero) return flow;
  }
}

int core_search(const std::string& path, const int samples,
                const std::uint64_t seed, const bool require_bad) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open " + path);
  std::mt19937_64 random(seed);
  std::string record;
  std::uint64_t graphs = 0, flows = 0, flow_trials = 0, bad = 0;
  while (std::getline(input, record)) {
    if (record.empty()) continue;
    Graph graph = decode_graph6(record);
    PackingOracle oracle(graph);
    ++graphs;
    for (int sample = 0; sample < samples; ++sample) {
      const std::vector<int> flow =
          random_flow(graph, random, &flow_trials);
      ++flows;
      const bool is_bad = !good(flow, oracle);
      bad += is_bad;
      if (require_bad && !is_bad) continue;
      std::vector<int> clean;
      for (int t = 1; t <= 7; ++t) {
        if (clean_suppressed_core(graph, flow, t)) clean.push_back(t);
      }
      if (clean.empty()) {
        std::cout << "{\"status\":\"CORE_COUNTERMODEL\",\"graph6\":\""
                  << record << "\",\"vertices\":" << graph.vertices
                  << ",\"bad\":" << (is_bad ? "true" : "false")
                  << ",\"flow\":[";
        for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
          if (edge) std::cout << ',';
          std::cout << flow[edge];
        }
        std::cout << "]}" << std::endl;
        return 3;
      }
    }
  }
  std::cout << "{\"status\":\"CORE_PASS\",\"graphs\":" << graphs
            << ",\"flows\":" << flows << ",\"bad\":" << bad
            << ",\"require_bad\":" << (require_bad ? "true" : "false")
            << ",\"flow_trials\":" << flow_trials << "}" << std::endl;
  return 0;
}

int apx_sample_search(const std::string& path, const int samples,
                      const std::uint64_t seed) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open " + path);
  std::mt19937_64 random(seed);
  std::string record;
  std::uint64_t graphs = 0, flows = 0, flow_trials = 0, bad = 0;
  int minimum_score = 1 << 30;
  while (std::getline(input, record)) {
    if (record.empty()) continue;
    Graph graph = decode_graph6(record);
    PackingOracle oracle(graph);
    ++graphs;
    for (int sample = 0; sample < samples; ++sample) {
      const std::vector<int> flow =
          random_flow(graph, random, &flow_trials);
      ++flows;
      if (good(flow, oracle)) continue;
      ++bad;
      const int score = affine_packing_pair_count(graph, flow, oracle);
      if (score < minimum_score) {
        minimum_score = score;
        std::cerr << "graph=" << graphs << " sample=" << sample
                  << " bad=" << bad << " best_apx=" << minimum_score
                  << " cache=" << oracle.cache.size() << std::endl;
      }
      if (!score) {
        std::cout << "{\"status\":\"APX_SAMPLE_COUNTERMODEL\","
                  << "\"graph6\":\"" << record
                  << "\",\"vertices\":" << graph.vertices
                  << ",\"flow\":[";
        for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
          if (edge) std::cout << ',';
          std::cout << flow[edge];
        }
        std::cout << "]}" << std::endl;
        return 3;
      }
    }
  }
  std::cout << "{\"status\":\"APX_SAMPLE_DONE\",\"graphs\":" << graphs
            << ",\"flows\":" << flows << ",\"bad\":" << bad
            << ",\"minimum_apx_witness_count\":"
            << (minimum_score == (1 << 30) ? -1 : minimum_score)
            << ",\"flow_trials\":" << flow_trials << "}" << std::endl;
  return 0;
}

int husek_samal_sample_search(const std::string& path,
                              const int samples,
                              const std::uint64_t seed,
                              const int stop_after_bad) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open " + path);
  std::mt19937_64 random(seed);
  std::string record;
  std::uint64_t graphs = 0, flows = 0, flow_trials = 0, bad = 0;
  std::uint64_t legal_tested = 0, circuits_seen = 0;
  std::uint64_t maximum_tested = 0;
  while (std::getline(input, record)) {
    if (record.empty()) continue;
    Graph graph = decode_graph6(record);
    ++graphs;
    for (int sample = 0; sample < samples; ++sample) {
      const std::vector<int> flow =
          random_flow(graph, random, &flow_trials);
      ++flows;
      const auto initial_profile = husek_samal_profile(graph, flow);
      if (std::find(initial_profile.begin(), initial_profile.end(), 0) !=
          initial_profile.end()) {
        continue;
      }
      ++bad;
      int repair_value = 0;
      Key repair_circuit;
      std::uint64_t tested = 0, seen = 0;
      const bool repair = husek_samal_circuit_repair_stream(
          graph, flow, &repair_value, &repair_circuit, &tested, &seen);
      legal_tested += tested;
      circuits_seen += seen;
      maximum_tested = std::max(maximum_tested, tested);
      if (!repair) {
        std::cout << "{\"status\":\"HS_SAMPLE_COUNTERMODEL\","
                  << "\"graph6\":\"" << record
                  << "\",\"vertices\":" << graph.vertices
                  << ",\"sample\":" << sample
                  << ",\"initial_profile\":[";
        for (int index = 0; index < 7; ++index) {
          if (index) std::cout << ',';
          std::cout << initial_profile[index];
        }
        std::cout << "],\"circuits_seen\":" << seen
                  << ",\"legal_switches_tested\":" << tested
                  << ",\"flow\":[";
        for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
          if (edge) std::cout << ',';
          std::cout << flow[edge];
        }
        std::cout << "]}" << std::endl;
        return 3;
      }
      if (stop_after_bad > 0 &&
          bad >= static_cast<std::uint64_t>(stop_after_bad)) {
        std::cout << "{\"status\":\"HS_SAMPLE_DONE\",\"graphs\":"
                  << graphs << ",\"flows\":" << flows
                  << ",\"hs_bad\":" << bad
                  << ",\"flow_trials\":" << flow_trials
                  << ",\"circuits_seen_before_repairs\":"
                  << circuits_seen
                  << ",\"legal_switches_tested_before_repairs\":"
                  << legal_tested
                  << ",\"maximum_legal_switches_before_repair\":"
                  << maximum_tested << "}" << std::endl;
        return 0;
      }
    }
  }
  std::cout << "{\"status\":\"HS_SAMPLE_DONE\",\"graphs\":" << graphs
            << ",\"flows\":" << flows << ",\"hs_bad\":" << bad
            << ",\"flow_trials\":" << flow_trials
            << ",\"circuits_seen_before_repairs\":" << circuits_seen
            << ",\"legal_switches_tested_before_repairs\":"
            << legal_tested
            << ",\"maximum_legal_switches_before_repair\":"
            << maximum_tested << "}" << std::endl;
  return 0;
}

int husek_samal_radius_two_sample_search(
    const std::string& path, const int samples,
    const std::uint64_t seed) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open " + path);
  std::mt19937_64 random(seed);
  std::string record;
  std::uint64_t graphs = 0, flows = 0, flow_trials = 0, bad = 0;
  std::uint64_t first_traps = 0, first_neighbors = 0;
  std::uint64_t second_neighbors = 0;
  while (std::getline(input, record)) {
    if (record.empty()) continue;
    Graph graph = decode_graph6(record);
    const std::vector<Key> circuits = all_circuits(graph);
    ++graphs;
    for (int sample = 0; sample < samples; ++sample) {
      const std::vector<int> flow =
          random_flow(graph, random, &flow_trials);
      ++flows;
      if (husek_samal_good(graph, flow)) continue;
      ++bad;
      FlowSwitch first, second;
      std::uint64_t local_first = 0, local_second = 0;
      const bool repair = husek_samal_radius_two_repair(
          graph, circuits, flow, &first, &second,
          &local_first, &local_second);
      first_neighbors += local_first;
      second_neighbors += local_second;
      first_traps += second.value != 0;
      if (!repair) {
        const auto initial_profile = husek_samal_profile(graph, flow);
        std::cout << "{\"status\":\"HS_RADIUS2_COUNTERMODEL\","
                  << "\"graph6\":\"" << record
                  << "\",\"vertices\":" << graph.vertices
                  << ",\"sample\":" << sample
                  << ",\"circuits\":" << circuits.size()
                  << ",\"initial_profile\":[";
        for (int index = 0; index < 7; ++index) {
          if (index) std::cout << ',';
          std::cout << initial_profile[index];
        }
        std::cout << "],\"first_neighbors_exhausted\":"
                  << local_first
                  << ",\"second_neighbors_exhausted\":"
                  << local_second << ",\"flow\":[";
        for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
          if (edge) std::cout << ',';
          std::cout << flow[edge];
        }
        std::cout << "]}" << std::endl;
        return 3;
      }
    }
  }
  std::cout << "{\"status\":\"HS_RADIUS2_SAMPLE_DONE\",\"graphs\":"
            << graphs << ",\"flows\":" << flows
            << ",\"hs_bad\":" << bad
            << ",\"radius1_traps\":" << first_traps
            << ",\"flow_trials\":" << flow_trials
            << ",\"first_neighbors_tested\":" << first_neighbors
            << ",\"second_neighbors_tested\":" << second_neighbors
            << "}" << std::endl;
  return 0;
}

int pair_deletion_search(const std::string& path, const int samples,
                         const std::uint64_t seed,
                         const bool require_lift) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open " + path);
  std::mt19937_64 random(seed);
  std::string record;
  std::uint64_t graphs = 0, flows = 0, flow_trials = 0, bad = 0;
  while (std::getline(input, record)) {
    if (record.empty()) continue;
    Graph graph = decode_graph6(record);
    PackingOracle oracle(graph);
    const std::vector<Key> circuits =
        require_lift ? all_circuits(graph) : std::vector<Key>{};
    ++graphs;
    for (int sample = 0; sample < samples; ++sample) {
      const std::vector<int> flow =
          random_flow(graph, random, &flow_trials);
      ++flows;
      if (good(flow, oracle)) continue;
      ++bad;
      const auto value_classes = classes(flow);
      bool pair_deletion = false;
      bool pair_lift = false;
      int pair_value = 0, first_edge = -1, second_edge = -1;
      for (int value = 1;
           value <= 7 && !(require_lift ? pair_lift : pair_deletion);
           ++value) {
        std::vector<int> members;
        for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
          if (flow[edge] == value) members.push_back(edge);
        }
        for (int left = 0;
             left < static_cast<int>(members.size()) &&
             !(require_lift ? pair_lift : pair_deletion);
             ++left) {
          for (int right = 0; right < left; ++right) {
            Key reduced = value_classes[value - 1];
            erase(reduced, members[left]);
            erase(reduced, members[right]);
            if (oracle.packs(reduced)) {
              pair_deletion = true;
              pair_value = value;
              first_edge = members[right];
              second_edge = members[left];
              if (!require_lift) break;
              for (int t = 1; t <= 7 && !pair_lift; ++t) {
                if (t == value) continue;
                Key forbidden = value_classes[t - 1];
                forbidden.lo |= value_classes[(value ^ t) - 1].lo;
                forbidden.hi |= value_classes[(value ^ t) - 1].hi;
                Key remaining_same = value_classes[value - 1];
                erase(remaining_same, first_edge);
                erase(remaining_same, second_edge);
                forbidden.lo |= remaining_same.lo;
                forbidden.hi |= remaining_same.hi;
                for (const Key circuit : circuits) {
                  if (!selected(circuit, first_edge) ||
                      !selected(circuit, second_edge)) {
                    continue;
                  }
                  if ((circuit.lo & forbidden.lo) ||
                      (circuit.hi & forbidden.hi)) {
                    continue;
                  }
                  pair_lift = true;
                  break;
                }
              }
            }
          }
        }
      }
      if (!(require_lift ? pair_lift : pair_deletion)) {
        std::cout << "{\"status\":\""
                  << (require_lift ? "PAIR_LIFT_COUNTERMODEL"
                                   : "PAIR_DELETION_COUNTERMODEL")
                  << "\","
                  << "\"graph6\":\"" << record << "\",\"vertices\":"
                  << graph.vertices << ",\"flow\":[";
        for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
          if (edge) std::cout << ',';
          std::cout << flow[edge];
        }
        std::cout << "]}" << std::endl;
        return 3;
      }
      (void)pair_value;
      (void)first_edge;
      (void)second_edge;
    }
  }
  std::cout << "{\"status\":\""
            << (require_lift ? "PAIR_LIFT_PASS" : "PAIR_DELETION_PASS")
            << "\",\"graphs\":" << graphs
            << ",\"flows\":" << flows << ",\"bad\":" << bad
            << ",\"flow_trials\":" << flow_trials << "}" << std::endl;
  return 0;
}

int main(int argc, char** argv) {
  if (argc == 6 && std::string(argv[1]) == "--hill") {
    try {
      return hill_search(argv[2], std::stoi(argv[3]),
                         std::stoull(argv[4]), std::stoi(argv[5]));
    } catch (const std::exception& error) {
      std::cerr << "ERROR: " << error.what() << std::endl;
      return 1;
    }
  }
  if (argc == 6 && std::string(argv[1]) == "--apx-hill") {
    try {
      return apx_hill_search(argv[2], std::stoi(argv[3]),
                             std::stoull(argv[4]), std::stoi(argv[5]));
    } catch (const std::exception& error) {
      std::cerr << "ERROR: " << error.what() << std::endl;
      return 1;
    }
  }
  if (argc != 5) {
    std::cerr << "usage: search graph6-file flows-per-graph seed stop-after\n";
    return 2;
  }
  try {
    if (std::string(argv[1]) == "--apx-neighborhood") {
      return apx_neighborhood_search(
          argv[2], std::stoi(argv[3]), std::stoull(argv[4]));
    }
    if (std::string(argv[1]) == "--circuit-audit" ||
        std::string(argv[1]) == "--circuit-first") {
      return circuit_repair_audit(
          argv[2], std::string(argv[1]) == "--circuit-first");
    }
    if (std::string(argv[1]) == "--hs-circuit-audit" ||
        std::string(argv[1]) == "--hs-circuit-first") {
      return husek_samal_circuit_audit(
          argv[2], std::string(argv[1]) == "--hs-circuit-first");
    }
    if (std::string(argv[1]) == "--hs-rewire40" ||
        std::string(argv[1]) == "--hs-rewire40-girth5") {
      return husek_samal_rewire_search(
          std::stoi(argv[2]), std::stoull(argv[3]),
          std::string(argv[1]) == "--hs-rewire40-girth5");
    }
    if (std::string(argv[1]) == "--rewire40" ||
        std::string(argv[1]) == "--rewire40-cyclic4") {
      return rewire_search(std::stoi(argv[2]), std::stoull(argv[3]),
                           std::stoi(argv[4]),
                           std::string(argv[1]) == "--rewire40");
    }
    if (std::string(argv[1]) == "--apx-rewire40" ||
        std::string(argv[1]) == "--apx-rewire40-cyclic4") {
      return apx_rewire_search(
          std::stoi(argv[2]), std::stoull(argv[3]),
          std::stoi(argv[4]),
          std::string(argv[1]) == "--apx-rewire40");
    }
    if (std::string(argv[1]) == "--perturb40") {
      return perturb_search(std::stoi(argv[2]), std::stoull(argv[3]),
                            std::stoi(argv[4]));
    }
    if (std::string(argv[1]) == "--core" ||
        std::string(argv[1]) == "--core-bad") {
      return core_search(argv[2], std::stoi(argv[3]),
                         std::stoull(argv[4]),
                         std::string(argv[1]) == "--core-bad");
    }
    if (std::string(argv[1]) == "--apx-sample") {
      return apx_sample_search(
          argv[2], std::stoi(argv[3]), std::stoull(argv[4]));
    }
    if (std::string(argv[1]) == "--hs-sample") {
      return husek_samal_sample_search(
          argv[2], std::stoi(argv[3]), std::stoull(argv[4]), 0);
    }
    if (std::string(argv[1]) == "--hs-radius2-sample") {
      return husek_samal_radius_two_sample_search(
          argv[2], std::stoi(argv[3]), std::stoull(argv[4]));
    }
    if (std::string(argv[1]) == "--pair-bad") {
      return pair_deletion_search(
          argv[2], std::stoi(argv[3]), std::stoull(argv[4]), false);
    }
    if (std::string(argv[1]) == "--pair-lift-bad") {
      return pair_deletion_search(
          argv[2], std::stoi(argv[3]), std::stoull(argv[4]), true);
    }
    const std::string path = argv[1];
    const int samples = std::stoi(argv[2]);
    std::mt19937_64 random(std::stoull(argv[3]));
    const int stop_after = std::stoi(argv[4]);
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open " + path);
    std::string record;
    std::uint64_t graphs = 0, flow_trials = 0, flows = 0, bad = 0;
    while (std::getline(input, record)) {
      if (record.empty()) continue;
      Graph graph = decode_graph6(record);
      PackingOracle oracle(graph);
      const std::vector<Key> circuits = all_circuits(graph);
      ++graphs;
      for (int sample = 0; sample < samples; ++sample) {
        const std::vector<int> flow =
            random_flow(graph, random, &flow_trials);
        ++flows;
        if (good(flow, oracle)) continue;
        ++bad;
        int connected_t = 0;
        Key connected_circuit;
        std::uint64_t connected_tested = 0;
        const bool connected_repair = connected_circuit_repair(
            graph, circuits, flow, oracle, &connected_t,
            &connected_circuit, &connected_tested);
        int repair_pairs = 0;
        int first_t = 0, first_b = 0;
        std::vector<int> first_switch;
        for (int t = 1; t <= 7; ++t) {
          for (int b = 1; b <= 7; ++b) {
            std::vector<int> support;
            if (binary_cycle_repair(graph, flow, t, b, &support)) {
              std::vector<int> switched = flow;
              std::vector<int> degree(graph.vertices, 0);
              for (const int edge : support) {
                if (flow[edge] == t) {
                  throw std::runtime_error(
                      "SAT repair contains a forbidden-value edge");
                }
                degree[graph.edges[edge].first] ^= 1;
                degree[graph.edges[edge].second] ^= 1;
                switched[edge] ^= t;
              }
              if (std::find(degree.begin(), degree.end(), 1) != degree.end()) {
                throw std::runtime_error("SAT repair support is not even");
              }
              if (!oracle.packs(classes(switched)[b - 1])) {
                throw std::runtime_error(
                    "SAT repair does not pack the requested value");
              }
              ++repair_pairs;
              if (!first_t) {
                first_t = t;
                first_b = b;
                first_switch = std::move(support);
              }
            }
          }
        }
        std::cout << "{\"status\":\"BAD\",\"graph6\":\"" << record
                  << "\",\"vertices\":" << graph.vertices
                  << ",\"sample\":" << sample
                  << ",\"circuits\":" << circuits.size()
                  << ",\"connected_repair\":"
                  << (connected_repair ? "true" : "false")
                  << ",\"connected_t\":" << connected_t
                  << ",\"connected_tested\":" << connected_tested
                  << ",\"connected_circuit\":[";
        bool comma = false;
        for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
          if (!selected(connected_circuit, edge)) continue;
          if (comma) std::cout << ',';
          comma = true;
          std::cout << edge;
        }
        std::cout << "]"
                  << ",\"binary_repair_pairs\":" << repair_pairs
                  << ",\"first_t\":" << first_t
                  << ",\"first_b\":" << first_b << ",\"first_switch\":[";
        for (int index = 0; index < static_cast<int>(first_switch.size());
             ++index) {
          if (index) std::cout << ',';
          std::cout << first_switch[index];
        }
        std::cout << "],\"flow\":[";
        for (int edge = 0; edge < static_cast<int>(flow.size()); ++edge) {
          if (edge) std::cout << ',';
          std::cout << flow[edge];
        }
        std::cout << "]}" << std::endl;
        if (!connected_repair || !repair_pairs ||
            (stop_after > 0 && bad >= stop_after)) {
          std::cerr << "graphs=" << graphs << " flows=" << flows
                    << " bad=" << bad << " trials=" << flow_trials
                    << std::endl;
          return (connected_repair && repair_pairs) ? 0 : 3;
        }
      }
    }
    std::cout << "{\"status\":\"DONE\",\"graphs\":" << graphs
              << ",\"flows\":" << flows << ",\"bad\":" << bad
              << ",\"flow_trials\":" << flow_trials << "}" << std::endl;
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << std::endl;
    return 1;
  }
}
