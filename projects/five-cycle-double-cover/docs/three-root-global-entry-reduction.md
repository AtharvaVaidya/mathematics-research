# The three-root global-entry reduction

Status: **proved reduction and exact finite audit; not a proof of the
Five-Cycle Double Cover Conjecture**.

Audit date: 2026-07-27.

This note tests the following proposed global entry into the standard
Five-Cycle Double Cover Conjecture (FiveCDC).  In a simple cyclically
4-edge-connected cubic graph \(G\), choose a three-edge matching \(R\) that
does not extend to a perfect matching.  Put
\[
             U=V(R),\qquad H=G-U.
\]
Choose a maximum matching \(P\) of \(H\), put \(M=R\cup P\), and try to use
\(M\) as the exact zero set of an \(\mathbb F_2^2\)-flow.  The calculation
below gives a sharp deficiency bound, completely classifies the resulting
two- and four-branch suppressed complements, and gives exact finite
conditions for the extra component-parity certificate that would imply a
standard FiveCDC.

The route does **not** by itself prove FiveCDC.  The Petersen graph is a
small, human-checkable warning: every nonextendable three-edge root and
every maximum choice \(P\) passes the four-flow test but fails the
component-parity test, although an explicit FiveCDC of the Petersen graph
is displayed below.

Throughout, a cycle means an Eulerian edge set, not necessarily connected.
The standard phrase “at most five” is equivalent here to five coordinates:
pad a shorter list by empty Eulerian edge sets.  No orientation condition is
imposed.

## 1. The sharp deficiency bound

Write
\[
 \operatorname{def}(H)=
 \max_{S\subseteq V(H)}\bigl(o(H-S)-|S|\bigr),
\]
where \(o\) counts odd components.

> **Theorem 1 (three-root deficiency).**
> Let \(G\) be a finite simple cyclically 4-edge-connected cubic graph and
> let \(R\) be a matching of size three.  If \(R\) does not extend to a
> perfect matching, then
> \[
>                         \operatorname{def}(G-V(R))\in\{2,4\}.
> \]
> Both values occur in the Petersen graph.

**Proof.**
Let \(S\subseteq V(H)\), set \(s=|S|\), and let
\(Q_1,\ldots,Q_t\) be the odd components of \(H-S\).  Every nonempty
proper shore of \(G\) has at least three boundary edges.  One way to see
the only delicate part is that an induced connected forest \(X\) in a
cubic graph has
\[
              |\delta(X)|=3|X|-2(|X|-1)=|X|+2;
\]
thus a shore of boundary at most two cannot be a forest, on either side,
and would contradict cyclic 4-edge-connectivity.

Every edge leaving a \(Q_j\) ends in \(S\cup U\).  Hence
\[
  3t\le\sum_j|\delta_G(Q_j)|
      \le 3s+|\delta_G(U)|.
\]
The six vertices in \(U\) have total degree \(18\), and the three edges of
\(R\) lie in \(G[U]\).  Consequently
\[
             |\delta_G(U)|
             =18-2|E(G[U])|\le 12.
\]
It follows that \(t-s\le4\) for every \(S\), so Tutte--Berge gives
\(\operatorname{def}(H)\le4\).  The order of \(H\) is even.  Because \(R\)
does not extend, \(H\) has no perfect matching; its deficiency is therefore
a positive even integer.  This proves the assertion. \(\square\)

The usual existence of a nonextendable three-edge matching in a cubic
graph of sufficient order can also be read from the standard minimum-degree
condition for 3-extendability.  The reduction above needs only the chosen
nonextendable \(R\), so no matching-extendability theorem is used in its
proof.

## 2. Equality at deficiency four

> **Theorem 2 (rigidity of the deficiency-four branch).**
> Under the hypotheses of Theorem 1, suppose a barrier \(S\) satisfies
> \(o(H-S)=|S|+4\).  Then:
>
> 1. \(|\delta(U)|=12\), so the only edges of \(G[U]\) are the three roots;
> 2. \(H-S\) has no even component;
> 3. every component of \(H-S\) is a singleton; and
> 4. with \(D=V(H)\setminus S\) and \(W=U\cup S\),
>    \(D\) is independent, \(|W|=|D|+2\), and \(E(G[W])=R\).

**Proof.**
Every inequality in
\[
 3(|S|+4)\le
 \sum_Q|\delta(Q)|
 \le3|S|+|\delta(U)|
 \le3|S|+12
\]
is equality.  Thus every odd component has boundary three, all edge
capacity at \(S\) and \(U\) is used by those components, and
\(|\delta(U)|=12\).  An even component would have no edge to the rest of
the connected graph, so none exists.

A boundary-three odd component is a singleton.  Indeed, if it is a tree,
the displayed forest formula gives \(|Q|=1\).  If it contains a cycle, its
complement also contains a cycle: a forest complement with at least the six
vertices of \(U\) has boundary at least eight.  The shore would then be a
cyclic 3-edge-cut, a contradiction.

Therefore \(D\) is independent and
\[
 |D|=|S|+4,\qquad |W|=|S|+6=|D|+2.
\]
There are \(3|D|\) \(D\)-to-\(W\) edges.  Cubic degree counting on \(W\)
gives
\[
 2|E(G[W])|=3|W|-3|D|=6.
\]
The three roots already lie in \(E(G[W])\), proving the last claim.
\(\square\)

This branch is already closed for the **standard** conjecture.  More
generally, if a bridgeless cubic graph has a partition
\(V(G)=D\mathbin{\dot\cup}W\), with \(D\) independent and
\(|W|=|D|+2\), then \(G[W]\) has three edges.  Choose one such edge \(t\).
The edge-prescribed Petersen theorem gives a perfect matching containing
\(t\).  Counting at \(D\) shows that this perfect matching contains exactly
one edge of \(G[W]\).  Its complementary 2-factor therefore contains only
the other two \(W\)-edges.  A circuit of the 2-factor is odd precisely when
it contains an odd number of those two edges, so the 2-factor has zero or
two odd circuits.  The Huck--Kochol small-oddness theorem supplies a
standard FiveCDC.

This is not a prescribed-root certificate: it does not say that
\(R\cup P\) is the exact zero set in a certificate of the required form.

## 3. The suppressed complement kernels

Let \(d=\operatorname{def}(H)\), let \(P\) be any maximum matching of
\(H\), and put
\[
                       M=R\cup P,\qquad F=G-M.
\]
The \(d\) vertices missed by \(P\) have degree three in \(F\); every other
vertex has degree two.  Suppress the maximal paths whose internal vertices
have degree two, retaining components that are circuits.  The branch
kernel \(K\) is a cubic multigraph on \(d\) vertices.  A loop records a
suppressed path returning to the same branch.

Flow values are constant along a suppressed degree-two path.  A circuit
component is always flowable.  Hence \(F\) has a nowhere-zero
\(\mathbb F_2^2\)-flow if and only if \(K\) does.

For \(d=2\), there are exactly two kernels:

| kernel | edge multiset | nowhere-zero \(\mathbb F_2^2\)-flow? |
|---|---|---:|
| theta | three parallel links | yes |
| dumbbell | a link and one loop at each end | no |

For \(d=4\), there are exactly eight kernels up to isomorphism:

| kernel | prototype edge multiset | flow? |
|---|---|---:|
| \(K_4\) | all six pairs | yes |
| doubled four-cycle | \(02,03,03,12,12,13\) | yes |
| theta + theta | \(01,01,01,23,23,23\) | yes |
| theta + dumbbell | disjoint union of those types | no |
| dumbbell + dumbbell | disjoint union | no |
| connected, one loop | \(01,02,03,12,12,33\) | no |
| connected, two loops | \(01,01,03,12,22,33\) | no |
| connected, three loops | \(01,02,03,11,22,33\) | no |

The five negative types contain a nonloop bridge.  A flow is zero on a
bridge.  The three positive types have direct nonzero
\(\mathbb F_2^2\)-flows (equivalently, proper three-edge-colourings at the
branch vertices).  This proves the classification once the eight cubic
multigraphs are listed.  The checker independently generates every
degree-three loop/multiplicity vector and obtains exactly these eight.

## 4. Exact component-parity condition

The project's matching/four-flow equivalence says that the flow condition
alone is not enough.  One also needs a spanning odd factor
\(J\subseteq F\) such that every component of \(J\) contains an even number
of endpoints of \(M\).

Every component of an odd factor has even order.  The endpoints of \(M\)
are all vertices except the \(d\) branch vertices.  Thus the condition is
equivalent to:

> every component of \(J\) contains an even number of branch vertices.

Give every suppressed kernel edge one of three statuses:
\[
\begin{array}{c|l}
D&\text{path length }1\text{ (a direct branch edge)},\\
O&\text{odd path length at least }3,\\
E&\text{even path length}.
\end{array}
\]
Let \(a,b\in\{0,1\}\) record whether the two end edges of a path are
selected in \(J\).  Since every internal degree-two vertex must have
selected degree one, the selected edges alternate.  Therefore
\[
       D\text{ or }O:\ a=b,\qquad E:\ a\ne b.             \tag{4.1}
\]
At each branch, the sum of its three incidence bits is odd.  Only a
selected \(D\)-edge joins two branch vertices in the same component:
selected edges on an \(O\)- or \(E\)-path stop before joining its two
branches.  Thus the branch components of \(J\) are exactly the components
of the selected \(D\)-edge graph.  A branch-free circuit component admits
an odd factor exactly when its length is even.

Equations (4.1), odd parity at each branch, even branch-component sizes,
and even branch-free circuits are a necessary and sufficient finite test.
For the four flowable kernels it simplifies as follows:

| kernel | good \(D/O/E\) signatures |
|---|---|
| theta | the number of \(E\)'s is even and at least one edge is \(D\) |
| theta + theta | the theta condition holds separately in both components |
| \(K_4\) | the number of \(E\)'s is even and every component of the available \(D\)-edge graph has even order |
| doubled four-cycle | the \(K_4\)-style condition, except the special family below |

For the doubled four-cycle, use edge order
\[
                         02,03_a,03_b,12_a,12_b,13.
\]
The exceptional bad family has \(02=13=D\), exactly one \(E\) in each
parallel pair, and at least one of the two non-\(E\) parallel mates equal
to \(O\).

The exact numbers of good signatures are
\[
\begin{array}{c|c|c}
\text{kernel}&\text{all signatures}&\text{good signatures}\\ \hline
\theta&27&10\\
\theta+\theta&729&100\\
K_4&729&125\\
\text{doubled four-cycle}&729&129.
\end{array}
\]
These formulas are checkable by the finite parity system (4.1).  The
standard-library checker exhausts all signatures and asserts both the
closed forms and the counts.

Consequently the three-root route has been reduced to a precise selection
problem: find a nonextendable root \(R\) and a maximum matching \(P\) for
which (i) the kernel is one of the flowable types, (ii) every branch-free
circuit is even, and (iii) the displayed status condition holds.  The
selection claim is false in general, as the next section shows.

## 5. Smallest focused warning: the Petersen graph

Use the vertex set \(\{0,\ldots,9\}\) and edge set
\[
\begin{split}
&01,04,05,12,16,23,27,34,38,49,\\
&57,58,68,69,79.
\end{split}
\]
The exact audit gives:

| item | count |
|---|---:|
| three-edge matchings \(R\) | 145 |
| extendable roots, deficiency \(0\) | 60 |
| nonextendable roots, deficiency \(2\) | 80 |
| nonextendable roots, deficiency \(4\) | 5 |
| maximum choices \(P\) over all nonextendable roots | 185 |
| choices whose complement is flowable | 185 |
| choices satisfying component parity | 0 |

For a deficiency-two representative, take
\[
                   R=\{01,23,58\}.
\]
Then \(H\) is the claw on \(\{4,6,7,9\}\), centered at \(9\).  For
\(P=\{49\}\), suppression of \(G-(R\cup P)\) gives a theta with path
lengths \(3,6,2\), hence status \(O,E,E\).  It has a nowhere-zero
\(\mathbb F_2^2\)-flow, but there is no direct \(D\)-edge, so the two
branches cannot lie in one even branch-component of an odd factor.

For a deficiency-four representative, take
\[
                   R=\{01,38,79\}.
\]
Then \(H\) is the independent set \(\{2,4,5,6\}\), so \(P=\varnothing\).
The kernel is \(K_4\), with all six path lengths equal to two.  Its
signature is \(E^6\): the flow exists, but the available \(D\)-graph has
four isolated vertices.

This invalidates the universal claim
“some nonextendable three-root maximum matching always supplies the exact
matching/component-parity certificate,” even in the smallest snark.  It
does **not** obstruct FiveCDC.  A checked FiveCDC of the same Petersen
graph is:
\[
\begin{array}{c|l}
C_1&01,04,12,23,34\\
C_2&01,05,16,58,68\\
C_3&04,05,49,57,79\\
C_4&23,27,38,68,69,79\\
C_5&12,16,27,34,38,49,57,58,69.
\end{array}
\]
Each row is a circuit and every Petersen edge occurs in exactly two rows.

## 6. Boundary information still obtained at deficiency two

Let \(S\) be a tight barrier with \(o(H-S)=|S|+2\), and write
\(b=|\delta(U)|\).  If the odd components have boundaries \(q_i\), then
\[
             \sum_i(q_i-3)\le b-6.                       \tag{6.1}
\]
Here \(b\) is even and \(b\le12\), so
\[
                         b\in\{6,8,10,12\}.
\]
Every \(q_i=3\) component is a singleton by the proof of Theorem 2.  Since
every \(q_i\) is odd, (6.1) leaves:

| \(b\) | possible non-singleton odd shores |
|---:|---|
| 6 | none |
| 8 | at most one boundary-5 shore |
| 10 | at most two boundary-5 shores, or one boundary-7 shore |
| 12 | at most three boundary-5 shores; or one boundary-7 plus one boundary-5; or one boundary-9 shore |

This is a finite **boundary-size** reduction, not a finite list of
multipoles: the internal order of a boundary-5, -7, or -9 odd shore is not
bounded by this argument.  No factor-criticality is needed here.  Any claim
that (6.1) alone yields a finite graph list would be false.

## 7. Reproduction and scope

Run:

```sh
python3 scratch/three_root_global_entry_checker.py \
  --output scratch/three-root-global-entry.json
```

The checker uses only the Python standard library.  It:

1. canonically generates the two- and four-branch cubic multigraph kernels;
2. checks their nowhere-zero \(\mathbb F_2^2\)-flows;
3. checks every \(D/O/E\) signature and the closed forms above;
4. enumerates every Petersen three-edge root and maximum matching;
5. independently checks the flow and odd-factor conditions on the
   unsuppressed complement; and
6. checks the displayed Petersen FiveCDC edge by edge.

The JSON result is a complete finite audit output, not an UNSAT certificate
for FiveCDC and not a counterexample.  No SAT solver is used in this
particular reduction.

## 8. Novelty and publication assessment

The deficiency inequality, the two-branch theta/dumbbell observation, and
small-oddness closure are close to standard matching/flow techniques and
should not be advertised as a major theorem without a literature review.
The exact four-branch kernel list, the \(D/O/E\) component-parity formulas,
and the exhaustive Petersen failure of the three-root selection route may
be useful as a short computational/structural note or as a rigorous section
of a broader research report.  Standing alone, they do not resolve an open
conjecture and are probably not yet strong enough for a high-impact
preprint.

A defensible preprint should state “partial structural reductions and
negative controls,” invite specialist checking, include the checker and
frozen output, and avoid implying that bounded experiments establish a
universal theorem.

## References used for convention and context

1. A. Huck and M. Kochol, *Five cycle double covers of some cubic graphs*,
   Journal of Combinatorial Theory, Series B 64 (1995), 119--125,
   <https://doi.org/10.1006/jctb.1995.1029>.
2. A. Huck, *On cycle-double covers of graphs of small oddness*, Discrete
   Mathematics 229 (2001), 125--165,
   <https://doi.org/10.1016/S0012-365X(00)00205-3>.
3. A. Hoffmann-Ostenhof, *A note on 5-cycle double covers*, Graphs and
   Combinatorics 29 (2013), 977--979,
   <https://arxiv.org/abs/1209.0096>.
4. D. Mattiolo et al., *Geometric description of d-dimensional flows of a
   graph*,
   Australasian Journal of Combinatorics 94 (2026), 376--384,
   <https://ajc.maths.uq.edu.au/pdf/94/ajc_v94_p376.pdf>.
5. S. Oum, *A proof of the Cycle Double Cover Conjecture by OpenAI: an
   exposition* (2026), <https://arxiv.org/abs/2607.16356>.  The exposition
   explicitly distinguishes the now-proved unrestricted CDC statement from
   the stronger FiveCDC, which it records as open.

## AI-use disclosure

This research note and its checker were developed with extensive assistance
from OpenAI Codex language models.  The models proposed reductions, wrote
and debugged code, performed finite enumerations, and drafted mathematical
arguments.  Human authors remain responsible for independently checking
every proof, running the software, verifying the literature and novelty
claims, and approving any public release.  No claim here should be treated
as peer reviewed.
