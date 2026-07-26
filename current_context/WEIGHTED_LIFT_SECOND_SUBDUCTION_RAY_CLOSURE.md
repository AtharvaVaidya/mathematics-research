# Closure of both second-subduction Newton rays

Date: 25 July 2026

> **Correction.**  The \(B\)-ray boundary-Euler proof below is
> superseded because it omits exact seed layers on \(t=u/x\).  The
> stated \(B\)-pivot conclusion is repaired by the exact first-lower
> double pole in
> `WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_CLOSURE.md`; the forbidden
> \(x^1\)-descent for the \(A\)-ray is unaffected.

## Outcome

Continue with the target polynomial \(U(A,B,C)\) constructed in
`WEIGHTED_LIFT_FIRST_NONLINEAR_CUSP_SUBDUCTION.md`.  On a polynomial
graph \(z=g(x,y)\), its highest form is
\[
U_0=\theta x^{49}y^{20}g_m^{17},\qquad \theta\ne0.
\tag{1}
\]
The preceding audit showed that the highest Jacobian of \((U,B)\) or
\((U,A)\) can vanish only on two sparse Newton rays.  This note closes
both rays, uniformly in their parameter.

More precisely, if \(L\) is any linear target form, then no
nonconstant polynomial graph makes either
\[
\bigl((U+L)\circ F,B\circ F\bigr)\big|_{z=g}
\quad\text{or}\quad
\bigl((U+L)\circ F,A\circ F\bigr)\big|_{z=g}
\tag{2}
\]
have nonzero constant Jacobian.  The same conclusion for pivot \(C\)
was already unconditional.  Thus the maximal first nonlinear
subduction, its second toric relation, and either original nonlinear
pivot \(A\) or \(B\) do not descend the degree-six threefold
counterexample to the plane.

The obstruction is theorem-driven:

- on the \(B\)-ray, the homogeneous recursion completes to a weighted
  Euler eigenfunction, but the fixed coefficient
  \(a=-57/34\) leaves an unavoidable \(xy\)-defect before any lower
  seed sector can enter;
- on the \(A\)-ray, the eigenfunction completion would require a term
  with only one factor of \(x\), whereas every graph contribution to
  \(\gamma\) is divisible by \(x^2\).

This is still not an all-nonlinear-target theorem.  In particular, a
general linear mixture of \(A,B,C\) as the second coordinate can
couple the two recursions and is not claimed here.

## 1. The two exact weighted-Euler operators

Put
\[
u=1+xy,\qquad
\gamma=1+a\,xy+x^2g(x,y),\qquad a=-\frac{57}{34}.
\tag{3}
\]
The highest seed sector of \(U\) is, up to a nonzero scalar,
\[
M=x^{-5}u^{20}\gamma^{17}.
\tag{4}
\]
The highest sectors of \(B\) and \(A\) are respectively
\[
N_B=x^{-1}u^5\gamma^4,\qquad
N_A=x^{-2}u^6\gamma^4.
\tag{5}
\]
Since
\[
J_{x,y}(R,S)=xJ_{x,u}(R,S),
\tag{6}
\]
direct logarithmic differentiation gives
\[
\begin{aligned}
J(M,N_B)
&=\frac{MN_B}{u\gamma}\,\mathcal L_B(\gamma),\\
J(M,N_A)
&=\frac{2MN_A}{u\gamma}\,\mathcal L_A(\gamma),
\end{aligned}
\tag{7}
\]
where
\[
\boxed{
\mathcal L_B=5x\partial_x-3u\partial_u-5,
\qquad
\mathcal L_A=11x\partial_x+7u\partial_u+5.
}
\tag{8}
\]

For later use, write these operators back in source coordinates.
On a monomial \(x^Iy^J\),
\[
\begin{aligned}
\mathcal L_B(x^Iy^J)
={}&(5I-5-8J)x^Iy^J
 -3Jx^{I-1}y^{J-1},\\
\mathcal L_A(x^Iy^J)
={}&(11I+5-4J)x^Iy^J
 +7Jx^{I-1}y^{J-1}.
\end{aligned}
\tag{9}
\]
Both operators preserve the difference \(I-J\), and are triangular
along each such diagonal.

## 2. Uniform closure of the \(B\)-ray

The \(B\)-ray is
\[
m=13k+12,\qquad
g_m=c\,x^{8k+7}y^{5k+5},\qquad k\ge0,\ c\ne0.
\tag{10}
\]
Its leading contribution to \(\gamma\) is
\[
c\,x^Iy^J,\qquad
I=8k+9,\quad J=5k+5.
\tag{11}
\]
The diagonal coefficient in the first line of (9) is zero:
\[
5I-5-8J=0.
\tag{12}
\]
To cancel the lower term in (9), the recursion successively forces
\[
c_n=\binom{J}{n}c,\qquad
c_nx^{I-n}y^{J-n},\qquad 0\le n\le J.
\tag{13}
\]
All of these terms are allowable graph contributions because
\[
I-J=3k+4\ge2.
\tag{14}
\]
Together they give the exact eigenfunction
\[
\gamma_{\rm ray}
=c\,x^{I-J}(1+xy)^J
=c\,x^{3k+4}u^{5k+5},
\qquad
\mathcal L_B(\gamma_{\rm ray})=0.
\tag{15}
\]
Equivalently, the forced graph part is
\[
g_{\rm ray}=c\,x^{3k+2}(1+xy)^{5k+5}.
\tag{16}
\]

The fixed low part of \(\gamma\) cannot join this eigenfunction:
\[
\mathcal L_B(1+a\,xy)
=-8a\,xy-(5+3a)
=\frac{228}{17}xy+\frac1{34}.
\tag{17}
\]
Could additional graph terms cancel the \(xy\)-coefficient?  Along
the diagonal \(I-J=0\), every graph contribution to \(\gamma\) starts
with \(x^ny^n\), \(n\ge2\).  If a finite nonzero sum of such terms is
present, choose its largest \(n\).  Its diagonal coefficient under
\(\mathcal L_B\) is
\[
-3n-5\ne0,
\tag{18}
\]
and there is no higher term to cancel it.  Descending induction forces
all those coefficients to vanish.  A degree-two graph term
\(d x^2\) has different monomial support from \(xy\).  Hence the
nonzero \(xy\)-term in (17) is unavoidable.

This defect appears \(m\) ordinary degrees below the highest
\((U,B)\)-Jacobian term.  The next seed term appears only \(m+4\)
degrees below: in the exact second-subduction numerator the next
monomial after \(w^{20}\gamma^2\) is
\(w^{19}\gamma^2\), and the same gap separates \(p_5w^5\) from
\(p_4w^4\).  Thus no lower seed sector can cancel (17).

Numerically, the unavoidable term has Jacobian degree
\[
(21m+84)-m=20m+84.
\tag{19}
\]
For any linear \(L\), the correction \(J(L,B)\) has degree at most
\[
8m+33<20m+84.
\tag{20}
\]
Therefore neither the lower seed nor the added linear target form can
remove the defect.  This closes the \(B\)-ray for every \(k\ge0\).

## 3. Uniform closure of the \(A\)-ray

The \(A\)-ray is
\[
m=15k+3,\qquad
g_m=c\,x^{4k-1}y^{11k+4},\qquad k\ge1,\ c\ne0.
\tag{21}
\]
Now the leading contribution to \(\gamma\) is
\[
c\,x^Iy^J,\qquad
I=4k+1,\quad J=11k+4.
\tag{22}
\]
The second diagonal coefficient in (9) vanishes:
\[
11I+5-4J=0.
\tag{23}
\]
The same triangular calculation forces
\[
c_n=\binom{J}{n}c,\qquad
c_nx^{I-n}y^{J-n}.
\tag{24}
\]
Indeed, at step \(n\) the diagonal coefficient is \(-7n\), while
the inherited lower coefficient is \(7(J-n+1)c_{n-1}\).

But a polynomial graph contributes to \(\gamma\) through \(x^2g\);
therefore every such monomial must have \(x\)-exponent at least two.
The recursion is allowable only through \(n=I-2\).  At
\[
n=I-1=4k
\tag{25}
\]
it requires
\[
\binom{J}{I-1}c\,
x\,y^{J-I+1}
=
\binom{11k+4}{4k}c\,
x\,y^{7k+4},
\tag{26}
\]
which is nonzero and cannot occur in \(x^2g\).  It is also neither of
the fixed terms \(1\) and \(a xy\).

The missing term occurs only \(2(I-1)=8k\) ordinary degrees below the
top.  This is earlier than the first lower seed sector because
\[
8k< m+4=15k+7.
\tag{27}
\]
It is also much earlier than an added linear-linear Jacobian could
enter:
\[
(21m+85-8k)-(8m+33)=187k+91>0.
\tag{28}
\]
Thus the missing \(x^1\)-term is an unavoidable obstruction, closing
the \(A\)-ray for every \(k\ge1\).

## 4. Scope

Combining the unconditional leading obstruction off the two rays with
Sections 2 and 3 gives
\[
\boxed{
\begin{aligned}
&J\bigl((U+L)\circ F|_g,\ B\circ F|_g\bigr)
\notin\mathbb C^\times,\\
&J\bigl((U+L)\circ F|_g,\ A\circ F|_g\bigr)
\notin\mathbb C^\times
\end{aligned}
}
\tag{29}
\]
for every linear target form \(L\) and every nonconstant polynomial
graph \(g\).

There is also a simpler local observation for \(U\) without a linear
addend.  At every source point \((0,0,z)\), one has
\[
F(0,0,z)=(A,0,0),
\tag{30}
\]
and all first target derivatives of \(U\) vanish on the line
\(\{B=C=0\}\).  Hence \(d(U\circ F|_g)=0\) at \((0,0)\), for every
graph.  The weighted analysis above is needed only because adding
\(L\) removes that immediate critical point.

The remaining nonlinear-projection problem must therefore change
both the subduced target coordinate and its pivot, rather than append
a linear term to \(U\) and retain \(A\), \(B\), or \(C\).  General
nonlinear pairs and general linear mixtures remain open.

The accompanying exact verifier is
`verify_weighted_lift_second_subduction_ray_closure.py`.
