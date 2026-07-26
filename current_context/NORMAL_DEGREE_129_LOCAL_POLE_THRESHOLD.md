# The local pole threshold at normal degree \((12,9)\)

Date: 26 July 2026

The integer-graded recurrence and the rationally ramified resonance
analysis are kept separate below.  This separation is essential: the
honest pole scale \(\rho=2\) has a half-order resonance which is
invisible after an unjustified normalization to primitive integer
orders.  Sections 4--5 include that resonance, all eight of its
Hensel branches, every rational support character, and the delayed
upper and \(P\)-multiple tails.

## Outcome

Let
\[
 g=w^9+\sum_{j=2}^9c_jw^{9-j},\qquad
 s=g^{1/9}=w+O(w^{-1}),
\]
and let \(f\) be monic of degree twelve.  At fixed \(s\), write
\[
 f=\Phi(s)+\sum_{\ell\geq1}A_\ell s^{-\ell},
\tag{1}
\]
where \(\Phi\) is a degree-twelve polynomial with constant
coefficients.  Suppose
\[
 A_1,\ldots,A_7\in\mathbf C
\]
and consider a place at which
\[
 \rho=\max_{2\leq j\leq9}
 \frac{\operatorname {pole}(c_j)}j>0.
\tag{2}
\]
Then
\[
 \boxed{\operatorname {pole}(A_8)\geq\frac72\rho.}
\tag{3}
\]

The proof is local and remains valid after a finite ramified
extension of the local parameter.  It allows every upper
approximate-root constant in \(\Phi\).

The smooth extremal boundary is a Davenport--Stothers/Belyi stratum
with passport
\[
 [3^{12}],\qquad[4^9],\qquad[20,1^{16}],
\tag{4}
\]
and has pole ratio \(20\).  A hypothetical ratio below \(7/2\)
must instead have the common-cubic leading form
\[
 f_0=P^4,\qquad g_0=P^3,\qquad
 P=X^3+AX+B.
\tag{5}
\]
The first transverse normal and the upper constants give a
common-cubic background.  An all-jet recurrence excludes the
primitive integer orders \(17,18,19\).  A separate rational
filtration reduces every ramified scalar to one half-order Hensel
problem; its two sign orbits and its two exceptional indirect chains
are all formally obstructed.

This is the degree-nine analogue of the local degree-eight pole
theorem.  Combined with the Laurent-line criterion, (3) is exactly
the estimate needed at the arithmetic frontier \((12,9)\).

## 1. Laurent weight and the sub-extremal lemma

The terminal coefficient \(A_8\) has natural weight
\[
 12+8=20.
\tag{6}
\]
After a finite local extension, let \(t\) be an honest uniformizer
and let the integral pole scale be \(m\).  Put
\[
 X=t^mw,\qquad
 \bar g=t^{9m}g(t,t^{-m}X),\qquad
 \bar f=t^{12m}f(t,t^{-m}X).
\tag{7}
\]
Both scaled coordinates are regular at \(t=0\).  For the leading-form
calculation one may measure all orders in units of \(m\), so that
\(\rho=1\) as a rational weight.  One may not assume that every
supported order is then an integer.  Sections 2--4 first record the
primitive integer slice, while Section 5 closes the remaining
rational orders in the honest \(t\)-grading.

For the primitive integer slice \(m=1\), write \(z=t\).  The formulas
in Sections 2--4 use this notation.

If \(\operatorname {pole}(A_8)<7/2\), then in particular its pole is
strictly smaller than its natural weight \(20\).  The conserved
levels and the terminal level therefore vanish in the weighted
leading form.  Equivalently,
\[
 \deg_X(\bar f_0^{\,3}-\bar g_0^{\,4})\leq15.
\tag{8}
\]

The following sub-extremal polynomial-\(abc\) lemma is sharp:
\[
 \deg(p^3-q^4)\leq15
 \quad\Longrightarrow\quad
 p^3=q^4
\tag{9}
\]
for monic \(\deg p=12,\deg q=9\).  No coprimality hypothesis is
needed.  Indeed, if the nonzero difference is \(R\), divide the
three-term equation by \(D=\gcd(p^3,q^4)\), of degree \(d_0\).
Mason's theorem gives
\[
 36-d_0
 \leq 12+9+(15-d_0)-1
 =35-d_0,
\]
a contradiction.  Unique factorization then gives (5).

For comparison, equality at degree sixteen in the coprime smooth
case gives the three branch partitions in (4).  Their ramification
contributions are
\[
 12(3-1)+9(4-1)+(20-1)=70=2\cdot36-2.
\]
Thus there is no fourth branch value, and the fixed passport has
only finitely many covers.  Monic depression leaves only weighted
scaling, so \(A_8=C\tau^{20}\).  Every one-pole curve in this smooth
stratum consequently has ratio \(20\), far above (3).

## 2. First transverse normal to the common cubic

The tangent space to \(P^3\) consists of multiples of \(P^2\).
After absorbing a tangent change of \(P\), write
\[
 \bar g=P^3+\varepsilon z^\delta S,\qquad
 \deg S<6.
\tag{10}
\]
Divide
\[
 S^2=P^2H+R,\qquad \deg R<6.
\tag{11}
\]
The polynomial part of \(\bar g^{4/3}\) begins
\[
 \bar f
 =P^4+\frac43\varepsilon z^\delta PS
 +\frac29\varepsilon^2z^{2\delta}H.
\tag{12}
\]
The quadratic term in
\(\bar f^{\,3}-\bar g^{\,4}\) is
\[
 -\frac23\varepsilon^2z^{2\delta}P^6R.
\tag{13}
\]
For \(\delta\leq6\), this occurs below the first possible scaled
constant invariant weight \(13\), so the conserved equations force
\(R=0\).  These are exactly the orders needed to identify the
post-order-six normal form.  Orders \(\delta\geq7\) are not discarded
here; all of them are retained simultaneously in Section 4.  Thus,
for the present low-order calculation,
\[
 P^2\mid S^2,\qquad S=PQ,\qquad \deg Q\leq2.
\tag{14}
\]

For scaled polynomials define
\[
 \mathcal B(\bar f,\bar g)
 =z(\bar f_z\bar g_X-\bar f_X\bar g_z)
 -12\bar f\bar g_X+9\bar f_X\bar g.
\tag{15}
\]
The original bracket is \(z^{-21}\mathcal B\).  Substituting
(12)--(14), the first remaining transverse term is
\[
 \frac49\varepsilon^3z^{3\delta}Q^2
 \left((\delta-6)QP'+3PQ'\right).
\tag{16}
\]
It cannot be a nonzero constant in \(X\).  If it vanishes, then
\[
 Q^3=C P^{\,6-\delta}.
\tag{17}
\]
Degree and factor comparison leave only
\[
\begin{array}{c|c|c}
\delta&P&Q\\ \hline
4&L^3&cL^2\\
5&L^3&cL\\
6&\text{arbitrary cubic}&c.
\end{array}
\tag{18}
\]
In the first two rows, depression gives \(L=X\), so the leading form
has no genuine coefficient pole and the valuation must be restarted.
The only positive-pole silent normal is therefore
\[
 \bar g=P^3+c z^6P.
\tag{19}
\]

In the original variables \(U=z^{-3}P\), its exact approximate-root
pair is the one-variable composition
\[
\begin{aligned}
 g&=U^3+cU,\\
 f&=U^4+\frac43cU^2+\frac29c^2,
\end{aligned}
\tag{20}
\]
up to upper constants and target translations.

## 3. All upper approximate-root constants

Let the highest surviving upper term be
\[
 \kappa_\ell(g^{\ell/9})_+,
\qquad
 \ell\in\{11,10,8,7,6,5,4,3,2,1\};
\tag{21}
\]
the \(\ell=9\) term is a target shear.  At (5), put
\[
 H_\ell=(P^{\ell/3})_+.
\]
Its leading scaled bracket is
\[
 3\kappa_\ell z^{12-\ell}P^2
 \left(3PH_\ell'-\ell P'H_\ell\right).
\tag{22}
\]
It cannot be a nonzero constant.  Vanishing gives
\[
 H_\ell^3=P^\ell.
\tag{23}
\]
If \(3\nmid\ell\), equation (23) forces \(P=L^3\), which is the
regular-scale restart already removed.  If \(3\mid\ell\), the term
is a polynomial in \(P\).  Thus the only surviving upper terms are
\[
 j(g^{2/3})_+,\qquad k(g^{1/3})_+.
\tag{24}
\]

## 4. The entire post-order-six tail

No finite-jet common-component assertion is needed.  Use the
canonical cubic approximate root to absorb, order by order, every
multiple of \(P^2\) in the lower coordinate.  Section 2 shows that
all transverse orders below six vanish and that the only genuine
order-six normal is \(cz^6P\).  Hence the full remaining tail is
\[
 \bar g=P^3+cz^6P+\Delta,\qquad
 \Delta=\sum_{r\geq7}z^rS_r,\qquad \deg S_r<6.
\tag{25}
\]
This includes composite jets, singular tangent jets, and ordinary
target-weight jets; none is assumed to lift to an identically
zero-Jacobian family.

The canonical cubic may depend on \(z\).  This introduces no omitted
terms in the normal calculation.  In the determinant part of (15),
replace
\[
 z\partial_z
 \quad\text{by}\quad
 z\partial_z-\frac{zP_z}{P_X}\partial_X.
\]
Adding a multiple of the \(X\)-derivative does not change a
determinant, and the new derivation holds \(P\) fixed.  Thus every
\(P_z\)-term cancels identically.  Division modulo \(P^2\) then gives
the canonical normal representative of degree below six used in
(25).  The formulas below are therefore covariant formulas in the
moving approximate-root gauge, not an assumption that the
coefficients of \(P\) are constant.

Put
\[
\begin{aligned}
 Q&=(\Delta/P)_+,\\
 H&=(\Delta^2/P^2)_+,\\
 R&=(\Delta^2)_{\rm rem\,P^2}
   =\sum_NR_Nz^N.
\end{aligned}
\tag{26}
\]
Through order nineteen, the exact polynomial part is
\[
\begin{aligned}
\bar f={}&P^4+\left(\frac43c+j\right)z^6P^2+kz^9P
 +\frac43P\Delta\\
&+\left(\frac49c+\frac23j\right)z^6Q
 +\frac29H.
\end{aligned}
\tag{27}
\]
The next binomial term is cubic in \(\Delta\) and starts at order
twenty-one.

For each \(S_r\), write
\[
 S_r=PQ_r+B_r,\qquad \deg Q_r,\deg B_r\leq2,
\tag{28}
\]
and interpret missing subscripts as zero.  Put
\[
 C=2c+3j,\qquad W_N=2R_N+3kS_{N-9}.
\]
Direct substitution in (15) gives, for \(13\leq N\leq19\),
\[
\boxed{
\begin{aligned}
\mathcal B_N={}&
-\frac23CP
 \left((N-15)B_{N-6}P'+3PB_{N-6}'\right)\\
&-PW_N'+\frac{18-N}{3}P'W_N\\
&+\mathbf1_{N=19}\frac{2cC}{9}
  \left(Q_7P'+3PQ_7'\right).
\end{aligned}}
\tag{29}
\]
This convolution identity includes interactions between different
jets, rather than only the self-interaction of a first split.  The
last line is the delayed pairing of the order-\(13\) \(Q_7\)-term in
\(\bar f\) with the order-\(6\) \(cP\)-term in \(\bar g\).

In the primitive integer slice, a finite terminal pole with ratio
below \(7/2\) would make the first constant scaled bracket occur at
one of
\[
 N=17,\quad18,\quad19,\qquad
 N=20-\operatorname {pole}(A_8).
\tag{30}
\]
At orders \(17\) and \(18\), define
\[
 Z_N=W_N+2CPB_{N-6}.
\tag{31}
\]
The first two lines of the master formula combine exactly to give
\[
\begin{array}{c|c|c}
N&Z_N&\mathcal B_N\\ \hline
17&2R_{17}+3kS_8+2CPB_{11}&
 \frac13(P'Z_{17}-3PZ_{17}')\\[1mm]
18&2R_{18}+3kS_9+2CPB_{12}&
 -PZ_{18}'.
\end{array}
\tag{32}
\]
This includes every self-term and every cross-term.  For example, an
order-nine jet \(S\) and an order-ten jet \(V\) contribute
\[
 R_{19}=2(SV/P^2)_{\rm rem}.
\]

The order-\(18\) operator cannot be a nonzero constant.  The
order-\(17\) operator has one apparent exceptional family:
\[
 P=X^3+B,\qquad Z=aX,\qquad
 \frac13(P'Z-3PZ')=-aB.
\tag{33}
\]
If \(aB\ne0\), then \(P\) is squarefree.  The earlier order-fourteen
equation gives \(P\mid S_7\) when \(C=0\): its only other homogeneous
possibility would require \(R_{14}^3\) to be a constant multiple of
\(P^4\).  When \(C\ne0\), the still earlier order-thirteen equation
already gives \(P\mid S_7\), unless \(P\) is a cube.  Reduce the
order-sixteen instance of (29) modulo \(P\).  Every term except
\(R_{16}P'\) vanishes, so
\[
 R_{16}\equiv S_8^2\equiv0\pmod P.
\tag{34}
\]
Squarefreeness gives \(P\mid S_8\).  It follows that \(R_{17}\),
\(3kS_8\), and \(2CPB_{11}\) are all divisible by \(P\).  Hence
\(Z_{17}\) is divisible by \(P\), contradicting \(Z_{17}=aX\).

At order \(19\), the delayed last line of (29) must be retained.
The earlier zero equations give
\[
 S_7=PQ_7,\qquad S_8=PQ_8,\qquad S_9=PQ_9+b
\]
when \(C\ne0\).  Writing \(d=4b+3k\), the order-\(16\) equation gives
\[
 B_{10}=-\frac{d}{2C}Q_7.
\]
The order-\(19\) remainder can then be written
\[
 W_{19}=PV+D_0,\qquad
 D_0=dB_{10},\qquad \deg V,\deg D_0\leq2.
\]
The delayed term combines with \(D_0\) after setting
\[
 D=D_0-\frac{2cC}{3}Q_7.
\]
If \(\mathcal B_{19}=\lambda\), reduction modulo \(P\) and substitution
into (29) yield
\[
 P'D+3\lambda=PM,\qquad
 3PZ'+4P'Z=-(3D'+M),
\]
with \(\deg M\leq1,\deg Z\leq2\).  The leading degree forces \(Z=0\);
then
\[
 3PD'+P'D=-3\lambda.
\]
Its left side has degree at least two for every nonzero
\(\deg D\leq2\).  Hence \(D=0\) and \(\lambda=0\).  The case \(C=0\)
is the simpler operator
\(-\frac13(3PW_{19}'+P'W_{19})\), which is constant only when it
vanishes.  Thus no primitive integer order \(17,18,\) or \(19\)
supplies the scalar.

## 5. Rational ramification and the half-order closure

Retain the honest integral scale \(m=\rho\), but divide displayed
orders by \(m\).  At a possible first scalar order \(N\) in
\[
 \frac{33}{2}<N<20,
\]
all quadratic, delayed-upper, and previously forced contributions
have a normal representative \(Z\), \(\deg Z<6\), on which the scalar
operator is
\[
 \mathscr D_N(Z)
 =-2PZ'+\frac23(18-N)P'Z.
\tag{35}
\]
Degree comparison shows that a nonzero constant is possible only for
\[
 N=17,\qquad P=X^3+B,\qquad Z=aX,\qquad aB\ne0.
\tag{36}
\]
In particular \(P\) is squarefree.

Induct over the discrete rational support below order \(17/2\).
At the self-order \(2r<17\), every unequal convolution contains a
strictly earlier \(P\)-divisible factor; reduction modulo \(P\)
therefore leaves a nonzero multiple of \(P'S_r^2\).  Squarefreeness
forces
\[
 P\mid S_r\qquad(r<17/2).
\tag{37}
\]
Reducing (36) modulo \(P\) then forces an actual half-order tail
\[
 S_{17/2}^2\equiv aX\pmod P.
\tag{38}
\]
After scaling \(X\) and absorbing its \(P\)-multiple part, this is the
Hensel equation
\[
 S^2\equiv X\pmod{(X^3-1)^2}.
\tag{39}
\]
Its eight roots form two sign/cyclic orbits.

For the six mixed-sign roots, the order-\(51\) correction operator
\[
 \mathscr L_{51}(R)=2PR'+5P'R
\]
has a two-dimensional cokernel and the exact forcing has nonzero
cokernel values
\[
 -\frac{43010}{243},\qquad \frac{17290}{243}.
\tag{40}
\]
The two equal-sign roots lift uniquely through that equation with
\[
 V=\frac1{16}X^4-\frac{11}{144}X,
\tag{41}
\]
but at order \(68\) the operator
\[
 \mathscr L_{68}(R)=PR'+\frac{16}{3}P'R
\]
has a cokernel functional which evaluates to \(945/2\ne0\).

Two indirect kernels must also be included.  A least earlier tail can
interact silently with \(S_{17/2}\) only at order \(13/2\); it is
\(aPX\) in the equal-sign normalization.  Keeping all six coefficients
of every descendant, all three \(P\mathbf C[X]_{<3}\) kernel
characters, and every nonlinear cross-product, the apparent
order-\(39\) obstruction is canceled by
\[
 Q_{18}=-\frac{a^4}{9}.
\]
The first invariant inconsistency is instead at order \(47\): its
equal-sign equations contain
\[
 u_0=u_1=u_2=0,\qquad 8u_2=3a^2,
\]
and the mixed-sign residuals are
\[
 -2a,\qquad \frac{28}{27}a.
\tag{42}
\]
Thus \(a=0\) in both orbits.  The only later zero kernel is the
order-\(19/2\) direction; its forced descendants reach an order-\(53\)
equation which forces its coefficient to zero.

Finally, let \(\gamma\) be the least support order outside
\(\frac12\mathbf Z\).  Its first interaction with the unit
\(S_{17/2}\) integrates to
\[
 Q^3=C_0 P^{13/2-\gamma}\quad(\gamma<17/2),
\qquad
 R^3=C_0 P^{19/2-\gamma}\quad(\gamma>17/2).
\tag{43}
\]
Unique factorization for squarefree \(P\) leaves only
\(\gamma=13/2\) or \(19/2\), the two already obstructed directions.
Hence no finer rational denominator survives.  Arbitrary upper
constants satisfy \(2c+3j=0\); their forced descendants, and the
\(k\)-term, leave the cokernel values (40)--(42) unchanged.

The exact all-character and all-rational calculations in this section
are independently checked by
`verify_normal_degree_129_half_order_hostile_audit.py`,
`verify_normal_degree_129_indirect_chain_obstruction.py`,
`verify_normal_degree_129_indirect_chain_upper_audit.py`, and
`verify_normal_degree_129_rational_filtration.py`.
They close the ramification gap and prove (3).

## 6. Scope

The theorem is a local invariant-boundary statement.  It does not
assume that the coefficient curve is rational, and it does not use
the global one-pole classification.  Its inputs are:

* polynomial \(abc\) at the sub-extremal boundary;
* the finite smooth Belyi passport (4);
* the common-cubic normal operator (16);
* the upper-character operator (22);
* the repaired all-jet split calculation (29)--(34);
* the all-branch half-order cokernels (35)--(42); and
* the rational-support filtration (43).

It is therefore available both on a split cube chart and at a place
of a connected cubic Kummer normalization.
