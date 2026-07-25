# The outer quartic is a residual incidence divisor, not an extra branch obstruction

Date: 25 July 2026

## Audited conclusion

For the normalized outer case-c equation
\[
UV+2hUV'-3hU'V=1,\qquad
\deg U=7,\quad\deg V=10,
\]
put
\[
R(h)=h\frac{V(h)^2}{U(h)^3},\qquad
L=\frac{v_{10}^2}{u_7^3},\qquad
E(h)=hV(h)^2-LU(h)^3.
\]
Then \(E\) has degree four and its roots are the four residual,
unramified points in the fiber \(R^{-1}(L)\).  The ramification in that
fiber is concentrated at \(h=\infty\), with index \(17\).  Thus \(E\)
is naturally an **incidence polynomial on the normalized outer
dicritical component**, but it is not a branch divisor.

The four roots do not contradict the diagonal degree/contact data by
Riemann--Hurwitz, local monodromy, or valuation theory alone.  In fact,
the complete \((8,12)\), contact-one diagonal formal cap can be built
uniformly over the étale quartic algebra \(k[t]/(E)\).  Therefore any
obstruction must use the finite Newton cutoff or a new global
incidence correspondence.

There is one sharp conditional monodromy route.  A permutation of type
\((17,1^4)\) has no invariant subset of size \(8\) or \(12\).  Hence
case c would be impossible if the eight \(P\)-leaves or twelve
\(Q\)-leaves could be identified injectively and equivariantly with
subsets of the twenty-one outer sheets.  No such leaf-to-sheet map is
currently established.  Treating it as automatic would conflate the
diagonal Puiseux branches with sheets of the outer rational function.

## 1. Exact differential identities

The outer equation gives
\[
R'(h)
=\frac{V}{U^4}
\left(UV+2hUV'-3hU'V\right)
=\frac{V}{U^4}. \tag{1}
\]
Also
\[
R-L=\frac{E}{U^3} \tag{2}
\]
and direct differentiation gives
\[
UE'-3U'E
=V\left(UV+2hUV'-3hU'V\right)
=V. \tag{3}
\]

The outer equation proves \(\gcd(U,V)=1\).  Moreover:

- \(E\) and \(U\) cannot share a root: \(U(0)=1\), and at a nonzero
  root of \(U\), one has \(E=hV^2\ne0\);
- \(E\) and \(V\) cannot share a root because
  \(E=-LU^3\ne0\) there; and
- at a root \(\alpha\) of \(E\), (3) gives
  \[
  E'(\alpha)=\frac{V(\alpha)}{U(\alpha)}\ne0.
  \]

Thus \(E\) is squarefree and coprime to \(UV\).  In particular every
finite point of \(E=0\) is an unramified point of \(R\), since
\[
R'(\alpha)=\frac{V(\alpha)}{U(\alpha)^4}\ne0. \tag{4}
\]
Finally,
\[
E(0)=-L\ne0, \tag{5}
\]
so all four incidence points lie in the open boundary orbit where the
diagonal parameter \(t\) is a unit.

## 2. Riemann--Hurwitz forces, rather than forbids, the quartic

The rational function \(R\) has degree \(21\).  Its three fibers have
partitions
\[
(2^{10},1),\qquad(3^7),\qquad(17,1^4). \tag{6}
\]
The ramification contributions are
\[
10,\qquad14,\qquad16,
\]
and
\[
10+14+16=40=2\cdot21-2. \tag{7}
\]
Thus Riemann--Hurwitz is exactly saturated.

One can also use (7) to derive \(\deg E=4\).  If \(\deg E=d\), then
(2) has order \(21-d\) at infinity, so the contribution there is
\(20-d\).  The first two fibers already contribute \(10+14\), hence
\[
10+14+(20-d)=40,
\]
which forces \(d=4\).  The four finite roots of \(E\) contribute no
ramification.  They are required to complete the degree-\(21\) fiber;
they are not surplus points competing for a ramification budget.

Equivalently,
\[
\operatorname{div}_0(R-L)
=17[\infty]+\operatorname{div}(E),\qquad
\operatorname{div}_\infty(R-L)=3\operatorname{div}(U). \tag{8}
\]
At each root \(\alpha\) of \(E\),
\[
\operatorname{ord}_{\alpha}(R-L)=1. \tag{9}
\]
This unit valuation carries no parity or semigroup restriction capable
of excluding pole degrees \(8\) and \(12\).

## 3. What monodromy does and does not say

Let \(\sigma_L\) be local monodromy around the third branch value.
From (6),
\[
\sigma_L\sim(17)(1)(1)(1)(1). \tag{10}
\]
The four roots of \(E\) are the four fixed sheets in (10); the
seventeen-cycle comes from infinity.

Every invariant subset of the sheet set is a union of cycles of
\(\sigma_L\).  Its size therefore belongs to
\[
\{0,1,2,3,4,17,18,19,20,21\}. \tag{11}
\]
In particular there is no invariant subset of size \(8\) or \(12\).
This proves the following conditional statement.

> **Conditional leaf--sheet obstruction.**
> If the eight diagonal \(P\)-leaves, or the twelve diagonal
> \(Q\)-leaves, inject into the outer twenty-one-sheet fiber in a way
> preserved by monodromy around \(L\), then case c is impossible.

The hypothesis is the whole missing theorem.  The outer sheets
parameterize preimages of a target value under \(R\).  The diagonal
leaves are roots of leading cap polynomials after a different toric
normalization.  Newton support and the bracket do not currently provide
an injection between those sets.  They may map with multiplicity,
through a correspondence, or not at all.  Transitivity of the complete
outer monodromy also prevents treating the four fixed sheets as a
separate degree-four subcover.

Thus (11) is a useful target for a future global incidence theorem, not
an unconditional obstruction.

## 4. A simultaneous formal countermodel over the quartic fiber

Let \(k\) be algebraically closed of characteristic zero and
\[
A=k[t]/(E(t)).
\]
Equations (3)--(5) show that \(A\) is étale of rank four and that \(t\)
is a unit in \(A\).  Take
\[
f(v)=v^8-1,\qquad g(v)=v^{12}+2v. \tag{12}
\]
They are squarefree and coprime, and
\[
\gcd(f',g')=1. \tag{13}
\]
The bounded linear operator
\[
(\phi,\psi)\longmapsto \phi g'-f'\psi
\]
from degrees \((8,12)\) onto degree at most \(19\) is surjective over
\(\mathbf Q\), hence remains surjective after base change to \(A\).

The formal transverse lifting recursion therefore constructs
\[
X,Y\in A[v][[u]]
\]
with
\[
X(0,v)=f(v),\qquad Y(0,v)=g(v),
\]
\[
\deg_v[u^n]X\le8,\qquad
\deg_v[u^n]Y\le12,
\]
and
\[
X_uY_v-X_vY_u=u^2(t+uv)^2. \tag{14}
\]
After base change to any of the four geometric roots of \(E\), (14)
is an exact formal diagonal cap with eight and twelve simple leaves.
Under the standard blowdown it has the contact-one star and resultant
order \(96\).

This is not a finite global case-c polynomial pair.  It proves the
narrow no-go statement needed here: the étale incidence algebra, its
four valuations, and arbitrarily deep completed local bracket jets are
jointly compatible with the diagonal degree/contact data.  Chinese
remaindering over
\[
A\simeq\prod_{\alpha:E(\alpha)=0}k
\]
also shows that finite jets at the four points can be prescribed
independently.  A contradiction must therefore couple them through the
global finite-support cutoff or through the missing monodromy-equivariant
leaf--sheet correspondence.

## 5. Exact good-reduction check

At the certified rational outer point \(s=26839\) modulo \(32003\),
\[
E=
15441h^4+14388h^3+3553h^2-6746h-2249.
\]
It is squarefree and factors as two linear factors and one irreducible
quadratic.  Its constant term, discriminant, and resultants with \(U\)
and \(V\) are all nonzero.  This is an independent exact check of the
incidence and étaleness statements.

Companion verifier:

```text
.venv/bin/python current_context/verify_case_c_outer_quartic_incidence_no_go.py
```
