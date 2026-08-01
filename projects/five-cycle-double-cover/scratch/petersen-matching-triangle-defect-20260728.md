# A sharp Petersen no-go for equal local triangles on a perfect matching

Date: **2026-07-28**.

Status: **human-checkable finite no-go for a strengthening; not a
Five-Cycle Double Cover result**.

## Statement

In a standard five-cycle-double-cover labelling of a cubic graph, every
edge receives a two-subset of \([5]\), and the three labels incident with a
vertex are the three edges of a unique triangle in \(K_5\).  Call this the
vertex's *local triangle*.

The following tempting strengthening is false:

> There is a FiveCDC labelling and a perfect matching such that the two
> endpoint local triangles agree on every matching edge.

It is already false for the Petersen graph.  More sharply:

> **Proposition.** For every FiveCDC labelling of the Petersen graph and
> every perfect matching \(M\), at most two of the five edges of \(M\)
> have equal endpoint local triangles.  The bound two is attained.

This proposition does not obstruct FiveCDC.  The retained enumeration
contains 6,000 literal FiveCDC labellings relative to one fixed matching.
It only rules out a stronger matching-based compression.

## Reduction to two cyclic lifts

Every perfect matching of the Petersen graph is equivalent under an
automorphism.  For completeness, the checker enumerates the six perfect
matchings and verifies six explicit vertex permutations preserving the
Petersen edge set whose images of the spoke matching are exactly those
six matchings.  Fix the usual presentation with

\[
 a_i a_{i+1},\qquad b_i b_{i+2},\qquad a_i b_i
 \quad (i\in\mathbb Z_5),
\]

and take the five spokes \(a_i b_i\) as the matching.  Let \(p_i\) be the
two-subset label on spoke \(i\).

At \(a_i\), if the two adjacent outer-cycle labels are \(x_{i-1},x_i\),
then

\[
 x_{i-1}\mathbin\triangle x_i=p_i.
\]

Both \(x_{i-1}\) and \(x_i\) have size two.  Hence they must meet in one
colour, and they are adjacent vertices of \(L(K_5)\).  Conversely, every
such cyclic lift gives the three labels of a \(K_5\)-triangle at \(a_i\).
The same statement holds on the inner cycle.

The spoke order on the outer cycle is

\[
 0,1,2,3,4,
\]

whereas its order on the inner pentagram is

\[
 0,2,4,1,3.
\]

Thus a FiveCDC labelling relative to this matching is exactly a pair of
closed lifts in \(L(K_5)\) of the same word
\((p_0,\ldots,p_4)\), read in these two orders.  The necessary boundary
equation is

\[
 p_0\triangle p_1\triangle p_2\triangle p_3\triangle p_4=\varnothing.
\]

There are 6,240 such ordered words.

For one lifted transition \(x_{i-1},x_i\), the local triangle is their
three-colour union, and its complementary two-subset is

\[
 q_i=[5]\setminus(x_{i-1}\cup x_i).
\]

The local triangles at \(a_i,b_i\) agree exactly when their \(q_i\)'s
agree.

## Six-row human table

Act simultaneously by \(S_5\) on the five colours.  The affine group
\(\operatorname{AGL}(1,5)\) acts on the spoke indices and is the
stabilizer of the displayed perfect matching in the Petersen
automorphism group.  The 6,240 words fall into only six orbits:

| representative | orbit | outer lifts | inner lifts | largest agreement |
|---|---:|---:|---:|---:|
| `01 01 01 02 12` | 600 | 3 | 0 | — |
| `01 01 02 03 23` | 2,400 | 2 | 0 | — |
| `01 01 02 23 03` | 1,200 | 1 | 2 | 0 |
| `01 01 23 24 34` | 600 | 2 | 2 | 2 |
| `01 02 13 24 34` | 1,200 | 1 | 1 | 1 |
| `01 02 23 34 14` | 240 | 0 | 1 | — |

The orbit sizes sum to 6,240.  Each lift column can be checked by trying
the ten possible label choices on the cycle edge immediately before
vertex \(0\), then repeatedly xoring the displayed spoke label.  No SAT
solver is involved.  In the three rows liftable in both orders, comparing
the five literal complements \(q_i\) gives the last column.  Its maximum
is two.

Counting every word and every pair of lifts gives

\[
\begin{array}{c|rrr}
\text{number of agreeing spokes}&0&1&2\\ \hline
\text{literal labellings}&2400&2400&1200.
\end{array}
\]

This also proves attainment.

## Reproduction

Run:

```text
python3 scratch/verify_petersen_matching_triangle_defect.py
```

The checker uses only the Python standard library.  It enumerates the
perfect matchings, verifies the explicit automorphism transversal,
regenerates the 6,240 words, both cyclic lift sets, the six group orbits,
every literal Petersen vertex equation, and the displayed distribution.

## Scope and AI-use disclosure

OpenAI Codex agents, directed by the user, found and tested the failed
strengthening, reduced it to the six-row Petersen calculation, wrote the
checker, and drafted this note.  The proof is included so that a reader
can verify it without trusting the AI system.  No claim of novelty is
made without a specialist literature review.  This result is not an
UNSAT instance of the FiveCDC formula, not a counterexample to FiveCDC,
and not a resolution of the conjecture.
