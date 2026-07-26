# Kempe transversality, the stable-triple boundary, and an order-88 bound

Date: **2026-07-26**.

Status: **human-checkable lemmas plus one independently replayed finite
counterexample**.  Nothing in this note resolves the five-cycle double
cover conjecture.

## 1. A one-switch transversality lemma

Let \(H\) be a cubic graph with a proper edge-colouring by
\(\{a,b,c\}\).  Put
\[
 F_{ac}=H[a,c].
\]
This is a spanning 2-factor.  Let \(R\) be one \(ab\)-circuit.  Switching
\(a\) and \(b\) on \(R\) is the neutral \(\mathbb F_2^2\)-switch by
\(c\), and its new \(ac\)-factor is
\[
 F'_{ac}=F_{ac}\mathbin\triangle R.                    \tag{1}
\]

Say that \(R\) is **transverse to \(F_{ac}\)** if it contains at most
one \(a\)-edge from each circuit component of \(F_{ac}\).

> **Kempe transversality lemma.**
> If \(R\) is transverse to \(F_{ac}\), then all components of
> \(F_{ac}\) met by \(R\) merge into one component of \(F'_{ac}\).

### Proof

Let the components met by \(R\) be \(C_1,\ldots,C_k\), and let
\(r_i=u_iv_i\) be the unique \(a\)-edge of \(R\cap C_i\).  Deleting
\(r_i\) turns \(C_i\) into one \(u_i\)-to-\(v_i\) path \(P_i\).
The \(b\)-edges of the alternating circuit \(R\) join the ends of these
paths in the cyclic order in which the \(a\)-edges \(r_i\) occur on
\(R\).  Consequently
\[
 \bigcup_i P_i\ \cup\ (E(R)\cap E_b)
\]
is one circuit.  It is precisely the part of
\(F_{ac}\triangle R\) supported on the components met by \(R\).
\(\square\)

Let \(S\) be a universally separated matching and use the
mark-precolouring lemma to make all marks \(c\)-coloured.  Distinct marks
then lie on distinct \(ac\)-circuits and on distinct \(bc\)-circuits.
The transversality lemma gives the following rigorous necessary
condition.

> **Kempe-stability obstruction.**
> If an \(ab\)-circuit \(R\) meets two \(ac\)-circuits containing marks,
> then \(R\) contains at least two \(a\)-edges from some \(ac\)-circuit.
> Symmetrically, if it meets two marked \(bc\)-circuits, it contains at
> least two \(b\)-edges from some \(bc\)-circuit.

Indeed, otherwise the neutral \(c\)-switch on \(R\) would put the two
unchanged \(c\)-marks on one new bichromatic circuit, contradicting
universal separation.

This is a genuine Kempe constraint, but it is not by itself a cut
theorem.  Repeated intersection is the exact escape from the elementary
merge operation.

The retained examples stress-test this distinction.  The two order-16
stable triples, the order-20 stable triple, the first order-20
cyclically-four stable pair, and the order-24 triple below all satisfy
the obstruction literally in every colouring in which the marks are
precoloured \(c\).  For example, the cyclically-four graph

```text
S??????_B?Y?QCb??X?T?Cg?SO@I?@B??
```

has the universally separated pair \((1,10),(7,19)\).  In one
all-\(c\)-mark colouring its \(ab\)-factor is Hamiltonian and its
\(ac\)-factor has lengths \(16,4\).  The Hamilton circuit uses eight
\(a\)-edges of the first \(ac\)-circuit and both \(a\)-edges of the
second.  Thus even a cyclically-four stable pair can escape through
heavy repetition; the stronger inference “a repeated intersection
forces a cyclic cut of size at most three” is not valid at the pair
level.  These are exact finite diagnostics, not ingredients of the
proof above.

## 2. The cyclic-three-cut atom conjecture is false

The package

```text
search/cyclic4-universally-separated-triple-n24-20260726/
```

contains the graph

```text
W`??A???A_@_A_cO?S_Gc`_?@O@@?@OO??_????_??H_A?E
```

with marked edges
\[
 (0,1),\qquad(2,3),\qquad(20,23).                       \tag{2}
\]
The clean-room verifier independently checks that:

1. the graph is connected, simple, and cubic of order \(24\);
2. it has \(36\) Tait colourings modulo global colour permutation;
3. the triple (2) is separated in every one of those colourings;
4. it has no cyclic edge cut of size at most three; and
5. it has the cyclic four-edge cut
   \[
    \{(2,3),(0,16),(7,17),(10,19)\}.                    \tag{3}
   \]

The two shores of (3) contain the internal marks \((0,1)\) and
\((20,23)\), respectively, while the third mark \((2,3)\) belongs to
the cut.  Thus its marked cut profile is \(1+1+1\).

This refutes the proposed statement

> every universally separated triple is exposed by a cyclic cut of
> size at most three,

even when the host is cyclically \(4\)-edge-connected.  Any proof using
canonical three-sum decomposition must therefore allow a genuine
cyclically \(4\)-edge-connected atom.

The witness evades the transversality lemma exactly through repeated
intersections.  Among the four Tait colourings modulo \(a/b\)-exchange
in which all three marks have colour \(c\), the \(ab\)-factor is always
one Hamilton circuit.  The exact bichromatic length profiles are
\[
\begin{array}{c|c|c|c}
\text{number}&ac&bc&ab\\ \hline
2&(4,4,16)&(8,8,8)&(24)\\
2&(4,4,8,8)&(4,8,12)&(24).
\end{array}                                             \tag{4}
\]
In every row the Hamilton \(ab\)-circuit meets all three marked
\(ac\)-circuits and all three marked \(bc\)-circuits, but repeats at
least one of them.  Hence the one-switch merge hypothesis is false, as
the lemma requires.

These finite facts are reproducible by literal enumeration; they are
not used to prove the transversality lemma.

The witness has girth four, marked-subdivision girth five, and fails the
strong circuit-length condition inherited from a girth-ten ambient
minimum counterexample.  It therefore does **not** refute a theorem
which genuinely uses girth at least ten.  No such stable-triple theorem
is proved here.

Nor does it refute the isolated three-mark odd-state conjecture from
`marked-three-edge-cut-signatures.md`.  Deleting each vertex not incident
with a mark and imposing the exact local marked-cut inequality leaves
18 eligible three-poles.  Direct cycle-space enumeration gives all
three odd open boundary states, with all three marks on the open
component, for every one of the 18 poles.  This is an exact finite
diagnostic, not a proof for arbitrary three-poles.

## 3. Universal precolouring improves the size-four order bound

The same mark-precolouring flexibility has a useful consequence which
does not require a stable-triple theorem.

Let \(G\) be a finite loopless cubic multigraph, let \(M\) be an
ordinary matching of \(r\) nonloop edges, and put \(K=G-M\).  Let \(T\)
be the \(2r\) distinct endpoints of \(M\).  Assume that simultaneous
suppression of the vertices of \(T\) produces loopless Tait-colourable
cubic cores \(H_j\), with one distinct marked edge \(s_t\) for every
\(t\in T\), and that the resulting marked sets \(S_j\) are matchings.
Thus
\[
 \sum_j |S_j|=2r.                                      \tag{5}
\]
Assume each \(S_j\) is universally separated in \(H_j\).

Let \(g_{\rm odd}\) be the least odd integer at least the girth of
\(G\).

> **Monochromatic-mark girth lemma.**
> Under these hypotheses, \(G\) contains \(2r\) vertex-disjoint odd
> circuits, each of length at least \(g_{\rm odd}\).  Consequently
> \[
>  |V(G)|\ge 2r\,g_{\rm odd}.                           \tag{6}
> \]

### Proof

Use the mark-precolouring lemma independently on the cores to give every
marked edge colour \(c\).  In each \(H_j[a,c]\), different marks lie on
different circuit components by universal separation.  Hence the
marked circuits over all cores are \(2r\) pairwise vertex-disjoint even
circuits, each containing exactly one mark.

Undo the suppression.  On each marked circuit, its unique marked edge
is replaced by a two-edge path through the corresponding endpoint of
\(M\).  The resulting circuit in \(G\) is therefore odd.  The restored
circuits remain vertex-disjoint because distinct suppressed marks have
distinct terminal vertices.  Every odd circuit of \(G\) has length at
least \(g_{\rm odd}\), proving (6).
\(\square\)

For the extremal size-four branch of the project,
\[
 r=4,\qquad \operatorname{girth}(G)\ge10,
\]
so \(g_{\rm odd}=11\) and
\[
 \boxed{|V(G)|\ge88}.                                  \tag{7}
\]
Equivalently, the suppressed cores contain eight vertex-disjoint even
marked circuits of length at least ten and therefore have total order
at least \(80\).

This improves the earlier bound \(68\) for the size-four extremal
branch.  It applies both when \(G-M\) is connected, giving one
eight-mark core, and when \(G-M\) has two components, giving two
four-mark cores: all core colourings lift independently because the
deleted matching edges have value zero.  The distinct-mark suppression
hypotheses are not automatic for an arbitrary matching; they are proved
for this branch in `extremal-marked-core-reduction.md`.  A clean-room
scope and convention audit is in
`audit-eight-mark-girth-bound.md`.

## 4. What remains open

The sound conclusions are:

- universal separation forbids a transverse Kempe circuit from meeting
  two marked bichromatic components;
- a repeated intersection is the precise local escape;
- cyclic \(4\)-edge-connectivity alone does not exclude a universally
  separated triple; and
- girth ten plus monochromatic mark precolouring raises the size-four
  minimum-counterexample order bound to \(88\).

The following statements remain unproved:

1. that a universally separated triple in a girth-ten cubic graph must
   be exposed by any bounded cyclic cut;
2. that the order-24 four-cut obstruction cannot be inflated while
   preserving girth ten and universal separation; and
3. that every universally separated eight-mark girth-ten core has a
   balanced selector in the signed-holonomy system of
   `eight-mark-bichromatic-code.md`.

In particular, neither the new finite counterexample nor the order bound
settles the connected eight-mark branch.

## AI-use disclosure

The lemmas, the transition analysis, and this exposition were developed
by OpenAI Codex agents under human direction.  The order-24 witness and
its verification package were also AI-generated and AI-checked; the
literal data and complete verifier are retained so that a human can
replay every finite claim without trusting an AI assertion.
