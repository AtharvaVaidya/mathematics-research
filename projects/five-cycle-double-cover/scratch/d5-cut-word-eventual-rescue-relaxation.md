# Eventual rescue in the relaxed cut-word system

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE WORD-REWRITING THEOREM / LIFTING TO KEMPE
COMPONENTS OPEN / NOT A FIVECDC RESOLUTION**.

## Abstract system

Let
\[
                    w=\lambda_0\lambda_1\cdots\lambda_{N-1}
\]
be a word of two-subsets of \(\{0,1,2,3,4\}\).  A relaxed rooted move
chooses a coordinate transposition and applies it to a prefix of \(w\).
Suffix moves could also be allowed, but are not needed below.

Fix any factor \(Y_{ij}\).  Call a letter \(\lambda\)
\((i,j)\)-active when it contains exactly one of \(i,j\).

## Termination theorem

**Theorem.**  Every length-\(N\) word can be changed, using at most
\(N\) relaxed prefix moves, into a word on which one fixed prescribed
factor \(Y_{ij}\) is active at every position.

**Proof.**  Process positions from right to left.  Suppose positions
\(k+1,\ldots,N-1\) are already active.  If \(\lambda_k\) is active, do
nothing.  Otherwise it contains both \(i,j\), or neither.

If it contains both, transpose \(i\) with a coordinate outside
\(\lambda_k\).  If it contains neither, transpose one coordinate of
\(\lambda_k\) with \(i\).  In either case the new letter at position
\(k\) is active.  Apply this transposition to the prefix ending at
\(k\).  It does not change any already fixed position to the right.

The rightmost inactive position therefore decreases strictly after
each nontrivial move.  After at most \(N\) moves every position is
active. \(\square\)

## What this proves—and what it does not

For a capped ladder, a final cut word active everywhere in one factor is
a necessary cut-level condition for a common root circuit.  The theorem
shows that the nested-cut word obstruction alone cannot create a closed
bad orbit: in the relaxed system it always terminates, with the
rightmost-inactive position as a monotone potential.

An actual root-component switch does act by a transposition on a prefix
or suffix of the cut word.  The converse is the missing statement:

> Given the desired transposition and cutoff, is there a factor
> component containing the chosen root whose crossed cuts are exactly
> that prefix?

This is false without hypotheses on the internal circuit pairing of
each ladder cell.  Therefore the relaxed theorem is not an eventual
Kempe-rescue theorem.  It isolates the surviving problem as a
**word-move lifting lemma**, not a parity or termination problem.

For the explicit \(H=0\) capped-ladder family, exact BFS through
\(L_6\) finds eventual rescues, at distances \(2,3,3,6,8\) from either
endpoint.  No closed bad ring is known.

## Reproduction

```text
python3 scratch/check_d5_cut_word_eventual_rescue_relaxation.py
```

The checker exhausts every word through length five and all ten target
factors, applies the constructive right-to-left algorithm, and verifies
the bound and monotone suffix invariant.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the relaxed word
system, proved the termination algorithm, implemented the exhaustive
checker, and identified the precise missing lifting implication.  This
is not peer review and is not a resolution of FiveCDC.
