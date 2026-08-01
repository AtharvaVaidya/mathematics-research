// Exact boundary-CSP search for
//   two C5 five-poles + four sharp four-poles.
//
// Reuse the independently audited atom-relation reconstruction from the
// frontier-three search, but replace its macrograph and CSP layers by the
// six-atom versions below.

#define main frontier3_main_not_used
#include "search_d5_frontier3_boundary.cpp"
#undef main

static constexpr std::array<std::pair<int, int>, 15> PAIRS6 = {{
  {0,1},{0,2},{0,3},{0,4},{0,5},
  {1,2},{1,3},{1,4},{1,5},
  {2,3},{2,4},{2,5},
  {3,4},{3,5},{4,5}
}};

static bool macro6_connected_without(
    const std::array<int, 15> &multiplicity, int skipped_type) {
  std::array<char, 6> seen = {true,false,false,false,false,false};
  std::array<int, 6> stack = {0,0,0,0,0,0};
  int size = 1;
  while (size) {
    int current = stack[--size];
    for (int type = 0; type < 15; ++type) {
      int copies = multiplicity[type] - (type == skipped_type);
      if (copies <= 0) continue;
      auto [left, right] = PAIRS6[type];
      int other = left == current ? right : right == current ? left : -1;
      if (other >= 0 && !seen[other]) {
        seen[other] = true;
        stack[size++] = other;
      }
    }
  }
  return std::count(seen.begin(), seen.end(), true) == 6;
}

static bool macro6_bridgeless(const std::array<int, 15> &multiplicity) {
  if (!macro6_connected_without(multiplicity, -1)) return false;
  for (int type = 0; type < 15; ++type)
    if (multiplicity[type] &&
        !macro6_connected_without(multiplicity, type))
      return false;
  return true;
}

static std::vector<std::array<int, 15>> labelled_macro6_matrices() {
  const std::array<int, 6> target = {5,5,4,4,4,4};
  std::array<int, 6> degree = {0,0,0,0,0,0};
  std::array<int, 15> multiplicity = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
  };
  std::vector<std::array<int, 15>> answer;
  std::function<void(int)> enumerate = [&](int type) {
    if (type == 15) {
      if (degree == target && macro6_bridgeless(multiplicity))
        answer.push_back(multiplicity);
      return;
    }
    auto [left, right] = PAIRS6[type];
    int maximum = std::min(
        target[left] - degree[left], target[right] - degree[right]);
    for (int copies = 0; copies <= maximum; ++copies) {
      multiplicity[type] = copies;
      degree[left] += copies;
      degree[right] += copies;
      enumerate(type + 1);
      degree[left] -= copies;
      degree[right] -= copies;
    }
    multiplicity[type] = 0;
  };
  enumerate(0);
  return answer;
}

static std::vector<std::vector<int>> type6_preserving_orders(
    const std::array<char, 6> &types) {
  std::vector<std::vector<int>> answer;
  std::vector<int> order = {0,1,2,3,4,5};
  do {
    bool okay = true;
    for (int position = 0; position < 6; ++position)
      okay &= types[order[position]] == types[position];
    if (okay) answer.push_back(order);
  } while (std::next_permutation(order.begin(), order.end()));
  return answer;
}

static std::array<int, 15> canonical_macro6(
    const std::array<int, 15> &multiplicity,
    const std::array<char, 6> &types) {
  std::array<std::array<int, 6>, 6> matrix{};
  for (int type = 0; type < 15; ++type) {
    auto [left, right] = PAIRS6[type];
    matrix[left][right] = matrix[right][left] = multiplicity[type];
  }
  std::array<int, 15> best;
  best.fill(99);
  for (const auto &order : type6_preserving_orders(types)) {
    std::array<int, 15> transformed;
    for (int type = 0; type < 15; ++type) {
      auto [left, right] = PAIRS6[type];
      transformed[type] = matrix[order[left]][order[right]];
    }
    best = std::min(best, transformed);
  }
  return best;
}

static bool csp6_sat(
    int edge_count,
    const std::array<Constraint, 6> &constraints,
    std::vector<int> *witness) {
  std::vector<int> values(edge_count, -1);
  std::function<bool()> search = [&]() -> bool {
    int best_edge = -1;
    std::array<int, 10> best_labels{};
    int best_count = 11;
    for (int edge = 0; edge < edge_count; ++edge) {
      if (values[edge] >= 0) continue;
      std::array<int, 10> labels{};
      int count = 0;
      for (int label = 0; label < 10; ++label) {
        values[edge] = label;
        bool okay = true;
        for (const auto &constraint : constraints)
          if (!constraint_extendable(constraint, values)) {
            okay = false;
            break;
          }
        values[edge] = -1;
        if (okay) labels[count++] = label;
      }
      if (!count) return false;
      if (count < best_count) {
        best_edge = edge;
        best_labels = labels;
        best_count = count;
        if (count == 1) break;
      }
    }
    if (best_edge < 0) {
      for (const auto &constraint : constraints)
        if (!constraint_extendable(constraint, values)) return false;
      *witness = values;
      return true;
    }
    for (int index = 0; index < best_count; ++index) {
      values[best_edge] = best_labels[index];
      if (search()) return true;
    }
    values[best_edge] = -1;
    return false;
  };
  return search();
}

int main(int argc, char **argv) {
  std::string mode = argc > 1 ? argv[1] : "all";
  const std::array<std::string, 5> modes = {
    "AAAA","AAAB","AABB","ABBB","BBBB"
  };
  if (mode != "all" &&
      std::find(modes.begin(), modes.end(), mode) == modes.end()) {
    std::cerr << "mode must be all, AAAA, AAAB, AABB, ABBB, or BBBB\n";
    return 2;
  }

  const Relation F = make_relation(five_atom());
  const Relation A = make_relation(four_a());
  const Relation B = make_relation(four_b());
  if (F.rows.size() != 4620 || A.rows.size() != 580 ||
      B.rows.size() != 630 || F.stabilizer.size() != 10 ||
      A.stabilizer.size() != 8 || B.stabilizer.size() != 24 ||
      F.assignment_representatives.size() != 12 ||
      A.assignment_representatives.size() != 3 ||
      B.assignment_representatives.size() != 1)
    throw std::runtime_error("unexpected exact relation or stabilizer");

  const auto labelled = labelled_macro6_matrices();
  if (labelled.size() != 4222)
    throw std::runtime_error("unexpected labelled macro count");
  const std::array<int, 5> expected_macros = {143,410,643,410,143};

  uint64_t total_states = 0;
  uint64_t total_empty = 0;
  std::vector<std::string> row_json;
  for (int mode_index = 0; mode_index < 5; ++mode_index) {
    const std::string &current_mode = modes[mode_index];
    if (mode != "all" && mode != current_mode) continue;
    std::array<char, 6> types = {
      'F','F',current_mode[0],current_mode[1],
      current_mode[2],current_mode[3]
    };
    std::set<std::array<int, 15>> canonical_set;
    for (const auto &multiplicity : labelled)
      canonical_set.insert(canonical_macro6(multiplicity, types));
    if (canonical_set.size() !=
        static_cast<size_t>(expected_macros[mode_index]))
      throw std::runtime_error("unexpected canonical macro count");

    uint64_t states = 0;
    uint64_t empty = 0;
    for (const auto &multiplicity : canonical_set) {
      std::vector<MacroEdge> macro_edges;
      std::array<std::vector<int>, 6> incident;
      for (int edge_type = 0; edge_type < 15; ++edge_type) {
        auto [left, right] = PAIRS6[edge_type];
        for (int copy = 0; copy < multiplicity[edge_type]; ++copy) {
          int edge = static_cast<int>(macro_edges.size());
          macro_edges.push_back({left, right});
          incident[left].push_back(edge);
          incident[right].push_back(edge);
        }
      }
      if (macro_edges.size() != 13)
        throw std::runtime_error("wrong macro edge count");

      std::array<const Relation *, 6> relations = {
        &F, &F,
        types[2] == 'A' ? &A : &B,
        types[3] == 'A' ? &A : &B,
        types[4] == 'A' ? &A : &B,
        types[5] == 'A' ? &A : &B
      };
      std::array<Constraint, 6> constraints;
      std::array<int, 6> selected = {0,0,0,0,0,0};
      std::function<bool(int)> enumerate_states = [&](int atom) -> bool {
        if (atom == 6) {
          ++states;
          for (int vertex = 0; vertex < 6; ++vertex) {
            constraints[vertex].relation = relations[vertex];
            const auto &assignment =
                relations[vertex]->assignment_representatives[
                    selected[vertex]];
            for (int port = 0; port < relations[vertex]->arity; ++port)
              constraints[vertex].port_edge[port] =
                  incident[vertex][assignment[port]];
          }
          std::vector<int> witness;
          if (!csp6_sat(
                  static_cast<int>(macro_edges.size()),
                  constraints, &witness)) {
            ++empty;
            std::cerr << "{\"classification\":\"EMPTY_D5_CANDIDATE\","
                      << "\"mode\":\"" << current_mode
                      << "\",\"multiplicity\":[";
            for (int index = 0; index < 15; ++index) {
              if (index) std::cerr << ",";
              std::cerr << multiplicity[index];
            }
            std::cerr << "],\"local_states\":[";
            for (int index = 0; index < 6; ++index) {
              if (index) std::cerr << ",";
              std::cerr << selected[index];
            }
            std::cerr << "]}\n";
            return true;
          }
          return false;
        }
        int count = static_cast<int>(
            relations[atom]->assignment_representatives.size());
        for (selected[atom] = 0; selected[atom] < count; ++selected[atom])
          if (enumerate_states(atom + 1)) return true;
        return false;
      };
      if (enumerate_states(0)) {
        std::cout << "{\"classification\":"
                     "\"EMPTY_D5_CANDIDATE_UNCERTIFIED\"}\n";
        return 20;
      }
    }
    total_states += states;
    total_empty += empty;
    row_json.push_back(
        "{\"mode\":\"" + current_mode + "\",\"canonical_macros\":" +
        std::to_string(canonical_set.size()) +
        ",\"boundary_states\":" + std::to_string(states) +
        ",\"empty_d5\":" + std::to_string(empty) + "}");
  }

  std::cout << "{\"classification\":\""
            << (total_empty ? "EMPTY_D5_CANDIDATE_UNCERTIFIED" :
                "NO_EMPTY_D5_IN_CANONICAL_FRONTIER4")
            << "\",\"labelled_macros\":" << labelled.size()
            << ",\"rows\":[";
  for (int index = 0; index < static_cast<int>(row_json.size()); ++index) {
    if (index) std::cout << ",";
    std::cout << row_json[index];
  }
  std::cout << "],\"boundary_states\":" << total_states
            << ",\"empty_d5\":" << total_empty << "}\n";
  return total_empty ? 20 : 0;
}
