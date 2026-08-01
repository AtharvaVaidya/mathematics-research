#if defined(__clang__)
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wreturn-type"
#elif defined(__GNUC__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#endif
#define main fano_all_bad_projection_search_linear_main
#include "../fano_all_bad_projection_search_linear.cpp"
#undef main
#if defined(__clang__)
#pragma clang diagnostic pop
#elif defined(__GNUC__)
#pragma GCC diagnostic pop
#endif

std::string json_escape(const std::string &value) {
  std::string result;
  for (const char character : value) {
    if (character == '\\' || character == '"') result.push_back('\\');
    result.push_back(character);
  }
  return result;
}

bool projection_extendable(
    const Graph &graph,
    const std::vector<Mask> &cycles,
    const std::vector<Mask> &edge_coefficients,
    Mask projection,
    Mask all_edges,
    int dimension) {
  const Mask factor = all_edges ^ projection;
  const Mask rhs_one = Mask{1} << dimension;
  std::vector<Mask> equations;
  equations.reserve(graph.edges.size());
  for (const Mask first : cycles) {
    equations.clear();
    Mask missing = factor & ~first;
    while (missing) {
      const int edge = std::countr_zero(missing);
      missing &= missing - 1;
      equations.push_back(edge_coefficients[edge] | rhs_one);
    }
    if (consistent_system(equations, dimension)) return true;
  }
  return false;
}

int main(int argc, char **argv) {
  if (argc != 2) {
    std::cerr << "usage: minimum-projection-scan FILE.g6" << std::endl;
    return 1;
  }
  try {
    std::ifstream stream(argv[1]);
    if (!stream) throw std::runtime_error("cannot open input");
    std::string row;
    int row_index = 0;
    while (std::getline(stream, row)) {
      if (row.empty()) {
        ++row_index;
        continue;
      }
      const Graph graph = decode_graph6(row);
      const std::vector<Mask> basis = cycle_basis(graph);
      const std::vector<Mask> cycles = enumerate_cycles(basis);
      const Mask all_edges = (Mask{1} << graph.edges.size()) - 1;
      std::vector<Mask> edge_coefficients(graph.edges.size(), 0);
      for (int coordinate = 0;
           coordinate < static_cast<int>(basis.size());
           ++coordinate) {
        Mask support = basis[coordinate];
        while (support) {
          const int edge = std::countr_zero(support);
          support &= support - 1;
          edge_coefficients[edge] |= Mask{1} << coordinate;
        }
      }

      int minimum = -1;
      int extendable_count = 0;
      std::vector<Mask> bad;
      for (int weight = 1; weight <= static_cast<int>(graph.edges.size());
           ++weight) {
        for (const Mask projection : cycles) {
          if (std::popcount(projection) != weight) continue;
          if (!projection_extendable(
                  graph,
                  cycles,
                  edge_coefficients,
                  projection,
                  all_edges,
                  static_cast<int>(basis.size()))) {
            continue;
          }
          minimum = weight;
          ++extendable_count;
          if (!projection_clean(
                  graph,
                  basis,
                  cycles,
                  edge_coefficients,
                  projection,
                  all_edges)) {
            bad.push_back(projection);
          }
        }
        if (minimum >= 0) break;
      }
      std::cout << "{\"row\":" << row_index
                << ",\"graph6\":\"" << json_escape(row)
                << "\",\"minimum\":" << minimum
                << ",\"minimum_extendable\":" << extendable_count
                << ",\"bad_minimum\":" << bad.size()
                << ",\"bad_hex\":[";
      for (std::size_t index = 0; index < bad.size(); ++index) {
        if (index) std::cout << ',';
        std::cout << "\"0x" << std::hex << bad[index] << std::dec << "\"";
      }
      std::cout << "]}" << std::endl;
      ++row_index;
    }
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << std::endl;
    return 1;
  }
}
