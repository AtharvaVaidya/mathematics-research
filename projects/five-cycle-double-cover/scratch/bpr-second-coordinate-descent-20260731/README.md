# Second-coordinate BPR descent frontier

This package closes the **single selected shore** part of the
larger-blocker problem.  The coordinatewise-minimal non-tight odd
profiles are \((3,3)\) and \((5,1)\).  For either profile, a cut value
\(t\) can be chosen whose partner \(b+t\) is absent, and a short
cycle/cut-space argument proves that some legal \(t\)-switch makes the
old blocker shore terminal-even.  The same result holds for every odd
blocker with fewer than nine nonmatching cut edges; nine is sharp.

The package also gives a corrected conditional second-coordinate
descent theorem.  In the residual-fixed all-in transport, it tracks the
**integer** change in every surviving odd component, rather than only
its parity.  When old even components remain even and no surviving odd
component loses target-cut edges, the selected blocker disappears and
the globally reoptimized lexicographic potential strictly decreases.

What remains open is simultaneous coordination: the guaranteed legal
cycle need not lie in the all-in cycle space, the parity constraints can
have the exact cut-space obstruction displayed in `HUMAN-PROOF.md`, and
the signed integer gains need not all have the favorable direction.
Unrestricted global rerouting can help, but is not proved always to
avoid new bad shores.

The existing 30,450-vertex graph is non-Tait and girth ten, but its
retained package expressly has no cyclic-connectivity certificate.  The
Petersen-lift samples produced no qualifying non-Tait host.  Therefore
this package does not claim a high-girth counterexample, BPR, or a
FiveCDC resolution.

## Reproduction

```sh
python3 -B verify_minimal_profiles.py
python3 -B verify_minimal_profiles_independent.py
shasum -a 256 -c SHA256SUMS
```

The first finite script exhausts sorted cut multisets.  The second is an
independently written count-vector enumerator.  Both cover all target
values and all admissible profiles of sizes 3, 5, 7, and 9.  The proof
itself is independent of the enumeration.

## AI disclosure

OpenAI Codex agents, directed by Atharva Vaidya, derived the lemmas,
wrote the finite checker, and prepared this report.  No independent
human peer review has occurred.
