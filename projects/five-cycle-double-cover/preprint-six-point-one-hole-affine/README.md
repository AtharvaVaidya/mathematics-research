# Six-point one-hole affine preprint

Status: **research draft for independent human verification**.

This standalone manuscript proves a fixed-flow affine normal form for a
six-coordinate cover with one unused pair, gives the complete local orbit
table, and records two independently replayed finite separations.  It does
not prove or refute the standard Five-Cycle Double Cover Conjecture, which
remains open.  It makes no claim about the orientable variant.

The theorem and its human proof are in `main.tex`.  The finite audit package
is in:

```text
../scratch/six-point-one-hole-affine-20260729/
```

From the project root, rerun the four exact checks with:

```sh
python3 scratch/six-point-one-hole-affine-20260729/audit_six_point_one_hole_affine.py
node scratch/six-point-one-hole-affine-20260729/verify_six_point_one_hole_affine.mjs
python3 scratch/six-point-one-hole-affine-20260729/audit_all_flows_12v.py
node scratch/six-point-one-hole-affine-20260729/verify_all_flows_12v.mjs
```

Build deterministically from this directory:

```sh
SOURCE_DATE_EPOCH=1785283200 tectonic main.tex
```

The PDF was rendered page by page with Poppler and visually inspected.
The source contains a prominent disclosure of the material contribution
from OpenAI Codex agents.  Implementation independence is not independent
human review; specialist proof and prior-art review remain necessary before
submission.

In particular, any novelty assessment must account for the earlier
projective, affine, and abelian colouring framework of Král', Máčajová,
Pangrác, Raspaud, Sereni, and Škoviera (European Journal of Combinatorics
30 (2009), 53-69, DOI 10.1016/j.ejc.2007.11.029), as well as the 2026
eight-coordinate and five-set/component-parity treatment of Hušek and
Šámal.  This draft claims only a provisional, narrower contribution: the
fixed-flow six-support/missing-duad affine normal form, its local orbit
tables, and the strict fixed-flow separation.
