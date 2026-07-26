# Order 100: unmarked-factor exclusion and the exact row-star frontier

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE UNMARKED EXCLUSION / SOLVER-FREE FINITE
ROW-STAR CENSUS / INDEPENDENT EXACT-SMT REPLAY / THREE ABSTRACT PROFILE
ORBITS REMAIN / CONNECTED EIGHT-MARK SIZE-FOUR BRANCH ONLY / FIVE-CDC
STILL OPEN**.

This note advances the connected eight-mark extremal exact-zero
size-four branch from the order-\(98\) exclusion.  At ambient order
\(100\), unmarked bichromatic factor circuits are arithmetically possible
for the first time after order \(98\).  Section 2 excludes them by a short
Kempe-incidence argument.

The resulting all-marked problem has \(1002\) excess-profile orbits.  The
proved local overlap caps leave \(155\).  An exact weighted-kernel
row-and-column-star census leaves only three.  These are still abstract
local incidence objects: the independently chosen stars have not yet been
glued to one global cubic rotation system.

Nothing here resolves the five-cycle double cover conjecture or makes an
orientable claim.

## 1. Setup

Write
\[
                         |V(G)|=88+2t.
\]
At order \(100\), \(t=6\), and the suppressed cubic core has order \(92\).
In either bichromatic factor, write the eight marked circuit lengths as
\[
                         10+2x_0,\ldots,10+2x_7
\]
and the unmarked circuit lengths as \(10+2z_s\).  The factor-size equation
is
\[
                  \sum_{i=0}^7x_i+\sum_s(5+z_s)=6.       \tag{1}
\]

For marked circuits \(A_i,B_j\), let \(m_{ij}\) count their common
\(c\)-edges.  The exact marked--marked caps through excess four are the
two tables proved in `marked-two-factor-overlap-cap-table.md`.  We also
use the marked--unmarked bound
\[
        \left|E(A_i)\cap E(U)\right|\le x_i+z+1          \tag{2}
\]
when \(U\) is an unmarked circuit of length \(10+2z\).

The marked Kempe-incidence inequality says that a marked factor circuit
with \(d\) \(c\)-edges, meeting \(p\) marked and \(u\) unmarked opposite
factor circuits, satisfies
\[
                            2p+u\le d+2.                \tag{3}
\]

We need one parallel form.  If the switched factor circuit itself is
unmarked, no affected opposite mark leaves its old factor circuit.
Consequently all \(p\) affected marks must remain on distinct new factor
circuits.  In the three-matching rank proof this improves
\(\ell\ge p-1\) to \(\ell\ge p\).  Since
\[
                         (p+u)+\ell\le d+1,
\]
we obtain
\[
       \boxed{\text{unmarked switched circuit: }\ 2p+u\le d+1.} \tag{4}
\]
This derivation is the same binary cycle-rank calculation as the proof of
(3); it uses no new graph reduction.

## 2. No factor has an unmarked circuit

Suppose the \(B\)-factor has an unmarked circuit.  Equation (1) forces its
complete profile:

- one unmarked core \(C_{10}\), denoted \(U\);
- seven marked core \(C_{10}\)'s; and
- one marked core \(C_{12}\), denoted \(B_k\).

Fix a marked core \(C_{10}\), say \(A_i\), in the other factor.  It has
five \(c\)-edge incidences.

Every marked \(B\)-side \(C_{10}\) contributes at most one incidence.
The unique marked \(C_{12}\) contributes at most two off the diagonal and
at most one on the diagonal.  The unmarked \(C_{10}\) contributes at most
one by (2).

If \(A_i\) misses \(U\), then (3) gives \(p\le3\).  Three marked
neighbours can contribute at most four incidences, even when one is
\(B_k\).  This is impossible.

If \(A_i\) meets \(U\), then \(u=1\), so (3) again gives \(p\le3\).
The maximum contribution is
\[
             1\text{ from }U+
             2\text{ from }B_k+
             1+1\text{ from two marked }C_{10}\text{'s}=5.       \tag{5}
\]
Thus equality is forced throughout.  In particular, every marked
\(A\)-side \(C_{10}\):

1. meets \(U\) once;
2. meets exactly three marked \(B\)-circuits; and
3. meets \(B_k\) twice.

The third item must be off-diagonal, because the same-mark
\(C_{10}\)--\(C_{12}\) cap is one.

If the \(A\)-factor also has an unmarked circuit, (1) gives it seven
marked \(C_{10}\)'s.  Those seven circuits would contribute fourteen
incidences to \(B_k\), whose \(c\)-degree is six.  Hence the \(A\)-factor
is all-marked.

Let \(q\) be the number of marked \(A\)-side \(C_{10}\)'s.  Since
\(\sum_i x_i=6\), at least two of the eight \(x_i\)'s vanish, so \(q\ge2\).
None of those zero entries is \(x_k\), and the diagonal marked edge gives
\(m_{kk}\ge1\).  The \(B_k\) column therefore has load at least
\[
                              2q+1.
\]
Its degree is six, so \(q\le2\).  Hence \(q=2\), and the other six
\(A\)-circuits are all \(C_{12}\)'s.

Finally consider the unmarked \(B\)-side circuit \(U\).  It meets each of
the two short \(A\)-circuits once.  Applying (4) to \(U\), with \(d=5\)
and no unmarked \(A\)-circuit, gives \(p\le3\).  The other three
incidences of \(U\) must therefore all lie on one further marked
\(A\)-circuit.  That circuit is a \(C_{12}\), but (2) bounds its overlap
with \(U\) by two.  This contradiction proves:

> **Order-\(100\) unmarked-factor exclusion.**
> In the connected eight-mark size-four branch, both bichromatic factors
> at ambient order \(100\) consist only of their eight marked circuits.

The argument is symmetric in the two factors.

## 3. The all-marked cap-table census

We may now write
\[
             x_i,y_j\ge0,\qquad
             \sum_i x_i=\sum_jy_j=6.                 \tag{6}
\]
The matrix \(M=(m_{ij})\) satisfies:
\[
\begin{aligned}
 \sum_jm_{ij}&=5+x_i,&
 \sum_im_{ij}&=5+y_j,&
 m_{ii}&\ge1;                                        \tag{7}\\
 |\{j:m_{ij}>0\}|&\le\left\lfloor{7+x_i\over2}\right\rfloor,&
 |\{i:m_{ij}>0\}|&\le\left\lfloor{7+y_j\over2}\right\rfloor. \tag{8}
\end{aligned}
\]
Every entry whose two excesses are at most four is bounded by the exact
local table in `marked-two-factor-overlap-cap-table.md`.  For a larger
excess, the census retains the general marked-overlap bound together with
the elementary private-mark cap.  It also retains the previously proved
short-\(C_{10}\)-to-\(C_{12}\) spacing condition.

Sorting \(x\) nonincreasingly and sorting \(y\) inside each equal-\(x\)
block gives one representative of every simultaneous-\(S_8\) orbit.
There are exactly
\[
                              1002                 \tag{9}
\]
such profile pairs.

`scratch/enumerate_order100_incidence_relaxation.py` is a solver-free
bounded-composition backtracker.  Its complete result is

```text
order-100 all-marked incidence relaxation: PASS
canonical_profile_pairs=1002
surviving_profiles=155
total_search_nodes=2242008
census_sha256=68e509b357a5bea2d645899ef1288fbaad258136f4e706bc4b72ccb4fab7d4dd
survivor_sha256=07124090c52d1bda9de37a55c6e4df40d365c91fbb7dfd5a94c83e45891ae27f
```

The complete \(155\)-witness stream is frozen in
`scratch/order100-incidence-relaxation-survivors.json`.  A separately
written multiset-orbit QF_LIA encoding in
`scratch/check_order100_incidence_relaxation_z3.py` independently returns
\(155\) SAT and \(847\) UNSAT profile orbits.

The first canonical cap-table survivor has
\[
\begin{aligned}
x&=(4,1,1,0,0,0,0,0),\\
y&=(0,0,0,2,2,1,1,0),
\end{aligned}
\]
and
\[
M=\begin{pmatrix}
2&2&2&0&0&0&1&2\\
2&1&2&0&1&0&0&0\\
0&2&1&0&0&1&0&2\\
0&0&0&1&2&0&2&0\\
1&0&0&0&2&0&2&0\\
0&0&0&2&2&1&0&0\\
0&0&0&2&0&2&1&0\\
0&0&0&2&0&2&0&1
\end{pmatrix}.                                      \tag{10}
\]

This matrix is not row-star realizable; it is retained here as the exact
frontier of the cap-table relaxation.

## 4. A human simultaneous-spacing obstruction

> **Consecutive \(C_{10}\)--\(C_{14}\) lemma.**
> Differently marked core factor circuits \(C_{10}\) and \(C_{14}\) cannot
> share exactly two \(c\)-edges that are consecutive in the cyclic
> \(c\)-edge order of the \(C_{10}\), if the marked expansion has girth at
> least ten.

### Proof

Lift the two marked circuits to lengths \(11\) and \(15\).  Their two
common edges are ordinary, because the marks differ.  Delete those common
edges.

On the lifted \(C_{11}\), the residual paths have lengths \(1\) and \(8\):
the path between consecutive \(c\)-edges is their intervening
\(a\)-edge, while the private marked subdivision lies on the other path.
The two residual paths on the lifted \(C_{15}\) have positive lengths
\(b_1,b_2\) with
\[
                              b_1+b_2=13,             \tag{11}
\]
so \(\min(b_1,b_2)\le6\).

Contract the four residual paths.  The two common edges \(Q\), the two
\(A\)-paths \(P_A\), and the two \(B\)-paths \(P_B\) are three perfect
matchings on four labelled endpoints; both \(Q\cup P_A\) and
\(Q\cup P_B\) are Hamilton circuits.

If \(P_A\ne P_B\), the kernel is \(K_4\).  One of its triangles uses the
length-one \(A\)-path, the shorter \(B\)-path, and one unit common edge.
Its expanded length is at most
\[
                              1+6+1=8.
\]

If \(P_A=P_B\), the residual paths occur in two parallel pairs.  If the
shorter \(B\)-path is parallel to the length-one \(A\)-path, their
two-edge circuit has length at most seven.  Otherwise, the circuit formed
by the length-one \(A\)-path, the shorter \(B\)-path, and the two common
unit edges has length at most
\[
                              1+6+2=9.
\]
Every case contradicts girth ten. \(\square\)

In row \(3\) of (10), the doubled \(C_{12}\) neighbour must occupy the two
\(c\)-neighbours of the row's marked edge.  The doubled \(C_{14}\)
neighbour is then forced onto the two remaining positions, which are
consecutive.  The lemma excludes (10).

A solver-free five-position word filter imposes these two spacing rules
on every short row and column.  It reduces the \(155\) profiles to \(13\);
the retained checker is
`scratch/enumerate_order100_cyclic_word_relaxation.py`.

## 5. Exact weighted-kernel row stars

The preceding hand lemma is one cell of a complete row-local finite model.
Fix a marked \(A_i\) circuit and label its \(5+x_i\) \(c\)-edge positions
cyclically, with its marked edge at position zero.  If its overlap with
\(B_j\) uses a fixed position set \(S\), delete those common connections.

On the resulting \(2|S|\) endpoints, retain three perfect matchings:

- \(Q\), the common connections;
- \(P_A\), the fixed residual \(A_i\)-paths; and
- \(P_B\), the residual \(B_j\)-paths.

For consecutive positions of \(S\) separated by \(g\) \(c\)-steps, the
corresponding \(A\)-path has weight \(2g-1\), plus one precisely when the
private marked edge at position zero lies in that residual path.  In the
diagonal case, position zero belongs to \(S\); its \(Q\)-connection has
weight two and all other \(Q\)-connections have weight one.

The \(B_j\)-path weights are parameterized exactly by a positive
composition of \(5+y_j\).  Off the diagonal, exactly one part contains
the private \(B_j\) mark, has size at least two, and receives the one-unit
subdivision increment.  Every cyclic order and every endpoint orientation
of the common connections is enumerated.

Thus:
\[
\begin{split}
S\text{ is pair-feasible}
\quad\Longleftrightarrow\quad
&\text{some enumerated }P_B\text{ makes every weighted}\\
&\text{circuit of }Q\cup P_A\cup P_B\text{ have weight at least ten}.
                                                               \tag{12}
\end{split}
\]
This is an equivalence for the isolated two-circuit union, including
parallel kernel paths.  As a self-check, the independent implementation
recovers every entry of both \(5\times5\) exact cap tables.

A row star is feasible when its \(c\)-edge positions can be partitioned
among its neighbours into pair-feasible sets \(S\).  Apply the same
definition to every column.  Distinct opposite factor circuits are
vertex-disjoint, so every graph realization must pass all these tests.
The converse is deliberately not asserted: independently feasible stars
may fail to glue globally.

`scratch/enumerate_order100_exact_row_star_relaxation.py` generates every
pair-feasible subset, every row-star domain, and every column-star domain,
then joins the domains with exact bit-mask propagation.  Starting from the
frozen \(155\)-profile artifact, it reports

```text
order-100 exact row-star incidence relaxation: PASS
canonical_profile_pairs=1002
surviving_profiles=3
total_search_nodes=2543
pair_subset_queries=1066
census_sha256=d6d05a654820f3e72a19a573f4cbf0e2ad416e5ca754be91ebfcaec806b12ac8
survivor_sha256=f7c1791167efed6d82cd68f0e045858d6415bc0fd5c127a8d1762fd9b95ebf1a
```

The three complete local witnesses are frozen in
`scratch/order100-exact-row-star-survivors.json`.

For an independent replay:

1. `scratch/check_order100_row_star_patterns.py` independently constructs
   fixed-gap kernels and recovers all 50 exact cap-table entries; and
2. `scratch/check_order100_exact_row_star_z3.py` literally enumerates
   multiset words, builds row and column domains independently, and asks
   Z3 only to join those finite domains.

The replay reports

```text
order-100 independent exact row-star SMT replay: PASS
canonical_profile_pairs=1002
baseline_unsat=847
row_star_sat=3
row_star_unsat=152
status_sha256=f0736f1774b666e3cc2745a3b1f96f123772b3732de8166c054e0792afee322b
survivor_sha256=7b34681ed4ba91fb0f0824961c9f7002833ca011e05e9d9f2e76ccbee7f62d72
```

The different survivor-stream hashes are expected: each program may choose
a different first matrix inside a feasible profile.  Their feasible
profile sets agree.

## 6. The three remaining profile orbits

All three survivors have the same unlabelled excess partition on both
shores:
\[
                         (2,2,1,1,0,0,0,0).           \tag{13}
\]
They differ only in the relative alignment of the four nonzero
coordinates.

The first canonical row-star survivor is
\[
\begin{aligned}
x&=(2,2,1,1,0,0,0,0),\\
y&=(0,0,0,0,2,2,1,1),
\end{aligned}
\]
with
\[
M=\begin{pmatrix}
2&0&2&2&0&0&1&0\\
0&2&2&2&0&0&0&1\\
2&0&1&0&1&0&0&2\\
0&2&0&1&0&1&0&2\\
1&0&0&0&2&0&2&0\\
0&1&0&0&0&2&2&0\\
0&0&0&0&2&2&1&0\\
0&0&0&0&2&2&0&1
\end{pmatrix}.                                      \tag{14}
\]
The JSON artifact includes an explicit feasible position partition for
every row and every column.

## 7. Global gluing: certified fixed-matrix controls

The phrase "three profile orbits" in Section 6 must not be confused with
three incidence matrices.  The exact row/column-star domain join contains,
respectively,
\[
                         1864,\quad1680,\quad1984      \tag{15}
\]
labelled matrices in the three aligned profiles.

The stabilizer of an aligned profile permutes indices having the same pair
\((x_i,y_i)\).  Its orders are \(16,4,16\), respectively.
`scratch/enumerate_order100_row_star_matrix_orbits.py` canonically quotients
the matrices under these simultaneous permutations and obtains
\[
                          128,\quad427,\quad272        \tag{16}
\]
matrix orbits, for \(827\) in total.  The complete artifact is
`scratch/order100-row-star-matrix-orbits.json`.

For the one primary matrix retained in each profile by Section 5, the
global gluing problem has also been decided.  The finite variables choose:

1. one complete cyclic neighbour word for each of the sixteen factor
   circuits;
2. in every nonempty incidence cell, a bijection between its row and
   column positions and an orientation bit for every shared edge; and
3. after a girth-ten expansion of \(G-M\) is found, one of the \(105\)
   pairings of the eight marked subdivision vertices.

Every cell option is first checked against the exact two-circuit weighted
kernel.  The selected options reconstruct one labelled graph, with no
geometric information discarded.  A short circuit yields a clause
forbidding precisely the chosen cell options which determine its
\(B\)-edges.

The incremental propositional solver
`scratch/solve_order100_global_word_gluing_sat.py` found all three primary
matrices UNSAT already in \(G-M\):

| primary profile | variables | final clauses | lazy models |
|---:|---:|---:|---:|
| 0 | 1320 | 98478 | 1903 |
| 1 | 1520 | 144354 | 2419 |
| 2 | 1710 | 128696 | 2314 |

For each row, the final CNF was replayed by CaDiCaL and CryptoMiniSat.
CaDiCaL emitted a DRAT proof, `drat-trim` converted it to LRAT, and both
the independent C `lrat-check` program and the CakeML-generated
`cake_lpr` program accepted the LRAT.  The CNF hashes are

```text
profile 0  04ed5bd9edd2a32eb77f4a3dd6373d5551500312c9e2c0da2b74d7eca9b5c61e
profile 1  f05546373b4f16f78bdac228b115bbbcb9285e7efc27a5e3a85e41283b083cfe
profile 2  9b08d985a4b6a447163af0788e0099ab1094e903e1512fc5bbda471320a510be
```

Their LRAT hashes are

```text
profile 0  9f38e77f994012d5207644eec262be88a156a53d9c3d4768c02fed232499ba18
profile 1  10aeb13e30a24df57a1541031744180845925f68c973e750b19a6c1f56a9fa99
profile 2  31fa3c659e80fa6997f6748bbdcc22494b4c27febb4ee993f33ec34907e90669
```

This certified control is stronger than pairwise star compatibility: a
separate exact checker finds that all three primary matrices do admit
pairwise-compatible row and column rotations, but their first glued
expansions have girths \(5,4,6\).  The certified obstruction therefore
uses circuits traversing multiple factor circuits.

Most importantly, three fixed-matrix UNSAT results do **not** exclude the
complete set of \(827\) canonical matrix cases in (16).  The next exact question is
global gluing over that complete matrix-orbit artifact.  A SAT realization
would only show that this incidence frontier is geometrically nonempty; a
checked UNSAT result for every matrix orbit would exclude order \(100\) in
this branch.

## AI-use disclosure

OpenAI Codex agents, under human direction, discovered and checked the
unmarked-factor argument, formulated the fixed-position weighted-kernel
model, wrote the two primary enumerators and the independent replay, and
prepared this note.  The human arguments, exact finite domains, complete
survivor artifacts, and executable checks are supplied for inspection.
This is not independent human peer review.
