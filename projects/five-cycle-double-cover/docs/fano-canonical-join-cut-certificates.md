# Canonical Fano joins have exact cut certificates

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE NECESSARY CONDITIONS / REDUCED FANO
ONE-SWITCH ROUTE / UNCROSSING OPEN**.

This note translates failure of the seven value-class packing tests into
ordinary binary cut certificates.  It then takes the linear dual of all
valid fixed-line switches.  The resulting obstruction is a four-shore
checkerboard with exact value restrictions.

The conclusions are necessary conditions for a switch-local bad flow.
They do not prove that a connected circuit switch repairs the flow, and
they do not resolve the five-cycle double cover conjecture.

## 1. Setup and the four canonical joins

Let \(G\) be a finite loopless cubic graph and let
\[
        f:E(G)\longrightarrow\mathbb F_2^3\setminus\{0\}       \tag{1}
\]
be a flow.  Put
\[
                         M_k=f^{-1}(k)\qquad(k\ne0).
\]
Every \(M_k\) is a matching: the three values at a cubic vertex are
distinct and sum to zero.

Fix \(k\ne0\), put \(K_k=G-M_k\), and let
\[
 \Lambda_k=\{\lambda\in(\mathbb F_2^3)^*:\lambda(k)=1\}.
\]
For \(\lambda\in\Lambda_k\), define
\[
 J_\lambda^k
   =\{e\in E(K_k):\lambda(f(e))=1\}.                  \tag{2}
\]
Applying \(\lambda\) to the flow equation proves
\[
                         \partial J_\lambda^k=\partial M_k,
\]
so the four sets in (2) are canonical \(\partial M_k\)-joins.

For distinct \(\lambda,\mu\in\Lambda_k\), the affine planes
\(\lambda^{-1}(1)\) and \(\mu^{-1}(1)\) meet in two points
\(\{k,w\}\).  Removing \(M_k\) gives
\[
                 J_\lambda^k\cap J_\mu^k=M_w.         \tag{3}
\]

All identities here are over edge objects; parallel edges cause no
change.

## 2. Repairing one canonical pair is a cycle-trace problem

Let \(Z_1(K_k;\mathbb F_2)\) be the binary cycle space of \(K_k\).
Hold \(J_\mu^k\) fixed and add a binary cycle \(C\) to
\(J_\lambda^k\).  The new set \(J_\lambda^k\triangle C\) remains a
\(\partial M_k\)-join.  By (3), it is disjoint from \(J_\mu^k\) exactly
when
\[
                         C\cap J_\mu^k=M_w.            \tag{4}
\]

The standard cycle/cut orthogonality theorem gives an exact alternative.

> **Canonical-pair cut theorem.**  Equation (4) has a solution
> \(C\in Z_1(K_k;\mathbb F_2)\) if and only if
> \[
>              |D\cap M_w|\equiv0\pmod2               \tag{5}
> \]
> for every cut \(D\) of \(K_k\) whose support is contained in
> \(J_\mu^k\).

### Proof

Restrict the cycle space of \(K_k\) to the coordinate set
\(J_\mu^k\).  The orthogonal complement of this restricted space
consists exactly of the edge sets \(D\subseteq J_\mu^k\) whose zero
extension is a cut of \(K_k\).  The target trace in (4) is
\(1_{M_w}\).  It belongs to the restricted cycle space precisely when
it is orthogonal to every such \(D\), which is (5). \(\square\)

Thus, if \(M_k\) fails to pack two edge-disjoint
\(\partial M_k\)-joins, then every ordered pair
\((\lambda,\mu)\) has a literal witness cut
\[
 D_{\lambda,\mu}\subseteq J_\mu^k,\qquad
 |D_{\lambda,\mu}\cap M_w|\equiv1.                    \tag{6}
\]
This is more explicit data than the mere existence of an odd-\(K_{2,3}\)
graft minor for the fixed support, although it is only a certificate
against this canonical-pair repair.

## 3. The witness is one rainbow-odd factor component

For a nonzero functional \(\mu\), put
\[
 F_\mu=\{e:\mu(f(e))=0\}.                              \tag{7}
\]
At every vertex, \(F_\mu\) has degree one or three.  It is therefore a
spanning odd factor.

If \(\mu(k)=1\), then
\[
                         E(K_k)-J_\mu^k=F_\mu.         \tag{8}
\]
A cut of \(K_k\) contained in \(J_\mu^k\) is consequently the cut of a
union of components of \(F_\mu\).  If its intersection with \(M_w\) is
odd, at least one individual component \(W\) of \(F_\mu\) satisfies
\[
 |\delta_{K_k}(W)\cap M_w|\equiv1.                    \tag{9}
\]

Every edge of \(\delta_G(W)\) has value in the four-point affine plane
\[
                         A_\mu=\{v:\mu(v)=1\}.         \tag{10}
\]
Flow conservation over \(W\) gives
\[
                 \bigoplus_{e\in\delta_G(W)}f(e)=0.   \tag{11}
\]
The four vectors in \(A_\mu\) have rank three and their unique nonzero
binary dependence is the sum of all four.  Hence the four value
multiplicities on \(\delta_G(W)\) have either all-even or all-odd
parity.

Call \(W\) **rainbow-odd** in the latter case.  Equation (9) makes \(W\)
rainbow-odd, and the same component is odd in every one of the four
affine value classes.

> **All-class failure consequence.**  If all seven matchings \(M_k\)
> fail the two-\(T\)-join packing test, then, for every nonzero
> functional \(\mu\), the odd factor \(F_\mu\) has a rainbow-odd
> component.

Indeed, choose any \(k\) with \(\mu(k)=1\), choose
\(\lambda\ne\mu\) in \(\Lambda_k\), and apply (6)--(11).
The number of rainbow-odd components of a fixed \(F_\mu\) is even:
for any one value \(v\in A_\mu\), the \(v\)-valued edges have precisely
those components as their odd-degree vertices after the factor
components are contracted.

This recovers the rainbow obstruction from a packing failure without
assuming a five-coordinate lift.

## 4. Exact fixed-line switch update

Fix \(\mu\ne0\) and a nonzero
\[
                         t\in\ker\mu.                  \tag{12}
\]
A valid switch by \(t\) uses a binary cycle
\[
                C\in Z_1(G-M_t;\mathbb F_2).           \tag{13}
\]
Translation by \(t\) preserves \(\ker\mu\) and its affine complement,
so it leaves the edge set \(F_\mu\), and hence its component partition,
unchanged.

Translation by \(t\) partitions \(A_\mu\) into two orbits
\[
                 P=\{b,b+t\},\qquad
                 P'=A_\mu-P.                          \tag{14}
\]
Let \({\cal K}_\mu\) be the components of \(F_\mu\), and let
\[
 r_\mu\in\mathbb F_2^{{\cal K}_\mu}
\]
indicate the rainbow-odd components.  Define
\[
 \tau_t(C)_W
   =|C\cap\delta_G(W)\cap f^{-1}(P)|\pmod2.            \tag{15}
\]
Because a binary cycle crosses every cut evenly, either orbit in (14)
gives the same bit.

Switching translates the colors inside each orbit.  Directly at every
factor component,
\[
                         r_\mu\longmapsto
                         r_\mu+\tau_t(C).              \tag{16}
\]
The map
\[
 \tau_t:Z_1(G-M_t;\mathbb F_2)
             \longrightarrow\mathbb F_2^{{\cal K}_\mu}
\]
is linear.  Thus the line can be cleaned by a sequence of valid
connected-circuit \(t\)-switches exactly when
\[
                         r_\mu\in\operatorname{im}\tau_t. \tag{17}
\]
The binary cycle solving (17) may be disconnected, but its circuit
components all avoid \(M_t\) and can be switched one at a time.

Condition (17) is a multi-switch reachability statement.  It does not
say that one connected circuit already makes a value class pack.

## 5. The dual obstruction is a split cut

The failure of (17) has an exact cut form.

> **Split-cut duality theorem.**  Condition (17) fails if and only if
> there is a set \({\cal Y}\subseteq{\cal K}_\mu\) containing an odd
> number of rainbow-odd components such that, for
> \[
>                     U=\bigcup_{W\in{\cal Y}}V(W),
> \]
> the edge set
> \[
>                     R=\delta_G(U)\cap f^{-1}(P)      \tag{18}
> \]
> is a cut of \(G-M_t\).

### Proof

By finite-dimensional linear duality, (17) fails exactly when there is
a vector \(y\in\mathbb F_2^{{\cal K}_\mu}\) such that
\[
 y\cdot r_\mu=1,\qquad
 y\cdot\tau_t(C)=0
 \quad\text{for every }C\in Z_1(G-M_t;\mathbb F_2).   \tag{19}
\]
Let \({\cal Y}\) be the support of \(y\), and let \(U\) be its vertex
union.  Edges between two selected factor components are counted twice,
so (15) gives
\[
 y\cdot\tau_t(C)=|C\cap R|\pmod2.                     \tag{20}
\]
The second condition in (19) says that \(R\) is orthogonal to the cycle
space of \(G-M_t\).  Cycle/cut orthogonality says exactly that \(R\) is
a cut of \(G-M_t\).  The first condition in (19) is the asserted odd
rainbow count.  Every step is reversible. \(\square\)

The complementary orbit half
\[
                     R'=\delta_G(U)\cap f^{-1}(P')     \tag{21}
\]
is also a cut of \(G-M_t\): the whole \(\delta_G(U)\) contains no
\(\ker\mu\)-valued edge and is a cut in \(G-M_t\), so
\(R'=\delta_G(U)\mathbin\triangle R\).

Since \({\cal Y}\) contains an odd number of rainbow components, each of
the four affine colors occurs oddly on \(\delta_G(U)\).  Therefore both
\(R\) and \(R'\) are nonempty even-cardinality cuts, of size at least
two.

## 6. Four-shore checkerboard form

Choose \(X\subseteq V(G)\) with
\[
                         \delta_{G-M_t}(X)=R.          \tag{22}
\]
Intersect the two shores \(U,\bar U\) and \(X,\bar X\):
\[
\begin{array}{c|cc}
 &X&\bar X\\ \hline
 U&A&B\\
 \bar U&C&D .
\end{array}                                            \tag{23}
\]
Equations (18), (21), and (22) impose the following exact restrictions.

* A non-\(t\) edge between \(A,B\) or between \(C,D\) is impossible.
  Only \(t\)-valued edges can cross \(X\) without crossing \(U\).
* Edges between \(A,D\) or between \(B,C\) which cross both partitions
  have values in \(P\).
* Edges between \(A,C\) or between \(B,D\) which cross only the
  \(U\)-partition have values in \(P'\).
* Values in \(\ker\mu-\{t\}\) stay inside the four cells.

Thus failure of fixed-line cleaning is not an unspecified cohomology
class.  It is a color-restricted checkerboard decomposition in which
the two affine translation pairs form the two diagonal cut systems and
the value \(t\) is the only possible horizontal connector.

The remaining uncrossing problem is precise:

> Can a cyclically \(4\)-edge-connected cubic graph of girth at least
> ten support the required split-cut checkerboards for all three
> \(t\in\ker\mu-\{0\}\) and all seven dirty functionals \(\mu\), while
> remaining bad after every connected circuit switch?

Neither cyclic \(4\)-edge-connectivity nor girth alone immediately
forbids one checkerboard: deleting the matching \(M_t\) can create
two-edge cuts, and the cells in (23) need not all be cyclic.  A sound
uncrossing proof must use the simultaneous seven-functional system or
show that one checkerboard yields a connected repair circuit.

## 7. Finite transcription audit

`scratch/audit_fano_canonical_cut_certificates.py` checks the retained
ten-vertex all-value-class-bad flow.  It independently verifies flow
conservation, enumerates its entire binary cycle space, checks all
\(7\cdot4\cdot3=84\) ordered canonical-pair trace failures, finds a
literal component cut for every failure, and verifies the rainbow
parity on every factor component.  It also directly enumerates all
\(T\)-joins to reconfirm that the seven original value classes fail,
then finds a valid connected-circuit switch by value \(1\), on edges
\(\{0,1,9\}\), after which value class \(5\) packs.  Thus this finite
instance illustrates the cut certificates but is not a countermodel to
the surviving connected-switch statement.

The computation is a transcription audit only.  The universal arguments
above do not depend on it.

## AI-use disclosure

This cut formulation, split-cut duality, checkerboard reduction, audit,
and exposition were developed by an OpenAI Codex agent under human
direction.  The canonical Fano joins and the fixed-line rainbow update
were already present in the project; the prescribed-trace cut theorem
and its four-shore dual are displayed here in full for independent human
checking.  No conjecture-resolution claim is made.
