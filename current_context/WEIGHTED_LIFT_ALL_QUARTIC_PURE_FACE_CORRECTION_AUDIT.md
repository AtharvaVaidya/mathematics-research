# Correction audit for the pure faces in the quartic-pivot theorem

Date: 25 July 2026

> **Later repair.**  The two gaps found here, together with the inherited
> quadratic and cubic chains, are now closed by the global Newton-vertex
> proof and cubic first-coordinate bifiltration in
> `WEIGHTED_LIFT_NONHOMOGENEOUS_NEWTON_VERTEX_CLOSURE.md`.  Thus, when
> combined with the cases that survived this audit, the original bounded
> quartic theorem is restored.  The first-lower collision calculations
> below remain valid and document why the former local argument failed.

## Outcome

The boundary-Euler argument in Section 2.2 of
`WEIGHTED_LIFT_ALL_QUARTIC_PIVOT_CLOSURE.md` is not valid: after
changing from \((x,t)\) to \((x,u)\), lower exact seed terms can
occupy the same \(x\)-boundary order as the alleged Euler diagonal.
The quartic theorem therefore has to be re-audited with the exact
first-lower forcing.

That audit has a sharp result.

- The pure \(B^4\) face is rigorously reclosed by a nonzero
  first-lower double pole before \(Q_{\le3}\) or \(R_{\le3}\) can
  enter.
- The pure linear \(B\)-ray in the \(A/B\)-versus-\(C^4\)
  interleaving is also reclosed when the \(C^4\)-coefficient is zero.
  When it is nonzero, the existing exact negative-tail argument still
  applies.
- The descending pure faces remain closed by their forbidden
  \(x^1\)-terms, and the remaining pure \(C\)-faces are nonresonant.
- Two \(C\)-divisible pure faces are **not** reclosed uniformly:
  \(AB^2C\) and \(A^2C^2\).  In each case an allowed cubic target
  coefficient enters the same normalized \(x^{-1}\)-sector and can
  cancel the exact first-lower double pole.  After that tuning the
  whole normalized \(x^{-1}\)-equation admits a polynomial
  coefficient \(\psi(t)\).

Thus this audit does not disprove the quartic theorem, but it shows
that the proof of the theorem with arbitrary \(Q_{\le3}\) remains
incomplete on two explicit quartic one-parameter families.  Moreover,
the theorem's lower-tier staircase cites quadratic and cubic closure
statements that have analogous open pure chains.  No full-quartic
closure claim should be cited until later exact recurrences close all
of these families.

## 1. Exact pure first-lower coefficient

Take a pure top face with \(n\) factors from \(\{A,B\}\), \(c\)
factors \(C\), and pure binary polynomial \(P=t^d\).  Put
\[
A=4n+c.
\]
On the resonant maximal sector \(\gamma_I=x^It^J\), equation (10) of
the quartic note gives
\[
J=
\frac{(5n-20c+17d)I-(5n+20c)+15d}{8n+2c}.
\tag{1}
\]
The two logarithmic determinants at the exact first-lower slice
simplify, after using (1), to
\[
\begin{aligned}
D_U&=(I+1)(c-d-n),\\
D_V&=-\frac{(17I+15)(c-d-n)}{c+4n}.
\end{aligned}
\tag{2}
\]
The fixed first-lower ratios are
\[
-\frac{70}{3},
\qquad
p_{n,d}=-\frac{35n}{6}+\frac{7d}{30}.
\tag{3}
\]
Hence the coefficient of the normalized \(x^{-1}t^{-2}\)-forcing is
\[
\begin{aligned}
\Omega_{n,c,d,I}
&=-\frac{70}{3}D_U+p_{n,d}D_V\\
&=
-\frac{
7(c-d-n)
\left(
100Ic+17Id-25In+100c+15d+25n
\right)
}{
30(c+4n)
}.
\end{aligned}
\tag{4}
\]
The polynomial correction operator on this sector is
\[
\mathcal L_{-1}(\psi)
=-(8n+2c)\psi'
-\frac{10n+2d}{t}\psi.
\tag{5}
\]
It has at most a simple pole for \(\psi\in\mathbb C[t]\).  Therefore
\(\Omega\ne0\) is an exact double-pole obstruction, provided no lower
target face enters the same \(x^{-1}\)-sector.

## 2. The rigorously repaired pure faces

For \(B^4\),
\[
(n,c,d)=(4,0,0),
\qquad
\Omega=-\frac{35}{6}(I-1)\ne0
\tag{6}
\]
on every graph sector \(I\ge2\).  Its first-lower drop is \(m+4\).
The closest cubic target face is lower by at least \(3m+11\), and
the first-coordinate perturbation is lower by \(5m+15\).  Both are
strictly later.

For the pure linear \(B\)-ray,
\[
(n,c,d)=(1,0,0),
\qquad
\Omega=-\frac{35}{24}(I-1)\ne0.
\tag{7}
\]
If \(C^4\) is present, Section 6 of the quartic note already gives a
negative coefficient before the seed recurrence.  If \(C^4\) is
absent, the next surviving target tier lies after the first-lower
pole.

The pure binary rows with \(d>0\) used in Section 3 are descending
and retain their earlier forbidden-\(x^1\) proof.  The \(C^3(A,B)\)
and \(C^4\) pure faces remain nonresonant.

## 3. Exact collision on \(AB^2C\)

For the pure \(AB^2C\) face,
\[
(n,c,d)=(3,1,1),
\qquad
I=13k+6,\quad J=6k+2.
\tag{8}
\]
Equations (2) and (4) give
\[
D_V=\frac{3(17I+15)}{13},
\qquad
\Omega=\frac{7(21I+95)}{65}.
\tag{9}
\]
A lower binary cubic face has highest form
\[
x^{12}t^{15}\gamma^{12}H(t).
\tag{10}
\]
Its constant coefficient \(h_0=H(0)\), corresponding to \(B^3\)
after the seed constants are absorbed, has exactly the same support
as the first-lower target slice.  It changes (9) to
\(\Omega+h_0D_V\).  The allowed choice
\[
\boxed{
h_0
=-\frac{7(21I+95)}{15(17I+15)}
=-\frac{7(21k+17)}{15(17k+9)}
}
\tag{11}
\]
cancels the double pole exactly.
If \(\mu\) and \(\nu\) are the original target coefficients of
\(AB^2C\) and \(B^3\), respectively, then \(q_6/p_5=5/6\) gives
\[
\frac{\nu}{\mu}
=-\frac{7(21k+17)}{18(17k+9)}.
\tag{11a}
\]

All remaining terms then lie in \(t^{-1}\mathbb C[t]\).  Formula
(5) maps \(\mathbb C[t]\) bijectively onto this space, because
\[
\mathcal L_{-1}(t^{q+1})
=-\left((8n+2c)(q+1)+10n+2d\right)t^q
\tag{12}
\]
has nonzero coefficient for every \(q\ge-1\).  Thus the complete
first-lower \(x^{-1}\)-equation, not merely its leading pole, has a
polynomial coefficient solution after (11).  This is a local
recurrence statement; it does not construct a globally compatible
polynomial graph.

## 4. Exact collision on \(A^2C^2\)

For the pure \(A^2C^2\) face,
\[
(n,c,d)=(2,2,2),
\qquad
I=5k+5,\quad J=k.
\tag{13}
\]
Here
\[
D_V=\frac{17I+15}{5},
\qquad
\Omega=\frac{28(23I+35)}{75}.
\tag{14}
\]
The lower cubic face \(CQ_2(A,B)\) has polynomial
\[
H(t)=h_0+h_1t+h_2t^2.
\tag{15}
\]
The \(h_0\)-term would create a nonzero \(t^{-3}\)-pole, so take
\(h_0=0\).  The coefficient \(h_1\), corresponding to \(ABC\) after
normalization, then shares the exact first-lower support.  The choice
\[
\boxed{
h_1
=-\frac{28(23I+35)}{15(17I+15)}
=-\frac{28(23k+30)}{15(17k+20)}
}
\tag{16}
\]
cancels the double pole.  As in Section 3, (5) then solves every
remaining \(t^{-1}\mathbb C[t]\) term with a polynomial coefficient
on this Laurent sector.
If \(\mu\) and \(\nu\) are the original coefficients of \(A^2C^2\)
and \(ABC\), respectively, then
\[
\frac{\nu}{\mu}
=-\frac{14(23k+30)}{9(17k+20)}.
\tag{16a}
\]

## 5. Inherited lower-tier gaps

Section 7 of the quartic note invokes the arbitrary-lower-tier cubic
and quadratic theorems when a lower-degree target face lies above the
remaining quartic \(C\)-face.  The corrected audit of those theorems
finds the same remove-one-\(C\) collision:
\[
ABC+\lambda B^2,
\qquad
AC+\lambda B.
\tag{17}
\]
In both cases the lower monomial occurs at the exact first-lower drop
\(m+4\) and can cancel the \(t^{-2}\) coefficient.  Therefore the
quartic theorem also inherits these gaps in specializations where the
corresponding lower tier leads.  See
`WEIGHTED_LIFT_QUADRATIC_CUBIC_LOWER_TIER_CORRECTION_AUDIT.md`.

## 6. Minimal correction banner

The smallest accurate banner for the old quartic note is:

> **Correction (25 July 2026).** Section 2.2 uses an invalid
> boundary-Euler separation.  The corrected exact first-lower
> calculation re-closes the pure \(B^4\) and pure linear \(B\) rays,
> but not the \(AB^2C\) and \(A^2C^2\) rays with arbitrary cubic lower
> target terms.  In those two families, normalized \(B^3\) and \(ABC\)
> coefficients respectively can cancel the first-lower double pole,
> and the remaining normalized \(x^{-1}\)-equation admits a
> polynomial coefficient solution.
> Therefore equation (69), as stated for arbitrary \(Q_{\le3}\), is
> not currently proved.  Its lower-tier argument also inherits the
> open \(ABC+B^2\) and \(AC+B\) chains from the cubic and quadratic
> notes.  All descending, mixed negative-tail, nonresonance,
> nonzero-\(C^4\) interleaving, and constant-graph certificates remain
> valid.

The accompanying exact check is
`verify_weighted_lift_all_quartic_pure_face_correction_audit.py`.
