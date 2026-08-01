# An edge-rooted Moore count and the first external-coverage order

Date: **2026-07-31**

Status: **HUMAN-CHECKABLE STRUCTURAL THEOREM / BOUNDED DEVELOPMENT
SCREEN / NOT A UNIVERSAL EXTERNAL-COVERAGE THEOREM / NOT A PROOF OF
FIVECDC**.

## 1. Setting

Let `(A,z,r)` be a relevant rooted cap in the minimum-counterexample
three-cut branch.  Thus `A` is a simple cubic graph, `z` is the cap
vertex, and `r` is a proper edge not incident with `z`.  Put

\[
                    K=A-z,\qquad L=K-r,\qquad n=|V(K)|.
\]

The already proved cap reduction gives the following facts, and these are
the only facts used below.

1. `K` is connected and bridgeless, has three vertices of degree two and
   all other vertices of degree three.
2. `L` has girth at least ten.
3. `K` contains a circuit and has girth at least nine.

The degree sum of `K` is `3n-3`, so `n` is odd.  Deleting `r` gives

\[
 |E(L)|=m={3n-5\over2},\qquad
 \sum_{v\in V(L)}(3-d_L(v))=5.                       \tag{1}
\]

Notice that an endpoint of `r` is allowed to have degree two in `K`.
Such an endpoint has degree one in `L`.  The argument below explicitly
allows this case.

## 2. Nonbacktracking-walk estimates

For `j>=1`, let `W_j` be the number of **oriented nonbacktracking walks
of length `j`** in `L`.  Thus a walk counted by `W_j` is a vertex word

\[
 v_0v_1\ldots v_j,\qquad v_{i-1}\ne v_{i+1}.
\]

Let `N_j(v)` be the number of these walks which end at `v`.  Reversal is
a bijection from walks ending at `v` to walks starting at `v`.  Since
`Delta(L)<=3`, after choosing the first edge there are at most two choices
at each further step.  Hence

\[
                         N_j(v)\le d(v)2^{j-1}.          \tag{2}
\]

Write `delta(v)=3-d(v)`.  Extending a length-`j` walk ending at `v`
offers `d(v)-1=2-delta(v)` choices.  Therefore, exactly,

\[
 W_{j+1}=2W_j-\sum_v\delta(v)N_j(v).                    \tag{3}
\]

All degrees of `L` lie in `{1,2,3}`.  For both possible deficient
degrees one has

\[
 (3-d)d=2\quad(d=1,2).
\]

Each deficient vertex consumes at least one unit of the total deficit
five in (1), so there are at most five of them.  Equivalently,

\[
                    \sum_v\delta(v)d(v)\le10.            \tag{4}
\]

Equations (2)--(4) give the recurrence bound

\[
                         W_{j+1}\ge2W_j-10\,2^{j-1}.      \tag{5}
\]

The initial length-two count can be sharpened.  Since
`d=3-delta` and `sum delta=5`,

\[
\begin{aligned}
 W_2
 &=\sum_v d(v)(d(v)-1)\\
 &=6n-5\sum_v\delta(v)+\sum_v\delta(v)^2\\
 &\ge6n-25+5=6n-20.                                    \tag{6}
\end{aligned}
\]

The last inequality uses that the nonnegative integer deficits sum to
five, so their squares sum to at least five.  Degree-one vertices have
deficit two and make this inequality stronger, not weaker.

Applying (5) three times to (6) yields

\[
 W_3\ge12n-60,\qquad
 W_4\ge24n-160,\qquad
 W_5\ge48n-400.                                         \tag{7}
\]

## 3. The edge-rooted girth-ten ball

Fix an edge `uv` of `L`.  Start at `u`, forbid `uv` as the first edge,
and take every nonbacktracking path of lengths one through four.  Do the
same at `v`, forbidding `vu`, and include `u,v` themselves.

All endpoints in this two-sided collection are distinct.  Two paths on
the same side meeting again would contain a circuit of length at most
eight.  Paths from opposite sides meeting would, together with `uv`,
contain a circuit of length at most `4+4+1=9`.  A path meeting `u` or `v`
again gives an even shorter circuit.  All contradict `g(L)>=10`.

Consequently the size of this edge-rooted ball is at most `n`.  Sum over
all `m` choices of `uv`.  The two roots contribute `2m`.  Every oriented
nonbacktracking walk of length `j` for `2<=j<=5` occurs exactly once:
its first edge is the forbidden central edge, and its remaining `j-1`
edges form the path on the side of its second vertex.  Thus

\[
                  mn\ge2m+W_2+W_3+W_4+W_5.              \tag{8}
\]

Substitute `m=(3n-5)/2` and (6)--(7) into (8).  After multiplying by
two and collecting terms,

\[
                         3n^2-191n+1290\ge0.              \tag{9}
\]

Direct integer arithmetic gives

\[
 f(8)=-46<0,\qquad f(55)=-140<0,
 \qquad f(56)=2>0,                                      \tag{10}
\]

where `f(n)=3n^2-191n+1290`.  Its vertex lies between 31 and 32, so it
is negative throughout the integer interval `8<=n<=55`.  Since `K`
contains a circuit of length at least nine, `n>=9`; hence (9) forces
`n>=56`.  Finally `n` is odd, so in fact `n>=57`.

> **Theorem 3.1 (self-contained relevant-cap cutoff).**  Every relevant
> core has at least 57 vertices and every relevant cap has at least 58
> vertices.  If both shores of the eliminated graph are capped, restoring
> the two deleted endpoints gives a parent of order at least
> `57+57+2=116`.

This improves the former bounds `55`, `56`, and `112`, respectively.

## 4. Exact order-58 cage control

The official House of Graphs file `cagesk3g09.g6` contains the complete
18 cubic `(3,9)`-cages on 58 vertices from the Brinkmann--McKay--Saager
classification.  The checker verifies independently that every row is
simple, cubic, connected, has girth nine, and is Tait-colourable.  It also
enumerates every 9-circuit and finds no pair `(z,r)` for which `r` is a
proper edge contained in every 9-circuit avoiding `z`.  Equivalently,
none of these 18 cages has `g((A-z)-r)>=10`.

This is only a control slice.  A relevant order-58 cap may have a short
circuit through `z`, so its whole graph need not be a `(3,9)`-cage.  The
18-row check is therefore not a complete order-58 cap classification.

There is also a useful control at the later subdivision frontier.  If five
degree-two vertices of a girth-ten core are suppressed and the resulting
cubic graph is one of these cages, the five suppressed edge units would
have to hit every 9-circuit.  This is impossible for all 18 cages.  The
checker gives a short positive packing certificate: 16 cages contain six
edge-disjoint 9-circuits; in each of the remaining two it finds eleven
9-circuits such that every edge occurs at most twice.  Five edges can hit at
most five circuits in the first case and at most ten in the second.  This
does not exclude suppressed cubic graphs of girth at most eight and hence
is still not a complete classification of the first possible core order.

## 5. Exact single-flow simultaneous-external SAT characterization

A stronger sufficient target asks for one `D5` flow whose external states
cover all three physical ports.  Normalize the ordered port labels to

\[
                         q(a)=01,\quad q(b)=02,\quad q(c)=12.       \tag{11}
\]

This loses no solutions: at a cubic vertex the three weight-two labels
form a coordinate triangle, and `S5` is transitive on ordered coordinate
triangles.  An external `ab` state uses factor `03` or `04`; external
`ac` uses `13` or `14`; external `bc` uses `23` or `24`.

Two physical pairs cover all three ports exactly when the two pairs are
distinct.  Choose their common physical port.  The swap `3<->4`, which
fixes (11), leaves only two factor orbits: the two factors use the same
outside coordinate, or they use different outside coordinates.  There
are therefore exactly six cases: three choices of two physical pairs,
times these two outside-coordinate orbits.

For each case, `simultaneous_external_sat.py` uses one common `D5` label
word and two copies of the exact transition-boundary connectivity
encoding.  Each copy proves that the root and the common physical port
lie on one circuit of its fixed factor.  The port normalization then
makes the corresponding inactive port label disjoint from that factor,
so both states are external.  Conversely, any single flow with two
distinct external physical pairs can be normalized to one of the six
cases.  Thus the disjunction of the six formulas is equivalent to the
stronger single-flow target.

The script emits both native-XOR extended DIMACS and fully expanded CNF.
Every SAT assignment is checked again from the weight-two labels, vertex
xors, both complete factor components, both inactive ports, and the
three-port union.  An UNSAT solver response is explicitly uncertified;
excluding an interface requires checked proofs for all six cases.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the edge-rooted count,
implemented the replay, and performed the bounded cage screen.  The proof
is fully displayed but has not undergone independent human peer review.
No universal external-coverage or FiveCDC resolution claim is made.
