# Shared-pair self-reentry defeats distance-primary lifting

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE NO-GO FOR ONE PROPOSED TERMINAL-PLATEAU
PROOF MOVE / NOT A FIVECDC RESOLUTION**.

## The sound shortest-chain reduction

Let \(K_1,\ldots,K_d\) be a shortest chain of factor components from
root edge \(r\) to root edge \(s\) in the current state.  If a factor
component \(H\) containing \(r\) meets \(K_j\) for
some \(j\ge3\), then
\[
                         H,K_j,K_{j+1},\ldots,K_d
\]
has length \(d-j+2<d\), a contradiction.  Thus an endpoint component
can re-enter only the first two chain blocks.

If \(H\) meets \(K_2\), choose on the circuit \(K_2\) the last
\(H\)-edge before the \(K_2\)-to-\(K_3\) join.  An \(H\)-path from
\(r\) to that edge followed by the \(H\)-free suffix of \(K_2\) makes
\(H\) exactly the maximal active prefix of the resulting line-graph
walk.  If \(H\) is disjoint from \(K_2\), the same construction uses
the last \(H\cap K_1\) edge before the \(K_1\)-to-\(K_2\) join.

This proves a one-step *word-lifting* statement.  It does not prove that
the switch preserves the shortest factor-chain distance.

There is one clean case.  If \(K_1\) is a \(Y_P\)-component, \(H\) is a
\(Y_Q\)-component, and \(P\cap Q=\varnothing\), switching \(Q\) on
\(H\) leaves \(Y_P\) unchanged.  Hence \(K_1\) and the original
length-\(d\) chain survive.  The shared-coordinate case
\(|P\cap Q|=1\) is different:
\[
                             Y_P'=Y_P\mathbin\triangle H.       \tag{1}
\]
The following literal terminal-plateau example shows that (1) can
increase \(d\).

## Exact terminal witness

Use graph6
```text
K??FEagT@WB_
```
with its endpoint-sorted edge order
\[
\begin{split}
 &(06),(07),(08),(16),(17),(19),(26),(28),(2\,10),\\
 &(37),(39),(3\,11),(48),(4\,10),(4\,11),(59),(5\,10),(5\,11)
\end{split}
\]
and state
```text
03 05 06 05 09 0c 06 03 05 0c 09 05 05 03 06 05 06 03
```
on root edges \(r=4\) and \(s=13\).

Take
\[
\begin{array}{c|c|l}
\text{component}&\text{factor pair}&\text{edge set}\\ \hline
K_1&01&\{1,2,3,4,6,8,10,11,12,14,15,16\}\\
K_2&02&\{13,14,16,17\}\\
H&13&\{4,5,9,10\}.
\end{array}
\]
Then \(r\in K_1\cap H\), \(s\in K_2\),
\(K_1\cap K_2\ne\varnothing\), and \(H\cap K_2=\varnothing\).
Moreover \(H\cap K_1=\{4,10\}\) has two components, so this is literal
first-block self-reentry.  The pairs \(01\) and \(13\) share coordinate
\(1\).

The initial surface Euler characteristic is \(2\).  Its twenty
nonempty component switches have delta histogram
\[
                              \{0:15,\ -2:5\}.
\]
Switching pair \(13\) on \(H\) is neutral, but the exact
factor-component-chain distance changes
\[
                              2\longrightarrow3.               \tag{2}
\]

This is not merely a one-state local maximum.  Exhausting its complete
equal-\(\chi\) component modulo global \(S_5\) gives 42 states and no
positive-\(\chi\) exit.  Thus (2) occurs inside a genuine terminal
plateau.

After (2), the \(Y_{01}\)-component through the old join edge \(14\) is
\[
                         L=\{1,2,9,11,12,14\}.
\]
Switching \(01\) on \(L\) gives distance \(1\), but changes
\(\chi:2\to-2\).  Therefore the obvious two-switch splice repair leaves
the terminal plateau and cannot prove fixed-\(d\) plateau descent.

## Consequence

A Johnson prefix/suffix proof may safely absorb remote re-entry at
chain block \(K_j\), \(j\ge3\), as an immediate chain shortening, and
may safely use a first-block switch whose factor pair is disjoint from
the pair of \(K_1\).  It may **not** prescribe an arbitrary neutral
shared-coordinate endpoint switch while using \(d\) as the primary
well-founded coordinate.

The surviving order-14 theorem is weaker: within every fixed-\(d>1\)
subplateau there exists some neutral route to a descent.  In this
witness six other neutral first moves already lower \(d\); only the
prescribed self-reentry move fails.  A proof therefore needs a choice
rule selecting a safe neutral move, or a closed-cage argument over the
whole fixed-\(d\) subplateau.

## Reproduction

```text
python3 scratch/check_d5_terminal_shared_pair_self_reentry_no_go.py
```

The standard-library checker verifies the graph, bridgelessness, cubic
flow equations, displayed factors, intersection pattern, all initial
deltas, the complete 42-state terminal plateau, the distance sequence,
and the failed two-switch neutral repair.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the proposed
shortest-chain lifting move, found and checked the self-reentry
obstruction, wrote the independent replay, and drafted this note.  This
is not peer review and is not a resolution of FiveCDC.
