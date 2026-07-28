// Exhaustive graph generator for the first unresolved D5 multipole frontier.
//
// The four atoms are two C5 five-poles followed by two four-poles.  A
// four-pole is either graph6 C] ("A") or graph6 ECxo ("B").  Every terminal
// is paired to a terminal of a different atom.  Only connected bridgeless
// macrographs are emitted.  Each expanded graph is simple and cubic.
//
// Usage:
//   generate_d5_frontier2_graphs AA > graphs.g6
//   generate_d5_frontier2_graphs AB > graphs.g6
//   generate_d5_frontier2_graphs BB > graphs.g6
//
// The output is graph6.  Exact counters are written to stderr.

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
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
  return {4, {{0,2},{1,2},{0,3},{1,3}}, {0,1,2,3}};
}

static Atom four_b() {
  return {
    6,
    {{0,3},{0,4},{1,4},{2,4},{1,5},{2,5},{3,5}},
    {0,1,2,3}
  };
}

static bool connected_without(
    const Pairing &pairing, int skipped) {
  std::array<char, 4> seen = {true, false, false, false};
  std::array<int, 4> stack = {0, 0, 0, 0};
  int size = 1;
  while (size) {
    int current = stack[--size];
    for (int edge = 0; edge < static_cast<int>(pairing.size()); ++edge) {
      if (edge == skipped) continue;
      int left = pairing[edge].first.atom;
      int right = pairing[edge].second.atom;
      int other = -1;
      if (left == current) other = right;
      if (right == current) other = left;
      if (other >= 0 && !seen[other]) {
        seen[other] = true;
        stack[size++] = other;
      }
    }
  }
  return seen[0] && seen[1] && seen[2] && seen[3];
}

static bool macro_bridgeless(const Pairing &pairing) {
  if (!connected_without(pairing, -1)) return false;
  for (int edge = 0; edge < static_cast<int>(pairing.size()); ++edge)
    if (!connected_without(pairing, edge)) return false;
  return true;
}

static std::pair<int, std::vector<std::pair<int,int>>> expand(
    const std::array<Atom, 4> &atoms, const Pairing &pairing) {
  std::array<int, 4> offset;
  int vertices = 0;
  std::vector<std::pair<int,int>> edges;
  for (int index = 0; index < 4; ++index) {
    offset[index] = vertices;
    for (auto [left, right] : atoms[index].edges)
      edges.push_back({vertices + left, vertices + right});
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

static std::string graph6(
    int vertices, const std::vector<std::pair<int,int>> &edges) {
  if (vertices > 62) throw std::runtime_error("long graph6 not implemented");
  std::vector<std::vector<char>> adjacent(
      vertices, std::vector<char>(vertices, false));
  for (auto [left, right] : edges) {
    if (left == right || adjacent[left][right])
      throw std::runtime_error("expanded graph is not simple");
    adjacent[left][right] = adjacent[right][left] = true;
  }
  std::string answer(1, static_cast<char>(vertices + 63));
  int accumulator = 0;
  int bits = 0;
  for (int right = 1; right < vertices; ++right)
    for (int left = 0; left < right; ++left) {
      accumulator = 2 * accumulator + adjacent[left][right];
      if (++bits == 6) {
        answer.push_back(static_cast<char>(accumulator + 63));
        accumulator = 0;
        bits = 0;
      }
    }
  if (bits) {
    accumulator <<= 6 - bits;
    answer.push_back(static_cast<char>(accumulator + 63));
  }
  return answer;
}

int main(int argc, char **argv) {
  std::string mode = argc > 1 ? argv[1] : "AA";
  if (mode != "AA" && mode != "AB" && mode != "BB") {
    std::cerr << "mode must be AA, AB, or BB\n";
    return 2;
  }
  const Atom F = five_atom();
  const Atom A = four_a();
  const Atom B = four_b();
  std::array<Atom, 4> atoms = {
    F, F, mode[0] == 'A' ? A : B, mode[1] == 'A' ? A : B
  };
  std::vector<Port> ports;
  for (int atom = 0; atom < 4; ++atom)
    for (int position = 0;
         position < static_cast<int>(atoms[atom].terminals.size());
         ++position)
      ports.push_back({atom, position});

  std::vector<char> used(ports.size(), false);
  Pairing pairing;
  uint64_t leaves = 0;
  uint64_t accepted = 0;
  auto enumerate = [&](auto &&self) -> void {
    int first = -1;
    for (int i = 0; i < static_cast<int>(ports.size()); ++i)
      if (!used[i]) { first = i; break; }
    if (first < 0) {
      ++leaves;
      if (!macro_bridgeless(pairing)) return;
      ++accepted;
      auto [vertices, edges] = expand(atoms, pairing);
      std::cout << graph6(vertices, edges) << '\n';
      return;
    }
    used[first] = true;
    for (int second = first + 1;
         second < static_cast<int>(ports.size()); ++second) {
      if (used[second] || ports[first].atom == ports[second].atom) continue;
      used[second] = true;
      pairing.push_back({ports[first], ports[second]});
      self(self);
      pairing.pop_back();
      used[second] = false;
    }
    used[first] = false;
  };
  enumerate(enumerate);
  std::cerr << "{\"mode\":\"" << mode << "\",\"pairing_leaves\":"
            << leaves << ",\"accepted\":" << accepted << "}\n";
  return 0;
}
