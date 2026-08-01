# Development SAT probe record

The external-state probe was run on three retained non-Tait corpora.  For
every cap vertex `z`, every proper root `r`, and every selected physical
port, a vertex-disjoint root/port pair was checked by SAT.  Every positive
model was immediately replayed from its `D5` labels, vertex XOR equations,
fixed factor, selected root path, and external inactive-port condition.
Adjacent root/port pairs were counted separately because Lemma 2.1 proves
them without SAT.

| corpus | graphs | independent SAT queries | adjacent cases | result |
|---|---:|---:|---:|---|
| cyclically 4-edge-connected non-Tait, order 18 | 2 | 2,376 | 216 | all SAT/model-checked |
| cyclically 4-edge-connected non-Tait, order 20 | 6 | 9,000 | 720 | all SAT/model-checked |
| retained strong snarks, order 34 | 7 | 32,844 | 1,428 | all SAT/model-checked |
| **total** | **15** | **44,220** | **2,364** | **no failure** |

A separate deterministic sample used seed `20260731`, selected 50 of the
7,654 retained order-40 strong snarks, and tested 20 independent interfaces
per selected graph.  All 1,000 additional SAT models passed semantic replay.
This is a sample, not a complete order-40 census.  The selected zero-based
row numbers were

```text
131,192,203,498,732,915,1105,1263,1440,1463,1866,1948,1992,2013,2070,
2138,2190,2199,2295,2629,2901,3109,3424,3638,3860,4319,4357,4425,4617,
4660,4746,4886,4957,5315,5420,5477,5639,5666,5811,6094,6350,6601,6634,
7207,7333,7448,7540,7543,7567,7649
```

Finally, the same seed selected ten independent interfaces of the
890-vertex Petersen--Foster graph.  All ten were SAT/model-checked:

```text
(z,root,port) =
(26,74,49), (294,772,453), (727,135,1100), (250,34,383),
(592,777,901), (258,478,345), (117,643,158), (495,495,754),
(162,197,252), (372,430,568).
```

The sibling
`../petersen-foster-full-typed-cap-signature-20260731/checker.py` directly
checks that this graph is non-Tait, simple, cubic, has no one- or two-edge
cut, and has girth ten.  Its
canonical reconstruction digest is
`3fe0630cb52d5a0b29a473faff02389195c7e119ea8f7a6f95f3ba9c38272282`.
Thus these ten samples lie in the local marked-girth cap geometry, although
the graph is not asserted to be an actual shore of a minimum obstruction.
For example, the first sample replays with

```sh
python3 probe.py --petersen-foster --z 26 --root 74 --port-slot 1
```

The complete retained corpora replay from this package directory with:

```sh
python3 batch_probe.py ../../search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order18.g6
python3 batch_probe.py ../../search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order20.g6
python3 batch_probe.py ../../search/strong_snarks/source/strongsnarks_34_5_cyc4.g6
```

The deterministic samples replay with:

```sh
python3 sample_probe.py --order40
python3 sample_probe.py --petersen-foster
```

Input SHA-256 values are:

```text
2660e7d5c8a351b4ed3d69f8df316e748e264a630c01328ea4bed43f96f78dfd  cyclic4-nontait-order18.g6
a65153d9dc38bebffca52b2c2ec05f194807b10ca097f50a551d5aab871244f1  cyclic4-nontait-order20.g6
2f087d5cbd1e97b1e10e7a5a064fe83d037872f838372e4d317c9d3f912fbf1f  strongsnarks_34_5_cyc4.g6
61d7b01786e983084a6255bb0afe22a503cbb8645fe186b8a962d60609224e1d  strongsnarks_40_5_cyc4.g6
```

The imported root-transition source had SHA-256
`6d935e12caaf5086d591c64cb171d1e00699d8531ba3f75d4f67555a8a05b14c`.

This is a single SAT implementation and the literal models and aggregate
terminal logs were not retained.  The counts above are therefore
**development evidence only**, reproducible by rerunning the commands, and
not an independently certified finite theorem.  None of the three complete
corpora lies in the relevant marked-girth cap domain, whose cap-order cutoff
is 56.  Only the ten explicitly labelled Petersen--Foster samples enter that
local geometry; they are not a census.

The separately retained `pf-fixed-flow-labels.b85` certificate is different:
`check_pf_fixed_flow_counterexample.py` is a standard-library semantic
checker which reconstructs the graph and verifies every flow equation and
factor component.  It proves a negative statement about one fixed flow, not
about the existential SAT queries above.  In particular, the same graph has
other flows realizing the exact aggregate signature `63`; there is no
contradiction between the fixed-flow counterexample and these positive probes.
