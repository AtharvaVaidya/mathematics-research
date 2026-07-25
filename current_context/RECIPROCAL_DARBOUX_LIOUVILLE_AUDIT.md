# Reciprocal Darboux powers and the exact Liouville obstruction

Date: 25 July 2026

This note audits the reciprocal-coordinate differential identities for the
universal radial \((2,3)\) outer pair and extracts the strongest field
descent consequence that follows from them alone.  The result is a
non-eliminative equivalence:

\[
\text{the whole comparison branch descends}
\quad\Longleftrightarrow\quad
\Xi^5\text{ descends}
\quad\Longleftrightarrow\quad
T^{5k+2}\text{ descends}.
\]

An exact completed-local model at the maximally ramified cusp then shows
that neither Darboux power is forced to descend by the Wronskian,
symplecticity, or the local ramification signature.  Thus the remaining
step really must use the global normalized sheet and the Newton support
of a polynomial completion.

Work over an algebraically closed field \(\Bbbk\) of characteristic zero.
Put
\[
m\ge1,\qquad
p=2m+1,\qquad q=3m+1,\qquad N=5m+2.
\tag{1}
\]
Let
\[
A(t)=t^pU(t^{-1}),\qquad B(t)=t^qV(t^{-1})
\tag{2}
\]
be the reversed endpoint polynomials.  We assume
\[
\deg A=p,\quad \deg B=q,\quad
A(0)B(0)[t^p]A[t^q]B\ne0.
\tag{3}
\]

## 1. Sign and constant audit

Use
\[
t=w^{-1},\qquad \xi=zw^m,
\qquad z=\xi t^m,\qquad w=t^{-1}.
\tag{4}
\]
The radial outer pair becomes
\[
P_0=\xi^2A(t),\qquad Q_0=\xi^3B(t).
\tag{5}
\]
The source two-form transforms as
\[
\frac{z^4}{w^3}\,dz\wedge dw
=-\xi^4t^{5m+1}\,d\xi\wedge dt
=-\xi^4t^{N-1}\,d\xi\wedge dt.
\tag{6}
\]
On the other hand,
\[
dP_0\wedge dQ_0
=\xi^4(2AB'-3A'B)\,d\xi\wedge dt.
\tag{7}
\]
Consequently the bracket equation is exactly
\[
\boxed{\ 3A'(t)B(t)-2A(t)B'(t)=t^{N-1}.\ }
\tag{8}
\]
There is no undetermined nonzero scalar after the normalization in (6).

Now define
\[
S=\xi^5,\qquad Y=t^N.
\tag{9}
\]
A direct calculation, using (8), gives the two exact identities
\[
\boxed{
3Q_0\,dP_0-2P_0\,dQ_0
=\xi^5t^{N-1}dt
=\frac SN\,dY ,
\ }
\tag{10}
\]
and
\[
\boxed{
dP_0\wedge dQ_0
=-\frac1{5N}\,dS\wedge dY.
\ }
\tag{11}
\]
Thus one compatible Darboux convention is
\[
\mathsf q=\frac S5,\qquad \mathsf p=-\frac YN,
\qquad dP_0\wedge dQ_0=d\mathsf q\wedge d\mathsf p.
\tag{12}
\]
In particular, the sign in (11) is negative when the ordered form is
\(dS\wedge dY\).

## 2. Darboux-power descent theorem

Let \(K/\Bbbk\) be a finitely generated function field with constant
field \(\Bbbk\), and let \(M/K\) be a finite separable function-field
extension.  Suppose that nonconstant \(T,\Xi\in M^\times\) and
\(P,Q\in K\) satisfy
\[
P=\Xi^2A(T),\qquad Q=\Xi^3B(T).
\tag{13}
\]
Set
\[
S=\Xi^5,\qquad Y=T^N,\qquad
\alpha=3Q\,dP-2P\,dQ\in\Omega^1_{K/\Bbbk}.
\tag{14}
\]
Substitution into (10) gives
\[
\alpha=\frac SN\,dY
\quad\text{in }\Omega^1_{M/\Bbbk}.
\tag{15}
\]

> **Darboux-power descent theorem.**
> Under (1)--(3) and (13),
> \[
> \boxed{\quad
> \Xi,T\in K
> \quad\Longleftrightarrow\quad
> S=\Xi^5\in K
> \quad\Longleftrightarrow\quad
> Y=T^N\in K.
> \quad}
> \tag{16}
> \]

Here is the differential step.  If \(S\in K\), then (15) says
\(dY\in\Omega^1_{K/\Bbbk}\).  Since \(M/K\) is finite separable,
\[
\Omega^1_{M/\Bbbk}
\simeq M\otimes_K\Omega^1_{K/\Bbbk}.
\]
If \(d=[M:K]\), trace commutes with the universal derivation, so
\[
d\!\left(\frac{\operatorname {Tr}_{M/K}Y}{d}\right)=dY.
\]
The kernel of \(d:M\to\Omega^1_{M/\Bbbk}\) is \(\Bbbk\).  Hence
\(Y-\operatorname {Tr}(Y)/d\in\Bbbk\), and therefore \(Y\in K\).

Conversely, if \(Y\in K\), then \(dY\ne0\).  Both \(\alpha\) and \(dY\)
belong to the \(K\)-vector space \(\Omega^1_{K/\Bbbk}\), while (15)
says that \(\alpha=(S/N)dY\).  Applying a \(K\)-linear functional that
is nonzero on \(dY\) gives \(S\in K\).  This proves
\[
S\in K\quad\Longleftrightarrow\quad Y\in K.
\tag{17}
\]

It remains to remove the fifth and \(N\)-th roots.  Work in a normal
closure and let \(\sigma\) fix \(K\).  From \(S,Y\in K\),
\[
\sigma(\Xi)=\varepsilon\Xi,\quad \varepsilon^5=1,
\qquad
\sigma(T)=\eta T,\quad \eta^N=1.
\tag{18}
\]
The first equation in (13) yields
\[
\varepsilon^2A(\eta T)=A(T).
\tag{19}
\]
Since \(T\) is nonconstant, it is transcendental over \(\Bbbk\).
Comparison of the nonzero constant coefficient in (19) gives
\(\varepsilon^2=1\), and hence \(\varepsilon=1\).  Comparison of the
nonzero top coefficient gives \(\eta^p=1\).  But
\[
\gcd(p,N)=\gcd(2m+1,5m+2)=1,
\tag{20}
\]
so \(\eta=1\).  Every \(K\)-automorphism fixes \(\Xi,T\), proving
\(\Xi,T\in K\).  The reverse implications in (16) are immediate.

The same proof over an intermediate field gives a stronger primitive
generator statement.  Apply the theorem over \(K(S)\), where \(S\)
belongs to the base by construction, and over \(K(Y)\), where \(Y\)
does.  It follows that
\[
\boxed{\qquad
K(\Xi,T)=K(S)=K(Y).
\qquad}
\tag{20a}
\]
Thus in a normal closure the four elements \(\Xi,T,S,Y\) have the same
stabilizer.  Passing to the fifth and \(N\)-th powers loses no field
information once the genuine endpoint support and the Liouville identity
are retained.

This sharpens the invariant criterion in
`RADIAL_INVARIANT_FIELD_DESCENT.md`: a global argument need not descend
\(\Xi\) itself.  It is enough to descend either of the canonical
Darboux powers \(S\) or \(Y\).

## 3. The exact one-variable correspondence

Suppose \((\xi,t)\) and \((\widetilde\xi,u)\) give the same \(P,Q\).
Put
\[
R(t)=\frac{B(t)^2}{A(t)^3},\qquad
c(t,u)=\frac{B(t)A(u)}{B(u)A(t)}.
\tag{21}
\]
Then
\[
R(t)=R(u),\qquad
\frac{\widetilde\xi}{\xi}=c(t,u).
\tag{22}
\]
Differentiating \(R\) and using (8) gives
\[
R'(t)=-\frac{t^{N-1}B(t)}{A(t)^4}.
\tag{23}
\]
On every normalization component of \(R(t)=R(u)\), equations
(22)--(23) imply
\[
\boxed{\quad
c(t,u)^5\,d(u^N)=d(t^N).
\quad}
\tag{24}
\]
Thus equality of the Liouville forms is not an additional generic
constraint on the outer correspondence: it is exactly the cotangent
multiplier of the one-variable inverse correspondence of \(R\).
This explains why differential algebra alone does not select the
distinguished sheet.

For the exact \(m=1\) endpoint pair,
\[
\begin{aligned}
A(t)&=t^3+t^2+\frac6{25}t+\frac9{250},\\
B(t)&=t^4+\frac23t^3+\frac6{25}t^2
      +\frac{36}{875}t+\frac{18}{4375},
\end{aligned}
\tag{25}
\]
one has
\[
3A'B-2AB'=t^6,\qquad
R(0)=\frac{160}{441},
\tag{26}
\]
and
\[
B(t)^2-\frac{160}{441}A(t)^3
=-\frac{t^7(800t^2+195t+36)}{2205}.
\tag{27}
\]
The map \(R:\mathbf P^1\to\mathbf P^1\) has degree \(9\), with the
expected ramification-\(7\) point at \(t=0\).  The polynomial
\[
B(t)^2-rA(t)^3\in\Bbbk(r)[t]
\]
is irreducible of degree \(9\): it is the generic-fiber polynomial of
the degree-\(9\) rational map \(R\).  Thus the generic inverse
correspondence already supplies nontrivial algebraic \(S,Y\) satisfying
(10)--(11).  It has no normalized global identity sheet, so it is a
countermodel only to a differential-only descent claim.

## 4. A genuine-endpoint local cusp countermodel

There is a sharper completed-local obstruction that retains the genuine
endpoint pair and the exact ramification signature.

Choose a formal square root
\[
H(t)^2=A(t)
\tag{28}
\]
at \(t=0\), and put
\[
r(t)=\frac{B(t)}{H(t)^3},\qquad r_0=r(0).
\tag{29}
\]
Equation (8) gives
\[
r'(t)=-\frac{t^{N-1}}{2A(t)^{5/2}}.
\tag{30}
\]
Therefore
\[
u=r(t)-r_0=t^N\cdot(\text{a unit in }\Bbbk[[t]]).
\tag{31}
\]
Let
\[
K=\Bbbk(x)((u)),\qquad M=\Bbbk(x)((t)),
\tag{32}
\]
where \(u\) is embedded by (31).  Then \(M/K\) is totally ramified of
degree \(N\).  Define
\[
T=t,\qquad \Xi=\frac{x}{H(t)},\qquad
P=x^2,\qquad Q=x^3(r_0+u).
\tag{33}
\]
These satisfy the genuine endpoint equations
\[
P=\Xi^2A(T),\qquad Q=\Xi^3B(T)
\tag{34}
\]
with \(P,Q\in K\).  Moreover,
\[
3Q\,dP-2P\,dQ=-2x^5\,du
=\Xi^5T^{N-1}dT.
\tag{35}
\]

Neither Darboux power descends in this model.

First, \(\Xi\notin K\), since otherwise the birational endpoint lemma
would give \(T\in K\), contradicting \([M:K]=N\).  If
\(S=\Xi^5\) belonged to \(K\), then \(K(\Xi)/K\) would have degree
dividing \(5\) and also dividing \(N\).  Since
\[
\gcd(5,N)=1,
\]
this would force \(\Xi\in K\), again a contradiction.

Second, \(Y=T^N\notin K\).  If \(T^N\in K\), the extension would be the
degree-\(N\) Kummer extension generated by \(T\), so every
\(T\mapsto\zeta T\), \(\zeta^N=1\), would fix \(u=r(T)-r_0\).  Thus
\(r(\zeta T)=r(T)\), and (30) would imply
\(A(T)^5\in\Bbbk((T^N))\).  Since \(A(0)\ne0\), this forces
\(A(\zeta T)=A(T)\) for every \(\zeta^N=1\).  But
\[
0<\deg A=p<N,
\]
which is impossible.

Finally put
\[
W=T^{-1},\qquad Z=\Xi T^m.
\tag{36}
\]
At \(u=0\), normalized in \(M\),
\[
\boxed{\qquad
(e,\nu(Z),\nu(W))=(N,m,-1).
\qquad}
\tag{37}
\]
Thus the Wronskian, the exact Liouville identity, the genuine endpoint
polynomials, and the sole allowed ramification signature are all
compatible with failure of descent in a completed neighborhood of the
cusp divisor.

## 5. What remains global

The local model does not have the extra global datum present in the
Jacobian problem: the selected branch must also be the sheet normalized
to the identity at the unramified \(t=\infty\) end, and \(P,Q\) must come
from a bounded polynomial Keller completion in the original plane.

Consequently the precise remaining bridge can be stated in either of two
equivalent forms:

> **Global Darboux-power section lemma.**  For the comparison component
> selected by the normalized infinity germ of a bounded polynomial
> Keller completion, either
> \[
> T^N\in\Bbbk(z,w)
> \qquad\text{or, equivalently,}\qquad
> \Xi^5\in\Bbbk(z,w).
> \]

By (16), this lemma is already the full field-descent statement.  The
completed-local construction (28)--(37) proves that it cannot follow
from a calculation at the cusp divisor, from the valuation signature,
or from the Liouville form alone.  A successful proof must connect the
normalized infinity sheet to the cusp globally, using the original
Newton support, component incidence, or a degree-lowering theorem.

The signs, constants, exact \(m=1\) endpoint, ramification order, and
non-descent diagnostics are checked in
`verify_reciprocal_darboux_liouville.py`.
