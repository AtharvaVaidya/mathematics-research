# Eight-to-five local-rule rigidity package

Date: **2026-07-31**

Status: **PASS / partial structural no-go / FiveCDC remains unresolved**.

## Result

This package goes beyond the earlier linear-coordinate compression
obstruction.  It permits an arbitrary nonlinear lookup table

```text
old unordered coordinate pair -> new weight-two five-bit label
```

and assumes only that the table is context-free: repeated occurrences of
one old pair receive one new label.

A new 12-vertex simple bridgeless cubic Oum cover realizes twelve local
coordinate triangles whose binary incidence rows span the full
10-dimensional cycle space of `K6`.  The local parity equations therefore
force every such nonlinear table to be a coboundary

```text
r(xy) = a[x] xor a[y].
```

Weight two on all fifteen old pairs would give a `K6 -> R5`
homomorphism, but `omega(R5)=5`.  Hence this supplied eight-cover has no
context-free pair recolouring to five coordinates.

The full-rank mechanism cannot occur below order 12: the xor of all local
triangle rows is zero, so rank 10 needs at least 11 rows, and a cubic graph
has even order.  The witness attains 12.

The witness graph is 3-edge-colourable, and the package freezes an
explicit three-cycle double cover.  It is therefore **not** a graph
counterexample.  The result rules out only a static pair-type lookup.  It
does not rule out edge-dependent recolouring, flow or potential changes,
circuit switches, or a different eight-cover.

## Files

- `HUMAN-PROOF.md` gives the complete proof and exact scope.
- `verify.py` reconstructs the labelled witness from an explicit edge
  list, checks Oum compatibility, computes the triangle rank, searches
  `R5`, and checks the positive FiveCDC control.
- `certificate.json` is its frozen certificate and exact expected output.
- `independent_check.py` is differently structured: it decodes graph6,
  infers labels from block intersections, uses Tarjan bridges, low-pivot
  row reduction, enumerates all `2^15` scalar pair tables, compares them
  with all cuts of `K6`, exhausts all 906,192 six-subsets of `R5`, and
  independently finds a Tait colouring.  It imports no project code and
  does not contain the primary labelled edge list.
- `independent-output.json` is its frozen output.
- `SOURCE-AUDIT.md` records the primary-source comparison and cautious
  novelty boundary.
- `run_all.sh` runs both checks and the hash ledger.

Both implementations use only the Python standard library.  They are
independently structured, but both are AI-written and neither is
independent human review.

## Reproduction

From this directory:

```sh
./run_all.sh
```

Expected final lines:

```text
primary certificate: PASS
independent certificate: PASS
hash ledger: PASS
ALL CHECKS PASSED
```

## Novelty and literature caveat

A bounded primary-source screen through 2026-07-31 found no prior exact
statement of the 12-triangle full-rank rigidity witness, the nonlinear
context-free no-go, or the sharp order-12 lower bound for this mechanism.
Priority is **not established**.

The surrounding language is not new.  Král'--Máčajová--Pangrác--Raspaud--
Sereni--Škoviera developed configuration homomorphisms and proved the
Desargues-configuration characterization of FiveCDC in 2009.  Oum's 2026
exposition supplies the eight-cycle construction, and Hušek--Šámal prove
the exact bijection between lifting solutions and labelled covers and the
flow characterization of FiveCDC.  The present result should be described
only as a small route-delimiting lemma inside those frameworks unless a
specialist literature review establishes more.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, found the witness, wrote
the proofs and programs, performed the literature screen, and prepared
this package.  No peer review is claimed.  A human author should check the
proof line by line, reproduce the two computations, and conduct a
specialist prior-art review before scholarly submission.
