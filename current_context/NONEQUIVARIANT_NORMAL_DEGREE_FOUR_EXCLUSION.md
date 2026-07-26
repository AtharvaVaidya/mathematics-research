# Non-equivariant normal degree four: exact exclusion

Date: 26 July 2026

## Outcome

Let \(K=\mathbf C\), and write
\[
 [U,V]_{x,y}=U_xV_y-U_yV_x.
\]
This note proves the next coefficient-level obstruction after
`NONEQUIVARIANT_NODAL_LOW_NORMAL_DEGREE_OBSTRUCTIONS.md`.

> **Theorem.** There are no \(F,G\in K[x,y]\) such that
> \[
>   [F,G]_{x,y}\in K^\times,\qquad
>   (\deg_yF,\deg_yG)=(4,3).
> \tag{1}
> \]

Together with elementary target shears, this has two consequences.

> **Corollary 1.** If a Keller pair has maximum \(y\)-degree four, a
> polynomial target automorphism reduces both \(y\)-degrees to at most
> three.

> **Corollary 2.** If a Keller map is noninjective on the line \(y=0\),
> then
> \[
>   \boxed{\max(\deg_yF,\deg_yG)\geq5.}
> \tag{2}
> \]
> In particular, every plane Keller map of maximum \(y\)-degree at most
> four is an automorphism.

For the last assertion, the preceding low-normal-degree note proves
injectivity of the boundary after the degree reduction.  The
injectivity-on-one-line theorem of Gwoździewicz then gives
invertibility; see V. Shpilrain and J.-T. Yu, *Polynomial retracts and
the Jacobian conjecture*, Trans. Amer. Math. Soc. **352** (2000),
477--484, Corollary 1.5
([preprint](https://arxiv.org/abs/math/9701210)).

### Relation to a prior partial-degree claim

Moskowicz,
[*A variation on Magnus' theorem and its generalizations*,
Theorem 2.7](https://arxiv.org/abs/1810.08202), gives the stronger
criterion that a Keller map is invertible whenever even one coordinate
has \(y\)-degree at most four.  One route through the printed proof
invokes Theorem 2.4 and the number-theoretic Lemma 2.3.  That lemma is
false as stated: for
\[
 (a,b,c,d,\epsilon)=(1,1,2,1,2),
\]
its two linear forms are \(L+1,L+2\), while the conclusion requires
both to be coprime to \(2\).  Consecutive integers cannot both be odd.
The corresponding proposed degree tuple
\((n,u,r,v)=(1,1,2,4)\) is not a realizable Keller branch, because the
top Jacobian coefficient forces \(nv=ru\).  More generally, for
\(u,v>0\) that equality makes the two reduced degree pairs identical,
so the unequal-pair branch of Theorem 2.4 is vacuous for Keller data.

The stronger theorem is also repairable without Lemma 2.3.  Writing
\(n=A\widetilde n\), \(u=A\widetilde u\) with coprime reduced degrees,
the partial-degree hypothesis gives \(A\mid n\le4\), hence
\(A\in\{1,2,3,4\}\).  Dirichlet gives arbitrarily large \(L\) for which
\(\widetilde u+L\widetilde n\) is prime.  The source shear
\(y\mapsto y+x^L\) then puts the relevant total degree in the
prime, four-times-prime, or product-of-two-primes class treated by the
classical Magnus-type criteria used in that paper.  If \(u=0<n\),
take \(L\) itself to be a sufficiently large prime and use the same
argument; the zero-\(n\) case is triangular.  Thus the theorem
statement should be regarded as prior art even though the auxiliary
lemma is defective.

The exact \((4,3)\) nonexistence statement is also a short consequence
of that repaired result and M. Karaś,
*On weighted bidegree of polynomial automorphisms of
\(\mathbf C^2\)*, Bull. Polish Acad. Sci. Math. **70** (2022),
107--114, Theorem 1.1
([DOI](https://doi.org/10.4064/ba220430-21-3)).
The leading equation gives
\(f_4=\alpha h^4,\ g_3=\beta h^3\).  For weight \((1,N)\), with \(N\)
larger than every lower coefficient \(x\)-degree, the weighted
coordinate degrees are
\[
4(N+\deg h),\qquad3(N+\deg h).
\]
Moskowicz first makes the Keller pair an automorphism, whereas Karaś's
classification requires divisibility between these non-base weighted
degrees.  Neither divides the other.

The theorem in this note is an independent coefficient proof only of
the simultaneous bound \(\max(\deg_yF,\deg_yG)\leq4\).  It neither
invokes Lemma 2.3 nor claims novelty for the theorem statement.  Its
value is the explicit rational normal form and local valuation proof
for the exact \((4,3)\) coefficient system.

The proof is not a bounded search.  It first integrates the entire
degree-\((4,3)\) coefficient system over \(K(x)\).  At every zero of
the common leading factor \(h\), the remaining constant equation fixes
the possible order of the one rational parameter.  Restoring just the
two polynomial boundary coefficients then gives a noncancelling
leading pole.  A separate calculation treats the chart on which that
rational parameter vanishes identically.

This is a scoped partial-degree theorem, not a proof of the plane
Jacobian conjecture and not a claim of priority over the statement of
the 2018 result.

## 1. Why \((4,3)\) is the only new degree-four case

Suppose
\[
 U=u_m(x)y^m+\cdots,\qquad V=v_n(x)y^n+\cdots
\]
with \(u_m v_n\ne0\).  The coefficient of \(y^{m+n-1}\) in
\([U,V]_{x,y}\) is
\[
 n u_m'v_n-mu_mv_n'.
\tag{3}
\]

If \((m,n)=(4,4)\), equation (3) says that \(u_4/v_4\) is constant.
A constant linear target shear removes one quartic term.  After
possibly interchanging the target coordinates, it is enough to
consider \((4,n)\) with \(n\leq3\).

If \(n=1\), (3) gives \(u_4=c v_1^4\).  The target shear
\[
 U\longmapsto U-cV^4
\tag{4}
\]
lowers the maximum \(y\)-degree to at most three.  If \(n=2\), it gives
\(u_4=cv_2^2\), and
\[
 U\longmapsto U-cV^2
\tag{5}
\]
does the same.  If \(n=0\), the coefficient of \(y^3\) in the
Jacobian is \(-4u_4V'\), so \(V'=0\), contradicting a nonzero constant
Jacobian.  Thus only \((4,3)\) is not already reduced.

## 2. Monic normalization over \(K(x)\)

Assume (1), and write the leading coefficients as \(f_4,g_3\).
Equation (3) becomes
\[
 3f_4'g_3-4f_4g_3'=0.
\tag{6}
\]
Thus \(f_4^3/g_3^4\in K^\times\).  Unique factorization in \(K[x]\)
gives
\[
 f_4=\alpha h^4,\qquad g_3=\beta h^3
\tag{7}
\]
for \(h\in K[x]\setminus\{0\}\) and
\(\alpha,\beta\in K^\times\).  Rescale the target coordinates by
constants and put
\[
 z=h(x)y.
\tag{8}
\]
Over \(K(x)\), the pair now has the form
\[
\begin{aligned}
 F&=z^4+A z^3+B_0z^2+C_0z+P_0,\\
 G&=z^3+D z^2+E_0z+Q_0 .
\end{aligned}
\tag{9}
\]
The change (8) satisfies
\[
 [F,G]_{x,y}=h[F,G]_{x,z},
\tag{10}
\]
where the \(x\)-derivatives on the right hold \(z\) fixed.  Hence
\[
 [F,G]_{x,z}=\frac{\lambda}{h}
\tag{11}
\]
for some \(\lambda\in K^\times\).

The coefficient of \(z^5\) in (11) is
\[
 3A'-4D'=0.
\tag{12}
\]
Therefore \(a=A-\frac43D\in K\).  Set
\[
 t=\frac D3,\qquad w=z+t,
\tag{13}
\]
and apply the constant target shear \(F\mapsto F-aG\).  Translation by
the \(x\)-dependent rational function \(t\) preserves
\([\,\cdot,\cdot\,]_{x,z}\), because \(dw\wedge dx=dz\wedge dx\).
We arrive at the depressed pair
\[
\boxed{
\begin{aligned}
 f&=w^4+Bw^2+Cw+P,\\
 g&=w^3+Ew+Q,
\end{aligned}}
\tag{14}
\]
still satisfying \([f,g]_{x,w}=\lambda/h\).

The translation (13) is used only over \(K(x)\).  It need not be a
polynomial source automorphism.  Polynomiality will be restored
explicitly in Section 4.

## 3. Complete integration of the depressed system

Expansion of (14) gives
\[
\begin{aligned}
 [w^4]:\quad&3B'-4E'=0,\\
 [w^3]:\quad&3C'-4Q'=0,\\
 [w^2]:\quad&-2BE'+EB'+3P'=0,\\
 [w^1]:\quad&-2BQ'-CE'+EC'=0,\\
 [w^0]:\quad&-CQ'+EP'=\lambda/h.
\end{aligned}
\tag{15}
\]
The first three equations integrate to
\[
\boxed{
 B=\frac{4E+k}{3},\qquad
 C=\frac{4Q+l}{3},\qquad
 P=\frac{2E^2}{9}+\frac{2kE}{9}+M
}
\tag{16}
\]
for constants \(k,l,M\in K\).  The fourth has the first integral
\[
\boxed{4EQ+2kQ+lE=N}
\tag{17}
\]
with \(N\in K\).

Put
\[
 r=2E+k,\qquad \Delta=lk+2N.
\tag{18}
\]
There are two charts.

### 3.1 The generic chart \(r\ne0\)

Solving (17) in \(K(x)\) gives
\[
\boxed{
\begin{aligned}
 E&=\frac{r-k}{2},&
 Q&=-\frac l4+\frac{\Delta}{4r},\\
 B&=\frac{2r-k}{3},&
 C&=\frac{\Delta}{3r},\\
 P&=\frac{r^2-k^2}{18}+M.
\end{aligned}}
\tag{19}
\]
The constant coefficient in (15) is
\[
\begin{aligned}
 -CQ'+EP'
 &=r'\left(
 \frac{r(r-k)}{18}+\frac{\Delta^2}{12r^3}
 \right)\\
 &=\frac d{dx}\left(
 \frac{r^3}{54}-\frac{kr^2}{36}
 -\frac{\Delta^2}{24r^2}
 \right).
\end{aligned}
\tag{20}
\]
Thus, with
\[
 \mathcal H(T)=
 \frac{T^3}{54}-\frac{kT^2}{36}
 -\frac{\Delta^2}{24T^2},
\tag{21}
\]
the last equation is exactly
\[
 \boxed{(\mathcal H(r))'=\lambda/h.}
\tag{22}
\]

### 3.2 The degenerate chart \(r=0\)

Division by \(r\) would lose this chart.  Here
\[
 E=-\frac k2,\quad B=-\frac k3,\quad
 P=M-\frac{k^2}{18},\quad C=\frac{4Q+l}{3},
\tag{23}
\]
and (17) merely says \(N=-lk/2\).  The last equation becomes
\[
 \boxed{
 \left(-\frac23Q^2-\frac l3Q\right)'=\lambda/h.
 }
\tag{24}
\]

Equations (19)--(24) are an exact parametrization of every rational
depressed solution.

## 4. Returning to the polynomial coefficients

It is useful to undo the translation without assuming that it was
polynomial.  Since \(t=D/3\), equation (14) gives
\[
\boxed{
\begin{aligned}
G={}&h^3y^3+h^2Dy^2
+h\left(\frac{D^2}{3}+E\right)y
+\left(\frac{D^3}{27}+\frac{ED}{3}+Q\right),\\
F-aG={}&h^4y^4+\frac43h^3Dy^3
+h^2\left(\frac{2D^2}{3}+B\right)y^2\\
&+h\left(\frac{4D^3}{27}+\frac{2BD}{3}+C\right)y\\
&+\left(\frac{D^4}{81}+\frac{BD^2}{9}
+\frac{CD}{3}+P\right).
\end{aligned}}
\tag{25}
\]
Every displayed coefficient is a polynomial.  In particular,
\[
 q_0=\frac{D^3}{27}+\frac{ED}{3}+Q,\qquad
 p_0=\frac{D^4}{81}+\frac{BD^2}{9}+\frac{CD}{3}+P
\tag{26}
\]
are regular at every finite point.  Also \(h^2D\in K[x]\), so a pole
of \(D\) can occur only at a zero of \(h\).

In the generic chart, (20) and (10) say directly
\[
\boxed{
\lambda=h r'W(r),\qquad
W(r)=\frac{r(r-k)}{18}+\frac{\Delta^2}{12r^3}.
}
\tag{27}
\]
This identity and the regularity of (26) exclude every zero of \(h\).

## 5. The generic chart has no zero of \(h\)

Fix a zero \(s=x-a\) of \(h\), and write \(e=v_s(h)>0\).
There are three exhaustive cases.

### 5.1 The parameter \(r\) has a pole

Suppose \(v_s(r)=-\beta<0\).  Then
\[
 v_s(r')=-\beta-1,\qquad v_s(W)=-2\beta,
\]
so (27) forces
\[
 e=3\beta+1.
\tag{28}
\]
The functions \(Q\) and \(C\) in (19) are regular at \(s=0\), whereas
\(E\sim r/2\), \(B\sim2r/3\), and \(P\sim r^2/18\).

If \(D\) is regular, then \(P\sim r^2/18\) is the unique lowest term
of \(p_0\), already a contradiction.  Thus \(D\) has a pole.  Put
\(v_s(D)=-\alpha<0\).  Regularity of \(q_0\) says that its two
possible lowest terms, \(D^3/27\) and \(ED/3\), must cancel, so
\[
 \beta=2\alpha.
\tag{29}
\]
If \(r=\rho s^{-\beta}+\cdots\) and
\(D=d s^{-\alpha}+\cdots\), their leading cancellation gives
\[
 \frac{\rho}{d^2}=-\frac29.
\tag{30}
\]
In \(p_0\), the three terms of order \(-4\alpha\) have, after division
by \(d^4\), leading coefficient
\[
 \frac1{81}+\frac2{27}\frac{\rho}{d^2}
+\frac1{18}\left(\frac{\rho}{d^2}\right)^2
=-\frac1{729}\ne0.
\tag{31}
\]
Thus \(p_0\) has a pole, a contradiction.

### 5.2 The parameter \(r\) has a zero

Suppose \(v_s(r)=\beta>0\).  If \(\Delta=0\), then
\(v_s(hr'W)>0\), whether \(k=0\) or \(k\ne0\), immediately
contradicting (27).  Hence \(\Delta\ne0\).  Now
\[
 v_s(r')=\beta-1,\qquad v_s(W)=-3\beta,
\]
and (27) forces
\[
 e=2\beta+1.
\tag{32}
\]

Here \(Q\sim\Delta/(4r)\) and \(C\sim\Delta/(3r)\).
Regularity of \(q_0\) forces \(D\) to have a pole of order
\(\alpha>0\).  The only possible lowest cancellation is between
\(D^3/27\) and \(Q\): indeed
\(v_s(ED)\ge-\alpha>-3\alpha\).  Therefore
\[
 \beta=3\alpha,\qquad
 \frac{d^3}{27}+\frac{\Delta}{4\rho}=0,
\tag{33}
\]
where \(r=\rho s^\beta+\cdots\) and
\(D=d s^{-\alpha}+\cdots\).
The terms \(D^4/81\) and \(CD/3\) in \(p_0\) then both have order
\(-4\alpha\).  Their normalized leading coefficient is
\[
 \frac1{81}+\frac{\Delta}{9\rho d^3}
=\frac1{81}-\frac4{243}
=-\frac1{243}\ne0.
\tag{34}
\]
All other terms have higher order.  Again \(p_0\) has a pole.

### 5.3 The parameter \(r\) is a local unit

If \(v_s(r)=0\), then \(r'\) and \(W(r)\) are regular at \(s=0\).
Thus \(v_s(hr'W)>0\), contradicting (27).

All three cases are impossible.  Therefore \(h\) has no zero and is a
nonzero constant.

With \(h\) constant, polynomiality in (25) first gives
\(D\in K[x]\), then \(E,r,B\in K[x]\).  If \(\Delta\ne0\), the
coefficient of \(y\) in \(F-aG\) shows that
\(C=\Delta/(3r)\) is a polynomial.  Hence \(r\) is a unit, and (27)
vanishes, a contradiction.  If \(\Delta=0\), equation (27) is
\[
 \lambda=\frac h{18}r'r(r-k).
\tag{35}
\]
No constant or nonconstant polynomial \(r\) makes the right side a
nonzero constant.  This excludes the generic chart.

## 6. The degenerate chart \(r=0\)

It remains to exclude (23)--(24).  In original coordinates,
\[
 \boxed{\lambda=-\frac h3(4Q+l)Q'.}
\tag{36}
\]
At a zero \(s=x-a\) of \(h\), a locally regular \(Q\) makes the
right-hand side nonunit.  Hence \(Q\) would have to have a pole, say
\[
 v_s(Q)=-\beta<0.
\]
Equation (36) forces
\[
 e=v_s(h)=2\beta+1.
\tag{37}
\]

Here \(E=-k/2\), \(B=-k/3\), and \(P=M-k^2/18\).  Regularity of
\(q_0\) in (26) forces \(D\) to have a pole of order \(\alpha\), with
\(v_s(ED)\ge-\alpha>-3\alpha\), so only \(D^3/27\) and \(Q\) can
occur at the lowest order.  Hence
\[
 \beta=3\alpha,\qquad
 \frac{d^3}{27}+\rho=0
\tag{38}
\]
for \(D=d s^{-\alpha}+\cdots\) and
\(Q=\rho s^{-\beta}+\cdots\).
The lowest terms of \(p_0\) are \(D^4/81\) and \(CD/3\).  Their
normalized leading coefficient is
\[
 \frac1{81}+\frac{4\rho}{9d^3}
=\frac1{81}-\frac4{243}
=-\frac1{243}\ne0.
\tag{39}
\]
This contradicts regularity of \(p_0\).  Thus \(h\) has no zero.

Finally, if \(h\) is constant, (25) gives \(D,Q\in K[x]\).
Equation (36) cannot be a nonzero constant: it vanishes for constant
\(Q\), while for nonconstant \(Q\) its degree is \(2\deg Q-1\geq1\).
The degenerate chart is impossible.  This completes the proof.

## Verification

Run

```bash
.venv/bin/python \
  current_context/verify_nonequivariant_normal_degree_four_exclusion.py
```

The verifier expands the general and depressed Jacobians, checks every
first integral and both constant terms, verifies the inverse
translation formula, checks all low-degree target shears, and confirms
the two terminal leading-coefficient contradictions.
