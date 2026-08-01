# Human audit of the unrestricted support-16 fixed-word frontier

Date: 2026-07-29

Status: **EXACT BOUNDED CENSUS / DIRECT-TEST RESIDUALS / NOT A GLOBAL
MINIMUM OR FIVECDC RESULT**.

## 1. Boundary state

Let \(K=\mathbb F_2^2=\{0,1,2,3\}\), with addition written as xor.
The support is two oriented 8-circuits carrying low words
\[
                 c=\texttt{01010123|01012302}.
\]
Every circuit is proper and uses all four low colours, as required by
the minimum-projection exchange theorem.  At the support occurrence
between the preceding and current support edges put
\[
                         d_i=c_{i-1}+c_i.
\]
This gives
\[
                 d=\texttt{31111131|21113132}.               \tag{1}
\]

A complement-component partition is a restricted-growth word
\(\pi_0\ldots\pi_{15}\).  It is charge-valid when every block \(a\)
satisfies
\[
                         \bigoplus_{\pi_i=a}d_i=0.             \tag{2}
\]
Equation (2) makes the displayed identity extension feasible, so every
enumerated state is flowable in the abstract boundary sense.

A size-two block with both occurrences on one circuit is an
**interaction loop**.  A block of size greater than two is a
**higher-occurrence component**.  Unlike the ordinary interaction
multigraph, the present partition model permits both.

## 2. Canonicalization

The state symmetries are:

- the global affine action on the four low colours;
- independent dihedral actions on the two circuits; and
- interchange of the equal-length circuits.

First-occurrence renaming of the four colours quotients the affine
action because \(\operatorname{AGL}(2,2)\cong S_4\).  Applying the two
dihedral actions and circuit interchange gives 512 normalized images of
the displayed word.  `verify_residuals.py` checks that all 512 are
different and that the displayed word is their unique lexicographic
minimum.  Thus the word stabilizer is trivial.

Every component partition is generated in restricted-growth form by
taking the block containing the least remaining position first.  Since
the word stabilizer is trivial, two different generated partition words
cannot represent equivalent states in this word orbit.  The census
therefore counts canonical states, not labelled overcounts.

## 3. Complete partition count

There are \(10,2,4\) occurrences of derivative values \(1,2,3\) in
(1).  The primary program enumerates every set partition satisfying
(2).  Independently, `verify_partition_count.py` uses the recurrence
\[
 F(R)=\sum_{\substack{B\subseteq R\\
                      \min R\in B\\
                      \oplus_{i\in B}d_i=0}}F(R-B),
 \qquad F(\varnothing)=1.                                \tag{3}
\]
The distinguished least element makes the block choice unique, so (3)
counts every partition exactly once.  Both computations give
\[
                              8,046,330.                    \tag{4}
\]

If every block has size two, equal derivative values must be paired.
There are
\[
                       9!!\,1!!\,3!!=2,835                 \tag{5}
\]
such partitions.  Every one contains an interaction loop: derivative
value 2 occurs zero times on the first circuit and twice on the second,
so an all-cross-circuit pairing is impossible.  Thus none of the states
in (4) is already covered by the loopless two-occurrence theorem.

## 4. Exact classification

For each component block \(a\), choose
\(L_a\in\operatorname{GL}(2,2)\).  A common global map changes neither
cleanliness nor deletion, so the program fixes \(L_0=I\) and exhausts
the remaining six choices per block.  It transforms
\[
                         d'_i=L_{\pi_i}d_i.                   \tag{6}
\]
A tuple is feasible exactly when (6) xors to zero around each support
circuit.  The program integrates the two circuits, exhausts their four
relative translations, and tests the literal component/colour boundary
parities.  A circuit strictly deletes exactly when its integrated low
word omits a colour.

The mutually exclusive results are
\[
\begin{array}{c|r}
\text{clean}&8,041,808\\
\text{strict-delete-only}&4,514\\
\text{residual}&8.
\end{array}                                               \tag{7}
\]
The input categories split as follows; each entry is
clean/delete-only/residual:
\[
\begin{array}{c|r@{/}r@{/}r}
\text{loop only}&2,835&0&0\\
\text{higher occurrence, no loop}&3,060,801&2,872&8\\
\text{loop and higher occurrence}&4,978,172&1,642&0.
\end{array}                                               \tag{8}
\]
In particular, this complete word orbit has no loop-caused residual.
Every residual has a higher-occurrence component.

The program freezes the category counts and two ordered FNV-1a streams:

```text
classified_fnv64=17068633071306477955
residual_fnv64=6039899158318007243
```

The independently evaluated, sorted residual-key file has SHA-256

```text
3b0d26a74107e67b64878342cb9fb509bc1b8830d9da89a308fb5a1305274c0d
```

## 5. The eight residuals

In the matrix column below, \(a/b\) gives a component's number of
occurrences on the first/second circuit.

| partition | block profile | per-circuit matrix |
|---|---|---|
| `0001234000314200` | \(8+2+2+2+2\) | \(4/4,1/1,1/1,1/1,1/1\) |
| `0001234003144422` | \(5+4+3+2+2\) | \(4/1,1/1,1/2,1/1,1/3\) |
| `0012344041300022` | \(6+3+3+2+2\) | \(3/3,1/1,1/2,1/1,2/1\) |
| `0012344044130244` | \(6+4+2+2+2\) | \(3/1,1/1,1/1,1/1,2/4\) |
| `0012344400314200` | \(6+4+2+2+2\) | \(2/4,1/1,1/1,1/1,3/1\) |
| `0012344403144422` | \(6+3+3+2+2\) | \(2/1,1/1,1/2,1/1,3/3\) |
| `0123444441300022` | \(5+4+3+2+2\) | \(1/3,1/1,1/2,1/1,4/1\) |
| `0123444444130244` | \(8+2+2+2+2\) | \(1/1,1/1,1/1,1/1,4/4\) |

All have five components.  None has a size-two interaction loop, and
all have higher-occurrence components.  An independent matrix-based
implementation finds, for each row,
\[
             320\ \text{feasible maps},\qquad
             0\ \text{clean},\qquad 0\ \text{delete}.         \tag{9}
\]

The last row is exactly the partition displayed in
`minimum-projection-size16-multiswitch-counterstate-20260729`.
The lexicographically first canonical residual is the first row.  If
“smallest” instead minimizes the largest component, the two
\(5+4+3+2+2\) rows are minimal, with maximum block size five.

## 6. Minimum-projection semantics

For a clean row, the component maps and translations give a clean
extension.  For a strict-delete row, choose a colour omitted by the
integrated circuit and toggle the corresponding three-bit constant
around that circuit.  No edge becomes zero, while the entire circuit
leaves the first-coordinate support.  Such a row cannot be globally
cardinality-minimum.

A residual in (9) says only that this direct dichotomy has no outcome.
The abstract partition records neither the internal complement graph nor
its bichromatic path pairings.  It cannot test:

- existence of a bridgeless cubic realization;
- support-neutral Kempe moves inside complement components; or
- whether another extendable projection has smaller support.

Indeed, the existing 42-vertex realization of the final row is
Tait-colourable, so its minimum projection has size zero.  The present
census does not realize the other seven rows.  Hence none of the eight
is a FiveCDC counterexample or a certified globally minimum obstruction.

## 7. Full-frontier gap

The possible support shapes at total 16 are
\[
\begin{gathered}
16;\quad4+12,\ 5+11,\ 6+10,\ 7+9,\ 8+8;\\
4+4+8,\ 4+5+7,\ 4+6+6,\ 5+5+6;\quad4+4+4+4.
\end{gathered}
\]
The one-circuit row is covered by the existing tensor theorem.  This
package completes one word orbit in \(8+8\), not the remaining nine
multi-circuit shapes.

There are 5,544 proper all-four-colour cyclic length-eight words.  The
raw `8+8` pair set has 30,735,936 elements, while the full symmetry group
has order at most 12,288.  Thus `8+8` alone has at least 2,502 word
orbits.  A full support-16 enumeration was not computationally feasible
within this turn.

OpenAI Codex agents under Atharva Vaidya's direction derived, implemented,
and checked this bounded census.  It awaits independent human review and
makes no FiveCDC-resolution claim.
