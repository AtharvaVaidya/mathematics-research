# Full static exchange inequalities do not force one-round Kempe descent

## 1. Algebraic boundary model

Put \(K=\mathbb F_2^2=\{0,1,2,3\}\), with addition written as xor.
Let

\[
                    H=A\mathbin{\dot\cup}B
\]

be the first-coordinate support, where \(A=(0,\ldots,7)\) and
\(B=(8,\ldots,15)\) are oriented 8-circuits.  If \(c_i\in K\) is the
low value on support edge \(i\), define its boundary derivative by

\[
                         d_i=c_{i-1}+c_i,                 \tag{1}
\]

where the predecessor is taken on the same support circuit.  The
displayed state is

\[
\begin{aligned}
c&=\texttt{01010123|01012302},\\
d&=\texttt{31111131|21113132},\\
\pi&=\texttt{0123444444130244}.                           \tag{2}
\end{aligned}
\]

The word \(\pi\) assigns boundary occurrences to the five components of
\(G-H\).  Its blocks are

\[
\begin{aligned}
W_0&=\{0,12\},&W_1&=\{1,10\},&W_2&=\{2,13\},\\
W_3&=\{3,11\},&W_4&=\{4,5,6,7,8,9,14,15\}.
\end{aligned}
\]

Direct xor in (2) is zero on each support circuit and on each component
block.  Hence (1) integrates on \(A\) and \(B\), and the component
charges are feasible.  Every \(d_i\) is nonzero, and each support
circuit uses all four values of \(K\).

Here is the general matching formulation used below.  Fix distinct
nonzero \(x,y\in K\), and put \(\Delta=x+y\).  In a complement component
\(W\), retain the low edges with value \(x\) or \(y\).  At every internal
cubic vertex the retained degree is two.  Its boundary terminals are

\[
                 T_{W;x,y}=\{i\in W:d_i\in\{x,y\}\}.
\]

Consequently the path components give a perfect matching
\(P_{W;x,y}\) of this terminal set.  Switching one matched path exchanges
\(x\) and \(y\) and changes the boundary data by

\[
                   d\longmapsto d+\Delta(\mathbf e_i+\mathbf e_j).
                                                               \tag{3}
\]

For a set \(Q\) of paths, write \(\partial Q\) for the mod-two endpoint
incidence vector.  Then the simultaneous switch is simply

\[
                         d'=d+\Delta\partial Q.          \tag{4}
\]

Internal component charge is automatic because every path contributes
two endpoints in its own component.  In the two-circuit setting, (4)
integrates on both support circuits exactly when \(Q\) contains an even
number of paths with one endpoint in \(A\) and the other in \(B\).
This is the path/matching version of the circuit-charge equation.

Componentwise affine repair has an equally concise form.  Choose
\(L_W\in\operatorname{GL}(2,2)\) and replace

\[
                         d_i\longmapsto L_{\pi_i}d_i.     \tag{5}
\]

The maps are feasible precisely when the transformed derivatives xor to
zero around \(A\) and \(B\).  Prefix integration then determines the
support values up to one translation on each circuit.  If support edge
\(i\) joins component blocks \(\pi_i\) and \(\pi_{i+1}\), it contributes
its integrated colour to both corresponding cut-parity rows.  The
extension is clean exactly when every such block/colour parity is zero.
If an integrated support circuit omits a colour \(\mu\), translate that
circuit by \(\mu\) and delete it from \(H\); no newly exposed low value is
zero.

These statements are linear identities and do not assume a particular
interior realization.  The matchings do depend on the realization.

## 2. The edge-inflation two-pole

Let \(e=uv\) be a non-support edge of low colour \(t\).  Delete \(e\),
add four new vertices \(a,b,r,s\), and add

\[
 ua,\quad bv,\quad rs,\quad ar,\quad bs,\quad as,\quad br.      \tag{6}
\]

Give \(ua,bv,rs\) colour \(t\).  If the other two nonzero colours are
\(x,y\), give \(ar,bs\) colour \(x\) and \(as,br\) colour \(y\).
Every new vertex sees \(1,2,3\), so (6) preserves the low-flow equation.
It is a \(K_4-e\) two-pole whose internal degree-two terminals are \(a,b\).

Two elementary properties are crucial.

1. For either pair \(\{t,x\}\) or \(\{t,y\}\), its bichromatic path joins
   the two old endpoints \(u,v\).  For the pair \(\{x,y\}\), the
   bichromatic component is internal.  Thus substituting (6) preserves
   every two-colour pairing among the original boundary occurrences.
2. The internal terminals \(a,b\) are distance two apart.  Every path
   from the old endpoint \(u\) to the old endpoint \(v\) through (6),
   including the two attachment edges, has length at least four.  Every
   circuit contained wholly in (6) has positive length.

Perform this substitution independently on all 47 non-support edges of
the literal 42-vertex graph in `base-edges.tsv`.  Support edges are left
unchanged.  The result has

\[
             42+4\cdot47=230\quad\hbox{vertices},\qquad
             16+7\cdot47=345\quad\hbox{edges}.             \tag{7}
\]

The gadgets are vertex-disjoint, so the result is simple and cubic.
It is connected.  The base graph is bridgeless; every attachment edge
lies on a circuit obtained from a base circuit through \(e\), and every
internal gadget edge lies on a gadget circuit or on such a terminal
path.  Hence the inflated graph is bridgeless.  The primary checker also
applies Tarjan's bridge test to all 345 edges.

### General static-exchange inflation lemma

The same gadget gives a general theorem.  Start with any finite connected
simple cubic bridgeless graph, a 2-regular support \(H\), and a displayed
extension whose low value classes \(M_c\) meet every circuit component of
\(H\).  Replace each edge outside \(H\) by a chain of \(r\) copies of
(6).  Consecutive copies are joined terminal-to-terminal by a colour-\(t\)
edge.  The resulting replacement chain has old-endpoint distance

\[
                              L=3r+1.                    \tag{7a}
\]

It preserves the low flow, the components of \(G-H\), and every
two-colour boundary pairing.  Simplicity, cubicity, connectedness, and
bridgelessness are preserved as above.

If \(L\geq |H|\), then the inflated graph satisfies all four exchange
families (8).  To prove this, decompose a binary cycle avoiding \(M_c\)
into circuits.  A circuit contained in one replacement chain has no
support edges.  Any other circuit either uses a replacement chain from
terminal to terminal, contributing at least \(L\) non-support edges, or
is contained in \(H\).  The latter would be a circuit component of the
2-regular graph \(H\), and hence would meet \(M_c\), contrary to
avoidance.  In the former case

\[
              |C-H|\geq L\geq |H|\geq |C\cap H|.
\]

Summing over the circuit decomposition proves (8).

Thus, after the elementary four-colours-per-support-circuit condition is
met, arbitrary local boundary data and its complement-path matchings can
be made compatible with all *static* minimum-exchange inequalities merely
by metric inflation.  This does not make \(H\) globally minimum: smaller
projections can use different affine zero classes.  It proves that a
general resolution cannot extract further local boundary restrictions
from the initial four inequality families alone.

## 3. Transfer of every binary-cycle inequality

For \(c\in K\), put

\[
                         M_c=\{e\in H:s(e)=c\}.
\]

The minimum-projection exchange inequality for the displayed extension is

\[
 C\cap M_c=\varnothing
 \quad\Longrightarrow\quad
 |C\cap H|\le |C-H|                                    \tag{8}
\]

for every binary cycle \(C\) of the full inflated graph.

Assign weight \(-1\) to a support edge of the base graph and weight \(4\)
to a non-support edge.  Exhausting its \(2^{22}\) binary cycles gives the
following minimum weight among nonzero cycles avoiding \(M_c\):

\[
\begin{array}{c|rrrr}
c&0&1&2&3\\ \hline
\min\bigl(4|D-H|-|D\cap H|\bigr)&10&10&6&9.
\end{array}                                             \tag{9}
\]

This finite statement transfers to the entire 230-vertex cycle space.
Indeed, decompose an inflated binary cycle into edge-disjoint circuits.
A circuit wholly contained in a gadget has positive weight.  Any other
circuit traverses each visited gadget from terminal to terminal.  On
contracting those traversals it projects to a base circuit \(D\), and
each projected non-support edge used at least four inflated edges.
Therefore its inflated weight is at least

\[
                         4|D-H|-|D\cap H|>0              \tag{10}
\]

by (9).  Avoidance of \(M_c\) is unchanged because the \(M_c\)'s are
unsubstituted support edges.  Summing (10) proves (8) for every binary
cycle, including disconnected ones.

There is a second, independent verification that avoids the transfer
enumeration.  The class sizes are

\[
                         (|M_0|,|M_1|,|M_2|,|M_3|)
                         =(6,5,3,2).                     \tag{11}
\]

For each \(c\), remove \(M_c\), let \(T_c\) be its endpoints, and solve
the unit-weight shortest-\(T_c\)-join problem in the 230-vertex graph.
The independently computed join sizes are

\[
                              (10,11,13,14).              \tag{12}
\]

Adjoining \(M_c\) gives a binary cycle containing \(M_c\), and removing
\(M_c\) is the inverse correspondence.  Equations (11)--(12) say that
the minimum containing-cycle size is 16 for all four colours.  This is
equivalent to all four families (8), and \(H\) itself attains equality.

Thus the state satisfies the complete simultaneous shortest-join
consequences of global minimality.  It does not merely satisfy the five
component charge equations.

## 4. Exact one-round failure

The inflation preserves the following simultaneous boundary path
pairings:

\[
\begin{array}{c|l}
\{1,2\}&1\!-\!10,\ 2\!-\!13,\ 3\!-\!11,\
          4\!-\!15,\ 5\!-\!7,\ 8\!-\!9,\\
\{1,3\}&0\!-\!12,\ 1\!-\!10,\ 2\!-\!13,\ 3\!-\!11,\
          4\!-\!7,\ 5\!-\!6,\ 9\!-\!14,\\
\{2,3\}&0\!-\!12,\ 6\!-\!8,\ 14\!-\!15.
\end{array}                                             \tag{13}
\]

There are 31, 63, and 3 nonempty subsets of these respective rows with
even cross-circuit parity.  For every one of the 97 charge-restoring
multiswitches, exhaustive iteration over the \(6^4\) normalized
component-map tuples in (5) gives zero clean maps and zero maps deleting
a support circuit.  The initial state itself has 320 feasible normalized
map tuples, zero clean tuples, and zero deletion tuples.

Consequently the four complete static exchange families (8), together
with every fixed-colour one-round path multiswitch and every subsequent
componentwise affine map, do not force descent.

## 5. A human-checkable two-round escape

The obstruction is not a multi-round trap.

First use colours \(\{1,2\}\), so \(\Delta=3\), and switch the two
cross-circuit paths

\[
                             1\!-\!10,\qquad4\!-\!15.     \tag{14}
\]

Two cross paths preserve both circuit charges.  Equation (4) gives

\[
                 d^{(1)}=\texttt{32112131|21213131}.     \tag{15}
\]

Zero-start integration is

\[
                 b^{(1)}=\texttt{31013210|23103210};     \tag{16}
\]

both halves still use all four colours.  Recompute the bichromatic
components in this new low flow.  The \(\{1,3\}\)-subgraph now contains
the same-circuit path \(5\!-\!6\).  Switch it, so \(\Delta=2\).  Then

\[
\begin{aligned}
d^{(2)}&=\texttt{32112311|21213131},\\
b^{(2)}&=\texttt{31013010|23103210}.                     \tag{17}
\end{aligned}
\]

Colour 2 is absent from the first half of \(b^{(2)}\).  Translate all
low values on \(A\) by 2 and remove \(A\) from the first-coordinate
support.  Every translated value on \(A\) is nonzero, and every other
edge remains nonzero as a three-coordinate value.  This is an extendable
projection supported only on \(B\), of size eight.

Equivalently, after the second neutral recolouring the new affine class
\(M^{(2)}_2\) misses the binary cycle \(A\), and

\[
                    |A\cap H|=8>|A-H|=0.                \tag{18}
\]

Thus the second round deliberately reaches a strict exchange violation.

The finite reconfiguration picture can be completed for this particular
complement multipole.  The four small \(K_4-e\) components each have one
of three boundary colours; their two terminals are forced to have the
same colour.  The large component has exactly 252 proper
three-edge-colourings and their 252 boundary profiles are distinct.
There are exactly 5,094 products of boundary profiles whose terminal
derivatives integrate on both support circuits.  Literal internal
colourings of an inflated two-pole with the same boundary data are
collapsed in this quotient.

Join two such states when one is obtained from the other by switching one
same-circuit bichromatic path, or two cross-circuit bichromatic paths, for
one fixed colour pair.  These moves generate every charge-restoring path
subset.  Exact enumeration gives a connected graph on all 5,094
boundary-profile states, with 64,497 edges and degree range 19 through
34.  Exactly 3,294 profiles admit a direct component-map clean or deletion
certificate.  Breadth-first search puts (2) at distance two from this goal
set, in agreement with (14)--(17).  Edge inflation does not change this
boundary-profile graph: every proper colouring of a replacement two-pole
has equal terminal colours, and contracting it recovers the corresponding
base-edge colour.

This connectedness is a theorem only about the displayed five
multipoles.  It does not establish a universal Kempe-connectivity theorem
for arbitrary cubic complement components.

## 6. Logical conclusion

The graph is Tait-colourable: the literal base Tait colouring extends
through every \(K_4-e\) gadget by the same construction (6).  Its actual
minimum extendable projection therefore has size zero.  The size-sixteen
projection is not globally minimum and is not a FiveCDC counterexample.

What the example proves is sharper than the earlier component-partition
counterstate:

> The four full binary-cycle exchange inequalities for one extension,
> even combined with all one-round fixed-colour complement-path
> multiswitches and all componentwise affine maps, do not imply cleaning
> or descent.

For a genuinely globally minimum projection, the exchange theorem applies
not only to the initial extension but to every extension obtained by a
support-neutral recolouring.  The two-round sequence shows why this
quantifier matters: the initial four families hold, the first round stays
four-colour on each support circuit, and the second round produces the
forbidden negative exchange (18).

Therefore a universal proof must establish a dynamic statement: from a
dirty extension, neutral reconfiguration reaches either a clean extension
or a new affine class violating one of the full cycle inequalities.  This
package neither proves nor refutes that dynamic statement.
