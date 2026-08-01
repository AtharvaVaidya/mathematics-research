# A certificate-checked finite rooted-interface theorem

Date: **2026-08-01**

Status: **HUMAN-CHECKABLE DEFINITIONS AND CERTIFICATES / FINITE INPUTS ONLY /
NOT A PROOF OR DISPROOF OF THE FIVE-CYCLE DOUBLE COVER CONJECTURE**.

## 1. D5 flows and five cycle double covers

Let

\[
D_5=\{x\in\mathbb F_2^5: |x|=2\}.
\]

A `D5` flow on a graph assigns a label in `D5` to each edge and requires the
xor of the incident labels to vanish at every vertex.  An edge belongs to the
two coordinate edge sets named by its label.  The xor equation says that each
coordinate edge set has even degree at every vertex.  Conversely, five even
edge sets covering each edge exactly twice give precisely such labels and xor
equations.  Thus `D5` flows are exactly five-cycle-double-cover labelings in
the even-edge-set convention.  Empty coordinate sets are allowed; this is
the usual “at most five” padding convention.

This elementary equivalence is global.  The theorem proved by this package is
about additional rooted local properties of `D5` flows on specified finite
graphs; it is not a global existence theorem for arbitrary bridgeless graphs.

## 2. Rooted typed interfaces

Let `G` be a simple cubic graph.  Fix a cap vertex `z`.  Its three incident
edges, in graph6 decoder incidence order, are physical ports 0, 1, and 2.  Fix
a root edge `r` not incident with `z`; such `(z,r)` is a *proper interface*.

For a coordinate pair `P` and a `D5` flow `q`, define

\[
Y_P(q)=\{e: |q(e)\cap P|=1\}.
\]

At every vertex, `Y_P(q)` has even degree, so every nonempty component is a
circuit in a cubic graph.  Consider a component of `Y_P(q)` that contains
`r` and exactly two cap ports.  Its physical type is one of `01`, `02`, or
`12`.  Let `L` be the label on the inactive third cap edge.  Local xor implies
that either `P=L` or `P` is disjoint from `L`.  Call these modes *internal*
and *external*, respectively.

The typed signature of `(z,r)` is a six-bit mask: one bit for each
`(physical type, mode)`.  The aggregate signature is the union over the
examined `D5` flows.  A *double star* means that, for two distinct physical
types, both their internal and external bits occur.

For one flow, its external port mask is the union of the physical ports on
all external factor components containing `r`.  Mask `111` means that at
least two distinct physical types occur and hence all three cap ports are
covered.  The three predicates checked here are:

- **double star:** the aggregate typed signature contains a double star;
- **aggregate external:** the union of external port masks is `111`; and
- **simultaneous external:** one flow has external port mask `111`.

The last predicate implies the second, but both are reported separately so
that aggregate and one-flow assertions cannot be conflated.

## 3. Exact finite theorem

For every proper interface in each row of the following inputs, all three
predicates hold.

| input | graphs | interfaces | compact witness flows |
|:--|--:|--:|--:|
| all biconnected simple cubic order 16 | 3,874 | 1,301,664 | 65,185 |
| cyclic-4 non-Tait order 18 | 2 | 864 | 23 |
| cyclic-4 non-Tait order 20 | 6 | 3,240 | 102 |
| cyclic-4 non-Tait order 22 | 31 | 20,460 | 1,039 |
| cyclic-4 non-Tait order 24 | 155 | 122,760 | 5,299 |
| cyclic-4 non-Tait order 26 | 1,297 | 1,213,992 | 51,436 |
| retained order-34 strong-snark rows | 7 | 11,424 | 997 |
| **total** | **5,372** | **2,674,404** | **124,081** |

The order-16 input is the exact byte stream from

```sh
geng -Cq -d3 -D3 16
```

and has SHA-256
`57104aba69a542707e11ebdd8d6105afc2ce56d78b45f2e1ff0db55c1fab9de2`.
The order 18--26 files were generated and retained by the documented
Snarkhunter command `snarkhunter n 4 S s C4 o g`.  Their generator logs and
hashes are frozen in `SOURCES.md`.  Completeness of those canonical corpora
depends on nauty/Snarkhunter; the witness checker independently verifies the
properties of every supplied row but is not a second canonical generator.

The order-34 claim is intentionally only about the seven literal retained
rows.  No completeness claim about all order-34 strong snarks is made here.

## 4. Why the certificate proves the table

`predicate_stream.cpp` enumerates `D5` flows using xor propagation.  It fixes
the first assigned edge to `01` and quotients the remaining search by the
setwise stabilizer of `01` in `S5`.  This is sound because every global `S5`
orbit has a representative with that edge labeled `01`, and two such
representatives differ by the stabilizer.  The search stops on a graph only
after all three existential predicates are witnessed at every interface.

For a positive result, neither completeness of this flow enumeration nor the
symmetry argument must be trusted: the program emits the explicit flow states
actually needed.  For each interface the certificate retains one
simultaneous-external provider and providers for the four typed bits of a
double star.  Duplicate provider flows are shared across interfaces.

`verify_witnesses.py` is a separate implementation.  From the graph6 row and
hexadecimal edge labels alone it:

1. decodes the graph and checks the claimed graph metadata;
2. checks every label has weight two and every vertex xor is zero;
3. reconstructs every `Y_P` and its connected components;
4. recomputes the six-bit typed and external port masks; and
5. checks all three predicates at every proper interface.

It hashes the graph6 rows embedded in the certificate, so a certificate for a
different corpus cannot pass under the expected digest.  The expected primary
and independent outputs are compared byte-for-byte by `run_all.sh`.

## 5. Exact limitations and publication status

This computation finds no rooted-interface obstruction in the stated finite
inputs.  It does not establish a finite cutoff, a reduction from arbitrary
minimal counterexamples to these inputs, or a universal double-star or
simultaneous-external theorem.  It therefore does not prove FiveCDC.  It also
does not provide an UNSAT instance or certificate and therefore does not
disprove FiveCDC.

The local simultaneous condition can support an external/external gluing
step when compatible capped shores are already available, but this package
does not prove that arbitrary 3-cuts can always be decomposed into such shores
or that repeated gluing preserves every required root condition.

The finite predicate and its order-26/retained-order-34 census may be suitable
as a scoped computational appendix after a conventional literature and
novelty review.  It must not be advertised as a resolution or as an
order-34 exhaustive theorem.

## AI-use disclosure

OpenAI Codex agents, under human direction, proposed the rooted predicates,
wrote the search and independent certificate checker, ran the computations,
and drafted this package.  Agent cross-checks are not independent human
verification or peer review.  Any submission should disclose this use,
rerun the artifacts in a clean environment, have a human graph theorist check
the definitions and claims, and assign normal scholarly responsibility to
human authors.
