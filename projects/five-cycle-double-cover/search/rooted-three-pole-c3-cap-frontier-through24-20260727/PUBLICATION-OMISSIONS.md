# Publication omissions

This Git snapshot deliberately omits two large, byte-identical generated
transcripts:

| omitted path | compressed bytes | uncompressed bytes | compressed SHA-256 | uncompressed SHA-256 |
|---|---:|---:|:---|:---|
| `artifacts/cadical-transcript.tsv.gz` | 34,355,648 | 575,806,820 | `7e305bf431c35d2378f662b58a9991eff65c60f6ad0095190f51ff11d969ca44` | `130180f347c4fe3f82b94eeb16c3c990be967680ef16a02283e4962383464c75` |
| `artifacts/csp-transcript.tsv.gz` | 34,355,648 | 575,806,820 | `7e305bf431c35d2378f662b58a9991eff65c60f6ad0095190f51ff11d969ca44` | `130180f347c4fe3f82b94eeb16c3c990be967680ef16a02283e4962383464c75` |

`SHA256SUMS` retains the original compressed identities. The shard logs,
statuses, compact report, input corpora, expanded core stream, classifier
source hashes, verifier, and exact regeneration instructions remain in
the repository.

To reconstruct either transcript, compile the corresponding classifier
identified in `SOURCES.sha256`, run the six deterministic shards with
`--transcript --fail-on-violation`, concatenate shards `a` through `f`,
and compress with `gzip -n`, as described in `REPRODUCING.md`. A
reconstructed file is accepted only if both the compressed and
uncompressed hashes above match.

Without the omitted transcripts, `verify.py` cannot perform its complete
10,824,084-row semantic replay. It is nevertheless retained so a reviewer
can audit its logic and run the full check after regeneration or separate
artifact transfer. The compact Git snapshot can verify every present
frozen artifact with:

```sh
shasum -a 256 -c CHECKSUMS-PUBLISHED.sha256
shasum -a 256 -c SOURCES.sha256
python3 -m py_compile verify.py
python3 -m json.tool report.json >/dev/null
```

This omission changes storage only. It does not enlarge the finite
theorem and does not create a Five-Cycle Double Cover claim.
