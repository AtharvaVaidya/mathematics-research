# Route A: exact progress memo

Date: 2026-07-24

## Outcome

No pair \(P,Q\in B_{\mathbb C}\) with \(\{P,Q\}=1\) was found, so this
work does **not** produce a plane counterexample.

At the start of this investigation, the workspace contained only Git
metadata; there were no pre-existing Route A notes, proofs, or scripts.
All files under `route_a/` listed below were created during this bounded
attempt.  Files concurrently created elsewhere in the workspace were not
modified.

The useful exact results are:

1. the characteristic-\(3\) pair has a \(3\)-adic deformation to every
   order when its support is allowed to grow;
2. no such tower can have bounded polynomial degree inside the full
   \(\mathbb G_m\)-homogeneous ansatz;
3. in fact, there is no characteristic-zero homogeneous Darboux pair at
   all;
4. no affine-linear Hamiltonian \(P\) has a slice \(Q\in B\);
5. the symplectic form is algebraically exact and
   \(H^1_{\mathrm{dR}}(B)=0\), reducing the remaining issue to a genuine
   polynomial Pfaff decomposition;
6. several finite low/sparse-support ansätze were eliminated by exact
   rational linear algebra;
7. BF0--BF2 were derived for arbitrary nonhomogeneous pairs, and the full
   coefficient variety with \(\deg P,\deg Q\leq4\) was eliminated.
8. the unequal full coefficient varieties
   \(\deg P\leq2,\deg Q\leq5\) and
   \(\deg P\leq2,\deg Q\leq6\) were eliminated over \(\mathbb Q\);
9. every Hamiltonian \(P=cw+f(u)\), \(c\ne0\), was excluded against
   partners of arbitrary degree.
10. every Hamiltonian \(P=cv+f(w)\), \(c\ne0\), was likewise excluded
    against partners of arbitrary degree, by the exact differential on its
    generic hyperelliptic fiber.
11. every Hamiltonian \(P=cu+f(w)\), \(c\ne0\), was excluded by residues
    of the forced differential on its rational generic fiber.
12. permuting the two roles in the generic-fiber argument excludes the
    remaining three elementary families \(cv+f(u)\), \(cu+f(v)\), and
    \(cw+f(v)\).  Thus every \(P=cx_i+f(x_j)\), \(i\ne j\), is excluded
    against partners of arbitrary degree.
13. two genuinely three-generator families are also excluded:
    \(av+cw+f(u)\) and \(au+cw+f(v)\).  These allow both complementary
    linear coefficients to be nonzero and an arbitrary polynomial in the
    third generator.
14. the remaining separated family \(au+bv+f(w)\) is excluded by its
    Newton polygon.  Consequently every Hamiltonian that is a linear
    combination of two generators plus an arbitrary polynomial in the
    third is excluded against partners of arbitrary degree.
15. the mixed family \(av+C(u)w+F(u)\), with arbitrary polynomial
    coefficient \(C(u)\), is excluded by an exact hyperelliptic
    completion.  This goes beyond separated polynomials and allows
    nonlinear \(u^mw\) terms.
16. the characteristic-\(3\)-inspired mixed family
    \(cw+\lambda uv\) is excluded by an explicit rational mate whose
    unavoidable boundary pole has order one.  In particular the seed
    \(w+uv\) has no characteristic-zero polynomial lift of any degree.
17. the bilinear result extends to \(cw+\lambda uv+F(u)\) for arbitrary
    \(F\).  For \(\deg F\ge2\), exactness would produce a rational
    function with exactly one simple pole on a positive-genus curve; for
    affine \(F\), the explicit boundary-pole calculation applies.
18. allowing an arbitrary coefficient \(C(u)\) in front of \(w\) gives
    the still larger excluded family \(C(u)w+\lambda uv+F(u)\).  Its only
    genus-zero locus has an explicit rational primitive with the same
    unavoidable boundary pole.  This structurally excludes all 17
    low-degree characteristic-\(3\) seed Hamiltonians found in the search.
19. adding the smallest absent support perturbation, a linear \(v\)-term,
    leads to the fully excluded affine-coefficient family
    \((b+\lambda u)v+C(u)w+F(u)\).  This covers every polynomial that is
    affine in \(v\), polynomially linear in \(w\), and otherwise arbitrary
    in \(u\).
20. the next absent degree-two perturbation \(v^2\) is also excluded:
    \(cw+\lambda uv+\mu v^2\) has a nonzero holomorphic toric residue
    differential associated with the interior Newton point \((1,1)\).
21. the complementary quadratic perturbation \(vw\) is excluded by two
    explicit residues on its rational generic fiber:
    \(cw+\lambda uv+\nu vw\) has forced residues
    \(1/\nu\) and \(-1/\nu\).
22. the \(v^2\) Newton argument extends to every polynomial tail
    \(cw+\lambda uv+G(v)\).  Its Newton polygon has vertices
    \((0,0),(2\deg G,0),(1,2),(0,2)\), with the same interior residue
    differential.
23. the apparent \(w^2\)-perturbation is the reduced mixed support
    \(u+u^2v\).  It produces new exact characteristic-\(3\) pairs, but
    the whole characteristic-zero family
    \(u(b+\kappa u)v+C(u)w+F(u)\) is excluded by a one-pole
    hyperelliptic argument and an explicit genus-zero boundary pole.
24. among the next reduced degree-three orbits, \(uvw\) has a direct
    rational-fiber residue obstruction in every characteristic:
    \(w+uv+\kappa uvw\) forces residues \(-\kappa,\kappa\).
25. the \(uv^2\) orbit has a singular affine plane model whose two
    normalization branches at the missing origin carry residues
    \(\pm1/(2\sqrt{\kappa P})\).  It likewise has no rational mate in
    characteristic zero or characteristic \(3\).
26. the remaining degree-three orbit \(v^2w\) forces a nonzero
    holomorphic differential on the complete normalization.  Exact local
    calculations cover both finite cusps and the resonant double point at
    infinity, excluding it in characteristic zero.
27. the first reduced degree-four orbit \((uv)^2\) belongs to a larger
    all-degree family: every \(cw+H(uv)\) with nonlinear \(H\) has a
    rational generic fiber on which the forced differential has nonzero
    residues.  Thus it has no rational mate in characteristic zero; the
    two signed quadratic tails are likewise excluded over
    characteristic \(3\).
28. the next degree-four orbit \(uv^3\) produces one new exact
    characteristic-\(3\) pair, with partner degree nine.  In
    characteristic zero its forced differential is nonzero and
    holomorphic on the complete normalization, including at all finite
    cusps and the sole resonant infinity branch.  The modular pair also
    has an all-support obstruction already modulo \(9\).
29. \(uv^2w\) is excluded in characteristic zero and characteristic
    \(3\) by the residue \(1/\kappa\) at \((s,w)=(-1,0)\).
30. \(u^2vw\) has a squarefree degree-six hyperelliptic model of genus
    two.  Its forced differential has exactly one double pole and zero
    residue, so it cannot be exact in characteristic zero.
31. \(v^3w\) forces a nonzero holomorphic differential on the complete
    normalization; exact local checks cover both finite cusp groups and
    the only resonant infinity branch.
32. \(u^3v\) has Newton arithmetic genus four and one tacnode of
    delta-invariant two, hence generic genus two.  Its forced
    differential again has a unique double pole, excluding exactness in
    characteristic zero.
33. these orbit calculations are instances of a monomial-cone theorem.
    For \(P=w+uv+\kappa u^av^bw^c\), \(c=0,1\), the theorem excludes
    every \(a>b\ge1\), every diagonal \(a=b\) except the affine base
    case, and the whole \(v\)-side cone
    \(b>a,\ b\ge2a+c-1\).  The mechanisms
    are respectively a positive-genus one-pole obstruction, a residue,
    and a Newton-interior/residue/one-pole trichotomy.
34. the two degree-five modular seeds belong to an infinite exact
    Frobenius-central family.  For every positive-degree
    \(H\in B_{\mathbb F_3}\), putting \(A=1+H^3\) gives
    \(P=w+Auv,\ Q=-v+uv^2+Av^2w\).  Every member fails the first
    unrestricted Hensel equation by the same functional
    \([v]+[uv^2]\).
35. inside the remaining middle wedge, put
    \(m=2(b-a)-c\).  Every exponent with \(m\mid b\) is excluded for
    every nonzero coefficient by an explicit Puiseux residue.
36. the whole middle wedge is excluded for a transcendental, hence
    generic, perturbation coefficient: the first variation from the
    rational base fiber has a nonzero residue proportional to
    \(\partial_P^{m+2}[P^b(1+P)^{b-a}]\).
37. the Newton-interior argument extends from monomials to arbitrary
    finite sums in the strict cone \(b>2a+c\), provided the cleared
    generic curve is Newton nondegenerate.  This holds on a Zariski-open
    coefficient locus; degenerate initial forms remain outside the
    theorem.
38. the first residue-zero wall inside the middle wedge is now excluded
    for every coefficient.  On \(b-m=2\), explicit toric adjoints make
    the canonical evaluation map onto the two jets prescribed by the
    primitive pole divisor.  Riemann--Roch gives \(L(E)=k\), so the
    forced differential cannot have a rational primitive.
39. more generally, the normalization has an explicit canonical row
    basis and an exact Fourier-by-jet staircase criterion for
    \(L(E)=k\).  This criterion unconditionally excludes every
    fixed-coefficient middle-wedge monomial satisfying
    \(m>(b-m)^2\), as well as many additional arithmetic cases.
40. the whole next wall \(b-m=3\) is also excluded for every
    coefficient.  The staircase handles all but the residue cases and
    one genus-two curve; on that exception \(L(3p)\) has an explicit
    generator whose derivative has incompatible values at two points.
41. parity sharpens the uniform staircase region substantially.  For
    \(c=1\), it holds as soon as \(m\ge2(b-m)-1\).  For \(c=0\) and
    \(b-m\ge4\), it holds whenever \(3m>2(b-m)^2\).
42. the entire third inner wall \(b-m=4\) is excluded for every
    coefficient.  Its only non-residue staircase exceptions have
    \(L(4p)=\langle1,vw\rangle\), while \(d(vw)/\eta\) takes the
    incompatible values \(\kappa P\) and \(4\kappa P\).
43. the complete coprime middle wedge is excluded for every coefficient:
    if \(\gcd(m,b-m)=1\), canonical gaps and explicit monomial functions
    are complementary lattice points.  The only possible maximal-pole
    section is \(vw\); all lower-pole sections have zero first jet at
    \((s,w)=(0,P)\), forcing an incompatible derivative normalization.
44. the same gap/function reciprocity decomposes into \(g\)-by-\(g\)
    Fourier blocks when \(g=\gcd(m,b-m)>1\).  In the top block, only the
    \(vw\) character matches the principal part of the forced
    differential, and its normalization at \((0,P)\) differs by the
    factor \(b-m\).  This closes the entire monomial middle wedge for
    every fixed nonzero coefficient.
45. this is stable under finite perturbations strictly behind the three
    exposed faces of a middle-wedge monomial.  On the coefficient locus
    where no additional singularities occur, the Newton polygon,
    conductor, Fourier principal parts, and regular comparison point
    are unchanged, giving a facewise exclusion theorem for nonsparse
    Hamiltonians.
46. every finite middle-wedge support has a three-signature
    combinatorial dichotomy.  A unique common extremizer is
    automatically denominator-maximal and satisfies the exposed-face
    theorem.  Every support not covered this way lies either on one of
    three explicit ratio-tie loci or in one of four separated-extremizer
    types.  These multi-face configurations are the precise residual
    combinatorial obstruction to a global nonsparse theorem.
47. all four separated types and all first-face ties with maximal
    denominator at least two are removed coefficient-uniformly.  The
    first lower-left Newton face has polynomial \(G(X)-P\), which is
    automatically separable over \(k(P)\); its interpolating primitive
    is controlled by \((XG')^{-1}\), whose constant term has
    incompatible normalization at \((0,P)\).  Degeneracy on later
    faces only refines terms of \(s\)-order at least two and cannot
    alter this first-jet contradiction.
48. the horizontal \(m=1\) resonance is also excluded for every
    coefficient.  In this family
    \(F=w^2+(s-P)w+A(s)\), with \(A=(1+s)K(s)\) divisible by
    \(s^3(1+s)\), and the forced differential has the same residues as
    \(ds/A\) along \(w=0\).  A reciprocal polynomial differential
    \(ds/A\) cannot have all residues zero if \(A\) has two distinct
    roots.  Thus every nonzero finite middle-wedge sum is excluded in
    characteristic zero, with no genericity condition on its
    coefficients.

Here
\[
 B=k[u,v,w]/(w^2-u-u^2v)
\]
and
\[
 \{u,v\}=-2w,\qquad \{u,w\}=-u^2,\qquad
 \{v,w\}=1+2uv.
\]

## 1. Poisson derivations and the Laurent chart

For reduced representatives \(f,g\), the bracket is
\[
\begin{aligned}
\{f,g\}={}&-2w(f_u g_v-f_vg_u)
-u^2(f_u g_w-f_wg_u)\\
&+(1+2uv)(f_vg_w-f_wg_v).
\end{aligned}
\]
In particular,
\[
\begin{aligned}
D_u&=\{u,-\}=-2w\partial_v-u^2\partial_w,\\
D_v&=\{v,-\}=2w\partial_u+(1+2uv)\partial_w,\\
D_w&=\{w,-\}=u^2\partial_u-(1+2uv)\partial_v.
\end{aligned}
\]

Set \(r=u^{-1}\).  Then
\[
B[u^{-1}]=k[r,r^{-1},w],\qquad
v=r^2w^2-r,
\]
and
\[
\{r,w\}=1.
\]
Thus Route A is precisely the problem of finding a canonical Laurent pair
which lies in the boundary-regular subring
\[
k[r^{-1},w,r^2w^2-r].
\]

Let \(D=(u,w)\), whose coordinate is \(v\).  At the generic point of \(D\),
\[
\operatorname{ord}_D(w)=1,\qquad
\operatorname{ord}_D(u)=2,\qquad
\operatorname{ord}_D(r)=-2.
\]
This immediately gives two useful slice exclusions:

* If \(P=w\), then \(-\partial_r Q=1\), hence
  \(Q=-r+f(w)\).  Its order along \(D\) is \(-2\), so it is not in \(B\).
* If \(P=u=r^{-1}\), then \(-r^{-2}\partial_wQ=1\), hence
  \(Q=-r^2w+f(r)\).  The first term has odd order \(-3\), which cannot be
  cancelled by the even orders of the Laurent monomials in \(f(r)\).

The same argument excludes every nonconstant \(P\in k[w]\): the Laurent
equation first forces \(P\) to be affine in \(w\), and then the preceding
boundary pole remains.

## 2. The exact characteristic-\(3\) pair

Put \(s=uv\).  Over \(\mathbb F_3\),
\[
P_0=w,\qquad Q_0=2v+uv^2=v(s+2)
\]
satisfies
\[
\{P_0,Q_0\}=1.
\]
Using the displayed integer representatives,
\[
\{P_0,Q_0\}
=-2-6s-3s^2
=1-3(1+s)^2.
\]
Using the congruent lift \(Q_0=-v+uv^2\) instead gives
\(\{P_0,Q_0\}=1-3s^2\).

For the natural integer lift, the first deformation equation is
\[
\{A,Q_0\}+\{w,B\}=(1+s)^2\pmod 3.
\]
On the complete reduced basis
\[
\{u^iv^jw^k:k\in\{0,1\},\ i+j+k\le d\}
\]
for both \(A\) and \(B\), exact row reduction over \(\mathbb F_3\) gives no
solution for \(d=0,\ldots,6\).  The first solution occurs at \(d=7\):
\[
A=2uvw+2u^2v^2w,\qquad B=2v+2u^3v^4.
\]
The corresponding integer lift
\[
\begin{aligned}
P&=w+6uvw+6u^2v^2w,\\
Q&=8v+uv^2+6u^3v^4
\end{aligned}
\]
obeys the exact identity
\[
\begin{aligned}
\{P,Q\}-1={}&-9-162s-459s^2-378s^3\\
&-288s^4-540s^5-324s^6,
\end{aligned}
\]
so it is a solution modulo \(9\).

## 3. Complete reduction of the homogeneous ansatz

Give \(B\) the hyperbolic grading
\[
\operatorname{wt}(u)=2,\qquad \operatorname{wt}(v)=-2,\qquad
\operatorname{wt}(w)=1.
\]
The bracket raises weight by \(1\).  A homogeneous Darboux pair must
therefore have weights summing to \(-1\).

Every homogeneous component is a monomial in \(u\), \(v\), and possibly
\(w\), times a polynomial in the invariant \(s=uv\).  If an even-weight
component has nonnegative weight \(2k\), a possible ordered pair has the
form
\[
P=u^k a(s),\qquad Q=v^{k+1}w b(s).
\]
For \(k\ge1\), its bracket is divisible by \(s^k\); for \(k=0\), its
bracket is still divisible by \(s\).  For negative even weight
\(-2h\), the corresponding bracket is divisible by \(s^{h-1}\) unless
\(h=1\).  Odd/even ordering is obtained by swapping the pair.

Consequently the only homogeneous weights that can possibly give a
constant bracket are \(1\) and \(-2\), and, after swapping, every such
pair is
\[
P=w\,a(s),\qquad Q=v\,b(s).
\]
A direct calculation gives
\[
\{P,Q\}
=-\frac1{a(s)}
\frac{d}{ds}\left[s(1+s)a(s)^2b(s)\right].
\]
Therefore \(\{P,Q\}=1\) is equivalent to
\[
\frac{d}{ds}\left[s(1+s)a(s)^2b(s)\right]=-a(s). \tag{*}
\]
If \(a,b\) are nonzero polynomials over a characteristic-zero field, the
left side has degree
\[
2\deg a+\deg b+1,
\]
whereas the right side has degree \(\deg a\).  Equality is impossible.
This proves:

> **Homogeneous obstruction.**  There is no
> \(\mathbb G_m\)-homogeneous Darboux pair in \(B\) over any
> characteristic-zero field.

In characteristic \(3\), \(a=1\), \(b=s-1\) solves (*) because
\[
\left[s(1+s)(s-1)\right]'=(s^3-s)'=-1.
\]
This identifies the Frobenius mechanism exactly.

### The full \(3\)-adic tower in this ansatz

Define
\[
E(a,b)=\left[s(1+s)a^2b\right]'+a.
\]
At the seed \((a_0,b_0)=(1,s-1)\), its linearization over
\(\mathbb F_3\) is
\[
L(\alpha,\beta)
=\left[s(1+s)((2s+1)\alpha+\beta)\right]'+\alpha.
\]
This operator is surjective on \(\mathbb F_3[s]\): for any \(h\), choose
\[
\alpha=h,\qquad \beta=-(2s+1)h.
\]
Then \(L(\alpha,\beta)=h\).  Hence there is no first-order Cartier
obstruction at any stage, and the seed lifts recursively modulo
\(3^N\) for every \(N\).

However, a bounded-degree tower would converge to polynomials over
\(\mathbb Q_3\), contradicting the characteristic-zero degree argument
above.  Degree/support escape is therefore necessary, not an artifact of
the search.  The supplied script verifies twelve successive stages,
through modulus \(3^{13}=1594323\).

## 4. No affine-linear Hamiltonian has a slice

Let
\[
P=au+bv+cw+d.
\]
The constant \(d\) is irrelevant.

If \(b\ne0\) and \((a,c)\ne(0,0)\), \(P\) has a critical point on the
surface.  Indeed, choose a nonzero root of
\[
c^2u^3-2abu^2-2b^2=0,
\]
which exists because this is nonconstant with nonzero constant term, and
set
\[
w=-\frac{cu^2}{2b},\qquad v=\frac{w^2-u}{u^2}.
\]
Then \(dP\) is proportional to
\(d(w^2-u-u^2v)\), so \(D_P\) vanishes there.  It cannot satisfy
\(D_PQ=1\).

The exceptional pure-\(v\) case is also impossible.  Over
\(K=\mathbb C(v)(\sqrt v)\), the generic fiber becomes
\[
K[z,z^{-1}],\qquad
z=(1+2uv)+2\sqrt v\,w,
\]
and
\[
D_vz=2\sqrt v\,z.
\]
Thus \(D_v\) is a nonzero scalar multiple of \(z\,d/dz\), whose image on
Laurent polynomials has zero constant coefficient and cannot contain
\(1\).

If \(b=c=0\), then \(P=au\), and \(D_P\) vanishes along \(D=(u,w)\).

It remains to consider \(b=0,c\ne0\).  In the function field, \((P,u)\)
are coordinates and
\[
\{P,Q\}=cu^2\frac{\partial Q}{\partial u}\bigg|_P.
\]
A rational solution has the form
\[
Q=-\frac1{cu}+h(P),\qquad h\in\mathbb C(P).
\]
Regularity forces \(h\) to have no finite poles.  For a fiber \(P=t\)
with \(t\ne0\), \(u\) never vanishes, so a pole of \(h\) cannot cancel
against the first term.  The fiber \(P=0\) also has a component with
\(u\ne0\), given by \(w=-au/c\).  Hence \(h\in\mathbb C[P]\), leaving
the uncancelled pole \(-1/(cu)\) along \(D\).  This is again impossible.

Therefore no affine-linear \(P\) admits any polynomial slice \(Q\), of
arbitrary degree.

The same Laurent argument gives a genuinely nonlinear all-degree extension.
Let
\[
P=cw+f(u),\qquad c\ne0,\quad f\in\mathbb C[u].
\]
In the coordinates \(r=u^{-1},w\), holding \(P\) fixed gives
\[
\{P,Q\}=-c\frac{\partial Q}{\partial r}\bigg|_P.
\]
Consequently every rational solution in the function field is
\[
Q=-\frac{1}{cu}+h(P),\qquad h\in\mathbb C(P).
\]
The fiber \(P=t\) has a dense curve with \(u\ne0\) for every finite \(t\):
take any \(u\ne0\), put \(w=(t-f(u))/c\), and recover
\(v=(w^2-u)/u^2\).  Since \(Q+1/(cu)=h(P)\) is regular at the generic
point of this curve, \(h\) has no finite pole.  Hence \(h\) is a
polynomial.  Along the boundary \(D=(u,w)\), \(h(P)\) is regular whereas
\(-1/(cu)\) has a pole.  This contradiction proves:

> **Nonlinear triangular Hamiltonian obstruction.**  No
> \(P=cw+f(u)\), with \(c\ne0\), has a Darboux mate in \(B\).

This includes the nonhomogeneous characteristic-\(3\) seeds
\(P=w\pm u^2\): their apparent first Hensel steps cannot converge to a
characteristic-zero pair.

There is a complementary nonlinear family for which the generic-fiber
obstruction becomes especially transparent.  Let
\[
P=cv+f(w),\qquad c\ne0,\quad f\in\mathbb C[w],
\]
and put \(K=\mathbb C(P)\).  In the generic fiber define
\[
z=1+2uv.
\]
The surface equation gives the exact identity
\[
z^2=1+4vw^2
   =1+\frac4c(P-f(w))w^2. \tag{HF}
\]
Thus its function field is the hyperelliptic function field
\[
K(w,z),\qquad
z^2=1+\frac4c(P-f(w))w^2.
\]
Moreover
\[
\{P,w\}=c(1+2uv)=cz.
\]
If \(\{P,Q\}=1\), restriction to the generic fiber would therefore give
\[
dQ=\frac{dw}{cz}. \tag{HD}
\]

For \(n=\deg f\ge1\), the polynomial on the right of (HF) is squarefree
over \(K\) and has degree \(n+2\) in \(w\).  The differential \(dw/z\)
extends to a nonzero holomorphic differential on the smooth projective
hyperelliptic model: at finite branch points it is regular, and at infinity
its order is \(n-1\) when \(n\) is odd and \((n-2)/2\) when \(n\) is even.
A nonzero exact rational differential cannot be holomorphic on a complete
curve, since a pole of a rational function produces a pole of its
differential in characteristic zero.  When \(f\) is constant, the generic
fiber is the conic \(z^2=1+\lambda w^2\), and \(dw/z\) has nonzero residues
at its two points at infinity, which also forbids exactness.  Hence:

> **Hyperelliptic triangular Hamiltonian obstruction.**  No
> \(P=cv+f(w)\), with \(c\ne0\), has a Darboux mate in \(B\).

The remaining two-generator triangular orientation also has a short
all-degree obstruction.  Let
\[
P=cu+f(w),\qquad c\ne0,
\]
and again work over \(K=\mathbb C(P)\).  The generic fiber has rational
parameter \(w\), with \(u=(P-f(w))/c\), and
\[
\{P,w\}=c\{u,w\}=-cu^2=-\frac{(P-f(w))^2}{c}.
\]
A mate would force
\[
dQ=-\frac{c\,dw}{(P-f(w))^2}. \tag{RD}
\]
If \(\deg f\ge2\), take a simple root \(\alpha\) of \(P-f(w)\) over
\(\overline K\).  The residue of (RD) at \(w=\alpha\) is
\[
\frac{c f''(\alpha)}{f'(\alpha)^3}.
\]
All these residues could vanish only if \(f''\) vanished at every root of
\(f(w)-P\).  Since \(\deg f''<\deg(f-P)\), this would force \(f''=0\),
contrary to \(\deg f\ge2\).  Exact rational differentials have zero
residues, so no \(Q\) exists.  If \(\deg f\le1\), the Hamiltonian is
affine-linear and was already excluded above.  Therefore:

> **Rational triangular Hamiltonian obstruction.**  No
> \(P=cu+f(w)\), with \(c\ne0\), has a Darboux mate in \(B\).

The same calculation closes the other three ordered two-generator
orientations.  In each row, \(K=\mathbb C(P)\), the displayed equation is
the generic fiber, and \(\{P,Q\}=1\) would make the displayed differential
exact:
\[
\begin{array}{c|c|c}
P & \text{generic fiber} & dQ\\ \hline
cv+f(u) &
w^2=u+\dfrac{u^2}{c}(P-f(u)) &
\dfrac{du}{2cw}\\[6pt]
cu+f(v) &
w^2=\dfrac{P-f(v)}c+
      \dfrac{v(P-f(v))^2}{c^2} &
-\dfrac{dv}{2cw}\\[6pt]
cw+f(v) &
z^2=1+\dfrac{4v(P-f(v))^2}{c^2},\quad z=1+2uv &
-\dfrac{dv}{cz}.
\end{array} \tag{TF}
\]
For \(n=\deg f\ge1\), the first right-hand polynomial in (TF) has
degree \(n+2\); the other two have degree \(2n+1\).  They are squarefree
over the generic field \(K\).  The differentials in the last column extend
to nonzero holomorphic differentials on the corresponding smooth
projective hyperelliptic curves.  At infinity their orders are,
respectively,
\[
n-1\ \text{(odd \(n\)) or }(n-2)/2\ \text{(even \(n\))},
\qquad 2n-2,\qquad 2n-2,
\]
all nonnegative.  They therefore cannot be exact.  The cases
\(\deg f=0\) reduce to the affine or constant cases already handled.
Together with the preceding three results this proves:

> **All elementary two-generator Hamiltonians.**  For distinct
> \(x_i,x_j\in\{u,v,w\}\), no Hamiltonian
> \(P=cx_i+f(x_j)\), \(c\ne0\), has a Darboux mate in \(B\), regardless
> of the degree of \(f\) or of the prospective mate.

The method continues beyond two-generator shears.  First let
\[
P=av+cw+f(u),\qquad a\ne0,
\]
put \(K=\mathbb C(P)\), and complete the square with
\[
W=w+\frac{c}{2a}u^2.
\]
The generic fiber and Hamiltonian derivative are
\[
\begin{aligned}
W^2&=u+\frac{u^2}{a}(P-f(u))+\frac{c^2}{4a^2}u^4=:G_P(u),\\
\{P,u\}&=2aw+cu^2=2aW.
\end{aligned}
\]
Thus a mate would force \(dQ=du/(2aW)\).  Except when the \(u^4\)
and \(u^3\) terms cancel, \(G_P\) has degree at least three, and
\(du/W\) is a nonzero holomorphic differential on the smooth projective
generic hyperelliptic fiber.  In the cancellation case
\[
f(u)=f_0+\frac{c^2}{4a}u^2
\quad\text{(also including \(c=0,f=f_0\))},
\]
one has \(G_P=u+(P-f_0)u^2/a\); then \(du/W\) has nonzero residues at
the two points at infinity.  Exactness is impossible in every case.
When \(a=0,c\ne0\), this reduces to the already excluded
\(cw+f(u)\) family.

Next let
\[
P=au+cw+f(v),\qquad a\ne0,
\]
and set \(z=1+2uv\) and \(Y=2aw+cz\).  The identities
\[
\begin{aligned}
Y^2&=c^2+4a(P-f(v))+4v(P-f(v))^2=:H_P(v),\\
\{P,v\}&=-Y
\end{aligned}
\]
give \(dQ=-dv/Y\).  If \(n=\deg f\ge1\), then \(H_P\) has odd degree
\(2n+1\), and \(dv/Y\) is a nonzero holomorphic differential (order
\(2n-2\) at the unique point at infinity).  If \(f\) is constant, \(P\)
is affine-linear and Section 4 already excludes it.  The case \(a=0\)
is the elementary \(cw+f(v)\) family.  Hence:

> **Two separated three-generator orientations.**  No Hamiltonian of either
> form
> \[
> av+cw+f(u)\quad\text{or}\quad au+cw+f(v)
> \]
> has a Darboux mate when the displayed two linear coefficients are not
> both zero.  This is an all-degree result for these two separated
> families; it does not yet cover \(au+bv+f(w)\).

The last orientation has a plane-curve form.  Let
\[
P=au+bv+f(w),\qquad ab\ne0,
\]
and work over \(K=\mathbb C(P)\).  Eliminating \(v\) gives the generic
fiber
\[
F(u,w)
=au^3-(P-f(w))u^2-bu+bw^2=0. \tag{NF}
\]
Direct differentiation and the Poisson formulas give
\[
\{P,u\}=F_w,\qquad \{P,w\}=-F_u.
\]
Thus \(D_P\) is exactly the curve-Jacobian field
\[
D_P=F_w\partial_u-F_u\partial_w,
\]
and a Darboux mate would force the Poincaré-residue differential
\[
dQ=\frac{du}{F_w}=-\frac{dw}{F_u}. \tag{ND}
\]

Suppose \(n=\deg f\ge1\).  The Newton polygon of (NF) is the convex hull
of
\[
(0,2),\ (1,0),\ (3,0),\ (2,n).
\]
The point \((1,1)\) lies strictly in its interior for every \(n\ge1\).
The generic curve is nondegenerate for this polygon.  Its non-binomial
bottom face is
\[
u\bigl(au^2-(P-f_0)u-b\bigr),
\]
whose quadratic factor is squarefree over \(K\) because its discriminant
\((P-f_0)^2+4ab\) is nonzero; every other face is a binomial.  The standard
toric adjunction description therefore says that the interior point
\((1,1)\) gives precisely the nonzero holomorphic differential
\(du/F_w\) on the smooth projective toric model.  It cannot be exact.
If \(f\) is constant, \(P\) is affine-linear and was excluded in Section
4.  If \(a=0\) or \(b=0\), this reduces to one of the elementary families
already handled.  We obtain:

> **All separated three-generator Hamiltonians.**  For any permutation
> \((x_i,x_j,x_k)\) of \((u,v,w)\), no Hamiltonian
> \[
> P=a x_i+b x_j+f(x_k)
> \]
> has a Darboux mate when \((a,b)\ne(0,0)\).  This is an all-degree
> theorem for the separated family; it does not classify polynomials with
> nonlinear mixed terms.

A first mixed-coefficient family is still exactly solvable.  Let
\[
P=av+C(u)w+F(u),\qquad a\ne0,\quad C,F\in\mathbb C[u],
\]
and define on the generic fiber
\[
Y=2aw+C(u)u^2.
\]
The surface relation and Hamiltonian bracket give
\[
\begin{aligned}
Y^2
&=4a^2u+4au^2(P-F(u))+C(u)^2u^4=:G_P(u),\\
\{P,u\}&=Y.
\end{aligned} \tag{MC}
\]
Conversely, from \(u,Y\) one recovers
\[
w=\frac{Y-C(u)u^2}{2a},\qquad
v=\frac{P-C(u)w-F(u)}a.
\]
Thus (MC) is an isomorphism of the generic fiber with the affine
hyperelliptic curve \(Y^2=G_P(u)\), not merely a dominant auxiliary
model.

If \(G_P\) is not squarefree over \(\mathbb C(P)\), the generic fiber is
singular, so \(P\) has a critical point and cannot have a slice.  If it
is squarefree, a mate would force
\[
dQ=\frac{du}{Y}.
\]
The transcendental coefficient \(4aP\,u^2\) ensures
\(\deg_uG_P\ge2\).  For degree at least three, \(du/Y\) is a nonzero
holomorphic differential on the smooth projective hyperelliptic model.
For degree two, it has nonzero residues at the two points at infinity.
It is never exact.  Therefore:

> **Mixed linear-coefficient Hamiltonians.**  No Hamiltonian
> \[
> P=av+C(u)w+F(u),\qquad a\ne0,
> \]
> has a Darboux mate, for arbitrary polynomial \(C,F\) and arbitrary
> partner degree.  In particular this excludes nonlinear mixed supports
> \(u^mw\) throughout this family.

The other low-degree mixed seed from characteristic \(3\) also admits a
closed function-field analysis.  Let
\[
P=cw+\lambda uv,\qquad \lambda\ne0.
\]
An exact calculation in \(\operatorname{Frac}(B)\) gives
\[
Q_0
=-\frac{2\lambda w+cu}{2\lambda u(\lambda+P)},
\qquad
\{P,Q_0\}=1. \tag{BM}
\]
Every rational solution is \(Q_0+h(P)\), with
\(h\in\mathbb C(P)\).  The fiber \(P=0\) has a dense curve with \(u\ne0\):
for \(c\ne0\), take \(s=uv\) and use
\[
w=-\frac{\lambda s}{c},\qquad
u=\frac{\lambda^2s^2}{c^2(1+s)};
\]
the case \(c=0\) is even simpler.  At its generic point \(Q_0\) is
regular.  Thus a polynomial \(Q=Q_0+h(P)\) forces \(h\) to be regular at
\(P=0\).

Along \(D=(u,w)\), however,
\[
\operatorname{ord}_D(2\lambda w+cu)=1,\qquad
\operatorname{ord}_D(u)=2,\qquad
\lambda+P\ \text{is a unit}.
\]
Hence \(\operatorname{ord}_D(Q_0)=-1\).  A function \(h(P)\) regular at
zero cannot cancel this pole.  Therefore:

> **Bilinear characteristic-\(3\) seed obstruction.**  No
> \(P=cw+\lambda uv\), \(\lambda\ne0\), has a polynomial Darboux mate of
> any degree in characteristic zero.  In particular this excludes
> \(P=w+uv\), even though that Hamiltonian participates in an exact
> characteristic-\(3\) Darboux pair.

In fact the same mechanism survives an arbitrary polynomial \(u\)-tail.
Let
\[
P=cw+\lambda uv+F(u),\qquad \lambda\ne0,
\]
and put \(y=2\lambda w+cu\).  On the generic fiber,
\[
\begin{aligned}
y^2
&=u\left[c^2u+4\lambda\bigl(\lambda+P-F(u)\bigr)\right]
  =:K_P(u),\\
\{P,u\}&=uy.
\end{aligned} \tag{BT}
\]
The generic fiber has \(u\ne0\), and (BT) identifies its function field
with that of the displayed hyperelliptic curve.  A mate would force
\[
dQ=\frac{du}{uy}. \tag{BW}
\]
If \(K_P\) has a repeated nonzero root, the generic fiber is singular and
\(P\) already has a critical point.  Otherwise its smooth projective
model has a single point over \(u=0\), because \(u=0\) is a simple root:
the other factor there is
\(4\lambda(\lambda+P-F(0))\ne0\) over \(\mathbb C(P)\).

For \(n=\deg F\ge2\), \(\deg K_P=n+1\ge3\), so the projective curve has
positive genus.  The differential (BW) has a double pole at the point
over \(u=0\), is regular at every other finite point, and is regular at
infinity.  If it were \(dQ\), then \(Q\) would have exactly one simple
pole.  Such a function gives a degree-one morphism to
\(\mathbb P^1\), forcing the curve itself to be rational, a
contradiction.

If \(F(u)=\alpha u+\beta\), (BW) is exact in the function field, with
\[
Q_0
=-\frac{2\lambda w+cu}
        {2\lambda u(\lambda+P-\beta)}.
\]
Every rational mate is \(Q_0+h(P)\).  On the nonboundary component of
\(P=\beta\), \(Q_0\) is regular, so polynomiality forces \(h\) to be
regular at \(\beta\).  Along \(D\), \(Q_0\) has order \(-1\), which such
an \(h(P)\) cannot cancel.  Therefore:

> **Bilinear-plus-tail obstruction.**  No Hamiltonian
> \[
> P=cw+\lambda uv+F(u),\qquad \lambda\ne0,
> \]
> has a polynomial Darboux mate, for arbitrary \(F\in\mathbb C[u]\) and
> arbitrary mate degree.

The coefficient of \(w\) can also vary.  Let
\[
P=C(u)w+\lambda uv+F(u),\qquad \lambda\ne0,
\]
and set
\[
y=2\lambda w+C(u)u.
\]
Then
\[
\begin{aligned}
y^2
&=u\left[C(u)^2u+
4\lambda\bigl(\lambda+P-F(u)\bigr)\right]=:L_P(u),\\
\{P,u\}&=uy.
\end{aligned} \tag{VC}
\]
On the generic fiber \(u\ne0\), and one recovers
\[
w=\frac{y-C(u)u}{2\lambda},\qquad
v=\frac{P-C(u)w-F(u)}{\lambda u}.
\]
Thus the same curve analysis applies.  If the squarefree hyperelliptic
model has degree at least three, \(du/(uy)\) has exactly one double pole
on a positive-genus complete curve and cannot be exact.  A repeated
nonzero root instead makes the generic fiber singular.

The remaining genus-zero locus is exactly
\[
C(u)^2u-4\lambda F(u)=r_1u+r_0.
\]
Since the left side has constant term \(-4\lambda F(0)\), write
\[
F(u)=\frac{C(u)^2u}{4\lambda}+\alpha u+\beta.
\]
The forced differential then has the explicit primitive
\[
Q_0
=-\frac{2\lambda w+C(u)u}
        {2\lambda u(\lambda+P-\beta)}.
\]
As before, every rational mate is \(Q_0+h(P)\).  The nonboundary
component of \(P=\beta\) forces \(h\) to be regular at \(\beta\), whereas
\(Q_0\) has boundary order \(-1\).  Hence:

> **Variable-coefficient bilinear obstruction.**  No Hamiltonian
> \[
> P=C(u)w+\lambda uv+F(u),\qquad \lambda\ne0,
> \]
> has a polynomial Darboux mate, for arbitrary \(C,F\in\mathbb C[u]\).

Every one of the 17 degree-\((2,5)\) characteristic-\(3\) seed
Hamiltonians listed by the exhaustive search is either elementary or has
the displayed variable-coefficient form.  Consequently none of those
Hamiltonians can underlie a characteristic-zero polynomial pair, at any
partner degree.

The smallest generator perturbation absent from that characteristic-\(3\)
seed list is a linear \(v\)-term: neither \(v+w+uv\) nor
\(-v+w+uv\) has a partner through degree \(20\) in the exact modular
linear search.  Over characteristic zero the entire resulting support
family can be closed, without relying on that finite search.  Let
\[
P=A(u)v+C(u)w+F(u),\qquad
A(u)=b+\lambda u\ne0. \tag{AC}
\]
Set
\[
Y=2A(u)w+C(u)u^2.
\]
Then
\[
\begin{aligned}
Y^2
&=4A(u)^2u+4A(u)u^2(P-F(u))+C(u)^2u^4=:M_P(u),\\
\{P,u\}&=Y.
\end{aligned} \tag{AF}
\]
The function fields of the generic fiber and \(Y^2=M_P(u)\) agree.

First suppose \(b\ne0\).  If a repeated root \(\rho\) of \(M_P\) has
\(A(\rho)\ne0\), it is a singular point of the generic fiber and rules out
a slice.  If \(A(\rho)=0\), then \(\lambda\ne0\) and
\(\rho=-b/\lambda\ne0\).  A root also requires \(C(\rho)=0\), but its
derivative is then
\[
M_P'(\rho)=4\lambda\rho^2(P-F(\rho))\ne0
\]
over \(\mathbb C(P)\).  Hence it is simple.  Under the slice hypothesis,
\(M_P\) is therefore squarefree.

If \(\lambda\ne0\), the coefficient \(4P\,A(u)u^2\) forces
\(\deg M_P\ge3\).  The required differential \(du/Y\) is a nonzero
holomorphic differential on the complete hyperelliptic model and cannot
be exact.  If \(\lambda=0\), (AC) is the already excluded
\(av+C(u)w+F(u)\) family.  Finally, if \(b=0\), (AC) is exactly the
variable-coefficient bilinear family above.  Thus:

> **Affine \(v\)-coefficient obstruction.**  No Hamiltonian
> \[
> P=(b+\lambda u)v+C(u)w+F(u),
> \qquad (b,\lambda)\ne(0,0),
> \]
> has a polynomial Darboux mate, for arbitrary \(C,F\in\mathbb C[u]\)
> and arbitrary mate degree.

The next degree-two support absent from the characteristic-\(3\) list is
\(v^2\): neither \(w+uv+v^2\) nor \(w+uv-v^2\) has a partner through
degree \(20\) in the exact modular slice search.  Let, in characteristic
zero,
\[
P=cw+\lambda uv+\mu v^2,\qquad c\lambda\mu\ne0,
\]
and work over \(K=\mathbb C(P)\).  Put
\[
L=\lambda+2P-2cw-2\mu v^2
\]
and
\[
F(v,w)=L^2-\lambda^2(1+4vw^2). \tag{VQ}
\]
Since \(L=\lambda(1+2uv)\) on the fiber, (VQ) is its exact plane-curve
equation.  Direct differentiation gives
\[
\{P,v\}=\frac{F_w}{4\lambda},\qquad
\{P,w\}=-\frac{F_v}{4\lambda}.
\]
Thus a mate would force
\[
dQ=4\lambda\frac{dv}{F_w}
    =-4\lambda\frac{dw}{F_v}. \tag{VR}
\]

The Newton polygon of \(F\) has vertices
\[
(0,0),\quad(4,0),\quad(1,2),\quad(0,2),
\]
and \((1,1)\) is strictly interior.  Its bottom and left face polynomials
factor as
\[
4(P-\mu v^2)(\lambda+P-\mu v^2),\qquad
4(P-cw)(\lambda+P-cw),
\]
which are squarefree over \(K\).  The remaining two faces are the
binomials
\[
4w^2(c^2-\lambda^2v),\qquad
4v(\mu^2v^3-\lambda^2w^2).
\]
Hence the toric boundary is nondegenerate.  If the affine generic curve
were singular, \(P\) would have a critical point and already be excluded.
Otherwise toric adjunction identifies \(dv/F_w\) with the nonzero
holomorphic differential belonging to the interior point \((1,1)\).
It cannot be exact.  Therefore:

> **Quadratic \(v^2\)-perturbation obstruction.**  No
> \(P=cw+\lambda uv+\mu v^2\), with \(c\lambda\mu\ne0\), has a
> polynomial Darboux mate of any degree.

The same proof does not depend on the tail being quadratic.  Let
\[
P=cw+\lambda uv+G(v),\qquad c\lambda\ne0,
\]
where \(n=\deg G\ge2\), and set
\[
L=\lambda+2P-2cw-2G(v),\qquad
\mathcal F=L^2-\lambda^2(1+4vw^2).
\]
As before,
\[
D_P=\frac1{4\lambda}
\left(\mathcal F_w\partial_v-\mathcal F_v\partial_w\right).
\]
The Newton polygon now has vertices
\[
(0,0),\quad(2n,0),\quad(1,2),\quad(0,2),
\]
and \((1,1)\) remains strictly interior.  The bottom face is
\[
4(P-G(v))(\lambda+P-G(v)).
\]
It is squarefree over \(\mathbb C(P)\): each factor \(G(v)-P\) is
separable in characteristic zero because \(P\) is transcendental, and the
two factors cannot share a root because \(\lambda\ne0\).  The left face is
\[
4(P-G(0)-cw)(\lambda+P-G(0)-cw),
\]
and the other two faces are binomials.  Toric adjunction again makes
\(dv/\mathcal F_w\) a nonzero holomorphic differential, unless the affine
generic curve is singular, in which case \(P\) has a critical point.
Thus no mate exists.  If \(\deg G\le1\), the Hamiltonian lies in the
affine \(v\)-coefficient family already excluded.  Consequently:

> **Arbitrary \(v\)-tail obstruction.**  No
> \[
> P=cw+\lambda uv+G(v),\qquad c\lambda\ne0,
> \]
> has a polynomial Darboux mate, for any \(G\in\mathbb C[v]\) or any
> partner degree.

The next apparent perturbation \(w^2\) must first be reduced using
\[
w^2=u+u^2v.
\]
It is a genuine new construction lead in characteristic \(3\).  For
example, over \(\mathbb F_3\),
\[
\begin{aligned}
P&=u+w+uv+u^2v,\\
Q&=-v+w-vw+uv^2+v^2w+uv^2w
\end{aligned}
\]
satisfies \(\{P,Q\}=1\).  The analogous pair with the \(w^2\)-coefficient
\(-1\) is also verified by the exact finite-field search.

Over characteristic zero, consider the entire simple-zero coefficient
family
\[
P=uB(u)v+C(u)w+F(u),\qquad
B(u)=b+\kappa u,\quad b\ne0. \tag{SZ}
\]
Put
\[
y=2B(u)w+C(u)u.
\]
Then
\[
\begin{aligned}
y^2
&=u\left[4B(u)^2+4B(u)(P-F(u))+C(u)^2u\right]
  =:N_P(u),\\
\{P,u\}&=uy.
\end{aligned} \tag{SH}
\]
On the generic fiber \(u\ne0\), these formulas give its hyperelliptic
function field, and a mate would force
\[
dQ=\frac{du}{uy}. \tag{SD}
\]

At \(u=0\), the second factor of \(N_P\) is
\(4b(b+P-F(0))\ne0\), so there is one simple branch point and (SD) has
one double pole there.  A repeated nonzero root away from \(B=0\) is a
singular point of the generic fiber.  At the possible root
\(\rho=-b/\kappa\) of \(B\), a root also requires \(C(\rho)=0\), but the
derivative of the second factor is
\[
4\kappa(P-F(\rho))\ne0,
\]
so it is simple.

If \(\deg N_P\ge3\), the smooth projective model has positive genus.
Exactness of (SD) would give a rational function with one simple pole and
therefore a degree-one map to \(\mathbb P^1\), impossible.  The only
remaining locus is where the bracketed factor in (SH) is affine in \(u\).
Writing \(\beta=F(0)\), its constant term is
\(4b(b+P-\beta)\), and (SD) has the explicit primitive
\[
Q_0
=-\frac{2B(u)w+C(u)u}
        {2b\,u(b+P-\beta)}.
\]
Every rational mate is \(Q_0+h(P)\).  Regularity on the nonboundary
component of \(P=\beta\) forces \(h\) to be regular at \(\beta\), while
\(Q_0\) has boundary order \(-1\).  Thus:

> **Simple-zero \(v\)-coefficient obstruction.**  No Hamiltonian
> \[
> P=u(b+\kappa u)v+C(u)w+F(u),\qquad b\ne0,
> \]
> has a polynomial Darboux mate, for arbitrary \(C,F\in\mathbb C[u]\)
> and arbitrary mate degree.

For the literal perturbation
\[
P=w+uv+\kappa w^2
=w+uv+\kappa u+\kappa u^2v,
\]
one has \(B=1+\kappa u,\ C=1,\ F=\kappa u\), and the bracketed factor
in (SH) is affine.  Its rational primitive specializes to
\[
Q_0=-\frac{2(1+\kappa u)w+u}{2u(1+P)},
\]
whose order-\(-1\) boundary pole proves the all-degree
characteristic-zero obstruction directly.

### The new characteristic-\(3\) seeds do not lift modulo \(9\)

The characteristic-\(3\) construction above has an immediate,
degree-independent first Hensel obstruction.  Use the displayed integer
representatives \(P_k,Q_k\), \(k=\pm1\), and write
\[
\{P_k,Q_k\}=1+3E_k.
\]
Any lift modulo \(9\), with completely arbitrary polynomial corrections,
would have the form
\[
P=P_k+3A,\qquad Q=Q_k+3B
\]
and would require
\[
\{A,Q_k\}+\{P_k,B\}=-E_k\pmod3. \tag{W9}
\]
Define the coefficient functional on \(B_{\mathbb F_3}\)
\[
\ell(R)=[v]R+[uv^2]R.
\]
Direct monomial inspection of the bracket shows that the only
\(A\)-monomials capable of contributing to these two output coefficients
are
\[
v,\quad v^2,\quad vw,
\]
and the only such \(B\)-monomial is \(v^2\).  On each of these four
columns, the two coefficients are negatives of one another.  Therefore
\[
\ell\bigl(\{A,Q_k\}+\{P_k,B\}\bigr)=0
\]
for all polynomial \(A,B\), without a degree or support bound.  But exact
integer expansion gives
\[
\ell(-E_k)=1\pmod3
\]
for both signs.  Equation (W9) is impossible.

> **All-support first Hensel obstruction.**  Both new \(w^2\)-perturbed
> characteristic-\(3\) pairs fail to lift modulo \(9\), even with
> arbitrary expanding polynomial support.  Consequently neither can lift
> modulo \(27\) or define a \(3\)-adic tower.

This behavior is strictly stronger than the previously examined
\(P=w\pm u^2\) seeds.  Those admit a first correction modulo \(9\) once
degree-eight support is allowed; no all-support statement about their next
modulo-\(27\) equation is claimed here.  The new \(w^2\) seeds are already
killed by the two-coefficient functional above.  They also differ from the
homogeneous \(P=w\) seed, whose support-expanding Hensel tower continues to
every order.

### The next degree-three orbit: \(uvw\)

The exact \(\mathbb F_3\) slice search next tests the three reduced
degree-three perturbations
\[
uv^2,\qquad uvw,\qquad v^2w.
\]
For each sign, none has a partner through degree \(25\).  The \(uvw\)
orbit has an all-degree explanation that works directly in the function
field, including in characteristic \(3\).

Put \(s=uv\).  Then
\[
\{s,w\}=w^2,\qquad
\operatorname{Frac}(B)=k(s,w),
\]
because
\[
u=\frac{w^2}{1+s},\qquad
v=\frac{s(1+s)}{w^2}.
\]
For
\[
P=w+s+\kappa sw=w+uv+\kappa uvw,\qquad \kappa\ne0,
\]
the generic fiber is rational:
\[
s=\frac{P-w}{1+\kappa w}.
\]
Moreover
\[
\{P,w\}=w^2(1+\kappa w).
\]
Thus any rational mate would force
\[
\begin{aligned}
dQ
&=\frac{dw}{w^2(1+\kappa w)}\\
&=\left(
\frac1{w^2}-\frac{\kappa}{w}
+\frac{\kappa^2}{1+\kappa w}
\right)dw. \tag{UWR}
\end{aligned}
\]
The residues at \(w=0\) and \(w=-1/\kappa\) are respectively
\(-\kappa\) and \(+\kappa\).  Exact rational differentials have zero
residues in every characteristic.  Therefore:

> **\(uvw\)-perturbation obstruction.**  No
> \[
> P=w+uv+\kappa uvw,\qquad \kappa\ne0,
> \]
> has a rational Darboux mate.  This holds both in characteristic zero
> and over \(\mathbb F_3\), explaining the complete absence of the two
> signed perturbations from the modular slice search.

The \(uv^2\) orbit also reduces to a rational plane curve with a
normalization-residue obstruction.  Since
\[
uv^2=\frac{s^2(1+s)}{w^2},
\]
the Hamiltonian
\[
P=w+uv+\kappa uv^2
=w+s+\kappa\frac{s^2(1+s)}{w^2}
\]
has generic plane model
\[
F(s,w)
=w^3+(s-P)w^2+\kappa s^2(1+s)=0. \tag{UV2}
\]
Here \(F=w^2(P(s,w)-P)\), and the Poisson equation gives exactly
\[
D_P=F_s\partial_w-F_w\partial_s.
\]
A mate would force the curve-residue differential
\[
dQ=-\frac{ds}{F_w}=\frac{dw}{F_s}. \tag{UVR}
\]

The affine model (UV2) has a missing singular point at \((s,w)=(0,0)\).
Blow it up by writing \(s=yw\).  Dividing by \(w^2\) gives
\[
-P+\kappa y^2
+w(1+y+\kappa y^3)=0.
\]
Thus the normalization has two branches there,
\[
y=a_\pm=\pm\sqrt{P/\kappa}.
\]
Along either branch, \(ds=a_\pm\,dw+O(w\,dw)\), while
\[
F_w=w(3w+2s-2P)=-2Pw+O(w^2).
\]
The residues of (UVR) are therefore
\[
\operatorname{res}_{a_\pm}(UVR)
=\frac{a_\pm}{2P}
=\pm\frac1{2\sqrt{\kappa P}},
\]
both nonzero.  This calculation remains valid over characteristic \(3\),
where \(2\ne0\).  Hence:

> **\(uv^2\)-perturbation obstruction.**  No
> \[
> P=w+uv+\kappa uv^2,\qquad \kappa\ne0,
> \]
> has a rational Darboux mate, in characteristic zero or characteristic
> \(3\).

The last minimal degree-three orbit is \(v^2w\).  In the same chart,
\[
v^2w=\frac{s^2(1+s)^2}{w^3},
\]
so
\[
P=w+uv+\kappa v^2w
=w+s+\kappa\frac{s^2(1+s)^2}{w^3}
\]
has generic plane model
\[
F(s,w)
=w^4+(s-P)w^3+\kappa s^2(1+s)^2=0. \tag{V2W}
\]
Since \(F=w^3(P(s,w)-P)\),
\[
D_P=\frac1w\left(F_s\partial_w-F_w\partial_s\right).
\]
A mate would force
\[
dQ=-\frac{w\,ds}{F_w}=\frac{w\,dw}{F_s}. \tag{V2R}
\]

The differential (V2R) extends holomorphically across every point of the
complete normalization in characteristic zero.  At \((s,w)=(0,0)\), use
\[
w=t^2,\qquad s=a t^3+\cdots,\qquad \kappa a^2=P.
\]
Then
\[
F_w=-3P\,t^4+\cdots,\qquad
-\frac{w\,ds}{F_w}=\frac{a}{P}\,dt+\cdots.
\]
At \((s,w)=(-1,0)\), writing \(s+1=a t^3+\cdots\) gives
\[
\kappa a^2=P+1,\qquad
-\frac{w\,ds}{F_w}=\frac{a}{P+1}\,dt+\cdots.
\]
Thus both finite cusp branches are regular.

At infinity put \(x=1/s\) and \(t=w/s\).  The equation becomes
\[
\phi(t,x)
=t^4+(1-Px)t^3+\kappa(1+x)^2=0,
\]
and (V2R) is, up to sign,
\[
\frac{t\,dx}{\phi_t}.
\]
It is regular at every simple root of
\[
\phi(t,0)=t^4+t^3+\kappa.
\]
This polynomial has a repeated nonzero root only at
\[
t=-\frac34,\qquad \kappa=\frac{27}{256}.
\]
At that value \(\phi_{tt}=9/4\ne0\), while
\(\phi_x=27(2P+1)/128\ne0\) over \(\mathbb C(P)\).  Hence locally
\(x\) is a nonzero constant times \((t+3/4)^2\), and
\(dx/\phi_t\) is still regular on the normalization.

Therefore (V2R) is a nonzero holomorphic differential on a complete
smooth curve.  A holomorphic exact rational differential must vanish, so:

> **\(v^2w\)-perturbation obstruction.**  No
> \[
> P=w+uv+\kappa v^2w,\qquad \kappa\ne0,
> \]
> has a rational Darboux mate over characteristic zero.  The exact
> characteristic-\(3\) search also finds no polynomial mate through
> degree \(25\), but no all-degree characteristic-\(3\) claim is made for
> this orbit.

The first new reduced degree-four support is \((uv)^2\), and in fact the
same argument closes every nonlinear polynomial tail in \(uv\).  Put
\(s=uv\) as above and consider
\[
P=cw+H(s),\qquad c\ne0,\quad \deg H\ge2. \tag{ST}
\]
The generic fiber is rational:
\[
w=\frac{P-H(s)}c.
\]
Since \(\{s,w\}=w^2\), its Hamiltonian derivation satisfies
\[
D_P(s)=\{P,s\}=-cw^2
              =-\frac{(P-H(s))^2}{c}.
\]
Consequently a rational mate would force
\[
dQ=-\frac{c\,ds}{(P-H(s))^2}. \tag{STR}
\]
Let \(\alpha\) be any root of \(H(s)-P\).  It is simple over
\(\mathbb C(P)\), and direct local expansion gives
\[
\operatorname{res}_{s=\alpha}(STR)
=\frac{cH''(\alpha)}{H'(\alpha)^3}. \tag{STRes}
\]
The polynomial \(H(s)-P\) is irreducible over \(\mathbb C(P)\), whereas
\(\deg H''<\deg H\).  In characteristic zero \(H''\ne0\), so
\(H''(\alpha)\ne0\).  Thus (STR) has a nonzero residue and is not exact.
Therefore:

> **Nonlinear \(uv\)-tail obstruction.**  No
> \[
> P=cw+H(uv),\qquad c\ne0,\quad \deg H\ge2,
> \]
> has a rational Darboux mate over characteristic zero.

For the minimal orbit \(H(s)=s+\kappa s^2\), formula (STRes) is
\[
\frac{2c\kappa}{(1+2\kappa\alpha)^3},
\]
which is also nonzero in characteristic \(3\).  Hence
\(w+uv+\kappa u^2v^2\), \(\kappa\ne0\), has no rational mate in
characteristic \(3\) as well.  The exact modular slice calculation
independently finds no polynomial mate for either sign through degree
\(25\).

The next orbit \(uv^3\) is exceptional in the finite-field triage.  For
the positive sign, the exact pair over \(\mathbb F_3\) is
\[
\begin{aligned}
P={}&w+uv+uv^3,\\
Q={}&-u-v+w+uv-u^2v+uv^2+uvw+v^2w-u^2v^2+v^3w\\
   &+uv^4+uv^3w-v^4w+uv^4w-u^2v^5-uv^5w+v^6w+uv^7w,
\end{aligned} \tag{UV3Pair}
\]
and direct reduction gives \(\{P,Q\}=1\).  Its partner has generator
degree nine.  The negative sign has no modular partner through degree
\(25\).

Characteristic zero still has an all-degree obstruction.  In the
\((s,w)\)-chart,
\[
uv^3=\frac{s^3(1+s)^2}{w^4},
\]
so
\[
P=w+s+\kappa\frac{s^3(1+s)^2}{w^4},\qquad \kappa\ne0,
\]
has generic plane model
\[
F=w^5+(s-P)w^4+\kappa s^3(1+s)^2=0. \tag{UV3}
\]
Since \(F=w^4(P(s,w)-P)\),
\[
D_P=\frac1{w^2}
\left(F_s\partial_w-F_w\partial_s\right),
\]
and a mate would force
\[
dQ=-\frac{w^2\,ds}{F_w}. \tag{UV3R}
\]

This differential is regular on the complete normalization.  At
\((s,w)=(0,0)\), put
\[
w=t^3,\qquad s=a t^4+\cdots,\qquad \kappa a^3=P.
\]
Then (UV3R) is \(a\,dt/P+\cdots\).  At \((s,w)=(-1,0)\), put
\[
w=t,\qquad s+1=a t^2+\cdots,\qquad
\kappa a^2=-(P+1);
\]
there it is \(a\,dt/(2(P+1))+\cdots\).

At infinity set \(x=1/s\) and \(t=w/s\).  The equation and differential
become
\[
\phi=t^5+(1-Px)t^4+\kappa(1+x)^2=0,
\qquad
\frac{t^2\,dx}{\phi_t}.
\]
The roots at \(x=0\) are simple except at
\[
t=-\frac45,\qquad \kappa=-\frac{256}{3125}.
\]
At this sole resonance,
\[
\phi_{tt}=-\frac{64}{25}\ne0,\qquad
\phi_x=-\frac{256(5P+2)}{3125}\ne0
\]
over \(\mathbb C(P)\), so \(x\) is a unit times
\((t+4/5)^2\) and the differential remains regular.  Thus (UV3R) is a
nonzero holomorphic differential on a complete smooth curve and cannot
be exact:

> **\(uv^3\)-perturbation obstruction.**  No
> \[
> P=w+uv+\kappa uv^3,\qquad \kappa\ne0,
> \]
> has a rational Darboux mate in characteristic zero.

The exact modular pair (UV3Pair) also fails immediately as a lifting
seed.  For its centered integer representatives write
\(\{P,Q\}=1+3E\), and define over \(\mathbb F_3\)
\[
\ell(R)=[v^4]R+[uv^5]R.
\]
The only \(A\)-monomials that can contribute to these coefficients in
\(\{A,Q\}\) are
\[
v,\quad v^2,\quad v^5,\quad v^4w,
\]
and the only contributing \(B\)-monomial in \(\{P,B\}\) is \(v^5\).
On every column the two selected coefficients sum to zero, whereas
\(\ell(-E)=1\).  Hence
\[
\{A,Q\}+\{P,B\}=-E\pmod3
\]
has no polynomial solution with arbitrary support.

> **All-support \(uv^3\) Hensel obstruction.**  The new degree-nine
> characteristic-\(3\) pair does not lift modulo \(9\), and therefore
> cannot start a characteristic-zero or \(3\)-adic lift.

The support \(uv^2w\) has an even shorter obstruction.  Here
\[
uv^2w=\frac{s^2(1+s)}w
\]
and the generic plane curve is
\[
F=w^2+(s-P)w+\kappa s^2(1+s)=0. \tag{UV2W}
\]
Because \(F=w(P(s,w)-P)\),
\[
D_P=w(F_s\partial_w-F_w\partial_s),\qquad
dQ=-\frac{ds}{wF_w}.
\]
At \((s,w)=(-1,0)\), putting \(r=s+1\) gives
\[
w=\frac{\kappa}{P+1}r+O(r^2),\qquad
dQ=\frac1\kappa\frac{dr}{r}+O(dr).
\]
Thus:

> **\(uv^2w\)-perturbation obstruction.**  No
> \(w+uv+\kappa uv^2w\), \(\kappa\ne0\), has a rational mate in
> characteristic zero or characteristic \(3\).

For \(u^2vw\), the chart identity
\[
u^2vw=\frac{s w^3}{1+s}
\]
gives
\[
F=(1+s)(w+s-P)+\kappa s w^3=0,\qquad
dQ=-\frac{(1+s)\,ds}{w^2F_w}. \tag{U2VW}
\]
Completing this quadratic in \(s\) produces
\[
y^2=\Delta(w),\qquad
\Delta=(1+w-P+\kappa w^3)^2-4(w-P).
\]
The polynomial \(\Delta\) has degree six, and its exact discriminant is
\[
\begin{aligned}
-4096\kappa^8(P+1)^3\bigl(&729P^4\kappa^2
+729P^3\kappa^2+216P^2\kappa\\
&+972P\kappa+729\kappa+16\bigr),
\end{aligned}
\]
which is nonzero over \(\mathbb C(P)\).  The normalization therefore has
genus two.  In the \(w\)-coordinate,
\[
dQ=\frac{(1+s)\,dw}{w^2y}.
\]
It is regular at the branch over \(s=-1\), at all ramification points,
and at both points at infinity.  At the other point over \(w=0\),
\[
s=P-w+O(w^3),\qquad dQ=\frac{dw}{w^2}+O(dw);
\]
this is its unique double pole and its residue is zero.  If it were
exact in characteristic zero, its primitive would be a rational
function with one simple pole, giving a degree-one map from a genus-two
curve to \(\mathbb P^1\), impossible.  Hence:

> **\(u^2vw\)-perturbation obstruction.**  No
> \(w+uv+\kappa u^2vw\), \(\kappa\ne0\), has a rational mate in
> characteristic zero.

For \(v^3w\), use
\[
v^3w=\frac{s^3(1+s)^3}{w^5}.
\]
The generic curve and forced differential are
\[
F=w^6+(s-P)w^5+\kappa s^3(1+s)^3=0,\qquad
dQ=-\frac{w^3\,ds}{F_w}. \tag{V3W}
\]
At the groups over \(s=0\) and \(s=-1\), the respective normalizations
\[
\begin{array}{lll}
w=t^3,&s=a t^5+\cdots,&\kappa a^3=P,\\
w=t^3,&s+1=a t^5+\cdots,&\kappa a^3=-(P+1)
\end{array}
\]
make (V3W) regular.  At infinity, with \(x=1/s,t=w/s\),
\[
\phi=t^6+(1-Px)t^5+\kappa(1+x)^3,\qquad
dQ=\frac{t^3\,dx}{\phi_t}.
\]
The only repeated nonzero root occurs at
\[
t=-\frac56,\qquad \kappa=\frac{3125}{46656}.
\]
There
\[
\phi_{tt}=\frac{625}{216},\qquad
\phi_x=\frac{3125(2P+1)}{15552},
\]
so the differential remains regular on the normalization.  It is
nonzero and holomorphic, hence not exact in characteristic zero.

> **\(v^3w\)-perturbation obstruction.**  No
> \(w+uv+\kappa v^3w\), \(\kappa\ne0\), has a rational mate in
> characteristic zero.

Finally, the remaining coefficient-side orbit satisfies
\[
u^3v=\frac{s w^4}{(1+s)^2}.
\]
Its plane curve and forced differential are
\[
F=(1+s)^2(w+s-P)+\kappa s w^4=0,\qquad
dQ=\frac{(1+s)^2\,dw}{w^2F_s}. \tag{U3V}
\]
The Newton polygon has vertices
\[
(0,0),(3,0),(1,4),(0,1)
\]
and four interior lattice points.  Its only degenerate boundary point is
the tacnode at \((s,w)=(-1,0)\): writing
\(s=-1+a w^2+\cdots\) gives
\[
(P+1)a^2+\kappa=0.
\]
This has delta-invariant two; every other face is nondegenerate, so the
generic normalization has genus two.  The differential (U3V) is regular
at the two tacnode branches, all other finite points, and the three
points at infinity.  At the point \(s=P,w=0\),
\[
s=P-w+O(w^4),\qquad dQ=\frac{dw}{w^2}+O(w^2\,dw),
\]
so it has exactly one double pole and zero residue.  The same one-pole
argument yields:

> **\(u^3v\)-perturbation obstruction.**  No
> \(w+uv+\kappa u^3v\), \(\kappa\ne0\), has a rational mate in
> characteristic zero.

For the signed \(u^2vw,v^3w,u^3v\) orbits, the exact
characteristic-\(3\) search finds no polynomial mate through degree
\(25\); no all-degree characteristic-\(3\) claim is made for these
three one-pole or holomorphic-differential arguments.

### A monomial-cone theorem

The preceding calculations admit a common formulation that avoids
support-by-support enumeration.  Put \(s=uv\).  Every reduced monomial
has the Laurent-chart expression
\[
u^av^bw^c
=s^b(1+s)^{b-a}w^{2(a-b)+c},
\qquad c\in\{0,1\}. \tag{MC0}
\]
Consider
\[
P=w+s+\kappa u^av^bw^c,\qquad \kappa\ne0. \tag{MC}
\]

First suppose \(b>a\), and set
\[
r=b-a,\qquad m=2r-c.
\]
The generic curve and forced differential are
\[
\begin{aligned}
F&=w^{m+1}+(s-P)w^m+\kappa s^b(1+s)^r=0,\\
\eta&=-\frac{w^{m-2}\,ds}{F_w}. \tag{MCV}
\end{aligned}
\]
The Newton lattice point representing \(\eta\) is \((1,m-1)\).  Direct
convex-hull calculation shows
\[
(1,m-1)\in\operatorname{Int}(\Newt F)
\quad\Longleftrightarrow\quad
m>b
\quad\Longleftrightarrow\quad
b>2a+c. \tag{MCI}
\]
In this strict cone, toric adjunction makes \(\eta\) holomorphic away
from the two finite degenerate groups.  Their normalization orders are
\[
\frac{m-b}{\gcd(m,b)}-1,\qquad
\frac{m-r}{\gcd(m,r)}-1,
\]
both nonnegative.  The only possible non-binomial infinity face occurs
when \(a+c=1\).  Writing \(N=m+1=b+r\), it is
\[
\phi=t^N+(1-Px)t^{N-1}+\kappa(1+x)^r.
\]
Its sole repeated nonzero root has
\[
t=-\frac{N-1}{N},\qquad
\phi_{tt}=N t^{N-2}\ne0,\qquad
\phi_x=-t^{N-1}\!\left(P+\frac rN\right)\ne0.
\]
Thus \(\eta\) remains regular there as well.  It is a nonzero
holomorphic differential and is not exact.

On the wall \(m=b\), equivalently \(b=2a+c\), the branches over the
origin have \(s=A w+\cdots\), where
\(\kappa A^b=P\).  Formula (MCV) has residue
\[
\frac{A}{bP}\ne0. \tag{MCRes}
\]
On the adjacent wall \(m=b-1\), equivalently
\[
b=2a+c-1,
\]
the origin is a single branch carrying the unique double pole of
\(\eta\).  After resolving the \(s=-1\) face, the normalization genus is
\[
g=
\begin{cases}
2(a-1),&c=0,\\
2a-1,&c=1.
\end{cases} \tag{MCG}
\]
It is positive in every applicable case.  An exact primitive would have
one simple pole and force a degree-one map to \(\mathbb P^1\), which is
impossible.  The smallest \(c=1\) case is \(uv^2w\), where the additional
residue \(1/\kappa\) already gives the contradiction.

Now suppose \(a>b\ge1\), and put
\[
d=a-b,\qquad e=2d+c.
\]
Then
\[
\begin{aligned}
F&=(1+s)^d(w+s-P)+\kappa s^b w^e=0,\\
\eta&=\frac{(1+s)^d\,dw}{w^2F_s}. \tag{MCU}
\end{aligned}
\]
Its Newton polygon is
\[
(0,0),\quad(d+1,0),\quad(b,e),\quad(0,1).
\]
The only degenerate face has local type \(z^d+w^e\) at \(s=-1\).
Writing
\[
\begin{aligned}
g_0&=\gcd(d,e),\\
g_1&=\gcd(|b-d-1|,e),\\
g_2&=\gcd(b,e-1),
\end{aligned}
\]
Pick's theorem minus that face's delta invariant gives the exact
normalization genus
\[
g=e+\frac{b-g_0-g_1-g_2}{2}. \tag{MCUG}
\]
Since \(g_0\le d,\ g_1\le e,\ g_2\le b\),
\[
g\ge\frac{e-d}{2}=\frac{d+c}{2}>0.
\]
The differential (MCU) is regular at the resolved \(s=-1\) branches
and at infinity.  Its sole pole is
\[
s=P-w+O(w^e),\qquad
\eta=\frac{dw}{w^2}+O(dw)
\]
at the other point over \(w=0\).  The same one-pole argument excludes
exactness.

Finally, on the diagonal \(a=b\), the case \(c=0\) is the nonlinear
\(H(uv)\) residue theorem above, while for \(c=1\)
\[
P=w+s+\kappa s^a w
\]
is rational and its forced differential has residue
\(-\kappa aP^{a-1}\) at \(s=P\).

Combining these cases gives:

> **Monomial-cone obstruction.**  In characteristic zero, (MC) has no
> rational Darboux mate whenever
> \[
> a>b\ge1,\qquad
> a=b\ge1\ \text{outside the affine base case},\qquad\text{or}\qquad
> b>a\ \text{and}\ b\ge2a+c-1.
> \]
> Thus all reduced monomial perturbations outside the still-open middle
> wedge
> \[
> a<b<2a+c-1
> \]
> are structurally excluded, apart from the previously settled pure-tail
> boundary cases.

This theorem contains every reduced perturbation of generator degree at
most five.  In particular the degree-five supports \(uv^4,v^4w\) lie
in the strict holomorphic cone, \(uv^3w\) lies on the residue wall,
\(u^2v^3\) lies on the one-pole wall, every \(a>b\) support lies in
(MCU), and \(u^2v^2w\) is diagonal.

The middle wedge itself has two further uniform obstructions.  Continue
to write
\[
r=b-a,\qquad m=2r-c,
\]
and put
\[
g=\gcd(m,b),\qquad M=m/g,\qquad B=b/g.
\]
At the branches over \((s,w)=(0,0)\), use
\[
s=t^M,\qquad w=A t^B y(t),\qquad A^m=\kappa/P,\quad y(0)=1.
\]
The forced differential has leading order
\[
\eta=
\frac{M}{A mP}\,
t^{M-B-1}\bigl(1+O(t)\bigr)\,dt. \tag{MW0}
\]
Its residue vanishes unless \(M=1\).  When \(m\mid b\), write
\(B=b/m\).  The normalized curve equation determines, through degree
\(B-1\),
\[
y^m=\frac{(1+t)^r}{1-t/P}+O(t^B).
\]
Substitution into (MW0) gives the exact residue
\[
\operatorname{res}\eta
=\frac1{A mP}
[t^{B-1}]
(1+t)^{-r/m}
(1-t/P)^{-(m-1)/m}. \tag{MWRes}
\]
This coefficient is nonzero over \(\mathbb C(P)\).  If \(m>1\), its
highest \(P^{-1}\)-degree term, of degree \(B-1\), has nonzero
coefficient.  If \(m=1\), it is the nonzero coefficient of
\((1+t)^{-r}\).  Therefore:

> **Middle-wedge residue sublattice.**  Every (MC) in the middle wedge
> with
> \[
> 2(b-a)-c\mid b
> \]
> has no rational mate in characteristic zero, for every
> \(\kappa\ne0\).

There is also a generic-coefficient obstruction throughout the entire
wedge.  Introduce a deformation parameter \(\tau\):
\[
P_\tau=w+s+\tau\kappa
\frac{s^b(1+s)^r}{w^m}.
\]
At \(\tau=0\), its generic fiber is the rational curve \(w=P-s\).
Expanding the forced differential gives
\[
\eta_\tau
=-\frac{ds}{(P-s)^2}
-\tau\kappa(m+2)
\frac{s^b(1+s)^r}{(P-s)^{m+3}}\,ds
+O(\tau^2). \tag{MWDef}
\]
The residue of the coefficient of \(\tau\) at \(s=P\) is
\[
\frac{(-1)^m\kappa}{(m+1)!}
\left.
\frac{d^{m+2}}{ds^{m+2}}
\bigl(s^b(1+s)^r\bigr)
\right|_{s=P}. \tag{MWVar}
\]
It is nonzero: the polynomial being differentiated has degree
\[
b+r=m+2+(a+c-2)\ge m+2
\]
throughout the middle wedge.  If \(\eta_\tau\) were exact over
\(\mathbb C(\tau,P)\), after subtracting \(\tau\)-dependent constants
its primitive could be expanded at \(\tau=0\), forcing every coefficient
in (MWDef) to be exact.  The nonzero residue (MWVar) contradicts this.

> **Generic middle-wedge obstruction.**  For every exponent triple in
> the middle wedge, (MC) has no rational mate when its coefficient is
> transcendental over \(\mathbb C\).  Equivalently, the generic
> one-parameter monomial perturbation is excluded.  This does **not**
> rule out every isolated fixed complex value of \(\kappa\); outside the
> residue sublattice, that specialization issue remains open.

The first fixed-coefficient wall beyond the residue sublattice can be
closed by canonical jets.  Put
\[
\delta=b-m=2a+c-b.
\]
At the \(g=\gcd(m,b)\) points \(p_\nu\) over the origin, (MW0) shows that
a primitive of \(\eta\), if it existed, could have poles bounded by
\[
E=\frac{\delta}{g}\sum_{\nu=1}^g p_\nu. \tag{MWE}
\]
Indeed \(\eta\) has order \(-\delta/g-1\) at each point.  A toric
adjoint
\[
\omega_{i,j,k}
=s^{i-1}(1+s)^kw^{j-1}\frac{ds}{F_w} \tag{MWAdj}
\]
has origin order
\[
M i+B(j-m)-1, \tag{MWOrd0}
\]
and, if \(h=\gcd(m,r)\), order
\[
\frac{r(j-m)+m(k+1)-h}{h} \tag{MWOrd1}
\]
on every branch over \(s=-1\).  Requiring the horizontal lattice segment
\((i,j),\ldots,(i+k,j)\) to lie in the strict interior of the Newton
polygon makes (MWAdj) holomorphic at every other toric boundary point.

Now suppose \(\delta=2\).  For \(c=0\), write
\[
m=2r,\qquad b=2r+2.
\]
There are two origin branches, and the two holomorphic adjoints
\[
\begin{aligned}
\omega_0&=
s^{r-1}(1+s)^{\lfloor(r-1)/2\rfloor}w^r\frac{ds}{F_w},\\
\omega_1&=
s^{2r}(1+s)^{r-1}\frac{ds}{F_w}
\end{aligned} \tag{MW2e}
\]
both have order zero there.  Their leading coefficients are proportional
to \(A^{1-r}\) and \(A^{1-2r}\), respectively.  Their ratio is
proportional to \(A^r\), whose sign distinguishes the two branches.
Thus evaluation of canonical differentials at the two points has rank
two.

For \(c=1\), write
\[
m=2r-1,\qquad b=2r+1.
\]
When \(r\ge2\), there is one origin branch and the holomorphic adjoints
\[
\begin{aligned}
\omega_0&=
s^{r-1}(1+s)^{\lfloor(r-1)/2\rfloor}
w^{r-1}\frac{ds}{F_w},\\
\omega_1&=
s^{2r-1}(1+s)^{r-1}\frac{ds}{F_w}
\end{aligned} \tag{MW2o}
\]
have orders zero and one.  Hence the two-jet evaluation map at that
point again has rank two.  The omitted case \(r=1\) has \(m=1\mid b\)
and was already excluded by (MWRes).

In both parity cases, if \(C\) is the complete normalization, the exact
sequence for \(K_C-E\) and Riemann--Roch give
\[
\ell(E)=\deg E+1-g(C)+\ell(K_C-E)
=3-g(C)+(g(C)-2)=1.
\]
Thus \(L(E)=k\).  A primitive of \(\eta\) would be a nonconstant member
of \(L(E)\), which is impossible.

> **Inner middle-wall obstruction.**  Every monomial perturbation in the
> middle wedge satisfying
> \[
> 2a+c-b=2
> \]
> has no rational mate in characteristic zero, for every
> \(\kappa\ne0\).  This is the first infinite fixed-coefficient family
> with vanishing Puiseux residue to be closed by the pole divisor itself.

The preceding two-jet calculation is the first instance of a general
canonical staircase.  For \(1\le j\le m\), the strict interior points in
the \(w^{j-1}\)-row have \(s\)-indices
\[
L_j\le i\le U_j,\qquad
L_j=\left\lfloor\frac{b(m-j)}m\right\rfloor+1,\quad
U_j=\left\lfloor
\frac{(b+r)(m+1-j)-1}{m+1}
\right\rfloor. \tag{MWRows}
\]
At the singularity over \(s=-1\), the coefficient of \(w^{j-1}\) must
vanish to order
\[
k_j=\left\lfloor\frac{r(m-j)}m\right\rfloor. \tag{MWCon}
\]
Consequently
\[
s^{i-1}(1+s)^{k_j}w^{j-1}\frac{ds}{F_w},
\qquad L_j\le i\le U_j-k_j, \tag{MWBasis}
\]
is a basis of \(H^0(C,K_C)\).  Indeed the number of raw interior
adjoints is the arithmetic genus, while
\[
\sum_{j=1}^m k_j
=\frac{mr-m-r+\gcd(m,r)}2
\]
is exactly the delta-invariant of the sole non-toric boundary
singularity \(z^r+w^m\).  Thus (MWBasis) has the geometric genus
dimension and supplies every canonical differential.

This basis makes restriction to (MWE) completely arithmetic.  Write
\[
\delta=b-m,\qquad g=\gcd(m,\delta),\qquad
M=m/g,\qquad q=\delta/g,\qquad B=M+q.
\]
For each jet order \(0\le n<q\), let \(x_0\in[0,M-1]\) be the unique
solution of
\[
q x_0+n+1\equiv0\pmod M. \tag{MWCong}
\]
For \(0\le t<g\), put
\[
x_t=x_0+tM,\qquad j_t=m-x_t,\qquad
i_t=x_t+\frac{q x_t+n+1}{M}. \tag{MWStair}
\]
The corresponding member of (MWBasis), when it exists, has order
exactly \(n\) at every origin branch.  Choose branch constants
\(A_\nu=A_0\zeta_m^\nu\), \(0\le\nu<g\).  Up to nonzero row and column
factors, the leading-coefficient matrix of the \(g\) forms in
(MWStair) is
\[
\bigl(\zeta_m^{-\nu tM}\bigr)_{\nu,t}
=\bigl(\zeta_g^{-\nu t}\bigr)_{\nu,t}, \tag{MWFourier}
\]
the nonsingular discrete Fourier matrix.  Different \(n\)'s occupy
successive local jet orders, so the full restriction matrix is block
triangular with these Fourier blocks.

It follows that the following finite arithmetic test is an exact
sufficient certificate:
\[
L_{j_t}\le i_t\le U_{j_t}-k_{j_t}
\quad
(0\le n<q,\ 0\le t<g). \tag{MWCert}
\]
Whenever (MWCert) holds, the canonical restriction map along \(E\) has
rank \(\deg E=\delta\).  Hence
\[
\ell(K_C-E)=g(C)-\delta,\qquad \ell(E)=1,
\]
and the forced differential has no rational primitive.

There is a useful uniform region where (MWCert) always holds.  Suppose
\[
m>\delta^2. \tag{MWTail}
\]
Writing \(N=n+1\), the congruence gives
\[
h=\frac{\delta x_t+gN}{m}\in\mathbb Z,\qquad
i_t=x_t+h.
\]
Since \(0<gN\le\delta<m\), this is exactly \(i_t=L_{j_t}\).
The remaining upper-row inequality has strict slack
\[
\frac{(m+\delta+r)j_t}{m(m+1)}
-\frac{gN}{m}
+\left\{-\frac{rj_t}{m}\right\}. \tag{MWSlack}
\]
It is positive under (MWTail).  If \(c=0\), the fractional term is
\(1/2\) for odd \(j_t\); for even \(j_t\), the congruence forces
\(\delta j_t-gN\) to be a positive multiple of \(m\), which is even
stronger.  If \(c=1\), the fractional term is
\(1-j_t/(2m)\) for even \(j_t\) and
\((m-j_t)/(2m)\) for odd \(j_t\); in both cases (MWSlack) is bounded
below using \(m/2>\delta\).

> **Canonical-staircase obstruction.**  Every fixed-coefficient
> middle-wedge monomial satisfying (MWCert) has no rational mate in
> characteristic zero.  In particular this holds uniformly whenever
> \[
> 2(b-a)-c>\bigl(2a+c-b\bigr)^2.
> \]
> Unlike the deformation argument, this conclusion includes every
> \(\kappa\ne0\), not just a generic coefficient.

The parity in (MWSlack) gives better uniform bounds than (MWTail).
If \(c=1\), then \(m\) is odd and \(r=(m+1)/2\).  Multiplying (MWSlack)
by \(m\), its fractional contribution is \(m-j/2\) for even \(j\) and
\((m-j)/2\) for odd \(j\).  Since
\[
\frac{m+\delta+r}{m+1}
=\frac32+\frac{\delta-1}{m+1},
\]
the slack is positive for every staircase point as soon as
\[
m\ge2\delta-1. \tag{MWOdd}
\]
If \(c=0\), then \(r=m/2\).  For odd \(j\), the fractional contribution
is \(m/2\).  For even \(j\), it is zero, but the congruence forces
\(\delta j-gN\) to be a positive multiple of \(m\), so \(j>m/\delta\).
Since \((m+\delta+r)/(m+1)>3/2\), this proves positivity whenever
\[
\delta\ge4,\qquad 3m>2\delta^2. \tag{MWEven}
\]

> **Sharpened canonical regions.**  Every fixed-coefficient
> middle-wedge monomial is excluded by (MWCert) under (MWOdd), or under
> (MWEven) in the even case.

The complementary odd region has a useful geometric explanation.  The
function
\[
vw=\frac{s(1+s)}w
\]
has pole divisor exactly \(E\) over the origin, is regular over
\(s=-1\), and has order
\[
\delta+r-m-2
\]
at the slanted infinity boundary.  For \(c=1\), this order is
nonnegative precisely when \(m\le2\delta-3\), exactly the region
complementary to (MWOdd).  Thus the staircase rank defect there is
genuine: \(L(E)\) already contains \(1\) and \(vw\).  For \(c=0\), the
same section is regular at infinity when \(m\le2\delta-4\).

This observation extends to a complete solution whenever the origin is
unibranch.  Assume
\[
\gcd(m,\delta)=1. \tag{MWCop}
\]
For each possible pole order \(1\le p\le\delta\), there is a unique
\(1\le\beta\le m\) and an integer \(\alpha\) such that
\[
\beta b-\alpha m=p. \tag{MWBez}
\]
Put
\[
k_\beta=\left\lceil\frac{\beta r}{m}\right\rceil,\qquad
f_p=\frac{s^\alpha(1+s)^{k_\beta}}{w^\beta}. \tag{MWFunc}
\]
The function is regular over \(s=-1\) by construction.  Its order at
the slanted infinity boundary is
\[
I_p=\beta(b+r)-(\alpha+k_\beta)(m+1). \tag{MWInf}
\]
Thus \(f_p\) is a member of \(L(\delta p_0)\) exactly when
\(I_p\ge0\), and then its sole pole has order \(p\).

There is an exact lattice reciprocity with the canonical row basis.  The
raw canonical point complementary to (MWFunc) is
\[
(i,j)=(b-\alpha,\beta).
\]
Its origin order is \(p-1\), and
\[
\left\lceil\frac{\beta r}{m}\right\rceil
+\left\lfloor\frac{r(m-\beta)}m\right\rfloor=r.
\]
Substituting this identity into the upper inequality in (MWRows) shows
\[
(b-\alpha,\beta)\ \text{belongs to (MWBasis)}
\quad\Longleftrightarrow\quad I_p<0. \tag{MWRec}
\]
Hence for every \(p\le\delta\), exactly one of the following occurs:

* \(p\) is a canonical gap, witnessed by the differential of order
  \(p-1\);
* \(p\) is a nongap, witnessed by the explicit function \(f_p\).

The gap theorem and (MWRec) show that \(1\), together with the functions
\(f_p\) for \(I_p\ge0\), is a basis of \(L(\delta p_0)\).

At the top order \(p=\delta\), coprimality in (MWBez) forces
\[
\beta=\alpha=1.
\]
Thus the unique possible maximal-pole basis element is
\[
q=-\frac{\kappa s(1+s)}w.
\]
For every lower pole \(p<\delta\), (MWBez) forces \(\alpha\ge2\), so
\(df_p=0\) at the second point \((s,w)=(0,P)\).  If \(I_\delta<0\),
no member of \(L(\delta p_0)\) has the pole order required of a
primitive, and exactness is already impossible.  If
\(I_\delta\ge0\), local comparison gives
\[
\left.\frac{dq}{\eta}\right|_{p_0}=\delta\kappa P,\qquad
\left.\frac{dq}{\eta}\right|_{(0,P)}=\kappa P. \tag{MWTop}
\]
A putative primitive must use \(q\) with coefficient
\((\delta\kappa P)^{-1}\) to match the leading pole at \(p_0\).  At
\((0,P)\), all lower-pole basis functions have zero derivative, so its
derivative ratio would be \(1/\delta\), not \(1\).

> **Coprime middle-wedge theorem.**  If
> \[
> \gcd\bigl(2(b-a)-c,\ 2a+c-b\bigr)=1,
> \]
> then the monomial perturbation has no rational mate in characteristic
> zero for any \(\kappa\ne0\).

The coprime argument is one Fourier block of a statement with no
arithmetic restriction.  Drop (MWCop), retain
\[
g=\gcd(m,\delta),\quad M=m/g,\quad q=\delta/g,\quad B=b/g.
\]
For each \(1\le p\le q\), choose the unique
\(1\le\beta_0\le M\) satisfying
\[
\beta_0B\equiv p\pmod M.
\]
For \(0\le t<g\), set
\[
\beta_t=\beta_0+tM,\qquad
\alpha_t=\frac{\beta_tB-p}{M}. \tag{MWMulti}
\]
Then
\[
f_{p,t}
=\frac{s^{\alpha_t}(1+s)^{\lceil\beta_t r/m\rceil}}
       {w^{\beta_t}} \tag{MWMultiF}
\]
has pole order \(p\) at each of the \(g\) origin branches and no other
finite pole.  As before, it is regular at the slanted infinity boundary
exactly when
\[
I_{p,t}
=\beta_t(b+r)
-(\alpha_t+\lceil\beta_t r/m\rceil)(m+1)\ge0. \tag{MWMultiI}
\]
Its complementary canonical point is
\[
(i,j)=(b-\alpha_t,\beta_t),
\]
which has order \(p-1\) at every origin branch and belongs to (MWBasis)
exactly when \(I_{p,t}<0\).

Choose the branch constants \(A_\nu=A_0\zeta_m^\nu\).  For fixed \(p\),
the principal-part columns of (MWMultiF) are, up to diagonal factors,
\[
\bigl(A_\nu^{-\beta_t}\bigr)_{\nu,t}
\sim\bigl(\zeta_g^{-\nu t}\bigr)_{\nu,t}. \tag{MWMultiDFT}
\]
Thus they form the same nonsingular Fourier matrix as (MWFourier).
For every one of the \(\delta=gq\) branch/jet-character slots, exactly
one of a canonical column and an explicit function column occurs.
Riemann--Roch then gives the complete basis
\[
L(E)=
\left\langle
1,\ f_{p,t}: I_{p,t}\ge0
\right\rangle. \tag{MWMultiBasis}
\]

In the top block \(p=q\), (MWMulti) becomes
\[
\beta_t=1+tM,\qquad \alpha_t=1+tB.
\]
The \(t=0\) column is
\[
q_0=-\frac{\kappa s(1+s)}w,
\]
whose branch character \(A_\nu^{-1}\) is exactly the leading character
of \(\eta\).  All other top columns are Fourier-independent of it.  If
\(q_0\notin L(E)\), the leading principal part of \(\eta\) is absent
from the function span, so \(\eta\) is not exact.  If \(q_0\in L(E)\),
matching the leading principal part uniquely forces its coefficient to
be
\[
\frac1{\delta\kappa P}.
\]
Every other function in (MWMultiBasis) has \(\alpha_t\ge2\), and hence
zero differential at \((s,w)=(0,P)\).  Since
\[
\left.\frac{dq_0}{\eta}\right|_{(0,P)}=\kappa P,
\]
the normalized candidate primitive has derivative ratio \(1/\delta\)
there, not \(1\).

> **Full middle-wedge theorem.**  For every exponent triple
> \[
> a<b<2a+c-1,\qquad c\in\{0,1\},
> \]
> and every \(\kappa\ne0\), the monomial perturbation (MC) has no
> rational mate in characteristic zero.

Together with the outer monomial-cone theorem, this removes the former
asymptotic gap: every non-affine reduced monomial perturbation with both
\(u\)- and \(v\)-exponents positive is now excluded in characteristic
zero.  The previously separated pure-tail boundaries remain governed
by their own hyperelliptic and boundary arguments.

The multibranch proof is stable under perturbations which do not change
its three boundary faces.  Let the selected middle-wedge term have
parameters
\[
r=b-a,\qquad m=2r-c,\qquad \delta=b-m,
\]
and let additional \(v\)-side terms have
\[
r_i=b_i-a_i,\qquad m_i=2r_i-c_i.
\]
After clearing \(w^m\), the family is
\[
\begin{aligned}
F={}&w^m(w+s-P)+\kappa s^b(1+s)^r\\
&+\sum_i\kappa_i
s^{b_i}(1+s)^{r_i}w^{m-m_i}. \tag{MWFaceF}
\end{aligned}
\]
Assume \(m_i\le m,\ b_i\ge2\), and the three strict face inequalities
\[
\begin{aligned}
m b_i&>b m_i,\\
m r_i&>r m_i,\\
(m+1)(b_i+r_i)+(b+r)(m-m_i)
&<(b+r)(m+1).
\end{aligned} \tag{MWFace}
\]
The first says that every perturbation lies strictly above the origin
edge from \((0,m)\) to \((b,0)\).  The second makes it higher than the
local \(z^r+w^m\) face over \(s=-1\).  The third places its largest
\(s\)-exponent strictly below the slanted infinity edge.  Consequently
the Newton polygon remains
\[
\operatorname{conv}\{(0,m),(b,0),(b+r,0),(0,m+1)\},
\]
and the prescribed boundary singularities have the same conductors.

Suppose, in addition, that the complete curve is smooth away from these
prescribed boundary branches; this is a Zariski-open condition on the
nonzero coefficients.  Then (MWBasis), (MWMultiF), and the complementary
Fourier decomposition (MWMultiDFT) remain valid without change.
The first inequality preserves the origin principal parts, while
\(b_i\ge2\) ensures that every perturbation has zero first \(s\)-jet at
\((s,w)=(0,P)\).  Thus the same top-character normalization gives the
factor-\(\delta\) mismatch.

> **Exposed middle-face theorem.**  Every finite perturbation satisfying
> (MWFace) has no rational mate in characteristic zero on the
> Zariski-open coefficient locus where (MWFaceF) has no extra
> singularities.  This is a genuine nonsparse extension of the full
> monomial middle-wedge theorem.  Special coefficients which create
> additional affine singularities are not included in this statement.

There is a finite global dichotomy describing exactly when a support
has such an exposed term.  Associate to every middle-wedge term the
three rational signatures
\[
O=\frac bm,\qquad
Z=\frac rm,\qquad
I=\frac{b+r}{m+1}. \tag{MWSig}
\]
They are respectively the slopes controlling the origin edge, the
\(s=-1\) local face, and the slanted infinity edge.  For a finite
support \(\mathcal S\), let
\[
\mathcal L=\arg\min_{\mathcal S}O,\qquad
\mathcal Z=\arg\min_{\mathcal S}Z,\qquad
\mathcal R=\arg\max_{\mathcal S}I. \tag{MWExt}
\]

The signatures also control the denominator:
\[
O_x\le O_y,\quad Z_x\le Z_y,\quad I_x\ge I_y
\quad\Longrightarrow\quad m_x\ge m_y. \tag{MWDom}
\]
This follows by direct cross multiplication in the four possibilities
\((c_x,c_y)\in\{0,1\}^2\).  In particular,
\(Z=1/2\) when \(c=0\), while
\(Z=r/(2r-1)\) strictly decreases with \(r\) when \(c=1\); the remaining
same-parity comparisons reduce to the two affine fractions in \(a\)
and \(r\).

Suppose the three sets in (MWExt) have a common member \(x\), and all
three extrema are strict.  Then (MWDom) shows that \(m_x\) is the unique
largest denominator.  Moreover, for every other term \(i\),
\[
O_x<O_i,\quad Z_x<Z_i,\quad I_x>I_i
\]
are exactly the three inequalities (MWFace), after clearing positive
denominators.  Thus the exposed middle-face theorem applies.

If the extrema are unique but have no common member, there are exactly
four possibilities:
\[
\begin{array}{c|c}
\text{type}&\text{extremizer pattern}\\ \hline
\mathrm{LZ}&L=Z\ne R,\\
\mathrm{LR}&L=R\ne Z,\\
\mathrm{ZR}&Z=R\ne L,\\
\mathrm{D}&L,Z,R\ \text{all distinct}.
\end{array} \tag{MWTypes}
\]
If an extremum is not unique, the support lies on at least one of the
three explicit tie loci
\[
\begin{aligned}
b_i m_j&=b_jm_i,\\
r_i m_j&=r_jm_i,\\
(b_i+r_i)(m_j+1)&=(b_j+r_j)(m_i+1).
\end{aligned} \tag{MWTies}
\]
These are exposed multi-term faces rather than exposed monomials.

> **Face-signature dichotomy.**  Every finite support consisting of
> middle-wedge terms with \(b_i\ge2\) has exactly one of the following
> forms:
>
> 1. a unique common \(O\)-minimum, \(Z\)-minimum, and \(I\)-maximum, in
>    which case it is generically excluded by the exposed middle-face
>    theorem;
> 2. one of the four separated-extremizer types (MWTypes);
> 3. a support on one or more tie loci (MWTies).
>
> Hence (MWTypes) and (MWTies) are the complete exceptional
> configurations still requiring a multi-face argument.  This is a
> finite combinatorial classification, not a degree-bounded inventory.

The first lower-left face in fact treats all four types and all
origin-face ties simultaneously.  Let
\(\mathcal M=\max_i m_i\), clear \(w^{\mathcal M}\), and let the first
edge of the Newton polygon run from
\[
(0,\mathcal M)
\quad\text{in primitive direction}\quad
(B,-M_0),
\qquad B>M_0.
\]
If its lattice length is \(N\), the terms on this face have
\[
(b_i,m_i)=n_i(B,M_0),\qquad 1\le n_i\le N.
\]
Set
\[
X=\frac{s^B}{w^{M_0}},\qquad
G(X)=\sum_{i\ \mathrm{on\ face}}\kappa_iX^{n_i}. \tag{MWFacePoly}
\]
The face equation on the generic \(P\)-fiber is
\[
G(X)-P=0.
\]
It is separable over \(k(P)\) in characteristic zero.  The branches are
indexed by its roots \(A\), and the leading forced differential is
\[
\eta=
\frac{1}{C\,A\,G'(A)}
t^{M_0-B-1}dt+\cdots,
\qquad w=Ct^B,\ s=t^{M_0}. \tag{MWFaceEta}
\]

Let \(H_P(X)\) be the inverse of \(XG'(X)\) in the face algebra:
\[
XG'(X)H_P(X)\equiv1\pmod{G(X)-P}. \tag{MWFaceInv}
\]
The unique associated-graded principal part integrating (MWFaceEta) on
all first-face branches is
\[
Q_{\mathrm{face}}
=-\frac{s}{(B-M_0)w}H_P(X). \tag{MWFaceQ}
\]
The root-evaluation matrix implicit here is the generalized Vandermonde
version of (MWMultiDFT).

Every other toric pole of \(\eta\) lies on a later edge of the same
lower-left Newton chain.  A Laurent monomial with \(s\)-order one and
any \(w\)-denominator already has first-edge valuation
\[
M_0-B\beta<0\qquad(\beta\ge1).
\]
Thus its coefficient is already fixed by (MWFaceQ).  Principal parts
from later edges, and lower first-edge pole orders, have \(s\)-order at
least two and contribute zero first derivative at
\((s,w)=(0,P)\).  Terms with nonnegative \(w\)-order and \(s\)-order one
are excluded by regularity at the remaining toric boundaries.

Consequently exactness would force
\[
\frac{P\,H_P(0)}{B-M_0}=1. \tag{MWFaceNeed}
\]
This identity is impossible.  If \(N=\deg G\), Euclidean inversion in
(MWFaceInv), or equivalently rescaling the roots as \(P\to\infty\),
gives
\[
\lim_{P\to\infty}P\,H_P(0)=\frac1N. \tag{MWFaceLim}
\]
Every term on the first face is in the middle wedge, so
\[
N(B-M_0)\ge2.
\]
The limit of the left side of (MWFaceNeed) is therefore
\(1/[N(B-M_0)]\ne1\).

The toric point representing \(\eta\) is
\((1,\mathcal M-1)\).  Direct convexity shows that every edge on which
it is not interior belongs to the initial lower-left chain just used.
The only exception is \(\mathcal M=1\), when it can also lie on a
horizontal edge.

There is no exceptional coefficient stratum hidden in the first face.
Indeed \(G(X)-P\) is squarefree over \(k(P)\) for every nonconstant
\(G\) in characteristic zero: a common root with \(G'\) would make the
transcendental \(P\) equal to a constant critical value of \(G\).
Possible repeated initial forms on later faces also do not affect the
argument.  After passing to the normalization, they merely refine the
valuations belonging to those later faces.  The first-edge associated
graded algebra remains \(k(P)[X]/(G-P)\), while the convexity
calculation above places every later-face correction in \(s\)-order at
least two.  Hence such corrections have zero first derivative at
\((0,P)\), exactly as in the nondegenerate case.

> **Coefficient-uniform global first-face theorem.**  Let \(H\) be any
> finite sum of
> middle-wedge terms with \(b_i\ge2\), and suppose
> \(\mathcal M=\max_i m_i\ge2\).  For every choice of nonzero
> coefficients, \(w+s+H\) has no rational mate in characteristic zero.
>
> This theorem includes every separated-extremizer type (MWTypes) and
> every first-face tie.  The only remaining middle-wedge case is the
> horizontal \(\mathcal M=1\) resonance.

That resonance is coefficient-uniform as well.  The identity
\(m=2r-c=1\) forces \(r=c=1\), so every term is
\(s^b(1+s)/w\), with \(b\ge3\).  Thus for a nonzero polynomial
\[
K(s)=\sum_{b\ge3}\kappa_b s^b,\qquad
A(s)=(1+s)K(s),
\]
the cleared generic fiber and forced differential are
\[
F=w^2+(s-P)w+A(s),\qquad
\eta=-\frac{ds}{w(2w+s-P)}. \tag{MWHorizontal}
\]
Put \(D=s-P\).  Since \(A=-w(D+w)\) on \(F=0\),
\[
\eta-\frac{ds}{A(s)}
=\frac{ds}{(D+w)(D+2w)}. \tag{MWHorizontalPP}
\]
The right side is regular at every point over \(w=0\), including points
over multiple roots of \(A\).  Hence the residues of \(\eta\) there are
exactly the residues of \(ds/A\).

We use the following elementary reciprocal-residue lemma.  If a
polynomial \(A\) over a characteristic-zero field has at least two
distinct roots, then \(ds/A\) has a nonzero residue.  Otherwise it has
a rational primitive \(R=B/C\).  Write
\[
D_0=\operatorname{rad}(A),\qquad C=A/D_0,
\]
and subtract the value of \(R\) at infinity so that
\(\deg B<\deg C=n\).  A simple root already gives a nonzero residue, so
all root multiplicities may be assumed at least two.  Differentiating
\(R\) and comparing with \(1/A=1/(CD_0)\) gives
\[
B'C-BC'=\frac{C}{D_0}. \tag{MWReciprocalWronskian}
\]
If \(r\ge2\) is the number of distinct roots and \(\deg B=k<n\), the
left side has degree \(k+n-1\ge n-1\), while the right side has degree
\(n-r\le n-2\), a contradiction.

Here \(A\) is divisible by \(s^3(1+s)\), so it always has the two
distinct roots \(0\) and \(-1\).  Therefore \(\eta\) has a nonzero
residue and cannot be exact.

> **Complete finite middle-wedge theorem.**  Every nonzero finite sum
> of reduced middle-wedge monomials added to \(w+uv\) has no rational
> mate in characteristic zero, for every choice of its nonzero
> coefficients.

The next wall \(\delta=3\) illustrates both the reach and the one small
limitation of the staircase.  It verifies (MWCert) in every non-residue
case except
\[
(a,b,c)=(4,5,0),\qquad
F=w^3+(s-P)w^2+\kappa s^5(1+s).
\]
The two \(c=1\) exceptions have \(m\mid b\) and are already covered by
(MWRes).  On the displayed curve, \(C\) has genus two and
\(E=3p\), so Riemann--Roch gives \(\ell(3p)=2\).  A generator is
\[
q=-\frac{\kappa s(1+s)}w
=\frac{w(w+s-P)}{s^4}. \tag{MW3q}
\]
The first presentation is regular at the second point over \(s=0\);
at \(s=-1\), the local orders \(1+s=t^2,\ w\asymp t\) show regularity;
and the second presentation plus the toric infinity valuations shows
that its only pole is the order-three pole at \(p\).  Thus
\[
L(3p)=\langle1,q\rangle.
\]
If \(dq\) were a constant multiple of \(\eta\), the ratio would be
constant.  At \((s,w)=(0,P)\),
\[
\frac{dq}{\eta}=\kappa P.
\]
At \(p\), using \(s=t^2,\ w=A t^5+\cdots,\ A^2=\kappa/P\), it is
\[
\frac{dq}{\eta}=3\kappa P.
\]
They are incompatible in characteristic zero.

> **Second inner-wall obstruction.**  Every middle-wedge monomial with
> \[
> 2a+c-b=3
> \]
> has no rational mate in characteristic zero for any
> \(\kappa\ne0\).

The wall \(\delta=4\) can be closed similarly.  In the even case, its
only staircase failures have \(m\mid\delta\), so (MWRes) applies.  In
the odd case, \(m=1\) is again a residue case and the only remaining
failures are
\[
(m,c)=(3,1),\qquad(5,1).
\]
For both curves, three explicit members of (MWBasis) have consecutive
orders \(0,1,2\) at the unique point \(p\) over the origin.  Hence the
canonical restriction to \(4p\) has rank three and
\[
\ell(4p)=5-3=2.
\]
The function
\[
q=-\frac{\kappa s(1+s)}w
\]
is regular away from \(p\) in both cases and has pole order four there,
so
\[
L(4p)=\langle1,q\rangle.
\]
The same general local computation as on the preceding wall gives
\[
\left.\frac{dq}{\eta}\right|_{(s,w)=(0,P)}=\kappa P,\qquad
\left.\frac{dq}{\eta}\right|_p=4\kappa P.
\]
Thus no member of \(L(4p)\) differentiates to \(\eta\).

> **Third inner-wall obstruction.**  Every middle-wedge monomial with
> \[
> 2a+c-b=4
> \]
> has no rational mate in characteristic zero for any
> \(\kappa\ne0\).

The Newton-interior half of the theorem also extends to nonsparse
Hamiltonians.  Let \(R\) be any finite sum of Laurent-chart monomials
coming from exponent triples satisfying \(b>2a+c\).  For each term put
\(m_i=2(b_i-a_i)-c_i\) and let \(M=\max m_i\).  Clearing \(w^M\) gives
\[
F=w^M(w+s-P)
 +\sum_i\kappa_i
 s^{b_i}(1+s)^{b_i-a_i}w^{M-m_i},\qquad
\eta=-\frac{w^{M-2}ds}{F_w}. \tag{MCSum}
\]
Choose a term with \(m_i=M\).  Its single-term Newton polygon already
contains \((1,M-1)\) strictly in its interior; adding the other supports
only enlarges that polygon.  Hence \((1,M-1)\) remains interior for the
full sum.

> **Strict-cone sum theorem.**  If the cleared curve (MCSum) is Newton
> nondegenerate, then \(\eta\) is a nonzero holomorphic differential on
> its complete toric model and cannot be exact.  Newton nondegeneracy is
> Zariski open in the coefficients, so arbitrary finite strict-cone
> supports are excluded generically.  No unconditional claim is made on
> the degenerate initial-form locus, where boundary singularities can
> turn dualizing differentials into meromorphic normalization
> differentials.

### Frobenius-central seeds and a universal no-lift functional

The degree-five modular hits are not isolated.  Let
\[
H\in B_{\mathbb F_3}
\]
have zero constant term and put \(A=1+H^3\).  The cube \(H^3\) is
Poisson central, so the exact identities
\[
\boxed{
P=w+Auv,\qquad
Q=-v+uv^2+Av^2w
} \tag{FC}
\]
give
\[
\{P,Q\}=1
\]
over \(\mathbb F_3\).  For \(H=v\) and \(H=u\), these are precisely the
two signed degree-five edge families:
\[
\begin{array}{ll}
P=w+uv+\kappa uv^4,&
Q=-v+uv^2+v^2w+\kappa v^5w,\\
P=w+uv+\kappa u^4v,&
Q=-v+uv^2+v^2w+\kappa u^3v^2w.
\end{array}
\]

Nevertheless no member of (FC) is a lifting seed.  For centered integer
representatives write \(\{P,Q\}=1+3E\) and define
\[
\ell(R)=[v]R+[uv^2]R.
\]
Reduced Frobenius monomials in \(H^3\) have one of the forms
\[
u^{3i}v^{3j},\qquad
u^{3i+1}v^{3j}w,\qquad
u^{3i+2}v^{3j+1}w.
\]
Since \(H\) has no constant term, none of the \(H\)-dependent columns can
reach the two coefficients selected by \(\ell\).  The only correction
monomials that can reach them at all are
\[
A_{\rm corr}=vw,\qquad B_{\rm corr}=v^2,
\]
and each contributes coefficients \((1,-1)\).  Therefore
\[
\ell(\{A_{\rm corr},Q\}+\{P,B_{\rm corr}\})=0
\]
for arbitrary polynomial corrections, while exact integer expansion
gives
\[
\ell(-E)=1.
\]

> **Frobenius-family no-lift theorem.**  Every exact pair (FC) fails its
> first unrestricted Hensel equation modulo \(9\).  This is a single
> support-independent obstruction for an infinite characteristic-\(3\)
> construction family, rather than a bounded seed search.

The other absent quadratic perturbation \(vw\) has a rational generic
fiber but a direct residue obstruction.  Let
\[
P=cw+\lambda uv+\nu vw,\qquad \nu\ne0,
\]
put \(s=uv\), and use
\[
vw=\frac{s(1+s)}w
\]
in the function field.  The generic fiber is the conic
\[
F(s,w)=cw^2+(\lambda s-P)w+\nu s(1+s)=0. \tag{WQ}
\]
Since \(\{s,w\}=w^2\), direct differentiation on (WQ) gives
\[
D_P=w\left(F_s\partial_w-F_w\partial_s\right).
\]
A mate would therefore force
\[
dQ=-\frac{ds}{wF_w}=\frac{dw}{wF_s}. \tag{WR}
\]

The smooth completion has two points with \(w=0\), namely \(s=0\) and
\(s=-1\).  At the first,
\[
F_w=-P,\qquad F_s=\nu,\qquad
\frac{ds}{dw}=\frac{P}{\nu},
\]
so the residue of (WR) is \(1/\nu\).  At the second,
\[
F_w=-\lambda-P,\qquad F_s=-\nu,
\]
and the residue is \(-1/\nu\).  Both are nonzero.  Exact rational
differentials have zero residues, hence:

> **Quadratic \(vw\)-perturbation obstruction.**  No
> \(P=cw+\lambda uv+\nu vw\), with \(\nu\ne0\), has even a rational
> Darboux mate in \(\operatorname{Frac}(B)\), and therefore has no
> polynomial mate of any degree.

As a smaller coefficient check, if both \(P,Q\) are affine-linear, the
constant coefficient of their bracket is
\(\Delta=a_vb_w-a_wb_v\), while the \(uv\) coefficient is \(2\Delta\).
The equations \(\Delta=1\) and \(2\Delta=0\) already contradict one
another in characteristic zero.

## 5. De Rham and Pfaff calculation

The symplectic form corresponding to the bracket is globally represented
by
\[
\Omega
=(1+2uv)\,dv\wedge dw+2vw\,du\wedge dv.
\]
On \(u\ne0\), this is \(dr\wedge dw=-u^{-2}du\wedge dw\).

Let
\[
\mathcal E=2u\partial_u-2v\partial_v+w\partial_w.
\]
The form has weight \(-1\), so
\(\mathcal L_{\mathcal E}\Omega=-\Omega\).  The polynomial one-form
\[
\begin{aligned}
\beta=-\iota_{\mathcal E}\Omega
={}&-4v^2w\,du+w(1-2uv)\,dv\\
&+2v(1+2uv)\,dw
\end{aligned}
\]
satisfies
\[
d\beta=\Omega
\]
in \(\Omega_B^2\).  Thus the naive de Rham-class obstruction vanishes
over \(\mathbb Z\), hence also after reduction modulo \(3\).

In characteristic zero one can also close the previously open
closed-one-form issue: \(H^1_{\mathrm{dR}}(B)=0\).  Indeed, every
homogeneous closed one-form of nonzero weight is exact by Cartan's
formula for \(\mathcal E\).  Put \(s=uv\).  A weight-zero one-form is,
modulo the differential of the defining relation, of the form
\[
\alpha=A(s)v\,du+B(s)u\,dv+C(s)vw\,dw.
\]
On the Laurent chart it becomes
\[
\alpha=\frac{X(s)}r\,dr+rwY(s)\,dw,\quad
X=-sA+(2s+1)B,\quad Y=2B+sC,
\]
where \(s=rw^2-1\).  Closedness is
\[
Y+(s+1)Y'-2X'=0.
\]
Consequently \(X-(s+1)Y/2\) is constant; its value at \(s=0\) is zero
because \(X(0)=B(0)\) and \(Y(0)=2B(0)\).  Integrating the polynomial
\(Y/2\) now writes \(\alpha=dh(s)\).  This proves the claim.

If a Darboux pair existed, then
\[
d(P\,dQ)=dP\wedge dQ=\Omega.
\]
The remaining problem is therefore a polynomial Pfaff-decomposition
problem: can a primitive of \(\Omega\) be written
\[
\beta=P\,dQ+dh
\]
rather than an exactness problem for \(\Omega\) itself?  On the Laurent
chart the displayed primitive has the particularly simple form
\[
\beta=w\,dr+2r\,dw=d(rw)+r\,dw.
\]
Thus a necessary global-fiber condition is that \(r\,dw\) restrict
exactly to the generic fiber of \(P\).  This recovers the logarithmic
residue obstruction for \(P=v\), but it is not by itself a proof for
arbitrary \(P\): for example the restriction is exact on fibers of
\(P=w\), which fail instead by the boundary-pole argument.

Contracting the Pfaff equation with the two Hamiltonian vector fields
gives another degree-independent necessary system:
\[
\boxed{\quad
\{P,h\}=-(\mathcal E+1)P,\qquad
\{Q,h\}=-\mathcal E Q.
\quad} \tag{Pf}
\]
Here \(\beta(D_P)=-\mathcal E(P)\),
\(D_PQ=1\), and \(D_QP=-1\).  For example, when \(P=w\), the first
equation forces \(h=2rw+f(w)\) on the Laurent chart, exposing exactly
the forbidden boundary pole.  Unlike BF0--BF2, (Pf) couples the local
boundary behavior to the global grading.  A universal classification
of its polynomial solutions would be a plausible route to closing this
branch, but no such classification is claimed here.

## 6. Exact finite searches

The search uses the unique reduced basis
\[
u^iv^jw^k,\qquad k\in\{0,1\}.
\]
All arithmetic is either over \(\mathbb Q\) using `Fraction` or over a
specified prime field using modular row reduction.

The following characteristic-zero finite ansätze have no solution:

* every monomial \(P\) of generator total degree at most \(4\), against
  every \(Q\) of total degree at most \(15\) (24 choices of \(P\));
* every monomial or binomial \(P\) of total degree at most \(3\), with
  first coefficient normalized to \(1\) and second coefficient
  \(\pm1\), against every \(Q\) of total degree at most \(10\)
  (225 choices of \(P\)).

These are finite exact exclusions only; they are not evidence of a
global obstruction by themselves.

### Full nonhomogeneous coefficient variety through degree two

There is also an exact elimination which ranges over **all** coefficients
of both \(P\) and \(Q\), rather than fixing a sparse Hamiltonian.
Constants can be discarded.  Since the constant coefficient of the
bracket is
\[
 [v]P\,[w]Q-[w]P\,[v]Q=1,
\]
an \(SL_2\) change of the target, which preserves both the bracket and a
common degree bound, puts every prospective quadratic pair into the form
\[
\begin{aligned}
P={}&v+au+du^2+euv+fv^2+guw+hvw,\\
Q={}&w+bu+Du^2+Euv+Fv^2+Guw+Hvw.
\end{aligned}
\]
Only eight nonconstant coefficient rows of \(\{P,Q\}=1\) are needed.
The \(uv,uvw,uv^2,uv^3,u^2w,u^2vw,u^2v^2,u^4\) rows are
\[
\begin{aligned}
 Eh-6Fg+6Gf-He+2&=0,\\
 8Df-8Fd+2h&=0,\\
 2H+4f&=0,\\
 -4Fh+4Hf&=0,\\
 4De-4Ed-g&=0,\\
 5Gh-5Hg&=0,\\
 Eh-8Fg+8Gf-He&=0,\\
 2Dg-2Gd&=0.
\end{aligned}
\]
Subtracting the seventh row from the first gives
\(Fg-Gf=-1\).  The third, fourth, and sixth rows then imply, after
multiplying this determinant identity by \(h\),
\[
h=f=H=0.
\]
Thus \(Fg=-1\).  The second row gives \(d=0\), the last gives \(D=0\),
and the fifth then gives \(g=0\), contradicting \(Fg=-1\).

Hence:

> **Full degree-two obstruction.**  Over a characteristic-zero field,
> there is no Darboux pair for which both reduced representatives have
> generator total degree at most \(2\).

The eight equations also have exact Gröbner basis \([1]\) over
\(\mathbb Q\), independently checked by
`route_a/nonhomogeneous_boundary.py`.  This is a bounded theorem, not a
global nonexistence proof.

The same full-coefficient calculation was carried out two degrees farther.
After the identical forced \(SL_2\) normalization, the common
degree-\(3\) system has 26 free coefficient variables and 43 nonconstant
bracket equations, while common degree \(4\) has 44 variables and 75
equations.  Singular 4.4.1p5 computes the reduced Gröbner basis \([1]\)
over \(\mathbb Q\) in both cases.  Thus:

> **Full degree-four obstruction.**  Over a characteristic-zero field,
> there is no Darboux pair for which both reduced representatives have
> generator total degree at most \(4\).

An unequal-degree elimination reaches beyond this common bound.  If
\(\deg P\leq2\) and \(\deg Q\leq d\), mixing \(Q\) into \(P\) is not a
degree-preserving normalization.  Instead the constant equation
\[
p_vq_w-p_wq_v=1
\]
has two exhaustive degree-preserving charts.  On \(p_v\ne0\), scaling and
shearing \(Q\) by \(P\) gives
\[
p_v=1,\qquad q_v=0,\qquad q_w=1.
\]
On \(p_v=0\), the same operations give
\[
p_v=0,\qquad p_w=1,\qquad q_v=-1,\qquad q_w=0.
\]
For \(d=5\), these charts have respectively 40 and 39 variables and 60
nonzero equations.  For \(d=6\), they have 53 and 52 variables and 77
nonzero equations.  Singular computes the reduced Gröbner basis \([1]\)
over \(\mathbb Q\) in all four systems.  Therefore:

> **Unequal degree-\((2,6)\) obstruction.**  There is no ordered Darboux
> pair with \(\deg P\leq2\) and \(\deg Q\leq6\).  By swapping the pair,
> the same holds whenever one member has degree at most two and the other
> has degree at most six.

This statement is reproducible from the generated coefficient system,
not from a saved opaque CAS session:

```sh
brew install singular  # if Singular is not already available
.venv/bin/python route_a/full_bounded_groebner.py --degree 4

.venv/bin/python route_a/unequal_bounded_groebner.py --q-degree 6
```

The script independently reconstructs the bracket rows and checks that
the reduced normal form of \(1\) is zero.  It deliberately supports only
the three bounds actually certified here.  As a reconnaissance check
before the rational computation, the degree-four ideal also reduced to
\([1]\) over \(\mathbb F_{32003}\); only the subsequent rational run is
used for the characteristic-zero theorem.

## 6a. First boundary-filtration equation

In the completion along \(D=(u,w)\), use \(w\) as a uniformizer; the
surface equation gives
\[
u=w^2-vw^4+2v^2w^6-\cdots,\qquad \{v,w\}=1+O(w^2).
\]
For arbitrary reduced polynomials write
\[
\begin{aligned}
P&=P_0(v)+wP_1(v)+O(w^2),\\
Q&=Q_0(v)+wQ_1(v)+O(w^2).
\end{aligned}
\]
The order-zero part of the Darboux equation is the polynomial Bézout
identity
\[
P_0'(v)Q_1(v)-P_1(v)Q_0'(v)=1. \tag{BF0}
\]
This holds without any homogeneity or sparse-support assumption.  In
particular the tangent and normal boundary jets of \(P,Q\) can never
become collinear.  The new verifier checks (BF0) symbolically for a
generic reduced support.

Writing primes for \(d/dv\), the next two universal equations are
\[
\begin{aligned}
\text{(BF1)}\quad
2P_0'Q_2+P_1'Q_1-P_1Q_1'-2P_2Q_0'&=0,\\
\text{(BF2)}\quad
3P_0'Q_3+2P_1'Q_2+P_2'Q_1-P_1Q_2'\\
\qquad{}-2P_2Q_1'-3P_3Q_0'&=-2v.
\end{aligned}
\]
Here BF2 uses
\(\{v,w\}=\sqrt{1+4vw^2}=1+2vw^2+O(w^4)\).
The verifier reconstructs BF0--BF2 directly from the global bracket.

These local recurrences cannot by themselves give a finite-order
contradiction.  For example \(P=v\) has the formal boundary slice
\[
Q=\int\frac{dw}{\sqrt{1+4vw^2}}
=w-\frac23vw^3+\frac65v^2w^5-\cdots
\in\mathbb Q[v][[w]],
\]
which solves every boundary recurrence, even though Section 4 proves
that \(v\) has no global polynomial slice.  A degree-independent
obstruction therefore has to use finite polynomial termination or a
second boundary/global-fiber condition, not BF0--BF2 alone.

## 7. Relation to the July-2026 graded threefold mechanism

The pseudo-plane here is not the quotient surface appearing in the
graded three-dimensional construction.  For weights \((1,-1,-2)\), that
source quotient is already an affine plane with invariant coordinates,
and the descended map satisfies a *degenerate* equation
\[
\operatorname{Jac}(P,Q)=2L^2
\]
along a contracted divisor.  It needs no desingularization.  By contrast,
\(B\) is the smooth nontrivial pseudo-plane
\[
u(1+uv)=w^2,
\]
and Route A asks for a nowhere-degenerate symplectic equation
\(\{P,Q\}=1\) on it.  There is no identified pullback square between the
two constructions.

There is a conceptual analogy: both use a mixed-sign
\(\mathbb G_m\)-grading and nonproper behavior.  But the threefold
construction spends its quotient ramification on the factor \(L^2\).
Importing it directly into dimension two leaves precisely that
nonconstant Jacobian factor rather than a Keller pair.  The homogeneous
obstruction above shows that the most direct graded attempt to absorb the
factor inside this pseudo-plane cannot work in characteristic zero.
It does **not** exclude a genuinely nonhomogeneous Darboux pair.

Relevant current source:
T. Shaska, *Graded Keller maps and the Jacobian Conjecture*,
[arXiv:2607.20210](https://arxiv.org/abs/2607.20210), especially the
descent identity and the discussion of the dimension-two graded case.

## 8. Reproduction

From the repository root:

```sh
python3 route_a/verify_claims.py

.venv/bin/python route_a/nonhomogeneous_boundary.py

.venv/bin/python route_a/full_bounded_groebner.py --degree 4

python3 route_a/route_a_search.py exhaustive-mod-p \
  --prime 3 --p-degree 2 --q-degree 5 --max-solutions 10

python3 route_a/equivariant_hensel.py --stages 12 --max-degree 120

.venv/bin/python route_a/verify_w2_hensel_obstruction.py

python3 route_a/route_a_search.py sparse-char-zero \
  --p-degree 4 --q-degree 15 --support-size 1

python3 route_a/route_a_search.py sparse-char-zero \
  --p-degree 3 --q-degree 10 --support-size 2
```

The full degree-four calculation additionally requires Singular; all
other Route A commands use only the Python environment in
`requirements.txt`.

## 9. Two ledgers

### Construction ledger

* The characteristic-\(3\) pair is exact and has an unobstructed formal
  \(3\)-adic tower.
* The two \(w^2\)-perturbed characteristic-\(3\) pairs are also exact,
  but unlike the homogeneous seed they have an all-support obstruction
  already modulo \(9\).
* The tower cannot stabilize in degree in the homogeneous family.
* A viable redesign must break the \(\mathbb G_m\)-homogeneity and control
  boundary regularity simultaneously.
* The global primitive \(\beta\) suggests searching for short polynomial
  Pfaff decompositions rather than only coefficientwise brackets.

### Obstruction ledger

* Boundary valuation excludes the obvious \(u\)- and \(w\)-Hamiltonians.
* Generic-fiber residue excludes the pure-\(v\) Hamiltonian.
* Every affine-linear Hamiltonian is excluded, even against unbounded
  \(Q\).
* Every Hamiltonian \(cw+f(u)\), including nonlinear \(f\), is excluded
  against unbounded \(Q\).
* Every Hamiltonian \(cv+f(w)\), including nonlinear \(f\), is excluded
  against unbounded \(Q\).
* Every Hamiltonian \(cu+f(w)\), including nonlinear \(f\), is excluded
  against unbounded \(Q\).
* More generally, all six ordered elementary families
  \(cx_i+f(x_j)\), \(i\ne j\), are excluded against unbounded \(Q\).
* All separated families \(a x_i+b x_j+f(x_k)\) are excluded against
  unbounded \(Q\).  Hamiltonians with nonlinear mixed terms remain open.
* The mixed family \(av+C(u)w+F(u)\) is excluded against unbounded \(Q\),
  allowing arbitrary nonlinear \(u^mw\) terms.
* The bilinear family \(cw+\lambda uv\) is excluded against unbounded
  \(Q\), including the nonhomogeneous characteristic-\(3\) seed \(w+uv\).
* More generally \(cw+\lambda uv+F(u)\) is excluded for every polynomial
  \(F\), covering the \(u+w\pm uv\) characteristic-\(3\) seeds as well.
* The full variable-coefficient family
  \(C(u)w+\lambda uv+F(u)\) is excluded, structurally closing all 17
  low-degree characteristic-\(3\) seed Hamiltonians in characteristic
  zero.
* Adding a constant term to the \(v\)-coefficient is still excluded:
  \((b+\lambda u)v+C(u)w+F(u)\) has no mate for any affine nonzero
  \(b+\lambda u\).
* The structurally new quadratic support
  \(cw+\lambda uv+\mu v^2\) is excluded by its Newton polygon and toric
  residue differential.
* More generally, \(cw+\lambda uv+G(v)\) is excluded for every polynomial
  \(G\).
* The \(w^2\)-perturbation produces exact new characteristic-\(3\) pairs
  but is excluded in characteristic zero as part of the full
  \(u(b+\kappa u)v+C(u)w+F(u)\) family.
* Both new \(w^2\)-perturbed pairs fail the first Hensel equation modulo
  \(9\) by the functional \([v]+[uv^2]\).
* The next \(uvw\) perturbation has no rational mate by two nonzero
  residues, over either characteristic zero or \(\mathbb F_3\).
* The companion \(uv^2\) perturbation has no rational mate by its two
  nonzero normalization residues, again in either characteristic.
* The final \(v^2w\) perturbation is excluded in characteristic zero by a
  nonzero holomorphic differential on its complete normalization.
* Every nonlinear tail \(cw+H(uv)\) is excluded in characteristic zero
  by a nonzero generic-fiber residue; the minimal \((uv)^2\) orbit is
  also excluded in characteristic \(3\).
* The next \(uv^3\) orbit is excluded in characteristic zero by a
  holomorphic normalization differential.  Its positive-sign
  characteristic-\(3\) pair has an all-support obstruction modulo \(9\).
* The \(uv^2w\) orbit is excluded in both characteristics by residue
  \(1/\kappa\).
* The \(u^2vw\) and \(u^3v\) orbits are excluded in characteristic zero
  by genus-two one-pole arguments.
* The \(v^3w\) orbit is excluded in characteristic zero by a holomorphic
  normalization differential.
* More generally, the monomial-cone theorem excludes every
  \(w+uv+\kappa u^av^bw^c\) with \(a>b\ge1\), every non-affine diagonal
  case, and the full cone \(b>a,\ b\ge2a+c-1\).
* In the residual middle wedge, the sublattice
  \(2(b-a)-c\mid b\) is excluded for every coefficient by Puiseux
  residues, and every exponent is excluded for a generic coefficient by
  the nonzero first-variation residue.
* Arbitrary finite sums supported in the strict cone \(b>2a+c\) are
  excluded whenever their cleared Newton curve is nondegenerate; this
  includes a Zariski-open coefficient locus for every such support.
* The infinite Frobenius-central characteristic-\(3\) family
  \(P=w+(1+H^3)uv,\ Q=-v+uv^2+(1+H^3)v^2w\) is exact, but every member
  has the same all-support obstruction \([v]+[uv^2]\) modulo \(9\).
* The complementary support \(cw+\lambda uv+\nu vw\) is excluded by two
  nonzero residues on its generic conic.
* Every homogeneous Darboux pair is excluded in characteristic zero.
* Every pair with ordered degrees at most \((2,6)\), and hence every
  unordered pair with degree bounds \(\{2,6\}\), is excluded.
* De Rham exactness is **not** an obstruction.
* The reported low/sparse searches are exact only within their displayed
  bounds.
