// Independent streaming checker for the retained order-28 two-orbit
// fixed-five certificates.  This checker does not use CaDiCaL and does
// not import the producer.  It reads the two gzip streams directly,
// reconstructs graph6 incidence, and checks every displayed D5 label.

#include <zlib.h>

#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

using Boundary = std::array<int, 4>;

constexpr std::uint64_t kExpectedRows = 9'725'709;
constexpr std::array<unsigned, 6> kExceptional = {
    0x02b, 0x053, 0x119, 0x2e4, 0x3a4, 0x3c4};
constexpr std::array<int, 2> kOrbits = {0, 2};

std::string gzip_line(gzFile file) {
  std::string result;
  std::array<char, 4096> buffer{};
  while (true) {
    char* value = gzgets(file, buffer.data(), static_cast<int>(buffer.size()));
    if (value == nullptr) {
      if (gzeof(file)) {
        return result;
      }
      int code = Z_OK;
      const char* message = gzerror(file, &code);
      throw std::runtime_error(std::string("gzip read failed: ") + message);
    }
    result += value;
    if (!result.empty() && result.back() == '\n') {
      result.pop_back();
      return result;
    }
    if (gzeof(file)) {
      return result;
    }
  }
}

std::vector<int> d5_values() {
  std::vector<int> values;
  for (int value = 0; value < 32; ++value) {
    if (std::popcount(static_cast<unsigned>(value)) == 2) {
      values.push_back(value);
    }
  }
  if (values.size() != 10) {
    throw std::runtime_error("D5 enumeration failed");
  }
  return values;
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

Boundary canonical_boundary(const Boundary& word) {
  std::array<int, 5> permutation = {0, 1, 2, 3, 4};
  Boundary best = {99, 99, 99, 99};
  do {
    Boundary candidate{};
    for (int position = 0; position < 4; ++position) {
      candidate[position] = permute_mask(word[position], permutation);
    }
    best = std::min(best, candidate);
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  return best;
}

std::vector<Boundary> orbit_representatives() {
  const std::vector<int> values = d5_values();
  std::set<Boundary> representatives;
  for (int first : values) {
    for (int second : values) {
      for (int third : values) {
        const int fourth = first ^ second ^ third;
        if (std::popcount(static_cast<unsigned>(fourth)) == 2) {
          representatives.insert(
              canonical_boundary({first, second, third, fourth}));
        }
      }
    }
  }
  if (representatives.size() != 10) {
    throw std::runtime_error("boundary orbit enumeration failed");
  }
  return {representatives.begin(), representatives.end()};
}

std::pair<int, std::vector<std::pair<int, int>>> decode_graph6(
    const std::string& record) {
  if (record.empty() || static_cast<unsigned char>(record.front()) == 126) {
    throw std::runtime_error("only short graph6 is supported");
  }
  const int vertices = static_cast<unsigned char>(record.front()) - 63;
  if (vertices < 0 || vertices > 62) {
    throw std::runtime_error("invalid graph6 order");
  }
  std::vector<std::pair<int, int>> edges;
  std::size_t bit = 0;
  for (int right = 1; right < vertices; ++right) {
    for (int left = 0; left < right; ++left, ++bit) {
      const std::size_t byte = 1 + bit / 6;
      if (byte >= record.size()) {
        throw std::runtime_error("short graph6 record");
      }
      const int value = static_cast<unsigned char>(record[byte]) - 63;
      if (value < 0 || value >= 64) {
        throw std::runtime_error("invalid graph6 character");
      }
      if ((value >> (5 - bit % 6)) & 1) {
        edges.emplace_back(left, right);
      }
    }
  }
  const std::size_t used_bits =
      static_cast<std::size_t>(vertices) * (vertices - 1) / 2;
  for (std::size_t extra = used_bits;
       extra < 6 * (record.size() - 1); ++extra) {
    const int value =
        static_cast<unsigned char>(record[1 + extra / 6]) - 63;
    if ((value >> (5 - extra % 6)) & 1) {
      throw std::runtime_error("nonzero graph6 padding");
    }
  }
  return {vertices, edges};
}

void check_labels(const std::string& record, const std::string& encoded,
                  int orbit, const std::vector<Boundary>& representatives,
                  std::uint64_t row) {
  const auto [vertices, edges] = decode_graph6(record);
  std::vector<std::vector<int>> incidence(vertices);
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    incidence[edges[edge].first].push_back(edge);
    incidence[edges[edge].second].push_back(edge);
  }
  std::vector<int> terminals;
  for (int vertex = 0; vertex < vertices; ++vertex) {
    if (incidence[vertex].size() == 2) {
      terminals.push_back(vertex);
    } else if (incidence[vertex].size() != 3) {
      throw std::runtime_error("row " + std::to_string(row) +
                               ": non-cubic pole incidence");
    }
  }
  if (terminals.size() != 4) {
    throw std::runtime_error("row " + std::to_string(row) +
                             ": expected four terminals");
  }

  const std::vector<int> values = d5_values();
  const std::size_t total_edges = edges.size() + 4;
  if (encoded.size() != total_edges) {
    throw std::runtime_error("row " + std::to_string(row) +
                             ": wrong witness length");
  }
  std::vector<int> labels;
  labels.reserve(total_edges);
  for (char digit : encoded) {
    if (digit < '0' || digit > '9') {
      throw std::runtime_error("row " + std::to_string(row) +
                               ": non-digit witness label");
    }
    labels.push_back(values.at(static_cast<std::size_t>(digit - '0')));
  }

  const Boundary expected = representatives.at(orbit);
  for (int position = 0; position < 4; ++position) {
    if (labels[edges.size() + position] != expected[position]) {
      throw std::runtime_error("row " + std::to_string(row) +
                               ": wrong boundary word");
    }
    incidence[terminals[position]].push_back(
        static_cast<int>(edges.size()) + position);
  }
  for (int vertex = 0; vertex < vertices; ++vertex) {
    if (incidence[vertex].size() != 3) {
      throw std::runtime_error("row " + std::to_string(row) +
                               ": completed incidence is not cubic");
    }
    int sum = 0;
    for (int edge : incidence[vertex]) {
      sum ^= labels[edge];
    }
    if (sum != 0) {
      throw std::runtime_error("row " + std::to_string(row) +
                               ": vertex xor failure");
    }
  }
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 3) {
    std::cerr << "usage: verify_boundary_two_orbit_witness_fast "
                 "POLES.g6.gz WITNESSES.tsv.gz\n";
    return 2;
  }
  try {
    for (unsigned mask : kExceptional) {
      bool excluded = false;
      for (int orbit : kOrbits) {
        excluded |= ((mask >> orbit) & 1U) == 0;
      }
      if (!excluded) {
        throw std::runtime_error("two-orbit mask gate failed");
      }
    }
    const std::vector<Boundary> representatives = orbit_representatives();
    if (representatives.at(0) != Boundary{3, 3, 3, 3} ||
        representatives.at(2) != Boundary{3, 3, 12, 12}) {
      throw std::runtime_error("unexpected canonical orbit order");
    }

    gzFile poles = gzopen(argv[1], "rb");
    gzFile witnesses = gzopen(argv[2], "rb");
    if (poles == nullptr || witnesses == nullptr) {
      if (poles != nullptr) gzclose(poles);
      if (witnesses != nullptr) gzclose(witnesses);
      throw std::runtime_error("could not open an input stream");
    }

    std::uint64_t rows = 0;
    while (true) {
      const std::string pole = gzip_line(poles);
      if (pole.empty() && gzeof(poles)) {
        break;
      }
      const std::string witness = gzip_line(witnesses);
      if (witness.empty() && gzeof(witnesses)) {
        throw std::runtime_error("short witness stream");
      }
      const std::size_t first_tab = witness.find('\t');
      const std::size_t second_tab =
          first_tab == std::string::npos
              ? std::string::npos
              : witness.find('\t', first_tab + 1);
      if (first_tab == std::string::npos ||
          second_tab == std::string::npos ||
          witness.find('\t', second_tab + 1) != std::string::npos) {
        throw std::runtime_error("malformed witness row");
      }
      if (witness.substr(0, first_tab) != pole) {
        throw std::runtime_error("pole/witness stream mismatch");
      }
      ++rows;
      check_labels(pole,
                   witness.substr(first_tab + 1,
                                  second_tab - first_tab - 1),
                   kOrbits[0], representatives, rows);
      check_labels(pole, witness.substr(second_tab + 1), kOrbits[1],
                   representatives, rows);
    }
    const std::string extra = gzip_line(witnesses);
    const bool witness_has_extra = !extra.empty() || !gzeof(witnesses);
    gzclose(poles);
    gzclose(witnesses);
    if (witness_has_extra) {
      throw std::runtime_error("long witness stream");
    }
    if (rows != kExpectedRows) {
      throw std::runtime_error("unexpected row count");
    }

    std::cout
        << "{\"classification\":\"PASS\","
        << "\"checker\":\"independent-zlib-cpp\","
        << "\"certificate_orbits\":[0,2],"
        << "\"rows\":" << rows << ","
        << "\"witnesses\":" << 2 * rows << "}\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR " << error.what() << '\n';
    return 3;
  }
}
