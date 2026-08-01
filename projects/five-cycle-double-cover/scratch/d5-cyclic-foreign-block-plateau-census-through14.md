# Cyclic foreign-block plateau census through order 14

Date: **2026-07-28**

Status: **COMPLETE FINITE CENSUS / REFINED HUMAN PROOF TARGET / NOT A
FIVECDC RESOLUTION**.

## Refined potential

Fix ordered roots \(r,s\), and let \(d_q(r,s)\) be the exact shortest
factor-component-chain distance.

For each shortest first component pair \(C(P),D(Q)\), retain only
choices for which:

1. \(|P\cap Q|=1\);
2. a \(Y_Q\)-component \(H\) contains \(r\);
3. \(H\ne D\).

Read the \(Y_Q\)-component blocks cyclically around the circuit \(C\).
Starting from the \(C\cap H\) block containing \(r\), ignore all later
returns to \(H\).  In each orientation, count the foreign
\(Y_Q\)-component blocks before the first \(D\)-block.  Define
\(b^*(q;r,s)\) as the minimum count over both orientations and all
eligible shortest choices.

If no eligible shared-coordinate choice exists, set \(b^*=0\).  This
means only that the particular shared-coordinate obstruction is
absent; it does **not** mean \(d=1\) or that the roots are good.

The exact local splice identity is

\[
Y_{\tau_Q(P)}'
  =Y_P\mathbin\triangle (Y_Q\setminus H).
\]

It proves that returns to \(H\) are harmless and that a foreign
\(Y_Q\)-component is the only possible early diversion.  In
particular, a blocker-free eligible choice preserves a length-\(d\)
root chain after the \(H\)-switch.  Neutrality remains a separate
surface-Euler issue.

## Plateau statement tested

Let \(T\) be a terminal equal-\(\chi\) plateau.  For fixed ordered
roots and fixed \(d>1,b^*\), form a connected component under neutral
moves that preserve both values.  The tested statement is:

> Every fixed-\((d,b^*)\) subplateau has a neutral boundary edge to a
> state with lexicographically smaller \((d,b^*)\).

This is stronger than merely finding a one-step \(H\)- or
first-blocker switch.  Such a restricted one-step statement is false
at order 14; see
`scratch/d5-cyclic-block-one-step-no-go-order14.md`.

## Complete results

All biconnected simple cubic graphs were generated canonically by
`geng -Cq -d3 -D3`.

| quantity | order 12 | order 14 |
|---|---:|---:|
| graphs | 81 | 480 |
| normalized \(D_5\) flows | 25,960 | 537,418 |
| states in terminal \(\chi\)-plateaus | 20,578 | 400,668 |
| ordered state-root tests | 6,296,868 | 168,280,560 |
| eligible shared-coordinate tests | 278,412 | 8,362,978 |
| tests with \(b^*>0\) | 508 | 47,011 |
| maximum observed \(b^*\) | 1 | 1 |
| fixed-\((d,b^*)\) subplateaus | 67,504 | 1,293,664 |
| failing subplateaus | **0** | **0** |

The machine-readable summaries are

```text
scratch/d5-cyclic-block-lex-order12.json
scratch/d5-cyclic-block-lex-order14.json
```

The use of ordered roots is intentional: the cyclic scan is based at
the first root, so reversing the roots is a distinct test.

## Interpretation

The earlier factor-chain census proved finite fixed-\(d\) plateau
descent.  The present census refines that object:

* at \(b^*=1\), a neutral route may first remove the cyclic blocker
  while keeping \(d\) fixed;
* at \(b^*=0\), no further blocker descent is possible, so the tested
  boundary edge must lower \(d\).

Thus a universal proof of the fixed-\((d,b^*)\) statement would imply
the terminal-\(\chi\) chain theorem.  The first-foreign-component
splice lemma supplies the circuit topology, while terminality must be
used to prove the required neutral exit from a putative closed cage.

The census does not prove this universal closed-cage exclusion.

## Reproduction

Compile:

```text
clang++ -std=c++17 -O3 -DNDEBUG \
  scratch/search_d5_terminal_cyclic_block_obstruction.cpp \
  -o /tmp/search_d5_terminal_cyclic_block_obstruction
```

Run:

```text
/opt/homebrew/bin/geng -Cq -d3 -D3 12 \
  | /tmp/search_d5_terminal_cyclic_block_obstruction

/opt/homebrew/bin/geng -Cq -d3 -D3 14 \
  | /tmp/search_d5_terminal_cyclic_block_obstruction
```

The producer enumerates normalized flows modulo global \(S_5\),
reconstructs every factor component and Kempe edge, computes
\(\chi,d,b^*\), identifies terminal equal-\(\chi\) plateaus, and
exhausts every fixed-\((d,b^*)\) component.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the cyclic
block potential, proved the local splice lemma, implemented the
census, found and independently replayed its sharp one-step no-go,
and drafted this report.  The artifacts are reproducible but have not
undergone independent human peer review.
