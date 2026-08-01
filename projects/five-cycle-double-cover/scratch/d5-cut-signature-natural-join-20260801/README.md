# D5 cut-signature natural join

This frozen development package proves and replays the exact finite-state
composition of the simultaneous external-cap condition across a 2- or
3-edge cut separating the root edge from the cap vertex.

It is a structural frontier, not a FiveCDC resolution.  In particular, it
does not claim that every realizable pair of shore relations has a good
join.

Run:

```sh
./run_all.sh
```

The Python checker uses only the standard library.  An optional complete
small-pole census additionally requires Brendan McKay's `geng`:

```sh
./run_census.sh
```

The complete parity/S5-local abstract relation frontier is standard-library
only:

```sh
./run_abstract.sh
```

See `HUMAN-PROOF.md` for a proof independent of the code, the exact bounded
scope of the census, and an honest AI-use disclosure.
