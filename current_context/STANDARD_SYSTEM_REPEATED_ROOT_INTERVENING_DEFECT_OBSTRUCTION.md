# Intervening homogeneous equations exclude the saturated \((2,3)\) deck countermodels

Date: 26 July 2026

## Outcome

The degree/divisor countermodel from
`STANDARD_SYSTEM_REPEATED_ROOT_GLOBAL_DECK_BUDGET_COUNTERMODEL.md`
does not survive the intervening homogeneous Keller equations, even
after arbitrary reciprocal-compatible coefficients are added.

The precise statement is stronger than the failure of the displayed
sparse pair.  Let \(5\le g\le20\), and let
\(P,Q\in\mathbf C[X,\tau]\) satisfy the reciprocal degree caps for
\[
n=2g,\qquad m=3g,
\]
and suppose their highest ordinary homogeneous forms dehomogenize to
\[
\boxed{
p_0(x)=d(x)^2+ux,\qquad q_0(x)=d(x)^3,
\qquad
d(x)=x^{g-1}(x+\ell),\quad u\ell\ne0.
}
\tag{1}
\]
Then \(P,Q\) cannot satisfy the homogenized Keller identity with
nonzero right side.

More exactly:

* if \(\ell^{2g-1}+(g-1)u\ne0\), the intrinsic defect-three
  obstruction is nonzero; and
* if \(\ell^{2g-1}+(g-1)u=0\), defect three vanishes but the
  defect-four obstruction is nonzero.

Thus every member of (1) is excluded by defect at most four.  This is
an all-lower-coefficient theorem: it does not assume that the
coefficients between the common first face and the affine endpoint
vanish.

For \(g=5\), the nonsaturated limit \(\ell=0\) is also excluded:
defects three and four vanish, but defect five is nonzero.  Hence the
degree-\((10,15)\) theorem remains valid for every \(\ell\), provided
\(u\ne0\).

For the saturated two-root countermodel
\[
a=2,\quad b=3,\quad
R=X^2(X-1)^3,\quad
L=X(X-1)^2(X-2),
\tag{2}
\]
the leading coefficient of \(L\) is \(\ell=1\), and the endpoint
\(\tau^9(X-\beta)\) has \(u=1\).  Its defect-three scalar is
\[
\boxed{-\frac{8000}{9}\ne0.}
\tag{3}
\]
Consequently no choice of the omitted intermediate coefficients can
complete that support countermodel to a Keller pair.

## 1. The total-defect complex

For affine polynomials \(F,G\) of degrees \(n,m\), put
\[
P(X,\tau)=\tau^nF(X/\tau,1/\tau),\qquad
Q(X,\tau)=\tau^mG(X/\tau,1/\tau).
\]
The reciprocal Keller operator is
\[
\mathscr K_X(P,Q)
=\tau(P_XQ_\tau-P_\tau Q_X)+nPQ_X-mQP_X.
\]
If \(x=X/\tau,\ y=1/\tau\), then
\[
\begin{aligned}
P_X&=\tau^{n-1}F_x,&
P_\tau&=n\tau^{n-1}F-\tau^{n-2}(XF_x+F_y),\\
Q_X&=\tau^{m-1}G_x,&
Q_\tau&=m\tau^{m-1}G-\tau^{m-2}(XG_x+G_y).
\end{aligned}
\]
Substitution cancels the Euler terms and gives the exact identity
\[
\boxed{
\mathscr K_X(P,Q)
=-\tau^{n+m-2}J(F,G)(X/\tau,1/\tau).
}
\]
Thus a constant Jacobian \(J(F,G)=J\ne0\) is equivalent to the
reciprocal identity
\[
\mathscr K_X(P,Q)=-J\tau^{n+m-2}.
\]

Write the ordinary homogeneous decompositions as
\[
\begin{aligned}
P(X,\tau)
 &=\sum_{r=0}^{2g}\tau^{2g-r}p_r(X/\tau),\\
Q(X,\tau)
 &=\sum_{s=0}^{3g}\tau^{3g-s}q_s(X/\tau).
\end{aligned}
\tag{4}
\]
Thus
\[
\deg p_r\le 2g-r,\qquad
\deg q_s\le 3g-s.
\tag{5}
\]
The homogeneous Keller equations are
\[
\sum_{r+s=k}
\left(rp_rq_s'-sq_sp_r'\right)
=
\begin{cases}
-J,&k=1,\\
0,&k\ne1.
\end{cases}
\tag{6}
\]
One may take \(J=1\) without changing \(p_0,q_0\) or the degree
filtration.  Algebraically, replace
\[
p_r\longmapsto J^{-r}p_r,\qquad
q_r\longmapsto J^{-r}q_r.
\tag{7}
\]
Every defect-\(k\) left side is multiplied by \(J^{-k}\), so the
defect-one right side becomes \(-1\) and every homogeneous zero
equation remains zero.  Equivalently, this is rescaling the formal
defect-bookkeeping variable while leaving its zero-jet fixed.

Put
\[
A=p_0',\qquad B=q_0'.
\tag{8}
\]
The first equation is the bounded Bezout identity
\[
Aq_1-Bp_1=1.
\tag{9}
\]
For \(k\ge2\), define
\[
H_k=
\sum_{\substack{i+j=k\\i,j\ge1}}
\left(jp_i'q_j-ip_iq_j'\right).
\tag{10}
\]
Then the new coefficient equation is
\[
\boxed{
Aq_k-Bp_k=-\frac{H_k}{k}.
}
\tag{11}
\]

For \(2\le k\le2g\), the linear differential in (11) is
\[
T_k:
\mathbf C[x]_{\le3g-k}\oplus
\mathbf C[x]_{\le2g-k}
\longrightarrow
\mathbf C[x]_{\le5g-k-1},
\qquad
T_k(q,p)=Aq-Bp.
\tag{12}
\]
Since \(\gcd(A,B)=1\), \(T_k\) is injective and has cokernel dimension
\(k-2\).  Indeed, \(Aq=Bp\) forces
\[
q=Bs,\qquad p=As
\]
for some polynomial \(s\).  But
\[
\deg q\le3g-k<3g-1=\deg B
\]
when \(k\ge2\), so \(s=0\).  Finally, the target and source
dimensions are respectively
\[
5g-k,\qquad
(3g-k+1)+(2g-k+1)=5g-2k+2,
\]
whose difference is \(k-2\).  If
\[
\rho(h)=\operatorname{rem}_{B}(A^{-1}h),
\tag{13}
\]
then
\[
h\in\operatorname{im}T_k
\quad\Longleftrightarrow\quad
\deg\rho(h)\le3g-k.
\tag{14}
\]
Equations (12)--(14) are the finite cohomological formulation of the
intervening coefficient problem.  The obstruction at defect \(k\)
is the class of \(-H_k/k\) in \(\operatorname{coker}T_k\), represented
by the coefficients of
\[
x^{3g-k+1},\ldots,x^{3g-2}
\tag{15}
\]
in its modular remainder.

At defect two the cokernel is zero, so the equation is always
uniquely solvable.  Defect three is the first equation which can
carry a genuine obstruction.

## 2. Gauge normalization

All bounded solutions of (9) differ by
\[
(p_1,q_1)\longmapsto(p_1+\lambda A,q_1+\lambda B),
\qquad \lambda\in\mathbf C.
\tag{16}
\]
This is precisely the change induced by the degree-preserving source
shear:
\[
(x,t)\longmapsto(x+\lambda t,t),
\tag{17}
\]
where
\[
p(t,x)=\sum_rt^rp_r(x),\qquad
q(t,x)=\sum_rt^rq_r(x)
\]
are the total-defect bookkeeping series.  Here \(t\) is the
dehomogenized defect variable, not the repeated-root Rees coordinate
\(\tau\).  Expanding \(p(t,x+\lambda t)\) gives
\(p_1\mapsto p_1+\lambda p_0'\), and likewise for \(q_1\).
The affine shear has determinant one and preserves every degree
bound.  It may change a chosen Rees presentation, but the present
top-form theorem asks whether any filtered completion exists, so this
gauge change loses no relevant information.  Hence existence of a
filtered extension is unchanged if one fixes
any one bounded Bezout representative.  Once that representative is
fixed, every later coefficient is unique whenever its obstruction
vanishes, because every \(T_k\) in the displayed range is injective.
It is therefore enough to compute the obstruction sequence for one
convenient representative.

For (1), exact Euclidean reduction gives
\[
\begin{aligned}
p_1&=-\frac{4d'}{3u^2},\\
q_1&=\frac1u-\frac{2dd'}{u^2},
\end{aligned}
\tag{18}
\]
and one checks directly that \(Aq_1-Bp_1=1\).  Both polynomials lie
well inside their degree bounds.

## 3. The first obstruction and its exceptional locus

For each integer \(5\le g\le20\), put
\[
r_g=\operatorname{rem}_{d}(d')^3.
\]
Because
\[
d=x^{g-1}(x+\ell),
\qquad
d'=x^{g-2}(gx+(g-1)\ell),
\]
division by \(x+\ell\) gives the exact identity
\[
\boxed{r_g=\ell^{2g-2}x^{g-1}.}
\tag{19}
\]
The inverse of \(A=u+2dd'\) modulo
\(B=3d^2d'\) is exactly \(q_1\), since \((dd')^2\) is divisible by
\(B\).  The defect-two source and its unique bounded solution are
\[
\begin{aligned}
-\frac{H_2}{2}
 &=\frac{2d''}{3u^3}+\frac{4(d')^3}{3u^4},\\
q_2
 &=\frac{2d''}{3u^4}+\frac{4(d')^3}{3u^5}
   -\frac{4dd'd''}{3u^5}-\frac{8dd'r_g}{3u^6},\\
p_2
 &=\frac{8}{9u^5}
 \left(\frac{(d')^3-r_g}{d}-d'd''
       -\frac{2d'r_g}{u}\right).
\end{aligned}
\tag{20}
\]
The quotient in the last line is polynomial by the definition of
\(r_g\).  Direct substitution proves
\(Aq_2-Bp_2=-H_2/2\), and the displayed degrees are at most
\(3g-2\) and \(2g-2\), respectively.

Let \((p_2,q_2)\) be the unique bounded solution at defect two, form
\[
H_3=
2p_1'q_2-p_1q_2'
+p_2'q_1-2p_2q_1',
\tag{21}
\]
and put \(h_3=-H_3/3\).  The following cubic-tail calculation reduces
its modular remainder to three exact scalar evaluations.  The
verifier performs these quotient/remainder calculations separately
over \(\mathbf Q(\ell,u)\) for every integer \(5\le g\le20\).

Indeed,
\[
B=3x^N T_g,\qquad
N=3g-4,\qquad
T_g=(x+\ell)^2(gx+(g-1)\ell).
\]
For \(f_k=q_1h_k\), split
\[
f_k=(f_k)_{<N}+x^NS_k.
\]
Because \(q_1=A^{-1}\pmod B\), the part of
\(\rho(h_k)=\operatorname{rem}_B(f_k)\) in degrees
\(N,N+1,N+2\) is
\[
x^NR_k,\qquad R_k=\operatorname{rem}_{T_g}S_k.
\]
The quadratic \(R_k\) is determined by the Hermite data
\[
R_k(-\ell)=S_k(-\ell),\qquad
R_k'(-\ell)=S_k'(-\ell),\qquad
R_k\!\left(-\frac{g-1}{g}\ell\right)
=S_k\!\left(-\frac{g-1}{g}\ell\right).
\tag{22}
\]

For defect three, set \(E=\ell^{2g-1}\) and
\[
C_g=(-1)^g\frac{32}{27u^{10}}.
\]
Substitution of (18)--(21), followed only by (19), gives
\[
\begin{aligned}
S_3(-\ell)
 &=C_g\ell^{g-1}u\bigl(3E+(6g-4)u\bigr),\\
S_3'(-\ell)
 &=C_g\ell^{g-2}
 \bigl(-6E^2+(-15g+12)Eu
       +(-10g^2+16g-6)u^2\bigr),\\
S_3\!\left(-\frac{g-1}{g}\ell\right)
 &=2gC_g\ell^{g-1}u^2.
\end{aligned}
\tag{23}
\]
Solving the three scalar equations (22), one obtains
\[
R_3=c_{30}+c_{31}x+c_{32}x^2,
\]
where
\[
\begin{aligned}
c_{30}
 &=C_g\ell^{g-1}\bigl(
 6(g-1)E^2+3(g-1)(4g-5)Eu\\
 &\hspace{42mm}
 +2(3g^3-11g^2+14g-5)u^2\bigr),\\
c_{31}
 &=C_g\ell^{g-2}\bigl(
 6(2g-1)E^2+3(8g^2-13g+4)Eu\\
 &\hspace{42mm}
 +2(g-1)(2g-3)(3g-1)u^2\bigr),\\
c_{32}
 &=6gC_g\ell^{g-3}\bigl(E+(g-1)u\bigr)^2.
\end{aligned}
\tag{24}
\]
The permitted degree at defect three is \(3g-3=N+1\).
Consequently the unique forbidden coefficient is
\[
\boxed{
\left[x^{3g-2}\right]\rho\!\left(-\frac{H_3}{3}\right)
=
(-1)^g\frac{64g}{9u^{10}}\,
\ell^{g-3}
\left(\ell^{2g-1}+(g-1)u\right)^2.
}
\tag{25}
\]
This proves the theorem unless
\[
\ell^{2g-1}+(g-1)u=0.
\tag{26}
\]
In particular, (25) gives (3) at \((g,\ell,u)=(5,1,1)\).

Assume next that \(u=-\ell^{2g-1}/(g-1)\).  Defect three is
then solvable.  Its unique bounded solution is certified without any
choice by
\[
q_3=\operatorname{rem}_B(q_1h_3),\qquad
p_3=\frac{Aq_3-h_3}{B}.
\tag{27}
\]
Because \(Aq_1\equiv1\pmod B\), the remainder definition gives
\[
Aq_3\equiv Aq_1h_3\equiv h_3\pmod B.
\]
Hence the displayed \(p_3\) is a polynomial.  Moreover,
Equation (24) has \(c_{32}=0\) on this branch, so
\(\deg q_3\le3g-3\); equation (11) then gives
\[
\deg p_3
\le\max\{\deg(Aq_3),\deg h_3\}-\deg B
\le(5g-4)-(3g-1)=2g-3.
\]
Thus (27) is exactly the unique bounded defect-three solution.  Form
\[
H_4=
3p_1'q_3-p_1q_3'
+2p_2'q_2-2p_2q_2'
+p_3'q_1-3p_3q_1',
\qquad h_4=-\frac{H_4}{4}.
\tag{28}
\]

For \(f_4=q_1h_4=(f_4)_{<N}+x^NS_4\), exact substitution in
(27)--(28) gives, for each \(5\le g\le20\),
\[
\begin{aligned}
S_4(-\ell)
 &=\frac{32(g-1)^{12}(9g^2+41g-25)}
         {81\ell^{20g-8}},\\
S_4'(-\ell)
 &=\frac{160g(g-1)^{12}(11g+8)}
         {243\ell^{20g-7}},\\
S_4\!\left(-\frac{g-1}{g}\ell\right)
 &=\frac{32g(g-1)^{12}(3g+7)}
         {27\ell^{20g-8}}.
\end{aligned}
\tag{29}
\]
Solving (22) now gives
\[
\begin{aligned}
[x^N]\rho(h_4)
 &=-\frac{32(g-1)^{12}
 (115g^3-117g^2-163g+75)}
 {243\ell^{20g-8}},\\
[x^{N+1}]\rho(h_4)
 &=-\frac{160g(g-1)^{12}(46g^2-25g-8)}
          {243\ell^{20g-7}},\\
[x^{N+2}]\rho(h_4)
 &=-\frac{160g^2(g-1)^{12}(23g-7)}
          {243\ell^{20g-6}}.
\end{aligned}
\tag{30}
\]
At defect four the permitted modular degree is at most \(3g-4\), while
the two forbidden coefficients are
\[
\boxed{
\begin{aligned}
\left[x^{3g-3}\right]\rho\!\left(-\frac{H_4}{4}\right)
 &=-\frac{160g(g-1)^{12}(46g^2-25g-8)}
          {243\ell^{20g-7}},\\
\left[x^{3g-2}\right]\rho\!\left(-\frac{H_4}{4}\right)
 &=-\frac{160g^2(g-1)^{12}(23g-7)}
          {243\ell^{20g-6}}.
\end{aligned}}
\tag{31}
\]
Both are nonzero for \(5\le g\le20\).  These formulas follow from one
further application of (13) after substituting (26); no root or
genericity assumption remains.

For completeness, specialize now to \(g=5,\ell=0\).  The bounded
equations through defect four are solvable.  At defect five the
permitted modular degree is at most \(10\), and
\[
\boxed{
\left(
[x^{11}],[x^{12}],[x^{13}]
\right)
\rho\!\left(-\frac{H_5}{5}\right)
=
\left(0,\frac{60160000}{243u^{13}},0\right).
}
\tag{32}
\]
Because \(u\ne0\), this is nonzero.  Equations (25) and (31) prove
the stated finite-range saturated theorem, and (32) adds the nonsaturated
\(g=5\) limit.

## 4. Why the deck countermodel has the top forms (1)

Let \(R\) be monic of degree \(g\), let \(L\) have exact degree
\(g-1\), and write \(\ell=[X^{g-1}]L\ne0\).  Put
\[
D=R+\tau L.
\tag{33}
\]
The highest ordinary homogeneous part of \(D\) is
\[
D_0=X^g+\ell\tau X^{g-1},
\tag{34}
\]
whose dehomogenization is \(d=x^{g-1}(x+\ell)\).

Now allow the full affine endpoint
\[
P=D^2+\tau^{2g-1}(uX+v),\qquad
Q=D^3+w\tau^{3g-1},
\qquad uw\ne0.
\tag{35}
\]
The \(uX\tau^{2g-1}\) term has total degree \(2g\) and hence changes
the top form of \(P\); the \(v\tau^{2g-1}\) and
\(w\tau^{3g-1}\) terms have defect one.  Therefore the top
dehomogenized forms of (35) are exactly (1).
More importantly, the theorem depends only on those top forms, so it
still applies after arbitrary lower homogeneous pieces are added to
(35).

This identifies the earliest missing information in the global deck
budget: it is not another root-counting inequality, but the
total-degree filtered Keller cohomology.  The generic family fails at
its first possible class, defect three; its exceptional hypersurface
fails at defect four.

## Scope

The theorem closes the saturated common-deformation countermodel
family for \(a=2,b=3\) and every \(5\le g\le20\), whenever the endpoint
contributes a nonzero linear \(P\)-jet.  It does not exclude every
repeated-root standard-system candidate.  In particular, other
degree pairs, other highest homogeneous forms, or countermodels in
which additional top-degree terms already change \(p_0,q_0\) require
their own obstruction calculation.

The symbolic Hermite reconstruction from the displayed tail data,
the degree bounds, and the concrete countermodel are checked exactly by
`verify_standard_system_repeated_root_intervening_defect_obstruction.py`.
The verifier also evaluates the full quotient/remainder recurrence,
including the three tail evaluations in (23) and (29), separately
over the exact coefficient fields for every \(5\le g\le20\).  No
claim beyond that finite range rests on the displayed parameter
formulas.
