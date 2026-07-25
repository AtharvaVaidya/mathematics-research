# The sharp resonant cap stars are formally unobstructed

Date: 25 July 2026

## Audited conclusion

Apply the branchwise Euler invariant of
`CAP_PUISEUX_EULER_JET_INVARIANT.md` to the two actual GGHV case-c cap
types.  The forbidden same-color contact sums
\[
5,\ 9,\ 10,\ 14
\]
do **not** force a contradiction, even after imposing ultrametricity,
conjugacy, every branch residue, and the norm/resultant equation.

There is a unique minimum-height contact tree at each cap:

\[
\begin{array}{c|c|c|c|c|c|c|c}
\text{cap}&(a,b)&c&e_i&d_j&\tau_i&\rho_j&
\operatorname {ord}_u\operatorname {Res}_v(F,G)\\ \hline
\text{vertical}&(2,3)&4&4&8&12&8&24\\
\text{diagonal}&(8,12)&1&7&11&12&8&96 .
\end{array}
\tag{1}
\]

Here \(a,b\) are the numbers of \(F\)- and \(G\)-leaves, \(c\) is the
contact of every pair of distinct leaves, \(e_i,d_j\) are the
same-color contact sums, and \(\tau_i,\rho_j\) are the cross-color sums.
Thus every leaf lies in the allowed resonant alternative, not at a
forbidden value.

More strongly, both stars lift to exact formal solutions of the complete
local bracket equation.  Hence no theorem using only the completed local
cap germ, even through arbitrarily many infinitely-near jets, can exclude
case c.  The obstruction in the global certificate must use the finite
Newton-support cutoff, or an equivalent global relation joining the two
caps to the common outer Hurwitz cover.

The formal lifts below are generally infinite in the boundary parameter.
They are **not** finite global case-c polynomials and are not
counterexamples to the Jacobian conjecture.

## 1. A sharp star lemma

Consider a cap with \(a\) \(F\)-leaves, \(b\) \(G\)-leaves, pole orders
\[
p=ac,\qquad q=bc,
\tag{2}
\]
and normalized bracket exponent \(\kappa\).  Put
\[
N=p+q+1+\kappa.
\tag{3}
\]
Assume
\[
\delta:=c+1+\kappa>0.
\tag{4}
\]

Choose distinct constants
\[
A_1,\ldots,A_a,B_1,\ldots,B_b\in k
\]
and take
\[
\alpha_i=A_i u^c+O(u^{c+1}),\qquad
\beta_j=B_j u^c+O(u^{c+1}).
\tag{5}
\]
Every pairwise contact is then \(c\).  Consequently
\[
\begin{aligned}
e_i&=(a-1)c,&
\tau_i&=bc=q,\\
d_j&=(b-1)c,&
\rho_j&=ac=p.
\end{aligned}
\tag{6}
\]
Moreover
\[
\begin{aligned}
N-q-e_i&=c+1+\kappa=\delta,\\
N-p-d_j&=c+1+\kappa=\delta.
\end{aligned}
\tag{7}
\]
Thus \(e_i<N-q\) and \(d_j<N-p\), and (6) selects exactly the
nonzero-resonant-constant alternatives
\[
\tau_i=q,\qquad \rho_j=p
\tag{8}
\]
in the branchwise Euler dichotomy.

This tree has minimum possible height.  Indeed, let \(h\) be the largest
contact between any two leaves.  If \(h<c\), then
\[
e_i\le(a-1)h<(a-1)c<N-q.
\]
The Euler dichotomy would give \(\tau_i\ge q=bc\), while the sum of its
\(b\) cross-contacts is at most \(bh<bc\), a contradiction.  Hence
\[
h\ge c.
\tag{9}
\]
If \(h=c\), equality in the same argument forces every cross-contact to
equal \(c\).  The ultrametric inequality applied to two same-color
leaves and one opposite-color leaf then forces every same-color contact
to be at least \(c\), hence exactly \(c\).  Therefore the star in (5) is
the unique tree of minimum height.

## 2. The two case-c stars

### 2.1 Vertical cap

For the vertical cap,
\[
(a,b,p,q,\kappa,N)=(2,3,8,12,-4,17),
\qquad c=4,\quad\delta=1.
\tag{10}
\]
Equations (6)--(7) give
\[
e_i=4\ne5,\qquad d_j=8\ne9,\qquad
\tau_i=12,\qquad\rho_j=8.
\tag{11}
\]
The branch-residue integrands have leading exponent
\[
N-q-1-e_i=N-p-1-d_j=c+\kappa=0.
\tag{12}
\]
They are regular, so their \(u^{-1}\)-coefficients vanish.

### 2.2 Diagonal cap

For the diagonal cap,
\[
(a,b,p,q,\kappa,N)=(8,12,8,12,1,22),
\qquad c=1,\quad\delta=3.
\tag{13}
\]
Thus
\[
e_i=7\ne10,\qquad d_j=11\ne14,\qquad
\tau_i=12,\qquad\rho_j=8.
\tag{14}
\]
Here the residue-integrand exponent is
\[
N-q-1-e_i=N-p-1-d_j=c+\kappa=2,
\tag{15}
\]
so the integrands again have no residue.  The factor
\((t+v)^2\) in the diagonal bracket is a unit because the cap lies in
the open boundary orbit, where \(t\ne0\).

## 3. Resultant and conjugacy gluing

Let
\[
f(w)=\prod_i(w-A_i),\qquad
g(w)=\prod_j(w-B_j).
\tag{16}
\]
The cross-contacts in (5) give
\[
\operatorname {Res}_v(F,G)
=u^{abc}\bigl(\operatorname {Res}_w(f,g)+O(u)\bigr).
\tag{17}
\]
Because
\[
abc=aq=bp,
\tag{18}
\]
the normalized resultant in the norm equation has a free nonzero
constant:
\[
\frac{\operatorname {Res}_v(F,G)}{u^{aq}}
=\operatorname {Res}_w(f,g)+O(u).
\tag{19}
\]
The orders are \(24\) and \(96\) in the two rows of (1).

The first correction to (19), computed from the \(F\)-branches or from
the \(G\)-branches, is consistent by the elementary identity
\[
\sum_i\frac1{f'(A_i)g(A_i)}
+
\sum_j\frac1{g'(B_j)f(B_j)}
=0.
\tag{20}
\]
This is the sum of the finite residues of
\[
\frac{dw}{f(w)g(w)};
\]
its residue at infinity is zero.  Thus the trace equation does not
remove the constant in (19).

Over the algebraically closed ground field all the factors in (16) are
linear, so the conjugacy rule gives one constant per leaf and no further
identification.  The examples below are defined over \(\mathbf Q\);
after extension to \(k\), they are therefore compatible with descent as
well.

## 4. A formal lifting theorem

The compatibility is not merely numerical.

> **Formal transverse lifting theorem.**
> Let \(f,g\in k[w]\) have degrees \(a,b\), with
> \(\gcd(f',g')=1\), and let
> \[
> K(u,w)\in k[w][[u]],\qquad
> \deg_w[u^n]K\le a+b-1.
> \]
> Then there exist
> \[
> X,Y\in k[w][[u]]
> \]
> such that
> \[
> X(0,w)=f(w),\qquad Y(0,w)=g(w),
> \]
> \[
> \deg_w[u^n]X\le a,\qquad
> \deg_w[u^n]Y\le b,
> \tag{21}
> \]
> and
> \[
> X_uY_w-X_wY_u=K.
> \tag{22}
> \]

To prove it, consider
\[
\mathcal L(\phi,\psi)=\phi g'-f'\psi.
\tag{23}
\]
The map
\[
k[w]_{\le a}\oplus k[w]_{\le b}
\longrightarrow k[w]_{\le a+b-1}
\tag{24}
\]
defined by (23) is onto.  Given \(R\) of degree at most \(a+b-1\),
choose \(\psi\) of degree \(<b-1\) such that
\[
f'\psi\equiv-R\pmod {g'}.
\]
Then
\[
\phi=\frac{R+f'\psi}{g'}
\]
is a polynomial of degree at most \(a\).

Now write
\[
X=f+\sum_{r\ge1}u^r\phi_r,\qquad
Y=g+\sum_{r\ge1}u^r\psi_r.
\tag{25}
\]
After the coefficients below \(u^n\) have been fixed, the contribution
of the new pair \((\phi_{n+1},\psi_{n+1})\) to the \(u^n\)-coefficient
of the Jacobian is
\[
(n+1)\mathcal L(\phi_{n+1},\psi_{n+1}).
\tag{26}
\]
Surjectivity of (24) and characteristic zero solve (26) recursively.
The degree bounds in (21) are preserved at every step.

Put \(w=v/u^c\), \(p=ac\), and \(q=bc\).  Then
\[
\mathcal F=u^pX(u,v/u^c),\qquad
\mathcal G=u^qY(u,v/u^c)
\tag{27}
\]
belong to \(k[[u,v]]\): a term \(u^{p+r}w^d\), with \(d\le a\),
becomes \(u^{p+r-cd}v^d\), whose \(u\)-exponent is nonnegative.
Furthermore,
\[
\left[u^{-p}\mathcal F,u^{-q}\mathcal G\right]_{u,v}
=u^{-c}\left(X_uY_w-X_wY_u\right).
\tag{28}
\]

For the vertical cap choose
\[
f=w^2-1,\qquad
g=(w-2)(w-3)(w-4),\qquad K=-1.
\tag{29}
\]
The roots are simple and disjoint and
\(\gcd(f',g')=1\).  Equations (27)--(28), with \(c=4\), give the exact
bracket
\[
\left[u^{-8}\mathcal F,u^{-12}\mathcal G\right]_{u,v}
=-u^{-4}.
\tag{30}
\]

For the diagonal cap choose
\[
f=w^8-1,\qquad g=w^{12}+2w,\qquad
K=u^2(t+uw)^2.
\tag{31}
\]
Again the roots are simple and disjoint, and
\[
\gcd(8w^7,12w^{11}+2)=1.
\]
With \(c=1\), (28) becomes
\[
\left[u^{-8}\mathcal F,u^{-12}\mathcal G\right]_{u,v}
=u(t+v)^2,
\tag{32}
\]
the exact diagonal bracket.

The reductions \(f,g\) in (29) and (31) have all \(a+b\) roots
distinct.  Hensel lifting therefore gives the stars in (1), with no
change in their contact orders.

## 5. Closed form for the vertical lift

The vertical lift can even be written without recursion.  Let
\(A\in u\,k[[u]]\) be the unique solution of
\[
26A+\frac34A^2=-u.
\tag{33}
\]
Set
\[
\begin{aligned}
X&=w^2-1+A,\\
Y&=w^3-9w^2+26w-24
  +A\left(\frac32w-9\right).
\end{aligned}
\tag{34}
\]
Differentiating (33) gives
\[
A'\left(26+\frac32A\right)=-1,
\]
and direct calculation yields
\[
X_uY_w-X_wY_u
=A'\left(26+\frac32A\right)
=-1.
\tag{35}
\]
The quadratic equation (33) produces an infinite algebraic power
series.  This is a concrete view of the distinction between formal
local solvability and finite polynomial support.

## 6. Exact scope and next target

The theorem proves that all of the following are locally compatible:

1. the actual pole orders \(p=8,q=12\);
2. the vertical and diagonal face multiplicities;
3. the four forbidden-contact inequalities;
4. every branchwise residue equation;
5. conjugacy and norm/resultant gluing; and
6. the complete local Jacobian equation to arbitrary jet order.

It does **not** preserve the finite range of boundary powers dictated by
the global case-c Newton polygons.  The recursive series in (25)
generally continues forever.  The global certificate can therefore be
viewed conceptually as a termination obstruction: the seven admissible
initial modes cannot terminate simultaneously at both ends of the fixed
Newton polygon.

The sharp next theorem should use one of two genuinely global inputs:

- a finite-support termination functional on (25), sensitive to the last
  allowed boundary coefficient; or
- the outer identity
  \[
  wV(w)^2-LU(w)^3=D_4(w),
  \tag{36}
  \]
  where the left side has degree at most four because the outer cover has
  passport \((17,1^4)\) over \(L\).  Its four finite simple sheets are the
  natural global object to compare with the degree-four diagonal
  dicritical, while the contact-\(17\) sheet is the natural object to
  compare with the vertical chain.

Either route uses information absent from a single completed cap germ
and avoids returning to unrestricted coefficient enumeration.

## 7. The exact outer norm relation available for the next step

There is already a precise relation joining the contact-\(17\) sheet to
the four simple sheets of the outer cover.  It does not yet identify the
local star constants with those sheets, so it is not a contradiction,
but it sharply formulates the missing global comparison.

For the case-c outer solution put
\[
R(w)=\frac{wV(w)^2}{U(w)^3},\qquad
L=R(\infty),\qquad
D(w)=wV(w)^2-LU(w)^3.
\tag{37}
\]
The passport \((17,1^4)\) over \(L\) gives
\[
\deg D=4,
\tag{38}
\]
with four simple roots.  The outer differential equation
\[
UV+2wUV'-3wU'V=1
\tag{39}
\]
implies, without elimination,
\[
\boxed{UD'-3U'D=V.}
\tag{40}
\]
Indeed, the left side of (40) is
\[
V\left(UV+2wUV'-3wU'V\right).
\]

Let \(d=[w^4]D\) and let \(r_1,\ldots,r_4\) be the roots of \(D\).
Equation (40) gives
\[
D'(r_i)=\frac{V(r_i)}{U(r_i)}.
\tag{41}
\]
Taking the product over the four simple sheets yields the exact norm
identity
\[
\boxed{
\operatorname {Res}(D,V)
=d\,\operatorname {Disc}(D)\operatorname {Res}(D,U).
}
\tag{42}
\]
At the remaining point \(w=\infty\),
\[
R(w)-L
=\frac{d}{u_7^3}w^{-17}+O(w^{-18}),
\qquad u_7=[w^7]U.
\tag{43}
\]
Thus (42)--(43) tie the leading coefficient of the unique
contact-\(17\) sheet to the norm of the derivatives on all four simple
sheets.

The missing incidence statement is now concrete: identify the vertical
resonant normalization with the sheet in (43), and the four branches of
the degree-four diagonal dicritical with the roots in (41).  Under that
identification, (42) becomes an exact relation between the two cap
normalizations.  Establishing the identification requires the global
boundary correspondence; it cannot be inferred from either local star.
