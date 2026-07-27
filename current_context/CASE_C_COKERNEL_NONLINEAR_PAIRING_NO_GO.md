# Case c: the first nonlinear cokernel pairings are nondegenerate

Date: 25 July 2026

## Audited conclusion

Let \(L_4,L_5\) be the first two case-c radial new-block operators
with two-dimensional complete-row cokernels, and let
\[
E(h)=hV(h)^2-\lambda U(h)^3
\]
be the corrected degree-four outer incidence divisor.

The preceding adjoint audit proves that the two cokernel duals share
exactly the support-top functional
\[
T(F)=[h^{19}]F.
\tag{1}
\]
This note constructs the two remaining adjoint lines canonically,
computes their scaling law, and tests the smallest nonlinear ways of
coupling them.

The result is another sharp no-go:

> **Nonlinear pairing no-go.** In the natural degree-filtered
> normalization, the residual deficit-four and deficit-five adjoints
> define two distinct, nonisotropic lines in the trace-zero part of
> the quartic algebra \(k[h]/(E)\).  Their individual norms, their
> trace-Gram determinant, and the norm of their Wronskian are all
> nonzero on every one of the five certified outer points.
>
> The corresponding weight-nine determinant of the two source
> cokernel vectors is not a universal finite-support identity: it is
> an explicit nonzero polynomial in the seven radial modes.

Thus the first determinant, resultant, norm, and bilinear-pairing
candidates do not supply an incompatibility theorem.  Any successful
nonlinear invariant must use more than the two abstract cokernel planes
and the quartic Frobenius algebra—for example, a new identity involving
later finite-support rows.

## 1. Canonical Frobenius representatives

Put
\[
\mathcal A_5=k[h]/(E^5),\qquad \dim_k\mathcal A_5=20.
\]
Use the Frobenius pairing
\[
\langle F,G\rangle_5
=[h^{19}]\operatorname {rem}_{E^5}(FG).
\tag{2}
\]
It is nondegenerate.  In this pairing the common functional (1) is
represented by \(G=1\).

The annihilator of \(\operatorname {im}L_4\) in \(\mathcal A_5\) has
dimension two.  Exact row reduction has free coefficient positions
\[
\{0,16\}.
\tag{3}
\]
Hence it has a unique basis
\[
1,\quad G_4,
\qquad
\deg G_4=16,\quad [h^{16}]G_4=1,\quad G_4(0)=0.
\tag{4}
\]

For \(L_5\), the annihilator in the ambient \(\mathcal A_5\) has
dimension three, with free positions
\[
\{0,18,19\}.
\tag{5}
\]
One line annihilates the whole bounded row space
\(\langle h,\ldots,h^{19}\rangle\).  The two actual cokernel
functionals may be represented uniquely by
\[
1,\quad G_5,
\qquad
\deg G_5=18,\quad [h^{18}]G_5=1,\quad
G_5(0)=[h^{19}]G_5=0.
\tag{6}
\]

The pivot patterns (3), (5) hold on the two rational and one cubic
good-reduction factors, hence over the characteristic-zero quintic
outer Hurwitz field.

Reduce \(G_4,G_5\) modulo \(E\):
\[
g_4,g_5\in\mathcal A_1:=k[h]/(E).
\tag{7}
\]
Adding the common adjoint \(1\) changes either representative by a
constant.  Remove this ambiguity by trace centering:
\[
x_d=g_d-\frac14\operatorname {Tr}_{\mathcal A_1/k}(g_d),
\qquad d=4,5.
\tag{8}
\]
The resulting lines \(kx_4,kx_5\) in the three-dimensional trace-zero subspace of
\(\mathcal A_1\) are intrinsic to the degree-filtered normalization.

## 2. Scaling weights

Under the outer-coordinate scaling
\[
h\longmapsto ch,
\qquad
U_c(h)=U(ch),\quad V_c(h)=V(ch),
\tag{9}
\]
one has
\[
\lambda_c=c^{-1}\lambda,\qquad
E_c(h)=c^{-1}E(ch).
\tag{10}
\]
The new-block images transform by
\[
F(h)\longmapsto cF(ch).
\tag{11}
\]
The monic degree-filtered adjoints consequently transform as
\[
\boxed{
G_{4,c}(h)=c^{-16}G_4(ch),\qquad
G_{5,c}(h)=c^{-18}G_5(ch).
}
\tag{12}
\]
The companion verifier recomputes both annihilators after the
nontrivial scaling \(c=7\) and checks (12) exactly.

Therefore the basic vanishing invariants have scaling weights
\[
\begin{array}{c|c}
\text{invariant}&c\text{-factor}\\ \hline
N_4=\operatorname {Nm}(x_4)&c^{-64}\\
N_5=\operatorname {Nm}(x_5)&c^{-72}\\
\Delta_{\rm tr}
=\operatorname {Tr}(x_4^2)\operatorname {Tr}(x_5^2)
-\operatorname {Tr}(x_4x_5)^2&c^{-68}\\
\Omega
=\operatorname {Nm}(x_4x_5'-x_4'x_5)&c^{-132}.
\end{array}
\tag{13}
\]
Their numerical values depend on the coordinate normalization, but
their vanishing does not.

The first two norms are, up to nonzero leading-coefficient factors,
the resultants
\[
\operatorname {Res}(E,x_4),\qquad
\operatorname {Res}(E,x_5).
\tag{14}
\]
The trace-Gram determinant is the smallest bilinear degeneracy test
for the two centered lines.  The Wronskian norm tests whether their
ratio becomes stationary at any of the four outer incidence points.
Here derivatives are taken after choosing the unique representatives
of degree below four in \(k[h]/(E)\).

## 3. Exact values: every smallest candidate is a unit

At the good-reduction prime \(32003\), the exact values are
\[
\begin{array}{c|rrrr}
\text{outer factor}&N_4&N_5&\Delta_{\rm tr}&\Omega\\ \hline
t=26839&10393&6360&9117&-3053\\
t=16621&-14442&-6743&-320&10379\\
K_3&
9385-9246t-3198t^2&
12016-9857t+15351t^2&
-2013-13717t+1493t^2&
7562+8638t+10709t^2.
\end{array}
\tag{15}
\]
All entries are nonzero.  Taking the product over the two rational
points and the field norm of the cubic entry gives
\[
\begin{array}{c|rrrr}
&N_4&N_5&\Delta_{\rm tr}&\Omega\\ \hline
\operatorname {Nm}_{\text{outer}/\mathbf F_{32003}}
&11948&9339&15804&4832.
\end{array}
\tag{16}
\]
In particular every value in (16) is a unit.

Thus:

1. neither adjoint symbol vanishes on any outer incidence point;
2. the two centered lines are not trace-isotropic or trace-dependent;
3. their ratio has no forced critical point on \(E=0\); and
4. no norm or resultant vanishing is available.

Good reduction then proves the corresponding characteristic-zero
elements are nonzero.

## 4. The source-vector determinant is not an identity

Let \(S_4,S_5\) be the complete source polynomials at deficits four and
five, after solving all earlier new blocks.  Use the canonical cokernel
coordinates
\[
\begin{aligned}
t_4&=T(S_4),&
r_4&=\langle S_4,G_4\rangle_5,\\
t_5&=T(S_5),&
r_5&=\langle S_5,G_5\rangle_5.
\end{aligned}
\tag{17}
\]
All four are polynomials in the seven radial modes
\[
X_0,\ldots,X_6,\qquad
\operatorname {wt}(X_i)=(1,1,2,2,3,3,4).
\tag{18}
\]
The deficit-four pair has weight four and the deficit-five pair has
weight five.  Hence the smallest determinant candidate
\[
\mathcal D=t_4r_5-r_4t_5
\tag{19}
\]
has weight nine.

Exact reconstruction gives
\[
\begin{array}{c|cccc|c}
\text{factor}&\#t_4&\#r_4&\#t_5&\#r_5&\#\mathcal D\\ \hline
\text{all five points}&3&3&10&32&76,
\end{array}
\tag{20}
\]
where \(\#\) denotes the number of nonzero monomials.  In particular
\(\mathcal D\) is not zero.  The coefficient of
\[
X_0^5X_1^4
\tag{21}
\]
is
\[
\begin{array}{c|c}
\text{factor}&[X_0^5X_1^4]\mathcal D\\ \hline
t=26839&-6846\\
t=16621&14556\\
K_3&7767+11865t-11011t^2.
\end{array}
\tag{22}
\]
Its total outer norm is
\[
-3257\ne0\pmod {32003}.
\tag{23}
\]
Therefore (19) is not a characteristic-zero polynomial identity.

The two deficit-four coordinates are both multiples of the already
known square conormal equation.  Equation (19) merely multiplies that
old condition by a nonzero weight-five expression; it does not create
a new obstruction.

## 5. Invariant-theoretic reason the search stops here

Abstractly, each cokernel dual has the flag
\[
kT\subset kT+kG_d.
\tag{24}
\]
Without the degree-filtered Frobenius normalization, the residual
generator may be changed by
\[
G_d\longmapsto a_dG_d+b_dT,\qquad a_d\ne0,
\tag{25}
\]
independently for \(d=4,5\).  The invariant ring of one vector in each
of the two residual one-dimensional quotients has no canonical
cross-determinant: a comparison requires choosing the relative scales
\(a_4/a_5\).

The construction (2)--(8) is the smallest natural way to make such a
choice.  Its complete list of first degeneracy tests is precisely
(13), together with the source determinant (19).  Equations
(15)--(23) show that none vanishes.

This is a focused no-go, not a proof that every conceivable nonlinear
identity is impossible.  It proves that determinant, resultant, norm,
trace pairing, and Wronskian constructions formed from only the first
two cokernel planes and the corrected quartic cover provide no new
finite-support contradiction.

Any successful continuation must import additional structure:

- a later terminal row giving a canonical multiplication map between
  the two residual lines;
- a nonlinear identity among three or more cokernel stages; or
- a global norm relation not implied by the Frobenius algebra
  \(k[h]/(E^5)\).

Companion verifier:

```text
.venv/bin/python current_context/verify_case_c_cokernel_nonlinear_pairing_no_go.py
```
