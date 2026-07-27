# Standard-system Sylvester-remainder correction audit

Date: 26 July 2026

## Outcome

The Laurent obstruction in equation (34) of
`STANDARD_SYSTEM_WEIGHTED_ESCAPE.md` is correct, but the determinant
conclusion formerly drawn from it is not.

For
\[
 P_\epsilon=R^a+\epsilon T,
\]
the first nonpolynomial term of \(P_\epsilon^{\,b/a}\) occurs at the
binomial index
\[
 \ell_0=\left\lfloor\frac ba\right\rfloor+1.
\]
That does **not** imply that the derivative Sylvester remainder of
\((P_\epsilon)_X\) and the polynomial truncation of
\(P_\epsilon^{\,b/a}\) first occurs at order \(\epsilon^{\ell_0}\).
Differentiating the earlier polynomial binomial terms already produces
an order-\(\epsilon\) remainder relative to the fixed special-fiber
quotient.

The smallest coprime case \(a=2,b=3\) makes the distinction exact.
Put
\[
 P_\epsilon=R^2+\epsilon T,\qquad
 Q_\epsilon=R^3+\frac32\epsilon RT .
\tag{1}
\]
The displayed \(Q_\epsilon\) contains every polynomial binomial term
strictly before the first Laurent obstruction
\(\frac38\epsilon^2T^2/R\).  Nevertheless, with
\[
 A=(P_\epsilon)_X,\qquad B=(Q_\epsilon)_X,
\]
one has the exact identity
\[
 \boxed{\;
 B-\frac32RA=\frac32\epsilon R'T .
 \;}
\tag{2}
\]
Thus the derivative remainder is already linear in \(\epsilon\).

There is a general generic formula for this particular first
polynomial binomial truncation.  It is not a replacement contact
formula for an arbitrary standard-system arc: special choices of
\(T\), repeated roots, earlier jets, or later polynomial corrections
can raise the contact or make the resultant vanish identically.

## 1. The division-free derivative remainder

Let
\[
 q=\left\lfloor\frac ba\right\rfloor,\qquad
 r=b-aq,\qquad 1\le r<a,
\tag{3}
\]
and retain every polynomial binomial term before the first Laurent
pole:
\[
\begin{aligned}
P_\epsilon&=R^a+\epsilon T,\\
Q_q&=\sum_{\ell=0}^{q}
\binom{b/a}{\ell}
\epsilon^\ell R^{\,b-a\ell}T^\ell .
\end{aligned}
\tag{4}
\]
Put
\[
A=(P_\epsilon)_X,\qquad B=(Q_q)_X.
\]
The binomial recurrence
\[
a(\ell+1)\binom{b/a}{\ell+1}
=(b-a\ell)\binom{b/a}{\ell}
\tag{5}
\]
gives the exact polynomial identity
\[
\boxed{
B-H_\epsilon A
=\binom{b/a}{q}r\epsilon^q
R^{\,r-1}R'T^q,
}
\tag{6}
\]
where
\[
H_\epsilon
=\sum_{\ell=1}^{q}
\ell\binom{b/a}{\ell}
\epsilon^{\ell-1}R^{\,b-a\ell}T^{\ell-1}.
\tag{7}
\]
No division by \(R\), \(T\), or \(A\) is used.  Indeed,
the \(H_\epsilon\epsilon T'\) terms cancel the \(T'\)-terms
in \(B\), while (5) telescopes all \(R'\)-terms except the
\(\ell=q\) endpoint.

Thus the derivative remainder is generically visible at order
\(\epsilon^q\), one order before the first nonpolynomial binomial term
at \(\epsilon^{q+1}\).

## 2. Generic contact of this truncation

Let \(R\) be monic of degree \(g\), let
\(\deg T\le ga-2\) as in the first normal kernel, and assume
\(R\) is squarefree and
\[
\gcd(T,RR')=1,\qquad \gcd(T',RR')=1.
\tag{8}
\]
These are Zariski-open genericity conditions on \(R,T\).

The degree bounds give
\[
\deg A=ga-1,\qquad \deg B=gb-1,
\]
with leading coefficients independent of \(\epsilon\).  The remainder
on the right of (6) has smaller \(X\)-degree than \(B\).  With the
convention
\[
\operatorname{Res}(F,G)
=\operatorname{lc}(F)^{\deg G}
\prod_{F(\alpha)=0}G(\alpha),
\]
the replacement \(B\mapsto B-H_\epsilon A\) changes the resultant
only by the power
\(\operatorname{lc}(A)^{\deg B-\deg(B-H_\epsilon A)}\).
This is a nonzero constant independent of \(\epsilon\), so it does
not change the contact order.

Multiplicativity of the resultant in the second argument now gives,
again up to a nonzero constant,
\[
\begin{aligned}
\operatorname{Res}(A,B)
\doteq{}&
\epsilon^{q(ga-1)}
\operatorname{Res}(A,R)^{r-1}
\operatorname{Res}(A,R')
\operatorname{Res}(A,T)^q .
\end{aligned}
\tag{9}
\]
At a root of \(R\) or \(R'\), respectively,
\[
A|_{R=0}=\epsilon T',\qquad
A|_{R'=0}=\epsilon T'.
\tag{10}
\]
The hypotheses (8) therefore give
\[
\begin{aligned}
\operatorname{ord}_\epsilon\operatorname{Res}(A,R)&=g,\\
\operatorname{ord}_\epsilon\operatorname{Res}(A,R')&=g-1,\\
\operatorname{ord}_\epsilon\operatorname{Res}(A,T)&=0.
\end{aligned}
\tag{11}
\]
Substitution in (9) yields the exact generic valuation
\[
\boxed{
\operatorname{ord}_\epsilon\operatorname{Res}(A,B)
=q(ga-1)+g(r-1)+(g-1)
=gb-q-1=m-q-1.
}
\tag{12}
\]

This theorem concerns the explicitly defined truncation (4).  It does
not assert that every solution of the reciprocal standard equations
has the same contact.

## 3. The \(a=2,b=3\) specialization

Let \(R\) be monic of degree \(g\), let
\(\deg T\le 2g-2\), and impose (8).  Here \(q=r=1\).

Then \(\deg A=2g-1\).  Resultant row reduction by (2), followed by
multiplicativity, gives, up to a nonzero scalar independent of
\(\epsilon\),
\[
\begin{aligned}
\operatorname{Res}(A,B)
&\doteq
\operatorname{Res}\left(A,\epsilon R'T\right)\\
&\doteq
\epsilon^{\,2g-1}
\operatorname{Res}(A,R')\operatorname{Res}(A,T).
\end{aligned}
\tag{13}
\]
At a root \(\beta\) of \(R'\),
\[
 A(\beta)=\epsilon T'(\beta),
\]
so
\[
 \operatorname{ord}_\epsilon\operatorname{Res}(A,R')=g-1.
\tag{14}
\]
The genericity conditions (8) give
\[
 \operatorname{Res}(A,T)|_{\epsilon=0}
 =\operatorname{Res}(2RR',T)\ne0.
\tag{15}
\]
Consequently
\[
\boxed{\;
\operatorname{ord}_\epsilon\operatorname{Res}(A,B)
=(2g-1)+(g-1)=3g-2=m-2 .
\;} \tag{16}
\]
For \(g=2\) this is \(4\), whereas the invalid inference from the
Laurent index \(\ell_0=2\) would give
\((n-1)\ell_0=6\).  For \(g=3\) it is \(7\), rather than \(10\).

The role of the extra \(g-1\) in (16) is also transparent.  The
order-\(\epsilon\) remainder in (2) contains \(R'\), so it still
vanishes on the critical cluster of the common root.  The deformation
of \(A\) lifts that cluster at one further order for each root of
\(R'\).

## 4. Exact \(g=2\) generic calculation

Take
\[
 R=X^2+r,\qquad
 T=uX^2+vX+w,\qquad r\ne0.
\tag{17}
\]
For (1), direct elimination gives
\[
\begin{aligned}
\operatorname{Res}_X(A,B)
=432\epsilon^4v\bigl(&
4\epsilon^2u^4w-\epsilon^2u^3v^2
+16\epsilon r u^3w-4\epsilon r u^2v^2\\
&-16\epsilon u^2w^2+20\epsilon uv^2w-4\epsilon v^4\\
&+16r^2u^2w-32ruw^2+16rv^2w+16w^3
\bigr).
\end{aligned}
 \tag{18}
\]
Its \(\epsilon^4\)-coefficient is
\[
6912\,v w\bigl((ru-w)^2+rv^2\bigr),
 \tag{19}
\]
which is nonzero on a Zariski-open set.  Hence the generic contact is
exactly four.

## 5. Exact \(g=3\) specialization

Take
\[
 R=X^3+1,\qquad T=X^2+X+1.
\tag{20}
\]
Then
\[
\boxed{\;
\operatorname{Res}_X(A,B)
=\frac{14348907}{2}\,
\epsilon^7(\epsilon^2-12\epsilon+48).
\;}
\tag{21}
\]
In the reciprocal small-case test with
\(\epsilon=\tau^4\), this becomes
\[
\frac{14348907}{2}\,
\tau^{28}(\tau^8-12\tau^4+48).
\tag{22}
\]
The contact is \(28\), not the \(40\) that would follow from the
invalid \((n-1)\ell_0\) rule.

## 6. Correct use of the Laurent obstruction

The term
\[
\binom{b/a}{\ell_0}
R^{\,b-a\ell_0}T^{\ell_0}
\]
still identifies the first binomial term that need not be a
polynomial in \(X\).  It is therefore a valid obstruction in the
reciprocal standard equations.  What it does not determine by itself
is the first contact of the derivative resultant.

Any later use must keep two filtrations separate:

1. the Laurent/polynomiality filtration of
   \(P_\epsilon^{\,b/a}\); and
2. the Euclidean-remainder filtration of
   \((P_\epsilon)_X,(Q_\epsilon)_X\).

The second filtration sees derivatives of all earlier polynomial
terms and can start strictly before the first Laurent pole.
