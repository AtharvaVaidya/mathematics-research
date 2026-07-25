# Laurent edge-cutting versus polynomial degree descent

Date: 25 July 2026

## Conclusion

There is a rigorous polynomial-descent theorem for one natural subclass
of a Laurent-normalized terminal corner:

> If a pair with Jacobian \(c x^r\) lies in the Rees subring
> \[
> k[x,x^r y]\subset k[x,y],
> \]
> then the monomial Jacobian can be absorbed by a birational affine
> modification.  Expressing the pair in the polynomial coordinates
> \[
> u=x,\qquad v=x^r y
> \]
> produces a genuine constant-Jacobian pair, with the same function-field
> degree.

This gives an exact degree-lowering/minimality criterion and excludes
every normalized terminal support contained in the cone
\[
a\ge rb
\tag{1}
\]
when the resulting coordinate degrees violate the chosen minimality
bound.

The criterion does **not** apply to the GGHV \((72,108)\) polygons.
Their required vertices lie far outside (1).  More importantly, the
usual local data at the contracted boundary do not force Rees-subring
membership.  There is an exact infinite countermodel:
\[
\boxed{
\begin{aligned}
P_N&=x+(xy)^N,\\
Q_N&=x^2y+\frac{N}{N+1}(xy)^{N+1},
\qquad N\ge2,
\end{aligned}}
\tag{2}
\]
for which
\[
[P_N,Q_N]=x^2.
\tag{3}
\]
The line \(x=0\) is contracted to one point, its first two normal jets
are precisely the apparently birational affine-modification jets, and
the function-field degree is \(N+1\), which is arbitrarily large.
Nevertheless neither coordinate belongs to \(k[x,x^2y]\).

Thus valuation positivity, boundary contraction, the leading normal
form, and even a lower bound on function-field degree cannot turn
Laurent edge-cutting into polynomial descent.  The missing input must be
a **full Rees-semigroup or equivalent all-jet theorem**, not a
divisorial valuation statement.

## 1. Context from the standard-pair reduction

The primary references are:

- J. A. Guccione, J. J. Guccione, and C. Valqui,
  *On the shape of possible counterexamples to the Jacobian
  Conjecture*, arXiv:1401.1784,
  <https://arxiv.org/abs/1401.1784>;
- J. A. Guccione, J. J. Guccione, and C. Valqui,
  *The two-dimensional Jacobian conjecture and the lower side of the
  Newton polygon*, arXiv:1605.09430,
  <https://arxiv.org/abs/1605.09430>;
- J. A. Guccione, J. J. Guccione, R. Horruitiner, and C. Valqui,
  *Some algorithms related to the Jacobian Conjecture*,
  arXiv:1708.07936,
  <https://arxiv.org/abs/1708.07936>;
- the same authors, *Increasing the degree of a possible counterexample
  to the Jacobian Conjecture from 100 to 108*,
  arXiv:2204.14178,
  <https://arxiv.org/abs/2204.14178>.

The first three sources show that, if \(JC(2)\) is false, one may choose
a standard minimal pair and attach an admissible chain of Newton
corners.  Edge cutting uses automorphisms of Laurent extensions
\[
L^{(l)}=k[x^{1/l},x^{-1/l},y],
\]
typically
\[
x^{1/l}\longmapsto x^{1/l},\qquad
y\longmapsto y+\lambda x^{-\kappa/l}.
\tag{4}
\]
Such a map preserves the bracket because its source Jacobian is one,
but it need not preserve \(k[x,y]\).

At the end of GGHV Proposition 4.3, the monomial chart
\[
x\longmapsto x^{-1},\qquad y\longmapsto x^4y
\tag{5}
\]
has Jacobian \(-x^2\).  It converts the remaining equation to
\[
[P,Q]=x^2.
\tag{6}
\]
The attractive minimality idea is to absorb this factor \(x^2\) into a
new polynomial source chart and thereby obtain a smaller Keller pair.
The next theorem states exactly when the most natural affine
modification does this.

## 2. Fixed-line affine-modification descent theorem

Let \(k\) be a characteristic-zero field, let \(r\ge1\), and put
\[
A=k[x,y],\qquad
B_r=k[x,x^r y].
\tag{7}
\]
The elements
\[
u=x,\qquad v=x^r y
\tag{8}
\]
are algebraically independent, so \(B_r=k[u,v]\) is an abstract
polynomial ring.  Moreover
\[
k(u,v)=k(x,y)
\tag{9}
\]
because \(y=v/u^r\).  Thus (8) is a birational polynomial affine
modification, not a finite quotient.

### Theorem

Suppose \(P,Q\in B_r\) and
\[
[P,Q]_{x,y}=c x^r,\qquad c\in k^\times.
\tag{10}
\]
Write uniquely
\[
P=\bar P(u,v),\qquad Q=\bar Q(u,v).
\]
Then
\[
\boxed{[\bar P,\bar Q]_{u,v}=c.}
\tag{11}
\]
Furthermore
\[
[k(x,y):k(P,Q)]
=[k(u,v):k(\bar P,\bar Q)].
\tag{12}
\]
Consequently, if the pair in (10) is birationally obtained from a
noninvertible Keller pair, then \((\bar P,\bar Q)\) is itself a genuine
plane Keller counterexample.

### Proof

The chain rule and (8) give
\[
[u,v]_{x,y}=x^r
\]
and hence
\[
[P,Q]_{x,y}
=[\bar P,\bar Q]_{u,v}[u,v]_{x,y}
=x^r[\bar P,\bar Q]_{u,v}.
\]
Equation (11) follows from (10).  Equality (12) follows from (9).
If \((\bar P,\bar Q)\) were a polynomial automorphism, its rational
function field would equal \(k(u,v)\), contradicting nontriviality of
the degree on the left of (12).  This proves the theorem.

The same subring is obtained from every fixed-line modification
\[
u=x,\qquad v=x^r y-f(x),\qquad f\in k[x],
\tag{13}
\]
because adjoining \(f(x)\) does not change
\[
k[x,x^r y-f(x)]=k[x,x^r y].
\tag{14}
\]
Thus polynomial translations of the center do not enlarge the theorem.

## 3. Exact Newton and degree criterion

For
\[
R=\sum_{a,b}c_{ab}x^ay^b,
\]
monomial independence gives
\[
\boxed{
R\in B_r
\quad\Longleftrightarrow\quad
c_{ab}\ne0\Longrightarrow a\ge rb.
}
\tag{15}
\]
Equivalently, the coefficient of \(y^b\) must be divisible by
\(x^{rb}\).  This is a full transverse-jet condition.

Under (8),
\[
x^ay^b=u^{a-rb}v^b
\]
and its new total degree is
\[
\deg_{u,v}=a-(r-1)b.
\tag{16}
\]
Hence a normalized terminal pair satisfying (15) gives an explicitly
computable smaller Keller pair whenever
\[
\max_{(a,b)\in\operatorname{Supp}P\cup\operatorname{Supp}Q}
\bigl(a-(r-1)b\bigr)
\tag{17}
\]
is below the minimality measure of the original counterexample.

This is the rigorous degree-lowering subclass theorem sought from the
corner machinery.  It is uniform in the corner and requires no
coefficient elimination.  Its limitation is equally exact: a
divisorial statement such as
\[
P(0,y),Q(0,y)\in k
\tag{18}
\]
only says that the coefficients of \(y^b\), \(b>0\), are divisible by
\(x\).  Descent needs divisibility by \(x^{rb}\) for every \(b\).

In particular, if the original standard pair was chosen with
\[
B=\min\gcd(\deg P,\deg Q)
\]
among all Keller counterexamples, and the right side of (17) is smaller
than \(B\), the descended pair contradicts the definition of \(B\):
its two coordinate degrees have gcd at most their maximum.  This is the
precise minimality corollary; no comparison of vague polygon “sizes” is
being used.

## 4. The required GGHV vertices obstruct this descent

For Proposition 4.3, \(r=2\).  In the a/b polygon the required vertices
\[
(8,16)\in\Delta_P,\qquad(12,24)\in\Delta_Q
\]
have Rees defects
\[
8-2\cdot16=-24,\qquad
12-2\cdot24=-36.
\tag{19}
\]
In case c the additional required vertices are even farther outside:
\[
0-2\cdot8=-16,\qquad
0-2\cdot12=-24.
\tag{20}
\]
Since these vertex coefficients are nonzero, neither GGHV alternative
lies in \(B_2\).  Target polynomial automorphisms cannot repair this:
if two new target coordinates belonged to \(B_2\), applying the inverse
target automorphism would put the original \(P,Q\) in \(B_2\) as well.

This proves that the obvious affine modification associated with the
Jacobian divisor \(2\{x=0\}\) cannot be the missing GGHV-to-Keller
descent.  The obstruction is a semigroup failure, not merely a poor
choice of the center translation \(f(x)\).

## 5. Contracted \(x^2\)-boundary jet theorem

One might hope that (18), together with (6), recursively forces (15).
Even its leading consequence is unexpectedly rigid, but not rigid
enough.

### Theorem

Let
\[
[P,Q]=c x^2,\qquad c\ne0,
\tag{21}
\]
and suppose \(P(0,y)\) and \(Q(0,y)\) are constants.  After subtracting
those constants, interchanging \(P,Q\) if necessary, and making a
linear target shear, there are nonzero \(A,B\in k[y]\) such that
\[
\begin{aligned}
P&=xA(y)+O(x^2),\\
Q&=x^2B(y)+O(x^3),
\end{aligned}
\tag{22}
\]
and
\[
A B'-2A'B=c.
\tag{23}
\]
Moreover
\[
\boxed{\deg A\le1.}
\tag{24}
\]
More precisely:

1. if \(A=a\in k^\times\), then
   \[
   B=\frac ca\,y+b;
   \tag{25}
   \]
2. if \(A=ay+b\), \(a\ne0\), then
   \[
   B=\lambda A^2-\frac{c}{2a}.
   \tag{26}
   \]

### Proof

Both coordinates vanish modulo \(x\).  If both had \(x\)-order at least
two, their bracket would have \(x\)-order at least three, contrary to
(21).  Choose \(P\) with order one.  If \(Q\) also has order one, write
their leading coefficients as \(A,C\).  The coefficient of \(x\) in
the bracket is
\[
AC'-A'C=0,
\]
so \(C/A\) is constant.  A linear target shear removes this term from
\(Q\).  Its new \(x\)-order must be two, and the \(x^2\) row is (23).

Let \(d=\deg A\) and \(e=\deg B\).  If \(d=0\), equation (25) follows.
Assume \(d\ge1\).  The highest coefficient on the left of (23) is
\[
(e-2d)\operatorname{lc}(A)\operatorname{lc}(B)
y^{d+e-1}.
\tag{27}
\]
Unless \(e=2d\), constancy forces \(d+e-1=0\), hence \(d=1,e=0\).
If \(e=2d\), subtract the unique scalar multiple of \(A^2\) that kills
the leading term of \(B\).  This does not change (23).  Applying the
previous sentence to the new, lower-degree \(B\) again gives \(d=1\).
Solving (23) for linear \(A\) gives (26).

The two alternatives are respectively the leading jets of:

- the birational modification \((x,x^2y)\); and
- the quadratic fold \((xy,-x^2/2)\), after target scaling and shearing.

The theorem is useful local structure, but it controls only the first
two normal jets, whereas (15) controls every transverse jet.

## 6. Exact Laurent-canonical countermodel

Put
\[
s=xy.
\]
For every \(N\ge2\), define (2).  In the \((x,s)\)-coordinates,
\[
P_N=x+s^N,\qquad
Q_N=xs+\frac{N}{N+1}s^{N+1}.
\tag{28}
\]
Since
\[
[x,s]_{x,y}=x
\]
and
\[
[P_N,Q_N]_{x,s}
=(x+Ns^N)-Ns^N=x,
\]
equation (3) follows.

Both coordinates vanish identically on \(x=0\).  Their leading normal
jets are
\[
P_N=x+O(x^2),\qquad
Q_N=x^2y+O(x^3),
\tag{29}
\]
so they lie in the constant-\(A\) alternative (25).  Nevertheless the
monomials
\[
x^Ny^N,\qquad x^{N+1}y^{N+1}
\]
violate (15), and hence
\[
P_N,Q_N\notin B_2.
\tag{30}
\]

The example is not hiding a bounded field-degree defect.  From (28),
\[
x=P_N-s^N
\]
and
\[
s^{N+1}-(N+1)P_Ns+(N+1)Q_N=0.
\tag{31}
\]
Over \(k(P_N)\), the right coordinate is a polynomial of degree \(N+1\)
in the transcendental parameter \(s\).  Equivalently, the rational map
\[
s\longmapsto P_Ns-\frac{s^{N+1}}{N+1}
\]
has degree \(N+1\).  Therefore
\[
\boxed{
[k(x,y):k(P_N,Q_N)]=N+1.
}
\tag{32}
\]
The degrees in (32) are unbounded.

The smallest member \(N=2\) is especially sharp:
\[
P_2=x+x^2y^2,\qquad
Q_2=x^2y+\frac23x^3y^3.
\tag{33}
\]
Every displayed monomial lies inside the GGHV a/b polygon caps, and the
two fixed-pole vertices \((1,0)\) and \((2,1)\) are present.  What is
missing are the required outer vertices.  Thus polygon containment,
the monomial Jacobian, the fixed poles, and contracted-boundary jets
still do not imply polynomial descent; the full vertices used by the
all-scale obstruction carry essential information.

This family is best understood as a Laurent canonical transformation.
Starting from \(u=x,\ v=x^2y\), put \(s=v/u=xy\).  The rational
constant-bracket pair
\[
U=u+s^N,\qquad
V=us+\frac{N}{N+1}s^{N+1}
\tag{34}
\]
satisfies \([U,V]_{u,v}=1\), but uses the Laurent ratio \(s=v/u\).
After substituting \(v=x^2y\), all denominators cancel and (34) becomes
the polynomial pair (2).  This is exactly the mechanism that defeats a
valuation-only conversion of Laurent edge-cutting into polynomial
minimality.

## 7. Rees flatness does not separate the diagonal sheet

The member \(N=2\) also directly tests the transverse Rees proposal.  Put
\[
z=xy,\qquad
P=x+z^2,\qquad
Q=xz+\frac23z^3.
\tag{35}
\]
It has the exact radial caps \(\deg_zP=2,\deg_zQ=3\).  Consequently its
Rees deformation is constant:
\[
\begin{aligned}
P_t&=t^2P(x/t^2,ty)=P,\\
Q_t&=t^3Q(x/t^2,ty)=Q.
\end{aligned}
\tag{36}
\]
In particular the family is polynomial and flat in the strongest
possible sense, and its total Jacobian remains \(x^2\).

The comparison cover has an equally explicit equation.  For target
coordinates \(p,q\), the radial coordinate \(T\) satisfies
\[
\boxed{T^3-3pT+3q=0.}
\tag{37}
\]
Indeed \(x=p-T^2\) and
\[
q=pT-\frac13T^3.
\]
Equation (37) is monic, so its comparison algebra is finite flat of rank
three over \(k[p,q]\), hence proper.  It is irreducible over
\(k(p,q)\): over \(k(p)\), the polynomial map
\[
T\longmapsto pT-\frac13T^3
\]
has degree three.

After pulling (37) back along the source point \((x,z)\), it factors as
\[
\begin{aligned}
T^3-3PT+3Q
&=(T-z)
\bigl(T^2+zT-3x-2z^2\bigr).
\end{aligned}
\tag{38}
\]
The first factor is the diagonal comparison sheet.  On that sheet the
residual factor restricts to
\[
z^2+z^2-3x-2z^2=-3x.
\tag{39}
\]
Thus the diagonal component meets the residual component exactly along
the ramification divisor \(x=0\).  Its image there is
\[
p=z^2,\qquad q=\frac23z^3,
\qquad 4p^3-9q^2=0.
\tag{40}
\]
The discriminant of (37) is
\[
27(4p^3-9q^2),
\tag{41}
\]
so the joining locus is precisely the high cusp component.

This is a direct countermodel to the proposed implication

\[
\text{proper/flat Rees comparison}
\Longrightarrow
\text{the diagonal sheet stays separate from the high cusp}.
\]

The comparison is finite flat, the Rees family is constant, and the
generic cover is irreducible; nevertheless the diagonal section after
base change joins the residual sheet on the cusp.  Minimality is not
encoded in this model, and (35) omits the required outer vertices, so it
does not refute a theorem that essentially uses the complete admissible
chain.  It proves that neither Rees flatness nor properness can supply
that missing information.

## 8. What remains viable

The audit leaves a precise hierarchy.

1. **Proved:** full support containment in the Rees cone (15) gives a
   genuine polynomial Keller descent with preserved field degree.
2. **Proved:** the first contracted-boundary jets have only the two
   forms (25)--(26).
3. **Refuted:** boundary contraction, leading affine-modification jets,
   or any fixed lower bound on function-field degree forces Rees
   containment.
4. **Refuted for GGHV:** the obvious fixed-line affine modification can
   absorb the final \(x^2\) Jacobian.

A successful global bridge must therefore use information absent from
the divisor \(x=0\) and its first normal rows.  Two exact possibilities
remain:

- prove the all-jet inequalities
  \[
  \operatorname{ord}_x [y^b]P,
  \operatorname{ord}_x [y^b]Q\ge2b
  \tag{42}
  \]
  after a different birational boundary chart; or
- prove that the Laurent ratio analogous to \(s=v/u\) cannot have
  nontrivial algebraic degree when the normalized pair comes from a
  standard minimal **polynomial Keller pair** through the complete
  admissible chain.

The countermodel (2) shows that either proof must use the global
polynomial origin of the entire chain, not merely the terminal Newton
polygon, monomial Jacobian, or local boundary valuation.

## Reproduction

Run:

```bash
.venv/bin/python current_context/verify_laurent_degree_descent.py
```

The verifier checks:

- the affine-modification chain rule;
- both leading normal forms;
- (2)--(3) for \(2\le N\le10\);
- the degree-\(N+1\) relation (31);
- the constant Rees deformation and factorization (37)--(41);
- failure of the Rees cone for every tested member; and
- failure of the Rees cone at the required GGHV a/b and case-c vertices.
