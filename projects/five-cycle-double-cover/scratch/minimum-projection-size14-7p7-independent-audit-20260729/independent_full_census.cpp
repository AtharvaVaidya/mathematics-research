#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int n = 14;
constexpr int maps[6][4] = {
    {0, 1, 2, 3}, {0, 1, 3, 2}, {0, 2, 1, 3},
    {0, 2, 3, 1}, {0, 3, 1, 2}, {0, 3, 2, 1},
};

struct Block {
    std::uint16_t vertices;
    bool dirty;
};

struct Totals {
    std::uint64_t words = 0;
    std::uint64_t charge_valid = 0;
    std::uint64_t dirty = 0;
    std::uint64_t direct_failures = 0;
    std::uint64_t dichotomy_failures = 0;
};

class WordAudit {
  public:
    explicit WordAudit(std::string text) : text_(std::move(text)) {
        assert(text_.size() == n);
        for (int i = 0; i < n; ++i) {
            word_[i] = text_[i] - '0';
            assert(0 <= word_[i] && word_[i] < 4);
        }
        for (int offset : {0, 7}) {
            for (int j = 0; j < 7; ++j) {
                derivative_[offset + j] =
                    word_[offset + (j + 6) % 7] ^ word_[offset + j];
                assert(derivative_[offset + j] != 0);
            }
        }
        generate_valid_blocks();
    }

    Totals run() {
        recurse((std::uint16_t{1} << n) - 1, false);
        return totals_;
    }

  private:
    std::string text_;
    std::array<int, n> word_{};
    std::array<int, n> derivative_{};
    std::vector<Block> blocks_;
    std::array<std::vector<int>, n> at_anchor_;
    std::vector<int> chosen_;
    std::array<int, n> component_of_{};
    std::array<int, 7> map_choice_{};
    Totals totals_;
    bool deletion_seen_ = false;

    void generate_valid_blocks() {
        for (std::uint16_t subset = 1;
             subset < (std::uint16_t{1} << n); ++subset) {
            std::array<int, 4> cut_parity{};
            for (int offset : {0, 7}) {
                for (int j = 0; j < 7; ++j) {
                    int left = offset + j;
                    int right = offset + (j + 1) % 7;
                    bool crosses =
                        (((subset >> left) ^ (subset >> right)) & 1) != 0;
                    if (crosses) cut_parity[word_[left]] ^= 1;
                }
            }
            if (!(cut_parity[0] == cut_parity[1] &&
                  cut_parity[1] == cut_parity[2] &&
                  cut_parity[2] == cut_parity[3])) {
                continue;
            }
            int index = static_cast<int>(blocks_.size());
            blocks_.push_back({subset, cut_parity[0] != 0});
            for (int vertex = 0; vertex < n; ++vertex) {
                if ((subset >> vertex) & 1) at_anchor_[vertex].push_back(index);
            }
        }
    }

    bool evaluate_maps(int component_count) {
        std::array<int, n> transformed{};
        std::array<int, n> base{};
        for (int position = 0; position < n; ++position) {
            int component = component_of_[position];
            transformed[position] =
                maps[map_choice_[component]][derivative_[position]];
        }

        for (int offset : {0, 7}) {
            int running = 0;
            for (int j = 0; j < 7; ++j) {
                running ^= transformed[offset + j];
                base[offset + j] = running;
            }
            if (running != 0) return false;
        }

        for (int offset : {0, 7}) {
            int used = 0;
            for (int j = 0; j < 7; ++j) used |= 1 << base[offset + j];
            if (used != 15) deletion_seen_ = true;
        }

        for (int relative_shift = 0; relative_shift < 4; ++relative_shift) {
            bool parity[7][4] = {};
            for (int offset : {0, 7}) {
                int shift = offset == 7 ? relative_shift : 0;
                for (int j = 0; j < 7; ++j) {
                    int left = offset + j;
                    int right = offset + (j + 1) % 7;
                    int a = component_of_[left];
                    int b = component_of_[right];
                    if (a != b) {
                        int colour = base[left] ^ shift;
                        parity[a][colour] ^= true;
                        parity[b][colour] ^= true;
                    }
                }
            }
            bool clean = true;
            for (int component = 0; component < component_count; ++component) {
                for (int colour = 0; colour < 4; ++colour) {
                    if (parity[component][colour]) clean = false;
                }
            }
            if (clean) return true;
        }
        return false;
    }

    bool choose_maps(int component, int component_count) {
        if (component == component_count) {
            return evaluate_maps(component_count);
        }
        for (int choice = 0; choice < 6; ++choice) {
            map_choice_[component] = choice;
            if (choose_maps(component + 1, component_count)) return true;
        }
        return false;
    }

    std::pair<bool, bool> classify() {
        for (int component = 0;
             component < static_cast<int>(chosen_.size()); ++component) {
            std::uint16_t subset = blocks_[chosen_[component]].vertices;
            while (subset) {
                int vertex = __builtin_ctz(static_cast<unsigned>(subset));
                component_of_[vertex] = component;
                subset &= subset - 1;
            }
        }
        map_choice_[0] = 0;
        deletion_seen_ = false;
        bool clean = choose_maps(1, static_cast<int>(chosen_.size()));
        return {clean, deletion_seen_};
    }

    void emit_failure() const {
        std::cout << "COUNTERSTATE word=" << text_.substr(0, 7) << "|"
                  << text_.substr(7) << " partition=";
        for (int position = 0; position < n; ++position) {
            std::cout << component_of_[position];
        }
        std::cout << "\n";
    }

    void recurse(std::uint16_t remaining, bool has_dirty) {
        if (remaining == 0) {
            ++totals_.charge_valid;
            if (!has_dirty) return;
            ++totals_.dirty;
            auto [clean, deletable] = classify();
            if (!clean) {
                ++totals_.direct_failures;
                if (!deletable) {
                    ++totals_.dichotomy_failures;
                    emit_failure();
                }
            }
            return;
        }

        int anchor = __builtin_ctz(static_cast<unsigned>(remaining));
        for (int block_index : at_anchor_[anchor]) {
            std::uint16_t subset = blocks_[block_index].vertices;
            if ((subset & remaining) != subset) continue;
            chosen_.push_back(block_index);
            recurse(
                static_cast<std::uint16_t>(remaining ^ subset),
                has_dirty || blocks_[block_index].dirty
            );
            chosen_.pop_back();
        }
    }
};

}  // namespace

int main() {
    std::string header;
    if (!std::getline(std::cin, header)) return 1;
    assert(header == "7 7");

    Totals total;
    std::string word;
    while (std::getline(std::cin, word)) {
        if (word.empty()) continue;
        WordAudit audit(word);
        Totals row = audit.run();
        ++total.words;
        total.charge_valid += row.charge_valid;
        total.dirty += row.dirty;
        total.direct_failures += row.direct_failures;
        total.dichotomy_failures += row.dichotomy_failures;
        if (total.words % 25 == 0) {
            std::cout
                << "progress=" << total.words
                << " charge_valid=" << total.charge_valid
                << " dirty=" << total.dirty
                << " direct_failures=" << total.direct_failures
                << " dichotomy_failures=" << total.dichotomy_failures
                << "\n";
        }
    }
    std::cout
        << "FINAL words=" << total.words
        << " charge_valid=" << total.charge_valid
        << " dirty=" << total.dirty
        << " direct_failures=" << total.direct_failures
        << " dichotomy_failures=" << total.dichotomy_failures
        << "\n";
}
