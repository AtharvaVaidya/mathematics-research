// Exact whole-state checker for monotone parity descent in a Jaeger
// vertex-star fibre.  States are ordered partitions into three cographic
// bases; adjacency is every reciprocal two-tree symmetric exchange.
// Objectives: one fixed coordinate, the minimum over the three coordinate
// planes, or the minimum exact component defect over all seven Fano planes.

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using Mask = std::uint64_t;

struct DSU {
  std::vector<int> parent;
  std::vector<int> size;

  explicit DSU(int n) : parent(n), size(n, 1) {
    std::iota(parent.begin(), parent.end(), 0);
  }

  int find(int x) {
    while (parent[x] != x) {
      parent[x] = parent[parent[x]];
      x = parent[x];
    }
    return x;
  }

  void unite(int x, int y) {
    x = find(x);
    y = find(y);
    if (x == y) return;
    if (size[x] < size[y]) std::swap(x, y);
    parent[y] = x;
    size[x] += size[y];
  }
};

struct Graph {
  int n = 0;
  std::vector<std::pair<int, int>> edges;
};

Graph parse_graph6(std::string record) {
  const std::string header = ">>graph6<<";
  if (record.rfind(header, 0) == 0) record.erase(0, header.size());
  if (record.empty() || record[0] == '~') {
    throw std::runtime_error("only short graph6 records are supported");
  }
  Graph graph;
  graph.n = static_cast<unsigned char>(record[0]) - 63;
  std::vector<int> bits;
  for (std::size_t i = 1; i < record.size(); ++i) {
    const int value = static_cast<unsigned char>(record[i]) - 63;
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }
  int cursor = 0;
  for (int v = 1; v < graph.n; ++v) {
    for (int u = 0; u < v; ++u) {
      if (bits.at(cursor)) graph.edges.emplace_back(u, v);
      ++cursor;
    }
  }
  return graph;
}

bool connected_after_deletions(const Graph& graph, int deleted_a, int deleted_b) {
  std::vector<std::vector<int>> adjacency(graph.n);
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    if (edge == deleted_a || edge == deleted_b) continue;
    auto [u, v] = graph.edges[edge];
    adjacency[u].push_back(v);
    adjacency[v].push_back(u);
  }
  std::vector<int> stack = {0};
  std::vector<char> seen(graph.n, false);
  seen[0] = true;
  while (!stack.empty()) {
    int vertex = stack.back();
    stack.pop_back();
    for (int other : adjacency[vertex]) {
      if (!seen[other]) {
        seen[other] = true;
        stack.push_back(other);
      }
    }
  }
  return std::all_of(seen.begin(), seen.end(), [](char value) { return value; });
}

bool is_three_edge_connected(const Graph& graph) {
  if (!connected_after_deletions(graph, -1, -1)) return false;
  const int m = graph.edges.size();
  for (int first = 0; first < m; ++first) {
    if (!connected_after_deletions(graph, first, -1)) return false;
    for (int second = first + 1; second < m; ++second) {
      if (!connected_after_deletions(graph, first, second)) return false;
    }
  }
  return true;
}

bool is_tree_on_deleted_root(const Graph& graph, int root,
                             const std::vector<int>& internal_edges,
                             Mask omitted) {
  std::vector<int> parent(graph.n);
  std::iota(parent.begin(), parent.end(), 0);
  auto find = [&](int x) {
    while (parent[x] != x) {
      parent[x] = parent[parent[x]];
      x = parent[x];
    }
    return x;
  };
  int count = 0;
  for (int local = 0; local < static_cast<int>(internal_edges.size()); ++local) {
    if ((omitted >> local) & 1ULL) continue;
    auto [u, v] = graph.edges[internal_edges[local]];
    int a = find(u);
    int b = find(v);
    if (a == b) return false;
    parent[a] = b;
    ++count;
  }
  if (count != graph.n - 2) return false;
  int representative = -1;
  for (int vertex = 0; vertex < graph.n; ++vertex) {
    if (vertex == root) continue;
    int current = find(vertex);
    if (representative < 0) representative = current;
    if (current != representative) return false;
  }
  return true;
}

Mask odd_core(const Graph& graph, Mask tree) {
  std::vector<std::vector<std::pair<int, int>>> adjacency(graph.n);
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    if (!((tree >> edge) & 1ULL)) continue;
    auto [u, v] = graph.edges[edge];
    adjacency[u].emplace_back(v, edge);
    adjacency[v].emplace_back(u, edge);
  }
  std::vector<int> parent(graph.n, -1);
  std::vector<int> parent_edge(graph.n, -1);
  std::vector<int> order = {0};
  parent[0] = 0;
  for (std::size_t cursor = 0; cursor < order.size(); ++cursor) {
    int vertex = order[cursor];
    for (auto [other, edge] : adjacency[vertex]) {
      if (parent[other] >= 0) continue;
      parent[other] = vertex;
      parent_edge[other] = edge;
      order.push_back(other);
    }
  }
  if (static_cast<int>(order.size()) != graph.n) {
    throw std::runtime_error("odd_core received a disconnected tree");
  }
  std::vector<int> subtree_size(graph.n, 1);
  Mask answer = 0;
  for (int cursor = graph.n - 1; cursor >= 1; --cursor) {
    int vertex = order[cursor];
    if (subtree_size[vertex] & 1) answer |= 1ULL << parent_edge[vertex];
    subtree_size[parent[vertex]] += subtree_size[vertex];
  }
  return answer;
}

std::array<int, 7> fano_parity_profile(
    const Graph& graph, const std::vector<std::array<int, 3>>& incident,
    const std::array<Mask, 3>& cores) {
  const int m = graph.edges.size();
  std::array<unsigned char, 64> flow{};
  for (int edge = 0; edge < m; ++edge) {
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      if (!((cores[coordinate] >> edge) & 1ULL)) {
        flow[edge] |= 1 << coordinate;
      }
    }
    if (flow[edge] == 0) {
      throw std::runtime_error("the derived Fano flow has a zero edge");
    }
  }
  std::array<unsigned char, 64> normal{};
  for (int vertex = 0; vertex < graph.n; ++vertex) {
    for (int candidate = 1; candidate < 8; ++candidate) {
      bool annihilates = true;
      for (int edge : incident[vertex]) {
        annihilates &=
            (__builtin_popcount(candidate & flow[edge]) & 1) == 0;
      }
      if (annihilates) {
        if (normal[vertex] != 0) {
          throw std::runtime_error("incident flow plane has two normals");
        }
        normal[vertex] = candidate;
      }
    }
    if (normal[vertex] == 0) {
      throw std::runtime_error("incident flow plane has no normal");
    }
  }

  std::array<int, 7> profile{};
  for (int functional = 1; functional < 8; ++functional) {
    std::array<int, 64> parent{};
    std::iota(parent.begin(), parent.begin() + graph.n, 0);
    auto find = [&](int x) {
      while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
      }
      return x;
    };
    auto unite = [&](int x, int y) {
      x = find(x);
      y = find(y);
      if (x != y) parent[x] = y;
    };
    std::array<unsigned char, 64> zero_degree{};
    for (int edge = 0; edge < m; ++edge) {
      if (__builtin_popcount(functional & flow[edge]) & 1) continue;
      auto [u, v] = graph.edges[edge];
      ++zero_degree[u];
      ++zero_degree[v];
      unite(u, v);
    }
    const int transverse_point = 1 << __builtin_ctz(functional);
    std::array<unsigned char, 64> parity{};
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      if (zero_degree[vertex] != 1 && zero_degree[vertex] != 3) {
        throw std::runtime_error("zero-plane degree is not one or three");
      }
      if (zero_degree[vertex] == 1) {
        const int leaf_bit = __builtin_popcount(
                                 (normal[vertex] ^ functional) &
                                 transverse_point) &
                             1;
        parity[find(vertex)] ^= leaf_bit;
      }
    }
    int score = 0;
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      if (find(vertex) == vertex && parity[vertex]) ++score;
    }
    profile[functional - 1] = score;
  }
  return profile;
}

enum class Objective { FixedCoordinate, ThreeCoordinates, SevenPlanes };

const char* objective_name(Objective objective) {
  if (objective == Objective::FixedCoordinate) return "fixed-coordinate-2";
  if (objective == Objective::ThreeCoordinates) return "min-three-coordinates";
  return "min-seven-fano-planes";
}

int objective_score(const std::array<int, 7>& profile, Objective objective) {
  if (objective == Objective::FixedCoordinate) return profile[3];
  if (objective == Objective::ThreeCoordinates) {
    return std::min({profile[0], profile[1], profile[3]});
  }
  return *std::min_element(profile.begin(), profile.end());
}

struct State {
  Mask omitted0;
  Mask omitted1;
  int score;
};

struct Result {
  bool applicable = false;
  bool failure = false;
  int states = 0;
  int max_score = 0;
  int bad_level = -1;
  int bad_component_size = 0;
  Mask witness0 = 0;
  Mask witness1 = 0;
  std::array<int, 7> witness_profile{};
};

Result analyze(const Graph& graph, int root, Objective objective) {
  Result result;
  std::vector<std::array<int, 3>> incidence(graph.n);
  std::vector<int> incidence_degree(graph.n, 0);
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    auto [u, v] = graph.edges[edge];
    incidence[u][incidence_degree[u]++] = edge;
    incidence[v][incidence_degree[v]++] = edge;
  }
  if (!std::all_of(incidence_degree.begin(), incidence_degree.end(),
                   [](int degree) { return degree == 3; })) {
    return result;
  }
  std::vector<int> spokes;
  std::vector<int> internal_edges;
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    auto [u, v] = graph.edges[edge];
    if (u == root || v == root) {
      spokes.push_back(edge);
    } else {
      internal_edges.push_back(edge);
    }
  }
  if (spokes.size() != 3 || internal_edges.size() > 21) return result;
  result.applicable = true;
  const int p = internal_edges.size();
  const int class_size = graph.n / 2 - 1;
  const Mask all_internal = (1ULL << p) - 1;
  std::vector<char> is_basis(1ULL << p, false);
  std::vector<Mask> bases;
  for (Mask mask = 0; mask <= all_internal; ++mask) {
    if (__builtin_popcountll(mask) != class_size) continue;
    if (is_tree_on_deleted_root(graph, root, internal_edges, mask)) {
      is_basis[mask] = true;
      bases.push_back(mask);
    }
  }

  Mask internal_to_full[21];
  for (int local = 0; local < p; ++local) {
    internal_to_full[local] = 1ULL << internal_edges[local];
  }
  auto full_tree = [&](Mask omitted, int coordinate) {
    Mask tree = 1ULL << spokes[coordinate];
    Mask present = all_internal ^ omitted;
    while (present) {
      int local = __builtin_ctzll(present);
      present &= present - 1;
      tree |= internal_to_full[local];
    }
    return tree;
  };

  std::vector<State> states;
  for (Mask omitted0 : bases) {
    const Mask remaining = all_internal ^ omitted0;
    Mask omitted1 = remaining;
    for (;;) {
      if (__builtin_popcountll(omitted1) == class_size && is_basis[omitted1]) {
        const Mask omitted2 = remaining ^ omitted1;
        if (is_basis[omitted2]) {
          std::array<Mask, 3> cores = {
              odd_core(graph, full_tree(omitted0, 0)),
              odd_core(graph, full_tree(omitted1, 1)),
              odd_core(graph, full_tree(omitted2, 2)),
          };
          const auto profile = fano_parity_profile(graph, incidence, cores);
          int score = objective_score(profile, objective);
          states.push_back({omitted0, omitted1, score});
          result.max_score = std::max(result.max_score, score);
        }
      }
      if (omitted1 == 0) break;
      omitted1 = (omitted1 - 1) & remaining;
    }
  }
  result.states = states.size();

  auto key_of = [&](Mask omitted0, Mask omitted1) {
    return omitted0 | (omitted1 << p);
  };
  std::unordered_map<Mask, int> index;
  index.reserve(states.size() * 2);
  for (int state = 0; state < static_cast<int>(states.size()); ++state) {
    index.emplace(key_of(states[state].omitted0, states[state].omitted1), state);
  }

  DSU dsu(states.size());
  std::vector<char> has_lower(states.size(), false);
  for (int state = 0; state < static_cast<int>(states.size()); ++state) {
    std::array<Mask, 3> omitted = {
        states[state].omitted0,
        states[state].omitted1,
        all_internal ^ states[state].omitted0 ^ states[state].omitted1,
    };
    for (int first = 0; first < 3; ++first) {
      for (int second = first + 1; second < 3; ++second) {
        Mask first_edges = omitted[first];
        while (first_edges) {
          int first_edge = __builtin_ctzll(first_edges);
          first_edges &= first_edges - 1;
          Mask second_edges = omitted[second];
          while (second_edges) {
            int second_edge = __builtin_ctzll(second_edges);
            second_edges &= second_edges - 1;
            auto changed = omitted;
            changed[first] ^= (1ULL << first_edge) | (1ULL << second_edge);
            changed[second] ^= (1ULL << first_edge) | (1ULL << second_edge);
            auto found = index.find(key_of(changed[0], changed[1]));
            if (found == index.end()) continue;
            int other = found->second;
            if (states[state].score == states[other].score) {
              dsu.unite(state, other);
            } else if (states[state].score > states[other].score) {
              has_lower[state] = true;
            } else {
              has_lower[other] = true;
            }
          }
        }
      }
    }
  }

  std::vector<char> component_has_lower(states.size(), false);
  for (int state = 0; state < static_cast<int>(states.size()); ++state) {
    if (has_lower[state]) component_has_lower[dsu.find(state)] = true;
  }
  for (int state = 0; state < static_cast<int>(states.size()); ++state) {
    if (states[state].score == 0) continue;
    int component = dsu.find(state);
    if (!component_has_lower[component]) {
      result.failure = true;
      result.bad_level = states[state].score;
      result.bad_component_size = dsu.size[component];
      result.witness0 = states[state].omitted0;
      result.witness1 = states[state].omitted1;
      const Mask omitted2 =
          all_internal ^ result.witness0 ^ result.witness1;
      const std::array<Mask, 3> cores = {
          odd_core(graph, full_tree(result.witness0, 0)),
          odd_core(graph, full_tree(result.witness1, 1)),
          odd_core(graph, full_tree(omitted2, 2)),
      };
      result.witness_profile = fano_parity_profile(graph, incidence, cores);
      return result;
    }
  }
  return result;
}

int main(int argc, char** argv) {
  bool all_roots = false;
  int fixed_root = 0;
  Objective objective = Objective::FixedCoordinate;
  for (int i = 1; i < argc; ++i) {
    std::string argument = argv[i];
    if (argument == "--all-roots") {
      all_roots = true;
    } else if (argument == "--root" && i + 1 < argc) {
      fixed_root = std::atoi(argv[++i]);
    } else if (argument == "--objective" && i + 1 < argc) {
      const std::string value = argv[++i];
      if (value == "fixed") {
        objective = Objective::FixedCoordinate;
      } else if (value == "three") {
        objective = Objective::ThreeCoordinates;
      } else if (value == "seven") {
        objective = Objective::SevenPlanes;
      } else {
        std::cerr << "unknown objective: " << value << "\n";
        return 2;
      }
    } else {
      std::cerr << "usage: search_jaeger_star_parity_descent "
                   "[--all-roots | --root V] "
                   "[--objective fixed|three|seven] < graph6-stream\n";
      return 2;
    }
  }
  std::string record;
  int graph_index = 0;
  int analyzed = 0;
  while (std::cin >> record) {
    Graph graph = parse_graph6(record);
    if (!is_three_edge_connected(graph)) {
      ++graph_index;
      continue;
    }
    int first_root = all_roots ? 0 : fixed_root;
    int last_root = all_roots ? graph.n : fixed_root + 1;
    for (int root = first_root; root < last_root; ++root) {
      Result result = analyze(graph, root, objective);
      if (!result.applicable) continue;
      ++analyzed;
      std::cout << "{\"graph_index\":" << graph_index
                << ",\"graph6\":\"" << record << "\",\"root\":" << root
                << ",\"objective\":\"" << objective_name(objective) << "\""
                << ",\"states\":" << result.states
                << ",\"max_score\":" << result.max_score
                << ",\"failure\":" << (result.failure ? "true" : "false");
      if (result.failure) {
        std::cout << ",\"bad_level\":" << result.bad_level
                  << ",\"bad_component_size\":" << result.bad_component_size
                  << ",\"omitted0\":" << result.witness0
                  << ",\"omitted1\":" << result.witness1
                  << ",\"fano_profile\":[";
        for (int functional = 0; functional < 7; ++functional) {
          if (functional) std::cout << ",";
          std::cout << result.witness_profile[functional];
        }
        std::cout << "]";
      }
      std::cout << "}\n";
      if (result.failure) return 1;
    }
    ++graph_index;
  }
  std::cerr << "analyzed " << analyzed << " rooted instances\n";
  return 0;
}
