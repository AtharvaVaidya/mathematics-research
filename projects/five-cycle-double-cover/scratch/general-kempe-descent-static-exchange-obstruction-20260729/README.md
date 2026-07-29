# Static exchange is not a one-round Kempe descent theorem

Date: 2026-07-29

Status: **RIGOROUS PROOF-METHOD OBSTRUCTION / NOT A GLOBALLY MINIMUM
PROJECTION / NOT A FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## Result

This package turns the 42-vertex size-sixteen one-round counterstate into
a connected simple cubic bridgeless graph on 230 vertices.  Every
non-support edge is replaced by one coloured \(K_4-e\) two-pole.  The
replacement has distance four between the old attachment endpoints,
counting both attachment edges, and preserves every complement two-colour
boundary pairing.  Its internal degree-two terminals are distance two
apart.

The construction has a general human-proof consequence.  Given any
coloured cubic boundary realization whose every support circuit uses all
four affine colours, replace each non-support edge by a long enough chain
of these two-poles.  The support, component partition, and all
two-colour boundary pairings are unchanged, while all four full
binary-cycle exchange inequalities become true.  Taking the distance
between old attachment endpoints at least the total support size suffices.
Therefore the static exchange
inequalities impose no additional universal constraint on the local
boundary/Kempe model beyond the already known four-colours-per-support-
circuit condition.  Their force in a genuine minimum proof must be
dynamic: they apply again after every neutral recolouring.

For the displayed extension \(f=(h,s)\):

- \(h\) is the union of two 8-circuits;
- for every affine class \(M_c=\{e\in h:s(e)=c\}\), \(h\) is a
  minimum-cardinality binary cycle containing \(M_c\);
- equivalently, **every** binary cycle \(C\) of the 230-vertex graph
  disjoint from \(M_c\) satisfies
  \[
  |C\cap h|\leq |C-h|;
  \]
- every one of the 97 nonempty charge-restoring fixed-colour path
  multiswitches still fails both direct cleaning and circuit deletion.

The four full exchange inequalities are checked in two different ways.
The primary checker exhausts the \(2^{22}\) binary cycles of the base
graph with effective complement weight four.  The independent checker
solves four shortest \(T\)-join problems directly in the inflated graph:

```text
affine class size       6   5   3   2
shortest T-join        10  11  13  14
containing cycle       16  16  16  16
```

Thus the obstruction accounts for the complete binary cycle space, not
only the component partition or its cut charges.

The state is not dynamically trapped.  There is a literal two-round
escape:

1. switch the \(1,2\)-paths with endpoints \(1\!-\!10\) and
   \(4\!-\!15\);
2. recompute the bichromatic paths and switch the \(1,3\)-path
   \(5\!-\!6\).

The resulting derivative is

```text
32112311|21213131
```

and zero-start integration gives

```text
31013010|23103210.
```

Colour 2 is absent from the first 8-circuit, so translating that circuit
by 2 and deleting it gives an extendable projection of size eight.

This explains the exact logical boundary.  Global minimality makes the
exchange theorem apply again after every support-neutral recolouring.
Checking the four inequalities only for the initial affine classes is
not enough.  A successful general proof must use this **dynamic exchange
closure**, or a stronger invariant that implies it.

The complete multi-round boundary-profile graph for this particular
multipole can also be enumerated.  Its large component has 252 proper
three-edge-colourings with 252 distinct boundary profiles.  Combining
these with the four small two-poles gives 5,094 circuit-integrable
profile states after literal internal colourings with the same boundary
data are collapsed.  Their charge-preserving boundary Kempe graph is
connected, with 64,497 edges, and 3,294 profiles directly clean or delete.
The displayed profile has distance exactly two from that goal set.  This
is finite positive evidence for multi-round descent in this realization,
not a universal theorem.

The graph is also Tait-colourable, so its actual minimum projection is
zero.  It is not a counterexample to the minimum-projection conjecture or
to FiveCDC.

## Files and replay

- `HUMAN-PROOF.md`: algebraic model, inflation lemma, exact theorem, and
  the hand-checkable two-round descent.
- `base-edges.tsv`: literal 42-vertex coloured base graph.
- `verify.py`: primary cycle-space, graph, one-round, and two-round
  verifier.
- `independent_audit.py`: independently written shortest-\(T\)-join
  verifier in the 230-vertex graph.  It independently checks the four
  exchange inequalities, but shares `base-edges.tsv` and the gadget
  construction and does not independently audit the other claims.
- `kempe_state_graph.py`: complete multi-round boundary reconfiguration
  census for this particular complement multipole.
- `verification-output.txt` and `independent-output.txt`: frozen output.
- `kempe-state-graph-output.txt`: frozen reconfiguration-census output.
- `SHA256SUMS`: integrity ledger.

Replay from this directory:

```sh
python3 verify.py
python3 independent_audit.py
python3 kempe_state_graph.py
shasum -a 256 -c SHA256SUMS
```

Both programs use only the Python standard library.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, found the edge-inflation
construction, proved the transfer lemma, found the two-round escape, and
wrote this package.  The claims are finite and reproducible, but they
have not received independent human peer review.
