# Two-end Hamiltonian geometry of the seven radial modes

Date: 24 July 2026

## 1. Exact \(k=1\) split

For the normalized \(k=1\) outer point,
\[
\begin{aligned}
U&=1+w+\frac6{25}w^2+\frac9{250}w^3,\\
V&=1+\frac23w+\frac6{25}w^2+\frac{36}{875}w^3
  +\frac{18}{4375}w^4.
\end{aligned}
\]
The outer pair
\[
P_0=\frac{z^2U}{w},\qquad Q_0=\frac{z^3V}{w}
\]
has
\[
\Omega=dP_0\wedge dQ_0=\frac{z^4}{w^3}\,dz\wedge dw.
\tag{1}
\]
For a deficit-\(d\) kernel polynomial \(C\), put \(c=5-d\) and
\[
H_{d,C}=-\frac{z^cC(w)}{cw}.
\tag{2}
\]

The seven classes split canonically by their endpoint construction.
The three low classes are
\[
(d,C)=(1,1),(2,w),(3,w),
\tag{3}
\]
with potentials
\[
-\frac{z^4}{4w},\qquad-\frac{z^3}{3},\qquad-\frac{z^2}{2}.
\]
The four high classes are
\[
\begin{array}{c|l}
d&C_d^+(w)\\ \hline
1&
w^5+\frac{40}{3}w^4+100w^3+\frac{11500}{27}w^2
 +\frac{92500}{81}w,\\[1mm]
2&
\frac{18}{4375}w^4+\frac{36}{875}w^3+\frac6{25}w^2,\\[1mm]
3&
\frac9{250}w^3+\frac6{25}w^2,\\[1mm]
4&w^2.
\end{array}
\tag{4}
\]
For a Laurent potential, record the pair
\[
\bigl(\operatorname {ord}_{w=0}H,\operatorname {ord}_{w=\infty}H\bigr).
\]
The low pairs are
\[
(-1,1),(0,0),(0,0),
\tag{5}
\]
whereas the high pairs are
\[
(0,-4),(1,-3),(1,-2),(1,-1).
\tag{6}
\]
Thus (3)--(4) are genuinely opposite endpoint lattices: the low modes are
bounded at infinity and contain the unique pole at zero, while the high
modes are regular at zero and carry all positive pole orders at infinity.

## 2. Why the split is not two independent unipotent subgroups

The scalar Hamiltonian bracket is
\[
C\star D
=-(5-d-e)w\left(
\frac{(wC'-C)D}{5-d}
+\frac{C(D-wD')}{5-e}
\right).
\tag{7}
\]
It gives
\[
[H_{1,1},H_{2,w}]=H_{3,w^2/2},
\qquad
[H_{1,1},H_{3,w}]=H_{4,w^2/4},
\qquad
[H_{2,w},H_{3,w}]=0.
\tag{8}
\]
The second commutator is one quarter of the high \(d=4\) mode in (4).
The first is already outside the three-dimensional low space.
Consequently the \(3+4\) split cannot literally be the Lie algebras of
two independent opposite unipotent subgroups.  It is a split of the
tangent/associated-graded lattice; taking Lie closure mixes the ends and
creates precisely the support-escape terms measured by the nonlinear
equations.

This is useful structurally.  A parahoric formulation must place the
seven classes in graded quotients of two larger endpoint Lie lattices,
not declare the low and high spans themselves to be parahoric radicals.

## 3. Coarse opposite parahorics have a nontrivial rational intersection

There is an exact family of rational symplectic countermodels.  Put
\[
r=\frac{z^5}{w^2}
\]
and let \(g(r)\) be any nonzero rational function.  Define
\[
T_g(z,w)=\bigl(zg(r)^2,\;wg(r)^5\bigr).
\tag{9}
\]
Then \(r\circ T_g=r\), \(T_{g^{-1}}\) is the rational inverse, and
\[
T_g^*\Omega=\Omega.
\tag{10}
\]
One transparent proof uses the canonical coordinates
\[
q=\frac{z^5}{5},\qquad p=-\frac1{2w^2},
\qquad \Omega=dq\wedge dp.
\]
Here \(r=-10qp\), and (9) becomes
\[
q\longmapsto qg(r)^{10},\qquad
p\longmapsto p\,g(r)^{-10}.
\]
It fixes \(qp\), so it preserves \(dq\wedge dp\).

Choose, for example,
\[
g(r)=\frac{r^2+ar+1}{r^2+br+1},
\qquad a\ne b.
\tag{11}
\]
At the two ends,
\[
\begin{aligned}
g(r)&=1+(a-b)r+O(r^2)&& (r\to0,\;w\to\infty),\\
g(r)&=1+(a-b)r^{-1}+O(r^{-2})
 &&(r\to\infty,\;w\to0).
\end{aligned}
\tag{12}
\]
Thus \(T_g\) is tangent to the identity at both \(w\)-ends.  It belongs
to the intersection of the two coarse formal symplectic congruence
groups, yet it is nontrivial.  Its zero and pole curves
\[
r^2+ar+1=0,\qquad r^2+br+1=0
\]
lie in the interior torus.  Pulling back the \(k=1\) outer pair gives
\[
\widetilde P=P_0\circ T_g,\qquad
\widetilde Q=Q_0\circ T_g,\qquad
d\widetilde P\wedge d\widetilde Q=\Omega.
\tag{13}
\]
These are exact rational symplectic deformations, indistinguishable from
the identity to the first formal order at both ends, but they leave the
bounded polynomial Newton support through their interior denominators.

Therefore a two-end Birkhoff or parahoric argument cannot force identity
from endpoint regularity alone.  It must use the absence of interior
zero/pole divisors—equivalently, the global polynomial support condition.

There is nevertheless an exact positive theorem inside this countermodel
family.  The pullbacks have the forms
\[
\begin{aligned}
P_0\circ T_g
&=\frac{z^2}{w}\left(
g^{-1}+wg^4+\frac6{25}w^2g^9+\frac9{250}w^3g^{14}
\right),\\
Q_0\circ T_g
&=\frac{z^3}{w}\left(
g+\frac23wg^6+\frac6{25}w^2g^{11}
+\frac{36}{875}w^3g^{16}+\frac{18}{4375}w^4g^{21}
\right).
\end{aligned}
\tag{13a}
\]
At a finite interior zero of \(g\), the unique \(g^{-1}\) term gives a
pole of \(P_0\circ T_g\).  At a finite interior pole of \(g\), the unique
top \(g^{21}\) term gives a pole of \(Q_0\circ T_g\).  Hence regularity
on the torus forces \(g\) to have no interior zero or pole:
\[
g=\lambda r^n.
\tag{13b}
\]
Identity jets at both ends force \(n=0\) and \(\lambda=1\).  Thus the
intersection is trivial once the no-interior-divisor condition is imposed,
at least in this entire rational centralizer.

This family is not ad hoc.  In the canonical coordinates
\((q,p)\), every symplectic birational map in the identity component that
fixes \(s=qp\) has
\[
q\mapsto qh(s),\qquad p\mapsto p/h(s).
\]
For it to lift rationally through \(q=z^5/5\) and
\(p=-1/(2w^2)\), the function \(h\) must be both a fifth power and a
square in \(\mathbf C(s)\), hence \(h=g^{10}\).  This recovers exactly
(9).  Therefore (13a)--(13b) close the full identity component of the
rational symplectic centralizer of \(r\), not just the example (11).

The first support escape of (11) is also geometrically meaningful.  Near
\(w=0\), write
\[
g(r)=1+\kappa r^{-1}+O(r^{-2}).
\]
Its infinitesimal vector field begins with
\[
\delta z=2\kappa\frac{w^2}{z^4},\qquad
\delta w=5\kappa\frac{w^3}{z^5}.
\tag{13c}
\]
Up to sign, this is the Hamiltonian vector field of
\(\kappa\log r\).  It has the exponent pattern \(d=5,C=w\), precisely
the first resonant deficit where (2) has \(c=5-d=0\) and the bounded
kernel vanishes.  Thus the stable cutoff at \(d=5\) removes the
logarithmic centralizer direction created by a hidden interior divisor.

## 4. What a compactified log-surface theorem can prove

On \(\mathbf P^1_z\times\mathbf P^1_w\),
\[
\operatorname {div}(\Omega)
=4Z_0-6Z_\infty-3W_0+W_\infty.
\tag{14}
\]
The four coefficients are distinct.  Hence every regular automorphism of
the compactified surface preserving \(\Omega\) fixes all four boundary
components individually.  It must have the form
\[
z\longmapsto\alpha z,\qquad w\longmapsto\beta w,
\qquad \alpha^5=\beta^2.
\tag{15}
\]
Over an algebraically closed field this is the one-dimensional torus
\[
(\alpha,\beta)=(s^2,s^5).
\tag{16}
\]
After fixing the outer normalization, this residual Levi torus is the
identity.  Thus the desired “opposite intersection is trivial” statement
is true for globally regular automorphisms of this fixed compactification,
modulo the explicit scaling Levi.

The rational maps (9) show exactly why this theorem does not yet solve the
radial problem: formal Hamiltonian gauge transformations need not extend
regularly across the interior.  Proving that all 19 bounded support
conditions remove those interior divisors is essentially the missing
nonlinear theorem, not a consequence of Birkhoff factorization.

## 5. Consequence for the research route

The useful geometric reformulation is now:

> The 19 compatibility rows should be interpreted as a no-interior-divisor
> criterion upgrading a two-end formal symplectomorphism to a regular
> automorphism of the compactified log surface.

If that upgrade is proved, (14)--(16) finish the argument after
normalization.  Without it, (9)--(13) give an infinite-dimensional family
of exact rational countermodels.  The next productive target is therefore
an algebraic divisor theorem for the finite support escape, not a more
abstract opposite-parahoric intersection theorem and not another
coefficient Gröbner expansion.

The formulas in this memo are checked in
`route_bd_radial_parahoric_geometry.py`.
