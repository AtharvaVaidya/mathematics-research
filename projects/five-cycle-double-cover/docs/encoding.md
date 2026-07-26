# SAT/XOR encoding

Status: frozen for the standard target.  Verifier A 1.0.0 and Verifier B
0.1.0 implement independent CNF translations and direct semantic checkers;
the fixed-graph equivalence is machine-checked in Lean.

For every indexed edge \(e\in E\) and coordinate \(i\in\{0,1,2,3,4\}\),
introduce a Boolean variable \(x_{e,i}\).

## Exact-two constraints

For each edge \(e\),

\[
\sum_{i=0}^{4} x_{e,i}=2.
\]

## Native XOR constraints

For each vertex \(v\) and coordinate \(i\),

\[
\bigoplus_{(e,\text{ incidence})\text{ at }v} x_{e,i}=0.
\]

An edge occurs once in this XOR for each incidence at \(v\).  Thus a loop
occurs twice and cancels.  Implementations may omit both copies only after
recording that semantic equivalence.

## Equivalence obligation

For a fixed coordinate \(i\), the selected edge set
\(C_i=\{e:x_{e,i}=1\}\) is an even/Eulerian edge-subset if and only if its
incidence XOR is zero at every vertex.  The exact-two constraints say exactly
that every edge occurs in two distinct list coordinates.  Combining these two
facts gives a bijection between satisfying assignments and indexed 5-CDCs.

The prose proof below, the machine-checked theorem in
`formal/FiveCDC/FiveCDC/Encoding.lean`, and both independent verifier suites
discharge this obligation for the fixed-graph semantics.

### Prose proof

Given a satisfying assignment, set
\(C_i=\{e:x_{e,i}=1\}\).  The integer exact-two row says precisely that each
edge belongs to two indexed sets.  The incidence XOR at \((v,i)\) is the
degree of \(v\) in \((V,C_i)\) modulo two, so every \(C_i\) is even.

Conversely, the characteristic functions of five even edge-subsets that
double-cover \(E\) satisfy the two constraint families.  These maps are
mutual inverses.  Thus satisfying assignments and indexed 5-CDCs are in
bijection.

The loop case is included: its two incidences contribute twice and cancel in
the degree parity, but its one binary membership value remains subject to
exact-two across coordinates.

### Direct auxiliary-free certificate CNF

For exactly two of five variables, add all ten negative clauses on triples
(at most two) and all five positive clauses on four-subsets (at least two).

For a parity row \(z_1\oplus\cdots\oplus z_d=0\), add one blocking clause
for every odd bit-vector \(a\in\{0,1\}^d\):

\[
\bigvee_{a_j=1}\neg z_j\ \vee\ \bigvee_{a_j=0}z_j.
\]

This second encoding has no parity auxiliaries and is the intended independent
cross-check of Verifier A's chained XOR-gate CNF.  It is exponential in
high vertex degree but small for the cubic search domain.

### Pseudo-Boolean alternative

Exact-two is a native equality.  For a degree-\(d\) parity row, introduce
one-hot \(q_t\), \(0\le t\le\lfloor d/2\rfloor\), and impose

\[
\sum_tq_t=1,\qquad
\sum_j z_j-2\sum_t t q_t=0.
\]

This is retained as a future VeriPB route; no frozen PB generator exists yet.

## Certificate policy

The native-XOR instance is a discovery representation.  Each reported UNSAT
result must also be emitted as certificate-producing CNF or pseudo-Boolean
constraints.  A graph is a counterexample only if its complete certificate is
checked by a separately implemented verifier.

An UNSAT proof certifies only the emitted formula.  It does not certify graph
parsing, bridgelessness, incidence multiplicity, or the correspondence above;
those remain separate acceptance checks.
