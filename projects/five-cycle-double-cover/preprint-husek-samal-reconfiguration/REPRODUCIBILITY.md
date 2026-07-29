# Reproducibility

Run from `projects/five-cycle-double-cover`:

```sh
sha256sum \
  scratch/verify_husek_samal_one_switch_boundary.py \
  scratch/verify_fano_order60_flow_repair.py \
  scratch/husek-samal-one-switch-countermodel-order26.txt \
  scratch/husek-samal-one-switch-countermodel-order40.txt

python3 scratch/verify_husek_samal_one_switch_boundary.py
python3 scratch/verify_fano_order60_flow_repair.py
```

Frozen hashes used by the manuscript:

```text
ac51aaf266178eb764fcada85b25e17dc2c18c129413abb51a2b309513ea415d  scratch/verify_husek_samal_one_switch_boundary.py
09f9bdc797948b49cf6b7a3080160e07111dad718f0e07ae00a2a9c0958b9a6e  scratch/verify_fano_order60_flow_repair.py
1c8c0b5959fb7e8f7333b44860a519e1351f366e0a78ab5be8a061287f9dfd46  scratch/husek-samal-one-switch-countermodel-order26.txt
6e1dc5fb3b290fe8364559844ed419ee6dda1ec974b2ad3aebfd21442c8fe6aa  scratch/husek-samal-one-switch-countermodel-order40.txt
```

Build the paper:

```sh
cd preprint-husek-samal-reconfiguration
SOURCE_DATE_EPOCH=1785271878 tectonic main.tex
```

The checkers use only the Python standard library. “Independent” means
independent of the discovery implementation; both were AI-assisted and
still require independent human reimplementation.
