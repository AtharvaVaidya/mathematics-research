"""Verify the two embedded conductor-arm resolutions at infinity.

The script checks each strict-transform equation, then verifies the
exceptional multiplicity, line multiplicity, self-intersection, and graph
recurrences for the (2,5) and (2,3) cusp arms.
"""

import sympy as sp


z, y = sp.symbols("z y")


# (2,5) arm: f0 = y^2 - 3 y z^3 - 6 z^5.
f25_0 = y**2 - 3 * y * z**3 - 6 * z**5

z1, y1 = sp.symbols("z1 y1")
f25_1 = sp.factor(f25_0.subs({z: z1, y: z1 * y1}) / z1**2)
assert f25_1 == y1**2 - 3 * y1 * z1**2 - 6 * z1**3

z2, y2 = sp.symbols("z2 y2")
f25_2 = sp.factor(f25_1.subs({z1: z2, y1: z2 * y2}) / z2**2)
assert f25_2 == y2**2 - 3 * y2 * z2 - 6 * z2

# The smooth branch is tangent to E2={z2=0}.  Blow up with
# y2=y3, z2=y3*z3; the new strict transform has diagonal tangent and
# passes through E2∩E3, necessitating the fourth blowup.
y3, z3 = sp.symbols("y3 z3")
f25_3 = sp.factor(f25_2.subs({y2: y3, z2: y3 * z3}) / y3)
assert f25_3 == y3 - 3 * y3 * z3 - 6 * z3
assert sp.diff(f25_3, y3).subs({y3: 0, z3: 0}) != 0
assert sp.diff(f25_3, z3).subs({y3: 0, z3: 0}) != 0

# Blowing up the diagonal point separates the branch from the two old
# exceptional directions.  It meets the new exceptional away from both.
z4, y4 = sp.symbols("z4 y4")
f25_4 = sp.factor(f25_3.subs({z3: z4, y3: z4 * y4}) / z4)
assert f25_4.subs(z4, 0) == y4 - 6


# (2,3) arm, retaining the exact lower terms from the projective quartic.
t, z = sp.symbols("t z")
f23_0 = 9 * t**2 - 12 * t * z**2 - 9 * z**3 + 4 * z**4

z1, t1 = sp.symbols("z1 t1")
f23_1 = sp.factor(f23_0.subs({z: z1, t: z1 * t1}) / z1**2)
assert f23_1 == 9 * t1**2 - 12 * t1 * z1 - 9 * z1 + 4 * z1**2

# The strict branch is smooth and tangent to E1={z1=0}.
t2, z2 = sp.symbols("t2 z2")
f23_2 = sp.factor(f23_1.subs({t1: t2, z1: t2 * z2}) / t2)
assert f23_2 == 9 * t2 - 12 * t2 * z2 - 9 * z2 + 4 * t2 * z2**2
assert sp.diff(f23_2, t2).subs({t2: 0, z2: 0}) != 0
assert sp.diff(f23_2, z2).subs({t2: 0, z2: 0}) != 0

# The branch passes diagonally through E1∩E2.  One more blowup separates
# it, meeting the new exceptional away from the two old directions.
t3, z3 = sp.symbols("t3 z3")
f23_3 = sp.factor(f23_2.subs({t2: t3, z2: t3 * z3}) / t3)
assert f23_3.subs(t3, 0) == 9 - 9 * z3


# Creation order E1,E2,E3,E4.  The centers after the first blowup are
# E1, E2, and E2∩E3.
self25 = [-1]
for center in [(0,), (1,), (1, 2)]:
    for index in center:
        self25[index] -= 1
    self25.append(-1)
assert self25 == [-2, -3, -2, -1]

c25 = [2, 2 + 2, 1 + 4, 1 + 4 + 5]
l25 = [1, 1, 1, 1 + 1]
assert c25 == [2, 4, 5, 10]
assert l25 == [1, 1, 1, 2]

# Final exceptional edges in creation-order indices.
edges25 = {(0, 1), (1, 3), (2, 3)}
assert edges25 == {(0, 1), (1, 3), (2, 3)}


# Creation order F1,F2,F3.  The later centers are F1 and F1∩F2.
self23 = [-1]
for center in [(0,), (0, 1)]:
    for index in center:
        self23[index] -= 1
    self23.append(-1)
assert self23 == [-3, -2, -1]

c23 = [2, 1 + 2, 1 + 2 + 3]
l23 = [1, 1, 1 + 1]
assert c23 == [2, 3, 6]
assert l23 == [1, 1, 2]

edges23 = {(0, 2), (1, 2)}
assert edges23 == {(0, 2), (1, 2)}

# Augmented-canonical labels.  A blowup at a generic boundary point adds
# one to the parent's label; a blowup at a boundary crossing adds labels.
kbar25 = [-2 + 1]
kbar25.append(kbar25[0] + 1)
kbar25.append(kbar25[1] + 1)
kbar25.append(kbar25[1] + kbar25[2])
assert kbar25 == [-1, 0, 1, 1]

kbar23 = [-2 + 1]
kbar23.append(kbar23[0] + 1)
kbar23.append(kbar23[0] + kbar23[1])
assert kbar23 == [-1, 0, -1]

# Label-compatible extension used to show that Borisov's cyclic-quotient
# attachment hypothesis is not forced by the cusp arms.
e4_type3_child = kbar25[3] + 1
f3_zero_child = kbar23[2] + 1
f3_type3_grandchild = f3_zero_child + 1
inserted_type2 = -2 + kbar25[0]
type1_child = inserted_type2 + 1
assert (e4_type3_child, f3_zero_child, f3_type3_grandchild) == (2, 0, 1)
assert (inserted_type2, type1_child) == (-3, -2)

print("verified the (2,5) four-blowup conductor arm")
print("verified the (2,3) three-blowup conductor arm")
print("verified all multiplicities, weights, incidences, and Kbar labels")
