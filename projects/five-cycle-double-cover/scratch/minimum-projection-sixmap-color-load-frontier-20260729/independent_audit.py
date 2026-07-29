#!/usr/bin/env python3
"""Independent matrix-level audit of constructive colour-load descent."""

from itertools import product


def bits(x):
    return ((x >> 1) & 1, x & 1)


def apply(matrix, x):
    a, b = bits(x)
    return (
        (((matrix[0] * a + matrix[1] * b) & 1) << 1)
        | ((matrix[2] * a + matrix[3] * b) & 1)
    )


matrices = []
for matrix in product(range(2), repeat=4):
    image = tuple(apply(matrix, x) for x in range(4))
    if set(image) == set(range(4)):
        matrices.append((matrix, image))
assert len(matrices) == 6


def alpha(kernel, x):
    """The unique nonzero functional with nonzero kernel vector kernel."""
    if kernel == 1:
        return bits(x)[0]
    if kernel == 2:
        return bits(x)[1]
    assert kernel == 3
    a, b = bits(x)
    return a ^ b


assert all(
    [x for x in range(4) if alpha(kernel, x) == 0] == [0, kernel]
    for kernel in (1, 2, 3)
)

profile_checks = 0
descent_checks = 0
for N in product(range(4), repeat=3):
    for O in product(range(4), repeat=3):
        total = sum(N) + sum(O)
        for outside_kernel, inside_kernel in product((1, 2, 3), repeat=2):
            candidates = [
                image for _, image in matrices
                if image[inside_kernel] == outside_kernel
            ]
            assert len(candidates) == 2
            image = candidates[0]
            ones = sum(
                O[colour - 1] * alpha(outside_kernel, colour)
                for colour in (1, 2, 3)
            )
            ones += sum(
                N[colour - 1] * alpha(outside_kernel, image[colour])
                for colour in (1, 2, 3)
            )
            assert ones == total - O[outside_kernel - 1] - N[inside_kernel - 1]
            profile_checks += 1

            for h in range(2 * total + 1):
                if 2 * ones >= h:
                    continue
                for support_ones in range(h + 1):
                    # At least one of alpha(s^U) and h+alpha(s^U)
                    # has a strict support majority.
                    assert support_ones > ones or h - support_ones > ones
                    descent_checks += 1


# Independently check the incidence substitution
# 2N_b=n_Y+k_b(Y), 2O_a=n_O+k_a(outside).
boundary_checks = 0
for n_y, n_o in product(range(7), repeat=2):
    for k_y in product(range(7), repeat=3):
        for k_o in product(range(7), repeat=3):
            if any((n_y + value) % 2 for value in k_y):
                continue
            if any((n_o + value) % 2 for value in k_o):
                continue
            N = tuple((n_y + value) // 2 for value in k_y)
            O = tuple((n_o + value) // 2 for value in k_o)
            h = sum(k_y) + sum(k_o)
            m = (3 * (n_y + n_o) + h) // 2
            if sum(N) + sum(O) != m:
                continue
            for a, b in product(range(3), repeat=2):
                lhs_load = 2 * (O[a] + N[b])
                rhs_load = 2 * m - h
                lhs_boundary = k_o[a] + k_y[b]
                rhs_boundary = 2 * (n_y + n_o)
                assert (lhs_load <= rhs_load) == (lhs_boundary <= rhs_boundary)
                boundary_checks += 1

print(
    "PASS:",
    f"GL_matrices={len(matrices)}",
    f"profile_checks={profile_checks}",
    f"descent_checks={descent_checks}",
    f"boundary_checks={boundary_checks}",
)
