# Two adjacent boundary valuations do not force Darboux-product descent

Date: 25 July 2026

## Audited conclusion

Let
\[
J=\Xi^5T^N=\frac{Z^5}{W^2},\qquad N=5m+2,
\]
be the reciprocal Darboux product of the normalized comparison branch.
Two adjacent boundary valuations can prove descent only after a separate
**support-exhaustion theorem** says that every zero and pole of every
quotient
\[
\frac{\sigma J}{J}
\]
is carried by those two divisors.  With that extra hypothesis the proof
is immediate.  Without it, even the genuine reciprocal endpoint,
exact symplecticity, polynomial original-plane support, a normalized
identity branch at both adjacent valuations, and nonzero lower support
terms do not force the divisor of \(J\) to be Galois invariant.

The countermodel below is global and exact.  It is obtained from the
genuine endpoint map by an affine symplectic target transformation.  Its
failure of descent is certified without coefficient elimination: the
high-contact cusp branch divisor has an infinite target orbit.

This countermodel is deliberately not claimed to satisfy the complete
GGHV five-block or case-c Newton polygons.  It contains a constant
vertex in each coordinate and a full subleading transverse block in the
second coordinate, but it does not contain the particular forced inner
cap vertices of a reduced Keller pair.  Consequently the exact positions
and degrees of those cap vertices remain a possible source of a genuine
global support-exhaustion theorem.  What is ruled out here is any argument
using only two adjacent orders, their normalized local branches, and the
mere presence of lower support.

Work over an algebraically closed field \(k\) of characteristic zero.
Put
\[
p=2m+1,\qquad q=3m+1,\qquad N=5m+2
\tag{1}
\]
and take a genuine reciprocal endpoint
\[
P_0=\xi^2A(t),\qquad Q_0=\xi^3B(t),
\tag{2}
\]
where
\[
\deg A=p,\quad\deg B=q,\quad
A(0)B(0)[t^p]A[t^q]B\ne0,
\tag{3}
\]
\[
3A'B-2AB'=t^{N-1}.
\tag{4}
\]
As before,
\[
dP_0\wedge dQ_0=-\xi^4t^{N-1}\,d\xi\wedge dt.
\tag{5}
\]

## 1. The exact positive statement

Let \(M/K\) be the finite comparison extension, let
\(\widetilde M/K\) be a normal closure with group \(G\), and choose a
common normal projective \(G\)-model.  Let \(D_1,D_2\) be two prime
divisors on it.

> **Two-boundary support criterion.**  Suppose that for every
> \(\sigma\in G\)
> \[
> \operatorname{Supp}\operatorname{div}\left(\frac{\sigma J}{J}\right)
> \subseteq D_1\cup D_2
> \tag{6}
> \]
> and
> \[
> \operatorname{ord}_{D_i}\left(\frac{\sigma J}{J}\right)=0
> \quad(i=1,2).
> \tag{7}
> \]
> Then the comparison branch descends to \(K\).

Indeed, (6)--(7) give
\[
\operatorname{div}(\sigma J/J)=0.
\]
Thus
\[
\sigma\operatorname{div}(J)=\operatorname{div}(J)
\]
for every \(\sigma\).  The divisor-invariance section theorem in
`GLOBAL_DARBOUX_DIVISOR_SECTION_AUDIT.md` then gives
\[
\Xi,T,Z,W\in K.
\]

Adjacency is not used in this last step.  Its possible role is geometric:
the forced Newton vertices might conceivably prove (6) by showing that
the two adjacent boundary components exhaust all zeros and poles.  The
orders in (7), by themselves, contain no such information.

## 2. An affine symplectic endpoint deformation

Choose
\[
a,c\in k^\times,\qquad d\in k
\]
and let
\[
\tau(p,q)=(p+a,\ q+cp+d).
\tag{8}
\]
Its Jacobian is one.  Define
\[
P=P_0+a,\qquad Q=Q_0+cP_0+d.
\tag{9}
\]
Then
\[
dP\wedge dQ=dP_0\wedge dQ_0.
\tag{10}
\]

Let \((X,T)\) be the comparison branch selected at reciprocal infinity:
\[
P_0(X,T)=P,\qquad Q_0(X,T)=Q.
\tag{11}
\]
Set
\[
\epsilon=\xi^{-1},\qquad r=X/\xi.
\]
Equations (11) become
\[
\begin{aligned}
r^2A(T)&=A(t)+a\epsilon^2,\\
r^3B(T)&=B(t)+c\epsilon A(t)+d\epsilon^3.
\end{aligned}
\tag{12}
\]
At fixed \(t\ne0\), the implicit determinant at
\((r,T,\epsilon)=(1,t,0)\) is
\[
\det
\begin{pmatrix}
2A&A'\\
3B&B'
\end{pmatrix}
=-t^{N-1}.
\tag{13}
\]
Thus (12) has the usual unique normalized solution
\[
r=1+O(\epsilon),\qquad T=t+O(\epsilon).
\tag{14}
\]

## 3. The branch is normalized at two adjacent corner valuations

The point \(t=0\) is precisely where (13) degenerates, so ordinary
fixed-\(t\) implicit-function theory does not justify a corner claim.
The exact high-contact quotient does.

Put
\[
R(t)=\frac{B(t)^2}{A(t)^3}.
\tag{15}
\]
Equation (4) gives
\[
R'(t)=-\frac{t^{N-1}B(t)}{A(t)^4}.
\tag{16}
\]
Writing
\[
L=R(0),\qquad
\kappa=-\frac{B(0)}{N A(0)^4}\ne0,
\]
one has
\[
R(t)=L+\kappa t^N+O(t^{N+1}).
\tag{17}
\]

Eliminate \(r\) from (12), write \(T=tu\), and set
\[
\delta=\frac{\epsilon}{t^N}.
\tag{18}
\]
The resulting equation is
\[
R(tu)=
\frac{\bigl(B(t)+c\epsilon A(t)+d\epsilon^3\bigr)^2}
     {\bigl(A(t)+a\epsilon^2\bigr)^3}.
\tag{19}
\]
After substituting \(\epsilon=\delta t^N\), divide (19) minus \(R(t)\)
by \(t^N\).  Both sides are regular in \(k[[t,\delta,u-1]]\).  At
\(t=0\) they are respectively
\[
\kappa(u^N-1)
\quad\text{and}\quad
\frac{2cB(0)}{A(0)^2}\delta.
\tag{20}
\]
The derivative of the left side with respect to \(u\) at
\((u,\delta)=(1,0)\) is \(N\kappa\ne0\).  Formal implicit-function
theory therefore gives a unique solution
\[
u=1+O(\delta).
\tag{21}
\]
The first equation of (12), taking the square root with residue one,
then gives
\[
r=1+O(\delta).
\tag{22}
\]

For a monomial divisorial valuation \(v_{\rho,s}\) with
\[
v(\epsilon)=\rho,\qquad v(t)=s>0,
\]
conditions (21)--(22) give a normalized identity branch whenever
\[
\rho>Ns.
\tag{23}
\]
More strongly, for any integer \(\ell\ge1\), take the two primitive rays
\[
v_\ell(\epsilon,t)=(N+\ell,1),\qquad
v_{\ell+1}(\epsilon,t)=(N+\ell+1,1).
\tag{24}
\]
Their determinant is \(-1\), so they are adjacent rays in a smooth
toric boundary fan.  Their orders of \(\delta\) are respectively
\(\ell,\ell+1\).  At both,
\[
v_i(T/t-1)>0,\qquad v_i(X/\xi-1)>0,
\tag{25}
\]
Consequently
\[
\frac{J_{\rm branch}}{J_{\rm source}}
=\frac{X^5T^N}{\xi^5t^N}
=r^5u^N
=1+O(\delta)
\tag{26}
\]
is a unit with residue one at both divisors.  By increasing \(\ell\),
the affine deformation is invisible to arbitrarily high prescribed
valuation order on a pair of adjacent rays.  In particular, the two
boundary orders of the Darboux product agree exactly.

These are also adjacent divisorial valuations in the original
\((x,y)\)-plane.  Since
\[
t=w^{-1},\quad \epsilon=(zw^m)^{-1},\quad
z=xy,\quad w=xy^2,
\tag{27}
\]
the two valuation vectors are
\[
\begin{aligned}
v_\ell(x,y)&=(-8m-3-2\ell,\ 4m+1+\ell),\\
v_{\ell+1}(x,y)&=(-8m-5-2\ell,\ 4m+2+\ell),
\end{aligned}
\tag{28}
\]
again with determinant \(-1\).

## 4. Global monodromy still moves the divisor of \(J\)

The endpoint map \(F_0=(P_0,Q_0)\) is generically finite.  Indeed,
\(R(t)=Q_0^2/P_0^3\) is nonconstant by (16), so it recovers \(t\)
up to a finite extension, after which \(\xi\) is finite over the target
field.

The divisor \(t=0\) is ramified with transverse index \(N\), and its
image is the cusp
\[
C_0:\quad q^2=Lp^3,\qquad
L=\frac{B(0)^2}{A(0)^3}.
\tag{29}
\]
Suppose the selected branch (11) were rational.  It would give a
dominant rational self-map \(H\) satisfying
\[
F_0\circ H=\tau\circ F_0.
\tag{30}
\]
The image of the induced embedding of \(k(\xi,t)\) has the same degree
over \(k(P_0,Q_0)\) as the whole field, so the embedding is surjective.
Thus \(H\) is birational and gives a semilinear automorphism of the
finite endpoint extension.  In particular, \(\tau\) must permute its
finite branch-divisor set.

But
\[
\tau^j(0,0)
=\left(ja,\ jd+\frac{ca\,j(j-1)}2\right).
\tag{31}
\]
The cusp \(\tau^j(C_0)\) is singular at this point.  Since \(a\ne0\),
these points, and hence these cusp curves, are pairwise distinct as
\(j\) varies.  The branch-divisor set would contain an infinite orbit,
a contradiction.

Therefore the selected comparison branch is not rational.  By the
divisor-invariance section theorem,
\[
\boxed{\operatorname{div}(J)\ \text{is not \(G\)-invariant}.}
\tag{32}
\]
Equations (24)--(26) show exactly where the missing divisor information
lives: it is supported away from the two visible adjacent boundary
components.

## 5. Polynomial support and the role of the inner vertices

Return to the original plane through
\[
z=xy,\qquad w=xy^2,\qquad
t=w^{-1},\qquad \xi=zw^m.
\tag{33}
\]
If
\[
U(w)=w^pA(w^{-1}),\qquad
V(w)=w^qB(w^{-1}),
\]
then
\[
P_0=\frac{z^2U(w)}w,\qquad
Q_0=\frac{z^3V(w)}w.
\tag{34}
\]
Every monomial in (34) is polynomial in \(x,y\), and (9) is therefore
a polynomial pair satisfying
\[
[P,Q]_{x,y}=x^2.
\tag{35}
\]

The deformation has genuine lower support:

- \(a\) and \(d\) give nonzero constant vertices;
- \(cP_0\) gives a complete transverse-\(z^2\) block in \(Q\), strictly
  below the transverse-\(z^3\) endpoint block;
- the two endpoint coefficients of this subleading block are nonzero by
  (3).

Thus the obstruction is not an artifact of an outer homogeneous pair
with no lower terms.  Nevertheless this is only an **inner-block
analogue**.  In the GGHV five-block coordinates, the required
transverse-\(z^2\) block of \(Q\) starts at \(w^0\), whereas \(cP_0\)
contains the \(w^{-1}\) endpoint.  The required high \(z^0\) cap vertices
in both coordinates are also absent.  Those exact support conditions are
stronger than the hypotheses of this countermodel.

## Strategic consequence

The hoped-for statement
\[
\text{two adjacent normalized boundary valuations}
\Longrightarrow
\operatorname{div}(J)\text{ is \(G\)-invariant}
\]
is false, even with the genuine endpoint and exact symplectic equation.
The viable replacement is:

> Prove from the **complete forced inner Newton caps** that every prime in
> \(\operatorname{div}(\sigma J/J)\) lies on the two controlled boundary
> components.  Then apply the two-boundary support criterion.

This identifies the missing global input precisely.  Local valuation
matching, even at adjacent rays, cannot replace support exhaustion.

The identities, adjacent-ray arithmetic, original-plane polynomiality,
and cusp-orbit formulas are checked by
`verify_two_boundary_divisor_orbit.py`.
