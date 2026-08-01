# Odd-side forests in a Jaeger star fibre

Date: 2026-07-28

Status: **HUMAN ALGEBRAIC IDENTITIES / EXACT PETERSEN OBSTRUCTION TO
DISJOINTNESS / NOT A PROOF OF THE PARITY-SELECTION LEMMA**.

## 1. The odd-side forest is the zero set

Let \(G\) be a cubic graph of even order, let \(T\) be a spanning tree,
and define
\[
 K(T)=\{e\in T:\text{a component of }T-e\text{ has odd order}\}.
\]
Both components have the same parity, so this is well defined.

Let \(F(T)\) be the fundamental completion: the xor of the fundamental
circuits of all edges outside \(T\).  If \(e\in T\), and \(X\) is one
side of \(T-e\), then
\[
 e\in F(T)
 \quad\Longleftrightarrow\quad
 |\delta_G(X)-\{e\}|\text{ is odd}.
\]
Since \(G\) is cubic,
\[
 |\delta_G(X)|\equiv 3|X|\equiv |X|\pmod2.
\]
It follows that \(e\in F(T)\) exactly when \(|X|\) is even.  Every
cotree edge belongs to \(F(T)\), and therefore
\[
                         F(T)=E(G)-K(T).                       \tag{1}
\]

In particular, \(K(T)\) is a forest and every vertex has odd degree in
\(K(T)\): the complement of an Eulerian subgraph in a cubic graph has
odd degree at every vertex.  Equivalently,
\[
                         \partial K(T)=V(G).                   \tag{2}
\]
Thus every component of \(K(T)\) has even order.

There is also a rooted description.  Root \(T\) arbitrarily.  A
nonroot edge belongs to \(K(T)\) exactly when the subtree below it has
odd order.  The usual leaf recursion then gives (2) directly.

## 2. The star-fibre parity target

Take a vertex-star multiplicity fibre and number the three incident
edges so that the \(i\)-th spoke belongs only to \(T_i\).  Put
\[
 K_i=K(T_i),\qquad F_i=E(G)-K_i,
\]
and let \(\phi=(1_{F_1},1_{F_2},1_{F_3})\).  Empty common intersection
of the three trees implies
\[
                         K_1\cap K_2\cap K_3=\varnothing.       \tag{3}
\]
Consequently the pure third-coordinate value class is exactly
\[
 \{e:\phi(e)=001\}=K_1\cap K_2.                               \tag{4}
\]

For the coordinate plane \(\ker(x_3)\), the five-point
component-parity criterion therefore says precisely:
\[
 |\delta_G(Q)\cap K_1\cap K_2|\equiv0\pmod2
 \quad\text{for every component }Q\text{ of }K_3.             \tag{5}
\]
Equivalently, \(K_1\cap K_2\) is Eulerian after every component of
\(K_3\) is contracted.

This flow-level criterion is independently Theorem 3.16 of Radek
Hušek and Robert Šámal, *Exponentially Many Circuit Double Covers*,
[arXiv:2607.24724](https://arxiv.org/abs/2607.24724); their Conjecture
3.19 asks for the required flow.  The new obligation studied here is
therefore the special Jaeger star/tree selection and its exchange
landscape, not priority for the component-parity characterization.

Some parity is automatic but not enough.  By (2), for every component
\(Q\) of \(K_3\),
\[
 |\delta_G(Q)\cap K_1|
 \equiv|\delta_G(Q)\cap K_2|
 \equiv |Q|\equiv0\pmod2.                                    \tag{6}
\]
The parity of the intersection of those two even sets is not
determined.  If
\[
 \omega_3(Q)=|\delta_G(Q)\cap K_1\cap K_2|\pmod2,
\]
then
\[
                  \bigoplus_Q\omega_3(Q)=0,                   \tag{7}
\]
because every edge between distinct contracted components is counted
at both ends.  Thus the failing components always occur in pairs.
The missing theorem must eliminate these paired local defects; their
global parity already vanishes.

## 3. Exact exchange law

Make a tree exchange
\[
 T'=T-a+b,\qquad a\in C_T(b),
\]
where \(C_T(b)\) is the fundamental circuit of \(b\).  The fundamental
completion exchange identity and (1) give
\[
 K(T')=
 \begin{cases}
 K(T),&a\notin K(T),\\
 K(T)\mathbin\triangle C_T(b),&a\in K(T).
 \end{cases}                                                   \tag{8}
\]
Thus an exchange removing an edge outside the odd-side forest is
completion-neutral.  An active exchange toggles one whole fundamental
circuit.  Since a circuit is Eulerian, (8) also directly preserves the
boundary identity (2).

Suppose \(K_3\) is fixed and exchanges in the first two trees give
\[
 K_1'=K_1\triangle\alpha C_1,\qquad
 K_2'=K_2\triangle\beta C_2,
\]
where \(\alpha,\beta\in\{0,1\}\) record whether the corresponding
removed edge lies in its old \(K\)-forest.  For edge-indicator
functions over \(\mathbb F_2\),
\[
\begin{split}
 1_{K_1'\cap K_2'}
  ={}&1_{K_1\cap K_2}
   +\alpha\,1_{C_1\cap K_2}
   +\beta\,1_{C_2\cap K_1}\\
   &+\alpha\beta\,1_{C_1\cap C_2}.                             \tag{9}
\end{split}
\]
Taking boundaries after contracting \(K_3\) gives the exact update of
the defect vector \(\omega_3\).  Formula (9) exposes the difficulty:
the target is bilinear in the two odd-side forests, so ordinary linear
boundary invariance does not force (5).

### A coordinate-free form of every Fano defect bit

Let \(W=\mathbb F_2^3\), let
\(\phi:E(G)\to W-\{0\}\) be the flow of the packing, and for
\(0\ne h\in W^*\) put
\[
                         E_h=\{e:h(\phi(e))=0\}.
\]
Choose any \(w\in W\) with \(h(w)=1\).  For a component \(Q\) of
\(E_h\), its component-parity defect bit is
\[
 \beta_h(Q)=|\delta(Q)\cap\phi^{-1}(w)|\pmod2.                \tag{10}
\]
This does not depend on the chosen \(w\).  Indeed, flow conservation
summed over \(Q\) says that the xor of the values on \(\delta(Q)\) is
zero.  All those values lie in the four-point affine plane \(h=1\).
The \(3\times4\) matrix formed by those four columns has one-dimensional
kernel, spanned by \((1,1,1,1)\).  Hence the four colour-class parities
on \(\delta(Q)\) are equal.

Equivalently, choose \(g,\ell\in W^*\) so that
\((g,\ell,h)\) is a basis of \(W^*\).  The common zero set
\(E_g\cap E_\ell\) is exactly one of the four colour classes in \(h=1\),
so
\[
                  \beta_h=\partial_h(E_g\cap E_\ell),        \tag{11}
\]
where \(\partial_h\) is boundary after contracting every \(E_h\)
component.  In particular \(d_h=|\operatorname{supp}\beta_h|\) is
always even, by the handshake lemma in the quotient multigraph.

### The exact all-seven topology law

For the reciprocal exchange below, define
\[
 Z_i=\begin{cases}C_i,&b\in K_i,\\\varnothing,&b\notin K_i,\end{cases}
 \qquad
 Z_j=\begin{cases}C_j,&a\in K_j,\\\varnothing,&a\notin K_j.\end{cases}
\]
Then (8) and \(F_s=E-K_s\) give the exact flow update
\[
                 \phi'=\phi+e_i1_{Z_i}+e_j1_{Z_j}.           \tag{12}
\]
For every \(0\ne f\in W^*\), put
\[
                  Z_f=f(e_i)Z_i\triangle f(e_j)Z_j.
\]
It follows edge by edge that
\[
                              E_f'=E_f\triangle Z_f.         \tag{13}
\]
Equations (10), (11), and (13) are a complete coordinate-free update
rule: choose \(g,\ell\) completing \(h\), take the components of
\(E_h\triangle Z_h\), and on each new component take the boundary
parity of
\[
                  (E_g\triangle Z_g)\cap(E_\ell\triangle Z_\ell).
                                                                    \tag{14}
\]
If \(Z_h=\varnothing\), the old and new quotient vertices are the same.
Expanding (14) over \(\mathbb F_2\) gives
\[
 R=(Z_g\cap E_\ell)\triangle(E_g\cap Z_\ell)
                         \triangle(Z_g\cap Z_\ell)
\]
and therefore
\[
                         \beta_h'=\beta_h+\partial_hR.        \tag{15}
\]
If \(Z_h\ne\varnothing\), (13)--(14) remain exact, but the component
partition itself changes; one cannot compare defect vectors by a fixed
quotient boundary.

When both exchange circuits are active, precisely one of the seven
nonzero functionals has \(Z_f=\varnothing\), two have \(Z_f=Z_i\), two
have \(Z_f=Z_j\), and two have \(Z_f=Z_i\triangle Z_j\).  With exactly
one active circuit, three planes are unchanged and four toggle.  With
neither active, the full flow and all seven defects are unchanged.

### The exact quotient-boundary and Hamming-weight update

The preceding statement can be made completely explicit.  Consider a
reciprocal exchange between omitted classes \(A_i,A_j\).  Let
\(a\in A_i\), \(b\in A_j\), so that
\[
 T_i'=T_i+a-b,\qquad T_j'=T_j+b-a.
\]
Write \(C_i=C_{T_i}(a)\), \(C_j=C_{T_j}(b)\), and put
\[
 \alpha=1_{b\in K_i},\qquad \beta=1_{a\in K_j}.
\]
The exchange law (8) gives
\[
 K_i'=K_i\triangle\alpha C_i,\qquad
 K_j'=K_j\triangle\beta C_j.                                \tag{16}
\]
Let \(k\) be the coordinate not in \(\{i,j\}\).  Since \(T_k\), hence
\(K_k\), is unchanged, contract the components of \(K_k\) once and for
all.  If
\[
 \partial_k:\mathbb F_2^{E(G)}\longrightarrow
 \mathbb F_2^{\operatorname{comp}(K_k)}
\]
is the boundary map after this contraction, define
\[
\begin{split}
 Q={}&\alpha(C_i\cap K_j)
   \triangle\beta(C_j\cap K_i)\\
   &\triangle\alpha\beta(C_i\cap C_j).
\end{split}
\]
Boolean expansion of the intersection gives the exact identity
\[
 (K_i'\cap K_j')\triangle(K_i\cap K_j)=Q.
\]
Consequently the untouched-coordinate defect vector satisfies
\[
 \omega_k'=\omega_k+\partial_k Q.     \tag{17}
\]
In particular, writing \(|\cdot|\) for Hamming weight,
\[
 d_k'-d_k
  =|\partial_kQ|
   -2\,|\operatorname{supp}(\omega_k)
          \cap\operatorname{supp}(\partial_kQ)|.             \tag{18}
\]
Thus this exchange lowers the untouched-coordinate defect precisely
when its quotient-boundary toggle meets more currently bad components
than good components.  It is neutral precisely when those two numbers
are equal.

This is a cut criterion, but not by itself an averaging proof.  The
14-vertex fixed-coordinate countermodel has a selected coordinate for
which every legal exchange that keeps its quotient fixed moves in the
wrong direction.  Exchanges involving that coordinate change the
quotient itself, and the other six Fano planes also change their
zero-subgraphs.  Therefore a proof of descent for the minimum over all
seven planes cannot follow by averaging (12) in one fixed quotient.

The literal audit

```sh
python3 scratch/verify_jaeger_reciprocal_exchange_defect_formula.py
```

checks (16)--(18) for every legal exchange incident with both the
14-vertex fixed-coordinate countermodel and the explicit
\((4,4,4,4,4,4,4)\) state in the targeted order-16 fibre.  It checks 108
and 147 candidate swaps respectively, including 18 and 25 legal swaps.
This finite audit verifies the transcription of the formula; the proof
above is the general argument.

## 4. A rigorous obstruction to the disjointness strengthening

A tempting strengthening of (5) is to seek a packing with
\[
                         K_i\cap K_j=\varnothing               \tag{19}
\]
for some two coordinates.  This is false already in the Petersen
graph, independently of the chosen star or packing.

Indeed, let \(K,L\) be two edge-disjoint spanning subgraphs of a cubic
graph such that every vertex has odd degree in each.  At a vertex,
\[
 \deg_K(v)+\deg_L(v)\leq3
\]
and both summands are positive and odd.  Hence both are one.  Therefore
\(K\) and \(L\) are disjoint perfect matchings, and \(K\cup L\) is a
2-factor whose cycles alternate between the two matchings.  Every one
of those cycles is even.

The Petersen graph has no even 2-factor.  In its standard outer-cycle,
inner-star presentation, a perfect matching uses an odd number of
spokes.  Three spokes are impossible: the two unmatched outer indices
would have to differ by one modulo five, while the same two inner
indices would have to differ by two.  With one or five spokes, the
complement is directly two 5-cycles.  Hence every 2-factor of Petersen
is two odd 5-cycles.

By (2), every \(K(T_i)\) is an all-vertex odd subgraph.  The preceding
argument proves
\[
                  K(T_i)\cap K(T_j)\ne\varnothing
                  \quad\text{for every }i\ne j                 \tag{20}
\]
for every triple of Petersen spanning trees, including every
vertex-star packing.  Thus no proof of (5) can work by forcing the pure
coordinate class (4) to be empty.

The independent exhaustive checker enumerates every star packing.  For
each of the ten choices of the star it finds 4,416 ordered packings;
none has a disjoint pair of \(K\)-forests.  Nevertheless 384 packings
have at least one coordinate satisfying (5), confirming that the exact
contracted-Eulerian target survives while the disjointness
strengthening fails:

```sh
python3 scratch/verify_jaeger_k_forest_petersen.py
```

## What remains

Equations (5), (8), and (9) reduce the star-fibre support-five problem
to cancelling an even set of component defects by legal reciprocal
tree exchanges.  No argument proving that cancellation exists in every
3-edge-connected cubic graph is obtained here.  The Petersen
obstruction shows that nonemptiness of the pure coordinate class is not
itself a defect; only its boundary in the contracted \(K_i\)-quotient
matters.

## AI-use disclosure

OpenAI Codex, under human direction, derived the identities, found the
Petersen obstruction, implemented the exhaustive checker, and drafted
this note.  The universal component-parity selection lemma remains
unproved, and no resolution of FiveCDC is claimed.
