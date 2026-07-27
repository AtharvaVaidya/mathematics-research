# The full cube-\(h\) chart has four Laurent integrals and one rational time

Date: 26 July 2026

## Outcome

Consider the cube-\(h\) chart left open in
`NORMAL_DEGREE_ARITHMETIC_FRONTIER_AND_96_CONNECTED_REDUCTION.md`.
Thus
\[
 h=r^3,\qquad r\in\mathbf C[x]\setminus\{0\},
\]
and, after putting \(z=ry\) and depressing the monic sextic, one has
\[
 g=w^6+aw^4+bw^3+cw^2+dw+q
\tag{1}
\]
over \(\mathbf C(x)\).  The full upper approximate-root form is
\[
 f=(\Phi(g^{1/6}))_+,
\tag{2}
\]
where
\[
\Phi(S)=S^9+\kappa _8S^8+\kappa _7S^7+\kappa _5S^5
 +\kappa _4S^4+jS^3+\kappa _2S^2+\kappa _1S
\tag{3}
\]
and all seven displayed coefficients are constants.

There are canonical rational functions
\[
 A_1,\ldots,A_5\in\mathbf C(x)
\]
with the following properties:

1. the four full lower equations are exactly
   \[
   A_1'=A_2'=A_3'=A_4'=0;
   \tag{4}
   \]
2. the terminal Keller equation is exactly
   \[
   6A_5'=\frac{\lambda}{r};
   \tag{5}
   \]
3. on the connected-character slice, the previously displayed
   first integrals satisfy
   \[
   I_{10}=6A_1,\quad I_{11}=6A_2,\quad
   I_{12}=6A_3,\quad I_{13}=6A_4.
   \tag{6}
   \]

Consequently \(T=6A_5\in\mathbf C(x)\) obeys
\[
 T'=\frac{\lambda}{r}.
\tag{7}
\]
This has a strong global consequence:

> **Laurent-time reduction.**  Either \(r\) is constant and \(T\) is
> affine linear, or there are \(a,\alpha,\beta,\gamma\in\mathbf C\),
> \(\beta\gamma\ne0\), and an integer \(k\ge1\) such that
> \[
> T=\alpha+\frac{\beta}{(x-a)^k},
> \qquad
> r=\gamma(x-a)^{k+1}.
> \tag{8}
> \]

Thus every nonconstant cube-\(h\) candidate whose \(r\) has two
distinct roots is excluded.  The remaining cube chart consists only
of constant \(r\) and the single-root pure-power family (8).
This is a reduction, not an exclusion of those residual families.

## 1. Laurent definition of the five functions

Let
\[
 s=g^{1/6}=w+O(w^{-1})
\tag{9}
\]
be the distinguished formal sixth root at \(w=\infty\).  Depression
of \(g\) removes the constant term in \(s-w\), so the inverse
coordinate has the form
\[
 w=w(x,s)=s+O(s^{-1}),\qquad
 w_s=1+O(s^{-2}).
\tag{10}
\]
By (2), after re-expanding in the \(s\)-coordinate there is a unique
Laurent expansion
\[
 \widehat f(x,s):=f(x,w(x,s))
 =\Phi(s)+\sum_{\ell\ge1}A_\ell(x)s^{-\ell}.
\tag{11}
\]
Equivalently,
\[
 A_\ell
 =-\operatorname {Res}_{s=\infty}
 s^{\ell-1}\bigl(\widehat f-\Phi(s)\bigr)\,ds.
\tag{12}
\]
Formula (12), or formal series reversion, shows directly that every
\(A_\ell\) is a polynomial in \(a,b,c,d,q\) with coefficients in the
constant parameter ring
\[
\mathbf Q[\kappa _8,\kappa _7,\kappa _5,\kappa _4,
j,\kappa _2,\kappa _1].
\]
In particular \(A_\ell\in\mathbf C(x)\).

There is also a residue formula which avoids explicitly inverting
\(s(w)\):
\[
 A_\ell=[w^{-1}]\,
 s(w)^{\ell-1}
 \bigl(f(w)-\Phi(s(w))\bigr)s_w(w).
\tag{13}
\]
This is the formula used by the exact verifier.

## 2. The four conserved quantities

At fixed \(s\), the function \(\Phi(s)\) has no \(x\)-dependence.
The chain rule, using \(g=s^6\), gives
\[
\begin{aligned}
[f,g]_{x,w}
 &=g_w\left(\frac{\partial\widehat f}{\partial x}\right)_s\\
 &=6s^5s_w
 \sum_{\ell\ge1}A_\ell'(x)s^{-\ell}.
\end{aligned}
\tag{14}
\]
Because \(s_w=1+O(s^{-2})\), the coefficients of
\(s^4,s^3,s^2,s\) in (14) are triangular, with diagonal entries
\[
 6A_1',\quad6A_2',\quad6A_3',\quad6A_4'.
\]
The change \(s=w+O(w^{-1})\) preserves vanishing of the positive
part.  Hence the coefficients of \(w^4,w^3,w^2,w\) in the bracket
vanish if and only if (4) holds.

Once (4) holds, the constant term of (14) is \(6A_5'\).  Since the
normalized cube-chart Jacobian is
\[
 [f,g]_{x,w}=\frac{\lambda}{r},
\tag{15}
\]
this proves (5).

For comparison with the connected calculation, set all character
constants except \(j\) to zero.  The exact triangular identities
there read
\[
\begin{aligned}
R_4&=I_{10}',&
R_3&=I_{11}',\\
R_2&=I_{12}'+\frac a2R_4,&
R_1&=I_{13}'+\frac b3R_4+\frac a3R_3.
\end{aligned}
\tag{16}
\]
Expanding (14) in \(w\) gives the same identities with
\(6A_1,\ldots,6A_4\) in place of
\(I_{10},\ldots,I_{13}\).  Both sets vanish at
\(a=b=c=d=q=0\), proving (6).

The construction answers one structural question in the cube chart:
the seven upper constants do not destroy the four first integrals.
They merely deform their polynomial formulas.  The invariant
definition (11) is substantially shorter than those expanded
formulas.

## 3. Classification of the rational time

Put \(T=6A_5\).  Equation (7) says that \(T'\) has no finite zero.

Suppose first that \(T\) is a polynomial.  A polynomial of degree at
least two has a finite critical point, so \(T\) is affine linear.
Equation (7) then makes \(r\) constant.

Now suppose that \(T\) has finite poles.  Let its degree as a map
\(\mathbf P^1_x\to\mathbf P^1_T\) be \(D\), and suppose it has \(s\)
distinct finite poles, of orders \(m_1,\ldots,m_s\).
There is no ramification at a finite nonpole, since \(T'\) has no
finite zero.

The point at infinity cannot also be a pole.  If its pole order were
\(m_\infty\), all ramification would occur at the poles and would
contribute
\[
 \sum_{i=1}^s(m_i-1)+(m_\infty-1)
 =D-s-1<2D-2,
\]
contrary to Riemann--Hurwitz.

Thus \(T(\infty)\) is finite.  Let \(e_\infty\) be the local degree at
infinity.  Riemann--Hurwitz now gives
\[
 (D-s)+(e_\infty-1)=2D-2,
\qquad\text{so}\qquad
 e_\infty=D+s-1.
\tag{17}
\]
Since \(e_\infty\le D\), one has \(s=1\) and
\(e_\infty=D\).  Hence \(T-T(\infty)\) has one pole of order \(D\)
and one zero of order \(D\), at infinity.  Therefore
\[
 T=\alpha+\frac{\beta}{(x-a)^k}
\]
with \(k=D\ge1\).  Differentiating and comparing with (7) gives
\[
 r=-\frac{\lambda}{k\beta}(x-a)^{k+1}.
\tag{18}
\]
This proves (8).

The conclusion is sharp at the level of the terminal equation:
for example, \(r=x^2\) admits the rational primitive
\[
 T=-\frac{\lambda}{x}.
\]
Excluding the residual pure-power and constant-\(r\) charts therefore
requires polynomial descent or a further use of the four conserved
levels; the rational-time equation alone cannot do it.

## Scope

This note does not prove the \((9,6)\) case or the plane Jacobian
conjecture.  It replaces the previously unspecified full lower
cube-\(h\) system by four canonical Laurent levels and reduces the
possible polynomial \(r\) to two sharply defined families.  The next
problem is the descent analysis at the single root in (8), together
with the polynomial coefficient curve when \(r\) is constant.
