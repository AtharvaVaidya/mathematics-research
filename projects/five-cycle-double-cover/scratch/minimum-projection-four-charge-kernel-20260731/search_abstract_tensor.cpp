#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <limits>
#include <random>
#include <vector>

namespace {

using Map = std::array<unsigned char, 4>;

constexpr std::array<Map, 6> maps{{
    {{0, 1, 2, 3}}, {{0, 1, 3, 2}}, {{0, 2, 1, 3}},
    {{0, 2, 3, 1}}, {{0, 3, 1, 2}}, {{0, 3, 2, 1}},
}};

Map compose(const Map& left, const Map& right) {
  Map result{};
  for (int value = 0; value < 4; ++value) {
    result[value] = left[right[value]];
  }
  return result;
}

int index_of(const Map& map) {
  for (int index = 0; index < 6; ++index) {
    if (maps[index] == map) return index;
  }
  std::abort();
}

unsigned matrix_mask(const Map& map) {
  return (map[1] & 1) | ((map[1] >> 1 & 1) << 1)
      | ((map[2] & 1) << 2) | ((map[2] >> 1 & 1) << 3);
}

int alternating(int left, int right) {
  return ((left & 1) & (right >> 1 & 1))
      ^ ((left >> 1 & 1) & (right & 1));
}

struct Configuration {
  std::vector<unsigned char> relative;
  unsigned allowed_degrees = 0;
};

struct Search {
  explicit Search(int vertices) : vertices(vertices) {
    for (int left = 0; left < vertices; ++left) {
      for (int right = left + 1; right < vertices; ++right) {
        endpoints.push_back({left, right});
      }
    }
    std::array<int, 6> inverse{};
    for (int left = 0; left < 6; ++left) {
      for (int right = 0; right < 6; ++right) {
        if (compose(maps[left], maps[right]) == maps[0]
            && compose(maps[right], maps[left]) == maps[0]) {
          inverse[left] = right;
        }
      }
    }
    std::vector<int> spin(vertices);
    spin[0] = 0;
    auto generate = [&](auto&& self, int vertex) -> void {
      if (vertex == vertices) {
        int charge = 0;
        for (int marked = 0; marked < 4; ++marked) {
          charge ^= maps[spin[marked]][1];
        }
        if (charge) return;
        Configuration configuration;
        for (auto [left, right] : endpoints) {
          configuration.relative.push_back(matrix_mask(compose(
              maps[inverse[spin[left]]], maps[spin[right]])));
        }
        for (int translation = 0; translation < 4; ++translation) {
          int degree = 0;
          for (int marked = 0; marked < 4; ++marked) {
            degree |= alternating(
                translation, maps[spin[marked]][1]) << marked;
          }
          configuration.allowed_degrees |= 1u << degree;
        }
        configurations.push_back(std::move(configuration));
        return;
      }
      for (int value = 0; value < 6; ++value) {
        spin[vertex] = value;
        self(self, vertex + 1);
      }
    };
    generate(generate, 1);
  }

  int score(const std::vector<unsigned char>& tensor) const {
    int result = 0;
    for (const Configuration& configuration : configurations) {
      int degree = 0;
      for (std::size_t edge = 0; edge < endpoints.size(); ++edge) {
        if (std::popcount(
                static_cast<unsigned>(tensor[edge]
                                      & configuration.relative[edge]))
            & 1) {
          degree ^= (1 << endpoints[edge][0]) | (1 << endpoints[edge][1]);
        }
      }
      result += (configuration.allowed_degrees >> degree) & 1;
    }
    return result;
  }

  int vertices;
  std::vector<std::array<int, 2>> endpoints;
  std::vector<Configuration> configurations;
};

}  // namespace

int main(int argc, char** argv) {
  int vertices = argc > 1 ? std::stoi(argv[1]) : 5;
  int restarts = argc > 2 ? std::stoi(argv[2]) : 10000;
  if (vertices < 4 || vertices > 8) return 2;
  Search search(vertices);
  std::cerr << "vertices=" << vertices
            << " edges=" << search.endpoints.size()
            << " feasible_map_gauges=" << search.configurations.size()
            << "\n";
  std::mt19937_64 random(0x4c4841524745ULL + vertices);
  int global_best = std::numeric_limits<int>::max();
  std::vector<unsigned char> best;
  for (int restart = 0; restart < restarts; ++restart) {
    std::vector<unsigned char> tensor(search.endpoints.size());
    for (auto& mask : tensor) mask = random() & 15;
    int current = search.score(tensor);
    bool changed = true;
    while (changed) {
      changed = false;
      int next_score = current, next_edge = -1, next_bit = -1;
      for (std::size_t edge = 0; edge < tensor.size(); ++edge) {
        for (int bit = 0; bit < 4; ++bit) {
          tensor[edge] ^= 1 << bit;
          int candidate = search.score(tensor);
          tensor[edge] ^= 1 << bit;
          if (candidate < next_score) {
            next_score = candidate;
            next_edge = edge;
            next_bit = bit;
          }
        }
      }
      if (next_edge >= 0) {
        tensor[next_edge] ^= 1 << next_bit;
        current = next_score;
        changed = true;
      }
    }
    if (current < global_best) {
      global_best = current;
      best = tensor;
      std::cout << "best=" << global_best << " masks=";
      for (auto mask : best) std::cout << ' ' << int(mask);
      std::cout << '\n';
    }
    if (!global_best) return 1;
  }
  return 0;
}
