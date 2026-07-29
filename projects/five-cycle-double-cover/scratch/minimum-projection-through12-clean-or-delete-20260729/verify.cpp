#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <functional>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

using Word = std::array<unsigned char, 12>;

struct Shape {
    std::vector<int> lengths;
    std::vector<int> offsets;
};

static std::vector<std::array<unsigned char, 4>> gl_maps() {
    std::vector<std::array<unsigned char, 4>> result;
    std::array<unsigned char, 3> values{1, 2, 3};
    do {
        result.push_back({0, values[0], values[1], values[2]});
    } while (std::next_permutation(values.begin(), values.end()));
    return result;
}

static const auto GL = gl_maps();

static std::string normalized(const Word& word,
                              const std::vector<int>& indices) {
    std::array<int, 4> names{-1, -1, -1, -1};
    int next = 0;
    std::string result;
    for (int index : indices) {
        int value = word[index];
        if (names[value] < 0) names[value] = next++;
        result.push_back(char('0' + names[value]));
    }
    return result;
}

static std::vector<std::vector<int>> edge_actions(int length, int offset) {
    std::vector<std::vector<int>> result;
    for (int anchor = 0; anchor < length; ++anchor) {
        std::vector<int> rotation, reflection;
        for (int index = 0; index < length; ++index) {
            rotation.push_back(offset + (anchor + index) % length);
            int reflected = (anchor - index - 1) % length;
            if (reflected < 0) reflected += length;
            reflection.push_back(offset + reflected);
        }
        result.push_back(rotation);
        result.push_back(reflection);
    }
    return result;
}

static std::vector<std::vector<int>> vertex_actions(int length, int offset) {
    std::vector<std::vector<int>> result;
    for (int anchor = 0; anchor < length; ++anchor) {
        std::vector<int> rotation, reflection;
        for (int index = 0; index < length; ++index) {
            rotation.push_back(offset + (anchor + index) % length);
            int reflected = (anchor - index) % length;
            if (reflected < 0) reflected += length;
            reflection.push_back(offset + reflected);
        }
        result.push_back(rotation);
        result.push_back(reflection);
    }
    return result;
}

static std::string normalized_partition(
    const std::array<unsigned char, 12>& partition,
    const std::vector<int>& indices) {
    std::array<int, 12> names;
    names.fill(-1);
    int next = 0;
    std::string result;
    for (int index : indices) {
        int value = partition[index];
        if (names[value] < 0) names[value] = next++;
        result.push_back(char('0' + names[value]));
    }
    return result;
}

static std::string canonical_pair_key(
    const Word& word,
    const std::array<unsigned char, 12>& partition,
    const Shape& shape) {
    if (shape.lengths.size() != 2)
        throw std::runtime_error("pair key is needed only for two circuits");
    auto edge0 = edge_actions(shape.lengths[0], shape.offsets[0]);
    auto edge1 = edge_actions(shape.lengths[1], shape.offsets[1]);
    auto vertex0 = vertex_actions(shape.lengths[0], shape.offsets[0]);
    auto vertex1 = vertex_actions(shape.lengths[1], shape.offsets[1]);
    std::string best(25, '9');
    for (int first = 0; first < (int)edge0.size(); ++first) {
        for (int second = 0; second < (int)edge1.size(); ++second) {
            for (int swapped = 0;
                 swapped <= (shape.lengths[0] == shape.lengths[1]);
                 ++swapped) {
                std::vector<int> edges, vertices;
                if (!swapped) {
                    edges = edge0[first];
                    edges.insert(edges.end(),
                                 edge1[second].begin(), edge1[second].end());
                    vertices = vertex0[first];
                    vertices.insert(vertices.end(),
                                    vertex1[second].begin(),
                                    vertex1[second].end());
                } else {
                    edges = edge1[second];
                    edges.insert(edges.end(),
                                 edge0[first].begin(), edge0[first].end());
                    vertices = vertex1[second];
                    vertices.insert(vertices.end(),
                                    vertex0[first].begin(),
                                    vertex0[first].end());
                }
                std::string key = normalized(word, edges) + " " +
                                  normalized_partition(partition, vertices);
                best = std::min(best, key);
            }
        }
    }
    return best;
}

static std::string canonical_word(const Word& word, const Shape& shape) {
    std::vector<std::vector<std::vector<int>>> actions;
    for (int circuit = 0; circuit < (int)shape.lengths.size(); ++circuit) {
        actions.push_back(edge_actions(shape.lengths[circuit],
                                       shape.offsets[circuit]));
    }
    std::string best(12, '9');
    if (shape.lengths.size() == 1) {
        for (const auto& first : actions[0])
            best = std::min(best, normalized(word, first));
    } else if (shape.lengths.size() == 2) {
        for (const auto& first : actions[0]) {
            for (const auto& second : actions[1]) {
                std::vector<int> indices = first;
                indices.insert(indices.end(), second.begin(), second.end());
                best = std::min(best, normalized(word, indices));
                if (shape.lengths[0] == shape.lengths[1]) {
                    indices = second;
                    indices.insert(indices.end(), first.begin(), first.end());
                    best = std::min(best, normalized(word, indices));
                }
            }
        }
    } else {
        std::array<int, 3> order{0, 1, 2};
        for (const auto& first : actions[0]) {
            for (const auto& second : actions[1]) {
                for (const auto& third : actions[2]) {
                    std::array<std::vector<int>, 3> rows{first, second, third};
                    order = {0, 1, 2};
                    do {
                        std::vector<int> indices;
                        for (int which : order)
                            indices.insert(indices.end(),
                                           rows[which].begin(),
                                           rows[which].end());
                        best = std::min(best, normalized(word, indices));
                    } while (std::next_permutation(order.begin(), order.end()));
                }
            }
        }
    }
    return best;
}

static Word from_string(const std::string& text) {
    Word result{};
    for (int index = 0; index < (int)text.size(); ++index)
        result[index] = text[index] - '0';
    return result;
}

static bool proper_piece(const std::vector<unsigned char>& piece) {
    std::array<bool, 4> seen{};
    for (int index = 0; index < (int)piece.size(); ++index) {
        seen[piece[index]] = true;
        if (piece[index] == piece[(index + 1) % piece.size()]) return false;
    }
    return std::all_of(seen.begin(), seen.end(), [](bool value) {
        return value;
    });
}

static std::vector<std::vector<unsigned char>> proper_words(int length) {
    std::vector<std::vector<unsigned char>> result;
    uint64_t limit = uint64_t(1) << (2 * length);
    for (uint64_t code = 0; code < limit; ++code) {
        std::vector<unsigned char> word(length);
        uint64_t value = code;
        for (int index = 0; index < length; ++index) {
            word[index] = value & 3;
            value >>= 2;
        }
        if (proper_piece(word)) result.push_back(word);
    }
    return result;
}

static std::vector<Word> canonical_single_representatives(int length) {
    Shape shape{{length}, {0}};
    std::set<std::string> representatives;
    Word word{};
    std::function<void(int, int)> recurse = [&](int index, int maximum) {
        if (index == length) {
            if (maximum == 3 && word[length - 1] != word[0])
                representatives.insert(canonical_word(word, shape));
            return;
        }
        for (int value = 0; value <= std::min(3, maximum + 1); ++value) {
            if (value == word[index - 1]) continue;
            word[index] = value;
            recurse(index + 1, std::max(maximum, value));
        }
    };
    word[0] = 0;
    recurse(1, 0);
    std::vector<Word> result;
    for (const auto& text : representatives) result.push_back(from_string(text));
    return result;
}

static std::vector<Word> shape_words(const Shape& shape) {
    if (shape.lengths.size() == 1)
        return canonical_single_representatives(shape.lengths[0]);

    std::vector<std::vector<unsigned char>> firsts;
    if (shape.lengths[0] == 4) {
        firsts.push_back({0, 1, 2, 3});
    } else if (shape.lengths[0] == 5) {
        firsts.push_back({0, 1, 0, 2, 3});
    } else {
        for (const auto& word :
             canonical_single_representatives(shape.lengths[0])) {
            firsts.emplace_back(word.begin(),
                                word.begin() + shape.lengths[0]);
        }
    }
    auto seconds = proper_words(shape.lengths[1]);
    std::vector<std::vector<unsigned char>> thirds;
    if (shape.lengths.size() == 3)
        thirds = proper_words(shape.lengths[2]);
    else
        thirds.push_back({});

    std::set<std::string> representatives;
    for (const auto& first : firsts) {
        for (const auto& second : seconds) {
            for (const auto& third : thirds) {
                Word word{};
                int index = 0;
                for (auto value : first) word[index++] = value;
                for (auto value : second) word[index++] = value;
                for (auto value : third) word[index++] = value;
                representatives.insert(canonical_word(word, shape));
            }
        }
    }
    std::vector<Word> result;
    for (const auto& text : representatives) result.push_back(from_string(text));
    return result;
}

struct Counts {
    uint64_t charge_valid = 0;
    uint64_t dirty = 0;
    uint64_t direct_clean = 0;
    uint64_t delete_branch = 0;
    uint64_t failures = 0;
};

struct Auditor {
    Shape shape;
    Word word{};
    std::array<unsigned char, 12> derivative{};
    std::array<unsigned char, 12> partition{};
    int components = 0;
    std::array<std::array<unsigned char, 4>, 6> maps{};
    std::array<std::array<unsigned char, 4>, 6> certificate_maps{};
    std::array<unsigned char, 12> certificate_base{};
    int certificate_circuit = -1;
    int certificate_missing_colour = -1;
    std::set<std::string> delete_orbits;
    Counts counts;

    Auditor(Shape input) : shape(std::move(input)) {
        maps[0] = {0, 1, 2, 3};
    }

    void set_derivative() {
        for (int circuit = 0; circuit < (int)shape.lengths.size(); ++circuit) {
            int offset = shape.offsets[circuit];
            int length = shape.lengths[circuit];
            for (int local = 0; local < length; ++local) {
                int previous = offset + (local + length - 1) % length;
                derivative[offset + local] =
                    word[previous] ^ word[offset + local];
            }
        }
    }

    bool is_dirty() const {
        std::array<unsigned char, 6> parity{};
        for (int circuit = 0; circuit < (int)shape.lengths.size(); ++circuit) {
            int offset = shape.offsets[circuit];
            int length = shape.lengths[circuit];
            for (int local = 0; local < length; ++local) {
                int edge = offset + local;
                int successor = offset + (local + 1) % length;
                int first = partition[edge], second = partition[successor];
                if (first != second && word[edge] == 0) {
                    parity[first] ^= 1;
                    parity[second] ^= 1;
                }
            }
        }
        return std::any_of(parity.begin(), parity.begin() + components,
                           [](unsigned char value) { return value; });
    }

    bool clean_for_bases(
        const std::array<unsigned char, 12>& base) const {
        int relative_circuits = (int)shape.lengths.size() - 1;
        int translations = 1 << (2 * relative_circuits);
        for (int code = 0; code < translations; ++code) {
            std::array<unsigned char, 3> shift{};
            int value = code;
            for (int circuit = 1; circuit < (int)shape.lengths.size();
                 ++circuit) {
                shift[circuit] = value & 3;
                value >>= 2;
            }
            bool parity[6][4]{};
            for (int circuit = 0; circuit < (int)shape.lengths.size();
                 ++circuit) {
                int offset = shape.offsets[circuit];
                int length = shape.lengths[circuit];
                for (int local = 0; local < length; ++local) {
                    int edge = offset + local;
                    int successor = offset + (local + 1) % length;
                    int first = partition[edge], second = partition[successor];
                    if (first != second) {
                        int colour = base[edge] ^ shift[circuit];
                        parity[first][colour] ^= true;
                        parity[second][colour] ^= true;
                    }
                }
            }
            bool any = false;
            for (int component = 0; component < components; ++component)
                for (int colour = 0; colour < 4; ++colour)
                    any |= parity[component][colour];
            if (!any) return true;
        }
        return false;
    }

    std::pair<bool, bool> evaluate_maps() {
        std::array<unsigned char, 12> transformed{}, base{};
        bool deletable = false;
        for (int index = 0; index < 12; ++index)
            transformed[index] =
                maps[partition[index]][derivative[index]];
        int deletable_circuit = -1;
        int missing_colour = -1;
        for (int circuit = 0; circuit < (int)shape.lengths.size(); ++circuit) {
            int offset = shape.offsets[circuit];
            int length = shape.lengths[circuit];
            unsigned char value = 0;
            unsigned char used = 0;
            for (int local = 0; local < length; ++local) {
                value ^= transformed[offset + local];
                base[offset + local] = value;
                used |= 1u << value;
            }
            if (value != 0) return {false, false};
            if (__builtin_popcount(used) < 4) {
                deletable = true;
                if (deletable_circuit < 0) {
                    deletable_circuit = circuit;
                    for (int colour = 0; colour < 4; ++colour) {
                        if (!(used >> colour & 1)) {
                            missing_colour = colour;
                            break;
                        }
                    }
                }
            }
        }
        if (deletable && certificate_circuit < 0) {
            certificate_maps = maps;
            certificate_base = base;
            certificate_circuit = deletable_circuit;
            certificate_missing_colour = missing_colour;
        }
        return {clean_for_bases(base), deletable};
    }

    std::pair<bool, bool> map_search(int component, bool deletion_seen) {
        if (component == components) {
            auto [clean, deletable] = evaluate_maps();
            return {clean, deletion_seen || deletable};
        }
        bool seen = deletion_seen;
        for (const auto& map : GL) {
            maps[component] = map;
            auto [clean, deletable] = map_search(component + 1, seen);
            if (clean) return {true, true};
            seen |= deletable;
        }
        return {false, seen};
    }

    void classify_partition() {
        ++counts.charge_valid;
        if (components == 1 || !is_dirty()) return;
        ++counts.dirty;
        certificate_circuit = -1;
        certificate_missing_colour = -1;
        auto [clean, deletable] = map_search(1, false);
        if (clean) {
            ++counts.direct_clean;
        } else if (deletable) {
            ++counts.delete_branch;
            if (certificate_circuit < 0)
                throw std::runtime_error("missing deletion certificate");
            delete_orbits.insert(canonical_pair_key(word, partition, shape));
            std::cout << "DELETESTATE shape=";
            for (int circuit = 0; circuit < (int)shape.lengths.size();
                 ++circuit) {
                if (circuit) std::cout << "+";
                std::cout << shape.lengths[circuit];
            }
            std::cout << " word=";
            int word_offset = 0;
            for (int circuit = 0; circuit < (int)shape.lengths.size();
                 ++circuit) {
                if (circuit) std::cout << "|";
                for (int local = 0; local < shape.lengths[circuit]; ++local)
                    std::cout << int(word[word_offset + local]);
                word_offset += shape.lengths[circuit];
            }
            std::cout << " partition=";
            for (int index = 0; index < 12; ++index)
                std::cout << int(partition[index]);
            std::cout << " maps=";
            for (int component = 0; component < components; ++component) {
                if (component) std::cout << "/";
                for (int colour = 0; colour < 4; ++colour)
                    std::cout << int(certificate_maps[component][colour]);
            }
            std::cout << " base=";
            word_offset = 0;
            for (int circuit = 0; circuit < (int)shape.lengths.size();
                 ++circuit) {
                if (circuit) std::cout << "|";
                for (int local = 0; local < shape.lengths[circuit]; ++local)
                    std::cout << int(
                        certificate_base[word_offset + local]);
                word_offset += shape.lengths[circuit];
            }
            std::cout << " delete_circuit=" << certificate_circuit
                      << " missing_colour=" << certificate_missing_colour
                      << "\n";
        } else {
            ++counts.failures;
            std::cout << "COUNTERSTATE word=";
            int offset = 0;
            for (int circuit = 0; circuit < (int)shape.lengths.size();
                 ++circuit) {
                if (circuit) std::cout << "|";
                for (int local = 0; local < shape.lengths[circuit]; ++local)
                    std::cout << int(word[offset + local]);
                offset += shape.lengths[circuit];
            }
            std::cout << " partition=";
            for (int index = 0; index < 12; ++index)
                std::cout << int(partition[index]);
            std::cout << "\n";
        }
    }

    void partition_recurse(
        uint16_t remaining, int component,
        const std::array<std::vector<uint16_t>, 12>& blocks) {
        if (!remaining) {
            components = component;
            classify_partition();
            return;
        }
        int first = __builtin_ctz(remaining);
        for (uint16_t block : blocks[first]) {
            if ((block & remaining) != block) continue;
            uint16_t mask = block;
            while (mask) {
                int bit = __builtin_ctz(mask);
                partition[bit] = component;
                mask &= mask - 1;
            }
            partition_recurse(remaining ^ block, component + 1, blocks);
        }
    }

    void audit_word() {
        set_derivative();
        std::array<unsigned char, 1 << 12> charge{};
        std::array<std::vector<uint16_t>, 12> blocks;
        for (int mask = 1; mask < (1 << 12); ++mask) {
            int bit = __builtin_ctz(mask);
            charge[mask] = charge[mask ^ (1 << bit)] ^ derivative[bit];
            if (charge[mask] == 0) blocks[__builtin_ctz(mask)].push_back(mask);
        }
        partition_recurse((1 << 12) - 1, 0, blocks);
    }
};

static void run_shape(const Shape& shape, const std::string& name) {
    auto words = shape_words(shape);
    Auditor auditor(shape);
    for (int index = 0; index < (int)words.size(); ++index) {
        auditor.word = words[index];
        auditor.audit_word();
        if ((index + 1) % 25 == 0 || index + 1 == (int)words.size()) {
            std::cout << name << " progress=" << index + 1 << "/"
                      << words.size() << " dirty=" << auditor.counts.dirty
                      << " failures=" << auditor.counts.failures << "\n";
        }
    }
    std::cout << "RESULT shape=" << name
              << " canonical_words=" << words.size()
              << " charge_valid=" << auditor.counts.charge_valid
              << " dirty=" << auditor.counts.dirty
              << " direct_clean=" << auditor.counts.direct_clean
              << " delete_branch=" << auditor.counts.delete_branch
              << " delete_orbits=" << auditor.delete_orbits.size()
              << " dichotomy_failures=" << auditor.counts.failures << "\n";
    for (const auto& orbit : auditor.delete_orbits)
        std::cout << "DELETEORBIT shape=" << name << " " << orbit << "\n";
}

int main(int argc, char** argv) {
    if (argc == 2 && !std::freopen(argv[1], "w", stdout))
        throw std::runtime_error("could not open output file");
    if (argc > 2)
        throw std::runtime_error("usage: verify [optional-output-file]");
    run_shape(Shape{{12}, {0}}, "12");
    run_shape(Shape{{4, 8}, {0, 4}}, "4+8");
    run_shape(Shape{{5, 7}, {0, 5}}, "5+7");
    run_shape(Shape{{6, 6}, {0, 6}}, "6+6");
    run_shape(Shape{{4, 4, 4}, {0, 4, 8}}, "4+4+4");
}
