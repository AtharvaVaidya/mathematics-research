// Exact selector scan on the all-C10 Tait colourings of CVT[80,30].
//
// Input: one graph6 row on stdin.
// Output: a JSON certificate on stdout.
//
// The normalized Tait enumeration fixes the three incident edge objects at
// vertex 0 to colours 0,1,2.  For each colouring whose three bichromatic
// factors are eight 10-cycles, and for each common mark colour c, this
// enumerates every perfect matching of the 8+8 c-edge incidence multigraph.
// Each matching is an eight-edge mark set.  All 256 corresponding
// bichromatic selectors are then traced exactly.

#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using std::array;
using std::bitset;
using std::cin;
using std::cout;
using std::map;
using std::pair;
using std::set;
using std::string;
using std::vector;

namespace {

constexpr int MAX_EDGES = 128;
using EdgeMask = bitset<MAX_EDGES>;

struct Graph {
  int n = 0;
  vector<pair<int, int>> edges;
  vector<vector<int>> incident;
};

Graph parse_graph6(const string& row) {
  if (row.empty() || row[0] == ':' || row[0] == '>') {
    throw std::runtime_error("expected one graph6 row");
  }
  vector<int> values;
  for (unsigned char byte : row) {
    const int value = static_cast<int>(byte) - 63;
    if (value < 0 || value > 63) throw std::runtime_error("bad graph6 byte");
    values.push_back(value);
  }
  int n = 0;
  int header = 0;
  if (values[0] <= 62) {
    n = values[0];
    header = 1;
  } else if (values.size() >= 4 && values[1] <= 62) {
    n = (values[1] << 12) | (values[2] << 6) | values[3];
    header = 4;
  } else {
    throw std::runtime_error("unsupported graph6 header");
  }
  Graph graph;
  graph.n = n;
  graph.incident.assign(n, {});
  int bit = 0;
  for (int v = 1; v < n; ++v) {
    for (int u = 0; u < v; ++u, ++bit) {
      const int position = header + bit / 6;
      if (position >= static_cast<int>(values.size())) {
        throw std::runtime_error("truncated graph6 row");
      }
      if ((values[position] >> (5 - bit % 6)) & 1) {
        const int edge = static_cast<int>(graph.edges.size());
        graph.edges.push_back({u, v});
        graph.incident[u].push_back(edge);
        graph.incident[v].push_back(edge);
      }
    }
  }
  return graph;
}

string profile_key(vector<int> counts) {
  std::sort(counts.begin(), counts.end());
  std::ostringstream stream;
  for (int i = 0; i < static_cast<int>(counts.size()); ++i) {
    if (i) stream << "+";
    stream << counts[i];
  }
  return stream.str();
}

struct Factor {
  vector<vector<int>> circuits;
  vector<EdgeMask> masks;
  vector<int> circuit_of_edge;
};

struct CaseSummary {
  uint64_t colouring_index = 0;
  int common_colour = 0;
  uint64_t mark_sets = 0;
  uint64_t mark_sets_with_good = 0;
  uint64_t no_good_mark_sets = 0;
  uint64_t good_selectors = 0;
  int minimum_good = 257;
  int maximum_good = -1;
  map<int, uint64_t> good_count_histogram;
};

struct NoGoodWitness {
  bool present = false;
  uint64_t colouring_index = 0;
  int common_colour = 0;
  vector<int> colours;
  vector<int> marks;
  vector<vector<int>> factor_a;
  vector<vector<int>> factor_b;
};

struct Scan {
  const Graph& graph;
  const int m;
  vector<int> colour;
  vector<unsigned> used;
  uint64_t normalized_colourings = 0;
  uint64_t all_c10_colourings = 0;
  uint64_t selector_evaluations = 0;
  uint64_t mark_set_records = 0;
  uint64_t records_with_good = 0;
  uint64_t no_good_records = 0;
  uint64_t total_good_selectors = 0;
  map<int, uint64_t> permanent_histogram;
  map<int, uint64_t> good_count_histogram;
  map<string, uint64_t> profile_histogram;
  set<pair<uint64_t, uint64_t>> unique_mark_sets;
  vector<CaseSummary> cases;
  vector<string> c10_colour_words;
  NoGoodWitness first_no_good;

  explicit Scan(const Graph& input)
      : graph(input),
        m(static_cast<int>(input.edges.size())),
        colour(m, -1),
        used(input.n, 0) {
    if (m > MAX_EDGES) throw std::runtime_error("too many edges");
  }

  bool assign(int edge, int value) {
    if (colour[edge] != -1) return colour[edge] == value;
    const auto [u, v] = graph.edges[edge];
    const unsigned bit = 1U << value;
    if ((used[u] & bit) || (used[v] & bit)) return false;
    colour[edge] = value;
    used[u] |= bit;
    used[v] |= bit;
    return true;
  }

  void unassign(int edge, int value) {
    const auto [u, v] = graph.edges[edge];
    colour[edge] = -1;
    used[u] &= ~(1U << value);
    used[v] &= ~(1U << value);
  }

  Factor factor_omitting(int omitted) const {
    Factor factor;
    factor.circuit_of_edge.assign(m, -1);
    vector<char> seen(m, 0);
    for (int start = 0; start < m; ++start) {
      if (colour[start] == omitted || seen[start]) continue;
      const int index = static_cast<int>(factor.circuits.size());
      vector<int> stack = {start};
      vector<int> circuit;
      EdgeMask mask;
      seen[start] = 1;
      while (!stack.empty()) {
        const int edge = stack.back();
        stack.pop_back();
        circuit.push_back(edge);
        mask.set(edge);
        factor.circuit_of_edge[edge] = index;
        const auto [u, v] = graph.edges[edge];
        for (int vertex : {u, v}) {
          for (int other : graph.incident[vertex]) {
            if (colour[other] != omitted && !seen[other]) {
              seen[other] = 1;
              stack.push_back(other);
            }
          }
        }
      }
      std::sort(circuit.begin(), circuit.end());
      factor.circuits.push_back(circuit);
      factor.masks.push_back(mask);
    }
    return factor;
  }

  vector<int> marked_profile(const EdgeMask& cycle,
                             const vector<char>& marked) const {
    vector<char> seen(graph.n, 0);
    vector<int> answer;
    for (int root = 0; root < graph.n; ++root) {
      bool active = false;
      for (int edge : graph.incident[root]) active |= cycle.test(edge);
      if (!active || seen[root]) continue;
      vector<int> stack = {root};
      seen[root] = 1;
      int twice_marks = 0;
      while (!stack.empty()) {
        const int vertex = stack.back();
        stack.pop_back();
        for (int edge : graph.incident[vertex]) {
          if (!cycle.test(edge)) continue;
          if (marked[edge]) ++twice_marks;
          const auto [u, v] = graph.edges[edge];
          const int other = u ^ v ^ vertex;
          if (!seen[other]) {
            seen[other] = 1;
            stack.push_back(other);
          }
        }
      }
      const int marks = twice_marks / 2;
      if (marks) answer.push_back(marks);
    }
    std::sort(answer.begin(), answer.end());
    return answer;
  }

  int evaluate_mark_set(const vector<int>& marks,
                        const Factor& factor_a,
                        const Factor& factor_b) {
    vector<int> b_for_a(8, -1);
    vector<int> mark_for_a(8, -1);
    vector<char> marked(m, 0);
    for (int edge : marks) {
      const int a = factor_a.circuit_of_edge[edge];
      const int b = factor_b.circuit_of_edge[edge];
      if (a < 0 || b < 0 || a >= 8 || b >= 8) {
        throw std::runtime_error("mark not in both factors");
      }
      if (b_for_a[a] != -1) throw std::runtime_error("two marks in A factor");
      b_for_a[a] = b;
      mark_for_a[a] = edge;
      marked[edge] = 1;
    }
    vector<char> used_b(8, 0);
    for (int a = 0; a < 8; ++a) {
      if (b_for_a[a] < 0 || used_b[b_for_a[a]]) {
        throw std::runtime_error("marks are not a perfect transversal");
      }
      used_b[b_for_a[a]] = 1;
    }

    int good = 0;
    for (int selector = 0; selector < 256; ++selector) {
      EdgeMask cycle;
      for (int a = 0; a < 8; ++a) {
        if ((selector >> a) & 1) {
          cycle ^= factor_a.masks[a];
        } else {
          cycle ^= factor_b.masks[b_for_a[a]];
        }
      }
      const vector<int> profile = marked_profile(cycle, marked);
      int sum = 0;
      bool even = true;
      for (int count : profile) {
        sum += count;
        even &= (count % 2 == 0);
      }
      if (sum != 8) throw std::runtime_error("selector loses a mark");
      ++profile_histogram[profile_key(profile)];
      if (even) ++good;
      ++selector_evaluations;
    }
    return good;
  }

  void enumerate_perfect_matchings(
      int a,
      uint16_t used_b,
      vector<int>& marks,
      const vector<vector<int>>& c_edges_by_a,
      const Factor& factor_a,
      const Factor& factor_b,
      CaseSummary& summary) {
    if (a == 8) {
      ++summary.mark_sets;
      ++mark_set_records;
      uint64_t low = 0;
      uint64_t high = 0;
      for (int edge : marks) {
        if (edge < 64) low |= uint64_t{1} << edge;
        else high |= uint64_t{1} << (edge - 64);
      }
      unique_mark_sets.insert({low, high});
      const int good = evaluate_mark_set(marks, factor_a, factor_b);
      summary.good_selectors += good;
      summary.minimum_good = std::min(summary.minimum_good, good);
      summary.maximum_good = std::max(summary.maximum_good, good);
      ++summary.good_count_histogram[good];
      ++good_count_histogram[good];
      total_good_selectors += good;
      if (good) {
        ++summary.mark_sets_with_good;
        ++records_with_good;
      } else {
        ++summary.no_good_mark_sets;
        ++no_good_records;
        if (!first_no_good.present) {
          first_no_good.present = true;
          first_no_good.colouring_index = summary.colouring_index;
          first_no_good.common_colour = summary.common_colour;
          first_no_good.colours = colour;
          first_no_good.marks = marks;
          first_no_good.factor_a = factor_a.circuits;
          first_no_good.factor_b = factor_b.circuits;
        }
      }
      return;
    }
    for (int edge : c_edges_by_a[a]) {
      const int b = factor_b.circuit_of_edge[edge];
      if ((used_b >> b) & 1U) continue;
      marks.push_back(edge);
      enumerate_perfect_matchings(
          a + 1, used_b | (uint16_t{1} << b), marks,
          c_edges_by_a, factor_a, factor_b, summary);
      marks.pop_back();
    }
  }

  void record() {
    ++normalized_colourings;
    array<Factor, 3> factors = {
        factor_omitting(0), factor_omitting(1), factor_omitting(2)};
    bool all_c10 = true;
    for (const Factor& factor : factors) {
      all_c10 &= factor.circuits.size() == 8;
      for (const auto& circuit : factor.circuits) {
        all_c10 &= circuit.size() == 10;
      }
    }
    if (!all_c10) return;
    ++all_c10_colourings;
    string word;
    for (int value : colour) word.push_back(static_cast<char>('0' + value));
    c10_colour_words.push_back(word);

    for (int common = 0; common < 3; ++common) {
      const int first_other = (common + 1) % 3;
      const int second_other = (common + 2) % 3;
      const Factor& factor_a = factors[second_other];
      const Factor& factor_b = factors[first_other];
      vector<vector<int>> c_edges_by_a(8);
      for (int edge = 0; edge < m; ++edge) {
        if (colour[edge] != common) continue;
        const int a = factor_a.circuit_of_edge[edge];
        const int b = factor_b.circuit_of_edge[edge];
        if (a < 0 || b < 0) throw std::runtime_error("bad common edge");
        c_edges_by_a[a].push_back(edge);
      }
      if (!std::all_of(c_edges_by_a.begin(), c_edges_by_a.end(),
                       [](const vector<int>& row) { return row.size() == 5; })) {
        throw std::runtime_error("incidence row is not degree five");
      }
      CaseSummary summary;
      summary.colouring_index = normalized_colourings;
      summary.common_colour = common;
      vector<int> marks;
      enumerate_perfect_matchings(
          0, 0, marks, c_edges_by_a, factor_a, factor_b, summary);
      if (summary.mark_sets == 0) throw std::runtime_error("no transversal");
      ++permanent_histogram[static_cast<int>(summary.mark_sets)];
      cases.push_back(summary);
    }
  }

  void recurse(int assigned) {
    if (assigned == m) {
      record();
      return;
    }
    int best = -1;
    unsigned choices = 0;
    int best_count = 4;
    for (int edge = 0; edge < m; ++edge) {
      if (colour[edge] != -1) continue;
      const auto [u, v] = graph.edges[edge];
      const unsigned allowed = 7U & ~(used[u] | used[v]);
      const int count = __builtin_popcount(allowed);
      if (!count) return;
      if (count < best_count) {
        best = edge;
        choices = allowed;
        best_count = count;
        if (count == 1) break;
      }
    }
    for (int value = 0; value < 3; ++value) {
      if (!((choices >> value) & 1U)) continue;
      if (assign(best, value)) {
        recurse(assigned + 1);
        unassign(best, value);
      }
    }
  }

  void run() {
    if (graph.n != 80 || m != 120) {
      throw std::runtime_error("expected an order-80 cubic graph");
    }
    for (const auto& row : graph.incident) {
      if (row.size() != 3) throw std::runtime_error("graph is not cubic");
    }
    int assigned = 0;
    for (int value = 0; value < 3; ++value) {
      const int edge = graph.incident[0][value];
      if (!assign(edge, value)) throw std::runtime_error("normalization failed");
      ++assigned;
    }
    recurse(assigned);
  }
};

template <typename K>
void print_histogram(const map<K, uint64_t>& histogram) {
  cout << "{";
  bool first = true;
  for (const auto& [key, count] : histogram) {
    if (!first) cout << ",";
    first = false;
    cout << "\"" << key << "\":" << count;
  }
  cout << "}";
}

void print_int_vector(const vector<int>& row) {
  cout << "[";
  for (int i = 0; i < static_cast<int>(row.size()); ++i) {
    if (i) cout << ",";
    cout << row[i];
  }
  cout << "]";
}

void print_circuit_rows(const vector<vector<int>>& rows) {
  cout << "[";
  for (int i = 0; i < static_cast<int>(rows.size()); ++i) {
    if (i) cout << ",";
    print_int_vector(rows[i]);
  }
  cout << "]";
}

}  // namespace

int main() {
  try {
    string row;
    if (!std::getline(cin, row)) throw std::runtime_error("missing graph6 input");
    const Graph graph = parse_graph6(row);
    Scan scan(graph);
    scan.run();

    cout << "{\n";
    cout << "\"schema\":\"order80-c10-selector-scan-v1\",\n";
    cout << "\"graph6\":\"" << row << "\",\n";
    cout << "\"vertices\":" << graph.n << ",\"edges\":" << graph.edges.size() << ",\n";
    cout << "\"normalized_tait_colourings\":" << scan.normalized_colourings << ",\n";
    cout << "\"all_three_c10_colourings\":" << scan.all_c10_colourings << ",\n";
    cout << "\"common_colour_cases\":" << scan.cases.size() << ",\n";
    cout << "\"mark_set_records\":" << scan.mark_set_records << ",\n";
    cout << "\"unique_edge_mark_sets\":" << scan.unique_mark_sets.size() << ",\n";
    cout << "\"selector_evaluations\":" << scan.selector_evaluations << ",\n";
    cout << "\"records_with_good_selector\":" << scan.records_with_good << ",\n";
    cout << "\"no_good_selector_records\":" << scan.no_good_records << ",\n";
    cout << "\"total_good_selectors\":" << scan.total_good_selectors << ",\n";
    cout << "\"permanent_histogram\":";
    print_histogram(scan.permanent_histogram);
    cout << ",\n\"good_selector_count_histogram\":";
    print_histogram(scan.good_count_histogram);
    cout << ",\n\"marked_component_profile_histogram\":";
    print_histogram(scan.profile_histogram);
    cout << ",\n\"all_c10_colour_words\":[";
    for (int i = 0; i < static_cast<int>(scan.c10_colour_words.size()); ++i) {
      if (i) cout << ",";
      cout << "\"" << scan.c10_colour_words[i] << "\"";
    }
    cout << "],\n\"cases\":[";
    for (int i = 0; i < static_cast<int>(scan.cases.size()); ++i) {
      if (i) cout << ",";
      const CaseSummary& item = scan.cases[i];
      cout << "{\"colouring_index\":" << item.colouring_index
           << ",\"common_colour\":" << item.common_colour
           << ",\"mark_sets\":" << item.mark_sets
           << ",\"mark_sets_with_good\":" << item.mark_sets_with_good
           << ",\"no_good_mark_sets\":" << item.no_good_mark_sets
           << ",\"good_selectors\":" << item.good_selectors
           << ",\"minimum_good\":" << item.minimum_good
           << ",\"maximum_good\":" << item.maximum_good
           << ",\"good_count_histogram\":";
      print_histogram(item.good_count_histogram);
      cout << "}";
    }
    cout << "],\n\"first_no_good\":";
    if (!scan.first_no_good.present) {
      cout << "null";
    } else {
      const NoGoodWitness& witness = scan.first_no_good;
      cout << "{\"colouring_index\":" << witness.colouring_index
           << ",\"common_colour\":" << witness.common_colour
           << ",\"colours_by_edge\":";
      print_int_vector(witness.colours);
      cout << ",\"marks\":";
      print_int_vector(witness.marks);
      cout << ",\"mark_edges\":[";
      for (int i = 0; i < static_cast<int>(witness.marks.size()); ++i) {
        if (i) cout << ",";
        const auto [u, v] = graph.edges[witness.marks[i]];
        cout << "[" << u << "," << v << "]";
      }
      cout << "],\"factor_a\":";
      print_circuit_rows(witness.factor_a);
      cout << ",\"factor_b\":";
      print_circuit_rows(witness.factor_b);
      cout << "}";
    }
    cout << "\n}\n";
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << "\n";
    return 2;
  }
  return 0;
}
