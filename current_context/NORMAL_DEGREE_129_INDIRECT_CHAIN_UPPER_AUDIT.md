# Upper-constant audit of the \((12,9)\) order-\(13\) chain

Date: 26 July 2026

## Result

The order-\(13\) indirect chain remains obstructed when all upper
constants and every delayed \(P\)-multiple character are retained.
This calculation strengthens Section 6 of
`NORMAL_DEGREE_129_HALF_ORDER_HOSTILE_AUDIT.md`, whose verifier sets
the upper constants to zero.

Use the honest \(\rho=2\) grading, put
\[
 P=X^3-1,\qquad 2c+3j=0,
\]
and retain
\[
 G_{12}=cP,\qquad F_{18}^{\rm upper}=kP.
\]
For either Hensel sign orbit, let
\[
 G_{13}=aPq,\qquad a\ne0,
\]
where
\[
\begin{aligned}
 S_{\rm eq}&=-\frac12X^2(X^3-3),&
 q_{\rm eq}&=X,\\
 S_{\rm mix}&=
 -\frac{3X^5-2X^4+2X^3-9X^2+14X+10}{18},&
 q_{\rm mix}&=-\frac{2X^2-X+2}{3}.
\end{aligned}
\]
These are normalized by
\[
 qS\equiv1\pmod P.
\]

At every bracket order \(31\leq N\leq47\), split the new jet as
\[
 S_{N-13}=B_{N-13}+P Q_{N-13},\qquad \deg B,\deg Q<3.
\]
The order-\(N\) equation determines the three coefficients of
\(B_{N-13}\).  Its cokernel constrains the older triple
\(Q_{N-21}\).  All ordered quadratic and cubic convolutions are
retained.

## The delayed cancellation at order \(39\)

The apparent pure-chain obstruction at order \(39\) is not valid by
itself.  In both sign orbits the exact consistency equation chooses
\[
 Q_{18}=-\frac{a^4}{9}.
\]
This delayed \(P\)-multiple cancels the \(-4a^3/3\)-type cubic
forcing.  Any proof that drops this term is incomplete.

## The genuine obstruction at order \(47\)

The chain continues uniquely, up to one surviving order-\(15\)
parameter, through order \(46\).  At order \(47\), solve the first
three final equations for the last quotient triple.

For the equal-sign orbit the two residual equations are
\[
 \boxed{0,\qquad \frac{189}{4}a.}
\]
For the mixed-sign orbit they are
\[
 \boxed{-\frac{1729}{108}a,\qquad \frac{63}{4}a.}
\]
They are independent of \(c\), \(k\), and the surviving
order-\(15\) parameter.  Since \(a\ne0\), both systems are
inconsistent.

Thus the upper constants do not rescue the order-\(13\) indirect
chain.  The exact recurrence and both residual calculations are
checked in
`verify_normal_degree_129_indirect_chain_upper_audit.py`.
