# Independent audit of the minimized strict-lock construction

Date: 2026-07-29

Status: **EXACT COUNTEREXAMPLE TO THE MINIMUM-PROJECTION SELECTION
CONJECTURE / HAS A FIVE-CYCLE DOUBLE COVER / NOT A FIVECDC
COUNTEREXAMPLE**.

This package independently rebuilds and audits the first strict
two-pole lock found in the project and minimizes the number of locked
base edges.

The exact conclusions are:

- the closure is a simple bridgeless cubic graph on 18 vertices;
- at its distinguished edge 5,
  \(a_0=7\) and \(a_1=5\);
- the \(a_1\)-minimum support is unique:
  \(\{5,13,14,16,17\}\);
- among all \(2^{14}=16,384\) lock sets and all 1,008 extendable base
  terminal supports, eight locks are necessary and sufficient;
- there are exactly 180 minimum eight-lock sets;
- for
  \[
             L=\{0,2,3,4,7,8,9,10\}
  \]
  the nearest competitor has relative cost one;
- the resulting graph has 162 vertices and 243 edges and is simple,
  cubic, connected, and bridgeless;
- its unique globally minimum extendable projection has size 54 and
  consists of two 27-circuits;
- that projection is uncleanable; but
- the graph has a five-cycle double cover.

Thus the graph disproves the proposed claim that every globally minimum
extendable projection is cleanable.  It does **not** disprove the
Five-Cycle Double Cover Conjecture.

## Direct FiveCDC certificate

For every edge \(e\) and \(i\in\{0,\ldots,4\}\), the mandatory formula is
\[
 \sum_i x_{e,i}=2,\qquad
 \sum_{e\ni v}x_{e,i}=0\pmod2.
\]

`fivecdc-direct-labels.txt` gives a literal two-subset label for every
one of the 243 edges in the independently specified edge order.
`verify.py` checks exact cardinality two and every one of the
\(162\cdot5\) parity equations.  Its SHA-256, including the final
newline, is

```text
845668d8778e48ae55cf7373ed159519804407a6d7afeb9999fda02cf97ae8c7
```

There is also a shorter human construction.  FiveCDC labels of the
18-vertex base and the 18-vertex closure are frozen in the checker.
For each substitution, an \(S_5\) permutation sends the closure's
marked-edge pair to the replaced base-edge pair.  Delete the two
matched edges and give both new links their common pair.  The resulting
second literal certificate has digest

```text
f1b77b572dfbd127e9dbf97a6b84a7b5be2e6d344393abb7f14b358af7b7fcd9
```

## Reproduction

From the repository root:

```sh
python3 projects/five-cycle-double-cover/scratch/minimum-projection-strict-lock-minimized-independent-audit-20260729/verify.py
python3 projects/five-cycle-double-cover/scratch/minimum-projection-strict-lock-minimized-independent-audit-20260729/independent_audit.py
shasum -a 256 -c projects/five-cycle-double-cover/scratch/minimum-projection-strict-lock-minimized-independent-audit-20260729/SHA256SUMS
```

`verify.py` uses only the Python standard library.  It constructs the
full CNF form of the exact-two/parity formula in memory, checks the
literal assignment clause by clause, and reports its deterministic
digest.

## Trust boundary and disclosure

OpenAI Codex agents under Atharva Vaidya's direction found the strict
lock, minimized the substitution set, wrote the proof and both
checkers, and produced the FiveCDC certificates.  The complete finite
claims and the human reduction are supplied for checking.  This has
not received independent human peer review, and no literature-wide
novelty or priority claim is made.
