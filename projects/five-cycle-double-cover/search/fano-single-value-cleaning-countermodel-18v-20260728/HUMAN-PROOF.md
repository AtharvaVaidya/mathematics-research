# An 18-vertex countermodel to single-value fixed-line cleaning

Date: **2026-07-28**.

Status: **THE SUFFICIENT LEMMA BELOW IS FALSE / THIS IS NOT A
COUNTEREXAMPLE TO FIVE-CDC**.

## 1. The exact sufficient lemma and why it would have worked

Let \(\phi:E(G)\to W-\{0\}\), \(W=\mathbb F_2^3\), be a flow.  For a
nonzero functional \(\mu\), write
\[
 L=\ker\mu-\{0\},\qquad F_\mu=\{e:\phi(e)\in L\}.
\]
Index the components of \(F_\mu\).  On each component the four affine
values \(a\notin L\) have one common boundary parity.  The vector of these
parities is \(r_\mu\).

For \(0\ne t\in L\), let \(M_t=\{e:\phi(e)=t\}\).  If \(C\) is any binary
cycle in \(G-M_t\), switching
\[
             \phi'(e)=\phi(e)+t\,1_C(e)                 \tag{1}
\]
preserves conservation and nowhere-zeroness.  Direct boundary counting
gives
\[
             r_\mu(\phi')=r_\mu(\phi)+\tau_t(C).        \tag{2}
\]
The support \(C\) may be disconnected: its edge-disjoint circuit
components can be switched one at a time, and all continue to avoid
\(M_t\).

Here is the claimed sufficient lemma that this record refutes:

> If every Oum-compatible cover of \(\phi\) has non-5-colourable
> coordinate co-occurrence graph, then some \(\mu\ne0\) and
> \(0\ne t\in\ker\mu\) satisfy \(r_\mu\in\operatorname{im}\tau_t\).

The conclusion really would yield a standard five-cycle double cover of
\(G\).  Choose \(C\) with \(\tau_t(C)=r_\mu\).  Equations (1)--(2) give
\(r_\mu(\phi')=0\).  To see the lift explicitly, put
\[
 E_5=\{x\in\mathbb F_2^5:|x|\text{ is even}\},\quad
 D_5=\{x\in E_5:|x|=2\}.
\]
Quotient \(E_5\) by a weight-four vector \(\kappa\).  The three nonzero
quotient values with two representatives in \(D_5\) form a Fano line;
the other four values have one forced representative.

For every component of the line-valued factor, conservation makes the
parities of the four forced affine classes equal.  Thus \(r_\mu=0\) is
exactly the condition that the forced lift bits extend over that component.
Choose the remaining bits on a spanning tree.  The resulting
\(q:E(G)\to D_5\) is conserved.  For \(i=1,\ldots,5\), set
\[
             C_i=\{e:q(e)_i=1\}.
\]
Every \(C_i\) is Eulerian because \(q\) is conserved, and every edge is in
exactly two \(C_i\) because every \(q(e)\) has weight two.  Empty
coordinates are allowed, so this is the ordinary “at most five” FiveCDC.

Likewise, a 5-colouring of an Oum coordinate co-occurrence graph merges
its eight Eulerian coordinates into at most five without identifying the
two labels on any edge.  Consequently the easy Oum branch or the claimed
cleaning branch would prove FiveCDC for each graph in the stated domain.
Passing from that domain to all finite bridgeless graphs still requires
the separate exact cubic/cut reductions; none is asserted here.

## 2. The countermodel

The graph has canonical graph6 record

```text
Q???C@?GCoOoDO[?CcAO_?k?J??
```

The 27-edge list is in `construction.json`.  In edge-ID order, take
\[
\phi=(1,2,3,4,3,7,2,6,4,6,3,5,4,1,5,2,4,6,1,2,3,7,6,2,6,6,4).
\]
At every vertex the three displayed values XOR to zero.  The independent
checker also verifies directly that the graph is simple, cubic,
bridgeless, cyclically 4-edge-connected, and non-Tait.

### Oum-hard premise

Use one three-bit vertex potential \(p_v\) at each vertex and fix
\(p_0=0\).  Edge compatibility supplies two independent scalar equations
per edge.  The resulting 57-row system in 54 bits has rank 53, hence
exactly two solutions:
\[
\begin{aligned}
&(0,1,4,6,0,6,3,5,0,6,7,3,7,3,0,3,6,7),\\
&(0,1,2,6,0,6,3,5,4,0,7,3,7,3,6,3,4,7).
\end{aligned}
\]
This potential parametrization is exact: the eight possible local
triangles at a cubic vertex are its eight potential translations, and
the edge equations say that the endpoint labels agree.  For both
solutions, the used-pair graph on coordinates \(0,\ldots,7\) contains
all 15 pairs on \(\{0,1,2,3,4,5\}\).  Thus it contains \(K_6\), is not
5-colourable, and the premise holds.

### Failure of all 21 cleaning choices

Masks below use the component order produced by taking the least unseen
vertex.  For every row, the checker enumerates the entire cycle space of
\(G-M_t\).  The final mask \(\lambda\) satisfies
\[
 \lambda\cdot r_\mu=1,\qquad
 \lambda\cdot\tau_t(C)=0\quad
 \text{for every }C\in Z_1(G-M_t),                       \tag{3}
\]
so it is a short dual certificate that \(r_\mu\notin\operatorname{im}\tau_t\).

| \(\mu\) | \(t\) | components | \(r_\mu\) | cycle dim. | image rank | \(\lambda\) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 3 | 6 | 5 | 1 | 3 |
| 1 | 4 | 3 | 6 | 5 | 1 | 2 |
| 1 | 6 | 3 | 6 | 4 | 1 | 3 |
| 2 | 1 | 8 | 51 | 7 | 4 | 1 |
| 2 | 4 | 8 | 51 | 5 | 2 | 2 |
| 2 | 5 | 8 | 51 | 8 | 5 | 65 |
| 3 | 3 | 7 | 58 | 6 | 3 | 32 |
| 3 | 4 | 7 | 58 | 5 | 2 | 2 |
| 3 | 7 | 7 | 58 | 8 | 5 | 33 |
| 4 | 1 | 6 | 27 | 7 | 3 | 6 |
| 4 | 2 | 6 | 27 | 5 | 2 | 1 |
| 4 | 3 | 6 | 27 | 6 | 3 | 2 |
| 5 | 2 | 9 | 243 | 5 | 2 | 1 |
| 5 | 5 | 9 | 243 | 8 | 5 | 6 |
| 5 | 7 | 9 | 243 | 8 | 5 | 2 |
| 6 | 1 | 7 | 15 | 7 | 3 | 27 |
| 6 | 6 | 7 | 15 | 4 | 2 | 4 |
| 6 | 7 | 7 | 15 | 8 | 4 | 33 |
| 7 | 3 | 6 | 36 | 6 | 2 | 14 |
| 7 | 5 | 6 | 36 | 8 | 4 | 5 |
| 7 | 6 | 6 | 36 | 4 | 2 | 7 |

This proves the displayed sufficient lemma false even when disconnected
binary-cycle switches are allowed and executed componentwise.

## 3. An outside-line switch repairs this very flow

Edges \(0,2,18,20,22\) form the 5-circuit
\[
             0-11-6-17-7-0.
\]
None has value \(5\).  Switch this circuit by \(t=5\).  The line
\(\{2,4,6\}=\ker(1)-\{0\}\) then has \(r_1=0\).  Notice that
\(5\notin\{2,4,6\}\): this is precisely an outside-line repair.

`construction.json` contains the switched flow and the five lifted
Eulerian edge sets.  The checker verifies both their quotient relation
and that every edge occurs exactly twice.  Therefore this obstruction
only kills the fixed-line/single-value lemma.  The next surviving exact
claim is:

> Every Oum-hard flow admits some admissible binary-cycle switch of an
> arbitrary nonzero value, after which some Fano line is clean.

The countermodel satisfies this stronger flexible claim by one 5-circuit
switch; no universal proof is claimed.

## 4. Minimality scope

The complete cyclically-4, non-Tait, simple cubic corpus through order 18
contains the Petersen graph at order 10, no graphs at orders 12, 14, or
16, and the two Blanuša snarks at order 18.  One representative of every
nowhere-zero \(\mathbb F_2^3\)-flow orbit under \(GL(3,2)\) was enumerated.

| graph | normalized flow orbits | no cleaning pair | exact Oum-hard countermodels |
|---|---:|---:|---:|
| Petersen (10) | 170 | 0 | 0 |
| first Blanuša (18) | 118,960 | 1,888 | 624 |
| second Blanuša (18) | 119,260 | 2,390 | 332 |

Thus order 18 is minimal in that complete **strict-snark** scope.  This
does not claim minimality among all Tait-colourable cyclically-4 cubic
graphs, multigraphs, or arbitrary bridgeless graphs.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated and implemented the
cycle-image test, ran the normalized-flow census, found and minimized the
record, derived the displayed implication and dual certificates, and
drafted this note.  The standard-library checker is intended to make every
finite assertion independently reproducible.  This is not independent
human peer review, and it is not a resolution of the Five-Cycle Double
Cover Conjecture.
