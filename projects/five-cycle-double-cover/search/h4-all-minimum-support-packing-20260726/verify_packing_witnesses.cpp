#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <regex>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

static std::vector<std::pair<int, int>> load_graph(const std::string &path) {
  std::ifstream source(path);
  std::stringstream buffer;
  buffer << source.rdbuf();
  const std::string document = buffer.str();
  const std::regex edge_pattern(
      R"("id":\s*([0-9]+),\s*"u":\s*([0-9]+),\s*"v":\s*([0-9]+))");
  std::vector<std::pair<int, int>> result;
  for (std::sregex_iterator cursor(document.begin(), document.end(),
                                  edge_pattern),
       end;
       cursor != end; ++cursor) {
    const int identifier = std::stoi((*cursor)[1]);
    if (identifier != static_cast<int>(result.size()))
      throw std::runtime_error("nonconsecutive graph edge identifiers");
    result.emplace_back(std::stoi((*cursor)[2]), std::stoi((*cursor)[3]));
  }
  return result;
}

static bool connected_after_edge_deletion(
    int vertices, const std::vector<std::pair<int, int>> &edges,
    int deleted) {
  std::vector<std::vector<std::pair<int, int>>> adjacency(vertices);
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    auto [first, second] = edges[edge];
    adjacency[first].push_back({second, edge});
    adjacency[second].push_back({first, edge});
  }
  std::vector<unsigned char> seen(vertices);
  std::vector<int> stack{0};
  seen[0] = 1;
  while (!stack.empty()) {
    const int vertex = stack.back();
    stack.pop_back();
    for (auto [neighbour, edge] : adjacency[vertex]) {
      if (edge == deleted || seen[neighbour]) continue;
      seen[neighbour] = 1;
      stack.push_back(neighbour);
    }
  }
  return std::all_of(seen.begin(), seen.end(),
                     [](unsigned char value) { return value != 0; });
}

static void audit_graph(
    int vertices, const std::vector<std::pair<int, int>> &edges) {
  if (vertices != 162 || edges.size() != 243)
    throw std::runtime_error("unexpected H4 dimensions");
  std::vector<int> degree(vertices);
  std::unordered_set<std::uint32_t> edge_set;
  for (auto [first, second] : edges) {
    if (first < 0 || second < 0 || first >= vertices || second >= vertices ||
        first == second)
      throw std::runtime_error("invalid graph edge");
    ++degree[first];
    ++degree[second];
    const int low = std::min(first, second);
    const int high = std::max(first, second);
    if (!edge_set.insert(low | (high << 8)).second)
      throw std::runtime_error("parallel graph edge");
  }
  if (std::any_of(degree.begin(), degree.end(),
                  [](int value) { return value != 3; }))
    throw std::runtime_error("graph is not cubic");
  if (!connected_after_edge_deletion(vertices, edges, -1))
    throw std::runtime_error("graph is disconnected");
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    if (!connected_after_edge_deletion(vertices, edges, edge))
      throw std::runtime_error("graph has a bridge");
  }
}

static std::array<int, 4> read_support(
    const std::string &line, std::uint64_t row) {
  std::istringstream fields(line);
  std::array<int, 4> support{};
  for (int &edge : support) {
    if (!(fields >> edge))
      throw std::runtime_error("short support row " + std::to_string(row));
  }
  int extra;
  if (fields >> extra)
    throw std::runtime_error("long support row " + std::to_string(row));
  if (!(support[0] < support[1] && support[1] < support[2] &&
        support[2] < support[3]))
    throw std::runtime_error("noncanonical support row " +
                             std::to_string(row));
  return support;
}

static bool bit(const std::array<unsigned char, 31> &record, int edge) {
  return (record[edge >> 3] >> (edge & 7)) & 1u;
}

static void audit_record(
    int vertices, const std::vector<std::pair<int, int>> &edges,
    const std::array<int, 4> &support,
    const std::array<unsigned char, 31> &record, std::uint64_t row) {
  if (record.back() & 0xf8u)
    throw std::runtime_error("nonzero witness padding at row " +
                             std::to_string(row));
  std::vector<unsigned char> terminal(vertices);
  for (int edge : support) {
    if (edge < 0 || edge >= static_cast<int>(edges.size()))
      throw std::runtime_error("out-of-range support at row " +
                               std::to_string(row));
    if (bit(record, edge))
      throw std::runtime_error("witness intersects support at row " +
                               std::to_string(row));
    auto [first, second] = edges[edge];
    if (terminal[first] || terminal[second])
      throw std::runtime_error("support is not a matching at row " +
                               std::to_string(row));
    terminal[first] = terminal[second] = 1;
  }

  std::vector<std::vector<int>> cycle(vertices);
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    if (!bit(record, edge)) continue;
    auto [first, second] = edges[edge];
    cycle[first].push_back(second);
    cycle[second].push_back(first);
  }
  for (int vertex = 0; vertex < vertices; ++vertex) {
    const std::size_t degree = cycle[vertex].size();
    const bool valid =
        terminal[vertex] ? degree == 2 : degree == 0 || degree == 2;
    if (!valid)
      throw std::runtime_error("invalid cycle degree at row " +
                               std::to_string(row));
  }

  std::vector<unsigned char> reached(vertices);
  for (int root = 0; root < vertices; ++root) {
    if (reached[root] || cycle[root].empty()) continue;
    int marked = 0;
    std::queue<int> frontier;
    frontier.push(root);
    reached[root] = 1;
    while (!frontier.empty()) {
      const int vertex = frontier.front();
      frontier.pop();
      marked += terminal[vertex] != 0;
      for (int neighbour : cycle[vertex]) {
        if (reached[neighbour]) continue;
        reached[neighbour] = 1;
        frontier.push(neighbour);
      }
    }
    if (marked & 1)
      throw std::runtime_error("odd-marked witness circuit at row " +
                               std::to_string(row));
  }
}

int main(int argc, char **argv) {
  if (argc != 5) {
    std::cerr << "usage: verify graph.json vertices supports witnesses.bin\n";
    return 2;
  }
  const auto edges = load_graph(argv[1]);
  const int vertices = std::stoi(argv[2]);
  audit_graph(vertices, edges);

  std::ifstream supports(argv[3]);
  std::ifstream witnesses(argv[4], std::ios::binary);
  std::unordered_set<std::uint32_t> distinct;
  distinct.reserve(5000000);
  std::string line;
  std::uint64_t rows = 0;
  while (std::getline(supports, line)) {
    ++rows;
    const auto support = read_support(line, rows);
    const std::uint32_t key =
        static_cast<std::uint32_t>(support[0]) |
        (static_cast<std::uint32_t>(support[1]) << 8) |
        (static_cast<std::uint32_t>(support[2]) << 16) |
        (static_cast<std::uint32_t>(support[3]) << 24);
    if (!distinct.insert(key).second)
      throw std::runtime_error("duplicate support row " +
                               std::to_string(rows));
    std::array<unsigned char, 31> record{};
    witnesses.read(reinterpret_cast<char *>(record.data()), record.size());
    if (witnesses.gcount() != static_cast<std::streamsize>(record.size()))
      throw std::runtime_error("short witness file at row " +
                               std::to_string(rows));
    audit_record(vertices, edges, support, record, rows);
    if (rows % 100000 == 0)
      std::cerr << "verified " << rows << '\n';
  }
  char extra;
  if (witnesses.get(extra))
    throw std::runtime_error("witness file has trailing bytes");
  if (rows != 4931430)
    throw std::runtime_error("unexpected support count " +
                             std::to_string(rows));
  std::cout << "VERIFIED rows " << rows
            << " distinct " << distinct.size()
            << " packing_witnesses " << rows << '\n';
}
