# Hostile audit of the \((12,9)\) half-order resonance

Date: 26 July 2026

## Verdict

The half-order scalar at honest pole scale \(\rho=2\) is real, but
the two canonical residue-square-root branches do not continue to a
formal Keller jet:

* the six mixed-sign Hensel roots are obstructed at order \(51\);
* the two equal-sign roots lift uniquely through order \(51\), but
  are obstructed at order \(68\).

The obstruction is not the result of eight unrelated computer
solves.  The eight roots form two symmetry orbits, and at each
obstructed order a two-dimensional cokernel of one explicit
first-order polynomial operator detects the failure.

All intermediate jets after order \(17\), and the surviving upper
\(k\)-term, have been included for the equal-sign branch.  A
one-dimensional silent order-\(19\) direction propagates for several
orders, but the order-\(53\) equation forces it to vanish.  The
\(k\)-term is neutralized by a unique constant order-\(18\) jet and
does not change the final obstruction.

Earlier \(P\)-multiple tails at orders \(13,\ldots,16\) can also be
included without a symmetry assumption.  A three-character
triangular calculation, retaining all six coefficients of every
new jet, forces the sole order-\(13\) kernel to vanish at bracket
order \(47\).  This closes the symmetry-breaking caveat for the
half-order Hensel branches.

The remaining rational-ramification gap also admits a filtration
argument: any finer-denominator tail is killed by its self-equation
and its first interaction with the unit half-order tail.  The only
surviving normalized orders are \(13/2,17/2,19/2\), all already
present in the denominator-two calculation.  Sections 8--9 give
this reduction.  Subject to the common-cubic reduction audited in
the companion note, the fractional-resonance gap in the local
\(7/2\) theorem is therefore closed.

## 1. The honest ramified grading

Use an honest uniformizer \(t\), coefficient pole scale \(\rho=2\),
and
\[
 X=t^2w,\qquad
 \bar f=t^{24}f,\qquad
 \bar g=t^{18}g.
\]
The scaled bracket is
\[
 \mathcal B(\bar f,\bar g)
 =t(\bar f_t\bar g_X-\bar f_X\bar g_t)
  -24\bar f\bar g_X+18\bar f_X\bar g.
\tag{1}
\]
Take
\[
 P=X^3-1,\qquad
 S_+=-\frac12X^2(X^3-3).
\tag{2}
\]
Then
\[
 S_+^2=P^2\frac{X(X^3-4)}4+X.
\tag{3}
\]
For
\[
 \bar g=P^3+t^{17}S_+,\qquad
 \bar f=(\bar g^{4/3})_+,
\]
the first nonzero bracket coefficient is
\[
 [t^{34}]\mathcal B=4.
\tag{4}
\]
It corresponds to terminal pole \(6\) and ratio \(6/2=3\).

This does not contradict conservation.  The quadratic residual has
\(X\)-degree \(19\), hence lies on the natural weight of the
conserved \(A_5\)-level:
\[
 12+5=17,\qquad 2\cdot17=34.
\]
The integer-graded argument incorrectly discarded this tie when it
divided all orders by \(\rho\).

## 2. The eight Hensel roots and their two orbits

In
\[
 \mathcal A=\mathbf C[X]/(P^2)
 \cong\prod_{a^3=1}\mathbf C[X]/((X-a)^2),
\]
the equation
\[
 S^2=X
\tag{5}
\]
has exactly \(2^3=8\) roots.  At each root \(a\) of \(P\), one
independently chooses
\[
 S(a)=\epsilon_a a^2,\qquad
 S'(a)=\frac{\epsilon_a a}{2},
\qquad \epsilon_a\in\{\pm1\}.
\tag{6}
\]

Overall sign and the cyclic symmetry
\[
 S(X)\longmapsto\omega S(\omega X),
\qquad \omega^3=1,
\tag{7}
\]
preserve (5) and the complete lifting equations.  They have two
orbits:

1. two equal-sign choices, represented by \(S_+\);
2. six mixed-sign choices, represented by
   \[
   S_m=
   -\frac{
   3X^5-2X^4+2X^3-9X^2+14X+10
   }{18}.
   \tag{8}
   \]

It is therefore enough to audit these two representatives.

## 3. A human-readable cokernel at order \(51\)

Let \(V\), of degree below six, be an order-\(34\) correction.  Its
linear contribution to the order-\(51\) equation depends on
\[
 R=\operatorname{rem}_{P^2}(2SV).
\]
Since every root \(S\) of (5) is a unit in \(\mathcal A\), the map
\(V\mapsto R\) is an isomorphism on degree-below-six
representatives.  Up to a nonzero scalar, the linear operator is
\[
 \mathscr L_{51}(R)=2PR'+5P'R.
\tag{9}
\]
On monomials,
\[
 \mathscr L_{51}(X^m)
 =(2m+15)X^{m+2}-2mX^{m-1},
\qquad 0\leq m<6.
\tag{10}
\]
Its image has codimension two in the polynomials of degree at most
seven.  Two cokernel functionals are
\[
\begin{aligned}
 \Lambda_{51,0}(K)
 &=391[X^0]K+46[X^3]K+16[X^6]K,\\
 \Lambda_{51,1}(K)
 &=95[X^1]K+20[X^4]K+8[X^7]K.
\end{aligned}
\tag{11}
\]

For the mixed representative (8), the known cubic forcing is
\[
 K_m=
 \frac{
 450X^7-690X^6+1316X^5-3980X^4+
 2620X^3-2531X^2+4076X-2260
 }{4374}.
\tag{12}
\]
Exact evaluation gives
\[
 \Lambda_{51,0}(K_m)=-\frac{43010}{243},
\qquad
 \Lambda_{51,1}(K_m)=\frac{17290}{243}.
\tag{13}
\]
Thus no order-\(34\) correction exists for any of the six
mixed-sign roots.

For \(S_+\), both functionals vanish.  The order-\(51\) system has
the unique solution
\[
 V=\frac1{16}X^4-\frac{11}{144}X.
\tag{14}
\]
The cubic binomial coefficient used here is
\[
 {4/3\choose3}=-\frac4{81}.
\]

## 4. The equal-sign obstruction at order \(68\)

After inserting (14), the known order-\(68\) forcing is
\[
 K_+=
 \frac{
 X(1323X^6-5139X^3+3776)
 }{1296}.
\tag{15}
\]
An order-\(51\) correction \(W\) again gives an arbitrary
degree-below-six remainder
\[
 R=\operatorname{rem}_{P^2}(2S_+W).
\]
Up to a nonzero scalar, its linear operator is
\[
 \mathscr L_{68}(R)
 =PR'+\frac{16}{3}P'R.
\tag{16}
\]
On \(X^m\), after multiplying by three,
\[
 3\mathscr L_{68}(X^m)
 =3(m+16)X^{m+2}-3mX^{m-1}.
\]
The two cokernel functionals can be taken as
\[
\begin{aligned}
 \Lambda_{68,0}(K)
 &=85[X^0]K+5[X^3]K+[X^6]K,\\
 \Lambda_{68,1}(K)
 &=189[X^1]K+21[X^4]K+5[X^7]K.
\end{aligned}
\tag{17}
\]
They annihilate the image of (16), whereas
\[
 \Lambda_{68,0}(K_+)=0,\qquad
 \Lambda_{68,1}(K_+)=\frac{945}{2}\ne0.
\tag{18}
\]
No order-\(51\) correction can cancel (15).  The negative
equal-sign root has the same obstruction by overall-sign symmetry.

The numerical value in (18) changes by an inessential factor under
different normalizations of \(R=2S_+W\); its nonvanishing is the
invariant statement.

## 5. Intermediate jets and the \(k\)-term

Allow every jet
\[
 \bar g=P^3+\sum_{r\geq17}t^rS_r
\]
with \(\deg S_r<6\), and include the surviving upper term
\(kt^{18}P\) in \(\bar f\).  Solving in increasing bracket order
gives:

* the order-\(35\) equation uniquely sets
  \[
  S_{18}=-\frac34k;
  \]
* the order-\(36\) equation has one silent parameter
  \[
  S_{19}=aX(X^3-3);
  \]
* its successive forced descendants occur at orders
  \(21,23,\ldots,35\);
* the order-\(53\) equation forces \(a=0\);
* after that specialization, the remaining \(c\)-dependent
  equations force
  \[
  \begin{aligned}
  S_{29}&=\frac{c}{48}X^2(5X^3-11),\\
  S_{41}&=-\frac{7c^2}{2304}X^2(9X^3-19),\\
  S_{46}&=-\frac{c}{864}X(35X^3-52);
  \end{aligned}
  \]
  these cancel all \(c\)-dependent bracket coefficients below order
  \(68\), and (15)--(18) remain unchanged.

Thus neither a nonzero \(k\) nor any later intermediate jet removes
the equal-sign obstruction.  When \(c,j\) are retained, the
order-\(29\) coefficient is
\[
 -2(2c+3j)XP(3X^3-4).
\tag{19}
\]
It occurs before the scalar order \(34\), so
\[
 2c+3j=0.
\tag{20}
\]
Under (20), all \(c,j\) interactions with the half-order tail cancel
through the forced jets displayed above.  The upper constants
therefore do not remove (13) or (18).

## 6. Earlier \(P\)-multiple tails and all three characters

Suppose an earlier normal tail occurs at order \(r=13,14,15,16\).
The equations below the scalar order force it to be a multiple of
\(P\).  Pairing it with the unit \(S_+\) at order \(r+17\) kills the
orders \(14,15,16\).  At order \(13\) there is one apparent kernel:
\[
 S_{13}=aPX.
\tag{21}
\]

The simultaneous character calculation is still triangular.  At
each bracket order, solve for the full six coefficients of the new
jet.  The homogeneous kernel has dimension three and is precisely
\[
 P\cdot\mathbf C[X]_{<3};
\]
retain all three kernel parameters rather than imposing cyclic
symmetry.  The next consistency equation acts on an older kernel
triple.  Thus no symmetry-breaking mode is discarded.

In particular, bracket order \(39\) is **not** an obstruction.  The
delayed order-\(18\) \(P\)-multiple is forced to be
\[
 S_{18}=P Q_{18},\qquad Q_{18}=-\frac{a^4}{9};
\tag{21d}
\]
for \(a=1\), this is the independently observed
\(Q_{18}=-1/9\), and it cancels the order-\(39\) coefficient exactly
for both sign orbits.  The first invariant inconsistency after all
such delayed freedoms is bracket order \(47\).

For the equal-sign representative, the final order-\(47\)
consistency system on the surviving triple
\((u_0,u_1,u_2)\) contains
\[
 u_0=u_1=u_2=0,\qquad
 8u_2=3a^2.
\tag{21a}
\]
It is consistent only when \(a=0\).

For the mixed representative, the first three equations give
\[
 u_0=-\frac{a^2}{27},\qquad
 u_1=0,\qquad
 u_2=-\frac{10a^2}{81},
\tag{21b}
\]
while the remaining two evaluate to
\[
 -2a,\qquad \frac{28}{27}a.
\tag{21c}
\]
Again \(a=0\).

The order-\(47\) residual systems (21a)--(21c) are unchanged when
the arbitrary surviving upper \(c,k\) terms and all of their forced
six-coefficient descendants are retained.  Thus the obstruction is
not an artifact of setting the upper constants to zero.

These systems result after retaining every cross-character
quadratic and cubic product through order \(47\).  They prove that
the only earlier order-\(13\) singular chain is formally obstructed
for all eight Hensel roots, before the direct obstructions of
Sections 3--4.  The full triangular recurrence is checked
independently in
`verify_normal_degree_129_indirect_chain_obstruction.py`.

## 7. Mechanism and possible generalization

The obstruction mechanism is finite-dimensional and does not depend
on enumerating a large coefficient ansatz:

1. a conserved-level tie produces a Hensel equation in
   \(\mathbf C[X]/(P^2)\);
2. CRT reduces its roots to finitely many sign or character orbits;
3. the next correction is controlled by
   \[
   P R'+\alpha P'R,
   \]
   acting on the degree-bounded remainder space;
4. gaps between the six-dimensional domain and the
   degree-seven target give explicit trace-like cokernel
   functionals;
5. a nonzero functional evaluation is a formal lifting obstruction.

For a general common component of degree \(d\), the same strategy
replaces the three doubled roots of \(P\) by the CRT algebra
\(\mathbf C[X]/(P^2)\) of dimension \(2d\), and replaces (10) by the
corresponding monomial chains modulo \(d\).  This is a plausible
route to a uniform fractional-resonance theorem.

## 8. Primitive rational-resonance classification

There is only one primitive quadratic scalar resonance in the
\((12,9)\) common-cubic chart.  Work at honest integral pole scale
\(\rho=m\), let the first transverse order be \(\delta>6m\), and
write
\[
 S^2=P^2H+R.
\]
If a conserved-level tie permits a monomial
\[
 R=aX^r,
\]
then degree comparison in
\(-\frac23P^6R\) gives
\[
 2\delta=(18-r)m,\qquad 0\leq r<6.
\tag{22}
\]
The quadratic scaled bracket is
\[
 -2mPR'+\frac23(18m-2\delta)P'R.
\tag{23}
\]
For
\[
 P=X^3+AX+B,\qquad R=aX^r,
\]
use (22) to reduce (23) to
\[
 -\frac43mraA\,X^r-2mraB\,X^{r-1}.
\tag{24}
\]
It is a nonzero scalar only when
\[
 r=1,\qquad A=0,\qquad B\ne0,\qquad
 \frac{\delta}{m}=\frac{17}{2}.
\tag{25}
\]
After scaling \(X\), this is exactly \(P=X^3-1\),
\(R=aX\).  An honest integral order requires \(m\) even; the
primitive choice is \(m=2,\delta=17\).

Thus every direct quadratic rational scalar reduces to the
half-order Hensel problem audited above.

## 9. Rational-filtration theorem

Normalize the honest grading by \(\rho\), allowing rational orders.
The support is discrete because it comes from an honest finite
ramified uniformizer.  The coefficient of any potential scalar in
the dangerous interval \(33/2<N<20\), at normalized order \(N\),
has the universal first-order form
\[
 \mathscr D_N(Z)
 =-2PZ'+\frac23(18-N)P'Z,
\qquad \deg Z<6,
\tag{26}
\]
after absorbing the delayed \(c,j\) term into \(Z\).  If
\(\mathscr D_N(Z)\) is a nonzero scalar, comparison of the leading
degree of \(Z\), followed by the two lower coefficients of
\(P=X^3+AX+B\), gives
\[
 \boxed{N=17,\quad P=X^3+B,\quad Z=aX,\quad aB\ne0.}
\tag{27}
\]
The apparent \(N=18\), constant-\(Z\) kernel gives zero, not a
nonzero scalar; no \(N>18\) scalar exists.

Since \(P=X^3+B\) is squarefree, every tail of normalized order
\(r<17/2\) is divisible by \(P\).  Induct over the discrete support,
assuming \(P\mid S_u\) for every supported \(u<r\).  Reduce the zero
bracket equation at order \(2r<17\) modulo \(P\).  In every unequal
convolution pair \(u+v=2r\), one index is below \(r\), so its factor
is divisible by \(P\).  The \(C\)-operator has an explicit factor
\(P\), and the \(k\)-term involves \(S_{2r-9}\), whose order is
below \(r\).  The surviving term is a nonzero multiple of
\[
 P'S_r^2\pmod P.
\]
Thus \(P\mid S_r^2\), and squarefreeness gives \(P\mid S_r\).

Now reduce \(Z_{17}\) modulo \(P\).  In every unequal pair
\(S_rS_{17-r}\), one index is below \(17/2\), so that product
vanishes modulo \(P\).  The \(kS_8\) and \(CPB\) terms also vanish.
Therefore (27) requires an actual half-order tail
\[
 S_{17/2}^2\equiv aX\pmod P.
\tag{28}
\]
If no lower \(P\)-multiple tail is present, the order-\(17\)
equation upgrades (28) to the Hensel congruence modulo \(P^2\)
treated in Sections 2--4.  If a lower tail is present, take its least
order \(\alpha\).  Its first interaction with the unit
\(S_{17/2}\) gives (29) below; hence only
\(\alpha=13/2\) can survive.  Section 6 obstructs that possibility
with every cross-character descendant retained.

It remains to show that a finer denominator cannot hide in the
formal lift.  First note that the preceding argument eliminates
every tail below \(17/2\): the only possible least order is \(13/2\),
and Section 6 obstructs it.  Now suppose
\(\gamma\notin\frac12\mathbf Z\) is the least off-half-lattice order
in a surviving lift.

* For completeness, if one starts before that elimination with a
  least \(\gamma<17/2\), its self-equation occurs first and makes it
  \(P\)-divisible.  Write \(S_\gamma=PQ\).  At order
  \(\gamma+17/2\), every other unequal pair contains an earlier
  \(P\)-divisible factor.  The remaining zero-kernel equation is
  \[
  V^3=C P^{\,13/2-\gamma}.
  \tag{29}
  \]
  Since \(6<\gamma<17/2\), the exponent lies strictly between
  \(-2\) and \(1/2\); unique factorization leaves only exponent zero,
  namely \(\gamma=13/2\).

* If \(\gamma>17/2\), there is no positive-order tail below
  \(17/2\) in the surviving branch.  Hence its first interaction
  with the unit \(S_{17/2}\) occurs before its self-interaction and
  contains no other off-lattice pair.  The zero-kernel equation is
  \[
  R^3=C P^{\,19/2-\gamma}.
  \tag{30}
  \]
  For \(17/2<\gamma\), the exponent is below one.  Its only
  nonnegative value compatible with a polynomial cube is zero:
  \(\gamma=19/2\), again a half-integer.  This is the silent
  order-\(19\) direction of Section 5.  Its forced descendants are
  retained there, and the order-\(53\) consistency equation forces
  its coefficient to zero.

Unique factorization justifies the word "only": \(P\) is
squarefree, and all exponents of a polynomial cube are divisible by
three.  Hence no tail outside the half-integer lattice survives.

Every rationally ramified scalar branch therefore reduces to:

1. the two Hensel sign orbits of Sections 2--4;
2. the earlier \(13/2\) all-character chain of Section 6;
3. the later \(19/2\) silent direction and upper-term descendants
   of Section 5.

All three are formally obstructed.  This is the desired
all-rational-ramification closure of the half-order resonance.
