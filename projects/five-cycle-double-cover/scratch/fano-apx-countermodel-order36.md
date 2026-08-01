# A 36-vertex countermodel to the affine pair-exchange axiom

Status: **EXACT AUXILIARY COUNTERMODEL / HUMAN-CHECKABLE FINITE
PROOF / NOT A FIVECDC COUNTEREXAMPLE**.

This note refutes the affine pair-exchange axiom (APX) stated in
`fano-reduced-kp-two-bond-frontier.md`.  Consequently APX cannot be used
to prove the reduced one-switch lemma or the Five-Cycle Double Cover
Conjecture.  The graph itself has the explicit standard five-cycle double
cover in Section 6.

## 1. The exact theorem

> **Theorem.**  There is a simple cyclically 4-edge-connected
> non-3-edge-colourable cubic graph \(G\) and a bad nowhere-zero
> \(\mathbb F_2^3\)-flow \(f\) for which
> \[
> {\cal P}_s\cap{\cal A}_s=\varnothing
> \qquad\text{for every }s\in\mathbb F_2^3-\{0\}.
> \]
> In particular, APX is false.

The graph has graph6 record

```text
chc?GC@@G?_P?H??_?G?@??C??G?@G??C??P??@G?A?__?@_???C???g???GA??@?A??CG???G???GG????C_???@??A??G??A??_???OH
```

and the flow, in standard graph6 upper-triangle edge order, is

```text
3,5,1,6,7,2,4,1,7,6,1,6,3,7,5,2,4,7,
3,5,3,1,2,4,5,4,1,6,5,5,3,5,6,1,6,7,
5,1,2,4,1,6,6,7,1,4,7,6,3,7,5,4,6,2
```

The same two lines are frozen in
`fano-apx-countermodel-order36.txt`.

## 2. Definitions used in the check

For \(s\ne0\), put \(M_s=f^{-1}(s)\).  For every Fano line
\(U=\ker\mu\) containing \(s\), let \(B_U\) be the binary cycle
\[
                     B_U=\{e:\mu(f(e))=1\}.
\]
For \(p=xy\in M_s\), let
\(\tau_U(p)\) be the unordered pair of \(B_U\)-components containing
\(x,y\).  Repetitions are allowed.  Then
\[
\begin{split}
 {\cal A}_s&=\bigcup_{U\ni s}
   \{\{p,q\}\subseteq M_s:\tau_U(p)=\tau_U(q)\},\\
 {\cal P}_s&=\{\{p,q\}\subseteq M_s:
       M_s-\{p,q\}\text{ packs two edge-disjoint boundary }T\text{-joins}\}.
\end{split}
\]

These are exactly the APX definitions.  No proxy relation is used.

The packing test is reduced to a finite binary-cycle test by the following
elementary lemma.

> **Even-marked-circuit lemma.**  Let \(M\) be a matching in a cubic
> graph, \(K=G-M\), and \(T=\partial M\).  Then \(K\) has two
> edge-disjoint \(T\)-joins if and only if \(K\) has a binary cycle \(D\)
> such that every terminal has degree two in \(D\) and every nontrivial
> component of \(D\) contains an even number of terminals.

**Proof.**  If \(J_1,J_2\) are disjoint \(T\)-joins, then
\(D=J_1\dot\cup J_2\) has even degree everywhere.  At a terminal, \(K\)
has degree two and each join has odd degree, so the two incident edges
split between the joins and both lie in \(D\).  On each circuit component
of \(D\), membership alternates between the two joins whenever a terminal
is passed, so the number of terminals is even.

Conversely, orient neither graph.  On every circuit component of \(D\),
start with one of the two joins and swap the assignment of the two
successive arcs at each terminal.  Even terminal parity makes the
assignment close consistently.  Put all edges outside \(D\) in neither
join.  The two resulting edge sets are disjoint, have odd degree exactly
at \(T\), and hence are the desired \(T\)-joins. \(\square\)

Thus nonpacking is certified by enumerating the complete binary cycle
space of \(K\), not by a heuristic SAT cutoff.

## 3. Direct graph and flow checks

Decoding the graph6 word gives 36 vertices and 54 distinct nonloop edges.
Every vertex has degree three and the graph is connected.  The xor of the
three displayed incident values is zero at each vertex, and all values
lie in \(\{1,\ldots,7\}\), so the displayed map is a nowhere-zero
\(\mathbb F_2^3\)-flow.

The independent checker removes every set of one, two, or three edges.
No removal has two cyclic components.  Removing edges
\[
                         \{e_{15},e_{29},e_{36},e_{38}\}
\]
does have two cyclic components.  Hence the cyclic edge connectivity is
exactly four.  A shortest-path calculation gives girth five.

A cubic graph is three-edge-colourable exactly when some perfect matching
has an even-cycle complementary 2-factor.  The checker enumerates all 221
perfect matchings; every complementary 2-factor has an odd circuit.
Therefore \(G\) is non-3-edge-colourable.

All of these checks use only the graph and flow printed above.

## 4. Complete APX table

For each \(s\), the table gives the size of \(M_s\), the number of all
pairs, the number whose deletion packs, the complementary nonpacking
budget \(q_s\), the number of affine-compatible occurrences counted with
their line \(U\), and the number of distinct affine-compatible pairs.
The last column is the number of affine-compatible occurrences whose
deletion packs.

| \(s\) | \(|M_s|\) | all pairs | packing | \(q_s\) | affine occurrences | distinct affine pairs | affine + packing |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 9 | 36 | 6 | 30 | 5 | 5 | **0** |
| 2 | 5 | 10 | 9 | 1 | 0 | 0 | **0** |
| 3 | 6 | 15 | 12 | 3 | 0 | 0 | **0** |
| 4 | 7 | 21 | 10 | 11 | 2 | 2 | **0** |
| 5 | 9 | 36 | 9 | 27 | 4 | 4 | **0** |
| 6 | 10 | 45 | 0 | 45 | 14 | 14 | **0** |
| 7 | 8 | 28 | 11 | 17 | 8 | 7 | **0** |

Every original \(M_s\) is nonpacking, so the flow is bad.  The complete
list of 33 affine-compatible \((s,\mu,\{p,q\})\) occurrences is:

```text
mu=1: (4;23,25),
      (6;3,9) (6;3,32) (6;3,34) (6;3,42)
      (6;9,32) (6;9,34) (6;9,42)
      (6;32,34) (6;32,42) (6;34,42)
mu=2: (5;14,29)
mu=3: (4;6,51),
      (7;4,35) (7;8,13) (7;8,43) (7;13,43)
mu=4: (1;2,33) (1;37,40) (1;37,44) (1;40,44)
mu=5: (5;1,31) (5;19,28),
      (7;4,35) (7;4,43) (7;17,46) (7;35,43)
mu=6: (1;21,26), (6;11,27)
mu=7: (5;24,36),
      (6;32,41) (6;32,52) (6;41,52)
```

The pair \(\{e_4,e_{35}\}\subset M_7\) occurs for two lines; hence there
are 33 occurrences but 32 distinct pairs.  Complete cycle-space
enumeration proves that all 32 reduced matchings are nonpacking.  This is
exactly
\({\cal P}_s\cap{\cal A}_s=\varnothing\) for all \(s\), and proves the
theorem.

The verifier answers all 198 distinct packing queries (the seven original
classes and every pair deletion), enumerating 1,274,117 binary cycles in
total.  The largest cycle-space rank encountered is 16.

## 5. Audit of the global counting route

The countermodel also audits identities (19)--(27) in
`fano-reduced-kp-two-bond-frontier.md`.  With line \(U=\ker\mu\), the
exact local data are:

| \(\mu\) | \(z_U\) | \(a_U\) | \(r_U\) | \(N_U\) | nonzero \(h_{s,U}\) |
|---:|---:|---:|---:|---:|---|
| 1 | 4 | 0 | 2 | 3 | \(h_2=1,h_4=3,h_6=6\) |
| 2 | 7 | 3 | 3 | 6 | \(h_1=3,h_4=1,h_5=3\) |
| 3 | 3 | 1 | 2 | 3 | \(h_3=3,h_4=4,h_7=6\) |
| 4 | 2 | 0 | 3 | 6 | \(h_1=7,h_2=3,h_3=4\) |
| 5 | 4 | 1 | 3 | 6 | \(h_2=1,h_5=5,h_7=5\) |
| 6 | 9 | 7 | 2 | 3 | \(h_1=2,h_6=3,h_7=2\) |
| 7 | 7 | 3 | 2 | 3 | \(h_3=1,h_5=2,h_6=4\) |

The checker directly verifies identities (19)--(23).  The global values
in (25)--(27) are
\[
\begin{gathered}
 A=15,\qquad H=69,\qquad B=90,\qquad Q=134,\\
 L_B(H)=0,\qquad
 \sum_{U,s\in U-\{0\}}L_{N_U}(h_{s,U})=9,\qquad
 3Q=402,\\
 \sum_U r_U=17,\qquad
 g\sum_Ur_U=85\le216=6n.
\end{gathered}
\]
Thus the proved collision lower bounds are far below the literal
nonpacking budget.  No universal estimate strong enough to reverse
(25) or (26) can hold on the APX domain, because this instance satisfies
the entire premise and fails the conclusion.

## 6. Positive FiveCDC and one-switch controls

The following pair label on each edge, in the same 54-edge order, is a
standard five-cycle double cover.  Its five coordinates are
\(\{0,4,5,6,7\}\):

```text
56 05 45 05 57 46 56 05 47 04 07 45 57 45 47 57 56 06
04 47 05 04 45 46 47 07 67 67 06 67 07 06 47 04 06 07
06 67 05 07 07 57 06 05 56 04 46 07 06 57 67 46 45 56
```

Every word has two distinct coordinates.  At every vertex, each coordinate
occurs on zero or two of the three incident edges.  Therefore each
coordinate support is Eulerian and every edge is covered exactly twice.
Their sizes are \(25,19,21,21,22\).  The standard-library checker verifies
these statements directly, without using the Fano flow or APX machinery.

The APX failure also does not refute the broader reduced one-switch lemma.
Switch value \(1\) on the connected circuit
\[
 \{e_0,e_1,e_{17},e_{18},e_{20},e_{22},e_{31},
   e_{45},e_{47},e_{48},e_{49},e_{51},e_{53}\}.
\]
The circuit contains no value-\(1\) edge, so the switch remains nowhere
zero.  In the switched flow, value class \(3\) packs.  The independent
cycle-space checker verifies this particular repair.

A complete C++ audit enumerates all 166,792 simple circuits.  There are
9,532 legal pairs of a circuit and an avoided switch value; 6,699 of them
produce a good flow.  Thus the countermodel is sharply scoped:

- APX fails;
- the same flow is nevertheless one-circuit repairable;
- the same graph has an explicit standard five-cycle double cover.

## 7. Reproduction and independent methods

Run the standard-library verifier:

```bash
python3 scratch/verify_fano_apx_countermodel_order36.py
```

It decodes graph6, checks the premises, enumerates all perfect matchings,
reconstructs every affine-complement component, enumerates every pair,
and applies the even-marked-circuit lemma by complete binary-cycle-space
enumeration.

The independent C++/CaDiCaL implementation uses two disjoint
\(T\)-join variables instead of enumerating binary cycles:

```bash
clang++ -O3 -std=c++20 -I/opt/homebrew/include \
  scratch/search_fano_reduced_one_switch_binary.cpp \
  /opt/homebrew/lib/libcadical.a -o /tmp/search_fano_apx
/tmp/search_fano_apx --apx-neighborhood \
  scratch/fano-apx-countermodel-order36.txt 0 20260728
```

It returns `best_apx_witness_count:0` (and exit status 3, the search
program's countermodel status).  The two verifiers use different exact
packing characterizations.

For the complete one-circuit count, run:

```bash
/tmp/search_fano_apx --circuit-audit \
  scratch/fano-apx-countermodel-order36.txt 0 0
```

The expected totals are `circuits:166792`, `legal_switches_tested:9532`,
and `good_switches:6699`.

The compact frozen result is
`fano-apx-countermodel-order36-result.json`.  Source bindings are:

```text
7df19997f820af9b2a916cafed36c8d891ebc803b769b1a066c67823b9ea5320  scratch/verify_fano_apx_countermodel_order36.py
d2cf3ff53e1108287dbd84ec0fdc99513af0c062a1a149866e09521bf96414e0  scratch/search_fano_reduced_one_switch_binary.cpp
50f74970536e13062a9ac670e2cdbf7452098962a6ca0380654ec2f199a0d856  scratch/fano-apx-countermodel-order36.txt
98a0569ec675179c752533fe431fcf46b5ce89d03fac260c11d39c87b881056a  scratch/fano-apx-countermodel-order36.g6
```

## 8. Scope

This theorem closes one proposed proof route negatively.  APX was only a
sufficient auxiliary statement.  Its failure does **not** imply that the
graph lacks a five-cycle double cover; the explicit positive witness above
proves that this graph has one.

OpenAI Codex agents, under human direction, formulated APX, found this
countermodel by adversarial flow search, wrote both implementations, and
drafted this proof.  The result has not received independent human peer
review.
