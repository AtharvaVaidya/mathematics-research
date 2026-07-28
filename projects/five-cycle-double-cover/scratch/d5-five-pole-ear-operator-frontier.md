# The \(D_5\) five-pole open-ear frontier

Status: **human-checkable structural lemmas, exact finite semigroup
audits, and an abstract countermodel to coarse invariants**.

This note does not prove or disprove the Five-Cycle Double Cover
Conjecture.  It does not prove the universal 46-orbit five-pole statement,
and its abstract countermodel is not claimed to be realizable by a graph.
Nothing here concerns the orientable five-CDC variant.

## 1. Boundary convention

Let

\[
\Gamma=\{x\in\mathbb F_2^5: |x|\text{ is even}\},\qquad
B=\{x\in\Gamma:|x|=2\}.
\]

Thus \(|\Gamma|=16\) and \(|B|=10\).  A \(B\)-flow assigns a value in \(B\)
to every proper edge and semiedge, with xor zero at each vertex.  At a
cubic vertex, three \(B\)-values xor to zero exactly when they are the
three edges of a triangle on the five color vertices.

For \(k\) ordered semiedges, put

\[
U_k=\{(q_1,\ldots,q_k)\in B^k:q_1\oplus\cdots\oplus q_k=0\}.
\]

For five semiedges,

\[
|U_5|=6240,
\]

and the global \(S_5\)-action on colors has 62 orbits.  For four
semiedges, \(|U_4|=640\) and there are 10 color orbits.

The five-cycle pole admits 4,620 words in 46 color orbits.  The four-cycle
pole admits 580 words in 9 color orbits.

The orbit and ordered-word lower bounds are logically different.  The
five-boundary orbit sizes are 60 for the \(A,C\) multiset types and 120
for the \(B,D\) types.  Thus 46 arbitrary orbits can contain only 4,320
words, while 4,620 words need not occupy 46 orbits.  The five-cycle
relation happens to attain both proposed bounds simultaneously.

## 2. Why open ears apply

Let \(P\) be a connected internally bridgeless proper pole core in which
every degree is two or three.

**Lemma 2.1.** \(P\) has no cut vertex.

**Proof.**  If \(v\) were a cut vertex, every component of \(P-v\) would
have at least two edges to \(v\); otherwise its unique edge to \(v\) would
be a bridge.  There are at least two components, forcing
\(\deg_P(v)\ge4\), contrary to subcubicity. \(\square\)

Consequently \(P\) is 2-vertex-connected.  The standard Whitney
open-ear theorem constructs it from a cycle by repeatedly adjoining a
path whose distinct endpoints are old vertices and whose internal
vertices are new.

To make this construction compatible with poles, attach one formal port
at every unit of unused cubic degree in the current partial graph.  Adding
an ear consumes the ports at its two endpoints.  Each internal ear vertex
has proper degree two when it is created, so it contributes one new port.
At the end, the remaining ports are precisely the semiedges of the pole.

## 3. Exact ear-addition operator

Let \(R\subseteq U_k\) be the boundary relation of the current partial
pole.  Choose two port positions \(a,b\).  Add an open ear

\[
u=w_0,w_1,\ldots,w_m,w_{m+1}=v
\]

with \(m\) internal vertices.  Write \(y_0,\ldots,y_m\in B\) for the
values on its \(m+1\) proper edges, and \(z_i\in B\) for the new port at
\(w_i\), \(1\le i\le m\).

**Ear operator lemma.**  The new boundary relation is

\[
\begin{split}
E_m^{a,b}(R)=\{&(q_j)_{j\ne a,b},z_1,\ldots,z_m:\ q\in R,\\
&y_0=q_a,\ y_m=q_b,\quad
z_i=y_{i-1}\oplus y_i\in B\ (1\le i\le m),\\
&y_i\in B\ (0\le i\le m)\}.
\end{split}                                                   \tag{1}
\]

**Proof.**  At endpoint \(u\), replacing its old port by the first ear
edge preserves the old vertex equation only when \(y_0=q_a\).  Similarly
\(y_m=q_b\).  The equation at internal vertex \(w_i\) is

\[
y_{i-1}\oplus y_i\oplus z_i=0,
\]

so \(z_i=y_{i-1}\oplus y_i\).  All values must lie in \(B\).  Conversely,
these equations extend the old flow across every new vertex, proving
both inclusions. \(\square\)

Equivalently, \(y_0,\ldots,y_m\) is a length-\(m\) walk in

\[
T(5)=L(K_5),
\]

because two members of \(B\) have xor in \(B\) exactly when the
corresponding \(K_5\)-edges share one endpoint.  The new value \(z_i\) is
the third edge of the resulting \(K_5\)-triangle.

For \(m=0\), the new ear is one edge and (1) keeps only states with
\(q_a=q_b\).  For \(m=1\), it keeps only states with
\(q_a\oplus q_b\in B\), replacing the two labels by that xor.  For each
fixed output value in the \(m=1\) case there are exactly six ordered
endpoint pairs: choose the third triangle color in three ways and order
the two incident edges.

The executable audit gives the complete row- and column-degree profiles
of this local channel for \(0\le m\le5\).  Already the first cases show
the obstacle to a scalar induction:

| \(m\) | supported endpoint pairs | row degrees | output column degrees |
|---:|---|---|---|
| 0 | 10 equal pairs | 1 | 10 |
| 1 | 60 pairs sharing one color | 1 | 6 |
| 2 | all 100 pairs | 6 on equal, 3 on sharing, 4 on disjoint | the same profile |

For \(m\ge3\), collision multiplicities become still more nonuniform.

## 4. Exact abstract countermodel to coarse induction

This section concerns an abstract color-invariant subset of \(U_5\), not
a graph pole.

Fix boundary positions 0 and 1 and define the partial \(m=1\) map

\[
\phi(q_0,\ldots,q_4)
  =(q_2,q_3,q_4,q_0\oplus q_1)
\]

when \(q_0\oplus q_1\in B\).  Let \(S\subseteq U_4\) be the union of the
five color orbits represented, in hexadecimal bit-mask notation, by

\[
\begin{split}
&(03,03,03,03),\quad (03,05,03,05),\quad(03,05,05,03),\\
&(03,05,0a,0c),\quad(03,05,0c,0a).
\end{split}
\]

Their ordered orbit sizes are \(10,60,60,120,120\), so \(|S|=370\).
Now set

\[
R=\{q\in U_5:q_0\oplus q_1\notin B\}
  \ \cup\ \phi^{-1}(S).                                     \tag{2}
\]

The first set in (2) consists of the states whose first two labels are
equal or disjoint.  It has 2,400 words in 25 color orbits.  Every word of
\(S\) has exactly six lifts through \(\phi\), and the five selected output
orbits split into 21 input color orbits.  Therefore

\[
|R|=2400+6\cdot370=4620
\]

and \(R\) has exactly \(25+21=46\) color orbits.

The direct audit additionally verifies:

1. every two-coordinate projection of \(R\) is all of \(B^2\), hence has
   size 100;
2. \(R\) meets each of the twelve five-cycle-cap relations, with
   intersection sizes
   \[
   33,37,33,37,33,33,35,35,32,35,35,32;
   \]
3. \(R\) passes the elementary bichromatic-switch closure test used in
   the existing five-cycle boundary calculus; and
4. its ear image is exactly
   \[
   E_1^{0,1}(R)=S,
   \]
   with only 370 words in five color orbits.  The image passes the same
   elementary single-pair switching test.

Thus the exact proposed thresholds, normalized density, log-support,
full pair projections, cap intersections, and the elementary
single-bichromatic-pair closure do not form an inductive invariant under
the exact ear operator.  Numerically, density drops from

\[
\frac{4620}{6240}\approx0.74038
\quad\text{to}\quad
\frac{370}{640}=0.578125,
\]

and maximum support entropy drops from \(\log_2 4620\) to
\(\log_2 370\).

This does **not** refute the 46-state conjecture.  Relation \(R\) is not
known or claimed to be graph-realizable.  In particular, this audit does
not encode the simultaneous-switch and internal bichromatic-path
intersection topology highlighted in the realizability frontier.  It
shows precisely why a proof must retain richer decorated information.

## 5. Positive finite semigroup theorems

The same audit proves two restricted, but infinite, graph-family
statements.

### 5.1 Repeated two-internal-vertex ears

Start from the five-cycle pole and repeatedly add an ear with exactly two
internal vertices between any two current terminals.  This operation
keeps five boundary ports.

Modulo color and terminal permutations, the complete reachable relation
semigroup has only seven states.  Their orbit supports are

\[
46,\ 57,\ 58,\ 58,\ 60,\ 61,\ 62.
\]

The seven-state transition table is emitted by the checker.  Hence every
pole in this infinite ear-generated family has at least 46 boundary
orbits.  This is an exact induction over a finite transition table, not a
bounded-order graph census.

### 5.2 Ears of sizes one through three in the \(4/5/6\)-port band

Start again from the five-cycle pole.  Allow ears with one, two, or three
internal vertices, subject to every intermediate boundary size belonging
to \(\{4,5,6\}\).

The complete semigroup contains 72 canonical relations:

\[
3\text{ with four ports},\qquad
9\text{ with five ports},\qquad
60\text{ with six ports}.
\]

The five-port support profile is

\[
\{46:1,\ 56:1,\ 57:1,\ 58:2,\ 60:2,\ 61:1,\ 62:1\}.
\]

Thus every five-pole in this second infinite family also satisfies the
46-orbit bound.

These families do not cover a general open-ear decomposition.  A general
decomposition may start with a cycle of another length, use a
zero-internal-vertex ear or an ear with at least four internal vertices,
and pass through boundary sizes outside \(\{4,5,6\}\).  For a final
five-pole, deleting its last ear can expose any predecessor boundary size
from two through seven.  The missing universal invariant must therefore
handle those larger state spaces or prove a sound ear-reordering theorem.

## 6. Relevant primary literature

The \(B\)-flow formulation and its contractor are prior work.  Garijo,
Goodall, and Nešetřil, *Contractors for flows*, specialize their general
Fourier theory in Section 5.4.4 to

\[
B=S_2^5\subseteq\mathbb F_2^5.
\]

They identify this \(B\)-flow with a five-colorable cycle double cover.
The Cayley graph has two isomorphic components and eigenvalues
\(10,2,-2\).  Their explicit contractor is

\[
\frac16\,[C_2-4\overline K_2],
\]

giving the closed-graph counting identity

\[
F_B(G\parallel e)=4F_B(G-e)+6F_B(G/e).
\]

See [Garijo--Goodall--Nešetřil, arXiv:1011.5958,
Section 5.4.4](https://arxiv.org/abs/1011.5958).
This identity concerns the **number** of closed-graph \(B\)-flows.  Its
negative contractor coefficient and its lack of boundary support data
mean that it does not imply a 46-orbit or 4,620-word lower bound.

Máčajová, Mazzuoccolo, and Tabarelli define the same two-subset
CDC-coloring of multipoles and develop bichromatic-chain switches in
Definition 3.1 and Section 3.1 of
[*Cycle separating cuts in possible counterexamples to the cycle double
cover and the Berge--Fulkerson conjectures*](https://doi.org/10.26493/1855-3974.3409.c13),
*Ars Mathematica Contemporanea* 26 (2026), P2.03.  Their Remark 3.2
separates the five-color specialization from unrestricted CDC while
showing that their four-cut restrictions apply to FiveCDC.  Their
five-pole section studies the different six-color Berge--Fulkerson
boundary problem, not the present standard \(D_5\) five-pole threshold.

The ear construction uses Whitney's classical synthesis of nonseparable
graphs; see [Whitney, *Non-Separable and Planar Graphs*, Trans. AMS 34
(1932), 339--362](https://doi.org/10.1090/S0002-9947-1932-1501641-2).

No theorem located in these primary sources gives the proposed universal
46-orbit/4,620-word support bound.

## 7. Reproduction

Quick audit:

```sh
python3 scratch/audit_five_pole_ear_operator.py \
  > /tmp/d5-ear-quick.json
```

Extended 72-state semigroup audit:

```sh
python3 scratch/audit_five_pole_ear_operator.py --extended \
  > /tmp/d5-ear-extended.json
```

Independent replay of the abstract countermodel:

```sh
python3 scratch/verify_d5_ear_countermodel_independent.py \
  > /tmp/d5-ear-countermodel-independent.json
```

The script uses only the Python standard library.  It reconstructs every
boundary universe, orbit, cap relation, ear kernel, abstract countermodel,
and finite transition semigroup from definitions.  The independent
countermodel replay imports neither the primary audit nor another project
module and recomputes its 6,240-word universe directly.

## 8. AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, derived the operator,
constructed the abstract countermodel, wrote both audit programs, ran the
finite computations, and drafted this note.  Agent-to-agent agreement is
not independent human verification or peer review.  The operator proof is
displayed for line-by-line human checking; the countermodel and restricted
semigroups are reproducible from the retained standard-library programs.
