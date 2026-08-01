#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <functional>
#include <iostream>
#include <set>
#include <string>
#include <tuple>
#include <vector>

using Word = std::vector<int>;

static std::vector<int> d_values() {
  std::vector<int> out;
  for (int mask = 0; mask < 32; ++mask)
    if (__builtin_popcount((unsigned)mask) == 2) out.push_back(mask);
  return out;
}

static int permute_mask(int mask, const std::array<int, 5>& permutation) {
  int out = 0;
  for (int color = 0; color < 5; ++color)
    if ((mask >> color) & 1) out |= 1 << permutation[color];
  return out;
}

static Word canonical_word(const Word& word) {
  std::array<int, 5> permutation = {0, 1, 2, 3, 4};
  Word best(word.size(), 99);
  do {
    Word candidate(word.size());
    for (int i = 0; i < (int)word.size(); ++i)
      candidate[i] = permute_mask(word[i], permutation);
    best = std::min(best, candidate);
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  return best;
}

static std::vector<Word> orbit_representatives(int terminals) {
  const auto d = d_values();
  std::set<Word> representatives;
  Word prefix;
  std::function<void(int, int)> extend = [&](int position, int total) {
    if (position == terminals - 1) {
      if (__builtin_popcount((unsigned)total) != 2) return;
      Word word = prefix;
      word.push_back(total);
      representatives.insert(canonical_word(word));
      return;
    }
    for (int value : d) {
      prefix.push_back(value);
      extend(position + 1, total ^ value);
      prefix.pop_back();
    }
  };
  extend(0, 0);
  return {representatives.begin(), representatives.end()};
}

static std::pair<int, std::vector<std::pair<int, int>>> parse_graph6(
    const std::string& record) {
  if (record.empty()) throw std::runtime_error("empty graph6");
  const int n = ((unsigned char)record[0]) - 63;
  if (n < 0 || n > 62) throw std::runtime_error("unsupported graph6 order");
  std::vector<int> bits;
  for (size_t i = 1; i < record.size(); ++i) {
    int value = ((unsigned char)record[i]) - 63;
    for (int shift = 5; shift >= 0; --shift)
      bits.push_back((value >> shift) & 1);
  }
  size_t cursor = 0;
  std::vector<std::pair<int, int>> edges;
  for (int right = 1; right < n; ++right)
    for (int left = 0; left < right; ++left) {
      if (cursor >= bits.size()) throw std::runtime_error("short graph6");
      if (bits[cursor]) edges.emplace_back(left, right);
      ++cursor;
    }
  return {n, edges};
}

static int label_index(int mask, const std::vector<int>& d) {
  auto it = std::find(d.begin(), d.end(), mask);
  return it == d.end() ? -1 : int(it - d.begin());
}

static int variable(int edge, int label) { return 1 + 10 * edge + label; }

static std::tuple<int, std::string, unsigned long long> solve_record(
    const std::string& record, int terminal_count, int stop_at) {
  const auto [n, proper_edges] = parse_graph6(record);
  const auto d = d_values();
  const auto representatives = orbit_representatives(terminal_count);
  if (representatives.size() > 64) throw std::runtime_error("orbit count");

  std::vector<std::vector<int>> incident(n);
  for (int edge = 0; edge < (int)proper_edges.size(); ++edge) {
    auto [left, right] = proper_edges[edge];
    incident[left].push_back(edge);
    incident[right].push_back(edge);
  }
  std::vector<int> terminals;
  for (int vertex = 0; vertex < n; ++vertex) {
    if (incident[vertex].size() == 2) terminals.push_back(vertex);
    else if (incident[vertex].size() != 3)
      throw std::runtime_error("not degree 2/3");
  }
  if ((int)terminals.size() != terminal_count)
    throw std::runtime_error("wrong terminal count");

  const int first_boundary = proper_edges.size();
  for (int i = 0; i < terminal_count; ++i)
    incident[terminals[i]].push_back(first_boundary + i);
  const int total_edges = first_boundary + terminal_count;

  CaDiCaL::Solver solver;
  for (int edge = 0; edge < total_edges; ++edge) {
    for (int label = 0; label < 10; ++label)
      solver.add(variable(edge, label));
    solver.add(0);
    for (int left = 0; left < 10; ++left)
      for (int right = left + 1; right < 10; ++right) {
        solver.add(-variable(edge, left));
        solver.add(-variable(edge, right));
        solver.add(0);
      }
  }

  // The first two edge labels at a cubic vertex uniquely force the third:
  // three weight-two masks have xor zero exactly when they are a triangle.
  for (const auto& edges : incident) {
    if (edges.size() != 3) throw std::runtime_error("bad cubic incidence");
    for (int left = 0; left < 10; ++left)
      for (int right = 0; right < 10; ++right) {
        int forced = label_index(d[left] ^ d[right], d);
        solver.add(-variable(edges[0], left));
        solver.add(-variable(edges[1], right));
        if (forced >= 0) solver.add(variable(edges[2], forced));
        solver.add(0);
      }
  }

  int count = 0;
  unsigned long long mask = 0;
  for (int orbit = 0; orbit < (int)representatives.size(); ++orbit) {
    const auto& boundary = representatives[orbit];
    for (int position = 0; position < terminal_count; ++position) {
      int label = label_index(boundary[position], d);
      solver.assume(variable(first_boundary + position, label));
    }
    int result = solver.solve();
    if (result == 10) {
      ++count;
      mask |= 1ULL << orbit;
      if (count >= stop_at) break;
    } else if (result != 20) {
      throw std::runtime_error("unknown SAT result");
    }
  }
  return {count, record, mask};
}

int main(int argc, char** argv) {
  int stop_at = 63;
  int terminal_count = 5;
  for (int i = 1; i < argc; ++i) {
    std::string option = argv[i];
    if (option == "--stop-at" && i + 1 < argc)
      stop_at = std::stoi(argv[++i]);
    else if (option == "--terminals" && i + 1 < argc)
      terminal_count = std::stoi(argv[++i]);
    else {
      std::cerr << "usage: boundary_cadical [--terminals K] [--stop-at N]\n";
      return 2;
    }
  }
  std::string record;
  while (std::getline(std::cin, record)) {
    if (record.empty()) continue;
    try {
      auto [count, same_record, mask] =
          solve_record(record, terminal_count, stop_at);
      std::cout << same_record << '\t' << count << '\t'
                << std::hex << mask << std::dec << '\n';
    } catch (const std::exception& error) {
      std::cout << record << "\tERROR\t" << error.what() << '\n';
    }
  }
}
