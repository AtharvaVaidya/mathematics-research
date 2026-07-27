# Closure of the general mixed linear pivot after second subduction

Date: 25 July 2026

> **Correction.**  The inherited \(B\)-ray boundary-Euler proof is
> superseded because it omits exact seed layers on \(t=u/x\).  The
> \(B/C\) conclusion is repaired by the exact binary first-lower
> double pole, which occurs before the lower \(C\)-sector; the
> independent mixed \(A/B\) forbidden-\(x^1\) argument is unaffected.
> See `WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_CLOSURE.md`.

## Outcome

Let \(F=(A,B,C):\mathbb A^3\to\mathbb A^3\) be the
generic-degree-six Gallagher weighted lift from the degree-five seed,
and let \(U(A,B,C)\) be the second-subduction polynomial constructed
in `WEIGHTED_LIFT_FIRST_NONLINEAR_CUSP_SUBDUCTION.md`.  For every
polynomial graph
\[
z=g(x,y),
\tag{1}
\]
every target-linear form \(L\), and every nonzero target-linear form
\[
V=\alpha A+\beta B+\delta C,
\tag{2}
\]
the restricted pair
\[
\left((U+L)\circ F,\ V\circ F\right)\big|_{z=g}
\tag{3}
\]
does not have nonzero constant Jacobian.

This closes the linear-pivot omission in
`WEIGHTED_LIFT_SECOND_SUBDUCTION_RAY_CLOSURE.md`.  The only apparent
new coupling occurs when \(\alpha\beta\ne0\): the \(A\)-Jacobian is
one ordinary degree above the \(B\)-Jacobian.  The coupled
weighted-Euler equation can nevertheless be solved formally.  On the
only possible \(A\)-ray it forces exactly the same forbidden source
monomial as the pure \(A\)-pivot calculation, with coefficient
\[
\binom{11k+4}{4k},
\tag{4}
\]
independent of the mixing ratio.  Thus the \(B\)-component cannot
repair the \(A\)-ray.

If \(\alpha=0\) and \(\beta\ne0\), the already known \(B\)-ray defect
appears \(m\) degrees below the top, whereas the \(C\)-component can
first enter only \(3m+14\) degrees below it.  Hence that mixture
cannot repair the \(B\)-ray either.  Constant graphs have an immediate
nonzero highest-form obstruction.

This is an all-polynomial-graph theorem for the first coordinate
\(U+L\) and a general linear second coordinate.  It is **not** an
all-nonlinear-target theorem: replacing \(U+L\) or \(V\) by genuinely
new nonlinear target polynomials remains outside the argument.

## 1. The coupled highest-sector equation

Put
\[
u=1+xy,\qquad
\Gamma=1+a\,xy+x^2g(x,y),\qquad a=-\frac{57}{34}.
\tag{5}
\]
Up to nonzero constants, the relevant highest seed sectors are
\[
M=x^{-5}u^{20}\Gamma^{17},\qquad
N_A=x^{-2}u^6\Gamma^4,\qquad
N_B=x^{-1}u^5\Gamma^4.
\tag{6}
\]
As in the preceding ray audit, define
\[
\mathcal L_A=11x\partial_x+7u\partial_u+5,\qquad
\mathcal L_B=5x\partial_x-3u\partial_u-5.
\tag{7}
\]
The exact logarithmic-derivative identities are
\[
\begin{aligned}
J_{x,y}(M,N_A)
 &=\frac{2MN_A}{u\Gamma}\mathcal L_A(\Gamma),\\
J_{x,y}(M,N_B)
 &=\frac{MN_B}{u\Gamma}\mathcal L_B(\Gamma).
\end{aligned}
\tag{8}
\]
Let \(q_6=-5/92\) and \(p_5=-3/46\) be the leading seed
coefficients.  If \(\alpha\ne0\), the simultaneous cancellation of
the highest \(A\)- and \(B\)-sectors is therefore governed by
\[
\boxed{
u\mathcal L_A(\Gamma)+\rho x\mathcal L_B(\Gamma)=0,
\qquad
\rho=\frac{\beta p_5}{2\alpha q_6}.
}
\tag{9}
\]
This is the coupling absent from the pure-pivot note.

For a nonconstant graph of degree \(m\), the three raw Jacobian
degrees are
\[
\begin{aligned}
\deg J(U,A)&=21m+85,\\
\deg J(U,B)&=21m+84,\\
\deg J(U,C)&=18m+70.
\end{aligned}
\tag{10}
\]
Consequently, when \(\alpha\ne0\), the top equation is still the
\(A\)-equation.  Away from the \(A\)-ray it is nonzero and dominates
both other components.

## 2. Exact closure of the mixed \(A/B\) ray

The top \(A\)-equation can vanish only when
\[
m=15k+3,\qquad k\ge1,
\tag{11}
\]
and the leading graph contribution to \(\Gamma\) is
\[
c x^I y^J,\qquad
I=4k+1,\quad J=11k+4.
\tag{12}
\]
Indeed \(11I+5-4J=0\).

Equation (9) has a particularly useful exact characteristic
solution.  Set
\[
r=\frac{5k}{2},\qquad s=\frac{17k}{2}+4,
\qquad r+s=J.
\tag{13}
\]
Then, as a formal Laurent series at source infinity,
\[
\Gamma_{\mathrm{formal}}
=c\,x^{I-J}u^r(u+2\rho x)^s
\tag{14}
\]
solves (9) and starts with \(c x^Iy^J\).  Direct differentiation
gives
\[
\left(u\mathcal L_A+\rho x\mathcal L_B\right)
\left(x^{I-J}u^r(u+2\rho x)^s\right)=0.
\tag{15}
\]
For completeness, this is not a guessed ansatz.  Writing
\(\Gamma=x^I\phi(t)\), \(t=u/x\), reduces (9) to
\[
4t(t+2\rho)\phi'
=\bigl((11I+5)t+5\rho(I-1)\bigr)\phi.
\]
Its normalized solution is
\(\phi=t^r(t+2\rho)^s\), with
\[
r=\frac{5(I-1)}8,\qquad
s=\frac{17I+15}8,
\]
which becomes (13) because \(I=4k+1\).

The exponents in (13) may be half-integral.  That causes no
difficulty: (14) is used only as the unique descending formal
solution of the triangular homogeneous recursion before a lower seed
sector enters.

Now substitute \(u=1+xy\).  To obtain a term with \(x\)-exponent one
from the leading term \(x^Iy^J\), the recursion must replace
\(I-1=4k\) copies of \(xy\) by constant pieces.  If it also uses
\(q>0\) copies of the \(2\rho x\) piece, the resulting \(x\)-exponent
is still one, but its \(y\)-exponent is
\[
J-(I-1)-q=7k+4-q.
\tag{16}
\]
Therefore the **highest-\(y\)** monomial with \(x\)-exponent one,
\(x y^{7k+4}\), necessarily has \(q=0\).  Its coefficient is obtained
by choosing only constant lower pieces in the two factors of (14).
Generalized Vandermonde gives
\[
\sum_{j=0}^{4k}
\binom rj\binom s{4k-j}
=\binom{r+s}{4k}
=\binom{11k+4}{4k}\ne0.
\tag{17}
\]
Thus (9) forces
\[
c\binom{11k+4}{4k}x\,y^{7k+4}.
\tag{18}
\]
Crucially, (18) is independent of \(\rho\).  Terms with \(q>0\)
cannot cancel it because they have lower \(y\)-degree.  It cannot occur in
\(\Gamma=1+a xy+x^2g\): every graph contribution is divisible by
\(x^2\), while the only fixed term with \(x\)-exponent one is \(a
xy\).

The forbidden term occurs at ordinary-degree drop
\[
2(I-1)=8k.
\tag{19}
\]
The first lower seed sector enters only at drop
\[
m+4=15k+7>8k.
\tag{20}
\]
The \(C\)-part is still farther away: by (10) it enters at drop
\(3m+15\) from the \(A\)-top.  Finally, every linear-linear correction
\(J(L,V)\) has degree at most \(8m+33\), whereas the surviving defect
has degree \(21m+85-8k\).  Hence none of the omitted terms can cancel
(18).

This closes every \(\alpha\ne0\) mixed pivot, including
\(\alpha\beta\ne0\).

## 3. The \(B/C\) mixture

Suppose \(\alpha=0\) and \(\beta\ne0\).  The top \(B\)-equation can
vanish only on
\[
m=13k+12,\qquad k\ge0.
\tag{21}
\]
The preceding audit completed its triangular recursion and found the
fixed nonzero \(xy\)-defect at degree
\[
20m+84=(21m+84)-m.
\tag{22}
\]
The \(C\)-Jacobian has degree \(18m+70\), so it lies
\[
(21m+84)-(18m+70)=3m+14>m
\tag{23}
\]
degrees below the \(B\)-top.  It therefore enters strictly after the
defect (22).  Lower seed sectors enter at drop \(m+4\), also too
late, and
\[
(20m+84)-(8m+33)=12m+51>0
\tag{24}
\]
keeps every \(J(L,V)\) correction below the defect.

If \(\alpha=\beta=0\), then \(V\) is a nonzero multiple of \(C\).
The highest form of \(J(U,C)\) is nonzero on every nonconstant graph,
as proved in the first subduction audit.

## 4. Constant graphs

Let \(g=z_0\) be constant and put
\[
h=a y+z_0x,\qquad C_0=x^2h.
\tag{25}
\]
The highest forms are
\[
A_0=q_6y^6C_0^4,\qquad
B_0=p_5y^5C_0^4,\qquad
U_0=\theta x^{32}y^{20}h^{17},
\tag{26}
\]
with \(\theta\ne0\).  Exact differentiation gives
\[
\begin{aligned}
J(U_0,A_0)
 &=6q_6\theta x^{39}y^{25}h^{20}
   (4ay+9z_0x),\\
J(U_0,B_0)
 &=p_5\theta x^{39}y^{24}h^{20}
   (-8ay+5z_0x),\\
J(U_0,C_0)
 &=-6\theta x^{33}y^{19}h^{17}
   (7ay+10z_0x).
\end{aligned}
\tag{27}
\]
Because \(a=-57/34\ne0\), all three forms are nonzero for every
\(z_0\).  Their degrees are respectively \(85,84,70\).  Successive
degree separation selects the \(A\)-, then \(B\)-, then \(C\)-term
according to the first nonzero coefficient in
\((\alpha,\beta,\delta)\).  Linear-linear corrections have degree at
most \(33\), so constant graphs are excluded as well.

## 5. Scope and next boundary

Combining Sections 2--4 proves
\[
\boxed{
J_{x,y}\left(
(U+L)\circ F|_{z=g},\
(\alpha A+\beta B+\delta C)\circ F|_{z=g}
\right)\notin\mathbb C^\times
}
\tag{28}
\]
for every polynomial \(g\), every linear \(L\), and every
\((\alpha,\beta,\delta)\ne(0,0,0)\).

The useful structural point is not merely that another coefficient
search failed.  The one-degree \(A/B\) coupling integrates to the
characteristic form (14), and its first inadmissible source monomial
is protected from the mixing parameter by the exponent of \(x\).
The next honest weighted-lift problem must therefore use a genuinely
nonlinear second target coordinate (or a different nonlinear first
coordinate), not another linear mixture of \(A,B,C\).

The accompanying exact verifier is
`verify_weighted_lift_mixed_linear_pivot_closure.py`.
