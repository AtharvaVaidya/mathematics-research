# A minimum Fano value class need not pack

Date: 2026-07-29

Status: **EXACT PROOF-STRATEGY COUNTERMODEL / NOT A FIVECDC
COUNTEREXAMPLE**.

## Theorem

There is a finite simple connected bridgeless cubic graph \(G\) for which

\[
 \rho_3(G)=5,
\]

but no value class of cardinality \(\rho_3(G)\) in any nowhere-zero
\(\mathbb F_2^3\)-flow packs two edge-disjoint boundary \(T\)-joins.
Equivalently, the minimum-class packing defect
\(\delta_\rho(G)\) is positive.

Here

\[
 \rho_3(G)=
 \min\{|f^{-1}(a)|:f\text{ is a nowhere-zero }\mathbb F_2^3
 \text{-flow},\ a\ne0\}.
\]

Thus both of the following proposed proof steps are false without extra
hypotheses:

1. every globally minimum Fano value class packs; and
2. some globally minimum Fano value class packs.

The graph is the 130-vertex graph already frozen in
`../minimum-zero-exchange-countermodel-130v-20260727/`.  It has an
explicit size-six packing certificate and an explicit standard FiveCDC,
so it is not a counterexample to FiveCDC.

## Short human proof

Project the displayed nowhere-zero \(\mathbb F_2^3\)-flow modulo the
distinguished value \(a=(1,0,0)\).  In the integer encoding used by
`witness.json`, the first bit is the \(a\)-coordinate and the two higher
bits encode the quotient.  The exact class of value \(a\) is

\[
                  M=\{35,48,97,135,148\}.
\]

The standalone checker xors the three incident values at every vertex,
checks that no edge is zero, and checks that \(M=f^{-1}(a)\).  Hence
\(\rho_3(G)\le5\).

The independently generated CNF
`../minimum-zero-exchange-countermodel-130v-20260727/flow-at-most-four-zero.cnf`
asks for an arbitrary \(\mathbb F_2^2\)-flow with at most four zeros.
Its checked LRAT refutation proves \(r_f(G)\ge5\).  Projecting any Fano
value class gives an \(\mathbb F_2^2\)-flow with that class as its exact
zero set, so

\[
                         \rho_3(G)\ge r_f(G)\ge5.
\]

Therefore \(\rho_3(G)=5\).

Finally,
`../minimum-zero-exchange-countermodel-130v-20260727/extension-at-most-five.cnf`
is the complete exact-zero-matching/two-cycle encoding with matching
size at most five.  Its independently checked LRAT refutation proves
that no exact-zero matching of size at most five packs two disjoint
boundary \(T\)-joins.  Every Fano value class is an exact-zero matching
under quotient.  Consequently every \(\rho_3\)-minimum Fano value class
is nonpacking.

The size-six positive certificate in the inherited package proves that
the obstruction disappears one cardinality level later and directly
reconstructs a standard FiveCDC.

## Reproduction

From `projects/five-cycle-double-cover`:

```sh
python3 search/minimum-fano-class-nonpacking-130v-20260729/verify.py
python3 search/minimum-zero-exchange-countermodel-130v-20260727/verify.py
```

The first command is a dependency-free semantic check of the new Fano
witness and the inherited artifact ledger.  The second independently
regenerates both CNFs, checks the positive size-six certificate and
FiveCDC, and sends both LRAT proofs to two proof checkers.  The proof
checker executables described by the inherited package must be installed
under a discovered `.tools` directory.  In a separate worktree, set
`FIVECDC_TOOLS=/absolute/path/to/.tools` for the second command.

## Scope and novelty

This is a counterexample to an auxiliary minimum-class selection
principle, not a resolution of FiveCDC.  The graph has girth four and
cyclic edge-connectivity three, so the theorem does not rule out a
carefully justified reduced-domain version.

As of the stated date, this exact minimum-Fano-class obstruction was
found during this project and was not located in the cited sources.
That is a conservative source audit, not a claim of literature-wide
priority.  Independent specialist review is required before any formal
priority claim.

## AI-use disclosure

OpenAI Codex agents under human direction formulated the selection
principle, found and independently reproduced the retained Fano witness,
checked the logical distinction between one-join liftability and
two-join packing, and prepared this package.  The result is reduced to
explicit finite data, direct semantic checks, independently generated
CNFs, and LRAT proofs; trusting an AI system is not part of the proof.
