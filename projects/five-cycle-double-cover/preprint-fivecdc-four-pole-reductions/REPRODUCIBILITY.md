# Reproducibility

Run these commands from the repository root:

```sh
python3 scratch/verify_petersen_four_pole_extension_theorem_20260728.py
python3 scratch/verify_heawood_four_pole_full_boundary_20260728.py
python3 scratch/verify_cube_four_pole_full_boundary_20260728.py
python3 scratch/verify_k33_four_pole_boundary_20260728.py
sha256sum -c scratch/heawood-four-pole-SHA256SUMS-20260728.txt
```

The Petersen replay must report 13 certificate rows, 120 coordinate
permutations, 100 ordered label pairs, 550 boundary checks in its ordered
enumeration, and `all_boundary_assignments_extend: true`.

The Heawood replay must report:

- graph6 `KhEGHC@AI?_P`;
- a simple, connected, bridgeless order-12 proper core of girth 6;
- 10 certificate rows;
- 120 coordinate permutations;
- 640 xor-zero boundary words; and
- `all_boundary_words_extend: true`.

The fresh Heawood JSON output must equal
`scratch/heawood-four-pole-full-boundary-result-20260728.json`.

The cube replay must report a six-vertex, seven-edge simple connected
bridgeless proper core, 10 certificate rows, and exact coverage of all 640
xor-zero words. Its checker is paired with the human minimum-order proof in
`scratch/fivecdc-minimum-full-boundary-cube-four-pole-20260728.md`.

The `K3,3` replay must report 640 admissible xor-zero words, 580 extended
words, and the exact 60-word missing orbit represented by `02 02 03 03`.
Its SHA-256 is
`1601e5eaeac1a3f059ab1ab219a05c7fec3e53de9679ac5ef54319fe14e908cf`.

Build the manuscript:

```sh
cd preprint-fivecdc-four-pole-reductions
SOURCE_DATE_EPOCH=1785271878 tectonic main.tex
```

Run the same command twice and compare `main.pdf` byte for byte. The
committed hashes are recorded in `SHA256SUMS` after the verified build.

Trust boundary: all three pole claims are positive finite certificates checked by
standard-library programs. No SAT solver or UNSAT proof trace is involved.
The `K3,3` nonextension also has a separate human proof in the manuscript.
