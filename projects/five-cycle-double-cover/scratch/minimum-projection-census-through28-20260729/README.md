# Exact finite minimum-projection cleanability census

Date: **2026-07-29**.

Status: **EXACT FINITE EVIDENCE / NO UNIVERSAL CLAIM / NO FIVECDC
CLAIM**.

## Definitions and exact test

Let \(G\) be a connected simple cubic non-Tait graph, as in every
nonempty tested source file, and let
\(h\in Z_1(G;\mathbb F_2)\) be nonzero.  Put \(K=E(G)-h\).

The projection \(h\) is **extendable** iff there are binary cycles
\(p,q\) such that

\[
                         K\subseteq p\cup q.                 \tag{1}
\]

Indeed, \(f=(h,p,q)\) is then a nowhere-zero
\(\mathbb F_2^3\)-flow; conversely the last two coordinates of every
extension satisfy (1).

The exact two-cycle normal form says that \(h\) is **cleanable** iff
there are such \(p,q\) for which, for every component \(W\) of \(K\),

\[
                 |p\cap q\cap\delta(W)|\equiv0\pmod2.       \tag{2}
\]

This is exactly the Hušek--Šámal four-affine-value component condition,
not a relaxation.

For a fixed \(h\) and first cycle \(p\), write the second cycle \(q\) in
a cycle basis.  Condition (1) forces \(q_e=1\) on \(K-p\), and (2)
adds one linear equation

\[
                      q\mathbin{\cdot}(p\cap\delta(W))=0
\]

per component.  Thus both extendability and cleanability are decided by
Gaussian elimination over \(\mathbb F_2\).  `scan.cpp` enumerates all
binary cycles by increasing cardinality, finds the first extendable
cardinality, and tests every extendable projection at that cardinality
for cleanability.

## Frozen finite results

### Cyclically-four source through order 28

The ten source files are the exact graph6 files retained by
`search/focused-theta-choice-through28-20260727`.  On their literal
14,009 records the result is:

| order | records | minimum extendable-projection size profile | minimum extendable projections | bad minima |
|---:|---:|:---|---:|---:|
| 10 | 1 | \(5:1\) | 12 | 0 |
| 12 | 0 | empty | 0 | 0 |
| 14 | 0 | empty | 0 | 0 |
| 16 | 0 | empty | 0 | 0 |
| 18 | 2 | \(5:2\) | 18 | 0 |
| 20 | 6 | \(5:6\) | 40 | 0 |
| 22 | 31 | \(5:31\) | 228 | 0 |
| 24 | 155 | \(5:155\) | 1,129 | 0 |
| 26 | 1,297 | \(5:1297\) | 9,634 | 0 |
| 28 | 12,517 | \(5:12515,\ 6:1,\ 9:1\) | 92,754 | 0 |

The upstream package classifies these as every retained cyclically
4-edge-connected non-Tait simple cubic graph of even order 10 through
28.  Completeness of that graph-class population and the Snarkhunter
option semantics are inherited from its documented generation; the
present checker proves the minimum-projection statement unconditionally
for the literal frozen files.

### Broader frozen order-22 hard source

The separate file

```text
search/four-pole-order22-cap-20260727/artifacts/order22-hard.g6
```

has 12,892 records.  The upstream order-22 package identifies and
independently verifies them as the bridgeless non-Tait rows among its
7,319,447 generated connected simple cubic order-22 records.  For this
literal 12,892-row file:

```text
minimum extendable-projection size 5:  11,776 graphs
minimum extendable-projection size 6:   1,025 graphs
minimum extendable-projection size 7:      55 graphs
minimum extendable-projection size 8:      20 graphs
minimum extendable-projection size 9:       6 graphs
minimum extendable-projection size 10:     10 graphs

minimum extendable projections at those levels: 54,785
uncleanable minimum extendable projections:          0
```

This population statement must not be paraphrased as a new independent
enumeration of all order-22 graphs by this package.  The unconditional
claim here is about the exact frozen file; its broader graph-class
provenance is supplied and checked by the upstream census.

## Exact exchange reduction

Let \(f=(h,s)\) be an extension and

\[
                  M_c=\{e:h(e)=1,\ s(e)=c\}.
\]

If \(C\) is any binary cycle containing \(M_c\), then
\(X=h\mathbin{\triangle}C\) avoids the full value \((1,c)\).
Switching \(f\) by \((1,c)\) on \(X\) is therefore nowhere zero.  Its
first coordinate is \(C\), and its new \(c\)-class is exactly the old
\(M_c\): old \(M_c\)-edges are not switched, while a new edge from
\(K\) could have colour \(c\) only if its old \(s\)-value were zero,
which is impossible on \(K\).

Consequently, on a non-Tait graph, a globally minimum nonzero extendable
\(h\) is a
minimum-cardinality binary cycle containing each \(M_c\).  Equivalently,
with \(T_c\) the endpoints of the matching \(M_c\),
\(h-M_c\) is a minimum \(T_c\)-join in \(G-M_c\).
Cleanliness is precisely the assertion that every component of \(G-h\)
is \(T_c\)-even.  The Petersen artifact next to this package shows why
one cannot prove that last assertion from a single \(M_c\) alone.

## Triangle expansion lemma

Let \(G\) be obtained from a loopless cubic graph \(H\) by replacing one
vertex by a triangle, and let
\(\pi:Z_1(G;\mathbb F_2)\to Z_1(H;\mathbb F_2)\) contract that
triangle.

> **Lemma.** A prescribed projection \(h'\) is cleanable in \(G\) iff
> \(\pi(h')\) is cleanable in \(H\).

At a cubic vertex, three conserved \(D_5\)-labels are
\(ab,ac,bc\) for distinct coordinates \(a,b,c\).  Attach these to the
three new triangle vertices.  In cyclic internal-edge order the complete
list of \(D_5\)-extensions is

\[
              (bc,ab,ac),\qquad(ad,cd,bd),                 \tag{3}
\]

where in the second pattern \(d\) is either coordinate outside
\{a,b,c\}.  Fix the distinguished coordinate \(r\).  If
\(r\notin\{a,b,c\}\), the external \(r\)-pattern is \(000\), and (3)
realizes both possible internal cycle patterns \(000\) and \(111\).
If \(r=a\), the external pattern has weight two, and (3) realizes the
two possible internal patterns \(011\) and \(100\).  Thus every
prescribed binary-cycle lift of the distinguished coordinate extends
locally.  Conversely, summing the three triangle vertex equations
cancels the internal edges and contracts every \(D_5\)-flow to one on
\(H\).  This proves both implications.

There is a useful edge case.  If \(h'\) is extendable and
\(\pi(h')=0\), contraction gives a nowhere-zero
\(\mathbb F_2^2\)-flow on \(H\).  Embedding its three values as
\(ab,ac,bc\) makes the zero distinguished projection clean on \(H\);
the lemma then cleans \(h'\).  Hence the new triangle-kernel projection
cannot be a first unclean minimum.

## Replay and hashes

Run:

```sh
python3 scratch/minimum-projection-census-through28-20260729/verify_summary.py
```

The replay compiles `scan.cpp`, verifies every frozen input digest,
checks every emitted graph6 row against its source row, and checks every
aggregate above.  It takes about two minutes on the recorded machine.

Input hashes are embedded in `verify_summary.py`; the package and its
borrowed linear-classifier source are frozen in `SHA256SUMS`.

## AI-use disclosure

OpenAI Codex agents under human direction derived the linear tests,
implemented and replayed the census, proved the exchange and triangle
lemmas, and prepared this report.  Agent cross-checks are not independent
human peer review.  The source files, hashes, exact aggregates, and
replay code are included so the finite claims can be checked without
trusting an AI system.  No literature-wide priority claim is made.
