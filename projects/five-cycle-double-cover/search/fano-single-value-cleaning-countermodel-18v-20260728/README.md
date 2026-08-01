# Fixed-line single-value cleaning: order-18 countermodel

This frozen package refutes the exact sufficient lemma

```text
Oum-hard(phi) =>
there exist mu != 0 and 0 != t in ker(mu) with r_mu in image(tau_t).
```

It does **not** refute FiveCDC.  An outside-line switch on a 5-circuit
repairs the retained flow and yields the explicit ordinary five-cycle
double cover in `construction.json`.

Files:

- `HUMAN-PROOF.md`: definitions, the sufficient implication, countermodel
  proof, outside-line repair, and precise minimality scope;
- `construction.json`: canonical graph, ordered flow, Oum data, repair,
  and explicit FiveCDC;
- `report.json`: all 21 image ranks, bases, and dual separators;
- `small-snark-census.json`: complete normalized-flow census through the
  two order-18 Blanuša snarks;
- `semantic_checker.py`: independent standard-library checker;
- `SHA256SUMS`: hashes of the frozen artifacts.

Run:

```bash
python3 semantic_checker.py
sha256sum -c SHA256SUMS
```

Expected semantic output ends in:

```text
independent semantic checker: PASS
```
