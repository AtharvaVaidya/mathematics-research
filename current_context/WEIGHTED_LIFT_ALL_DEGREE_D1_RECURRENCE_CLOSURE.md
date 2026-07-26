# Closure of every binary degree-one Newton face

Date: 25 July 2026

## Outcome

Let \(F=(A,B,C)\) be the generic-degree-six Gallagher weighted lift
and let \(U\) be its second-subduction coordinate.  For every
\(n\ge1\), consider
\[
Q_n=B^{n-1}(\lambda A+\mu B),
\qquad \lambda\ne0,
\tag{1}
\]
with arbitrary \(\mu\).  No polynomial graph \(z=g(x,y)\) makes
\[
\bigl(U\circ F,\ Q_n\circ F\bigr)\big|_{z=g}
\tag{2}
\]
have nonzero constant Jacobian.

In the all-degree binary characteristic classification, (1) is
exactly the family with Newton degree \(d=1\).  The earlier highest
sector argument closed its descending, negative-tail, and pure
specializations, but the first honest mixed polynomial completion
occurred at \(n=6\).  The calculation below is uniform in \(n\):
after including the first lower seed, its source-axis residue is
\[
\boxed{
-\frac{
2975In^2+952In-2023I
-3035n^2+22780n-1785
}{2040n}.
}
\tag{3}
\]
It is strictly negative for every \(n\ge1\) and every graph sector
\(I\ge2\).  Thus every binary \(d=1\) face is closed in every target
degree, not merely the formerly exceptional sextic case.

Arbitrary affine perturbations of either target coordinate enter
after this obstruction and do not change the result.  This theorem
does not address binary faces of Newton degree \(d\ge2\), nor targets
involving \(C\).

## 1. Highest characteristic

Put
\[
u=1+xy,\qquad t=\frac ux,\qquad
\gamma=1-\frac{57}{34}xy+x^2g(x,y).
\tag{4}
\]
The highest sectors are, up to nonzero constants,
\[
\begin{aligned}
U^{(0)}&=\theta x^{15}t^{20}\gamma^{17},\\
A^{(0)}&=q_6x^4t^6\gamma^4,\\
B^{(0)}&=p_5x^4t^5\gamma^4,
\end{aligned}
\tag{5}
\]
where
\[
p_5=-\frac3{46},\qquad q_6=-\frac5{92}.
\tag{6}
\]
After absorbing \(\lambda q_6p_5^{n-1}\), and writing
\[
\eta=\frac{\mu p_5}{\lambda q_6},
\tag{7}
\]
the highest sector of (1) is
\[
V^{(0)}
=x^{4n}t^{5n}\gamma^{4n}(t+\eta).
\tag{8}
\]
The highest Jacobian equation is
\[
\mathcal L_n(\gamma)=0,
\tag{9}
\]
where
\[
\begin{aligned}
\mathcal L_n(\gamma)={}&
x\left(\frac{5n}{t}+\frac{17}{t+\eta}\right)\gamma_x
-8n\gamma_t\\
&+\left(-\frac{5n}{t}+\frac{15}{t+\eta}\right)\gamma.
\end{aligned}
\tag{10}
\]
On a fixed \(x\)-Laurent sector it has the unique formal solution
\[
G=c\,x^It^r(t+\eta)^s,
\qquad
r=\frac{5(I-1)}8,\qquad
s=\frac{17I+15}{8n}.
\tag{11}
\]
Its leading \(t\)-degree is
\[
J=r+s,\qquad m=I+J-2.
\tag{12}
\]
If (11) is descending, has a negative \(t\)-tail, or fails to be
graph-divisible, the highest-sector mechanisms already exclude it.
It remains only to test any honest polynomial characteristic
completion against the first lower seed.

## 2. The exact first-lower slices

The exact second-subduction numerator has consecutive terms
\[
\theta w^{20}\gamma^2
-\frac{70}{3}\theta w^{19}\gamma^2
\tag{13}
\]
before division by \(x^5\gamma^5\).  Therefore
\[
U^{(1)}
=-\frac{70}{3}\theta x^{14}t^{19}\gamma^{16}.
\tag{14}
\]

The exact seed ratios are
\[
\frac{q_5}{q_6}=-\frac{28}{5},
\qquad
\frac{p_4}{p_5}=-\frac{35}{6}.
\tag{15}
\]
In the \(A B^{n-1}\) term, the first-lower coefficient is
\[
a_n=\frac{q_5}{q_6}
+(n-1)\frac{p_4}{p_5}
=-\frac{28}{5}-\frac{35(n-1)}6.
\tag{16}
\]
In \(B^n\), it is
\[
b_n=n\frac{p_4}{p_5}=-\frac{35n}{6}.
\tag{17}
\]
Thus
\[
V^{(1)}
=x^{4n-1}t^{5n-1}\gamma^{4n-1}
\left(a_nt+b_n\eta\right).
\tag{18}
\]

These are the only terms on the first-lower graph-weight slice.
Replacing \(q_6\) by \(q_5\), or \(p_5\) by \(p_4\), costs exactly
\(m+4\).  A \(q_4\) or \(p_3\) term, or two first-lower
replacements, costs \(2(m+4)\).  The added \(w\gamma\) in \(A\) and
\(\gamma\) in \(B\) cost \(4m+18>m+4\).  The exact 77-term support of
the second-subduction numerator likewise certifies that (14) is its
unique first-lower slice.

## 3. The uniform lower recurrence

Evaluate
\[
J(U^{(1)},V^{(0)})+J(U^{(0)},V^{(1)})
\tag{19}
\]
on the characteristic (11), then divide by the common top-top
Jacobian factor.  Exact logarithmic differentiation gives
\[
\begin{aligned}
\mathcal R_{n,I}
=-\frac{7}{
120nxt^2(t+\eta)^2
}\bigl(&
25I\eta^2n^2
+50I\eta n^2t
-60I\eta nt\\
&+25In^2t^2+8Int^2-17It^2\\
&-25\eta^2n^2-50\eta n^2t-100\eta nt\\
&-25n^2t^2-40nt^2-15t^2
\bigr).
\end{aligned}
\tag{20}
\]
The first-lower equation is
\[
\mathcal L_n(\delta\gamma)+\mathcal R_{n,I}=0.
\tag{21}
\]
No characteristic amplitude occurs in (20).

Put
\[
\begin{aligned}
H&=u+\eta x,\\
K&=5nH+17u,\\
L&=-5nH+15u.
\end{aligned}
\tag{22}
\]
Multiplying (21) by \(uH\) and returning to \((x,y)\) turns the
homogeneous part into the polynomial operator
\[
\mathcal E_n(\phi)
=xK(x\phi_x-y\phi_y)
+u(K-8nH)\phi_y
+xL\phi.
\tag{23}
\]
The fixed boundary jet is
\[
\gamma_{\rm fix}=1-\frac{57}{34}(u-1).
\tag{24}
\]
Modulo \(x^2\), it gives
\[
\mathcal E_n(\gamma_{\rm fix})
\equiv\frac{n-459}{34}x.
\tag{25}
\]
Transforming (20) in the same way gives
\[
uH\mathcal R_{n,I}
\equiv
-\frac{
7(n+1)(25In-17I-25n-15)
}{120n}x
\pmod{x^2}.
\tag{26}
\]
Adding (25) and (26) yields exactly (3).

Every polynomial graph correction enters \(\gamma\) as
\(x^2h(x,y)\).  Each term of (23) preserves divisibility by \(x^2\),
so no same-weight or lower graph coefficient can alter the
source-axis residue (3).  Any honest characteristic (11) is itself
graph-divisible and lies in the kernel of the homogeneous operator,
so it does not change the residue either.

## 4. Uniform nonvanishing

Let the numerator in (3) be \(N(I,n)\).  It is affine in \(I\), with
\[
\frac{\partial N}{\partial I}
=2975n^2+952n-2023.
\tag{27}
\]
For \(n\ge1\), this is positive: its value at \(n=1\) is \(1904\)
and it is strictly increasing.  Therefore \(N(I,n)\) is minimized
over \(I\ge2\) at \(I=2\).  There,
\[
N(2,n)=2915n^2+24684n-5831.
\tag{28}
\]
This is also strictly increasing for \(n\ge1\), and
\[
N(2,1)=21768>0.
\tag{29}
\]
Hence \(N(I,n)>0\) for all \(n\ge1,I\ge2\), proving that (3) never
vanishes.

For a nonconstant graph, the obstruction occurs at drop \(m+4\).
An affine second-coordinate perturbation lies farther below the
degree-\(n\) face for \(n\ge2\); for \(n=1\), it only changes
\((\lambda,\mu)\) or adds a constant.  An affine first-coordinate
perturbation is at least \(13m+51\) below \(U\).  Neither can repair
(3).  Constant graphs are already covered by the separated
highest-form calculation in the all-degree binary reduction.

Thus every binary \(d=1\) face is closed in every degree.

The accompanying exact verifier is
`verify_weighted_lift_all_degree_d1_recurrence_closure.py`.
