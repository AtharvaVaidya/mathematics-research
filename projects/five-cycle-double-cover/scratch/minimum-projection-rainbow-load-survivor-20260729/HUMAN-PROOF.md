# A goal-free rainbow/load survivor with all static exchange inequalities

Date: 2026-07-29

Status: **EXACT PROOF-METHOD COUNTERSTATE / NOT GLOBALLY MINIMUM /
NOT A FIVECDC RESOLUTION**.

Put \(K=\mathbb F_2^2=\{0,1,2,3\}\), with addition written as xor.
This note gives an exact boundary state which simultaneously has

- a rainbow-odd affine-cleaning witness;
- integrability under all six common
  \(\operatorname{GL}(2,2)\) switches on that witness shore;
- no clean or whole-circuit-deletion outcome after any of the six
  switches;
- all nine six-map colour-load inequalities; and
- a simple bridgeless cubic realization satisfying all four complete
  static minimum-exchange families.

The realized projection is nevertheless not globally minimum.  Its
exact minimum size is seven.  The example therefore isolates genuine
global minimality, rather than any one listed necessary consequence, as
the still-missing hypothesis.

## 1. Boundary state and witness

Take two oriented support 7-circuits.  Their low words and complement
component word are
\[
\begin{split}
 r&=\texttt{3231320|1320320},\\
 \pi&=\texttt{01234444413024}.
\end{split}                                                \tag{1}
\]
The derivative word \(g_i=r_{i-1}+r_i\), with predecessors taken on
their own circuits, is
\[
                         g=\texttt{3112212|1212312}.       \tag{2}
\]
Every entry of (2) is nonzero.  The xor on every component block of
\(\pi\) is zero.

Let
\[
                              Y=W_0\cup W_1\cup W_3.       \tag{3}
\]
On each 7-circuit the selected derivatives are one copy each of
\(1,2,3\), so their xor is zero.  Consequently postcomposing all
components in \(Y\) by any \(U\in\operatorname{GL}(2,2)\) preserves
integration on both circuits.

The support edges crossing between \(Y\) and its complement have colour
multiplicities
\[
                              (1,1,1,3)                   \tag{4}
\]
in colours \(0,1,2,3\).  All four entries are odd, so \(Y\) is a
rainbow-odd affine dual witness.

## 2. Complete six-map table

Write a linear map as its permutation of the three nonzero values.
Direct integration after switching (3) gives:

| map | zero-start circuit words | crossing multiplicities | witness bit |
|---|---|---:|---:|
| `123` | `3231320|1320320` | \((1,1,1,3)\) | 1 |
| `132` | `2321320|1321320` | \((1,1,1,3)\) | 1 |
| `213` | `3101320|1310320` | \((2,2,0,2)\) | 0 |
| `231` | `1321320|1312320` | \((1,1,1,3)\) | 1 |
| `312` | `2101320|1301320` | \((2,2,0,2)\) | 0 |
| `321` | `1231320|1302320` | \((1,1,1,3)\) | 1 |

Each displayed circuit word uses all four elements of \(K\), so no
whole circuit can be deleted.  For each row, exhaust the four relative
translations of the second circuit.  The component cut-colour parity is
nonzero for every translation, so none is clean.

This is stronger than retaining one witness: two maps neutralize the
displayed witness, but another component row remains obstructed.  The
full underlying size-fourteen boundary counterstate in fact has no clean
or deletion outcome under any integrable component-map tuple, not only
these six.

## 3. The colour-load inequalities

The derivative colour counts are
\[
\begin{split}
 (k_1(Y),k_2(Y),k_3(Y))&=(2,2,2),\\
 (k_1(\overline Y),k_2(\overline Y),k_3(\overline Y))&=(4,4,0).
\end{split}                                                \tag{5}
\]
A common linear map merely permutes the first triple, so all six rows
have
\[
       \max_b k_b(Y)+\max_a k_a(\overline Y)=2+4=6.       \tag{6}
\]

The smallest literal realization below has four off-support vertices,
and therefore
\[
                  6\le8=2(|V|-|h|).                      \tag{7}
\]
Thus all nine boundary-load inequalities hold already before metric
inflation.

## 4. The 18-vertex base realization

Use support circuits
\[
 0\,1\,2\,3\,4\,5\,6\,0,\qquad
 7\,8\,9\,10\,11\,12\,13\,7.                             \tag{8}
\]
Add the four complement edges
\[
 0\!-\!11,\quad1\!-\!9,\quad2\!-\!12,\quad3\!-\!10,
                                                               \tag{9}
\]
and the tree edges
\[
\begin{gathered}
14\!-\!4,\ 14\!-\!5,\ 14\!-\!15,\ 15\!-\!6,\ 15\!-\!16,\\
16\!-\!13,\ 16\!-\!17,\ 17\!-\!7,\ 17\!-\!8.             \tag{10}
\end{gathered}
\]
In the order (9)--(10), give these edges low values
\[
                 \texttt{3112213212312}.                 \tag{11}
\]
Together with (1), the three incident low values xor to zero at every
vertex.  Give (8) first coordinate one and (9)--(10) first coordinate
zero.  This is a nowhere-zero three-bit flow.

The graph is simple, cubic, connected, and bridgeless.  Removing (8)
has the five components encoded by \(\pi\).

Its cycle-space dimension is ten.  Exact enumeration gives 1,024 binary
cycles and 66,207 distinct sets simultaneously missed by two low
cycles.  For the displayed support:
\[
      \text{ordered extensions}=15{,}360,\qquad
      \text{clean extensions}=0.                         \tag{12}
\]
Thus the support itself is uncleanable, not merely the displayed
extension.

## 5. Metric inflation and all four static exchange families

For every one of the thirteen non-support edges \(uv\) of low colour
\(t\), replace it by a chain of five coloured \(K_4-e\) two-poles.
One pole has new vertices \(a,b,r,s\), terminal links at \(a,b\), and
edges
\[
 rs,\ ar,\ bs,\ as,\ br.                                 \tag{13}
\]
Give the two old-endpoint terminal links, \(rs\), and every link between
consecutive poles colour \(t\).  If
\(\{x,y\}=K-\{0,t\}\), give \(ar,bs\) colour \(x\) and \(as,br\)
colour \(y\).

Every new cubic vertex sees \(1,2,3\).  The old-endpoint distance of a
five-pole chain is
\[
                              3\cdot5+1=16.               \tag{14}
\]
The inflated graph has
\[
                         |V|=278,\qquad |E|=417.          \tag{15}
\]
It remains simple, cubic, connected, and bridgeless, and the component
partition on the support remains \(\pi\).

Every support circuit in (1) contains every low colour.  A binary circuit
avoiding one class \(M_c\) therefore cannot lie wholly in the support.
If it enters a replacement chain from one old endpoint and leaves at the
other, it uses at least sixteen non-support edges, while it can use at
most fourteen support edges.  Circuits internal to a pole have no
support edges.  Decomposing a binary cycle into circuits proves all four
exchange inequalities
\[
 C\cap M_c=\varnothing
   \quad\Longrightarrow\quad |C\cap h|\le |C-h|.          \tag{16}
\]

An independent shortest-\(T_c\)-join computation gives the exact values:

| \(c\) | \(|M_c|\) | shortest \(T_c\)-join in \(G-M_c\) | containing cycle |
|---:|---:|---:|---:|
| 0 | 3 | 11 | 14 |
| 1 | 2 | 12 | 14 |
| 2 | 4 | 10 | 14 |
| 3 | 5 | 9 | 14 |

Thus the displayed support itself attains all four static optima.

Any low flow on the inflated graph with first-coordinate support fixed
to (8) contracts through each two-pole chain: summing flow conservation
over its internal vertices says that its two nonzero terminal values are
equal.  Contraction gives a low flow on the 18-vertex base with the same
support cut parities.  A clean inflated extension would therefore
contradict (12).  Hence the inflated size-fourteen support is also
uncleanable.

For the inflated graph,
\[
 |V|-|h|=264,\qquad
 6\le528=2(|V|-|h|),                                     \tag{17}
\]
so the load inequalities continue to hold.

## 6. Exact global minimum is seven

The inflation does **not** make the displayed projection globally
minimum.

Contract an arbitrary nowhere-zero three-bit flow on the inflated graph
through every replacement chain.  The equal, nonzero terminal values
give a nowhere-zero three-bit flow on the base graph.  If a contracted
non-support edge has first coordinate one, both terminal-link edges of
its chain have first coordinate one.  Therefore the inflated support
size is at least the weight of the contracted base support when old
support edges have weight one and old non-support edges have weight two.

Exact enumeration of the 1,024 base binary cycles and all 66,207
two-low-cycle missing sets gives
\[
 \min\bigl(
   |h'\cap E(\text{old support})|
   +2|h'-E(\text{old support})|
 \bigr)=7,                                                \tag{18}
\]
with six minimizers.  Thus every inflated projection has size at least
seven.

Conversely, the first 7-circuit in (8) is an extendable base projection.
One explicit full-flow vector, in the 27-edge order (8)--(10), is
\[
\begin{split}
(&3,1,3,7,5,1,5,\ 6,4,6,2,4,6,2,\\
 &6,2,2,4,2,4,6,4,2,4,6,4,2).
\end{split}                                                \tag{19}
\]
Its first coordinate is one exactly on the first seven edges.  Every
non-support value in (19) lies in the low two-dimensional subspace, so
it extends through every two-pole using only values in that subspace.
The lifted projection still has size seven.

Equations (18)--(19) prove that the inflated graph's exact minimum
extendable projection size is seven.  The displayed size-fourteen
projection is not globally minimum.

## 7. Exact conclusion and minimality

The previous exhaustive clean-or-delete theorem through total support
thirteen shows that no charge-valid boundary state of smaller support is
globally goal-free under all component maps.  The state (1) is therefore
the smallest known—and, relative to that frozen census, smallest
possible—fully goal-free abstract boundary survivor.

It proves that the conjunction of

- a balanced rainbow-odd witness;
- all six witness switches;
- the nine colour-load inequalities;
- all-four-colours on every support circuit; and
- all four complete static shortest-join inequalities

does not imply cleaning or deletion.

It does not refute the globally minimum projection route.  Exact
enumeration instead shows precisely why the state is excluded: its true
minimum is seven.  A successful resolution must use global minimality
dynamically or add a condition stronger than all four static exchange
families.

OpenAI Codex agents under Atharva Vaidya's direction found and checked
this strengthening, wrote the proof and programs, and performed the
finite computations.  It has not received independent human peer review.
