# The degree-four boundary parametrization is necessarily nodal

Date: 24 July 2026

> **Later result.**  The nodal power passport isolated in this memo is
> impossible: its fourth transverse Taylor coefficient has an uncancelled
> \(w^{-2}\) term.  See `AB_DELTA4_NODAL_OBSTRUCTION.md`.  Thus the final
> conclusion is \(\delta\ne4\).  The classification below remains the
> input to that obstruction.

## Verdict

Let
\[
\Gamma=\overline{\{(p(w),q(w)):w\in\mathbf A^1\}}
\]
be the full a/b asymptotic component, and suppose its parametrization
degree is
\[
\delta=[\mathbf C(w):\mathbf C(p,q)]=4.
\]
Write
\[
p=A(h),\qquad q=B(h),\qquad
\deg h=4,\quad \deg A=2,\quad \deg B=3,
\]
where \(h\) is the normalization parameter.  Let
\[
\mathcal H(X,Y)
=Y^2-LX^3+c_5XY+c_4X^2+c_3Y+c_2X+c_0
\]
be the universal osculating cubic constructed from the full a/b pair.
Since
\[
\deg_w\mathcal H(p,q)\le7,
\]
one has
\[
\deg_h\mathcal H(A,B)\le1.
\]

The linear alternative is impossible.  Consequently
\[
\boxed{\mathcal H(A(h),B(h))\ \text{is constant}.}
\]
Thus \(\Gamma\) itself is a singular member of the generalized
Weierstrass pencil.  The cuspidal alternative is incompatible with the
fixed \(z^2/w\) pole of the five-block system.  Therefore
\[
\boxed{\delta=4\quad\Longrightarrow\quad
\Gamma\ \text{is a nodal cubic}.}
\]

There is a further exact restriction.  In nodal normalization
\[
X=h^2,\qquad Y=h(h^2-c^2),\qquad c\ne0,
\]
the coefficient \(n_5(w)\) of the first transverse term satisfies
\[
\boxed{
-5h'(w)n_5(w)=\kappa\,\frac{h(w)^2-c^2}{w^3}
}
\]
for a nonzero constant \(\kappa\).  The five-block pole bound then forces
\[
\boxed{
h(0)\in\{c,-c\},\qquad
\operatorname{CritVal}(h)\subseteq\{c,-c\}.
}
\]
In other words, \(h\) is a degree-four Shabat polynomial with the marked
point \(w=0\) lying above the node.

The same section argument sharpens the other two parametrization degrees.
The Abhyankar--Moh--Suzuki degree theorem says that a polynomial embedding
\(h\mapsto(A(h),B(h))\) requires one of \(\deg A,\deg B\) to divide the
other.  None of
\[
(8,12),\qquad(4,6),\qquad(2,3)
\]
has that property.  Hence a linear restriction is impossible for every
\(\delta\).  A constant restriction would put \(\Gamma\) inside a cubic,
which is impossible when its projective degree \(12/\delta\) is greater
than three.  Therefore the exact intrinsic degree spectrum is
\[
\boxed{
\begin{array}{c|c}
\delta&\deg_h\mathcal H(A,B)\\ \hline
1&2,3,4,5,6,\text{ or }7,\\
2&2\text{ or }3,\\
4&0.
\end{array}}
\]
Thus no boundary component is a section of the elliptic pencil:
\(\delta=1,2\) give genuine multisections of degree at least two, while
\(\delta=4\) is the singular nodal fiber described above.

This is a sharp restriction, not a contradiction.  The exact curve-level
model
\[
h(w)=8w^4-8w^2+1,\qquad
p=h^2,\qquad q=h^3-h
\]
has \(\delta=4\) and nodal image
\[
Y^2=X(X-1)^2.
\]
It also obeys the required critical-value and pole ledger:
\[
\frac{h^2-1}{w^3h'}
=\frac{(w^2-1)(2w^2-1)}{w^2}.
\]
The model is not asserted to extend to a full five-block Jacobian
solution; it shows that the new curve-level conclusion cannot by itself
be strengthened to exclude \(\delta=4\).

## 1. Why the linear restriction is impossible

Put
\[
G(h)=\mathcal H(A(h),B(h)).
\]
The pullback bound and \(\deg h=4\) give \(\deg G\le1\).  If
\(G(h)=ah+b\) with \(a\ne0\), then
\[
h=\frac{\mathcal H(A(h),B(h))-b}{a}\in\mathbf C[A(h),B(h)].
\]
Hence the polynomial parametrization
\[
h\longmapsto(A(h),B(h))
\]
would be a closed embedding of \(\mathbf A^1\) with a polynomial inverse.

For all three degree pairs its failure follows from the
Abhyankar--Moh--Suzuki degree theorem.  For degrees \((2,3)\), which is
the only case needed for the nodal conclusion, it is also elementary.
Translate \(h\) so that
\[
A(h)=a_2h^2+a_0,\qquad a_2\ne0,
\]
and write
\[
B(h)=b_3h^3+b_2h^2+b_1h+b_0,\qquad b_3\ne0.
\]
If \(b_1\ne0\), choose a nonzero root \(\rho\) of
\[
b_3\rho^2+b_1=0.
\]
Then
\[
A(\rho)=A(-\rho),\qquad B(\rho)=B(-\rho),
\]
contradicting injectivity.  If \(b_1=0\), both \(A'\) and \(B'\) vanish
at zero.  Differentiating a hypothetical polynomial identity
\(h=K(A(h),B(h))\) at zero gives \(1=0\).  Therefore the linear case is
impossible, and \(G\) is constant.

The projective closure of \(\Gamma\) has degree three.  Since it is
contained in a cubic fiber of the pencil, it is that fiber.  It cannot be
a smooth plane cubic because its normalization is \(\mathbf P^1\).
The unique point at infinity of a generalized Weierstrass cubic is always
smooth, so its singularity is affine and is either a node or a cusp.

## 2. Why the cubic cannot be cuspidal

Complete the square in the target:
\[
Y_1=Y+\frac{c_5X+c_3}{2}.
\]
After translating and rescaling \(X,Y_1\), a cuspidal member has equation
\[
Y_1^2=LX_1^3.
\]
Apply the same affine target change to the full a/b pair.  It preserves
the Jacobian up to a nonzero constant.  Its five-block pole shape becomes
\[
\begin{aligned}
X_1&=p_0+p_1z+p_2z^2,&
&\operatorname{ord}_{w=0}p_2=-1,\\
Y_1&=q_0+q_1z+q_2z^2+q_3z^3,&
&\operatorname{ord}_{w=0}q_2,\operatorname{ord}_{w=0}q_3\ge-1.
\end{aligned}
\]
The extra possible pole in \(q_2\) comes from the shear by \(X\), and is
still only simple.

On the boundary,
\[
p_0=\alpha h^2,\qquad q_0=\beta h^3,\qquad
\beta^2=L\alpha^3,\qquad \deg h=4.
\]
With
\[
t=\frac{\alpha Y_1}{\beta X_1},\qquad
n=Y_1^2-LX_1^3,
\]
one computes on the cusp
\[
\det\frac{\partial(t,n)}{\partial(X_1,Y_1)}
=\frac{\beta}{\alpha}h^2.
\]
Since \(J(X_1,Y_1)\) is a nonzero constant times \(z^4/w^3\), comparison
of the first transverse coefficient gives
\[
-5h'(w)n_5(w)
=\kappa\,\frac{h(w)^2}{w^3},
\qquad \kappa\ne0.
\]
Here
\[
n=z^5n_5+z^6n_6
\]
because the transverse ramification order is five.  Direct expansion
gives
\[
n_5=2q_2q_3-3Lp_1p_2^2,
\]
so \(\operatorname{ord}_0n_5\ge-2\).

If \(h(0)\ne0\), the displayed differential identity gives a pole of
order at least three, a contradiction.  Thus \(h(0)=0\).  Every nonzero
critical point of \(h\) must also be a zero of \(h\), since \(n_5\) is
regular away from zero.  A characteristic-zero polynomial all of whose
critical points are roots has only one distinct root.  Hence
\[
h=cw^4.
\]

The coefficients of \(z,z^2,z^3,z^4\) in \(n\) vanish.  Eliminating
\(q_1,q_2,q_3\) from the first three gives the exact fourth-coefficient
identity
\[
n_4
=-\frac{3q_0^2}{64p_0^4}
\left(4p_0p_2-p_1^2\right)^2.
\]
Therefore
\[
p_1^2=4p_0p_2.
\]
But \(p_0=Aw^8\) and \(p_2\) has a nonzero \(w^{-1}\) coefficient, so
the right side has exact \(w\)-adic order seven.  A polynomial square
cannot have odd valuation.  This excludes the cusp.

## 3. The nodal critical-value equation

Every nodal cubic of this form is affinely equivalent to
\[
n(X,Y)=Y^2-X(X-c^2)^2=0,
\]
with normalization
\[
X=h^2,\qquad Y=h(h^2-c^2).
\]
The rational inverse normalization coordinate is
\[
t=\frac{Y}{X-c^2}.
\]
A direct calculation on \(n=0\) gives
\[
\det\frac{\partial(t,n)}{\partial(X,Y)}
=h^2-c^2.
\]
If
\[
n(P,Q)=z^5n_5(w)+O(z^6),
\]
the chain rule and the reduced Jacobian therefore yield
\[
-5h'n_5=\kappa\frac{h^2-c^2}{w^3}.
\]

The left side has no poles away from \(w=0\).  Hence every nonzero zero
of \(h'\) maps to \(c\) or \(-c\).  At \(w=0\), the bound
\(\operatorname{ord}_0n_5\ge-2\) forces \(h(0)^2=c^2\); otherwise the
right side has order at most \(-3\).  It follows in particular that
\[
h'\mid h^2-c^2
\]
in \(\mathbf C[w]\), which is the two-critical-value, or Shabat,
condition.

## 4. The finite degree-four list

At the curve level, the Shabat conclusion reduces the normalization cover
to three unmarked types.  Let \(\lambda_+,\lambda_-\) be the multiplicity partitions of
the fibers \(h^{-1}(c)\) and \(h^{-1}(-c)\).  The finite part of
Riemann--Hurwitz for a degree-four polynomial is
\[
(4-\ell(\lambda_+))+(4-\ell(\lambda_-))=3,
\]
so \(\ell(\lambda_+)+\ell(\lambda_-)=5\).  Up to swapping the two node
branches, the only possibilities are
\[
\boxed{
(4)\mid(1,1,1,1),\qquad
(3,1)\mid(2,1,1),\qquad
(2,2)\mid(2,1,1).
}
\]
Each has a unique polynomial model up to affine changes of source and
target.  Convenient representatives with critical values
\(\{-1,1\}\) are
\[
\begin{array}{c|c}
\text{fiber type}&h(w)\\ \hline
(4)\mid(1,1,1,1)&2w^4-1,\\
(3,1)\mid(2,1,1)&-6w^4+8w^3-1,\\
(2,2)\mid(2,1,1)&8w^4-8w^2+1.
\end{array}
\]
Marking a point of \(h^{-1}(\{-1,1\})\) as \(w=0\) produces only
finitely many marked variants.  Thus the \(\delta=4\) branch becomes a
three-passport problem before any lower five-block coefficients enter.

The full reduced Jacobian collapses this list further.  Let \(w_0\ne0\)
map to the node, put \(s=w-w_0\), and choose analytic target coordinates
\((u,v)\) in which the node is \(uv=0\) and the relevant branch is
\(u=0\).  The boundary map has
\[
v(s,0)=s^m\cdot\text{unit},
\]
where \(m\) is the multiplicity of the corresponding root of
\(h-c\) or \(h+c\).  Generic transverse inertia five and divisibility
along the whole boundary branch give
\[
u(s,z)=z^5U(s,z).
\]
The coefficient of \(z^4\) in the local Jacobian is therefore
\[
5U(s,0)\,\partial_s v(s,0).
\]
On the other hand, an analytic target coordinate change multiplies the
reduced Jacobian by a unit, and
\[
J(P,Q)=\frac{z^4}{w^3}
\]
has a unit \(z^4\)-coefficient at \(w_0\ne0\).  Hence
\[
U(0,0)\,\partial_s v(0,0)\ne0,
\]
so \(m=1\).

Thus every nonzero point above the node is simple.  Since every critical
point of \(h\) lies above the node, \(h'\) has no nonzero root.  It follows
that
\[
\boxed{h(w)=h(0)+aw^4,\qquad a\ne0.}
\]
After normalizing the two node values, only the power passport survives:
\[
\boxed{(4)\mid(1,1,1,1).}
\]
The fork and Chebyshev models are exact curve-level warnings but cannot
occur as the boundary of a full reduced-Jacobian pair.

The surviving curve-level model can be taken as
\[
h=2w^4-1,\qquad p=h^2,\qquad q=h^3-h.
\]
It obeys
\[
\frac{h^2-1}{w^3h'}=\frac{w^4-1}{2w^2},
\]
so even the full local pole and unramified-nonzero-node conditions do not
yet contradict the power passport.

## 5. Strategic meaning

The elliptic-pencil route does not eliminate the last parametrization
degree.  It turns it into a rigid finite geometric alternative:

- \(\delta=4\) cannot be a section of the pencil;
- it must be a singular cubic fiber;
- the singularity must be a node;
- the degree-four covering polynomial of its normalization has only the
  two node branches as finite critical values, with \(w=0\) above the
  node;
- the full reduced Jacobian forces the unique power passport
  \((4)\mid(1,1,1,1)\).

The remaining \(\delta=4\) analysis is therefore a finite marked
power-cover problem coupled to the later five-block equations, not a
general coefficient search.
