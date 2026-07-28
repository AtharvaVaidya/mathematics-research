# Independent-root feasibility: exact Desargues frontier

Date: **2026-07-28**

Scope: standard, unoriented five-even-subgraph double covers.  This note
does **not** claim a resolution of the Five-Cycle Double Cover Conjecture.
It isolates a proof-grade edge-extension equivalence, records the extra
geometry forced by a minimum counterexample, and reports reproducible SAT
falsification tests.

## 1. Conventions

Write
\[
 D_5=\{a\in\mathbb F_2^5:|a|=2\}.
\]
A \(D_5\)-flow on a loopless cubic graph is a map
\(q:E(G)\to D_5\) such that
\[
                     \bigoplus_{f\ni x}q(f)=0
                     \qquad(x\in V(G)).
\]
For a two-set \(P\subset[5]\), let
\[
 Y_P(q)=\{f:|q(f)\cap P|=1\}.
\]
Coordinate projection shows that \(Y_P(q)\) is even.  Since the graph is
cubic, its nonempty components are circuits.

At a cubic vertex the three labels are necessarily the three two-subsets
of one three-set.  Indeed, if \(a+b+c=0\), then \(c=a+b\); two distinct
weight-two vectors have a weight-two sum exactly when they meet in one
coordinate.

## 2. Edge-adapted reverse-insertion equivalence

Let \(H\) be loopless and cubic and let \(r,s\) be distinct edges.  Form
\(G\) by subdividing \(r,s\) with new vertices \(u,v\), respectively,
and adding \(e=uv\).

> **Theorem 2.1 (edge-adapted equivalence).**  The following are
> equivalent.
>
> 1. \(H\) has a \(D_5\)-flow \(p\) and a two-set \(P\) such that one
>    component of \(Y_P(p)\) contains both \(r\) and \(s\).
> 2. \(G\) has a \(D_5\)-flow \(q\) such that \(u,v\) lie on the same
>    component of \(Y_{q(e)}(q)\).

### Forward proof

Subdivide \(r,s\) and copy the old label to both halves.  Let \(K\) be
the \(Y_P(p)\)-circuit through both roots, and choose either \(u\)-to-\(v\)
arc \(A\) of the subdivided \(K\).  On every edge of \(A\), transpose the
two coordinates in \(P\), and give \(e\) label \(P\).

If a label is active for \(P\), this transposition changes it by xor with
\(P\) and leaves it in \(D_5\).  Every internal vertex of \(A\) sees two
such additions.  Each endpoint sees one addition of \(P\), cancelled by
the new edge label \(P\).  All vertex xors are therefore zero.
Transposition preserves membership in \(Y_P\), while \(e\), whose label
is \(P\), is inactive.  Hence \(u,v\) remain on the same \(Y_P\)-circuit.

### Reverse proof

Put \(P=q(e)\), and let \(K\) be the common \(Y_P(q)\)-circuit through
\(u,v\).  The edge \(e\) is inactive.  Thus at \(u\) the other two labels
are active and have the form \(a,a+P\); the same holds at \(v\).

Choose a \(u\)-to-\(v\) arc \(A\) of \(K\) and transpose the coordinates
in \(P\) on its edges.  Internal vertex xors are unchanged.  At each
endpoint the xor defect is \(P\), exactly the label removed when \(e\)
is deleted.  Moreover, exactly one of \(a,a+P\) was transposed, so the
two surviving labels at that degree-two vertex become equal.  Suppress
\(u,v\), retaining that common label on each restored root edge.
This gives a \(D_5\)-flow on \(H\).  Membership in \(Y_P\) was unchanged,
so suppressing \(K\) gives one factor circuit containing \(r,s\).
\(\square\)

This theorem is stronger than the one-way insertion lemma, but it also
shows why root feasibility is not a harmless local add-on: it is exactly
an edge-extension problem for five-covers, with an explicit adaptation
condition on the extended graph.

## 3. Desargues state and deterministic port routing

At a vertex \(x\), let \(S_x\) be the three-set whose two-subsets are the
three incident labels and put
\[
                         B_x=[5]\setminus S_x.
\]
For an edge \(f\), put \(T_f=[5]\setminus q(f)\).  Then
\[
                         B_x\subset T_f
                         \qquad(f\ni x).
\]
Thus \(B_x\) is a point and \(T_f\) is an incident line of the
\((10_3)\) Desargues configuration.  The three incident lines are
\[
                    B_x\cup\{c\},\qquad c\in[5]\setminus B_x,
\]
so the three elements outside \(B_x\) are literal local port names.

Now consider the inserted edge \(e=uv\), put \(P=q(e)\), and set
\(T_e=[5]\setminus P\).  At either endpoint \(x\in\{u,v\}\),
\[
 B_x\subset T_e,\qquad
 c_e=T_e\setminus B_x,\qquad
 [5]\setminus B_x=P\mathbin{\dot\cup}\{c_e\}.
\]
An incident edge belongs to \(Y_P\) exactly when its port lies in \(P\).
Consequently, the central edge uses port \(c_e\), while the factor
\(Y_P\) deterministically pairs the other two ports, which are the two
elements of \(P\).

> **Port criterion.**  Condition 2 of Theorem 2.1 says precisely that
> the deterministic \(P\)-port routing which avoids the central edge
> returns from \(u\) to \(v\) on one circuit.

There is an equivalent boundary-label version.  A circuit \(K\) is a
component of \(Y_P(q)\) iff, at every vertex of \(K\), the third incident
edge has label \(P\).  Chords of \(K\), if present, are counted as the
third edge at both ends and also have label \(P\).

## 4. Geometry forced by edge elimination

Let \(G\) be simple cubic of girth at least ten, let \(e=uv\), and let
\(H=G\div e\) be obtained by deleting \(u,v\) and replacing their two
remaining incident pairs by root edges \(r,s\).

The roots are independent and \(H\) is simple.  If a circuit of \(H\)
uses \(k\in\{0,1,2\}\) root edges, restoring \(u,v\) turns it into a
circuit of \(G\) of length larger by \(k\).  Hence:

* \(g(H)\ge8\);
* every 8-circuit of \(H\) contains both \(r,s\);
* every 9-circuit of \(H\) contains at least one of \(r,s\).

Equivalently, every path in
\(H-\{r,s\}\) joining an endpoint of \(r\) to an endpoint of \(s\) has
length at least seven, because adjoining its two spokes and \(e\) gives
a circuit of \(G\).

### A connectivity strengthening

The standard fixed-five pasting across a nontrivial 3-edge-cut allows a
minimum counterexample to be chosen cyclically 4-edge-connected.  For
such a \(G\), the reduced graph \(H\) has no 2-edge-cut.

To prove this, let \(\delta_H(A)\) be a 2-cut and let \(t\) be the number
of roots crossing it.

* If \(t=2\), put \(u,v\) on the same shore.  The two split root pairs
  contribute one crossing spoke each and \(e\) is internal, producing a
  2-cut of \(G\).
* If \(t=1\), put the new vertex for the noncrossing root on its root
  shore and put the other new vertex there too.  One old cut edge and
  one crossing spoke produce a 2-cut of \(G\).
* If \(t=0\) and both root pairs lie on the same shore, the old two cut
  edges remain a 2-cut of \(G\).
* If \(t=0\) and the pairs lie on opposite shores, putting \(u,v\) on
  their respective shores gives a 3-cut, with \(e\) as its third edge.
  Both shores contain circuits: in a cubic graph a shore of a 2-cut
  cannot be a tree, since
  \(3|A|=2(|A|-1)+2\) has no solution.  The 3-cut is therefore cyclic,
  contrary to cyclic 4-edge-connectivity.

Thus the root premise needed by the minimum-counterexample induction may
be narrowed from biconnected graphs to **3-edge-connected** simple cubic
graphs with the root-specific 8/9-cycle geometry above.

A similar count shows that every nontrivial 3-cut of \(H\), if present,
must have neither root crossing and must place the two root endpoint
pairs on opposite shores.  Every other placement reconstructs a cyclic
3-cut of \(G\).  The surviving case reconstructs a root-separating
4-cut of \(G\).

## 5. The Tait shortcut and its exact limitation

Suppose the inserted graph \(G\) has a proper 3-edge-colouring in which
the endpoints of \(e\) lie on one component of the two-colour factor
complementary to the colour of \(e\).  Encoding the three colours as the
three labels on a coordinate triangle gives condition 2 of Theorem 2.1,
so \(H\) is root-good.

In particular, a Hamilton circuit of \(G\) avoiding \(e\) supplies such
a colouring: alternate two colours on the circuit and use the third
colour on the complementary perfect matching.

This does not settle the minimum-counterexample case.  In fact, if a
Tait flow on \(H\) made the roots good, the forward construction in
Theorem 2.1 would use only the same three coordinate-triangle labels and
would give a Tait colouring of \(G\).  Therefore, when \(G\) is a snark,
**every Tait flow on \(H\) is necessarily root-bad**.  Any proof must
use a genuinely five-coordinate flow, even when the reduced graph happens
to be 3-edge-colourable.

## 6. SAT falsification tests

The script
`scratch/search_d5_independent_pair_sat.py` generates a CNF asking for a
root-good flow.  It uses:

* exact-weight-two clauses for every edge label;
* the four-clause CNF encoding of cubic xor parity, for each coordinate;
* Tseitin clauses for membership in \(Y_{01}\);
* a layered, active-edge line-graph reachability witness joining the
  roots.

Fixing \(P=01\) loses no solutions because a global \(S_5\) permutation
sends any successful pair to \(01\).  Every SAT model is checked again
directly for weight, vertex xor, and factor connectivity.

Commands:

```text
python3 scratch/search_d5_independent_pair_sat.py \
  --graph tutte-coxeter --all-independent-orbits

python3 scratch/search_d5_independent_pair_sat.py \
  --graph gray --all-independent-orbits
```

Results:

| graph | order | girth | independent root-pair orbits | result |
|---|---:|---:|---:|---|
| Tutte--Coxeter | 30 | 8 | 3 | all SAT |
| Gray | 54 | 8 | 9 | all SAT |

The Tutte--Coxeter instances have 2,295 variables and 7,488 clauses.
The Gray instances have 7,047 variables and 22,224 clauses.  These are
positive witnesses, not a completeness theorem.  No UNSAT certificate
is involved because no candidate counterexample was found.

### A complete girth-ten edge-elimination screen

The frozen 130-vertex, 195-edge graph
`artifacts/structured/graphs/lift13_petersen_girth10.json` has girth ten
and is cyclically 4-edge-connected.  The independent checker enumerates
all its 3-edge-cuts and confirms that all 130 are trivial vertex cuts.
Every one of its 195 edge eliminations was also tested, without
automorphism quotienting.  All 195 reduced root instances are SAT.  Each
has 128 vertices, 192 edges, 38,016 variables, and 116,611 clauses; the
reduced girths are nine or ten.  The complete positive label witnesses
are in
`output/d5-root-feasibility-lift13-girth10/all-eliminations.json`.

The separate checker
`scratch/verify_d5_root_feasibility_lift13_girth10.py` does not import the
producer or trust solver syntax.  It reconstructs all 195 reductions
from the parent graph, checks every weight-two label and vertex xor, and
independently verifies that the two roots lie on one \(Y_{01}\)
component.  It reports:

```text
PASS: 195/195 edge eliminations of the 130-vertex girth-10 cyclically-4
lift have independently verified root-good D5-flow witnesses; reduced
girths are 9 or 10
```

The report SHA-256 is
`31e25fe1fc3cd1cdb844171e33cf7a1788cb2b76464238ef78981f11f0506ea2`.
This is the first complete screen in the project of every edge
elimination of a genuinely girth-ten cubic graph.  It is still one
finite graph, not a proof of the rooted theorem.

## 7. Exact unresolved core

The proof would close if one could establish the following statement.

> Let \(H\) be a 3-edge-connected simple cubic graph with independent
> roots \(r,s\), \(g(H)\ge8\), every 8-circuit containing both roots, and
> every 9-circuit containing at least one root.  If \(H\) has a
> \(D_5\)-flow, then it has one whose deterministic Desargues port routing
> joins \(r\) to \(s\).

Neither the port formulation nor the SAT tests prove this.  Theorem 2.1
shows that asserting it without a new monotone invariant simply restates
the hard edge-extension step.  A valid next proof must therefore provide
one of:

1. a port-routing invariant whose improvement terminates globally;
2. a reducible configuration forced by the root-specific 8/9-cycle
   geometry; or
3. an UNSAT instance with a separately checked proof certificate,
   disproving the root premise (but not automatically disproving
   FiveCDC unless the unreduced graph itself is also certified UNSAT).
