# Exact Kempe-drift identities and an eight-vertex no-go

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE IDENTITIES / AVERAGED-POSITIVE DRIFT
REFUTED / TERMINAL-PLATEAU THEOREM STILL OPEN**.

This note concerns the standard, non-orientable Five-Cycle Double
Cover formulation.  No orientation variables are used.

Let \(q:E(G)\to\binom{[5]}2\) be a \(D_5\)-flow on a connected cubic
graph \(G\) of order \(n\).  Put
\[
 C_i=\{e:i\in q(e)\},\qquad
 Y_{ij}=C_i\mathbin\triangle C_j,
\]
and let \(\kappa(C_i)\) be the number of nonempty circuit components of
\(C_i\).  The normalized coloured surface has
\[
 \Phi(q)=\chi(S(q))=\sum_{i=0}^4\kappa(C_i)-\frac n2.       \tag{1}
\]
For \(K\in\operatorname{comp}(Y_{ij})\), write \(q^{ij,K}\) for the
state obtained by transposing \(i,j\) on \(K\), and write
\[
 \Delta_q(ij,K)=\Phi(q^{ij,K})-\Phi(q).                    \tag{2}
\]

## 1. Where cross-pair coupling occurs

Let \(P=\{i,j\}\), let \(K\) be a component of \(Y_P\), and let
\(Q\in\binom{[5]}2\).  Directly from the label definition,
\[
 Y_Q(q^{P,K})=
 \begin{cases}
 Y_Q(q),&|P\cap Q|\text{ is even},\\
 Y_Q(q)\mathbin\triangle K,&|P\cap Q|=1.
 \end{cases}                                                \tag{3}
\]
Thus:

* \(Y_P\), including its individual components, is fixed by a
  \(P\)-switch;
* the three factors disjoint from \(P\) are fixed;
* the six factors sharing one coordinate with \(P\) can be split,
  joined, or otherwise repartitioned by symmetric difference with
  \(K\).

The last six factors are the entire cross-pair coupling.  In
particular, if \(P\cap Q=\varnothing\), a \(P\)-move and a \(Q\)-move
commute, their chosen circuits remain available in either order, and
their mixed Euler difference is zero:
\[
\begin{split}
 &\Phi(q^{P,K;Q,L})-\Phi(q^{P,K})\\
 &\qquad-\Phi(q^{Q,L})+\Phi(q)=0.                           \tag{4}
\end{split}
\]
For pairs sharing one coordinate, (4) need not even have a canonical
term-by-term analogue: equation (3) can replace the \(Q\)-component
list by a different partition.

## 2. The exact fixed-pair interaction identity

Fix \(P\), and list the components of \(Y_P(q)\) as
\(K_1,\ldots,K_t\).  Since a \(P\)-switch leaves \(Y_P\) fixed, these
switches commute.  For \(S\subseteq[t]\), let \(q_S\) be the result of
switching precisely the components indexed by \(S\), and put
\[
 f_P(S)=\Phi(q_S),\qquad
 \delta_r(S)=f_P(S\mathbin\triangle\{r\})-f_P(S).           \tag{5}
\]

### Theorem 1 (fixed-pair cube identity)

For every \(S\subseteq[t]\) and \(r\in[t]\),
\[
\begin{aligned}
 f_P(S)&=f_P([t]\setminus S),                              &&\tag{6}\\
 \delta_r(S\mathbin\triangle\{r\})&=-\delta_r(S),           &&\tag{7}\\
 \delta_r([t]\setminus S)&=\delta_r(S),                    &&\tag{8}\\
 \sum_{S\subseteq[t]}\delta_r(S)&=0.                       &&\tag{9}
\end{aligned}
\]
Consequently,
\[
 \sum_{S\subseteq[t]}\sum_{r=1}^t\delta_r(S)=0.            \tag{10}
\]

If
\[
 f_P(S)=\sum_{A\subseteq[t]}\widehat f_P(A)
              (-1)^{|A\cap S|}
\]
is its Boolean Fourier expansion, then
\[
 \widehat f_P(A)=0\quad\text{when }|A|\text{ is odd},       \tag{11}
\]
and the sum of all initial \(P\)-drifts is exactly
\[
 \sum_{r=1}^t\Delta_q(P,K_r)
 =-2\!\!\sum_{\substack{\varnothing\ne A\subseteq[t]\\
                         |A|\ {\rm even}}}
       |A|\,\widehat f_P(A).                                \tag{12}
\]

#### Proof

Switching every component of \(Y_P\) applies the global coordinate
transposition \(P\) to \(q\).  Global coordinate permutations do not
change \(\Phi\).  Applying that global transposition after the switches
in \(S\) gives the switches in its complement, proving (6).
Equation (7) is reversal of one involutive move.  Equation (8) follows
by applying (6) to both terms in (5), and (9) follows by pairing \(S\)
with \(S\mathbin\triangle\{r\}\).  This proves (10).

Under complementation, the Fourier character indexed by \(A\) is
multiplied by \((-1)^{|A|}\).  Hence (6) kills every odd coefficient,
which proves (11).  Finally,
\[
 f_P(\{r\})-f_P(\varnothing)
   =-2\sum_{A\ni r}\widehat f_P(A).
\]
Summing over \(r\) and using (11) gives (12). \(\square\)

Equation (12) is the exact obstruction to a naive component average:
there is no linear, one-component term.  The initial drift is made
entirely from even cross-component interactions, with no forced sign.

## 3. The all-pairs orbit identity

Work in one **literal** Kempe orbit \(\mathcal O\), without quotienting
by graph automorphisms or \(S_5\).  Make an indexed multigraph
\(\mathcal K\) whose edges are Kempe moves: parallel edges are retained
if different pairs or components happen to reach the same state.
Every indexed move has the same pair and edge-set component as its
reverse, by (3).

Define the full ten-pair drift
\[
 D(q)=
 \sum_{P\in\binom{[5]}2}
 \sum_{K\in\operatorname{comp}(Y_P(q))}
       \bigl(\Phi(q^{P,K})-\Phi(q)\bigr).                   \tag{13}
\]

### Theorem 2 (Kempe Green identity)

For every real function \(g\) on \(\mathcal O\),
\[
 \sum_{q\in\mathcal O}g(q)D(q)
 =
 -\sum_{\{q,q'\}\in E(\mathcal K)}
       \bigl(g(q')-g(q)\bigr)
       \bigl(\Phi(q')-\Phi(q)\bigr).                        \tag{14}
\]
The orientation chosen for each edge on the right is irrelevant.
In particular,
\[
\begin{aligned}
 \sum_{q\in\mathcal O}D(q)&=0,                             &&\tag{15}\\
 \sum_{q\in\mathcal O}\Phi(q)D(q)
   &=-\sum_{\{q,q'\}\in E(\mathcal K)}
          \bigl(\Phi(q')-\Phi(q)\bigr)^2\le0.              &&\tag{16}
\end{aligned}
\]
More generally, for every nondecreasing \(w:\mathbb R\to\mathbb R\),
\[
 \sum_{q\in\mathcal O}w(\Phi(q))D(q)\le0.                  \tag{17}
\]

#### Proof

Pair every directed indexed move in (13) with its reverse.  The two
terms belonging to an undirected indexed edge \(\{q,q'\}\) are
\[
 g(q)\bigl(\Phi(q')-\Phi(q)\bigr)
 +g(q')\bigl(\Phi(q)-\Phi(q')\bigr),
\]
which is the corresponding summand in (14).  Set \(g=1\),
\(g=\Phi\), or \(g=w\circ\Phi\), respectively. \(\square\)

This identity includes all cross-pair effects: the component list in
(13) is recomputed at every state, so all splicing from (3) is already
present.  Equation (16) shows that a weighted orbit-average ascent
argument points in exactly the wrong direction unless every move is
Euler-neutral.

## 4. Exact flux from a terminal plateau

Let \(T\) be an equal-\(\Phi\) plateau at level \(h\), and suppose it
is terminal: no state in \(T\) has an increasing move.  Summing (13)
only over \(T\), all internal neutral edges cancel, and every boundary
edge goes down.  Hence
\[
 \sum_{q\in T}D(q)
 =
 -\!\!\sum_{\substack{q\in T,\ q'\notin T\\q\to q'}}
       \bigl(h-\Phi(q')\bigr)\le0.                          \tag{18}
\]
It is strictly negative exactly when \(T\) has a downward exit.
Terminality therefore gives a nonpositive outward flux, not a positive
average capable of forcing root-universality.

## 5. A minimum-order negative-drift witness

Use the cube with edge order
\[
\begin{array}{c|rrrrrrrrrrrr}
e&0&1&2&3&4&5&6&7&8&9&10&11\\ \hline
uv&01&03&04&12&17&23&26&35&45&47&56&67.
\end{array}
\]
Give these edges the labels
\[
 02,01,12,01,12,02,12,12,01,02,02,01.                     \tag{19}
\]
The xor of the three incident labels is zero at each cube vertex.
The five coordinate-component counts are
\[
                    (2,2,2,0,0),
\]
so (1) gives \(\Phi=2\).  The coloured surface is connected, and a
connected closed surface has Euler characteristic at most two.
Therefore every move from (19) is nonincreasing and its equal-\(\Phi\)
plateau is terminal.

There are eighteen indexed moves.  Their complete drift histogram is
\[
                 \#\{\Delta=0\}=12,\qquad
                 \#\{\Delta=-2\}=6,                        \tag{20}
\]
and consequently
\[
                            D(q)=-12.                       \tag{21}
\]
Here is the complete hand-checkable component and drift table:
\[
\begin{array}{c|c|c}
P&\operatorname{comp}(Y_P)&\text{component drifts}\\ \hline
01&0249,\ 567(10)&-2,-2\\
02&1278,\ 346(11)&-2,-2\\
03&0135,\ 89(10)(11)&0,0\\
04&0135,\ 89(10)(11)&0,0\\
12&0135,\ 89(10)(11)&-2,-2\\
13&1278,\ 346(11)&0,0\\
14&1278,\ 346(11)&0,0\\
23&0249,\ 567(10)&0,0\\
24&0249,\ 567(10)&0,0\\
34&\varnothing&\text{none}.
\end{array}                                                 \tag{22}
\]
Parentheses distinguish the two-digit edge indices \(10,11\) from
strings of one-digit indices.  Thus, for example,
\(567(10)=\{5,6,7,10\}\).  The six decreasing moves are precisely both
components for each of the pairs \(01,02,12\).

For a rooted version, choose root edges \(0=01\) and \(6=26\) in the
edge table.  No component of any of the ten factors \(Y_P\) contains
both roots.  Thus (19) is simultaneously root-bad, in a terminal
plateau, and of strictly negative full drift.  It refutes each of the
following pointwise claims:

* a root-bad state has \(D(q)\ge0\);
* a root-bad terminal state has a positive or nonnegative average
  Euler drift;
* every move at a root-bad terminal state is neutral.

It does **not** refute terminal-plateau root-universality: another state
reachable by a neutral move in the same plateau does rescue the chosen
roots.  Explicitly, switch pair \(03\) on the component
\(\{0,1,3,5\}\).  The resulting label row is
\[
 23,13,12,13,12,23,12,12,01,02,02,01,
\]
its coordinate-component counts are \((1,2,2,1,0)\), and hence it
still has \(\Phi=2\).  In that state, the \(Y_{02}\)-component
\[
                    \{0,2,4,5,6,7,8,11\}
\]
contains both root edges \(0\) and \(6\).  Thus the displayed
root-bad **state** and its root-good terminal **plateau** are explicitly
distinguished.

Among connected simple cubic graphs this is a minimum-order example
with negative drift.  There is no such graph on two vertices; the only
one on four vertices is \(K_4\), and the two on six vertices are
\(K_{3,3}\) and the triangular prism.  Direct enumeration of all
\(180+840+540=1560\) literal \(D_5\)-flows on those three graphs finds
every Kempe move Euler-neutral.  The accompanying small checker
performs this minimality audit as well as checking (19)--(21), the
factor update law (3), and the fixed-pair identities.

## 6. Consequence for the proof program

The exact equations do not classify terminal plateaus strongly enough
to imply root-universality.  They instead isolate the missing input:
one must use the combinatorial placement of roots inside the six
shared-coordinate symmetric differences, and one must allow sequences
of neutral cross-pair splicings.  Neither a sum of local drifts nor any
nondecreasing function of \(\Phi\) can supply that information.

Reproduction:

```text
python3 scratch/check_d5_kempe_drift_cube_no_go.py
```

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the identities,
located the cube witness in the existing surface-switch artifacts,
wrote the checker, and drafted this note.  All equations and the
finite witness are exposed for independent human verification.  This
has not undergone peer review and is not a resolution of FiveCDC.
