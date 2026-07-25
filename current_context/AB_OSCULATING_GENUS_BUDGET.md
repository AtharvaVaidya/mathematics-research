# A genus budget from the osculating cubic

Date: 24 July 2026

## Result

The osculating cubic gives a uniform geometric obstruction, not merely a
bounded coefficient condition.

Let \(r\ge2\), let
\[
\deg A=2r,\qquad \deg B=3r,\qquad
\mathbf C(A,B)=\mathbf C(w),
\]
and let
\[
\mathcal H(X,Y)
=Y^2-LX^3+c_5XY+c_4X^2+c_3Y+c_2X+c_0,
\qquad L\ne0,
\]
satisfy
\[
G(w)=\mathcal H(A(w),B(w)),\qquad
d:=\deg G\le r+3.
\]
Then \(G\) is nonconstant and the affine singularities of the image curve
\(C=\overline{(A,B)(\mathbf A^1)}\) satisfy
\[
\boxed{\quad
\sum_{p\in C\cap\mathbf A^2}\delta_p
\le
\left\lfloor
\frac{(d+1)r-d+1}{2}
\right\rfloor .
\quad}
\tag{1}
\]
In particular, without knowing \(d\) more precisely,
\[
\boxed{\quad
\sum_{p\in C\cap\mathbf A^2}\delta_p
\le
\left\lfloor\frac{r^2+3r-2}{2}\right\rfloor .
\quad}
\tag{2}
\]

For the full a/b boundary, \(r=4\), so the total affine delta budget is
at most \(13\).  Combining this with the exhaustive fixed-pole Puiseux
table eliminates three of its five surviving cells:
\[
\boxed{(5,8),\ (7,11),\ (m,N)=(4,14)\ \text{are impossible}.}
\tag{3}
\]
Only
\[
\boxed{(3,5)\quad\text{and}\quad(m,N)=(3,10)}
\tag{4}
\]
remain.  The abstract genus bound forces \(d\ge5\) in the second cell.
For an actual full a/b solution, the leading osculating ODE is stronger:
it forces \(d=7\).  Consequently the infinity branch has characteristic
pair \((4,29)\), its delta invariant is exactly \(42\), and the total
affine delta is exactly \(13\).

This is an all-\(r\) genus/contact sieve.  Its proof uses the normalization,
the smooth flex place of the osculating cubic, and the local semigroup at
infinity; it does not eliminate boundary coefficients.

## 1. The projective curve and its unique infinity branch

Homogenize the polynomial parametrization to degree \(3r\):
\[
\nu:\mathbf P^1\longrightarrow\mathbf P^2,\qquad
[s:t]\longmapsto
\left[t^{3r}A(s/t):t^{3r}B(s/t):t^{3r}\right].
\tag{6}
\]
Here the first entry is \(t^rA^{\rm h}(s,t)\), where
\(A^{\rm h}=t^{2r}A(s/t)\); thus all three displayed entries are
homogeneous forms of degree \(3r\).
There is no base point at \(t=0\), because the leading coefficient of
\(B\) is nonzero.  The assumption
\(\mathbf C(A,B)=\mathbf C(w)\) makes \(\nu\) birational onto its image.
Consequently \(C\) is an irreducible rational plane curve of degree
\(3r\), and it has a unique normalization point above the line at
infinity:
\[
p_\infty=[0:1:0].
\]

In the chart \(Y=1\), put
\[
u=X/Y,\qquad v=T/Y.
\]
With \(t=1/w\), one has
\[
\operatorname {ord}_{t=0}u=r,\qquad
\operatorname {ord}_{t=0}v=3r.
\tag{7}
\]

The projective osculating cubic is
\[
\begin{aligned}
\overline{\mathcal H}={}&
TY^2-LX^3+c_5TXY+c_4TX^2\\
&+c_3T^2Y+c_2T^2X+c_0T^3.
\end{aligned}
\tag{8}
\]
Its local equation at \(p_\infty\) is
\[
f(u,v)=
v-Lu^3+c_5uv+c_4u^2v+c_3v^2+c_2uv^2+c_0v^3.
\tag{9}
\]
Since \(f_v(0,0)=1\), the pair \((u,f)\) is a regular system of local
coordinates.  Exact substitution gives
\[
f\!\left(\frac AB,\frac1B\right)
=\frac{\mathcal H(A,B)}{B^3}.
\]
Therefore the intersection order of the infinity branch with the smooth
osculating cubic is
\[
\boxed{
q:=\operatorname {ord}_{t=0}f(u(t),v(t))=9r-d.
}
\tag{10}
\]
The bound \(d\le r+3\) gives \(q\ge8r-3\).

The polynomial \(G\) cannot be constant.  Otherwise the degree-\(3r\)
irreducible curve \(C\) would be contained in a cubic, impossible for
\(r\ge2\).

## 2. Local semigroup bound

We use the following elementary plane-branch lemma.

> **Smooth-contact delta lemma.**  Let an irreducible plane branch have
> local coordinates \(x,y\) with
> \[
> \operatorname {ord}x=m,\qquad
> \operatorname {ord}y=q>m.
> \]
> Then
> \[
> 2\delta=\mu\ge(m-1)(q-1).
> \tag{11}
> \]

To prove it, formally reparametrize so that \(x=s^m\).  If \(m\nmid q\),
then \(q\) is the first characteristic exponent.  Put
\(e_1=\gcd(m,q)\).  The characteristic-exponent formula
\[
\mu=\sum_i(e_{i-1}-e_i)(\beta_i-1),
\qquad e_0=m,\quad e_g=1,
\tag{12}
\]
has first contribution \((m-e_1)(q-1)\).  Every later
\(\beta_i\) is larger than \(q\), and the remaining coefficients
\(e_{i-1}-e_i\) sum to \(e_1-1\).  This proves (11).

If \(m\mid q\), subtract the analytic monomial
\(a x^{q/m}\) from \(y\).  Repeating this for any later exponents
divisible by \(m\), the first characteristic exponent is strictly larger
than \(q\).  Formula (12) then gives the strict version of (11).
Such a characteristic exponent must occur because the branch is
irreducible and its normalization parameter is primitive.

Apply the lemma to the regular coordinates \((u,f)\) from (9).  Equations
(7) and (10) give
\[
\delta_\infty
\ge
\left\lceil
\frac{(r-1)(9r-d-1)}2
\right\rceil .
\tag{13}
\]

## 3. The global genus budget

The arithmetic genus of a degree-\(3r\) plane curve is
\[
p_a(C)=\frac{(3r-1)(3r-2)}2.
\tag{14}
\]
The normalization has genus zero, so
\[
\delta_\infty+
\sum_{p\in C\cap\mathbf A^2}\delta_p=p_a(C).
\tag{15}
\]
Combining (13)--(15) and simplifying gives (1):
\[
\sum_{p\in C\cap\mathbf A^2}\delta_p
\le
\left\lfloor
\frac{(d+1)r-d+1}{2}
\right\rfloor .
\]
The right side increases with \(d\).  Setting \(d=r+3\) proves (2).

## 4. Application to the five a/b cells

For \(r=4\), the projective curve has degree \(12\) and arithmetic genus
\(55\).  The infinity contact is at least \(29\), and (11) gives
\[
\delta_\infty\ge42.
\]
Hence all affine singularities together have delta at most \(13\).

The local delta lower bounds at the marked point are:
\[
\begin{array}{c|c|c}
\text{cell}&\text{regular local coordinate orders}&\delta_0\text{ lower bound}\\ \hline
(3,5)&(3,5)&4\\
(5,8)&(5,8)&14\\
(7,11)&(7,11)&30\\
(3,10)&(3,10)&9\\
(4,14)&(4,14)&20
\end{array}
\tag{16}
\]
For the last two rows, the second coordinate is obtained by subtracting
the analytic quadratic and cubic terms from \(B-B(0)\).  In the
\((4,14)\) row, the next characteristic exponent is at least \(15\);
(12) gives
\[
2\delta_0\ge(4-2)(14-1)+(2-1)(15-1)=40.
\]

The three rows with \(\delta_0>13\) contradict the global budget and give
(3).  In the \((3,10)\) row, (1) gives a budget at most \(8\) when
\(d\le4\), so \(d\ge5\).  Finally, at any marked cell,
\[
\operatorname {ord}_0(G-G(0))
\ge\min(\operatorname {ord}_0(A-A(0)),
        \operatorname {ord}_0(B-B(0)))=m.
\]
Since \(G\) is nonconstant, \(d\ge m\).  This gives the stated range for
the \((3,5)\) cell in the abstract setting.

For the full reduced-Jacobian system one can sharpen \(d\le7\) to
\[
\boxed{d=7.}
\tag{17}
\]
Indeed, put \(K=\mathcal H(P,Q)\).  The exact identity
\[
\{P,K\}=(2Q+c_5P+c_3)\frac{z^4}{w^3}
\]
has right side of top total degree \(3r+1\).  Since
\(\deg P=2r\), it first forces \(\deg K=r+3\).  The leading equation has
the five-term solution
\[
K_{r+3}
=w^{r-1}\sum_{j=0}^4 a_jz^{4-j}w^j,
\]
where, after a nonzero normalization,
\[
\bigl(r(j-5)+3\bigr)a_j+r(j-5)a_{j-1}=0
\qquad(1\le j\le4).
\tag{18}
\]
At \(r=4\), all four denominators and \(a_0\) are nonzero, so
\(a_4\ne0\).  The pure term \(a_4w^7\) survives on \(z=0\), proving
(17).  This is the same leading-ODE calculation verified independently
in `route_bd_osculating_leading_ode.py`.

Now \(q=36-d=29\) is coprime to four.  It is the first characteristic
exponent of the infinity branch, so (12) is an equality:
\[
\boxed{\delta_\infty=\frac{(4-1)(29-1)}2=42.}
\tag{19}
\]
Equation (15) therefore gives
\[
\boxed{\sum_{p\in C\cap\mathbf A^2}\delta_p=55-42=13.}
\tag{20}
\]
The marked branch delta is exactly \(4\) in the \((3,5)\) cell and
exactly \(9\) in the \((3,10)\) cell, because the displayed pairs are
coprime.  Thus a surviving curve must carry additional affine delta
\[
\boxed{
9\ \text{in the }(3,5)\text{ cell},\qquad
4\ \text{in the }(3,10)\text{ cell}.
}
\tag{21}
\]
This extra delta may occur at other singular points or through other
normalization branches meeting the marked image point; (21) counts both.

There is also an exact global semigroup consequence.  Let
\[
R_C=\mathbf C[A,B]\subset\mathbf C[w]
\]
be the affine coordinate ring of the boundary, and let
\[
S_\infty=\{\deg_w f:0\ne f\in R_C\}.
\]
The normalization quotient has length
\[
\dim_{\mathbf C}\mathbf C[w]/R_C
=\sum_{p\in C\cap\mathbf A^2}\delta_p=13.
\tag{22}
\]
The degree filtration identifies this length with the number of gaps of
the numerical semigroup \(S_\infty\).  Since
\[
\deg G=7,\qquad\deg A=8,\qquad\deg B=12,
\]
one has
\[
\langle7,8,12\rangle\subseteq S_\infty.
\]
But
\[
\mathbf Z_{\ge0}\setminus\langle7,8,12\rangle
=\{1,2,3,4,5,6,9,10,11,13,17,18,25\},
\tag{23}
\]
which already has thirteen elements.  Inclusion can only remove gaps,
so (22) forces
\[
\boxed{S_\infty=\langle7,8,12\rangle.}
\tag{24}
\]
Equivalently,
\[
\boxed{\{G,A,B\}\text{ is a SAGBI basis of }R_C
\text{ for the degree filtration}.}
\tag{25}
\]
This is considerably stronger than the three degree statements
separately: every cancellation among polynomials in \(G,A,B\) must reduce
to another degree in the same semigroup.

The Apéry set modulo seven is
\[
\operatorname {Ap}(S_\infty;7)
=\{0,8,16,24,32,12,20\},
\tag{26}
\]
listed by residues \(0,1,\ldots,6\).  It follows by leading-term
reduction that \(R_C\) is a free \(\mathbf C[G]\)-module with basis
\[
\boxed{1,\ A,\ A^2,\ A^3,\ A^4,\ B,\ AB.}
\tag{27}
\]
Indeed their leading degrees are precisely the seven Apéry values; any
element of \(R_C\) can be reduced by the matching basis element times a
power of \(G\), and the distinct residues give linear independence.

This semigroup equality is the most rigid scalable output of the genus
argument.  It converts the remaining problem into a small
approximate-root/order problem over the degree-seven map \(G\), without
returning to the original five-block coefficient space.

## 5. What Riemann--Hurwitz adds, and where it stops

The degree-seven polynomial
\[
G:\mathbf P^1_w\longrightarrow\mathbf P^1
\]
has finite ramification total six.  Let
\[
e_0=\operatorname {ord}_0(G-G(0)).
\]
The local Puiseux forms and the fact \(e_0\le7\) give
\[
\begin{array}{c|c|c}
\text{cell}&e_0&\text{ramification away from }0,\infty\\ \hline
(3,5)&3,5,\text{ or }6&4,2,\text{ or }1\\
(3,10)&3\text{ or }6&4\text{ or }1.
\end{array}
\tag{28}
\]
For example, in the \((3,10)\) chart substitute
\[
B-B(0)=c_2x^2+c_3x^3+y,\qquad
\operatorname {ord}x=3,\quad\operatorname {ord}y=10
\]
into the cubic \(\mathcal H\).  Below order eight, the only possible
nonzero orders are three and six.  The \((3,5)\) row follows similarly
from the cubic monomial orders \(3,5,6,8,9,10\).

These passports are all compatible with Riemann--Hurwitz.  Bare
degree-seven maps already realize them:
\[
G_e(w)=w^e+w^7,\qquad e\in\{3,5,6\}.
\tag{29}
\]
Their derivatives have a zero of order \(e-1\) at the marked point and
\(7-e\) simple finite zeros elsewhere.  Therefore normalization,
semigroup, flex contact, and Riemann--Hurwitz alone do **not** eliminate
the last two cells.

The SAGBI module gives the same honest stopping point.  The fiber algebra
\(R_C/(G-G(0))\) has length seven.  In the two cells the local value
semigroups give
\[
\langle3,5\rangle\cap[1,7]=\{3,5,6\},\qquad
\langle3,10\rangle\cap[1,7]=\{3,6\},
\]
exactly the indices in (28); the residual fiber length \(7-e_0\) is
positive in every case.  Extra affine delta may also come from nodal
collisions of distinct normalization points, which consume no
ramification of \(G\).

Finally, on a smooth cubic fiber \(E_c=\{\mathcal H=c\}\), the flex point
\(O=[0:1:0]\) gives
\[
C|_{E_c}=29O+D_c,\qquad \deg D_c=7,\qquad D_c\sim7O.
\]
The corresponding elliptic-group condition \(\sum D_c=O\) is compatible
with every \(e_0\) in (28).  Thus the exact flex divisor supplies no
additional contradiction beyond the genus/SAGBI theorem.

## 6. Strategic consequence

Bare elliptic-pencil geometry was previously too weak because Bézout
allows the high contact at infinity.  The missing invariant is the
normalization genus: the same contact forces at least \(42\) of the
available \(55\) delta units to occur at the unique infinity branch.
The fixed-pole marked cusp must fit inside the remaining budget.

The next global problem is now only two cells with a degree-seven
restriction and a prescribed residual affine delta.  A scalable
continuation would prove that the five-block transverse structure forbids
the additional affine singularities required by (21), or would attach
their normalization branches to the fifth-inertia monodromy.  Merely
recounting ramification of \(G\), its SAGBI fiber length, or the flex
divisor cannot close the argument.
