# A normalized one-pole cusp at \((12,8)\) and its exact lift obstruction

Date: 26 July 2026

## Outcome

At the next normal-degree frontier
\[
 (\deg_yF,\deg_yG)=(12,8),
\]
the fourth-power chart has the same Laurent-time structure as the
cube chart at \((9,6)\), with one important numerical change.  After
normalization and depression there are six conserved Laurent
coefficients \(A_1,\ldots,A_6\), and
\[
 8A_7'=\frac{\lambda}{r}.
\]
The pure-power reduction therefore again has
\[
 v=u^m,\qquad r=\gamma u^{mn+1},\qquad
 8A_7=\alpha+\beta v^{-n}.
\]
For a depressed monic octic, the line-injectivity descent needs the
weighted pole bound
\[
 n\geq3\rho,
\]
rather than the bound \(n\geq2\rho\) which sufficed for a sextic.

There is a nontrivial exact rational invariant curve satisfying every
normalized condition.  It has one-pole time
\[
 A_7=-\frac{2^{18}\sqrt{21}}{3^7\,7^{10}}v^{-19}
\]
and normalized Jacobian
\[
 [f,g]_{v,w}
 =\frac{2^{21}19\sqrt{21}}{3^7\,7^{10}}v^{-20}.
\]
Its coefficient pole scale is \(\rho=1\), so its ratio is
\[
 \frac{\operatorname{pole}(A_7)}{\rho}=19.
\]
Thus it does not evade the degree-eight line threshold.

More strongly, this cusp cannot be the normalization of a polynomial
pair for **any** rational depressing center.  Its homogeneous binary
forms \(F_0,G_0\) have
\[
 \operatorname {Res}(F_0,G_0)
 =-\frac{2^{88}19^2}{3^{36}7^{48}}\ne0.
\]
Polynomiality at the root \(u=0\) would force the bounded center
parameter to tend to a common zero of \(F_0,G_0\), contradicting this
resultant.

This is an exact counterexample to any attempt to exclude the
\((12,8)\) chart using only the normalized Laurent equations or the
one-pole-time condition.  It is not a polynomial Keller
counterexample.  It supplies instead a reusable finite-cusp lift
obstruction and identifies the still-open task: classify the
non-homogeneous boundary arcs on which cancellation might reduce the
ratio from \(19\) below \(3\).

## 1. Normalized fourth-power geometry

Write the leading coefficients as
\[
 f_{12}=h^3,\qquad g_8=h^2.
\]
In the fourth-power chart, \(h=r^4\) with
\(r\in\mathbf C[x]\setminus\{0\}\).  Put \(z=ry\) and depress the
monic octic:
\[
 g=w^8+aw^6+bw^5+cw^4+dw^3+ew^2+fw+q.
\tag{1}
\]
Let
\[
 s=g^{1/8}=w+O(w^{-1}).
\]
The upper triangular equations put \(f\) in the approximate-root
form
\[
 f=(\Phi(s))_+,
\tag{2}
\]
where \(\Phi\) is a degree-twelve polynomial with constant
coefficients; its \(s^8\) term and its constant term can be removed
by target transformations.

In the inverse \(s\)-coordinate there is a unique expansion
\[
 \widehat f=\Phi(s)+\sum_{\ell\geq1}A_\ell s^{-\ell}.
\tag{3}
\]
At fixed \(s\), the chain rule gives
\[
 [f,g]_{x,w}
 =8s^7s_w\sum_{\ell\geq1}A_\ell'(x)s^{-\ell}.
\tag{4}
\]
Since \(s_w=1+O(s^{-2})\), the coefficients of
\(w^6,w^5,\ldots,w\) in (4) are triangular with diagonal \(8\).
Consequently
\[
 A_1'=\cdots=A_6'=0,\qquad
 8A_7'=\frac{\lambda}{r}.
\tag{5}
\]

Set \(T=8A_7\).  Then \(T'=\lambda/r\), so the same
Riemann--Hurwitz argument used in normal degree \((9,6)\) gives
either constant \(r\) and affine \(T\), or
\[
 r=\gamma u^{k+1},\qquad
 T=\alpha+\beta u^{-k}.
\tag{6}
\]
The coefficient field contains \(\mathbf C(u^k)\) and is contained
in \(\mathbf C(u)\).  Cyclic Galois correspondence therefore gives
\[
 K=\mathbf C(v),\qquad v=u^m,\qquad k=mn,
\tag{7}
\]
and
\[
 [f,g]_{v,w}=\frac{\lambda}{m\gamma v^{n+1}},
 \qquad 8A_7=\alpha+\beta v^{-n}.
\tag{8}
\]

## 2. The degree-eight polynomial-lift threshold

For the coefficient of \(w^{8-j}\) in (1), put
\[
 \rho=\max_{2\leq j\leq8}
 \frac{\operatorname {pole}_0(c_j)}j,
\tag{9}
\]
including \(0\) in the maximum.  Undo depression in the form
\[
 G(u,y)=g\bigl(u^m,\gamma u^{mn+1}y+t(u)\bigr),
\tag{10}
\]
and let \(e=\max(0,-\operatorname {ord}_0t)\).

Monicity gives the center bound
\[
 e\leq m\rho.
\tag{11}
\]
Indeed, if \(e>m\rho\), the term \(t^8\) is the unique most singular
term of \(G(u,0)=g(u^m,t)\), contradicting polynomiality.

The coefficient \(G_i(u)\) of \(y^i\) then satisfies
\[
 \operatorname {ord}_0G_i
 \geq i(mn+1)-m(8-i)\rho.
\tag{12}
\]
If \(n\geq3\rho\), then for every \(i\geq2\),
\[
\begin{aligned}
 \operatorname {ord}_0G_i
 &\geq i+m\bigl(3i-(8-i)\bigr)\rho\\
 &=i+4m(i-2)\rho>0.
\end{aligned}
\tag{13}
\]
Thus \(G(0,y)\) is affine.  If its linear coefficient is nonzero,
the second coordinate separates the line \(u=0\).  If it vanishes,
the Keller identity restricted to that line makes \(F(0,y)\) affine
and nonconstant.  The original Keller map is injective on one affine
line, hence is an automorphism by Gwoździewicz's theorem.

We record the reusable consequence:

> **Degree-eight line criterion.**  A noninvertible pure-power
> \((12,8)\) candidate must have an invariant one-pole coefficient
> curve with
> \[
> \operatorname {pole}_0(A_7)<3\rho.
> \tag{14}
> \]

The strict inequality in (14) is a necessary condition, not a claim
that such a curve exists.

## 3. An exact normalized one-pole cusp

It is enough to work on the zero upper-constant slice
\[
 f=(g^{3/2})_+.
\tag{15}
\]
Let \(\tau\) be a parameter and scale the seven coefficients of (1)
by their deficits:
\[
\begin{array}{c|c}
\text{coefficient}&\text{value}\\ \hline
a&\tau^2\\
b&-\dfrac{22\sqrt{21}}{441}\tau^3\\
c&\dfrac{169}{504}\tau^4\\
d&-\dfrac{47\sqrt{21}}{1029}\tau^5\\
e&\dfrac{6721}{148176}\tau^6\\
f&-\dfrac{13679\sqrt{21}}{1555848}\tau^7\\
q&\dfrac{268777}{49787136}\tau^8 .
\end{array}
\tag{16}
\]
The residue construction (3), checked exactly in the accompanying
verifier, gives
\[
 A_1=\cdots=A_6=0,\qquad
 A_7=-\frac{2^{18}\sqrt{21}}{3^7\,7^{10}}\tau^{19}.
\tag{17}
\]
Equation (4), or direct differentiation, gives
\[
 [f,g]_{\tau,w}
 =-\frac{2^{21}19\sqrt{21}}{3^7\,7^{10}}\tau^{18}.
\tag{18}
\]

Now put \(\tau=v^{-1}\).  Then
\[
 [f,g]_{v,w}
 =\frac{2^{21}19\sqrt{21}}{3^7\,7^{10}}v^{-20}.
\tag{19}
\]
This is exactly (8) with \(n=19\), after choosing the harmless
constant \(\gamma\).  The field generated by the coefficients is
\(\mathbf C(v)\), because it contains both \(v^{-2}\) and a nonzero
multiple of \(v^{-3}\).  The time has one pole and no finite critical
point.  Hence (16) satisfies the full normalized pure-power geometry,
not merely its leading equations.

Every coefficient in (16) has pole order equal to its deficit, so
\[
 \rho=1,\qquad n=19.
\tag{20}
\]
The cusp is therefore far from the possible escape range (14).

## 4. Exact obstruction to every polynomial lift

Because (16) is weighted homogeneous, there are monic polynomials
\(F_0,G_0\in\mathbf C[X]\), of degrees twelve and eight, such that
\[
 f(v,w)=v^{-12}F_0(vw),\qquad
 g(v,w)=v^{-8}G_0(vw).
\tag{21}
\]
Their explicit coefficients are generated from (15)--(16) by the
verifier.  Exact elimination gives
\[
 \boxed{
 \operatorname {Res}_X(F_0,G_0)
 =-\frac{2^{88}19^2}{3^{36}7^{48}}.
 }
\tag{22}
\]

Suppose a polynomial lift existed after an arbitrary rational
depressing center \(t(u)\).  At \(y=0\), put
\[
 X(u)=v\,t(u),\qquad v=u^m.
\]
Equations (10) and (21) imply
\[
\begin{aligned}
 G(u,0)&=v^{-8}G_0(X(u)),\\
 F(u,0)&=v^{-12}F_0(X(u)).
\end{aligned}
\tag{23}
\]
Both expressions must be regular at \(u=0\).

The rational function \(X(u)\) cannot tend to infinity: monicity of
\(G_0\) would make the first expression in (23) still more singular.
It therefore has a finite limit \(\xi\).  Regularity in (23) forces
\[
 G_0(\xi)=F_0(\xi)=0,
\]
contradicting (22).  Thus no rational center can lift this normalized
cusp to a pair in \(\mathbf C[u,y]^2\).

This argument is independent of the line criterion and proves the
following general lemma.

> **Finite-cusp lift obstruction.**  If a normalized weighted cusp
> has
> \[
> f=v^{-M}F_0(vw),\qquad
> g=v^{-N}G_0(vw)
> \]
> with monic \(F_0,G_0\) and
> \(\operatorname {Res}(F_0,G_0)\ne0\), then it admits no polynomial
> lift through a rational depressing center.

## 5. The entire Davenport--Stothers extremal stratum is isotrivial

The preceding cusp is not an isolated lucky certificate.  There is a
structural reason that no rational deformation of a
Davenport--Stothers extremal pair can enter the escape range (14).

Let \(K\) be a characteristic-zero function field and suppose
\[
 p,q\in K[w],\qquad
 \deg p=12,\quad\deg q=8,\quad
 \deg(p^2-q^3)\leq5,
\tag{24}
\]
with \(p,q\) monic.  A nonzero normalized Jacobian implies
\(\gcd(p,q)=1\).  Indeed, if a nonconstant
\(s\in K[w]\) divided both \(p\) and \(q\), then it would divide
\[
 \partial_vp\,\partial_wq-\partial_wp\,\partial_vq.
\]
The normalized bracket is a nonzero element of \(K\), independent of
\(w\), so this is impossible.

Apply the polynomial \(abc\) theorem over an algebraic closure of
\(K\) to
\[
 p^2-q^3-(p^2-q^3)=0.
\]
It gives
\[
 24\leq
 \deg\operatorname {rad}\bigl(pq(p^2-q^3)\bigr)-1.
\tag{25}
\]
The radical on the right has degree at most
\[
 12+8+5=25.
\]
Equality is forced everywhere.  Therefore
\[
 \deg(p^2-q^3)=5,
\]
and \(p,q,p^2-q^3\) are squarefree and pairwise coprime.

The rational function
\[
 R=\frac{p^2}{q^3}
\tag{26}
\]
has degree \(24\) and the exact ramification passport
\[
 [2^{12}],\qquad[3^8],\qquad[19,1^5]
\tag{27}
\]
over \(0,\infty,1\), respectively.  Indeed, the finite roots account
for the \(2^{12},3^8,1^5\) entries, while at \(w=\infty\),
\[
 R-1=\frac{p^2-q^3}{q^3}
\]
vanishes to order \(19\).  The ramification contribution is
\[
 12+16+18=46=2\cdot24-2.
\]
Riemann--Hurwitz leaves no fourth branch value.

There are only finitely many degree-24 covers with the fixed passport
(27), up to a source projective transformation.  Hence every
rational family satisfying (24) is isotrivial.  The point of
ramification index \(19\) is unique, so polynomial equivalence
preserves infinity and the source change is affine.  If a fixed
representative \(P_0,Q_0\) is monic and \(Q_0\) is depressed, every
other monic depressed representative has the form
\[
\begin{aligned}
 p(w)&=\alpha^{-12}P_0(\alpha w),\\
 q(w)&=\alpha^{-8}Q_0(\alpha w).
\end{aligned}
\tag{28}
\]
The translation part vanishes because it would create the
\(w^7\)-coefficient \(8\beta/\alpha\) in \(q\).  With
\(\tau=\alpha^{-1}\), every coefficient of deficit \(j\) is a
constant times \(\tau^j\).

The terminal Laurent coefficient is consequently
\[
 A_7=C\tau^{19}.
\tag{29}
\]
Here \(C\ne0\), since otherwise the normalized bracket would vanish.
Let \(\delta\) be the gcd of the deficits whose fixed coefficients
are nonzero.  The coefficient field is
\(\mathbf C(\tau^\delta)\).  But \(A_7\) is a polynomial in those
coefficients, so \(\tau^{19}\) belongs to that field.  Cyclic field
descent gives \(\delta\mid19\).  Since no nonzero deficit is as large
as \(19\), one has \(\delta=1\).  Thus the coefficient field is
\(\mathbf C(\tau)\).

If this family also has the pure-power one-pole time, then
\[
 C\tau^{19}=A+Bv^{-n},
\qquad \mathbf C(\tau)=\mathbf C(v).
\tag{30}
\]
The parameters differ by a Möbius transformation.  Comparing map
degrees gives \(n=19\).  The right side has no critical point away
from its pole; the derivative of the left side vanishes at the zero
of \(\tau\).  Hence that zero must be \(v=\infty\), and after a
constant rescaling
\[
 \tau=v^{-1}.
\tag{31}
\]
Every nonconstant coefficient then has weighted pole scale one:
\[
 \boxed{\frac{n}{\rho}=19.}
\tag{32}
\]

This proves:

> **Extremal-stratum obstruction.**  No coprime rational deformation
> with
> \(\deg_w(p^2-q^3)\leq5\) can have one-pole ratio below \(3\).
> Every nonzero-Jacobian one-pole deformation is isotrivial and has
> ratio exactly \(19\).

Thus a possible \((12,8)\) counterexample cannot lie on the
Davenport--Stothers equality stratum.  It must arise on a secondary
non-homogeneous boundary after the leading extremal pair has itself
degenerated.

There is a precise description of that secondary boundary.  The
polynomial \(abc\) argument also proves the sub-extremal lemma
\[
 \deg(p^2-q^3)\leq4
 \quad\Longrightarrow\quad
 p^2=q^3.
\tag{33}
\]
No coprimality hypothesis is needed.  If the difference were
nonzero, let \(S=\gcd(p^2,q^3)\), of degree \(s\), and divide the
three-term equation by \(S\).  Polynomial \(abc\) would give
\[
 24-s
 \leq
 \deg\operatorname {rad}
 \left(\frac{p^2q^3(p^2-q^3)}{S^3}\right)-1
 \leq20+(4-s)-1,
\]
which is impossible.  Unique factorization and monicity then give
\[
 \boxed{p=P^3,\qquad q=P^2}
\tag{34}
\]
for a monic quartic \(P\).

This applies directly to a putative low-ratio pole.  In the
zero-upper-constant slice,
\[
 f=s^{12}+\sum_{\ell\geq1}A_\ell s^{-\ell},
\]
so \(A_1=\cdots=A_7=0\) in a weighted leading form implies
\(\deg(f^2-g^3)\leq4\).  At a coefficient pole of scale \(\rho\),
the six conserved levels have lower weight than their leading
homogeneous terms.  If
\(\operatorname {pole}(A_7)<3\rho\), then it is certainly less than
the natural terminal weight \(19\rho\), so the leading \(A_7\) also
vanishes.  Equations (33)--(34) show that the weighted limit must be
\[
 f_0=P^3,\qquad g_0=P^2.
\tag{35}
\]
Depression of \(g_0\) makes
\[
 P=w^4+Aw^2+Bw+C.
\tag{36}
\]

Hence the danger locus is not an unknown component of a large
seven-variable resultant.  It is the explicit three-dimensional
common-quartic locus (35)--(36).  The next calculation should be the
normal cone and successive invariant equations along this locus.

### 5.1 Exact normal cone and collision partitions

Write a first transverse deformation as
\[
 g=P^2+\varepsilon S,\qquad \deg S\leq3,
\tag{37}
\]
after absorbing the quotient of the original perturbation modulo
\(P\) into a tangent deformation of \(P\).  Divide
\[
 S^2=PH+R,\qquad \deg R<4.
\tag{38}
\]
The polynomial part of \(g^{3/2}\) starts
\[
 f=P^3+\frac32\varepsilon PS+\frac38\varepsilon^2H.
\tag{39}
\]
Exact expansion gives
\[
 f^2-g^3
 =-\frac34\varepsilon^2P^2R+O(\varepsilon^3).
\tag{40}
\]
Conservation through \(w\)-degree six forces
\[
 \boxed{R=0,\qquad P\mid S^2.}
\tag{41}
\]

If \(P\) is squarefree, (41) would make \(P\mid S\), impossible for
\(\deg S\leq3\).  The only possible multiplicity partitions of the
quartic are therefore
\[
 [2,1,1],\qquad[2,2],\qquad[3,1],\qquad[4].
\tag{42}
\]
This is the finite stable-collision list requested by the
Davenport--Stothers perspective.

Let \(z\) be a local uniformizer after a harmless ramified extension,
normalize the coefficient pole scale to one, and suppose the first
normal term is \(z^\delta S\).  When (41) holds, the scaled Jacobian
contribution at order \(z^{3\delta}\) is, up to the nonzero constant
\(3/8\),
\[
 \boxed{
 \frac{S^2}{P^2}
 \left(4PS'+(\delta-8)SP'\right).
 }
\tag{43}
\]
It must be a constant in the scaled \(w\)-coordinate.

Factor comparison at the roots of \(P\), together with the degree at
infinity, shows that (43) can never be a nonzero constant.  If it
vanishes, then
\[
 S^4=cP^{\,8-\delta}.
\tag{44}
\]
Combining (41), \(\deg P=4\), and \(\deg S\leq3\) leaves only two
silent normal types:
\[
\begin{array}{c|c|c|c}
\text{type}&P&S&\delta\\ \hline
I&Q^2&cQ&6\\
II&L^4&cL^3&5,
\end{array}
\tag{45}
\]
where \(Q\) is monic quadratic and \(L\) is monic linear.  Thus the
partitions \([2,1,1]\) and \([3,1]\) are excluded already in the
first normal cone.  Type I covers partitions \([2,2]\) and its
\([4]\) collision; Type II is the remaining \([4]\) direction.

They are called silent because their first normal Jacobian is zero.
They merely turn on a conserved level:

* Type I turns on the degree-six coefficient of \(f^2-g^3\);
* Type II turns on a degree-nine coefficient.

### 5.2 The silent types do not split into a one-pole branch

Depression makes the quadratic in Type I
\[
 Q=X^2+C.
\tag{46}
\]
In scaled variables its exact pair is
\[
\begin{aligned}
 \bar g&=Q^4+c z^6Q,\\
 \bar f&=Q^6+\frac32c z^6Q^3+\frac38c^2z^{12}.
\end{aligned}
\tag{47}
\]
In the original normalized variables, with \(X=vw\) and \(z=v\),
this is the univariate composition
\[
\begin{aligned}
 g&=U^4+cU,\\
 f&=U^6+\frac32cU^3+\frac38c^2,\\
 U&=w^2+Cv^{-2}.
\end{aligned}
\tag{48}
\]

It remains to check that a later term cannot split the composition.
Let the first such term in \(\bar g\) be
\[
 z^\eta R(X),\qquad \eta>6,
\]
and divide \(R=QA+B\), with \(\deg B<2\).  The quotient \(QA\) is
tangent to the \(Q\)-composite stratum.  Including the exact
polynomial-part correction in \(\bar f\), the leading transverse
Jacobian is
\[
 \boxed{
 3c\,z^{\eta+6}Q^2
 \left((8-\eta)BQ'-2QB'\right).
 }
\tag{49}
\]
It again cannot be a nonzero constant because of the factor \(Q^2\).
For \(Q=X^2+C\) with \(C\ne0\), the vanishing equation has only:

1. \(B=0\) when \(\eta=7\);
2. constant \(B\) when \(\eta=8\);
3. \(B=0\) when \(\eta>8\).

The constant at \(\eta=8\) is an ordinary constant target
translation of \(g\).  Removing it and repeating the first-splitting
argument shows that every formal branch remains \(Q\)-composite.
For a composite pair
\[
 f=\mathcal F(v,U),\qquad g=\mathcal G(v,U),
\]
the Jacobian is divisible by
\[
 U_w=2w,
\]
and hence cannot be a nonzero function independent of \(w\).

If \(C=0\), the exceptional solution at \(\eta=7\) is
\(B\propto X\).  But then (48) and this added term have constant
coefficients in the original variables; they contribute no
coefficient pole.  One must restart at a later genuine pole, where
the preceding argument applies again.

Type II is even more immediate.  Depression forces \(L=X\), and its
scaled terms become
\[
 v^{-8}\left(X^8+cv^5X^3\right)=w^8+cw^3
\]
in the original variables, again with no coefficient pole.  It
cannot be the leading form at a place with \(\rho>0\).

We have therefore excluded every one-step and iterated split of the
four collision partitions in (42), on the zero-upper-constant slice:

> **Secondary-degeneration obstruction.**  A rational one-pole
> branch with \(\rho>0\) and
> \(\operatorname {pole}(A_7)<3\rho\) cannot arise from a
> degeneration of the Davenport--Stothers passport
> \([2^{12}],[3^8],[19,1^5]\) when
> \(f=(g^{3/2})_+\).

### 5.3 Highest extra upper constant

The first effect of a nonzero extra approximate-root constant is also
structural.  Write the highest surviving upper term as
\[
 \kappa_\ell(g^{\ell/8})_+,\qquad
 \ell\in\{11,10,9,7,6,5,4,3,2,1\},
\tag{50}
\]
where the \(\ell=8\) term has been removed by a target shear.  At the
common-quartic leading form \(g_0=P^2\), put
\[
 H_\ell=(P^{\ell/4})_+.
\]
This term occurs in the scaled \(f\)-coordinate at order
\(z^{12-\ell}\).  Its exact leading Jacobian contribution is
\[
 2\kappa_\ell z^{12-\ell}P
 \left(4PH_\ell'-\ell P'H_\ell\right).
\tag{51}
\]
The factor \(P\) prevents (51) from being a nonzero constant.
Vanishing integrates to
\[
 H_\ell^4=P^\ell.
\tag{52}
\]

Consequently:

1. if \(\ell\) is odd, \(P=L^4\); depression gives \(L=X\), so this
   leading form carries no coefficient pole and the valuation must
   be restarted at a smaller scale;
2. if \(\ell\equiv2\pmod4\), \(P=Q^2\), with
   \(Q=X^2+C\);
3. if \(\ell=4\), the term is \(\kappa_4P\) and is automatically
   silent on the square cone itself.

The \(\ell=4\) case, conventionally written \(j=\kappa_4\), closes at
the first transverse normal.  Write
\[
\begin{aligned}
 P&=w^4+Aw^2+Bw+C,\\
 S&=Uw^3+Vw^2+Ww+Z,\\
 g&=P^2+\varepsilon S.
\end{aligned}
\]
Since \((g^{1/2})_+=P\), exact Laurent expansion gives
\[
\begin{aligned}
 [\varepsilon]A_1&=-\frac j2U,&
 [\varepsilon]A_2&=-\frac j2V,\\
 [\varepsilon]A_3&=\frac j8(3AU-4W),&
 [\varepsilon]A_4&=\frac j8(2AV+3BU-4Z).
\end{aligned}
\tag{53}
\]
If \(j\ne0\), constancy of the four levels forces
\[
 U=V=W=Z=0.
\]
Thus the only-\(j\) chart has no transverse square-cone normal.  If
\(j=0\), Sections 5.1--5.2 exclude the four repeated-root types.

Thus every genuine positive-pole chart with an extra highest upper
constant is either driven back to the square-quartic composite Type I
or is the now-excluded only-\(j\) chart.  In the square case, all
surviving even upper terms become ordinary polynomials in
\[
 U=w^2+Cv^{-2},
\]
while any lower odd term repeats (51) and forces the fourth-power,
regular-scale restart.  Descending through the finite list (50)
therefore leaves only even upper terms on a genuine positive-pole
square chart.  Their leading pair remains \(U\)-composite.
A counterexample would have to split this composition at a later
normal order.  Formula
(49) excludes that split when the Type-I conserved parameter
\(c\ne0\); the remaining exact chart is the square-quartic composite
with \(c=0\) and a highest upper exponent congruent to two modulo
four.  This is a one-variable transverse-operator problem, not a
seven-coefficient search.

### 5.4 The even-upper residual also has no split

The last chart in Section 5.3 has
\[
 Q=X^2+C,\qquad \bar g_0=Q^4,
\]
and one of the upper terms
\[
 \kappa z^aQ^p,\qquad
 (p,a)=(5,2),(3,6),(1,10).
\tag{54}
\]
The \((p,a)=(2,8)\) only-\(j\) case was closed by (53).

After absorbing every \(Q\)-composite tangent, let the first split be
\[
 \bar g=Q^4+\varepsilon z^\eta B,\qquad
 B=b_1X+b_0.
\tag{55}
\]
Before any upper cross, the exact quadratic normalized bracket is
\[
 -6\varepsilon^2z^{2\eta}QB
 \left(
 Cb_1+(\eta-7)b_1X^2+(\eta-8)b_0X
 \right).
\tag{56}
\]
It cannot be a nonzero constant.  Its only nonzero vanishing
possibilities are
\[
\begin{array}{c|c}
\eta=8&B=b_0,\\
\eta=7,\ C=0&B=b_1X .
\end{array}
\tag{57}
\]
The first is a constant target translation in the original
variables.  The second has regular, not polar, original coefficients
and forces a restart at the next genuine pole scale.

For \(p=5,a=2\), the upper term is linear-silent and its first
nonzero contribution occurs later than (56), so (57) is exhaustive.
For \(p=3,2,1\), the upper-linear operator is respectively
\[
 -6Q^2L,\qquad -4QL,\qquad -2L,
 \quad
 L=Cb_1+(\eta-7)b_1X^2+(\eta-8)b_0X.
\tag{58}
\]
If \(a+\eta<2\eta\), (58) is the first equation and has no genuine
polar split.  If \(a+\eta>2\eta\), equation (56) comes first and gives
only (57).  At the three ties \(\eta=a\), the complete leading
expressions factor, up to nonzero scalars, as
\[
\begin{array}{c|l}
(p,a)&\text{leading bracket}\\ \hline
(3,6)&
Q(-Cb_1+X^2b_1+2Xb_0)(\kappa Q+\varepsilon B),\\
(2,8)&
b_1Q^2(3\varepsilon B+2\kappa),\\
(1,10)&
(Cb_1+3X^2b_1+2Xb_0)
(3\varepsilon QB+\kappa).
\end{array}
\tag{59}
\]
No row in (59) is a nonzero constant or vanishes for a genuine
non-composite \(B\).  Thus the even-upper residual is closed.

Combining Sections 5.1--5.4 yields the pole statement needed by the
line criterion:

> **Pure-power pole threshold, zero and extra upper constants.**
> Every rational one-pole invariant curve in the fourth-power
> \((12,8)\) chart satisfies
> \[
> \boxed{\operatorname {pole}(A_7)\geq3\rho.}
> \tag{60}
> \]

A smaller ratio would force the weighted common-quartic limit (35).
The highest upper term gives the finite alternatives in Section 5.3,
and the four collision partitions and every first split are excluded
by (43), (49), (53), and (56)--(59).  A regular-scale alternative in
(57) contributes no pole and is removed by restarting at the first
actual Laurent pole.

## 6. Counterexample status and next exact target

The cusp (16) is an exact nonzero-Jacobian, one-pole solution
of the normalized \((12,8)\) system recorded in this project.  It
shows that the normalized equations themselves have highly
nontrivial solutions and that searching only for an inconsistency in
the six Laurent levels cannot close the frontier.

It is not a polynomial counterexample: both the threshold argument
and the resultant obstruction exclude its lift.  A genuine
counterexample candidate must instead come from a non-homogeneous
boundary arc satisfying all of the following:

1. \(A_1,\ldots,A_6\) are constant;
2. \(A_7\) has exactly one pole and no other critical point;
3. its pole ratio is strictly below \(3\);
4. its depressing-center limit avoids the finite-cusp resultant
   obstruction.

Section 5 removes the smooth Davenport--Stothers equality stratum and
all four collision partitions, with zero or nonzero upper constants.
Consequently no normalized fourth-power pure-power curve can evade
the ratio-three line criterion.  This closes that pure-power chart
from a noninvertible Keller map.  It does not address the
constant-\(r\) coefficient curves or the connected
non-fourth-power cover, and therefore does not yet exclude the full
normal-degree pair \((12,8)\).
