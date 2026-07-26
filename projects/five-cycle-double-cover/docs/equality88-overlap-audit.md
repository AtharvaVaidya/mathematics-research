# Blind audit of the equality-\(88\) overlap and Kempe contradiction

Date: **2026-07-26**.

Target: `docs/equality88-kempe-girth-contradiction.md`.

Status: **PASS, with one local exposition repair**.  Under the hypotheses
stated in the target note, the overlap lemma and the subsequent Kempe
contradiction are correct.  No finite search or unproved rotation
assumption is needed.

The repair is this: the symmetric difference of two arbitrary circuits
need not itself be a disjoint union of vertex-disjoint circuits; it can
have a vertex of degree four.  In the present \(ac\)-versus-\(bc\)
setting, however, the symmetric difference is \(2\)-regular for a
specific elementary reason proved below.  Thus this wording issue does
not create a gap in the theorem.

This audit treats the equality-case setup as a conditional hypothesis.  It
does not reaudit the earlier minimum-counterexample and exact-zero-flow
reductions.

## 1. Reconstruction of the equality data

Let \(H\) be the connected simple cubic core on \(80\) vertices, properly
edge-coloured by \(a,b,c\).  Let
\[
 S=\{s_0,\ldots,s_7\}
\]
be the universally separated marked matching, precoloured so that every
mark has colour \(c\).  At equality the two factors containing \(c\) are
\[
 H[a,c]=A_0\sqcup\cdots\sqcup A_7,\qquad
 H[b,c]=B_0\sqcup\cdots\sqcup B_7,
\]
where every displayed component is a \(10\)-circuit and
\[
 s_i\in A_i\cap B_i.
\]

Here is the equality count from first principles.  Every marked
\(ac\)-circuit contains exactly one mark, by universal separation.
Undoing suppression replaces that one marked edge by a two-edge path, so
the even core circuit becomes an odd circuit of \(G\).  Since
\(\operatorname{girth}(G)\ge 10\), that odd circuit has length at least
\(11\), and its core circuit has length at least \(10\).  The eight
marked \(ac\)-circuits are vertex-disjoint and \(H\) has \(80\) vertices.
At equality they must therefore all have length \(10\) and must exhaust
the \(ac\)-factor.  The identical argument applies to the \(bc\)-factor.

Let \(K=G-M\).  Undoing the eight suppressions lifts each \(A_i\) and
each \(B_j\) to an \(11\)-circuit
\(\widetilde A_i,\widetilde B_j\) in \(K\), hence in \(G\).

## 2. Exact intersection anatomy

At every old core vertex, an \(ac\)-factor component uses the incident
\(a\)- and \(c\)-edges, while a \(bc\)-factor component uses the incident
\(b\)- and \(c\)-edges.  Therefore
\[
 v\in V(A_i)\cap V(B_j)
\]
if and only if the unique \(c\)-edge incident with \(v\) belongs to both
\(A_i\) and \(B_j\).  In particular:

1. \(A_i\) and \(B_j\) meet exactly along common \(c\)-edges;
2. distinct common \(c\)-edges have disjoint endpoints, since the
   \(c\)-edges form a perfect matching;
3. if \(i\ne j\), every common edge is unmarked; and
4. if \(i=j\), the marked common edge lifts to one common two-edge path,
   while every other common edge remains a one-edge common path.

There is no hidden intersection at a subdivision vertex.  The terminal
on \(s_k\) lies only on the lifts of \(A_k\) and \(B_k\).

Now take one lifted \(A\)-circuit and one lifted \(B\)-circuit.  After
their common paths are cancelled in the symmetric difference, every
remaining support vertex has degree two:

- away from a common path it has the two edges of its unique circuit;
- at an old endpoint of a common path, the shared \(c\)-edge is
  cancelled and the remaining \(a\)- and \(b\)-edges give degree two;
- the internal vertex of a shared marked two-edge path has degree zero.

Thus, in this setting, the nonempty symmetric difference is a
vertex-disjoint union of simple circuits.  It is nonempty because the
old vertices of an \(A\)-circuit use \(a\)-edges whereas those of a
\(B\)-circuit use distinct \(b\)-edges.

Every component of this symmetric difference is a circuit of the
subgraph \(K\subseteq G\), so it has length at least ten.  Consequently,
if its total length is less than \(20\), it has exactly one component.
This supplies the qualification missing from the overly general
symmetric-difference sentence in the target note.

## 3. Diagonal overlaps

Fix \(i\), and suppose \(A_i\) and \(B_i\) have \(r\ge2\) common
\(c\)-edges in the core.  Their lifts share the two-edge path replacing
\(s_i\) and \(r-1\) unmarked edges.  Hence the total size of their common
paths is \(r+1\), and
\[
\begin{aligned}
 \left|E(\widetilde A_i\triangle\widetilde B_i)\right|
  &=11+11-2(r+1)\\
  &=20-2r\\
  &\le16.
\end{aligned}
\]
The symmetric difference is therefore one circuit \(L\).

Choose any common unmarked edge \(e=uv\), which exists because \(r\ge2\).
The vertices \(u,v\) lie on \(L\), while \(e\notin E(L)\).  The edge
\(e\), together with the shorter \(u\)-to-\(v\) arc of \(L\), is a
simple circuit in \(G\) of length at most
\[
 1+\frac{|L|}{2}\le9,
\]
contradicting girth at least ten.  Therefore
\[
                         |E(A_i)\cap E(B_i)|=1.
\]

Notice that the argument deliberately uses an additional unmarked
one-edge chord.  It does not try to use the already subdivided marked
path as a one-edge chord.

## 4. Off-diagonal overlaps of size at least three

Let \(i\ne j\), and suppose that \(A_i,B_j\) have \(r\ge3\) common
\(c\)-edges.  None is marked, so their lifted circuits share exactly
\(r\) one-edge paths.  Thus
\[
 \left|E(\widetilde A_i\triangle\widetilde B_j)\right|
 =22-2r\le16.
\]
As above, the symmetric difference is one circuit \(L\).  Every common
edge is then a chord of \(L\), and any such chord plus a shorter
\(L\)-arc has length at most nine.  This again contradicts the girth.

## 5. The delicate off-diagonal two-overlap case

It remains to consider \(i\ne j\) with exactly two common edges
\(e_1,e_2\).  The symmetric difference has length
\[
                         22-2\cdot2=18.
\]
It cannot have two components, since two circuits in a girth-ten graph
would have total length at least \(20\).  Hence it is one
\(18\)-circuit \(L\).

Deleting \(e_1,e_2\) from \(\widetilde A_i\) leaves two paths, and
deleting them from \(\widetilde B_j\) leaves two paths.  The four paths
occur alternately on \(L\).  Write their positive lengths in cyclic
order as
\[
                  \alpha,\ \beta,\ \gamma,\ \delta,
\]
with the \(\alpha,\gamma\) paths belonging to
\(\widetilde A_i\) and the \(\beta,\delta\) paths belonging to
\(\widetilde B_j\).  Since both original circuits have length \(11\),
\[
                  \alpha+\gamma=9,\qquad
                  \beta+\delta=9.                    \tag{1}
\]

For completeness, the common edges really are the two diagonals of this
four-path circuit.  Regard the two \(A\)-paths, the two \(B\)-paths, and
the two common edges as three pairings of the four path endpoints.
The \(A\)- and \(B\)-pairings differ because their union is the single
circuit \(L\).  The common-edge pairing differs from the \(A\)-pairing
because otherwise adding the two common edges to the two \(A\)-paths
would make two circuits rather than the single circuit
\(\widetilde A_i\).  It differs from the \(B\)-pairing for the same
reason.  There are only three perfect matchings of four objects, so the
common-edge pairing is the third matching: the diagonal pairing of the
four-cycle formed by the \(A\)- and \(B\)-path pairings.

For the first common-edge chord, its two arcs on \(L\) have lengths
\(\alpha+\beta\) and \(\gamma+\delta\).  Each chord-plus-arc circuit has
length at least ten, so
\[
 \alpha+\beta\ge9,\qquad \gamma+\delta\ge9.
\]
The two left sides sum to \(18\), hence
\[
 \alpha+\beta=\gamma+\delta=9.                       \tag{2}
\]
The other chord gives
\[
 \beta+\gamma=\delta+\alpha=9.                       \tag{3}
\]
Equations (2) and (3) imply \(\alpha=\gamma\).  Equation (1) would then
give
\[
                         2\alpha=9,
\]
which is impossible for an integral path length.

Equivalently, girth forces both common edges to be antipodal chords of
the \(18\)-circuit; two antipodal chords force the opposite
\(A\)-path lengths to agree, whereas the two \(A\)-paths must have odd
total length nine.

As a mechanical sanity check, exhaustive enumeration of all positive
integer quadruples satisfying (1) and the four chord inequalities finds
zero quadruples.  The algebra above is the certificate and does not
depend on that enumeration.

Sections 3--5 prove
\[
                         m_{ij}\le1
\]
for every \(i,j\).

## 6. Audit of the Kempe switch

Every \(A_i\) has length ten and alternates \(a,c\), so it contains five
\(c\)-edges.  The overlap result says those five edges lie on five
distinct \(B\)-circuits.  One is the diagonal circuit \(B_i\), met in
the marked edge \(s_i\); call the other four
\[
                         B_{j_1},\ldots,B_{j_4}.
\]

Switch \(a\) and \(c\) on the entire circuit \(A_i\).  This is a valid
Kempe interchange and produces another proper Tait colouring.  In the
new \(bc\)-factor:

- the five old \(c\)-edges of \(A_i\) are deleted, one from each of the
  five distinct \(B\)-circuits;
- the five old \(a\)-edges of \(A_i\), now coloured \(c\), are added.

Label the \(c\)-edges cyclically around \(A_i\) as
\(x_k y_k\), so that the intervening old \(a\)-edge is
\(y_kx_{k+1}\), with indices modulo five.  Deleting \(x_ky_k\) from its
old \(B\)-circuit leaves a \(9\)-edge path from \(x_k\) to \(y_k\).
The added edges \(y_kx_{k+1}\) therefore concatenate the five residual
paths in one cyclic order.  They cannot split into multiple circuits.
The resulting circuit has length
\[
                         5\cdot9+5=50.
\]

The residual path from \(B_i\) has lost its mark \(s_i\).  For
\(j_k\ne i\), the deleted common edge cannot be \(s_{j_k}\), because
\(s_{j_k}\) belongs to \(A_{j_k}\), not to the disjoint factor component
\(A_i\).  Thus the new \(50\)-circuit contains exactly the four marks
\[
                         s_{j_1},\ldots,s_{j_4}.
\]

Universal separation applies to every proper Tait colouring, including
this switched colouring; it does not require all marks to retain colour
\(c\).  A bichromatic circuit containing four marks is therefore a
contradiction.

This verifies the connected equality-case exclusion.

## 7. Two-component equality case

In the two-component branch, each suppressed core component has four
marks.  Its four marked \(ac\)-circuits use at least \(40\) vertices.
The two core orders sum to \(80\), so each component has order exactly
\(40\), and its four marked \(ac\)-circuits are \(C_{10}\)'s spanning
the component.  The same holds for its four marked \(bc\)-circuits.

The overlap proof is internal to one component and applies unchanged.
It would make that component's incidence graph a simple bipartite graph
on \(4+4\) factor vertices.  But every factor \(C_{10}\) contains five
\(c\)-edges, so every incidence vertex would have degree five.  A simple
bipartite graph with only four vertices on the opposite shore has
maximum degree four.  This is impossible.

Thus the two-component equality case is also excluded.

## 8. Counterexample audit and final verdict

The following possible failure modes were checked explicitly.

1. **Symmetric difference with multiple or degree-four components.**
   Multiple components are excluded whenever the total length is below
   \(20\); degree four cannot occur because a common \(A/B\) vertex
   necessarily lies on a shared \(c\)-edge.
2. **A hidden shared terminal in the off-diagonal case.**
   The terminal on \(s_k\) belongs only to the lifts of \(A_k,B_k\).
3. **A non-diagonal pairing in the \(r=2\) case.**
   The three-pairing argument forces the common edges to be the
   diagonals.
4. **A rotation or twist that splits the Kempe splice.**
   Literal endpoint tracing \(x_k\to y_k\to x_{k+1}\) shows that the
   five paths form one circuit independently of any incidence rotation
   encoding.
5. **Loss of the universal-separation hypothesis after switching.**
   Universal separation quantifies over all Tait colourings, and the
   Kempe interchange produces one of them.

No countermodel exists under the stated hypotheses.  The result soundly
excludes order \(88\) in the exact-zero size-four minimum-counterexample
branch and, together with even order, raises that branch-specific lower
bound to \(90\).

It does **not** exclude larger graphs in that branch, other flow-support
branches, or a five-cycle-double-cover counterexample in general.

## AI-use disclosure

This blind audit and its exposition were produced by an OpenAI Codex
agent under human direction.  The proof above is fully displayed for
line-by-line human checking.  The audit is not independent human peer
review.
