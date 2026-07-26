# Cyclic characters force unbounded delay in the two-block filtered recurrence

Date: 26 July 2026

## Outcome

Consider the repeated-root top data
\[
 d=x^s(x^E+\ell),\qquad
 p_0=d^2+ux,\qquad q_0=d^3,
 \qquad s\ge2,\quad E\ge1,\quad \ell u\ne0,
\tag{1}
\]
of common-root degree \(g=s+E\).  The exact filtered recurrence does
not admit a uniform bounded-defect exclusion on this family.

More precisely, suppose
\[
 E\mid 2s-1.
\tag{2}
\]
Then the cyclic group \(\mu_E\) makes every defect-\(k\) jet a single
character.  The defect-\(k\) cokernel can be nonzero only if
\[
 \boxed{
 r\equiv k(s-1)\pmod E
 \quad\text{for some}\quad 1\le r\le k-2.
 }
\tag{3}
\]
This is an exact support condition, not an experimental pattern.

Consequently, for every prescribed cutoff \(K\), choose any odd
integer
\[
 E>3K-4,\qquad s={E+1\over2}.
\tag{4}
\]
Then all obstruction vectors through defect \(K\) vanish
identically in \(\ell,u\), and the reciprocal-bounded filtered jets
exist through that order.

Thus:

> There is no absolute \(K\) such that every two-block endpoint (1)
> is excluded by defect at most \(K\).

In particular, the proposed bound \(K=6\) is false.  A concrete
algebraic endpoint with \(g=14,E=9,s=5\) survives through defect six
and is first necessarily excluded at defect seven.

This is not a polynomial Keller counterexample.  For each fixed
endpoint the recurrence may still fail at a later, \(E\)-dependent
defect.  The theorem instead rules out an important proof strategy:
an all-two-block exclusion cannot come from checking any fixed
finite list of filtered defects.  It needs either an unbounded
cyclic descent, a generating-function argument for the full defect
sequence, or additional global rigidity.

## 1. The exact filtered recurrence

Put
\[
 A=p_0'=u+2dd',\qquad B=q_0'=3d^2d'.
\tag{5}
\]
The bounded defect-one pair is
\[
 p_1=-{4d'\over3u^2},\qquad
 q_1={1\over u}-{2dd'\over u^2},
\tag{6}
\]
and satisfies \(Aq_1-Bp_1=1\).

Assume bounded jets have been constructed through defect \(k-1\):
\[
 \deg p_i\le2g-i,\qquad
 \deg q_i\le3g-i.
\tag{7}
\]
At defect \(k\), write
\[
 h_k=-{1\over k}
 \sum_{\substack{i+j=k\\i,j\ge1}}
 \left(jp_i'q_j-ip_iq_j'\right).
\tag{8}
\]
The next equation is
\[
 Aq_k-Bp_k=h_k.
\tag{9}
\]
Since \(\gcd(A,B)=1\), there is a unique residue
\[
 q_k\equiv A^{-1}h_k\pmod B,\qquad \deg q_k<3g-1.
\tag{10}
\]
The exact obstruction vector consists of the coefficients of
\[
 x^{3g-k+1},\ldots,x^{3g-2}
\tag{11}
\]
in this residue.  If they vanish, then \(\deg q_k\le3g-k\), and
\[
 p_k={Aq_k-h_k\over B}
\tag{12}
\]
is a polynomial of degree at most \(2g-k\).  Indeed every term of
\(h_k\) has degree at most \(5g-k-1\), so the degree bound follows
after division by the degree-\((3g-1)\) polynomial \(B\).

This is the same exact modular recurrence used in the arbitrary
common-root obstruction
\[
 \operatorname{rem}_{\,3d^2d'}
 \left((2dd'+u)^{-1}h_k\right).
\tag{13}
\]

## 2. Cyclic-character theorem

Let \(\zeta^E=1\), and call \(f\in\mathbf C[x]\) a character-\(a\)
polynomial if
\[
 f(\zeta x)=\zeta^a f(x).
\tag{14}
\]
The polynomial \(d=x^s(x^E+\ell)\) has character \(s\), while \(d'\)
has character \(s-1\).

Under (2),
\[
 2s\equiv1\pmod E.
\tag{15}
\]
It follows that \(p_0\) has character \(1\), \(q_0\) has character
\(3s\), \(A\) is invariant, and \(B\) has character \(3s-1\).
Set
\[
 \delta=s-2.
\tag{16}
\]
We claim inductively that
\[
 \boxed{
 p_k\text{ has character }P_k=1+k\delta,\qquad
 q_k\text{ has character }Q_k=3s+k\delta.
 }
\tag{17}
\]
For \(k=0\) this was just checked.  Formula (6) gives character
\(s-1=1+\delta\) for \(p_1\), and \(q_1\) is invariant.  The latter
agrees with (17), because
\[
 3s+\delta=4s-2=2(2s-1)\equiv0\pmod E.
\]

For the induction step, both summands in (8) have character
\[
 P_i-1+Q_j=3s+k\delta=Q_k.
\tag{18}
\]
Thus \(h_k\) has character \(Q_k\).  Multiplication by the invariant
\(A\) and reduction modulo the character polynomial \(B\) preserve
the \(\mu_E\)-decomposition.  The unique residue (10) therefore has
character \(Q_k\).  Finally
\[
 (3s-1)+P_k=3s+k\delta=Q_k,
\tag{19}
\]
so (12) has character \(P_k\).  This proves (17).

The forbidden exponent at offset \(r\) in (11) is
\[
 n=3g-k+r,\qquad 1\le r\le k-2.
\tag{20}
\]
Since \(g=s+E\), its character is
\[
 n\equiv3s-k+r\pmod E.
\tag{21}
\]
It can occur in \(q_k\) only if this equals \(Q_k\).  Using (16)
gives exactly
\[
 r\equiv k(s-1)\pmod E.
\tag{22}
\]
This proves (3).

## 3. No uniform defect bound

Fix \(K\ge2\), choose \(E,s\) as in (4), and suppose a forbidden
coefficient occurs at some \(k\le K\).  Because
\[
 s-1={E-1\over2},
\]
condition (3) implies
\[
 2r+k\equiv0\pmod E.
\tag{23}
\]
But
\[
 0<2r+k\le3k-4\le3K-4<E,
\tag{24}
\]
which is impossible.  The obstruction vector is therefore zero at
every defect through \(K\).  Induction using Section 1 constructs
all bounded jets through that order.

The delay can be quantified.  For odd \(E\ge5\) and
\(s=(E+1)/2\), the first defect at which a forbidden character is
even permitted is
\[
 \boxed{
 k_0=\text{the smallest odd integer at least }
 \left\lceil{E+4\over3}\right\rceil.
 }
\tag{25}
\]
At \(k_0\), the unique permitted forbidden offset is
\[
 r_0={E-k_0\over2}.
\tag{26}
\]
Indeed an odd \(k\) first reaches the multiple \(E\) in
\(2r+k\), while an even \(k\) would have to reach \(2E\).
This linear growth is the structural source of the unbounded delay.
Equation (25) says only when a class may appear; it does not assert
that its coefficient is nonzero for every parameter.

## 4. Exact hostile example to defect six

Take
\[
 E=9,\qquad s=5,\qquad g=14,\qquad \ell=1.
\tag{27}
\]
The character test makes defects two, three, four, and six vanish
identically.  Defect five has one possible coordinate.  Apart from a
nonzero scalar and a power of \(u\), it is
\[
\begin{aligned}
 P_5(u)={}&186838225u^5+23740768548u^4
 +532637805132u^3\\
 &+4447199793231u^2
 +15962498987778u
 +23724081064404.
\end{aligned}
\tag{28}
\]
Choose any root \(\alpha\) of \(P_5\).  Its constant term is nonzero,
so \(\alpha\ne0\).  Over the exact number field
\(\mathbf Q(\alpha)\), all bounded equations through defect six
are soluble.

At defect seven, the single possible coordinate has numerator
\[
\begin{aligned}
 P_7(u)={}&3559879483055u^8
 +1254368611253457u^7\\
 &+74129178578871600u^6
 +1662884438039607177u^5\\
 &+18545694665345607285u^4
 +115093632573725049054u^3\\
 &+411718849720612848108u^2
 +810110778243003255744u\\
 &+713249706931339822992.
\end{aligned}
\tag{29}
\]
Exact Euclidean division gives
\[
 \gcd_{\mathbf Q[u]}(P_5,P_7)=1.
\tag{30}
\]
Thus every algebraic branch surviving through defect six fails at
defect seven.  This example is a finite filtered countermodel to the
bound six, not a counterexample to the Jacobian conjecture.

## 5. Consequence for the repeated-root route

The exact chamber formula
\[
 2s-3=qE+j,\qquad
 \operatorname{rem}_d(d')^3
 =(-1)^{q+1}E^3\ell^{q+3}x^{s+j}
\tag{31}
\]
still controls the first nonlinear remainder.  The cyclic theorem
shows why formulas at any fixed list of defects cannot settle all
\((q,j)\)-chambers: the resonant subfamily
\[
 2s-1=E
\tag{32}
\]
has no admissible cokernel coordinate until defect on the order of
\(E/3\).

A promising next target is therefore not “defect at most six,” but
one of:

1. derive a generating recurrence for the single allowed character
   along (32) and prove its successive obstruction polynomials have
   no common nonzero root;
2. descend an equivariant formal solution through the
   \(\mu_E\)-quotient and find a global incompatibility;
3. prove that actual polynomial Keller endpoints cannot enter the
   resonant chamber (32), using data not present in the filtered
   top-form recurrence.

The character theorem, the exact \(E=9,s=5\) obstruction
polynomials, their coprimality, and direct recurrence samples are
audited by
`verify_general_two_block_cyclic_defect_delay.py`.
