#include <array>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

// Heuristic only: minimize the number of clean relative GL assignments
// for an arbitrary six-vertex tensor system.  A zero would be a candidate
// countermodel and must be checked by verify_tensor_frontier.py.

static constexpr int K = 6;
static constexpr int EDGE_COUNT = K * (K - 1) / 2;
static constexpr int SPIN_COUNT = 6 * 6 * 6 * 6 * 6;

using Map = std::array<unsigned char, 4>;
static const std::array<Map, 6> gl = {{
    {{0,1,2,3}}, {{0,1,3,2}}, {{0,2,1,3}},
    {{0,2,3,1}}, {{0,3,1,2}}, {{0,3,2,1}}
}};

Map compose(const Map &left, const Map &right) {
    Map result{};
    for (int value = 0; value < 4; ++value) result[value] = left[right[value]];
    return result;
}

int map_index(const Map &map) {
    for (int index = 0; index < 6; ++index) if (gl[index] == map) return index;
    std::abort();
}

unsigned matrix_mask(const Map &map) {
    return (map[1] & 1)
        | ((map[1] >> 1 & 1) << 1)
        | ((map[2] & 1) << 2)
        | ((map[2] >> 1 & 1) << 3);
}

int main(int argc, char **argv) {
    const int restarts = argc > 1 ? std::stoi(argv[1]) : 2000;
    std::array<int, 6> inverse{};
    for (int left = 0; left < 6; ++left) {
        for (int right = 0; right < 6; ++right) {
            if (compose(gl[left], gl[right]) == gl[0]
                && compose(gl[right], gl[left]) == gl[0]) {
                inverse[left] = right;
            }
        }
    }
    std::array<std::array<int, 2>, EDGE_COUNT> endpoints{};
    int edge = 0;
    for (int left = 0; left < K; ++left)
        for (int right = left + 1; right < K; ++right)
            endpoints[edge++] = {{left, right}};

    std::vector<std::array<unsigned char, EDGE_COUNT>> relative(SPIN_COUNT);
    int spin_index = 0;
    for (int a = 0; a < 6; ++a)
    for (int b = 0; b < 6; ++b)
    for (int c = 0; c < 6; ++c)
    for (int d = 0; d < 6; ++d)
    for (int e = 0; e < 6; ++e) {
        const std::array<int, K> spin = {{0,a,b,c,d,e}};
        for (int f = 0; f < EDGE_COUNT; ++f) {
            const int left = endpoints[f][0], right = endpoints[f][1];
            relative[spin_index][f] = matrix_mask(
                compose(gl[inverse[spin[left]]], gl[spin[right]])
            );
        }
        ++spin_index;
    }

    auto score = [&](const std::array<unsigned char, EDGE_COUNT> &tensor) {
        int clean = 0;
        for (int s = 0; s < SPIN_COUNT; ++s) {
            unsigned degree = 0;
            for (int f = 0; f < EDGE_COUNT; ++f) {
                const int value = __builtin_parity(
                    tensor[f] & relative[s][f]
                );
                if (value) {
                    degree ^= 1u << endpoints[f][0];
                    degree ^= 1u << endpoints[f][1];
                }
            }
            clean += degree == 0;
        }
        return clean;
    };

    std::mt19937_64 rng(0x51A6C017ULL);
    int global_best = SPIN_COUNT + 1;
    std::array<unsigned char, EDGE_COUNT> best_tensor{};
    for (int restart = 0; restart < restarts; ++restart) {
        std::array<unsigned char, EDGE_COUNT> tensor{};
        for (auto &mask : tensor) mask = rng() & 15;
        int current = score(tensor);
        bool improved = true;
        while (improved) {
            improved = false;
            int chosen_edge = -1, chosen_bit = -1, chosen_score = current;
            for (int f = 0; f < EDGE_COUNT; ++f) {
                for (int bit = 0; bit < 4; ++bit) {
                    tensor[f] ^= 1u << bit;
                    const int candidate = score(tensor);
                    tensor[f] ^= 1u << bit;
                    if (candidate < chosen_score) {
                        chosen_score = candidate;
                        chosen_edge = f;
                        chosen_bit = bit;
                    }
                }
            }
            if (chosen_edge >= 0) {
                tensor[chosen_edge] ^= 1u << chosen_bit;
                current = chosen_score;
                improved = true;
            }
        }
        if (current < global_best) {
            global_best = current;
            best_tensor = tensor;
            std::cout << "best clean relative assignments = " << global_best
                      << "\nmasks =";
            for (auto mask : best_tensor) std::cout << ' ' << int(mask);
            std::cout << '\n';
        }
        if (global_best == 0) return 1;
    }
    return 0;
}
