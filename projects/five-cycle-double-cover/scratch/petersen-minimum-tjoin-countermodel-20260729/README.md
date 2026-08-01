# A Petersen obstruction to the one-matching alternating-cycle shortcut

Date: **2026-07-29**.

Status: **EXACT COUNTEREXAMPLE TO AN INTERMEDIATE LEMMA / NOT A
COUNTEREXAMPLE TO THE MINIMUM-PROJECTION CONJECTURE OR FIVECDC**.

## Statement

The following tempting claim is false:

> If \(M\) is a matching in a cubic graph and \(C\) is a
> minimum-cardinality binary cycle containing \(M\), then some such
> minimum \(C\) has the property that every component of \(G-C\)
> contains an even number of endpoints of \(M\).

Take the Petersen graph with graph6 record

```text
ICOf@pSb?
```

and the following literal edge order:

| id | edge | id | edge | id | edge |
|---:|:---:|---:|:---:|---:|:---:|
| 0 | 03 | 5 | 18 | 10 | 38 |
| 1 | 06 | 6 | 25 | 11 | 47 |
| 2 | 09 | 7 | 26 | 12 | 49 |
| 3 | 14 | 8 | 27 | 13 | 58 |
| 4 | 16 | 9 | 37 | 14 | 59 |

Let

\[
                       M=\{1,3,6\}.
\]

This is a matching.  Exactly eight binary cycles contain \(M\).  Their
cardinality profile is

\[
                    2x^8+4x^9+2x^{10}.
\]

Thus the minimum cardinality is eight, and the two minimum cycles are

\[
\begin{aligned}
C_1&=\{1,2,3,5,6,7,12,13\},\\
C_2&=\{1,2,3,4,6,8,11,14\}.
\end{aligned}
\]

For \(C_1\), the components of \(G-C_1\) are

\[
 \{0,2,3,4,7,8\},\qquad \{1,6\},\qquad \{5,9\},
\]

and their endpoint parities for \(M\) are \(1,0,1\).  For \(C_2\), the
components are

\[
 \{0,1,3,5,7,8\},\qquad \{2,6\},\qquad \{4,9\},
\]

again with parities \(1,0,1\).  Neither minimum cycle is clean.

## Short finite proof

The Petersen cycle space has dimension \(15-10+1=6\).  One cycle basis,
in the displayed edge order, is

```text
0 1 7 8 9
0 1 4 5 10
3 4 7 8 11
1 2 3 4 12
4 5 6 7 13
1 2 6 7 14
```

XORing the \(2^6=64\) subsets and retaining those containing
\(\{1,3,6\}\) gives the eight-cycle profile above and exactly the two
displayed minima.  Deleting either minimum edge set from the literal
edge table gives the displayed components.  Counting the six endpoints
of \(M\) in those components gives \(1,0,1\).

The checker below instead exhausts all \(2^{15}\) edge subsets and tests
even degree directly, so it does not depend on the displayed basis.

```sh
python3 scratch/petersen-minimum-tjoin-countermodel-20260729/verify.py
```

## Why this does not refute the four-colour route

For an extension \(f=(h,s)\), each of the four affine colour classes
\(M_c\) is simultaneously a matching in \(h\), and the same components
are odd for all four classes.  The example above supplies only one
matching \(M\); it does not realize those four synchronized structures.
Moreover its minimum containing cycles have size eight, whereas the
Petersen graph has cleanable extendable projections of size five.

Therefore a proof cannot invoke a one-matching minimum-\(T\)-join theorem.
It must use the simultaneous four-colour flow constraints.

## AI-use disclosure

OpenAI Codex agents under human direction found, checked, and documented
this finite obstruction.  The complete graph, both minimum cycles, and a
dependency-free exhaustive checker are included so the claim can be
verified without trusting an AI system.  No literature-wide priority
claim is made.
