#!/usr/bin/env python3
"""Exact finite audit of the refined fixed-F potential formula."""

from __future__ import annotations

from itertools import product


def tight(d, q):
    return d == 4 and (q & 1)


def potential(profiles):
    return (
        sum(tight(d, q) for d, q in profiles),
        sum(d - q for d, q in profiles if q & 1),
    )


def exact_second_change(old, new):
    old_odd_stay = 0
    old_odd_flip = 0
    old_even_flip = 0
    for (d, q), (new_d, new_q) in zip(old, new):
        assert d == new_d
        epsilon = (new_q - q) & 1
        if q & 1:
            if epsilon:
                old_odd_flip -= d - q
            else:
                old_odd_stay -= new_q - q
        elif epsilon:
            old_even_flip += d - new_q
    return old_odd_stay + old_odd_flip + old_even_flip


def aggregate_gain(old, new):
    """Positive exactly when the second coordinate decreases."""
    return -exact_second_change(old, new)


def verify_component_identity():
    cases = 0
    for d in range(0, 22, 2):
        for q, new_q in product(range(d + 1), repeat=2):
            old, new = ((d, q),), ((d, new_q),)
            literal = potential(new)[1] - potential(old)[1]
            assert literal == exact_second_change(old, new)
            cases += 1
    return cases


def verify_tight_creation_identity():
    cases = 0
    for d in range(0, 22, 2):
        for q, new_q in product(range(d + 1), repeat=2):
            if tight(d, q):
                continue
            epsilon = (new_q - q) & 1
            predicted = int(d == 4 and not (q & 1) and epsilon)
            assert int(tight(d, new_q)) == predicted
            cases += 1
    return cases


def verify_refined_theorem_two_components():
    checked = descending = 0
    sizes = tuple(range(2, 16, 2))
    for d0, d1 in product(sizes, repeat=2):
        for q0, new_q0 in product(range(d0 + 1), repeat=2):
            for q1, new_q1 in product(range(d1 + 1), repeat=2):
                old = ((d0, q0), (d1, q1))
                new = ((d0, new_q0), (d1, new_q1))
                if potential(old)[0] != 0:
                    continue
                # Protect exactly the old even d=4 components.
                protected = all(
                    not (d == 4 and not (q & 1)) or not ((new_q - q) & 1)
                    for (d, q), (_new_d, new_q) in zip(old, new)
                )
                if not protected:
                    continue
                checked += 1
                assert potential(new)[0] == 0
                assert potential(new)[1] - potential(old)[1] == exact_second_change(old, new)
                if aggregate_gain(old, new) > 0:
                    assert potential(new) < potential(old)
                    descending += 1
    return checked, descending


def verify_strict_weakening_examples():
    # An old even non-four-cut is allowed to flip; its cost is compensated.
    even_flip_old = ((6, 1), (6, 2))
    even_flip_new = ((6, 0), (6, 3))
    assert potential(even_flip_old) == (0, 5)
    assert potential(even_flip_new) == (0, 3)
    assert aggregate_gain(even_flip_old, even_flip_new) == 2

    # A surviving odd component may lose target edges if another removed
    # summand more than compensates for its integer loss.
    compensated_old_loss_old = ((6, 1), (8, 5))
    compensated_old_loss_new = ((6, 0), (8, 3))
    assert potential(compensated_old_loss_old) == (0, 8)
    assert potential(compensated_old_loss_new) == (0, 5)
    assert aggregate_gain(compensated_old_loss_old, compensated_old_loss_new) == 3

    # A d=4 old even flip creates a tight component and must be protected for
    # a lexicographic descent from first coordinate zero.
    tight_old = ((6, 3), (4, 2))
    tight_new = ((6, 2), (4, 1))
    assert potential(tight_old) == (0, 3)
    assert potential(tight_new) == (1, 3)
    return (
        even_flip_old,
        even_flip_new,
        compensated_old_loss_old,
        compensated_old_loss_new,
        tight_old,
        tight_new,
    )


def main():
    component_cases = verify_component_identity()
    tight_cases = verify_tight_creation_identity()
    theorem_cases = verify_refined_theorem_two_components()
    verify_strict_weakening_examples()
    print(f"single-component exact-change cases={component_cases}")
    print(f"single-component tight-creation cases={tight_cases}")
    print(
        f"two-component protected cases={theorem_cases[0]} "
        f"positive-aggregate-gain cases={theorem_cases[1]}"
    )
    print("allowed even flip: old=(6,1)|(6,2) new=(6,0)|(6,3) potential (0,5)->(0,3)")
    print("compensated odd loss: old=(6,1)|(8,5) new=(6,0)|(8,3) potential (0,8)->(0,5)")
    print("necessary d=4 protection: old=(6,3)|(4,2) new=(6,2)|(4,1) potential (0,3)->(1,3)")
    print("PASS REFINED FIXED-F FORMULA")


if __name__ == "__main__":
    main()
