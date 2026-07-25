# Degree-125 clean-room publication replay

This directory archives the cache-free reference replay for the bounded
degree-\(125\) exclusion.  The replay began with these three accelerator
files absent:

```text
tmp/case_c_n3_generic_charts_Q.pkl
tmp/case_c_n3_special_charts_Q.pkl
tmp/case_c_n3_special_recurrence_Q.pkl
```

From the repository root, the recorded command was:

```bash
zsh -o pipefail -c \
  'publication_artifacts/degree-125-bound/cleanroom-2026-07-25/replay.sh \
  2>&1 | tee \
  publication_artifacts/degree-125-bound/cleanroom-2026-07-25/replay.log'
```

The plain-text log records Python, SymPy, Singular, and `modstd.lib`
versions; confirms that Python optimization was disabled; reconstructs the
three caches; and ends with:

```text
RESULT: CLEAN-ROOM DEGREE-125 REPLAY PASSED
```

`SOURCE_SHA256SUMS` covers the proof sources and replay driver.
`CACHE_SHA256SUMS` records the regenerated caches as diagnostics only:
the caches are ignored by Git and are not proof premises.
`ARTIFACT_SHA256SUMS` covers the archived log and the two preceding
manifests.

The replay does not compile the LaTeX manuscript because no TeX engine was
available in the reference environment.  It also does not independently
reprove or human-referee the imported GGHV preprint implications.  The
result is a computer-assisted bounded exclusion, not a proof of the plane
Jacobian conjecture.
