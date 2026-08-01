// Exact search for a vertex-star fibre whose every packing has even
// six-point/one-hole solubility parity modulo coordinate translations.

#ifndef SIX_POINT_PARITY_MAX_N
#define SIX_POINT_PARITY_MAX_N 16
#endif
#ifndef SIX_POINT_PARITY_MAX_M
#define SIX_POINT_PARITY_MAX_M 24
#endif
#define JAEGER_AUDIT_MAX_N SIX_POINT_PARITY_MAX_N
#define JAEGER_AUDIT_MAX_M SIX_POINT_PARITY_MAX_M
#define main frozen_two_tree_census_unused_main
#include "census_jaeger_two_tree_exchange_through14.cpp"
#undef main

#include <optional>
#include <sstream>

namespace {

using DirectFlow = std::array<unsigned char, MAX_M>;

int direct_flow_value(const DirectFlow& flow, int edge) {
  return static_cast<int>(flow[edge]);
}

DirectFlow direct_flow_from_supports(
    const std::array<uint32_t, 3>& supports, int edge_count) {
  DirectFlow flow{};
  for (int edge = 0; edge < edge_count; ++edge) {
    for (int bit = 0; bit < 3; ++bit) {
      flow[edge] |=
          static_cast<unsigned char>(((supports[bit] >> edge) & 1U) << bit);
    }
  }
  return flow;
}

DirectFlow canonical_direct_flow(
    const DirectFlow& flow, int edge_count) {
  DirectFlow best{};
  best.fill(8);
  for (const auto& table : gl3_tables()) {
    DirectFlow transformed{};
    for (int edge = 0; edge < edge_count; ++edge) {
      transformed[edge] = table[direct_flow_value(flow, edge)];
    }
    if (std::lexicographical_compare(
            transformed.begin(), transformed.begin() + edge_count,
            best.begin(), best.begin() + edge_count)) {
      best = transformed;
    }
  }
  return best;
}

std::string direct_flow_key(
    const DirectFlow& flow, int edge_count) {
  return std::string(
      reinterpret_cast<const char*>(flow.data()),
      static_cast<std::size_t>(edge_count));
}

int parity_dot(int first, int second) {
  return __builtin_popcount(first & second) & 1;
}

struct AffineRow {
  uint64_t mask = 0;
  int rhs = 0;
};

struct AffineResult {
  bool soluble = false;
  int rank = 0;
};

AffineResult eliminate_affine(
    int variables, const std::vector<AffineRow>& input) {
  std::array<uint64_t, 64> basis{};
  std::array<int, 64> rhs{};
  int rank = 0;
  for (AffineRow row : input) {
    while (row.mask) {
      const int pivot = 63 - __builtin_clzll(row.mask);
      if (!basis[pivot]) {
        basis[pivot] = row.mask;
        rhs[pivot] = row.rhs;
        ++rank;
        break;
      }
      row.mask ^= basis[pivot];
      row.rhs ^= rhs[pivot];
    }
    if (!row.mask && row.rhs) return {false, rank};
  }
  assert(rank <= variables);
  return {true, rank};
}

std::vector<std::array<int, 4>> pair_orbit_representatives() {
  std::set<std::array<int, 4>> representatives;
  for (int r0 = 0; r0 < 8; ++r0) {
    for (int r1 = r0 + 1; r1 < 8; ++r1) {
      for (int m0 = 0; m0 < 8; ++m0) {
        if (m0 == r0 || m0 == r1) continue;
        for (int m1 = m0 + 1; m1 < 8; ++m1) {
          if (m1 == r0 || m1 == r1) continue;
          std::array<int, 4> best = {8, 8, 8, 8};
          for (int shift = 0; shift < 8; ++shift) {
            std::array<int, 2> omitted = {r0 ^ shift, r1 ^ shift};
            std::array<int, 2> missing = {m0 ^ shift, m1 ^ shift};
            std::sort(omitted.begin(), omitted.end());
            std::sort(missing.begin(), missing.end());
            best = std::min(
                best,
                std::array<int, 4>{
                    omitted[0], omitted[1], missing[0], missing[1]});
          }
          representatives.insert(best);
        }
      }
    }
  }
  assert(representatives.size() == 63);
  return {representatives.begin(), representatives.end()};
}

const std::vector<std::array<int, 4>> PAIR_ORBITS =
    pair_orbit_representatives();

std::array<int, 8> local_allowed(
    int plane_mask, int omitted_mask, int missing_mask) {
  std::array<int, 8> allowed{};
  for (int potential = 0; potential < 8; ++potential) {
    int triangle_mask = 0;
    for (int value = 1; value < 8; ++value) {
      if (plane_mask & (1 << value)) {
        triangle_mask |= 1 << (potential ^ value);
      }
    }
    if (triangle_mask & omitted_mask) continue;
    if ((triangle_mask & missing_mask) == missing_mask) continue;
    allowed[potential] = 1;
  }
  return allowed;
}

AffineResult six_hole_system(
    const Graph& graph, const DirectFlow& flow,
    const std::array<int, 4>& pair_choice) {
  const int omitted_mask =
      (1 << pair_choice[0]) | (1 << pair_choice[1]);
  const int missing_mask =
      (1 << pair_choice[2]) | (1 << pair_choice[3]);
  std::vector<AffineRow> rows;
  for (int vertex = 0; vertex < graph.n; ++vertex) {
    int plane_mask = 1;
    for (const int edge : graph.incidence[vertex]) {
      plane_mask |= 1 << direct_flow_value(flow, edge);
    }
    const auto allowed =
        local_allowed(plane_mask, omitted_mask, missing_mask);
    int base = -1;
    for (int point = 0; point < 8; ++point) {
      if (allowed[point]) {
        base = point;
        break;
      }
    }
    assert(base >= 0);
    for (int functional = 1; functional < 8; ++functional) {
      bool annihilates = true;
      for (int point = 0; point < 8; ++point) {
        if (allowed[point] &&
            parity_dot(functional, point ^ base)) {
          annihilates = false;
        }
      }
      if (!annihilates) continue;
      uint64_t mask = 0;
      for (int bit = 0; bit < 3; ++bit) {
        if (functional & (1 << bit)) {
          mask |= uint64_t{1} << (3 * vertex + bit);
        }
      }
      rows.push_back({mask, parity_dot(functional, base)});
    }
  }
  for (int edge = 0; edge < graph.m(); ++edge) {
    const int left = graph.edges[edge][0];
    const int right = graph.edges[edge][1];
    const int left_other = *std::find_if(
        graph.incidence[left].begin(), graph.incidence[left].end(),
        [&](int candidate) { return candidate != edge; });
    const int right_other = *std::find_if(
        graph.incidence[right].begin(), graph.incidence[right].end(),
        [&](int candidate) { return candidate != edge; });
    const int constant =
        direct_flow_value(flow, left_other) ^
        direct_flow_value(flow, right_other);
    const int value = direct_flow_value(flow, edge);
    for (int functional = 1; functional < 8; ++functional) {
      if (parity_dot(functional, value)) continue;
      uint64_t mask = 0;
      for (const int vertex : {left, right}) {
        for (int bit = 0; bit < 3; ++bit) {
          if (functional & (1 << bit)) {
            mask ^= uint64_t{1} << (3 * vertex + bit);
          }
        }
      }
      rows.push_back({mask, parity_dot(functional, constant)});
    }
  }
  return eliminate_affine(3 * graph.n, rows);
}

struct ParityProfile {
  int soluble = 0;
  int unique = 0;
  int parallel_soluble = 0;
  int skew_soluble = 0;
  int coordinate_parallel_soluble = 0;
};

ParityProfile parity_profile(const Graph& graph, const DirectFlow& flow) {
  ParityProfile profile;
  for (const auto& pair_choice : PAIR_ORBITS) {
    const auto result = six_hole_system(graph, flow, pair_choice);
    if (!result.soluble) continue;
    ++profile.soluble;
    if ((pair_choice[0] ^ pair_choice[1]) ==
        (pair_choice[2] ^ pair_choice[3])) {
      ++profile.parallel_soluble;
      int direction_plane_mask = 0;
      for (const int point : pair_choice) {
        direction_plane_mask |=
            1 << (point ^ pair_choice[0]);
      }
      // The three coordinate-kernel planes are the 2-planes on which
      // one of the three ordered packing coordinates vanishes.
      if (direction_plane_mask == 0x0f ||
          direction_plane_mask == 0x33 ||
          direction_plane_mask == 0x55) {
        ++profile.coordinate_parallel_soluble;
      }
    } else {
      ++profile.skew_soluble;
    }
    if (result.rank == 3 * graph.n) ++profile.unique;
  }
  return profile;
}

std::unordered_map<uint32_t, std::vector<uint32_t>>
completion_tree_map(const Graph& graph) {
  std::unordered_map<uint32_t, std::vector<uint32_t>> answer;
  const uint32_t universe = uint32_t{1} << graph.m();
  for (uint32_t mask = 0; mask < universe; ++mask) {
    if (!is_tree(graph, mask)) continue;
    answer[fundamental_completion(graph, mask)].push_back(mask);
  }
  return answer;
}

std::optional<std::array<uint32_t, 3>> packing_for_supports(
    const Graph& graph,
    const std::unordered_map<uint32_t, std::vector<uint32_t>>& by_completion,
    const std::array<uint32_t, 3>& supports, int root) {
  for (const uint32_t support : supports) {
    if (!by_completion.count(support)) return std::nullopt;
  }
  const uint32_t all_edges = (uint32_t{1} << graph.m()) - 1;
  uint32_t root_edges = 0;
  for (const int edge : graph.incidence[root]) {
    root_edges |= uint32_t{1} << edge;
  }
  const uint32_t other_edges = all_edges ^ root_edges;
  std::unordered_set<uint32_t> third_trees(
      by_completion.at(supports[2]).begin(),
      by_completion.at(supports[2]).end());
  for (const uint32_t first : by_completion.at(supports[0])) {
    for (const uint32_t second : by_completion.at(supports[1])) {
      if (first & second & root_edges) continue;
      if (other_edges & ~(first | second)) continue;
      const uint32_t third =
          (root_edges & ~(first | second)) |
          (other_edges & (first ^ second));
      if (third_trees.count(third)) {
        return std::array<uint32_t, 3>{first, second, third};
      }
    }
  }
  return std::nullopt;
}

struct Attainment {
  uint64_t transformed_flow = 0;
  std::array<uint32_t, 3> supports{};
  std::array<uint32_t, 3> trees{};
};

std::optional<Attainment> attained_at_root(
    const Graph& graph, uint64_t orbit_flow,
    const std::unordered_map<uint32_t, std::vector<uint32_t>>& by_completion,
    int root) {
  const auto tables = gl3_tables();
  for (const auto& table : tables) {
    const uint64_t transformed =
        transform_flow(orbit_flow, graph.m(), table);
    std::array<uint32_t, 3> supports{};
    for (int edge = 0; edge < graph.m(); ++edge) {
      const int value = flow_value(transformed, edge);
      for (int bit = 0; bit < 3; ++bit) {
        if (value & (1 << bit)) {
          supports[bit] |= uint32_t{1} << edge;
        }
      }
    }
    const auto packing =
        packing_for_supports(graph, by_completion, supports, root);
    if (packing) {
      return Attainment{transformed, supports, *packing};
    }
  }
  return std::nullopt;
}

void print_mask_array(const std::array<uint32_t, 3>& values) {
  std::cout << '[' << values[0] << ',' << values[1] << ',' << values[2]
            << ']';
}

void print_flow_word(const Graph& graph, uint64_t flow) {
  std::cout << '[';
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (edge) std::cout << ',';
    std::cout << flow_value(flow, edge);
  }
  std::cout << ']';
}

struct DirectAttainment {
  DirectFlow flow{};
  std::array<uint32_t, 3> supports{};
  std::array<uint32_t, 3> trees{};
};

void print_direct_flow_word(
    const Graph& graph, const DirectFlow& flow) {
  std::cout << '[';
  for (int edge = 0; edge < graph.m(); ++edge) {
    if (edge) std::cout << ',';
    std::cout << direct_flow_value(flow, edge);
  }
  std::cout << ']';
}

struct RootSearch {
  bool feasible = false;
  bool has_odd = false;
  uint64_t packings_examined = 0;
  std::optional<DirectAttainment> first_even;
  std::optional<DirectAttainment> first_odd;
  int first_even_soluble = -1;
  int first_odd_soluble = -1;
};

RootSearch search_root_packings(
    const Graph& graph, int root,
    const std::vector<uint32_t>& trees,
    const std::unordered_set<uint32_t>& tree_set,
    const std::unordered_map<uint32_t, uint32_t>& completion_of_tree,
    std::unordered_map<std::string, ParityProfile>& profile_cache) {
  RootSearch result;
  uint32_t root_edges = 0;
  for (const int edge : graph.incidence[root]) {
    root_edges |= uint32_t{1} << edge;
  }
  const uint32_t all_edges = (uint32_t{1} << graph.m()) - 1;
  const uint32_t other_edges = all_edges ^ root_edges;
  const int anchor_edge = *std::min_element(
      graph.incidence[root].begin(), graph.incidence[root].end());
  std::array<int, 2> remaining_root_edges{};
  int remaining_index = 0;
  for (const int edge : graph.incidence[root]) {
    if (edge != anchor_edge) {
      remaining_root_edges[remaining_index++] = edge;
    }
  }
  std::sort(remaining_root_edges.begin(), remaining_root_edges.end());
  const uint32_t anchor_bit = uint32_t{1} << anchor_edge;
  const uint32_t second_root_bit =
      uint32_t{1} << remaining_root_edges[0];
  const uint32_t third_root_bit =
      uint32_t{1} << remaining_root_edges[1];
  const int omission_size = graph.n / 2 - 1;

  for (const uint32_t first : trees) {
    if ((first & root_edges) != anchor_bit) continue;
    const uint32_t first_omissions = other_edges & ~first;
    assert(__builtin_popcount(first_omissions) == omission_size);
    const uint32_t available = other_edges & ~first_omissions;
    std::array<int, MAX_M> available_edges{};
    int available_count = 0;
    for (int edge = 0; edge < graph.m(); ++edge) {
      if (available & (uint32_t{1} << edge)) {
        available_edges[available_count++] = edge;
      }
    }
    assert(available_count == 2 * omission_size);

    // Choose the non-root edges omitted by the second tree.  The remaining
    // available edges are omitted by the third tree.  Thus the three
    // omission sets partition E minus the root star, exactly encoding
    // multiplicity two there; the sorted root edges encode multiplicity one.
    uint32_t combination = (uint32_t{1} << omission_size) - 1;
    const uint32_t combination_limit =
        uint32_t{1} << available_count;
    while (combination < combination_limit) {
      uint32_t second_omissions = 0;
      for (int index = 0; index < available_count; ++index) {
        if (combination & (uint32_t{1} << index)) {
          second_omissions |=
              uint32_t{1} << available_edges[index];
        }
      }
      const uint32_t third_omissions = available ^ second_omissions;
      const uint32_t second =
          (other_edges & ~second_omissions) | second_root_bit;
      const uint32_t third =
          (other_edges & ~third_omissions) | third_root_bit;
      if (tree_set.count(second) && tree_set.count(third)) {
        result.feasible = true;
        ++result.packings_examined;
        const std::array<uint32_t, 3> packing = {first, second, third};
        const std::array<uint32_t, 3> supports = {
            completion_of_tree.at(first),
            completion_of_tree.at(second),
            completion_of_tree.at(third),
        };
        const DirectFlow flow =
            direct_flow_from_supports(supports, graph.m());
        for (int edge = 0; edge < graph.m(); ++edge) {
          assert(direct_flow_value(flow, edge) != 0);
        }
        const DirectFlow canonical =
            canonical_direct_flow(flow, graph.m());
        const std::string key = direct_flow_key(canonical, graph.m());
        auto found = profile_cache.find(key);
        if (found == profile_cache.end()) {
          found = profile_cache.emplace(
              key, parity_profile(graph, canonical)).first;
        }
        const ParityProfile profile = found->second;
        const DirectAttainment witness{flow, supports, packing};
        if (profile.soluble & 1) {
          result.has_odd = true;
          result.first_odd = witness;
          result.first_odd_soluble = profile.soluble;
          return result;
        }
        if (!result.first_even) {
          result.first_even = witness;
          result.first_even_soluble = profile.soluble;
        }
      }

      // Gosper's hack: next omission_size-subset of available_count bits.
      const uint32_t low = combination & -combination;
      const uint32_t ripple = combination + low;
      if (!ripple) break;
      combination =
          ripple | (((combination ^ ripple) >> 2) / low);
    }
  }
  return result;
}

}  // namespace

#ifndef SIX_POINT_PARITY_NO_MAIN
int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr
        << "usage: search_six_point_star_perpacking_parity GRAPH6\n";
    return 64;
  }
  const std::string graph6 = argv[1];
  const Graph graph = parse_graph6(graph6);
  if (!is_cubic_connected(graph) || !is_bridgeless(graph)) return 3;

  const auto by_completion = completion_tree_map(graph);
  std::vector<uint32_t> trees;
  std::unordered_set<uint32_t> tree_set;
  std::unordered_map<uint32_t, uint32_t> completion_of_tree;
  for (const auto& [completion, completion_trees] : by_completion) {
    for (const uint32_t tree : completion_trees) {
      trees.push_back(tree);
      tree_set.insert(tree);
      completion_of_tree.emplace(tree, completion);
    }
  }
  std::sort(trees.begin(), trees.end());
  std::unordered_map<std::string, ParityProfile> profile_cache;
  std::vector<RootSearch> root_results;
  for (int root = 0; root < graph.n; ++root) {
    root_results.push_back(search_root_packings(
        graph, root, trees, tree_set, completion_of_tree, profile_cache));
  }

  int counter_root = -1;
  for (int root = 0; root < graph.n; ++root) {
    if (root_results[root].feasible && !root_results[root].has_odd) {
      counter_root = root;
      break;
    }
  }

  std::cout << "{\"schema\":\"six-point-star-perpacking-parity-cpp-v2\","
            << "\"status\":\""
            << (counter_root >= 0 ? "COUNTERMODEL" : "GRAPH_PASS")
            << "\",\"graph6\":\"" << graph6 << "\""
            << ",\"vertices\":" << graph.n
            << ",\"edges\":" << graph.m()
            << ",\"spanning_trees\":" << trees.size()
            << ",\"evaluated_flow_gl_orbits\":"
            << profile_cache.size()
            << ",\"completion_supports\":" << by_completion.size()
            << ",\"roots\":[";
  for (int root = 0; root < graph.n; ++root) {
    if (root) std::cout << ',';
    const RootSearch& row = root_results[root];
    std::cout << "{\"root\":" << root
              << ",\"feasible\":" << (row.feasible ? "true" : "false")
              << ",\"has_odd_packing\":"
              << (row.has_odd ? "true" : "false")
              << ",\"packings_examined\":" << row.packings_examined;
    if (row.first_odd) {
      std::cout << ",\"odd_witness\":{\"soluble_orbits\":"
                << row.first_odd_soluble << ",\"tree_masks\":";
      print_mask_array(row.first_odd->trees);
      std::cout << ",\"completion_masks\":";
      print_mask_array(row.first_odd->supports);
      std::cout << ",\"flow\":";
      print_direct_flow_word(graph, row.first_odd->flow);
      std::cout << '}';
    }
    if (row.first_even) {
      std::cout << ",\"even_control\":{\"soluble_orbits\":"
                << row.first_even_soluble << ",\"tree_masks\":";
      print_mask_array(row.first_even->trees);
      std::cout << ",\"completion_masks\":";
      print_mask_array(row.first_even->supports);
      std::cout << ",\"flow\":";
      print_direct_flow_word(graph, row.first_even->flow);
      std::cout << '}';
    }
    std::cout << '}';
  }
  std::cout << ']';
  if (counter_root >= 0) {
    std::cout << ",\"counterexample_root\":" << counter_root;
  }
  std::cout
      << ",\"scope\":\"Per-packing parity selector only; not a "
         "fixed-fibre or FiveCDC obstruction.\"}\n";
  return counter_root >= 0 ? 2 : 0;
}
#endif
