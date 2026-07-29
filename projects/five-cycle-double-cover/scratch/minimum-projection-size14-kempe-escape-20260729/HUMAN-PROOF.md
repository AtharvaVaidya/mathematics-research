# Kempe deletion of all order-fourteen boundary obstructions

Date: 2026-07-29

Status: **GRAPH-INDEPENDENT REDUCTION OF ALL 224 FROZEN \(7+7\)
ABSTRACT FAILURES / NOT A FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## 1. Conventions

Put \(K=\mathbb F_2^2=\{0,1,2,3\}\), with addition written as xor.
Let the support of the first coordinate be two disjoint oriented
7-circuits \(A,B\), numbered \(0,\ldots,6\) and \(7,\ldots,13\).
For a low edge word \(c\), put
\[
                         d_i=c_{i-1}+c_i,
\]
with the predecessor taken on the same circuit.

The first two census states, used for the fully displayed examples below,
share
\[
 c=\texttt{0101023|0101232},\qquad
 d=\texttt{3111121|2111311}.                         \tag{1}
\]
The entries of the partition word say which component of \(G-H\)
contains the corresponding occurrence of \(H=A\mathbin{\dot\cup}B\).
A realization of this boundary model has a distinct (possibly split)
boundary vertex for each occurrence \(i\), and the xor of the incident
non-support low values there is \(d_i\).  In particular this is
automatic in a cubic realization, where the occurrence has one
non-support edge.  The argument below does not claim the same conclusion
for a model that first identifies several circuit occurrences at one
higher-degree graph vertex without retaining their individual boundary
syndromes.

The complete census contains other words and partitions.  The only graph
fact used for all of them is the following elementary path-switch lemma.

## 2. Path-switch lemma

Fix two distinct nonzero low colours \(x,y\), and put
\(\Delta=x+y\).  Inside one component \(W\) of \(G-H\), retain the
non-support edges whose low value is \(x\) or \(y\).  There is a linear
functional \(\ell:K\to\mathbb F_2\) with
\[
                 \ell(x)=\ell(y)=1,\qquad\ell(\Delta)=0.
\]
At an internal vertex of \(W\), the retained degree is even because it
is \(\ell\) applied to the low-flow equation.  At a boundary occurrence
\(i\), its parity is \(\ell(d_i)\).  In particular, the occurrences
whose \(d_i\) is \(x\) or \(y\) are paired by paths in the retained
subgraph.

Interchange \(x\) and \(y\) on one such path.  Every internal flow
equation is unchanged: the two selected path edges both change by
\(\Delta\).  At the two endpoints the boundary derivatives change by
\(\Delta\).  All non-support edge values remain nonzero.

If the endpoints lie on the same support circuit, its two changes
cancel and the new derivatives integrate around both circuits.  If the
endpoints lie on different circuits, each circuit closure changes by
\(\Delta\).  An auxiliary component whose selected two-colour subgraph
has exactly two odd boundary occurrences, one on each circuit, contains
a path between them.  Switching that path changes both closures by a
second \(\Delta\), restoring integrability.  The all-state certificate
names such an auxiliary component whenever it uses a cross-circuit
primary pair.  In the two fully displayed examples below, block 1
serves this role.

Within this split-occurrence boundary model, the argument does not
require the complement component to be a tree or cubic.  It only uses
the low-flow equations and the fact that the displayed occurrences are
the odd boundary vertices of the selected two-colour subgraph.

## 3. Pairing-robust finite reduction

For a chosen component block and two colours \(x,y\), let \(T\) be the
boundary occurrences whose derivatives lie in \(\{x,y\}\).  The path
lemma gives a perfect matching of \(T\), but the matching depends on the
unknown realization inside the component.

The certificate therefore does not assume a pairing.  It stores a set
\(S\) of endpoint pairs such that
\[
               M\cap S\ne\varnothing
        \quad\hbox{for every perfect matching }M\hbox{ of }T. \tag{2}
\]
For each pair in \(S\), it stores a literal component-map and deletion
certificate.  There are three possible perfect matchings when
\(|T|=4\), and fifteen when \(|T|=6\).  The frozen certificates use
three and five endpoint rows, respectively.

Two independently written exhaustive boundary censuses give the same
224 raw failures:
\[
\begin{array}{c|r}
\text{component-size profile}&\text{failures}\\ \hline
6+2+2+2+2&46\\
4+4+2+2+2&178
\end{array}                                               \tag{3}
\]
The second census independently regenerates all 333 word orbits,
91,481,505 charge-valid partitions, and 80,104,020 dirty states by a
valid-block exact-cover method.  The all-state certificate finds a
deletion-only strategy for every failure.

There is one necessary refinement in the six-block profile.  Twenty-six
states use all six terminals in a majority/minority two-colour
subgraph.  The other twenty use only four terminals: the majority
colour and the colour absent from the boundary tuple.  The latter is
the usual rigid-six-pole Kempe move.  Switching one of its two paths
changes two majority terminals to the absent colour.

The four-terminal set can be distributed \(3+1\) between the two
support circuits.  In four states no suitable auxiliary cross-circuit
path exists.  This is harmless: every perfect matching of a \(3+1\)
set contains a pair among the three terminals on the same circuit, and
that path switch is integrable without an auxiliary move.

The complete 724 literal rows are in
`all-kempe-certificates.json`, and the independently written
`verify_all_certificates.py` checks (2), every map, every integrated
word, and every omitted colour.

## 4. Fully displayed \(6+2+2+2+2\) example

Take
\[
                     \pi=\texttt{0123444|4413024}.       \tag{4}
\]
Block 4 has the six occurrences
\[
                         4,5,6,7,8,13
\]
with derivative values \(1,2,1,2,1,1\).  Apply the path-switch lemma
with \(\{x,y\}=\{1,2\}\), so \(\Delta=3\).  Its three paths pair these
six occurrences somehow.  The following table covers every one of the
fifteen possible endpoint pairs.  `b1` means that a cross-circuit pair
also uses the forced auxiliary path in block 1.

All component maps not displayed are the identity `0123`.  A displayed
map `abcd` means \(0\mapsto a,1\mapsto b,2\mapsto c,3\mapsto d\).
The base column is the zero-start integration after the maps.  The last
column gives a circuit and a colour absent from its base word.

| endpoints | auxiliary | nonidentity maps | integrated base \(A|B\) | delete |
|---|---:|---|---|---|
| 4,5 | — | \(L_4=\texttt{0321}\) | `3232030\|2101230` | \(A,\mu=1\) |
| 4,6 | — | — | `3232020\|2323010` | \(A,\mu=1\) |
| 4,7 | b1 | — | `3101310\|1023010` | \(A,\mu=2\) |
| 4,8 | b1 | — | `3101310\|2023010` | \(A,\mu=2\) |
| 4,13 | b1 | — | `3101310\|2310320` | \(A,\mu=2\) |
| 5,6 | — | — | `3232320\|2323010` | \(A,\mu=1\) |
| 5,7 | b1 | — | `3101010\|1023010` | \(A,\mu=2\) |
| 5,8 | b1 | — | `3101010\|2023010` | \(A,\mu=2\) |
| 5,13 | b1 | — | `3101010\|2310320` | \(A,\mu=2\) |
| 6,7 | b1 | \(L_4=\texttt{0132}\) | `3101030\|1023010` | \(A,\mu=2\) |
| 6,8 | b1 | \(L_4=\texttt{0132}\) | `3101030\|3023010` | \(A,\mu=2\) |
| 6,13 | b1 | \(L_4=\texttt{0132}\) | `3101030\|3201230` | \(A,\mu=2\) |
| 7,8 | — | \(L_3=L_4=\texttt{0213}\) | `3231320\|2320320` | \(B,\mu=1\) |
| 7,13 | — | \(L_3=\texttt{0213},L_4=\texttt{0312}\) | `3231230\|3013010` | \(B,\mu=2\) |
| 8,13 | — | \(L_3=L_4=\texttt{0213}\) | `3231320\|1013010` | \(B,\mu=2\) |

For example, if the first path has endpoints \(4,7\), change derivatives
4 and 7 by 3 and also change the two block-1 derivatives by 3.  With
all component maps equal to the identity, integration gives
`3101310|1023010`; colour 2 is absent from the first circuit.

## 5. Fully displayed \(4+4+2+2+2\) example

Now take
\[
                     \pi=\texttt{0012340|4413024}.       \tag{5}
\]
There are two four-occurrence blocks.

Block 0 has occurrences \(0,1,6,11\), with derivatives \(3,1,1,3\).
Use the pair \(\{1,3\}\), so \(\Delta=2\).  The six possible path
endpoint pairs have these certificates:

| endpoints | auxiliary | nonidentity maps | integrated base \(A|B\) | delete |
|---|---:|---|---|---|
| 0,1 | — | \(L_1=L_4=\texttt{0213}\) | `1201010\|1310320` | \(A,\mu=3\) |
| 0,6 | — | — | `1010130\|2323010` | \(A,\mu=2\) |
| 0,11 | b1 | \(L_2=L_4=\texttt{0213}\) | `1031010\|1301020` | \(A,\mu=2\) |
| 1,6 | — | — | `3010130\|2323010` | \(A,\mu=2\) |
| 1,11 | b1 | \(L_2=L_4=\texttt{0213}\) | `3031010\|1301020` | \(A,\mu=2\) |
| 6,11 | b1 | \(L_1=\texttt{0132},L_2=L_3=\texttt{0213},L_4=\texttt{0132}\) | `3202030\|3202310` | \(A,\mu=1\) |

Block 4 has occurrences \(5,7,8,13\), with derivatives \(2,2,1,1\).
Use \(\{1,2\}\), so \(\Delta=3\):

| endpoints | auxiliary | nonidentity maps | integrated base \(A|B\) | delete |
|---|---:|---|---|---|
| 5,7 | b1 | \(L_3=L_4=\texttt{0213}\) | `3201310\|2020320` | \(B,\mu=1\) |
| 5,8 | b1 | \(L_3=\texttt{0213},L_4=\texttt{0231}\) | `3201310\|3020320` | \(B,\mu=1\) |
| 5,13 | b1 | \(L_3=L_4=\texttt{0213}\) | `3201310\|1313010` | \(B,\mu=2\) |
| 7,8 | — | \(L_3=L_4=\texttt{0213}\) | `3232010\|2320320` | \(B,\mu=1\) |
| 7,13 | — | \(L_3=\texttt{0213},L_4=\texttt{0312}\) | `3232010\|3013010` | \(B,\mu=2\) |
| 8,13 | — | \(L_3=L_4=\texttt{0213}\) | `3232010\|1013010` | \(B,\mu=2\) |

The path decomposition supplies at least one of the listed endpoint
pairs in each displayed block.  In fact every possible pair is covered.

## 6. Why an omitted colour gives a smaller projection

Apply the displayed component automorphisms to all low values in their
components, and put the integrated base values on \(H\).  This is again
a low flow, and all values off \(H\) remain nonzero.

If \(\mu\) is absent from the displayed circuit word, translate every
low value on that circuit by \(\mu\).  None becomes zero.  Now remove
that whole 7-circuit from the first-coordinate support.  The first
coordinate is still a binary cycle; all newly exposed edges have
nonzero low value; and every other edge was already nonzero as a
three-coordinate value.  The result is an extendable projection of
size seven.

Consequently every one of the 224 frozen size-fourteen failures has,
in every graph realization to which the boundary model applies, a
strictly smaller extendable projection.

This eliminates all order-fourteen obstructions to the
minimum-projection route.  It does not prove that all larger abstract
obstructions admit such an escape, and it does not resolve FiveCDC.
