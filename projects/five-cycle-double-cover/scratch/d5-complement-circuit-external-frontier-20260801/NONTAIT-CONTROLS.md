# Frozen non-Tait controls

The same C++ auditor was run on the retained cyclically four-connected
non-Tait controls at orders 18 and 20.  These are corpus checks, not complete
all-graph censuses at those orders.

Inputs:

```text
2660e7d5c8a351b4ed3d69f8df316e748e264a630c01328ea4bed43f96f78dfd  cyclic4-nontait-order18.g6
a65153d9dc38bebffca52b2c2ec05f194807b10ca097f50a551d5aab871244f1  cyclic4-nontait-order20.g6
```

Results:

```text
ORDER18 graphs=2 flows_mod_s5=18790 kempe_orbits_mod_s5=10 orbit_interfaces=4320 bad_orbit_interfaces=0 PASS
ORDER20 graphs=6 flows_mod_s5=221680 kempe_orbits_mod_s5=85 orbit_interfaces=45900 bad_orbit_interfaces=0 PASS
```

Thus every ordinary Kempe orbit in these eight frozen non-Tait graphs already
contains a simultaneous external flow for every rooted interface.  No
complement move is needed on this corpus.  This does not prove the universal
proper-cap statement.
