# Exclusion of the full normal-degree \((12,9)\) frontier

Date: 26 July 2026

The local input includes the honest ramified grading.  In particular,
the half-order resonance, all eight Hensel branches, the exceptional
earlier and later indirect chains, arbitrary upper constants, and all
finer rational support characters are included in the cited local
theorem.

## Outcome

Let
\[
 [F,G]_{x,y}=\lambda\in\mathbf C^\times,\qquad
 \deg_yF=12,\qquad \deg_yG=9,
\tag{1}
\]
and suppose this is the \(t=3\) arithmetic normal-degree chart.  Thus
the leading coefficients have the form
\[
 F_{12}=h^4,\qquad G_9=h^3,\qquad
 \gcd(3,\deg h)=3.
\tag{2}
\]
Then \(F,G\) cannot be a noninvertible Keller pair.

The proof combines:

1. the local degree-nine pole theorem
   \[
   \operatorname {pole}(A_8)\geq\frac72\rho;
   \tag{3}
   \]
2. the exact inverse-character differential classification on
   \(H^3=h\);
3. injectivity on one source line;
4. the established total-degree lower bound \(125\) for a plane
   Keller counterexample.

This closes the split cube chart, the constant cube chart, and the
connected noncube chart at \((12,9)\).  It is a normal-degree theorem,
not a proof of the plane Jacobian conjecture in arbitrary degree.

## 1. Normalization and terminal time

On the cubic cover
\[
 H^3=h,\qquad z=Hy,
\tag{4}
\]
depress the monic lower coordinate and write
\[
 g=w^9+\sum_{j=2}^9c_jw^{9-j},\qquad
 s=g^{1/9}=w+O(w^{-1}).
\tag{5}
\]
At fixed \(s\), expand
\[
 f=\Phi(s)+\sum_{\ell\geq1}A_\ell s^{-\ell}.
\tag{6}
\]
The normalized bracket gives
\[
 A_1'=\cdots=A_7'=0,\qquad
 9A_8'=\frac{\lambda}{H}.
\tag{7}
\]
At any place of the coefficient field set
\[
 \rho=\max_{2\leq j\leq9}
 \frac{\operatorname {pole}(c_j)}j.
\tag{8}
\]
The local theorem proved in
`NORMAL_DEGREE_129_LOCAL_POLE_THRESHOLD.md` is
\[
 \boxed{\operatorname {pole}(A_8)\geq\frac72\rho.}
\tag{9}
\]
It is local after a finite ramified extension and includes all upper
approximate-root constants.  It therefore applies both on a split
chart and at a place of the connected cubic normalization.

## 2. The split cube chart

Suppose first that \(h=r^3\) with \(r\in\mathbf C[x]\).  Then
\[
 [f,g]_{x,w}=\frac{\lambda}{r},\qquad
 T=9A_8,\qquad T'=\frac{\lambda}{r}.
\tag{10}
\]

If \(r\) is nonconstant, rational-time classification gives
\[
 T=\alpha+\beta(x-a)^{-k},\qquad
 r=\gamma(x-a)^{k+1}.
\tag{11}
\]
Put \(u=x-a\), and compute all pole orders directly in this
coordinate.  Since \(A_8\) has pole order \(k\), (9) gives
\[
 k\geq\frac72\rho.
\tag{12}
\]
Let \(\tau(u)\) be the depressing center.  Polynomiality of
\(G(u,0)=g(u,\tau(u))\) gives
\[
 \operatorname {pole}_0(\tau)\leq\rho.
\tag{13}
\]
Writing \(G=\sum_iG_i(u)y^i\) and expanding after
\(w=\gamma u^{k+1}y+\tau\) yields
\[
 \operatorname {ord}_0G_i
 \geq i(k+1)-(9-i)\rho.
\]
For \(i\geq2\), the right side is at least
\[
 \left(\frac92i-9\right)\rho+i>0.
\]
Thus \(G(a,y)\) is affine.  If it is nonconstant, the second
coordinate is injective on \(x=a\).  If it is constant, the Keller
identity makes \(F(a,y)\) affine and nonconstant.  Gwoździewicz's
one-line theorem makes the map an automorphism.  This direct estimate
avoids any field-descent hypothesis.

Now let \(r\) be constant.  Then \(A_8\) is affine, and at infinity
\[
 \operatorname {pole}_\infty(A_8)=1.
\]
The coefficient curve of \(g\) is nonconstant.  Otherwise every
\(c_j\) would be constant, and the fixed-\(s\) bracket identity would
make a polynomial \(f_x\) times the nonconstant polynomial \(g_w\)
equal to \(\lambda/r\), which is impossible.  Hence \(\rho>0\), and
(9) gives
\[
 \rho\leq\frac27.
\tag{14}
\]
The coefficient of \(w^{9-j}\) in \(g\) has \(x\)-degree at most
\(2j/7\).  For completeness, polynomiality says
\[
 f=(\Phi(g^{1/9}))_+.
\]
The coefficient of deficit \(k\) in the leading \(s^{12}\)-term is
a weighted polynomial of total coefficient weight \(k\) in the
\(c_j\).  A lower constant term \(s^\ell\) uses weight at most \(k\)
at the same \(w\)-coefficient.  Therefore every coefficient of
deficit \(k\) in \(f\) has \(x\)-degree at most \(2k/7\).
Consequently
\[
 \deg_{\rm tot}g\leq9,\qquad
 \deg_{\rm tot}f\leq12.
\tag{15}
\]
The independently established lower bound \(125\) for a
noninvertible Keller map excludes this pair.

## 3. The connected noncube chart

Assume \(h\) is not a cube.  Since three is prime,
\(\mathbf C(x,H)/\mathbf C(x)\) is connected.  The deck action sends
\[
 H\longmapsto\zeta H,\qquad
 w\longmapsto\zeta w.
\]
Because \(8\equiv-1\pmod3\), the terminal coefficient lies in the
inverse character:
\[
 A_8=\frac{S}{H},\qquad S\in\mathbf C(x).
\tag{16}
\]
Equation (7) becomes
\[
 3S'-\frac{h'}hS=\frac{\lambda}{3}.
\tag{17}
\]

The exact Kummer differential classification makes \(S\) a
nonconstant squarefree polynomial.  If
\[
 S=L\prod_i(x-a_i),
\]
then
\[
 h=C\prod_i(x-a_i)^{M_i},\qquad
 M_i=3-\frac{\lambda}{3S'(a_i)}
 \in\mathbf Z_{\geq0},\qquad M_i\ne3.
\tag{18}
\]
When \(\deg S\geq2\), the integers \(3-M_i\) sum to zero.  Some
\(M_i>3\), and \(A_8\) has a finite pole over \(a_i\).

The one-root alternative is
\[
 h=C(x-a)^M,\qquad M\ne3.
\tag{19}
\]
But (2) says \(3\mid M\).  If \(M=0\), \(h\) is a constant cube.  If
\(M>0\), (19) is a cube in \(\mathbf C[x]\).  Thus every genuinely
noncube chart has a finite terminal pole.

Choose \(M>3\), put
\[
 d_0=\gcd(3,M),\qquad
 e=\frac3{d_0},\qquad
 h_0=\frac{M}{d_0},\qquad
 n=h_0-e,
\tag{20}
\]
and choose a local parameter \(t\) such that
\[
 x-a=t^e\cdot(\text{unit}),\qquad
 H=t^{h_0}\cdot(\text{unit}).
\tag{21}
\]
Since \(S\) has a simple zero at \(a\),
\[
 \operatorname {pole}_t(A_8)=n,\qquad
 [f,g]_{t,w}=(\text{unit})t^{-n-1}.
\tag{22}
\]
The local theorem gives
\[
 n\geq\frac72\rho.
\tag{23}
\]

Let \(\tau(t)\) be the depressing center.  Regularity of
\(G(x(t),0)=g(t,\tau(t))\) gives
\[
 \operatorname {pole}_t(\tau)\leq\rho.
\tag{24}
\]
If \(G=\sum_iG_i(x)y^i\), Taylor expansion after
\(w=Hy+\tau\) gives
\[
 \operatorname {ord}_tG_i(x(t))
 \geq i h_0-(9-i)\rho.
\tag{25}
\]
For \(i\geq2\), equations (20) and (23) imply
\[
\begin{aligned}
 i h_0-(9-i)\rho
 &=i(n+e)-(9-i)\rho\\
 &\geq\left(\frac92i-9\right)\rho+ie>0.
\end{aligned}
\tag{26}
\]
Thus
\[
 G_i(a)=0\qquad(i\geq2),
\]
and \(G(a,y)\) is affine.  If it is nonconstant, it separates the
line \(x=a\).  If it is constant, the Keller identity makes
\(F(a,y)\) affine and nonconstant.  The one-line theorem again makes
the map an automorphism.

This eliminates the connected noncube chart and completes the full
normal-degree \((12,9)\) exclusion.

## 4. Scope

The proof closes all leading-factor possibilities at this frontier:

* nonconstant cubes;
* constant cubes;
* connected cubic Kummer covers.

The local threshold is special to lower normal degree nine.  Later
frontiers require new invariant-boundary estimates.
