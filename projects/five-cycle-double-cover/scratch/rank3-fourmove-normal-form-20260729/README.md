# Rank-three four-move normal form and exact audit

This package proves a general affine-incidence criterion for deciding whether
an ordered spanning four-tuple of fixed vectors can reconfigure one
nowhere-zero \(\mathbb F_2^3\)-flow into another while every move support is
Eulerian and every intermediate flow remains nowhere-zero.

It then independently checks all 1,848 ordered rank-three four-tuples for the
890-vertex Petersen--Foster certificate:

- 1,176 are blocked on at least one edge;
- 672 are locally legal but fail a global component-parity condition;
- none is a legal four-move path.

The result concerns arbitrary Eulerian supports, which may be disconnected.
It does not concern single-connected-cycle adjacency and it does not resolve
the Five-Cycle Double Cover Conjecture.

Files:

- `HUMAN-PROOF.md`: theorem, proof, loop/parallel-edge convention, scope;
- `verify.py`: independent standard-library reconstruction and exhaustive
  audit;
- `verification-output.json`: frozen successful output;
- `SHA256SUMS`: hashes for this package and its two source inputs.

Run:

```sh
python3 verify.py
shasum -a 256 -c SHA256SUMS
```

Expected runtime is about five seconds on a laptop.

AI disclosure: this package was written by an OpenAI Codex agent.  It has not
yet received independent human peer review.
