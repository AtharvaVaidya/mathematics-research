# A cyclic-block one-step no-go at order 14

Date: **2026-07-28**

Status: **EXACT NO-GO FOR THE RESTRICTED \(H/J\) ONE-STEP RULE;
NOT A FIVECDC RESOLUTION**.

## Metric

Fix ordered roots \(r,s\).  Among all shortest first component pairs
\(C(P),D(Q)\), retain only those for which:

1. \(|P\cap Q|=1\);
2. the \(Y_Q\)-component \(H\) containing \(r\) exists and is
   distinct from \(D\).

Around the circuit \(C\), ignore returns to \(H\).  In each
orientation count the foreign \(Y_Q\)-component blocks before the
first \(D\)-block.  Let \(b^*\) be the minimum count over both
orientations and all eligible shortest choices.  If no eligible
choice exists, set \(b^*=0\), meaning only that this
shared-coordinate obstruction is absent.  It does **not** mean that
the roots are good.

The primary metric remains the exact factor-chain distance \(d\).

## Exact witness

Use graph6

```text
M??CEB@W_sE_J?F??
```

with endpoint-sorted labels

```text
03 05 06 06 05 03 05 09 0c 03 05 06 06 05 03 0c 09 05 06 05 03
```

and ordered roots \((r,s)=(16,3)\).  A minimizing profile has

\[
\begin{array}{c|l}
C&\{6,7,10,11,12,13,16,17,18,19\}\\
H&\{7,8,15,16\}\\
D&\{0,2,3,5,18,20\}\\
J&\{9,11,12,14\}.
\end{array}
\]

It occurs for \(P=01\) or \(23\), and \(Q=02\) or \(13\).  All four
choices satisfy the explicit shared-coordinate condition
\(|P\cap Q|=1\).

A cyclic order for \(C\), rooted at edge 16, is

```text
16(H), 13, 12(J), 19, 18(D), 6, 7(H), 10, 11(J), 17.
```

Thus the first foreign block is the same component \(J\) in both
directions and

\[
                              (d,b^*)=(2,1).
\]

## Restricted moves all fail

For every minimizing profile, test switching either its root
component \(H\) or first blocker \(J\):

\[
\begin{array}{c|c|c}
Q&\text{component}&(\Delta\chi;\ d',b^{*'})\\ \hline
02&H&(-2;\ 2,1)\\
02&J&(-2;\ 2,1)\\
13&H&(0;\ 3,0)\\
13&J&(0;\ 3,0).
\end{array}
\]

The \(02\)-moves leave the terminal plateau.  The \(13\)-moves are
neutral but increase the primary distance.  Hence no prescribed
\(H/J\) move decreases the lexicographic metric.

## Exact shortest rescue

The obstruction is only to that restricted move set.  The
\(Y_{24}\)-component

\[
                         L=\{6,8,12,13,18,19\}
\]

has a neutral switch with

\[
                         (d,b^*):(2,1)\longrightarrow(1,0).
\]

This one move is automatically a shortest neutral rescue because the
source has \(d=2>1\).  Afterward the roots lie on the same
\(Y_{02}\)-component

\[
\{0,2,3,5,6,7,9,11,13,14,15,16,19,20\}.
\]

The next local lemma therefore cannot restrict attention to the two
pairs visible in the minimizing cyclic word; a third Johnson pair can
perform the decisive splice.

## Terminal semantics

The source has \(\chi=1\), with 20 nonempty switches and delta
histogram

\[
                              \{0:18,-2:2\}.
\]

Its complete equal-\(\chi\) component modulo global \(S_5\) has 236
states.  Across their directed switches the histogram is

\[
                              \{0:4248,-2:336\}.
\]

There is no positive exit, so this is a genuine terminal plateau.

## Reproduction

```text
python3 scratch/check_d5_cyclic_block_one_step_no_go_order14.py
```

The standard-library checker independently verifies graph6 decoding,
simplicity, cubicity, bridgelessness, the D5 flow equations, exact
shared-coordinate eligibility, all minimizing cyclic profiles, every
restricted outcome, the shortest rescue, and the complete terminal
plateau.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the cyclic
block metric, found the obstruction, independently replayed it, wrote
the checker, and drafted this note.  It has not undergone human peer
review and is not a resolution of FiveCDC.
