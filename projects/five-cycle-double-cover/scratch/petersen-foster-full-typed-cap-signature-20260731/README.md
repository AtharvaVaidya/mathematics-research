# A full typed signature on one high-girth non-Tait cap

This package freezes six literal `D5`-flow witnesses proving that one
rooted interface of the 890-vertex Petersen--Foster graph has the complete
six-state typed signature.

The graph is simple, cubic, 3-edge-connected, non-Tait, and has girth ten.
For cap vertex `z=0` and root edge `552=(363,400)`, every physical port
pair occurs in both internal and external mode.  Thus the exact typed mask
is `63`.

The six label words are embedded in `checker.py` as one compressed literal.
The checker reconstructs the graph, validates its graph properties, checks
every weight-two label and vertex XOR, reconstructs the relevant factor
component, and verifies all six typed states semantically.

Run:

```sh
./run_all.sh
```

This is one bounded positive control.  It is not a census, a universal
double-star theorem, or a resolution of FiveCDC.
