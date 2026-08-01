# Typed-cap external coverage inside Kempe orbits

This package gives human-checkable algebraic reductions, three exact orbit
delimiters, and one surviving finite frontier:

- `D5` flows using at most four coordinate names are exactly the Tait case;
- the four external factors through a selected cap port project exactly to
  the four coordinates of the nonzero even-weight code
  `E4 ~= F_2^3`;
- a Kempe switch adds one constant projected value along one factor circuit
  and toggles exactly the factors meeting its coordinate pair oddly; and
- through order 14, every proper interface has some `D5` flow, across all
  orbits, which simultaneously externally covers all three physical ports.

The orbit hierarchy fails in three steps: double stars fail in an
eight-vertex Wagner orbit; existence of one simultaneous covering flow in
every orbit fails at order 12; and even aggregate external coverage inside
every orbit fails at order 14.  Literal flows and exact semantic replays are
included.  The order-12 and order-14 counterexamples are Tait/low-girth and
do not enter the relevant non-Tait marked-girth branch.

Run:

```sh
./run_all.sh
```

Requirements are Python 3 and nauty `geng` at `/opt/homebrew/bin/geng`, or
set `GENG`.  The complete through-order-12 replay takes about one minute on
the development machine.

The optional complete order-14 C++ run takes a few minutes:

```sh
./run_order14.sh
```

The all-flow statement remains a finite observation, not a universal
external-coverage theorem, and this package does not resolve FiveCDC.  See
`HUMAN-PROOF.md` for the exact scope and AI-use disclosure.
