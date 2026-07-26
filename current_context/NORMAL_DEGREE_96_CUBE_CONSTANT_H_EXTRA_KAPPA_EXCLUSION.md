# The constant-\(h\) cube chart with an extra upper coefficient is impossible

Date: 26 July 2026

## Outcome

Work in the cube chart of
`NORMAL_DEGREE_96_CUBE_LAURENT_TIME_REDUCTION.md`, with \(r\) a
nonzero constant:
\[
 g=w^6+aw^4+bw^3+cw^2+dw+q,
\qquad
 f=(\Phi(g^{1/6}))_+,
\]
where
\[
 \Phi(S)=S^9+\kappa _8S^8+\kappa _7S^7+\kappa _5S^5
 +\kappa _4S^4+jS^3+\kappa _2S^2+\kappa _1S .
\]
Let \(A_1,\ldots,A_5\) be the Laurent coefficients defined there.
The Keller equations are
\[
 A_1'=A_2'=A_3'=A_4'=0,\qquad
 6A_5'=\lambda/r\ne0.
\tag{1}
\]
Thus \(A_1,\ldots,A_4\) are constant and \(A_5\) is affine of
degree exactly one.

This note proves:

> **Extra-\(\kappa\) theorem.**  There is no polynomial solution of
> (1) for which at least one of
> \[
> \kappa _8,\kappa _7,\kappa _5,\kappa _4,\kappa _2,\kappa _1
> \tag{2}
> \]
> is nonzero.

Together with
`NORMAL_DEGREE_96_CUBE_CONSTANT_H_ONLY_J_EXCLUSION.md`, this excludes
the full constant-\(h\) cube chart, with all seven upper constants
allowed.  It does not exclude the remaining nonconstant pure-power
\(r\) chart and is not a proof of the plane Jacobian conjecture.

## 1. Centered variables and weights

Put
\[
 C=c-\frac{a^2}{4},\qquad
 D=d-\frac{ab}{2},\qquad
 Q=q-\frac{b^2}{4}.
\tag{3}
\]
Use the natural weights
\[
 \operatorname {wt}(a,b,C,D,Q)=(2,3,4,5,6),
\qquad
 \operatorname {wt}(\kappa_k)=9-k.
\tag{4}
\]
Then \(A_\ell\) has weight \(9+\ell\).

Set all seven upper constants to zero.  The terms quadratic in
\((C,D,Q)\) are \(N_\ell\):
\[
\begin{aligned}
N_1={3\over16}(C^2a-4CQ-2D^2),\qquad
N_2={3\over16}(C^2b+2CDa-4DQ),\\
N_3=-{1\over16}
 (C^2a^2-6CDb-4CQa-2D^2a+6Q^2),\\
N_4=-{1\over32}
 (3C^2ab+2CDa^2-8CQb-4D^2b-4DQa),\\
N_5={1\over192}
 (C^2a^3-6C^2b^2-12CDab-4CQa^2-2D^2a^2+24DQb).
\end{aligned}
\tag{5}
\]
The cubic transverse terms are
\[
H=(H_1,\ldots,H_5)
=\left(0,0,{C^3\over16},{3C^2D\over16},
-{C(C^2a-2CQ-4D^2)\over32}\right).
\tag{6}
\]
There are no higher transverse terms in the four conserved
coefficients.

## 2. The complete pure boundary

The pure weighted leading equations have exactly two projective
strata.  Indeed, on \(A_1=A_2=0\),
\[
A_4+\frac b3A_1+\frac a6A_2=\frac{3}{16}C^2D.
\tag{7}
\]
If \(C=0\), the first and third equations successively give
\(D=Q=0\).  If \(C\ne0\), (7) gives \(D=0\), and the remaining
equations give
\[
b=0,\qquad C=\frac{3a^2}{8},\qquad Q=\frac{3a^3}{32}.
\tag{8}
\]
Thus the two strata are
\[
\mathcal R:\ C=D=Q=0
\tag{9}
\]
and the cusp (8).  In uncentered coordinates the cusp is
\[
b=d=0,\qquad c=\frac{5a^2}{8},\qquad q=\frac{3a^3}{32}.
\]
Writing \(a=4v\), its terminal leading coefficient is
\[
A_5=-\frac{27}{2}v^7\ne0.
\tag{10}
\]
Its pole degree is \(14\rho\), where \(\rho>0\) is the weighted pole
scale.  Since \(2\rho=\deg a\) is a positive integer,
\(14\rho>1\), contradicting (1).  Only the perfect-square stratum
\(\mathcal R\) remains.

On \(\mathcal R\),
\[
g_0=\left(w^3+\frac a2w+\frac b2\right)^2.
\tag{11}
\]

## 3. First extra coefficient and the two projective charts

Let \(k_*\) be the greatest exponent in (2) having nonzero
coefficient, and put
\[
\delta=9-k_*\in\{1,2,4,5,7,8\}.
\tag{12}
\]
A constant dilation of the normalized \(w\)-coordinate makes
\(\kappa_{k_*}=1\).  This dilation is independent of the local
projectivization at coefficient infinity.

Let
\[
K_\ell^{(k_*)}
=\left.[\kappa_{k_*}]A_\ell\right|_{C=D=Q=0}.
\tag{13}
\]
These are exact polynomials in \(a,b\); in particular
\(K_3^{(k_*)}=0\) for all six cases.  The verifier reconstructs them
directly from the Laurent residues.

The weighted projective \((a,b)\)-line is covered over
\(\mathbf C\) by
\[
\mathcal U_a:\ a=1,\qquad
\mathcal U_b:\ a=0,\ b=1.
\tag{14}
\]
For each \(k_*\), exact Gröbner reduction gives
\[
\begin{array}{c|c|c|c|c}
k_*&\delta&
\langle K_1,K_2,K_3,K_4\rangle_{\mathcal U_a}&
\langle K_1,K_2,K_3,K_4\rangle_{\mathcal U_b}&
\langle N_1+K_1,\ldots,N_4+K_4,N_5+K_5\rangle
\\ \hline
8&1&[1]&[1]&[1]\text{ in both charts}\\
7&2&[1]&[1]&[1]\text{ in both charts}\\
5&4&[1]&[1]&[1]\text{ in both charts}\\
4&5&[1]&[1]&[1]\text{ in both charts}\\
2&7&[1]&[1]&[1]\text{ in both charts}\\
1&8&[1]&[1]&[1]\text{ in both charts}
\end{array}
\tag{15}
\]
All denominators are cleared before forming the ideals.  Thus (15)
consists of twenty-four exact unit-ideal certificates, twelve of which
are the balanced terminal certificates.

For example, in the \(k_*=8,a=1\) balanced four-equation fiber, one
lexicographic eliminant is
\[
270b^4-90b^2+1.
\tag{16}
\]
Adding the terminal leading coefficient makes the Gröbner basis
\([1]\).  The verifier computes every chart from (13), rather than
using a prerecorded eliminant.

## 4. Exhaustion of transverse pole profiles

Let
\[
\rho=\max\left\{
{\deg a\over2},{\deg b\over3},{\deg c\over4},
{\deg d\over5},{\deg q\over6}\right\}>0.
\tag{17}
\]
At a perfect-square boundary point define the first normalized
transverse deficit by
\[
\eta=\min\{4\rho-\deg C,\ 5\rho-\deg D,\
6\rho-\deg Q\}>0,
\tag{18}
\]
omitting a zero polynomial from the minimum.
The first pure transverse term has deficit \(2\eta\); the first extra
upper term has deficit \(\delta\rho\).

If \(2\eta>\delta\rho\), the first four equations require
\(K_1=\cdots=K_4=0\), contrary to the first two unit certificates in
(15).

If \(2\eta=\delta\rho\), their leading ideal is
\[
N_1+K_1=\cdots=N_4+K_4=0.
\tag{19}
\]
The terminal coefficient is \(N_5+K_5\), and the last column of
(15) says it is nonzero at every solution of (19).

It remains to justify that \(2\eta<\delta\rho\) cannot hide a
singular secondary arc.  The leading quadratic normal equations
\(N_1=\cdots=N_4=0\) have, besides the zero transverse vector, only
\[
a=-6v^2,\quad b=4v^3,\quad
(C,D,Q)=s(1,v,-2v^2),
\qquad s,v\ne0.
\tag{20}
\]
This follows directly from the first three equations: after setting
\(C=1\), they give
\[
Q=-2D^2,\qquad a=-6D^2,\qquad b=4D^3.
\]
The factorization behind (20) is
\[
\begin{aligned}
w^3+\frac a2w+\frac b2&=(w-v)^2(w+2v),\\
Cw^2+Dw+Q&=C(w-v)(w+2v).
\end{aligned}
\tag{21}
\]
Thus the secondary normal cone exposes a squarefree quadratic factor,
but it is still necessary to check the singular correction direction.

Normalize \(s=1\).  The Jacobian \(J=d(N_1,\ldots,N_4)\), with
columns ordered as \((a,b,C,D,Q)\), is
\[
J=\begin{pmatrix}
3/16&0&-3v^2/4&-3v/4&-3/4\\
3v/8&3/16&-3v^3/4&-3v^2/4&-3v/4\\
3v^2/8&3v/8&0&0&0\\
v^3/8&3v^2/16&v^5/4&v^4/4&v^3/4
\end{pmatrix}.
\tag{22}
\]
It has rank two and left kernel
\[
\ell_1=(2v^2,-2v,1,0),\qquad
\ell_2=(4v^3/3,-v^2,0,1).
\tag{23}
\]
The pure cubic vector is
\[
L=(0,0,1/16,3v/16).
\tag{24}
\]
For the six first-\(\kappa\) vectors \(K\), the determinants
\[
\det\begin{pmatrix}
\ell_1K&\ell_1L\\
\ell_2K&\ell_2L
\end{pmatrix}
\tag{25}
\]
are, in the order \(k_*=8,7,5,4,2,1\),
\[
-{6175v^{12}\over972},\
{2737v^{11}\over648},\
-{1235v^9\over648},\
{187v^8\over144},\
-{91v^6\over144},\
{11v^5\over24}.
\tag{26}
\]
They are all nonzero.

There is one more infinitesimal kernel direction beyond the two
tangent directions of the family (20).  Modulo those tangent
directions choose
\[
n=(4v^2,-4v^3,1,0,0).
\tag{27}
\]
Its quadratic self-interaction \(M\) satisfies
\[
(\ell_1M,\ell_2M)=(-3v^4/2,0).
\tag{28}
\]
Consequently a first non-tangent correction cannot occur alone.  It
also cannot balance only \(K\) or only \(L\): the corresponding two
cokernel vectors are independent.  This leaves only a triple
collision of \(K,L,M\).

For the fifth row,
\[
J_5=v^4J_1-\frac23v^3J_2.
\tag{29}
\]
Solving the two cokernel equations in a triple collision and then
applying the terminal quotient from (29) gives, again in the order
\(k_*=8,7,5,4,2,1\),
\[
{20900\over243}v^{13},\
-{13685\over243}v^{12},\
{1976\over81}v^{10},\
-{1309\over81}v^9,\
{65\over9}v^7,\
-{44\over9}v^6.
\tag{30}
\]
Every entry is nonzero.

Equations (22)--(30) also account for arbitrary unequal correction
orders.  At the first new order, tangent kernel corrections are
absorbed into the formal parameters \(s,v\).  A non-tangent correction
first appears through \(M\).  If its order is isolated, tied to one
of \(K,L\), or tied to both, (28), (25), or (30), respectively,
excludes it.  Hence no further Newton profile remains.  This proves
that the three comparisons
\[
2\eta>\delta\rho,\qquad
2\eta=\delta\rho,\qquad
2\eta<\delta\rho
\]
are exhaustive, including the singular secondary cone.

The upper constant \(j\) and every lower extra coefficient enter
strictly after these first obstructions.  When \(\delta=7\) or \(8\),
the first \(j\)-dependent transverse term has deficit
\(6\rho+\eta\); it is still later than the relevant quadratic,
cubic, or first-\(\kappa\) order.  Thus they cannot alter the case
split.

## 5. Pole order versus affine \(A_5\)

In either the initial balanced case (19) or the singular triple
collision (30), the nonzero terminal leading coefficient has pole degree
\[
\deg A_5=(14-\delta)\rho.
\tag{31}
\]
At least one of the resonant leading coefficients \(a,b\) is
nonzero.  If \(a_0\ne0\), then \(2\rho=\deg a\ge1\), and hence
\[
(14-\delta)\rho\ge\frac{14-\delta}{2}\ge3.
\tag{32}
\]
If \(a_0=0\), then \(b_0\ne0\), so \(3\rho=\deg b\ge1\), and
\[
(14-\delta)\rho\ge\frac{14-\delta}{3}\ge2.
\tag{33}
\]
Thus the terminal pole degree is always greater than one.  In
particular there is no affine-degree-one arithmetic exception.

This completes the extra-\(\kappa\) theorem.

## Exact verification

Run
```bash
.venv/bin/python \
  current_context/verify_normal_degree_96_cube_constant_h_extra_kappa_exclusion.py
```
The script reconstructs \(A_1,\ldots,A_5\) from the independent
Laurent-residue verifier, checks the boundary split, computes all
projective-chart Gröbner unit ideals, and verifies (22)--(30) over
\(\mathbf Q\).
