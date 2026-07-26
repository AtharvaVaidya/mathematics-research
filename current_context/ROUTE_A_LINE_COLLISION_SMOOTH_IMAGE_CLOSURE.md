# Route A: a smooth line-collision image forces invertibility

Date: 25 July 2026

## Outcome

Let
\[
F=(p,q):\mathbf A^2_{\mathbf C}\longrightarrow\mathbf A^2_{\mathbf C}
\]
have nonzero constant Jacobian, and let \(L\subset\mathbf A^2\) be an
affine coordinate line.  Suppose that
\[
F|_L:L\longrightarrow\Gamma=\overline{F(L)}
\]
is birational and surjective.

There is an exact closure theorem in the smooth or rectifiable case:

> **Smooth collision-image theorem.**  If \(\Gamma\) is smooth, then
> \(F\) is a polynomial automorphism.  Consequently
> \(F^{-1}(\Gamma)=L\), so no additional component can dominate
> \(\Gamma\).

The same conclusion holds if \(\Gamma\) is rectifiable.  In particular,
the degree-six plane Keller map obtained by composing a hypothetical
Route A cubic with the canonical quadratic plane chart cannot have a
smooth or rectifiable distinguished collision curve.

This does not close the singular case.  Birationality, surjectivity, and
the immersion supplied by the Keller condition do not prove that
\(\Gamma\) is smooth.  A singular image can have several smooth branches
whose normalization identifies distinct points of \(L\).  Thus every
surviving Route A cubic must produce precisely such a multi-branch
singularity.

## 1. Primary theorem used

Gwoździewicz proved:

> If a polynomial map \(H:\mathbf A^2\to\mathbf A^2\) over an
> algebraically closed field of characteristic zero has nonzero
> constant Jacobian and is injective on one affine line, then \(H\) is a
> polynomial automorphism.

The primary source is J. Gwoździewicz,
*Injectivity on one line*, 1993,
[arXiv:alg-geom/9305008](https://arxiv.org/abs/alg-geom/9305008).
Its proof rectifies the embedded image by the Abhyankar--Moh theorem and
then uses the Newton polygons of a Jacobian pair.  The embedding theorem
is S. S. Abhyankar and T. T. Moh,
*Embeddings of the line in the plane*, J. Reine Angew. Math. 276
(1975), 148--166,
[doi:10.1515/crll.1975.276.148](https://doi.org/10.1515/crll.1975.276.148).

Yang and Du later formulated the directly relevant smooth-image
criterion: if the image of one line under a complex Keller map is
smooth, the map is invertible.  See H. Yang and X. Du,
*Polynomial maps in two variables with smoothness on one line*,
Comm. Algebra 46 (2018), 1534--1538,
[doi:10.1080/00927872.2017.1347667](https://doi.org/10.1080/00927872.2017.1347667).

## 2. Why smoothness gives injectivity here

Write \(L=\operatorname {Spec}\mathbf C[t]\), and let
\[
\gamma(t)=F|_L(t).
\]
The coordinate ring of \(\Gamma\) is
\[
A=\mathbf C[\gamma_1(t),\gamma_2(t)]\subset\mathbf C[t].
\]
Choose a nonconstant \(h(t)\in A\).  The element \(t\) is integral over
\(\mathbf C[h(t)]\), hence over \(A\).  Therefore
\[
\nu:\mathbf A^1=\operatorname {Spec}\mathbf C[t]\longrightarrow\Gamma
\tag{1}
\]
is finite.  By hypothesis it is birational and surjective, so it is the
normalization of \(\Gamma\).

If \(\Gamma\) is smooth, it is normal.  The finite birational map (1) is
then an isomorphism.  In particular \(F|_L\) is injective.  The
Gwoździewicz theorem now makes \(F\) an automorphism.

For an automorphism,
\[
F^{-1}(F(L))=L.
\tag{2}
\]
Thus (2) contradicts any mandatory collision hypothesis asserting that
a second source component dominates \(\Gamma\).

If \(\Gamma\) is rectifiable, a target automorphism sends it to a
coordinate line, so it is already smooth and the same argument applies.

## 3. Exact normalized form

In the rectifiable case, affine and polynomial automorphisms of source
and target put
\[
L=V(x),\qquad \Gamma=V(p),
\]
and normalize the birational restriction to
\[
F(0,y)=(0,y).
\tag{3}
\]
Consequently
\[
p=xR(x,y),\qquad
q=y+xS(x,y).
\tag{4}
\]
After scaling the target area form, assume \(J(p,q)=1\).  Direct
expansion gives
\[
\boxed{
1
=R
+x\left(R_x+RS_y-R_yS\right)
+x^2\left(R_xS_y-R_yS_x\right).
}
\tag{5}
\]
Restriction to \(x=0\) gives
\[
R(0,y)=1.
\tag{6}
\]

Equation (3) makes \(F\) injective on \(L\).  Hence \(F\) is an
automorphism by the primary theorem.  Its first coordinate \(p\) is a
coordinate polynomial, so its zero fiber is irreducible.  Since
\(p=xR\) and \(R(0,y)=1\), this forces
\[
R=1.
\tag{7}
\]
Equation (5) then reduces to \(S_y=0\).  Thus every normalized solution
is triangular:
\[
\boxed{
p=x,\qquad q=y+h(x),\qquad h(0)=0.
}
\tag{8}
\]
In the notation (4), \(S=h(x)/x\in\mathbf C[x]\).

Therefore an additional component \(V(R)\) is impossible.  The
normalized Jacobian equation has no nontrivial collision solution.

## 4. Application to the Route A degree-six lift

For the quadratic pseudo-plane
\[
S=\operatorname {Spec}
\mathbf C[u,v,w]/(w^2-u-u^2v),
\]
the polynomial étale plane chart is
\[
u=a^2,\qquad
w=a(1+2a^2b),\qquad
v=4b(1+a^2b).
\tag{9}
\]
The line
\[
\widetilde D=V(a)\simeq\mathbf A^1_b
\tag{10}
\]
maps isomorphically to the distinguished divisor
\[
D=V(u,w)\simeq\mathbf A^1_v,\qquad v=4b.
\tag{11}
\]

If a Route A étale map \(e:S\to\mathbf A^2\) had generic degree three,
then
\[
H=e\circ\pi_2:\mathbf A^2_{a,b}\longrightarrow\mathbf A^2
\tag{12}
\]
would be a Keller map of generic degree six.  The mandatory collision
theorem says that \(D\) maps birationally onto its image
\(\Gamma_D\), with at least one additional source divisor dominating
the same curve.  Equations (10)--(12) show that
\[
H|_{\widetilde D}:\widetilde D\longrightarrow\Gamma_D
\]
is the normalization map.

If \(\Gamma_D\) were smooth or rectifiable, the smooth collision-image
theorem would make \(H\) an automorphism, contradicting its generic
degree six and the additional collision component.  Hence
\[
\boxed{
\text{every surviving Route A cubic forces }\Gamma_D
\text{ to be a nonnormal singular plane curve.}
}
\tag{13}
\]

Moreover \(dH\) is invertible, so the normalization map is immersive.
More decisively, \(H\) has degree six and is not an automorphism, so the
contrapositive of Gwoździewicz's theorem supplies distinct
\(b_1,b_2\in\widetilde D\) with
\[
H(0,b_1)=H(0,b_2).
\]
Thus the singular image must identify distinct normalization points; it
cannot be explained only by a unibranch cusp with vanishing
normalization derivative.

## 5. Why smoothness cannot be inferred

Consider
\[
\gamma(t)=\left(t^2-1,\ t(t^2-1)\right).
\tag{14}
\]
It is finite, birational, and surjective onto
\[
\Gamma_0:\quad Y^2=X^2(X+1).
\tag{15}
\]
The inverse on \(X\ne0\) is \(t=Y/X\).  Its derivative is
\[
\gamma'(t)=(2t,3t^2-1),
\tag{16}
\]
which never vanishes.  Nevertheless
\[
\gamma(1)=\gamma(-1)=(0,0),
\]
and \(\Gamma_0\) has a node at the origin.

This phenomenon is compatible even with an ambient map whose Jacobian
is nonzero all along the line.  Define
\[
G(x,t)
=
\left(
t^2-1-x,\
t(t^2-1)-\frac32xt
\right).
\tag{17}
\]
Then
\[
J(G)=1+\frac32x,
\tag{18}
\]
so \(J(G)=1\) on \(x=0\), and \(G|_{x=0}=\gamma\).  The map is not a
Keller map because (18) vanishes on another line, but it proves that
birationality, surjectivity, and linewise étaleness do not imply a smooth
image.

It also realizes the additional collision component exactly.  If
\[
f(X,Y)=Y^2-X^2(X+1),
\]
then
\[
\boxed{
f(G(x,t))
=
\frac{x}{4}
\left(
4(x+1)^2-(3x+4)t^2
\right).
}
\tag{19}
\]
The second factor is irreducible and defines another curve dominating
\(\Gamma_0\).  On the affine open
\[
U=D(2+3x)\subset\mathbf A^2,
\]
the map \(G|_U\) is étale, the full line \(x=0\) is retained, and the
second component in (19) is retained densely.  Thus the smooth-branch
normalization, its nodal self-identification, and an additional
collision divisor are all compatible with étaleness on an affine open.
The price is the nonconstant unit \(2+3x\); this is not a plane Keller
counterexample.

The unresolved input is therefore precise: rule out the self-
identifications of the normalization line using genuinely global Keller
information.  The extra collision component and the degree-six count do
not by themselves provide that argument.
