# Edge contraction and the degree-four \(D_5\) boundary

Date: 2026-07-28

**Later same-day update.**  The universal generalized-circuit orbit
statement suggested as a remaining search direction below is false.  A
minimum-order exact orbit trap is recorded in
`scratch/d5-contraction-generalized-circuit-no-go.md`.  The local lemmas and
the contracted-Petersen calculation in this note remain valid.

## The exact extension condition

Let \(G\) be a simple cubic graph, let \(uv\in E(G)\), and contract \(uv\)
to a degree-four vertex \(w\) of \(H=G/uv\).  Denote the two surviving
edges formerly incident with \(u\) by \(a,b\), and those formerly incident
with \(v\) by \(c,d\).

For a \(D_5\)-flow \(q\) on \(H\), parity at \(w\) gives

\[
 z:=q(a)+q(b)=q(c)+q(d)\quad\text{in }\mathbb F_2^5.
\]

The flow extends over the split and the restored edge \(uv\) exactly when
\(z\in D_5\), in which case one must put \(q(uv)=z\).  Since \(q(a)\) and
\(q(b)\) both have weight two,

\[
 \operatorname{wt}(z)\in\{0,2,4\}.
\]

Thus weight two is precisely the good boundary condition.

There is a useful warning built into this observation:

> \(D_5\)-flows on \(G\) are in bijection with \(D_5\)-flows on \(H\)
> whose prescribed side xor has weight two.

Consequently, a general theorem saying that a good flow can always be
chosen on the contraction of a bridgeless cubic graph is already the
extension step needed for FiveCDC.  It does not follow merely from the
unrooted assertion that \(H\) has some \(D_5\)-flow.

## Component Kempe switches preserve the obstruction

For a coordinate pair \(p=\{i,j\}\), let

\[
 Y_p=\{e:|q(e)\cap p|=1\}.
\]

This is an even subgraph.  A standard component Kempe switch interchanges
\(i,j\) on one connected component of \(Y_p\).

**Lemma.**  Every such switch preserves
\(\operatorname{wt}(q(a)+q(b))\).

**Proof.**  Let \(\tau_p\) be the coordinate transposition \(i\leftrightarrow
j\).  On an active label,

\[
 \tau_p(q(e))=q(e)+\mathbf1_p,
\]

while on an inactive label \(\tau_p\) fixes \(q(e)\).

If the switched component does not contain \(w\), no boundary label
changes.  If it contains \(w\), it contains **all** active edges incident
with \(w\), because all such edges meet at \(w\) and hence lie in the same
connected component of \(Y_p\).  The switch therefore has exactly the same
effect on the four boundary labels as applying the single coordinate
permutation \(\tau_p\) to all four of them.  In particular,

\[
 q'(a)+q'(b)=\tau_p(q(a))+\tau_p(q(b))
            =\tau_p(q(a)+q(b)).
\]

A coordinate permutation preserves Hamming weight. \(\square\)

The weight \(0/2/4\) of the side xor is therefore an invariant of every
standard component-Kempe orbit.  Such an orbit cannot repair a bad
contracted flow.

## A proper circuit switch is stronger

At a degree-four vertex, a connected component of \(Y_p\) can contain two
circuits meeting at \(w\).  It is valid to switch on any even edge-subset
\(Z\subseteq Y_p\), not only on the whole connected component: add
\(\mathbf1_p\) to the labels of the edges in \(Z\).  The labels stay in
\(D_5\), and the vertex xor equations are preserved because \(Z\) is even.

For such a switch,

\[
 z'=z+
 \bigl(|Z\cap\{a,b\}|\bmod2\bigr)\mathbf1_p.                 \tag{1}
\]

Evenness of \(Z\) at \(w\) says that \(Z\) uses an odd number of \(u\)-side
edges exactly when it uses an odd number of \(v\)-side edges.  Hence a
proper circuit switch can change \(z\) only when its circuit crosses the
prescribed split at \(w\).  This is the exact point missed by component
switching.

This alternate move is real, but one such move is not universally enough,
even on a very small positive example.

## Exact contracted-Petersen witness

Contract edge \(01\) in the Petersen graph.  Relabel the contracted vertex
as \(0\) and old vertices \(2,\ldots,9\) as \(1,\ldots,8\).  In the edge
order

\[
\begin{array}{c|cccccccccccccc}
r&0&1&2&3&4&5&6&7&8&9&10&11&12&13\\ \hline
h_r&
01&12&23&03&04&05&16&27&38&46&68&58&57&47
\end{array}
\]

the sides are

\[
 \{a,b\}=\{h_3,h_4\},\qquad \{c,d\}=\{h_0,h_5\}.
\]

Here the two digits in the edge row are graph vertices.  Assign the
following coordinate-pair labels:

\[
\begin{array}{c|cccccccccccccc}
r&0&1&2&3&4&5&6&7&8&9&10&11&12&13\\ \hline
q(h_r)&
01&02&01&03&12&23&12&12&13&02&01&03&02&01 .
\end{array}
\]

Direct xor at each of the nine vertices is zero, while

\[
 q(h_3)+q(h_4)=03+12=0123
                  =01+23=q(h_0)+q(h_5).
\]

The side xor has weight four.

To repair it in one proper circuit switch, equation (1) requires a
coordinate pair \(p\subseteq0123\) and a \(Y_p\)-circuit crossing the split.
The only pairs active on all four boundary edges are \(p=02\) and \(p=13\).
For either pair, \(Y_p\) is the union of the two 5-circuits

\[
 (h_0,h_5,h_6,h_{10},h_{11})
 \quad\text{and}\quad
 (h_2,h_3,h_4,h_7,h_{13}),
\]

meeting only at \(w\).  The first uses both \(v\)-side edges and the second
both \(u\)-side edges.  No even subset crosses the split.  Thus no single
proper circuit switch repairs this flow.

Two circuit switches do repair it:

\[
\begin{array}{rcl}
0123
&\xrightarrow[\{h_0,h_1,h_2,h_3\}]{p=04}&1234,\\[2mm]
1234
&\xrightarrow[\{h_0,h_4,h_6,h_9\}]{p=24}&13.
\end{array}
\]

Both displayed edge sets are 4-circuits in the factor active at the time
of the switch.  The final flow therefore extends to the Petersen graph
with label \(13\) on the restored edge.

## What this does and does not give

The exact census on this contracted Petersen graph contains 14,700 literal
\(D_5\)-flows:

\[
\begin{array}{c|ccc}
\text{side-xor weight}&0&2&4\\ \hline
\text{number of flows}&3300&6000&5400.
\end{array}
\]

Thus choosing a different flow can matter.  The checker also finds that all
14,700 flows form one orbit under generalized even-subgraph circuit
switches.  This explains why the displayed bad flow can eventually be
repaired.

It is only finite evidence, not an induction theorem.  On an arbitrary
contraction, reaching a weight-two boundary from the given flow would
certify a \(D_5\)-flow on the original split graph.  Requiring this from
every starting orbit may be strictly stronger than FiveCDC; allowing the
starting flow to be chosen makes the assertion exactly the extension
condition above.  Neither assertion follows from the unrooted existence of
some flow on \(H\).  Bridgelessness alone has not supplied the required
cross-side factor circuit.  Therefore:

1. ordinary component Kempe switching is rigorously closed by the invariant;
2. one proper circuit switch is refuted by the explicit positive witness;
3. sequences of proper circuit switches remain a valid search mechanism,
   but their universal success is false: the later 14-vertex example has a
   complete generalized-switch orbit containing no good boundary state.

## Independent replay

Run:

```text
python3 scratch/check_d5_contraction_kempe_invariant.py
```

The checker uses only the Python standard library.  It validates the
displayed labels, exhausts every component switch and every one-step even
factor switch, replays the two-step repair, enumerates all flows, and
independently builds the complete generalized-switch orbit.

## AI-use disclosure

OpenAI Codex agents, under human direction, proved the component invariant,
identified the proper-circuit refinement, found and exhaustively checked
the contracted-Petersen witness, and drafted this note.
