#!/usr/bin/env python3
"""Primary bounded arithmetic audit of density-equality rigidity."""

profiles = 0
equalities = 0
for h in range(1, 241):
    for m in range(0, 241):
        sigma = 4 * m - 3 * h
        if sigma < 0:
            continue
        profiles += 1

        # Exhaust aggregate defect decompositions.  Equation (7) says
        # sigma is a sum of eight nonnegative integers.
        if sigma == 0:
            equalities += 1
            assert m * 4 == h * 3

            # Cubic equality requires V=(m+h)*2/3 and n=V-h.
            numerator = 2 * (m + h)
            if numerator % 3:
                continue
            vertices = numerator // 3
            n = vertices - h
            assert 6 * n == h

            # Three colour classes are at most h/4 and sum to m.
            possible = []
            for m1 in range(m + 1):
                for m2 in range(m - m1 + 1):
                    m3 = m - m1 - m2
                    if max(m1, m2, m3) * 4 <= h:
                        possible.append((m1, m2, m3))
            assert possible == [(h // 4, h // 4, h // 4)]
            assert h % 12 == 0
            k = tuple(2 * value - n for value in possible[0])
            assert k == (h // 3, h // 3, h // 3)
            q = (h - n) // 2
            assert q * 12 == 5 * h

print(
    "PASS:",
    f"profiles={profiles}",
    f"density_equalities={equalities}",
    "max_h=240 max_m=240",
)
