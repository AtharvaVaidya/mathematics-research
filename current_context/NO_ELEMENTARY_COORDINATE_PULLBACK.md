# No target function pulls back to a one-step elementary source coordinate

Date: 24 July 2026

The preceding triangular-coordinate note treated
\(H\circ F=\lambda z+\phi(x,y)\) by hand.  The same cubic inverse model
rules out all three source directions:

\[
\begin{aligned}
H\circ F&=\lambda x+\phi(y,z),\\
H\circ F&=\lambda y+\phi(x,z),\\
H\circ F&=\lambda z+\phi(x,y),
\end{aligned}
\qquad \lambda\ne0.
\tag{1}
\]

Thus no target polynomial coordinate becomes a source coordinate after one
elementary triangular automorphism and a permutation of \(x,y,z\).

## Exact function-field test

Use target coordinates \((A,B,C)\) and the cubic inverse parameter \(T\):

\[
\mathcal P(T)=CT^3-2T^2+BT-2A,\qquad
r=\mathcal P'(T)=3CT^2-4T+B.
\]

The source reconstruction is

\[
x=\frac2r,\qquad
y=T-\frac r2,\qquad
z=\frac54r^2-\frac32Tr-\frac C8r^3.
\tag{2}
\]

Fix \(\xi\in\{x,y,z\}\).  If the corresponding identity in (1) holds, the
chain rule gives

\[
H_A\,\partial_\xi a+
H_B\,\partial_\xi b+
H_C\,\partial_\xi c=\lambda.
\tag{3}
\]

Substitute (2), clear the power of \(r\), and reduce (3) modulo
\(\mathcal P(T)\).  The coefficients of \(1,T,T^2\) form a \(3\times3\)
linear system over \(\mathbb C(A,B,C)\).  For each \(\xi\), it has a unique
solution for the putative gradient \((H_A,H_B,H_C)\).

A rational vector can be a gradient only if

\[
\partial_BH_A-\partial_AH_B=0.
\tag{4}
\]

Exact elimination gives the following values of the left side of (4) at the
ordinary target point \((A,B,C)=(0,1,0)\), after setting \(\lambda=1\):

\[
\begin{array}{c|c|c}
\xi&(H_A,H_B,H_C)&
\partial_BH_A-\partial_AH_B\\ \hline
x&(-16/63,-1/63,-17/126)&247/147\\
y&(6/47,-1/47,-4/47)&-474/2209\\
z&(1,-1/2,-1/8)&-6.
\end{array}
\]

Every denominator is nonzero at this point, and every displayed curl is
nonzero.  Therefore none of the three rational vector fields is integrable.
No rational \(H\), and hence no polynomial \(H\), can satisfy (1).

For \(\lambda=0\), the same nonsingular systems force the target gradient
to vanish generically, so a pullback independent of one of the three source
variables must be constant.

## Scope

This closes every descent in which a target coordinate pulls back to a
coordinate of the form

\[
\lambda\xi+\text{polynomial in the other two source variables}.
\]

It does not classify coordinates obtained by a composition of several
nonlinear source automorphisms.
