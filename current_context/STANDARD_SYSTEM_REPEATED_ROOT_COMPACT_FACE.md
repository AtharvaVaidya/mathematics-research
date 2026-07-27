# Strict compact faces at a repeated common root

Date: 26 July 2026

## Outcome

The strict compact-face bridge extends locally to a repeated root, but
the normalized face need not be a linear root shift.

Let a root of the degree-\(g\) common polynomial \(R\) have
multiplicity \(e\ge2\).  Put
\[
p=ae,\qquad q=be,\qquad n=ga,\qquad m=gb,
\qquad N=n+m-2,
\]
where \(\gcd(a,b)=1\).  In a local coordinate with \(R=s^e\), let the
entire first \(P\)-face have primitive slope \(d'/h'<g/e\).

For an actual polynomial Keller pair:

1. the entire lowest \(Q\)-face is automatically the matched face;
2. if the compact bracket lies below the scalar forcing, then
   \[
   P_0=D_0^a,\qquad Q_0=D_0^b,
   \qquad
   D_0=s^eC\!\left(\frac{\tau^{d'}}{s^{h'}}\right);
   \]
3. if it lies above the forcing, the Keller identity is impossible;
4. if it has exactly the forcing weight, the apparent scalar
   coincidence is also impossible: polynomiality makes the required
   Wronskian monomial one degree too high.

Thus every strict compact face that can occur is a common polynomial
deformation of the repeated local factor \(s^e\).  Unlike the
squarefree case, \(C\) can have degree greater than one and can split
the repeated factor.  The slope-\(g/e\) resonant face remains
unclassified.

## 1. Local bracket and a general \(Q\)-coset

More explicitly, at a root \(\alpha\) of multiplicity \(e\), write
\[
R=(X-\alpha)^e u(X),\qquad u(\alpha)\ne0.
\]
Choose the unique normalized formal \(e\)-th root of the unit and set
\[
s=(X-\alpha)u(X)^{1/e}\in\mathbb C[[X-\alpha]].
\]
Then \(R=s^e\) and \(ds/dX\) is a unit.  The inverse formal coordinate
exists, so polynomial \(X\)-coefficients have expansions with integral
nonnegative \(s\)-orders.  In this coordinate, write
\[
R=s^e,\qquad P(0,s)=s^p,\qquad Q(0,s)=s^q.
\]
The change from \(X\) to \(s\) multiplies the local bracket by a unit.
Consequently the local right side is a unit times
\(-c\tau^N\), whose initial weight is the weight of \(\tau^N\).

Let
\[
P_0=s^pA(z),\qquad
z=\frac{\tau^{d'}}{s^{h'}},
\qquad A(0)=1,
\tag{1}
\]
where \(\gcd(d',h')=1\).  Give \(s,\tau\) weights \(d',h'\).
A \(Q\)-face in one lattice coset has the form
\[
Q_{u,v}=\tau^u s^vB(z),\qquad B(0)\ne0,
\tag{2}
\]
and has weight
\[
w=h'u+d'v.
\tag{3}
\]
Set
\[
\gamma=\frac ge,\qquad
\Delta=d'-\gamma h',\qquad
L=u+\gamma v-m.
\tag{4}
\]
Direct differentiation gives the exact local formula
\[
\boxed{
\begin{aligned}
\mathscr K(P_0,Q_{u,v})
=\tau^u s^{p+v-1}\bigl(
&pL\,AB
+p\Delta z\,AB'\\
&+(mh'-w)z\,A'B
\bigr).
\end{aligned}
}
\tag{5}
\]
Here \(pL=pu+nv-mp\), so (5) is integral even when \(e\nmid g\).
The constant coefficient of the polynomial in parentheses is
\[
pL\,A(0)B(0).
\tag{6}
\]

## 2. The lowest \(Q\)-face is automatically matched

Suppose that the actual \(Q\) had a lowest face of weight
\[
w<qd'.
\tag{7}
\]
The bracket of this face with \(P_0\) has weight
\[
(p-1)d'+w.
\tag{8}
\]
It is the lowest possible left-side weight.  If its Euler defect
\(L\) were nonzero, (6) would give a nonzero term
\[
\tau^u s^{p+v-1}.
\]
This cannot disappear into the scalar right side even if (8) happens
to equal \(h'N\), because \(p+v-1>0\).  If (8) is below or above
\(h'N\), it is likewise incompatible with the Keller identity.
Therefore \(L=0\).

But \(L=0\) gives
\[
u=\gamma(q-v)
\]
and hence, at the strict slope \(\Delta<0\),
\[
\begin{aligned}
w
&=h'\gamma(q-v)+d'v\\
&=qd'+(q-v)(\gamma h'-d')\\
&\ge qd',
\end{aligned}
\tag{9}
\]
contrary to (7).  Thus no \(Q\)-face lies below \(s^q\).

All integer points on the weight-\(qd'\) line belong to one lattice
coset because \(\gcd(d',h')=1\).  Since \(s^q\) is present at
\(\tau=0\), the entire face is
\[
\boxed{
Q_0=s^qB(z),\qquad B(0)=1.
}
\tag{10}
\]
As in the squarefree bridge, all adjacent faces have strictly greater
weight and cannot enter the initial bracket.

## 3. The matched compact bracket

Substituting \(u=0,v=q,w=qd'\) into (5) gives
\[
\boxed{
\mathscr K(P_0,Q_0)
=\Delta s^{p+q-1}z
\left(pAB'-qA'B\right).
}
\tag{11}
\]
The face weight is
\[
W_{\rm face}=(p+q-1)d',
\]
whereas the local scalar forcing has weight \(h'N\).  Put
\[
\begin{aligned}
\mathcal D
&=h'N-(p+q-1)d'\\
&=(p+q-1)(\gamma h'-d')
  +(\gamma-2)h'.
\end{aligned}
\tag{12}
\]
The second expression exhibits the new repeated-root phenomenon:
\(\gamma=g/e\) can be less than \(2\).

If \(\mathcal D<0\), the scalar right side has smaller weight than
every left-side term, so the Keller identity is impossible.

If \(\mathcal D>0\), (11) lies below the forcing and must vanish.
Since \(\Delta\ne0\),
\[
pAB'-qA'B=0.
\tag{13}
\]
Thus
\[
B^p=A^q.
\]
Because \(\gcd(p,q)=e\), unique factorization and the normalized
constant terms give
\[
\boxed{
A=C^a,\qquad B=C^b.
}
\tag{14}
\]
If \(k=\deg C\), local polynomiality gives \(kh'\le e\), and the
face becomes
\[
\boxed{
P_0=
\left[
s^eC\!\left(\frac{\tau^{d'}}{s^{h'}}\right)
\right]^a,
\qquad
Q_0=
\left[
s^eC\!\left(\frac{\tau^{d'}}{s^{h'}}\right)
\right]^b.
}
\tag{15}
\]
The expression in square brackets is polynomial on the face:
\[
s^eC(z)
=\sum_{j=0}^{k}c_j\tau^{d'j}s^{e-h'j}.
\tag{16}
\]
This is the precise repeated-factor analogue of the linear shift in
the squarefree theorem.

## 4. Exact forcing-weight coincidence cannot supply the scalar

It remains to treat \(\mathcal D=0\), rather than assuming that the
face vanishes.  Write
\[
S=a+b,\qquad
\Lambda=p+q-1=eS-1.
\]
Weight equality gives
\[
\frac{d'}{h'}=\frac{N}{\Lambda}.
\]
In lowest terms,
\[
t=\gcd(N,\Lambda),\qquad
d'=\frac Nt,\qquad
h'=\frac{\Lambda}{t}.
\tag{17}
\]
This ratio is strict precisely when
\[
\frac N\Lambda<\frac ge
\quad\Longleftrightarrow\quad
2e>g.
\tag{18}
\]

A monomial \(z^j\) in the outer factor
\[
z\left(pAB'-qA'B\right)
\]
is scalar in \(s\) only when
\[
\Lambda-h'j=0.
\]
By (17), this requires
\[
j=t.
\tag{19}
\]
Therefore the Wronskian
\[
W(z)=pAB'-qA'B
\]
would need a nonzero \(z^{t-1}\)-coefficient.

Polynomiality gives
\[
\deg A\le\left\lfloor\frac p{h'}\right\rfloor,
\qquad
\deg B\le\left\lfloor\frac q{h'}\right\rfloor.
\tag{20}
\]
These two bounds miss the required degree by exactly one.  Indeed,
\[
t\mid eN-g\Lambda=g-2e,
\tag{21}
\]
while \(t h'=\Lambda=eS-1\).  Hence
\[
\gcd(t,e)=\gcd(h',e)=1.
\]
Since \(e\le g<2e\), equation (21) gives \(t\le2e-g\le e\);
as \(e>1\), coprimality forces \(t<e\), and therefore
\[
h'=\frac{eS-1}{t}>S.
\tag{22}
\]

Now
\[
\frac p{h'}+\frac q{h'}=t+\frac1{h'}.
\]
The sum of the floors in (20) could equal \(t\) only if
\[
p\bmod h'\in\{0,1\}.
\]
The first case would imply \(h'\mid a\), because
\(\gcd(h',e)=1\); the second would imply \(h'\mid b\), after
subtracting \(ae\equiv1\pmod{h'}\) from
\(eS\equiv1\pmod{h'}\).  Both contradict (22).  Consequently
\[
\boxed{
\left\lfloor\frac p{h'}\right\rfloor+
\left\lfloor\frac q{h'}\right\rfloor=t-1.
}
\tag{23}
\]
It follows that
\[
\deg W
\le\deg A+\deg B-1
\le t-2.
\tag{24}
\]
The required \(z^{t-1}\)-coefficient does not exist.  Thus the
weight-coincident compact bracket cannot equal the nonzero Keller
scalar.

The first small arithmetic coincidence for which a nonconstant
\(P\)-face fits locally is
\[
(g,e,a,b)=(5,4,3,4).
\]
Here
\[
N=33,\quad \Lambda=27,\quad
t=3,\quad(d',h')=(11,9).
\]
Both \(A\) and \(B\) have degree at most one, so
\(zW(z)\) has degree at most two, while the scalar would require
\(z^3\).  This is an exact near-miss, not a surviving scalar face.

## 5. Scope

For a repeated root, every strict first compact face of an actual
polynomial Keller pair must satisfy \(\mathcal D>0\), and is therefore
the common local-factor deformation (15).  There is no exceptional
strict scalar face at \(\mathcal D=0\).

This is a local theorem.  It does not yet glue the deformations of
different repeated factors into one global polynomial approximate
root.  It also does not classify:

* the resonant slope \(d'/h'=g/e\), where \(\Delta=0\);
* interactions after a repeated factor splits; or
* noncompact formal faces.
