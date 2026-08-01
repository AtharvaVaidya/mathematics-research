# Human proof of the rooted transition encoding

## 1. D5 labels and five Eulerian edge sets

For every graph edge e and coordinate i in {0,1,2,3,4}, let x(e,i) be a
Boolean variable.  The exact-weight-two clauses say that exactly two of the
five variables x(e,i) are true.  Thus e receives a label L(e), a two-subset
of the five coordinates.

At every cubic vertex v and for every coordinate i, the encoding imposes

    xor_{e incident with v} x(e,i) = 0.

Consequently C_i = {e : x(e,i)=1} has even degree at every vertex.  Conversely,
the incidence vectors of any five Eulerian edge subsets that cover every
edge exactly twice satisfy exactly these constraints.  Hence the x-part of
the formula is equivalent to a FiveCDC labeling on a loopless cubic graph.

Parallel edges cause no difficulty because variables and incidences are
indexed by edge identity.  Loops are excluded by this implementation.  In
the usual incidence convention a loop contributes twice, hence contributes
zero to each parity equation; extending the implementation to loops requires
preserving that doubled incidence explicitly.

## 2. The coordinate-pair factor

Define

    y(e) = x(e,0) xor x(e,1).

Taking the xor of the two vertex equations for coordinates 0 and 1 shows
that the number of incident y-edges is even at every vertex.  Since H is
cubic, that number is zero or two.  Therefore the active y-edges form a
vertex-disjoint union of circuits.

At a vertex whose active y-edges are e and f, join the edge-nodes e and f by
one local transition.  The resulting transition graph T(Y) is a disjoint
union of cycles, and its connected components are exactly the circuits of Y.

## 3. Boundary characterization

For every vertex v and every unordered pair {e,f} of its three incident
edges, introduce z(v;e,f).  Impose

    z(v;e,f) -> y(e),
    z(v;e,f) -> y(f).

For every graph edge e impose the xor equation

    xor z(v;a,b) = 1 if e is r or s, and 0 otherwise,

where the xor ranges over all local transitions containing edge-node e at
either endpoint of e.

Theorem.  These z constraints are satisfiable exactly when r and s lie on
the same circuit of Y.

Proof.  If r and s lie on the same circuit, select the local transitions of
one r-to-s path in T(Y).  Its odd-degree edge-nodes are exactly r and s, so
all boundary equations hold.

Conversely, the selected z variables form an edge subset Z of T(Y).  Every
connected component of Z has an even number of odd-degree vertices.  The
only odd-degree vertices globally are r and s.  Therefore r and s occur in
the same component of Z, and hence in the same component of T(Y), which is
one circuit of Y.

There is no missing at-most-one constraint at a graph vertex.  The y-parity
condition permits only zero or two active incident y-edges.  Thus at most one
of the three local pairs can have both implications satisfied.

## 4. Clause-level equivalence

The implementation converts every xor equation to CNF by listing and
forbidding precisely the assignments of the wrong parity.

- Exact weight two on five x variables uses ten negative triple clauses and
  five positive four-variable clauses.
- A three-variable even-parity equation uses four clauses.
- The definition y = x0 xor x1 is the even-parity equation
  x0 xor x1 xor y = 0 and uses four clauses.
- Each transition implication is one binary clause.
- In a loopless cubic graph each edge-node is contained in four possible
  local transitions, so its boundary xor uses eight clauses.

For a cubic graph with m edges and n=2m/3 vertices, the formula has

    5m + m + 3n = 8m

variables.  The connectivity portion alone has 6n=4m implication clauses
and 8m boundary clauses, hence 12m clauses.  The complete formula has
15m + 20n + 4m + 4m + 8m = 133m/3 clauses.

The old layered reachability construction used order m squared variables
and clauses.  The boundary construction is linear.

Optionally the search can fix the label of the first root to {0,2}.
This is an equisatisfiable symmetry break: the stabilizer in S5 of the
unordered coordinate pair {0,1} acts transitively on the six two-subsets
that contain exactly one of 0,1.  The first root must have one of those six
labels.  This adds five unit clauses.  The default output is the literal
unrestricted instance.

## 5. Certificate boundary

A satisfying assignment is a constructive witness and search.py independently
checks:

1. every edge label has weight two;
2. every vertex xor is zero;
3. the selected transition set has boundary {r,s};
4. its selected transition graph contains an r-to-s path;
5. the full Y factor has one component containing both roots.

An UNSAT answer from a solver is not, on its own, an accepted mathematical
certificate.  The driver can retain the DIMACS instance and ask CaDiCaL for
a proof trace.  Any conjecture-level negative claim must freeze that instance,
retain the trace, and check it with an independently implemented proof
checker.
