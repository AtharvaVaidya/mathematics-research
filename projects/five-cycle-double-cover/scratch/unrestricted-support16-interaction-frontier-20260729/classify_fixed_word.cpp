// Exact classifier for every charge-valid component partition of the
// support-16 word 01010123|01012302.
//
// This deliberately includes interaction loops and blocks of arbitrary
// even-xor size.  States already proved by the loopless two-occurrence
// theorem are counted separately and skipped from the new frontier.

#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <string>
#include <utility>
#include <vector>

static constexpr int N = 16;
static constexpr int CIRCUITS = 2;
using Values = std::array<unsigned char, N>;

static const std::array<int, CIRCUITS> OFFSET{0, 8};
static const std::array<int, CIRCUITS> LENGTH{8, 8};
static const std::string WORD_TEXT = "01010123|01012302";

static std::vector<std::array<unsigned char, 4>> make_gl() {
    std::vector<std::array<unsigned char, 4>> result;
    std::array<unsigned char, 3> row{1, 2, 3};
    do {
        result.push_back({0, row[0], row[1], row[2]});
    } while (std::next_permutation(row.begin(), row.end()));
    return result;
}

static const auto GL = make_gl();

static std::uint64_t fnv_byte(std::uint64_t hash, unsigned char byte) {
    hash ^= byte;
    return hash * 1099511628211ULL;
}

struct Counts {
    std::uint64_t charge_valid = 0;
    std::uint64_t covered_loopless_pairs = 0;
    std::uint64_t eligible = 0;
    std::uint64_t clean = 0;
    std::uint64_t delete_only = 0;
    std::uint64_t residual = 0;
    std::uint64_t initially_clean = 0;
    std::uint64_t searched_dirty = 0;
    std::uint64_t classified_hash = 1469598103934665603ULL;
    std::uint64_t residual_hash = 1469598103934665603ULL;
    // First index: loop-only, higher-only, both.  Second: clean,
    // delete-only, residual.
    std::array<std::array<std::uint64_t, 3>, 3> category_outcomes{};
};

class Classifier {
  public:
    Values word{};
    Values derivative{};
    Values owner{};
    int components = 0;
    Counts counts;
    std::string first_residual;
    std::array<std::uint64_t, 17> largest_block_histogram{};
    std::map<std::string, std::uint64_t> residual_profiles;

    Classifier() {
        const std::string flat = "0101012301012302";
        for (int i = 0; i < N; ++i) word[i] = flat[i] - '0';
        for (int circuit = 0; circuit < CIRCUITS; ++circuit) {
            for (int local = 0; local < LENGTH[circuit]; ++local) {
                const int current = OFFSET[circuit] + local;
                const int previous = OFFSET[circuit] +
                    (local + LENGTH[circuit] - 1) % LENGTH[circuit];
                derivative[current] = word[previous] ^ word[current];
                assert(derivative[current] != 0);
            }
        }
        assert(derivative_text() == "31111131|21113132");
    }

    std::string derivative_text() const {
        std::string answer;
        for (int i = 0; i < N; ++i) {
            if (i == 8) answer += "|";
            answer += char('0' + derivative[i]);
        }
        return answer;
    }

    std::string partition_key() const {
        std::string key;
        key.reserve(N);
        for (int i = 0; i < N; ++i) key += char('0' + owner[i]);
        return key;
    }

    bool is_old_loopless_two_occurrence() const {
        std::array<int, 8> size{};
        std::array<int, 8> circuit_mask{};
        for (int position = 0; position < N; ++position) {
            const int block = owner[position];
            ++size[block];
            circuit_mask[block] |= 1 << (position >= 8);
        }
        for (int block = 0; block < components; ++block) {
            if (size[block] != 2 || circuit_mask[block] != 3) return false;
        }
        return true;
    }

    bool clean_at_displayed_extension() const {
        std::array<std::array<unsigned char, 4>, 8> parity{};
        for (int circuit = 0; circuit < CIRCUITS; ++circuit) {
            const int offset = OFFSET[circuit];
            const int length = LENGTH[circuit];
            for (int local = 0; local < length; ++local) {
                const int edge = offset + local;
                const int successor = offset + (local + 1) % length;
                const int first = owner[edge];
                const int second = owner[successor];
                if (first == second) continue;
                parity[first][word[edge]] ^= 1;
                parity[second][word[edge]] ^= 1;
            }
        }
        for (int block = 0; block < components; ++block) {
            for (int colour = 0; colour < 4; ++colour) {
                if (parity[block][colour]) return false;
            }
        }
        return true;
    }

    std::pair<bool, bool> evaluate_maps(
        const std::array<int, 8>& map_index) const {
        Values transformed{}, base{};
        bool deletes = false;
        for (int position = 0; position < N; ++position) {
            transformed[position] =
                GL[map_index[owner[position]]][derivative[position]];
        }
        for (int circuit = 0; circuit < CIRCUITS; ++circuit) {
            unsigned char point = 0;
            unsigned char used = 0;
            for (int local = 0; local < LENGTH[circuit]; ++local) {
                const int position = OFFSET[circuit] + local;
                point ^= transformed[position];
                base[position] = point;
                used |= 1u << point;
            }
            assert(point == 0);
            deletes = deletes || used != 15;
        }

        for (int relative_shift = 0; relative_shift < 4;
             ++relative_shift) {
            std::array<std::array<unsigned char, 4>, 8> parity{};
            for (int circuit = 0; circuit < CIRCUITS; ++circuit) {
                const int shift = circuit == 0 ? 0 : relative_shift;
                for (int local = 0; local < LENGTH[circuit]; ++local) {
                    const int edge = OFFSET[circuit] + local;
                    const int successor = OFFSET[circuit] +
                        (local + 1) % LENGTH[circuit];
                    const int first = owner[edge];
                    const int second = owner[successor];
                    if (first == second) continue;
                    const int colour = base[edge] ^ shift;
                    parity[first][colour] ^= 1;
                    parity[second][colour] ^= 1;
                }
            }
            bool dirty = false;
            for (int block = 0; block < components; ++block) {
                for (int colour = 0; colour < 4; ++colour) {
                    dirty = dirty || parity[block][colour];
                }
            }
            if (!dirty) return {true, deletes};
        }
        return {false, deletes};
    }

    std::pair<bool, bool> search_maps() const {
        std::array<std::array<unsigned char, 6>, 8> contribution{};
        for (int block = 0; block < components; ++block) {
            for (int map = 0; map < 6; ++map) {
                int encoded = 0;
                for (int circuit = 0; circuit < CIRCUITS; ++circuit) {
                    int sum = 0;
                    for (int local = 0; local < LENGTH[circuit]; ++local) {
                        const int position = OFFSET[circuit] + local;
                        if (owner[position] == block) {
                            sum ^= GL[map][derivative[position]];
                        }
                    }
                    encoded |= sum << (2 * circuit);
                }
                contribution[block][map] = encoded;
            }
        }

        // reachable[i][z] says the maps on components i,... can xor to z.
        std::array<std::array<unsigned char, 16>, 9> reachable{};
        reachable[components][0] = 1;
        for (int block = components - 1; block >= 1; --block) {
            for (int tail = 0; tail < 16; ++tail) {
                if (!reachable[block + 1][tail]) continue;
                for (int map = 0; map < 6; ++map) {
                    reachable[block][tail ^ contribution[block][map]] = 1;
                }
            }
        }

        std::array<int, 8> maps{};
        bool deletion_seen = false;
        std::function<bool(int, int)> recurse = [&](int block, int closure) {
            if (!reachable[block][closure]) return false;
            if (block == components) {
                assert(closure == 0);
                const auto [clean, deletes] = evaluate_maps(maps);
                deletion_seen = deletion_seen || deletes;
                return clean;
            }
            for (int map = 0; map < 6; ++map) {
                maps[block] = map;
                if (recurse(block + 1,
                            closure ^ contribution[block][map])) {
                    return true;
                }
            }
            return false;
        };

        maps[0] = 0;  // common GL(2,2) normalization
        const bool clean = recurse(1, contribution[0][0]);
        return {clean, deletion_seen};
    }

    void record_hash(const std::string& key, const unsigned char category) {
        for (const unsigned char byte : key) {
            counts.classified_hash = fnv_byte(counts.classified_hash, byte);
        }
        counts.classified_hash = fnv_byte(counts.classified_hash, category);
        if (category == 2) {
            for (const unsigned char byte : key) {
                counts.residual_hash = fnv_byte(counts.residual_hash, byte);
            }
            counts.residual_hash = fnv_byte(counts.residual_hash, '\n');
        }
    }

    void classify_partition() {
        ++counts.charge_valid;
        if (is_old_loopless_two_occurrence()) {
            ++counts.covered_loopless_pairs;
            return;
        }
        ++counts.eligible;

        std::array<int, 8> sizes{};
        std::array<int, 8> circuit_mask{};
        for (int position = 0; position < N; ++position) {
            ++sizes[owner[position]];
            circuit_mask[owner[position]] |= 1 << (position >= 8);
        }
        int largest = 0;
        bool has_loop = false;
        bool has_higher = false;
        for (int block = 0; block < components; ++block) {
            largest = std::max(largest, sizes[block]);
            has_loop = has_loop ||
                (sizes[block] == 2 && circuit_mask[block] != 3);
            has_higher = has_higher || sizes[block] > 2;
        }
        assert(has_loop || has_higher);
        const int frontier_category =
            has_loop && has_higher ? 2 : (has_higher ? 1 : 0);
        ++largest_block_histogram[largest];

        const std::string key = partition_key();
        if (components == 1 || clean_at_displayed_extension()) {
            ++counts.clean;
            ++counts.initially_clean;
            ++counts.category_outcomes[frontier_category][0];
            record_hash(key, 0);
            return;
        }

        ++counts.searched_dirty;
        const auto [clean, deletes] = search_maps();
        if (clean) {
            ++counts.clean;
            ++counts.category_outcomes[frontier_category][0];
            record_hash(key, 0);
        } else if (deletes) {
            ++counts.delete_only;
            ++counts.category_outcomes[frontier_category][1];
            record_hash(key, 1);
        } else {
            ++counts.residual;
            ++counts.category_outcomes[frontier_category][2];
            record_hash(key, 2);
            std::vector<int> profile;
            for (int block = 0; block < components; ++block) {
                profile.push_back(sizes[block]);
            }
            std::sort(profile.begin(), profile.end(), std::greater<int>());
            std::string profile_text;
            for (const int size : profile) {
                if (!profile_text.empty()) profile_text += "+";
                profile_text += std::to_string(size);
            }
            ++residual_profiles[profile_text];
            if (first_residual.empty() || key < first_residual) {
                first_residual = key;
            }
            if (counts.residual <= 20) {
                std::cout << "RESIDUAL key=" << WORD_TEXT << "|"
                          << key << " profile=" << profile_text
                          << " matrix=";
                for (int block = 0; block < components; ++block) {
                    if (block) std::cout << ",";
                    int first_count = 0;
                    int second_count = 0;
                    for (int position = 0; position < 8; ++position) {
                        first_count += owner[position] == block;
                        second_count += owner[position + 8] == block;
                    }
                    std::cout << first_count << "/" << second_count;
                }
                std::cout << " interaction_loop=" << int(has_loop)
                          << " higher_occurrence=" << int(has_higher)
                          << "\n";
            }
        }

        if (counts.eligible % 1000000 == 0) {
            std::cerr << "PROGRESS eligible=" << counts.eligible
                      << " clean=" << counts.clean
                      << " delete_only=" << counts.delete_only
                      << " residual=" << counts.residual << "\n";
        }
    }

    void enumerate_partitions() {
        std::array<unsigned char, 1 << N> charge{};
        std::array<std::vector<std::uint16_t>, N> blocks;
        for (int mask = 1; mask < (1 << N); ++mask) {
            const int bit = __builtin_ctz(mask);
            charge[mask] = charge[mask ^ (1 << bit)] ^ derivative[bit];
            if (charge[mask] == 0) {
                blocks[__builtin_ctz(mask)].push_back(mask);
            }
        }
        std::function<void(std::uint16_t, int)> recurse =
            [&](const std::uint16_t remaining, const int block) {
                if (!remaining) {
                    components = block;
                    classify_partition();
                    return;
                }
                const int first = __builtin_ctz(remaining);
                for (const std::uint16_t selected : blocks[first]) {
                    if ((selected & remaining) != selected) continue;
                    std::uint16_t row = selected;
                    while (row) {
                        const int position = __builtin_ctz(row);
                        owner[position] = block;
                        row &= row - 1;
                    }
                    recurse(remaining ^ selected, block + 1);
                }
            };
        recurse(std::numeric_limits<std::uint16_t>::max(), 0);
    }
};

int main() {
    Classifier classifier;
    std::cout << "WORD word=" << WORD_TEXT
              << " derivative=" << classifier.derivative_text() << "\n";
    classifier.enumerate_partitions();
    const auto& c = classifier.counts;
    assert(c.charge_valid == 8046330);
    assert(c.covered_loopless_pairs == 0);
    assert(c.eligible == 8046330);
    assert(c.clean == 8041808);
    assert(c.delete_only == 4514);
    assert(c.residual == 8);
    assert(c.initially_clean == 845732);
    assert(c.searched_dirty == 7200598);
    assert(c.classified_hash == 17068633071306477955ULL);
    assert(c.residual_hash == 6039899158318007243ULL);
    assert((c.category_outcomes[0] ==
            std::array<std::uint64_t, 3>{2835, 0, 0}));
    assert((c.category_outcomes[1] ==
            std::array<std::uint64_t, 3>{3060801, 2872, 8}));
    assert((c.category_outcomes[2] ==
            std::array<std::uint64_t, 3>{4978172, 1642, 0}));
    assert(classifier.first_residual == "0001234000314200");
    assert(c.eligible + c.covered_loopless_pairs == c.charge_valid);
    assert(c.clean + c.delete_only + c.residual == c.eligible);
    std::cout << "RESULT"
              << " charge_valid=" << c.charge_valid
              << " covered_loopless_pairs=" << c.covered_loopless_pairs
              << " eligible=" << c.eligible
              << " clean=" << c.clean
              << " delete_only=" << c.delete_only
              << " residual=" << c.residual
              << " initially_clean=" << c.initially_clean
              << " searched_dirty=" << c.searched_dirty
              << " classified_fnv64=" << c.classified_hash
              << " residual_fnv64=" << c.residual_hash << "\n";
    std::cout << "FIRST_RESIDUAL key=" << WORD_TEXT << "|"
              << classifier.first_residual << "\n";
    std::cout << "LARGEST_BLOCK_HIST";
    for (int size = 2; size <= 16; ++size) {
        if (classifier.largest_block_histogram[size]) {
            std::cout << " size" << size << "="
                      << classifier.largest_block_histogram[size];
        }
    }
    std::cout << "\nRESIDUAL_PROFILES";
    for (const auto& [profile, count] : classifier.residual_profiles) {
        std::cout << " " << profile << "=" << count;
    }
    const std::array<std::string, 3> category_name{
        "loop_only", "higher_only", "loop_and_higher"};
    std::cout << "\nCATEGORY_OUTCOMES";
    for (int category = 0; category < 3; ++category) {
        std::cout << " " << category_name[category]
                  << "=" << c.category_outcomes[category][0]
                  << "/" << c.category_outcomes[category][1]
                  << "/" << c.category_outcomes[category][2];
    }
    std::cout << "\nPASS exact fixed-word unrestricted census\n";
}
