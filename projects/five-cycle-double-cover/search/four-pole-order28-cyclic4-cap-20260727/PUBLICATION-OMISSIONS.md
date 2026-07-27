# Publication archive omissions

Date: **2026-07-27**.

This Git publication includes the canonical cap source, theorem and
reproduction notes, complete shard logs and statuses, compact reports,
package verifier, independent checker sources, and the original full
checksum ledgers.

Two generated streams are deliberately omitted from ordinary Git:

| artifact | compressed bytes | compressed SHA-256 | uncompressed SHA-256 |
|---|---:|---|---|
| `artifacts/cyclic4-nontait-order28-poles.g6.gz` | 40,210,290 | `eaaf47ce074008b1b7da9ca438a38b36e4a838af400989e9189519034643b7b4` | `f42168e2786bdee409304e9e7b167ae0a0e250c78e7c2413e55ee56f5627a839` |
| `artifacts/cadical-two-orbit-witness.tsv.gz` | 363,463,166 | `169a574788259d92c58bbee35898d4af4d51091b860e3bdd9fdb4dcd4a3a06b6` | `658374b00418fa626da704670689f4dfad25cf740121509a725da4158491ef7d` |

The second file exceeds GitHub's ordinary per-file limit.  The first is a
deterministically regenerated intermediate consumed by the second
checker, so both streams are kept out of the normal repository rather
than publishing an incomplete certificate payload.

`SHA256SUMS` is intentionally retained unchanged and therefore names the
two absent files.  `REPRODUCING.md` gives the exact commands for
regenerating and authenticating both streams.  Before publication, the
full local package passed `SHA256SUMS` and `SOURCES.sha256`; the
standard-library Python verifier and the separately written C++/zlib
checker had both replayed all 9,725,709 rows and 19,451,418 displayed
labellings.  The C++ replay was rerun once more against the frozen local
streams and reproduced `independent-fast-replay.json` byte for byte.
The paths inside `SOURCES.sha256` are intentionally relative to that
original laboratory layout, not to this nested publication copy; the
ledger preserves the source identities rather than pretending that the
omitted generator binary is present in Git.

The omitted streams contain positive witnesses, not an UNSAT certificate.
The finite theorem and its scoped order-30 corollary do not resolve the
Five-Cycle Double Cover Conjecture.
