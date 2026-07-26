# Exact correction audit for the quadratic and cubic lower-tier chains

Date: 25 July 2026

## Outcome

The invalid boundary-Euler lemma can be replaced on the pure binary
faces:
\[
B^2,\qquad B^3
\]
both have a nonzero exact first-lower double pole before any allowed
lower target or first-coordinate term can enter.

It cannot be replaced uniformly on the pure \(C\)-divisible faces
when arbitrary lower target tiers are allowed:
\[
\boxed{
AC+\lambda B,
\qquad
ABC+\lambda B^2.
}
\tag{1}
\]
In each chain the lower target monomial occurs in the same normalized
\(x^{-1}\)-sector and at the same ordinary drop \(m+4\) as the
first-lower seed.  An explicit allowed value of \(\lambda\) cancels
the entire \(t^{-2}\) forcing.  After that tuning the normalized
\(x^{-1}\)-equation admits a polynomial coefficient solution.

Consequently:

- the arbitrary-affine quadratic theorem is not currently proved on
  the \(AC+\lambda B\) chain;
- the arbitrary-lower-tier cubic theorem is not currently proved on
  the \(ABC+\lambda B^2\) chain;
- the cubic theorem additionally depends on the open quadratic chain
  when a quadratic \(AC\)-face leads above its surviving cubic
  \(C\)-face.

These are proof gaps, not constructed Keller pairs or counterexamples
to the final conclusions.

## 1. Common exact calculation

For a pure face
\[
A^dB^{n-d}C^c
\]
on a resonant sector \(\gamma_I=x^It^J\), the exact first-lower
calculation gives
\[
\begin{aligned}
D_U&=(I+1)(c-d-n),\\
D_V&=-\frac{(17I+15)(c-d-n)}{c+4n},\\
\Omega_{n,c,d,I}
&=-\frac{70}{3}D_U
+\left(-\frac{35n}{6}+\frac{7d}{30}\right)D_V.
\end{aligned}
\tag{2}
\]
Here \(\Omega\) is the coefficient of the normalized
\(x^{-1}t^{-2}\)-forcing.

Deleting one \(C\) gives an allowed target face of degree one less.
Its monomial with binary polynomial \(t^{d-1}\) has exactly the same
support as the first-lower target slice and contributes \(hD_V\) to
the double-pole coefficient.  Thus
\[
\boxed{
h_{\rm cancel}=-\frac{\Omega}{D_V}
}
\tag{3}
\]
whenever \(d\ge1\) and \(D_V\ne0\).

The graph-coefficient operator in the normalized \(x^{-1}\)-sector is
\[
\mathcal L_{-1}(\psi)
=-(8n+2c)\psi'
-\frac{10n+2d}{t}\psi.
\tag{4}
\]
For \(q\ge-1\),
\[
\mathcal L_{-1}(t^{q+1})
=-\left((8n+2c)(q+1)+10n+2d\right)t^q.
\tag{5}
\]
Every multiplier is nonzero.  Hence \(\mathcal L_{-1}\) maps
\(\mathbb C[t]\) bijectively onto
\(t^{-1}\mathbb C[t]\).  Once the double pole is tuned away, every
remaining Laurent-polynomial source on this slice has a polynomial
coefficient solution.  This is a local recurrence statement, not a
construction of a globally compatible polynomial graph.

## 2. Quadratic target: \(AC+\lambda B\)

For the pure \(AC\)-ray,
\[
(n,c,d)=(1,1,1),
\qquad
I=5k+5,\quad J=k,\quad m=6k+3.
\tag{6}
\]
Equations (2) give
\[
\Omega=\frac{14(23k+30)}{15},
\qquad
D_V=17k+20.
\tag{7}
\]
The affine \(B\)-term lies exactly at drop
\[
(5m+21)-(4m+17)=m+4.
\tag{8}
\]
Its normalized coefficient may be chosen as
\[
\boxed{
\lambda
=-\frac{14(23k+30)}{15(17k+20)}.
}
\tag{9}
\]
Then \(\Omega+\lambda D_V=0\).  If the remaining affine coefficients
are zero, the whole first-lower inhomogeneous source vanishes on the
pure characteristic.  More generally, after the double pole is
removed, (4)--(5) solve the remaining normalized
\(t^{-1}\mathbb C[t]\) source with a polynomial \(\psi(t)\).
If \(\mu\) is the coefficient of \(AC\) and \(\ell_B\) the
coefficient of \(B\) in the original target coordinates, then
\(q_6/p_5=5/6\) converts (9) to
\[
\boxed{
\frac{\ell_B}{\mu}
=-\frac{7(23k+30)}{9(17k+20)}.
}
\tag{9a}
\]

By contrast, the pure binary \(B^2\)-ray has
\[
(n,c,d)=(2,0,0),
\qquad
\Omega=-\frac{35}{12}(I-1)\ne0
\quad(I\ge2).
\tag{10}
\]
Its affine target tier and first-coordinate perturbation enter
strictly after the first-lower pole.  The descending binary faces,
the mixed \(AC/BC\) negative-tail case, the nonresonant \(BC\)-face,
the \(C^2\) product argument, and the constant-graph calculation are
unchanged.

Therefore the quadratic theorem is currently open only on the tuned
pure \(AC+B\) chain identified above.

## 3. Cubic target: \(ABC+\lambda B^2\)

For the pure \(ABC\)-ray,
\[
(n,c,d)=(2,1,1),
\qquad
I=18k+15,\quad J=7k+5,\quad m=25k+18.
\tag{11}
\]
Equations (2) give
\[
\Omega=\frac{14(67k+65)}{15},
\qquad
D_V=4(17k+15).
\tag{12}
\]
The lower \(B^2\)-term lies exactly at drop
\[
(9m+38)-(8m+34)=m+4.
\tag{13}
\]
Its normalized coefficient may be chosen as
\[
\boxed{
\lambda
=-\frac{7(67k+65)}{30(17k+15)}.
}
\tag{14}
\]
Again \(\Omega+\lambda D_V=0\), and (4)--(5) show that the remaining
normalized \(x^{-1}\)-equation passes the polynomial-coefficient
test.
If \(\mu\) is the coefficient of \(ABC\) and \(\nu\) the coefficient
of \(B^2\) in the original target coordinates, the corresponding
ratio is
\[
\boxed{
\frac{\nu}{\mu}
=-\frac{7(67k+65)}{36(17k+15)}.
}
\tag{14a}
\]

The pure binary \(B^3\)-ray instead has
\[
(n,c,d)=(3,0,0),
\qquad
\Omega=-\frac{35}{8}(I-1)\ne0.
\tag{15}
\]
Its quadratic target tier arrives strictly after the pole.  The
descending binary and \(CA^2\) faces, mixed \(ABC/B^2C\) negative
tail, nonresonant \(B^2C,C^2(A,B),C^3\) faces, and constant-graph
calculation remain valid.

There is a second logical dependency.  When the cubic face is
nonresonant and a lower quadratic \(AC\)-face leads, Section 4 of the
cubic note cites the full quadratic theorem.  That citation does not
close the tuned \(AC+B\) chain in Section 2.  Thus a corrected cubic
statement must list both (9) and (14) as open lower-tier families.

## 4. Minimal correction banners

For the quadratic note:

> **Correction (25 July 2026).** The pure-face boundary-Euler
> argument is invalid.  The exact first-lower calculation re-closes
> the pure binary \(B^2\)-ray, but an allowed affine \(B\)-coefficient
> can cancel the first-lower pole on the pure \(AC\)-ray at the exact
> drop \(m+4\).  Therefore the arbitrary-affine quadratic conclusion
> is not currently proved on the \(AC+B\) chain.  The descending,
> mixed negative-tail, nonresonance, product, and constant-graph
> certificates remain valid.

For the cubic note:

> **Correction (25 July 2026).** The pure-face boundary-Euler
> argument is invalid.  The exact first-lower calculation re-closes
> the pure binary \(B^3\)-ray, but a lower \(B^2\)-coefficient can
> cancel the pole on the pure \(ABC\)-ray at the exact drop \(m+4\).
> The proof also cites the open quadratic \(AC+B\) chain when a lower
> quadratic face leads.  Therefore the arbitrary-lower-tier cubic
> conclusion is not currently proved on these two chains.  All
> descending, mixed negative-tail, nonresonance, and constant-graph
> certificates remain valid.

The accompanying exact verifier is
`verify_weighted_lift_quadratic_cubic_lower_tier_correction_audit.py`.
