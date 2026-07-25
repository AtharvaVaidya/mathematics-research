# Adversarial audit of the cusp-complement route

Date: 24 July 2026

## Verdict

The single-signature reduction over the source open set \(x\ne0\) survives
the audit, but the proposed comparison of finite étale covers of the fixed
cusp complement is not yet available.  Three independent assertions would
be needed:

1. the nonproper-value set of the completed map is contained in the fixed
   cusp;
2. the completed map has the same covering degree as the outer model;
3. the fixed outer edge determines the full \(B_3\)-monodromy
   representation, not only its local cycle types.

None follows from the outer Belyi equation alone.  The first assertion
already encounters an explicit additional asymptotic curve in the
five-block normal form.

## 1. What is exact for the identity outer model

Put
\[
P_0=\frac{z^2U(w)}w,\qquad
Q_0=\frac{z^3V(w)}w,\qquad
L=\frac{v_{3k+1}^2}{u_{2k+1}^3}.
\]
Then
\[
Q_0^2-LP_0^3
=\frac{z^6}{w^3}F_0(w),\qquad
F_0(w)=wV(w)^2-LU(w)^3. \tag{1}
\]
The passport gives
\[
\deg F_0=k+1,
\]
and \(F_0\) is squarefree.  Thus the identity divisor has \(k+1\)
finite components \(w=\gamma_i\).  On each,
\[
\tau=\frac{Q_0}{\sqrt L\,P_0}
=\frac{zV(\gamma_i)}{\sqrt L\,U(\gamma_i)}
\]
has degree one.  This is the clean component separation present at the
undeformed point.

## 2. Every full five-block completion has another asymptotic curve

For the a/b five-block form,
\[
\begin{aligned}
P&=\frac{z^2}{w}+a_0(w)+za_1(w)+z^2a_2(w),\\
Q&=\frac{z^3}{w}+b_0(w)+zb_1(w)+z^2b_2(w)+z^3b_3(w).
\end{aligned} \tag{2}
\]
Fix \(w=w_0\ne0\) and let \(z\to0\).  In the original coordinates
\[
x=\frac{z^2}{w},\qquad y=\frac wz,
\]
the source point escapes to infinity: \(x\to0\) and \(y\to\infty\).
Nevertheless
\[
(P,Q)\longrightarrow(a_0(w_0),b_0(w_0)). \tag{3}
\]
Consequently the nonproper-value set \(S_F\) contains
\[
\Gamma_F=\overline{\{(a_0(w),b_0(w)):w\in\mathbf A^1\}}. \tag{4}
\]
This is an exact necessary inclusion, not a genericity assertion.

For the fixed cusp
\[
C_L=\{q^2=Lp^3\},
\]
the condition \(\Gamma_F\subset C_L\) is exactly
\[
b_0(w)^2=L\,a_0(w)^3. \tag{5}
\]
Over an algebraically closed characteristic-zero field, unique
factorization shows that (5) is equivalent to
\[
a_0=\alpha h^2,\qquad b_0=\beta h^3,\qquad
\beta^2=L\alpha^3. \tag{6}
\]
Indeed \(2\nu_\pi(b_0)=3\nu_\pi(a_0)\) for every irreducible
\(\pi\), so every valuation of \(a_0\) is even and every valuation of
\(b_0\) is divisible by three.  With the required a/b vertices,
\(\deg a_0=8,\deg b_0=12\), formula (6) forces \(\deg h=4\).

No current radial theorem proves (5) or (6).  Nor has every other toric
boundary been excluded from contributing an additional nonproper curve.
Therefore
\[
S_F\subset C_L \tag{7}
\]
is a substantive missing theorem.  Removing the contracted affine line
\(x=0\) from the source does not remove the escaping paths (3).

For the full case-c support the same obstruction is even more direct.
The line \(x=0\) is not contracted:
\[
p(y)=P(0,y),\qquad q(y)=Q(0,y),\qquad
\deg p=8,\quad\deg q=12.
\]
If \(q^2-Lp^3\not\equiv0\), a dense open subset of this critical line
maps into \(Y=\mathbf A^2\setminus C_L\).  Hence
\(F^{-1}(Y)\to Y\) is not étale.  The forced top edge proves only
\(q(y)^2/p(y)^3\to L\) as \(y\to\infty\), not the polynomial identity
\(q^2=Lp^3\).  Thus in case c the same square/cube factorization is a
necessary hypothesis even before properness is considered.

## 3. The covering degree is not fixed by the outer edge

Bernstein mixed volumes give a quick warning.  After adjoining the target
constants, the identity outer polygons have mixed volume
\[
21.
\]
The complete a/b polygons have mixed volume
\[
45,
\]
and the complete case-c polygons have mixed volume
\[
141. \tag{8}
\]
These are generic torus-fiber counts.  A bracket solution can be
Newton-degenerate, so (8) does not prove that its degree is \(45\) or
\(141\).  It does prove that the fixed outer edge alone does not establish
degree \(21\).  Equality of covering degrees needs its own argument.

## 4. Conditional cusp-complement lemma

The following statement is sound.

> Let \(F=(P,Q)\) satisfy \([P,Q]=x^2\), with the critical
> line \(x=0\) mapping into \(C_L\).  If every nonproper value of \(F\) lies in
> \(C_L\), then
> \[
> F:F^{-1}(\mathbf A^2\setminus C_L)
> \longrightarrow\mathbf A^2\setminus C_L
> \]
> is finite étale.  If, after labeling one fiber, its full monodromy
> homomorphism
> \[
> \langle a,b\mid a^2=b^3\rangle\longrightarrow S_d
> \]
> equals that of the outer model, the two covers are isomorphic.

Quasi-finiteness follows because the Jacobian is nonzero on \(x\ne0\);
properness is precisely the asserted absence of nonproper values outside
the cusp.  Equality on the two generators gives equality of the covering
representations.  The conclusion is therefore correct but conditional.

The outer edge supplies the passport of the two generator images and the
peripheral product.  A passport does not determine a cover: at \(k=3\)
there are already five Hurwitz points with the same three cycle types.
Even after fixing one outer point, one must still prove that the
completed cover has the same labeled images of both \(B_3\) generators.

## 5. Exact component-joining countermodel

There is an abstract pullback model using the actual outer rational
function which shows why the \(k+1\) finite branches are insufficient.
Write
\[
R(W)-L=\frac{F_0(W)}{G(W)},\qquad
G=U^3,
\]
so
\[
\deg G=6k+3,\qquad \deg F_0=k+1,\qquad
\gcd(F_0,G)=1.
\]
Over \(K(w,z)\), set
\[
\rho=R(w)+\frac1z,\qquad R(W)=\rho. \tag{9}
\]
At \(z=\infty\), Hensel expansion selects the normalized root
\[
W=w+\frac{1}{zR'(w)}+O(z^{-2}). \tag{10}
\]
The pullback of the cusp value is
\[
zF_0(w)+G(w)=0. \tag{11}
\]
Equation (11) is irreducible: it is linear in \(z\), and a factor
independent of \(z\) would divide both \(F_0\) and \(G\).  Nevertheless it
has \(k+1\) distinct formal branches at \(z=\infty\), one above each root
of \(F_0\).

The generic root polynomial for (9) is irreducible over \(K(w,z)\).
Indeed \(A(T)-\rho B(T)\) is the minimal polynomial defining
\(K(T)/K(R(T))\), and adjoining the independent transcendental \(w\)
preserves irreducibility.  Hence the component containing the identity
germ (10) is the whole degree-\(6k+3\) component.  Over (11) it also
contains the \(W=\infty\) point of ramification index \(5k+2\).

Thus one irreducible component can simultaneously contain all the
normalized finite branches and the forbidden infinity valuation.  This
model is not claimed to arise from a bounded symplectic completion.  It
proves the precise negative statement needed for the audit:

> the Newton polygon of \(D\), its \(k+1\) finite identity branches, and
> the outer passport do not by themselves give component separation.

## 6. Status of the single-signature criterion

The corrected criterion in
`RADIAL_RATIONAL_DESCENT_CRITERION.md` is not refuted by this audit.  Its
proof works over
\[
U=\{x\ne0\}\simeq\mathbf G_m\times\mathbf A^1.
\]
If the \((5k+2,k,-1)\) valuation is absent, the selected normalization is
finite étale over \(U\), hence is a Kummer cover \(u^e=x\).  At the split
radial valuation \(t=1/w\), \(z\) is a unit and
\[
x=z^2t
\]
has valuation one.  Since the selected formal root already lies in
\(K(z)((t))\), no nontrivial \(e\)-th root of \(x\) can occur; hence
\(e=1\).

Two qualifications should remain explicit:

1. the title “sole ramification divisor” means sole possible divisor
   **over \(x\ne0\)**; the full case-c line \(x=0\) is not contracted and
   its residue \(Q(0,y)^2/P(0,y)^3\) has not been controlled;
2. the cusp-complement comparison is an optional route to excluding the
   signature, not a proved consequence of the outer edge.

The exact finite calculations in this audit are reproduced by
`route_bd_radial_cusp_complement_audit.py`.

## 7. Why polynomial parametrization of nonproper components does not close
the missing-end argument

Chau's polynomial-parametrization theorem does not contradict the
single-signature connection.  There are three separate reasons.

First, the theorem applies to a polynomial map with everywhere nonzero
constant Jacobian.  The bounded normal form used here has
\([P,Q]=x^2\), so applying the theorem requires a justified transfer back
to the original Keller map.

Second, even after such a transfer, a missing finite nonzero cusp parameter
\(\tau_0\) says only that the cusp point
\[
(\tau_0^2,\sqrt L\,\tau_0^3)
\]
lies on some nonproper component \(\Lambda\).  It does not say that an open
dense subset of \(\Lambda\) is parametrized by \(\tau\), and hence does not
force \(\widetilde\Lambda\simeq\mathbf G_m\).  An allowed polynomially
parametrized \(\mathbf A^1\)-component can meet the cusp in finitely many
nonzero points.  The shear stress test
\(\Lambda=\{p=q^2\}\) exhibits exactly this incidence.

Third, even the cusp itself is not prohibited: its normalization is
\[
\mathbf A^1\longrightarrow C_L,\qquad
\tau\longmapsto(\tau^2,\sqrt L\,\tau^3).
\]
Only after deleting the cusp origin does the normalization become
\(\mathbf G_m\).  Thus the appearance of \(\mathbf G_m\) in the
cusp-complement argument is caused by removing \(\tau=0\), not by a
two-ended normalization of a complete nonproper component.

Therefore the identity/infinity connection forces at most an allowed
\(\mathbf A^1\)-component meeting \(C_L\), not a forbidden
\(\mathbf G_m\)-normalized component.  Polynomial parametrization supplies
no contradiction without an additional theorem showing that the same
nonproper component is exhausted by all nonzero cusp parameters and cannot
acquire the missing \(\tau=0\) point in its normalization.
