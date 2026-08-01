# A no-go lemma for translating one internal factor circuit

## 1. Definitions and normalization

Identify a label in

\[
 D_5=\binom{[5]}2
\]

with its weight-two incidence vector in \(\mathbb F_2^5\).  Addition is
symmetric difference.  A `D5`-flow on a cubic graph assigns one label to each
edge so that the three labels incident with every vertex have xor zero.

For a coordinate pair \(P\), write

\[
 Y_P(q)=\{e:|q(e)\cap P|=1\}.
\]

Every vertex has degree zero or two in \(Y_P(q)\), so its nonempty components
are circuits.

Let \(z\) be a cap vertex with physical ports \(a,b,c\).  Suppose a circuit
component \(K\) of \(Y_P(q)\) contains the root, contains \(a,b\), and does not
contain \(c\).  Assume this witness is internal, meaning \(P=q(c)\).  A global
coordinate permutation lets us normalize

\[
 q(a)=01,\qquad q(b)=02,\qquad q(c)=P=12.                 \tag{1}
\]

Thus every label on \(K\) crosses the cut \(12\mid034\).

For one even vector \(h\in\mathbb F_2^5\), define \(q^h\) by

\[
 q^h(e)=
 \begin{cases}
 q(e)\mathbin\triangle h,&e\in E(K),\\
 q(e),&e\notin E(K).
 \end{cases}                                               \tag{2}
\]

The inactive port \(c\) is not in \(K\), so its label remains \(12\).  Hence
the external coordinate pairs after the translation are precisely

\[
                         03,\quad04,\quad34.                \tag{3}
\]

The pair \(34\) in (3) is essential: it can become active at both translated
ports even though it is inactive at both ports in (1).

## 2. Exact weight-two condition

> **Lemma 2.1.**  Let \(A\in D_5\) and let \(h\) have even weight.  Then
> \(A\triangle h\in D_5\) exactly in the following cases:
>
> 1. \(h=\varnothing\);
> 2. \(|h|=2\) and \(|A\cap h|=1\); or
> 3. \(|h|=4\) and the unique coordinate outside \(h\) is not in \(A\).

**Proof.**  The even vectors on five coordinates have weights zero, two, or
four.  Since

\[
 |A\triangle h|=|A|+|h|-2|A\cap h|,
\]

setting the left side and \(|A|\) equal to two gives the three displayed
conditions.  In the weight-four case it requires \(|A\cap h|=2\), equivalently
that \(A\) avoid the coordinate outside \(h\).  \(\square\)

> **Lemma 2.2.**  The assignment (2) is a `D5`-flow if and only if every
> translated label has weight two.

**Proof.**  Every vertex of the circuit \(K\) is incident with exactly two
members of \(K\).  Its local xor therefore changes by \(h+h=0\).  Vertices
outside \(K\) are unchanged.  Thus the xor equations are automatic, and the
only remaining requirement is membership of every translated label in
\(D_5\).  \(\square\)

## 3. Six-case no-go theorem

> **Theorem 3.1 (same-circuit translation no-go).**  In the normalized
> situation (1), suppose (2) is a `D5`-flow.  If the same circuit \(K\) is an
> external factor circuit of \(q^h\), then \(K\) was already an external
> factor circuit of \(q\).

**Proof.**  Legality on just the two translated port labels \(01,02\), using
Lemma 2.1, restricts \(h\) to six values.  Direct intersection with the three
external pairs in (3) gives the middle column below.  The final column records
an external factor that was already active on every edge of \(K\).

\[
\begin{array}{c|c|c}
h&\text{possible external target after translation}
 &\text{external factor already present before translation}\\ \hline
\varnothing&03,04&\text{the target pair}\\
12&03,04&\text{the target pair}\\
03&03,34&03\\
0123&03,34&03\\
04&04,34&04\\
0124&04,34&04
\end{array}                                                   \tag{4}
\]

Here are the global justifications for the last column; the local port table
alone is not enough.

- If \(h=\varnothing\), activity is unchanged.  If \(h=12\), every external
  target in its row is disjoint from \(h\), so symmetric difference by \(h\)
  preserves intersection parity with that target.  Thus every edge of \(K\)
  was already active for the target pair.
- If \(h=03\) or \(h=04\), Lemma 2.1 says that legality of every translated
  label is exactly the assertion that every original label on \(K\) crosses
  \(03\) or \(04\), respectively.
- If \(h=0123\), Lemma 2.1 says every original label on \(K\) avoids \(4\).
  Such a label crosses \(12\) by the original internal-factor hypothesis, so
  its other coordinate is in \(\{0,3\}\).  It therefore crosses \(03\).
  The case \(h=0124\) is symmetric and forces every original label to cross
  \(04\).

In every row, all edges of \(K\) were consequently active in the external
factor stated in the last column.  At a vertex of \(K\), coordinate parity
forces the third incident edge to be inactive for that factor.  Hence the
connected circuit \(K\) was a whole component of the stated \(Y_R(q)\), not
merely a subset of one.  It contains the root and the same two physical ports,
while the inactive port label \(12\) is disjoint from \(R\).  This is an
external witness before translation.  \(\square\)

The six possible values of \(h\) in (4) can also be obtained without a table.
For weight two, crossing both \(01\) and \(02\) leaves \(12,03,04\).  For
weight four, the missing coordinate must avoid
\(01\cup02=\{0,1,2\}\), leaving the complements of \(3\) and \(4\), namely
\(0124\) and \(0123\).

## 4. Consequence and limitation

Uniformly translating the already-known internal circuit cannot amplify its
mode.  Any successful proof of universal external coverage must therefore do
something genuinely global, such as change the relevant factor component or
move through a sequence of interacting component switches.

The theorem assumes an initial `D5`-flow and an internal root-to-cap factor
circuit.  It proves no such flow or circuit exists in an arbitrary cap.  In
particular it is not a proof of the double-star premise, rooted universality,
or FiveCDC.

## AI-use and novelty disclosure

OpenAI Codex, under human direction, found and checked this argument.  The
finite replay is redundant error detection for the displayed proof, not a
substitute for human review.  No claim of external novelty or standalone
publishability is made.
