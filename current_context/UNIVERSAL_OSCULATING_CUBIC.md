# A universal osculating Weierstrass cubic

Date: 24 July 2026

## Verdict

The proposed strengthening of the radial contact theorem is true, with
one important geometric qualification.

Let \(r=k+1\ge2\).  Work in the Laurent total-degree filtration in
\((z,w)\), and suppose
\[
\deg P=2r,\qquad \deg Q=3r,\qquad \deg\{P,Q\}\le1,
\]
with leading forms
\[
P_{2r}=\alpha R^2,\qquad Q_{3r}=\beta R^3,
\qquad
R=w^{r-1}(uw+vz),
\]
where \(\alpha\beta uv\ne0\).  Put
\[
L=\frac{\beta^2}{\alpha^3}.
\]
Then there are constants \(c_5,c_4,c_3,c_2\) such that
\[
\boxed{
\mathcal H(P,Q)
=Q^2-LP^3+c_5PQ+c_4P^2+c_3Q+c_2P
}
\tag{1}
\]
has total Laurent degree at most
\[
\boxed{\deg\mathcal H(P,Q)\le r+3.}
\tag{2}
\]
An arbitrary constant \(c_0\) may be added without changing (2).

Thus the earlier four-valued contact spectrum is not an obstruction:
each of its possible high centralizer terms can be absorbed, in descending
order, by a coefficient of a generalized Weierstrass cubic.

The target curve
\[
\mathcal H(X,Y)+c_0=0
\tag{3}
\]
is not generically cuspidal.  It is a generalized Weierstrass cubic with
one **smooth** place at infinity.  For all but at most two values of
\(c_0\), it is a smooth plane cubic, hence an elliptic curve.  Singular
nodal or cuspidal members occur only at exceptional values.

Whenever restriction to \(z=0\) is regular and the leading form survives,
as it does in the a/b branch, write
\[
p(w)=P(0,w),\qquad q(w)=Q(0,w).
\]
Then
\[
\deg_w\mathcal H(p,q)\le r+3.
\tag{4}
\]
In the natural weighted compactification this says that the pullback
intersection order along the \(w\)-parametrization at infinity is at least
\[
\boxed{6r-(r+3)=5r-3.}
\tag{5}
\]
For a/b, \(r=4\), so a suitable target cubic has parametrized weighted
contact at least \(17\).

The word “parametrized” is essential.  If
\(\delta=[\mathbf C(w):\mathbf C(p,q)]\), the intrinsic intersection
multiplicity on the normalization of the image curve is the pullback
order divided by \(\delta\).  In the a/b branch
\(\delta\in\{1,2,4\}\), so the guaranteed intrinsic lower bounds are,
respectively,
\[
17,\qquad 9,\qquad 5.
\tag{6}
\]
Consequently (5) must not be advertised as intrinsic contact \(17\)
unless birationality of the boundary parametrization has separately been
proved.

## 1. The recursive cancellation

For constants already selected, put
\[
K(X,Y)=Y^2-LX^3+c_5XY+c_4X^2+c_3Y+c_2X.
\]
The exact chain-rule identity is
\[
\boxed{
\{P,K(P,Q)\}
=(2Q+c_5P+c_3)\{P,Q\}.
}
\tag{7}
\]
Its right side has degree at most \(3r+1\).  Therefore, if \(K(P,Q)\)
has top homogeneous degree \(d>r+3\), its leading part centralizes
\(P_{2r}=\alpha R^2\), hence \(R\).

The homogeneous Laurent centralizer lemma from the radial contact theorem
then gives
\[
d\equiv0\pmod r,\qquad
[K(P,Q)]_d=\gamma R^{d/r}.
\tag{8}
\]
After the degree-\(6r\) cancellation in \(Q^2-LP^3\), the only possible
high powers are \(R^5,R^4,R^3,R^2\).  They are exactly the leading forms
of
\[
PQ,\qquad P^2,\qquad Q,\qquad P:
\]
\[
\alpha\beta R^5,\qquad
\alpha^2R^4,\qquad
\beta R^3,\qquad
\alpha R^2.
\tag{9}
\]

Start with \(K_6=Q^2-LP^3\).  Descend through \(m=5,4,3,2\).
If \(mr>r+3\), equation (8) writes
\[
[K_{m+1}]_{mr}=\gamma_mR^m.
\]
Add the corresponding term from (9), with coefficient
\[
\begin{aligned}
c_5&=-\gamma_5/(\alpha\beta),&
c_4&=-\gamma_4/\alpha^2,\\
c_3&=-\gamma_3/\beta,&
c_2&=-\gamma_2/\alpha.
\end{aligned}
\tag{10}
\]
If a layer is already zero, take \(\gamma_m=0\).  Adding the degree-\(mr\)
term cannot recreate a previously killed higher layer.  If the new top
degree were still above \(r+3\), (8) would make it another multiple of
\(r\); there is no such multiple strictly between \((m-1)r\) and \(mr\).
This proves the induction and (2).

For \(r=2\) or \(r=3\), the \(2r\)-layer is already at or below the
threshold:
\[
\begin{array}{c|c|c}
r&r+3&\text{layers that need cancellation}\\ \hline
2&5&5r,4r,3r\\
3&6&5r,4r,3r\\
r\ge4&r+3&5r,4r,3r,2r.
\end{array}
\]
Thus \(c_2=0\) is sufficient in the two small cases.  This is the only
small-\(r\) adjustment.

## 2. Geometry of the target cubic

The ordinary projective closure of (3), in coordinates \([X:Y:T]\), is
\[
\begin{aligned}
\overline{\mathcal H}={}&
TY^2-LX^3+c_5TXY+c_4TX^2\\
&+c_3T^2Y+c_2T^2X+c_0T^3.
\end{aligned}
\tag{11}
\]
On \(T=0\), its only point is \([0:1:0]\).  Moreover
\[
\frac{\partial\overline{\mathcal H}}{\partial T}(0,1,0)=1,
\tag{12}
\]
so this point is smooth for every choice of the coefficients.  In the
chart \(Y=1\), its branch begins \(T=Lu^3+\cdots\); the line at infinity
is a flex tangent, not a cuspidal branch.

Completing the square,
\[
Y'=Y+\frac{c_5X+c_3}{2},
\]
puts the affine equation in the form
\[
Y'^2
=LX^3+\left(\frac{c_5^2}{4}-c_4\right)X^2
+ \left(\frac{c_5c_3}{2}-c_2\right)X
+ \left(\frac{c_3^2}{4}-c_0\right).
\tag{13}
\]
The discriminant of the cubic on the right is a quadratic polynomial in
its constant term with leading coefficient \(-27L^2\ne0\).  Hence only
at most two values of \(c_0\) make (3) singular.  A generic choice makes
it a smooth genus-one cubic.

## 3. Exact infinity-contact statement

The weighted homogenization in
\(\mathbf P(2,3,1)_{[X:Y:T]}\) is
\[
\begin{aligned}
\mathcal H^{\mathrm{wt}}={}&
Y^2-LX^3+c_5XYT+c_4X^2T^2\\
&+c_3YT^3+c_2XT^4+c_0T^6.
\end{aligned}
\tag{14}
\]
All terms have weighted degree six.  With \(t=1/w\), compactify the
boundary parametrization by
\[
X(t)=t^{2r}p(1/t),\qquad
Y(t)=t^{3r}q(1/t),\qquad T(t)=t^r.
\tag{15}
\]
Then exactly
\[
\mathcal H^{\mathrm{wt}}(X(t),Y(t),T(t))
=t^{6r}\mathcal H(p(1/t),q(1/t)).
\tag{16}
\]
Equation (4) proves (5).  Choose \(c_0\) outside the finite set consisting
of the singular values and the at most one value for which the restricted
polynomial vanishes identically.  Then the target is smooth and the
intersection order is finite.

For comparison, in the ordinary projective plane the pullback
intersection order is
\[
9r-\deg_w\mathcal H(p,q)\ge8r-3.
\tag{17}
\]
The extra baseline \(3r\) comes from ordinary homogenization.  Formula
(5), rather than (17), is the contact deficit used in the earlier
weighted cusp-contact memos.

If \(p=A(h),q=B(h)\) with \(\deg h=\delta\), the local parameter \(w^{-1}\)
maps to the normalization parameter with ramification index \(\delta\) at
infinity.  Dividing (16) by this index gives the intrinsic multiplicity.
For \(r=4\), the pullback order is divisible by \(\delta\); combining this
with its lower bound \(17\) gives (6).

The division is not cosmetic.  At the level of polynomial boundary
curves, take
\[
p=w^8,\qquad q=w^{12}+w^4.
\tag{18}
\]
Then \(\delta=4\), and
\[
q^2-p^3-2p^2-p=0.
\tag{19}
\]
After adding a nonzero generic \(c_0\), the pullback of the corresponding
smooth cubic is the nonzero constant \(c_0\).  Its weighted pullback order
at infinity is \(24\), while the intrinsic order on the normalization is
only \(24/4=6\).  This example is not asserted to extend to a full a/b
Jacobian solution; it is an exact warning that parametrized contact cannot
be relabeled as intrinsic curve contact without first controlling
\(\delta\).

## 4. Strategic meaning

This is a genuine strengthening of the radial contact package: a
hypothetical full pair carries a low-degree polynomial
\(\mathcal H(P,Q)\) obtained without coefficient brute force.  On the a/b
boundary it produces a pencil of target elliptic cubics whose pullbacks
have degree at most seven.

It is not yet a contradiction.  Bezout is exactly compatible with the
large contact: in the ordinary plane, a boundary curve of degree
\(3r/\delta\) has total intersection \(9r/\delta\) with a cubic, and
(17) consumes all but at most \((r+3)/\delta\) of it at infinity.  A next
step would need extra control of those few affine intersections, of
\(\delta\), or of how this elliptic pencil interacts with the transverse
fifth-order inertia.
