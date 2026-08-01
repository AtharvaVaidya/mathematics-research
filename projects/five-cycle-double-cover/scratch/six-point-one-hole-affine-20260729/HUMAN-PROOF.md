# Six-point one-hole compression is an affine FiveCDC lift

Date: **2026-07-29**

Status: **HUMAN-CHECKABLE EXACT CHARACTERIZATION / STRICTLY BROADER
THAN THE FIXED-FLOW FIVE-POINT LIFT / NOT A RESOLUTION OF FiveCDC**.

This note isolates a nonlinear compression of the July 2026
eight-coordinate triangle construction.  An eight-coordinate cover need
not be supported on only five points.  It is enough that it be supported
on six points and omit one pair among those six: identify the two
non-co-occurring points.

For a fixed nowhere-zero Fano flow, fixed omitted pair, and fixed merge
pair, the whole question is one affine system over \(\mathbb F_2\).
Unlike the five-point restriction, the local variables can live on
several Fano lines at once.

The graph-level existential statement is exactly FiveCDC.  The new
content is the fixed-flow affine normal form, the complete local list,
and a strict 34-vertex witness showing that it goes beyond every
five-point restriction of the same flow.

## 1. Coordinate triangles and potentials

Put \(W=\mathbb F_2^3\).  Let \(G\) be a finite loopless cubic
multigraph and let
\[
                 f:E(G)\longrightarrow W-\{0\}
\]
be a flow.  At every vertex \(v\), the three incident values are the
nonzero points of a Fano plane
\[
                 H_v=\{0\}\cup\{f(e):e\ni v\}.
\]

For \(t\in W\), define
\[
                 \Delta_H(t)=(t+H)-\{t\}.                    \tag{1}
\]
This is a three-point affine triangle.  Its three sides have differences
equal to the three nonzero points of \(H\).

If \(e\ni v\), put \(p=f(e)\), and choose either one of the other two
incident values \(s_{v,e}\).  The side of \(\Delta_{H_v}(t_v)\) having
difference \(p\) is
\[
       P_{v,e}=t_v+s_{v,e}+\langle p\rangle
       =\{t_v+s_{v,e},t_v+s_{v,e}+p\}.                       \tag{2}
\]
The other choice of \(s_{v,e}\) differs by \(p\), so (2) is independent
of that choice.

For an edge \(e=uv\), the two endpoint labels agree exactly when
\[
 t_u+t_v+s_{u,e}+s_{v,e}\in\langle f(e)\rangle.               \tag{3}
\]
After applying either of the two nonzero linear functionals annihilating
\(f(e)\), equation (3) becomes two scalar affine equations over
\(\mathbb F_2\).

Conversely, every compatible two-point cover with pair differences
\(f\) gives a unique \(t_v\): the three incident pairs form a triangle,
and \(t_v\) is the xor of its three coordinate points.  Thus (1)--(3)
parameterize exactly all compatible coordinate-triangle covers for
the fixed flow.

## 2. Six used points and one missing pair

Choose disjoint two-subsets
\[
                         R,M\in\binom W2,
 \qquad R\cap M=\varnothing.                                 \tag{4}
\]
The points of \(R\) are forbidden, so the support is
\[
                         S=W-R,\qquad |S|=6.                 \tag{5}
\]
The pair \(M\subset S\) is also forbidden as an edge label.

For a Fano plane \(H\), define the local list
\[
 {\cal A}_H(R,M)=
 \{t\in W:\Delta_H(t)\subseteq S,\ M\nsubseteq\Delta_H(t)\}.  \tag{6}
\]
The second condition says exactly that none of the three sides of the
local triangle is \(M\).

> **Theorem 2.1 (affine six-point one-hole criterion).**
> For fixed \(G,f,R,M\), a compatible coordinate-triangle cover
> supported in \(S=W-R\) and not using \(M\) exists if and only if the
> following affine system is soluble:
> \[
>                         t_v\in{\cal A}_{H_v}(R,M)
>                                                        \quad(v\in V(G)),
>                                                                    \tag{7}
> \]
> \[
> t_u+t_v+s_{u,e}+s_{v,e}\in\langle f(e)\rangle
>                                                        \quad(e=uv).
>                                                                    \tag{8}
> \]
> Every set in (7) is a nonempty affine subspace of \(W\), of dimension
> zero, one, or two.  Hence (7)--(8) is an ordinary affine system over
> \(\mathbb F_2\), decidable by Gaussian elimination.

The equivalence between a solution and compatible labels is immediate
from (1)--(3).  The claim that every local list is affine follows from
the complete calculation below.

## 3. Complete local list

Translate the coordinate points so that
\[
                     R=\{0,d\},\qquad M=\{a,b\},
 \qquad m=a+b.                                               \tag{9}
\]
Translation changes neither pair differences nor Fano planes.

There are two affine orbits for the ordered pair \((R,M)\).

* **Parallel:** \(m=d\).  Then \(R\cup M\) is the plane
  \(H_0=\langle d,a\rangle\).
* **Skew:** \(m\ne d\).  Disjointness forces
  \(a\notin\langle d,m\rangle\), so \(d,m,a\) are a basis of \(W\).

The local lists are as follows.

### Parallel case

\[
{\cal A}_H(R,M)=
\begin{cases}
W-H,&H=H_0,\\
M,&d\in H,\ H\ne H_0,\\
R,&d\notin H.
\end{cases}                                                  \tag{10}
\]
The seven list sizes are
\[
                         4,2,2,2,2,2,2.                      \tag{11}
\]

### Skew case

\[
{\cal A}_H(R,M)=
\begin{cases}
M,&d,m\in H,\\
W-H,&d\in H,\ m\notin H,\\
\{r\in R:a+r\notin H\},&d\notin H,\ m\in H,\\
R,&d,m\notin H.
\end{cases}                                                  \tag{12}
\]
The seven list sizes are
\[
                         4,4,2,2,2,1,1.                      \tag{13}
\]

To check the table, first ignore \(M\).  If \(d\in H\), the two
forbidden points \(0,d\) lie in the same \(H\)-coset, so the triangle
must use the other coset; its omitted point \(t\) may initially be any
of the four points of that coset.  If \(d\notin H\), the forbidden
points lie in opposite cosets, and the only possible omitted points
are \(t=0,d\).

Now impose the missing-pair condition.  If \(m\notin H\), the two
members of \(M\) lie in opposite \(H\)-cosets and can never both occur
in one triangle.  If \(m\in H\), they lie in one coset.  When that is
the chosen coset, one of \(a,b\) must itself be the omitted point.
This gives (10) and (12) case by case.

Every displayed set is a point, an affine line, or an affine plane.
This proves the last assertion of Theorem 2.1 without computation.

There are \(28\cdot15=420\) disjoint choices of \((R,M)\): 84 parallel
and 336 skew.  Literal enumeration over all seven Fano planes gives
6,720 admitted local triangles.  Both supplied implementations
reconstruct these totals independently.

## 4. Why one hole compresses six coordinates to five

Let a solution of (7)--(8) be given.  The labels (2) use only the six
points of \(S\), and none equals \(M=\{a,b\}\).  Identify \(a\) and
\(b\), leaving the other four points distinct.  This gives five
coordinate names.

No used pair collapses to a singleton, because \(M\) is the only pair
whose two endpoints are identified and \(M\) is unused.  Each old
coordinate has even degree at every graph vertex; after the
identification, the new merged coordinate has degree equal modulo two
to the sum of the old \(a\)- and \(b\)-degrees.  It too is even.
Thus the quotient labels are duads on five names and form a standard
FiveCDC.

The permitted 14 pair types make the nonlinear factorization explicit.
Six pairs avoid both \(a,b\) and map injectively to six target duads.
The eight pairs joining one of \(a,b\) to one of the other four points
map two-to-one to the remaining four target duads.  Thus the operation
is not a fixed pointwise map from the seven Fano values to ten duads:
the two preimages of one target duad have differences separated by
\(m=a+b\).

> **Corollary 4.1 (exact graph-level scope).**
> A finite loopless cubic multigraph has a standard FiveCDC if and only
> if there exist \(f,R,M\) for which (7)--(8) is soluble.

The reverse direction was just proved.  For the forward direction,
inject the five coordinate names of a FiveCDC into any five members of
a six-set \(S\subset W\), leaving the sixth point unused.  Take \(M\)
to join that unused point to any of the five used points.  Xor of each
edge pair gives a nowhere-zero \(W\)-flow, and the original local
triangles give a solution of (7)--(8).

Consequently Corollary 4.1 is an exact reformulation of FiveCDC, not a
proof.  The useful new statement is that **once \(f,R,M\) are fixed,
the nonlinear-looking compression is purely affine**.

## 5. Relation to the Fano component-parity lift

A five-point restriction has local-list profile
\[
                              4,1,1,1,1,1,1:
\]
one special Fano line carries a two-dimensional choice and every other
line is forced.  Eliminating the forced variables leaves precisely the
component-parity system on the special-line subgraph.

The profiles (11) and (13) have freedom on several Fano lines at once.
Their global equations can therefore couple and cancel defects belonging
to different line-component quotients.  They are not another choice of
one special Fano line.

## 6. A strict 34-vertex fixed-flow witness

The retained graph is the simple connected bridgeless cubic graph
encoded by

```text
as???SK????A?A?C_@_?B?@_??G??_I?GA_AA????_??@?????B??@_?o??????_C??CGO??B@????a????__??C@O??A?_
```

Its 51-edge Fano flow and literal compatible labels are frozen in

```text
output/jaeger-star-thinning-countermodel-34v/star-good-six-witness.json
```

with SHA-256

```text
e3160e5f6b2985823a3421e9f3b1a4582c9c8be4b9abfd1f0e2312d311eb8358
```

The displayed cover uses the six points
\[
                           \{0,3,4,5,6,7\}
\]
and uses all 14 pair types except \(45\).  Thus identifying 4 and 5
gives its displayed FiveCDC.

For the **same fixed flow**, exact elimination gives:

* zero soluble systems among all 56 five-point subsets of \(W\);
* eight soluble six-point one-hole systems among all 420 choices of
  \((R,M)\);
* every soluble choice is skew and has affine solution dimension one.

One of the eight is \(R=\{1,2\}\), \(M=\{4,5\}\), the literal cover
above.  Therefore the six-point one-hole normal form is strictly
broader, at fixed flow, than item 68's five-point/component-parity lift.
This is not merely the old pure-merge or forced-\(K_6\) phenomenon.

## 7. Exact dual obstruction

Write (7)--(8), after scalarization, as
\[
                               A x=b                       \tag{14}
\]
over \(\mathbb F_2\).  Here \(x\) has three bits for every vertex.
Every local affine subspace contributes the functionals annihilating its
direction space, and every edge contributes the two-dimensional
annihilator of \(f(e)\).

The system is inconsistent exactly when there is a row multiplier
\[
                         y\in\mathbb F_2^{\operatorname{rows}(A)}
\]
such that
\[
                         y^{\mathsf T}A=0,\qquad
                         y^{\mathsf T}b=1.                    \tag{15}
\]
Indeed, (15) xors a selected family of scalar local and edge equations
to the contradiction \(0=1\).  Conversely, Gaussian elimination of an
inconsistent binary system produces exactly such a row combination.

Thus every failed fixed choice \((f,R,M)\) has a short, independently
checkable parity certificate.  A universal selection proof would have
to show that these dual obstructions cannot exist simultaneously for
all flow and pair choices supplied by a suitable eight-coordinate
construction.  This left-kernel formulation is the natural algebraic
interface for that remaining selection problem.

Two five-row certificates make (15) literal on the 34-vertex flow.

For the failed five-set \(\{0,1,2,3,4\}\), vertices 0 and 1 both have
the forced potential \(t=7\).  Take the scalar local rows with
functionals 1 and 2 at each vertex.  Their xor is the functional-3 row
at both vertices, with total right side zero.  Edge 0 joins those
vertices, has flow value 3, and its functional-3 compatibility row has
right side one.  Xoring the five rows cancels every variable and gives
\(0=1\).

For the failed six-hole choice
\[
                    R=\{0,1\},\qquad M=\{2,3\},
\]
vertices 4 and 8 both have local list \(\{2,3\}\).  At each vertex,
xor the functional-4 row of right side zero with the functional-6 row
of right side one; this leaves functional 2.  Edge 5 joins vertices
4 and 8, has flow value 1, and its functional-2 compatibility row has
right side one.  Again all coefficients cancel and the five right
sides xor to one.

The primary audit emits the exact row indices and row metadata for both
certificates and directly re-xors the original coefficient rows.

## 8. Reproduction

Primary Python audit:

```sh
python3 scratch/six-point-one-hole-affine-20260729/audit_six_point_one_hole_affine.py
```

Independently structured JavaScript replay:

```sh
node scratch/six-point-one-hole-affine-20260729/verify_six_point_one_hole_affine.mjs
```

The Python checker uses full row reduction; the JavaScript checker uses
an incremental highest-pivot xor basis.  Both independently enumerate
the 2,940 local \((R,M,H)\) rows, verify the graph and literal cover,
test all 56 five-sets and all 420 six-point one-hole choices, and obtain
the same eight strict passes.

## Scope and AI-use disclosure

The theorem is for finite loopless cubic multigraphs; parallel edges
cause no change.  No claim is made here for unsuppressed higher-degree
vertices or loops.  Existing project reductions may be applied only
with their separately audited hypotheses.

OpenAI Codex agents, under human direction, discovered the six-point
one-hole affine normal form, derived the local tables and dual, wrote
both exact implementations, and drafted this proof.  The implementations
are independent in structure but both are AI-authored.  This is not
independent human peer review and not a proof or disproof of FiveCDC.
