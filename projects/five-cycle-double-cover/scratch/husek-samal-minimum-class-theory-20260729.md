# Minimum value classes and Hušek–Šámal packing defect

Date: 2026-07-29

Status: rigorous reformulations, exchange/cut lemmas, and two exact finite
auxiliary countermodels.  No FiveCDC resolution is claimed.

Scope: finite loopless cubic graphs; parallel edges cause no essential
change.  The matching language would need reformulation for loops.

Primary references:

- Hušek–Šámal, arXiv:2607.24724v1:
  <https://arxiv.org/abs/2607.24724>
- Mattiolo–Negrini–Pagani, arXiv:2604.22501v1:
  <https://arxiv.org/abs/2604.22501>

## 1. Executive conclusions

1. **Minimizing one value-class cardinality does not force that chosen
   class to pack.**  A pre-existing certified order-22 quotient witness
   lifts to a literal nowhere-zero \(\mathbb F_2^3\)-flow whose
   distinguished class is globally minimum of size two and is
   nonpacking.  The complete public package is
   `search/global-minimum-nonpacking-22v-20260729/`.

2. **Even the existential cardinal-minimum statement is false:** it is
   not true that some global-minimum Fano value class must pack.  On the
   certified 130-vertex graph,
   \[
                         \rho_3(G)=5,
   \]
   while every size-five value class is nonpacking.  A size-six class
   does pack and gives an explicit FiveCDC.  Thus the lexicographic
   minimum of
   \[
                 \bigl(|M|,\delta(M)\bigr)                 \tag{1}
   \]
   can have positive second coordinate when its first coordinate is
   forced to be \(\rho_3(G)\).  The complete public package is
   `search/minimum-fano-class-nonpacking-130v-20260729/`.

3. **Minimizing the Hušek–Šámal defect over all flows is not a
   simplification.**  For
   \[
        \beta(G)=\min_{f,\lambda} d_\lambda(f),             \tag{2}
   \]
   a \(\beta\)-minimizer has a packing value class if and only if
   \(\beta(G)=0\).  Universally proving that such a minimizer packs is
   exactly the Hušek–Šámal/FiveCDC existence assertion.

4. Cardinal-minimality nevertheless gives a strong exact exchange
   inequality.  If \((f,a)\) minimizes \(|M_a(f)|\), then for every
   \(t\ne0,a\) and every binary cycle \(X\subseteq G-M_t(f)\),
   \[
       |X\cap M_a(f)|\le |X\cap M_{a+t}(f)|.               \tag{3}
   \]
   Consequently every \(a\)-edge is a bridge after either companion
   quotient-color class is deleted.  This yields three simultaneous
   odd cut barriers around every \(a\)-edge.

5. A lexicographic minimizer of (1) still satisfies a sharp
   neutral-exchange obstruction: every size-neutral legal kernel switch
   toggles at most as many dirty components as clean components.  This
   is useful structural information, but the 130-vertex graph proves
   that these inequalities alone cannot force packing.

The order-22 every-minimizer countermodel has girth five and cyclic
edge-connectivity three.  It does **not** refute every-minimizer packing
on the cyclically 4-edge-connected or girth-at-least-10 domains.
The 130-vertex existential countermodel has girth four and cyclic
edge-connectivity three.  It therefore leaves the same reduced domains
open, provided a sound reduction or a genuinely restricted theorem is
supplied.

## 2. Setup and the fixed-pair packing bridge

Let \(V=\mathbb F_2^3\), let
\[
                     f:E(G)\to V-\{0\}
\]
be a flow, and fix \(a\ne0\).  Put
\[
 M=M_a(f)=f^{-1}(a),\qquad T=\partial M,\qquad K=G-M.       \tag{4}
\]
The class \(M\) is a matching.  Choose
\(\lambda\in V^*-\{0\}\) with \(\lambda(a)=1\), and put
\[
 F=F_\lambda(f)=\{e:\lambda(f(e))=1\},\quad
 J_0=F-M,\quad H=K-J_0.                                   \tag{5}
\]
Then \(F\) is Eulerian and
\[
                         \partial J_0=T.                   \tag{6}
\]
Thus \(J_0\) is the canonical first \(T\)-join.

The fixed-pair packing–switch equivalence is:
\[
\begin{split}
K\text{ contains two edge-disjoint }T\text{-joins}
\quad\Longleftrightarrow\quad
\text{an }a\text{-switch reaches a good }(\lambda,a)
\text{ pair}.                                             \tag{7}
\end{split}
\]
If \(J_1,J_2\subseteq K\) are disjoint \(T\)-joins, the switch support is
\[
                         X=J_0\mathbin\triangle J_1.        \tag{8}
\]
It is an Eulerian set avoiding \(M\).  After switching \(a\) on \(X\),
\[
                         F'=M\cup J_1,\qquad H'=K-J_1,     \tag{9}
\]
and \(J_2\subseteq H'\) proves the component condition.  Conversely,
any such switch supplies the two joins.

The support (8) may be a disjoint union of circuits.  Hence (7) is one
binary-cycle switch, or a finite sequence of simple-cycle switches; it
need not be one simple-cycle switch.

## 3. Exact quotient/lift characterization

Let \(\pi_a:V\to V/\langle a\rangle\cong\mathbb F_2^2\).  The projection
\[
                         \phi=\pi_a\circ f                 \tag{10}
\]
is an \(\mathbb F_2^2\)-flow with exact zero set \(M\).  On \(K\) it is
nowhere zero.  In particular, every component of \(K\) is bridgeless:
a bridge would be the sole nonzero term in the flow sum across a cut.

The converse has one necessary condition that must not be dropped.

### Lift lemma

Let \(\phi:E(G)\to\mathbb F_2^2\) be a flow with exact zero set \(M\).
Assume \(M\) is a matching.  Then \(\phi\) is the quotient of a
nowhere-zero \(V\)-flow having \(M\) as one value class if and only if
every component of \(G-M\) contains an even number of vertices of
\(T=\partial M\).

Proof.  Fix a linear section
\(s:\mathbb F_2^2\to V\) complementary to \(\langle a\rangle\).
A lift has the form
\[
                           f=s\phi+a h,                    \tag{11}
\]
where \(h\) is a binary flow.  Exact equality \(M_a(f)=M\) requires
\(h(e)=1\) on \(M\); away from \(M\), \(s\phi(e)\notin\langle a\rangle\),
so either value of \(h(e)\) remains nonzero and different from \(a\).
Writing
\[
                  \operatorname{supp}(h)=M\cup J,\quad J\subseteq G-M,
\]
the binary flow equation is exactly
\[
                              \partial J=\partial M=T.     \tag{12}
\]
Such a \(T\)-join exists precisely when every component of \(G-M\) is
\(T\)-even.  All implications reverse.

For a value class coming from an existing \(f\), (6) supplies the
required join automatically.  For an arbitrary minimum-zero
\(\mathbb F_2^2\)-flow, matching plus component parity must be checked;
the lift is not automatic.

Define the liftable matching resistance
\[
\rho_3(G)=\min_{f\ {\rm NZ}\ V\text{-flow},\,a\ne0}|M_a(f)|. \tag{13}
\]
Equivalently, (13) minimizes the zero-set size over
\(\mathbb F_2^2\)-flows whose zero set is a matching satisfying the lift
lemma.

Mattiolo–Negrini–Pagani define the flow resistance \(r_f(G)\) as the
minimum number of zeros in an \(\mathbb F_2^2\)-flow.  Projection gives
\[
                              \rho_3(G)\ge r_f(G).          \tag{14}
\]
Their Theorem 1.1 constructs cyclically 5-edge-connected snarks \(H_n\)
with
\[
                              r_f(H_n)=n.                  \tag{15}
\]
Therefore the minimum possible value-class size is not bounded by a
universal constant, even in a high-connectivity snark family.  Equality
in (14) need not hold: a minimum-zero quotient flow may fail the matching
or lift-parity condition.

## 4. Exact class-size exchange and cut barriers

Suppose \((f,a)\) globally minimizes \(|M_a|\); the following arguments
need only local minimality under the named switches.  Let \(t\ne0,a\),
and let \(X\) be any binary cycle satisfying
\[
                              X\cap M_t(f)=\varnothing.     \tag{16}
\]
Then \(f'=f+t1_X\) is a legal nowhere-zero flow and
\[
 M_a(f')=(M_a-X)\cup\bigl(X\cap M_{a+t}\bigr).             \tag{17}
\]
Minimality proves (3):
\[
                 |X\cap M_a|\le |X\cap M_{a+t}|.           \tag{18}
\]

### Three simultaneous bridge barriers

Fix \(e\in M_a\).  For every \(t\ne0,a\), the edge \(e\) is a bridge of
\[
                         G-\bigl(M_t\cup M_{a+t}\bigr).    \tag{19}
\]
Indeed, a circuit through \(e\) in (19) would be legal for the
\(t\)-switch, would remove at least one \(a\)-edge, and would add no new
\(a\)-edge, contradicting (18).

The six values outside \(\{0,a\}\) form three unordered pairs
\(\{t,a+t\}\), so (19) is three distinct bridge conditions.  For each
pair there is a shore \(U\) with
\[
 \delta_G(U)\setminus\bigl(M_t\cup M_{a+t}\bigr)=\{e\}.    \tag{20}
\]
Summing \(f\) across \(U\), and using the independent basis \((a,t)\),
shows
\[
 |\delta(U)\cap M_t|\equiv
 |\delta(U)\cap M_{a+t}|\equiv1\pmod2.                    \tag{21}
\]
Thus every barrier cut consists of \(e\), an odd positive number of
\(t\)-edges, and an odd positive number of \((a+t)\)-edges.  Its size is
odd and at least three.

In quotient language, deleting one nonzero quotient-color class makes
every edge of \(M\) a bridge.  If \(G\) is cyclically 4-edge-connected,
every size-three barrier is trivial: its tree shore has one vertex.  Such
a barrier is exactly the cut around an endpoint of \(e\) whose two other
incident quotient values equal that color.  Any barrier for a color not
appearing as the repeated local color at either endpoint of \(e\) has
size at least five.

These conclusions are genuine structure, but not packing: the lifted
order-22 global minimizer in Section 8 obeys them and still fails to pack.

## 5. Packing defect of a fixed matching

For a liftable \(M\), define
\[
\delta(M)=\min_{\partial J=T,\ J\subseteq K}
 \#\{Q\in\operatorname{Comp}(K-J):|Q\cap T|\text{ odd}\}. \tag{22}
\]
The fixed-pair bridge (7) gives
\[
                 \boxed{\ \delta(M)=0\iff M\text{ packs two }T
                 \text{-joins in }K.\ }                   \tag{23}
\]
Moreover, \(a\)-switches act transitively on the \(T\)-joins of \(K\):
the switch \(J_0\triangle J\) replaces the canonical join \(J_0\) by
\(J\) while leaving \(M\) fixed.  Hence \(\delta(M)\) is exactly the
least Hušek–Šámal defect attainable in the fixed-\(M\), fixed-quotient
orbit.

Choose \(J\) lexicographically minimizing
\[
 \left(o(J),|J|\right),\qquad
 o(J)=\#\{T\text{-odd components of }K-J\}.                \tag{24}
\]
Then:

1. \(J\) is a forest.  Removing a circuit from \(J\) preserves
   \(\partial J=T\), and adding its edges to \(K-J\) only merges
   components.  Merging cannot increase the number of odd components;
   lexicographic minimality gives the contradiction.

2. If \(Q\) is a bad component of \(K-J\), then
   \[
                         \delta_K(Q)\subseteq J,\qquad
                         |\delta_K(Q)|\text{ is odd}.       \tag{25}
   \]
   The first assertion is the definition of a complement component.
   The second follows by summing the \(J\)-degree parity
   \(\partial J=T\) on \(Q\).  Because \(K\) is bridgeless and a whole
   component of \(K\) is \(T\)-even, (25) has size at least three.

Thus a nonpacking matching has a normalized forest-supported obstruction
with a positive even number of bad components, each behind a saturated
odd \(T\)-cut.

## 6. The minimum-class selection principle is false

Define
\[
 \delta_\rho(G)=
 \min\{\delta(M_a(f)):f\text{ is NZ},\ a\ne0,\
                         |M_a(f)|=\rho_3(G)\}.              \tag{26}
\]
The formerly proposed target was
\[
 \boxed{\qquad \delta_\rho(G)=0. \qquad}                   \tag{27}
\]
Equivalently:

> Some globally minimum value class packs two boundary joins.

Equivalently again, a lexicographic minimizer of (1) has packing defect
zero.

Statement (27) is false.  The public 130-vertex package

```text
search/minimum-fano-class-nonpacking-130v-20260729/
```

contains a nowhere-zero \(\mathbb F_2^3\)-flow with distinguished class
\[
                         M=\{35,48,97,135,148\}.            \tag{28}
\]
Direct xor checks verify the flow and the exact value class.  Hence
\(\rho_3\le5\).  The independently generated and doubly checked LRAT
refutation for an arbitrary \(\mathbb F_2^2\)-flow with at most four
zeros proves \(r_f\ge5\), and (14) gives \(\rho_3\ge5\).  Thus
\(\rho_3=5\).

A second independently generated and doubly checked LRAT refutation
for the complete exact-zero-matching/two-cycle encoding with
\(|M|\le5\) proves that no size-five class packs.  Therefore
\[
                          \delta_\rho(G)>0.                 \tag{28a}
\]
The same graph has a size-six packing certificate and an explicit
standard FiveCDC.  This cleanly separates minimum Fano liftability
(one boundary \(T\)-join) from packing (two edge-disjoint boundary
\(T\)-joins).

The order-22 witness had already disproved only “every
\(\rho_3\)-minimizer packs”: its bad minimum support \(\{14,30\}\) has a
neutral switch to the packing co-minimum support \(\{3,30\}\).  APX36
similarly has \(\rho_3=2\) with all 598 minimum supports packing.  Those
positive finite observations did not justify (27).

By (7), (27) would have implied an H–S-good flow and therefore FiveCDC,
but the reverse implication was never justified.  Its failure does not
bear on the truth of FiveCDC.

## 7. Exact neutral-exchange optimality system

For structural analysis, choose a triple \((f,a,\lambda)\)
lexicographically as follows:

1. minimize \(|M_a(f)|=\rho_3(G)\);
2. among those triples minimize \(d_\lambda(f)\);
3. within the fixed matching orbit, use an \(a\)-switch to put the
   canonical \(T\)-join in the forest normal form of Section 5.

Let \(D\) be the set of dirty components of
\(H=G-F_\lambda(f)\), so \(|D|=d_\lambda(f)\).

For \(0\ne t\in\ker\lambda\), a legal kernel switch has the fixed
component update
\[
                         d'=d+\tau_t(X),                   \tag{29}
\]
where
\[
\tau_t(X)_Q=
 |\delta(Q)\cap X\cap(M_a\cup M_{a+t})|\pmod2.             \tag{30}
\]
The class-size change is
\[
        \Delta_t(X)=|X\cap M_{a+t}|-|X\cap M_a|.            \tag{31}
\]
The lexicographic choice gives the exact two-level inequalities
\[
\begin{array}{ll}
\Delta_t(X)\ge0
   &\text{for every binary cycle }X\subseteq G-M_t,\\[2mm]
\Delta_t(X)=0\Longrightarrow
 |d+\tau_t(X)|\ge |d|
   &\text{for every such size-neutral cycle}.              \tag{32}
\end{array}
\]
Equivalently, for \(S=\operatorname{supp}\tau_t(X)\) in the neutral case,
\[
                         2|D\cap S|\le |S|.                \tag{33}
\]
A neutral switch can decrease the defect exactly when it toggles more
dirty than clean components.  Thus (33), not merely a vague “local
minimum,” is the exact obstruction to the desired secondary-potential
descent.

There is also an exact fixed-support interpretation.  Contract each
component of \(H=G-F\) to a vertex, retaining the deleted \(F\)-edges as
a multigraph \(\mathcal H\).  For a neutral kernel switch put
\[
 A=X\cap M_a,\qquad B=X\cap M_{a+t}.                       \tag{34}
\]
Then \(A\subseteq M\), \(B\subseteq J=F-M\), and
\(|A|=|B|\).  Define
\[
 M'=M-A+B,\qquad J'=J-B+A.                                \tag{35}
\]
The union \(M'\cup J'=F\), so \(H\) is literally unchanged, and
\[
                         \partial J'=\partial M'.          \tag{36}
\]
If \(\partial_{\mathcal H}\) denotes endpoint parity after contraction,
then the new dirty-component vector is
\[
                         d'=d+\partial_{\mathcal H}(A\cup B). \tag{37}
\]
Consequently this neutral exchange reaches an H–S-good realization
with the unchanged complement \(H\), and thereby exhibits \(M'\) as a
packing co-minimizer via \(J'\) and a join in \(H\), exactly when
\[
                         \partial_{\mathcal H}(A\cup B)=d. \tag{38}
\]
The class \(M'\) could conceivably pack through a different first join
even when (38) fails; (38) is exact for the displayed unchanged-\(H\)
realization.  It is a finite parity problem on the component multigraph, coupled to
the cycle/legality and equal-cardinality conditions on \(X\).  It cleanly
separates the two missing ingredients: producing a legal neutral
exchange, and making its contracted boundary equal the dirty vector.

There is a particularly concrete family of tests.  Since \(F=M\cup J\)
is Eulerian and \(G\) is cubic, every nonisolated component of the
spanning subgraph \((V(G),F)\) has degree two at each of its vertices.
Thus the edge set \(F\) is the disjoint union of its circuit components
(including a two-edge circuit if parallel edges occur).  Any such circuit
\(C\subseteq F\) avoids every \(M_t\) with
\(0\ne t\in\ker\lambda\).  Hence for each such \(C,t\),
\[
                |C\cap M_a|\le |C\cap M_{a+t}|.            \tag{39}
\]
The three right-hand classes partition \(C-M_a\), so
\[
                         |C-M_a|\ge3|C\cap M_a|,\qquad
                         |C|\ge4|C\cap M_a|.                \tag{40}
\]
If equality holds in one instance of (39), switching \(t\) on \(C\) is a
cardinality-neutral simple-cycle exchange and (33) must hold.  If it
violates (33), the lexicographic minimizer cannot have positive defect.

### Dirty component cuts

For a dirty component \(Q\) of \(H\), every edge of \(\delta(Q)\) has
\(\lambda\)-value one.  The affine-parity calculation shows that each of
the four affine value classes
\[
                   a,\ a+p,\ a+q,\ a+p+q                  \tag{41}
\]
occurs an odd number of times on \(\delta(Q)\).  Therefore
\[
                              |\delta(Q)|\ge4              \tag{42}
\]
and the cut size is even.  If both shores contain cycles in a cyclically
5-edge-connected graph, its size is at least six.

The simultaneous data (20)–(21), (25), (32)–(42) are a rigorous
minimum-class normal form.  The 130-vertex theorem proves that no
unrestricted argument can force (27) from this normal form.

### A precise restricted neutral-circuit lemma

The following remains a possible proof target only on a proposed
restricted domain not containing the 130-vertex countermodel (for example
cyclically 4-edge-connected graphs of girth at least 10):

> **Neutral-circuit target.**  In every positive-defect lexicographic
> minimizer above, there exist \(0\ne t\in\ker\lambda\) and a circuit
> \(C\subseteq F\) such that
> \[
> |C\cap M_a|=|C\cap M_{a+t}|
> \quad\text{and}\quad
> 2|D\cap\operatorname{supp}\tau_t(C)|
>   >|\operatorname{supp}\tau_t(C)|.
> \tag{43}
> \]

Switching on \(C\) preserves the global minimum class size and strictly
decreases the secondary defect.  A universal theorem of this form is
false by (28a); any proof must use the additional domain hypotheses.

The exact obstruction to (43) is also explicit: for every circuit and
kernel direction, either the class-size inequality (39) is strict, or
the equality case satisfies the coset-leader inequality (33).  A proof
must rule out this combined “strict-size barrier / neutral coset leader”
configuration using connectivity and girth.  Neither connectivity nor
girth has yet been shown to do so.

A useful one-for-one neutral exchange has the following exact graphic
criterion.  Fix a quotient nonzero color \(c\), an edge \(e\in M\), and
an edge \(g\) of quotient color \(c\).  A switch replacing precisely
\(e\) by \(g\) exists exactly when \(e\) and \(g\) lie on a common circuit
of
\[
                   G-\bigl((M-\{e\})\cup(E_c-\{g\})\bigr). \tag{44}
\]
Such a circuit contains one zero and one \(c\)-edge, so an appropriate
lift of the quotient switch is automatically legal.  Formula (44)
reduces single neutral exchange to a standard cycle-matroid/block test.
The bridge barriers (20) say where its candidate \(g\)'s must cross, but
do not guarantee a common circuit.

For fixed \(c\), all \(M\)-edges are bridges in \(G-E_c\); their
fundamental shores form a laminar bridge-block forest after rooting.
This laminar system is the natural object for a cyclically-4/girth-10
proof attempt.  What remains missing is a theorem forcing either a
one-for-one circuit (44) that improves \(\delta\), or a multi-edge neutral
exchange satisfying the majority condition (33).

## 8. Exact order-22 every-minimizer countermodel

The public package

```text
search/global-minimum-nonpacking-22v-20260729/
```

freezes:

- graph6
  `U??????_A?E?I?B@A_Os?GoBA?A@_C@O?D_??U??`;
- source quotient masks
  \(p=516851579,\ q=7175781286\);
- source zero set \(M=\{14,30\}\);
- an explicit lift \(T\)-join and all 33 nowhere-zero
  \(\mathbb F_2^3\) values, with \(M_4=M\);
- exhaustive rejection of class size below two over all
  \(4096^2=16,777,216\) quotient flows;
- exhaustive nonpacking of the source over the 4,096-word cycle space;
- a neutral quotient switch to \(M'=\{3,30\}\);
- two explicit disjoint joins proving that \(M'\) packs; and
- a short parity/cut proof of the displayed nonpacking support; and
- a dependency-free exhaustive checker with a frozen SHA-256 ledger.

The standalone standard-library replay reports:

```text
minimum class size                 2
ordered minimum quotient states   19,440
distinct minimum supports         222
nonpacking minimum supports       11
source {14,30} packs              no
target {3,30} packs               yes
```

Package ledger:

```text
search/global-minimum-nonpacking-22v-20260729/SHA256SUMS
SHA-256 bea55e8e14c86bac15cb5cab9ffa6b12fe3be1bb50332fdfb1001098d41b17a9
```

The graph, both literal lifts, the complete quotient enumeration, the
packing-support census, the human obstruction, and both joins are checked
inside that public package.

## 9. Stress tests and exact logical gaps

### Order 12: simple-cycle plateau, not binary-support obstruction

The checked order-12 state has
\[
                         \min_\lambda d_\lambda=2.
\]
All 100 legal simple-cycle/value neighbors remain bad and none strictly
decreases that minimum.  Nevertheless its value-5 matching already
packs.  The packing support decomposes into two disjoint simple cycles,
both switched by value 5; their union reaches a good flow.

Therefore:

- local minimality under one **simple circuit** does not imply packing or
  defect descent;
- packing gives one arbitrary Eulerian/binary support, not necessarily
  one connected circuit; and
- the order-12 example does not refute an arbitrary binary-support
  switch lemma, because the two circuits can be switched simultaneously.

### APX36

The displayed flow has class sizes
\[
                         5,10,7,9,7,6,10
\]
and all seven displayed classes are nonpacking.  All 21 fixed-coordinate
kernel cleanup systems are UNSAT.  Thus “choose the least frequent value
of the current flow” and “one kernel direction cleans a fixed coordinate”
are false local rules.

This displayed flow is not globally class-minimal.  A separate exact
computation finds \(\rho_3=2\), 598 distinct global-minimum supports,
and all 598 packing.  It was a positive instance of the then-proposed
property (27), not evidence strong enough to justify it, and is not part
of the order-22 package cited above.

### The 144-vertex score-zero flow

Its class sizes are
\[
                         33,31,31,33,34,26,28.
\]
All seven classes are nonpacking, and all 21 arbitrary binary-cycle
repair incidences are certified UNSAT.  Therefore no single binary switch
creates a packing class, and no two-switch route of the form “arbitrary
switch, then distinguished-value packing switch” reaches good.

The same graph has an explicit FiveCDC and a different induced good flow.
Thus the state shows that fixed-flow coordinate selection, least-class
selection, and shallow repair can all fail simultaneously.  It says
nothing about \(\rho_3\) or \(\delta_\rho\) for that graph.

### Global defect minimization is circular

Let \((f,\lambda)\) attain (2), and choose any \(a\) with
\(\lambda(a)=1\).  If \(M_a(f)\) packs, (7) constructs a new flow with
defect zero.  Hence \(\beta(G)=0\).  Conversely, if
\(\beta(G)=0\), the canonical \(J_0\) and the \(T\)-join in \(H\) are
disjoint, so every eligible \(M_a\) packs.  Therefore
\[
\boxed{\ \text{a global defect minimizer has a packing class}
        \iff\beta(G)=0.\ }                                 \tag{45}
\]
Using (45) as the missing proof step merely restates the conjecture.

If instead one minimizes a total such as
\(\sum_\lambda d_\lambda(f)\), no packing implication follows from the
fixed-pair theorem: an affine switch can clean one line while splitting
and merging components on the other six.  No monotonicity formula for
that total has been proved.

## 10. Recommended restricted theorem/search target

Neither “every minimum class packs” nor “some minimum class packs” is a
viable unrestricted route.  A reduced-domain experiment may still:

1. choose a lexicographic \((|M|,\delta)\)-minimizer;
2. use the three simultaneous bridge-barrier forests (20);
3. normalize its canonical join to the forest/saturated-cut form
   (24)–(25);
4. exploit the four-odd affine boundary pattern (41) on every dirty
   component; and
5. test whether the extra cyclic-connectivity and girth hypotheses force
   a neutral exchange violating (33).

An exact computational screen should search directly for lexicographic
states satisfying all blocker conditions:

- positive \(\delta\);
- all inequalities (18);
- the three bridge barriers for every minimum-class edge;
- every neutral kernel cycle obeying (33); and
- no one-for-one exchange (44) decreasing \(\delta\).

Finding such a state in the restricted domain would refute the restricted
neutral-circuit lemma, not FiveCDC.  Proving none exists would be useful
only after either proving that a smallest FiveCDC counterexample lies in
that domain or embedding the restricted result into a separate complete
argument.

## AI-use disclosure

OpenAI Codex agents under human direction derived the new lemmas, lift,
checker, and this memo, and audited the cited computational artifacts.
The cited project “independent” checkers are implementation-independent,
not independent of AI.  These arguments and computations require
independent human review before publication.
