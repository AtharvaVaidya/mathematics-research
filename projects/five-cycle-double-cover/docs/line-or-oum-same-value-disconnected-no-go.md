# A disconnected no-go for same-value line-or-Oum repair

Date: 2026-07-28

Status: **EXACT COUNTERMODEL TO AN AUXILIARY ONE-SWITCH LEMMA / NOT A
FIVE-CYCLE DOUBLE COVER COUNTEREXAMPLE / CONNECTED REDUCTION UNAFFECTED**.

## 1. The assertion tested

Let \(W=\mathbb F_2^3\), and let
\[
        \phi:E(G)\longrightarrow W-\{0\}
\]
be a nowhere-zero flow on a loopless cubic graph.  For \(t\ne0\), put
\(M_t=\phi^{-1}(t)\).  If \(Q\) is a binary cycle in \(G-M_t\), then
\[
 \phi^{t,Q}(e)=
 \begin{cases}
 \phi(e)+t,&e\in Q,\\
 \phi(e),&e\notin Q
 \end{cases}
\tag{1}
\]
is again a nowhere-zero \(W\)-flow.

The finite strict-snark census suggested the following auxiliary
disjunction:

> **Same-value line-or-Oum repair assertion.** If \(\phi\) initially has
> neither a clean Fano line nor a five-colourable compatible Oum cover,
> then there are one value \(t\ne0\) and one nonempty binary cycle
> \(Q\subseteq G-M_t\) for which \(\phi^{t,Q}\) has at least one of those
> two properties.

Here a binary cycle may be disconnected, but the same value \(t\) is used
on all of its circuit components.  This note disproves the assertion when
\(G\) is allowed to be disconnected.  It does not disprove a connected or
cyclically highly connected version.

## 2. The two sufficient properties

For a nonzero functional \(\mu\in W^*\), let
\[
       L_\mu=\ker\mu-\{0\},\qquad
       F_\mu=\{e:\phi(e)\in L_\mu\}.
\]
For each component \(K\) of \(F_\mu\), conservation says that the four
values outside \(\ker\mu\) occur on \(\delta(K)\) with one common parity.
The line is *clean* when this parity is zero for every component.  This is
exactly the weight-two \(D_5\)-lifting condition used elsewhere in the
project.

An Oum-compatible potential is a vector \(p_v\in W\) at every vertex such
that, for each edge \(e=uv\),
\[
 p_u+p_v+\phi(a_{u,e})+\phi(a_{v,e})
            \in\langle\phi(e)\rangle,                 \tag{2}
\]
where \(a_{v,e}\) is either of the other two edges at \(v\).  It gives the
two-point edge label
\[
 P_e=p_u+\phi(a_{u,e})+\langle\phi(e)\rangle.          \tag{3}
\]
The eight coordinate subgraphs defined by these labels form an
eight-cycle double cover.  They can be purely merged into at most five
coordinates exactly when the coordinate co-occurrence graph on \(W\) is
five-colourable.

Both properties are sufficient for a standard five-cycle double cover.
Their failure for one fixed flow is not a graph obstruction to FiveCDC.

## 3. Seven fixed-value blocks

Every block uses the same 18-vertex graph

```text
Q???C@?GCoOoDO[?CcAO_?k?J??
```

with edges in lexicographic endpoint order.  The independent checker
verifies directly that this graph is simple, connected, cubic, bridgeless,
has girth five, has no cyclic edge cut below four, and is not
three-edge-colourable.

For switch value \(t=1,\ldots,7\), use the following flow row:

```text
t=1: 1 2 3 1 4 5 3 1 2 1 4 5 3 4 7 4 3 7 7 6 1 7 6 5 4 1 2
t=2: 1 2 3 4 3 7 2 5 7 4 2 6 6 1 7 2 7 5 1 2 3 5 4 2 6 6 4
t=3: 1 2 3 4 7 3 2 3 1 3 7 4 1 5 4 6 5 3 5 2 7 2 3 2 6 6 4
t=4: 1 2 3 2 4 6 6 1 7 4 1 5 6 4 2 7 4 3 4 2 6 5 4 4 6 2 4
t=5: 1 2 3 4 5 1 2 7 5 5 7 2 7 5 2 1 2 3 2 4 6 5 4 6 2 4 6
t=6: 1 2 3 4 1 5 2 7 5 7 1 6 5 1 4 5 6 3 6 4 2 7 6 6 2 4 6
t=7: 1 2 3 3 4 7 6 5 3 4 5 1 6 5 3 4 3 7 7 3 4 6 7 4 7 2 4
```

The checker verifies the following finite statement for every row.

1. The displayed values are nonzero and xor to zero at every vertex.
2. All seven Fano lines are initially dirty.
3. After fixing one vertex potential to zero, the complete solution space
   of (2) has respectively \(1,1,2,4,2,1,2\) elements.  Every resulting
   co-occurrence graph contains a \(K_6\).
4. The dimensions of the cycle spaces of \(G-M_t\) are respectively
   \(4,4,4,2,5,4,5\).  Thus there are only
   \(15,15,15,3,31,15,31\) nonzero switch cycles to test.
5. For every one of those 105 cycles, the switched flow has all seven
   Fano lines dirty.
6. Exhausting every gauged compatible potential after every switch gives
   \(15,15,18,12,46,15,62\) potential states in the seven rows.
   Every one contains a coordinate \(K_6\), so none is five-colourable.

The \(K_6\) certificates make the negative colouring decisions immediate:
six mutually adjacent coordinate points require six different colours.

## 4. The 126-vertex countermodel

Let \((G_t,\phi_t)\) be the block in row \(t\), and take the disjoint union
\[
              (G,\phi)=\coprod_{t=1}^7(G_t,\phi_t).
\]
Then \(G\) is a finite simple bridgeless cubic graph with 126 vertices and
189 edges.

Initially, every block has all seven lines dirty.  Since the factor
components of a disconnected union remain in their own graph components,
no Fano line is clean globally.  Every compatible global Oum potential
restricts on each block to a compatible block potential, up to a common
translation of its eight coordinate names.  A translation preserves
\(K_6\), so the global co-occurrence graph is not five-colourable.

Now choose any proposed switch value \(t\ne0\) and any nonempty binary
cycle \(Q\subseteq G-M_t\).  Its restriction \(Q_t=Q\cap E(G_t)\) is a
binary cycle in \(G_t-M_t\), possibly empty.

- If \(Q_t=\varnothing\), the initial certificate for block \(G_t\)
  survives unchanged.
- If \(Q_t\ne\varnothing\), the exhaustive fixed-\(t\) certificate says
  that the switched block still has all seven lines dirty and every
  compatible Oum potential still contains \(K_6\).

Thus the \(t\)-th block prevents both sufficient branches after every
global same-\(t\) switch.  Since this holds for all seven choices of \(t\),
the same-value line-or-Oum repair assertion is false.

## 5. Exact scope and consequence

This countermodel identifies a quantifier error:

\[
  \forall\text{ connected components }H\ \exists t_H
  \quad\not\Rightarrow\quad
  \exists t\ \forall H .
\]

The result therefore forces any use of this route to occur only after a
sound connected/minimum-counterexample reduction, or to permit different
switch values on different connected components.  Each individual block
is cyclically four-edge-connected, but their disjoint union is not
connected.  Nothing here refutes the still-surviving strict connected
version suggested by the order-20 and sampled order-28--36 computations.

The graph itself is not a FiveCDC counterexample.  This result only says
that one particular fixed-flow repair mechanism cannot be asserted in
unrestricted componentwise form.

## 6. Reproduction

Discovery certificate:

```bash
python3 scratch/search_line_or_oum_fixed_value_blocks.py \
  search/order22-filter-census-20260725/strict-snarks-through18.g6 \
  --output scratch/line-or-oum-fixed-value-blocks-through18-20260728.json
```

Independent semantic replay:

```bash
python3 scratch/check_line_or_oum_disconnected_countermodel.py
```

The replay reimplements graph6 decoding, graph checks, flow conservation,
binary cycle-space enumeration, clean-line defects, the complete binary
linear potential solver, pair-label reconstruction, \(K_6\) detection, and
five-colouring.  Its frozen output ends with `"status": "PASS"`.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the fixed-value
block search, found the seven finite witnesses, implemented the independent
semantic checker, proved the disjoint-union implication above, and drafted
this note.  The finite records and all algorithms are exposed for human
inspection and independent rerunning.  This is not human peer review and
is not a claim that the Five-Cycle Double Cover Conjecture has been
resolved.
