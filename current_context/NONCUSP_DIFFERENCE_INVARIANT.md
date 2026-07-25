# Non-cusp boundary difference: a contact gap, not a DZ extremal pair

Date: 24 July 2026

Put
\[
D(y)=q(y)^2-Lp(y)^3,\qquad \deg p=8,\quad\deg q=12,
\]
where \(L\) is the ratio of the squared/cubed leading coefficients.  Thus
the degree-24 term always cancels.  The two bounded branches give different
amounts of information about the next term.

## 1. Case c: contact is at least four

On the case-c critical line \(x=0\), the fixed negative-\(y\) base terms
vanish, so \(p,q\) are obtained by evaluating the positive parts
\[
P_+(h,y),\qquad Q_+(h,y)
\]
at the nonzero constant \(h=-t\).  The all-parameter approximate-root
theorem gives
\[
Q_+=\sum_{j=4}^{12}c_jA_j+S_3,\qquad
A_j=(P_+^{j/8})_+,\qquad \deg_yS_3\le3.
\]
The universal fractional descent now proves
\[
c_{11}=c_{10}=c_9=c_7=c_6=c_5=0.
\]
The lower four modes are eliminated by the required-\(r_4\) square cascade
in `CASE_C_UNIVERSAL_FRACTIONAL_DESCENT.md`.
After evaluation at \(h=-t\), write \(\ell^8\) for the leading coefficient
of \(p\).  Then \(A_j=\ell^j y^j+\cdots\), the leading coefficient of
\(q\) is \(c_{12}\ell^{12}\), and hence \(L=c_{12}^2\).  Since
\[
A_{12}-p^{3/2}=O(y^{-1}),
\]
one has
\[
\deg(A_{12}^2-p^3)\le11.
\]
It follows immediately that
\[
\boxed{\deg D\le20.}
\]

There is a sharper integral-resonance spectrum.  If \(c_8\ne0\), the
unique highest term of \(D\) is
\[
2c_{12}c_8\ell^{20}y^{20},
\]
so \(\deg D=20\).  If \(c_8=0,c_4\ne0\), the corresponding cross term
gives \(\deg D=16\).  If both integral modes vanish, then
\(\deg D\le15\).  Thus
\[
\boxed{\deg D\in\{20,16\}\quad\text{or}\quad\deg D\le15.}
\]
intersection multiplicity at the common cusp direction at infinity is
\[
I_\infty(\Gamma,C_L)=24-\deg D,
\]
and belongs to
\[
\boxed{\{4,8\}\ \cup\ \{9,10,\ldots\}.}
\]
In particular, contact one, two, and three at infinity are impossible.
The finite alternatives now read off the highest surviving integral
approximate power.

This is a genuine small invariant of the non-cusp curve.  It does not say
that \(D=0\), and it is far from the extremal Davenport--Zannier regime.
Under the additional hypothesis \(\gcd(p,q)=1\), Mason--Stothers gives
\[
\deg\operatorname{rad}D\ge5,
\]
because \(24\le\deg\operatorname{rad}(pqD)-1\le
19+\deg\operatorname{rad}D\).  The classical DZ classification concerns
equality at this lower boundary; the case-c result above is instead the
upper contact spectrum above.  No checked DZ theorem converts this
fourfold contact into a contradiction.

## 2. Later a/b improvement: contact is at least four

The negative first-block result below remains correct, but the remaining
four blocks have now been incorporated by the coordinate-free identity
\[
\{P,Q^2-LP^3\}=2Q\{P,Q\}.
\]
The resulting theorem, proved in
`AB_BOUNDARY_CONTACT_SPECTRUM.md`, is
\[
\deg(b_0^2-La_0^3)\in\{20,16,12,8\}\quad\text{or}\quad\le7.
\]
Thus the full a/b system has contact at least four at infinity, and the
possible contact orders are \(\{4,8,12,16\}\) or at least \(17\).

The following countermodel should now be read only as showing why the
first block by itself cannot prove that result.

For the a/b asymptotic curve \(p=a_0(w),q=b_0(w)\), the leading ratio only
gives \(\deg D\le23\).  Even the first bracket block does not improve it.
Indeed take
\[
p=w^8+w^7,\qquad q=w^{12},\qquad L=1,
\]
and set
\[
a_1=p',\qquad b_1=q'.
\]
Then the exact first block
\[
a_1q'-p'b_1=0
\]
holds with the required degree caps \(\deg a_1=7,\deg b_1=11\), while
\[
\deg(q^2-p^3)=23.
\]
This is not a full five-block solution.  It is a precise negative result:
degree \((8,12)\), the leading cusp direction, and the first Jacobian block
do not exclude simple contact.  Any a/b analogue of the case-c contact gap
must use the remaining four blocks together, not degree data or the tangent
syzygy alone.  The later contact-spectrum theorem does exactly that.

## Strategic consequence

For case c, all fractional resonances are now gone; the remaining
non-brute-force target is to control the two integral modes \(c_8,c_4\)
or exploit the discrete contact spectrum geometrically.  For a/b, the
coordinate-free consequence is now available and
is stronger than cancellation of \(w^{23}\): it gives the entire contact
spectrum above.  A direct DZ classification is still premature unless one
first reaches the lower Mason--Stothers boundary and proves the needed
coprimality.
