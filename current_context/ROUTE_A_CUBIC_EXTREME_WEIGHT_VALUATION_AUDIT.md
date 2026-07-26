# Route A: cubic extreme weights and the two boundary valuations

Date: 25 July 2026

## Outcome

Let
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v),\qquad
K=\operatorname {Frac}B=\mathbf C(s,w),\qquad s=uv,
\]
with hyperbolic weights
\[
\operatorname {wt}(u)=2,\qquad
\operatorname {wt}(v)=-2,\qquad
\operatorname {wt}(w)=1.
\]

The extreme-weight and degree-three program has one exact positive
conclusion and one exact limitation.

> **Two-boundary cubic rigidity theorem.**  Suppose a degree-three pair
> has been reduced by polynomial target symplectic transformations to
> the invariant resonant form
> \[
> P=wF(s),\qquad Q=vH(s),
> \]
> and its bracket equals \(1\) on both retained components
> \(D=V(u,w)\) and \(H_\infty=V(1+uv,w)\).  Then, up to a symplectic
> target scaling,
> \[
> P=w,\qquad Q=-v(1+2uv).
> \]
> Its global bracket is
> \[
> 1+6uv+6u^2v^2,
> \]
> so it is not a Darboux pair.

Thus every degree-three Darboux pair that admits a finite triangular
extreme-weight reduction to the resonant invariant family is excluded.

The missing reduction cannot be replaced by a direct bound on the raw
top and bottom weights.  Reversible target shears produce degree-three
maps with arbitrarily distant commuting extremes while preserving both
boundary extensions exactly.  The cubic inequality \(ef\le3\) applies
to the stabilized valued target field after all cancellations, not to
the first displayed homogeneous terms.

Consequently a surviving cubic Darboux pair must be
**triangularly irreducible at an extreme boundary**.  Its strict
commuting extreme terms must be coprime powers \(Z^m,Z^n\) with
\(m,n\ge2\); otherwise one target shear lowers the weight span.  This is
the precise unresolved cusp-at-infinity case.

## 1. Homogeneous pieces and their brackets

Every homogeneous rational function of weight \(a\) is
\[
w^a f(s),\qquad f(s)\in\mathbf C(s).
\]
The polynomial pieces in \(B\) are more restricted.  For \(n,h\ge0\),
\[
\begin{aligned}
B_{2n}&=u^n\mathbf C[s]
=w^{2n}(1+s)^{-n}\mathbf C[s],\\
B_{2n+1}&=u^nw\mathbf C[s]
=w^{2n+1}(1+s)^{-n}\mathbf C[s],\\
B_{-2h}&=v^h\mathbf C[s]
=w^{-2h}s^h(1+s)^h\mathbf C[s],\\
B_{1-2h}&=v^hw\mathbf C[s]
=w^{1-2h}s^h(1+s)^h\mathbf C[s].
\end{aligned}
\tag{1}
\]
These formulas record both boundary-corner conditions \(s=0,-1\).

In the \((s,w)\)-chart,
\[
\{R,T\}=w^2(R_sT_w-R_wT_s).
\tag{2}
\]
Therefore
\[
\boxed{
\{w^af(s),w^bg(s)\}
=
w^{a+b+1}\left(bf'(s)g(s)-af(s)g'(s)\right).
}
\tag{3}
\]

Let \(P_{\max},Q_{\max}\) be the top nonzero components of a Darboux
pair.  If their bracket has positive weight, it must vanish, since
\(\{P,Q\}=1\) has only weight zero.  The analogous statement holds for
the bottom components when their bracket has negative weight.

For nonzero weights \(a,b\), equation
\[
\{w^af,w^bg\}=0
\tag{4}
\]
is equivalent to
\[
b\,d\log f=a\,d\log g.
\tag{5}
\]
Put \(\delta=\gcd(|a|,|b|)\), \(a=\delta m\),
\(b=\delta n\), with signed coprime \(m,n\).  Divisors on
\(\mathbf P^1_s\) show that there is \(h(s)\in\mathbf C(s)\) and
nonzero constants \(c,d\) such that
\[
w^af=c\left(w^\delta h(s)\right)^m,\qquad
w^bg=d\left(w^\delta h(s)\right)^n.
\tag{6}
\]
This is the exact homogeneous centralizer statement needed at either
strict extreme.

If \(m,n>0\) and one exponent is \(1\), a polynomial target shear
cancels the larger extreme power.  If the pair is triangularly reduced,
then either the boundary has only one pole, or the coprime exponents in
(6) satisfy
\[
m,n\ge2.
\tag{7}
\]

## 2. What degree three says at a boundary

Let \(\nu_0\) and \(\nu_\infty\) be the valuations
\[
\nu_0(w)=1,\qquad \nu_\infty(w)=-1,\qquad
\nu_0(s)=\nu_\infty(s)=0.
\tag{8}
\]
Both have residue field \(\mathbf C(s)\).

For \(L=\mathbf C(P,Q)\subset K\) with \([K:L]=3\), restriction of
either valuation gives
\[
e_\bullet f_\bullet\le3,
\tag{9}
\]
where
\[
e_\bullet=[\nu_\bullet(K^\times):\nu_\bullet(L^\times)],
\qquad
f_\bullet=
[\mathbf C(s):\kappa(\nu_\bullet|_L)].
\]
Thus only
\[
(e,f)=(1,1),(1,2),(1,3),(2,1),(3,1)
\tag{10}
\]
can occur.

The important caution is that \(e\) and \(f\) belong to the full valued
field \(L\).  Cancellations between polynomials in \(P,Q\) can reveal
new values and new residue functions.  Hence the gcd of the two first
visible extreme weights need not equal \(e\), and the common coefficient
\(h(s)\) in (6) need not generate the residue field.

## 3. Exact equality in the resonant invariant family

Now take
\[
P=wF(s),\qquad
Q=vH(s)=\frac{s(1+s)H(s)}{w^2},
\tag{11}
\]
with nonzero \(F,H\in\mathbf C[s]\).  Put
\[
\mathcal R(s)=P^2Q=s(1+s)F(s)^2H(s).
\tag{12}
\]
Then
\[
L=\mathbf C(P,Q)=\mathbf C(P,\mathcal R(s)).
\]
Once a root \(s\) of (12) is chosen,
\[
w=\frac{P}{F(s)}.
\]
Consequently
\[
\boxed{
[K:L]=\deg\mathcal R
=2+2\deg F+\deg H.
}
\tag{13}
\]

At both valuations (8), \(P\) has value \(\pm1\).  Hence
\[
e_0=e_\infty=1.
\tag{14}
\]
Every value-zero residue is rational in \(\mathcal R(s)\), and therefore
\[
\kappa(\nu_0|_L)
=\kappa(\nu_\infty|_L)
=\mathbf C(\mathcal R(s)),
\qquad
f_0=f_\infty=\deg\mathcal R.
\tag{15}
\]
Thus (9) is an equality at both boundaries in this family.

If the field degree is three, (13) gives
\[
2\deg F+\deg H=1.
\]
Therefore
\[
F=f\in\mathbf C^\times,\qquad
H=h_0+h_1s,\quad h_1\ne0.
\tag{16}
\]

## 4. The retained jets force the cubic seed

Write
\[
C(s)=s(1+s)H(s).
\]
Formula (2) gives
\[
\{P,Q\}=-2C(s)F'(s)-C'(s)F(s).
\tag{17}
\]
At \(D\), where \(s=0\),
\[
\{P,Q\}|_D=-F(0)H(0).
\tag{18}
\]
At \(H_\infty\), where \(s=-1\),
\[
\{P,Q\}|_{H_\infty}=F(-1)H(-1).
\tag{19}
\]
Requiring both retained components to have bracket \(1\), and using
(16), yields
\[
fh_0=-1,\qquad f(h_0-h_1)=1.
\]
Hence
\[
H(s)=-\frac{1+2s}{f}.
\tag{20}
\]
The symplectic target scaling
\[
(P,Q)\longmapsto(f^{-1}P,fQ)
\]
gives the unique normalized seed
\[
P_0=w,\qquad Q_0=-v(1+2s).
\tag{21}
\]
Finally,
\[
\boxed{
\{P_0,Q_0\}
=
\left[s(1+s)(1+2s)\right]'
=1+6s+6s^2\ne1.
}
\tag{22}
\]
This proves the two-boundary cubic rigidity theorem.

## 5. Arbitrarily distant extremes with the same cubic field

The raw extreme weights do not measure \(e\) or \(f\).  Starting from
(21), let \(m,n\ge2\) and apply two target symplectic shears:
\[
\begin{aligned}
P_m&=P_0+Q_0^m,\\
Q_{m,n}&=Q_0+P_m^n.
\end{aligned}
\tag{23}
\]
Then
\[
\mathbf C(P_m,Q_{m,n})
=\mathbf C(P_0,Q_0),
\qquad
\{P_m,Q_{m,n}\}=\{P_0,Q_0\}.
\tag{24}
\]
The field degree remains three, and both boundary pairs remain
\[
(e,f)=(1,3).
\tag{25}
\]

Nevertheless the bottom weights include
\[
-2m,\qquad -2mn,
\]
and the top weights include
\[
1,\qquad n.
\]
Their initial forms are commuting powers of the same homogeneous
element.  At the bottom, the normalized common generator is
\[
Q_0^m
=w^{-2m}\left[-s(1+s)(1+2s)\right]^m.
\]
Its displayed coefficient has degree \(3m\), arbitrarily large, even
though the stabilized residue extension still has degree three.  The
inverse shears recover (21), and it is only after those cancellations
that the value \(\pm1\) and cubic residue function become visible.

This exact family proves:

> **Raw-extreme no-go.**  Neither the extreme weights, their gcds, nor
> their first common rational coefficient can be bounded directly from
> \([K:L]=3\) and \(ef\le3\).

## 6. Precise remaining target

The successful route would be a finite, boundary-regular SAGBI theorem:

1. use (3)--(6) to cancel every divisible extreme power by target
   symplectic shears;
2. prove that a triangularly reduced cusp with coprime exponents
   \(m,n\ge2\) is incompatible with the polynomial cones (1), the two
   boundary budgets (9), and the Darboux equation; and
3. conclude that the pair reaches (11), where (13)--(22) give the
   contradiction.

Step 2 is not supplied by the valuation inequality alone.  The common
leading term has residue field \(\mathbf C\); the nonconstant residue
parameter can first appear after a lower-weight cancellation.  Any
argument that identifies \(h(s)\) in (6) directly with the residue
generator skips this key-polynomial step.

The present theorem therefore closes every cubically finite pair whose
extreme-weight reduction terminates in the resonant invariant family,
and it isolates the only honest remaining alternative: a
triangularly irreducible cusp at \(w=0\) or \(w=\infty\).
