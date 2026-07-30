# The four-terminal matching game on all support-16 residuals

Date: 2026-07-29

Status: **SIX OF EIGHT HARD ABSTRACT RESIDUALS REDUCED BY A
MATCHING-ROBUST KEMPE STRATEGY / TWO LITERAL GRAPH-REALIZABLE ONE-ROUND
OBSTRUCTIONS / NOT A FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## 1. Fixed boundary state

Put \(K=\mathbb F_2^2=\{0,1,2,3\}\), with addition written as xor.  The
two support circuits have low words
\[
 c=\texttt{01010123|01012302}
\]
and boundary derivatives
\[
 d=\texttt{31111131|21113132}.                         \tag{1}
\]
The exact unrestricted fixed-word census leaves the following eight
component partitions:

```text
0001234000314200
0001234003144422
0012344041300022
0012344044130244
0012344400314200
0012344403144422
0123444441300022
0123444444130244
```

For each partition, normalizing the first component map to the identity
leaves \(6^4=1296\) map tuples.  Exactly 320 are circuit-integrable and
none cleans or deletes.  These are abstract boundary residuals for the
direct component-map search, not FiveCDC counterexamples.

## 2. One-colour-pair matching game

Fix one unordered pair of nonzero low colours
\[
                         P=\{x,y\},\qquad \Delta=x+y.
\]
In a complement component \(W\), retain its \(x,y\)-coloured edges.  Its
odd boundary vertices are exactly
\[
                     T_W(P)=\{i\in\partial W:d_i\in P\}. \tag{2}
\]
The path components pair these terminals.  Write the induced perfect
matching as \(M_W(P)\).

For one play of the game:

1. one colour pair \(P\) is fixed;
2. Nature supplies one perfect matching \(M_W(P)\) for every component;
3. the strategy may observe these matchings and switch any nonempty
   subset of their displayed paths;
4. all selected paths use the same pair \(P\);
5. the resulting two support-circuit charges must both be zero;
6. after the switches, all component maps and all relative circuit
   translations may be chosen to clean or delete.

Switching a path adds \(\Delta\) at both endpoints.  A same-circuit path
preserves both circuit charges.  A cross-circuit path changes both
charges by \(\Delta\).  Therefore a path subset is legal exactly when it
contains an even number of cross-circuit paths.              \(\tag{3}\)

The primary, matching-observed quantifiers are
\[
 \boxed{\quad
 \exists P\ \forall (M_W(P))_W\ \exists
 S\subseteq\mathop{\dot\bigcup}_W M_W(P):
 S\ne\varnothing,\ S\text{ satisfies (3), and }S\text{ cleans or deletes}.
 \quad}                                                     \tag{4}
\]
Only matchings for this one \(P\) occur in (4).  No matching belonging
to a second colour pair is silently combined with it.

The verifier enumerates **every abstract perfect matching** of every
terminal set in (2).  This may include matchings not supplied by a
particular graph realization, but that only strengthens a successful
universal certificate.

## 3. Six universal matching-observed reductions

For six residuals, the fixed pair \(P=\{1,3\}\) satisfies (4).  The
complete results are:

| profile | partitions | \(P=12\): rescued/all | \(P=13\): rescued/all | \(P=23\): rescued/all |
|---|---|---:|---:|---:|
| \(5+4+3+2+2\) | `0001234003144422`, `0123444441300022` | \(2/3\) | **\(9/9\)** | \(0/1\) |
| \(6+3+3+2+2\) | `0012344041300022`, `0012344403144422` | \(2/3\) | **\(15/15\)** | \(0/1\) |
| \(6+4+2+2+2\) | `0012344044130244`, `0012344400314200` | \(2/3\) | **\(9/9\)** | \(2/3\) |

Here “all” is the product of the perfect-matching counts over all five
complement components.  For every one of the 66 bold-column matching
rows, `matching-game-certificate.json` gives:

- the full matching tuple;
- a literal nonempty selected path subset;
- the changed derivative word;
- the complete feasible, clean, and delete counts;
- one component-map/base-word certificate.

For example, in partition `0001234003144422`, suppose the
\(\{1,3\}\)-matching contains the cross paths \(3\!-\!10\) in block 1
and \(6\!-\!11\) in block 4.  Switching both is legal by (3).  The
certificate then deletes the second support circuit with missing colour
3.  Other matching rows use one same-circuit path or two cross paths.

Thus all four residuals containing three-occurrence blocks are removed,
as are both \(6+4+2+2+2\) residuals.  This uses the first operation not
already contained in a uniform component map: a matching can expose a
path which changes a proper subset of a four- or six-terminal colour
class.

## 4. Why observing the matching matters

Consider a fixed terminal set \(T\) of even size at least four.  A
matching-independent endpoint set must be a union of matched pairs in
every perfect matching of \(T\).  The only possibilities are
\[
                              \varnothing,\qquad T.      \tag{5}
\]
Indeed, if a nonempty proper set \(U\) were a union in every matching,
choose \(u\in U\) and \(v\notin U\); some perfect matching contains
\(uv\), contradicting the union property.

Switching every path toggles every \(x,y\)-terminal.  At the boundary
this is exactly the uniform transposition \(x\leftrightarrow y\) on
that complement component, hence is already one of its
\(\operatorname{GL}(2,2)\) maps.  The same is true for a two-terminal
component.  Consequently a matching-unobserved one-pair action adds
nothing to the exhausted direct map search.  The verifier enumerates
all circuit-closed combinations of (5) and confirms zero rescues for
all eight residuals.

The six reductions in Section 3 therefore genuinely use the quantifier
order \(\forall M\,\exists S(M)\).

## 5. The two surviving matching systems

The two \(8+2+2+2+2\) residuals have the same result:

| partition | \(P=12\) | \(P=13\) | \(P=23\) |
|---|---:|---:|---:|
| `0001234000314200` | \(14/15\) | \(14/15\) | \(2/3\) |
| `0123444444130244` | \(14/15\) | \(14/15\) | \(2/3\) |

Thus each colour pair has exactly one adverse joint matching.  It would
be invalid to choose those three matchings independently and call them
a graph obstruction.  Here they are displayed first and then realized
simultaneously.

For partition
\[
                            \pi_A=\texttt{0001234000314200},
\]
the three adverse path systems are
\[
\begin{array}{c|l}
12&
0:(1\!-\!7,\,2\!-\!15,\,8\!-\!9),\
1:(3\!-\!11),\ 2:(4\!-\!13),\ 3:(5\!-\!10)\\
13&
0:(0\!-\!1,\,2\!-\!7,\,9\!-\!14),\
1:(3\!-\!11),\ 2:(4\!-\!13),\ 3:(5\!-\!10),\
4:(6\!-\!12)\\
23&
0:(0\!-\!8,\,14\!-\!15),\ 4:(6\!-\!12).
\end{array}                                               \tag{6}
\]

For
\[
                            \pi_B=\texttt{0123444444130244},
\]
they are
\[
\begin{array}{c|l}
12&
1:(1\!-\!10),\ 2:(2\!-\!13),\ 3:(3\!-\!11),\
4:(4\!-\!15,\,5\!-\!7,\,8\!-\!9)\\
13&
0:(0\!-\!12),\ 1:(1\!-\!10),\ 2:(2\!-\!13),\
3:(3\!-\!11),\
4:(4\!-\!7,\,5\!-\!6,\,9\!-\!14)\\
23&
0:(0\!-\!12),\ 4:(6\!-\!8,\,14\!-\!15).
\end{array}                                               \tag{7}
\]
The integer before each colon is the complement-component index.

The rows contain 6, 7, and 3 paths.  They have respectively
\[
                 31,\qquad63,\qquad3                    \tag{8}
\]
nonempty subsets satisfying (3).  For every one of the 97 legal
subsets, the changed state again has exactly 320 feasible component-map
tuples, zero clean tuples, and zero deleting tuples.

The smallest surviving row is the three-path \(P=23\) pattern.  It has
two cross paths and one same-circuit path.  Its only legal nonempty
subsets are the same-circuit path alone, the two cross paths together,
and all three paths; all three fail.

## 6. Simultaneous literal realization

The adverse triples (6) and (7) are not incompatible abstract choices.
Both have a simple cubic realization.

For every two-occurrence component, use the standard properly
three-edge-coloured \(K_4-e\) two-pole.  For the eight-occurrence
component, use ten internal vertices \(0,\ldots,9\) and internal colour
matchings
\[
\begin{array}{c|l}
1&24,\ 67,\ 89\\
2&06,\ 13,\ 28,\ 59\\
3&03,\ 19,\ 48,\ 57.
\end{array}                                               \tag{9}
\]
Attach local boundary vertices \(0,\ldots,7\) to support occurrences
in the order
\[
\begin{array}{c|l}
\pi_A&2,1,0,7,8,9,14,15\\
\pi_B&4,5,6,7,8,9,14,15.
\end{array}                                               \tag{10}
\]
The derivative colours in either order are
\[
                              1,1,3,1,2,1,3,2,
\]
so (9) is a literal low-flow realization.  Following its bichromatic
paths gives exactly (6) and (7), simultaneously for all three colour
pairs.

Joining the multipoles to the two support 8-circuits produces, in each
case, a 42-vertex, 63-edge graph.  `realization_audit.py` reconstructs
both graphs and checks:

- all edges and vertices are distinct as required for a simple graph;
- every vertex has degree three;
- the graph is connected and has no bridge;
- the displayed three-coordinate values satisfy every flow equation;
- all three induced path systems equal (6) or (7);
- every legal one-round multiswitch has the counts in Section 5.

The audit also finds a literal Tait colouring of each graph.  Hence its
zero projection is extendable, so the displayed size-16 projection is
not globally minimum.  These graphs are counterexamples only to this
one-round matching-game descent rule, not to FiveCDC or to the
minimum-projection conjecture.

## 7. Exact conclusion and next boundary

We have proved the following finite dichotomy for the eight hard
support-16 residuals:

> Six admit a one-colour-pair, matching-observed strategy robust against
> every abstract terminal perfect matching.  The remaining two have a
> jointly graph-realizable adverse matching for all three colour pairs,
> and no nonempty circuit-closed one-round path subset cleans or deletes.

The exact missing mechanism is therefore no longer a single
four-terminal path choice.  Any continuation must use at least one of:

1. more than one Kempe round, recomputing path components after the
   first switch;
2. a support-changing exchange not captured by deleting a whole support
   circuit;
3. a consequence of global minimum which excludes the two Tait
   realizations and constrains the eight-terminal component more
   strongly.

## 8. Verification and disclosure

Run:

```bash
python3 matching_game.py
python3 realization_audit.py
```

`matching_game.py` reads and cross-checks the sibling `residuals.tsv`,
then writes the complete 211-kB
`matching-game-certificate.json`.  The frozen certificate digest is

```text
96a5ff4201c411c278e03ea9941a0665669575bb07da73aeff59d0cca38c6966
```

OpenAI Codex agents under Atharva Vaidya's direction formulated the
matching game, generated the certificates, found the second terminal
reattachment, and wrote the proof and checkers.  This work has not
received independent human peer review.  No literature-priority claim
or FiveCDC resolution is made.
