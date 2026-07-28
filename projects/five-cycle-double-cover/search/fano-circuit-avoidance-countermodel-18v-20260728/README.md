# Fano prescribed-circuit avoidance countermodel

Status: **exact countermodel to one proof step; not a FiveCDC
counterexample**.

This package freezes the smallest retained simple cyclically
4-edge-connected non-Tait countermodel to:

> three equal-\(s\) edges, \(s\ne t\), always lie on a circuit avoiding
> the flow-value matching \(M_t\).

The graph is the first Blanuša snark.  For the displayed merge-bad Oum
flow, \(G-M_6\) is connected and bridgeless, yet three value-3 edges have
no common circuit because of a two-vertex separator.  A disconnected
binary cycle through exactly that prescribed triple repairs every
compatible \(K_6\) cover to a five-colourable cover.

The same flow has a different connected-circuit repair.  Thus the package
does not refute the broader existential one-circuit repair conjecture.

Files:

- `canonical.g6`: canonical graph encoding;
- `HUMAN-PROOF.md`: checkable mathematical proof and exact scope;
- `checker.py`: standard-library independent finite checker;
- `report.json`: complete checker output; and
- `SHA256SUMS`: frozen artifact hashes.

Replay:

```sh
python3 checker.py
```

The replay checks graph premises, non-Taitness, the flow, all four initial
and repaired Oum potentials, every elementary circuit, the separator
certificate, the disconnected repair, the separate connected repair, the
source hashes, and all 28,560 nowhere-zero flows on the Petersen graph.

## AI-use disclosure

OpenAI Codex, under human direction, developed the search, proof, checker,
and package.  The result is deliberately stated as a countermodel to a
specific proof strategy, not as a resolution of FiveCDC.
