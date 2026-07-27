#define main rooted_three_pole_csp_original_main
#include "rooted_three_pole_csp.cpp"
#undef main

#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>

struct BasePairDecision {
  int category = -1;  // 0 empty, 1 contains a base pair, 2 violation
  unsigned queried = 0;
  unsigned observed = 0;
  std::uint64_t calls = 0;
};

BasePairDecision screen_root_csp(const RootedCsp& solver, int root) {
  const auto values = d_values();
  std::array<int, 7> decision{};
  decision.fill(-1);
  BasePairDecision result;

  auto query = [&](int orbit) {
    if (decision[orbit] >= 0) {
      return decision[orbit];
    }
    int answer = -1;
    for (int label = 0; label < 10; ++label) {
      if (root_orbit(values[label]) != orbit) {
        continue;
      }
      const int current = solver.solve(root, label) ? 1 : 0;
      ++result.calls;
      if (answer >= 0 && answer != current) {
        throw std::runtime_error("stabilizer orbit decisions disagree");
      }
      answer = current;
    }
    if (answer < 0) {
      throw std::runtime_error("empty stabilizer orbit");
    }
    decision[orbit] = answer;
    result.queried |= 1U << orbit;
    if (answer) {
      result.observed |= 1U << orbit;
    }
    return answer;
  };

  constexpr std::array<std::array<int, 2>, 3> pairs = {
      std::array<int, 2>{2, 3},
      std::array<int, 2>{1, 4},
      std::array<int, 2>{0, 5},
  };
  for (const auto& pair : pairs) {
    if (query(pair[0]) && query(pair[1])) {
      result.category = 1;
      return result;
    }
  }
  for (int orbit = 0; orbit < 7; ++orbit) {
    query(orbit);
  }
  result.category = result.observed == 0 ? 0 : 2;
  return result;
}

int main(int argc, char** argv) {
  bool transcript = false;
  bool fail_on_violation = false;
  if (argc == 2 && std::string(argv[1]) == "--transcript") {
    transcript = true;
  } else if (argc == 2 && std::string(argv[1]) == "--fail-on-violation") {
    fail_on_violation = true;
  } else if (argc == 3) {
    transcript = std::string(argv[1]) == "--transcript" ||
                 std::string(argv[2]) == "--transcript";
    fail_on_violation =
        std::string(argv[1]) == "--fail-on-violation" ||
        std::string(argv[2]) == "--fail-on-violation";
    if (!transcript || !fail_on_violation) {
      std::cerr << "unrecognized option\n";
      return 2;
    }
  } else if (argc != 1) {
    std::cerr << "usage: rooted_base_pair_screen_csp "
                 "[--transcript] [--fail-on-violation]\n";
    return 2;
  }

  std::uint64_t graphs = 0;
  std::uint64_t nonbridge_roots = 0;
  std::uint64_t empty = 0;
  std::uint64_t closed = 0;
  std::uint64_t violations = 0;
  std::uint64_t calls = 0;
  std::string record;
  while (std::getline(std::cin, record)) {
    if (record.empty()) {
      continue;
    }
    try {
      const Graph graph = parse_graph6(record);
      const RootedCsp solver(graph);
      ++graphs;
      for (int root = 0; root < static_cast<int>(graph.edges.size()); ++root) {
        if (is_bridge(graph, root)) {
          continue;
        }
        ++nonbridge_roots;
        const auto decision = screen_root_csp(solver, root);
        calls += decision.calls;
        empty += decision.category == 0;
        closed += decision.category == 1;
        violations += decision.category == 2;
        if (transcript) {
          std::cout << record << '\t' << root << '\t' << decision.category
                    << '\t' << std::hex << decision.queried << '\t'
                    << decision.observed << std::dec << '\n';
        } else if (decision.category == 2) {
          std::cout << record << '\t' << root << '\t' << std::hex
                    << decision.observed << std::dec << '\n';
        }
      }
    } catch (const std::exception& error) {
      std::cerr << "ERROR record=" << record << " message=" << error.what()
                << '\n';
      return 3;
    }
  }
  std::cerr << "SUMMARY implementation=csp graphs=" << graphs
            << " nonbridge_roots=" << nonbridge_roots
            << " empty=" << empty << " closed=" << closed
            << " violations=" << violations << " calls=" << calls << '\n';
  return fail_on_violation && violations ? 4 : 0;
}
