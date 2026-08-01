# The paired cyclic-cut condition for the connected eight-mark core

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE NECESSARY CONDITION / CONNECTED SIZE-FOUR
BRANCH / UNIVERSAL CLOSURE OPEN**.

This note records the exact low-cut information inherited by the
connected branch of the extremal size-four reduction.  It is different
from the unpaired inequality used for either four-mark component in the
two-component branch.

## 1. Expansion and pairing

Let \(H\) be a connected simple cubic graph and let \(S\) be an
eight-edge matching.  Subdivide every \(s\in S\) by a new vertex \(t_s\).
Let \(P\) be a perfect matching on the eight objects in \(S\), and for
every pair \(ss'\in P\) add the edge \(t_st_{s'}\).  Denote the resulting
cubic graph by
\[
   G=\operatorname{Exp}(H,S,P)
\]
and the four new pairing edges by \(M\).

This is exactly the connected case of the size-four marked-core
reduction: \(G-M\) is the subdivision of \(H\), the eight subdivision
vertices are \(\partial M\), and suppressing them recovers the marked
core \((H,S)\).  The four edges of \(M\) pair the eight marks; this
pairing is data that must not be discarded.

If \(H\) is Tait-colourable, every Tait colouring of \(H\) lifts to an
\(\mathbb F_2^2\)-flow on \(G\) whose exact zero set is \(M\): give both
halves of a subdivided marked edge the colour of that edge and give the
pairing edges value zero.

## 2. The exact lift formula

Fix \(X\subseteq V(H)\), and partition the marks into
\[
\begin{aligned}
 I_X&=S\cap E(H[X]),\\
 B_X&=S\cap\delta_H(X),\\
 O_X&=S\cap E(H[V(H)\setminus X]).
\end{aligned}
\]
Thus \(I_X,B_X,O_X\) are the marks internal to \(X\), crossing the core
cut, and internal to the opposite shore.

For any set
\[
   I_X\subseteq A\subseteq I_X\cup B_X,              \tag{1}
\]
let \(Y_A\subseteq V(G)\) consist of:

1. the old core vertices in \(X\); and
2. the subdivision vertex \(t_s\) precisely when \(s\in A\).

> **Paired lift formula.**
> \[
>   |\delta_G(Y_A)|
>      =|\delta_H(X)|+|\delta_P(A)|,                 \tag{2}
> \]
> where \(\delta_P(A)\) is the set of pairs in \(P\) having exactly one
> endpoint mark in \(A\).

**Proof.**  Every unmarked core edge contributes to the first cut
exactly when it contributes to the second.  A marked core edge in
\(\delta_H(X)\) contributes exactly one subdivided half, irrespective
of whether its subdivision vertex is put in \(Y_A\).  An internal
marked edge contributes neither half because (1) puts its subdivision
vertex in \(Y_A\).  An external marked edge contributes neither half
because its subdivision vertex is outside \(Y_A\).  These are exactly
the \(|\delta_H(X)|\) contributions.

The new edge \(t_st_{s'}\) crosses \(\delta_G(Y_A)\) exactly when one of
\(s,s'\) belongs to \(A\).  These are precisely the
\(|\delta_P(A)|\) remaining contributions. \(\square\)

If both \(H[X]\) and \(H[V(H)\setminus X]\) contain circuits, then both
shores of \(\delta_G(Y_A)\) contain circuits for every choice (1).
Indeed, all subdivision vertices of marks internal to either core shore
are placed on the same side as that shore, so its core circuit lifts
unchanged.

Consequently cyclic \(4\)-edge-connectivity of \(G\) implies
\[
   |\delta_H(X)|+|\delta_P(A)|\ge4                 \tag{3}
\]
for every choice (1).

## 3. Eliminating the flexible boundary marks

The minimum of the pairing term in (3) has a closed form.  Put
\[
 p_P(X)=
 \bigl|\{ss'\in P:
       s\in I_X,\ s'\in O_X\}\bigr|.                \tag{4}
\]
Thus \(p_P(X)\) counts pairs whose two marks lie **strictly internally**
on opposite core shores.  A pair incident with a boundary mark is not
counted.

> **Boundary optimization lemma.**
> \[
>  \min_{I_X\subseteq A\subseteq I_X\cup B_X}
>     |\delta_P(A)|=p_P(X).                         \tag{5}
> \]

**Proof.**  A pair with one endpoint in \(I_X\) and the other in \(O_X\)
crosses every permissible \(A\), giving the lower bound \(p_P(X)\).
Every other pair can be made noncrossing independently:

- include a boundary mate of a forced internal mark;
- exclude a boundary mate of a forced external mark;
- give two boundary mates the same membership; and
- do nothing for a pair contained in \(I_X\) or in \(O_X\).

These choices are compatible because \(P\) is a matching.  They produce
a permissible \(A\) whose crossing pairs are exactly those counted by
\(p_P(X)\). \(\square\)

Combining (3) and (5) gives the useful core condition.

> **Paired cyclic-cut lemma.**  If \(G=\operatorname{Exp}(H,S,P)\) is
> cyclically \(4\)-edge-connected and both core shores of \(X\) contain
> circuits, then
> \[
>       \boxed{|\delta_H(X)|+p_P(X)\ge4.}            \tag{6}
> \]

This is necessary, not asserted sufficient for cyclic
\(4\)-edge-connectivity of the expansion.  A cycle-separating cut of
\(G\) need not arise from a pair of cyclic core shores.

## 4. Consequences for low core cuts

Equation (6) has an exact interpretation:

- every cyclic three-edge cut of \(H\) has at least one pairing edge
  whose two marked endpoints lie strictly on opposite shores;
- every cyclic two-edge cut has at least two such pairing edges; and
- a cyclic bridge would require at least three such pairing edges.

For an unmarked cut, “strictly” is vacuous, so the number in (4) is just
the number of pairing chords crossing the induced partition of \(S\).
For a cut containing marked edges, a mark on the cut is flexible and
does not help (6); its subdivision vertex can be assigned to the more
favourable shore in the lifted cut.

Apply the standard cubic three-sum decomposition to a 3-connected core,
and suppose first that its principal cuts are unmarked.  Put the eight
marks at their factor nodes and draw in the four pairing paths in the
factor tree.  The first bullet says:

> every tree edge is covered by at least one of the four pairing paths.

In particular the decomposition tree has at most eight leaves, and
every terminal factor contains a mark paired outside that terminal
branch.  This converts the remaining connected size-four problem into a
four-demand routing problem on a tree of cyclically
\(4\)-edge-connected Tait-colourable atoms.

Marked principal cuts require the flexible-boundary version (4), not
the simpler chord count.  They remain part of the open reduction.

## 5. Relation to the extension criterion

Let \(K=G-M\) and \(T=\partial M\).  Suppressing the terminals identifies
them with the eight marked edges of \(H\).  The even-marked circuit
criterion says:

\[
\begin{split}
M\text{ extends to a standard five-cycle double cover}
\quad\Longleftrightarrow\quad
&\text{\(H\) has a binary cycle containing all eight marks}\\
&\text{and every component contains an even number of marks.}
\end{split}                                             \tag{7}
\]

Universal separation permits the eight marks to be assigned one common
Tait colour.  This already implies that some binary cycle contains all
eight marks.  Indeed, the restriction map from the binary cycle space
of \(H\) to \(S\) misses the all-one vector only if a cut contained in
\(S\) has odd size.  But a cut contained in one Tait colour class has
even size by the Parity Lemma.  The unresolved part of (7) is therefore
not mark containment; it is making every circuit component have even
marked parity.

For a minimum five-CDC counterexample in the size-four connected branch,
one has three additional facts:

1. \(S\) is universally separated;
2. the expansion has girth at least ten; and
3. \(M\) is cardinality-minimum among exact-zero matchings, so no
   matching-supported \(\mathbb F_2^2\)-flow has at most three zeros.

The paired cut lemma uses the first ambient connectivity information but
not yet the girth or minimum-support conditions.  A complete closure must
use those remaining facts, prove the four-demand atom routing in (7), or
show that failure constructs a smaller exact-zero matching.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the paired lift
formula, the boundary optimization, and the tree-path consequence.  A
separately prompted Codex agent then audited the proof and independently
recomputed the retained finite example with a clean-room checker.  This
is not human peer review.  All arguments are displayed for direct human
checking.  No finite computation is used as proof, and no claim of
resolving five-CDC is made.
