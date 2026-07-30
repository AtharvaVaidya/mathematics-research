# Order-40 augmented radius-two counterexample

Date: **2026-07-29**

Status: **EXACT COUNTEREXAMPLE TO AN AUXILIARY LOCAL-DESCENT
OBLIGATION / NOT A PROOF OR DISPROOF OF FIVECDC.**

This package freezes a cyclically four-edge-connected cubic graph and a
rooted Jaeger three-tree state whose exact augmented escape distance is
three under the project's current order
\[
             \Psi=(d_{\min},\,|K_0|+|K_1|+|K_2|).
\]
A state with a successful parallel component--circuit span flag is
terminal.  The witness therefore disproves the proposed universal
statement that every positive all-span-failing state escapes within two
reciprocal exchanges.

It does **not** disprove the Five-Cycle Double Cover Conjecture.  It only
closes this bounded-radius proof route.

The literal graph6 record is

```text
ghe?GC@@G??@?@??_@I??A?C_?G??G@?CA?@?C?G_??_@?@???@?@??_?C?G??C@?O??C?A??G????G????C????@??O??G?????_????H????_@?????G_????@G??_?C@
```

The masks and path below use this labeled record.  Applying nauty/Traces
`labelg -q` gives the canonical graph6 record frozen in
`canonical-graph6.txt`.

The standard-library structural audit proves it is simple cubic,
three-edge-connected, cyclically four-edge-connected, and of girth
five.  The external nauty/Traces `planarg -v` check classifies it as
nonplanar; the frozen result is `planarity.txt`.

At root `0`, in graph6 edge order with the three root spokes removed,
the three omitted-class masks are

```text
74750917167123596
60249003513889361
 9115267394842914
```

The seed has kernel sizes `(20,20,20)`, profile
`(4,6,2,6,6,6,2)`, `Psi=(2,60)`, and zero successful flags.
All three kernels are perfect matchings, so the kernel-sum coordinate
already has its cubic lower bound \(3|V|/2=60\).

The independent verifier checks all 1,083 candidate first swaps and
finds 93 legal neighbors.  None is lower or span-successful; 24 are
safe and equal.  It then checks every legal neighbor of those 24
states: 2,196 legal second arcs, again with no lower or successful
endpoint.  Hence escape distance is greater than two.

The following three local-position swaps give an escape:

```text
(10,9), (40,43), (15,17)
```

The first two states remain safe at `(2,60)`.  The endpoint has profile
`(6,6,6,6,4,4,0)`, kernel sizes `(20,20,21)`, `Psi=(0,61)`, and three
successful flags.  Thus the exact augmented escape distance is three.

Here the two kinds of success are kept distinct.  By
[Hušek--Šámal, Theorem 3.16](https://arxiv.org/abs/2607.24724), a zero
profile entry says that the **current** nowhere-zero
\(\mathbb F_2^3\)-flow satisfies the component-parity criterion and
therefore yields a FiveCDC.  A positive parallel span flag is a
separate, more permissive search terminal: it certifies that allowed
whole-circuit switches can reach such a zero defect.  Every state
through radius two has positive profile and zero flags.  The displayed
endpoint has both a zero profile entry and three flags; its direct
Theorem 3.16 success already suffices.

The graph itself is explicitly positive for standard FiveCDC.  In
graph6 edge order, `verify.py` checks the following 60 edge labels,
each a five-bit mask of weight two:

```text
20 24 9 5 3 17 24 18 10 9 3 5 20 5 6 12 12 6 20 17
18 3 9 10 10 3 10 9 10 3 3 9 10 17 3 10 18 9 24 24
17 17 9 24 10 18 9 17 24 24 20 9 12 3 5 12 6 24 18 10
```

Their coordinate sizes are `(27,25,15,30,23)`.  Each vertex sees xor
zero, equivalently every coordinate has even degree, and every edge has
exactly two coordinates.  The local trap therefore cannot be confused
with a FiveCDC counterexample.

Run:

```sh
python3 verify.py
shasum -a 256 -c SHA256SUMS
```

`verify.py` is independent of the C++ discovery search.  It imports only
the adjacent standard-library semantic implementation
`../jaeger-lift13-girth10-augmented-trap-20260729/independent_verify.py`;
that dependency is named and hashed in `SHA256SUMS`.

## Publication and AI-use disclosure

This finite obstruction appears new within this project, but the
radius-two obligation is a project-created auxiliary claim rather than
an established literature conjecture.  It is useful as a reproducible
negative result and proof-design constraint, not presently as a
standalone FiveCDC resolution paper.

OpenAI Codex agents, directed by Atharva Vaidya, designed the search,
found the state, independently replayed it, and drafted this package.
It has not received independent human peer review.
