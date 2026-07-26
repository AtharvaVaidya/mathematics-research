# Saturation does not force the \([g-1,1]\) repeated-root top form

Date: 26 July 2026

## Outcome

The symbolic obstruction for
\[
 p_0=d^2+ux,\qquad q_0=d^3,\qquad
 d=x^{g-1}(x+\ell)
\tag{1}
\]
does not yet apply to every saturated repeated-root endpoint.
The missing implication is false at the level of all presently proved
first-layer, local-face, reciprocal-degree, and affine-endpoint
conditions.

For every integer \(E\ge2\), there is an exact saturated support
family whose top common root is instead
\[
 \boxed{d_E=x^{g-E}(x^E+\ell).}
\tag{2}
\]
It has root multiplicity partition
\[
 [g-E,1,\ldots,1]
\tag{3}
\]
with \(E\) simple roots, whereas (1) has partition \([g-1,1]\).
The partition is invariant under every affine or projective change of
the boundary coordinate, so no admissible reciprocal source
normalization turns (2) into (1).  Replacing the transverse parameter
by an \(E\)-th root would change the source plane and the reciprocal
filtration; it is not a polynomial source normalization.

The intervening filtered equations can nevertheless exclude this
entire new diagonal family.  For \(g=2(E+1)\), every \(E\ge2\) fails
by defect at most five.  For every \(E\ge10\), one defect-four
coordinate is the uniform nonzero scalar
\[
 {160\over81}E^3(E+1)^2(188E^2+393E+183)
 {\ell^4\over u^{11}}.
\]
The range \(2\le E\le9\) is closed exactly by defects three through
five.  Thus the support family is a countermodel to the proposed
**normalization**, but not to the stronger filtered obstruction.

Moreover the resulting defect-one top data are formally
unobstructed.  For every monic \(d\) and \(u\ne0\),
\[
 p_0=d^2+ux,\qquad q_0=d^3
\tag{4}
\]
have coprime derivatives and the explicit bounded Bezout pair
\[
 p_1=-\frac{4d'}{3u^2},\qquad
 q_1=\frac1u-\frac{2dd'}{u^2}.
\tag{5}
\]
Consequently (4)--(5) admit an exact all-order formal Keller lift.
Thus neither the local repeated-root data nor the formal completion
can force \(E=1\).

This is not a polynomial Keller counterexample.  The support family
deliberately leaves intermediate filtered equations uncancelled, and
the formal lift normally violates the decreasing reciprocal degree
bounds.  The rigorous conclusion is narrower and decisive for the
current strategy:

> A universal repeated-root exclusion must treat arbitrary saturated
> order \(E\), and ultimately arbitrary monic \(d\), or prove a new
> filtered theorem excluding every \(E\ge2\).  The
> \(d=x^{g-1}(x+\ell)\) calculation alone cannot be bridged to all
> endpoints by normalization.

The first alternative is now proved for the diagonal
\(g=2(E+1)\) family constructed below.  Arbitrary \(g>E\), arbitrary
two-block partitions, and arbitrary monic \(d\) remain open.

## 1. An exact saturated family at every order \(E\ge2\)

Fix \(E\ge2\), put
\[
 r=E+1,\qquad g=2r=2E+2,
\tag{6}
\]
and choose distinct \(\alpha_1,\ldots,\alpha_r\).  Let
\[
 R(X)=\prod_{i=1}^r(X-\alpha_i)^2,\qquad
 L_0(X)=\prod_{i=1}^r(X-\alpha_i).
\tag{7}
\]
Choose a linear polynomial \(H\) which is nonzero at every
\(\alpha_i\), and set
\[
 L=L_0H,\qquad D=R+\tau^E L.
\tag{8}
\]
Then
\[
 \deg L=r+1=E+2=g-E.
\tag{9}
\]
Thus the first common shift saturates the sharp reciprocal
first-layer bound.

At \(\alpha_i\), use a local parameter \(s=X-\alpha_i\).  Up to
units, the first compact face of \(D\) is
\[
 s^2+c_i\tau^Es
 =s^2\left(1+c_i\frac{\tau^E}{s}\right).
\tag{10}
\]
Its exact local data are
\[
 e_i=2,\qquad d_i=E,\qquad h_i=1,\qquad
 f_i=1,\qquad G_i=h_ig-e_id_i=2.
\tag{11}
\]
The face is strict because
\[
 \frac{d_i}{h_i}=E
 <E+1=\frac{g}{e_i},
\tag{12}
\]
and for the \((2,3)\) common powers it lies in the deep band:
\[
 2G_i=4>1=h_i.
\tag{13}
\]
Every root is repeated, every residual zero survives, and all roots
obey the local deck-gap requirement.

Now put
\[
\begin{aligned}
 P&=D^2+\tau^{2g-1}(uX+v),\\
 Q&=D^3+w\tau^{3g-1},
\end{aligned}
\qquad uw\ne0.
\tag{14}
\]
All binomial coefficients of \(D^2,D^3\) obey the reciprocal caps:
\[
\begin{aligned}
 \deg_X(R^{2-j}L^j)&\le2g-jE,\\
 \deg_X(R^{3-j}L^j)&\le3g-jE.
\end{aligned}
\tag{15}
\]
The endpoint coefficients also obey their degree-one and
degree-zero caps.  For
\[
 \mathscr K(P,Q)
 =\tau(P_XQ_\tau-P_\tau Q_X)+2gPQ_X-3gQP_X,
\tag{16}
\]
the two affine endpoint terms contribute exactly
\[
 -uw\,\tau^{5g-2}.
\tag{17}
\]
Every cross term with \(D^2\) or \(D^3\) has smaller
\(\tau\)-order because \(E<g\).  Hence the coefficient of
\(\tau^{5g-2}\) in the full bracket is the nonzero scalar \(-uw\).
This is precisely the terminal affine endpoint required by the
support classification.

Let \(\ell\) be the leading coefficient of \(L\).  The ordinary
degree-\(g\) homogeneous part of \(D\) is
\[
 D_{\rm top}=X^g+\ell\tau^EX^{g-E}.
\tag{18}
\]
Dehomogenizing at \(\tau=1\) gives (2).  The top forms of (14) are
\[
 \boxed{
 p_0=d_E^2+ux,\qquad q_0=d_E^3.
 }
\tag{19}
\]
Thus the same filtered recurrence used for (1) starts, but with a
different common-root polynomial.

## 2. Why \(E\) cannot be normalized to one

Assume \(\ell\ne0\).  In characteristic zero, \(x^E+\ell\) is
squarefree and has no root at zero.  Hence the multiplicity partition
of \(d_E\) is exactly (3).  For \(E=1\), it is
\([g-1,1]\); for \(E\ge2\), the two partitions differ.

An invertible change of the boundary line is affine, or projective
after homogeneous compactification.  Such a change permutes roots
and preserves their multiplicities.  Target changes preserving the
\((2g,3g)\) degree pair do not alter the degree-\(3g\) form
\(q_0=d_E^3\) except by a nonzero scalar: no integral power of a
degree-\(2g\) form has degree \(3g\).  Finally, the monic cube root of
\(q_0\) is unique.  Therefore the partition of \(d_E\) is an
invariant of the admissible top data.

This already disproves the proposed normalization under the current
hypotheses.  It does not disprove a stronger theorem saying that the
later filtered Keller equations exclude all \(E\ge2\); that is exactly
the new theorem which would be needed.

## 3. The true top-form target is arbitrary \(d\)

The two-term polynomial (18) is only the smallest countermodel.
Suppose a common approximate root has reciprocal-compatible terms
\[
 S=R+\sum_{j=E}^g\tau^jL_j,\qquad
 \deg L_j\le g-j.
\tag{20}
\]
If \(c_j\) is the coefficient of \(X^{g-j}\) in \(L_j\), its ordinary
degree-\(g\) homogeneous part is
\[
 S_{\rm top}
 =X^g+\sum_{j=E}^gc_j\tau^jX^{g-j}.
\tag{21}
\]
After dehomogenization,
\[
 d(x)=x^g+\sum_{j=E}^gc_jx^{g-j}.
\tag{22}
\]
Thus saturation does not reduce the common root to a finite list of
fixed polynomials.  Even inside the common-power sector, later
top-saturating shifts carry genuine root-configuration moduli.

Accordingly the broad recurrence target is (4) with arbitrary monic
\(d\), subject to whatever additional divisibility constraints the
full repeated-root resolution eventually proves.  The special
\([g-1,1]\) family is the case \(E=1\) with every later \(c_j=0\).

## 4. Exact formal countermodel

Let \(d\) be any monic polynomial and let \(u\ne0\).  Put
\[
 A=p_0'=2dd'+u,\qquad B=q_0'=3d^2d'.
\tag{23}
\]
Any common divisor of \(A\) and \(B\) must divide either \(d\) or
\(d'\).  At a zero of either factor, \(A=u\), so
\[
 \gcd(A,B)=1.
\tag{24}
\]
Direct substitution of (5) gives
\[
 Aq_1-Bp_1=1.
\tag{25}
\]
The degrees are
\[
 \deg p_1\le2g-1,\qquad
 \deg q_1\le3g-1,
\tag{26}
\]
so this is a reciprocal-compatible defect-one endpoint.

Write
\[
 W=p_1'q_1-p_1q_1'.
\tag{27}
\]
There is a unique formal series
\[
 \phi=y+O(y^2)
\]
satisfying
\[
 \phi+\frac W2\phi^2=y.
\tag{28}
\]
Then
\[
\begin{aligned}
 F(x,y)&=p_0(x)+p_1(x)\phi(x,y),\\
 G(x,y)&=q_0(x)+q_1(x)\phi(x,y)
\end{aligned}
\tag{29}
\]
obey
\[
 J(F,G)=1.
\tag{30}
\]
Indeed the Jacobian of
\((p_0+p_1z,q_0+q_1z)\) is \(1+Wz\), while
differentiating (28) gives
\((1+W\phi)\phi_y=1\).

This formal lift preserves the zero- and one-jets exactly for every
\(E\).  Its higher coefficients generally exceed the reciprocal
degree caps, so it is an exact local/formal countermodel to the
normal-form bridge, not a polynomial counterexample to the Jacobian
conjecture.

## 5. The first genuinely filtered invariant for arbitrary \(d\)

The first filtered condition can be written without choosing a root
partition.  Let
\[
 r=\operatorname{rem}_d(d')^3,\qquad \deg r<g.
\tag{31}
\]
For (4), the unique bounded defect-two solution is
\[
\begin{aligned}
 p_2={8\over9u^5}\left(
 { (d')^3-r\over d}-d'd''-{2d'r\over u}\right),\\
 q_2={2d''\over3u^4}+{4(d')^3\over3u^5}
 -{4dd'd''\over3u^5}-{8dd'r\over3u^6}.
\end{aligned}
\tag{32}
\]
The quotient in \(p_2\) is polynomial by the definition of \(r\),
and
\[
 \deg p_2\le2g-2,\qquad \deg q_2\le3g-2.
\]
Put
\[
\begin{aligned}
 H_3={}&2p_1'q_2-p_1q_2'
 +p_2'q_1-2p_2q_1',\\
 h_3={}&-\frac13H_3.
\end{aligned}
\tag{33}
\]
Since \(Aq_1\equiv1\pmod B\), the exact defect-three class is
\[
 \boxed{
 \mathcal O_3(d,u)
 =[x^{3g-2}]
 \operatorname{rem}_{\,B}(q_1h_3),
 \qquad B=3d^2d'.
 }
\tag{34}
\]
The defect-three equation has a reciprocal-bounded solution if and
only if \(\mathcal O_3(d,u)=0\).  This is the first condition which
the all-order formal lift does not see.

There is also an invariant residue/trace formula.  Assume first that
\[
 A=u+2dd'
\tag{35}
\]
is squarefree.  The rational functions
\[
 {\operatorname{rem}_B(q_1h_3)\over B}
 \quad\hbox{and}\quad
 {h_3\over AB}
\]
have the same principal parts at the roots of \(B\).  The latter is
\(O(x^{-2})\) at infinity, and \(B\) has leading coefficient \(3g\).
The residue theorem therefore gives
\[
 \boxed{
 \mathcal O_3(d,u)
 =-3g\sum_{A(a)=0}{h_3(a)\over A'(a)B(a)}.
 }
\tag{36}
\]
This makes independence from Euclidean Bezout representatives
transparent: the class is a global residue attached to the fixed
boundary coordinate and derivative pair.

The summand can be made completely explicit.  Define
\[
\begin{aligned}
 \Psi={}&u^5-6u^3d^3d''+2u^2d^3r
 +12ud^6(d'')^2\\
 &\quad+4ud^5r'+24d^6rd''.
\end{aligned}
\tag{37}
\]
At a root of \(A\), one has \(d'=-u/(2d)\), and direct substitution
in (33) gives
\[
 h_3={2\Psi\over27u^7d^6}.
\tag{38}
\]
Since
\[
 A'={u^2+4d^3d''\over2d^2},\qquad
 B=-{3ud\over2}
\quad\text{on }A=0,
\]
Equation (36) becomes
\[
 \boxed{
 \mathcal O_3(d,u)
 ={8g\over27u^8}
 \sum_{A(a)=0}
 {\Psi(a)\over
 d(a)^5\bigl(u^2+4d(a)^3d''(a)\bigr)}.
 }
\tag{39}
\]
Equivalently, when the displayed denominator is invertible modulo
\(A\), this is the algebra trace
\[
 {8g\over27u^8}
 \operatorname{Tr}_{\mathbf C[x]/(A)}
 \left(
 {\Psi\over d^5(u^2+4d^3d'')}
 \right).
\tag{40}
\]
The modular definition (34) remains valid on the nonsquarefree
exceptional locus, where the simple-root display (39) must be
replaced by higher residues.

The first invariant is not universally nonzero.  For example,
\[
 d=x^5
\tag{41}
\]
has
\[
 \mathcal O_3=0,
\]
and even passes defect four, but its defect-five vector is
\[
 \left(0,{60160000\over243u^{13}},0\right)\ne0.
\tag{42}
\]
Thus an all-\(d\) proof genuinely needs the higher vector sequence;
no argument based only on (34) can close it.

No monic \(d\) is currently known for which every bounded defect
class vanishes and the recurrence terminates as a polynomial pair.
Finding one would produce a polynomial Keller map of degrees
\((2g,3g)\); proving none exists is already a substantial infinite
subfamily of the Jacobian conjecture.  The formal construction in
Section 4 cannot decide this because it drops the reciprocal degree
filtration.

## 6. Uniform filtered exclusion of the diagonal \(E\)-family

The support family in Section 1 is now excluded after the full lower
coefficients are admitted.

> **Theorem.**  Let \(E\ge2\), \(g=2(E+1)\), and
> \[
> d=x^{E+2}(x^E+\ell),\qquad \ell u\ne0.
> \]
> No reciprocal pair with top forms
> \[
> p_0=d^2+ux,\qquad q_0=d^3
> \]
> can satisfy all filtered Keller equations.  A nonzero obstruction
> occurs by defect at most five.

The exact low-\(E\) closure is
\[
\begin{array}{c|cccccccc}
E&2&3&4&5&6&7&8&9\\ \hline
\text{closing defect}&3&5&4&3&5&4&4&5.
\end{array}
\tag{43}
\]
At \(E=3,6,9\), the defect-four vector has an exceptional
nonzero polynomial locus in \(u\).  Taking the gcd in
\(\mathbf Q(\ell)[u]\) with the defect-five vector gives \(1\), so
there is no simultaneous zero.  For the other five values, the
listed defect already contains a parameter-independent nonzero
coordinate.

For every \(E\ge10\), the first forbidden defect-four coordinate is
\[
\boxed{
 \mathcal O_{4,1}
 ={160\over81}E^3(E+1)^2
 (188E^2+393E+183){\ell^4\over u^{11}}.
}
\tag{44}
\]
It is nonzero for every positive integer \(E\) when \(\ell u\ne0\).
The other defect-four forbidden coordinate is zero in the uniform
range.

Here is the symbolic core of the proof.  In the affine-exponent
notation \((a,b)\leftrightarrow x^{aE+b}\),
\[
 d=x^{2E+2}+\ell x^{E+2}.
\tag{45}
\]
The only remainder entering the universal defect-two formulas is
\[
\boxed{
 r=\operatorname{rem}_d(d')^3
 =-E^3\ell^5x^{E+3}.
}
\tag{46}
\]
Indeed, after removing \(x^{E+2}\), reduce modulo
\(x^E+\ell\).  One has
\[
\begin{aligned}
 d'&=x^{E+1}\bigl((2E+2)x^E+(E+2)\ell\bigr),\\
 x^{2E+1}&\equiv \ell^2x\pmod{x^E+\ell},\\
 (2E+2)x^E+(E+2)\ell&\equiv-E\ell
 \pmod{x^E+\ell},
\end{aligned}
\]
which gives (46).

Substitute (45)--(46) into (5), (32), and the filtered recurrences
through defect four.  Sparse polynomial division keeps each exponent
as an affine pair \((a,b)\).  For \(E\ge11\), every leading-term
comparison used by the division is certified at the threshold and
has nonnegative slope, hence stays valid throughout that chamber.
The unique forbidden exponent is \((6,3)\), namely
\[
 6E+3=3g-3,
\]
and its coefficient simplifies identically to (44).

A hostile exponent-collision audit finds exactly one integer in this
range, \(E=12\), where two transient affine exponents coincide.
Direct ordinary polynomial division at \(E=12\) gives (44), so the
formal sparse separation causes no missed cancellation.  The
boundary \(E=10\) is also checked by ordinary division.  This proves
(44) for every \(E\ge10\).  Exact quotient/remainder arithmetic over
\(\mathbf Q(\ell,u)\), together with the gcd test described after
(43), proves the remaining values \(2\le E\le9\).

This theorem is strictly broader than the \([g-1,1]\) calculation,
but it is not an arbitrary-partition result.  It treats the diagonal
relation \(g=2(E+1)\) forced by the clean saturated support family in
Section 1.  Experiments for other \(g>E\) are encouraging, but no
symbolic chamber proof for every pair \((g,E)\) is claimed here.

## 7. Exact remaining lemma

The present symbolic obstructions exclude the \(E=1\),
\([g-1,1]\) family and every diagonal family in Section 6.  To turn
them into an all-degree repeated-root theorem, one needs one of the
following genuinely new statements:

1. **All-two-block filtered exclusion.**  For every \(2\le E<g\),
   without the diagonal restriction \(g=2(E+1)\), every
   bounded completion with
   \[
   p_0=\bigl(x^{g-E}(x^E+\ell)\bigr)^2+ux,\qquad
   q_0=\bigl(x^{g-E}(x^E+\ell)\bigr)^3
   \]
   has a nonzero finite defect class.
2. **Arbitrary-\(d\) filtered exclusion.**  For every monic
   degree-\(g\) polynomial \(d\) and \(u\ne0\), the bounded recurrence
   attached to (4) fails before termination.
3. **A new global rigidity theorem.**  Use intervening Keller
   equations, not saturation or coordinate normalization, to prove
   that every actual repeated-root endpoint has \(E=1\) and no later
   top-saturating common shifts.

The second is the cleanest invariant formulation.  At defect \(k\),
the exact obstruction is already known: it is the top \(k-2\)
coefficients of
\[
 \operatorname{rem}_{\,3d^2d'}
 \left((2dd'+u)^{-1}\left(-\frac{H_k}{k}\right)\right).
\tag{47}
\]
What is missing is a proof that these classes cannot all vanish for
an arbitrary \(d\).

For the intermediate all-two-block target, one exact chamber
parameter is already available.  Write
\[
 d=x^s(x^E+\ell),\qquad s=g-E\ge2,
\]
and divide
\[
 2s-3=qE+j,\qquad 0\le j<E.
\]
Then
\[
\boxed{
 \operatorname{rem}_d(d')^3
 =(-1)^{q+1}E^3\ell^{q+3}x^{s+j}.
}
\tag{48}
\]
This follows by factoring \(x^s\), reducing \(x^{2s-3}\) modulo
\(x^E+\ell\), and using
\[
 gx^E+s\ell\equiv-E\ell\pmod{x^E+\ell}.
\]
It recovers (46) from \(q=2,j=1\).  It also shows a real difficulty
in extending the sparse proof: \(q\) is unbounded when \(g/E\) is
unbounded, so the two-parameter problem does not reduce to finitely
many ratio chambers without an additional descent or symmetry.

The family, top-form extraction, endpoint coefficient, derivative
coprimality, Bezout pair, finite formal-lift identity, and the
arbitrary-\(d\) modular/residue formula are checked by
`verify_general_repeated_root_normal_form_bridge_countermodel.py`.
The all-\(E\) diagonal theorem is checked independently by
`verify_partition_family_uniform_obstruction.py` and
`verify_partition_family_low_E_obstructions.py`.
