# Endpoint forcing can be invisible on every normalization branch

Date: 26 July 2026

## Outcome

The affine endpoint pairing in the homogenized Keller identity can be
nonzero while the branch coefficient
\[
[t^{em}]\left(\frac{\tau^N}{P_X}\Big|_\gamma\right)
\]
vanishes on every normalization branch at the common-root boundary.
Thus the endpoint pairing must be quotiented before a branch-resonance
or pole-filtered monodromy argument can begin.

This is a local compatibility theorem, not a standard-system or Keller
countermodel.  The model below has earlier cross terms between its
common-root leading powers and its affine tails.  The unresolved
nilpotent cascade would have to cancel those terms in a genuine
standard-system solution.

## 1. The reciprocal affine tails

Let
\[
n=ga,\qquad m=gb,\qquad N=m+n-2,
\]
where \(g\ge2\) and \(a,b\ge2\).  Let \(R\in k[X]\) be monic,
squarefree, and of degree \(g\).  For affine forms
\[
L_p(X)=uX+v,\qquad L_q(X)=sX+t,
\]
put
\[
\begin{aligned}
P(X,\tau)&=R(X)^a+\tau^{n-1}L_p(X),\\
Q(X,\tau)&=R(X)^b+\tau^{m-1}L_q(X).
\end{aligned}
\tag{1}
\]
Both affine tails exactly obey the reciprocal degree bounds.

Write the homogenized Keller bracket as
\[
\mathcal K(P,Q)
=\tau(P_XQ_\tau-P_\tau Q_X)+nPQ_X-mQP_X.
\tag{2}
\]
Its part bilinear in the two affine tails is
\[
\boxed{
\mathcal K\!\left(\tau^{n-1}L_p,\tau^{m-1}L_q\right)
=(sv-ut)\tau^N.
}
\tag{3}
\]
Indeed, the coefficient before simplification is
\[
u(m-1)L_q-s(n-1)L_p+nsL_p-muL_q
=sL_p-uL_q=sv-ut.
\]
Hence this contribution is nonzero exactly when the two original
affine-linear forms
\[
ux+vy,\qquad sx+ty
\]
have nonzero Jacobian \(ut-vs\).  The sign in (3) agrees with the
negative endpoint pairing in the reciprocal convention.

## 2. Newton--Puiseux calculation

Fix a root \(\alpha\) of \(R\), put \(r=R'(\alpha)\ne0\), and assume
\[
\ell=L_p(\alpha)=u\alpha+v\ne0.
\tag{4}
\]
Writing \(S=X-\alpha\), the lowest Newton edge of \(P=0\) is
\[
r^aS^a+\ell\tau^{n-1}.
\tag{5}
\]
Since
\[
\gcd(a,n-1)=\gcd(a,ga-1)=1,
\]
the Newton edge is irreducible and gives one normalization branch with
ramification index \(e=a\).  With \(\tau=t^a\), it has a
parametrization
\[
S=c\,t^{n-1}+\text{higher terms},
\qquad
r^ac^a+\ell=0.
\tag{6}
\]
The \(a\) choices of \(c\) are equivalent under
\(t\mapsto\zeta t\), \(\zeta^a=1\).  They describe the \(a\) generic
sheets of this single ramified branch, not \(a\) distinct
normalization branches.

Along this branch,
\[
P_X
=aR^{a-1}R'+u\tau^{n-1}
=a r^a c^{a-1}t^{(a-1)(n-1)}
+\text{higher terms}.
\tag{7}
\]
The displayed coefficient is nonzero, and the affine derivative term
has the strictly larger order \(a(n-1)\).  Therefore
\[
\begin{aligned}
\operatorname{ord}_t\frac{\tau^N}{P_X}
&=aN-(a-1)(n-1)\\
&=am+(n-a-1)\\
&=am+\bigl(a(g-1)-1\bigr)
>am.
\end{aligned}
\tag{8}
\]
It follows that
\[
\boxed{
[t^{am}]
\left(\frac{\tau^N}{P_X}\Big|_\gamma\right)=0
}
\tag{9}
\]
on every branch specializing to \(\alpha\).

If \(\gcd(R,L_p)=1\), condition (4) holds at every root of \(R\).
There is one ramified normalization branch over each of the \(g\)
root clusters, and its \(a\) generic sheets account for all
\(n=ga\) roots of \(P\) over a generic \(\tau\).  Consequently (9)
holds on each of the \(g\) normalization branches even when
\(sv-ut\ne0\), so the endpoint contribution (3) is nonzero.

## 3. Scope

The full bracket of (1) is not the scalar in (3).  It also contains
terms of orders \(\tau^{n-1}\) and \(\tau^{m-1}\) obtained by pairing
one common-root leading power with the opposite affine tail.  Thus
(1) does not solve the retained standard equations and is not a
Keller pair.

What (3)--(9) prove is narrower and useful: ordinary normalization-
branch residues cannot detect the affine endpoint pairing, even
branch by branch and even when that pairing is nonzero.  A valid
pole-filtered monodromy lemma must first quotient this endpoint class,
as well as the honest \(g\)-multiple approximate-root action.  The
remaining problem is global: determine whether the nilpotent normal
cascade can cancel the earlier cross terms compatibly across all root
clusters.

The accompanying exact arithmetic check is
`verify_standard_system_endpoint_pairing_branch_invisibility.py`.
