# Exclusion of the full normal-degree \((15,6)\) frontier

Date: 25 July 2026

## Outcome

Let
\[
 [F,G]_{x,y}=\lambda\in\mathbf C^\times,\qquad
 \deg_yF=15,\qquad \deg_yG=6,
\tag{1}
\]
and suppose this is the cubic arithmetic normal-degree chart:
\[
 F_{15}=h^5,\qquad G_6=h^2,\qquad
 3\mid\deg h.
\tag{2}
\]
Then \(F,G\) cannot be a noninvertible Keller pair.

The proof uses:

1. the all-character local pole theorem
   \[
   \operatorname {pole}(A_5)\ge2\rho;
   \tag{3}
   \]
2. exact inverse-character differentials on \(H^3=h\);
3. injectivity on one source line; and
4. the established total-degree lower bound \(125\) for a plane
   Keller counterexample.

This closes the nonconstant cube, constant cube, and connected
noncube leading-factor charts.

## 1. Cubic-cover normalization and the local input

On the cubic cover
\[
 H^3=h,\qquad z=Hy,
\tag{4}
\]
make the lower coordinate monic, depress it, and write
\[
 g=w^6+c_2w^4+c_3w^3+c_4w^2+c_5w+c_6,
\qquad s=g^{1/6}=w+O(w^{-1}).
\tag{5}
\]
The triangular approximate-root argument gives
\[
 f=(\Phi(g^{1/6}))_+,
\tag{6}
\]
where every coefficient of \(\Phi\) is constant.  At fixed \(s\),
\[
 f=\Phi(s)+\sum_{\ell\ge1}A_\ell s^{-\ell},
\tag{7}
\]
and the normalized bracket gives
\[
 A_1'=\cdots=A_4'=0,\qquad
 6A_5'=\frac{\lambda}{H}.
\tag{8}
\]

At a place of the coefficient field where \(A_5\) has positive pole
order, after an arbitrary finite ramified extension, put
\[
 \rho=\max_{2\le j\le6}
 \frac{\operatorname {pole}(c_j)}j.
\tag{9}
\]
The positive-terminal-pole local theorem proved in
`Q6_ODD_LOCAL_SUBEXTREMAL_AND_156_NODAL_HENSEL_AUDIT.md` is
\[
 \boxed{\operatorname {pole}(A_5)\ge2\rho.}
\tag{10}
\]
It retains every upper constant, every rational support character,
and every delayed moving-cubic character.  It therefore applies on
both split and connected cubic covers.

## 2. The split cube chart

Suppose first that
\[
 h=r^3,\qquad r\in\mathbf C[x]\setminus\{0\}.
\tag{11}
\]
Then
\[
 [f,g]_{x,w}=\frac{\lambda}{r},\qquad
 T=6A_5,\qquad T'=\frac{\lambda}{r}.
\tag{12}
\]

### 2.1 Nonconstant \(r\)

The rational-time classification gives, after \(u=x-a\),
\[
 T=\alpha+\beta u^{-k},\qquad
 r=\gamma u^{k+1},\qquad k\ge1.
\tag{13}
\]
Thus \(A_5\) has pole order \(k\), and (10) gives
\[
 k\ge2\rho.
\tag{14}
\]

Let \(\tau(u)\) be the depressing center.  Polynomiality of
\(G(u,0)=g(u,\tau(u))\) gives
\[
 \operatorname {pole}_0(\tau)\le\rho.
\tag{15}
\]
If \(G=\sum_{i=0}^6G_i(u)y^i\), expansion after
\[
 w=\gamma u^{k+1}y+\tau
\tag{16}
\]
gives
\[
 \operatorname {ord}_0G_i
 \ge i(k+1)-(6-i)\rho.
\tag{17}
\]
For every \(i\ge2\), (14) implies
\[
 i(k+1)-(6-i)\rho
 \ge(3i-6)\rho+i>0.
\tag{18}
\]
Hence \(G(a,y)\) is affine.  If it is nonconstant, it separates the
points of the line \(x=a\).  If it is constant, restriction of the
Keller identity makes \(F(a,y)\) affine and nonconstant.
Gwoździewicz's injectivity-on-one-line theorem makes the pair an
automorphism.

### 2.2 Constant \(r\)

If \(r\) is constant, then \(A_5\) is affine.  At infinity,
\[
 \operatorname {pole}_\infty(A_5)=1.
\tag{19}
\]
The depressed coefficient curve is nonconstant: otherwise (8)
would make a polynomial \(f_x\) times the nonconstant polynomial
\(g_w\) equal a nonzero constant.  Therefore \(\rho>0\), and (10)
gives
\[
 \rho\le\frac12.
\tag{20}
\]

The coefficient \(c_j\) has \(x\)-degree at most \(j/2\).
Every coefficient of \(w^{15-k}\) in (6) is a weighted polynomial
of coefficient weight at most \(k\), so it has \(x\)-degree at most
\(k/2\).  Consequently
\[
 \deg_{\rm tot}G\le6,\qquad
 \deg_{\rm tot}F\le15.
\tag{21}
\]
The established lower bound
\(\max(\deg F,\deg G)\ge125\) for a noninvertible plane Keller pair
excludes this chart.

## 3. The connected noncube chart

Assume \(h\) is not a cube in \(\mathbf C(x)\).  Since three is
prime, the cover \(H^3=h\) is connected.  Its deck action sends
\[
 H\longmapsto\zeta H,\qquad
 w\longmapsto\zeta w.
\tag{22}
\]
Because \(5\equiv-1\pmod3\), the terminal coefficient is in the
inverse character:
\[
 A_5=\frac{S}{H},\qquad S\in\mathbf C(x).
\tag{23}
\]
Equation (8) becomes
\[
 3S'-\frac{h'}hS=\frac{\lambda}{2}.
\tag{24}
\]

The exact Kummer differential classification makes \(S\) a
nonconstant squarefree polynomial.  If
\[
 S=L\prod_i(x-a_i),
\tag{25}
\]
then
\[
 h=C\prod_i(x-a_i)^{M_i},\qquad
 M_i=3-\frac{\lambda}{2S'(a_i)}
 \in\mathbf Z_{\ge0},\qquad M_i\ne3.
\tag{26}
\]
If there are at least two roots, the integers \(3-M_i\) sum to
zero.  Hence some \(M_i>3\), and \(A_5\) has a finite pole above
\(a_i\).

The one-root alternative is
\[
 h=C(x-a)^M,\qquad M\ne3.
\tag{27}
\]
Condition (2) gives \(3\mid M\).  If \(M=0\), \(h\) is a constant
cube; if \(M>0\), (27) is a cube in \(\mathbf C[x]\).  Thus every
genuinely connected chart has a finite terminal pole.

Choose a root with \(M>3\), and put
\[
 d_0=\gcd(3,M),\qquad
 e=\frac3{d_0},\qquad
 h_0=\frac M{d_0},\qquad
 n=h_0-e.
\tag{28}
\]
There is a local parameter \(t\) for which
\[
 x-a=t^e\cdot(\text{unit}),\qquad
 H=t^{h_0}\cdot(\text{unit}),
\tag{29}
\]
and, because \(S\) has a simple zero,
\[
 \operatorname {pole}_t(A_5)=n.
\tag{30}
\]
The local theorem gives
\[
 n\ge2\rho.
\tag{31}
\]

Let \(\tau(t)\) be the depressing center.  Regularity of
\(G(x(t),0)\) gives
\[
 \operatorname {pole}_t(\tau)\le\rho.
\tag{32}
\]
Taylor expansion after \(w=Hy+\tau\) gives
\[
 \operatorname {ord}_tG_i(x(t))
 \ge ih_0-(6-i)\rho.
\tag{33}
\]
For \(i\ge2\), equations (28) and (31) imply
\[
\begin{aligned}
 ih_0-(6-i)\rho
 &=i(n+e)-(6-i)\rho\\
 &\ge(3i-6)\rho+ie>0.
\end{aligned}
\tag{34}
\]
Therefore \(G_i(a)=0\) for \(i\ge2\), and \(G(a,y)\) is affine.
The same line-injectivity argument as in the split chart makes the
Keller pair an automorphism.

## 4. Conclusion and scope

Every leading-factor possibility is now excluded:

* a nonconstant cube by (13)--(18);
* a constant cube by (19)--(21); and
* a connected noncube by (22)--(34).

Thus the full arithmetic normal-degree \((15,6)\) frontier is
closed.  This is a normal-degree theorem, not a proof of the plane
Jacobian conjecture in arbitrary degree.

The arithmetic and valuation identities are checked in
`verify_normal_degree_156_full_exclusion.py`.
