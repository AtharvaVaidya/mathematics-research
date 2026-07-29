# The fixed-map affine cleaning lemma

Date: 2026-07-29

Status: **HUMAN-CHECKABLE REDUCTION / SHARP SIZE-FOURTEEN
BOUNDARY COUNTERSTATE / NOT A FIVECDC RESOLUTION**.

## 1. Transition boundary

Put \(A=\mathbb F_2^2\). Let \(H\) be a disjoint union of ordinary
circuits. Its vertices are partitioned into nonempty blocks
\(\mathcal W\). Identifying all vertices in each block produces an
Eulerian multigraph \(Q\): the edges of \(Q\) are the edges of \(H\), and
the circuits of \(H\) become a fixed decomposition of \(E(Q)\) into
closed walks. Loops and parallel edges are retained.

Give every edge \(e\) of \(H\) an original colour \(c_e\in A\). At an
occurrence \(i\) of a block \(W\) on a circuit, let \(e_i^-\) and
\(e_i^+\) be the incoming and outgoing edges and put
\[
                         d_i=c_{e_i^-}+c_{e_i^+}.          \tag{1}
\]
Assume adjacent colours differ, so \(d_i\ne0\), and assume the block
charge condition
\[
                         \bigoplus_{i\in W}d_i=0
                         \qquad(W\in\mathcal W).           \tag{2}
\]
In the minimum-projection application, every circuit colour word also
uses all four elements of \(A\).

Choose one map \(L_W\in\mathrm{GL}(A)\) for every block and define
\[
                         g_i=L_Wd_i\qquad(i\in W).         \tag{3}
\]
Call the map assignment **feasible** when
\[
                         \bigoplus_{i\in C}g_i=0           \tag{4}
\]
for every circuit \(C\) of \(H\). Condition (4) is exactly the cyclic
consistency condition for edge colours \(r_e\in A\) satisfying
\[
                         r_{e_i^-}+r_{e_i^+}=g_i.          \tag{5}
\]
For a fixed feasible assignment, choose one solution \(r^0\). Every
solution of (5), and no other one, has the form
\[
                         r_e=r^0_e+a_C\qquad(e\in C),      \tag{6}
\]
with one independently chosen translation \(a_C\in A\) per circuit.
Indeed, the difference of two solutions is equal on consecutive edges,
hence is constant around each circuit.

The identity assignment is always feasible: with \(L_W=I\), equation
(4) telescopes around each original colour word. Thus the feasible set
is never empty.

## 2. Defect is one bit

For a block \(W\), let \(\delta_Q(W)\) be the nonloop edges of \(Q\)
with exactly one endpoint \(W\). Every fixed circuit \(C\) meets this
cut evenly:
\[
                         |\delta_Q(W)\cap C|=0\pmod2.      \tag{7}
\]
This is just the fact that a closed walk enters a vertex as often,
modulo two, as it leaves.

Sum (5) over all occurrences in \(W\). A loop at \(W\) occurs twice and
cancels, while every cut edge occurs once. Equations (2)--(3) give
\[
                         \bigoplus_{e\in\delta_Q(W)}r_e=0. \tag{8}
\]
For \(x\in A\), let
\[
 p_W(x)=|\{e\in\delta_Q(W):r_e=x\}|\pmod2.
\]
Equation (7), summed over the circuit decomposition, says
\(\sum_xp_W(x)=0\). Equation (8) says
\(\sum_xp_W(x)x=0\). If the four points are ordered
\(00,01,10,11\), the latter two coordinate equations give
\[
 p_W(01)=p_W(11),\qquad p_W(10)=p_W(11),
\]
and the total-parity equation then gives \(p_W(00)=p_W(11)\).
Consequently
\[
                    (p_W(x):x\in A)\in\{0000,1111\}.      \tag{9}
\]
There is therefore one defect bit \(\varepsilon_W\): it is zero when
all four colour classes meet the cut evenly, and one when all four meet
it oddly.

## 3. Affine cleaning formula

Write \(x=(x_1,x_2)\), and define
\[
 q(x)=x_1x_2,\qquad
 B(x,y)=q(x+y)+q(x)+q(y)=x_1y_2+x_2y_1.                  \tag{10}
\]
The indicator of the zero point is
\[
 {\bf1}_{x=0}=(1+x_1)(1+x_2)=1+x_1+x_2+q(x).             \tag{11}
\]
On the cut of \(W\), the constant and linear sums in (11) vanish by
(7)--(8). Hence
\[
                         \varepsilon_W
             =\sum_{e\in\delta_Q(W)}q(r_e).               \tag{12}
\]

For the fixed base solution \(r^0\), put
\[
\begin{split}
 b_W&=\sum_{e\in\delta_Q(W)}q(r^0_e),\\
 s_{W,C}&=\bigoplus_{e\in\delta_Q(W)\cap C}r^0_e.
\end{split}                                               \tag{13}
\]
Using \(q(x+y)=q(x)+q(y)+B(x,y)\), equations (6)--(7) give
\[
 \boxed{\quad
 \varepsilon_W(a)=b_W+\sum_C B(s_{W,C},a_C).
 \quad}                                                   \tag{14}
\]
The \(q(a_C)\) term disappears because
\(|\delta_Q(W)\cap C|\) is even.

This proves:

> **Fixed-map affine cleaning lemma.** For a fixed feasible component-map
> assignment, deciding whether circuit translations make the repaired
> extension clean is an affine linear system over \(\mathbb F_2\).
> Explicitly, a clean translation exists if and only if
> \[
>       b\in\operatorname{im}\Phi,\qquad
>       \Phi((a_C)_C)_W=\sum_C B(s_{W,C},a_C).             \tag{15}
> \]

There is one harmless redundancy. From (8),
\[
                         \bigoplus_Cs_{W,C}=0,             \tag{16}
\]
so adding the same \(a\in A\) to every \(a_C\) does not change (14).
One circuit translation may therefore be fixed to zero. The system has
at most \(2(k-1)\) scalar variables when \(H\) has \(k\) circuits.

Equation (15) also gives short negative certificates for a fixed map
assignment. If no clean translation exists, ordinary binary linear
duality supplies \(y\in\mathbb F_2^{\mathcal W}\) such that
\[
                         y^\mathsf T\Phi=0,\qquad
                         y^\mathsf Tb=1.                  \tag{17}
\]
Both equalities can be checked by XOR alone.

### A map-invariant quadratic term

Every \(L\in\mathrm{GL}(2,2)\) preserves \(B\): in dimension two,
\[
                         B(Lx,Ly)=\det(L)B(x,y)=B(x,y),
\]
since the only nonzero scalar in \(\mathbb F_2\) is \(1\). Therefore the
polar form of \(q\circ L+q\) vanishes, so
\(q(Lx)+q(x)=\ell_L(x)\) for a linear functional \(\ell_L\). The charge
condition (2) then gives, block by block,
\[
\begin{split}
 \sum_{i\in W}q(L_Wd_i)
 &=\sum_{i\in W}q(d_i)
   +\ell_{L_W}\left(\bigoplus_{i\in W}d_i\right)\\
 &=\sum_{i\in W}q(d_i).
\end{split}
\]
Thus the pure quadratic transition contribution is independent of the
component map. Only the integrated-position terms can change with the
map choice.

## 4. The deletion alternative

For a circuit \(C\), let
\[
                         R_C=\{r^0_e:e\in C\}\subseteq A.  \tag{18}
\]
Translations do not change \(|R_C|\). If \(R_C\ne A\), choose
\(z\in A-R_C\) and set \(a_C=z\). Then
\[
                         r^0_e+z\ne0\qquad(e\in C).        \tag{19}
\]

In the graph application, transform the existing nonzero low flow inside
the component represented by \(W\) using \(L_W\), and use (6) on \(H\).
Now remove the whole circuit \(C\) from the first-coordinate support.
Edges of \(C\) have first coordinate zero but nonzero low coordinate by
(19); remaining support edges retain first coordinate one; all edges
inside the components retain nonzero low value because every \(L_W\) is
invertible. Equations (5) are exactly the missing vertex equations.
Thus:

> **Fixed-map deletion lemma.** If a feasible map assignment has
> \(R_C\ne A\) for some circuit \(C\), deleting \(C\) from the projection
> produces a strictly smaller extendable projection.

The statement includes the one-circuit case, where the new projection is
zero. In a non-Tait graph this alternative simply cannot occur for a
globally minimum projection.

## 5. The unrestricted map-choice statement fails at size fourteen

For a feasible assignment \(L=(L_W)_W\), let \(b(L)\),
\(\Phi_L\), and \(R_C(L)\) be the objects above. The whole remaining
abstract assertion suggested by the results through size thirteen was:

> **Universal clean-or-delete map-choice statement.** For every valid
> transition boundary satisfying (1)--(2), in which every original
> circuit word uses all four colours, there is a feasible choice
> \(L_W\in\mathrm{GL}(2,2)\) such that either
> \[
>       b(L)\in\operatorname{im}\Phi_L                    \tag{20}
> \]
> or
> \[
>       R_C(L)\ne A\quad\hbox{for some circuit }C.         \tag{21}
> \]

Equivalently, the exact implication still needing proof is
\[
\left[
\begin{array}{c}
 L\text{ is feasible and }R_C(L)=A\\
 \text{for every circuit }C
\end{array}
\text{ for all feasible }L
\right]
\Longrightarrow
\left[
\begin{array}{c}
 b(L)\in\operatorname{im}\Phi_L\\
 \text{for at least one feasible }L.
\end{array}
\right]                                                   \tag{22}
\]

If (20) holds, the fixed-map affine cleaning lemma constructs a clean
extension. If (21) holds, the deletion lemma contradicts cardinality
minimality. Thus this statement would have completed the proposed route.
It is, however, false.

The smallest total-support failure has two seven-circuits:
\[
\begin{split}
(c_e)&=\texttt{0101023}\mid\texttt{0101232},\\
(\pi_i)&=\texttt{01234444413024}.
\end{split}                                               \tag{22a}
\]
Its derivative word is
\(\texttt{3111121}\mid\texttt{2111311}\); every one of the five block
charges is zero, and both circuit words use all four colours. After fixing
one global left composition, there are \(6^4=1296\) component-map tuples.
Exactly 320 are feasible. For every feasible tuple, all four relative
circuit translations remain dirty and both integrated circuit ranges
equal all of \(A\). Hence neither (20) nor (21) holds.

This abstract counterstate is realizable by a simple connected bridgeless
non-Tait cubic graph on 18 vertices, with canonical graph6 encoding
```text
Qs???SC@GS@_CDOoC@@@?O?CO?g
```
The displayed size-fourteen projection has 15,360 ordered extensions and
none is clean. But it is not globally minimum: the graph has minimum
extendable-projection size five, exactly four minimum supports, and every
one has 120 clean extensions. Thus (22a) refutes the unrestricted
clean-or-delete statement, not the minimum-projection conjecture or
FiveCDC.

The exact classifier, 40-case reduced map certificate, independent
checker, graph realization, and exhaustive \(2^{10}\)-cycle-space audit
are in
`../minimum-projection-size14-dichotomy-counterstate-20260729/`.
The boundary implication does hold through total support size thirteen.
Any universal proof from this point must use global minimum-exchange
information beyond the fact that every circuit contains all four colours.

## 6. Map feasibility in charge form

For possible induction, define the per-circuit block charge
\[
                         u_{W,C}=\bigoplus_{i\in W\cap C}d_i. \tag{23}
\]
Then (2) says \(\bigoplus_Cu_{W,C}=0\), and feasibility is the compact
condition
\[
                         \bigoplus_WL_Wu_{W,C}=0
                         \qquad\text{for every }C.         \tag{24}
\]

A nonidentity transvection of \(A\) has the form
\[
                         T(x)=x+\ell(x)a,\qquad
                         \ker\ell=\{0,a\}.                 \tag{25}
\]
Changing only \(L_W\) from the identity to \(T\) preserves (24) exactly
when
\[
                         u_{W,C}\in\{0,a\}
                         \qquad\text{for every }C.         \tag{26}
\]
This is automatic for one circuit, because \(u_{W,C}=0\). For two
circuits, (2) makes their two charges equal, so the transvection fixing
that common charge is always feasible. With three or more circuits the
charges at one block may span \(A\), and coordinated block moves become
necessary. This is the first point at which a local one-block induction
can genuinely fail.

Kotzig \(\kappa\)-transformations and transition-matroid/local-
complementation theory describe changes among Euler systems of a
four-regular graph. The present operation is related but not identical:
the closed walks are fixed, while a block map permutes the three
nonzero **difference labels simultaneously at every occurrence of that
block**. No sourced Kotzig theorem currently found implies (22).

## 7. Dual obstructions give coordinated feasible moves

The dual certificate (17) has a graph interpretation. Regard \(y\) as
the indicator of a set \(\mathcal Y\subseteq\mathcal W\), and let
\(\delta_Q(\mathcal Y)\) be the aggregate cut between its blocks and the
other blocks. For a circuit \(C\), summing (13) over
\(W\in\mathcal Y\) cancels every edge with both ends in \(\mathcal Y\)
and leaves every aggregate-cut edge once:
\[
 \bigoplus_{W\in\mathcal Y}s_{W,C}
   =\bigoplus_{e\in\delta_Q(\mathcal Y)\cap C}r^0_e.       \tag{27}
\]
Likewise,
\[
 \sum_{W\in\mathcal Y}b_W
   =\sum_{e\in\delta_Q(\mathcal Y)}q(r^0_e).              \tag{28}
\]
Because \(\sum_Cs_{W,C}=0\), annihilating the relative-translation map
\(\Phi\) is equivalent to the right side of (27) being zero for every
circuit \(C\). Each circuit meets the aggregate cut evenly, so the
argument of Section 2 says that its four colour parities on this cut are
either all even or all odd. Equation (28) is one precisely when an odd
number of the fixed circuits are rainbow-odd on the aggregate cut.

Hence:

> **Dual-cut lemma.** A fixed feasible map assignment has no clean
> circuit translation if and only if there is a block union
> \(\mathcal Y\) such that
> \[
>  \bigoplus_{e\in\delta_Q(\mathcal Y)\cap C}r^0_e=0
>  \quad\text{for every }C,                              \tag{29}
> \]
> and an odd number of circuits meet
> \(\delta_Q(\mathcal Y)\) oddly in each of the four colours.

Such a dual cut automatically supplies a coordinated feasible map move.
Indeed, summing (5) over the occurrences belonging to
\(\mathcal Y\cap C\) gives
\[
 \bigoplus_{\substack{i\in C\\W(i)\in\mathcal Y}}g_i
 =\bigoplus_{e\in\delta_Q(\mathcal Y)\cap C}r^0_e=0.       \tag{30}
\]
For any \(T\in\mathrm{GL}(A)\), replace
\[
 L_W\longmapsto T\circ L_W\qquad(W\in\mathcal Y),         \tag{31}
\]
and leave the other maps unchanged. On each circuit, the transformed
sum over \(\mathcal Y\) is \(T(0)=0\), and the complementary sum is also
zero because the old total was zero. Thus all six coordinated choices
(31) remain feasible.

This sharpens the remaining obligation. At any fixed-map affine
obstruction, linear duality produces a nontrivial family of feasible
moves. A universal proof may therefore iterate:

1. solve the affine translation system;
2. if it is inconsistent, extract a dual block cut \(\mathcal Y\);
3. try the six postcompositions (31);
4. prove that either a circuit range becomes proper, the affine
   obstruction disappears, or a well-founded invariant decreases.

Steps 1--3 are theorems. The size-fourteen counterstate (22a) shows that
the desired progress assertion is false for unrestricted valid boundary
states: all feasible map choices can remain dirty and surjective on every
circuit. A surviving proof must bring the global minimum-exchange
inequalities into the invariant or derive a different smaller projection.

## Disclosure

OpenAI Codex agents under human direction derived the quadratic defect
formula, affine system, deletion criterion, and exact remaining
map-choice statement, then found and independently checked its sharp
size-fourteen failure. The derivation above is elementary and included
in full for human checking. It has not received independent peer review
and is not a FiveCDC resolution.
