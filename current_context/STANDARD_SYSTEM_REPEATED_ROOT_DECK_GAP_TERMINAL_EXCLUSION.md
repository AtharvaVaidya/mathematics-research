# A deck-gap exclusion for repeated-root compensating chains

Date: 26 July 2026

## Outcome

There is a simple structural obstruction to the unmatched
compensating chain at the residual zero root.

Keep the notation of the first repeated-root Rees chart:
\[
1<a<b,\qquad \gcd(a,b)=1,\qquad n=ag,\qquad m=bg,
\]
\[
\gcd(d,h)=1,\qquad 2\le e\le g,\qquad e=kh+f,\quad f\ge1,
\]
\[
\tau=t^h,\qquad s=t^d y,\qquad
G=hg-ed>0,
\]
arising from a strict lowest matched first face subject to the
reciprocal degree caps.  After the equivariant unit normalization,
suppose
\[
p(0,z)=z^{af},\qquad q(0,z)=z^{bf},\qquad f\ge1.
\tag{1}
\]
The transformed Keller equation has a nonzero right side whose
lowest \(z\)-term is
\[
c\,t^{N'},\qquad
N'=(a+b)G+d-2h.
\tag{2}
\]

Then:

> **Deck-gap terminal exclusion.**  If the full coefficient of the
> scalar term \(t^{N'}z^0\) in (2) is nonzero, necessarily
> \[
> \boxed{bG>h.}
> \tag{3}
> \]
> More precisely, every nonzero scalar pairing has residual orders
> \((0,1)\) or \((1,0)\), and its two \(t\)-orders are respectively
> \[
> \boxed{
> (aG-h,\ bG-h+d)
> \quad\text{or}\quad
> (aG-h+d,\ bG-h).
> }
> \tag{4}
> \]

This statement is independent of matchedness, secondary slope,
occupied support step, and the number of preceding cancellations.  It
uses only the Rees descent, the reciprocal degree caps, and the fact
that the zero-root boundary in (1) has no constant term.

The root here is specifically the deck-fixed residual root \(z=0\).
The termwise deck descent used below is not available on one isolated
nonzero root germ, because the deck group permutes those germs.

For the exceptional numerical configuration
\[
(g,e,h,d,G,a,b)=(9,7,4,5,1,2,3),
\tag{5}
\]
one has
\[
bG=3<4=h.
\]
Hence its residual zero-root chart cannot supply the Keller scalar,
even through an arbitrary unmatched compensating chain.  Equivalently,
the two putative terminal order pairs are
\[
(-2,4)\qquad\text{and}\qquad(3,-1),
\tag{6}
\]
so each asks for a negative \(t\)-order.

This removes that numerical repeated-root Rees configuration.  The
well-known exact local face
\[
p=z^2+2t,\qquad q=z^3+3tz,\qquad
\mathcal L(p,q)=6t^2
\tag{7}
\]
occurs at a nonzero simple residual root.  It does not rescue the
global first face: the same first-face polynomial has the zero root
in (1), and (3) excludes the required scalar equation in that chart.

Thus the orbit-residue calculation in
`STANDARD_SYSTEM_GLOBAL_CUBIC_RESIDUE_MOMENT_AUDIT.md` remains a
correct principal-endpoint test, but it is no longer needed to decide
the tuple (5): the fixed zero-root chart fails before a principal
endpoint can be reached.

The theorem does not exclude repeated-root charts with \(bG>h\).
Section 4 records a further global restriction on the intermediate
band \(aG\le h<bG\).

## 1. The transformed support and its descent

Before the unit normalization, write
\[
P=t^{aed}p,\qquad Q=t^{bed}q.
\tag{8}
\]
Because these factors are the weights of the entire lowest matched
first faces, the remaining \(t\)-orders in \(p,q\) are nonnegative.
After the formal \(z\)-change they lie in \(k[t][[z]]\), with finite
\(t\)-support; the \(z\)-series need not be polynomial.
The normalized coordinate has the form
\[
z=y\,U(y^h)^{1/f},
\qquad U(0)\ne0.
\tag{9}
\]
It is tangent to a nonzero scalar multiple of \(y\) and contains only
increments by multiples of \(h\).  In particular, a \(z\)-term of
order \(0\) or \(1\) comes from an original \(y\)-term of the same
order.  No higher \(y\)-order can create it.

Consider a monomial
\[
t^r z^\epsilon,\qquad \epsilon\in\{0,1\},
\tag{10}
\]
in \(p\).  Its leading pullback says that the reciprocal
\(\tau^I\)-coefficient has a nonzero local \(s^\epsilon\)-jet, where
\[
\boxed{hI+d\epsilon=aed+r.}
\tag{11}
\]
Similarly, a monomial \(t^s z^\eta\) in \(q\), with
\(\eta\in\{0,1\}\), gives a nonzero local \(s^\eta\)-jet in the
\(\tau^J\)-coefficient, where
\[
\boxed{hJ+d\eta=bed+s.}
\tag{12}
\]
Deck equivariance forces the integrality of \(I,J\) in these formulas.
The original reciprocal degree caps give
\[
I+\epsilon\le n,\qquad J+\eta\le m.
\tag{13}
\]
Indeed, a polynomial with a nonzero local jet of exact order
\(\epsilon\) has degree at least \(\epsilon\), even though the formal
coordinate \(s\) can make its full Taylor expansion infinite.

The transformed operator is
\[
\mathcal L(p,q)
=t(p_zq_t-p_tq_z)+aG\,p q_z-bG\,q p_z.
\tag{14}
\]
A pairing of (10) with its \(q\)-analogue has \(t\)-order \(r+s\)
and \(z\)-order \(\epsilon+\eta-1\).  Therefore a scalar
\(t^{N'}z^0\) requires
\[
\epsilon+\eta=1,\qquad r+s=N'.
\tag{15}
\]

Adding (11) and (12), and using (2), (15), and
\[
ed+G=hg,
\tag{16}
\]
gives
\[
\begin{aligned}
h(I+J)
&=aed+bed+r+s-d\\
&=(a+b)ed+(a+b)G-2h\\
&=h\bigl((a+b)g-2\bigr).
\end{aligned}
\]
Consequently
\[
\boxed{I+J=n+m-2.}
\tag{17}
\]

## 2. Only the affine defect-one indices are nonzero

First take \((\epsilon,\eta)=(0,1)\).  The caps (13) and (17)
leave
\[
(I,J)=(n,m-2)\quad\text{or}\quad(n-1,m-1).
\tag{18}
\]
The coefficient in (14) of a pair
\(A t^r\) and \(B t^s z\) is
\[
AB(aG-r).
\tag{19}
\]
By (11),
\[
aG-r=h(n-I).
\tag{20}
\]
Thus the first pair in (18) has zero coefficient, and every nonzero
pair has
\[
I=n-1,\qquad J=m-1.
\tag{21}
\]
Substitution into (11)--(12) gives the first pair in (4).

For \((\epsilon,\eta)=(1,0)\), the caps leave
\[
(I,J)=(n-2,m)\quad\text{or}\quad(n-1,m-1).
\tag{22}
\]
The coefficient of \(A t^r z\) paired with \(B t^s\) is
\[
AB(s-bG)=AB\,h(J-m).
\tag{23}
\]
Again the corner pair vanishes, and the only nonzero pair is (21).
Equations (11)--(12) now give the second pair in (4).

This is a direct Rees-coordinate refinement of the affine
defect-one endpoint classification.  It applies term by term, so
allowing several scalar contributions or arbitrarily many earlier
non-scalar cancellations does not change the conclusion.

More explicitly, the bracket is bilinear.  If the coefficient of
\(t^{N'}z^0\) is nonzero after all cancellations, at least one
monomial pairing contributing to it has nonzero coefficient.  The
argument above classifies every such pairing.  It never assumes that
the two terms form an isolated face or that earlier coefficients
vanish separately.  Identical monomials are first collected, so a
``nonzero monomial'' here always means a nonzero coefficient in the
full transformed series.

## 3. The strict deck gap

Assume \(bG\le h\).

For the first pair in (4),
\[
aG-h<bG-h\le0,
\]
so its \(P\)-order is negative.  Such a monomial is absent from
\(p\in\mathbf C[t][[z]]\).

For the second pair, the \(Q\)-order is
\[
bG-h\le0.
\]
It is negative if \(bG<h\).  If \(bG=h\), it is zero and would
require a \(t^0z^0\) term of \(q\).  But (1) says
\[
q(0,z)=z^{bf},
\]
so that coefficient is zero.  Thus neither nonzero terminal pairing
exists when \(bG\le h\), proving (3).

Notice why the inequality is strict.  Deck congruence alone would
allow a zero \(t\)-order at equality.  The exact zero-root boundary,
not congruence alone, removes it.

## 4. The intermediate deck band

Suppose
\[
aG\le h<bG.
\tag{24}
\]
The \((0,1)\) orientation in (4) is absent: its \(P\)-order is
negative when \(aG<h\), while at equality it asks for the absent
\(t^0z^0\) term of \(p(0,z)=z^{af}\).  Therefore only the
\((1,0)\) orientation can contribute.  Pulling it back through
(11)--(12) says that
\[
\operatorname{ord}_{s=0}P_{n-1}=1,\qquad
\operatorname{ord}_{s=0}Q_{m-1}=0.
\tag{25}
\]
The reciprocal cap gives \(\deg P_{n-1}\le1\).  Hence:

> **Intermediate-band corollary.**  Across the distinct repeated
> roots of the global common polynomial, at most one root can have
> \(aG\le h<bG\).

Indeed, each such root would be a distinct simple zero of the same
affine polynomial \(P_{n-1}\).  This is a global restriction, unlike
the local deck-gap inequality.

The surviving \(P\)-order \(aG-h+d\) is positive.  One direct check is
to combine the strict slope inequality \(d/h<g/e\) with
\[
\frac ge\le\frac{ag-1}{ae-1};
\]
it gives \(d(ae-1)<h(ag-1)\), equivalently
\(aG-h+d>0\).

If \(aG>h\), both orientations in (4) have positive orders and the
present argument imposes no analogous one-root bound.

The inequality \(bG>h\) itself is
\[
\frac dh<\frac ge-\frac1{be}.
\tag{26}
\]
Thus it removes only a thin near-resonant strip.  Its strength is the
complete elimination of the highlighted numerical chart and the
one-root restriction (25), not a broad count of all Rees parameters.

## 5. The numerical survivor without enumeration

For (5),
\[
N'=(2+3)\cdot1+5-2\cdot4=2.
\]
The deck characters imply that a \(p\)-monomial \(t^rz^u\) obeys
\[
r-u\equiv2\pmod4,
\]
while a \(q\)-monomial obeys
\[
s-u\equiv3\pmod4.
\]
At \(t=0\), (1) is
\[
p(0,z)=z^6,\qquad q(0,z)=z^9.
\]
The coefficient of \(t^2z^0\) in (14) can only pair residual
orders \(0\) and \(1\).  Formula (4) says that these would have
\(t\)-orders \((-2,4)\) or \((3,-1)\).  Hence the scalar coefficient
vanishes before any equation for the intervening faces is solved.

This is the promised structural reason that the unmatched chain
cannot repair the numerical case.  No scan of secondary slopes or
face coefficients is involved.

## Scope and novelty risk

The argument is an elementary support consequence of the already
established Rees operator and reciprocal endpoint bounds.  It appears
to be new within this project because the earlier terminal theorem
recorded only the original indices \((n-1,m-1)\), without translating
them back to the two exact Rees \(t\)-order pairs (4).

The source results used verbatim are equations (6)--(8), the
equivariant normalization in equation (9), and the terminal
classification (43)--(48) of
`STANDARD_SYSTEM_REPEATED_ROOT_ZERO_RESIDUAL_SECONDARY_FACE_NO_GO.md`.
Sections 1--2 above also rederive that terminal classification
directly, so the new inequality does not depend on any matched-face
part of that note.

No broad literature novelty is claimed.  The result is a scoped lemma
inside the standard-system reduction, not a proof of the plane
Jacobian conjecture.  Its value is that it closes the previously open
unmatched-chain loophole for every residual zero-root chart satisfying
\(bG\le h\), including the exceptional tuple (5).

The identities and a direct low-order audit of (5) are checked by
`verify_standard_system_repeated_root_deck_gap_terminal_exclusion.py`.
