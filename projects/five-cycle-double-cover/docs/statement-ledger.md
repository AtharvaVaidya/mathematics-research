# Statement ledger

Status: standard formulation frozen after independent semantic and
primary-literature audits.  The fixed-graph witness predicate, empty-slot
padding equivalence, SAT/XOR equivalence, and restricted \(D_5\)-flow
equivalence are machine-checked in `formal/FiveCDC/`.  The universal
conjecture and its exact negation are not formalized.

## Working statement

For every finite undirected bridgeless graph \(G=(V,E)\), there are five
indexed edge-subsets \(C_0,\ldots,C_4\subseteq E\) such that:

1. every vertex has even degree in each spanning subgraph \((V,C_i)\), with
   incidences counted with multiplicity; and
2. every edge of \(G\) belongs to exactly two of the \(C_i\).

The five objects form an indexed list.  Empty even subgraphs and repeated
edge-subsets are allowed.  Thus the formulation is equivalent to “at most
five” by padding with empty sets.

This matches the explicit “at most \(k\)” definitions in Oum (2026, §9.1) and
Zhang (2012, Definition 1.3.1).  The indexed representation is essential:
literal set cardinality would discard repeated members and padding positions.

## Working exact negation

There exists a finite undirected bridgeless graph \(G=(V,E)\) such that for
every tuple \((C_0,\ldots,C_4)\) of even edge-subsets, some edge belongs to a
number of the \(C_i\) different from two.

Equivalently, the SAT/XOR instance in `docs/encoding.md` is unsatisfiable.
No graph is accepted as a counterexample without an independently checked
UNSAT certificate.

## Variants kept separate

- The standard 5-CDC has no orientation compatibility requirement.
- The orientable 5-CDC is a strictly separate secondary branch.
- “Cycle” in the circuit-cover literature often means an even (possibly
  disconnected) subgraph, not a connected 2-regular circuit.
- Simple graphs are the initial computational search domain.  Results are not
  generalized to multigraphs until loop and parallel-edge reductions are
  proved or cited.

## Incidence conventions

- Parallel edges are distinct elements of the indexed edge set.
- A non-loop edge has one incidence at each endpoint.
- A loop has two incidences at its endpoint.  It therefore contributes
  \(2x_{e,i}=0\) to every parity equation over \(\mathbb F_2\), while still
  contributing once to the exact-two coverage equation for that edge.
- Isolated vertices impose only vacuous parity conditions.

## Connectedness normalization

A disconnected graph has a 5-CDC if and only if each nontrivial connected
component has one: restrict a cover to obtain the forward implication, and
take coordinate-wise unions of component covers for the reverse implication.
Thus a minimum counterexample is connected.  This normalization does not
discard isolated vertices semantically.

## Exact cubic flow normal form

For a loopless cubic graph, FiveCDC is equivalent to the existence of a
nowhere-zero flow
\[
f:E(G)\longrightarrow\mathbb F_2^3\setminus\{0\}
\]
and a nonzero functional \(\mu\) for which every component of the
\(\mu\)-kernel subgraph has even boundary multiplicity in each of the four
affine value classes.  This is Hušek--Šámal's component-parity
characterization.  Writing \(f=(h,s)\) with
\(h:E\to\mathbb F_2\) and \(s:E\to\mathbb F_2^2\), it says equivalently
that some extendable binary projection \(h\) has an extension for which no
component of \(G-h\) is rainbow-odd.

The quantifier over the flow is essential.  The project has exact positive
FiveCDC graphs carrying displayed flows for which all seven functional
projections are dirty.  Therefore a fixed-flow statement is not equivalent
to FiveCDC.

## Exact full-flow projection optimization

For an arbitrary \(\mathbb F_2^2\)-flow \(s'\), let \(M=Z(s')\).  A binary
projection is extendable exactly when it has the form
\[
                 h=M\mathbin{\dot\cup}J,
\]
where \(J\subseteq E-M\) and
\(\partial J=\partial M\).  Hence
\[
\mu(G)=
\min_{\substack{s'\text{ an }\mathbb F_2^2\text{-flow}\\
                 J\subseteq E-Z(s'),\ \partial J=\partial Z(s')}}
       \bigl(|Z(s')|+|J|\bigr)
\]
is the exact minimum extendable-projection size.  For a fixed feasible
zero set \(M\), cleanability is equivalent to the existence of a second
\(\partial M\)-join disjoint from \(M\cup J\).  This characterization is
proved and replayed in
`scratch/minimum-projection-full-flow-exchange-20260729/`.
It is a normal form, not a solution: the strict-lock graph proves that an
optimum triple need not admit the second join.

## Literature links

See `docs/current-status.md` for the dated status audit, primary sources,
reduction scope, and the known finite frontier.
