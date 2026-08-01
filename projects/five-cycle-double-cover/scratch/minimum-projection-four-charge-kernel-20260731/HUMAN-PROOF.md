# Four charged blocks do not force direct cleaning

Date: 2026-07-31

Status: **EXACT SMALLEST-BLOCK COUNTEREXAMPLE TO DIRECT CLEANING / ALL
EXTENSIONS DELETE OR KEMPE-DESCEND IN THE DISPLAYED REALIZATION / NOT A
GLOBALLY MINIMUM DIRTY PROJECTION / NOT A FIVECDC COUNTEREXAMPLE**.

## 1. Charged two-circuit reduction

Write (K=\mathbb F_2^2=\{0,1,2,3\}), with xor as addition, and put

\[
 q(x_1,x_2)=x_1x_2,
 \qquad B(x,y)=x_1y_2+x_2y_1.
\]

For one oriented support circuit, block (a), transformed block charge
(T_a), circuit start (z), and directed pair tensor
(w_{b\to a}), the obstruction bit is

\[
 Q_a=q(T_a)+B(z,T_a)+\sum_{b\ne a}w_{b\to a},             \tag{1}
\]

with

\[
 w_{b\to a}+w_{a\to b}=B(T_a,T_b).                       \tag{2}
\]

In a two-circuit boundary state, global block charge zero makes the two
per-circuit charges equal.  If (L_a\in\operatorname{GL}(2,2)) is the
map in block (a), write the common transformed charge as (t_a).
Adding (1) on the two circuits cancels the two copies of (q(t_a)).
Equation (2) also shows that the total pair contribution is symmetric.
Consequently

\[
 Q_a=\sum_{b\ne a}\phi_{ab}(L_a^{-1}L_b)+B(z,t_a),        \tag{3}
\]

where every \(\phi_{ab}\) is a linear functional on
\(\operatorname{Mat}_2(\mathbb F_2)\), and (z) is the relative circuit
translation.  Circuit integrability is

\[
                         \bigoplus_a t_a=0.               \tag{4}
\]

This reduction loses no arbitrary-occurrence states.  Every occurrence
pair contributes a bilinear term
(B(L_bx,L_ay)=B(L_a^{-1}L_bx,y)), hence a matrix-linear functional.
Same-block terms are precisely the quadratic terms already cancelled
above.  Arbitrary multiplicities and repeated owners therefore remain
covered.

Conversely, every matrix-linear functional is a sum of at most two
rank-one terms (B(Mx,y)).  The zero-charge word

\[
                         b(x),a(y),b(x),a(y)               \tag{5}
\]

realizes one such term.  Concatenating gadgets creates no cross terms,
because each gadget has zero charge in every owner.  Thus, when
arbitrary occurrences are allowed, (3) is also realizable rather than
merely a relaxation.

## 2. The five-block tensor

Blocks (0,1,2,3) have source charge (1) on each circuit, and block
(4) has charge zero.  In edge order

```text
01 02 03 04 12 13 14 23 24 34
```

take the coefficient masks

```text
 0  0  0  0  0  0 10  0  8  2
```

for matrix entries ((m_{11},m_{21},m_{12},m_{22})).  Thus only the
three edges from charged blocks (1,2,3) to the zero-charge block are
nonzero.

Normalize (L_0=I), so (t_0=1), and write

\[
 a=L_4(1),\qquad b=L_4(2),\qquad c=L_4(3)=a+b.             \tag{6}
\]

The three masks give

\[
 \phi_{14}=B(t_1,c),\qquad
 \phi_{24}=B(t_2,b),\qquad
 \phi_{34}=B(t_3,a).                                    \tag{7}
\]

Indeed, masks (10,8,2) select respectively
(m_{21}+m_{22},m_{22},m_{21}).

Suppose a clean assignment exists.  Since block (0) has no incident
tensor edge, its equation says

\[
 B(z,1)=0,
 \qquad\hbox{so}\qquad z\in\{0,1\}.                      \tag{8}
\]

If (z=0), equations (7) and cleanliness force

\[
                         t_1=c,\quad t_2=b,\quad t_3=a,   \tag{9}
\]

because the only nonzero vector orthogonal to a given nonzero vector in
(K) is that vector itself.  Hence
(t_1+t_2+t_3=a+b+c=0), contradicting (4), which requires this sum to
equal (t_0=1).

If (z=1), exactly one of (a,b,c) equals (1).  For either of the
other two values (r\in\{2,3\}), the corresponding clean equation is

\[
                         B(t,r+1)=0,
\]

and hence (t=r+1).  Those two forced (t)'s are (2) and (3),
whose xor is (1).  The remaining (t) is nonzero.  Therefore

\[
                    t_1+t_2+t_3=1+t_{\rm free}\ne1,      \tag{10}
\]

again contradicting (4).  This proves that the tensor has no directly
clean extension.  Once the equations at blocks (0,1,2,3) hold, the
block-4 equation would be automatic: its left side is the xor of the
three incident bits, namely
(B(z,t_1+t_2+t_3)=B(z,t_0)=0).

## 3. Literal twenty-occurrence state

Start both circuits with the charged base (0(1),1(1),2(1),3(1)).
On the first circuit only, append the three zero-charge gadgets

\[
\begin{array}{c|c}
14&4(3),1(1),4(3),1(1)\\
24&4(2),2(1),4(2),2(1)\\
34&4(1),3(1),4(1),3(1).
\end{array}                                               \tag{11}
\]

Equivalently, the owner and derivative words are

```text
A owners       0123414142424343
A derivatives  1111313121211111
B owners       0123
B derivatives  1111
```

Their per-circuit block-charge rows are both

```text
1 1 1 1 0
```

so exactly four blocks are charged.  Formula (5) shows that (11)
realizes exactly the three masks in (7).  The independent literal
checker enumerates all (6^5=7,776) block-map assignments.  Exactly
2,016 are circuit-integrable.  It checks all sixteen circuit-start pairs
for each, for 32,256 literal integrations in total, and finds zero clean
ones.  Every literal obstruction agrees with (3).

## 4. Smallest number of complement blocks

The exact SAT checker treats every pair tensor as an arbitrary
four-bit matrix-linear functional.  It fixes the common left gauge,
enumerates every integrable map assignment, and forbids every degree
vector obtainable from a relative translation.

For four blocks it covers all 56 integrable gauge classes and all 208
distinct clean targets.  The resulting CNF has 1,024 variables and
4,208 clauses and is UNSAT; CaDiCaL checks the generated proof.  Thus no
four-block tensor counterexample exists, even in the full abstract
model.  For five blocks the 10,632-variable, 43,616-clause instance is
SAT, and the literal state above independently verifies a witness.

Therefore five is the minimum number of complement blocks for a
four-charge direct-cleaning counterexample.  This is a block-order
minimality statement, not a claim that twenty is the minimum possible
number of occurrences.

## 5. Mod-two solution counts

Translation multiplicity prevents the naive parity count from proving
existence even before the counterexample is considered.  If all four
transformed charges are equal, every attainable target has two relative
translations.  If the charges form two distinct equal pairs, the target
map is injective and has one translation.

For the identically zero tensor on five blocks, the gauge-fixed clean
solution count is

\[
                    48\cdot2+288\cdot1=384\equiv0\pmod2. \tag{12}
\]

Restoring the six common maps and four common circuit starts gives
9,216 solutions, again even.  For the countertensor the solution count
is zero.  Hence an unweighted mod-two count is not an existence
certificate, and no universally existence-forcing weighted functional
supported on clean solutions can exist: it evaluates to zero on this
realizable counterexample.

## 6. Simple bridgeless cubic realization and descent

The verifier builds a simple cubic graph with 38 vertices and 57 edges.
Vertices (0,\ldots,15) and (16,\ldots,19) are the two support
circuits.  Block (0) is the edge (0-16).  Blocks (1,2,3) are
four-cycles of new internal vertices, with one spoke for each boundary
occurrence.  Block (4) is a six-cycle, with terminal derivative order

```text
1 3 2 2 3 1
```

around it.  Complementary ring values are alternately (3,2) in
blocks (1,2,3), and are (2,1,3,1,2,3) in block (4).  All
complementary values are nonzero.  Together with the integrated support
words, these values give a literal nowhere-zero
\(\mathbb F_2^3\)-flow whose first-coordinate support is the displayed
twenty-edge projection.

The checker verifies simplicity, degree three, connectedness, the flow
equation at every vertex, and connectedness after deletion of each of
the 57 edges.  Hence the realization is bridgeless.

There are 336 integrable component-map assignments after fixing the
common gauge:

```text
240  already omit a low colour on a support circuit and strictly delete
 96  use two complementary Kempe paths and then strictly delete
```

For each of the 96 residuals, one path crosses between occurrences
(0,16) in block (0), and a second crosses in block (1), with
endpoints (1,17) or (7,17).  Both paths use the same colour pair,
either \(\{1,2\}\) or \(\{1,3\}\).  Each of the four resulting
signatures occurs 24 times.  Switching both paths restores both circuit
closure equations and makes the four-edge circuit use only three low
colours.  The verifier explicitly switches the path edges, reintegrates
the support flow, translates by an omitted colour, removes the circuit
from the projection, and rechecks every full flow equation and every
nonzero edge.

Finally, a frozen proper 3-edge-colouring of all 57 graph edges is
checked at every vertex.  It is a nowhere-zero low flow with empty first
coordinate.  Thus the globally minimum extendable projection has size
zero and is clean.  The displayed size-twenty projection cannot be
globally minimum.

The exact conclusion is therefore narrow but definitive: four nonzero
per-circuit charge blocks do **not** guarantee a directly clean
extension in an arbitrary two-circuit boundary state.  The example
does not obstruct strict descent, global minimum selection, or a
five-cycle double cover.
