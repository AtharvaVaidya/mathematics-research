# Closed-cage forced inequalities and a \(b^*=2\) flag witness

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE REDUCTIONS AND AN EXACT NO-GO; NO CLOSED
CAGE CONTRADICTION AND NO FIVECDC RESOLUTION**.

## 1. Scope

Assume \(q\) lies in a terminal equal-surface-\(\chi\) Kempe plateau.
Fix ordered root edges \(r,s\), and suppose that the connected
fixed-\((d,b^*)\) subplateau containing \(q\), with \(d>1\), has no
neutral boundary edge to lexicographically smaller \((d,b^*)\).
The statements below are the consequences that follow directly from
the switch identities.  No minimal-counterexample property beyond this
explicit assumption is used.

The complete order-12 and order-14 censuses have no such subplateau.
The deductions below do not turn that finite fact into a universal
contradiction.

## 2. The complete ten-pair switch table

For a factor pair \(A\), write
\[
                         Y_A=C_a\mathbin\triangle C_b
 \qquad(A=\{a,b\}).
\]
If \(K\) is one component of \(Y_A\), switching \(A\) on \(K\) gives,
for every pair \(B\),
\[
 Y_B'=
 \begin{cases}
 Y_B\mathbin\triangle K,&|A\cap B|=1,\\
 Y_B,&|A\cap B|\in\{0,2\}.
 \end{cases}                                                  \tag{1}
\]

Normalize an eligible shortest first pair to
\[
                         P=01,\qquad Q=02.
\]
For an arbitrary switch pair \(A\), the complete effect on the two
visible factors is:

| \(A\) | \(Y_P'\) | \(Y_Q'\) |
|:---:|:---:|:---:|
| \(01\) | \(Y_P\) | \(Y_Q\triangle K\) |
| \(02\) | \(Y_P\triangle K\) | \(Y_Q\) |
| \(03,04,12\) | \(Y_P\triangle K\) | \(Y_Q\triangle K\) |
| \(13,14\) | \(Y_P\triangle K\) | \(Y_Q\) |
| \(23,24\) | \(Y_P\) | \(Y_Q\triangle K\) |
| \(34\) | \(Y_P\) | \(Y_Q\) |

Thus the visible root component \(H\), first blocker \(J\), and target
component \(D\) do not exhaust the possible surgeries.  The
order-14 cyclic-block witness is sharp: every minimizing \(H/J\)
switch either loses \(\chi\) or raises \(d\), while a neutral
\(24\)-switch joins the roots.  Any closed-cage proof must use all ten
rows of this table.

## 3. Every forced Euler inequality

For a switch on a component \(K\) of \(Y_{ab}\), only coordinates
\(a,b\) change, and
\[
\Delta_{ab}(K)=
 \kappa(C_a\triangle K)+\kappa(C_b\triangle K)
 -\kappa(C_a)-\kappa(C_b).                                  \tag{2}
\]
Equivalently, in the fixed-pair cubic core with matching involutions
\(m_{10},m_{01},m_{11}\),
\[
\Delta_{ab}(K)=\frac12\left[
 z(m'_{10}m_{11})+z(m'_{01}m_{11})
 -z(m_{10}m_{11})-z(m_{01}m_{11})
\right].                                                     \tag{3}
\]

Terminality gives, for **every** component of **every** one of the ten
factors,
\[
                            \Delta_{ab}(K)\le0.                \tag{4}
\]
The no-exit assumption sharpens (4) exactly when the switch would
lower the rooted metric:
\[
\boxed{\quad
 (d(q^K),b^*(q^K))<(d(q),b^*(q))
 \quad\Longrightarrow\quad
 \Delta_{ab}(K)\le-1.
 \quad}                                                       \tag{5}
\]
Indeed, equality in (2) would be a neutral lexicographic exit.  There
is no converse: a negative switch need not improve the metric, and a
neutral switch is allowed to preserve or raise it.

For two successive switches the only additional forced identity is
telescoping:
\[
 \chi(q^{K,L})-\chi(q)
 =\Delta_q(K)+\Delta_{q^K}(L).                               \tag{6}
\]
When the switch pairs are disjoint the two operations commute.  When
they share one coordinate, the second component must be traced in the
updated factor \(Y_B\triangle K\).  Treating it as an old component is
an invalid leap.

## 4. Boundary-interaction form

There is a useful exact strengthening of (4).  Fix \(A=ab\).  Make an
auxiliary multigraph \(\Gamma_A\):

* its vertices are the circuit components of \(Y_A\);
* an edge of \(G\) labelled exactly \(A\) joins the two \(Y_A\)
  components traversing its endpoint vertices; and
* it is a loop if those two components agree.

If \(K\) is a vertex of \(\Gamma_A\), let \(B(A,K)\) be the
non-loop \(A\)-labelled edges incident with it.  The corner-pairing
law gives
\[
 \Delta_A(K)=
 c(\mathcal P\mathbin\triangle B(A,K))-c(\mathcal P),         \tag{7}
\]
where \(\mathcal P\) is the current transition partition of the fixed
four-regular corner graph.  Moreover \(\Gamma_A\) is Eulerian, so
\[
                         |B(A,K)|=\deg_{\Gamma_A}(K)
                         \quad\hbox{is even}.                 \tag{8}
\]
If this degree is zero or two, the switch is neutral.  Combining this
with (5) gives the forced cage inequality
\[
\boxed{\quad
 (d(q^K),b^*(q^K))<(d(q),b^*(q))
 \quad\Longrightarrow\quad
 |B(A,K)|\ge4
 \ \hbox{ and }\ \Delta_A(K)\le-1.
 \quad}                                                       \tag{9}
\]

This is the strongest purely local conclusion presently justified.
The 28-vertex two-lift counterexamples in
`scratch/d5-local-neutral-corner-pairing-frontier.md` show that three
components through one graph corner can all have degree at least four
and can all have negative Euler change at a local \(\chi\)-maximum.
Therefore (9) alone is not a contradiction.

## 5. What \(b^*=0\) and \(b^*=1\) really force

### Eligible \(b^*=0\)

Let \(C\) be the root \(Y_P\)-component, \(D\) the next
\(Y_Q\)-component, and \(H\ne D\) the root \(Y_Q\)-component, with
\(|P\cap Q|=1\).  Put \(R=P\triangle Q\).  After switching \(Q\) on
\(H\),
\[
                         Y_R'=Y_P\triangle(Y_Q\setminus H).   \tag{10}
\]
If one orientation of \(C\) meets no foreign \(Q\)-component before
\(D\), (10) splices a root \(Y_R'\)-component onto \(D\), so
\[
                              d(q^H)\le d(q).                 \tag{11}
\]
For \(d=2\), if the result has \(d=1\), then (5) forces
\(\Delta_Q(H)\le-1\).  If it still has \(d=2\), no strict Euler
inequality follows: its new \(b^*\) can equal or exceed zero.

### Convention-only \(b^*=0\)

If no eligible shared-coordinate shortest pair exists, \(b^*=0\) by
definition.  Equation (10) has no objects to which it can be applied.
This branch must be handled separately; treating the convention as a
blocker-free profile is unsound.

### \(b^*=1\)

For a minimizing orientation, the visible cyclic word starts
\[
                            H,\ J,\ D
\]
after deleting gaps and later \(H\)-returns.  Equations (1) and (10)
describe the \(H\)- and \(J\)-surgeries exactly, but neither surgery
is forced to preserve \(d\).  The frozen order-14 witness has
\[
\begin{array}{c|c}
\hbox{visible switch}&(\Delta\chi;d',b^{*'})\\ \hline
02\hbox{ on }H\hbox{ or }J&(-2;2,1)\\
13\hbox{ on }H\hbox{ or }J&(0;3,0),
\end{array}
\]
while a third pair \(24\) gives \((0;1,0)\).  Therefore the only valid
general rule is (5), applied to all ten pairs.

## 6. A small support-minimality consequence

Choose a state in a hypothetical fixed-\((2,b^*)\) cage having the
maximum number of used coordinates.  For an eligible pair
\(P,Q\), their union has three coordinates; call the two outside
coordinates \(u,v\).

Suppose exactly \(u\) is used and \(v\) is unused.  If \(C_u\) has at
least two components, switch \(u,v\) on any one component \(L\).
This is a fresh-coordinate switch and is neutral:
\[
 C_u'=C_u\setminus L,\qquad C_v'=L.                           \tag{12}
\]
The pair \(uv\) is disjoint from both \(P,Q\), so the displayed
\(C,D,H\) profile is unchanged.  Hence \(d'\le2\), and if \(d'=2\)
then \(b^{*'}\le b^*\).  A strict inequality contradicts the assumed
no-exit property; equality places the state in the same fixed metric
subplateau but increases coordinate support, contradicting maximality.
Therefore
\[
\boxed{\quad
\hbox{if exactly one outside coordinate is used at such a maximal
state, its coordinate support is one circuit.}
\quad}                                                       \tag{13}
\]
This does not eliminate the case: if \(C_u\) is one circuit, (12)
merely exchanges the names \(u,v\) and does not increase support.

## 7. The potential \(b^*\) is unbounded

The order-14 terminal census observes only \(b^*\in\{0,1\}\), but this
is not a universal shortest-pair theorem.  In fact \(b^*\) is
unbounded even on Tait-supported states at a one-switch local
surface-\(\chi\) maximum.

For even \(n\ge4\), let \(M_n\) be the \(n\)-gonal bipyramid.  Its map
vertices are two apices \(a,b\) and an equatorial cycle
\(v_0,\ldots,v_{n-1}\).  Give it the \(2n\) oriented triangular faces
\[
 (a,v_i,v_{i+1}),\qquad(b,v_{i+1},v_i)
 \quad(i\in\mathbb Z_n).                                    \tag{14}
\]
Let \(G_n\) be its flag graph.  Thus a vertex of \(G_n\) is a flag
\((F,\text{side},\text{endpoint})\), and its three incident edges are
the standard flag involutions \(r_0,r_1,r_2\).  Label those three
perfect matchings by \(01,02,12\), respectively.

The graph \(G_n\) is simple connected cubic.  Every edge belongs to a
bichromatic flag circuit, so it is bridgeless.  The incident labels
at every vertex are \(01,02,12\), whose xor is zero.  Hence this is a
Tait-supported \(D_5\) state.

Take \(r\) to be the \(r_1\)-edge at apex \(a\) in face
\((a,v_0,v_1)\), and \(s\) the \(r_0\)-edge on the side \(av_{n/2}\)
in face \((a,v_{n/2},v_{n/2+1})\).  A Tait flag edge belongs to exactly
two feature circuits.  The source circuits are the apex circuit and
the first face circuit.  The target circuits are the opposite face
circuit and the edge circuit of \(av_{n/2}\).

The only incident source-target feature pair is the apex circuit
together with one of those two target features.  Eligibility requires
the second factor to contain the \(r_1\)-edge \(r\), which excludes
the edge-feature partition and leaves the face-feature partition.
Therefore every eligible shortest profile has:

* first component \(C\): the flag circuit around \(a\);
* root \(Q\)-component \(H\): face \((a,v_0,v_1)\); and
* target \(Q\)-component \(D\): face
  \((a,v_{n/2},v_{n/2+1})\).

Around the apex circuit, the \(n\) face components occur in their
cyclic order.  Either orientation from \(H\) to \(D\) encounters
exactly
\[
                              \frac n2-1
\]
foreign face components.  The multiple coordinate-pair names of the
three Tait feature partitions give exactly seven eligible shortest
profiles, but do not change these component circuits.  Consequently
\[
\boxed{\qquad
 d_{q_n}(r,s)=2,\qquad
 b^*_{q_n}(r,s)=\frac n2-1.
\qquad}                                                       \tag{15}
\]
This proves that \(b^*\) is unbounded.

The family lies in a terminal \(\chi\)-plateau.  The three
coordinate supports are precisely the face, edge, and vertex flag
circuits.  There are
\[
                         2n,\quad3n,\quad n+2
\]
of these, so \(\chi=2\).  The coloured surface is connected because
its triangle-adjacency graph is the connected graph \(G_n\).  Every
connected closed surface has Euler characteristic at most two.
Consequently no \(D_5\) state on \(G_n\) has larger \(\chi\), and the
entire equal-\(\chi\) component containing \(q_n\) is terminal.

More explicitly, every switch between a used and an unused
coordinate is a neutral fresh-coordinate transfer, giving
\(12n+4\) neutral switches.  A switch between two used coordinates
is performed on the flag circuit of one map feature of degree \(t\).
It merges the \(t\) incident feature circuits of each of the other
two ranks into one, and hence has
\[
                              \Delta\chi=2-2t.                \tag{16}
\]
The \(3n\) map edges have \(t=2\), the \(2n\) faces have \(t=3\), the
\(n\) equatorial vertices have \(t=4\), and the two apices have
\(t=n\).  Thus the complete delta histogram is
\[
\{\,0:12n+4,\ -2:3n,\ -4:2n,\ -6:n,\ -(2n-2):2\,\},          \tag{17}
\]
combining the last two entries when \(n=4\).  In particular no
one-switch \(\chi\)-increase exists.

Thus (15) refutes the unrestricted, local-maximum, and
terminal-plateau bounds \(b^*\le1\).  In fact it proves that \(b^*\)
is unbounded inside terminal plateaus.

The standard-library family checker reconstructs all profiles and
verifies (15)--(17) for arbitrary requested even parameters:

```text
python3 scratch/check_d5_bipyramid_bstar_unbounded.py
```

The separate triangular-torus witness
`scratch/check_d5_triangular_torus_bstar_two.py` gives another exact
\((d,b^*)=(2,2)\) example on 108 vertices.

## 8. What survives the unbounded family

The bipyramid family is not difficult for neutral reconfiguration.
Let \(L\) be the coordinate-\(2\) circuit around apex \(a\).
Coordinate \(4\) is unused, so \(L\) is a \(Y_{24}\)-component and
switching \(24\) on \(L\) is neutral.  The \(n\) edge-feature
components of \(Y_{02}\) each meet \(L\) in one edge.  The switch law
gives
\[
                              Y_{02}'=Y_{02}\triangle L.       \tag{18}
\]
Successively taking the symmetric difference of a circuit with
circuits meeting it in one path splices all \(n\) edge-feature
components and \(L\) into one circuit.  The root \(r\) lies on an
\(r_1\)-edge of \(L\) outside those common paths, and \(s\) lies on
the target edge-feature component outside \(L\).  Therefore that one
new \(Y_{02}\)-circuit contains both roots:
\[
                              d:2\longrightarrow1.             \tag{19}
\]
The family checker verifies (18)--(19) for every requested \(n\).

This is the decisive diagnosis.  The number of intervening
\(Q\)-components is unbounded, but one neutral **transversal** can
splice all of them simultaneously.  The raw blocker count measures
the length of a cyclic word, while the useful object is the contact
pattern of an arbitrary neutral switch component with all factor
components in that word.

For a state \(q\), define the exact one-step neutral reach
\[
 \sigma_q(r,s)=
 \min\left(
 d_q(r,s),\
 \min_{\substack{A,K\\K\text{ component of }Y_A\\
                  \Delta_A(K)=0}}
 d_{q^{A,K}}(r,s)
 \right).                                                     \tag{20}
\]
This is a certificate statistic rather than a claimed monotone.
The bipyramid family has unbounded \(b^*\) but
\[
                              \sigma_q(r,s)=1.                 \tag{21}
\]

The corrected plateau theorem is therefore the original
distance-primary statement, with no bounded blocker coordinate:

> **Neutral-transversal descent target.** Let \(T\) be a terminal
> \(\chi\)-plateau and \(D\) a connected component of states at one
> fixed value \(d_q(r,s)=d>1\), using only neutral equal-\(d\)
> moves.  Then some \(q\in D\) has
> \[
>                              \sigma_q(r,s)<d.
> \]

Equivalently, the lexicographic object is \((\chi,-d)\) with plateau
semantics at both levels.  The statistic \(b^*\) may diagnose a
particular failed \(H\)-switch, but it cannot be a bounded case
parameter.

A local sufficient condition for (20) is the following proved
multi-splice rule.  If \(z\) is unused, \(L\) is a component of
\(C_x\), and each \(Y_{ax}\)-component meeting \(L\) does so in one
nonempty proper path, then the neutral \(xz\)-switch makes
\[
                              Y_{ax}'=Y_{ax}\triangle L
\]
one circuit on the symmetric difference of \(L\) and all those
components.  Any two roots in that symmetric difference are rescued.
The bipyramids realize this rule with arbitrarily many components.

## 9. Remaining proof obligation

No contradiction to a closed fixed-\((d,b^*)\) cage has been derived.
A valid completion must use information not contained in the
pointwise inequalities (4), because local two-lifts realize all-negative
corner triples.  After the unbounded family, the sharper exact missing
implication is global:

> In a terminal plateau, a connected fixed-\(d>1\) component cannot
> simultaneously realize the strict boundary-twist inequalities (9)
> for every distance-lowering surgery among all ten pairs and fail
> every neutral transversal contact surgery.

The frozen 56-vertex terminal plateau supplies a further stress test.
For all 83 root pairs involving edge 75, its 55,652 states contain 126
fixed-distance subplateaus and no fixed-distance cage.  This is exact
positive evidence, not a universal proof.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the ten-pair and
boundary-interaction obligations, found the unbounded bipyramid and
triangular-torus families, wrote the independent checkers, and drafted
this note.  The arguments and finite certificates have not undergone
independent peer review and are not presented as a resolution of
FiveCDC.
