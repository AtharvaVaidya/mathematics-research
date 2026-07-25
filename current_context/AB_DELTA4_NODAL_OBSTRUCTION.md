# The nodal power passport is impossible

Date: 24 July 2026

## Theorem

The degree-four normalization alternative for the full a/b asymptotic
component does not occur:
\[
\boxed{\delta\ne4.}
\]

The preceding osculating-cubic analysis had already forced any
\(\delta=4\) boundary into the following rigid form:

1. the osculating cubic restricts constantly to the boundary;
2. the boundary is a nodal cubic;
3. after affine Weierstrass changes its normalization is
   \[
   X=h^2,\qquad Y=h(h^2-c^2),\qquad c\ne0;
   \]
4. the reduced Jacobian forces the power passport
   \[
   h(w)=c+aw^4,\qquad a\ne0,
   \]
   after possibly replacing \(c\) by \(-c\).

Only the first four transverse coefficients are needed to contradict
this last possibility.  No broad coefficient elimination is involved.

## 1. The nodal branch as a graph

The nodal cubic is
\[
n(X,Y)=Y^2-X(X-c^2)^2=0.
\]
On the normalization branch through \(h=c\), it is the graph
\[
Y=g(X),\qquad
g(X)=(X-c^2)\sqrt X,
\]
where the square-root branch is selected by \(\sqrt{h^2}=h\).

Apply the same affine triangular target change to the full a/b pair.  It
preserves the reduced Jacobian up to a nonzero constant and gives
\[
\begin{aligned}
X&=p_0+p_1z+p_2z^2,\\
Y&=q_0+q_1z+q_2z^2+q_3z^3,
\end{aligned}
\]
with
\[
p_0=h^2,\qquad q_0=h(h^2-c^2).
\]
The fixed five-block pole survives as
\[
\boxed{
p_1\in\mathbf C[w],\qquad
p_2=A_2(w)+\frac{\lambda}{w},
\quad \lambda\ne0.
}
\]
The affine shear may add a simple pole to \(q_2\), but that does not
enter the obstruction.

Since \(n(X,Y)\) is a local equation of the boundary curve at a generic
point, the transverse inertia-five calculation gives
\[
n(X,Y)=z^5n_5(w)+z^6n_6(w).
\]
Over the coefficient field \(\mathbf C(w)\), the other nodal factor
\(Y+g(X)\) is nonzero.  Hence
\[
Y-g(X)=O(z^5).
\]
Because \(Y\) has \(z\)-degree only three, the coefficient of \(z^4\) in
\(g(X)\) must vanish.

## 2. The fourth Taylor coefficient

Put
\[
\Delta=p_1z+p_2z^2.
\]
The coefficient of \(z^4\) in \(g(p_0+\Delta)\) is
\[
\boxed{
g_4=
\frac12g''(p_0)p_2^2
+\frac12g'''(p_0)p_1^2p_2
+\frac1{24}g''''(p_0)p_1^4.
}
\]
Writing \(p_0=h^2\), the derivatives are
\[
\begin{aligned}
g''(h^2)&=\frac{3h^2+c^2}{4h^3},\\
g'''(h^2)&=-\frac{3(h^2+c^2)}{8h^5},\\
g''''(h^2)&=\frac{3(3h^2+5c^2)}{16h^7}.
\end{aligned}
\]

Now use \(h(0)=c\ne0\).  The first derivative coefficient satisfies
\[
g''(c^2)=\frac1c\ne0.
\]
Therefore the fixed pole in \(p_2\) gives
\[
g_4
=\frac{\lambda^2}{2c}\frac1{w^2}
+O\!\left(\frac1w\right).
\]
The second summand in \(g_4\) has pole order at most one, and the third
is regular, because \(p_1\) is polynomial.  Thus the \(w^{-2}\)
coefficient cannot cancel.  This contradicts \(g_4=0\).

For reference, clearing denominators factors the same fourth-order
condition as
\[
\begin{aligned}
0={}&16h^4(3h^2+c^2)p_2^2
-24h^2(h^2+c^2)p_1^2p_2\\
&+(3h^2+5c^2)p_1^4\\
={}&(p_1^2-4h^2p_2)
\bigl((3h^2+5c^2)p_1^2
-4h^2(3h^2+c^2)p_2\bigr).
\end{aligned}
\]
Either factor separately also has an uncancelled simple pole, but the
double-pole argument above is shorter.

## 3. Consequence for the elliptic-pencil route

Together with the section and constant-fiber dichotomy, the possible
intrinsic restriction degrees are now
\[
\boxed{
\begin{array}{c|c}
\delta&\deg_h\mathcal H(A(h),B(h))\\ \hline
1&2,3,4,5,6,\text{ or }7,\\
2&2\text{ or }3,
\end{array}}
\]
and \(\delta=4\) is absent.

The useful continuation is therefore not a degree-four Shabat search.
It is the geometry of degree-two or degree-three multisections of the
elliptic pencil, together with their transverse \(5^\delta\) inertia.
