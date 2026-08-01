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

The July 31 update adds an unconditional single-shore parity-killing
switch for nonmatching blocker cuts of size three, five, or seven, and an
exact fixed-residual aggregate-gain characterization.  Only old even
four-cuts require parity protection.  A girth-ten cyclically-4 Tait
control shows that the resulting reduced cut-space system can still block
all partner-free directions of one blocker; the non-Tait coordination
problem remains open.

The same update gives a human-checkable 18-vertex Blanuša-snark
certificate showing that an arbitrary lexicographically optimal
representative can be blocked at both old odd residual components in all
six partner-free directions.  Two other optima for the same target class
do descend, so this rules out only the arbitrary-optimum shortcut.  It
does not rule out choosing a favourable optimum, BPR, or FiveCDC.  The
order-18 minimality statement is confined to the precisely stated simple,
cyclically-4, non-Tait host/state domain.

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
(cd scratch/bpr-second-coordinate-nontait-blocker-20260731 && ./run_all.sh)
```

The manuscript and all checking artifacts require independent human
review before submission.
