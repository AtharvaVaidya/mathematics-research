# Petersen adjacent-deletion four-cut localization does not close

Date: **2026-07-28**.

Status: **EXACT LOCAL NO-GO / EXHAUSTIVE DIRECT-GLUING NO-GO /
CENTRAL-CORE PROBE NEGATIVE / NOT A FIVE-CDC RESULT**.

## Proposed route

Start with a Petersen graph \(P\), a nowhere-zero
\(\mathbb F_2^3\)-flow \(f\), and a functional \(\mu\) for which
\[
 F_\mu=\{e:\mu(f(e))=0\}
\]
is a perfect matching.  Delete the endpoints \(u,v\) of an edge \(uv\),
leaving an eight-vertex four-pole.  The hope was that cleanability on a
larger graph would localize to cleanability on the capped Petersen graph,
as it does for the three-edge leaf sums in
`docs/fano-all-seven-petersen-sum-obstruction.md`.

It does not.  There are two cases, and each has a different escape.

## Case 1: \(uv\in F_\mu\)

The other four matching edges are internal to the four-pole.  If two
global binary cycles \(p,q\) cover those four edges and give their four
components defect zero, then the sum-of-defects identity does recover
defect zero for the deleted component after capping.

But it does **not** recover coverage of \(uv\).

Indeed, if the reconstructed cap edge were covered by \(p\) or \(q\),
the capped pair would clean all five matching components of the Petersen
graph, contradicting the Petersen matching obstruction.  Hence every
locally admissible pair necessarily leaves the reconstructed \(uv\)
uncovered.

The literal finite audit finds:

- 64 Petersen binary cycles;
- 48 ordered pairs satisfying coverage and zero defect on the four
  surviving matching components;
- 16 distinct boundary-word pairs; and
- zero of the 48 pairs covering the reconstructed edge \(uv\).

Thus total defect parity supplies the missing defect equation but not the
missing coverage clause.

## Case 2: \(uv\notin F_\mu\)

Now one matching edge at \(u\) and one at \(v\) becomes a boundary edge,
while the other three matching edges remain internal.  Coverage does
extend across the four-cut, so the previous gap disappears.

However, defect localization fails.  If the three internal matching
components have defect zero, the sum-of-defects identity says only that
the two boundary matching-component defects are equal.  They cannot both
be zero, because that would again give a clean Petersen pair.  Therefore
they are necessarily
\[
                         (1,1).
\]

This is not merely a parity possibility.  Exact enumeration finds 72
ordered cycle pairs, all 72 with boundary defect word \(11\).  Their 36
distinct boundary-word pairs are exactly all pairs of even four-bit words
which cover the two boundary matching edges.  In particular the local
Petersen block imposes no additional boundary restriction capable of
forbidding cancellation in a central connector.

## Exhaustive no-go for direct four-block gluing

The simplest cyclic-four construction pairs the sixteen ports of four
adjacent-deletion Petersen four-poles directly, always joining equal flow
values.  For the first case \(uv\in F_\mu\), an exhaustive audit gives:

- 28,560 labelled nowhere-zero \(\mathbb F_2^3\)-flows on Petersen;
- 70 distinct `(bad-functionals, port-value-multiset)` deletion
  signatures;
- 1,050 four-signature multisets whose bad-functional sets cover all
  seven nonzero functionals;
- 945 of those with even total multiplicity of every port value; but
- zero in which every port value can be paired between distinct blocks.

Therefore four directly joined Petersen four-poles cannot realize the
proposed all-seven obstruction with a compatible flow.

## Central eight-vertex connector probe

We also tested the corrected \(uv\notin F_\mu\) case with an eight-vertex
cubic central connector.  Each central vertex receives two leaf ports;
their XOR labels its third edge, and equal-XOR third edges are paired.
The retained deterministic probe generated nine simple cyclically
four-edge-connected order-40 graphs whose four local bad-functional rows
cover all seven functionals.  Exact CNF cleanability checks found **zero
bad projections on every one of the nine graphs**.

This central-core probe is not an exhaustive theorem about all central
cores.  Its role is diagnostic: the corrected blocks export the \(11\)
defect state, and the smallest natural connector cancels it rather than
turning it into an obstruction.

## Reproduction

Run:

```sh
python3 scratch/verify_petersen_four_cut_no_go.py
python3 scratch/search_petersen_fourpole_allseven.py \
  --central-core --deleted-outside-factor --trials 10 \
  --output scratch/petersen-fourpole-central-allseven-outside-probe.json
```

The first command is the independent standard-library/NetworkX finite
audit.  The second constructs the order-40 central-core instances and
uses the existing exact two-cycle-cleanability CNF semantics.

## Conclusion

The adjacent-deletion four-pole does not inherit the three-sum
leaf-localization lemma:

- deleting a matching edge loses a coverage clause;
- deleting a nonmatching edge exports two unit defects; and
- four direct blocks cannot even carry a compatible all-seven flow.

Accordingly this particular Petersen four-cut route is closed.  This
does not prove that a cyclically four-edge-connected all-seven fixed-flow
obstruction cannot exist by some other construction, and it says nothing
directly about the five-cycle double cover conjecture.

## AI-use disclosure

OpenAI Codex agents, under human direction, proposed and tested the
four-cut localization, found the missing coverage clause, derived the
corrected two-defect state, wrote the exhaustive checker and central-core
search, and drafted this note.  All finite claims above are reproducible;
this is not independent human peer review.
