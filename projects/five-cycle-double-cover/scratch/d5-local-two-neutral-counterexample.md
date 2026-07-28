# An order-16 counterexample to the two-neutral strengthening

Date: **2026-07-28**

Status: **EXACT LOCAL REFUTATION / NOT A COUNTEREXAMPLE TO FiveCDC**.

The following possible repair of the failed closed-or-all-neutral lemma is
also false:

> If the three local boundary sets \(B(P,K_P)\) are all nonempty, then
> at least two of the three switches are surface-Euler neutral.

Take the graph

```text
O????B_sDOM?D_BO@W?M?
```

and, in standard graph6 upper-triangle edge order, give its 24 edges the
labels

```text
03 05 06 0a 03 09 09 03 0a 06 05 03
0a 12 18 12 0a 18 18 09 11 18 11 09
```

At vertex \(4\), use edges \(8\) and \(15\).  Their labels are \(13\)
and \(14\), and the three factor pairs active on both are
\[
                              01,\quad12,\quad34.
\]
Direct factor tracing gives:

| \(P\) | \(E(K_P)\) | \(B(P,K_P)\) | component profile after | \(\Delta\chi\) |
|:---:|:---|:---|:---:|---:|
| 01 | 3,5,6,8,12,13,15,16 | 0,4,7,11 | (3,2,1,2,2) | \(+2\) |
| 12 | 7,8,10,11,12,13,15,16 | 2,9 | (2,1,1,2,2) | \(0\) |
| 34 | 3,5,6,8,12,13,15,16 | 14,17,18,21 | (2,1,1,1,1) | \(-2\) |

The profile before switching is
\[
                  (\kappa(C_0),\ldots,\kappa(C_4))=(2,1,1,2,2).
\]
All three boundary sets are nonempty, but only the \(12\)-switch is
neutral.

The independent checker

```text
python3 scratch/check_d5_local_two_neutral_counterexample.py
```

imports no project code.  It decodes the graph6 record and verifies
simplicity, cubicity, connectedness, bridgelessness, the five parity
equations at every vertex, the three factor components and boundaries,
flow preservation after switching, and all component counts in the
table.

This leaves only the sign target
\[
                         \max_P\Delta\chi(K_P;P)\geq0
\]
(or the empirically stronger existence of one zero delta).  The witness
has changes \((-2,0,+2)\), so it does not refute that target.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the witness in an exact
finite search, reduced it to the literal data above, wrote the independent
checker, and drafted this note.  Every claim is reproducible without
trusting the search implementation or an AI system.
