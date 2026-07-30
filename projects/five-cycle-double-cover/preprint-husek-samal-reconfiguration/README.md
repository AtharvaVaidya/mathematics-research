# H–S flow reconfiguration preprint

This is an AI-assisted research draft about an auxiliary reconfiguration
route toward the Five-Cycle Double Cover Conjecture.

It proves a human-checkable packing-to-switch lemma and an exact
difference-rank normal form for fixed-value Eulerian moves.  The latter
includes a smallest \(K_{3,3}\) rank-two legal-order obstruction and a
smallest cube bad-to-good shared-coordinate obstruction.  It also proves
an exact rank-three four-move criterion and gives a certified pair with
zero-allowing distance three but legal Eulerian-support distance five.
For the literature's connected-cycle adjacency, the same pair has only
the certified bounds \(5\le d\le63\).  The manuscript
also records an exact 26-vertex countermodel showing that a packable value
class can still require two circuit switches, 40- and 60-vertex controls,
and an exact distance-three obstruction to a separate radius-two
Jaeger-star reciprocal-exchange claim. It does **not** resolve FiveCDC.

Build:

```sh
SOURCE_DATE_EPOCH=1785271878 tectonic main.tex
```

The finite claims are replayed from the parent project directory:

```sh
python3 scratch/verify_husek_samal_packable_one_switch_countermodel.py
python3 scratch/verify_husek_samal_one_switch_boundary.py
python3 scratch/verify_fano_order60_flow_repair.py
python3 scratch/jaeger-order40-augmented-radius-two-counterexample-20260729/verify.py
python3 scratch/flow-rank-two-legal-order-20260729/verify.py
python3 scratch/petersen-foster-girth10-nontait-20260729/verify_reconfiguration.py
python3 scratch/rank3-fourmove-normal-form-20260729/verify.py
```

The manuscript and all checking artifacts require independent human
review before submission.
