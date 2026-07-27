# Case c: the correct cap incidence has degree four, not eight or twelve

Date: 25 July 2026

## Audited conclusion

The conditional monodromy argument based on invariant subsets of sizes
\(8\) and \(12\) cannot be upgraded by the natural toric
correspondence.  Those numbers count the separate \(P\)- and
\(Q\)-projections at the diagonal cap.  The common normalized boundary
map has degree
\[
\gcd(8,12)=4.
\]

The exact common object is the four-branch Kummer cover
\[
H=(z-\lambda)^4.
\]
It is numerically compatible with the four simple roots of the outer
quartic \(E\) in the fiber of type \((17,1^4)\).  Thus the corrected
monodromy subset has size \(4\), which is present, and gives no
contradiction.

There is also no canonical projective identification of these two
four-point sets.  The Kummer four-point divisor has vanishing classical
binary-quartic invariant \(J\), whereas the outer quartic has
\(J\ne0\) on all five certified geometric outer points modulo \(32003\).
An arbitrary set-theoretic bijection transports neither derivatives nor
cap normalizations.  Even after choosing one, the formal cap
normalization remains freely variable while the outer norm is fixed.

Finite Newton support can still obstruct termination of the cap lift,
but it does not change the degree-four face normalization.  Any positive
global proof must derive a new, non-projective correspondence from the
terminal bracket rows; it cannot come from injecting the eight or twelve
cap leaves into the outer sheet set.

## 1. The exact candidate correspondence

On the diagonal face, after removing the boundary monomials, the two
leading functions are
\[
\overline P=a(z-\lambda)^8,\qquad
\overline Q=b(z-\lambda)^{12},
\qquad ab\ne0.
\tag{1}
\]
Put
\[
\eta=z-\lambda,\qquad H=\eta^4.
\tag{2}
\]
Then
\[
\overline P=aH^2,\qquad
\overline Q=bH^3.
\tag{3}
\]
The image is the monomial cusp
\[
\overline Q^{\,2}=\frac{b^2}{a^3}\overline P^{\,3},
\tag{4}
\]
whose normalization parameter is
\[
H=\frac{a}{b}\frac{\overline Q}{\overline P}
\tag{5}
\]
away from the cusp point.  Therefore the common boundary map is
\[
\eta\longmapsto H=\eta^4
\tag{6}
\]
and has degree four.

By contrast, a generic value of \(\overline P\) has eight inverse
images: there are two possible values of \(H\), each with four fourth
roots.  A generic value of \(\overline Q\) has twelve inverse images:
three possible values of \(H\), again with four fourth roots.  The
eight- and twelve-leaf sets are therefore fibers of separate coordinate
projections.  They are not sheet sets of the common normalized map.

This factorization is intrinsic.  The finite Newton cutoff changes
successive normal jets, but all inward terms vanish on the face and
cannot change the function-field degree in (6).

## 2. Comparison with the outer passport

For the outer endpoint,
\[
R(h)=h\frac{V(h)^2}{U(h)^3},\qquad
E(h)=hV(h)^2-LU(h)^3,
\tag{7}
\]
and the fiber over \(L\) has partition
\[
(17,1,1,1,1).
\tag{8}
\]
The four roots of \(E\) are precisely the four simple sheets in (8).
Thus a four-to-four incidence is degree-compatible.  Local monodromy
fixes both the four-point residual set and every union of its singleton
cycles.  The corrected incidence produces compatibility, not an
obstruction.

The toric chart also explains why individual cap leaves are not outer
sheets.  In diagonal coordinates
\[
x=u(t+uw),\qquad y=u^{-1},
\]
the outer coordinate is
\[
h=xy^2=\frac{t}{u}+w.
\tag{9}
\]
For a simple cap leaf \(w=w_i(u)\) and \(t\ne0\), the reciprocal outer
coordinate satisfies
\[
h^{-1}=\frac{u}{t}+O(u^2).
\tag{10}
\]
Hence every leaf maps isomorphically to the same completed outer branch
at \(h=\infty\).  Since
\[
R(h)-L=\frac{d}{u_7^3}h^{-17}+O(h^{-18}),
\qquad d=[h^4]E,
\]
each leaf carries the entire local degree-\(17\) cover:
\[
R(h(u))-L
=\frac{d}{u_7^3t^{17}}u^{17}(1+O(u)).
\tag{11}
\]
Restricting valuations therefore sends all cap leaves to the same
ramified outer prime.  Selecting one generic sheet from its
\(17\)-cycle requires a noncanonical choice of a seventeenth-root
phase.  It is not an equivariant leaf-to-sheet construction.

## 3. The four-point sets are not projectively identical

A fiber of (6) is a Kummer divisor
\[
X^4-cZ^4=0,\qquad c\ne0.
\tag{12}
\]
For a binary quartic
\[
F=aX^4+bX^3Z+c_2X^2Z^2+dXZ^3+eZ^4,
\]
use the classical relative invariants
\[
\begin{aligned}
I(F)&=12ae-3bd+c_2^2,\\
J(F)&=72ac_2e+9bc_2d-27ad^2-27b^2e-2c_2^3.
\end{aligned}
\tag{13}
\]
Vanishing of \(J\) is invariant under projective changes of the source
coordinate.  The Kummer divisor (12) has
\[
J=0.
\tag{14}
\]

At the good-reduction prime \(32003\), the two rational factors and the
one cubic factor of the outer Hurwitz algebra give the following exact
values for \(J(E)\):
\[
\begin{array}{c|c}
\text{outer factor}&J(E)\\ \hline
t=26839&2818\\
t=16621&11135\\
\mathbf F_{32003}[t]/(t^3-11133t^2-11294t-6180)
&-13539-15225t+8221t^2.
\end{array}
\tag{15}
\]
All are nonzero.  Thus no projective isomorphism of the two toric
boundary components carries a Kummer fiber (12) to the four roots of
\(E\) on any of the five certified geometric outer points.

One can of course choose a bijection between two four-element sets over
an algebraic closure.  Such a choice is one of \(4!\) labelings, is not
functorial, and gives no transformation law for \(E'(r_i)\), the cap
residues, or the resonant constants.

## 4. A bijection does not constrain the cap constants

The freedom is exact already in the complete formal cap equation.  Keep
the outer pair \(U,V\), hence \(E\), fixed, and take
\[
f_A(w)=w^8-A,\qquad g(w)=w^{12}+2w.
\tag{16}
\]
For
\[
A\ne0,\qquad A^{11}\ne256,
\]
the two polynomials are squarefree and coprime, and
\[
\gcd(f_A',g')=1.
\]
The formal transverse lifting theorem therefore solves the complete
local diagonal bracket for every such \(A\), over every root of \(E\).
But
\[
\operatorname {Res}(f_A,g)
=A(A^{11}-256)
\tag{17}
\]
varies with \(A\), while the outer norm identity
\[
\operatorname {Res}(E,V)
=[h^4]E\;\operatorname {Disc}(E)\operatorname {Res}(E,U)
\tag{18}
\]
is unchanged.

Consequently neither a four-point labeling nor (18) fixes the cap
normalization.  A relation can only arise from the global finite-support
termination equations, which the formal family deliberately does not
satisfy.  Deriving such a relation would be a new terminal-row theorem,
not a consequence of monodromy or incidence alone.

## 5. General multiplicity-gcd rule

Suppose a cap face has
\[
\overline P=a\eta^m,\qquad
\overline Q=b\eta^n,\qquad ab\ne0,
\tag{19}
\]
and put
\[
g=\gcd(m,n),\qquad m=gm_0,\quad n=gn_0,
\quad\gcd(m_0,n_0)=1.
\]
Then
\[
H=\eta^g,\qquad
(\overline P,\overline Q)=(aH^{m_0},bH^{n_0}).
\tag{20}
\]
By Bézout, \(H\) is a Laurent monomial in
\(\overline P/a\) and \(\overline Q/b\), so \(H\) is the normalization
parameter of the common monomial curve.  The common face cover has
degree \(g\), not \(m\) or \(n\).

For the case-c caps this gives
\[
\begin{array}{c|c|c}
\text{cap}&(m,n)&g\\ \hline
\text{vertical}&(2,3)&1\\
\text{diagonal}&(8,12)&4.
\end{array}
\tag{21}
\]

For a higher corner chain, any sheet-incidence argument should therefore
compare the \(g\) branches of the normalized common face with an
outer residual divisor of degree \(g\).  For \(g\ge4\), projective
configuration invariants provide an immediate functoriality test:
a monomial Kummer fiber is highly special, and a generic residual
outer divisor will not be projectively equivalent to it.  If only a
higher-bidegree correspondence exists, its degree and inertia action
must be included explicitly; it cannot support a simple invariant-subset
argument.

Companion verifier:

```text
.venv/bin/python current_context/verify_case_c_degree_four_incidence_audit.py
```
