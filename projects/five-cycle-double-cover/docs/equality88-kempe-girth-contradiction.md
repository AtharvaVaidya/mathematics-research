# Girth and one Kempe switch exclude the order-\(88\) equality case

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE EQUALITY-CASE CONTRADICTION IN THE
EXTREMAL SIZE-FOUR BRANCH / FIVE-CDC STILL OPEN**.

This note closes only the equality case of the previously derived
order-\(88\) lower bound.  It does not resolve the five-cycle double
cover conjecture.  The proof uses two hypotheses inherited from the
minimum-counterexample reduction:

1. the ambient graph has girth at least ten; and
2. the marked matching in each suppressed Tait-colourable core is
   universally separated.

The key observation is that girth makes the equality-case bichromatic
incidence multigraph simple.  A single Kempe switch then puts four marks
on one bichromatic circuit, contradicting universal separation.

## 1. Equality notation

First consider the connected size-four branch.  Let \(G\) be the
ambient cubic graph, let \(M\) be the four-edge exact-zero matching, and
let \(K=G-M\).  Suppress the eight degree-two vertices of \(K\) to
obtain the connected simple cubic core \(H\), with universally separated
eight-edge marked matching
\[
                         S=\{s_0,\ldots,s_7\}.
\]
Use universal precolouring to give every mark colour \(c\), and call the
other colours \(a,b\).

At equality \(|V(G)|=88\), the monochromatic-mark girth argument gives
\[
\begin{aligned}
 H[a,c]&=A_0\sqcup\cdots\sqcup A_7,\\
 H[b,c]&=B_0\sqcup\cdots\sqcup B_7,                 \tag{1}
\end{aligned}
\]
where every \(A_i\) and \(B_j\) is a \(10\)-circuit and contains exactly
one mark.  Relabel so that
\[
                         s_i\in E(A_i)\cap E(B_i).   \tag{2}
\]
Undoing the suppression replaces the unique mark on each displayed
core circuit by a two-edge path.  It therefore lifts every \(A_i\) and
\(B_j\) to an \(11\)-circuit of \(K\), and hence of \(G\).

Let \(\Gamma\) be the bipartite incidence multigraph with vertices
\(\{A_i\}\sqcup\{B_j\}\), one edge for every \(c\)-edge of \(H\).
Thus
\[
 m_{ij}:=|E(A_i)\cap E(B_j)|
\]
is the multiplicity of \(A_iB_j\).  Every row and column of
\((m_{ij})\) sums to five.

## 2. The overlap lemma

> **Lemma 2.1 (equality-cycle overlap).**
> Under the notation above,
> \[
>                         m_{ij}\le 1                 \tag{3}
> \]
> for every \(i,j\).

### Proof

Write \(\widetilde A_i,\widetilde B_j\) for the lifted \(11\)-circuits
in \(K\).  Two core factor circuits \(A_i,B_j\) meet exactly in their
common \(c\)-edges: at an old core vertex, membership in both factors is
equivalent to membership of its incident \(c\)-edge in both.  Distinct
\(c\)-edges are vertex-disjoint.

In this particular setting the symmetric difference is \(2\)-regular.
Indeed, every common vertex of \(A_i\) and \(B_j\) is an endpoint of a
shared \(c\)-edge; cancelling that edge leaves exactly the incident
\(a\)-edge and \(b\)-edge at the vertex.  Away from the common edges,
the symmetric difference has degree two on its support.  It is therefore
a disjoint union of circuits.  If its total length is less than \(20\),
girth at least ten forces that union, when nonempty, to be one circuit.

### Diagonal case

Suppose \(i=j\) and \(m_{ii}=r\ge2\).  The two lifted circuits share the
two-edge path replacing \(s_i\), together with \(r-1\) ordinary
\(c\)-edges.  Their common paths therefore have total length \(r+1\).
Consequently
\[
 \left|E(\widetilde A_i\mathbin{\triangle}\widetilde B_i)\right|
       =11+11-2(r+1)=20-2r\le16.                     \tag{4}
\]
Girth makes the symmetric difference one circuit \(L\).  Choose one of
the common unmarked \(c\)-edges \(e\).  Its endpoints lie on \(L\), and
\(e\) together with the shorter of the two arcs between them on \(L\)
is a circuit of length at most
\[
                         1+\frac{|L|}{2}\le9.
\]
This contradicts the girth of \(G\).

### Off-diagonal case with at least three common edges

Suppose \(i\ne j\) and \(m_{ij}=r\ge3\).  The common \(c\)-edges are
unmarked, so \(\widetilde A_i\) and \(\widetilde B_j\) share exactly
\(r\) ordinary edges.  Hence
\[
 \left|E(\widetilde A_i\mathbin{\triangle}\widetilde B_j)\right|
       =22-2r\le16.                                   \tag{5}
\]
Again the symmetric difference is one circuit \(L\).  Any common edge
is a chord of \(L\), and that chord plus a shorter \(L\)-arc gives a
circuit of length at most
\[
                         1+\frac{|L|}{2}\le9,
\]
again impossible.

### Off-diagonal case with exactly two common edges

It remains to exclude \(i\ne j\) and \(m_{ij}=2\).  The symmetric
difference now has total length
\[
                              22-4=18.                \tag{6}
\]
If it had two or more circuit components, one would have length at most
nine.  It is therefore one \(18\)-circuit \(L\).

Delete the two common edges from each of
\(\widetilde A_i,\widetilde B_j\).  The remaining four paths occur
alternately around \(L\).  Denote their positive integral lengths by
\[
                         \alpha,\beta,\gamma,\delta,
\]
where the \(\alpha,\gamma\) paths come from \(\widetilde A_i\), and the
\(\beta,\delta\) paths come from \(\widetilde B_j\).

The two deleted common edges pair opposite branch vertices of this
four-path circuit.  To see this without a picture, regard the two
\(A\)-paths, the two \(B\)-paths, and the two common edges as three
perfect matchings of the four branch vertices.  The first two matchings
are distinct because their union is the one circuit \(L\).  The
common-edge matching differs from each of them because its union with
the corresponding path matching is the one original circuit
\(\widetilde A_i\) or \(\widetilde B_j\), rather than two disjoint
circuits.  These are therefore the three distinct perfect matchings on
four vertices.  Relative to the four-cycle formed by the first two, the
third matching joins opposite vertices.

Add back the first common edge.  Its two complementary arcs on \(L\)
have lengths \(\alpha+\beta\) and \(\gamma+\delta\).  Girth at least ten
and the fact that the chord has length one give
\[
       \alpha+\beta\ge9,\qquad \gamma+\delta\ge9.
\]
Their sum is \(|L|=18\), so both are equal to nine.  The other common
edge similarly gives
\[
       \beta+\gamma=9,\qquad \delta+\alpha=9.
\]
It follows that
\[
                              \alpha=\gamma.           \tag{7}
\]
But the two \(A\)-paths are what remains of the \(11\)-circuit
\(\widetilde A_i\) after deleting its two common edges.  Therefore
\[
                              \alpha+\gamma=9,         \tag{8}
\]
contradicting (7), since the left side of (8) would be even.

All cases \(m_{ij}\ge2\) are impossible, proving (3). \(\square\)

## 3. The forced Kempe surgery

Lemma 2.1 says that \(\Gamma\) is simple.  Since every \(A_i\) contains
five \(c\)-edges, it meets five distinct circuits among the \(B_j\).
One is \(B_i\), through the marked edge \(s_i\); call the other four
\[
                  B_{j_1},B_{j_2},B_{j_3},B_{j_4}.   \tag{9}
\]

Perform the Kempe interchange \(a\leftrightarrow c\) on the whole
\(ac\)-circuit \(A_i\).  This is another proper Tait colouring of \(H\).
Its new \(bc\)-factor is obtained from the old one by:

1. deleting the five \(c\)-edges of \(A_i\), one from each of the five
   distinct circuits in (9) together with \(B_i\); and
2. adding the five \(a\)-edges of \(A_i\).

Deleting one edge from a \(10\)-circuit leaves a \(9\)-edge path joining
the same two endpoints.  The five added \(a\)-edges join these five
paths in the cyclic order inherited from \(A_i\).  They therefore form
one new bichromatic circuit of length
\[
                            5\cdot9+5=50.             \tag{10}
\]
The three \(B\)-circuits not met by \(A_i\) remain unchanged.

The deleted edge on \(B_i\) is \(s_i\), so \(s_i\) changes from colour
\(c\) to colour \(a\) and is absent from the new \(bc\)-factor.  For
each \(k\in\{1,2,3,4\}\), the deleted edge on \(B_{j_k}\) is not its
mark \(s_{j_k}\): that mark is incident with \(A_{j_k}\) in \(\Gamma\),
whereas simplicity gives \(A_i\ne A_{j_k}\).  Thus all four marks
\[
                         s_{j_1},s_{j_2},s_{j_3},s_{j_4}
\]
lie on the single new \(50\)-circuit.

This contradicts universal separation, which permits at most one marked
edge on a bichromatic circuit in every proper Tait colouring.

We have proved:

> **Connected equality theorem.**
> The connected eight-mark branch of the extremal exact-zero size-four
> reduction cannot satisfy \(|V(G)|=88\).

## 4. The two-component equality case

The same argument also excludes equality when \(K=G-M\) has two
components.  Each suppressed component has four marks, hence four
vertex-disjoint marked \(ac\)-circuits of length at least ten.  The two
components together have \(80\) core vertices, so equality forces each
component to have order \(40\), and forces both its marked \(ac\)- and
marked \(bc\)-circuits to be four \(10\)-circuits spanning that
component.
Lemma 2.1 applies inside either component, so its incidence multigraph
would have to be a simple bipartite graph with four vertices on each
side.  But every incidence vertex has degree five, impossible in a
simple \(4\)-by-\(4\) bipartite graph.

Combining both branches with the existing order-\(88\) lower bound gives
the branch-specific improvement
\[
             |V(G)|\ne88,\qquad\text{hence}\qquad |V(G)|\ge90, \tag{11}
\]
because every cubic graph has even order.

This remains conditional on being in the extremal exact-zero
size-four minimum-counterexample branch.  It does not say that every
cubic graph of order below \(90\) has a five-cycle double cover, and it
does not address the surviving larger-order branch.

## 5. Human-checking checklist

The argument requires no finite search or solver:

1. equality supplies the sixteen marked core \(C_{10}\)'s;
2. their lifts are \(C_{11}\)'s in a girth-ten graph;
3. the three overlap cases in Lemma 2.1 prove that the incidence
   multigraph has no parallel edges; and
4. tracing one Kempe switch literally splices five \(9\)-edge paths with
   five edges into a \(C_{50}\) containing four marks.

The proof concerns the standard, non-orientable formulation only through
the surrounding minimum-counterexample reduction.  No orientability
claim is made.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived and audited the
incidence-overlap and Kempe-surgery argument and drafted this note.  The
complete proof is displayed for line-by-line human checking.  This is
not independent human peer review, and no resolution of the five-cycle
double cover conjecture is claimed.
