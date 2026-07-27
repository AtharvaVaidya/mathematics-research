# Case c: the later quartic-jet staircase and its first terminal scalar

Date: 25 July 2026

## Audited conclusion

Let
\[
L_d(A,B)=[A,q_3]+[p_2,B]
\]
be the case-c new-block operator at radial deficit \(d\), and let
\[
E(h)=hV(h)^2-\lambda U(h)^3
\]
be the corrected degree-four outer incidence divisor.  The first two
cokernel stages \(d=4,5\) have already been tested against linear and
two-stage nonlinear adjoints.  This note maps the complete later
quartic-jet complex and extracts the first intrinsic invariant involving
a third stage.

The result has two parts.

> **Multistage jet-staircase theorem.** For every \(4\le d\le15\), the
> reduction of \(L_d\) modulo \(E^j\) has the largest rank allowed by its
> full bounded rank:
> \[
> \operatorname {rank}(L_d\bmod E^j)=\min(4j,r_d),
> \tag{1}
> \]
> where
> \[
> (r_4,\ldots,r_{15})
> =(18,17,15,13,11,9,7,5,4,3,2,1).
> \tag{2}
> \]
> In particular, deficit six has a unique first adjoint modulo \(E^4\).
> Together with the canonical residual adjoints at deficits four and
> five, it gives three centered elements of the trace-zero quartic
> algebra.  Their trace-Gram determinant is nonzero.  Thus the smallest
> genuinely three-stage linear-dependence invariant is maximally
> nondegenerate, not an identity.
>
> Deficit eight has a unique first adjoint modulo \(E^3\).  The pure
> weight-four mode
> \[
> X_0=\cdots=X_5=0,\qquad X_6\ne0
> \tag{3}
> \]
> satisfies every preceding consistency row through deficit seven, but
> this canonical deficit-eight adjoint evaluates to
> \[
> C_8X_6^2,\qquad C_8\ne0.
> \tag{4}
> \]
> Hence \(X_6=0\).  By weighted degree, deficit eight is the first stage
> at which any equation can obstruct the pure \(X_6\)-axis.

Equation (4) compresses the five previously retained deficit-eight rows
on the deepest special chart to one degree-filtered quartic-jet scalar.
It is a genuine later finite-support invariant.  It does not eliminate
the two generic charts by itself, so it is a structural compression of
one terminal branch rather than a new independent proof of all case c.

## 1. The later new-block complex

At deficit \(d\),
\[
\deg_z A=2-d,\qquad \deg_z B=3-d,
\tag{5}
\]
and
\[
L_d(A,B)
=h\left((2-d)Aq_3'-3A'q_3
+2p_2B'-(3-d)p_2'B\right).
\tag{6}
\]
The Newton supports are
\[
A\in\langle h^{d-2},\ldots,h^8\rangle,\qquad
B\in\langle h^{d-3},\ldots,h^{12}\rangle,
\tag{7}
\]
with an empty interval interpreted as zero.

The full bounded ranks and the first defective jet lengths are:
\[
\begin{array}{c|rrrrrrrrrrrr}
d&4&5&6&7&8&9&10&11&12&13&14&15\\ \hline
r_d&18&17&15&13&11&9&7&5&4&3&2&1\\
\text{first defective }j&5&5&4&4&3&3&2&2&2&1&1&1\\
\dim\operatorname {coker}(L_d\bmod E^j)
&2&3&1&3&1&3&1&3&4&1&2&3
\end{array}
\tag{8}
\]
At every shorter jet length the operator is surjective.  Thus the
quartic-root distributions appear in a rigid staircase:
\[
E^5,\ E^4,\ E^3,\ E^2,\ E.
\tag{9}
\]
The even deficits \(6,8,10\) are distinguished by a unique first
adjoint.

The companion verifier computes (1) for \(j=1,\ldots,6\) over the two
rational and one cubic factors above \(32003\).  These factors exhaust
the five geometric points of the good outer fiber.  The nonzero maximal
minors lift to characteristic zero, while the full bounded ranks give
the matching upper bounds.  By \(j=6\) every row has already reached its
full rank \(r_d\).  Rank cannot decrease when \(E^j\) is replaced by
\(E^{j+1}\), so (1) then persists for every larger \(j\).

## 2. The first three-stage trace discriminant

Use the Frobenius pairing
\[
\langle F,G\rangle_j
=[h^{4j-1}]\operatorname {rem}_{E^j}(FG).
\tag{10}
\]
The degree-filtered residual adjoints from deficits four and five are
\[
G_4\in k[h]/(E^5),\quad \deg G_4=16,
\qquad
G_5\in k[h]/(E^5),\quad \deg G_5=18.
\tag{11}
\]
The unique deficit-six adjoint is
\[
G_6\in k[h]/(E^4),\qquad
\deg G_6=15,\qquad [h^{15}]G_6=1.
\tag{12}
\]
Reduce all three modulo \(E\), then remove their traces:
\[
x_d=G_d\bmod E-\frac14\operatorname {Tr}(G_d\bmod E),
\qquad d=4,5,6.
\tag{13}
\]
The smallest basis-free three-stage degeneracy test is
\[
\Delta_{456}
=\det\bigl(\operatorname {Tr}(x_ix_j)\bigr)_{i,j=4,5,6}.
\tag{14}
\]
Its exact good-reduction values are
\[
\begin{array}{c|c|c}
\text{outer factor}&\Delta_{456}&\operatorname {Nm}(x_6)\\ \hline
t=26839&1894&-222\\
t=16621&659&-1771\\
K_3&
-1130-8574t-5288t^2&
6161+11890t+12835t^2
\end{array}
\tag{15}
\]
in centered representatives modulo \(32003\), where
\[
K_3=\mathbf F_{32003}[t]/
(t^3-11133t^2-11294t-6180).
\]
The total norms over the complete outer fiber are
\[
\operatorname {Nm}(\Delta_{456})=-15416,\qquad
\operatorname {Nm}(\operatorname {Nm}(x_6))=-1785
\pmod {32003}.
\tag{16}
\]
Both are units.  Therefore \(x_4,x_5,x_6\) form a basis of the
three-dimensional trace-zero quartic algebra.  No universal
three-stage relation can come from linear dependence, trace isotropy,
or vanishing of the new residual symbol.

The normalization is degree-filtered, but its vanishing claims are
stable under outer-coordinate rescaling.  Under \(h\mapsto ch\),
\[
G_6(h)\longmapsto c^{-15}G_6(ch),
\tag{17}
\]
which the verifier checks at \(c=7\).

## 3. A canonical deficit-eight terminal scalar

At deficit eight, (1) gives
\[
\operatorname {rank}(L_8\bmod E^2)=8,\qquad
\operatorname {rank}(L_8\bmod E^3)=11.
\tag{18}
\]
Since \(k[h]/(E^3)\) has dimension \(12\), its annihilator is one
dimensional.  Let
\[
G_8\in k[h]/(E^3),\qquad
\deg G_8=11,\qquad [h^{11}]G_8=1
\tag{19}
\]
be its unique degree-filtered generator.  If \(S_8\) denotes the exact
source built from the seven preceding solved stages, define
\[
\Theta_8(S_8)
=[h^{11}]\operatorname {rem}_{E^3}(S_8G_8).
\tag{20}
\]
Solvability of the deficit-eight row forces \(\Theta_8(S_8)=0\).

The seven radial modes have weights
\[
(1,1,2,2,3,3,4).
\tag{21}
\]
On the pure \(X_6\)-axis, all preceding consistency polynomials vanish:
the deficit-four source is independent of the new kernel parameter
\(X_6\), and weights five, six, and seven are not multiples of four.
Weight eight is the first possible nonzero restriction.  Exact recurrence
and adjoint pairing give (4), with
\[
\begin{array}{c|c}
\text{outer factor}&C_8\\ \hline
t=26839&-1952\\
t=16621&10399\\
K_3&7227+10262t+13596t^2.
\end{array}
\tag{22}
\]
Their total norm is
\[
\boxed{\operatorname {Nm}(C_8)=-9989\ne0\pmod {32003}.}
\tag{23}
\]
Consequently \(C_8\) is nonzero in the characteristic-zero outer
Hurwitz field, and (20) forces \(X_6=0\).

This lift uses the already-audited coefficientwise transport of the
exact quintic-field recurrence through deficit eight in
`CASE_C_N3_SPECIAL_CHARTS_EXACT_Q.md`.  The companion verifier here
recomputes the good-reduction ranks and scalar independently; it does
not substitute a finite-field computation for that transport step.

Under \(h\mapsto ch\), the terminal adjoint transforms as
\[
G_8(h)\longmapsto c^{-11}G_8(ch),
\tag{24}
\]
so the vanishing of (20) is independent of outer-coordinate scaling.

## 4. Consequence for the search

The rank staircase sharply separates two facts.

1. Adding the third cokernel stage does not create a degeneracy:
   \(\Delta_{456}\) is a unit, so the residual symbols already span all
   trace-zero quartic directions.
2. A later finite-support row does create a canonical obstruction:
   the unique \(E^3\)-adjoint at deficit eight is the first possible
   equation on the deepest weight-four branch and kills it.

Thus a compact invariant does exist, but only for the deepest special
branch.  Any replacement for the remaining generic-chart computation
must use the source values of the later adjoints, not another norm or
determinant of the abstract adjoint symbols alone.

Companion verifier:

```text
.venv/bin/python current_context/verify_case_c_multistage_jet_staircase.py
```
