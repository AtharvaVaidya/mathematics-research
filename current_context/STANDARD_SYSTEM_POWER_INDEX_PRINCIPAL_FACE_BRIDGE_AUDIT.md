# Power-index descent ends at the unresolved principal face

Date: 26 July 2026

## Outcome

The nested-expansion/proper-divisor argument of
Makar-Limanov--Trakhtenberg does not close the unmatched
compensating-chain gap after a repeated-root Rees chart.

The cited argument has a useful but limited consequence.  If a chain of
secondary cancellations is first proved to be a subsequence of the
Newton resolution of the chosen decreasing Puiseux branch, then its
nonprincipal stages are finite: the common power denominators
\[
d_0>d_1>\cdots>d_r>1
\tag{1}
\]
form a proper-divisor chain.  What comes next, however, is the
**principal edge**, where the leading Jacobian is already nonzero.
It neither excludes that edge nor forces it to be a matched
face or a direct Kummer cross term.

In reciprocal standard-system coordinates, the new terminal endpoint
lemma identifies this surviving principal configuration exactly.  If
\[
P(X,\tau)=\tau^n F(X/\tau,1/\tau),\qquad
Q(X,\tau)=\tau^m G(X/\tau,1/\tau),
\tag{2}
\]
then
\[
\mathscr K_X(P,Q)
=-\tau^{n+m-2}J(F,G)(X/\tau,1/\tau).
\tag{3}
\]
Writing
\[
F(x,y)=p_0(x)+yp_1(x)+O(y^2),\qquad
G(x,y)=q_0(x)+yq_1(x)+O(y^2),
\tag{4}
\]
the principal equation is
\[
\boxed{p_0'q_1-p_1q_0'=c.}
\tag{5}
\]
Thus the only possible terminal found in the secondary-face theorem,
\[
I=n-1,\qquad J=m-1,
\tag{6}
\]
is not an impossible endpoint.  It is the reciprocal localization of
the ordinary defect-one Bezout equation (5).  Its necessary and
sufficient first-layer condition is
\[
\gcd(p_0',q_0')=1,
\tag{7}
\]
with the usual degree-bounded Bezout representatives.  This remains
true when \(p_0\) or \(q_0\) has smaller than maximal degree; the
constant-derivative and zero-derivative edge cases are included below.

Consequently the exact remaining problem is:

> classify the repeated-root Newton/Rees chains whose lower
> nonprincipal brackets cancel and whose terminal principal data
> satisfy (5), and prove that none extends through all later
> homogeneous equations.

This is the lifted-endpoint problem, not a further power-index
problem.

## 1. What the proper-divisor argument actually says

There is no theorem or proposition number for this statement in the
supplied source, Leonid Makar-Limanov and Leonid Trakhtenberg,
*Properties of a Jacobian mate*, MPIM preprint 24-33 (submitted
6 December 2024).  The exact source locations are:

- the named **Lemma on sub-expansion** in
  “Polynomiality conditions,” pp. 7--8, which proves that the
  expansions at successive edges are nested; and
- the unnumbered proper-divisor paragraphs in
  “Complexity of a counterexample,” p. 9, which define the \(d_i\)
  and state that a nonprincipal step makes \(d_i\) a proper factor of
  \(d_{i-1}\), and that prime \(d_i\) forces the next edge to be
  principal.

The finite bound on the number of nonprincipal stages is an inference
from those two statements, not a separately stated theorem in that
preprint.

At a nonprincipal edge \(e_i'\), write
\[
f_i(e_i')=\phi_i^{d_i'}
\tag{8}
\]
with \(d_i'\) maximal, and expand the mate in rational powers of
\(f_i\).  Makar-Limanov--Trakhtenberg prove that the expansions at
successive edges are nested.  If \(d_{i-1}\) is the common
denominator inherited from the preceding expansion and \(e_i'\) is
not principal, then
\[
d_i=\gcd(d_{i-1},d_i')
\tag{9}
\]
is a proper divisor of \(d_{i-1}\), and all exponents in the new
expansion lie in \(d_i^{-1}\mathbf Z\).  In particular, when \(d_i\)
is prime, the next edge is principal.

Repeated proper divisibility makes the number of nonprincipal power
drops finite (at most the number of prime factors of \(d_0\), counted
with multiplicity).  It does not assert that the principal edge is a
power, matched, radial, or impossible.  On the contrary, at the
principal edge their construction has
\[
J(f_s(e_s'),g_s(e_s'))=1.
\tag{10}
\]

There is no formal identification
\[
d_i\stackrel?=f,\qquad d_i\stackrel?=H,\qquad
d_i\stackrel?=\gcd(f,G)
\tag{11}
\]
with the residual multiplicity, occupied secondary step, or Kummer
index in the repeated-root Rees chart.  The quantities have different
definitions: \(d_i\) is a maximal-power/common-denominator invariant
of one resolved component and its mate expansion, while
\((f,H,G)\) records simultaneous support in a fixed ramified chart.

## 2. The principal category is nonempty

The principal equation can be seen directly in the fractional
Laurent ring used during Newton resolution.  Put
\[
u=x^\alpha y,\qquad
f_e=x^\rho A(u),\qquad
g_e=x^\sigma B(u).
\tag{12}
\]
Then
\[
\boxed{
J(f_e,g_e)
=x^{\rho+\sigma+\alpha-1}
\left(\rho AB'-\sigma A'B\right).
}
\tag{13}
\]
Hence a principal edge satisfies
\[
\rho+\sigma+\alpha=1,\qquad
\rho AB'-\sigma A'B=1.
\tag{14}
\]
These equations have nontrivial polynomial solutions under the
principal-edge sign conditions.  For example, take
\[
\alpha=\frac23,\qquad
\rho=\frac29,\qquad
\sigma=\frac19,
\tag{15}
\]
and
\[
A(u)=u+u^2,\qquad B(u)=-9-18u.
\tag{16}
\]
Then (14) holds.  On the ninth-root cover \(x=r^9\),
\[
\boxed{
f_e=r^8y+r^{14}y^2,\qquad
g_e=-9r-18r^7y,
}
\tag{17}
\]
and
\[
J_{r,y}(f_e,g_e)=9r^8,\qquad
J_{x,y}(f_e,g_e)=1.
\tag{18}
\]
The \(f_e\)-edge joins \((8/9,1)\) to \((14/9,2)\);
its geometric slope is \(3/2>1\), its \(x\)-axis intercept is
\(\rho=2/9>0\), and its order vertex has ordinate one.  Thus even the
local principal category allowed by the Newton-resolution theorem is
genuinely populated.  Proper-divisor descent is a route to this
category, not an exclusion of it.

## 3. Exact reciprocal interpretation

For polynomials \(F,G\) of degrees at most \(n,m\), respectively,
define (2).  A chain-rule calculation gives (3), where
\[
\mathscr K_X(P,Q)
=\tau(P_XQ_\tau-P_\tau Q_X)+nPQ_X-mQP_X.
\tag{19}
\]

The terms in (4) homogenize to
\[
\begin{aligned}
P^{[0]}&=\tau^n p_0(X/\tau),&
P^{[1]}&=\tau^{n-1}p_1(X/\tau),\\
Q^{[0]}&=\tau^m q_0(X/\tau),&
Q^{[1]}&=\tau^{m-1}q_1(X/\tau).
\end{aligned}
\tag{20}
\]
Equation (5) is exactly the total-defect-one part of (3).

For completeness, (7) is sufficient with all reciprocal degree
bounds.  Put
\[
A_0=p_0',\qquad B_0=q_0',
\qquad \deg p_0\le n,\quad \deg q_0\le m.
\tag{20a}
\]
If \(A_0,B_0\ne0\) and \(\gcd(A_0,B_0)=1\), the reduced Bezout
representatives can be chosen with
\[
A_0U+B_0V=c,\qquad
\deg U<\deg B_0,\quad \deg V<\deg A_0.
\tag{20b}
\]
Taking
\[
q_1=U,\qquad p_1=-V
\tag{20c}
\]
gives (5), with
\[
\deg p_1\le n-1,\qquad \deg q_1\le m-1.
\tag{20d}
\]
In fact the inequalities are normally one unit sharper.  If \(A_0\)
is a nonzero constant, take \(q_1=c/A_0,p_1=0\); the case of constant
\(B_0\) is symmetric.  If \(A_0=0\), condition (7) says that \(B_0\)
is a nonzero constant, and one takes
\(p_1=-c/B_0,q_1=0\); again the other case is symmetric.  If both
derivatives vanish, (5) is impossible.  Thus lower actual degrees
introduce no hidden exception.

At a local boundary coordinate \(s\), the two elementary terminal
pairings are already scalar:
\[
\begin{aligned}
\mathscr K_s(A\tau^{n-1},B\tau^{m-1}s)
  &=AB\,\tau^{n+m-2},\\
\mathscr K_s(A\tau^{n-1}s,B\tau^{m-1})
  &=-AB\,\tau^{n+m-2}.
\end{aligned}
\tag{21}
\]
Both obey the reciprocal degree bounds.  They are precisely the two
residual-order patterns \((0,1)\) and \((1,0)\) in the terminal
endpoint lemma.  Therefore no argument using only the terminal
support can exclude them.

What is difficult is not producing the last scalar.  It is arranging
that every earlier cross term between these endpoint pieces and the
repeated common boundary is canceled by admissible lower jets.  The
proper-divisor argument supplies no lifting statement of this kind.

## 4. Why the existing secondary no-gos do not cover it

The matched-face theorem assumes common anchors
\[
p_0=z^{af}A(t^D/z^H),\qquad
q_0=z^{bf}B(t^D/z^H).
\tag{22}
\]
The direct Kummer theorem assumes one such super face and one radial
Kummer monomial.  A principal endpoint of a compensating chain has
arbitrary anchors and is governed instead by
\[
C_0AB+C_B\xi AB'+C_A\xi A'B=c\xi^J,
\tag{23}
\]
the arbitrary-anchor operator.  Neither nestedness of the
Makar-Limanov--Trakhtenberg expansions nor proper divisibility of the
\(d_i\) sets \(C_0=0\), identifies the two anchors, or makes either
anchor radial.

The endpoint lemma does force the monomials contributing to the
right side of (23) to pull back to (6), but (21) shows that this is
compatible with a nonzero scalar.  Globally, all contributions along
the endpoint assemble into (5).

## 5. Hidden assumptions required for a stronger bridge

A proof using the power-index descent would still need each of the
following.

1. **Resolution embedding.**  Show that the support-cancellation
   chain in the fixed Rees chart is a subsequence of the Newton
   resolution of the particular decreasing Puiseux branch selected
   in the Makar-Limanov--Trakhtenberg normalization.
2. **Power-index identification.**  Relate their maximal power
   indices and denominators to the occupied support steps after all
   common holes and deck-equivariant cosets are removed.
3. **Principal-anchor rigidity.**  Prove that the first nonzero
   principal bracket must be matched or direct Kummer.  This is false
   as a statement about principal Laurent faces alone, by (17).
4. **Lifted endpoint exclusion.**  Use the original reciprocal
   degree bounds and all earlier equations to rule out every lift of
   (5).  Endpoint support, branch residues, and proper-divisor descent
   do not do this separately.

Without these inputs, importing the proper-divisor argument proves
finite nonprincipal complexity but does not reduce the open
compensating-chain problem.

The exact coordinate identities and the principal-edge witness are
checked by
`verify_standard_system_power_index_principal_face_bridge_audit.py`.
