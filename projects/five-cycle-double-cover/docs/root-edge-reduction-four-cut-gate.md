# Root avoidance by reducing the forbidden edge

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE ROOTED CLOSURE FOR THE CYCLICALLY
5-EDGE-CONNECTED CASE / EXACT INDEPENDENT FOUR-CUT GATE IN THE
CYCLICALLY 4-EDGE-CONNECTED CASE / GENERAL ROOTED THEOREM STILL OPEN**.

This note proves a prescribed-and-forbidden circuit lemma that is useful
at the cyclically \(4\)-edge-connected factor in the four-mark
decomposition.  Reducing the forbidden edge turns a circuit avoiding
that edge into an ordinary prescribed-edge circuit problem.  Separation
of the four common-colour marks is exactly what keeps their images
independent after the reduction.

The four-edge circuit theorem of Aldred, Ellingham, Hemminger, and
Holton then gives the desired circuit unless the reduced graph has a
cyclic cut of size at most three.  Pulling such a cut back proves that
the forbidden edge belongs to an independent cyclic four-edge cut.
Consequently the rooted assertion is automatic in the cyclically
\(5\)-edge-connected case.

The result is a genuine rooted closure theorem, but only for this
connectivity class.  A cyclically \(4\)-edge-connected graph may have
the displayed four-cut, so the note does not prove the unrestricted
rooted assertion or the Five-Cycle Double Cover Conjecture.

## 1. Setup and edge reduction

Let \(H\) be a finite simple cyclically \(4\)-edge-connected cubic
graph, let
\[
                         S=\{s_1,s_2,s_3,s_4\}
\]
be a four-edge matching, and let \(f=uv\notin S\).  Fix a Tait
colouring in which every member of \(S\) has colour \(c\), the root
\(f\) has colour \(a\ne c\), and \(S\) is separated: no bichromatic
factor circuit contains two members of \(S\).  Universal separation
implies this last fixed-colouring condition, but is stronger than what
is used below.

Write
\[
 N_H(u)-\{v\}=\{u_1,u_2\},\qquad
 N_H(v)-\{u\}=\{v_1,v_2\}.
\]
The **root-edge reduction**
\[
 R=H\mathbin{\ominus}f
\]
is obtained by deleting \(u,v\) and adjoining the two new edges
\[
                  \bar u=u_1u_2,\qquad
                  \bar v=v_1v_2.                       \tag{1}
 \]

There is no triangle in \(H\).  Indeed, \(S\) has four independent
edges, so \(|V(H)|\ge8\).  A triangle in a cubic graph of this order
has a three-edge boundary and the complementary shore contains a
circuit by the cubic degree count, contradicting cyclic
\(4\)-edge-connectivity.  It follows that the four vertices in (1)
are pairwise distinct whenever equality would create a triangle, that
\(u_1u_2,v_1v_2\notin E(H)\), and that the two new edge objects are
distinct.  Thus \(R\) is a simple cubic graph.  It is connected because
a cyclically \(4\)-edge-connected simple cubic graph of this order is
3-connected, and deleting the adjacent pair \(u,v\) leaves it
connected.

Map every edge \(s\in S\) to an edge \(\bar s\in E(R)\) by
\[
 \bar s=
 \begin{cases}
   \bar u,&s\text{ is incident with }u,\\
   \bar v,&s\text{ is incident with }v,\\
   s,&\text{otherwise}.
 \end{cases}                                           \tag{2}
\]
The matching property makes (2) unambiguous.

## 2. Separation keeps the reduced marks independent

> **Reduced-mark lemma.**  The four edges
> \[
>                         \bar S=\{\bar s:s\in S\}
> \]
> are distinct and form a matching in \(R\).

### Proof

The new edges in (1) are new edge objects, are distinct, and are not
old edges of \(H\), so (2) is injective.

Two unchanged images cannot be adjacent because \(S\) is a matching.
The two new images cannot be adjacent because that would give a common
neighbour of \(u\) and \(v\), hence a triangle through \(f\).

It remains to compare one new image with one unchanged image.  Suppose,
without loss of generality, that \(s=uu_1\in S\), so
\(\bar s=\bar u\).  At \(u\), the remaining nonroot edge \(uu_2\) has
the third colour \(b\).  If an unchanged marked edge
\(t\in S\) were incident with \(u_2\), then \(t\) has colour \(c\), and
the \(bc\)-factor circuit contains the consecutive marked edges
\[
                         s,\ uu_2,\ t .
\]
This contradicts separation.  An unchanged mark incident with \(u_1\)
would already be adjacent to \(s\) in \(H\), contradicting that \(S\)
is a matching.  The other choices at \(u\), and the two choices at
\(v\), are symmetric.  Hence \(\bar S\) is a matching. \(\square\)

## 3. A reducible root is avoidable

Aldred, Ellingham, Hemminger, and Holton prove that four independent
edges in a quasi \(4\)-connected graph lie on one cycle.  They also
record that a cyclically \(4\)-edge-connected cubic graph is quasi
\(4\)-connected:

R. E. L. Aldred, M. N. Ellingham, R. L. Hemminger, and D. A.
Holton, “Cycles in quasi 4-connected graphs,” *Australasian Journal of
Combinatorics* **15** (1997), 37--46,
<https://ajc.maths.uq.edu.au/pdf/15/ocr-ajc-v15-p37.pdf>.

> **Reducible-root lemma.**  If \(R=H\mathbin{\ominus}f\) is cyclically
> \(4\)-edge-connected, then \(H\) has a circuit which contains all four
> members of \(S\) and avoids \(f\).

### Proof

By the reduced-mark lemma, \(\bar S\) is a set of four independent
edges of \(R\).  The cited theorem supplies a cycle \(\bar C\) of \(R\)
through \(\bar S\).

Whenever \(\bar C\) uses \(\bar u\), replace that edge by the path
\[
                           u_1u u_2,
\]
and make the analogous replacement for \(\bar v\).  The two replacement
paths are internally disjoint, so the result is one circuit \(C\) in
\(H-f\).  If a mark \(s\) was incident with \(u\) or \(v\), its image
in (2) belongs to \(\bar C\), and the corresponding replacement path
contains \(s\).  Every unchanged mark also remains on the circuit.
Thus \(S\subseteq E(C)\) and \(f\notin E(C)\). \(\square\)

The circuit \(C\) is itself a closed rooted certificate: its unique
component contains four marks.

## 4. Exact pullback of a failed reduction

The preceding lemma has a sharp converse obstruction which does not
require the general edge-reduction theory.

> **Independent four-cut gate.**  If no circuit of \(H-f\) contains
> all four members of \(S\), then \(f\) belongs to an independent
> cyclic four-edge cut of \(H\).  More precisely,
> \(R=H\mathbin{\ominus}f\) has a cyclic three-edge cut
> \(\delta_R(X)\) such that
> \[
>                    \delta_H(X^\uparrow)
>                    =\delta_R(X)\mathbin{\dot\cup}\{f\}       \tag{3}
> \]
> for a shore \(X^\uparrow\) obtained by restoring exactly one of
> \(u,v\).

### Proof

By the reducible-root lemma, \(R\) is not cyclically
\(4\)-edge-connected.  Hence it has a cyclic cut
\(\delta_R(X)\) of size \(k\le3\).

Consider the positions of \(u_1,u_2\) in the two shores.  If they lie
on opposite shores, the new edge \(\bar u\) belongs to the cut.
Restoring \(u\) on either shore replaces \(\bar u\) by exactly one
crossing edge and does not change the cut size.  If \(u_1,u_2\) lie on
one shore, restoring \(u\) on that shore creates no crossing edge at
\(u\).  The same statements hold for \(v\).

Unless both neighbour pairs are unsplit and lie on opposite shores, we
may choose the shores of the restored vertices \(u,v\) to be the same.
Then \(f\) is internal, the pulled-back cut of \(H\) still has size
\(k\le3\), and both shores remain cyclic.  To see the last assertion,
an internal new edge used by a shore circuit is replaced by its
two-edge path through the restored vertex, while a crossing new edge
was not available to an internal shore circuit.  This contradicts
cyclic \(4\)-edge-connectivity of \(H\).

Therefore \(u_1,u_2\) lie together on one shore and \(v_1,v_2\) lie
together on the other.  Restoring \(u,v\) on their forced shores makes
\(f\) the only additional cut edge, proving (3).  Both shores are
still cyclic, so cyclic \(4\)-edge-connectivity gives
\[
                              k+1\ge4.
\]
Since \(k\le3\), equality holds and \(k=3\).

Finally, the three members of the cyclic three-cut
\(\delta_R(X)\) are independent.  If two shared an endpoint \(w\) on
one shore, then \(w\) would have only one edge internal to that shore,
so no shore circuit could use \(w\).  Moving \(w\) to the opposite
shore would replace two crossing edges by its one formerly internal
edge, producing a cyclic cut of size two.  The pullback argument in
the preceding paragraphs already excludes every cyclic cut of size at
most two in \(R\), since it would give a cyclic cut of size at most
three in \(H\).
The three cut edges also avoid \(u,v\), which are absent from \(R\).
Together with \(f\), they therefore form an independent four-edge
cut. \(\square\)

## 5. Rooted cyclically five-edge-connected closure

> **Rooted four-mark circuit theorem at cyclic connectivity five.**
> Let \(H,S,f\) satisfy the setup of Section 1, and assume in addition
> that \(H\) is cyclically \(5\)-edge-connected.  Then \(H-f\) has a
> circuit containing all four marks.

### Proof

Otherwise the independent four-cut gate gives a cyclic four-edge cut
of \(H\), contrary to cyclic \(5\)-edge-connectivity. \(\square\)

Thus the standard rooted four-mark assertion is proved in this
connectivity class, with the stronger conclusion of one all-four
circuit.

For a merely cyclically \(4\)-edge-connected factor, the exact remaining
case is now local: the forbidden root lies in an independent cyclic
four-cut.  Deleting the root turns the other three members into the
three-edge interface between the two resulting shores.  This is the
root-containing cyclic-four-cut branch treated algebraically in
`four-pole-exception-rooted-packing-algebra.md`; it is distinct from the
separate \(2+1+1\) marked-borrower two-pole.  The reduction shows that a
diffuse prescribed-cycle failure cannot survive outside this explicit
four-cut interface.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the forbidden-edge
reduction, observed that fixed-colouring separation preserves
independence of the reduced marks, proved the cut pullback, and wrote
this note.  The proof is displayed in full for line-by-line human
checking.  The only imported step is the cited four-independent-edge
cycle theorem.  No finite computation is used, and no unrestricted
Five-Cycle Double Cover result is claimed.
