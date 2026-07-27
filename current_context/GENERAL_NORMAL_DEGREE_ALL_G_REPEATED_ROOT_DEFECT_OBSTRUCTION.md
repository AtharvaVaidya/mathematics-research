# The saturated two-root defect obstruction holds in every degree

Date: 26 July 2026

## Result

Let \(g\geq5\), let \(\ell u\ne0\), and put
\[
d=x^{g-1}(x+\ell),\qquad
p_0=d^2+ux,\qquad q_0=d^3.
\]
In the total-defect Keller complex of
`STANDARD_SYSTEM_REPEATED_ROOT_INTERVENING_DEFECT_OBSTRUCTION.md`,
these top forms have no filtered Keller completion with nonzero
constant Jacobian.

More precisely:

* if
  \[
  \ell^{2g-1}+(g-1)u\ne0,
  \]
  the defect-three cokernel class is nonzero;
* on the exceptional hypersurface
  \[
  u=-\frac{\ell^{2g-1}}{g-1},
  \]
  the defect-four cokernel class is nonzero.

This removes the former restriction \(5\leq g\leq20\) for this
specific two-root top-form family.  It does not say that every
repeated-root endpoint can be put in this form.  In fact the deck
budgets also admit
\[
d_E=x^{g-E}(x^E+\ell),\qquad E\geq2,
\]
so a separate uniform \((g,E)\) obstruction is still required.

## 1. Symbolic defect three

Write
\[
A=p_0'=u+2dd',\qquad B=q_0'=3d^2d'.
\]
Use the bounded Bezout representative
\[
p_1=-\frac{4d'}{3u^2},\qquad
q_1=\frac1u-\frac{2dd'}{u^2}.
\]
The unique defect-two solution is the one displayed in the earlier
note.  The only nontrivial division in it is controlled by
\[
\operatorname{rem}_{d}(d')^3
=\ell^{2g-2}x^{g-1}.
\]

Put \(N=3g-4\), \(T_g=(x+\ell)^2(gx+(g-1)\ell)\), and, for
\(f_3=q_1h_3\), write
\[
f_3=(f_3)_{<N}+x^NS_3.
\]
The new symbolic verifier does not expand a separate polynomial for
each \(g\).  It keeps every term in the compact form
\[
c(g,\ell,u)\frac{x^{ag+b}}{(x+\ell)^p}
\]
and applies the exact Taylor-tail identity
\[
\frac{x^M}{(x+\ell)^p}
-\left[\frac{x^M}{(x+\ell)^p}\right]_{<N}
=x^N\frac{(-1)^L\ell^{-L}P_{p,L}(x/\ell)}
{(x+\ell)^p},
\qquad L=N-M,
\]
where \(P_{p,L}\) has degree \(p-1\).  Its coefficients are
\[
[z^r]P_{p,L}
=\sum_{s=1}^{p-r}(-1)^{s+1}
\binom{L+p-s-1}{p-1}\binom p{r+s}.
\]
This is a polynomial identity in the symbolic integer \(g\).

The three Hermite evaluations are exactly those in equation (23) of
the earlier note.  Solving the quadratic Hermite interpolation gives
\[
\boxed{
[x^{3g-2}]\rho(h_3)
=(-1)^g\frac{64g}{9u^{10}}\ell^{g-3}
\bigl(\ell^{2g-1}+(g-1)u\bigr)^2.
}
\]
Thus defect three excludes every point off the displayed exceptional
hypersurface, for every integer \(g\geq5\).

## 2. Defect four needs only the double-root Hermite jet

Now impose
\[
u=-\frac{\ell^{2g-1}}{g-1}.
\]
The defect-three class vanishes and the unique bounded
\((p_3,q_3)\) exists.  In compact symbolic form its denominators
before cancellation are
\[
\begin{aligned}
\operatorname{den}(p_3)
&=81\ell^{15g-5}x^5(x+\ell)^4
   (g\ell+gx-\ell),\\
\operatorname{den}(q_1h_4)
&=81\ell^{24g-7}x^{15}(x+\ell)^5
   (g\ell+gx-\ell)^2.
\end{aligned}
\]
They exhibit exactly the two Hermite points of \(T_g\).

Write
\[
q_1h_4=(q_1h_4)_{<N}+x^NS_4.
\]
For \(g\geq8\), the affine exponents \(ag+b\) lie in fixed
Taylor-truncation chambers.  A seven-term partial fraction tail
calculation at the double root \(x=-\ell\) gives symbolically
\[
\begin{aligned}
S_4(-\ell)
&=\frac{32(g-1)^{12}(9g^2+41g-25)}
        {81\ell^{20g-8}},\\
S_4'(-\ell)
&=\boxed{
\frac{160g(g-1)^{12}(11g+8)}
     {243\ell^{20g-7}}
}\ne0.
\end{aligned}
\]
The finitely many chamber-boundary degrees \(g=5,6,7\) are checked
by ordinary exact Euclidean division in the pre-existing verifier;
the same derivative formula holds there.

Let
\[
R_4=\operatorname{rem}_{T_g}S_4.
\]
Because \((x+\ell)^2\mid T_g\), Hermite reduction preserves the
double-root jet:
\[
R_4'(-\ell)=S_4'(-\ell)\ne0.
\]
On the other hand, defect-four solvability requires
\[
\deg q_4\leq3g-4=N.
\]
Since
\[
q_4=(q_1h_4)_{<N}+x^NR_4,
\]
this would force \(\deg R_4\leq0\), hence
\(R_4'(-\ell)=0\), a contradiction.

This derivative argument is shorter than reconstructing the two
forbidden monomial coefficients in equation (31).  In particular,
the third Hermite value at
\(-\frac{g-1}{g}\ell\) is not needed for the all-degree exclusion.

## Verification and scope

`GENERAL_NORMAL_DEGREE_SYMBOLIC_REPEATED_ROOT_OBSTRUCTION.py`
proves the defect-three identities with symbolic \(g\), and proves
the two double-root defect-four identities in the stable chamber
\(g\geq8\).  The independent exact verifier
`verify_standard_system_repeated_root_intervening_defect_obstruction.py`
contains the boundary cases \(g=5,6,7\) (as part of its exact
\(5\leq g\leq20\) audit).

The theorem excludes the whole \(E=1\) saturated family in all
degrees.  It is not a global endpoint theorem: the exact next
problem is to carry the same affine-exponent/Hermite-tail method out
for \(d_E=x^{g-E}(x^E+\ell)\), where the chamber structure depends
on both \(g\) and \(E\).
