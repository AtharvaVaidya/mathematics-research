# Independent audit package

This directory independently audits
`../d5-tait-prescribed-circuit-lift-20260731`.

Result: **PASS with explicit loop, circuit, root-distinctness, and
multigraph boundaries.**  See `AUDIT.md` for the complete human-checkable
argument.

Run:

```sh
./run_all.sh
```

The checker uses only the Python standard library and represents parallel
edges by distinct edge IDs.
