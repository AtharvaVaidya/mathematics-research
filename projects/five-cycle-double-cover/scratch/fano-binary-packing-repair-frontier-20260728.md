# Binary-cycle repair to a packable Fano value class

Date: **2026-07-28**

Status: **UNRESOLVED SUFFICIENT LEMMA / EXACT REFORMULATION AND FINITE
EVIDENCE / NOT A FIVECDC RESOLUTION**.

The Five-Cycle Double Cover Conjecture remains open.  This note isolates a
new, strictly stronger sufficient statement in one fixed
\(\mathbb F_2^3\)-flow and gives its exact SAT formulation.  It also records
the point--line symmetry that reduces 42 ordered repair questions to 21,
and a solver-free positive certificate on a cubic girth-ten graph.

## 1. Setup

Let \(G\) be a finite loopless cubic graph and let
\[
 f:E(G)\longrightarrow \mathbb F_2^3-\{0\}
 \tag{1}
\]
be a flow.  For \(a\ne0\), put \(M_a=f^{-1}(a)\).  At every vertex the
three incident values are distinct and sum to zero, so each \(M_a\) is a
matching.

Say that a matching \(M\) **packs** if \(G-M\) contains two
edge-disjoint \(\partial M\)-joins.  Here \(\partial M\) is the set of
vertices incident with \(M\).

The following implication is elementary and is the reason this packing
test matters.

> **Packable-value lemma.**  If \(M_a\) packs for some value \(a\) of a
> nowhere-zero \(\mathbb F_2^3\)-flow, then \(G\) has a standard
> five-cycle double cover.

To see this, quotient (1) by the line \(\langle a\rangle\).  After deleting
\(M_a\), the quotient is a nowhere-zero \(\mathbb F_2^2\)-flow on
\(G-M_a\).  If \(J_0,J_1\) are the two disjoint
\(\partial M_a\)-joins, then
\[
 A=M_a\mathbin{\dot\cup}J_0,\qquad
 B=M_a\mathbin{\dot\cup}J_1
\]
are binary cycles.  A four-cycle double cover of \(G-M_a\) can be chosen
with \(J_0\cup J_1\) as one coordinate: use the section
\[
 s(1)=1100,\quad s(2)=1010,\quad s(3)=0110
\]
of the quotient by \(1111\), and toggle by \(1111\) on the binary cycle
\((J_0\cup J_1)\mathbin\triangle\operatorname{supp}(s(\phi)_0)\).
Replace that first coordinate by \(A,B\).  The result consists of five
even edge sets and every edge occurs twice.  This is the unrooted case of
the fully written matching/four-flow construction in
`d5-root-good-matching-fourflow-characterization.md`.

## 2. The surviving sufficient statement

For \(t\ne0\), a **legal binary \(t\)-switch** is a binary cycle
\[
 X\in Z_1(G;\mathbb F_2),\qquad X\cap M_t=\varnothing.
 \tag{2}
\]
Its components are edge-disjoint simple cycles.  Replacing \(f(e)\) by
\(f(e)+t\) on \(X\) preserves the flow equations, and (2) prevents a
zero value.

The current proof target is:

> **Binary packing repair conjecture (BPR).**  Let \(G\) be a simple
> cyclically 4-edge-connected non-3-edge-colourable cubic graph of girth
> at least ten.  For every nowhere-zero \(\mathbb F_2^3\)-flow \(f\) for
> which none of \(M_1,\ldots,M_7\) packs, there are distinct nonzero
> \(t,b\) and a legal binary \(t\)-switch \(X\) such that the value class
> \(M_b\) packs after switching.

BPR would prove FiveCDC.  Indeed, take a minimum FiveCDC counterexample
and apply the audited reductions to the displayed graph class.  A
nowhere-zero eight-flow gives (1).  If one current value class packs, the
packable-value lemma is already a contradiction.  Otherwise BPR gives a
new nowhere-zero flow with a packable value class, and the same lemma is
a contradiction.

The girth-ten and cyclic-connectivity restrictions in BPR are used only
through the sourced minimum-counterexample reductions.  No claim is made
for cyclic connectivity five.  BPR is stronger than FiveCDC: it asks for
a packable flow in one binary-switch neighbourhood of an arbitrarily
chosen flow, whereas FiveCDC asks only that some matching/four-flow
certificate exist.

## 3. Exact SAT/XOR formulation

Fix distinct \(t,b\).  Introduce three Boolean variables per edge:
\[
 x_e,\quad r_e,\quad d_e.
\]
The support of \(x\) is the switch \(X\); \(r,d\) are the proposed red
and blue joins.  Put
\[
 m'_e=
 \begin{cases}
 1-x_e,&f(e)=b,\\
 x_e,&f(e)=b+t,\\
 0,&\text{otherwise}.
 \end{cases}
 \tag{3}
\]
This is exactly the indicator that the switched value of \(e\) is \(b\).
The formula is
\[
\begin{array}{ll}
\displaystyle\bigoplus_{e\ni v}x_e=0
   &\text{for every vertex }v,\\[2mm]
x_e=0&\text{when }f(e)=t,\\
\neg r_e\vee\neg d_e&\text{for every edge }e,\\
r_e\le1-m'_e,\quad d_e\le1-m'_e&\text{for every edge }e,\\[1mm]
\displaystyle\bigoplus_{e\ni v}(r_e+m'_e)=0,\quad
\bigoplus_{e\ni v}(d_e+m'_e)=0
   &\text{for every vertex }v.
\end{array}
\tag{4}
\]
All additions in the last line are over \(\mathbb F_2\).

Formula (4) is equivalent to the intended statement.  The first two
lines say that \(X\) is an even subgraph avoiding \(M_t\).  Equation (3)
is the literal switched value class.  The next two lines make the joins
edge-disjoint and keep both in \(G-M'_b\).  The last line says
\(\partial r=\partial M'_b=\partial d\).  Conversely, any switch and
two packed joins assign the variables and satisfy every constraint.

`search_fano_reduced_one_switch_binary.cpp` translates each XOR in (4)
to its complete forbidden-assignment CNF and sends the resulting formula
to CaDiCaL.  Every returned SAT model is immediately checked against the
graph semantics.  Most runs reported below are discovery and
positive-certificate calculations.  The connected UNSAT claim in
Section 6 is treated separately: it has an LRAT checked by two proof
checkers and an independent reconstruction of every CNF clause.

## 4. The 42 queries are 21 point--line incidences

For fixed \(t\), the targets \(b\) and \(b+t\) are equivalent.

Choose a nonzero functional \(\lambda\) with
\[
 \lambda(t)=0,\qquad\lambda(b)=1,
\]
and put \(S=\{e:\lambda(f(e))=1\}\).  Since \(\lambda\circ f\) is a
binary flow, \(S\) is a binary cycle.  It avoids \(M_t\).  If \(X\) is a
legal \(t\)-switch, then so is \(X\mathbin\triangle S\), and
\[
 M_b(f+t1_X)
 =
 M_{b+t}\bigl(f+t1_{X\mathbin\triangle S}\bigr).
\tag{5}
\]
For example, if the left side contains \(e\), then
\(\lambda(f(e))=\lambda(b)=1\), so toggling additionally on \(S\)
changes its switched value from \(b\) to \(b+t\).  The reverse implication
is identical.  Thus the matching, and hence its packing status, is
literally the same.

The unordered pair \(\{b,b+t\}\) is the non-\(t\) part of one Fano line.
Consequently the 42 ordered pairs \((t,b)\), \(t\ne b\), reduce to the 21
incidences between a Fano point \(t\) and a Fano line containing it.
The exact search scores occur in equal pairs, as (5) requires.

## 5. Quotient-and-lift form

Normalize \(t=(0,0,1)\) and write
\[
 f=(\phi,\ell),\qquad \phi:E(G)\to\mathbb F_2^2.
\]
Then \(\phi\) is a binary two-coordinate flow with exact zero set \(M_t\).
The third coordinate \(\ell\) is a binary cycle containing \(M_t\).
Every legal binary \(t\)-switch replaces \(\ell\) by
\(\ell+1_X\), and every lift of \(\phi\) that remains one on \(M_t\)
arises this way.

The other six Fano values form three pairs over the three nonzero values
of \(\phi\).  BPR therefore asks whether, for at least one of the seven
quotient directions \(t\), some lift has a packable half of one quotient
colour class.  This is a compact human formulation of the remaining
selection problem; it is not yet a proof.

## 6. Exact finite reconnaissance

The following searches use complete SAT decisions for each individual
query, but random seeded flow samples rather than complete flow censuses.

| graph source | sampled flows | initially all-seven nonpacking | smallest successful ordered-pair count |
|---|---:|---:|---:|
| 280 retained strict order-26 snarks, seed 20260802 | 84,000 | 1,057 | at least one repair in every case |
| 7 retained strong order-34 snarks | 2,100 | 232 | at least one repair in every case |
| 31 retained order-44 oddness-four snarks | 310 | 76 | at least one repair in every case |

A separate score sample counted all 42 ordered queries:

| source | all-seven-nonpacking states | minimum number of successful ordered queries |
|---|---:|---:|
| strict order 26 | 100 | 38 |
| strong order 34 | 61 | 32 |
| order-44 oddness four | 83 | 30 |

On the retained order-36 APX countermodel, an additional 10,000-flow
sample found 1,371 all-seven-nonpacking states.  The minimum was 30
successful ordered queries; the exact histogram was
\[
\{30:5,\ 32:10,\ 34:42,\ 36:207,\ 38:77,\ 40:239,\ 42:791\}.
\]
The originally displayed APX flow has 34 successful queries.  Its eight
failed ordered pairs reduce, using (5), to four failed point--line
incidences.

An adversarial walk in the same connected order-36 graph subsequently
found the frozen state `fano-binary-repair-score14-order36.txt`.  Exactly
14 of its 21 incidences repair and seven fail.  The failed incidences are
\[
\begin{split}
 &(2,\{2,4,6\}),\\
 &(2,\{2,5,7\}),\ (5,\{2,5,7\}),\ (7,\{2,5,7\}),\\
 &(3,\{3,4,7\}),\ (4,\{3,4,7\}),\ (7,\{3,4,7\}).
\end{split}
\tag{6}
\]
Solver-independent cycle-space enumeration checks all seven failures.
For the seven respective lift fibres it enumerates
\[
 64,\ 128,\ 256,\ 64,\ 1024,\ 128,\ 32
\]
reachable target matchings and finds no packing matching.  The complete
SAT audit finds 28 successful and 14 failed ordered pairs, exactly as the
point--line symmetry predicts.  Repeated hill climbs stopped at the same
score 14, but this is not a proved lower bound.

### Connectivity boundary

First consider the relaxation of BPR obtained by dropping connectedness.
Apply the following three invertible linear relabellings, specified by the
images of the basis \((1,2,4)\), to three disjoint copies of the score-14
state:
\[
 (1,2,4),\qquad(3,4,6),\qquad(7,6,2).
\tag{7}
\]
The three images of the seven incidences in (6) are pairwise disjoint and
partition all 21 Fano incidences.  Binary cycles, target matchings, and
two-join packing all restrict componentwise.  Therefore an incidence can
repair the disjoint union only if it repairs every component, but each
incidence fails in one of the three components.

This gives a 108-vertex disconnected cubic bridgeless counterexample to
the version of BPR with disconnected \(G\).  It is only an auxiliary
counterexample: each component, and therefore their union, has a standard
FiveCDC.  BPR deliberately keeps \(G\) connected while permitting the
switch support \(X\) itself to be disconnected.

In fact, connectedness alone is still insufficient.  Join the three
relabelled copies by two crossed cubic 2-sums, using base edge pairs
\[
              (e_{18},e_{29}),\qquad(e_{31},e_{34}),
\tag{8}
\]
where the middle two edges are in the second copy.  The paired edges
have equal flow values, so the two new cross edges inherit that value and
the flow equations remain valid.  The result is a connected simple
bridgeless cubic graph of order 108.

Unlike the disjoint-union argument, a 2-sum can create cycles and joins
which use both shores, so componentwise failure is not a proof.  The full
selector-gated CNF for all 21 incidences has 10,227 variables and 51,193
clauses and is UNSAT.  CaDiCaL's LRAT is accepted by both `lrat-check`
and the CakeML-generated verified checker `cake_lpr`.  A separately
structured standard-library audit reconstructs the composition, the
flow, every CNF clause, and an explicit standard FiveCDC.

This connected graph has girth five and exactly two cyclic 2-edge cuts.
It therefore refutes connected binary packing repair but remains outside
the cyclically 4-edge-connected, girth-ten BPR domain.  The complete
certificate package is
`search/fano-binary-repair-connected-countermodel-108v-20260728/`.

These data show abundance, not universality.  They neither sample the
minimum-counterexample girth-ten snark domain nor supply a compactness
argument.

### Cyclically-4 boundary

A subsequent fixed-host flow search closes the next relaxed boundary.  The
package
`search/fano-binary-repair-cyclic4-countermodel-144v-20260728/`
contains a simple connected cubic graph of order 144 and a nowhere-zero
\(\mathbb F_2^3\)-flow for which:

- the graph is non-3-edge-colourable and cyclically 4-edge-connected;
- none of the seven initial value classes packs; and
- all 21 normalized binary-cycle repair incidences fail.

The seven initial failures, the 21 repair failures, and non-Taitness have
individual CNFs and 29 LRAT proofs.  Both `lrat-check` and the
CakeML-generated verified checker `cake_lpr` accept every proof.  A
clean-room program reconstructs every CNF clause from the displayed
semantics.  A separate structural checker exhausts every one-, two-, and
three-edge deletion, and an explicit standard FiveCDC is checked directly.

The host has girth **five**.  Thus this is an exact counterexample to the
cyclically-4-only repair statement, but it does not refute BPR as stated in
Section 2 and is not a FiveCDC counterexample.

## 7. A solver-free girth-ten positive control

`order80-girth10-binary-repair-state.txt` freezes one sampled
all-seven-nonpacking flow on the sole order-80 cubic vertex-transitive
girth-ten graph in the retained census.  The exact search reports that
all 42 ordered repair queries are SAT.  Three deterministic MCMC runs
with seeds 20260816--20260818 sampled 163 all-seven-nonpacking states on
this graph; every state again had all 42 queries SAT.

The graph is 3-edge-colourable, so it is not in the non-Tait
minimum-counterexample domain.  Its value here is geometric: the repair
mechanism survives girth ten and cyclic connectivity four.

`verify_order80_girth10_binary_repair.py` uses only the Python standard
library and independently checks:

- the extended graph6 record has 80 vertices and 120 distinct edges;
- the graph is connected, cubic, has girth exactly ten, and has no cyclic
  edge cut of size one, two, or three;
- the retained three-valued flow is a Tait colouring;
- the sampled 120-edge Fano assignment is a nowhere-zero flow;
- the displayed 50-edge \(t=1\) switch is even and avoids \(M_1\);
- after the switch, the displayed red and blue joins are edge-disjoint
  \(\partial M_2\)-joins in \(G-M_2\); and
- the explicit matching/four-flow construction produces five Eulerian
  edge sets covering every edge exactly twice.

Thus one positive repair is a fully human-checkable certificate.  The
solver-free checker deliberately does not claim to prove initial
nonpacking or all 42 SAT answers.

## 8. What remains

A real resolution by this route requires one of:

1. a proof of BPR in the stated reduced graph class;
2. a graph and flow in the stated cyclically-4, girth-ten class for which
   all 21 incidence formulas are UNSAT, with independently checked proof
   certificates, which would refute BPR; or
3. a structural reduction showing that any simultaneous 21-incidence
   obstruction is reducible in a minimum FiveCDC counterexample.

The point--line quotient (5), the lift form, and formula (4) are the
current exact frontier.  No finite search result in this note is promoted
to a universal theorem.

## AI-use disclosure

This formulation, symmetry proof, exact encoding, search program,
certificates, and exposition were developed by OpenAI Codex agents under
human direction.  The mathematical arguments are written out for human
checking.  The conjecture remains unresolved, and none of the empirical
tables has been independently peer reviewed.
