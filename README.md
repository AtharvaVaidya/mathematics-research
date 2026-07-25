# Mathematics research archive

This repository is a reproducible research workspace for current and future
mathematics papers.  Its first project studies the plane Jacobian
conjecture, with exact symbolic verifiers, computational certificates, proof
notes, countermodels, and route audits.

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

This mechanism is genuinely special to transverse degree two.  The tempting
extension to general consecutive transverse degrees is refuted by an exact
local analytic \((3,4)\) countermodel, archived in
[`current_context/TRANSVERSE_34_ROOT_CONSUMPTION_COUNTERMODEL.md`](current_context/TRANSVERSE_34_ROOT_CONSUMPTION_COUNTERMODEL.md)
and checked by
[`route_bd_transverse_34_local_countermodel.py`](route_bd_transverse_34_local_countermodel.py).
Keeping such countermodels is part of the proof audit: they prevent a valid
special theorem from being promoted into a false general one.

The complementary Standard/Kummer route now has an exact one-coordinate
field-descent criterion.  For a normalized comparison branch, full descent
of \(Z,W\) is equivalent to descent of the single weighted invariant
\(\Xi=ZW^k\); an exact torus countermodel shows why valuations and local
symplecticity alone cannot force it.  See
[`current_context/RADIAL_INVARIANT_FIELD_DESCENT.md`](current_context/RADIAL_INVARIANT_FIELD_DESCENT.md).
The remaining global-invariance lemma is open.

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
