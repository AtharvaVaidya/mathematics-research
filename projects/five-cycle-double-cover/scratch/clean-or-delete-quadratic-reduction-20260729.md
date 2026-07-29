# The exact quadratic reduction of the clean-or-delete boundary problem

Date: 2026-07-29

Status: **PROVED ALGEBRAIC REDUCTION / THE UNQUALIFIED ABSTRACT
DICHOTOMY IS FALSE AT ORDER FOURTEEN / NOT A FIVECDC RESOLUTION**.

## 1. Boundary data

Put \(K=\mathbb F_2^2\).  Let \(D_1,\ldots,D_k\) be disjoint oriented
circuits.  On a circuit, let \(e_i\) be the edge after the vertex \(v_i\)
(indices are cyclic), and let \(\pi_i\in A\) be the component block
containing \(v_i\).  The given low edge values \(c_i\in K\) have
\[
                         d_i=c_{i-1}+c_i\ne0.              \tag{1}
\]
The charge condition is
\[
                   \mathop{\mathbin\oplus}_{\pi_i=a}d_i=0
                   \qquad(a\in A).                        \tag{2}
\]

Choose \(L_a\in\operatorname{GL}(K)\) for every block and put
\[
                         t_i=L_{\pi_i}d_i.                 \tag{3}
\]
These maps are **integrable** when
\[
                         \mathop{\mathbin\oplus}_{v_i\in D_j}t_i=0
                         \qquad(1\le j\le k).              \tag{4}
\]
Then choose one solution on every circuit of
\[
                         r_{i-1}+r_i=t_i.                 \tag{5}
\]
All other solutions are obtained by adding an independent translation
\(z_j\in K\) to every \(r_i\) on \(D_j\).

For a block \(a\) and colour \(\gamma\in K\), its cut-colour parity is
\[
 P_{a,\gamma}(r)=
 \sum_{\pi_i=a}\bigl({\bf1}_{r_{i-1}=\gamma}
                         +{\bf1}_{r_i=\gamma}\bigr)
 \quad\text{in }\mathbb F_2.                              \tag{6}
\]
An edge whose two endpoint blocks agree occurs twice in (6) and hence
cancels.  Thus (6) is exactly the parity of the \(\gamma\)-coloured
edges in the cut of \(a\).

## 2. Four parity equations collapse to one quadratic bit

Write \(x=(x_1,x_2)\), and define
\[
 q(x)=x_1x_2,\qquad
 B(x,y)=q(x+y)+q(x)+q(y)=x_1y_2+x_2y_1.                  \tag{7}
\]

> **Proposition 1 (parity collapse).**  For every block \(a\), the four
> bits \(P_{a,\gamma}(r)\), \(\gamma\in K\), are equal.  Their common
> value is
> \[
 Q_a(r)=
 \sum_{\pi_i=a}\bigl(q(r_{i-1})+q(r_i)\bigr).             \tag{8}
 \]
> Consequently \(r\) is clean exactly when \(Q_a(r)=0\) for every
> block \(a\).

**Proof.**  In \(\mathbb F_2\),
\[
 {\bf1}_{x=\gamma}
 =(1+x_1+\gamma_1)(1+x_2+\gamma_2).                      \tag{9}
\]
Apply (9) to \(x=r_{i-1}\) and \(x=r_i\), and add.  The constant terms
and the terms depending only on \(\gamma\) cancel.  The result is
\[
\begin{split}
 {\bf1}_{r_{i-1}=\gamma}+{\bf1}_{r_i=\gamma}
  ={}&q(r_{i-1})+q(r_i)\\
    &+(1+\gamma_2)(r_{i-1,1}+r_{i,1})\\
    &+(1+\gamma_1)(r_{i-1,2}+r_{i,2}).
\end{split}                                               \tag{10}
\]
By (5), the two parenthesized coordinate differences are the
coordinates of \(t_i\).  Moreover, (2)--(3) give
\[
                    \mathop{\mathbin\oplus}_{\pi_i=a}t_i
                    =L_a\left(
                       \mathop{\mathbin\oplus}_{\pi_i=a}d_i\right)=0.
                                                               \tag{11}
\]
After (10) is summed over \(\pi_i=a\), both terms involving \(\gamma\)
therefore vanish.  What remains is (8), independently of \(\gamma\).
\(\square\)

There is also a useful transition form.  Equation (7) gives
\[
 q(r_{i-1})+q(r_i)
 =q(t_i)+B(r_{i-1},t_i),                                 \tag{12}
\]
so
\[
 Q_a(r)=\sum_{\pi_i=a}
       \bigl(q(t_i)+B(r_{i-1},t_i)\bigr).                 \tag{13}
\]

The first sum in (13) is independent of the chosen component map.
Indeed every \(L\in\operatorname{GL}(2,2)\) preserves \(B\): in
dimension two,
\[
                         B(Lx,Ly)=\det(L)B(x,y)=B(x,y),    \tag{14}
\]
because the only nonzero scalar in \(\mathbb F_2\) is \(1\).
It follows that the polar form of \(q\circ L+q\) is zero, so
\(q(Lx)+q(x)=\ell_L(x)\) for a linear functional \(\ell_L\).  Hence
\[
\begin{split}
 \sum_{\pi_i=a}q(L_ad_i)
 &=\sum_{\pi_i=a}q(d_i)
   +\ell_{L_a}\left(
       \mathop{\mathbin\oplus}_{\pi_i=a}d_i\right)\\
 &=\sum_{\pi_i=a}q(d_i).                                 \tag{15}
\end{split}
\]

## 3. Circuit translations form an exact linear system

Fix integrable maps \(L_a\), and fix one zero-start solution \(r^0\) of
(5) on every circuit.  For each block-circuit pair define
\[
 T_{a,j}=
       \mathop{\mathbin\oplus}_{\substack{\pi_i=a\\v_i\in D_j}}t_i.
                                                               \tag{16}
\]

> **Proposition 2 (translation linearization).**  After translating
> circuit \(D_j\) by \(z_j\in K\), the block obstruction is
> \[
 Q_a(z)=Q_a(0)+\sum_{j=1}^k B(z_j,T_{a,j}).               \tag{17}
 \]
> Thus, for fixed component maps, direct cleanability is exactly the
> consistency of the linear system
> \[
 \sum_{j=1}^k B(z_j,T_{a,j})=Q_a(0)
 \qquad(a\in A).                                         \tag{18}
 \]
> A simultaneous common translation of all circuits has no effect, so
> one may fix \(z_1=0\).  The system then has only \(2(k-1)\) binary
> unknowns.

**Proof.**  At a vertex of \(D_j\), translating both incident values by
\(z_j\) changes the summand in (8) by
\[
\begin{split}
 &q(r_{i-1}+z_j)+q(r_i+z_j)+q(r_{i-1})+q(r_i)\\
 &\hspace{35mm}=B(r_{i-1}+r_i,z_j)=B(t_i,z_j).            \tag{19}
\end{split}
\]
Summing (19) over the vertices in block \(a\) gives (17).
Furthermore
\[
                     \mathop{\mathbin\oplus}_{j=1}^kT_{a,j}
                     =\mathop{\mathbin\oplus}_{\pi_i=a}t_i=0            \tag{20}
\]
by (11), proving the common-translation assertion.  Proposition 1 now
proves the equivalence with (18). \(\square\)

This replaces enumeration of \(4^{k-1}\) translations by ordinary
Gaussian elimination.

## 4. Exact dual obstruction

Because \(B\) is nondegenerate, the standard consistency criterion for
(18) has a concrete form.

> **Corollary 3 (dual witness).**  The translation system is
> inconsistent exactly when there is a subset \(S\subseteq A\) such
> that
> \[
 \mathop{\mathbin\oplus}_{a\in S}T_{a,j}=0
 \quad(1\le j\le k),\qquad
 \sum_{a\in S}Q_a(0)=1.                                  \tag{21}
 \]

**Proof.**  A binary linear system \(Mz=b\) is inconsistent exactly
when some row vector \(y\) satisfies \(yM=0\) and \(yb=1\).  In (18),
the coefficient of \(z_j\) after the rows in \(S=\{a:y_a=1\}\) are
added is the functional
\[
                     z_j\longmapsto
                     B\left(z_j,\mathop{\mathbin\oplus}_{a\in S}
                                      T_{a,j}\right).
\]
It vanishes for every \(z_j\) exactly when the displayed vector is zero.
The right-hand side of the added equation is the second expression in
(21). \(\square\)

The witness also recovers the usual four-odd cut description.  On a
circuit \(D_j\), the first condition in (21) is the xor of the \(r\)
values on the support edges crossing between \(S\) and its complement:
all other support edges occur zero or twice when the selected transition
equations are added.  A circuit crosses this cut an even number of
times.  For an even multiset of elements of \(K\), zero xor says that
the four colour multiplicities have one common parity.  The last
condition in (21), which is the parity of the colour with \(q=1\), says
that this common parity is odd.  Hence every one of the four colours
occurs oddly on the displayed cut.

## 5. The deletion branch

For fixed integrable maps, the zero-start values on a circuit are
determined up to translation.  The number of colours they use is
translation-invariant.

> **Proposition 4 (literal deletion certificate).**  If the integrated
> values on a circuit \(D_j\) omit a colour \(\mu\in K\), translating
> that circuit by \(\mu\) makes every one of its low values nonzero.
> In the graph-flow setting, deleting \(D_j\) from the first-coordinate
> support therefore gives a strictly smaller extendable projection.

**Proof.**  A translated value \(r_i+\mu\) is zero exactly when
\(r_i=\mu\), which never occurs.  Equation (5) is unchanged by the
translation.  On removing \(D_j\) from the first-coordinate support,
the full value there is consequently \((0,r_i+\mu)\ne0\); all other
full values remain nonzero, and the vertex equations still hold.
\(\square\)

## 6. Every individual dual obstruction has a legal neutralizing switch

There is a further general consequence which uses all six elements of
\(\operatorname{GL}(2,2)\).

Let \(S\subseteq A\) satisfy the first part of (21).  Starting with the
current maps \(L_a\), choose \(U\in\operatorname{GL}(2,2)\) and replace
\[
 L_a\longmapsto UL_a\quad(a\in S),\qquad
 L_a\longmapsto L_a\quad(a\notin S).                      \tag{22}
\]
This is a legal component-map switch.  Indeed, on every circuit the xor
of the transformed transitions at vertices in \(S\) was zero; applying
\(U\) to that xor leaves it zero.  The complementary xor is also zero,
so circuit integrability is preserved.  Moreover the selected balance
after the switch is still zero, now as \(U0=0\).  Thus \(S\) remains a
left-kernel row combination.  Proposition 2 shows at once that the
quantity \(F_S(U)\) below is invariant under arbitrary independent
translations of the support circuits.

For the three nonidentity involutions of
\(\operatorname{GL}(2,2)\), write
\(\tau_1,\tau_2,\tau_3\).  For the order-three subgroup write
\(\{I,\rho,\rho^2\}\).

> **Proposition 5 (six-map parity identity).**  Let
> \[
>                         F_S(U)=\sum_{a\in S}Q_a
> \]
> after the switch (22), with arbitrary fixed circuit translations.
> Then
> \[
\begin{split}
 F_S(I)+F_S(\rho)+F_S(\rho^2)&=0,\\
 F_S(\tau_1)+F_S(\tau_2)+F_S(\tau_3)&=0.                 \tag{23}
\end{split}
 \]
> In particular, if \(F_S(I)=1\), some \(U\in
> \operatorname{GL}(2,2)\) has \(F_S(U)=0\).

**Proof.**  It is enough to prove (23) on one support circuit and add
the answers over the circuits.  On that circuit let \(s_i=1\) exactly
when \(\pi_i\in S\).  The balance hypothesis says
\[
                             \bigoplus_{s_i=1}t_i=0.       \tag{24}
\]
Fix a base edge and define a cyclic edge potential \(a_i\) by
\[
                         a_i+a_{i-1}=s_it_i.              \tag{25}
\]
Equation (24) makes this well-defined.  If \(r_i\) are the edge values
before (22), edge values after (22) can be translated so that
\[
                         r_i^U=r_i+(U+I)a_i.              \tag{26}
\]
Both sides have the same transition at every vertex, which proves
(26).  A different common circuit translation does not change any cut
parity.

Let \(C\) be the set of circuit edges with one endpoint in \(S\) and
one outside.  The circuit contribution to \(F_S(U)\) is
\[
                             f(U)=\sum_{e_i\in C}q(r_i^U). \tag{27}
\]
The following four-by-four table is a direct evaluation in
\(K=\{0,1,2,3\}\), where \(q(3)=1\), \(q(0)=q(1)=q(2)=0\).
For every \(r,a\in K\), both three-term sums
\[
\begin{split}
 &\sum_{U\in\{I,\rho,\rho^2\}}q(r+(U+I)a),\\
 &\sum_{U\in\{\tau_1,\tau_2,\tau_3\}}q(r+(U+I)a)
\end{split}
\]
have the common value \(H(r,a)\):
\[
\begin{array}{c|cccc}
H(r,a)&a=0&a=1&a=2&a=3\\ \hline
r=0&0&1&1&0\\
r=1&0&1&0&1\\
r=2&0&0&1&1\\
r=3&1&1&1&1
\end{array}                                               \tag{28}
\]
Equivalently,
\[
                         H(r,a)=q(r+a)+{\bf1}_{a\ne0}.     \tag{29}
\]
Thus either left side of (23), restricted to the present circuit, is
\[
               \sum_{e_i\in C}
                    \bigl(q(r_i+a_i)+{\bf1}_{a_i\ne0}\bigr).             \tag{30}
\]

Put \(b_i=r_i+a_i\).  From (5) and (25),
\[
 b_i+b_{i-1}=(1+s_i)t_i.                                 \tag{31}
\]
Therefore \(b_i\) is constant across every consecutive run of selected
vertices.  The two cut edges flanking such a run have the same \(b\),
so their two \(q(b)\) terms in (30) cancel.  Similarly, (25) says that
\(a_i\) is constant across every consecutive run of unselected
vertices.  The two cut edges flanking that run have the same \(a\), so
their two \({\bf1}_{a\ne0}\) terms cancel.  Hence (30) is zero.  This
proves both identities in (23).

Finally the constant function \(F_S(U)=1\) violates either three-term
identity, because three copies of \(1\) add to \(1\) in
\(\mathbb F_2\).  Hence \(F_S(I)=1\) cannot persist for all six choices
of \(U\). \(\square\)

Proposition 5 says that every particular Farkas witness to failure of
the translation system can be made nonobstructing by a legal common
switch on precisely its components.  This is stronger than the finite
order census: it holds at every boundary order.

It does not prove simultaneous cleanliness.  After \(S\) is
neutralized, another subset can become (or remain) a dual obstruction,
because (22) can change both the obstruction vector \(Q\) and the
coefficient vectors \(T_{a,j}\) outside the single equation indexed by
\(S\).  The order-fourteen counterstate cited below shows that repeated
neutralization need not reach cleanliness or deletion.

## 7. Exact limit of the reduction

The component maps must satisfy the circuit integrability equations
(4).  Propositions 1--4 prove exactly how to test each such map tuple:
either (18) is consistent, giving a clean extension, or an integrated
circuit omits a colour, giving deletion.  They do **not** prove that one
of those outcomes occurs for every admissible boundary state.

The unqualified general statement would have been:

> For every boundary state satisfying (1)--(2), with every original
> circuit using all four colours, there is an integrable component-map
> tuple for which either (18) is consistent or some integrated circuit
> omits a colour.

This statement is false.  The package
`minimum-projection-size14-dichotomy-counterstate-20260729/` gives the
order-fourteen state
```text
word=0101023|0101232
partition=01234444413024
```
and proves, without a case table, that every integrable component-map
tuple fails (18) and that both integrated circuit walks nevertheless
use all four colours.  Its `HUMAN-PROOF.md` also realizes the state in a
simple bridgeless cubic graph.

The displayed size-fourteen projection in that realization is not
globally minimum: exact cycle-space enumeration finds an extendable
projection of size five.  Thus the counterstate disproves the proposed
deduction from only charge balance and four-colour occurrence.  It does
not disprove a stronger theorem using the full inequalities imposed by
global minimum, and it does not disprove FiveCDC.  Finding a sufficient
global-minimum invariant, or a globally minimum dirty projection, is
the remaining research problem.
