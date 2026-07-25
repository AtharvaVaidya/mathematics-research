# What the GGHV normalization does and does not preserve

Date: 24 July 2026

## Conclusion

The reduced \((8,28)\) systems of GGHV are obtained from a hypothetical
plane Keller counterexample by polynomial and Laurent birational
coordinate changes.  In the last step of Proposition 4.3 the authors use
the involution of
\[
L^{(1)}=K[x,x^{-1},y]
\]
given by
\[
\phi(x)=x^{-1},\qquad \phi(y)=x^4y.
\tag{1}
\]
This is an automorphism on \(x\ne0\), but not an automorphism of
\(\mathbb A^2\).  Its Jacobian is \(-x^2\), which explains the reduced
equation
\[
[\phi(P),\phi(Q)]=-x^2[P,Q].
\tag{2}
\]

Two different conclusions must therefore be kept separate.

1. The nonconstant finite-limit curves in the normalized chart do give
   genuine irreducible components of the original nonproper-value set.
   This follows from explicit escaping arcs and does not require a global
   boundary-tree identification.
2. The self-intersections and determinant labels of a convenient toric
   completion of the normalized chart are not automatically the labels of
   the complete boundary tree resolving the original polynomial map.
   Those require transporting every divisorial valuation through all
   preceding blowups and retaining the target-infinity descendants.

Thus the degree-\((8,12)\) non-cusp curve and its function-field
normalization data remain legitimate asymptotic invariants.  The proposed
local-to-global determinant contradiction does not.

## 1. Exact source in Proposition 4.3

The source is J. A. Guccione, J. J. Guccione, R. Horruitiner, and
C. Valqui, *Increasing the degree of a possible counterexample to the
Jacobian conjecture from 100 to 108*,
<https://arxiv.org/abs/2204.14178>.

On PDF page 10, Proposition 4.3 says that a counterexample in case
\((8,28)\) produces \(P,Q\in L^{(1)}\) with \([P,Q]=x^2\) and one of the
two final support pairs
\[
\begin{aligned}
\Delta_P&=\operatorname{conv}
\{(0,0),(1,0),(8,14),(8,16),(0,8)\},\\
\Delta_Q&=\operatorname{conv}
\{(0,0),(2,1),(12,21),(12,24),(0,12)\},
\end{aligned}
\tag{3c}
\]
or the same pair with the two vertical vertices omitted.

The proof first swaps \(x,y\), and then repeatedly uses Laurent
automorphisms
\[
x\longmapsto x,\qquad y\longmapsto y+\lambda x^{-j}
\quad(j=2,3,4)
\tag{4}
\]
to cut Newton edges.  On PDF page 12 it applies (1).  Immediately before
that last step, the relevant vertices are
\[
\begin{array}{c|c}
P&(-1,0),(0,0),(56,16),(48,14),(32,8)\ \text{in case c},\\
Q&(2,1),(0,0),(84,24),(72,21),(48,12)\ \text{in case c}.
\end{array}
\]
A monomial \(x^ay^b\) transforms under (1) to
\[
x^{-a+4b}y^b.
\tag{5}
\]
Formula (5) gives exactly (3c), including
\[
(32,8)\mapsto(0,8),\qquad(48,12)\mapsto(0,12).
\]
There is no finite Kummer cover in this Proposition 4.3 chain; the
function field is unchanged.

## 2. Transfer lemma for finite asymptotic curves

Let \(\Psi:U'\to U\) be the composite inverse birational coordinate
change on the common open set \(x\ne0\), and let
\[
F'=F\circ\Psi
\]
extend polynomially to a boundary divisor or an exceptional divisor in
the normalized chart.  Suppose a one-parameter family
\(\eta(t,c)\in U'\) satisfies
\[
\|\Psi(\eta(t,c))\|\longrightarrow\infty,\qquad
F'(\eta(t,c))\longrightarrow\gamma(c)
\quad(t\to0),
\tag{6}
\]
and \(\gamma\) is nonconstant.  Then every \(\gamma(c)\) is a nonproper
value of the original \(F\).  Since the nonproper set of a dominant plane
polynomial map is a curve, the irreducible closure of \(\gamma(\mathbb A^1)\)
is one of its components.

For the full case-c line, take in the final normalized chart
\[
x=t,\qquad y=c.
\]
Reversing (1) gives
\[
x_{\rm old}=t^{-1},\qquad y_{\rm old}=t^4c,
\tag{7}
\]
so the source escapes and the finite limit is
\[
\gamma_c(c)=(P(0,c),Q(0,c)),
\]
of degrees \((8,12)\).

For the a/b finite dicritical, put
\[
z=xy=t,\qquad w=xy^2=c\ne0.
\]
Then
\[
x=\frac{t^2}{c},\qquad y=\frac ct,
\]
and reversing (1) gives
\[
x_{\rm old}=\frac c{t^2},\qquad
y_{\rm old}=\frac{t^7}{c^3}.
\tag{8}
\]
Again the source escapes while the normalized map tends to
\[
\gamma_{ab}(c)=(a_0(c),b_0(c)).
\]
The earlier shifts (4) add only positive powers of \(t\) after the
inversion and cannot make the escaping \(t^{-1}\) or \(t^{-2}\) coordinate
bounded.  The initial polynomial swap or affine automorphism is proper and
also preserves escape.

Because all transformations are birational, the function-field degree
\[
\delta=[\mathbb C(c):\mathbb C(\gamma_1(c),\gamma_2(c))]
\]
and the inertia of the corresponding divisorial valuation transfer
without a Kummer rescaling.  They should still be phrased valuation
theoretically rather than attached to the bare coordinate line.

## 3. What remains chart-dependent

The normalized toric compactification omits data needed for a global
intersection-matrix argument:

- which additional exceptional divisors were created by the edge-cutting
  sequence (4);
- the complete chain between the normalized finite dicriticals and the
  original line at infinity;
- horizontal descendants above roots of the outer face that map to target
  infinity;
- self-intersections after all required source and target basepoints are
  resolved.

The augmented-canonical value of a fixed divisorial valuation can be
transported because (2) records the volume-form change.  A determinant
label computed from a truncated toric fan cannot: it is a cofactor of the
complete boundary intersection matrix and changes when omitted arms are
restored.

Accordingly:

- the non-cusp asymptotic-curve and contact-spectrum theorems survive this
  audit;
- the two local cluster resolutions survive as local valuation
  calculations;
- their provisional determinant labels and any Borisov type assignment
  do not yet furnish a global contradiction;
- the finite-field elimination of the two necessary GGHV coefficient
  systems is unaffected by this geometric distinction.
