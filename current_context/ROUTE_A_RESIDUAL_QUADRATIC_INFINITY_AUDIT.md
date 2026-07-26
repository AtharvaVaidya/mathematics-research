# Route A: the residual quadratic has free parity at infinity

Date: 25 July 2026

## Outcome

Assume the surviving Route A setup.  Thus
\[
F:S\longrightarrow {\bf A}^2
\]
is a hypothetical etale map of geometric degree three from
\[
S=\operatorname {Spec}{\bf C}[u,v,w]/(w^2-u-u^2v),
\qquad D=V(u,w)\simeq{\bf A}^1_v,
\]
and \(Y\to{\bf A}^2\) is its finite flat cubic normalization.  After
base change along the normalization
\(\nu_D:D\to\Gamma_D\), the distinguished etale section splits off:
\[
{\cal A}_D\simeq {\bf C}[v]\times
 {\bf C}[v,\tau]/(\tau^2-g(v)).
\tag{1}
\]

The exact conclusion of this audit is negative but sharp:

> **Residual-parity theorem.**  The cubic splitting determines a
> nonzero polynomial \(g\), up to multiplication by a nonzero square
> constant.  If
> \[
> g=c\,h^2s,\qquad s\ \hbox{squarefree},
> \tag{2}
> \]
> then the normalization of the residual factor has function field
> \[
> {\bf C}(v)(\sqrt{s}).
> \]
> It ramifies at a finite point \(v=v_0\) exactly when
> \(\operatorname {ord}_{v_0}g\) is odd, and it ramifies at
> \(v=\infty\) exactly when
> \[
> \boxed{\deg g\equiv1\pmod2.}
> \tag{3}
> \]
> Neither parity is constrained by the two boundary valuations of the
> canonical quadratic pseudoplane chart.  Those two valuations are the
> two split prolongations of the *distinguished cubic sheet* and are
> exchanged by the deck involution.  The cover (2), by contrast,
> permutes the *other two cubic sheets* longitudinally.

In particular, the defect-one distinguished dicritical class and its
residual defect budget \(4\) do **not** imply
\(\deg g=4\), \(\deg g\le4\), or even parity of \(\deg g\).  An exact
connected family of finite flat cubic covers below realizes every
nonzero polynomial \(g\) while retaining an everywhere-etale
distinguished section over the chosen line.  For squarefree \(g\), the
total cubic surface in this family is even smooth.  Thus no such
numerical claim follows from finite flatness, normality of the cubic
surface, the split section, or the deck involution alone.

This does not construct a Keller map from \(S\).  It isolates the
additional statement a contradiction would need: a global theorem
identifying residual cubic monodromy with particular nonproper
valuations of the degree-six plane composite.

## 1. What \(g\) records

Put \(R={\bf C}[v]\).  The rank-two factor in (1) has trace-zero
generator \(\tau\), unique up to multiplication by an element of
\(R^\times={\bf C}^{\times}\).  Hence replacing \(\tau\) by
\(\lambda\tau\) replaces \(g\) by \(\lambda^2g\).  In particular
\(\deg g\), the orders of its roots, and all their parities are
intrinsic.

The generic cubic extension is separable, so \(g\ne0\).  The two
generic decomposition types are
\[
\begin{array}{c|c}
g\notin{\bf C}(v)^{\times2}&1+2,\\
g\in{\bf C}(v)^{\times2}&1+1+1.
\end{array}
\tag{4}
\]
Because the constant field is algebraically closed, (2) shows that
the first case is equivalent to \(s\) being nonconstant.

Let \(\Delta_\pi(x,y)\) be a branch-discriminant equation for the
cubic cover.  The product decomposition makes the trace matrix block
diagonal, and changing a global cubic basis to the product basis
changes its determinant by a unit of \(R\).  Therefore
\[
\Delta_\pi(\nu_D(v))=c_0g(v),\qquad c_0\in{\bf C}^{\times}.
\tag{5}
\]
Consequently
\[
\deg g=\deg_v\Delta_\pi(\nu_D(v)),
\tag{6}
\]
with the degree on the right taken after all leading cancellations.
A root order of \(g\) is the corresponding intersection multiplicity
of the normalized curve with the cubic branch divisor.  This is the
only unconditional degree statement supplied by the discriminant.

Repeated factors of \(g\) affect the nonnormal model in (1), not its
quadratic function field.  More precisely, after (2) the normalization
is obtained from \(\rho=\tau/h\) and
\[
\rho^2=c\,s(v).
\tag{7}
\]
Thus finite ramification occurs precisely at the roots of \(s\).
At infinity,
\[
\operatorname {ord}_{\infty}g=-\deg g,
\]
which proves (3).  If \(r=\deg s>0\), the smooth projective
normalization has
\[
g_{\rm hyp}=\left\lfloor\frac{r-1}{2}\right\rfloor
\tag{8}
\]
and has one point over infinity for \(r\) odd and two for \(r\) even.
For \(s=1\), the generic residual factor is split.

## 2. The two canonical boundary valuations are different

Let
\[
K={\bf C}(S),\qquad M=K(\sqrt u).
\]
At the generic point of \(D\), \(w\) is a uniformizer and
\[
u(1+uv)=w^2.
\tag{9}
\]
In the completed field \({\bf C}(v)((w))\), the unit
\((1+uv)^{-1}\) has a square root congruent to \(1\) modulo \(w\).
Therefore \(u\) is a square in that completed field.  The valuation of
\(D\) has two prolongations to \(M\), characterized by
\[
\frac{\sqrt u}{w}\equiv+1
\quad\hbox{or}\quad
\frac{\sqrt u}{w}\equiv-1
\pmod w.
\tag{10}
\]
The deck involution \(\sqrt u\mapsto-\sqrt u\) exchanges them.

The polynomial chart makes the two prolongations concrete:
\[
u=a^2,\qquad
w=a(1+2a^2b),\qquad
v=4b(1+a^2b),
\tag{11}
\]
with rational deck involution
\[
\sigma(a,b)=(-a,-b-a^{-2}).
\tag{12}
\]
One prolongation is the finite line \(a=0\), where \(v=4b\).  The
other is the escaping dicritical branch.  In its polynomial chart
\[
(a,b)=(-t+\eta t^3,-t^{-2}),
\tag{13}
\]
the invariants extend across \(t=0\) and satisfy
\[
(u,v,w)|_{t=0}=(0,-8\eta,0).
\tag{14}
\]
Thus the same normalization parameter is related by
\[
\eta=-\frac v8.
\tag{15}
\]
Both prolongations have residue degree one, and (15) extends to an
unramified degree-one map at \(v=\infty\).

Equations (10)--(15) are independent of \(g\).  They describe how the
canonical quadratic extension \(M/K\) splits over the distinguished
prime \(D\).  Equation (7) instead describes the residue-field
extension of the other two primes of the cubic cover after base change
to \(D\).  One is transverse splitting in the quadratic pseudoplane
tower; the other is longitudinal \(S_2\)-monodromy in the cubic tower.
There is no valuation-theoretic reason for their infinity
ramification to agree.

There is also no hidden permutation obstruction.  In the standard
\(S_4\) realization of the degree-six tower, label the three cubic
sheets by the partitions
\[
{\cal P}_0=\{12,34\},\qquad
{\cal P}_1=\{13,24\},\qquad
{\cal P}_2=\{14,23\},
\]
and label the six degree-six sheets by the individual edges.  The
vertex transposition \((12)\) fixes \({\cal P}_0\), swaps
\({\cal P}_1\) and \({\cal P}_2\), and fixes both edges \(12\) and
\(34\) above \({\cal P}_0\).  Hence an odd-degree \(g\), whose infinity
monodromy swaps the two residual cubic sheets, is compatible with
complete splitting of the canonical double cover over the
distinguished sheet.  For even-degree \(g\), the identity permutation
does the same.  Both parities therefore survive even in the natural
six-sheet permutation model.

## 3. Every squarefree polynomial \(g\) occurs in a smooth connected
cubic family

The independence above is not merely formal.  Let
\[
A={\bf C}[x,y]
\]
and fix an arbitrary nonzero polynomial \(G(x)\).  In Miranda's
four-coefficient description of a finite flat triple cover, take
\[
a=1,\qquad b=y,\qquad c=-\frac{G}{3},\qquad d=0.
\tag{16}
\]
The resulting rank-three \(A\)-algebra has trace-zero basis \(z,w\)
and multiplication
\[
\begin{aligned}
z^2&=2+z+yw,\\
zw&=-\frac{yG}{3}-w,\\
w^2&=\frac{2G}{3}-\frac G3z.
\end{aligned}
\tag{17}
\]
Along the line \(y=0\), the map
\[
1\longmapsto(1,1),\qquad
z\longmapsto(2,-1),\qquad
w\longmapsto(0,\tau)
\tag{18}
\]
is an algebra isomorphism
\[
{\cal A}/(y)\simeq
{\bf C}[x]\times
{\bf C}[x,\tau]/(\tau^2-G(x)).
\tag{19}
\]
The first factor gives the section \(z=2,w=0\).  It is etale even at a
zero of \(G\): in the fiber algebra it is the isolated reduced
length-one factor, while all ramification is in the residual
length-two factor.

This cubic cover is connected.  On \(y\ne0\), \(z\) generates its
generic algebra; with \(T=z+1\), its equation is
\[
T^2(T-3)+\frac{y^2G(x)}3=0.
\tag{20}
\]
The monic cubic (20) has no root in \({\bf C}(x,y)\).  Indeed any such
root is integral over the UFD \({\bf C}[x,y]\), hence is a polynomial.
Writing it as \(r\), the identity
\[
r^2(r-3)=-\frac{y^2G}{3}
\tag{21}
\]
and \(\gcd(r,r-3)=1\) leave two possibilities for the \(y\)-adic
orders.  If \(y\mid r\), then \(r=yh\), and comparison of \(y\)-degrees
in
\[
h^2(yh-3)=-G/3
\]
is impossible.  If \(y\nmid r\), then \(r^2\) divides \(G(x)\), so
\(r\) is independent of \(y\); reduction of (21) modulo \(y\) forces
\(r=3\), again impossible.  Hence (20) is irreducible.

If \(G\) is squarefree, the total cubic surface is smooth.  On
\(y\ne0\), equation (20) is a hypersurface, and a singular point would
have
\[
3T(T-2)=0,\qquad y^2G'(x)=0,\qquad 2yG(x)=0.
\]
Since \(y\ne0\), this would force \(G=G'=0\), contrary to
squarefreeness.  On \(y=0\), the section \(z=2,w=0\) is smooth because
the \(z,w\) derivative minor of the first two relations in (17) is
\(9\).  On the residual component \(z=-1,w^2=G\), the same Jacobian
has rank two: if \(G\ne0\), the \(z,w\) minor from the first and third
relations is \(-6w\ne0\); if \(G=0\), then \(G'\ne0\), and the \(z,x\)
minor is \(3G'\ne0\).  Thus squarefree \(G\) gives a smooth, hence
normal, connected finite flat cubic cover.

The branch polynomial of (16) is
\[
{\cal D}
=\frac{G}{9}\bigl(y^2G-12\bigr),
\qquad
{\cal D}|_{y=0}=-\frac43G,
\tag{22}
\]
in agreement with (5).

Taking \(G=x\) gives odd degree and a residual cover ramified at
infinity.  Taking \(G=x^2-1\) gives even degree and a residual cover
unramified at infinity.  Taking polynomials of arbitrary degree proves
that the cubic algebra plus its etale section imposes no degree bound
or parity.  Both displayed choices are squarefree, so they are already
smooth normal countermodels to any deduction from the finite-cover
package.

This family is a countermodel only to deductions from the finite-flat
and section data.  Its etale locus is not the quadratic pseudoplane,
so it does not construct the hypothetical Route A map.

## 4. Why the dicritical defect budget does not count roots of \(g\)

For the degree-six plane composite
\[
H=F\circ\pi_2,
\]
the distinguished dicritical class (13) is etale and contributes
exactly \(1\) to Orevkov's formula.  The other classes contribute
\(4\).  Those summands are local-degree defects of polynomial maps on
dicritical boundary lines.  In contrast, a zero of \(g\) is a finite
target value where the two residual cubic sheets ramify in the finite
normalization.

No boundary divisor is created by an isolated zero of \(g\), and the
two notions are not terms in the same formula.  The family (16)--(22)
varies the number and parity of the zeros while leaving the split
distinguished section unchanged.  Therefore an implication such as
\[
\deg g\le4
\quad\hbox{or}\quad
\deg g\equiv4\pmod2
\tag{23}
\]
requires an additional global compactification theorem.  It cannot be
deduced by assigning one unit of dicritical defect to each root.

## 5. Conditional route that would be sufficient

A contradiction could still arise if one proves, for the **specific**
quadratic-pseudoplane Keller tower, both of the following new inputs:

1. every odd place of the residual quadratic extension (including
   infinity) determines a distinct non-distinguished dicritical
   contribution of prescribed positive size;
2. the canonical deck involution pairs those contributions without
   fixed classes.

Under those extra assumptions, the residual budget \(4\) would become
a genuine bound and parity condition.  Neither statement follows from
the local splitting (1), the valuation calculation (10), or the
parameter identification (15).  The present audit therefore closes
the direct infinity-parity shortcut and identifies the missing global
bridge precisely.

## Verification

Run

```sh
.venv/bin/python current_context/verify_route_a_residual_quadratic_infinity_audit.py
```

for the Miranda multiplication, line splitting, branch polynomial,
irreducible odd/even examples, canonical chart, dicritical limit, and
Jacobian checks.
