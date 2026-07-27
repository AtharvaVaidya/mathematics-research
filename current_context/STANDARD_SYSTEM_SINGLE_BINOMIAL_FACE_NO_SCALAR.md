# A single binomial face cannot supply the Keller scalar

Date: 26 July 2026

## Outcome

There is a complete obstruction for one isolated binomial Newton face.
Let
\[
n=ga,\qquad m=gb,\qquad
\gcd(a,b)=1,\qquad 1<a<b,
\]
and write
\[
q=\left\lfloor\frac ba\right\rfloor,\qquad
r=b-aq,\qquad 1\le r<a.
\tag{1}
\]
For the local face
\[
P=s^a+c\tau^d,\qquad c\ne0,
\tag{2}
\]
the homogenized Keller bracket forces the polynomial \(Q\)-face to
have the binomial coefficients through its last polynomial term when
\(d<n\).  The remaining endpoint is
\[
c\,r(n-d)C_q
\tau^{d(q+1)}s^{r-1}.
\tag{3}
\]
No distinct polynomial \(Q\)-monomial can cancel this endpoint.

For (3) to be the scalar Keller forcing, one needs
\[
r=1,\qquad d(q+1)=N=n+m-2.
\tag{4}
\]
Together with the reciprocal bound \(d\le n\) and \(g>1\), these
equalities force
\[
g=2,\qquad d=n.
\tag{5}
\]
But then the coefficient \(n-d\) in (3) is zero.  Hence one isolated
binomial face cannot supply a nonzero Keller scalar.

This theorem does not treat faces with interior \(P\)-monomials,
several Newton faces, or multi-jet interactions.

There is also a root-vanishing extension.  For
\[
P=s^a+c\tau^d s^\sigma,\qquad
0\le\sigma<a,\qquad h=a-\sigma,
\]
the chain step is \(h\), but its coefficients are still
\(c^j\binom{b/a}{j}\).  Its terminal coefficient contains
\(gh-d\).  Globally, for a squarefree common root \(R\), the reciprocal
degree bound and the local terminals classify every surviving
single-face first jet:
\[
\boxed{
d=g(a-\sigma),\qquad T=cR^\sigma.
}
\]
These are exactly the already known \(g\)-sector monomials.

## 1. Exact telescoping

Use the local version of the homogenized Keller bracket
\[
\mathscr K(P,Q)
=\tau(P_sQ_\tau-P_\tau Q_s)
+nP Q_s-mQ P_s.
\tag{6}
\]
Start the \(Q\)-face at \(s^b\):
\[
Q_{\mathrm{face}}
=\sum_{j=0}^{q}
C_j\tau^{dj}s^{b-aj},
\qquad C_0=1.
\tag{7}
\]
For a fixed summand
\[
Q_j=C_j\tau^{dj}s^{b-aj},
\]
the part of \(\mathscr K(P,Q_j)\) coming from \(s^a\) is
\[
a j(d-n)C_j
\tau^{dj}s^{b-a(j-1)-1},
\tag{8}
\]
whereas the part coming from \(c\tau^d\) is
\[
c(n-d)(b-aj)C_j
\tau^{d(j+1)}s^{b-aj-1}.
\tag{9}
\]
For \(0\le j<q\), (9) and the next copy of (8) occupy the same
lattice point.  When \(d<n\), their cancellation forces
\[
C_{j+1}
=c\,\frac{b-aj}{a(j+1)}C_j.
\tag{10}
\]
Consequently
\[
\boxed{
C_j=c^j\binom{b/a}{j}
\quad(0\le j\le q).
}
\tag{11}
\]

The \(j=q\) copy of (9) has no polynomial successor because
\(b-a(q+1)=r-a<0\).  It is exactly
\[
\boxed{
\mathscr K(P,Q_{\mathrm{face}})
=c\,r(n-d)C_q
\tau^{d(q+1)}s^{r-1}.
}
\tag{12}
\]

The case \(d=n\) must be stated separately.  Then both (8) and (9)
vanish term by term, so the Keller bracket does not force the
recurrence (10).  It also cannot produce the scalar: the entire face
bracket, including (12), is zero for arbitrary \(C_j\).

## 2. Why a new polynomial \(Q\)-monomial cannot cancel the endpoint

Consider a further polynomial monomial
\[
M=h\tau^e s^k,\qquad e,k\ge0.
\tag{13}
\]
Its bracket with the two terms of \(P\) has support only at
\[
(e,a+k-1)
\quad\text{and}\quad
(e+d,k-1)
\tag{14}
\]
in \((\tau\text{-order},s\text{-exponent})\).
The terminal point in (12) is
\[
\bigl(d(q+1),r-1\bigr).
\tag{15}
\]
Matching it through the first point of (14) would require
\[
e=d(q+1),\qquad k=r-a<0,
\]
which is not polynomial.  Matching it through the second point
requires
\[
e=dq,\qquad k=r.
\]
This is the existing \(j=q\) face monomial, not a new monomial.
Changing its coefficient destroys the preceding cancellation, and
(10) uniquely restores the nonzero value (11).

Thus no distinct polynomial \(Q\)-monomial cancels (12) within a
single face.  A second chain of monomials or a second \(P\)-face can
change this conclusion; those are explicitly outside the theorem.

## 3. Scalar endpoint arithmetic

The terminal is scalar in \(s\) only if \(r=1\).  Then
\[
b=aq+1
\]
and
\[
\begin{aligned}
N
&=g(a+b)-2\\
&=g\bigl(a(q+1)+1\bigr)-2\\
&=n(q+1)+g-2.
\end{aligned}
\tag{16}
\]
If its \(\tau\)-order is the forcing order, then
\[
d(q+1)=n(q+1)+g-2.
\tag{17}
\]
The reciprocal bound \(d\le n\) makes the left side at most
\(n(q+1)\).  Since the common-root case has \(g\ge2\), equation (17)
forces \(g=2\), and then forces \(d=n\).  Formula (12) consequently
has coefficient
\[
c\,r(n-d)C_q=0.
\tag{18}
\]
It cannot equal the nonzero Keller scalar.

## 4. A root-vanishing binomial face

Let
\[
P=s^a+c\tau^d s^\sigma,\qquad
0\le\sigma<a,\qquad h=a-\sigma,
\tag{19}
\]
and put
\[
q_h=\left\lfloor\frac bh\right\rfloor,\qquad
r_h=b-hq_h,\qquad 0\le r_h<h.
\tag{20}
\]
The polynomial \(Q\)-chain is now
\[
Q_{\mathrm{face}}
=\sum_{j=0}^{q_h}
C_j\tau^{dj}s^{b-hj},
\qquad C_0=1.
\tag{21}
\]

For its \(j\)-th monomial, the \(s^a\)-part of the bracket is
\[
a j(d-gh)C_j
\tau^{dj}s^{a+b-hj-1},
\tag{22}
\]
and the \(c\tau^ds^\sigma\)-part is
\[
c(gh-d)(b-aj)C_j
\tau^{d(j+1)}s^{\sigma+b-hj-1}.
\tag{23}
\]
The supports in (22)--(23) interlace because \(a-h=\sigma\).
Whenever \(d\ne gh\), cancellation forces the same recurrence as
before:
\[
C_{j+1}
=c\,\frac{b-aj}{a(j+1)}C_j,
\qquad
C_j=c^j\binom{b/a}{j}.
\tag{24}
\]
The terminal is
\[
\boxed{
\mathscr K(P,Q_{\mathrm{face}})
=c(gh-d)(b-aq_h)C_{q_h}
\tau^{d(q_h+1)}s^{\sigma+r_h-1}.
}
\tag{25}
\]
Because \(\gcd(a,b)=1\), one has
\[
b-aq_h\ne0,
\]
and the generalized binomial coefficient \(C_{q_h}\) is also nonzero.
Thus (25) is nonzero when \(d\ne gh\).

A distinct polynomial \(Q\)-monomial cannot cancel (25).  The two
possible source exponents would be
\[
\begin{aligned}
&e=d(q_h+1),\qquad k=r_h-h<0,\\
\text{or}\qquad
&e=dq_h,\qquad k=r_h.
\end{aligned}
\tag{26}
\]
The first is not polynomial, while the second is precisely the last
monomial already fixed by (24).

If the terminal were the scalar Keller forcing, then
\[
\sigma+r_h=1,\qquad d(q_h+1)=N.
\tag{27}
\]
But
\[
\begin{aligned}
a+b
&=(\sigma+h)+(hq_h+r_h)\\
&=h(q_h+1)+1,
\end{aligned}
\]
so
\[
N=gh(q_h+1)+g-2.
\tag{28}
\]
Under the local bound \(d\le gh\) and \(g\ge2\), equations (27)--(28)
force
\[
g=2,\qquad d=gh.
\]
The coefficient in (25) then vanishes.  Therefore every strict case
\(d<gh\) is obstructed within this single face, whether its terminal
is nonscalar or is a scalar candidate.

## 5. Global classification, including varying root orders

Let \(R\in\mathbb C[X]\) be monic, squarefree, and of degree \(g\).
Consider a reciprocal first jet
\[
P=R^a+\tau^dT+\text{higher \(\tau\)-order},
\qquad
\deg T\le n-d.
\tag{29}
\]
At every root \(\alpha\) of \(R\), assume
\[
\sigma_\alpha=\operatorname{ord}_\alpha T<a
\tag{30}
\]
and assume that the local initial pair consists only of the
root-vanishing \(P\)-face (19) and its single \(Q\)-chain (21).
Here one uses \(s=R(X)\) as the local coordinate.  Since \(R\) is
squarefree, \(R'(\alpha)\ne0\), and the \(X\)-derivative version of
the Keller bracket is the displayed \(s\)-derivative bracket times
this local unit.  Higher terms in the local unit
\(T/s^{\sigma_\alpha}\) lie strictly above the selected face and do
not change its terminal coefficient.
Put
\[
h_\alpha=a-\sigma_\alpha.
\]

Squarefreeness and (30) give
\[
\deg T\ge\sum_{R(\alpha)=0}\sigma_\alpha.
\]
Together with the reciprocal degree bound in (29), this yields
\[
d
\le ga-\sum_\alpha\sigma_\alpha
=\sum_\alpha h_\alpha.
\tag{31}
\]

If some \(gh_\alpha>d\), the strict local theorem above gives a
nonzero uncancellable terminal at that root.  Hence a surviving
single-face jet must obey
\[
gh_\alpha\le d
\quad\text{for every }\alpha.
\tag{32}
\]
Summing (32) gives
\[
\sum_\alpha h_\alpha\le d.
\]
Comparison with (31) forces equality everywhere:
\[
gh_\alpha=d
\quad\text{for every }\alpha.
\tag{33}
\]
Thus \(g\mid d\), all \(\sigma_\alpha\) have a common value
\[
\sigma=a-\frac dg,
\]
and both degree bounds are saturated:
\[
\deg T=\sum_\alpha\sigma_\alpha=g\sigma=n-d.
\tag{34}
\]
There are no additional zeros.  Since \(R\) is monic and squarefree,
\[
\boxed{
T=cR^\sigma,\qquad
d=g(a-\sigma).
}
\tag{35}
\]

Conversely this is exactly the surviving \(g\)-sector monomial
\[
P=R^a+c\tau^{g(a-\sigma)}R^\sigma,
\tag{36}
\]
whose single-face bracket has \(gh-d=0\).  This proves the promised
classification under the stated local single-face hypotheses.

The uniform-order special case is immediate: if \(T\) vanishes to
order \(\sigma\) at every root, then
\[
R^\sigma\mid T,\qquad
g\sigma\le\deg T\le n-d,
\]
so \(d\le g(a-\sigma)\); strict inequality is obstructed and equality
forces \(T=cR^\sigma\).
In particular, if \(\deg T>g\sigma\), then
\[
d\le n-\deg T<g(a-\sigma),
\]
so the strict local obstruction applies.  Extra degree cannot produce
another survivor inside the single-face hypothesis.

## 6. Conditional classification of a whole compact face

The binomial calculation has a compact-face extension which includes
all interior monomials on one edge.  Its hypotheses are stronger than
merely choosing a local Newton edge.

Let
\[
h=a-\sigma,\qquad
e=\gcd(h,d),\qquad
h=h'e,\qquad d=d'e,
\tag{37}
\]
and set
\[
z=\frac{\tau^{d'}}{s^{h'}}.
\]
Assume that the **entire isolated matched initial pair** at this slope
is
\[
P_0=s^aA(z),\qquad
Q_0=s^bB(z),
\qquad A(0)=B(0)=1,
\tag{38}
\]
with no second \(P\)- or \(Q\)-face contributing at the same or lower
face weight.  The nonzero far endpoint of the \(P\)-face gives
\[
\deg A=e.
\tag{39}
\]

Direct differentiation yields
\[
\boxed{
\mathscr K(P_0,Q_0)
=(d'-gh')s^{a+b-1}z
\left(aAB'-bA'B\right).
}
\tag{40}
\]
Give \(s,\tau\) weights \(d',h'\), respectively.  The face term in
(40) has weight
\[
(a+b-1)d',
\]
whereas the scalar right side has weight
\[
h'N.
\]
Their difference is
\[
h'N-(a+b-1)d'
=(a+b-1)(gh'-d')+h'(g-2).
\tag{41}
\]
Therefore, under the additional slope bound
\[
d'<gh',
\tag{42}
\]
the isolated face lies strictly below the Keller forcing and must
vanish:
\[
aAB'-bA'B=0.
\tag{43}
\]
Since \(A(0)=B(0)=1\), equation (43) gives
\[
B^a=A^b.
\]
Unique factorization and \(\gcd(a,b)=1\) imply
\[
A=C^a,\qquad B=C^b
\tag{44}
\]
for a polynomial \(C\) with \(C(0)=1\).

Now
\[
a\mid\deg A=e,\qquad
e\le h\le a.
\]
Thus \(e=a\), whence
\[
\sigma=0,\qquad h'=1,\qquad \deg C=1.
\]
Writing \(C=1+\kappa z\), the complete face is
\[
\boxed{
P_0=(s+\kappa\tau^{d/a})^a,\qquad
Q_0=(s+\kappa\tau^{d/a})^b.
}
\tag{45}
\]
It is a reduced common-root shift, not a nonreduced normal face.

At equality
\[
d'=gh'
\quad\Longleftrightarrow\quad
d=g(a-\sigma),
\tag{46}
\]
the prefactor in (40) vanishes identically.  This is precisely the
physical \(g\)-sector resonance, and (40) imposes no relation between
\(A\) and \(B\).

The slope bound used here is not automatically pointwise when the
orders \(\sigma_\alpha\) vary among the roots of a global \(R\).
For uniform vanishing it follows from
\[
g\sigma\le\deg T\le n-d,
\]
which gives \(d\le gh\).  With varying orders, the global statement is
only the averaged inequality (31); one must combine it with local
faces as in Section 5.

Likewise, (38) is a substantive hypothesis.  Standard
\(\lambda_k\tau^kC^{m-k}\)-terms can create another residue class or
another \(Q\)-edge.  Unless their combined initial form is already the
single polynomial \(s^bB(z)\), equation (40) is not the whole initial
Keller bracket.  Finally, local constants \(\kappa_\alpha\) can glue
to a polynomial reduced-cone deformation
\(R\mapsto R+\tau^{d/a}\dot R(X)\), rather than to one global scalar
shift.  The global gluing is not classified here.

## 7. Strict scope

The hypothesis (2) excludes every interior monomial on its Newton
edge.  Such a monomial has
\[
\tau^v s^k,\qquad
dk+av=ad,\qquad
0<k<a,\quad0<v<d.
\tag{47}
\]
There are \(\gcd(a,d)-1\) interior lattice points when
\(\gcd(a,d)>1\).  Their bracket contributions add new convolution
terms to (8)--(10), so the one-dimensional telescoping argument does
not apply.

For the root-vanishing edge (19), the corresponding equation is
\[
dk+hv=da,
\tag{48}
\]
and there are \(\gcd(h,d)-1\) strict interior lattice points.  They
are likewise excluded.

The theorem also excludes:

* lower \(P\)-jets away from the displayed edge;
* simultaneous or intersecting \(Q\)-faces;
* cancellation cascades between different \(\tau\)-orders;
* the full GGV standard-presentation constraints; and
* global branch gluing and endpoint pairing.

Accordingly this is a rigorous closure of one face, not a proof of the
branch-resonance lemma.
