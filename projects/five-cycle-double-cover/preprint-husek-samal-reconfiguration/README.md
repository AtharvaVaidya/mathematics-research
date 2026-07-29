# H–S flow reconfiguration preprint

This is an AI-assisted research draft about an auxiliary reconfiguration
route toward the Five-Cycle Double Cover Conjecture.

It proves a human-checkable packing-to-switch lemma and records an exact
26-vertex countermodel to direct radius-one domination, plus 40- and
60-vertex controls. It does **not** resolve FiveCDC.

Build:

```sh
SOURCE_DATE_EPOCH=1785271878 tectonic main.tex
```

The finite claims are replayed from the parent project directory:

```sh
python3 scratch/verify_husek_samal_one_switch_boundary.py
python3 scratch/verify_fano_order60_flow_repair.py
```

The manuscript and all checking artifacts require independent human
review before submission.
