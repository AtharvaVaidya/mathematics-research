# Mathematics research archive

This repository is a reproducible research workspace for current and future
mathematics papers.  It contains projects on the plane Jacobian conjecture
and the five-cycle double cover conjecture, with exact symbolic verifiers,
computational certificates, proof notes, countermodels, and route audits.

## Projects

- The files at the repository root and in `current_context/` study the
  plane Jacobian conjecture.
- [`projects/five-cycle-double-cover/`](projects/five-cycle-double-cover/)
  contains two AI-assisted research drafts, a computer-free marked-graph
  theorem, exact encodings, human-checkable intermediate countermodels,
  and compact reproducibility artifacts.  It explicitly does **not**
  claim to resolve the five-cycle double cover conjecture.

## Status

The plane Jacobian conjecture is **not resolved here**.  This repository
does not contain a proof or a counterexample in two variables.

The strongest independently audited structural result currently in the
workspace excludes every genuine consecutive \((2,3)\) five-block
completion, at every radial scale.  The proof combines the universal
deficit-one mode, a completed-square root-consumption lemma, and the
exhaustive fixed-pole Puiseux charts; it also closes ramified
multisections of the boundary normalization.  The precise hypotheses and
proof are in
[`current_context/ALLSCALE_MARKED_CUSP_OBSTRUCTION.md`](current_context/ALLSCALE_MARKED_CUSP_OBSTRUCTION.md),
with a symbolic verifier in
[`route_bd_allscale_marked_cusp_obstruction.py`](route_bd_allscale_marked_cusp_obstruction.py).
This eliminates the full consecutive five-block class, not arbitrary
Newton configurations or case c.

An exact scope audit identifies its consequence for the published GGHV
reduction: both alternatives a and b at the remaining \((72,108)\)
frontier are covered, while case c and the other higher-degree admissible
corner chains are not.  Thus the theorem plus the published reduction
forces any hypothetical counterexample of maximum degree below \(125\)
into case c; it does not by itself prove the \(125\) lower bound.  See
[`current_context/ALLSCALE_GGHV_SCOPE_AUDIT.md`](current_context/ALLSCALE_GGHV_SCOPE_AUDIT.md).

This mechanism is genuinely special to transverse degree two.  The tempting
extension to general consecutive transverse degrees is refuted by an exact
local analytic \((3,4)\) countermodel, archived in
[`current_context/TRANSVERSE_34_ROOT_CONSUMPTION_COUNTERMODEL.md`](current_context/TRANSVERSE_34_ROOT_CONSUMPTION_COUNTERMODEL.md)
and checked by
[`route_bd_transverse_34_local_countermodel.py`](route_bd_transverse_34_local_countermodel.py).
Keeping such countermodels is part of the proof audit: they prevent a valid
special theorem from being promoted into a false general one.

The proposed global degree-lowering bridge has also been audited.  Full
membership in the affine-modification subring \(k[x,x^r y]\) really does
turn a pair with Jacobian \(cx^r\) into a constant-Jacobian polynomial pair
with the same field degree.  However, an exact arbitrary-degree family
shows that boundary contraction, the leading normal jets, high field
degree, and even a finite-flat Rees comparison do not force that subring
membership or keep the diagonal sheet separate from the cusp.  See
[`current_context/LAURENT_DEGREE_DESCENT_AUDIT.md`](current_context/LAURENT_DEGREE_DESCENT_AUDIT.md).

The complementary Standard/Kummer route now has an exact one-coordinate
field-descent criterion.  For a normalized comparison branch, full descent
of \(Z,W\) is equivalent to descent of the single weighted invariant
\(\Xi=ZW^k\); an exact torus countermodel shows why valuations and local
symplecticity alone cannot force it.  See
[`current_context/RADIAL_INVARIANT_FIELD_DESCENT.md`](current_context/RADIAL_INVARIANT_FIELD_DESCENT.md).
The reciprocal Wronskian further gives canonical Darboux powers
\(S=\Xi^5\) and \(Y=T^{5k+2}\).  An exact trace-and-support argument proves
that descent of either power—or of their product
\(SY=Z^5/W^2\)—is equivalent to descent of the entire comparison branch.
A genuine-endpoint completed-local cusp model shows that none is forced by
the Liouville identity or the sole allowed ramification signature,
isolating the normalized global infinity sheet and polynomial Newton
support as essential.  See
[`current_context/RECIPROCAL_DARBOUX_LIOUVILLE_AUDIT.md`](current_context/RECIPROCAL_DARBOUX_LIOUVILLE_AUDIT.md).
The remaining global section lemma is open.

The counterexample-first fixed-source-plane route has a second independently
audited global theorem.  If a Darboux pair existed in its explicit pinch
ring and \(F(U,V)=D H\) were the pullback of the conductor-image equation,
then
\[
H|_C(-v)=-H|_C(v).
\]
Thus an additional affine preimage component over the conductor image is
compulsory.  If that image is smooth, one irreducible residual component
meets both marked cusp arms with positive odd multiplicity, and its Laurent
exponent satisfies \(m\equiv-1\pmod{2\delta}\).  Independently, the
Chau--Jelonek theorem forces a different nonproper-value component.  The
complete statement and its sharp countermodels are in
[`current_context/FIXED_SOURCE_PLANE_ROUTE.md`](current_context/FIXED_SOURCE_PLANE_ROUTE.md).
The associated counterexample-first test family is also closed exactly:
among all \(f(c)+g(c)D(3ct-2)\), the sole nonconstant submersions are
affine rescalings of \(cD(3ct-2)\), and that Hamiltonian has no polynomial
Darboux mate even in the normalization.  See
[`current_context/RESIDUAL_FACTOR_HAMILTONIAN.md`](current_context/RESIDUAL_FACTOR_HAMILTONIAN.md).
This still constrains only the fixed-source construction and is not a proof
of \(JC(2)\).

The corresponding projective intersection system has now been pushed
through the full effective pullback of the conductor image.  An exact dual
certificate rules out the first scalar boundary skeleton, but a second
19-component integral ledger satisfies every current effectivity,
adjunction, ramification, and residual-cover equation.  It fails the
minimal-resolution final-curve condition, so the next obstruction must
couple effectivity to finality rather than add more scalar inequalities.
The ledger is explicitly numerical—not a morphism or counterexample—and is
recorded in
[`current_context/GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md`](current_context/GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md).
For that ledger, the defect vector \(db-\eta\) now rules out every
branched or crossing exceptional cap over its decisive positive-label
final curve while the old coefficients are retained.  This is an exact
arbitrary-cluster theorem, although a different enlarged global ledger
remains possible; see
[`current_context/FIXED_PLANE_FINALITY_CAP_OBSTRUCTION.md`](current_context/FIXED_PLANE_FINALITY_CAP_OBSTRUCTION.md).

The workspace also contains a computer-assisted candidate elimination of
the remaining \((72,108)\) degree pair in the Guccione--Guccione--
Horruitiner--Valqui reduction.  If its full interface and reproducibility
audit is completed, it gives the bounded conclusion

\[
\max(\deg P,\deg Q)\ge125
\]

for a hypothetical complex plane Keller counterexample.  This bounded
conclusion has also been announced independently by other researchers, so
no priority or uniqueness claim is made here.

## Reproduction

The quick exact verifier suite is:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python verify_all.py
```

Several certificates also require
[Singular](https://www.singular.uni-kl.de/) 4.4 or newer.  Slow
characteristic-zero reconstruction and Gröbner calculations are kept
separate from the default suite; their notes give the exact invocation and
cache behavior.

Every script labeled a verifier uses exact arithmetic.  Files prefixed
`scratch_` are exploratory artifacts and should not be cited as proofs
without a corresponding audited note.

## Guide

- `current_context/` — focused theorem statements, derivations, and route
  audits.
- `route_bd_*.py` — exact verifiers for the bounded Newton-support and
  radial/Hurwitz program.
- `route_a/` — the pseudoplane/Darboux counterexample-first program.
- `route_3d_*.py` — audits connecting the known three-dimensional
  counterexample to two-dimensional descent problems.
- `RESEARCH_REPORT.md` — long-form research history and consolidated
  derivations.
- `STATUS_AND_PIVOT_2026-07-24.md` — the latest high-level result and
  strategy audit.
- `verify_all.py` — bundled deterministic regression suite.

## Standards used in this archive

- A finite-field calculation is not presented as a characteristic-zero
  theorem without a valid lifting or specialization argument.
- Probabilistic Gröbner output is labeled as evidence until accompanied by
  a deterministic membership, homogeneous, or independently reproduced
  certificate.
- Countermodels are retained when they falsify an attractive but invalid
  extrapolation.
- Publication claims are separated from the unresolved \(JC(2)\) goal.

## References

- J. A. Guccione, J. J. Guccione, R. Horruitiner, and C. Valqui,
  “Increasing the degree of a possible counterexample to the Jacobian
  Conjecture from 100 to 108,”
  [arXiv:2204.14178](https://arxiv.org/abs/2204.14178).
- A. Dubouloz and K. Palka, “The Jacobian Conjecture fails for
  pseudo-planes,”
  [arXiv:1701.01425](https://arxiv.org/abs/1701.01425).

## Attribution

The repository is maintained by Atharva Vaidya.  Computational and drafting
assistance from AI systems should be disclosed in any paper derived from
this archive, alongside independent human verification of the mathematical
claims.
