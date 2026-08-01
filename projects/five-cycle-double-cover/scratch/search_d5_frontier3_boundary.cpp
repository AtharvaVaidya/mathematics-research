// Exact boundary-CSP search for the loopless D5 macro frontier
//   two C5 five-poles + three sharp four-poles.
//
// The program:
//   1. reconstructs each atom's exact ordered D5 boundary relation;
//   2. computes the full terminal stabilizer of each relation;
//   3. enumerates connected bridgeless macro multiplicity matrices,
//      canonically modulo type-preserving atom permutations;
//   4. enumerates terminal-to-half-edge bijections modulo the independent
//      local relation stabilizers; and
//   5. solves the resulting exact relation CSP by a precomputed partial-word
//      extension dynamic program.
//
// Modes AAA, AAB, ABB, BBB use A = graph6 C] and B = graph6 ECxo.
// Port permutations of A cover the three masks 0x3ef, 0x3f7, 0x3fd;
// B covers 0x3fe.  Consequently the four modes cover every multiset of
// three sharp four-pole relations.

#include <algorithm>
#include <array>
#include <cstdint>
#include <functional>
#include <iostream>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

struct Atom {
  int vertices;
  std::vector<std::pair<int, int>> edges;
  std::vector<int> terminals;
};

struct Relation {
  int arity;
  std::vector<std::array<int, 5>> rows;
  std::vector<char> extendable;
  std::vector<std::vector<int>> stabilizer;
  std::vector<std::vector<int>> assignment_representatives;
};

struct MacroEdge {
  int left;
  int right;
};

struct Constraint {
  const Relation *relation;
  std::array<int, 5> port_edge;
};

static constexpr std::array<std::pair<int, int>, 10> PAIRS = {{
  {0,1},{0,2},{0,3},{0,4},{1,2},
  {1,3},{1,4},{2,3},{2,4},{3,4}
}};

static const std::array<int, 10> D5 = [] {
  std::array<int, 10> labels{};
  for (int index = 0; index < 10; ++index)
    labels[index] =
        (1 << PAIRS[index].first) | (1 << PAIRS[index].second);
  return labels;
}();

static Atom five_atom() {
  return {5, {{0,1},{1,2},{2,3},{3,4},{0,4}}, {0,1,2,3,4}};
}

static Atom four_a() {
  return {4, {{0,2},{1,2},{0,3},{1,3}}, {0,1,2,3}};
}

static Atom four_b() {
  return {
    6,
    {{0,3},{0,4},{1,4},{2,4},{1,5},{2,5},{3,5}},
    {0,1,2,3}
  };
}

static bool is_d5_label(int mask) {
  return std::find(D5.begin(), D5.end(), mask) != D5.end();
}

static bool extends_boundary(
    const Atom &atom, const std::array<int, 5> &boundary) {
  std::vector<std::vector<int>> incident(atom.vertices);
  for (int edge = 0; edge < static_cast<int>(atom.edges.size()); ++edge) {
    incident[atom.edges[edge].first].push_back(edge);
    incident[atom.edges[edge].second].push_back(edge);
  }
  std::vector<int> terminal_label(atom.vertices, 0);
  for (int port = 0; port < static_cast<int>(atom.terminals.size()); ++port)
    terminal_label[atom.terminals[port]] = D5[boundary[port]];

  std::function<bool(std::vector<int>)> search =
      [&](std::vector<int> values) -> bool {
    while (true) {
      bool changed = false;
      for (int vertex = 0; vertex < atom.vertices; ++vertex) {
        int xor_value = terminal_label[vertex];
        int unknown = -1;
        int unknown_count = 0;
        for (int edge : incident[vertex]) {
          if (values[edge] < 0) {
            unknown = edge;
            ++unknown_count;
          } else {
            xor_value ^= D5[values[edge]];
          }
        }
        if (!unknown_count) {
          if (xor_value) return false;
        } else if (unknown_count == 1) {
          if (!is_d5_label(xor_value)) return false;
          int label = static_cast<int>(
              std::find(D5.begin(), D5.end(), xor_value) - D5.begin());
          if (values[unknown] >= 0 && values[unknown] != label) return false;
          if (values[unknown] < 0) {
            values[unknown] = label;
            changed = true;
          }
        }
      }
      if (!changed) break;
    }
    int edge = -1;
    for (int index = 0; index < static_cast<int>(values.size()); ++index)
      if (values[index] < 0) { edge = index; break; }
    if (edge < 0) return true;
    for (int label = 0; label < 10; ++label) {
      std::vector<int> branch = values;
      branch[edge] = label;
      if (search(std::move(branch))) return true;
    }
    return false;
  };
  return search(std::vector<int>(atom.edges.size(), -1));
}

static int word_code(const std::array<int, 5> &word, int arity) {
  int code = 0;
  int power = 1;
  for (int port = 0; port < arity; ++port) {
    code += word[port] * power;
    power *= 11;
  }
  return code;
}

static Relation make_relation(const Atom &atom) {
  Relation answer;
  answer.arity = static_cast<int>(atom.terminals.size());
  int total = 1;
  for (int port = 0; port < answer.arity; ++port) total *= 10;
  for (int code = 0; code < total; ++code) {
    int remaining = code;
    std::array<int, 5> word = {0,0,0,0,0};
    for (int port = 0; port < answer.arity; ++port) {
      word[port] = remaining % 10;
      remaining /= 10;
    }
    if (extends_boundary(atom, word)) answer.rows.push_back(word);
  }

  int partial_total = 1;
  for (int port = 0; port < answer.arity; ++port) partial_total *= 11;
  answer.extendable.assign(partial_total, false);
  for (const auto &row : answer.rows) {
    for (int subset = 0; subset < (1 << answer.arity); ++subset) {
      std::array<int, 5> partial = {10,10,10,10,10};
      for (int port = 0; port < answer.arity; ++port)
        if ((subset >> port) & 1) partial[port] = row[port];
      answer.extendable[word_code(partial, answer.arity)] = true;
    }
  }

  std::vector<int> permutation(answer.arity);
  std::iota(permutation.begin(), permutation.end(), 0);
  do {
    bool preserves = true;
    for (const auto &row : answer.rows) {
      std::array<int, 5> transformed = {0,0,0,0,0};
      for (int port = 0; port < answer.arity; ++port)
        transformed[port] = row[permutation[port]];
      if (!answer.extendable[word_code(transformed, answer.arity)]) {
        preserves = false;
        break;
      }
    }
    if (preserves) answer.stabilizer.push_back(permutation);
  } while (std::next_permutation(permutation.begin(), permutation.end()));

  std::set<std::vector<int>> representatives;
  permutation.resize(answer.arity);
  std::iota(permutation.begin(), permutation.end(), 0);
  do {
    std::vector<int> canonical = permutation;
    for (const auto &symmetry : answer.stabilizer) {
      std::vector<int> transformed(answer.arity);
      for (int port = 0; port < answer.arity; ++port)
        transformed[port] = permutation[symmetry[port]];
      canonical = std::min(canonical, transformed);
    }
    representatives.insert(std::move(canonical));
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  answer.assignment_representatives.assign(
      representatives.begin(), representatives.end());
  return answer;
}

static bool macro_connected_without(
    const std::array<int, 10> &multiplicity, int skipped_type) {
  std::array<char, 5> seen = {true,false,false,false,false};
  std::array<int, 5> stack = {0,0,0,0,0};
  int size = 1;
  while (size) {
    int current = stack[--size];
    for (int type = 0; type < 10; ++type) {
      int copies = multiplicity[type] - (type == skipped_type);
      if (copies <= 0) continue;
      auto [left, right] = PAIRS[type];
      int other = left == current ? right : right == current ? left : -1;
      if (other >= 0 && !seen[other]) {
        seen[other] = true;
        stack[size++] = other;
      }
    }
  }
  return std::count(seen.begin(), seen.end(), true) == 5;
}

static bool macro_bridgeless(const std::array<int, 10> &multiplicity) {
  if (!macro_connected_without(multiplicity, -1)) return false;
  for (int type = 0; type < 10; ++type)
    if (multiplicity[type] &&
        !macro_connected_without(multiplicity, type))
      return false;
  return true;
}

static std::vector<std::array<int, 10>> labelled_macro_matrices() {
  const std::array<int, 5> target = {5,5,4,4,4};
  std::array<int, 5> degree = {0,0,0,0,0};
  std::array<int, 10> multiplicity = {0,0,0,0,0,0,0,0,0,0};
  std::vector<std::array<int, 10>> answer;
  std::function<void(int)> enumerate = [&](int type) {
    if (type == 10) {
      if (degree == target && macro_bridgeless(multiplicity))
        answer.push_back(multiplicity);
      return;
    }
    auto [left, right] = PAIRS[type];
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

static std::vector<std::vector<int>> type_preserving_orders(
    const std::array<char, 5> &types) {
  std::vector<std::vector<int>> answer;
  std::vector<int> order = {0,1,2,3,4};
  do {
    bool okay = true;
    for (int position = 0; position < 5; ++position)
      okay &= types[order[position]] == types[position];
    if (okay) answer.push_back(order);
  } while (std::next_permutation(order.begin(), order.end()));
  return answer;
}

static std::array<int, 10> canonical_macro(
    const std::array<int, 10> &multiplicity,
    const std::array<char, 5> &types) {
  std::array<std::array<int, 5>, 5> matrix{};
  for (int type = 0; type < 10; ++type) {
    auto [left, right] = PAIRS[type];
    matrix[left][right] = matrix[right][left] = multiplicity[type];
  }
  std::array<int, 10> best;
  best.fill(99);
  for (const auto &order : type_preserving_orders(types)) {
    std::array<int, 10> transformed;
    for (int type = 0; type < 10; ++type) {
      auto [left, right] = PAIRS[type];
      transformed[type] = matrix[order[left]][order[right]];
    }
    best = std::min(best, transformed);
  }
  return best;
}

static bool constraint_extendable(
    const Constraint &constraint, const std::vector<int> &values) {
  std::array<int, 5> word = {10,10,10,10,10};
  for (int port = 0; port < constraint.relation->arity; ++port) {
    int label = values[constraint.port_edge[port]];
    word[port] = label < 0 ? 10 : label;
  }
  return constraint.relation->extendable[
      word_code(word, constraint.relation->arity)];
}

static bool csp_sat(
    int edge_count,
    const std::array<Constraint, 5> &constraints,
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
  if (mode != "all" && mode != "AAA" && mode != "AAB" &&
      mode != "ABB" && mode != "BBB") {
    std::cerr << "mode must be all, AAA, AAB, ABB, or BBB\n";
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

  const auto labelled = labelled_macro_matrices();
  if (labelled.size() != 178)
    throw std::runtime_error("unexpected labelled macro count");
  const std::array<std::string, 4> modes = {"AAA","AAB","ABB","BBB"};

  std::cout << "{\"classification\":\"";
  uint64_t total_states = 0;
  uint64_t total_empty = 0;
  std::vector<std::string> row_json;
  for (const std::string &current_mode : modes) {
    if (mode != "all" && mode != current_mode) continue;
    std::array<char, 5> types = {
      'F','F',current_mode[0],current_mode[1],current_mode[2]
    };
    std::set<std::array<int, 10>> canonical_set;
    for (const auto &multiplicity : labelled)
      canonical_set.insert(canonical_macro(multiplicity, types));
    size_t expected_macros =
        current_mode == "AAA" || current_mode == "BBB" ? 25 : 56;
    if (canonical_set.size() != expected_macros)
      throw std::runtime_error("unexpected canonical macro count");

    uint64_t states = 0;
    uint64_t empty = 0;
    for (const auto &multiplicity : canonical_set) {
      std::vector<MacroEdge> macro_edges;
      std::array<std::vector<int>, 5> incident;
      for (int edge_type = 0; edge_type < 10; ++edge_type) {
        auto [left, right] = PAIRS[edge_type];
        for (int copy = 0; copy < multiplicity[edge_type]; ++copy) {
          int edge = static_cast<int>(macro_edges.size());
          macro_edges.push_back({left, right});
          incident[left].push_back(edge);
          incident[right].push_back(edge);
        }
      }
      if (macro_edges.size() != 11)
        throw std::runtime_error("wrong macro edge count");

      std::array<const Relation *, 5> relations = {
        &F, &F,
        types[2] == 'A' ? &A : &B,
        types[3] == 'A' ? &A : &B,
        types[4] == 'A' ? &A : &B
      };
      std::array<Constraint, 5> constraints;
      std::array<int, 5> selected = {0,0,0,0,0};
      std::function<bool(int)> enumerate_states = [&](int atom) -> bool {
        if (atom == 5) {
          ++states;
          for (int vertex = 0; vertex < 5; ++vertex) {
            constraints[vertex].relation = relations[vertex];
            const auto &assignment =
                relations[vertex]->assignment_representatives[
                    selected[vertex]];
            for (int port = 0; port < relations[vertex]->arity; ++port)
              constraints[vertex].port_edge[port] =
                  incident[vertex][assignment[port]];
          }
          std::vector<int> witness;
          if (!csp_sat(
                  static_cast<int>(macro_edges.size()),
                  constraints, &witness)) {
            ++empty;
            std::cerr << "{\"classification\":\"EMPTY_D5_CANDIDATE\","
                      << "\"mode\":\"" << current_mode
                      << "\",\"multiplicity\":[";
            for (int index = 0; index < 10; ++index) {
              if (index) std::cerr << ",";
              std::cerr << multiplicity[index];
            }
            std::cerr << "],\"local_states\":[";
            for (int index = 0; index < 5; ++index) {
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
        std::cout << "EMPTY_D5_CANDIDATE_UNCERTIFIED\"}\n";
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
  std::cout << (total_empty ? "EMPTY_D5_CANDIDATE_UNCERTIFIED" :
      "NO_EMPTY_D5_IN_CANONICAL_FRONTIER3")
            << "\",\"relations\":{\"F_rows\":" << F.rows.size()
            << ",\"A_rows\":" << A.rows.size()
            << ",\"B_rows\":" << B.rows.size()
            << ",\"F_stabilizer\":" << F.stabilizer.size()
            << ",\"A_stabilizer\":" << A.stabilizer.size()
            << ",\"B_stabilizer\":" << B.stabilizer.size()
            << "},\"labelled_macros\":" << labelled.size()
            << ",\"rows\":[";
  for (int index = 0; index < static_cast<int>(row_json.size()); ++index) {
    if (index) std::cout << ",";
    std::cout << row_json[index];
  }
  std::cout << "],\"boundary_states\":" << total_states
            << ",\"empty_d5\":" << total_empty << "}\n";
  return total_empty ? 20 : 0;
}
