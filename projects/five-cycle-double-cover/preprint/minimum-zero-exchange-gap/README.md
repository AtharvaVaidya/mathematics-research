# Minimum-zero exchange-gap preprint

Status: **draft secondary result; not a resolution of FiveCDC**.

`main.tex` gives a human-checkable proof that identical rooted two-edge
sums exactly double three parameters:

- minimum number `r_f` of zeros in an `F_2^2`-flow;
- minimum number `r_M` when the exact zero set must be a matching; and
- minimum certificate matching size `eta` when that matching must also be
  the intersection of two binary cycles.

Applied to the certified 130-vertex base graph, this produces an infinite
family with

```text
r_f(G_n) = r_M(G_n) = 5 * 2^n
eta(G_n)             = 6 * 2^n.
```

The additive gap is therefore unbounded. Every graph in the family has a
standard five-cycle double cover.

## Replay

From the project root:

```sh
cd search/minimum-zero-exchange-countermodel-130v-20260727
shasum -a 256 -c SHA256SUMS
python3 verify.py

cd ../../preprint/minimum-zero-exchange-gap
python3 audit_two_sum.py
```

The first verifier checks the finite base package, regenerates both CNFs,
and checks both LRATs with `lrat-check` and CakeML `cake_lpr`. The second
script is an independent positive-witness implementation. It checks every
one of the 195 possible choices of root edge for the first two-copy sum.

## Before submission

- Obtain independent human verification of the mathematical proof.
- Have an independent person replay the fixed certificate package.
- Have a domain specialist review the documented related-work comparison
  and apparent-novelty boundary in Section 7.
- Decide authorship and venue-specific AI-disclosure language.

The current draft intentionally makes no novelty or priority claim.
