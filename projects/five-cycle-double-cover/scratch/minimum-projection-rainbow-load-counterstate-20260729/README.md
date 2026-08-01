# Smallest balanced rainbow witness escaping the colour-load test

Date: 2026-07-29

Status: **EXACT ABSTRACT/LOCAL COUNTERSTATE / NOT A GLOBALLY MINIMUM
PROJECTION / NOT A FIVECDC RESOLUTION**.

The following proposed implication is false without an essential use of
global projection minimality:

> a balanced rainbow-odd affine-cleaning witness must violate the
> six-map colour-load inequality.

On one support 6-circuit take

```text
derivative word  112233
support word     102030
witness shore    010101
component word   010101
```

The two complement components each receive derivative multiset
`{1,2,3}`.  They are realized by two properly coloured 3-stars attached
alternately to the support circuit.  The resulting graph is finite,
simple, connected, bridgeless, cubic, and planar.

The selected derivative xor is zero, all six common
\(\operatorname{GL}(2,2)\) maps are integrable, and the witness cut is
rainbow-odd.  Nevertheless its inside and outside derivative-colour
counts are both \((1,1,1)\).  With two off-support star centres,
\[
 \max_b k_b(Y)+\max_a k_a(\overline Y)=2
       \leq 4=2(|V|-|h|).
\]
Thus the audited colour-load theorem gives no descent.

Within the subclass consisting of one support circuit and exactly two
minimally connected cubic-tree complement components, length six is
smallest.  Length four forces concentration \(2+2=4>0\), and length five
forces \(2+1=3>2\).  An exhaustive checker independently reproduces
these values.

The literal graph is Tait-colourable, so its globally minimum extendable
projection is empty.  Four of the six component-map choices also clean
the displayed projection.  Hence this is not a counterexample to the
global-minimum selection conjecture.  It proves the narrower and useful
point: cyclic-word parity, complement connectivity, minimal tree
realization, and one rainbow witness do not force the colour-load
inequality to fail.

## Replay

```sh
python3 verify.py
python3 independent_audit.py
shasum -a 256 -c SHA256SUMS
```

The universal claims used here are also proved directly in
`HUMAN-PROOF.md`.

## AI-use disclosure

OpenAI Codex agents under Atharva Vaidya's direction found the state,
proved its minimality in the stated subclass, constructed the literal
graph, and wrote both checkers.  The full witness is displayed for
human checking.  No literature-wide novelty or priority claim is made.
