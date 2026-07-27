# Why the endpoint-invisible quotient has no standalone obstruction

Date: 26 July 2026

## Outcome

The relative-log transport equation and normalization-branch residues
do not, by themselves, produce a nonzero finite-dimensional endpoint
obstruction after the affine endpoint-invisible terms are quotiented.
There is an exact dichotomy.

1. If every affine endpoint pairing is declared invisible, its image
   is the whole one-dimensional endpoint forcing space.  The quotient
   is zero, so it also kills the Keller forcing.
2. If only pairings coming from lower-order infinitesimal solutions
   are quotiented, no nonzero pure affine tail is available: every
   such tail already has a nonzero earlier cross term with the
   common-root leading powers.

Therefore the admissible endpoint quotient depends on whether those
earlier cross terms can be lifted through the nilpotent normal
cascade.  Determining that liftability is the unresolved
branch-resonance problem itself; branch residues do not turn it into
a smaller endpoint-only calculation.

This is a no-go theorem for a particular proof strategy, not a
Jacobian-conjecture result.

## 1. Exact three-layer bracket

Let
\[
n=ga,\qquad m=gb,\qquad N=m+n-2,
\]
with \(g,a,b\ge2\) and \(n<m\), equivalently \(a<b\), and let \(R\)
be monic and squarefree of degree \(g\).  For
\[
L_p=uX+v,\qquad L_q=sX+t,
\]
put
\[
P=R^a+\tau^{n-1}L_p,\qquad
Q=R^b+\tau^{m-1}L_q.
\tag{1}
\]
For the homogenized bracket
\[
\mathcal K(P,Q)
=\tau(P_XQ_\tau-P_\tau Q_X)+nPQ_X-mQP_X,
\tag{2}
\]
direct differentiation gives the exact decomposition
\[
\begin{aligned}
\mathcal K(P,Q)
={}&
b\tau^{n-1}R^{b-1}
\bigl(R'L_p-gR L_p'\bigr)\\
&+
a\tau^{m-1}R^{a-1}
\bigl(gR L_q'-R'L_q\bigr)\\
&+
(sv-ut)\tau^N.
\end{aligned}
\tag{3}
\]
There are no other terms.

The last line is the endpoint pairing
\[
\omega(L_p,L_q)=sv-ut.
\tag{4}
\]
It is surjective onto \(k\): for example,
\[
L_p=1,\qquad L_q=cX
\quad\Longrightarrow\quad
\omega(L_p,L_q)=c.
\tag{5}
\]

On the other hand, neither earlier linear map has a nonzero affine
kernel.  If
\[
R'L-gRL'=0
\tag{6}
\]
for a nonzero affine polynomial \(L\), then:

- if \(L\) is constant, (6) contradicts \(R'\ne0\);
- if \(L\) is nonconstant, (6) gives
  \(R'/R=gL'/L\), hence \(R=cL^g\), contradicting squarefreeness.

The sign-reversed equation has the same conclusion.  Thus
\[
\ker\bigl(L\mapsto R'L-gRL'\bigr)
\cap k[X]_{\le1}=0.
\tag{7}
\]
The affine tails producing (4) are not cycles of the first
lower-order deformation equation.

## 2. The branch map kills the entire endpoint space

Assume \(\gcd(R,L_p)=1\).  The endpoint-invisibility theorem proves,
on every normalization branch \(\gamma\) of \(P=0\) over \(\tau=0\),
\[
[t^{e_\gamma m}]
\left(\frac{\tau^N}{P_X}\Big|_\gamma\right)=0.
\tag{8}
\]
Multiplying the constant endpoint forcing by any scalar does not
change this conclusion.  Hence the branch-residue map on the endpoint
space is
\[
\rho_P:k\,\tau^N
\longrightarrow
\bigoplus_{\gamma\mid\tau=0}k,
\qquad
\rho_P=0.
\tag{9}
\]

Equations (5) and (9) give
\[
\frac{k\,\tau^N}{\operatorname{im}\omega}=0.
\tag{10}
\]
This is true branch by branch, before taking traces, cluster sums, or
monodromy invariants.  Consequently no representation-theoretic
refinement of the zero vector in (9) can recover the scalar forcing.

## 3. Why the relative-log PDE does not repair the quotient

Let
\[
p=\log P,\qquad q=\log Q,\qquad
\ell=aq-bp.
\]
The exact relative-log equation is
\[
\tau\left(p_X\ell_\tau-p_\tau\ell_X\right)
+ag\,\ell_X
=-\frac{ac\,\tau^N}{PQ}.
\tag{11}
\]
Put
\[
A=\frac{L_p}{R^a},\qquad
B=\frac{L_q}{R^b},\qquad
d=n-1,\quad e=m-1.
\tag{12}
\]
The part of the left side of (11) bilinear in \(A\) and \(B\), at
order \(d+e=N\), is
\[
\boxed{
\mathfrak e_R(L_p,L_q)
=a\bigl(eA'B-dAB'\bigr).
}
\tag{13}
\]
Equivalently,
\[
\mathfrak e_R
=\frac{a}{R^{a+b}}
\left(
(m-1)L_p'L_q
-(n-1)L_pL_q'
+(a-b)\frac{R'}R L_pL_q
\right).
\tag{14}
\]
This is not determined by the scalar \(\omega(L_p,L_q)\).  It retains
the lower-order extension data, including the rootwise pole term in
(14).  Algebraically, it incorporates the contributions obtained
when the earlier two lines of (3) are divided by \(PQ\) and expanded.

Thus quotienting only the raw last line of (3) is not compatible with
the transport equation.  To decide whether a given endpoint pairing
is removable, one must first choose higher jets that cancel the first
two lines of (3), then recompute their induced contribution at order
\(N\).  Different lifts can change that contribution.

## 4. The exact remaining finite-dimensional problem

The standard system is finite, so one can package a coarse linearized
shadow of the unresolved question as a finite obstruction quotient,
but doing so does not reduce its content.  Let \(\mathcal L\) denote
the set of lower jets through order \(N-1\) satisfying all reciprocal
equations through that order.  For a lower jet
\(\eta\in\mathcal L\), let
\[
\operatorname{ob}_N(\eta)\in k\,\tau^N
\tag{15}
\]
be the scalar endpoint projection of the order-\(N\) bracket left
after its lower equations have been solved.  One possible linearized
quotient is
\[
\frac{k\,\tau^N}
{\operatorname{span}_k\{\operatorname{ob}_N(\eta)-\operatorname{ob}_N(\eta'):
\eta,\eta'\in\mathcal L
\text{ have the same reduced boundary data}\}}.
\tag{16}
\]

Formula (3) shows that the affine endpoint pairing cannot be inserted
in the denominator of (16) without a lift in \(\mathcal L\).
Formula (13) shows that its contribution after a lift is not the raw
scalar (4).  Constructing or excluding such lifts is exactly the
non-\(g\), \(Z=0\) nilpotent cascade.

The quotient (16) is only a coarse shadow: membership of the Keller
scalar in the span of endpoint differences is not equivalent to its
being an actual value of the generally nonlinear map
\(\operatorname{ob}_N:\mathcal L\to k\tau^N\).  The actual image, not
only its linear span, is what must be classified.

Accordingly, a finite-dimensional endpoint obstruction exists only
after the following genuinely new input:

> **Lifted endpoint lemma.**  Classify the endpoint values
> \(\operatorname{ob}_N(\eta)\) of lower-order nilpotent lifts
> \(\eta\in\mathcal L\), root cluster by root cluster, and prove that
> the Keller scalar \(-c\tau^N\) is not among them.

Without this lemma, quotienting endpoint-invisible terms either
annihilates the entire forcing space, as in (10), or merely renames
the original nilpotent-cascade problem as (16).

The accompanying exact identities are checked by
`verify_standard_system_endpoint_quotient_no_go.py`.
