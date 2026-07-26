# The honest quotient by \(g\)-multiple approximate-root changes

Date: 26 July 2026

## Outcome

There is a canonical normal form for a pair of reciprocal
\(g\)-sector jets under change of approximate root, but it does **not**
kill all relative \(g\)-multiple deformations.

Let \(a,b\) be coprime positive integers and put
\[
 z=\frac{\tau^g}{R}.
\]
Write a pair of \(g\)-sector jets as
\[
 P=R^aA(z),\qquad Q=R^bB(z),
 \qquad A,B\in 1+zk[[z]].
\tag{1}
\]
Under
\[
 \bar R=R\phi(z),\qquad
 \bar z=\frac{z}{\phi(z)},\qquad
 \phi\in1+zk[[z]],
\tag{2}
\]
one can uniquely normalize either \(A\) or \(B\) to one.  After
normalizing \(A\), the remaining series is
\[
 \mathcal N(\bar z)
 =B(z)A(z)^{-b/a},
 \qquad
 \bar z=zA(z)^{-1/a}.
\tag{3}
\]
This is a complete orbit representative.

Equivalently, the relative unit
\[
 \mathcal I(z)=\frac{B(z)^a}{A(z)^b}
\tag{4}
\]
is invariant up to a tangent-to-the-identity change of its argument.
In particular,
\[
 \operatorname{ord}_z(\mathcal I-1)
\quad\text{and the first nonzero coefficient of }\mathcal I-1
\tag{5}
\]
are invariants of the quotient.

Consequently an honest approximate-root reparametrization cannot
canonically remove every relative deformation at orders divisible by
\(g\).  The first invariant class can already have residue zero modulo
\(g\).  The family
\[
 A=1+\kappa z^c,\qquad B=1,\qquad
 1\le c\le a,\quad\kappa\ne0,
\tag{6}
\]
gives the exact degree-bound-compatible countermodel
\[
 P=R^a+\kappa\tau^{gc}R^{a-c},\qquad Q=R^b,
\tag{7}
\]
with
\[
 \mathcal I=(1+\kappa z^c)^{-b}
 =1-b\kappa z^c+O(z^{c+1}).
\tag{8}
\]

Thus the full \(g\)-multiple parameter sector in the standard
presentation may hide (7), but it is not a gauge action on a fixed
reciprocal pair.  Declaring it to be gauge changes the invariant (4)
and needs an additional justification from the standard equations.
It is not supplied by approximate-root reparametrization alone.

This result does not prove or disprove the branch-resonance lemma.  It
identifies a necessary correction to its normal-form step: first
retain the relative unit (4), or explicitly prove that the standard
equations make its \(g\)-multiple coefficients removable by a larger
equivalence that preserves the Keller problem.

## 1. The action

The map
\[
 z\longmapsto \bar z=\frac{z}{\phi(z)}
\tag{9}
\]
has linear coefficient one, hence has a unique compositional inverse
\(z=z(\bar z)\).  Rewriting (1) in terms of \(\bar R\) gives
\[
 \begin{aligned}
 \bar A(\bar z)&=\phi(z)^{-a}A(z),\\
 \bar B(\bar z)&=\phi(z)^{-b}B(z).
 \end{aligned}
\tag{10}
\]
This defines the approximate-root action on every finite jet ring
\(k[[z]]/(z^{M+1})\), as well as on the inverse limit.

Taking
\[
 \phi=A^{1/a}
\tag{11}
\]
gives \(\bar A=1\), and (10) becomes exactly (3).  This choice is
unique: if \(\bar A=1\), then \(\phi^a=A\), and a unit with constant
term one has a unique \(a\)-th root in characteristic zero.  An
element preserving the slice \(\bar A=1\) satisfies \(\phi^a=1\),
hence \(\phi=1\).  Therefore every orbit meets the slice \(A=1\)
exactly once.

Equation (10) also gives
\[
 \frac{\bar B(\bar z)^a}{\bar A(\bar z)^b}
 =\frac{B(z)^a}{A(z)^b}.
\tag{12}
\]
Composition with \(z=\bar z+O(\bar z^2)\) preserves the order and
leading coefficient in (5).  This proves the quotient theorem.

The same argument works without change through the standard-system
order \(N=m+n-2\): take
\[
 M=\left\lfloor\frac N g\right\rfloor=a+b-1
\tag{13}
\]
and perform every operation in \(k[[z]]/(z^{M+1})\).  Root extraction,
composition, and compositional inversion are triangular, so no
coefficient above order \(M\) is needed to determine the normal form
through order \(N\).

## 2. Compatibility with reciprocal degree bounds

Let \(R\in k[X]\) be monic of degree \(g\).  If
\[
 A(z)=\sum_{q=0}^a A_qz^q
\tag{14}
\]
has scalar coefficients, then
\[
 R^aA(\tau^g/R)
 =\sum_{q=0}^a A_q\tau^{gq}R^{a-q}.
\tag{15}
\]
The coefficient of \(\tau^{gq}\) has \(X\)-degree
\[
 g(a-q)=n-gq,
\tag{16}
\]
which exactly saturates the reciprocal degree bound.  The analogous
statement holds for \(R^bB(z)\).  Thus (6)--(7) is not excluded by
polynomiality or by the coefficient bounds.

There is a sharper distinction between a formal change of
presentation and a simultaneous polynomial reparametrization of both
pure powers.  Suppose \(\phi\in1+zk[[z]]\) has the property that
\[
 \phi^a\in k[z],\quad\deg\phi^a\le a,
 \qquad
 \phi^b\in k[z],\quad\deg\phi^b\le b.
\tag{17}
\]
Since \(\gcd(a,b)=1\), unique factorization applied to
\((\phi^a)^b=(\phi^b)^a\) gives a polynomial \(H\) such that
\[
 \phi^a=H^a,\qquad\phi^b=H^b.
\tag{18}
\]
The normalized constant terms force \(\phi=H\), and the degree bounds
force \(\deg H\le1\).  Hence
\[
 \phi(z)=1+cz.
\tag{19}
\]
So the large formal group becomes only the one-parameter shift
\(R\mapsto R+c\tau^g\) if one requires both new pure powers to remain
polynomials with their reciprocal degree bounds.  The larger
triangular cancellation in the \(\lambda_{gq}\)-sector is therefore a
property of the standard presentation, not an honest simultaneous
polynomial change of the pair.

## 3. What survives after choosing a slice

For the residue decomposition
\[
 S=\sum_{r=0}^{g-1}
 \tau^rR^{\,b-r/g}B_r(z),
\tag{20}
\]
the action (2) is
\[
 \bar B_r(\bar z)
 =\phi(z)^{-(b-r/g)}B_r(z).
\tag{21}
\]
One may use \(B_0\) to choose the unique slice
\[
 \bar B_0=1,\qquad \phi=B_0^{1/b}.
\tag{22}
\]
In that slice, the first index \(r>0\) for which
\(\bar B_r\ne0\) is invariant under further approximate-root changes,
because the stabilizer of (22) is trivial.  This gives a canonical
**conditional** non-\(g\)-multiple class.

For the standard-system forcing,
\[
 N\equiv-2\pmod g,
\tag{23}
\]
so its formal residue class is \(r=g-2\) when \(g>2\), and \(r=0\)
when \(g=2\).  This grading survives the quotient (22), but its
nonvanishing is not by itself a Keller obstruction.  The endpoint
pairing between Laurent orders \(-1\) and \(g-1\) in Section 9 of
`STANDARD_SYSTEM_WEIGHTED_ESCAPE.md` represents the same
\(\zeta^{-2}\) class.  A valid branch-resonance proof must therefore
quotient that pairing in addition to choosing the approximate-root
slice.

The obstruction is now precise:

> Approximate-root reparametrization supplies a canonical slice, not
> the vanishing of the relative unit.  Any proof that removes all
> \(g\)-multiple relative jets must establish, from the standard
> equations and not from coordinate change, that the invariant
> \(\mathcal I\) has trivial jet through order \(a+b-1\).

## 4. The relative unit satisfies a linear exact equation

There is a useful invariant check on the conclusion.  For a
homogenized Keller pair, work \(\tau\)-adically over \(k(X)\).
After the common powers of \(R\) are removed, the relevant ratios have
constant term one, so the following formal logarithms are defined.  Set
\[
 p=\log P,\qquad q=\log Q,\qquad
 \ell=\log\mathcal I=aq-bp.
\tag{24}
\]
Divide the homogenized Keller identity
\[
 \tau(P_XQ_\tau-P_\tau Q_X)+ga\,PQ_X-gb\,QP_X
 =-c\tau^N
\tag{25}
\]
by \(PQ\).  Since
\[
 q=\frac ba p+\frac1a\ell,
\tag{26}
\]
the quadratic-looking determinant becomes linear in \(\ell\):
\[
\boxed{
\tau\left(
\frac{P_X}{P}\ell_\tau
-\frac{P_\tau}{P}\ell_X
\right)
+ag\,\ell_X
=-\frac{ac\,\tau^N}{PQ}.
}
\tag{27}
\]
Thus the relative unit is not merely an artifact of the chosen
presentation; it is the unknown in an exact linear transport equation.

If \(d<N\) is the first order with
\(\ell_d\ne0\), substitute \(P_0=R^a\) into (27).  Its coefficient at
order \(d\) is
\[
gR\ell_d'+dR'\ell_d=0,
\tag{28}
\]
so
\[
\ell_d=\kappa R^{-d/g}.
\tag{29}
\]
For a minimal Kummer exponent, rationality gives either
\(\kappa=0\) or \(g\mid d\).  This recovers the mod-\(g\) resonance
directly for the invariant (4).  It also shows why an
approximate-root change cannot remove it: that change only changes
the coordinates used to write a solution of (27).

There is one positive consequence.  Suppose \(g>2\) and, below order
\(N\), both \(P\) and \(\ell\) contain only \(g\)-multiple
\(\tau\)-orders.  Then the residue classes in (27) decouple.  Since
\(N\equiv-2\pmod g\), none of those lower terms contributes to the
order-\(N\) equation.  Writing
\[
 W=R^{a+b}\ell_N
\]
gives exactly
\[
gRW'-2R'W=-cR.
\tag{30}
\]
Hence lower \(g\)-multiple relative invariants do not themselves
prevent the endpoint obstruction.  The genuine unresolved mixing is
caused by non-\(g\)-multiple \(Z=0\) (nilpotent common) jets of \(P\),
which enter the coefficients of the transport operator in (27).
Those jets are not acted on by the group (2), and they are precisely
the cascade left open by the branch-resonance lemma.
