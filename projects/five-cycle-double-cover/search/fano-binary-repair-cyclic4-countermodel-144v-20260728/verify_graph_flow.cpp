#include <algorithm>
#include <fstream>
#include <iostream>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

struct Edge { int u, v; };
struct Graph {
  int n;
  std::vector<Edge> edges;
  std::vector<int> flow;
  std::vector<std::vector<int>> incidence;
};

static void require(bool condition, const std::string& message) {
  if (!condition) throw std::runtime_error(message);
}

static std::pair<int,std::vector<Edge>> decode_graph6(const std::string& text) {
  require(text.size() >= 4 && text[0] == '~' && text[1] != '~',
          "expected medium graph6");
  int n = 0;
  for (int index = 1; index < 4; ++index)
    n = (n << 6) | (static_cast<unsigned char>(text[index])-63);
  std::vector<int> bits;
  for (std::size_t index = 4; index < text.size(); ++index) {
    const int value = static_cast<unsigned char>(text[index])-63;
    require(0 <= value && value < 64, "invalid graph6 payload");
    for (int shift = 5; shift >= 0; --shift)
      bits.push_back((value >> shift)&1);
  }
  std::vector<Edge> edges;
  int cursor = 0;
  for (int v = 1; v < n; ++v)
    for (int u = 0; u < v; ++u)
      if (bits.at(cursor++)) edges.push_back({u,v});
  while (cursor < static_cast<int>(bits.size()))
    require(!bits[cursor++], "nonzero graph6 padding");
  return {n,edges};
}

static Graph read_graph(const std::string& path) {
  std::ifstream input(path);
  require(input.good(), "cannot open state");
  std::string record, flow_line;
  require(static_cast<bool>(std::getline(input,record)), "missing graph6");
  require(static_cast<bool>(std::getline(input,flow_line)), "missing flow");
  std::vector<int> flow;
  std::size_t start = 0;
  while (start <= flow_line.size()) {
    const std::size_t comma = flow_line.find(',',start);
    flow.push_back(std::stoi(flow_line.substr(start,comma-start)));
    if (comma == std::string::npos) break;
    start = comma+1;
  }
  auto [n,edges] = decode_graph6(record);
  require(edges.size() == flow.size(), "flow length differs");
  Graph graph{n,edges,flow,std::vector<std::vector<int>>(n)};
  std::set<std::pair<int,int>> seen;
  for (int edge = 0; edge < static_cast<int>(edges.size()); ++edge) {
    auto [u,v] = edges[edge];
    require(u != v, "loop");
    require(seen.insert({std::min(u,v),std::max(u,v)}).second,
            "parallel edge");
    graph.incidence[u].push_back(edge);
    graph.incidence[v].push_back(edge);
  }
  return graph;
}

struct Components { int count, cyclic; };

static Components components_after(
    const Graph& graph, int a = -1, int b = -1, int c = -1
) {
  std::vector<char> seen(graph.n,0);
  Components result{0,0};
  for (int root = 0; root < graph.n; ++root) {
    if (seen[root]) continue;
    ++result.count;
    seen[root] = 1;
    std::vector<int> queue{root};
    int degree_sum = 0;
    for (std::size_t cursor = 0; cursor < queue.size(); ++cursor) {
      const int vertex = queue[cursor];
      for (int edge : graph.incidence[vertex]) {
        if (edge == a || edge == b || edge == c) continue;
        ++degree_sum;
        const auto [u,v] = graph.edges[edge];
        const int other = u ^ v ^ vertex;
        if (!seen[other]) {
          seen[other] = 1;
          queue.push_back(other);
        }
      }
    }
    if (degree_sum/2 >= static_cast<int>(queue.size())) ++result.cyclic;
  }
  return result;
}

static int girth(const Graph& graph) {
  int answer = graph.n+1;
  for (int forbidden = 0;
       forbidden < static_cast<int>(graph.edges.size()); ++forbidden) {
    const auto [source,target] = graph.edges[forbidden];
    std::vector<int> distance(graph.n,-1);
    distance[source] = 0;
    std::queue<int> queue;
    queue.push(source);
    while (!queue.empty()) {
      const int vertex = queue.front();
      queue.pop();
      for (int edge : graph.incidence[vertex]) {
        if (edge == forbidden) continue;
        const auto [u,v] = graph.edges[edge];
        const int other = u ^ v ^ vertex;
        if (distance[other] < 0) {
          distance[other] = distance[vertex]+1;
          queue.push(other);
        }
      }
    }
    if (distance[target] >= 0) answer = std::min(answer,distance[target]+1);
  }
  return answer;
}

int main(int argc, char** argv) try {
  require(argc == 2, "usage: verify_graph_flow STATE");
  const Graph graph = read_graph(argv[1]);
  require(graph.n == 144 && graph.edges.size() == 216, "wrong order/size");
  require(std::all_of(
      graph.incidence.begin(),graph.incidence.end(),
      [](const auto& row){return row.size()==3;}), "not cubic");
  require(components_after(graph).count == 1, "disconnected");
  std::vector<int> class_sizes(8);
  for (int value : graph.flow) {
    require(1 <= value && value <= 7, "zero flow value");
    ++class_sizes[value];
  }
  for (const auto& row : graph.incidence)
    require((graph.flow[row[0]] ^ graph.flow[row[1]] ^ graph.flow[row[2]])==0,
            "flow conservation failure");
  long long cyclic1 = 0, cyclic2 = 0, cyclic3 = 0;
  for (int a = 0; a < static_cast<int>(graph.edges.size()); ++a) {
    const auto one = components_after(graph,a);
    require(one.count == 1, "bridge");
    cyclic1 += one.cyclic >= 2;
    for (int b = 0; b < a; ++b) {
      cyclic2 += components_after(graph,a,b).cyclic >= 2;
      for (int c = 0; c < b; ++c)
        cyclic3 += components_after(graph,a,b,c).cyclic >= 2;
    }
  }
  require(cyclic1 == 0 && cyclic2 == 0 && cyclic3 == 0,
          "cyclic cut below four");
  const int graph_girth = girth(graph);
  require(graph_girth == 5, "girth differs");
  std::cout << "status verified\norder 144\nedges 216\ngirth "
            << graph_girth << "\nclass_sizes";
  for (int value = 1; value <= 7; ++value)
    std::cout << ' ' << class_sizes[value];
  std::cout << "\nsimple true\ncubic true\nconnected true\nbridgeless true"
            << "\ncyclic_cut_count_1 0\ncyclic_cut_count_2 0"
            << "\ncyclic_cut_count_3 0\ncyclically4 true\n";
  return 0;
} catch (const std::exception& error) {
  std::cerr << "verification failed: " << error.what() << '\n';
  return 1;
}
