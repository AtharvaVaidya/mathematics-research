# Order-40 plateau audit under three distinct orders

Date: **2026-07-29**

Status: **EXACT AUXILIARY RESULT.  NOT A PROOF OR DISPROOF OF THE
FIVE-CYCLE DOUBLE COVER CONJECTURE.**

Three orders must not be conflated:

1. With \(d_{\min}\) as the only score, the first strictly lower
   \(d_{\min}\) state is exactly four reciprocal exchanges away.
2. With \(d_{\min}\) as the only numeric score but any successful
   parallel component/circuit span flag declared terminal, the first
   lower-or-successful state is exactly three exchanges away.
3. With the project's current lexicographic potential
   \[
                    \Psi=(d_{\min},S),\qquad S=\sum_i|K_i|,
   \]
   and span success terminal, the exact escape distance is **one**.
   The first exchange keeps \(d_{\min}=2\), has zero successful flags,
   and changes the odd-kernel sizes from \((26,27,25)\) to
   \((26,27,24)\).  Thus \(S\) drops from \(78\) to \(77\).

The previously reported phrase “augmented escape distance three” was
therefore correct only for order 2 and misleading if read as a claim
about the lexicographic \(\Psi\) used elsewhere in the project.

For orders 1 and 2, the complete \(d_{\min}=2\) radius-three ball
contains 958 states in layers \(1,13,108,836\).  The checker examines
1,037,514 candidate swaps and 67,392 legal exchange arcs.  No
strictly lower-\(d_{\min}\) boundary occurs before distance four.
Exactly one success-only arc leaves layer two, proving distance three
under order 2.  The explicit first exchange simultaneously proves
distance one under order 3.

Run:

```sh
python3 scratch/jaeger-plateau-augmented-radius-order40-20260729/verify.py
```

The standard-library verifier reconstructs the graph, trees, odd
kernels, seven exact component defects, all 21 span flags, and the
kernel-sum coordinate \(S\).  It reports and checks all three escape
distances separately and cross-checks every computed profile against
the independent profile routine used by the original radius-four
checker.

The 21-flag evaluation is vendored directly into `verify.py`; it no
longer imports the untracked discovery helper.  Its sole project-local
dependency is the tracked original checker
`../verify_jaeger_plateau_escape_radius4_order40.py`, whose digest is
included in `SHA256SUMS`.  A clean checkout containing this package and
that tracked file is therefore replay-closed.

Check frozen bytes:

```sh
cd scratch/jaeger-plateau-augmented-radius-order40-20260729
shasum -a 256 -c SHA256SUMS
```

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, performed the augmented
re-audit, wrote the verifier, and drafted this correction.  The result has
not received independent human peer review.
