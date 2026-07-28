# An \(H=0\) no-go for the newly-inactive-handle strategy

Date: **2026-07-28**

Status: **EXACT ORDER-12 COUNTEREXAMPLE TO AN AUXILIARY LEMMA / NOT A
FIVECDC COUNTEREXAMPLE**.

## The auxiliary claim that fails

A tempting endpoint argument is:

> After an all-bad line triangle has residual \(H=0\), make one
> root-component transition.  If that transition does not itself rescue
> the roots, it exposes a factor inactive on both roots; switching one
> of that factor's components completes a two-switch rescue.

This is false even if either endpoint of the line loop may be used and
the first transition may be any legal root-component switch.

## Literal witness

Use the cubic graph

```text
K?`@EQgLAcAo
```

whose lexicographically ordered edges are

```text
(0,4) (0,7) (0,8) (1,5) (1,7) (1,10)
(2,6) (2,8) (2,9) (3,9) (3,10) (3,11)
(4,7) (4,8) (5,9) (5,11) (6,10) (6,11).
```

The edge labels, written as bit masks for coordinates \(0,\ldots,4\),
are

```text
(3,5,6,9,12,5,5,12,9,17,9,24,9,10,24,17,12,9).
```

Equivalently these are

```text
(01,02,12,03,23,02,02,23,03,04,03,34,03,13,34,04,23,03).
```

Take roots \(r=2,s=11\), labeled \(12,34\), and lift the line sequence
\[
                            (01,12,02)
\]
at \(r\).  Its three dynamically chosen circuits are
\[
\begin{aligned}
K_1=K_3&=\{1,2,12,13\},\\
K_2&=\{0,2,4,5,6,7,12,16\}.
\end{aligned}
\]
All four line states are root-bad, and
\[
 H=K_1+K_3=0,\qquad
 Z=K_1+K_2=\{0,1,4,5,6,7,13,16\}.
\]

Now exhaust, from both the initial and final line states:

1. either root;
2. all six label-changing factor choices at that root;
3. after the resulting root-component switch, every factor inactive
   on both roots;
4. every circuit component of every such inactive factor.

No first switch is a rescue, and no second switch in item 4 is a
rescue.  Therefore “failure exposes an inactive handle” is not the
universal radius-two mechanism.

The endpoint is nevertheless rescued by two **root** transitions from
the initial state:

1. switch \(01\) on \(\{1,2,12,13\}\) at \(r\);
2. switch \(13\) on \(\{10,11,16,17\}\) at \(s\).

The resulting \(Y_{12}\)-circuit
\[
                    \{0,2,4,5,6,7,10,11,12,17\}
\]
contains both roots.  Thus this witness refutes only the proposed
inactive-handle proof hierarchy, not the broader radius-two root
transition lemma.

## Reproduction

Run

```text
python3 scratch/check_d5_hzero_inactive_handle_no_go.py
```

The checker verifies the cubic xor labeling, the exact line circuits,
root-badness, the exhaustive two-level no-go, and the displayed
two-root-transition rescue.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the auxiliary
claim, found this minimum-order failure during exhaustive testing,
extracted the literal witness, wrote the independent checker, and
drafted this note.  This is not peer review and is not a resolution of
FiveCDC.
