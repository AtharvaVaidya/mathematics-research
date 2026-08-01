# A balanced rainbow witness below the colour-load threshold

Date: 2026-07-29

Status: **HUMAN-CHECKABLE LOCAL NO-GO / FIVECDC REMAINS OPEN**.

## 1. Literal boundary state

Write \(K=\mathbb F_2^2=\{0,1,2,3\}\), with addition given by xor.
On an oriented support 6-circuit, let \(r_i\) be the low value of the
edge from vertex \(i\) to vertex \(i+1\).  Take
\[
\begin{array}{c|c}
\text{object}&\text{cyclic word at }i=0,\ldots,5\\ \hline
r_i&1\,0\,2\,0\,3\,0\\
g_i=r_{i-1}+r_i&1\,1\,2\,2\,3\,3\\
\epsilon_i&0\,1\,0\,1\,0\,1.
\end{array}                                                \tag{1}
\]
Put the three vertices with \(\epsilon_i=0\) in one complement component
\(W_0\), and those with \(\epsilon_i=1\) in another component \(W_1\).
Thus the component word is also `010101`.

Each component has boundary derivative xor
\[
                             1+2+3=0.                      \tag{2}
\]
The selected xor on the support circuit is zero, so postcomposing the
low values in \(W_1\) by any
\(U\in\operatorname{GL}(2,2)\) remains integrable.

Every support edge has one endpoint in each component.  Hence all six
support edges cross \(\delta(W_1)\).  Their low-colour multiplicities
from the first row of (1) are
\[
                         (m_0,m_1,m_2,m_3)=(3,1,1,1).      \tag{3}
\]
All four are odd.  Thus \(W_1\) is rainbow-odd, and the fixed-map affine
translation system is inconsistent.  Equivalently, with
\(q(x_1,x_2)=x_1x_2\), only the value \(3\) contributes and
\[
                    F_{W_1}(I)=\sum_{e\in\delta(W_1)}q(r_e)=1. \tag{4}
\]
Adding a common translation to the circuit permutes the four values and
preserves the four odd multiplicities, so translations do not clean the
fixed-map state.

The support word uses all four elements of \(K\), so it has no immediate
whole-circuit deletion.

## 2. The colour-load test is silent

The derivative-colour counts on either side are
\[
              (k_1(W_1),k_2(W_1),k_3(W_1))=(1,1,1),
 \qquad
              (k_1(W_0),k_2(W_0),k_3(W_0))=(1,1,1).       \tag{5}
\]
Each component is minimally realized by one cubic star centre joined to
its three support leaves.  There are therefore
\[
                             |V|-|h|=2                    \tag{6}
\]
off-support vertices.  The dynamic boundary inequality has left and
right sides
\[
  \max_a k_a(W_0)+\max_b k_b(W_1)=1+1=2
       \leq 4=2(|V|-|h|).                                 \tag{7}
\]
Thus this balanced rainbow witness does not trigger the explicit
six-map colour-load descent.

## 3. Literal graph and flow

Use vertices \(0,\ldots,7\).  The support edges, in word order, are
\[
 01,\ 12,\ 23,\ 34,\ 45,\ 50,                             \tag{8}
\]
with low values `102030`.  The complement edges and their low values
are
\[
\begin{array}{c|cccccc}
\text{edge}&06&26&46&17&37&57\\ \hline
\text{low value}&1&2&3&1&2&3.
\end{array}                                                \tag{9}
\]
Give the edges in (8) first coordinate one and those in (9) first
coordinate zero.

At every support vertex the two incident support low values xor to the
value on its spoke, by (1).  At either centre, the incident values xor
to \(1+2+3=0\).  The first coordinate is the 6-circuit.  Hence this is a
nowhere-zero \(\mathbb F_2^3\)-flow.

The graph is simple and cubic.  It is connected.  Deleting any support
edge leaves the support vertices connected around the remaining
5-edge path.  Deleting a spoke still leaves its centre joined to the
support circuit through its other two spokes.  Hence it is bridgeless.
Nauty gives the canonical graph6 string
```text
Gs@ipo
```
and `planarg` reports that it is planar.

The graph is Tait-colourable.  In the edge order
\[
 01,12,23,34,45,50,06,26,46,17,37,57,
\]
one proper three-edge-colouring is
```text
1 2 1 3 2 3 2 3 1 3 2 1
```
Therefore the empty projection is extendable and globally minimum.
The displayed size-six projection is not globally minimum.

## 4. What the other five maps do

Represent a linear map by its permutation of `0123`.  Direct integration
after applying it on \(W_1\) gives:

| map | one zero-start support word | cut parity | colours used |
|---|---|---|---:|
| `0123` | `102030` | `1111` | 4 |
| `0132` | `102120` | `0000` | 3 |
| `0213` | `131030` | `0000` | 3 |
| `0231` | `131210` | `1111` | 4 |
| `0312` | `120120` | `0000` | 3 |
| `0321` | `120210` | `0000` | 3 |

Every one of the four translations has the same parity profile in a
row.  Four maps clean the state and simultaneously make one colour
absent.  The identity and `0231` retain the rainbow obstruction.

This confirms the exact scope: the example is a counterstate to forcing
the load inequality from one current rainbow witness, not a counterstate
to six-map neutralization or direct cleanability.

## 5. Minimality in the two-tree one-circuit subclass

Consider one support circuit of length \(\ell\), split between exactly
two nonempty complement components \(Y,\overline Y\), each minimally
realized by a connected cubic tree.  Suppose the derivative xor on each
side is zero.  Since every derivative is nonzero, each side has at least
two occurrences.

A cubic tree with \(k\) degree-one support leaves and all other vertices
of degree three has \(k-2\) internal vertices.  Thus the total number of
off-support vertices is
\[
                 n=(|Y|-2)+(|\overline Y|-2)=\ell-4.       \tag{10}
\]

For \(\ell=4\), both sides have size two.  Two nonzero vectors xor to
zero only when they are equal.  Each side therefore has maximum
derivative-colour multiplicity two, and
\[
                              2+2=4>0=2n.                  \tag{11}
\]

For \(\ell=5\), the side sizes are two and three.  The size-two side has
maximum multiplicity two.  Three nonzero vectors xor to zero only when
they are \(1,2,3\), so the other maximum is one.  Hence
\[
                              2+1=3>2=2n.                  \tag{12}
\]

The state (1) has \(\ell=6\), side sizes three and three, both maxima
one, and satisfies (7).  Length six is therefore smallest in this
subclass.

The exhaustive primary checker additionally imposes closure of the
whole derivative word, use of all four support colours, and odd rainbow
bit.  It finds zero load-safe rows at lengths four and five and 888 at
length six, including (1).

## 6. Exact conclusion

The example rules out deriving a colour-load violation from:

- one balanced rainbow-odd witness;
- cyclic derivative integration;
- use of all four support colours;
- connected complement components; and
- minimal cubic-tree realizations of those components.

It does not rule out a theorem using the fact that the projection itself
is globally minimum, a simultaneous family of affine witnesses, an
optimal-dual laminar structure inside the complement, or a different
dynamic exchange.
