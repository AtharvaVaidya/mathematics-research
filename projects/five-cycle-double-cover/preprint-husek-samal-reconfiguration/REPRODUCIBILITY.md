# Reproducibility

Run from `projects/five-cycle-double-cover`:

```sh
sha256sum \
  scratch/verify_husek_samal_packable_one_switch_countermodel.py \
  scratch/verify_husek_samal_one_switch_boundary.py \
  scratch/verify_fano_order60_flow_repair.py \
  scratch/husek-samal-packable-one-switch-countermodel-order26.txt \
  scratch/husek-samal-one-switch-countermodel-order40.txt \
  scratch/jaeger-order40-augmented-radius-two-counterexample-20260729/verify.py \
  scratch/jaeger-order40-augmented-radius-two-counterexample-20260729/verification-output.json \
  scratch/jaeger-order40-augmented-radius-two-counterexample-20260729/canonical-graph6.txt \
  scratch/flow-rank-two-legal-order-20260729/HUMAN-PROOF.md \
  scratch/flow-rank-two-legal-order-20260729/WITNESSES.json \
  scratch/flow-rank-two-legal-order-20260729/verify.py \
  scratch/flow-rank-two-legal-order-20260729/verification-output.txt \
  scratch/petersen-foster-girth10-nontait-20260729/reconfiguration-certificate.json \
  scratch/petersen-foster-girth10-nontait-20260729/verify_reconfiguration.py \
  scratch/petersen-foster-girth10-nontait-20260729/reconfiguration-output.json \
  scratch/petersen-foster-girth10-nontait-20260729/audit-blind-20260729/independent_check.py \
  scratch/petersen-foster-girth10-nontait-20260729/audit-blind-20260729/independent-output.json \
  scratch/rank3-fourmove-normal-form-20260729/HUMAN-PROOF.md \
  scratch/rank3-fourmove-normal-form-20260729/verify.py \
  scratch/rank3-fourmove-normal-form-20260729/verification-output.json

python3 scratch/verify_husek_samal_packable_one_switch_countermodel.py
python3 scratch/verify_husek_samal_one_switch_boundary.py
python3 scratch/verify_fano_order60_flow_repair.py
python3 scratch/jaeger-order40-augmented-radius-two-counterexample-20260729/verify.py
python3 scratch/flow-rank-two-legal-order-20260729/verify.py
python3 scratch/petersen-foster-girth10-nontait-20260729/verify_reconfiguration.py
python3 scratch/petersen-foster-girth10-nontait-20260729/audit-blind-20260729/independent_check.py
python3 scratch/rank3-fourmove-normal-form-20260729/verify.py
```

Frozen hashes used by the manuscript are regenerated after every revision
and recorded in `SHA256SUMS`.

Build the paper:

```sh
cd preprint-husek-samal-reconfiguration
SOURCE_DATE_EPOCH=1785271878 tectonic main.tex
```

The checkers use only the Python standard library. “Independent” means
independent of the discovery implementation; both were AI-assisted and
still require independent human reimplementation.
