#include <cadical.hpp>

#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Word = std::array<int, 4>;

namespace {

constexpr std::array<unsigned, 6> kExceptionalMasks = {
    0x02b, 0x053, 0x119, 0x2e4, 0x3a4, 0x3c4};
constexpr std::array<int, 2> kCertificateOrbits = {0, 2};

std::vector<int> d_values() {
  std::vector<int> result;
  for (int value = 0; value < 32; ++value) {
    if (std::popcount(static_cast<unsigned>(value)) == 2) {
      result.push_back(value);
    }
  }
  if (result.size() != 10) {
    throw std::runtime_error("D5 construction failed");
  }
  return result;
}

int permute_mask(int mask, const std::array<int, 5>& permutation) {
  int result = 0;
  for (int coordinate = 0; coordinate < 5; ++coordinate) {
    if ((mask >> coordinate) & 1) {
      result |= 1 << permutation[coordinate];
    }
  }
  return result;
}

Word canonical_word(const Word& word) {
  std::array<int, 5> permutation = {0, 1, 2, 3, 4};
  Word best = {99, 99, 99, 99};
  do {
    Word candidate{};
    for (int position = 0; position < 4; ++position) {
      candidate[position] = permute_mask(word[position], permutation);
    }
    best = std::min(best, candidate);
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  return best;
}

std::vector<Word> orbit_representatives() {
  const auto values = d_values();
  std::set<Word> representatives;
  for (int first : values) {
    for (int second : values) {
      for (int third : values) {
        const int fourth = first ^ second ^ third;
        if (std::popcount(static_cast<unsigned>(fourth)) != 2) {
          continue;
        }
        representatives.insert(
            canonical_word({first, second, third, fourth}));
      }
    }
  }
  if (representatives.size() != 10) {
    throw std::runtime_error("expected ten boundary orbits");
  }
  return {representatives.begin(), representatives.end()};
}

std::pair<int, std::vector<std::pair<int, int>>> parse_graph6(
    const std::string& record) {
  if (record.empty() || static_cast<unsigned char>(record[0]) == 126) {
    throw std::runtime_error("only short graph6 records are supported");
  }
  const int vertices = static_cast<unsigned char>(record[0]) - 63;
  if (vertices < 0 || vertices > 62) {
    throw std::runtime_error("bad graph order");
  }
  std::vector<int> bits;
  for (std::size_t position = 1; position < record.size(); ++position) {
    const int value = static_cast<unsigned char>(record[position]) - 63;
    if (value < 0 || value >= 64) {
      throw std::runtime_error("invalid graph6 character");
    }
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }
  std::vector<std::pair<int, int>> edges;
  std::size_t cursor = 0;
  for (int right = 1; right < vertices; ++right) {
    for (int left = 0; left < right; ++left) {
      if (cursor >= bits.size()) {
        throw std::runtime_error("short graph6 record");
      }
      if (bits[cursor]) {
        edges.emplace_back(left, right);
      }
      ++cursor;
    }
  }
  return {vertices, edges};
}

int label_index(int mask, const std::vector<int>& values) {
  const auto found = std::find(values.begin(), values.end(), mask);
  return found == values.end() ? -1 : static_cast<int>(found - values.begin());
}

int variable(int edge, int label) { return 1 + 10 * edge + label; }

class BoundarySolver {
 public:
  explicit BoundarySolver(const std::string& record)
      : values_(d_values()), representatives_(orbit_representatives()) {
    const auto [vertices, proper_edges] = parse_graph6(record);
    std::vector<std::vector<int>> incident(vertices);
    for (int edge = 0; edge < static_cast<int>(proper_edges.size()); ++edge) {
      const auto [left, right] = proper_edges[edge];
      incident[left].push_back(edge);
      incident[right].push_back(edge);
    }
    std::vector<int> terminals;
    for (int vertex = 0; vertex < vertices; ++vertex) {
      if (incident[vertex].size() == 2) {
        terminals.push_back(vertex);
      } else if (incident[vertex].size() != 3) {
        throw std::runtime_error("graph is not degree two/three");
      }
    }
    if (terminals.size() != 4) {
      throw std::runtime_error("expected exactly four degree-two terminals");
    }
    first_boundary_ = static_cast<int>(proper_edges.size());
    for (int position = 0; position < 4; ++position) {
      incident[terminals[position]].push_back(first_boundary_ + position);
    }
    total_edges_ = first_boundary_ + 4;

    for (int edge = 0; edge < total_edges_; ++edge) {
      for (int label = 0; label < 10; ++label) {
        solver_.add(variable(edge, label));
      }
      solver_.add(0);
      for (int left = 0; left < 10; ++left) {
        for (int right = left + 1; right < 10; ++right) {
          solver_.add(-variable(edge, left));
          solver_.add(-variable(edge, right));
          solver_.add(0);
        }
      }
    }

    for (const auto& edges : incident) {
      if (edges.size() != 3) {
        throw std::runtime_error("bad cubic incidence");
      }
      for (int left = 0; left < 10; ++left) {
        for (int right = 0; right < 10; ++right) {
          const int forced =
              label_index(values_[left] ^ values_[right], values_);
          solver_.add(-variable(edges[0], left));
          solver_.add(-variable(edges[1], right));
          if (forced >= 0) {
            solver_.add(variable(edges[2], forced));
          }
          solver_.add(0);
        }
      }
    }
  }

  std::string solve_orbit_with_witness(int orbit) {
    const Word& boundary = representatives_.at(orbit);
    for (int position = 0; position < 4; ++position) {
      const int label = label_index(boundary[position], values_);
      if (label < 0) {
        throw std::runtime_error("boundary representative outside D5");
      }
      solver_.assume(variable(first_boundary_ + position, label));
    }
    const int result = solver_.solve();
    if (result == 20) {
      return {};
    }
    if (result != 10) {
      throw std::runtime_error("CaDiCaL returned UNKNOWN");
    }
    std::string witness;
    witness.reserve(total_edges_);
    for (int edge = 0; edge < total_edges_; ++edge) {
      int selected = -1;
      for (int label = 0; label < 10; ++label) {
        if (solver_.val(variable(edge, label)) > 0) {
          if (selected >= 0) {
            throw std::runtime_error("model selects two edge labels");
          }
          selected = label;
        }
      }
      if (selected < 0) {
        throw std::runtime_error("model omits an edge label");
      }
      witness.push_back(static_cast<char>('0' + selected));
    }
    return witness;
  }

 private:
  std::vector<int> values_;
  std::vector<Word> representatives_;
  int first_boundary_ = -1;
  int total_edges_ = -1;
  CaDiCaL::Solver solver_;
};

void check_certificate_orbits() {
  for (unsigned exceptional : kExceptionalMasks) {
    bool excluded = false;
    for (int orbit : kCertificateOrbits) {
      excluded |= ((exceptional >> orbit) & 1U) == 0;
    }
    if (!excluded) {
      throw std::runtime_error("certificate orbits do not hit every complement");
    }
  }
}

}  // namespace

int main(int argc, char** argv) {
  bool fail_on_missing = false;
  std::uint64_t progress = 0;
  for (int index = 1; index < argc; ++index) {
    const std::string option = argv[index];
    if (option == "--fail-on-missing") {
      fail_on_missing = true;
    } else if (option == "--progress" && index + 1 < argc) {
      progress = std::strtoull(argv[++index], nullptr, 10);
    } else {
      std::cerr << "usage: boundary_two_orbit_witness_cadical "
                   "[--fail-on-missing] [--progress N]\n";
      return 2;
    }
  }

  try {
    check_certificate_orbits();
    std::uint64_t rows = 0;
    std::uint64_t witnesses = 0;
    std::uint64_t missing = 0;
    std::string record;
    while (std::getline(std::cin, record)) {
      if (record.empty()) {
        continue;
      }
      BoundarySolver solver(record);
      const std::string first =
          solver.solve_orbit_with_witness(kCertificateOrbits[0]);
      const std::string second =
          solver.solve_orbit_with_witness(kCertificateOrbits[1]);
      ++rows;
      witnesses += !first.empty();
      witnesses += !second.empty();
      if (first.empty() || second.empty()) {
        ++missing;
      }
      std::cout << record << '\t' << (first.empty() ? "-" : first) << '\t'
                << (second.empty() ? "-" : second) << '\n';
      if (progress != 0 && rows % progress == 0) {
        std::cerr << "progress rows=" << rows << " witnesses=" << witnesses
                  << " missing=" << missing << '\n';
      }
    }
    std::cerr << "SUMMARY implementation=cadical mode=two-orbit-witness "
              << "rows=" << rows << " queries=" << 2 * rows
              << " witnesses=" << witnesses << " missing=" << missing
              << '\n';
    if (fail_on_missing && missing != 0) {
      return 4;
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR " << error.what() << '\n';
    return 3;
  }
}
