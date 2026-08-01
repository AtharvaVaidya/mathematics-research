# Unavoidable first-block reentry does not force immediate rescue

Date: **2026-07-28**

Status: **EXACT NO-GO FOR A SHORTEST-CHAIN SUBLEMMA; NOT A
RESOLUTION OF FIVECDC**.

## Result

The following proposed lemma is false:

> Let \(C,D\) be a shortest length-two factor-component chain from
> root \(r\) to root \(s\), with factor pairs \(P,Q\).  Let \(H\ne D\)
> be the \(Q\)-component through \(r\).  If, in both directions around
> \(C\), \(H\) re-enters \(C\) after the root block and before the
> first \(C\)-\(D\) join, then switching \(Q\) on \(H\) puts \(r,s\)
> on one factor component.

It remains false under all of the following additional hypotheses:

* the \(H\)-switch is \(\chi\)-neutral;
* the source belongs to a genuine terminal equal-\(\chi\) plateau;
* \(P,Q\) share a coordinate.

The same literal \(C,D,H\) also refutes the statement when \(P,Q\)
are disjoint.

## Literal graph and flow

Use graph6

```text
K??FEbGL@WB_
```

with endpoint-sorted edge order

\[
\begin{split}
 &(06),(07),(08),(16),(17),(18),(26),(29),(2\,10),\\
 &(37),(39),(3\,11),(48),(4\,10),(4\,11),(59),(5\,10),(5\,11),
\end{split}
\]

and edge labels

```text
03 05 06 05 06 03 06 03 05 03 06 05 05 06 03 05 03 06
```

where `03` denotes the coordinate set \(\{0,1\}\), `05` denotes
\(\{0,2\}\), and so on in binary-mask notation.  Take root edges
\(r=1\), \(s=15\), and \(Q=03\), meaning the coordinate pair
\(\{0,3\}\).

Every vertex is incident with one edge of each label `03`, `05`,
`06`.  Hence the three incident masks xor to zero at every vertex,
and every edge label has weight two.  This is a \(D_5\)-flow by direct
inspection.

The relevant \(Q\)-components and first factor component are

\[
\begin{array}{c|l}
C&\{1,2,3,4,6,8,12,13\}\\
D&\{7,8,15,16\}\\
H&\{0,1,3,5,9,11,12,14\}.
\end{array}
\]

The set \(C\) is simultaneously a component of \(Y_{01}\) and
\(Y_{24}\).  Thus either

\[
P=01,\ Q=03,\quad |P\cap Q|=1,
\]

or

\[
P=24,\ Q=03,\quad |P\cap Q|=0
\]

uses exactly the same three circuits.

Directly, \(r\in C\cap H\), \(s\in D\),
\(C\cap D=\{8\}\), \(H\cap D=\varnothing\), and

\[
H\cap C=\{1\}\mathbin{\dot\cup}\{3\}\mathbin{\dot\cup}\{12\}.
\]

No factor component initially contains both roots, while \(C,D\)
meet, so the exact factor-chain distance is two.

## Human check of unavoidable reentry

A cyclic edge order on \(C\), starting at \(r\), is

```text
1,2,12,13,8,6,3,4.
```

In the forward direction the relevant prefix is

```text
H(1), 2, H(12), 13, D(8).
```

In the reverse direction it is

```text
H(1), 4, H(3), 6, D(8).
```

Thus both directions leave the root \(H\)-block and encounter a new
\(H\)-component before the unique join edge \(8\).  There is no
choice of a different join.

## What the prescribed switch does

Switch \(Q=03\) on \(H\).  The new labels are

```text
03 05 06 05 06 03 06 0a 0c 03 06 05 05 06 03 0c 0a 06
```

For every coordinate pair \(R\), the exact factor identity is

\[
Y_R'=
\begin{cases}
Y_R,&|R\cap Q|\text{ even},\\
Y_R\mathbin\triangle H,&|R\cap Q|\text{ odd}.
\end{cases}
\]

The six factor components through \(r\) in the switched state are

\[
\begin{array}{c|l}
01,23&\{1,2,3,4,6,7,10,11,12,13,16,17\}\\
03,04,12&\{0,1,3,5,9,11,12,14\}\\
24&\{1,2,3,4,6,8,12,13\}.
\end{array}
\]

The six through \(s\) are

\[
\begin{array}{c|l}
02,13&\{0,2,4,5,6,8,9,10,13,14,15,17\}\\
03,12,34&\{7,8,15,16\}\\
24&\{10,11,15,17\}.
\end{array}
\]

No row on the first list equals a row on the second, so no factor
component contains both roots.  The first \(01\)-component and first
\(02\)-component intersect, so the distance is still exactly two.
Also

\[
\chi:0\longrightarrow0.
\]

Hence even a neutral unavoidable-reentry switch need not rescue.

There is an exact two-switch repair in this witness.  In the switched
state, the old set \(C\) is still the \(Y_{24}\)-component through
\(r\).  Switching \(24\) on \(C\) is neutral and changes the distance
\(2\to1\).  Thus the example refutes immediate rescue but is
consistent with a possible two-switch lemma.

## Terminal-plateau check

Exhausting the equal-\(\chi\) component modulo global \(S_5\) gives
the following seven states.  The final column counts every directed
nonempty component switch by its \(\chi\)-change.

| | labels | switch deltas |
|---:|---|---|
|1|`03 05 06 05 06 03 06 03 05 03 06 05 05 06 03 05 03 06`|`{-2:6, 0:12}`|
|2|`03 05 06 05 06 03 06 03 05 03 06 05 05 0c 09 05 09 0c`|`{-2:2, 0:12}`|
|3|`03 05 06 05 06 03 06 03 05 03 0a 09 05 06 03 09 03 0a`|`{-2:2, 0:12}`|
|4|`03 05 06 05 06 03 06 03 05 03 0a 09 05 14 11 09 11 18`|`{0:12}`|
|5|`03 05 06 05 06 03 06 0a 0c 03 06 05 05 06 03 0c 0a 06`|`{-2:2, 0:12}`|
|6|`03 05 06 05 06 03 06 0a 0c 03 06 05 05 14 11 0c 18 14`|`{0:12}`|
|7|`03 05 06 05 06 03 06 0a 0c 03 12 11 05 06 03 18 0a 12`|`{0:12}`|

Thus the complete directed histogram is

\[
\{-2:12,\ 0:84\},
\]

and there is no positive exit anywhere in the equal-\(\chi\)
component.  This is a terminal plateau, not merely a one-state local
maximum.

## Minimal-order audit

The producer

```text
python3 scratch/search_d5_unavoidable_first_block_reentry.py 4 6 8 10
```

canonically generated all connected simple cubic graphs, discarded
graphs with a bridge, and enumerated all \(D_5\)-flows modulo global
\(S_5\).  The census sizes were:

| order | bridgeless graphs | flows mod \(S_5\) |
|---:|---:|---:|
|4|1|2|
|6|2|13|
|8|5|128|
|10|18|1,525|

There was no unavoidable-reentry configuration through order eight.
At order ten there were 3,253 configurations (3,061 shared and 192
disjoint), and every prescribed switch rescued.  Therefore order
twelve is the smallest witness in this exhaustive simple bridgeless
cubic census.  The independent checker below verifies the witness
itself; the minimality statement additionally relies on `geng` and
the producer's exhaustive enumeration.

## Reproduction

```text
python3 scratch/check_d5_unavoidable_reentry_switch_no_go.py
```

The checker uses only the Python standard library.  It independently
decodes graph6, proves simplicity/cubicity/bridgelessness, checks all
\(D_5\) flow equations, verifies the displayed circuits and both
reentries, computes exact factor-chain distances before and after the
switch, verifies the factor identity, and exhausts the terminal
plateau.

## Consequence

Neither shortest-chain distance nor an “avoid reentry or switch the
root component” dichotomy can close the first-block case, even when
one restricts to neutral moves in a terminal plateau.  A viable proof
must use a more global splice, a multi-switch invariant, or a
different well-founded quantity.

This is not a counterexample to FiveCDC; the displayed labels are
themselves a \(D_5\)-flow on the graph.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated and searched
the exact sublemma, found the witness, wrote the independent checker,
and drafted this note.  The finite proof is replayable and its set
calculations are displayed above, but it has not undergone
independent human peer review.
