# The cyclic six-cut branch and its exact four-mark interface

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE CUT REDUCTION / AUTOMATIC CAPPING
ARGUMENT FAILS / EXACT CLOSED-STATE OBLIGATION**.

This note analyzes the \(p_P(X)=4\) branch left by
`size-four-terminal-gap-cut-reduction.md`.  The four zero matching edges
all cross the quotient shore, so each core shore contains four marks.
It is tempting to cap the two nonzero boundary edges on both shores and
apply the four-mark core theorem twice.

Universal separation does pass to both caps.  The marked cyclic-cut
inequality does not pass automatically, one cap has a forced parallel
marked/cap pair, and the cap-edge states supplied by the unrooted
four-mark theorem need not synchronize.  The exact residual condition is
an edge-avoiding, or **closed-state**, four-mark certificate on each
shore.

No finite computation is used, and no conjecture-resolution claim is
made.

## 1. The six-cut geometry

Use the connected exact-zero size-four setup.  Thus \(H\) is a connected
simple Tait-colourable cubic graph, \(S\) is a universally separated
eight-edge matching, \(P\) pairs its eight marks, and
\(G=\operatorname{Exp}(H,S,P)\) is the ambient cubic graph.  Precolour
all marks \(c\), and let \(R\) be the connected Eulerian quotient of the
lifted \(ac\)-factor after the four edges \(M\) are deleted.

Suppose the terminal-gap certificate at a marked quotient vertex \(q\)
has
\[
 \delta_R(X)=\{\ell_q,r_q\},\qquad p_P(X)=4.             \tag{1}
\]
Replace \(X\) by its complement if necessary so that \(q\in X\).
Let \(A\subseteq V(H)\) be the union of the \(ac\)-factor circuits
represented by \(X\), and put \(B=V(H)\setminus A\).

The two quotient edges in (1) are the two core \(b\)-edges
\[
 e_1=x_1y_1,\qquad e_2=x_2y_2,                          \tag{2}
\]
where \(x_1,x_2\in A\), \(y_1,y_2\in B\), and \(x_1x_2=s_q\)
is the marked \(c\)-edge flanked by \(\ell_q,r_q\).  Consequently
\[
             \delta_H(A)=\{e_1,e_2\}.                   \tag{3}
\]

Since all four edges of \(P\) cross \(X\), each pairing has one mark on
each side.  Hence
\[
             |S_A|=|S_B|=4,\qquad
 S_A=S\cap E(H[A]),\quad S_B=S\cap E(H[B]).             \tag{4}
\]
The corresponding ambient cut consists of \(e_1,e_2\) and all four
edges of \(M\), and therefore has size six.

Both \(H[A]\) and \(H[B]\) are connected.  For example, if \(R[X]\)
had two components, every component boundary in the Eulerian graph
\(R\) would have even size.  Since the total boundary of \(X\) has size
two, one component would have boundary zero or a component would have
boundary one.  The first contradicts connectedness of \(R\), and the
second contradicts Eulerian parity.  Connectivity of the quotient
shore lifts through its factor circuits to connectivity of the core
shore.  The same argument applies to the complement.

The two boundary ends on either shore are distinct.  If, for example,
\(x_1=x_2\), the third edge at that vertex would be the only connection
from the rest of \(H[A]\) to the vertex and the opposite shore, making it
a bridge.  A Tait-colourable cubic graph has no bridge.  The other shore
is identical.

## 2. The two edge caps

Define the capped cubic multigraphs
\[
\begin{aligned}
 H_A^+&=H[A]+f_A,\qquad f_A=x_1x_2,\\
 H_B^+&=H[B]+f_B,\qquad f_B=y_1y_2.                    \tag{5}
\end{aligned}
\]
Both are connected and cubic.

The cap \(f_A\) is parallel to the marked edge \(s_q=x_1x_2\).  This is
not an accidental degeneracy: it is exactly what “terminal-flanking”
means in the quotient certificate.

The opposite cap \(f_B\) is not parallel to an existing edge.  If
\(y_1y_2\) were already an edge \(d\), then
\[
 x_1s_qx_2e_2y_2dy_1e_1x_1
\]
would be a core circuit of length four.  It contains at least the mark
\(s_q\), and, because \(S\) is a matching, at most one additional mark.
Thus
\[
 |C|+|C\cap S|\le 4+2<10,
\]
contrary to the inherited marked-girth inequality.  Hence \(H_B^+\) is
simple.  The flanked cap \(H_A^+\) is genuinely a multigraph with a
parallel pair.

Every Tait colouring of \(H\) restricts to Tait colourings of the caps:
the two edges of a two-edge cut have one common colour by the Parity
Lemma, and the cap edge is given that colour.

## 3. Universal separation is inherited

> **Cap separation lemma.**  Each \(S_W\) is universally separated in
> \(H_W^+\), for \(W=A,B\), with binary two-circuits allowed in the
> parallel cap.

**Proof.**  Consider an arbitrary Tait colouring of \(H_A^+\).  Choose
any Tait colouring of \(H_B^+\), and globally permute its three colours
so that \(f_A\) and \(f_B\) have the same colour \(p\).  Delete both cap
edges and restore \(e_1,e_2\), giving both restored edges colour \(p\).
At every boundary end, the deleted cap incidence and the restored cut
incidence have the same colour.  The two cap colourings therefore glue
to a Tait colouring of \(H\).

Suppose a bichromatic circuit of \(H_A^+\) contains two marks of \(S_A\).
If it avoids \(f_A\), it is the same bichromatic circuit in the glued
colouring of \(H\), a contradiction.  If it uses \(f_A\), let its
colours be \(p,d\).  In \(H_B^+\), remove \(f_B\) from the
\(pd\)-bichromatic circuit containing it.  Removing \(f_A\) and \(f_B\)
leaves one boundary-to-boundary path on each shore; the two restored
colour-\(p\) cut edges join them into one bichromatic circuit of \(H\).
It still contains the two original marks, again contradicting universal
separation in \(H\).

The proof for \(B\) is symmetric.  A possible two-circuit
\(\{f_A,s_q\}\) contains only the single mark \(s_q\), so it creates no
exception. \(\square\)

Thus Tait colourability and universal separation survive capping.  The
remaining hypothesis of the four-mark theorem is the problematic one.

## 4. Where the marked cut inequality is lost

Fix one shore \(W\), write its boundary ends as \(w_1,w_2\), and let
\[
             L=H[W]+f,\qquad f=w_1w_2.                 \tag{6}
\]
All four pairing edges have their \(W\)-mark in \(S_W\) and their mate
strictly outside \(W\).

For \(Y\subseteq W\), put
\[
 m(Y)=|S_W\cap E(L[Y])|,\qquad
 k(Y)=|\{w_1,w_2\}\cap Y|.                             \tag{7}
\]
If \(k(Y)\le1\) and \(L[Y]\) contains a circuit, that circuit does not
use the cap edge and is already a circuit of \(H[Y]\).  Moreover,
\[
 |\delta_H(Y)|=|\delta_L(Y)|,\qquad p_P(Y)=m(Y).        \tag{8}
\]
The opposite core shore supplies a circuit on the complement side.
The paired cyclic-cut inequality in \(H\) therefore gives
\[
             |\delta_L(Y)|+m(Y)\ge4.                   \tag{9}
\]

If \(k(Y)=2\), however,
\[
             |\delta_H(Y)|=|\delta_L(Y)|+2.            \tag{10}
\]
Even when \(H[Y]\) contains a circuit, the inherited paired inequality
only gives
\[
             |\delta_L(Y)|+m(Y)\ge2,                   \tag{11}
\]
and if the only circuit of \(L[Y]\) uses the new cap edge, there need
not be a core circuit in \(H[Y]\) to which the paired inequality applies.

Therefore the four-mark cut hypothesis is inherited automatically for
all candidate shores containing at most one cap endpoint, but not for
candidate shores containing both cap endpoints.

The loss is realized literally on the flanked cap.  Take
\[
             Y=\{x_1,x_2\}\subseteq V(H_A^+).
\]
The induced graph contains the two-circuit
\(\{s_q,f_A\}\), while
\[
 |\delta_{H_A^+}(Y)|+|S_A\cap E(H_A^+[Y])|
       =2+1=3<4.                                       \tag{12}
\]
Hence \(H_A^+\) fails the hypotheses of the audited four-mark core
theorem.  That theorem also assumes simplicity, which the same cap
violates.

The opposite cap \(H_B^+\) is simple, but its marked cut inequality is
not automatic: only the possible shores containing both \(y_1,y_2\)
remain to be checked or excluded.

## 5. Removing the forced parallel pair

There is a clean way to encode the **closed** state on the flanked shore.
Let \(x_1z_1\) and \(x_2z_2\) be the third edges at \(x_1,x_2\) in
\(H_A^+\).  Delete \(x_1,x_2\) and replace the path
\[
             z_1x_1s_qx_2z_2
\]
by a new edge
\[
             g=z_1z_2.                                 \tag{13}
\]
Mark \(g\) in place of \(s_q\), retaining the other three marks.  Call
the resulting marked graph \((H_A^\circ,S_A^\circ)\).

The vertices \(z_1,z_2\) are distinct, and \(g\) is not parallel to an
existing edge.  Otherwise the original core would contain, respectively,
a marked triangle or a circuit of length four through \(s_q\), violating
\(|C|+|C\cap S|\ge10\).  The new edge is independent of the other
marks: in the all-\(c\) colouring, a marked edge incident with \(z_i\)
would lie on the same \(ac\)-circuit as \(s_q\), contradicting universal
separation.  Thus \(H_A^\circ\) is a connected simple cubic graph and
\(S_A^\circ\) is a four-edge matching.

It is Tait-colourable: in the inherited colouring, the two deleted
third edges have their common colour \(a\), so give \(g\) colour \(a\).
It is also universally separated.  To see this directly, start from an
arbitrary Tait colouring of \(H_A^\circ\).

- A bichromatic circuit containing two old marks but avoiding \(g\)
  survives when \(g\) is expanded.
- If a bichromatic circuit contains \(g\) and another mark, let the
  circuit colours be \(p,d\), with \(g\) coloured \(p\).  Expand \(g\)
  to the path in (13), give its two outside edges colour \(p\), give
  \(s_q\) colour \(d\), and give the parallel cap \(f_A\) the third
  colour.  The circuit expands to a bichromatic circuit containing
  \(s_q\) and the other mark.

In both cases the expanded cap colouring glues to a colouring of \(H\)
as in Section 3, contradicting universal separation there.

There is an exact cycle correspondence:

> \[
> \begin{split}
> &\{\text{binary cycles of \(H_A^+\) containing \(S_A\) and
> excluding \(f_A\)}\}\\
> &\qquad\longleftrightarrow
> \{\text{binary cycles of \(H_A^\circ\) containing
> \(S_A^\circ\)}\}.
> \end{split}                                           \tag{14}
> \]

Indeed, on the left, \(s_q\) is selected and \(f_A\) is not.  Even
degree at \(x_1,x_2\) forces both third edges
\(x_1z_1,x_2z_2\) to be selected.  Replace that selected three-edge
path by \(g\).  The inverse replacement is immediate.  The
correspondence preserves circuit components and replaces one mark by one
mark, so it preserves componentwise marked parity.

This removes the parallel-edge degeneracy for the closed state.  It does
not automatically prove the marked cut inequality for
\((H_A^\circ,S_A^\circ)\).  Establishing that inequality, or proving the
four-mark conclusion by another argument, remains an additional shore
obligation.

## 6. The cap-edge synchronization is forced

Call a **closed four-mark certificate** on a shore \(W\) a binary cycle
\[
             Q_W\subseteq E(H[W])                     \tag{15}
\]
which contains all four edges of \(S_W\) and whose every circuit
component contains an even number of those four marks.  Equivalently,
it is an even-marked all-four binary cycle in \(H_W^+\) which excludes
the cap edge \(f_W\).

> **Closed-state interface theorem.**  In the terminal-flanked six-cut
> geometry above, \(H\) has a binary cycle containing all eight marks
> and having even marked parity on every component if and only if both
> shores \(A\) and \(B\) have closed four-mark certificates.

### Proof

The union of two closed certificates is immediately a binary cycle in
\(H\): neither certificate uses a cut edge, all degrees are even on its
own shore, all eight marks are present, and all components are already
marked-even.

Conversely, let \(Q\) be an all-eight binary cycle in \(H\) with every
component marked-even.  Summing its degree parity over \(A\) shows that
\[
             |Q\cap\{e_1,e_2\}|\equiv0\pmod2.          \tag{16}
\]
Thus \(Q\) uses either neither or both cut edges.

Suppose it uses both.  Since \(s_q\) is a mark, \(s_q\in Q\).  At
\(x_1\), the selected edges \(e_1,s_q\) already give degree two, so the
third edge \(x_1z_1\) is absent from \(Q\).  Similarly
\(x_2z_2\notin Q\).  Therefore \(e_1,s_q,e_2\) belong to the unique
component of \(Q\) crossing the cut, while the other three marks of
\(S_A\) lie in components wholly contained in the remainder of the
\(A\)-shore.  Those remaining components contain three marks in total.
They cannot all have even marked cardinality.  This contradicts the
hypothesis on \(Q\).

Hence \(Q\) uses neither cut edge.  Its restrictions to \(A\) and \(B\)
are closed four-mark certificates. \(\square\)

This theorem is stronger than a generic “the two caps must choose the
same state” rule.  The terminal-flanked marked edge makes the open state
impossible for any globally valid cycle, so both caps are forced into
state zero.

## 7. What the four-mark theorem does and does not finish

If the simple smoothed graph \((H_A^\circ,S_A^\circ)\) satisfies the
marked cyclic-cut inequality of the four-mark core theorem, that theorem
and the correspondence (14) give a closed certificate on \(A\).

If the simple cap \((H_B^+,S_B)\) satisfies the theorem's marked
cyclic-cut inequality, the four-mark theorem gives an even-marked
all-four cycle in \(H_B^+\).  It does **not** prescribe whether that
cycle uses \(f_B\).  Only an output avoiding \(f_B\) is a closed
certificate usable in the six-cut branch.

Thus two independent applications of the existing four-mark theorem do
not prove reducibility:

1. the direct flanked cap is nonsimple and fails the marked cut
   inequality by (12);
2. after smoothing, the required marked cut inequality is a new
   obligation rather than an inherited fact;
3. on the opposite cap, possible cut-inequality failures are localized
   to shores containing both cap endpoints; and
4. even if that cap satisfies the theorem, the theorem does not force
   the cap edge to be absent.

The exact remaining interface obstruction is therefore:

> at least one of the two four-mark shores has no closed certificate.

By the closed-state interface theorem this is not merely a defect of the
capping proof; it is exactly the obstruction to an even-marked all-eight
binary cycle across this particular six-cut.

A closure of this branch could be supplied by a rooted strengthening of
the four-mark theorem which forces avoidance of a specified cap edge
under the inherited girth, paired-cut, and minimum-support hypotheses.
Alternatively, a direct four-pole argument could prove the closed state
on both shores.  Neither strengthening is proved here.

## 8. Scope

The note proves:

- the exact \(4+4\) mark split;
- Tait-colourability and universal-separation inheritance under edge
  capping;
- the precise two-incidence loss in the marked cut inequality;
- the forced parallel cap and its closed-state smoothing;
- and the exact closed-state gluing criterion.

It does not prove that either shore has a closed certificate, so it does
not eliminate the cyclic six-cut branch.  It uses neither the
cardinality-minimality of \(M\) nor a new exchange argument.  The result
does not resolve the connected size-four branch or the five-cycle double
cover conjecture.

## AI-use disclosure

This cut analysis and exposition were developed by an OpenAI Codex agent
under human direction.  Every parity, capping, smoothing, and gluing step
is displayed for direct human checking.  No computational search is used
as proof, and this is not human peer review.
