# Every minimum exact-zero matching of the frozen \(H_4\) extends

Status: **PROOF-CERTIFIED FINITE THEOREM FOR ONE GRAPH / NOT A RESOLUTION
OF THE FIVE-CYCLE DOUBLE COVER CONJECTURE**.

## Result

Let \(H_4\) be the 162-vertex, 243-edge simple cubic graph frozen as
`H4.graph.json`.  For an \(\mathbb F_2^2\)-flow \(\phi\), call its exact
zero set

\[
M=\{e:\phi(e)=0\}
\]

admissible when it is a matching.  This package proves:

> **Fixed-\(H_4\) theorem.**  The minimum cardinality of an admissible
> exact zero set on \(H_4\) is four.  Every minimum admissible exact zero
> set \(M\) has two edge-disjoint \(\partial M\)-joins in \(H_4-M\).
> Consequently every such \(M\) extends to a standard five-cycle double
> cover of \(H_4\).

The projected census contains 4,931,430 distinct four-edge rows.  The
proof does not need to assume that every listed row is realizable: the
blocking LRAT proves that every *realizable* support occurs in the list,
and the positive witness checker proves that every listed row packs.  The
original incremental enumeration did obtain every row from a flow model,
but the finite theorem above is deliberately based only on the smaller
proof obligations just stated.

This theorem concerns one fixed graph.  It neither proves nor disproves
the five-cycle double cover conjecture, and it says nothing about the
orientable variant.

## Proof, with every logical dependency exposed

### 1. The minimum is four

`H4-minimum.model` is a complete satisfying assignment for
`H4-minimum.cnf`.  The clean-room `verify_upper_witness.py` checks every
CNF clause and then directly verifies that:

- \(M=\{58,114,139,210\}\) is a matching;
- two retained edge sets are binary cycles with intersection \(M\);
- the two flow-bit supports are binary cycles; and
- their exact common zero set is \(M\).

Thus an admissible exact zero matching of size four exists.

Independently, `flow-at-most-three-zero.cnf` is UNSAT.  Its retained LRAT
is accepted by both the C `lrat-check` program and the verified
CakeML-generated `cake_lpr`.  This formula permits arbitrary zero sets,
so its UNSAT result is stronger than needed: no
\(\mathbb F_2^2\)-flow on \(H_4\) has at most three zero edges.  Hence the
minimum admissible exact zero matching size is exactly four.

### 2. The projected list is complete

`generate_blocking_cnf.py` deterministically reconstructs
`all-supports-blocked.cnf`.  For every edge \(e\), its variables are two
flow bits \(a_e,b_e\) and a zero indicator \(z_e\).  The three clauses

\[
(\neg z_e\vee\neg a_e),\quad
(\neg z_e\vee\neg b_e),\quad
(z_e\vee a_e\vee b_e)
\]

say exactly

\[
z_e\longleftrightarrow(\neg a_e\wedge\neg b_e).
\]

At each cubic vertex, four clauses forbid the four odd assignments for
each flow bit.  Thus both bit supports have even incidence.  Pairwise
clauses \(\neg z_e\vee\neg z_f\) for incident edges make the zero set a
matching.  A displayed Sinz sequential counter imposes
\(\sum_e z_e\le4\).

Finally, for each corpus row \(S=\{e_1,e_2,e_3,e_4\}\), the formula
contains

\[
\neg z_{e_1}\vee\neg z_{e_2}\vee
\neg z_{e_3}\vee\neg z_{e_4}.                       \tag{1}
\]

The resulting formula has 1,697 variables and 4,936,112 clauses:
4,682 base clauses and 4,931,430 clauses of form (1).  If a
cardinality-four admissible exact zero set were absent from the corpus,
its flow would satisfy every clause, including every block (1).

The formula is UNSAT.  CaDiCaL 3.0.1 emitted
`all-supports-blocked.lrat`, a 973,056,379-byte textual LRAT.  It is
accepted independently by:

- `lrat-check`: `c VERIFIED`;
- the verified CakeML checker `cake_lpr`: `s VERIFIED UNSAT`.

Therefore every minimum exact-zero matching occurs among the listed rows.
The same certificate also excludes supports of size below four; the
separate smaller lower-bound proof is retained as an independent check.

### 3. Every listed row packs

`packing-witnesses.bin` contains one 31-byte record per corpus row.  Bit
\(e\) of a record indicates whether edge \(e\) lies in a binary cycle
\(Q\subseteq H_4-M\); the five unused high bits of the last byte are zero.

The independently written `verify_packing_witnesses.cpp` does not invoke
a SAT solver.  It reconstructs and checks the graph, proves the
4,931,430 support rows distinct, and for every row verifies:

1. \(M\) is a four-edge matching;
2. \(Q\cap M=\varnothing\);
3. \(Q\) has degree two at every endpoint of \(M\);
4. \(Q\) has degree zero or two at every other vertex; and
5. every circuit component of \(Q\) contains an even number of endpoints
   of \(M\).

It reports:

```text
VERIFIED rows 4931430 distinct 4931430 packing_witnesses 4931430
```

Here is the elementary reason this is a packing certificate.  Traverse
one circuit of \(Q\).  Color its successive arcs red or blue, keeping the
color through a nonterminal and changing it at a terminal.  The even
number of terminals makes the coloring consistent when the traversal
closes.  On all circuits, the red and blue classes are edge-disjoint;
each has odd degree one at every terminal and even degree zero or two
elsewhere.  They are therefore two edge-disjoint \(\partial M\)-joins.

### 4. From the joins to five cycles

For the two joins \(J_1,J_2\), put

\[
A=M\mathbin{\dot\cup}J_1,\qquad
B=M\mathbin{\dot\cup}J_2.
\]

These are binary cycles and \(A\cap B=M\).  A direct reverse lift of the
exact-zero flow now produces the other three coordinates.  Write
\(D_0=A\triangle B\), use the linear section

\[
s(1)=1100,\qquad s(2)=1010,\qquad s(3)=0110,
\]

and put \(k=1111\).  With \(\ell(y)\) the first coordinate of \(s(y)\),
define

\[
h(e)=1_{D_0}(e)+\ell(\phi(e)),\qquad
d(e)=s(\phi(e))+h(e)k.
\]

Both \(s\circ\phi\) and \(h\) are flows, so all four coordinates of \(d\)
are binary cycles.  Outside \(M\), \(d(e)\) has weight two and its first
coordinate is \(D_0\); on \(M\) it is zero.  Consequently
\(A,B,D_1,D_2,D_3\) cover every edge exactly twice.

## Reproduction

From the project root:

```sh
sh search/h4-all-minimum-support-packing-20260726/verify_package.sh
```

The full replay:

1. checks every SHA-256 ledger entry;
2. regenerates the 104 MB blocking CNF byte-for-byte;
3. checks the upper witness directly;
4. verifies both LRATs with `lrat-check` and `cake_lpr`; and
5. compiles and runs the independent semantic checker over all
   4,931,430 packing records.

The proof checkers are the pinned project copies under `.tools/`.
Their SHA-256 values are
`bd7eb8052623525814a0a37502b47f05375d9d9dfaf96ddc2fcd858958517cea`
for `lrat-check` and
`2fee767af4478ed817f8bdf6feea5866e5e59f1f67c2a4477e98ee961612881d`
for `cake_lpr`.
Regenerating the positive witness file itself requires CaDiCaL headers and
library; the exact producer is `generate_packing_witnesses.cpp`.  The
producer was run in eight consecutive chunks described by
`merge_witness_parts.py`.  Positive verification does not depend on
CaDiCaL.

## Principal artifacts

- `H4.graph.json`: canonical frozen graph data used here.
- `supports.tsv`: 4,931,430 distinct four-edge rows.
- `packing-witnesses.bin`: 31-byte even-marked circuit certificate per row.
- `all-supports-blocked.cnf` and `.lrat`: projected completeness proof.
- `flow-at-most-three-zero.cnf` and `.lrat`: independent minimum lower
  bound.
- `H4-minimum.cnf`, `.model`, and `.result.json`: explicit upper witness.
- `generate_blocking_cnf.py`: exact master-CNF reconstruction.
- `generate_packing_witnesses.cpp`: SAT witness producer plus immediate
  semantic check.
- `verify_packing_witnesses.cpp`: independently structured, solver-free
  full positive checker.
- `verify_upper_witness.py`: clean-room size-four upper-witness checker.
- `proof-check-results.json`, `packing-witness-check.json`, `result.json`:
  frozen summaries.

## AI-use disclosure

This project used substantial AI assistance.  AI agents helped formulate
the finite theorem, derive the circuit criterion, write the generators and
independent checkers, run and inspect the computations, engineer the LRAT
certificate, and draft this exposition.  The human project owner directed
the investigation.  No claim should be accepted because an AI produced
it: the purpose of this package is to make the finite claim independently
checkable through an elementary proof, explicit data, two proof checkers,
and a solver-free positive replay.  Specialist human review remains
appropriate before publication.
