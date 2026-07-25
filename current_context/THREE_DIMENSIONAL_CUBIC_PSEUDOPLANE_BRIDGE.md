# The three-dimensional counterexample and a cubic pseudo-plane bridge

Date: 24 July 2026

## 1. Exact two-dimensional fiber

Consider the recently announced Keller map
\[
\begin{aligned}
\mathcal P&=(1+xy)^3z+y^2(1+xy)(4+3xy),\\
\mathcal Q&=y+3x(1+xy)^2z+3xy^2(4+3xy),\\
\mathcal R&=2x-3x^2y-x^3z .
\end{aligned}
\]
It satisfies
\[
\det J(\mathcal P,\mathcal Q,\mathcal R)=-2.
\]

On the fiber \(\mathcal R=c\), put \(t=xy\).  For \(x\ne0\),
\[
z=\frac{2x-3x^2y-c}{x^3}
\]
and the first two coordinates become
\[
\begin{aligned}
P_c(x,t)
&=\frac{(t+1)\bigl(x(t+2)-c(t+1)^2\bigr)}{x^3},\\
Q_c(x,t)
&=\frac{x(4t+6)-3c(t+1)^2}{x^2}.
\end{aligned}
\tag{1}
\]
Their ordinary Jacobian is
\[
\boxed{
\frac{\partial(P_c,Q_c)}{\partial(x,t)}=\frac2{x^4}.
}
\tag{2}
\]
Thus the three-dimensional example contains an exact symplectic
two-dimensional map on \(\mathbf G_m\times\mathbf A^1\).

Putting \(a=x^{-1}\) makes the functions polynomial:
\[
\begin{aligned}
\widehat P_c(a,t)
&=a^2(t+1)(t+2)-ca^3(t+1)^3,\\
\widehat Q_c(a,t)
&=2a(2t+3)-3ca^2(t+1)^2,
\end{aligned}
\tag{3}
\]
but
\[
\boxed{
\frac{\partial(\widehat P_c,\widehat Q_c)}
{\partial(a,t)}=-2a^2.
}
\tag{4}
\]
The puncture can therefore be filled polynomially only at the cost of a
double critical divisor.

For \(c=0\), set \(s=a(2t+3)\).  Then
\[
\widehat P_0=\frac{s^2-a^2}{4},
\qquad
\widehat Q_0=2s.
\tag{5}
\]
This is the elementary quotient \(a\mapsto-a\), restricted to \(a\ne0\).
The two colliding points are explained by the deleted branch divisor, not
by a plane Keller map.

## 2. The uniquely matched cubic pseudo-plane

The power \(x^{-4}\) in (2) selects the smooth cubic pseudo-plane
\[
B_3=
\mathbf C[u,v,w]/(w^3-u-u^2v).
\tag{6}
\]
Give it the Poisson bracket
\[
\boxed{
\{u,w\}=-u^2,\qquad
\{u,v\}=-3w^2,\qquad
\{v,w\}=1+2uv.
}
\tag{7}
\]
The polynomial map
\[
\begin{aligned}
\pi_3:\mathbf A^2&\longrightarrow B_3,\\
u&=a^3,\\
w&=a(1+3a^3b),\\
v&=9b+27a^3b^2+27a^6b^3
\end{aligned}
\tag{8}
\]
satisfies the surface equation.  Moreover, for every \(F,G\in B_3\),
\[
\boxed{
J_{a,b}(F\circ\pi_3,G\circ\pi_3)
=-9\,\{F,G\}_{B_3}.
}
\tag{9}
\]
The map \(\pi_3\) has built-in collisions.  If \(\zeta^3=1\) and
\(\zeta\ne1\), then
\[
(a,b)=(1,0),\qquad
(a,b)=\left(\zeta,\frac{\zeta^{-1}-1}{3}\right)
\tag{10}
\]
have the same image \((u,v,w)=(1,0,1)\).

Consequently:

> If \(F,G\in B_3\) satisfy \(\{F,G\}=1\), then
> \((F\circ\pi_3,G\circ\pi_3)\) is an explicit plane Keller
> counterexample of Jacobian \(-9\), with the exact collision (10).

This is the cubic analogue of the quadratic pseudo-plane route, now
selected directly by the exponent in the three-dimensional example.

## 3. Exact Kummer descent obstruction

On \(B_3[u^{-1}]\), take \(u=x^3,w=t\).  Equation (2) gives
\[
\{P_0,Q_0\}_{B_3}
=-u^2\frac{\partial(P_0,Q_0)}{\partial(u,w)}
=-\frac23.
\tag{11}
\]
So the fiber pair has exactly the right constant Darboux bracket on the
cubic Kummer cover.

It does **not** descend to \(B_3[u^{-1}]\):
\[
P_0=x^{-2}(w+1)(w+2),\qquad
Q_0=2x^{-1}(2w+3).
\tag{12}
\]
Under \(x\mapsto\zeta x\), these have characters \(\zeta\) and
\(\zeta^2\), respectively.  The missing plane counterexample is therefore
an exact regular-descent problem, not another search for a Jacobian
identity.

## 4. Literature correction: the pseudo-plane is classical

The surface (6) is exactly
\[
B_3=S(3,3,1)
\]
in A. Dubouloz and K. Palka,
[*The Jacobian Conjecture fails for pseudo-planes*](https://arxiv.org/abs/1701.01425),
Adv. Math. **339** (2018), 248-284.  Their Theorem C proves much more
than the existence of an isolated self-map: every surface
\[
u(1+u^{\bar r}v)=w^k
\]
with \(k\ge2,\bar r\ge1\) admits arbitrarily large families of nonproper
étale endomorphisms.  Thus neither the cubic pseudo-plane itself nor the
existence of nonproper étale dynamics on it is new.

For \(B_3\), their cyclic degree-three member can be written explicitly.
Choose a primitive cube root \(\varepsilon\), put
\[
t=-uv,\qquad
R_1(t)=1+(\varepsilon-1)t,\qquad
R_0(t)=\frac{R_1(t)^3-1}{t(t-1)},
\]
and define
\[
\eta(u,v,w)=
\bigl(w^3,\ vR_0(t),\ wR_1(t)\bigr).
\tag{13}
\]
The quotient in \(R_0\) is polynomial because
\(\varepsilon^2+\varepsilon+1=0\).  An exact calculation with (7) gives
\[
\{\eta^*u,\eta^*w\}
=c\,\eta^*\{u,w\},\quad
\{\eta^*u,\eta^*v\}
=c\,\eta^*\{u,v\},\quad
\{\eta^*v,\eta^*w\}
=c\,\eta^*\{v,w\},
\tag{14}
\]
where
\[
c=3(1-\varepsilon)\ne0.
\]
This directly verifies the constant symplectic multiplier of the étale
map.

Equation (14) does **not** produce a Darboux pair
\(B_3\to\mathbb A^2\).  It is an endomorphism of \(B_3\), so its three
coordinate functions still satisfy the pseudo-plane relation and the
nonconstant generator brackets.  For example,
\[
\{\eta^*v/c,\eta^*w\}=1+2(\eta^*u)(\eta^*v),
\]
not \(1\).  Pulling back the elementary rational Darboux pair
\((u^{-1},w)\) gives
\[
\left(w^{-3},wR_1(-uv)\right),
\]
which remains nonregular.  The literature therefore supplies a rich
deformation laboratory, but it does not solve the regular descent problem.

There is a second prior-art correction.  M. Miyanishi,
[*Affine pseudo-coverings of algebraic surfaces*](https://www.sciencedirect.com/science/article/pii/S0021869305000657),
J. Algebra **294** (2005), 156--176, and his lecture notes, Section 2.5,
prove that \(\mathbb A^2\) is a Galois affine pseudo-covering of every
affine pseudo-plane with a unique multiple fiber.  Thus the existence type
\[
\mathbb A^2\longrightarrow B_3
\]
of (8) is classical as well.  We have not performed the formula-level
comparison needed to decide whether (8) is conjugate to Miyanishi's
standard construction, so no novelty claim should be made for the filling
itself.

The genuinely narrower contribution of the present bridge is the exact
formula (8) selected by the three-dimensional fiber, together with its
constant Poisson multiplier and its use as a concrete lifting test.  A
regular Darboux pair on \(B_3\), or a compatible lift of a known nonproper
endomorphism through (8), would still convert into a plane Keller
counterexample.

## 5. Strategic target

The new counterexample-first problem is sharply stated:

\[
\boxed{
\text{Find a regular Darboux pair }F,G\in B_3
\text{ with }\{F,G\}=1,
}
\tag{15}
\]
preferably by deforming the Laurent Kummer pair (12) so that its two
characters cancel at \(u=0\).

This bridge is structurally different from the bounded
\((72,108)\) exclusion.  It imports the mechanism of the
three-dimensional counterexample, preserves built-in noninjectivity, and
reduces the plane problem to regularity of a canonical pair on one explicit
smooth surface.  It is not yet a counterexample: the descent in (15) is the
entire unresolved step.
