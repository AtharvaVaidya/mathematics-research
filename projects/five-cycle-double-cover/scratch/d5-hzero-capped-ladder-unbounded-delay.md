# \(H=0\) endpoint holonomy can have unbounded root-transition delay

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE INFINITE-FAMILY THEOREM / NOT A FIVECDC
RESOLUTION**.

## The family

Let \(L_m\), \(m\ge2\), be the capped ladder from
`d5-capped-ladder-delay-family.md`.  It has two terminal
\(K_4-e\) diamonds joined by a ladder, \(2m+10\) vertices, and nested
two-edge cuts
\[
                          D_0,D_1,\ldots,D_{m+1}.
\]
In the canonical Tait state write
\[
                        A=01,\quad B=02,\quad C=12.
\]
The cut-label word is
\[
                         A,C,B,A,C,B,\ldots.                  \tag{1}
\]

Use the edge order of the family checker.  Fix the left root
\(r=0\), initially labeled \(B=02\).  In the right cap choose any edge
\(s=s_m\) labeled \(B=02\); such an edge always exists, because its
five internal edges use all three Tait colors.

Starting from the Tait state, make two left-root switches:
\[
\begin{array}{c|c}
\text{pair}&\text{circuit}\\ \hline
03&P=\{0,3,4,5,6,7\},\\
24&Q=\{0,1,2,3\}.
\end{array}                                                   \tag{2}
\]
These supports and their legality are independent of \(m\).  Call the
resulting state \(q_m\).  Its root labels are
\[
                             q_m(r)=34,\qquad q_m(s_m)=02,     \tag{3}
\]
and all five coordinates occur.

## A uniform \(H=0\) line loop

At \(r\), lift the line sequence
\[
                              (13,34,14).                     \tag{4}
\]
Its dynamically selected circuits are
\[
                              K_1=K_3=Q,\qquad K_2=P.          \tag{5}
\]
Therefore
\[
\begin{aligned}
H&=K_1+K_3=0,\\
Z&=K_1+K_2=\{1,2,4,5,6,7\}.                                 \tag{6}
\end{aligned}
\]
In particular, the hidden support is a fixed six-edge circuit, entirely
inside the left cap, for every length of the ladder.

The first switch in (2) changes only the first cut label in (1), from
\(A=01\) to \(13\); the second switch is cap-internal.  Thus the cut word
of \(q_m\) is
\[
                         13,C,B,A,C,B,A,\ldots.               \tag{7}
\]
The first and third switches of (4) are cap-internal.  The middle switch
changes only the first cut label, from \(13\) to \(14\).  Consequently
every state along (4) has one of the two cut words
\[
                         13,C,B,A,\ldots,\qquad
                         14,C,B,A,\ldots.                     \tag{8}
\]

All four line states are root-bad.  Indeed, a factor circuit containing
both roots would cross every two-edge cut, so its factor would have to
be active on every cut label.  But the unchanged tail contains
\(C,B,A\), and
\[
                              A+B+C=0.
\]
No binary linear functional can take value one on all three: applying
it to the displayed xor would give \(1+1+1=1\ne0\).  This proves
root-badness without enumerating factor circuits.

## Unbounded-delay theorem

**Theorem.**  From either endpoint of the \(H=0\) line loop (4), every
root-transition rescue has length at least
\[
                              \left\lfloor{m+1\over3}\right\rfloor. \tag{9}
\]
Hence \(H=0\) endpoint delay is unbounded even when \(H\), \(Z\), the
root labels, and all local cap data are fixed.

**Proof.**  Xor the vertex equations on one side of a two-edge cut.
Its two edge labels are equal, so every state has a well-defined
cut-label word.

A factor circuit containing the left root meets a prefix of the nested
cuts; a factor circuit containing the right root meets a suffix.  Since
the circuit is Eulerian, at every cut it uses either both edges or
neither.  A root transition therefore applies one coordinate
transposition to a prefix or suffix of the cut word.

After \(t\) root transitions, their at most \(t\) boundaries partition
the original word into at most \(t+1\) intervals.  On each interval, one
fixed coordinate permutation has been applied.

The unchanged tail beginning at \(D_1\) is
\[
                              C,B,A,C,B,A,\ldots
\]
and contains \(\lfloor(m+1)/3\rfloor\) disjoint consecutive triples.
Every such triple has xor zero.  If one triple lay wholly inside one
interval, its three final labels would still have xor zero.

In a root-good final state, the common factor circuit crosses every cut.
The corresponding binary functional is therefore one on every final
cut label.  On the supposed unsplit triple this would make the xor of
its three values equal \(1+1+1=1\), contradicting the zero label xor.
Thus every disjoint triple contains a transition boundary.  One
boundary splits at most one of these triples, proving (9). \(\square\)

## Exact finite checks

Literal breadth-first search gives the following exact distances from
the two line endpoints:

\[
\begin{array}{c|c|c|c}
m&|V(L_m)|&\text{initial line endpoint}&\text{final line endpoint}\\ \hline
2&14&2&2\\
3&16&3&3\\
4&18&3&3\\
5&20&6&6\\
6&22&8&8.
\end{array}
\]

These values are not used in the theorem.  They confirm that the states
are eventually rescued in the tested range while the delay grows.

## Consequences

This rules out every fixed-radius \(H=0\) endpoint lemma.  It also rules
out a rescue bound depending only on
\[
       (H,\ |Z|,\ \kappa(Z),\ q(r),\ q(s),\text{ local cap geometry}),
\]
because all these data are constant in the family.

The precise surviving statement is unbounded:

> Does every \(H=0\) line endpoint in a finite rooted \(D_5\)-orbit
> admit some finite root-transition rescue?

The family neither proves nor refutes that statement.  A successful
potential must see global information such as the cut-label word; the
local residual support alone cannot be monotone enough.

## Reproduction

```text
python3 scratch/check_d5_hzero_capped_ladder_delay_family.py
python3 scratch/check_d5_hzero_capped_ladder_delay_family.py --through 6
```

The checker validates the construction, graph and flow equations,
fixed switch supports, exact \(H,Z\), cut words, line badness, and the
cut-word lower-bound hypotheses.  With `--through 6` it also checks the
displayed exact BFS distances.

## AI-use disclosure

OpenAI Codex agents, under human direction, recognized the repeating
two-edge-cut mechanism, constructed the uniform \(H=0\) states, proved
the cut-word lower bound, implemented the checks, and drafted this note.
This is not peer review and is not a resolution of FiveCDC.
