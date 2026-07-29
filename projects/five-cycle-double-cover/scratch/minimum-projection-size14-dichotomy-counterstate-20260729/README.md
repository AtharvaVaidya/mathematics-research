# The first clean-or-delete boundary counterstate

Date: 2026-07-29

Status: **EXACT ABSTRACT COUNTERSTATE, HUMAN PROOF, AND REALIZED
UNCLEANABLE PROJECTION / NOT A FIVE-CYCLE-DOUBLE-COVER COUNTEREXAMPLE**.

## Result

The proposed universal clean-or-delete boundary lemma is false.  Its
first failure occurs at total support size fourteen, with two
7-circuits:

```text
word       0101023|0101232
partition  01234444413024
```

Here the word entries lie in \(K=\mathbb F_2^2=\{0,1,2,3\}\).  On each
circuit, adjacent word entries are distinct and all four values occur.
If \(d_i=c_{i-1}+c_i\), every partition block has zero xor charge.

Nevertheless, after quotienting by one common
\(\operatorname{GL}(2,2)\) action:

- all \(6^4=1,296\) component-map tuples were checked;
- exactly 320 are circuit-integrable;
- these reduce to 40 distinct transformed transition tuples;
- none admits a clean relative circuit translation;
- in none does either integrated circuit omit a colour, so circuit
  deletion is impossible.

This refutes the abstract dichotomy based only on proper all-four
boundary words and zero block charges.  It does **not** refute a
version with the additional hypothesis that the projection is globally
cardinality-minimum.

## 1. Short human obstruction

Fix the map of block 0 to be the identity.  Put
\[
 u_i=L_i(1)\quad(i=1,2,3),\qquad
 a=L_4(1),\qquad b=L_4(2).
\]
Every \(u_i,a,b\) is nonzero and \(a\ne b\).  Circuit integrability is
equivalent to
\[
                         b=3+u_1+u_2+u_3.                \tag{1}
\]
Thus there are only 40 reduced possibilities; the factor \(2^3\)
between 40 and 320 comes from the unused second image in blocks 1--3.

For every integrable tuple, the two zero-start circuit walks are
\[
\begin{split}
A={}&[3,\ 3+u_1,\ 3+u_1+u_2,\ b,\ a+b,\ a,\ 0],\\
B={}&[b,\ a+b,\ 3+u_2+u_3+a,\ 3+u_2+a,\ u_2+a,\ a,\ 0].
\end{split}                                               \tag{2}
\]
Both contain \(\{0,a,b,a+b\}=K\).  Translation preserves the number of
colours used, so neither circuit can be deleted.

The four size-two blocks give necessary affine-line conditions on the
relative translation \(z\):
\[
\begin{array}{c|c}
\text{block}&\text{required line containing }z\\ \hline
0&u_2+a+\{0,3\}\\
1&3+a+b+\{0,u_1\}\\
2&3+u_1+u_2+a+\{0,u_2\}\\
3&u_1+u_3+a+\{0,u_3\}.
\end{array}                                               \tag{3}
\]
The first line writes \(z=u_2+a+\varepsilon3\).

If \(\varepsilon=1\), the block-2 condition forces \(u_1=u_2\), and
block 3 forces \(u_3=3\).  Equation (1) then gives \(b=0\), impossible.
If \(\varepsilon=0\), blocks 1 and 3 force respectively
\(u_3=u_1\) and \(u_2=u_1\); block 2 then forces \(u_1=3\), and (1)
again gives \(b=0\).  Hence no clean translation exists.  This proves
the counterstate without trusting the 40-row finite certificate.

`counterstate-certificate.json` records all 40 reduced cases, their two
integrated walks, the five quadratic obstruction bits for each relative
translation, and an exact dual row-subset witness.  `verify.py` also
replays all 1,296 full map tuples directly.

## 2. Simple cubic realization

There is a simple cubic realization on vertices \(0,\ldots,17\).
The two support circuits are
\[
0\,1\,2\,3\,4\,5\,6\,0,\qquad
7\,8\,9\,10\,11\,12\,13\,7.
\]
Add the four edges
\[
0\!-\!11,\quad1\!-\!9,\quad2\!-\!12,\quad3\!-\!10
\]
for partition blocks 0--3.  For block 4, use the internal path
\(14-15-16-17\) and attachments
\[
14-\{4,5\},\quad15-6,\quad16-13,\quad17-\{7,8\}.
\]

`analyze_realization.py` checks directly that the graph is simple,
connected, cubic, and remains connected after every single-edge
deletion.  It verifies the displayed nowhere-zero
\(\mathbb F_2^3\)-flow and recovers the exact boundary partition.

The canonical graph6 encoding is

```text
Qs???SC@GS@_CDOoC@@@?O?CO?g
```

The graph is nonplanar.  A human certificate is the following
subdivision of \(K_{3,3}\), with branch bipartition
\(\{2,10,16\}\mid\{3,9,12\}\):

```text
2--3             2--1--9           2--12
10--3            10--9             10--11--12
16--15--14--4--3 16--17--8--9      16--13--12
```

The nine path interiors are pairwise disjoint.  Independently, nauty
`planarg` classifies the canonical graph as nonplanar.

## 3. Why this is not a FiveCDC counterexample

The graph has cycle-space dimension 10, hence exactly 1,024 binary
cycles.  Exhausting all ordered pairs of low-coordinate cycles gives
66,207 distinct sets of edges simultaneously missed by the two low
coordinates.

For the displayed 14-edge projection:

- there are exactly 15,360 ordered low-cycle extensions;
- zero of them are clean.
- 3,840 have a deletable circuit, 1,920 for each displayed 7-circuit.

So this is a genuinely uncleanable extendable projection, not merely a
bad choice of extension.  But the abstract counterstate concerns the
componentwise-\(\operatorname{GL}(2,2)\) orbit of the displayed
extension: other extensions of the same projection can already enter
the deletion branch.

However, the graph has four cardinality-minimum extendable projections,
all of size 5.  Each has exactly 120 ordered extensions, and all 120
are clean.  The exact supports and counts are frozen in
`realization-analysis.json`.

Thus global cardinality-minimality is precisely the escape from this
counterstate.  The universal boundary lemma is dead, but the weaker
minimum-only route and FiveCDC remain open.

An independently written cycle-space analysis reproduced the canonical
graph, all graph metadata, 15,360/0 target extension counts, the four
size-5 minima, and 66,207 missing-edge sets.  It additionally enumerated
384,064 distinct semantic \((p\cup q,p\cap q)\) low-flow states.

## 4. Reproduction

Primary search:

```sh
clang++ -std=c++20 -O3 -DNDEBUG primary_search.cpp -o primary_search
./primary_search '7+7'
```

The program intentionally terminates on the first counterstate.  Its
first standard-output line is frozen in `primary-output.txt`.

Independent boundary and graph checks:

```sh
python3 verify.py
python3 analyze_realization.py
labelg -q labelled-realization.g6 regenerated-canonical.g6
cmp regenerated-canonical.g6 canonical-realization.g6
planarg -v -q canonical-realization.g6 regenerated-nonplanar.g6
cmp regenerated-nonplanar.g6 canonical-realization.g6
shasum -a 256 -c SHA256SUMS
```

## Scope and disclosure

The counterstate concerns an intermediate lemma in a proposed
minimum-projection approach, not the SAT/XOR formulation of FiveCDC
itself.  It is therefore not evidence of a graph without a five-cycle
double cover.

OpenAI Codex agents under human direction found the state, derived its
short algebraic proof, constructed and independently checked the graph
realization, exhausted its cycle space, and prepared this package.
Every finite claim needed for the result is replayable from included
source and data.  No literature-wide priority claim is made.
