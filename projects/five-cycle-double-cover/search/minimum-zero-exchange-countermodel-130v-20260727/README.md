# A 130-vertex countermodel to minimum-zero extension

Status: **EXACT ROUTE COUNTERMODEL / NOT A FIVE-CDC COUNTEREXAMPLE**.

This package refutes the `Minimum-zero matching conjecture` stated in
`docs/minimum-zero-tjoin-route.md`.  It does not refute the standard
Five-Cycle Double Cover Conjecture: the graph has an explicit standard
five-cover.

## Result

There is a finite simple connected bridgeless cubic graph \(G\) such that

\[
 r_f(G)=r_M(G)=5,
\]

but no exact-zero matching of size five packs two edge-disjoint boundary
\(T\)-joins.  Equivalently, no matching/four-flow certificate exists with
matching size at most five.  A certificate does exist with matching size
six, and its reverse lift is the retained standard five-cover.

Thus even the existential statement

> some cardinality-minimum exact-zero matching extends

is false.

## Human-checkable construction

Start with the documented 60-vertex Tait-colourable cubic core in
`docs/extremal-marked-core-reduction.md`, and mark

\[
(22,26),(30,34),(38,42),(46,50),(54,58).
\]

Take two copies.  Subdivide the five marked edges in each copy, in the
displayed order, and join corresponding subdivision vertices between the
copies.  The five new joining edges form a matching \(M_0\).

The retained `displayed_flow_values` assign zero exactly to \(M_0\) and
satisfy xor conservation at every vertex.  Deleting \(M_0\) leaves the two
65-vertex copies, each with five endpoints of \(M_0\).  Hence both
components are \(T\)-odd, so this displayed minimum support has no
\(T\)-join at all.

The lower-bound CNF allows an arbitrary \(\mathbb F_2^2\)-flow and merely
asks for at most four zero edges.  Its checked UNSAT proof therefore gives
\(r_f(G)\ge5\), stronger than the matching-supported lower bound.  The
displayed flow gives equality.

The second CNF is the complete matching/four-flow encoding plus
\(|M|\le5\).  Its checked UNSAT proof says that **none** of the minimum
exact-zero matchings extends.  The retained size-six witness verifies
directly:

- \(M=A\cap B\);
- \(M\) is a matching;
- \(A\) and \(B\) are binary cycles;
- the retained \(\mathbb F_2^2\)-flow has exact zero set \(M\); and
- the reverse-lifted five edge sets are Eulerian and cover every edge
  exactly twice.

These semantic checks are independent of the SAT solver.

## Scope

The graph has girth four and cyclic edge-connectivity three, inherited from
the recursive marked core.  It is therefore outside the cyclically
4-edge-connected, girth-at-least-ten minimum-counterexample domain.
It decisively closes the unrestricted minimum-zero exchange route, but it
does not rule out a reduced-domain variant with those extra hypotheses.

## Reproduction

From the project root:

```sh
python3 search/minimum-zero-exchange-countermodel-130v-20260727/verify.py
```

The verifier reconstructs the graph independently from the graph6 core and
marks, checks all positive witnesses by direct semantics, regenerates both
CNFs independently, and runs both `lrat-check` and CakeML `cake_lpr` on
both LRATs.

Regenerate every artifact and proof with:

```sh
python3 search/minimum-zero-exchange-countermodel-130v-20260727/build.py \
  --prove
```

## AI disclosure

The construction was found, encoded, checked, and documented with
substantial assistance from OpenAI Codex agents under human direction.
Every mathematical claim in this package is reducible to the explicit
construction, direct finite checks, and independently checked LRAT
certificates; trusting an AI system is not required.
