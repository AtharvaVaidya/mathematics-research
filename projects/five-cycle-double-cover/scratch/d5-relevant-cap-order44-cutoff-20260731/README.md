# Relevant typed caps start at order 44

This package proves a structural cutoff for the typed-cap route in the
minimum-counterexample edge-elimination setting.

If `G` is the hypothetical simple cyclically 4-edge-connected cubic
minimum FiveCDC counterexample of girth at least ten, `H = G div e` is the
usual two-root reduction, and a nontrivial three-edge cut of `H` is capped
on its two shores, then:

- the cut avoids both artificial roots and separates them;
- each cap is simple and 3-edge-connected;
- deleting the cap vertex leaves a connected bridgeless graph of girth at
  least nine in which every 9-cycle contains the shore root; and
- each cap has at least **44 vertices**.

The order bound has a self-contained nonbacktracking-walk proof.  It does
not use SAT, a graph census, or the irregular Moore bound as a black box.
It shows in particular that the existing typed-cap census through order 14
does not meet the marked-girth domain forced by a minimum obstruction.

The package also proves a modest one-sided replacement for the double-star
condition: a Tait-colourable cap has external-mode states covering all
three ports.  Hence two Tait-colourable caps glue root-good.  This does not
settle the case in which at least one cap is non-Tait.

Run the exact arithmetic and finite case-table replay with:

```sh
./run_all.sh
```

Read `HUMAN-PROOF.md` for the complete statement, proof, and precise open
boundary.  This package does not prove FiveCDC or the universal
double-star premise.
