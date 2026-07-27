# Closure of every quadratic second pivot

Date: 25 July 2026

> **Correction.**  The pure-face boundary-Euler subargument used below
> is not the full exact source-boundary equation after \(t=u/x\).
> Moreover, in the arbitrary-lower-tier theorem a lower \(B\) term can
> enter the same first-lower sector as the pure \(AC\) face.  The full
> quadratic conclusion stated below is therefore not currently proved
> on the \(AC+B\) chain.  The descending, mixed negative-tail,
> nonresonance, and constant-graph certificates remain valid.

## Outcome

Let \(F=(A,B,C)\) be the generic-degree-six Gallagher weighted lift
and let \(U(A,B,C)\) be the second-subduction polynomial from
`WEIGHTED_LIFT_FIRST_NONLINEAR_CUSP_SUBDUCTION.md`.  Let
\[
Q=\alpha A^2+\beta AB+\chi B^2
+\mu AC+\nu BC+\rho C^2
+\ell_AA+\ell_BB+\ell_C C+\ell_0,
\tag{1}
\]
and suppose that its homogeneous quadratic part is nonzero.
Then, for every polynomial graph \(z=g(x,y)\) and every target-linear
form \(L\),
\[
\left((U+L)\circ F,\ Q\circ F\right)\big|_{z=g}
\tag{2}
\]
does not have nonzero constant Jacobian.

This is the first all-family exclusion with a genuinely nonlinear
second target coordinate.  The squares \(A^2\) and \(B^2\) inherit the
old \(A\)- and \(B\)-rays.  The mixed monomial \(AB\), which is the
smallest new nonlinear pivot in the \(A,B\) face of the target Newton
semigroup, creates a new ray
\[
m=43k+1,\qquad
g_m=c\,x^{16k-1}y^{27k+2},\qquad k\ge1.
\tag{3}
\]
The whole binary quadratic, not only the monomial \(AB\), can be
integrated by one characteristic equation.  If \(\alpha\ne0\), its
formal solution still forces the forbidden \(x^1\)-term from the
old \(A\)-ray.  If \(\alpha=0\), \(\beta\ne0\), it forces
\[
c\binom{27k+2}{16k}x\,y^{11k+2},
\tag{4}
\]
independently of \(\chi/\beta\), before a lower seed sector can enter.
If only \(\chi\ne0\), the fixed
\(a=-57/34\) part of the graph leaves the old \(B\)-ray defect.

The binary \(A,B\)-face is the only difficult part.  Quadratic terms
involving \(C\) enter too late to repair any of its three defects.  If
the binary face vanishes, the remaining \(C(\mu A+\nu B+\rho C)\)
face has only one new resonant ray.  A mixed \(AC/BC\) pivot forces a
negative power of \(t=u/x\) before any lower sector enters; pure
\(AC\) leaves a fixed Euler defect; \(BC\) has no resonance.  The
remaining \(C^2\) case reduces to the already closed linear pivots.

Thus (2) excludes every quadratic second target coordinate, with
arbitrary affine perturbations.  It is **not** an arbitrary nonlinear
target theorem: cubic target faces can have new adjacent weights and
remain outside the argument.

## 1. The binary quadratic highest sector

Put
\[
u=1+xy,\qquad t=\frac ux=y+\frac1x,\qquad
\gamma=1+a\,xy+x^2g(x,y),\qquad a=-\frac{57}{34}.
\tag{5}
\]
Up to nonzero constants, the relevant highest sectors are
\[
\begin{aligned}
M&=x^{-5}u^{20}\gamma^{17}
  =x^{15}t^{20}\gamma^{17},\\
A_{\mathrm h}&=q_6x^{-2}u^6\gamma^4
  =q_6x^4t^6\gamma^4,\\
B_{\mathrm h}&=p_5x^{-1}u^5\gamma^4
  =p_5x^4t^5\gamma^4,
\end{aligned}
\tag{6}
\]
where
\[
p_5=-\frac3{46},\qquad q_6=-\frac5{92}.
\tag{7}
\]
Consequently the binary quadratic has highest seed slice
\[
N=x^8t^{10}\gamma^8P(t),
\qquad
P(t)=\alpha q_6^2t^2+\beta p_5q_6t+\chi p_5^2.
\tag{8}
\]
Let \(d=\deg P\).  Thus \(d=2,1,0\) according as the first nonzero
coefficient in \((\alpha,\beta,\chi)\) is \(\alpha,\beta,\chi\).

The vanishing of the highest Jacobian \(J(M,N)\) is equivalent to
\[
x\left(\frac{10}{t}+17\frac{P'}P\right)\gamma_x
-16\gamma_t
+\left(-\frac{10}{t}+15\frac{P'}P\right)\gamma=0.
\tag{9}
\]
For completeness, (9) is just logarithmic differentiation of (6)
and (8); no graph coefficient has been specialized.

Decompose formally by powers of \(x\) in the \((x,t)\)-chart.  A
sector \(\gamma=x^I\phi(t)\) satisfies
\[
\phi(t)=c\,t^rP(t)^s,\qquad
r=\frac{5I-5}{8},\qquad
s=\frac{17I+15}{16}.
\tag{10}
\]
If its leading term at \(t=\infty\) is \(cx^It^J\), then
\[
J=r+ds.
\tag{11}
\]
This one formula gives every possible highest resonance of a binary
quadratic pivot.

## 2. The three Newton faces

### 2.1. The \(A^2\)-face

Suppose \(\alpha\ne0\), so \(d=2\).  Equation (11) becomes
\[
4J=11I+5.
\tag{12}
\]
A leading graph monomial contributes \(I=i+2\) and \(J=m-i\).
The integral solutions with \(I\ge2\) are
\[
I=4k+1,\qquad J=11k+4,\qquad m=15k+3,
\qquad k\ge1.
\tag{13}
\]
Normalize the leading coefficient of \(P\).  Formula (10) begins
\[
\gamma_I=cx^It^J\left(1+O(t^{-1})\right).
\tag{14}
\]
The characteristic equation preserves each \(x\)-Laurent sector.
More precisely, on both (12) and (18) the leading weight
\(W(I)=I+J(I)\) is strictly increasing, while the source diagonal
\(D(I)=I-J(I)\) is strictly decreasing.  Any other resonant sector
lying below the chosen top therefore has \(I'<I\) and
\(D(I')>D(I)\).  Its descending \(t\)-terms have diagonals
\(D(I')+q\), \(q\ge0\), so none can reach \(D(I)\).  A sector with
\(I'>I\) would have larger leading weight and is absent, while a
nonresonant sector has no free leading coefficient in the homogeneous
recursion.  Thus the displayed forbidden monomial accounts for every
possible same-monomial cancellation, not only for the lower powers
inside one \(P(t)^s\).
On substituting \(t=y+x^{-1}\), the highest-\(y\) monomial with
\(x\)-exponent one comes only from the displayed \(t^J\) term:
\[
c\binom{J}{I-1}x\,y^{J-I+1}
=c\binom{11k+4}{4k}x\,y^{7k+4}.
\tag{15}
\]
Every \(O(t^{-q})\), \(q>0\), contribution has strictly smaller
\(y\)-degree at \(x\)-exponent one.  Hence neither the \(AB\) nor the
\(B^2\) coefficient can cancel (15).  But a graph enters \(\gamma\)
through \(x^2g\), and the fixed part of \(\gamma\) has only the
\(x^1\)-term \(a xy\).  Thus (15) is impossible.

The obstruction occurs at ordinary-degree drop
\[
2(I-1)=8k.
\tag{16}
\]
The next seed sector enters only at drop
\[
m+4=15k+7>8k.
\tag{17}
\]
This proves the exclusion uniformly in \(\beta\) and \(\chi\), not
just for the pure square \(A^2\).

### 2.2. The \(AB\)-face

Suppose \(\alpha=0\) and \(\beta\ne0\), so \(d=1\).  Now (11) is
\[
16J=27I+5.
\tag{18}
\]
Its graph solutions are precisely
\[
I=16k+1,\qquad J=27k+2,\qquad
m=43k+1,\qquad k\ge1,
\tag{19}
\]
which gives (3).  In this case (10) is especially concrete:
\[
r=10k,\qquad s=17k+2,\qquad
\gamma_I=cx^It^{10k}P(t)^{17k+2}.
\tag{20}
\]
Again normalize the leading coefficient of \(P\).  The leading
\(t^J\)-term forces
\[
c\binom{J}{I-1}x\,y^{J-I+1}
=c\binom{27k+2}{16k}x\,y^{11k+2}.
\tag{21}
\]
The \(B^2\)-part of \(P\) contributes only lower powers of \(t\), so
at \(x\)-exponent one it contributes only lower \(y\)-degrees.  It
cannot cancel (21).  As before, (21) is neither in \(x^2g\) nor in
the fixed part of \(\gamma\).

This new obstruction occurs at drop
\[
2(I-1)=32k,
\tag{22}
\]
strictly before the first lower seed sector:
\[
m+4=43k+5>32k.
\tag{23}
\]

### 2.3. The \(B^2\)-face

Finally let \(\alpha=\beta=0\), \(\chi\ne0\).  Equation (11) reduces
to
\[
8J=5I-5.
\tag{24}
\]
Writing the nonnegative solutions in graph notation gives
\[
I=8k+9,\qquad J=5k+5,\qquad
m=13k+12,\qquad k\ge0.
\tag{25}
\]
The formal sector completes polynomially:
\[
\gamma_{\rm ray}
=c\,x^{I-J}u^J
=c\,x^{3k+4}u^{5k+5}.
\tag{26}
\]
But the fixed part
\(\gamma_{\rm fix}=1+a(u-1)\) has
\[
\left(5x\partial_x-3u\partial_u-5\right)
\gamma_{\rm fix}
=\frac{228}{17}xy+\frac1{34}.
\tag{27}
\]
No graph contribution on the diagonal \(I-J=0\) can cancel this.
Indeed, for a finite sum of terms \(x^ny^n\), \(n\ge2\), the largest
\(n\) has nonzero diagonal coefficient \(-3n-5\).  Descending
induction therefore kills the whole sum.  The defect (27) occurs at
drop \(m\), four degrees before the first lower seed sector.

## 3. The \(C\)-quadratic faces

The quadratic terms involving \(C\) have top degrees
\[
\deg(AC,BC,C^2)=(5m+21,5m+20,2m+6),
\tag{28}
\]
whereas
\[
\deg(A^2,AB,B^2)=(8m+36,8m+35,8m+34).
\tag{29}
\]
If any of \(\alpha,\beta,\chi\) is nonzero, the appropriate binary
face therefore leads.  The first \(C\)-term enters below the
\(A^2,AB,B^2\) Jacobian tops at respective drops
\[
3m+15,\qquad3m+14,\qquad3m+13.
\tag{30}
\]
These are strictly later than the defects \(8k,32k,m\) proved above.
Thus arbitrary values of \(\mu,\nu,\rho\) cannot repair a binary-face
obstruction.

It remains to suppose
\[
\alpha=\beta=\chi=0.
\tag{31}
\]
If \(\mu\ne0\), the \(AC/BC\) slice has, in the \((x,t)\)-chart,
\[
N_C=x^5t^5\gamma^5R(t),\qquad
R(t)=\mu q_6t+\nu p_5.
\tag{32}
\]
The highest Jacobian vanishes only if
\[
x\left(-\frac{15}{t}+17\frac{R'}R\right)\gamma_x
-10\gamma_t
+\left(-\frac{25}{t}+15\frac{R'}R\right)\gamma=0.
\tag{33}
\]
A sector \(x^I\phi(t)\) is therefore
\[
\phi(t)=c\,t^{-(3I+5)/2}R(t)^{(17I+15)/10}.
\tag{34}
\]
At \(t=\infty\), its leading exponent \(J\) obeys
\[
I=5J+5.
\tag{35}
\]
The graph rays are
\[
I=5k+5,\qquad J=k,\qquad
m=6k+3,\qquad g_m=cx^{5k+3}y^k,\qquad k\ge0.
\tag{36}
\]

If \(\nu\ne0\), normalize \(R(t)=r_1(t+d)\) with \(d\ne0\).
Equation (34) becomes, up to a nonzero scalar,
\[
\phi(t)=t^J(1+d/t)^s,\qquad
s=\frac{17k+20}{2}.
\tag{37}
\]
Its coefficient of \(t^{-1}\) is
\[
\binom{s}{k+1}d^{k+1}\ne0.
\tag{38}
\]
Indeed \(s-j=(17k+20-2j)/2>0\) for
\(0\le j\le k\), so no factor in the generalized binomial coefficient
vanishes (whether \(s\) is integral or half-integral).
But for a polynomial graph, every coefficient of every \(x\)-power
in
\[
\gamma(x,t)=1-a+axt+x^2g(x,t-x^{-1})
\tag{39}
\]
is a polynomial in \(t\); it cannot contain \(t^{-1}\).  The forbidden
term cannot be canceled by another \(x\)-sector because (33) has
coefficients depending only on \(t\), so the Laurent decomposition in
\(x\) is a direct sum of independent first-order equations.

The two depth measurements are commensurable.  Give the infinity
chart the leading ordinary grading
\[
\operatorname{wt}(x^rt^s)=r+s;
\]
this agrees with ordinary source degree on the leading term because
\(t=y+x^{-1}\).  The resonant term \(x^It^J\) has weight
\(I+J=m+2\), and each descending \(t\)-step lowers this weight by
one.  Hence the demanded \(t^{-1}\) coefficient occurs at filtration
drop \(J+1=k+1\).  This is strictly before the next seed sector, whose
exact graph-weight drop is \(m+4=6k+7\).  The \(C^2\) sector is still
farther below, at gap \(3m+15\).

If \(\nu=0\), the formal ray completes to
\[
\gamma_{\rm ray}=c\,x^{I-J}u^J
=c\,x^{4k+5}u^k.
\tag{40}
\]
The normalized \(AC\) operator is
\[
\mathcal L_{AC}=x\partial_x-4u\partial_u-5,
\tag{41}
\]
and on \(\gamma_{\rm fix}=1+a(u-1)\) it gives
\[
\mathcal L_{AC}(\gamma_{\rm fix})
=\frac{513}{34}xy+\frac{29}{17}.
\tag{42}
\]
Graph terms on the diagonal \(I-J=0\) cannot cancel this: the largest
term \(x^ny^n\), \(n\ge2\), has nonzero diagonal coefficient
\(-4n-5\).  This defect occurs at drop \(m\), before both the next
seed sector and \(C^2\).

If \(\mu=0,\nu\ne0\), the leading pivot is \(BC\).  Its master Euler
operator has coefficients
\[
(-15,-25,-25),
\tag{43}
\]
so on a possible leading graph monomial \(x^Iy^J\) its diagonal
coefficient is
\[
-15I-10J-25<0.
\tag{44}
\]
There is no resonant ray.

Finally suppose only \(\rho C^2\) remains in the quadratic part.  If
the affine part has an \(A\)- or \(B\)-component, it leads the
\(C^2\)-Jacobian.  The latter enters below the \(A\)- and \(B\)-pivot
tops at drops \(2m+12\) and \(2m+11\), later than their respective
defects.  If the affine part is a function of \(C\), then
\[
J(U,\rho C^2+\ell_C C)
=(2\rho C+\ell_C)J(U,C),
\tag{45}
\]
whose highest form is nonzero.  This closes the last quadratic face.

## 4. Affine perturbations enter too late

For a nonconstant graph of degree \(m\),
\[
\deg U_0=17m+69,\quad
\deg A_0=4m+18,\quad
\deg B_0=4m+17.
\tag{46}
\]
The three binary-quadratic Jacobian tops have degrees
\[
\begin{array}{c|c}
\text{face}&\deg J(U,Q_2)\\ \hline
A^2&25m+103\\
AB&25m+102\\
B^2&25m+101.
\end{array}
\tag{47}
\]
For arbitrary target-linear \(L_1,L_2\),
\[
\deg J(U,L_2)\le21m+85,\qquad
\deg J(L_1,Q_2)\le12m+51,\qquad
\deg J(L_1,L_2)\le8m+33.
\tag{48}
\]
On the \(A^2\)-ray, the first gap in (48) below the surviving
obstruction is \(52k+30\).  On the \(AB\)-ray it is \(140k+21\).
On the \(B^2\)-ray it is \(3m+16\).  Thus no affine correction reaches
any of the three defects.

For the \(AC/BC\) face, the Jacobian top has degree \(22m+88\).
The first affine term \(J(U,A)\) lies \(m+3\) degrees below it, later
than the mixed obstruction \(k+1\) and the pure-\(AC\) defect \(m\).
All \(J(L_1,Q_2)\) terms have still smaller degree.

## 5. Constant graphs

Let \(g=z_0\) and
\[
h=ay+z_0x,\qquad C_0=x^2h.
\tag{49}
\]
The highest forms are
\[
A_0=q_6y^6C_0^4,\qquad
B_0=p_5y^5C_0^4,\qquad
U_0=\theta x^{32}y^{20}h^{17},
\tag{50}
\]
with \(\theta\ne0\).  The known nonzero forms \(J(U_0,A_0)\) and
\(J(U_0,B_0)\), together with the product rule, give
\[
\begin{aligned}
J(U_0,A_0^2)&=2A_0J(U_0,A_0)\ne0,\\
J(U_0,A_0B_0)
&=p_5q_6\theta x^{47}y^{30}h^{24}
  (16ay+59z_0x)\ne0,\\
J(U_0,B_0^2)&=2B_0J(U_0,B_0)\ne0.
\end{aligned}
\tag{51}
\]
Their respective degrees are \(103,102,101\), while every
\(J(U_0,L_2)\) has degree at most \(85\).  The same descending
separation first selects the binary face whenever it is present.

If the binary face vanishes, direct product-rule calculation gives
\[
\begin{aligned}
J(U_0,A_0C_0)
&=-6q_6\theta x^{41}y^{25}h^{21}
  (3ay+z_0x),\\
J(U_0,B_0C_0)
&=-5p_5\theta x^{41}y^{24}h^{21}
  (10ay+11z_0x),\\
J(U_0,C_0^2)
&=-12\theta x^{35}y^{19}h^{18}
  (7ay+10z_0x).
\end{aligned}
\tag{52}
\]
These nonzero forms have separated degrees \(88,87,73\).  Affine
terms cannot cancel the selected highest form, except when an affine
\(A\)- or \(B\)-term leads \(C^2\); that is exactly the already
separated linear-pivot case.

## 6. Scope and next Newton face

Combining all target Newton faces proves
\[
\boxed{
J_{x,y}\left(
(U+L)\circ F|_{z=g},\
Q\circ F|_{z=g}
\right)\notin\mathbb C^\times
}
\tag{53}
\]
for every polynomial \(g\), every target-linear \(L\), and every
\(Q\) of the form (1) with nonzero quadratic part.

The structural gain is the characteristic formula (10): it replaces
a coefficient search over three arbitrary quadratic coefficients by
the single integer \(d=\deg P\).  The next genuinely different Newton
layer is cubic.  The closest new candidates include
\[
A^3+\lambda A^2B+\cdots
\quad\text{and}\quad
C\,Q_2(A,B,C),
\tag{54}
\]
where two quadratic characteristic factors can interact.  Those are
not claimed here.

The accompanying exact verifier is
`verify_weighted_lift_all_quadratic_pivot_closure.py`.
