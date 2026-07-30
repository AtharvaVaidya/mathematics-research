# Blind implementation audit

`independent_check.py` is a fresh standard-library implementation of the
Petersen--Foster distance-five audit.  It imports none of the discovery or
source-checker code.  It independently reconstructs the graph, frozen flows,
rank-three lower-bound enumeration, legal five-move path, and the decomposition
of its five Eulerian supports into 63 simple cycles.

Run from the parent directory:

```sh
python3 audit-blind-20260729/independent_check.py \
  > reproduced-independent-output.json
diff -u audit-blind-20260729/independent-output.json \
  reproduced-independent-output.json
```

This is implementation independence only.  The audit was also produced by an
AI agent and is not a substitute for human reimplementation or peer review.
