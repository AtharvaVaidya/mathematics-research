# Known pseudo-plane étale maps do not lift through the plane filling

Date: 24 July 2026

## Exact conclusion

Let
\[
B_3=\{u(1+uv)=w^3\}=S(3,3,1)
\]
and use the explicit affine pseudo-covering
\[
\pi_3(a,b)=
\left(
a^3,\,
9b+27a^3b^2+27a^6b^3,\,
a(1+3a^3b)
\right).
\tag{1}
\]
Every nonproper \(\mathbf C^*\)-equivariant étale endomorphism of \(B_3\)
classified by Dubouloz--Palka fails to lift polynomially through (1).
The same is true after every standard \(\Theta^P\) deformation used in
their arbitrarily-dimensional families.

This is not a bounded coefficient calculation.  One Shabat branch is
excluded by a degree inequality and the other by incompatible values on
three cube-root components.

## 1. Lifting criterion

Put
\[
h=1+3a^3b.
\]
Then
\[
u=a^3,\qquad w=ah,\qquad
v=\frac{h^3-1}{a^3},\qquad t=-uv=1-h^3.
\tag{2}
\]
For an endomorphism \(\eta:B_3\to B_3\), a polynomial map
\[
H=(A,B):\mathbb A^2\to\mathbb A^2
\]
satisfies
\[
\pi_3\circ H=\eta\circ\pi_3
\tag{3}
\]
if and only if
\[
\boxed{
A^3=\pi_3^*(\eta^*u),\qquad
\frac{\pi_3^*(\eta^*w)}A=1+3A^3B.
}
\tag{4}
\]
Equality of the \(v\)-coordinates then follows from the surface equation.
Thus, after selecting the cube root \(A\), the exact regularity test is
\[
\boxed{
\frac{\pi_3^*(\eta^*w)}A\equiv1\pmod{A^3}.
}
\tag{5}
\]
The other cube-root choices differ by constants in \(\mu_3\); restriction
to \(a=0\) forces the choice used below.

If a nonproper étale \(\eta\) of degree \(d>1\) satisfied (3), then \(H\)
would be a plane Keller counterexample.  The multiplier pulled back to
\(\mathbb A^2\) is a polynomial unit, hence constant, so the symplectic
identity for \(\pi_3\) gives \(J(H)\in\mathbf C^*\).  Generic degrees in
(3) give \(\deg H=\deg\eta=d>1\).

## 2. Shabat data

In the notation of A. Dubouloz and K. Palka,
[*The Jacobian Conjecture fails for pseudo-planes*](https://arxiv.org/abs/1701.01425),
Adv. Math. **339** (2018), 248--284, every
\(\mathbf C^*\)-equivariant étale endomorphism of \(S(3,3,1)\) has
\(\alpha\in\{0,1\}\), \(\lambda\ne0\), and polynomials \(R_i\) satisfying
\[
t(1-t)^{1-\alpha}R_0R_2^3
=1-(1-t)^\alpha R_1^3,
\tag{6}
\]
\[
R_1(0)=R_2(0)=1,\qquad
(1-t)R_0R_1R_2\text{ squarefree},
\tag{7}
\]
and
\[
\eta^*u=u(1-t)^{1-\alpha}\lambda^3R_2^3,\qquad
\eta^*w=\lambda wR_1R_2.
\tag{8}
\]
Writing \(N=\deg R_2\), the degree ledger is
\[
\begin{array}{c|c|c}
\alpha&\deg\eta&\deg R_1\\ \hline
0&6N+3&2N+1\\
1&6N+1&2N.
\end{array}
\tag{9}
\]
For \(\alpha=1,N=0\), the map has degree one.  All other cases are
nonproper.

## 3. The \(\alpha=0\) obstruction

Equations (2), (5), and (8) force
\[
A=\lambda ahR_2(t),\qquad
\frac{\pi_3^*(\eta^*w)}A=R_1(t).
\]
Consequently a lift requires
\[
\boxed{
t(1-t)R_2(t)^3\mid R_1(t)-1.
}
\tag{10}
\]
The factor \(t\) is the order-three vanishing along \(a=0\), while
\(1-t=h^3\).  But
\[
\deg\bigl(t(1-t)R_2^3\bigr)=3N+2
>2N+1\ge\deg(R_1-1).
\]
No \(\alpha=0\) member lifts.

For the cyclic degree-three map, choose a primitive cube root
\(\varepsilon\) and \(R_1=1+(\varepsilon-1)t\).  The attempted second
plane coordinate is
\[
B=-(\varepsilon-1)b\,\frac{h^2+h+1}{h^3},
\]
which displays the uncancelled pole on \(h=0\).

## 4. The \(\alpha=1\) obstruction

Here
\[
A=\lambda aR_2(t),\qquad
\frac{\pi_3^*(\eta^*w)}A=hR_1(t).
\tag{11}
\]
If \(N\ge1\), let \(\beta\) be a root of the squarefree \(R_2\).
Equation \(t=1-h^3=\beta\) has three distinct components
\[
h=h_j,\qquad h_j^3=1-\beta.
\]
Divisibility in (5) by \(R_2^3\) would require
\[
h_jR_1(\beta)=1
\]
on all three components, which is impossible for three distinct \(h_j\).
Indeed (6) says these three products range through the cube roots of
unity.  The remaining \(N=0\) case has degree one.

## 5. Deformations preserve the obstruction

Dubouloz--Palka use automorphisms of the universal cover of the form
\[
\Theta^P(x,y,z)=
\left(
x,\,
y+x^{-3}\bigl((z+P(x)x^3)^3-z^3\bigr),\,
z+P(x)x^3
\right).
\]
After descent, the ratio in (5) changes only by
\[
\frac{\pi_3^*(\eta^*w)}A
\longmapsto
\frac{\pi_3^*(\eta^*w)}A+P(A)A^3.
\]
Its residue modulo \(A^3\) is unchanged.  Hence none of these deformations
lifts either.

## Prior-art boundary

M. Miyanishi,
[*Affine pseudo-coverings of algebraic surfaces*](https://www.sciencedirect.com/science/article/pii/S0021869305000657),
J. Algebra **294** (2005), 156--176, proves at the existence level that
\(\mathbb A^2\) is a Galois affine pseudo-covering of every affine
pseudo-plane with a unique multiple fiber.  Thus neither the surface
\(B_3\), its nonproper étale endomorphisms, nor the existence type
\(\mathbb A^2\to B_3\) is new.  Formula-level equivalence of (1) with
Miyanishi's standard construction has not been checked.

The sharp new candidate is narrower: the particular filling selected by
the three-dimensional fiber gives the exact congruence (5), and (10)--(11)
exclude the whole known Shabat/deformation architecture from producing a
plane counterexample through that filling.
