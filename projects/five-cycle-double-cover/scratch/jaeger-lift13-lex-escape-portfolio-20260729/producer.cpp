// Randomized high-girth stress test for the Jaeger vertex-star fibre.
//
// This program is deliberately separate from the exhaustive <= 16 vertex
// enumerator.  It supports extended graph6 records and dynamically sized
// edge sets, constructs a star packing by randomized cographic-base
// partition search, and then samples reciprocal-exchange states.  At every
// sampled state it exhaustively checks all incident reciprocal exchanges.
//
// The output is evidence only: the state sample is not exhaustive.  Each
// reported local-trap count is nevertheless exact for the sampled states.

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <queue>
#include <random>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

struct DSU {
  std::vector<int> parent;
  std::vector<int> size;

  explicit DSU(int n) : parent(n), size(n, 1) {
    std::iota(parent.begin(), parent.end(), 0);
  }

  int find(int value) {
    while (parent[value] != value) {
      parent[value] = parent[parent[value]];
      value = parent[value];
    }
    return value;
  }

  void unite(int first, int second) {
    first = find(first);
    second = find(second);
    if (first == second) return;
    if (size[first] < size[second]) std::swap(first, second);
    parent[second] = first;
    size[first] += size[second];
  }
};

struct Graph {
  int n = 0;
  std::vector<std::pair<int, int>> edges;
  std::vector<std::vector<int>> incidence;
};

Graph parse_graph6(std::string record) {
  const std::string header = ">>graph6<<";
  if (record.rfind(header, 0) == 0) record.erase(0, header.size());
  if (record.empty()) throw std::runtime_error("empty graph6 record");
  std::vector<int> values;
  values.reserve(record.size());
  for (char character : record) {
    const int value = static_cast<unsigned char>(character) - 63;
    if (value < 0 || value >= 64) {
      throw std::runtime_error("invalid graph6 byte");
    }
    values.push_back(value);
  }
  Graph graph;
  std::size_t data_start = 0;
  if (values[0] < 63) {
    graph.n = values[0];
    data_start = 1;
  } else if (values.size() >= 4 && values[1] < 63) {
    graph.n = (values[1] << 12) | (values[2] << 6) | values[3];
    data_start = 4;
  } else {
    throw std::runtime_error("36-bit graph6 orders are unsupported");
  }
  std::vector<unsigned char> bits;
  for (std::size_t index = data_start; index < values.size(); ++index) {
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((values[index] >> shift) & 1);
    }
  }
  const std::size_t required =
      static_cast<std::size_t>(graph.n) * (graph.n - 1) / 2;
  if (bits.size() < required) throw std::runtime_error("short graph6 body");
  std::size_t cursor = 0;
  for (int right = 1; right < graph.n; ++right) {
    for (int left = 0; left < right; ++left) {
      if (bits[cursor]) graph.edges.emplace_back(left, right);
      ++cursor;
    }
  }
  graph.incidence.assign(graph.n, {});
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    const auto [left, right] = graph.edges[edge];
    graph.incidence[left].push_back(edge);
    graph.incidence[right].push_back(edge);
  }
  return graph;
}

bool is_cubic_connected(const Graph& graph) {
  if (!std::all_of(graph.incidence.begin(), graph.incidence.end(),
                   [](const auto& row) { return row.size() == 3; })) {
    return false;
  }
  std::vector<char> seen(graph.n, false);
  std::vector<int> stack{0};
  seen[0] = true;
  while (!stack.empty()) {
    const int vertex = stack.back();
    stack.pop_back();
    for (int edge : graph.incidence[vertex]) {
      const auto [left, right] = graph.edges[edge];
      const int other = left ^ right ^ vertex;
      if (!seen[other]) {
        seen[other] = true;
        stack.push_back(other);
      }
    }
  }
  return std::all_of(seen.begin(), seen.end(),
                     [](char value) { return value; });
}

int graph_girth(const Graph& graph) {
  int answer = graph.n + 1;
  for (int source = 0; source < graph.n; ++source) {
    std::vector<int> distance(graph.n, -1);
    std::vector<int> parent(graph.n, -1);
    std::queue<int> queue;
    distance[source] = 0;
    queue.push(source);
    while (!queue.empty()) {
      const int vertex = queue.front();
      queue.pop();
      for (int edge : graph.incidence[vertex]) {
        const auto [left, right] = graph.edges[edge];
        const int other = left ^ right ^ vertex;
        if (distance[other] < 0) {
          distance[other] = distance[vertex] + 1;
          parent[other] = vertex;
          queue.push(other);
        } else if (parent[vertex] != other) {
          answer =
              std::min(answer, distance[vertex] + distance[other] + 1);
        }
      }
    }
  }
  return answer <= graph.n ? answer : -1;
}

struct RootModel {
  int root = 0;
  std::vector<int> internal;
  std::array<int, 3> spoke{};
  std::vector<unsigned char> omitted_class;
};

int tree_component_excess(const Graph& graph, const RootModel& model,
                          const std::vector<unsigned char>& state,
                          int coordinate) {
  DSU dsu(graph.n);
  dsu.unite(graph.edges[model.spoke[coordinate]].first,
            graph.edges[model.spoke[coordinate]].second);
  for (int local = 0; local < static_cast<int>(model.internal.size());
       ++local) {
    if (state[local] == coordinate) continue;
    const auto [left, right] = graph.edges[model.internal[local]];
    dsu.unite(left, right);
  }
  int components = 0;
  for (int vertex = 0; vertex < graph.n; ++vertex) {
    components += dsu.find(vertex) == vertex;
  }
  return components - 1;
}

int packing_defect(const Graph& graph, const RootModel& model,
                   const std::vector<unsigned char>& state) {
  int answer = 0;
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    answer += tree_component_excess(graph, model, state, coordinate);
  }
  return answer;
}

RootModel find_root_model(const Graph& graph, int root,
                          std::mt19937_64& random) {
  RootModel model;
  model.root = root;
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    const auto [left, right] = graph.edges[edge];
    if (left != root && right != root) {
      model.internal.push_back(edge);
    }
  }
  if (graph.incidence[root].size() != 3) {
    throw std::runtime_error("root degree is not three");
  }
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    model.spoke[coordinate] = graph.incidence[root][coordinate];
  }
  if (model.internal.size() % 3 != 0) {
    throw std::runtime_error("internal edge count is not divisible by three");
  }
  const int class_size = model.internal.size() / 3;
  std::vector<unsigned char> initial;
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    initial.insert(initial.end(), class_size, coordinate);
  }

  int best_global = graph.n * 3;
  std::vector<unsigned char> best_state;
  constexpr int restarts = 200;
  constexpr int steps_per_restart = 200000;
  for (int restart = 0; restart < restarts; ++restart) {
    std::shuffle(initial.begin(), initial.end(), random);
    std::vector<unsigned char> state = initial;
    int defect = packing_defect(graph, model, state);
    double temperature = 2.0;
    for (int step = 0; step < steps_per_restart && defect; ++step) {
      int first = random() % state.size();
      int second = random() % state.size();
      if (state[first] == state[second]) continue;
      std::swap(state[first], state[second]);
      const int changed = packing_defect(graph, model, state);
      const bool accept =
          changed <= defect ||
          std::generate_canonical<double, 53>(random) <
              std::exp((defect - changed) / temperature);
      if (accept) {
        defect = changed;
      } else {
        std::swap(state[first], state[second]);
      }
      temperature *= 0.99995;
      temperature = std::max(temperature, 0.03);
      if (defect < best_global) {
        best_global = defect;
        best_state = state;
      }
    }
    if (defect == 0) {
      model.omitted_class = std::move(state);
      return model;
    }
  }
  throw std::runtime_error("packing search failed; best defect " +
                           std::to_string(best_global));
}

std::array<std::vector<char>, 3> trees_of(
    const Graph& graph, const RootModel& model,
    const std::vector<unsigned char>& state) {
  std::array<std::vector<char>, 3> trees;
  for (auto& tree : trees) tree.assign(graph.edges.size(), false);
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    trees[coordinate][model.spoke[coordinate]] = true;
  }
  for (int local = 0; local < static_cast<int>(model.internal.size());
       ++local) {
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      trees[coordinate][model.internal[local]] =
          state[local] != coordinate;
    }
  }
  return trees;
}

bool is_tree(const Graph& graph, const std::vector<char>& tree) {
  if (std::count(tree.begin(), tree.end(), true) != graph.n - 1) {
    return false;
  }
  DSU dsu(graph.n);
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    if (!tree[edge]) continue;
    const auto [left, right] = graph.edges[edge];
    if (dsu.find(left) == dsu.find(right)) return false;
    dsu.unite(left, right);
  }
  return true;
}

std::vector<char> odd_kernel(const Graph& graph,
                             const std::vector<char>& tree) {
  std::vector<std::vector<std::pair<int, int>>> adjacency(graph.n);
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    if (!tree[edge]) continue;
    const auto [left, right] = graph.edges[edge];
    adjacency[left].emplace_back(right, edge);
    adjacency[right].emplace_back(left, edge);
  }
  std::vector<int> parent(graph.n, -1);
  std::vector<int> parent_edge(graph.n, -1);
  std::vector<int> order{0};
  parent[0] = 0;
  for (std::size_t cursor = 0; cursor < order.size(); ++cursor) {
    const int vertex = order[cursor];
    for (const auto [other, edge] : adjacency[vertex]) {
      if (parent[other] >= 0) continue;
      parent[other] = vertex;
      parent_edge[other] = edge;
      order.push_back(other);
    }
  }
  if (static_cast<int>(order.size()) != graph.n) {
    throw std::runtime_error("odd_kernel received a disconnected tree");
  }
  std::vector<int> subtree_size(graph.n, 1);
  std::vector<char> answer(graph.edges.size(), false);
  for (int cursor = graph.n - 1; cursor >= 1; --cursor) {
    const int vertex = order[cursor];
    if (subtree_size[vertex] & 1) answer[parent_edge[vertex]] = true;
    subtree_size[parent[vertex]] += subtree_size[vertex];
  }
  return answer;
}

using BitVector = std::vector<std::uint64_t>;

int highest_bit(const BitVector& vector) {
  for (int word = static_cast<int>(vector.size()) - 1; word >= 0; --word) {
    if (!vector[word]) continue;
    return word * 64 + 63 - __builtin_clzll(vector[word]);
  }
  return -1;
}

void xor_into(BitVector& target, const BitVector& source) {
  for (std::size_t word = 0; word < target.size(); ++word) {
    target[word] ^= source[word];
  }
}

bool in_binary_span(BitVector target, const std::vector<BitVector>& columns,
                    int dimension) {
  std::vector<BitVector> basis(
      dimension, BitVector((dimension + 63) / 64, 0));
  for (BitVector column : columns) {
    while (true) {
      const int pivot = highest_bit(column);
      if (pivot < 0) break;
      if (highest_bit(basis[pivot]) < 0) {
        basis[pivot] = std::move(column);
        break;
      }
      xor_into(column, basis[pivot]);
    }
  }
  while (true) {
    const int pivot = highest_bit(target);
    if (pivot < 0) return true;
    if (highest_bit(basis[pivot]) < 0) return false;
    xor_into(target, basis[pivot]);
  }
}

struct Evaluation {
  std::array<int, 7> profile{};
  int kernel_sum = 0;
  int parallel_successful_flags = 0;
};

Evaluation evaluate(const Graph& graph,
                    const std::array<std::vector<char>, 3>& trees,
                    bool calculate_parallel_flags) {
  std::array<std::vector<char>, 3> kernels;
  Evaluation result;
  for (int coordinate = 0; coordinate < 3; ++coordinate) {
    kernels[coordinate] = odd_kernel(graph, trees[coordinate]);
    result.kernel_sum +=
        std::count(kernels[coordinate].begin(), kernels[coordinate].end(),
                   true);
  }
  std::vector<unsigned char> flow(graph.edges.size(), 0);
  for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      if (!kernels[coordinate][edge]) flow[edge] |= 1 << coordinate;
    }
    if (!flow[edge]) throw std::runtime_error("zero derived flow edge");
  }
  std::vector<unsigned char> normal(graph.n, 0);
  for (int vertex = 0; vertex < graph.n; ++vertex) {
    for (int candidate = 1; candidate < 8; ++candidate) {
      bool annihilates = true;
      for (int edge : graph.incidence[vertex]) {
        annihilates &=
            (__builtin_popcount(candidate & flow[edge]) & 1) == 0;
      }
      if (!annihilates) continue;
      if (normal[vertex]) {
        throw std::runtime_error("two incident-plane normals");
      }
      normal[vertex] = candidate;
    }
    if (!normal[vertex]) {
      throw std::runtime_error("no incident-plane normal");
    }
  }

  for (int functional = 1; functional < 8; ++functional) {
    DSU zero_components(graph.n);
    std::vector<int> zero_degree(graph.n, 0);
    for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
      if (__builtin_popcount(functional & flow[edge]) & 1) continue;
      const auto [left, right] = graph.edges[edge];
      ++zero_degree[left];
      ++zero_degree[right];
      zero_components.unite(left, right);
    }
    const int transverse = 1 << __builtin_ctz(functional);
    std::vector<unsigned char> parity(graph.n, 0);
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      if (zero_degree[vertex] != 1 && zero_degree[vertex] != 3) {
        throw std::runtime_error("zero-plane degree is not one or three");
      }
      if (zero_degree[vertex] == 1) {
        parity[zero_components.find(vertex)] ^=
            __builtin_popcount((normal[vertex] ^ functional) & transverse) &
            1;
      }
    }
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      if (zero_components.find(vertex) == vertex && parity[vertex]) {
        ++result.profile[functional - 1];
      }
    }
    if (!calculate_parallel_flags) continue;

    std::vector<int> component_index(graph.n, -1);
    int component_count = 0;
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      const int root = zero_components.find(vertex);
      if (component_index[root] < 0) {
        component_index[root] = component_count++;
      }
    }
    const int words = (component_count + 63) / 64;
    BitVector beta(words, 0);
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      if (zero_components.find(vertex) == vertex && parity[vertex]) {
        const int index = component_index[vertex];
        beta[index / 64] ^= std::uint64_t{1} << (index % 64);
      }
    }

    DSU outside_components(graph.n);
    for (int edge = 0; edge < static_cast<int>(graph.edges.size()); ++edge) {
      if (!(__builtin_popcount(functional & flow[edge]) & 1)) continue;
      const auto [left, right] = graph.edges[edge];
      outside_components.unite(left, right);
    }
    std::vector<unsigned char> inside_value(graph.n, 0);
    for (int vertex = 0; vertex < graph.n; ++vertex) {
      if (zero_degree[vertex] != 1) continue;
      for (int edge : graph.incidence[vertex]) {
        if (!(__builtin_popcount(functional & flow[edge]) & 1)) {
          inside_value[vertex] = flow[edge];
          break;
        }
      }
      if (!inside_value[vertex]) {
        throw std::runtime_error("leaf has no inside value");
      }
    }

    for (int direction = 1; direction < 8; ++direction) {
      if (__builtin_popcount(functional & direction) & 1) continue;
      std::vector<BitVector> gamma_by_root(
          graph.n, BitVector(words, 0));
      for (int vertex = 0; vertex < graph.n; ++vertex) {
        if (zero_degree[vertex] != 1 ||
            inside_value[vertex] == direction) {
          continue;
        }
        const int zero_root = zero_components.find(vertex);
        const int outside_root = outside_components.find(vertex);
        const int index = component_index[zero_root];
        gamma_by_root[outside_root][index / 64] ^=
            std::uint64_t{1} << (index % 64);
      }
      std::vector<BitVector> columns;
      for (int vertex = 0; vertex < graph.n; ++vertex) {
        if (outside_components.find(vertex) == vertex &&
            highest_bit(gamma_by_root[vertex]) >= 0) {
          columns.push_back(gamma_by_root[vertex]);
        }
      }
      result.parallel_successful_flags +=
          in_binary_span(beta, columns, component_count);
    }
  }
  return result;
}

struct Potential {
  int d_min = 0;
  int kernel_sum = 0;
};

Potential potential(const Evaluation& evaluation) {
  return {*std::min_element(evaluation.profile.begin(),
                            evaluation.profile.end()),
          evaluation.kernel_sum};
}

bool operator<(const Potential& first, const Potential& second) {
  return first.d_min < second.d_min ||
         (first.d_min == second.d_min &&
          first.kernel_sum < second.kernel_sum);
}

bool operator==(const Potential& first, const Potential& second) {
  return first.d_min == second.d_min &&
         first.kernel_sum == second.kernel_sum;
}

struct Neighbour {
  int first = 0;
  int second = 0;
  Potential potential;
  int parallel_successful_flags = -1;
};

std::vector<Neighbour> evaluate_neighbours(
    const Graph& graph, const RootModel& model,
    std::vector<unsigned char>& state,
    bool calculate_parallel_flags = false) {
  std::vector<Neighbour> answer;
  for (int first_coordinate = 0; first_coordinate < 3;
       ++first_coordinate) {
    for (int second_coordinate = first_coordinate + 1;
         second_coordinate < 3; ++second_coordinate) {
      for (int first = 0; first < static_cast<int>(state.size()); ++first) {
        if (state[first] != first_coordinate) continue;
        for (int second = 0; second < static_cast<int>(state.size());
             ++second) {
          if (state[second] != second_coordinate) continue;
          std::swap(state[first], state[second]);
          if (tree_component_excess(graph, model, state,
                                    first_coordinate) == 0 &&
              tree_component_excess(graph, model, state,
                                    second_coordinate) == 0) {
            const auto trees = trees_of(graph, model, state);
            const Evaluation evaluation =
                evaluate(graph, trees, calculate_parallel_flags);
            answer.push_back(
                {first, second, potential(evaluation),
                 calculate_parallel_flags
                     ? evaluation.parallel_successful_flags
                     : -1});
          }
          std::swap(state[first], state[second]);
        }
      }
    }
  }
  return answer;
}

std::string state_key(const std::vector<unsigned char>& state) {
  return std::string(state.begin(), state.end());
}

std::array<std::uint64_t, 3> omitted_masks(
    const std::vector<unsigned char>& state) {
  if (state.size() > 64) {
    throw std::runtime_error("state is too large for 64-bit masks");
  }
  std::array<std::uint64_t, 3> answer{};
  for (int local = 0; local < static_cast<int>(state.size()); ++local) {
    answer[state[local]] |= std::uint64_t{1} << local;
  }
  return answer;
}

void print_profile(const std::array<int, 7>& profile) {
  std::cout << "[";
  for (int index = 0; index < 7; ++index) {
    if (index) std::cout << ",";
    std::cout << profile[index];
  }
  std::cout << "]";
}

void print_state_labels(const std::vector<unsigned char>& state) {
  std::cout << "[";
  for (int local = 0; local < static_cast<int>(state.size()); ++local) {
    if (local) std::cout << ",";
    std::cout << static_cast<int>(state[local]);
  }
  std::cout << "]";
}

std::string json_escape(const std::string& text) {
  std::string answer;
  for (char character : text) {
    if (character == '\\' || character == '"') answer.push_back('\\');
    answer.push_back(character);
  }
  return answer;
}

int main(int argc, char** argv) {
  const int steps = argc >= 2 ? std::atoi(argv[1]) : 20;
  const std::uint64_t seed =
      argc >= 3 ? std::strtoull(argv[2], nullptr, 10) : 1;
  const int requested_root = argc >= 4 ? std::atoi(argv[3]) : 0;
  const bool trap_directed = argc >= 5 &&
                             std::string(argv[4]) == "trap-directed";
  std::mt19937_64 random(seed);
  std::string record;
  int graph_index = 0;
  while (std::cin >> record) {
    const Graph graph = parse_graph6(record);
    if (!is_cubic_connected(graph)) {
      throw std::runtime_error("input is not connected cubic");
    }
    if (requested_root < 0 || requested_root >= graph.n) {
      throw std::runtime_error("root outside graph");
    }
    RootModel model = find_root_model(graph, requested_root, random);
    std::vector<unsigned char> state = model.omitted_class;
    const auto initial_trees = trees_of(graph, model, state);
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      if (!is_tree(graph, initial_trees[coordinate])) {
        throw std::runtime_error("constructed packing is not three trees");
      }
    }

    std::unordered_set<std::string> distinct;
    std::unordered_set<std::string> audited_local_minima;
    std::uint64_t positive_states = 0;
    std::uint64_t all_span_fail_states = 0;
    std::uint64_t all_span_fail_local_traps = 0;
    std::uint64_t exact_neighbours_checked = 0;
    int maximum_d_min = 0;
    int minimum_lower_degree = -1;
    int exact_augmented_traps = 0;
    int shake_remaining = 0;
    for (int step = 0; step < steps; ++step) {
      distinct.insert(state_key(state));
      const Evaluation current =
          evaluate(graph, trees_of(graph, model, state), true);
      const Potential current_potential = potential(current);
      maximum_d_min = std::max(maximum_d_min, current_potential.d_min);
      positive_states += current_potential.d_min > 0;
      all_span_fail_states +=
          current_potential.d_min > 0 &&
          current.parallel_successful_flags == 0;

      std::vector<Neighbour> neighbours =
          evaluate_neighbours(graph, model, state);
      exact_neighbours_checked += neighbours.size();
      int lower = 0;
      for (const Neighbour& neighbour : neighbours) {
        lower += neighbour.potential < current_potential;
      }
      if (current_potential.d_min > 0 &&
          current.parallel_successful_flags == 0) {
        if (minimum_lower_degree < 0 || lower < minimum_lower_degree) {
          minimum_lower_degree = lower;
        }
        if (lower == 0) {
          ++all_span_fail_local_traps;
          const std::string key = state_key(state);
          if (!trap_directed || audited_local_minima.insert(key).second) {
            std::vector<Neighbour> exact_neighbours =
                evaluate_neighbours(graph, model, state, true);
            const int success_neighbours = std::count_if(
                exact_neighbours.begin(), exact_neighbours.end(),
                [](const Neighbour& neighbour) {
                  return neighbour.parallel_successful_flags > 0;
                });
            const bool augmented = success_neighbours == 0;
            exact_augmented_traps += augmented;
            std::cout
                << "{\"status\":\""
                << (augmented ? "EXACT_AUGMENTED_TRAP"
                              : "EXACT_OLD_TRAP")
                << "\",\"graph_index\":" << graph_index << ','
                << "\"graph6\":\"" << json_escape(record) << "\","
                << "\"order\":" << graph.n << ','
                << "\"girth\":" << graph_girth(graph) << ','
                << "\"root\":" << requested_root << ','
                << "\"step\":" << step << ','
                << "\"d_min\":" << current_potential.d_min << ','
                << "\"kernel_sum\":" << current_potential.kernel_sum
                << ",\"profile\":";
            print_profile(current.profile);
            std::cout
                << ",\"parallel_successful_flags\":0,"
                << "\"legal_neighbours\":" << neighbours.size()
                << ",\"lower_neighbours\":0,"
                << "\"parallel_success_neighbours\":"
                << success_neighbours << ",\"state_labels\":";
            print_state_labels(state);
            if (state.size() <= 64) {
              const auto masks = omitted_masks(state);
              std::cout << ",\"omitted_masks\":["
                        << masks[0] << "," << masks[1] << ","
                        << masks[2] << "]";
            }
            if (augmented) {
              std::cout << ",\"full_neighbourhood\":[";
              for (int index = 0;
                   index < static_cast<int>(exact_neighbours.size());
                   ++index) {
                if (index) std::cout << ",";
                const auto& neighbour = exact_neighbours[index];
                std::cout
                    << "{\"local_positions\":["
                    << neighbour.first << "," << neighbour.second
                    << "],\"coordinates\":["
                    << static_cast<int>(state[neighbour.first]) << ","
                    << static_cast<int>(state[neighbour.second])
                    << "],\"psi\":["
                    << neighbour.potential.d_min << ","
                    << neighbour.potential.kernel_sum
                    << "],\"parallel_successful_flags\":"
                    << neighbour.parallel_successful_flags << "}";
              }
              std::cout << "]";
            }
            std::cout << "}\n";
          }
        }
      }
      if (neighbours.empty()) {
        throw std::runtime_error("sampled packing has no exchange");
      }
      int selected = random() % neighbours.size();
      if (trap_directed && shake_remaining == 0 && lower > 0) {
        std::vector<int> choices;
        Potential lowest = current_potential;
        int best_flag_penalty = 2;
        for (int index = 0; index < static_cast<int>(neighbours.size());
             ++index) {
          if (!(neighbours[index].potential < current_potential)) {
            continue;
          }
          std::swap(state[neighbours[index].first],
                    state[neighbours[index].second]);
          const Evaluation candidate =
              evaluate(graph, trees_of(graph, model, state), true);
          std::swap(state[neighbours[index].first],
                    state[neighbours[index].second]);
          const int flag_penalty =
              candidate.parallel_successful_flags > 0;
          if (choices.empty() ||
              flag_penalty < best_flag_penalty ||
              (flag_penalty == best_flag_penalty &&
               neighbours[index].potential < lowest)) {
            best_flag_penalty = flag_penalty;
            lowest = neighbours[index].potential;
            choices.assign(1, index);
          } else if (flag_penalty == best_flag_penalty &&
                     neighbours[index].potential == lowest) {
            choices.push_back(index);
          }
        }
        selected = choices[random() % choices.size()];
      } else if (!trap_directed && (random() & 1ULL)) {
        Potential highest = neighbours[0].potential;
        std::vector<int> choices{0};
        for (int index = 1; index < static_cast<int>(neighbours.size());
             ++index) {
          if (highest < neighbours[index].potential) {
            highest = neighbours[index].potential;
            choices.assign(1, index);
          } else if (highest == neighbours[index].potential) {
            choices.push_back(index);
          }
        }
        selected = choices[random() % choices.size()];
      }
      std::swap(state[neighbours[selected].first],
                state[neighbours[selected].second]);
      if (trap_directed) {
        if (shake_remaining > 0) {
          --shake_remaining;
        } else if (lower == 0) {
          // Leave the current basin before resuming exact descent.
          shake_remaining = 7 + random() % 14;
        }
      }
    }
    std::cout << "{\"status\":\"ROOT_DONE\","
              << "\"graph_index\":" << graph_index << ','
              << "\"graph6\":\"" << json_escape(record) << "\","
              << "\"order\":" << graph.n << ','
              << "\"edges\":" << graph.edges.size() << ','
              << "\"girth\":" << graph_girth(graph) << ','
              << "\"root\":" << requested_root << ','
              << "\"seed\":" << seed << ','
              << "\"steps\":" << steps << ','
              << "\"distinct_states\":" << distinct.size() << ','
              << "\"positive_states\":" << positive_states << ','
              << "\"all_span_fail_states\":" << all_span_fail_states
              << ",\"all_span_fail_no_immediate_descent_states\":"
              << all_span_fail_local_traps
              << ",\"exact_neighbours_checked\":"
              << exact_neighbours_checked
              << ",\"maximum_d_min\":" << maximum_d_min
              << ",\"minimum_lower_degree_on_all_span_fail\":"
              << minimum_lower_degree
              << ",\"distinct_local_minima_audited\":"
              << audited_local_minima.size()
              << ",\"exact_augmented_traps\":"
              << exact_augmented_traps << "}\n";
    ++graph_index;
  }
}
