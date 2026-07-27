# Cyclic characters force unbounded delay in the two-block filtered recurrence

Date: 25 July 2026

## Outcome

Consider the repeated-root top data
\[
 d=x^s(x^E+\ell),\qquad
 p_0=d^2+ux,\qquad q_0=d^3,
 \qquad s\ge2,\quad E\ge1,\quad \ell u\ne0,
\tag{1}
\]
of common-root degree \(g=s+E\).  The exact filtered recurrence does
not admit a uniform bounded-defect exclusion on this family.

More precisely, suppose
\[
 E\mid 2s-1.
\tag{2}
\]
Then the cyclic group \(\mu_E\) makes every defect-\(k\) jet a single
character.  The defect-\(k\) cokernel can be nonzero only if
\[
 \boxed{
 r\equiv k(s-1)\pmod E
 \quad\text{for some}\quad 1\le r\le k-2.
 }
\tag{3}
\]
This is an exact support condition, not an experimental pattern.

Consequently, for every prescribed cutoff \(K\), choose any odd
integer
\[
 E>3K-4,\qquad s={E+1\over2}.
\tag{4}
\]
Then all obstruction vectors through defect \(K\) vanish
identically in \(\ell,u\), and the reciprocal-bounded filtered jets
exist through that order.

Thus:

> There is no absolute \(K\) such that every two-block endpoint (1)
> is excluded by defect at most \(K\).

In particular, the proposed bound \(K=6\) is false.  A concrete
algebraic endpoint with \(g=14,E=9,s=5\) survives through defect six
and is first necessarily excluded at defect seven.

This is not a polynomial Keller counterexample.  For each fixed
endpoint the recurrence may still fail at a later, \(E\)-dependent
defect.  The theorem instead rules out an important proof strategy:
an all-two-block exclusion cannot come from checking any fixed
finite list of filtered defects.  It needs either an unbounded
cyclic descent, a generating-function argument for the full defect
sequence, or additional global rigidity.

## 1. The exact filtered recurrence

Put
\[
 A=p_0'=u+2dd',\qquad B=q_0'=3d^2d'.
\tag{5}
\]
The bounded defect-one pair is
\[
 p_1=-{4d'\over3u^2},\qquad
 q_1={1\over u}-{2dd'\over u^2},
\tag{6}
\]
and satisfies \(Aq_1-Bp_1=1\).

Assume bounded jets have been constructed through defect \(k-1\):
\[
 \deg p_i\le2g-i,\qquad
 \deg q_i\le3g-i.
\tag{7}
\]
At defect \(k\), write
\[
 h_k=-{1\over k}
 \sum_{\substack{i+j=k\\i,j\ge1}}
 \left(jp_i'q_j-ip_iq_j'\right).
\tag{8}
\]
The next equation is
\[
 Aq_k-Bp_k=h_k.
\tag{9}
\]
Since \(\gcd(A,B)=1\), there is a unique residue
\[
 q_k\equiv A^{-1}h_k\pmod B,\qquad \deg q_k<3g-1.
\tag{10}
\]
The exact obstruction vector consists of the coefficients of
\[
 x^{3g-k+1},\ldots,x^{3g-2}
\tag{11}
\]
in this residue.  If they vanish, then \(\deg q_k\le3g-k\), and
\[
 p_k={Aq_k-h_k\over B}
\tag{12}
\]
is a polynomial of degree at most \(2g-k\).  Indeed every term of
\(h_k\) has degree at most \(5g-k-1\), so the degree bound follows
after division by the degree-\((3g-1)\) polynomial \(B\).

This is the same exact modular recurrence used in the arbitrary
common-root obstruction
\[
 \operatorname{rem}_{\,3d^2d'}
 \left((2dd'+u)^{-1}h_k\right).
\tag{13}
\]

## 2. Cyclic-character theorem

Let \(\zeta^E=1\), and call \(f\in\mathbf C[x]\) a character-\(a\)
polynomial if
\[
 f(\zeta x)=\zeta^a f(x).
\tag{14}
\]
The polynomial \(d=x^s(x^E+\ell)\) has character \(s\), while \(d'\)
has character \(s-1\).

Under (2),
\[
 2s\equiv1\pmod E.
\tag{15}
\]
It follows that \(p_0\) has character \(1\), \(q_0\) has character
\(3s\), \(A\) is invariant, and \(B\) has character \(3s-1\).
Set
\[
 \delta=s-2.
\tag{16}
\]
We claim inductively that
\[
 \boxed{
 p_k\text{ has character }P_k=1+k\delta,\qquad
 q_k\text{ has character }Q_k=3s+k\delta.
 }
\tag{17}
\]
For \(k=0\) this was just checked.  Formula (6) gives character
\(s-1=1+\delta\) for \(p_1\), and \(q_1\) is invariant.  The latter
agrees with (17), because
\[
 3s+\delta=4s-2=2(2s-1)\equiv0\pmod E.
\]

For the induction step, both summands in (8) have character
\[
 P_i-1+Q_j=3s+k\delta=Q_k.
\tag{18}
\]
Thus \(h_k\) has character \(Q_k\).  Multiplication by the invariant
\(A\) and reduction modulo the character polynomial \(B\) preserve
the \(\mu_E\)-decomposition.  The unique residue (10) therefore has
character \(Q_k\).  Finally
\[
 (3s-1)+P_k=3s+k\delta=Q_k,
\tag{19}
\]
so (12) has character \(P_k\).  This proves (17).

The forbidden exponent at offset \(r\) in (11) is
\[
 n=3g-k+r,\qquad 1\le r\le k-2.
\tag{20}
\]
Since \(g=s+E\), its character is
\[
 n\equiv3s-k+r\pmod E.
\tag{21}
\]
It can occur in \(q_k\) only if this equals \(Q_k\).  Using (16)
gives exactly
\[
 r\equiv k(s-1)\pmod E.
\tag{22}
\]
This proves (3).

## 3. No uniform defect bound

Fix \(K\ge2\), choose \(E,s\) as in (4), and suppose a forbidden
coefficient occurs at some \(k\le K\).  Because
\[
 s-1={E-1\over2},
\]
condition (3) implies
\[
 2r+k\equiv0\pmod E.
\tag{23}
\]
But
\[
 0<2r+k\le3k-4\le3K-4<E,
\tag{24}
\]
which is impossible.  The obstruction vector is therefore zero at
every defect through \(K\).  Induction using Section 1 constructs
all bounded jets through that order.

The delay can be quantified.  For odd \(E\ge5\) and
\(s=(E+1)/2\), the first defect at which a forbidden character is
even permitted is
\[
 \boxed{
 k_0=\text{the smallest odd integer at least }
 \left\lceil{E+4\over3}\right\rceil.
 }
\tag{25}
\]
At \(k_0\), the unique permitted forbidden offset is
\[
 r_0={E-k_0\over2}.
\tag{26}
\]
Indeed an odd \(k\) first reaches the multiple \(E\) in
\(2r+k\), while an even \(k\) would have to reach \(2E\).
This linear growth is the structural source of the unbounded delay.
Equation (25) says only when a class may appear; it does not assert
that its coefficient is nonzero for every parameter.

For odd \(E\ge9\), there is a useful exact normal form for the first
two possible classes.  (The small cases \(E=5,7\) have a different
next-class pattern involving an even defect and must be treated
separately.)  Write
\[
 E=6m+\varepsilon,\qquad \varepsilon\in\{1,3,5\}.
\tag{26a}
\]
Then (25) becomes
\[
 k_0=2m+3.
\tag{26b}
\]
Give the parameters the scaling weights
\[
 \operatorname{wt}(\ell)=E,\qquad
 \operatorname{wt}(u)=2g-1=3E.
\tag{26c}
\]
The recurrence is homogeneous for these weights.  A common
denominator for the defect-\(k\) jets is \(u^{4k-2}\): it is true at
defect one, and (8) adds the denominators at \(i+j=k\), after which
multiplication by the inverse representative \(q_1\) adds two more
powers.

For the unique first permitted offset (26), the cleared obstruction
numerator has parameter weight
\[
 E\,{9k_0-13\over2}=E(9m+7).
\tag{26d}
\]
Indeed the recurrence gives
\(\operatorname{wt}(q_k)=3g+k(1-5g)\); subtracting the forbidden
\(x\)-exponent \(3g-k+(E-k)/2\) and then adding the denominator
weight \(3E(4k-2)\) yields the displayed number.
Since \(u\) has weight \(3E\), every exponent of \(\ell\) is
congruent to \(1\) modulo \(3\).  Thus the first two possible
obstruction numerators have the exact homogeneous forms
\[
\boxed{
 \ell\,P_{m,\varepsilon}(u,\ell^3),
 \qquad \deg P_{m,\varepsilon}=3m+2,
}
\tag{26e}
\]
and
\[
\boxed{
 \ell\,Q_{m,\varepsilon}(u,\ell^3),
 \qquad \deg Q_{m,\varepsilon}=3m+5.
}
\tag{26f}
\]
Here zero leading or trailing coefficients are allowed in the word
``degree'' only as homogeneous specializations; every monomial has
the displayed total degree in the two variables \(u,\ell^3\).

After \(\ell\ne0\) is normalized, the first-two-class strategy for
this \(E\ge9\) range is therefore exactly the univariate statement
\[
 \gcd_{\mathbf Q[u]}
 \left(P_{m,\varepsilon}(u,1),
       Q_{m,\varepsilon}(u,1)\right)=1
\tag{26g}
\]
for all admissible \(m\) and the three residue classes
\(\varepsilon\).  The verified cases \(E=9,11,13,15,17\) satisfy
(26g), but no uniform resultant identity is proved here.  Equations
(35)--(44) suggest that these polynomials should be treated as
consecutive Padé or Hankel defects of the Catalan quotient series,
not by expanding a growing grid.

### 3.1 Exact first resultant chamber

The first simultaneous odd-defect chamber of (26g) consists of
\(E=9,11\): in both cases defects five and seven are the first two
permitted classes.  Sparse reduction, with its coefficients retained
as polynomial functions of \(E\), gives
\[
 \mathcal O_5=
 -{\ell(3E+1)\over972u^{18}}\,P_5(E;u,\ell),
 \qquad
 \mathcal O_7=
 {\ell(3E+1)\over104976u^{26}}\,Q_7(E;u,\ell),
\tag{26h}
\]
where \(P_5\) and \(Q_7\) are homogeneous of degrees five and eight
in \(u,\ell^3\), respectively.  Their complete coefficient formulas
are recorded in
`verify_general_two_block_resonant_first_resultant_chamber.py`.
After normalizing \(\ell=1\), exact elimination gives
\[
 \operatorname{Res}_u(P_5,Q_7)
 =c\,E^{90}(E+1)(3E+1)^3R_{52}(E),
\tag{26i}
\]
with \(c\in\mathbf Q^\times\) and
\(\deg R_{52}=52\).  Every coefficient of
\[
 R_{52}(T+9)
\tag{26j}
\]
is strictly positive.  Hence this polynomial resultant family is
nonzero for every real \(E\ge9\), in particular at \(E=9,11\).

For the integer values \(E=9,11\), defect five is the first permitted
class and defect seven is the next one.  Therefore (26i) proves that
no parameter can kill both obstructions: every algebraic branch that
survives defect five fails at defect seven.  The nearby collision
case \(E=7\) is handled separately by defects five and six.

This is a genuine exact resultant calculation, but only for the two
simultaneous base-chamber endpoints \(E=9,11\) of the growing-degree
family.  It does not prove (26g) for arbitrary \(m\).  Its useful role
is an exact base-case checksum for a proposed Padé, Hankel, or
continuant recurrence.  The verifier checks the symbolic
factorization, coefficientwise positivity, and independent
ordinary-recurrence specializations at \(E=9,11\).

## 4. Exact hostile example to defect six

Take
\[
 E=9,\qquad s=5,\qquad g=14,\qquad \ell=1.
\tag{27}
\]
The character test makes defects two, three, four, and six vanish
identically.  Defect five has one possible coordinate.  Apart from a
nonzero scalar and a power of \(u\), it is
\[
\begin{aligned}
 P_5(u)={}&186838225u^5+23740768548u^4
 +532637805132u^3\\
 &+4447199793231u^2
 +15962498987778u
 +23724081064404.
\end{aligned}
\tag{28}
\]
Choose any root \(\alpha\) of \(P_5\).  Its constant term is nonzero,
so \(\alpha\ne0\).  Over the exact number field
\(\mathbf Q(\alpha)\), all bounded equations through defect six
are soluble.

At defect seven, the single possible coordinate has numerator
\[
\begin{aligned}
 P_7(u)={}&3559879483055u^8
 +1254368611253457u^7\\
 &+74129178578871600u^6
 +1662884438039607177u^5\\
 &+18545694665345607285u^4
 +115093632573725049054u^3\\
 &+411718849720612848108u^2
 +810110778243003255744u\\
 &+713249706931339822992.
\end{aligned}
\tag{29}
\]
Exact Euclidean division gives
\[
 \gcd_{\mathbf Q[u]}(P_5,P_7)=1.
\tag{30}
\]
Thus every algebraic branch surviving through defect six fails at
defect seven.  This example is a finite filtered countermodel to the
bound six, not a counterexample to the Jacobian conjecture.

## 5. Consequence for the repeated-root route

The exact chamber formula
\[
 2s-3=qE+j,\qquad
 \operatorname{rem}_d(d')^3
 =(-1)^{q+1}E^3\ell^{q+3}x^{s+j}
\tag{31}
\]
still controls the first nonlinear remainder.  The cyclic theorem
shows why formulas at any fixed list of defects cannot settle all
\((q,j)\)-chambers: the resonant subfamily
\[
 2s-1=E
\tag{32}
\]
has no admissible cokernel coordinate until defect on the order of
\(E/3\).

A promising next target is therefore not “defect at most six,” but
one of:

1. derive a generating recurrence for the single allowed character
   along (32) and prove its successive obstruction polynomials have
   no common nonzero root;
2. descend an equivariant formal solution through the
   \(\mu_E\)-quotient and find a global incompatibility;
3. prove that actual polynomial Keller endpoints cannot enter the
   resonant chamber (32), using data not present in the filtered
   top-form recurrence.

The character theorem, the exact \(E=9,s=5\) obstruction
polynomials, their coprimality, and direct recurrence samples are
audited by
`verify_general_two_block_cyclic_defect_delay.py`.

## 6. Quotient-ring generating equation on the resonant family

The resonant subfamily (32) admits a fixed all-order formulation.
Put
\[
 \delta={E-3\over2},\qquad
 X=x^E,\qquad Z=x^\delta y.
\tag{33}
\]
Every equivariant formal completion has a unique expression
\[
 F=x\,\mathcal A(X,Z),\qquad
 G=x^{-\delta}\mathcal B(X,Z),
\tag{34}
\]
where \(\mathcal A,\mathcal B\) are Laurent series in \(X\) and
formal series in \(Z\).  Direct differentiation transforms
\(J(F,G)=1\) into
\[
\boxed{
 E X\left(\mathcal A_X\mathcal B_Z
          -\mathcal A_Z\mathcal B_X\right)
 +\mathcal A\mathcal B_Z
 +\delta\mathcal B\mathcal A_Z=1.
}
\tag{35}
\]
This is the requested closed quotient-ring recurrence.  Its
coefficients depend polynomially on \(E\), while the reciprocal
filtration becomes an explicit Laurent window.

Indeed, writing
\[
 \mathcal A=\sum_{k\ge0}A_k(X)Z^k,\qquad
 \mathcal B=\sum_{k\ge0}B_k(X)Z^k,
\tag{36}
\]
the original jets are
\[
 p_k=x^{1+k\delta}A_k(X),\qquad
 q_k=x^{(k-1)\delta}B_k(X).
\tag{37}
\]
Consequently every exponent \(m\) of \(X\) in \(A_k\) must lie in
\[
\boxed{
 \left\lceil-{1+k\delta\over E}\right\rceil
 \le m\le
 \left\lfloor{3E-k-k\delta\over E}\right\rfloor,
}
\tag{38}
\]
and every exponent in \(B_k\) must lie in
\[
\boxed{
 \left\lceil-{(k-1)\delta\over E}\right\rceil
 \le m\le
 \left\lfloor{{(10-k)E+k\over2E}\right\rfloor.
}
\tag{39}
\]
Equations (35), (38), and (39) are an all-order criterion: the
resonant endpoint has a bounded completion exactly when the
coefficient recurrence from (35) can remain inside these windows
until both polynomials terminate.  The first lost Laurent slot is
the character event (25)--(26).

There is also a closed unrestricted formal solution.  Define
\[
\begin{aligned}
 a_0&=u+X(X+\ell)^2,\\
 b_0&=X^2(X+\ell)^3,\\
 a_1&=-{4\over3u^2}(gX+s\ell),\\
 b_1&={1\over u}
 -{2\over u^2}X(X+\ell)(gX+s\ell),
\end{aligned}
\tag{40}
\]
and
\[
 \omega=
 \left((\delta+1)a_1+EXa_1'\right)b_1
 -EXa_1b_1'.
\tag{41}
\]
Let \(\Phi\) be the unique series satisfying
\[
 \Phi+{\omega\over2}\Phi^2=Z.
\tag{42}
\]
Then
\[
 \boxed{
 \mathcal A=a_0+a_1\Phi,\qquad
 \mathcal B=b_0+b_1\Phi
}
\tag{43}
\]
solves (35).  Equivalently,
\[
 \Phi=\sum_{k\ge1}
 {(-1)^{k-1}C_{k-1}\over2^{k-1}}
 \omega^{k-1}Z^k,
\tag{44}
\]
where \(C_n\) is the \(n\)-th Catalan number.

The series (44) never terminates: in the original coordinate,
\[
 x^\delta\omega
 =-{4\over3u^4}\left(ud''+2(d')^3\right),
\tag{45}
\]
whose leading term from \((d')^3\) is nonzero.  This does not by
itself exclude a bounded polynomial completion, because the
homogeneous solutions at every defect correspond to formal source
reparametrizations and can move (44) between Laurent slots.  It
does, however, reduce the remaining resonant problem precisely:

> Can any formal source reparametrization of the Catalan solution
> (43) keep every coefficient inside (38)--(39) and terminate?

Thus the search for an infinite compatible sequence is no longer an
unstructured grid.  It is a Laurent-window normalization problem
for the single algebraic series (42).  A positive terminating answer
would reconstruct an exact polynomial Keller candidate; a proof
that normalization must eventually cross a window would exclude the
entire delayed resonant family.

## 7. Finite-quotient geometry and the exact Miyanishi gap

The same resonance has a useful quotient-surface interpretation.
With respect to a primitive \(E\)-th root, the source and target
actions have type
\[
 {1\over E}\left(1,{E+3\over2}\right).
\tag{46}
\]
This is the restriction of the positive weighted action
\[
 \lambda\cdot(x,y)=(\lambda^2x,\lambda^3y)
\tag{47}
\]
to a cyclic subgroup, but the completed map is only
\(\mu_E\)-equivariant.  The wrapping by multiples of \(E\) in
(38)--(39) is exactly what prevents promotion to full
\(\mathbf G_m\)-equivariance.

When \(3\nmid E\), action (46) is small.  Its
Hirzebruch--Jung string is unusually short:
\[
\begin{array}{c|c}
 E& E/((E+3)/2)\\ \hline
 E=6m+1 &[2,m+1,3]^-\\
 E=6m+5 &[2,m+2,2,2]^-.
\end{array}
\tag{48}
\]
Indeed the first Euclidean remainder is
\[
 2{E+3\over2}-E=3,
\]
after which the two congruence classes modulo six give the displayed
chains.

If \(E=3n\), the action contains a pseudoreflection subgroup
\(\mu_3\).  Quotienting it first leaves the small odd cyclic action
\[
 {1\over n}\left(1,{n+1\over2}\right),
\tag{49}
\]
whose Hirzebruch--Jung string is
\[
 [2,(n+1)/2]^-.
\tag{50}
\]

Miyanishi's equivariant Jacobian theorem proves that, for a small
finite group \(G\), a \(G\)-equivariant étale endomorphism of
\(\mathbf A^2\) is an automorphism when \(|G|\) is even.  His paper
also closes the scalar cyclic type \(1/n(1,1)\) by proving
preservation of the standard \(\mathbf A^1_*\)-fibration.  The small
actions (46), or (49) after pseudoreflection reduction, have odd
order and are non-scalar for the delayed range, so neither theorem
applies directly.

For a small cyclic action of type \((n,d)\), Miyanishi's standard
completion has two degenerate fibers.  Their distinguished
multiplicities are
\[
 m_0={n\over\gcd(n,d-1)},\qquad
 m_\infty={n\over\gcd(n,d^{-1}-1)}.
\tag{51}
\]
For both (46) and (49),
\[
 \gcd(n,d-1)=\gcd(n,d^{-1}-1)=1,
\qquad
 \boxed{m_0=m_\infty=n.}
\tag{52}
\]
Thus this family lies in a particularly symmetric two-fiber
subcase of the unresolved odd cyclic geometry.

There is an important hostile check on the proposed bridge.
Miyanishi proves preservation when the proper transform \(H\) of
the source infinity section is not contracted and maps to the target
infinity section \(S_1\).  If \(H\) is contracted, or maps into an
exceptional component over one of the two special fibers, the
argument explicitly leaves the problem open.

For a hypothetical completion here, the ordinary component degrees
are \((2g,3g)\).  Along a generic radial ray
\((x,y)=R(1,t)\),
\[
 {G(R,Rt)\over F(R,Rt)}
 \sim R^g\,{G_{3g}(1,t)\over F_{2g}(1,t)}.
\tag{53}
\]
Hence the naive image of the radial infinity section tends to the
special target direction \(G/F=\infty\), rather than moving along
the target section.  After resolving indeterminacies, this places
\(H\) precisely in the alternatives not covered by the existing
preservation lemma.  Equation (53) does not prove that the final
proper transform is contracted; it proves that
\(\Phi(H)=S_1\) cannot simply be assumed from equivariance.

The quotient-surface route is therefore reduced to a concrete new
lemma:

> For either short chain in (48), or the chain (50), exclude a
> boundary morphism of degree profile \((2g,3g)\) in which \(H\)
> contracts or lands in the exceptional chain over the
> \(m_\infty=n\) fiber.

Proving this would invoke Miyanishi's standard-fibration theorem and
exclude the entire resonant family at once.  At present it is an
exact promising gap, not a proved extension of the literature.

The continued fractions and multiplicity identities in
(48)--(52) are included in
`verify_general_two_block_cyclic_defect_delay.py`.  The literature
scope used here is Masayoshi Miyanishi,
*Equivariant Jacobian Conjecture in dimension two*,
arXiv:2110.06709.
