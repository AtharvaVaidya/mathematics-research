#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static const int GL[6][4] = {
    {0,1,2,3}, {0,1,3,2}, {0,2,1,3},
    {0,2,3,1}, {0,3,1,2}, {0,3,2,1}
};

struct Block {
    uint16_t vertices;
    uint16_t cut_edges;
    bool dirty;
};

struct Audit {
    std::vector<int> lengths;
    std::vector<int> offsets;
    std::vector<int> word;
    std::vector<int> pendant;
    std::vector<Block> allowed;
    std::vector<std::vector<int>> by_anchor;
    std::vector<Block> selected;
    uint64_t charge_valid = 0;
    uint64_t dirty = 0;
    uint64_t direct_failures = 0;
    uint64_t not_clean_or_delete = 0;

    Audit(const std::vector<int>& shape, const std::string& text)
        : lengths(shape), by_anchor(text.size()) {
        int offset = 0;
        for (int length : lengths) {
            offsets.push_back(offset);
            offset += length;
        }
        assert(offset == int(text.size()));
        for (char value : text) word.push_back(value - '0');
        pendant.resize(word.size());
        for (int circuit = 0; circuit < int(lengths.size()); ++circuit) {
            int start = offsets[circuit];
            int length = lengths[circuit];
            for (int local = 0; local < length; ++local) {
                int index = start + local;
                pendant[index] =
                    word[start + (local + length - 1) % length] ^
                    word[index];
                assert(pendant[index] != 0);
            }
        }

        const int order = int(word.size());
        for (uint16_t mask = 1; mask < (1u << order); ++mask) {
            int parity[4] = {};
            uint16_t cut = 0;
            for (int circuit = 0; circuit < int(lengths.size()); ++circuit) {
                int start = offsets[circuit];
                int length = lengths[circuit];
                for (int local = 0; local < length; ++local) {
                    int edge = start + local;
                    int successor = start + (local + 1) % length;
                    bool crosses =
                        ((mask >> edge) ^ (mask >> successor)) & 1;
                    if (crosses) {
                        parity[word[edge]] ^= 1;
                        cut |= uint16_t(1u << edge);
                    }
                }
            }
            if (
                parity[0] == parity[1] &&
                parity[1] == parity[2] &&
                parity[2] == parity[3]
            ) {
                int index = int(allowed.size());
                allowed.push_back({mask, cut, bool(parity[0])});
                for (int vertex = 0; vertex < order; ++vertex) {
                    if ((mask >> vertex) & 1) {
                        by_anchor[vertex].push_back(index);
                    }
                }
            }
        }
    }

    std::pair<bool, bool> clean_or_delete() const {
        int order = int(word.size());
        int components = int(selected.size());
        std::vector<int> labels(order);
        for (int component = 0; component < components; ++component) {
            for (int index = 0; index < order; ++index) {
                if ((selected[component].vertices >> index) & 1) {
                    labels[index] = component;
                }
            }
        }

        int assignments = 1;
        for (int component = 0; component < components; ++component) {
            assignments *= 6;
        }
        bool deletable = false;
        for (int code = 0; code < assignments; ++code) {
            std::vector<int> choice(components);
            int quotient = code;
            for (int component = 0; component < components; ++component) {
                choice[component] = quotient % 6;
                quotient /= 6;
            }

            std::vector<int> base(order);
            bool cyclic = true;
            for (int circuit = 0; circuit < int(lengths.size()); ++circuit) {
                int previous = 0;
                for (int local = 0; local < lengths[circuit]; ++local) {
                    int index = offsets[circuit] + local;
                    previous ^= GL[choice[labels[index]]][pendant[index]];
                    base[index] = previous;
                }
                if (previous != 0) {
                    cyclic = false;
                    break;
                }
            }
            if (!cyclic) continue;

            for (int circuit = 0; circuit < int(lengths.size()); ++circuit) {
                int used = 0;
                for (int local = 0; local < lengths[circuit]; ++local) {
                    used |= 1 << base[offsets[circuit] + local];
                }
                if (used != 15) deletable = true;
            }

            // A global translation preserves clean parity, so fix the
            // first circuit's start at zero.
            int relative_starts = 1;
            for (int circuit = 1; circuit < int(lengths.size()); ++circuit) {
                relative_starts *= 4;
            }
            for (int start_code = 0; start_code < relative_starts;
                 ++start_code) {
                std::vector<int> starts(lengths.size(), 0);
                int start_quotient = start_code;
                for (int circuit = 1; circuit < int(lengths.size());
                     ++circuit) {
                    starts[circuit] = start_quotient % 4;
                    start_quotient /= 4;
                }
                uint16_t colour_masks[4] = {};
                for (int circuit = 0; circuit < int(lengths.size());
                     ++circuit) {
                    for (int local = 0; local < lengths[circuit]; ++local) {
                        int index = offsets[circuit] + local;
                        int colour = base[index] ^ starts[circuit];
                        colour_masks[colour] |= uint16_t(1u << index);
                    }
                }
                bool clean = true;
                for (const Block& block : selected) {
                    for (int colour = 0; colour < 4; ++colour) {
                        if (__builtin_parity(
                            unsigned(block.cut_edges & colour_masks[colour])
                        )) {
                            clean = false;
                            break;
                        }
                    }
                    if (!clean) break;
                }
                if (clean) return {true, deletable};
            }
        }
        return {false, deletable};
    }

    void recurse(uint16_t remaining, bool has_dirty) {
        if (!remaining) {
            ++charge_valid;
            if (!has_dirty) return;
            ++dirty;
            auto outcome = clean_or_delete();
            if (!outcome.first) {
                ++direct_failures;
                if (!outcome.second) {
                    ++not_clean_or_delete;
                    std::cout << "ABSTRACT_DICHOTOMY_FAILURE word=";
                    for (int value : word) std::cout << value;
                    std::cout << " blocks=";
                    for (const Block& block : selected) {
                        std::cout << block.vertices << ",";
                    }
                    std::cout << "\n";
                }
            }
            return;
        }
        int anchor = __builtin_ctz(unsigned(remaining));
        for (int index : by_anchor[anchor]) {
            const Block& block = allowed[index];
            if ((block.vertices & remaining) != block.vertices) continue;
            selected.push_back(block);
            recurse(
                uint16_t(remaining ^ block.vertices),
                has_dirty || block.dirty
            );
            selected.pop_back();
        }
    }
};

int main() {
    std::string shape_line;
    if (!std::getline(std::cin, shape_line)) return 1;
    std::istringstream shape_stream(shape_line);
    std::vector<int> lengths;
    int length;
    while (shape_stream >> length) lengths.push_back(length);
    int order = 0;
    for (int value : lengths) order += value;
    assert(order == 12);

    uint64_t words = 0;
    uint64_t charge_valid = 0;
    uint64_t dirty = 0;
    uint64_t direct_failures = 0;
    uint64_t dichotomy_failures = 0;
    std::string word;
    while (std::getline(std::cin, word)) {
        if (word.empty()) continue;
        Audit audit(lengths, word);
        audit.recurse(uint16_t((1u << order) - 1), false);
        ++words;
        charge_valid += audit.charge_valid;
        dirty += audit.dirty;
        direct_failures += audit.direct_failures;
        dichotomy_failures += audit.not_clean_or_delete;
        if (words % 50 == 0) {
            std::cout
                << "words=" << words
                << " charge_valid=" << charge_valid
                << " dirty=" << dirty
                << " direct_failures=" << direct_failures
                << " dichotomy_failures=" << dichotomy_failures << "\n";
        }
    }
    std::cout
        << "FINAL words=" << words
        << " charge_valid=" << charge_valid
        << " dirty=" << dirty
        << " direct_failures=" << direct_failures
        << " dichotomy_failures=" << dichotomy_failures << "\n";
}
