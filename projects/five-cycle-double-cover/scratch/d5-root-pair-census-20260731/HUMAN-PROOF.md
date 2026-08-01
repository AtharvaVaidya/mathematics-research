# Human proof of the certified finite theorem

## 1. Statement

Call a simple cubic graph **independently D5-root-universal** if, for every
two vertex-disjoint edges `r,s`, there is a labeling

\[
    L:E(G)\longrightarrow \binom{[5]}2
\]

such that

\[
    \bigtriangleup_{e\ni v}L(e)=\varnothing
    \qquad\text{at every vertex }v,
\]

and, for some two-set `P` of coordinates, `r` and `s` lie on the same
component of

\[
    Y_P=\{e:|L(e)\cap P|\text{ is odd}\}.
\]

**Certified finite theorem.** Every simple cyclically 4-edge-connected cubic
graph of order at most 28 is independently D5-root-universal.

The theorem is conditional only on the documented completeness and option
semantics of the retained Snarkhunter streams.  All graph-dependent claims
after that source boundary have literal witnesses and a separate checker.

## 2. Why a displayed labeling is a five-cycle double cover

For coordinate `i`, let

\[
    C_i=\{e:i\in L(e)\}.
\]

Every label has size two, so every edge belongs to exactly two of the five
sets `C_i`.  The symmetric-difference equation at a vertex says, coordinate
by coordinate, that the degree of that vertex in each `C_i` is even.  Thus
each `C_i` is an Eulerian edge-subset and `(C_0,...,C_4)` is a five-cycle
double cover in the Eulerian-subgraph formulation.  Empty coordinates cause
no problem and express the standard “at most five” convention.

For `P={a,b}`, the factor `Y_P` is `C_a` symmetric-difference `C_b`.
Consequently it is Eulerian.  In a cubic graph every vertex has degree zero
or two in `Y_P`, so each nonempty component is a circuit.  Hence placing
`r,s` in one component is exactly the rooted condition required by the
edge-insertion reduction.

## 3. The Tait-colourable case

The prescribed-Tait-factor theorem in the accompanying preprint proves more:
in a 2-connected Tait-colourable cubic graph, any prescribed circuit can be
made exactly one factor of a D5 flow.  Any two edges of a 2-connected graph
lie on a common circuit.  A cyclically 4-edge-connected cubic graph is
2-connected: a bridge shore in a cubic graph necessarily contains a circuit.
Therefore every Tait-colourable graph in the present domain is independently
D5-root-universal.  This part is analytic and uses no census.  The Petersen
graph is the smallest bridgeless non-Tait cubic graph, so the non-Tait source
boundary begins at order ten.

## 4. The non-Tait source boundary

For even orders from 10 through 28, the retained command

```text
snarkhunter n 4 S s C4 o g
```

produces respectively

| order | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| non-Tait graphs | 1 | 0 | 0 | 0 | 2 | 6 | 31 | 155 | 1,297 | 12,517 |

The retained logs, source hashes, distinct-row checks, and independent
classification are audited by
`../../search/focused-theta-choice-through28-20260727/verify.py`.  Thus the
non-Tait part contains 14,009 graphs.  A simple cubic graph of order `n` has
`3n/2` edges and exactly

\[
    \binom{3n/2}{2}-3n
\]

independent unordered edge pairs: from all edge pairs, subtract the three
pairs meeting at each vertex.  Summing over the retained streams gives
10,689,351 root pairs.

## 5. What the compact certificate checks

The three `compact-witnesses-*.json*` files contain, for each of the 14,009
graph rows, a short list of edge-label vectors.  There are 30,858 vectors in
total.  The independent program `check_compact_certificate.py` performs
these steps on each file:

1. hash and parse each referenced graph6 stream without importing generator
   code;
2. check that each graph is simple and cubic and agrees with the recorded
   graph digest;
3. check that every edge label is a two-subset of five coordinates;
4. XOR the three labels at every vertex and require zero;
5. for each of the ten coordinate pairs, construct `Y_P`, require local
   degree zero or two, and find all its connected components;
6. enumerate every independent edge pair and require that at least one
   displayed flow and one of its ten factors contains both roots in one
   component;
7. recompute the block totals, whose sums are 14,009 graphs, 10,689,351
   root pairs, and 30,858 flows.

These checks prove the non-Tait part by direct positive witnesses.  Together
with Section 3 and the canonical source boundary in Section 4, they prove the
stated finite theorem.

## 6. What is not proved

This theorem stops at order 28.  It does not establish the universal rooted
theorem, does not remove the cyclically 4-edge-connected/simple/cubic
hypotheses, and therefore does not resolve FiveCDC.  No negative solver
answer occurs here, so no UNSAT certificate is claimed or needed.  The
priority of this precise finite rooted census has not been established by a
complete literature review.  A slower pair-by-pair SAT run was also
performed through order 24; it is a cross-check, not an input to the compact
positive-certificate proof.

## 7. AI disclosure

OpenAI Codex agents proposed this census, wrote the generator and independent
checker, ran the computations, and drafted this proof.  Human checking is
invited at the three explicit boundaries: the Tait theorem, the Snarkhunter
source provenance, and the literal witness checker.  The fact that AI was
used is not evidence for any mathematical assertion.
