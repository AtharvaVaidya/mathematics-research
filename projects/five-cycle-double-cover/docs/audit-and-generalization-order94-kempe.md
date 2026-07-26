# Independent audit and general Kempe-incidence inequality

Date: **2026-07-26**.

Audit target: `order94-kempe-surplus-bound.md`.

Status: **INDEPENDENT CODEX-AGENT AUDIT PASSED / HUMAN-CHECKABLE
GENERALIZATION / SIZE-FOUR BRANCH ONLY / FIVE-CDC STILL OPEN**.

The proof in the target note is correct under the connected eight-mark
hypotheses stated there.  In particular:

1. the three-matching cycle-rank argument has no missing independence
   assumption;
2. the mixed \(C_{10}\)-\(C_{12}\) antipodal-chord argument is valid;
3. the surplus capacities for \(t=0,1,2,3\) are exact; and
4. the conclusion
   \[
                         |V(G)|\ge 96
   \]
   follows in the connected extremal exact-zero size-four branch.

The disconnected \(4+4\) branch is not silently included in that
calculation.  It has already been eliminated, at arbitrary order, by
the independently audited four-mark core theorem in
`four-mark-core-closure.md`.

This note first reconstructs the two delicate points without relying on
the target proof.  It then proves an arbitrary-surplus version of the
Kempe-incidence inequality and a general marked-circuit overlap bound.
Finally, it gives an explicit order-\(96\) abstract incidence matrix
which passes all the one-switch and pairwise bounds proved here.  Thus
the method really stops at \(96\) unless further rotation, girth, or
multi-switch information is added.

## 1. Conventions

Work in one suppressed Tait-colourable cubic core \(H\).  Its marked
matching is universally separated.  Choose a Tait colouring in which
all marks have colour \(c\), and denote the other colours by \(a,b\).

Let \(A\) be one marked circuit of the \(ac\)-factor.  If its core
length is \(2d\), then \(A\) contains exactly \(d\) \(c\)-edges.
Subdividing its unique marked edge lifts it to a circuit
\(\widetilde A\) of length \(2d+1\) in \(G-M\), hence in \(G\).

Among the circuits of the opposite \(bc\)-factor met by the \(d\)
\(c\)-edges of \(A\), write

- \(p\) for the number containing a marked edge; and
- \(u\) for the number containing no marked edge.

The circuit containing the mark of \(A\) is one of the \(p\) marked
circuits.

## 2. Clean reconstruction of the three-matching rank bound

Cut the \(d\) \(c\)-edges of \(A\) at their \(2d\) endpoints.  On this
labelled endpoint set define three perfect matchings:

- \(R\), pairing the ends of each removed \(c\)-edge;
- \(P\), pairing the ends of each residual path in a cut-open
  \(bc\)-factor circuit; and
- \(D\), pairing endpoints joined by an \(a\)-edge of \(A\).

Parallel pairs are retained as distinct labelled edges.  No loop is
created: every residual path and every original edge has two distinct
ends.

The graph
\[
                           X=R\cup P\cup D
\]
is a connected cubic multigraph on \(2d\) vertices and \(3d\) edges.
It is connected because \(R\cup D\) is the circuit \(A\).  Therefore
its binary cycle-space dimension is
\[
                  3d-2d+1=d+1.                       \tag{1}
\]

Let
\[
       k=c(R\cup P)=p+u,\qquad
       \ell=c(D\cup P).
\]
The \(k\) circuits of \(R\cup P\) are exactly the old affected
\(bc\)-factor circuits after residual paths are contracted.  The
\(\ell\) circuits of \(D\cup P\) are exactly the new affected
\(bc\)-factor circuits after switching \(a\leftrightarrow c\) on
\(A\).

The \(k+\ell\) circuit vectors just displayed are linearly independent.
Indeed, the span of the \(R\cup P\) circuit vectors is supported on
\(R\cup P\), while the span of the \(D\cup P\) circuit vectors is
supported on \(D\cup P\).  A vector in their intersection would
therefore be supported on \(P\).  But \(P\) is a matching and contains
no nonzero binary cycle.  Hence the two spans meet trivially, and
\[
                         k+\ell\le d+1.               \tag{2}
\]

This is equivalent to the target note's presentation with the
additional circuit \(R\cup D\): the \(1+k+\ell\) bicoloured circuit
vectors have precisely the one relation in which all their
coefficients are \(1\).

## 3. Arbitrary-surplus marked/unmarked inequality

When the switch is performed, the mark on \(A\) changes from \(c\) to
\(a\) and leaves the new \(bc\)-factor.  Every other marked old
\(bc\)-circuit met by \(A\) retains its mark.  There are \(p-1\) such
marks.  Universal separation in the switched colouring forces them
onto distinct new \(bc\)-circuits, so
\[
                           \ell\ge p-1.                \tag{3}
\]
Combining (2) and (3) gives the general inequality
\[
                  \boxed{\,2p+u\le d+2\,}.            \tag{4}
\]

> **General Kempe-incidence inequality.**
> A marked \(ac\)-factor circuit containing \(d\) \(c\)-edges cannot
> meet \(p\) marked and \(u\) unmarked circuits of the opposite
> \(bc\)-factor unless (4) holds.

The statement is symmetric in the two bichromatic factors.

For a marked core \(C_{10}\), \(d=5\).  If the opposite factor has no
unmarked circuit, then \(u=0\) and (4) gives
\[
                            p\le3,                    \tag{5}
\]
which is exactly the short-factor support lemma used in the target
proof.  The lemma does not require the opposite circuits to be short,
but (5) does require all the opposite circuits met by \(A\) to be
marked.  In the target's range \(t<5\), every opposite factor circuit
is marked, so this condition is satisfied.

When unmarked circuits exist, their coefficient in (4) is only one.
This identifies the precise later-order escape:
\[
                       2p+u\le7                       \tag{6}
\]
permits a short marked circuit to meet more than three opposite
circuits if some are unmarked.

### 3.1 Simultaneous switches

There is also an exact multi-switch form.  Let \(\mathcal A\) be a
nonempty set of \(r\) marked \(ac\)-factor circuits and switch all of
them.  Put
\[
 d_{\mathcal A}=\sum_{A\in\mathcal A}|E_c(A)|.
\]
Let \(p\) and \(u\) count the marked and unmarked opposite-factor
circuits met by their union.  Finally, let \(h\) be the number of
components of the bipartite incidence graph induced by
\(\mathcal A\) and the opposite circuits it meets.

The three-matching graph now has \(2d_{\mathcal A}\) vertices,
\(3d_{\mathcal A}\) edges, and \(h\) components.  Its cycle-space
dimension is \(d_{\mathcal A}+h\).  The old and new opposite-factor
circuit spaces still meet trivially inside the residual-path matching,
so
\[
                  (p+u)+\ell\le d_{\mathcal A}+h.     \tag{MS1}
\]
Exactly \(r\) distinct marked opposite circuits lose their marks,
namely the circuits containing the marks of the switched members of
\(\mathcal A\).  The other \(p-r\) affected marks must remain
separated, giving \(\ell\ge p-r\).  Therefore
\[
             \boxed{\,2p+u\le d_{\mathcal A}+h+r\,}.  \tag{MS2}
\]
Since \(h\le r\), this implies the weaker
\[
                         2p+u\le d_{\mathcal A}+2r.
\]
For \(r=1\), (MS2) is exactly (4).

## 4. General marked-marked overlap bound

The local girth argument also generalizes.

Let \(A_i\) and \(B_j\) be marked circuits of the \(ac\)- and
\(bc\)-factors with core lengths
\[
                   10+2x,\qquad10+2y,
 \qquad x,y\ge0.                                     \tag{7}
\]
Their lifts have lengths \(11+2x\) and \(11+2y\).  Put
\[
                   m=|E(A_i)\cap E(B_j)|,             \tag{8}
\]
where the intersection consists of common \(c\)-edges.

> **Marked overlap bound.**
> If \(G\) has girth at least ten, then
> \[
                         \boxed{\,m\le x+y+1\,}.       \tag{9}
> \]

### 4.1 Diagonal case

If \(i=j\), the common marked edge lifts to a common two-edge path.
The other \(m-1\) common edges remain ordinary edges.  The lifted
symmetric difference has size
\[
 (11+2x)+(11+2y)-2(m+1)
       =20+2(x+y-m).                                  \tag{10}
\]
If \(m\ge x+y+2\), this size is at most \(16\).  The symmetric
difference is nonempty and \(2\)-regular in the specific
\(ac\)-versus-\(bc\) setting.  Girth at least ten makes it one circuit.
There is an ordinary common edge because \(m\ge2\); it is a chord of
that circuit.  The chord and a shorter circuit arc have total length
at most nine, a contradiction.

### 4.2 Off-diagonal case below length \(18\)

If \(i\ne j\), every common edge is ordinary and the symmetric
difference has size
\[
                 22+2(x+y-m).                         \tag{11}
\]
For \(m\ge x+y+3\), this is at most \(16\), and the same one-circuit
plus chord argument is a contradiction.

### 4.3 The exact length-\(18\) boundary

It remains to exclude
\[
                         m=x+y+2.                     \tag{12}
\]
Now the symmetric difference is one \(C_{18}\), say \(L\).  Every
common edge is a chord.  Girth forces each of its two \(L\)-arcs to
have length at least nine, so each common edge joins antipodal vertices
of \(L\).

The \(2m\) chord endpoints split \(L\) into positive-length arcs which
alternate between \(A_i\)-only and \(B_j\)-only paths.  Half-turn on
the metric \(C_{18}\) shifts the cyclic endpoint order by \(m\)
positions and preserves each intervening arc length.

If \(m\) is odd, this shift exchanges the \(A\)-arcs and \(B\)-arcs.
Their total lengths must both be nine.  But their actual totals are
\[
 (11+2x)-m=9+x-y,\qquad
 (11+2y)-m=9+y-x.                                    \tag{13}
\]
Equality would give \(x=y\), which would make
\(m=2x+2\) even, a contradiction.

If \(m\) is even, the half-turn preserves the two arc types.  It pairs
the arcs of either type without a fixed arc, so each total in (13)
must be even.  Yet (12) and even \(m\) imply that \(x+y\), hence
\(x-y\), is even, making both numbers in (13) odd.  This is again a
contradiction.

Thus (12) is impossible, completing the proof of (9).

The target note needs only the cases
\[
\begin{array}{c|c|c}
(x,y)&\text{factor lengths}&\text{bound}\\ \hline
(0,0)&C_{10}\text{ versus }C_{10}&m\le1,\\
(0,1)&C_{10}\text{ versus }C_{12}&m\le2.
\end{array}
\]
The second row is exactly its mixed-overlap lemma.

## 5. Marked-unmarked overlap bound

There is a parallel bound useful once unmarked factor circuits appear.
Let the marked circuit have core length \(10+2x\), and let an
unmarked opposite-factor circuit have length \(10+2z\).  The latter is
unchanged when the marks are unsuppressed.  Their lifted symmetric
difference has odd size
\[
                         21+2(x+z-m).                 \tag{14}
\]
If \(m\ge x+z+2\), this size is at most \(17\).  It cannot have two
circuit components, since girth ten would require total length at
least twenty.  Hence it is one circuit.  Any common edge is a chord,
and the chord with a shorter arc has length at most
\[
                         1+\left\lfloor17/2\right\rfloor=9,
\]
impossible.  Therefore
\[
                         \boxed{\,m\le x+z+1\,}.       \tag{15}
\]

In particular, a marked \(C_{10}\) and an unmarked \(C_{10}\) meet in
at most one \(c\)-edge.

## 6. Audit of the low-surplus arithmetic

Write
\[
                         |V(G)|=88+2t.
\]
Then \(|V(H)|=80+2t\).  For \(t<5\), eight marked circuits of either
factor consume at least 80 vertices and leave fewer than ten, so no
unmarked factor circuit exists.  Writing the marked circuit lengths as
\[
                         10+2h_0,\ldots,10+2h_7
\]
gives \(\sum h_i=t\).

In the opposite factor, let \(r\) be the number of long marked
circuits.  Their total \(c\)-edge incidence capacity is exactly
\[
                             5r+t.                    \tag{16}
\]
Since \(r\le t\), it is at most \(6t\).

There are at least \(8-t\) short circuits in the first factor.  By
(5), each has support at most three.  By the \((0,0)\) case of (9),
each short opposite circuit contributes at most one of its five
incidences.  Thus every short row sends at least three incidences to
long opposite circuits.

- For \(t=0\), there is no long capacity.
- For \(t=1\), demand is at least \(3\cdot7=21\), while capacity is at
  most \(6\).
- For \(t=2\), demand is at least \(3\cdot6=18\), while capacity is at
  most \(12\).
- For \(t=3\), demand is at least \(15\).  One or two long circuits
  have capacity at most \(8\) or \(13\), so the only numerical escape
  is three \(C_{12}\)'s of total capacity \(18\).  In that case (9)
  bounds every short-to-long entry by two.  Support at most three then
  forces every short row to send at least four incidences to the long
  columns.  The at least five short rows demand \(20>18\).

This independently reproduces every numerical contradiction in the
target proof.

## 7. Why the same local method stops at order \(96\)

At \(t=4\), no unmarked factor circuit exists, but the following
nonnegative integral incidence matrix survives all the pairwise bounds
(9), all row and column degree equations, the diagonal mark condition,
and every single-circuit specialization of (4):
\[
M=\begin{pmatrix}
1&3&0&3&0&0&0&0\\
3&1&0&0&0&0&0&3\\
0&0&2&0&0&0&2&1\\
0&0&2&1&0&2&0&0\\
0&1&2&0&2&0&0&0\\
0&0&0&1&2&2&0&0\\
1&0&0&0&0&2&2&0\\
0&0&0&0&2&0&2&1
\end{pmatrix}.                                      \tag{17}
\]
Use the excess profiles
\[
\begin{aligned}
 x&=(2,2,0,0,0,0,0,0),\\
 y&=(0,0,1,0,1,1,1,0).
\end{aligned}                                       \tag{18}
\]
Thus the \(A\)-factor has two \(C_{14}\)'s and six \(C_{10}\)'s,
while the \(B\)-factor has four \(C_{12}\)'s and four \(C_{10}\)'s.

The row sums of (17) are
\[
                         7,7,5,5,5,5,5,5,
\]
and its column sums are
\[
                         5,5,6,5,6,6,6,5,
\]
as required by (18).  Every diagonal entry is positive.  Entrywise,
\[
                         M_{ij}\le1+x_i+y_j,
\]
which is (9).  Each support has size three.  For a row or column of
half-length \(d\), (4) with no unmarked opposite circuit permits at
most \(\lfloor(d+2)/2\rfloor\) marked neighbours; this is three for
\(d=5\), four for \(d=6\), and four for \(d=7\).  Hence all supports
in (17) are allowed.

Matrix (17) is only an **abstract necessary-condition skeleton**.  It
does not assert that compatible cyclic orders and twist choices realize
a simple cubic core of ambient girth ten, much less a universally
separated marked core or a five-CDC counterexample.  Its role is to
certify the exact limit of the present local counting method: order
\(96\) requires genuinely new information.

The matrix also passes the simultaneous-switch inequality (MS2) for
every nonempty subset on either shore.  This last finite diagnostic is
not needed for any theorem above.  The transparent 255-subset checker
is
`scratch/verify_order96_kempe_incidence_frontier.py`; it also rechecks
all row sums, column sums, diagonal entries, pairwise bounds, and
single-switch support bounds.

## 8. Later surplus and unmarked circuits

For a general factor, write its eight marked circuit lengths as
\(10+2x_i\), and its unmarked circuit lengths as \(10+2z_j\).  The
factor-size equation is
\[
             \sum_i x_i+\sum_j(5+z_j)=t.             \tag{19}
\]
Thus unmarked circuits first become possible at \(t=5\), or ambient
order \(98\).

At that first value, an unmarked circuit cannot actually occur in
either factor under the present hypotheses.  If, for example, the
\(B\)-factor had an unmarked circuit, (19) would force exactly one
unmarked \(C_{10}\) and eight marked \(C_{10}\)'s.  The other factor
has at least three marked \(C_{10}\)'s, because its total surplus is
only five.  Fix one of them.  By (9) and (15), each opposite circuit
contributes at most one incidence, so its five \(c\)-edges meet five
distinct opposite circuits.  If it misses the unmarked circuit, then
\((p,u)=(5,0)\); if it meets it, then
\((p,u)=(4,1)\).  Both violate (6).  This contradiction proves:

> **Order-\(98\) unmarked-factor exclusion.**
> At \(t=5\), both bichromatic factors consist only of their eight
> marked circuits.

This does not exclude order \(98\): all-marked length profiles already
admit abstract incidence matrices satisfying (4) and (9).  For larger
surplus, (4), (9), (15), and the exact budget (19) remain necessary,
but unmarked circuits provide a genuine additional escape.  No
arbitrary-order contradiction follows from these inequalities alone.

## 9. Verdict and scope

The audited theorem is:

> In the connected eight-mark extremal exact-zero size-four
> minimum-counterexample branch, the ambient cubic graph has order at
> least \(96\).

The arbitrary-order additions proved here are:

1. the general Kempe-incidence inequality \(2p+u\le d+2\);
2. the marked-marked overlap bound \(m\le x+y+1\);
3. the marked-unmarked overlap bound \(m\le x+z+1\); and
4. the exclusion of unmarked factor circuits at ambient order \(98\).

The explicit order-\(96\) skeleton shows why these facts do not resolve
the connected eight-mark branch.  They do not settle the five-cycle
double cover conjecture and make no orientable claim.

## AI-use disclosure

An OpenAI Codex agent, independently of the agent that drafted the
target proof, reconstructed and audited its arguments, derived the
arbitrary-surplus generalizations, and wrote this note under human
direction.  All proofs and the order-\(96\) matrix are displayed for
line-by-line human checking.  This is not independent human peer review.
