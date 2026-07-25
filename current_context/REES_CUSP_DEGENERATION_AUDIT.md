# Rees degeneration versus the cusp complement

Date: 24 July 2026

## 1. The total Rees map and its ramification divisor

Use the original case-c plane coordinates
\[
z=xy,\qquad w=xy^2.
\]
The radial caps are \(\deg_z P\leq2\) and \(\deg_zQ\leq3\).
Consequently
\[
\begin{aligned}
P_s(x,y)&=s^2P(x/s^2,sy),\\
Q_s(x,y)&=s^3Q(x/s^2,sy)
\end{aligned}
\tag{1}
\]
are polynomials in \(x,y,s\).  In radial coordinates this is the same
family as
\[
\bigl(s^2P(z/s,w),s^3Q(z/s,w)\bigr).
\]
Let
\[
\mathcal H=(P_s,Q_s,s):
\mathbb A^2_{x,y}\times\mathbb A^1_s
\longrightarrow
\mathbb A^2_{p,q}\times\mathbb A^1_s.
\tag{2}
\]
For \(s\ne0\), the source change in (1) has determinant \(s^{-1}\), the
target change has determinant \(s^5\), and
\[
[P,Q](x/s^2,sy)=x^2/s^4.
\]
It follows, first on \(s\ne0\) and then polynomially on all of the total
space, that
\[
\det D\mathcal H=x^2.
\tag{3}
\]
Thus the ramification divisor of the total map is
\[
\mathcal R=\{x=0\}\times\mathbb A^1_s.
\tag{4}
\]

This corrects an important point: only the central outer map contracts
\(x=0\).  A full case-c completion has
\[
p(y):=P(0,y),\qquad q(y):=Q(0,y)
\]
of degrees \(8\) and \(12\), respectively, so its critical line maps
nontrivially.

## 2. The first missing condition is already one-dimensional

Fix \(L\ne0\), put
\[
C_L=\{q^2=Lp^3\},\qquad Y=\mathbb A^2\setminus C_L.
\]
On the ramification divisor,
\[
\mathcal H(0,y,s)=\bigl(s^2p(sy),s^3q(sy),s\bigr),
\tag{5}
\]
and hence
\[
\bigl(Q_s^2-LP_s^3\bigr)(0,y)
=s^6\bigl(q(sy)^2-Lp(sy)^3\bigr).
\tag{6}
\]
Because \(C_L\) is invariant under the target weights \((2,3)\), (6)
gives the exact equivalence
\[
\mathcal R\cap\mathcal H^{-1}(Y\times\mathbb A^1)=\varnothing
\quad\Longleftrightarrow\quad
q(y)^2=Lp(y)^3.
\tag{7}
\]
Therefore the restriction
\[
\mathcal H^{-1}(Y\times\mathbb A^1)
\longrightarrow Y\times\mathbb A^1
\tag{8}
\]
is not even unramified unless the boundary identity in (7) is proved.
The Newton support and the equation \([P,Q]=x^2\) do not by themselves
state this identity.

There is a sharp strengthening in the full-vertex case.  Suppose
\[
\deg p=8,\qquad \deg q=12,\qquad q^2=Lp^3.
\]
Unique factorization gives
\[
p=a h^2,\qquad q=b h^3,\qquad b^2=La^3,\qquad \deg h=4.
\tag{9}
\]
On the open part of \(x=0\) on which \(h\ne0\), set
\[
t=\frac{aQ}{bP},\qquad n=Q^2-LP^3.
\]
Then \(t|_{x=0}=h\), and direct differentiation gives
\[
\det\frac{\partial(t,n)}{\partial(P,Q)}
\bigg|_{x=0}
=\frac ba h^2.
\tag{10}
\]
Since \([P,Q]=x^2\), the right side of the pulled-back Jacobian is
\((b/a)h^2x^2\).  Write \(n=x^rA\) with \(A(0,y)\ne0\) generically.
The first term of \([t,n]\) is
\[
-r h'(y)A(0,y)x^{r-1}.
\]
Consequently
\[
r=3,\qquad
-3h'A(0,y)=\frac ba h^2.
\tag{11}
\]
In particular \(h'\mid h^2\).  In characteristic zero this is possible
for a nonconstant polynomial only when \(h\) has one distinct root:
\[
h=c(y-y_0)^4.
\tag{12}
\]
After the standard additive normalization
\(P(0,0)=Q(0,0)=0\), one gets \(y_0=0\).  Hence étaleness over the fixed
cusp complement forces
\[
P(0,y)=A y^8,\qquad Q(0,y)=B y^{12},
\qquad B^2=LA^3.
\tag{13}
\]
All lower coefficients on the vertical Newton edges must vanish.
This is a much smaller necessary test than any full coefficient
elimination.

The same calculation yields a useful exact factorization.  Under (7),
\[
Q^2-LP^3=x^3S(x,y),
\tag{14}
\]
and the Jacobian equation implies
\[
\begin{aligned}
x[P,S]-3P_yS&=2Q,\\
x[Q,S]-3Q_yS&=3LP^2.
\end{aligned}
\tag{15}
\]
Under the normalization (13),
\[
S(0,y)=-\frac{B}{12A}y^5.
\tag{16}
\]
Equations (14)--(16) are a possible low-dimensional entry point for
excluding the cusp-compatible boundary before studying global
monodromy.

## 3. Support containment does not imply (7)

The following exact map uses only monomials contained in the case-c
Newton polygons:
\[
\begin{aligned}
P&=x+y,\\
Q&=x^2y+xy^2+\frac13y^3.
\end{aligned}
\tag{17}
\]
Indeed
\[
[P,Q]
=(x^2+2xy+y^2)-(2xy+y^2)=x^2.
\]
Its critical line has image
\[
(p(y),q(y))=(y,y^3/3),
\]
which is not contained in any fixed cusp \(q^2=Lp^3\).  Its Rees family is
\[
\begin{aligned}
P_s&=x+s^3y,\\
Q_s&=x^2y+s^3xy^2+\frac{s^6}{3}y^3,
\end{aligned}
\tag{18}
\]
and has total Jacobian \(x^2\), but the restriction (8) is ramified.

This example does not have the required nonzero top vertices
\((0,8),(0,12)\).  It therefore does not disprove a theorem that
essentially uses the full Newton polygon.  It does prove that polygon
containment, the radial caps, and the Jacobian identity are insufficient;
the full-vertex argument must establish (13), rather than assume that the
critical line is still contracted.

## 4. Properness is a second, independent condition

Even after (7), étale and finite are different issues.  Let
\(S_{\mathcal H}\) denote the relative nonproper-value set of (2).
By (3) and (7), the restriction (8) is étale and hence quasi-finite.
It is finite exactly when
\[
S_{\mathcal H}\subseteq C_L\times\mathbb A^1.
\tag{19}
\]
Equivalently, take a normal compactification of the graph of
\(\mathcal H\), proper over the target.  Every source-boundary divisor
must map into \(C_L\times\mathbb A^1\).  This formulation includes both:

1. horizontal ends, which for \(s\ne0\) say \(S_F\subseteq C_L\); and
2. vertical Rees ends over \(s=0\), which are not ruled out merely by
   properness of the individual generic and central restrictions.

The family is equivariant for
\[
\lambda\cdot(x,y,s)=(\lambda^2x,\lambda^{-1}y,\lambda s),
\qquad
\lambda\cdot(p,q,s)=(\lambda^2p,\lambda^3q,\lambda s).
\tag{20}
\]
This organizes the possible boundary images, but does not eliminate
them.  In particular a vertical boundary image can be another weighted
cusp \(q^2=L'p^3\), an axis, or the fixed cusp.  Equivariance alone does
not force \(L'=L\).

A one-dimensional warning already shows the logical gap.  The equivariant
family
\[
(x,s)\longmapsto(sx,s)
\]
is finite over the punctured parameter and has empty central preimage
over \(\mathbb G_m\), but its restriction over
\(\mathbb G_m\times\mathbb A^1\) is not finite: the solution \(x=p/s\)
escapes as \(s\to0\).  Thus finite generic and central slices do not imply
relative finiteness.

## 5. What the cusp divisor detects

Let
\[
\mathcal D=\{Q_s^2-LP_s^3=0\}.
\]
On its normalization, away from \(P_sQ_s=0\), put
\[
\tau=\frac{Q_s}{\sqrt L\,P_s}.
\]
Then
\[
P_s=\tau^2,\qquad Q_s=\sqrt L\,\tau^3.
\tag{21}
\]
A boundary point of \(\mathcal D^\nu\) with finite nonzero \(\tau\)
records an intersection of a dicritical boundary image with the torus
part of the fixed cusp.  Such points are therefore effective witnesses
for extra nonproper curves and are well suited to a toric facet audit.

The converse needs care.  Another weighted cusp
\(q^2=L'p^3\), \(L'\ne L\), meets \(C_L\) only at the origin in the affine
plane.  It can violate (19) without creating a finite nonzero
\(\tau\)-end.  Thus an argument based only on finite nonzero ends of
\(\mathcal D^\nu\) must also prove that the residual weighted ratio
\(q^2/p^3\) of every vertical dicritical is \(L\).

## 6. Conditional payoff and recommended order of attack

If both (7) and (19) hold, (8) is finite étale.  Over an algebraically
closed field of characteristic zero, finite étale covers of
\(Y\times\mathbb A^1\) are pulled back from \(Y\).  Hence the fibers at
\(s=0\) and \(s=1\) are isomorphic covers of \(Y\).  With the normalized
peripheral sheet (or, equivalently, the trivial deck group of the fixed
outer dessin), this isomorphism gives the desired rational comparison
branch.

The efficient order is therefore:

1. test the one-variable boundary consequence (13);
2. if it survives, use (14)--(16) and the Newton caps to seek a direct
   contradiction;
3. only then audit toric boundary valuations for (19), separating
   horizontal nonproper curves from vertical Rees ends and checking the
   residual ratio \(q^2/p^3=L\).

At present neither (7) nor (19) follows from the stated Rees construction.
Thus the proposed total finite-étale assertion is a conditional route,
not an established bridge.
