# The exceptional cubic graph branch after the \(V\)-subduction

Date: 25 July 2026

## Outcome

This note closes the graph-degree \(L=3\) exception left in
`WEIGHTED_LIFT_SAGBI_AFTER_W_MARKOV_AND_NEXT_GENERATORS.md`.
It concerns the exact boundary generators
\[
C,\ B,\ A,\ T,\ U,\ W
\]
and the exact polynomial \(V\) produced there.  It does **not** assert
termination of the full SAGBI completion.

The actual cubic boundary polynomial is not arbitrary.  Its fixed
jets are
\[
f(1)=1,\qquad f'(1)=-\frac{57}{34}.
\]
Consequently it has the form
\[
f(u)=ru^3+du^2+
 \left(-\frac{57}{34}-3r-2d\right)u
+ \left(\frac{91}{34}+2r+d\right),
\qquad r\ne0.
\tag{1}
\]

For every polynomial (1), the projected \(L=3\) subduction of \(V\)
by the old displayed generators stops at a new value.  More precisely:

\[
\begin{array}{c|c}
\text{coefficient stratum}&
\text{first unreducible projected value}\\ \hline
d\ne0&(-11,138),\\
d=0,\ r\ne-91/68&(-11,136),\\
d=0,\ r=-91/68&(-11,133).
\end{array}
\tag{2}
\]

Thus the formal value \((-11,40,33)\) of \(V\), although reducible
after the cubic graph projection, always exposes a later genuinely
new projected value.  Together with the already proved
nonmembership for \(L=2\) and \(L\ge4\), this removes the only
graph-degree exception in the statement that the displayed
\(\{C,B,A,T,U,W\}\) is incomplete.

## 1. The finite projected semigroup table

At \(L=3\), the projected values are
\[
\begin{aligned}
C&=(1,3),& B&=(-1,17),& A&=(-2,18),\\
T&=(-6,82),&U&=(-5,71),&W&=(-7,85).
\end{aligned}
\tag{3}
\]
For a monomial \(C^cB^bA^aT^tU^vW^w\) of first component \(-11\),
eliminating \(c\) gives
\[
c=-11+b+2a+6t+5v+7w
\tag{4}
\]
and
\[
D=-33+20b+24a+100t+86v+106w,
\tag{5}
\]
where \(D\) is its \(u\)-degree.

The nonnegative solutions at the degrees used below are exactly
\[
\begin{array}{c|l}
D&\text{factorizations}\\ \hline
139&CA^3T,\quad B^5A^3,\\
138&\varnothing,\\
137&B^2AW,\\
136&\varnothing,\\
135&C^3A^7,\quad BA^2T,\\
133&\varnothing.
\end{array}
\tag{6}
\]
The two even-degree gaps also follow immediately from (5).  For
\(D=133\), equation (5) reduces to
\[
10b+12a+50t+43v+53w=83.
\]
It forces either \((v,w)=(1,0)\) or \((0,1)\).  The respective
remaining equations have only \((b,a,t)=(4,0,0)\) and
\((3,0,0)\), and (4) gives \(c=-2\) and \(c=-1\).

## 2. Exact coefficient branching

Let \(\kappa_V\ne0\) denote the coefficient
\([u^{40}f^{33}]V\) printed in the preceding audit.  Normalize either
of the two degree-\(139\) reducers in (6) to cancel the leading term
of \(V(f(u))\).  Both choices give the same coefficients through
degree \(136\); their normalized difference first occurs in degree
\(135\).

The degree-\(138\) coefficient of the remainder is
\[
\kappa_V\,d\,r^{32}.
\tag{7}
\]
If \(d\ne0\), (6) therefore proves the first row of (2).

Now set \(d=0\).  The degree-\(137\) coefficient is
\[
K_{137}r^{32}
\left(20234250r-750661967\right),
\qquad K_{137}\ne0.
\tag{8}
\]
Cancel it by the unique reducer \(B^2AW\); when the displayed
coefficient vanishes, this simply means subtracting zero.  The
degree-\(136\) coefficient becomes
\[
K_{136}r^{32}(68r+91),
\qquad K_{136}\ne0.
\tag{9}
\]
This proves the second row of (2).

The only remaining stratum is
\[
r=-\frac{91}{68},\qquad
f(u)=\frac{-91u^3+159u}{68}.
\tag{10}
\]
Here the remainder has nonzero degree \(135\).  Cancelling it by
either \(C^3A^7\) or \(BA^2T\) leaves degree \(133\), with coefficient
\[
\frac{
3^{25}5^8 7^{31}13^{31}\cdot76444077740123
}{
2^{127}17^{32}23^{44}
}\ne0.
\tag{11}
\]
All four choices obtained from the two reducers at degrees \(139\)
and \(135\) give the same coefficient (11).  The last gap in (6)
proves the third row of (2).

For reference, the nonzero constants in (8)--(9) are
\[
\begin{aligned}
K_{137}
&=-\frac{1723813088873291015625}{
129230026381362988475121198684461016956252545836408663083476189883762833805541376},\\
K_{136}
&=\frac{646429908327484130859375}{
244291165182160658743140262163442376098776079085838682577459716226394770898944}.
\end{aligned}
\tag{12}
\]

## 3. Why the calculation is finite

For
\[
f=ru^3+du^2+eu+s,
\]
the coefficient used in every step is given without expanding a
large symbolic polynomial:
\[
[u^{3j-k}]f^j
=
\sum_{\substack{n_1+2n_2+3n_3=k\\
                 n_1+n_2+n_3\le j}}
\frac{j!}{
(j-n_1-n_2-n_3)!\,n_1!\,n_2!\,n_3!
}
r^{j-n_1-n_2-n_3}d^{n_1}e^{n_2}s^{n_3}.
\tag{13}
\]
Applying (13) term by term to the exact bivariate boundary
polynomials proves (7)--(12).  Equation (5) supplies the complete
finite list of possible reducers.  No numerical sampling or
floating-point decision enters the proof.

The accompanying exact verifier is
`verify_weighted_lift_cubic_graph_v_subduction_closure.py`.
