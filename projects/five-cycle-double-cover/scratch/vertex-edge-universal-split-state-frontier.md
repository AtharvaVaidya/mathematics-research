# The terminal-distinct vertex/edge split state

Date: **2026-07-27**.

Status: **EXACT ROOTED EQUIVALENCE / LARGE FINITE POSITIVE EVIDENCE /
ADJACENT CASE LOCALLY IMPOSSIBLE / UNIVERSAL THEOREM OPEN**.

This note isolates one especially regular boundary state found in the
five-pole census.  It does **not** prove the Five-Cycle Double Cover
Conjecture.

## 1. Convention and closed-graph meaning

Let \(G\) be a finite loopless cubic graph, let \(v\in V(G)\), and let
\(e=xy\) have both endpoints outside the closed neighbourhood \(N[v]\).
Delete \(v\) and cut \(e\).  The resulting five semiedges terminate at the
three distinct neighbours of \(v\) and at \(x,y\); all five terminal
vertices are distinct.

Write \(D_5=\binom{[5]}2\), normalize
\[
 A=01,\qquad [5]\setminus A=\{2,3,4\},
\]
and prescribe
\[
 q_x=q_y=01,\qquad
 \{q_{N(v)}\}=\{23,24,34\}.                         \tag{1}
\]
The order of the last three labels is immaterial, because a permutation of
\(\{2,3,4\}\) realizes every ordering.

> **Vertex/edge split lemma.**  The five-pole has state (1) if and only if
> \(G\) has a standard 5-CDC in which the two members containing \(e\)
> both avoid \(v\).

**Proof.**  A \(D_5\)-label records the two cover members containing an
edge.  Gluing the two semiedges at \(x,y\) restores \(e\) with label \(01\).
Restoring \(v\) with labels \(23,24,34\) satisfies every coordinate parity:
coordinates \(0,1\) have degree zero at \(v\), and coordinates \(2,3,4\)
each have degree two.  Hence the members \(C_0,C_1\) contain \(e\) and
avoid \(v\).

Conversely, suppose the two members containing \(e\) are \(C_0,C_1\) and
both avoid \(v\).  Then \(q(e)=01\).  The three remaining members account
for six incidences at the cubic vertex \(v\).  Each has even degree, hence
degree two, at \(v\); every star edge is covered twice.  Therefore the
three star labels are exactly \(23,24,34\).  Cutting \(e\) and deleting
\(v\) gives (1). \(\square\)

Thus the natural closed-graph statement is:

> For every admissible pair \((v,e)\), there is a 5-CDC whose two members
> through \(e\) both avoid \(v\).                            \(\tag{VE}\)

This is a prescribed **vertex-and-edge** strengthening of ordinary
FiveCDC.

## 2. Exact matching, four-flow, and \(T\)-join form

The following is the rooted version of the matching/four-flow
characterization.  Put \(T=\partial M=V(M)\) for a matching \(M\), and put
\(K=G-M\).

> **Rooted matching/flow/packing lemma.**  Property (VE) for a fixed
> admissible \((v,e)\) is equivalent to the existence of:
>
> 1. a matching \(M\) with \(e\in M\) and
>    \(M\cap\delta(v)=\varnothing\);
> 2. an \(\mathbb F_2^2\)-flow on \(G\) whose exact zero set is \(M\)
>    (equivalently, a nowhere-zero \(4\)-flow on \(K\)); and
> 3. two edge-disjoint \(T\)-joins \(J_0,J_1\subseteq K\) satisfying
>    \[
>       (J_0\cup J_1)\cap\delta(v)=\varnothing.             \tag{2}
>    \]

**Proof.**  Given the cover in the vertex/edge split lemma, take
\[
 M=C_0\cap C_1,\qquad J_i=C_i-M\quad(i=0,1).
\]
At a cubic vertex a fixed pair label appears at most once, so \(M\) is a
matching.  The standard quotient construction gives an
\(\mathbb F_2^2\)-flow with exact zero set \(M\).  Since each \(C_i\) is
Eulerian,
\[
 \partial J_i=\partial M=T.
\]
The equality \(C_0\cap C_1=M\) makes the joins edge-disjoint.  The two
cover members avoid \(v\), giving (2).

Conversely, define
\[
 C_0=M\mathbin{\dot\cup}J_0,\qquad
 C_1=M\mathbin{\dot\cup}J_1.
\]
Both are binary cycles, their intersection is exactly \(M\), and both
avoid \(v\).  Here is the extension explicitly.  Put
\[
 D_0=C_0\mathbin\triangle C_1\subseteq E(K).
\]
Represent the three nonzero values of \(\mathbb F_2^2\) by \(1,2,3\),
choose the linear section
\[
 s(1)=1100,\qquad s(2)=1010,\qquad s(3)=0110,
\]
and put \(k=1111\).  Let \(\ell(y)\) be coordinate zero of \(s(y)\).  For
each edge of \(K\), set
\[
 h(f)=1_{D_0}(f)+\ell(\phi(f)),\qquad
 d(f)=s(\phi(f))+h(f)k.
\]
Both \(D_0\) and the support of the linear flow coordinate
\(\ell\circ\phi\) are binary cycles, so \(h\) is a binary cycle and \(d\)
is an even-weight four-coordinate flow.  Since \(\phi\) is nonzero on
\(K\), the two vectors in each \(k\)-coset are complementary
weight-two vectors.  Hence the four coordinate supports
\(D_0,D_1,D_2,D_3\) of \(d\) form a 4-CDC of \(K\), with the prescribed
first coordinate because
\[
 d(f)_0=\ell(\phi(f))+h(f)=1_{D_0}(f).
\]

Now \(C_0,C_1,D_1,D_2,D_3\) double-cover \(G\).  An edge of \(M\) lies
only in \(C_0,C_1\).  An edge of \(D_0=C_0\triangle C_1\) lies in exactly
one of \(C_0,C_1\) and exactly one of \(D_1,D_2,D_3\).  Every remaining
edge of \(K\) lies in neither \(C_0,C_1\) and exactly two of
\(D_1,D_2,D_3\).  Thus this is a 5-CDC retaining \(C_0,C_1\).  Since
\(e\in M\), these are precisely the two members through \(e\), and the
vertex/edge split lemma applies. \(\square\)

For completeness, the quotient can be seen directly.  Send colours
\(0,1\) to \(0\in\mathbb F_2^2\) and colours \(2,3,4\) to the three
nonzero values.  Extend linearly to pair labels.  Among the ten labels,
the zero fibre is exactly \(\{01\}\), while \(23,24,34\) map bijectively
to the three nonzero values.  This explains simultaneously the prescribed
zero edge, the zero matching, and the nowhere-zero local flow at \(v\).

## 3. Relation to published “strong 5-CDC” statements

The standard **Strong 5-Cycle Double Cover Conjecture** prescribes an
entire circuit \(C\) and asks for one member of a 5-CDC containing \(C\).
Property (VE) instead prescribes one edge and one distant vertex and
controls both members through the edge.  These are different root
conditions; neither is a reformulation of the other by definition.

Hoffmann-Ostenhof's Theorem 0.4 characterizes when a prescribed
2-regular subgraph lies in one member of a 5-CDC, and Corollary 0.6 gives
the unrooted matching/four-flow/two-cycle characterization.  The lemma
above is exactly Corollary 0.6 with the additional constraints
\[
 e\in C_0\cap C_1,\qquad
 \delta(v)\cap(C_0\cup C_1)=\varnothing.
\]
The published theorem does not supply those extra constraints.

Primary sources checked:

- A. Hoffmann-Ostenhof,
  [*A note on 5-cycle double covers*](https://arxiv.org/abs/1209.0096),
  *Graphs and Combinatorics* 29 (2013), 977--979,
  [doi:10.1007/s00373-012-1169-8](https://doi.org/10.1007/s00373-012-1169-8).
- S. Liu, R.-X. Hao, R. Luo, and C.-Q. Zhang,
  [*5-Cycle Double Covers, 4-Flows, and Catlin Reduction*](https://doi.org/10.1137/22M1472425),
  *SIAM Journal on Discrete Mathematics* 37 (2023), 253--267.

The second paper proves ordinary 5-CDC results for oddness at most four and
several superposition families.  Its stated results do not prescribe the
rooted pair \((v,e)\).  A targeted search of the primary literature found
no named theorem or conjecture with the exact “both members through \(e\)
avoid \(v\)” requirement.  That is evidence of novelty, not a proof that
the formulation has never appeared.

## 4. The repeated-terminal case is a local impossibility

The hypothesis \(x,y\notin N[v]\) is essential.  Suppose, for example,
\(x\in N(v)\).  After deleting \(v\) and cutting \(e\), the terminal
vertex \(x\) receives both:

- an \(01\)-semiedge from \(e\); and
- one of \(23,24,34\) from the deleted star at \(v\).

If \(r\) is the third label at \(x\), vertex parity forces
\[
 r=01\mathbin\triangle 23,\quad
   01\mathbin\triangle 24,\quad\text{or}\quad
   01\mathbin\triangle 34.
\]
Each right-hand side has weight four, whereas every allowed \(D_5\) label
has weight two.  No completion exists.

Therefore the earlier test using merely “\(e\) is nonincident with \(v\)”
was malformed: its first order-34 failure was only this universal local
obstruction.  It is not a strong-snark phenomenon and supplies no
counterexample to FiveCDC.  The corrected closed-neighbourhood exclusion
is the terminal-distinct case.

## 5. Exact finite evidence and its trust boundary

The program
`scratch/five-pole-universal-split-state-census.cpp` fixes every one of
the ten choices of doubled boundary positions and asks CaDiCaL for a
\(D_5\)-labeling.  Complete canonical simple connected
terminal-distinct core streams generated by
\[
 \texttt{geng -Cq -d2 -D3 n (3n-5)/2:(3n-5)/2}
\]
give:

| core order | canonical cores | prescribed-pair SAT checks |
|---:|---:|---:|
| 5 | 1 | 10 |
| 7 | 4 | 40 |
| 9 | 36 | 360 |
| 11 | 379 | 3,790 |
| 13 | 4,794 | 47,940 |
| 15 | 69,243 | 692,430 |
| 17 | 1,109,844 | 11,098,440 |
| **total** | **1,184,301** | **11,843,010** |

Every check was SAT.  In the closed-graph diagnostic
`scratch/cubic-vertex-edge-split-state-census.cpp`, the corrected
terminal-distinct property also passed the retained strong-snark files:

| graph order | source graphs | admissible \((v,e)\) checks |
|---:|---:|---:|
| 34 | 7 | 9,996 |
| 36 | 25 | 40,500 |
| 38 | 298 | 543,552 |

These are positive SAT censuses.  The current run summaries do not retain
all models, so CaDiCaL and the C++ encoder remain in the replay trust base.
They are strong experimental evidence, not proof beyond the finite
generated streams.

## 6. Why this is not yet a structural induction

The data do not provide a reduction map.  In particular:

1. witnesses for adjacent core orders were solved independently rather
   than obtained by extending smaller witnesses;
2. deleting or contracting an ear changes which boundary positions are
   roots, and the prescribed pair need not survive;
3. two- and three-cut gluing needs simultaneous agreement of the rooted
   zero class and of both \(T\)-joins avoiding \(\delta(v)\);
4. a minimum counterexample to (VE) could still possess an ordinary
   5-CDC, so reductions proved only for ordinary FiveCDC do not
   automatically apply; and
5. the universal terminal-distinct five-pole statement itself would imply
   standard FiveCDC by the existing path-extension reduction.

Accordingly, the order-17 and strong-snark results suggest a robust state
but do not presently justify induction.  A sound next theorem would be a
root-preserving ear-extension or cut-gluing lemma.  It must explicitly
transport \(M\), the exact four-flow, and both avoiding \(T\)-joins.

## 7. Independent local audit

The standard-library checker
`scratch/audit_vertex_edge_split_state_equivalence.py` exhausts the finite
local algebra: all 60 ordered cubic \(D_5\) states, the quotient zero
fibre, the complement-triangle coordinate degrees, and the repeated-
terminal obstruction.  Run:

```sh
python3 scratch/audit_vertex_edge_split_state_equivalence.py
```

It can also parse and total the small C++ PASS summaries with repeated
`--census-output` options.  That optional mode checks summary consistency
only; it does not replay the SAT decisions.

## 8. Publication assessment

The exact rooted equivalence, the complete simple-core census through
order 17, and the correction of the repeated-terminal scope look suitable
for a carefully labelled computational research note, especially if the
full positive witnesses are regenerated and independently checked.  They
are not presently a proof paper about FiveCDC: the universal rooted theorem
is open, no induction is known, and the positive census has a solver trust
boundary.

Any preprint should state prominently that OpenAI Codex, under human
direction, formulated the rooted branch, wrote code and prose, and ran or
assisted the computations; it should also invite independent reruns and
human review.

## 9. AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, formulated the rooted
branch, developed the proofs, wrote the programs and prose, and ran or
assisted the finite computations.  Agent cross-checks are not independent
human verification or peer review.  The two displayed equivalences are
included for line-by-line human checking; the census is labelled
separately with its solver and corpus trust boundaries.
