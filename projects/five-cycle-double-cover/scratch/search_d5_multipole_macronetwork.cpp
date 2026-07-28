// Deterministic discovery search for FiveCDC-obstructing multipole networks.
//
// Two or more C5 five-poles and any number of the two underlying
// internally bridgeless four-poles are connected by a random perfect
// matching of their terminals.  The four order<=14 proper relations are
// realized by the C4 atom under three terminal orders and the six-vertex
// atom under its terminal-symmetric order.  Random port matching samples
// every required terminal order.
//
// This is a discovery program.  Any UNSAT output must be regenerated as a
// complete graph CNF and certified independently before it is a result.

#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <functional>
#include <numeric>
#include <random>
#include <string>
#include <utility>
#include <vector>

struct Atom {
  int vertices;
  std::vector<std::pair<int, int>> edges;
  std::vector<int> terminals;
};

struct Port {
  int atom;
  int position;
};

using Pairing = std::vector<std::pair<Port, Port>>;

static Atom five_atom() {
  return {5, {{0,1},{1,2},{2,3},{3,4},{0,4}}, {0,1,2,3,4}};
}

static Atom four_a() {
  // graph6 C] = K_{2,2}; its terminal permutations realize the three
  // proper masks missing four-pole orbit 1, 3, or 4.
  return {4, {{0,2},{1,2},{0,3},{1,3}}, {0,1,2,3}};
}

static Atom four_b() {
  // graph6 ECxo; its relation is the proper mask missing orbit 0.
  return {
    6,
    {{0,3},{0,4},{1,4},{2,4},{1,5},{2,5},{3,5}},
    {0,1,2,3}
  };
}

static bool macro_connected_without(
    const Pairing &pairing, int atoms, int skipped) {
  std::vector<char> seen(atoms, false);
  std::vector<int> stack = {0};
  seen[0] = true;
  while (!stack.empty()) {
    int current = stack.back();
    stack.pop_back();
    for (int edge = 0; edge < static_cast<int>(pairing.size()); ++edge) {
      if (edge == skipped) continue;
      int left = pairing[edge].first.atom;
      int right = pairing[edge].second.atom;
      int other = -1;
      if (left == current) other = right;
      if (right == current) other = left;
      if (other >= 0 && !seen[other]) {
        seen[other] = true;
        stack.push_back(other);
      }
    }
  }
  return std::count(seen.begin(), seen.end(), true) == atoms;
}

static bool macro_bridgeless(const Pairing &pairing, int atoms) {
  if (!macro_connected_without(pairing, atoms, -1)) return false;
  for (int edge = 0; edge < static_cast<int>(pairing.size()); ++edge) {
    if (!macro_connected_without(pairing, atoms, edge)) return false;
  }
  return true;
}

static std::pair<int, std::vector<std::pair<int,int>>> expand(
    const std::vector<Atom> &atoms, const Pairing &pairing) {
  std::vector<int> offset(atoms.size());
  int vertices = 0;
  std::vector<std::pair<int,int>> edges;
  for (int index = 0; index < static_cast<int>(atoms.size()); ++index) {
    offset[index] = vertices;
    for (auto [left, right] : atoms[index].edges) {
      edges.push_back({vertices + left, vertices + right});
    }
    vertices += atoms[index].vertices;
  }
  for (const auto &connection : pairing) {
    Port left = connection.first;
    Port right = connection.second;
    int u = offset[left.atom] + atoms[left.atom].terminals[left.position];
    int v = offset[right.atom] + atoms[right.atom].terminals[right.position];
    if (u > v) std::swap(u, v);
    edges.push_back({u, v});
  }
  std::sort(edges.begin(), edges.end());
  return {vertices, edges};
}

static int variable(int edge, int coordinate) {
  return 5 * edge + coordinate + 1;
}

static void clause(CaDiCaL::Solver &solver, std::initializer_list<int> row) {
  for (int literal : row) solver.add(literal);
  solver.add(0);
}

static bool fivecdc_sat(
    int vertices, const std::vector<std::pair<int,int>> &edges) {
  CaDiCaL::Solver solver;
  std::vector<std::vector<int>> incident(vertices);
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    incident[edges[edge].first].push_back(edge);
    incident[edges[edge].second].push_back(edge);
    std::array<int,5> x;
    for (int c = 0; c < 5; ++c) x[c] = variable(edge, c);
    for (int a = 0; a < 5; ++a)
      for (int b = a + 1; b < 5; ++b)
        for (int c = b + 1; c < 5; ++c)
          clause(solver, {-x[a], -x[b], -x[c]});
    for (int omitted = 0; omitted < 5; ++omitted) {
      for (int c = 0; c < 5; ++c)
        if (c != omitted) solver.add(x[c]);
      solver.add(0);
    }
  }
  for (const auto &row : incident) {
    if (row.size() != 3) return false;
    for (int c = 0; c < 5; ++c) {
      int x = variable(row[0], c);
      int y = variable(row[1], c);
      int z = variable(row[2], c);
      clause(solver, {-x,-y,-z});
      clause(solver, {-x, y, z});
      clause(solver, { x,-y, z});
      clause(solver, { x, y,-z});
    }
  }
  int result = solver.solve();
  if (result == 10) {
    for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
      int count = 0;
      for (int c = 0; c < 5; ++c)
        count += solver.val(variable(edge, c)) > 0;
      if (count != 2) throw std::runtime_error("bad FiveCDC edge model");
    }
    for (const auto &row : incident)
      for (int c = 0; c < 5; ++c) {
        int parity = 0;
        for (int edge : row)
          parity ^= solver.val(variable(edge, c)) > 0;
        if (parity) throw std::runtime_error("bad FiveCDC parity model");
      }
    return true;
  }
  if (result == 20) return false;
  throw std::runtime_error("CaDiCaL returned UNKNOWN");
}

static bool tait_sat(
    int vertices, const std::vector<std::pair<int,int>> &edges) {
  CaDiCaL::Solver solver;
  std::vector<std::vector<int>> incident(vertices);
  auto x = [](int edge, int color) { return 3 * edge + color + 1; };
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    incident[edges[edge].first].push_back(edge);
    incident[edges[edge].second].push_back(edge);
    clause(solver, {x(edge,0), x(edge,1), x(edge,2)});
    clause(solver, {-x(edge,0), -x(edge,1)});
    clause(solver, {-x(edge,0), -x(edge,2)});
    clause(solver, {-x(edge,1), -x(edge,2)});
  }
  for (const auto &row : incident) {
    if (row.size() != 3) return false;
    for (int color = 0; color < 3; ++color) {
      clause(solver, {x(row[0],color),x(row[1],color),x(row[2],color)});
      clause(solver, {-x(row[0],color),-x(row[1],color)});
      clause(solver, {-x(row[0],color),-x(row[2],color)});
      clause(solver, {-x(row[1],color),-x(row[2],color)});
    }
  }
  int result = solver.solve();
  if (result == 10) {
    for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
      int count = 0;
      for (int color = 0; color < 3; ++color)
        count += solver.val(x(edge, color)) > 0;
      if (count != 1) throw std::runtime_error("bad Tait edge model");
    }
    for (const auto &row : incident)
      for (int color = 0; color < 3; ++color) {
        int count = 0;
        for (int edge : row)
          count += solver.val(x(edge, color)) > 0;
        if (count != 1) throw std::runtime_error("bad Tait vertex model");
      }
    return true;
  }
  if (result == 20) return false;
  throw std::runtime_error("CaDiCaL returned UNKNOWN");
}

static void emit_candidate(
    const std::vector<char> &types,
    const Pairing &pairing,
    int vertices,
    const std::vector<std::pair<int,int>> &edges,
    uint64_t seed,
    long long trial) {
  std::cout << "{\"classification\":\"UNSAT_CANDIDATE_UNCERTIFIED\","
            << "\"seed\":" << seed << ",\"trial\":" << trial
            << ",\"types\":\"";
  for (char type : types) std::cout << type;
  std::cout << "\",\"pairing\":[";
  for (int i = 0; i < static_cast<int>(pairing.size()); ++i) {
    if (i) std::cout << ",";
    const auto &p = pairing[i];
    std::cout << "[[" << p.first.atom << "," << p.first.position << "],["
              << p.second.atom << "," << p.second.position << "]]";
  }
  std::cout << "],\"vertices\":" << vertices << ",\"edges\":[";
  for (int i = 0; i < static_cast<int>(edges.size()); ++i) {
    if (i) std::cout << ",";
    std::cout << "[" << edges[i].first << "," << edges[i].second << "]";
  }
  std::cout << "]}" << std::endl;
}

int main(int argc, char **argv) {
  long long trials = argc > 1 ? std::stoll(argv[1]) : 100000;
  int minimum_four = argc > 2 ? std::stoi(argv[2]) : 0;
  int maximum_four = argc > 3 ? std::stoi(argv[3]) : 30;
  int five_count = argc > 4 ? std::stoi(argv[4]) : 2;
  uint64_t seed = argc > 5 ? std::stoull(argv[5]) : 20260728ULL;
  std::string four_mode = argc > 6 ? argv[6] : "mixed";
  if (five_count <= 0 || five_count % 2) {
    std::cerr << "five_count must be positive and even" << std::endl;
    return 2;
  }
  std::mt19937_64 random(seed);
  const Atom F = five_atom();
  const Atom A = four_a();
  const Atom B = four_b();

  long long accepted = 0;
  long long non_tait = 0;
  if (trials < 0) {
    if (minimum_four != maximum_four || four_mode == "mixed") {
      std::cerr << "exact mode needs one four-count and mode A or B\n";
      return 2;
    }
    std::vector<Atom> atoms;
    std::vector<char> types;
    for (int i = 0; i < five_count; ++i) {
      atoms.push_back(F);
      types.push_back('F');
    }
    for (int i = 0; i < minimum_four; ++i) {
      bool choose_b = four_mode == "B";
      atoms.push_back(choose_b ? B : A);
      types.push_back(choose_b ? 'B' : 'A');
    }
    std::vector<Port> ports;
    for (int atom = 0; atom < static_cast<int>(atoms.size()); ++atom)
      for (int position = 0;
           position < static_cast<int>(atoms[atom].terminals.size());
           ++position)
        ports.push_back({atom, position});
    std::vector<char> used(ports.size(), false);
    Pairing pairing;
    long long leaves = 0;
    std::function<bool()> enumerate = [&]() {
      int first = -1;
      for (int i = 0; i < static_cast<int>(ports.size()); ++i)
        if (!used[i]) { first = i; break; }
      if (first < 0) {
        ++leaves;
        if (!macro_bridgeless(pairing, atoms.size())) return false;
        ++accepted;
        auto [vertices, edges] = expand(atoms, pairing);
        if (tait_sat(vertices, edges)) return false;
        ++non_tait;
        if (!fivecdc_sat(vertices, edges)) {
          emit_candidate(types, pairing, vertices, edges, seed, leaves);
          return true;
        }
        return false;
      }
      used[first] = true;
      for (int second = first + 1;
           second < static_cast<int>(ports.size()); ++second) {
        if (used[second] || ports[first].atom == ports[second].atom) continue;
        used[second] = true;
        pairing.push_back({ports[first], ports[second]});
        if (enumerate()) return true;
        pairing.pop_back();
        used[second] = false;
      }
      used[first] = false;
      return false;
    };
    if (enumerate()) return 20;
    std::cout << "{\"classification\":\"NO_UNSAT_IN_EXACT_LABELLED_PAIRINGS\","
              << "\"five_atoms\":" << five_count << ",\"four_atoms\":"
              << minimum_four << ",\"four_mode\":\"" << four_mode
              << "\",\"pairing_leaves\":" << leaves << ",\"accepted\":"
              << accepted << ",\"non_tait\":" << non_tait << "}"
              << std::endl;
    return 0;
  }
  for (long long trial = 0; trial < trials; ++trial) {
    int four_count = minimum_four;
    if (maximum_four > minimum_four) {
      four_count += static_cast<int>(
          random() % (maximum_four - minimum_four + 1));
    }
    std::vector<Atom> atoms;
    std::vector<char> types;
    for (int i = 0; i < five_count; ++i) {
      atoms.push_back(F);
      types.push_back('F');
    }
    for (int i = 0; i < four_count; ++i) {
      bool choose_b =
          four_mode == "B" || (four_mode == "mixed" && (random() & 1));
      atoms.push_back(choose_b ? B : A);
      types.push_back(choose_b ? 'B' : 'A');
    }
    std::vector<Port> ports;
    for (int atom = 0; atom < static_cast<int>(atoms.size()); ++atom) {
      for (int position = 0;
           position < static_cast<int>(atoms[atom].terminals.size());
           ++position) {
        ports.push_back({atom, position});
      }
    }
    std::shuffle(ports.begin(), ports.end(), random);
    Pairing pairing;
    bool loop = false;
    for (int i = 0; i < static_cast<int>(ports.size()); i += 2) {
      if (ports[i].atom == ports[i + 1].atom) {
        loop = true;
        break;
      }
      pairing.push_back({ports[i], ports[i + 1]});
    }
    if (loop || !macro_bridgeless(pairing, atoms.size())) continue;
    ++accepted;
    auto [vertices, edges] = expand(atoms, pairing);
    if (tait_sat(vertices, edges)) {
      if (accepted % 10000 == 0) {
        std::cerr << "accepted=" << accepted << " non_tait=" << non_tait
                  << " trial=" << trial << "\n";
      }
      continue;
    }
    ++non_tait;
    if (!fivecdc_sat(vertices, edges)) {
      emit_candidate(types, pairing, vertices, edges, seed, trial);
      return 20;
    }
    if (accepted % 10000 == 0) {
      std::cerr << "accepted=" << accepted << " non_tait=" << non_tait
                << " trial=" << trial << "\n";
    }
  }
  std::cout << "{\"classification\":\"NO_UNSAT_IN_RANDOM_SAMPLE\","
            << "\"seed\":" << seed << ",\"trials\":" << trials
            << ",\"accepted\":" << accepted << ",\"non_tait\":"
            << non_tait << "}" << std::endl;
  return 0;
}
