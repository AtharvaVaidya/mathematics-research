# The arbitrary-\(d\) boundary has transverse degree at least fifteen

Date: 25 July 2026

## Outcome

Let \(d\in\mathbf C[x]\) be monic of positive degree, let
\(u\in\mathbf C^\times\), and put
\[
 \gamma(x)=\bigl(d(x)^2+ux,d(x)^3\bigr).
\tag{1}
\]
There are no \(P,Q\in\mathbf C[x,y]\) such that
\[
 [P,Q]_{x,y}\in\mathbf C^\times,\qquad
 (P(x,0),Q(x,0))=\gamma(x),\qquad
 \max(\deg_yP,\deg_yQ)\leq14.
\tag{2}
\]

At maximum transverse degree fifteen, after ordering the coordinates
and making the standard target reductions, the only arithmetic charts
not yet excluded are
\[
 (15,9),\qquad(15,10),\qquad(15,12).
\]
The fourth raw degree-fifteen survivor, \((15,6)\), is already
excluded.

The direct high-shear argument below excludes every maximum degree
through eight without a coefficient or first-integral classification.
Its first raw survivor is \((9,6)\), not \((5,6)\).  Combining the
exact exclusions of \((9,6)\), \((12,8)\), \((12,9)\), and
\((15,6)\) then gives the stronger bound fourteen.  Finally, the
boundary (1) has an explicit self-collision, so none of the
automorphic cases can complete it.

The result is not a construction, and it does not resolve the
arbitrary-degree polynomial-completion problem.

## 1. Target reduction and the actual degree patterns

Let
\[
 m=\deg_yP,\qquad n=\deg_yQ,\qquad m\geq n.
\tag{3}
\]
If \(n=0\), then \(Q=q(x)\) and
\[
 [P,Q]=-P_yq'\in\mathbf C^\times.
\]
Both factors are units, so \(q'\) and \(P_y\) are nonzero constants;
the pair is triangular and hence an automorphism.  Thus it is enough
to consider \(m\geq n>0\).

If \(m=n\), the coefficient of \(y^{2m-1}\) in the Jacobian says
that the two leading coefficients have constant ratio.  A constant
determinant-one target change lowers one of the two \(y\)-degrees.
Thus an unresolved maximum-six pair would reduce to
\[
 (m,n)=(6,n),\qquad n\leq5.
\tag{4}
\]

Write \(f_m,g_n\) for the leading coefficients.  The top Jacobian
equation is
\[
 n f_m'g_n-m f_mg_n'=0.
\tag{5}
\]
Put
\[
 d_0=\gcd(m,n),\qquad
 m=ad_0,\qquad n=bd_0,\qquad \gcd(a,b)=1.
\tag{6}
\]
Unique factorization, followed by constant target rescaling, gives
\[
 f_m=h^a,\qquad g_n=h^b
\tag{7}
\]
for a nonzero \(h\in\mathbf C[x]\).

If \(b=1\), subtracting the appropriate constant multiple of
\(Q^a\) from \(P\) lowers \(m\).  This is an exact polynomial target
shear, so it may be iterated.  Hence a minimal unresolved chart must
have
\[
 a>b\geq2.
\tag{8}
\]
The apparent \((5,6)\) pattern is therefore not a new approximate-root
system: it lies in the arithmetic automorphy range below.

## 2. The corrected high-shear arithmetic criterion

Let
\[
 s=\deg h,\qquad t=\gcd(d_0,s),
\tag{9}
\]
where \(\gcd(d_0,0)=d_0\).  Choose \(L\) larger than the
\(x\)-degree of every coefficient of \(P,Q\), and apply the source
automorphism
\[
 y\longmapsto y+x^L.
\tag{10}
\]
The total degrees become
\[
\begin{aligned}
 \deg P_L&=as+ad_0L=at\,p,\\
 \deg Q_L&=bs+bd_0L=bt\,p,
\end{aligned}
\qquad
 p=\frac{s}{t}+\frac{d_0}{t}L.
\tag{11}
\]
For \(s>0\), the two coefficients in the progression defining \(p\)
are coprime; Dirichlet therefore permits an arbitrarily large \(L\)
for which \(p\) is prime.  For \(s=0\), choose \(L=p\) prime.

The classical Magnus-type total-degree criteria used in the corrected
normal-degree arithmetic theorem imply automorphy if either
\[
 at\quad\hbox{or}\quad bt
\quad\hbox{lies in}\quad
 \{1,4\}\cup\{\text{prime numbers}\}.
\tag{12}
\]
Indeed, the corresponding coordinate in (11) then has total degree
\(p\), \(4p\), or a product of two primes.  The classical criteria
also cover \(t=1,2\) through the total-degree gcd \(tp\).

Precisely, only the classical gcd classes \(p,2p\) and the
one-coordinate classes \(p,p_1p_2,4p\) are being used here, with all
letters denoting primes.  These are Theorems 1.1 and 1.2 in
Moskowicz, [*A variation on Magnus' theorem and its
generalizations*](https://arxiv.org/abs/1810.08202v2); none of its
partial-degree or simultaneous-prime claims is needed.

This argument uses one prime progression only.  It does not use the
false simultaneous-prime lemma in the printed proof of the earlier
partial-degree theorem.

An exact enumeration of (6), (8), and all divisors \(t\mid d_0\)
through \(m=15\) shows:

* every unequal pair with \(m\leq8\) is removed by a power shear,
  (12), or the \(t=1,2\) criterion;
* there are no raw survivors at maximum degrees
  \(10,11,13,14\);
* the complete raw-survivor ledger is
  \[
  \begin{array}{c|c}
   m& (n,d_0,a,b,t,at,bt)\\ \hline
   9 &(6,3,3,2,3,9,6)\\
   12&(8,4,3,2,4,12,8),\ (9,3,4,3,3,12,9)\\
   15&(6,3,5,2,3,15,6),\ (9,3,5,3,3,15,9),\\
     &\quad(10,5,3,2,5,15,10),\
       (12,3,5,4,3,15,12).
  \end{array}
  \tag{13}
  \]

In particular every Keller pair of maximum \(y\)-degree six is a
polynomial automorphism.  No degree-\((5,6)\) first-integral system
survives the preceding normalization.

## 3. The four exact frontier exclusions

The first four entries of (13) are independently excluded as
noninvertible Keller maps:

1. the full \((9,6)\), \(t=3\) chart is closed by the connected,
   constant-cube, and nonconstant pure-power analyses culminating in
   `NORMAL_DEGREE_96_PURE_POWER_LINE_INJECTIVITY_EXCLUSION.md`;
2. `NORMAL_DEGREE_128_FULL_EXCLUSION.md` closes the full
   \((12,8)\), \(t=4\) chart;
3. `NORMAL_DEGREE_129_FULL_EXCLUSION.md` closes the full
   \((12,9)\), \(t=3\) chart, including the ramified half-order
   resonance; and
4. `NORMAL_DEGREE_156_FULL_EXCLUSION.md` closes the full
   \((15,6)\), \(t=3\) chart.

Each is an exact normal-degree theorem with the same leading-factor
condition recorded by its entry of (13).  Therefore target-reduction
induction and the arithmetic sieve make every Keller pair of maximum
\(y\)-degree at most fourteen an automorphism.  At exact maximum
fifteen, only the last three entries of (13) remain unresolved.

## 4. Imposing the arbitrary-\(d\) boundary

The boundary (1) is not injective.  Fix a primitive cube root
\(\zeta\), and set
\[
 c=\frac{1-\zeta^2}{u},\qquad
 \varphi(x)=x+c\,d(x)^2,
\qquad
 H_\zeta(x)=d(\varphi(x))-\zeta d(x).
\tag{14}
\]
The polynomial \(H_\zeta\) has degree \(2(\deg d)^2\), and
\[
 H_\zeta=dK_\zeta,\qquad
 \deg K_\zeta=2(\deg d)^2-\deg d>0,\qquad
 \gcd(K_\zeta,d)=1.
\tag{15}
\]
Indeed, if \(\alpha\) is any root of \(d\) of multiplicity \(r\),
then, locally at \(\alpha\),
\[
 \varphi(x)-\alpha=(x-\alpha)+O((x-\alpha)^{2r})
\]
and \(H_\zeta/d\) has nonzero leading value \(1-\zeta\).  Thus the
factor \(d\) contains exactly the inherited roots, including when
they are multiple.  This uses no hypothesis that \(d(0)=0\).

Choose a root \(x_0\) of \(K_\zeta\), and put
\(x_1=\varphi(x_0)\).  Then \(d(x_0)\ne0\), so \(x_1\ne x_0\), and
\[
 d(x_1)=\zeta d(x_0).
\tag{16}
\]
Consequently
\[
\begin{aligned}
 d(x_1)^3&=d(x_0)^3,\\
 d(x_1)^2+ux_1&=d(x_0)^2+ux_0.
\end{aligned}
\tag{17}
\]
Thus \(\gamma(x_1)=\gamma(x_0)\).

If a completion in (2) were an automorphism, its polynomial inverse,
restricted to the image of \(y=0\), would recover \(x\) from
\(\gamma(x)\).  Equation (17) makes that impossible.  Section 2 says
that every pair outside the raw ledger is an automorphism, and
Section 3 excludes every ledger entry below fifteen.  This gives the
required contradiction.

Therefore
\[
 \boxed{\max(\deg_yP,\deg_yQ)\geq15}
\tag{18}
\]
for any polynomial Keller completion of (1).  Equality can only occur,
after the standard target reductions, in one of
\[
 \boxed{(15,9),\ (15,10),\ (15,12).}
\tag{19}
\]
These three degree-fifteen charts are not excluded here.

The exact enumeration and collision identities are checked in
`verify_arbitrary_d_transverse_degree_fifteen_arithmetic_bound.py`.
The arithmetic dependency is developed independently in
`NORMAL_DEGREE_ARITHMETIC_FRONTIER_AND_96_CONNECTED_REDUCTION.md`
and
`NORMAL_DEGREE_86_TOTAL_DEGREE_CLOSURE_AND_CONNECTED_REDUCTION.md`;
the boundary collision is proved in
`ARBITRARY_D_CANONICAL_SYMPLECTIC_EXTENSION_AND_COLLISION_CRITERION.md`.
