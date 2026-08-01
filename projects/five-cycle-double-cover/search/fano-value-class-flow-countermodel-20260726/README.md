# Fano value-class flow countermodel

Status: **exact countermodel to a proposed proof lemma / not a
counterexample to five-CDC**.

The connected simple bridgeless cubic graph `ICOef?kF?` has the frozen
nowhere-zero \(\mathbb F_2^3\)-flow in `instance.json`.  Every one of its
seven nonzero value classes is a matching, but none of the seven complement
grafts packs two edge-disjoint \(T\)-joins.

Run the independent direct checker:

```sh
python3 independent_checker.py
```

It checks the graph6 record, cubicity, connectivity, every single-edge
deletion, flow conservation, all seven matching conditions, and every
subset of each complement.  It also validates a three-edge-colouring and
the resulting standard five-cycle double cover.

The producer search is:

```sh
python3 ../../tools/fano_value_class_tjoin_audit.py \
  --max-order 10 \
  --output report.json
```

It exhausts all nowhere-zero flows in the earlier canonical graphs and
stops at this first witness.  `HUMAN-PROOF.md` gives a checkable
edge-incidence proof and the complete forced-cycle table.

OpenAI Codex agents performed the search and drafted the artifact under
human direction.  Independent human verification is required before any
public claim.
