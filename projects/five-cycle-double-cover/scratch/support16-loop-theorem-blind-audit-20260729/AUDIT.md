# Blind audit of the support-16 two-occurrence loop theorem

Date: **2026-07-29**

Status: **FINITE LOOP AUDIT PASSES / THEOREM CONDITIONAL ON TWO IMPORTED
RESULTS / DEPENDENCIES MUST REMAIN EXPLICIT**.

This audit was written without importing or executing functions from
`../support16-loop-higheroccurrence-reduction-20260729/verify.py`.  The
candidate prose conclusions were not used as premises.  The candidate files
were frozen by SHA-256 before the audit.

## Verdict

No mathematical gap was found in the requested bounded loop checks.

Conditional on the previously proved loopless theorem and the universal
one-circuit tensor theorem, the human reduction and independent finite census
support the statement:

> Every flowable two-occurrence interaction state of total support at most
> 16, with loops allowed, has a feasible flow which cleans or deletes.

The audit does not turn this into an unconditional standalone theorem because
the two imported results are not reproved here.  Their exact source locations
or artifact hashes should be cited/frozen before publication.

An initially observed, unledgered `__pycache__/verify.cpython-314.pyc` was
removed from the candidate directory before the final freeze.  The final
source audit reports no unledgered generated files.

The candidate package's separate higher-occurrence no-go claim was outside
this requested blind audit, except for the local length-six triple
failure-orbit calculation.  This audit therefore does not independently
endorse that broader no-go census.

## 1. Marked-word canonicalization

`audit.py` independently implements the action of
\(\operatorname{AGL}(2,2)\) and the dihedral circuit group.  Marks index the
derivative between word positions \(p-1\) and \(p\).  Under
\[
 c'_k=L(c_{a+\epsilon k})+z,
\]
the marked derivative index becomes \(p-a\) for \(\epsilon=1\), and
\(a+1-p\) for \(\epsilon=-1\).  The implementation checks the transformed
derivative values literally for every image used in canonicalization.

The independent census found:

| length | dirty proper words | loop tests | loop failure orbits | triple tests | triple failure orbits |
|---:|---:|---:|---:|---:|---:|
| 4 | 24 | 48 | 0 | 0 | 0 |
| 5 | 120 | 360 | 0 | 360 | 0 |
| 6 | 480 | 2,304 | 7 | 2,112 | 2 |

The seven loop and two triple representatives agree exactly with the
candidate tables.  Their raw marked-instance multiplicities sum to 1,080 and
576, respectively.  For every candidate switch, the audit checks that only
the two marked derivatives change and that the new values are the intended
nonzero loop value or transposed triple values.

## 2. Shape reduction

The following deductions were checked independently.

- Total support is even because every complement component has exactly two
  boundary occurrences.
- A dirty circuit uses all four colours and therefore has length at least
  four.  Support at most 16 leaves at most four interaction vertices.
- A constant nonzero edge value deletes whenever all circuit lengths are
  even: each local walk alternates between two points, and loops contribute
  twice.
- The marked-word census proves the short-loop deletion step through length
  five.
- A separate 138-pattern port/loop-pair census verifies the two-vertex local
  deletion lemma at port profiles \(5{:}3,5\), \(7{:}3,5,7\).
- Four dirty vertices force lengths \(4+4+4+4\), already covered by the
  even-length case.
- For three vertices, exhaustive integer degree equations, connected-core
  checks, and normalized nowhere-zero flow tests leave exactly:

```text
((4,0),(5,0),(7,1); 2,2,3)
((4,0),(5,0),(7,2); 3,1,2)
((5,0),(5,0),(6,1); 3,2,2)
((5,0),(5,0),(6,2); 4,1,1)
```

Here `(length,loops)` is listed at each vertex and the last triple gives
the `01,02,12` parallel-edge multiplicities.  The bridge case with three
loops on the length-seven vertex has no nowhere-zero flow.  Three loops on
the length-six vertex disconnect that vertex and invokes the one-circuit and
two-vertex results componentwise.

The executable shape census examined 563 loop allocations and found no fifth
post-reduction profile.

## 3. Literal profile enumeration

The audit labels every interaction edge, generates cyclic orders modulo local
rotation and reversal, and normalizes the first edge value to 1 under the
global `GL(2,2)` action.  Flowability is tested by literal xor charge at all
three vertices.  A loop has one value, occurs twice at its vertex, and
cancels twice in the charge equation.

For each flow and local order, the audit integrates the walk and records the
literal unoriented endpoint set in \(K_4\) of every occurrence.  Deletion
means that a local visited-point set has size below four.  Cleaning means
that, after trying all relative circuit translations, the two endpoint sets
of every interaction edge are equal.  This comparison includes the two
occurrences of every loop.

| profile | local order counts | states | normalized flows | selected clean | selected delete | residual |
|---|---:|---:|---:|---:|---:|---:|
| `457-a` | 3, 12, 180 | 6,480 | 138 | 0 | 6,480 | 0 |
| `457-b` | 3, 12, 90 | 3,240 | 126 | 0 | 3,240 | 0 |
| `556-a` | 12, 12, 30 | 4,320 | 138 | 168 | 4,152 | 0 |
| `556-b` | 12, 12, 16 | 2,304 | 180 | 12 | 2,292 | 0 |

The independently generated category stream has SHA-256

```text
8168cff38b861ac162ada05f89bb9f6986d9fe12d1ae3eb9b1bbb02682826228
```

matching the candidate package.

## 4. Hashes, scope, and disclosure

The candidate ledger matches these frozen files:

```text
104cddcead47f35f4d58d68c178bf217b56304393ca2a1f29abe13652a1f859a  HUMAN-PROOF.md
d4d96c24263f965bea3b3530349f8d29aab3cb193c1acf1475a7bb5ba61b372c  README.md
1448dc8cec614b078cc22808781b7744f6f35aed17bc087e3cbe8390170c1fa6  verify.py
```

The candidate explicitly limits the result to the two-occurrence branch and
support 16, distinguishes abstract local failures from graph counterexamples,
and says it does not prove or disprove FiveCDC.  Its human proof discloses
OpenAI Codex assistance, Atharva Vaidya's direction, lack of independent
human peer review, and no literature-priority claim.

## Replay

From this audit directory:

```sh
python3 audit.py
```

The verifier uses only the Python standard library and completes in about
three seconds on the audit machine.
