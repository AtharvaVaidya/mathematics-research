# Human-checkable finite proof

This proves a finite auxiliary statement.  It is not a Five-Cycle
Double Cover counterexample.

Let \(G\), the root, and the three omitted masks be those printed in
`README.md`.  Decode graph6 in its standard upper-triangle order and
number the resulting 60 edges from zero.  Delete the three root edges
`(0,3,5)` from that edge list.  Bit \(j\) of omitted mask \(i\) says
that internal edge \(j\) belongs to omitted class \(A_i\), and put
\[
 T_i=\{s_i\}\cup(E(G-r)-A_i).
\]

For a tree \(T\), its odd kernel \(K(T)\) is the unique subset of tree
edges having odd degree at every vertex.  Rooting \(T\), an edge to a
child belongs to \(K(T)\) exactly when the child-side subtree has odd
order.  The three kernels give the standard
\(\mathbb F_2^3\)-flow used by the Jaeger-star construction.

The verifier performs the following finite proof.

1. The graph has 40 vertices and 60 distinct non-loop edges, with
   degree three at every vertex.  Deleting any zero, one, or two edges
   leaves it connected.  Exactly 40 three-edge deletions disconnect it,
   each separating one isolated vertex; no three-edge deletion leaves
   two cyclic components.  Thus it is three-edge-connected and
   cyclically four-edge-connected.  Its girth is five.
2. Each omitted mask contains 19 bits and the masks partition all 57
   internal edges.  Each \(T_i\) has 39 edges and a disjoint-set check
   proves it is a spanning tree.
3. The rooted-subtree rule gives kernel sizes `(20,20,20)`.  Direct
   degree counting verifies the odd-degree condition.  Since the graph
   is cubic, every kernel vertex has degree one or three; these three
   size-20 kernels are therefore perfect matchings.
4. For each nonzero functional \(a\), put
   \(F_a=\{e:a(f(e))=1\}\).  For each of the four values \(m\) with
   \(a(m)=1\), count the components of \(G-F_a\) containing an odd
   number of vertices incident with an \(m\)-edge.  These four counts
   agree for each \(a\), and the seven resulting counts are
   `(4,6,2,6,6,6,2)`.  This is exactly the component-parity defect in
   Hušek--Šámal Theorem 3.16.  Thus the current flow does not yet give a
   FiveCDC and \(\Psi=(2,60)\).  Separately, binary Gaussian elimination
   for the three allowed parallel switch directions in each plane gives
   zero successful span flags.
5. A reciprocal exchange chooses one element from each of two
   19-element omitted classes, so there are
   \(3\cdot19^2=1083\) candidates.  Testing both changed edge sets for
   the tree property leaves exactly 93 legal exchanges.
6. Recomputing all three kernels, the seven profile entries, and all 21
   flags for every legal neighbor finds no smaller \(\Psi\) and no
   successful flag.  Exactly 24 neighbors are safe with the same
   \(\Psi\).
7. Exhausting the legal neighborhoods of those 24 safe equal states
   checks 2,196 legal second arcs.  None has smaller \(\Psi\), and all
   2,196 have positive Theorem 3.16 component-parity defect and zero
   successful span flags.  Thus no augmented escape has length one or
   two.
8. Apply the local-position exchanges
   `(10,9)`, `(40,43)`, `(15,17)`.  Each is legal.  After the first and
   second swaps the state remains safe at `(2,60)`.  The third state has
   profile `(6,6,6,6,4,4,0)`, kernel sizes `(20,20,21)`,
   \(\Psi=(0,61)\), and three successful flags.  The zero profile entry
   is direct Theorem 3.16 component-parity success; the three span flags
   are an additional fact.  This is an augmented escape of length three.

Steps 5--7 prove the lower bound and step 8 proves the upper bound.
Therefore the exact augmented escape distance is three.  In particular,
the universal augmented radius-two obligation is false even for a
cyclically four-edge-connected cubic graph.

Finally, the 60 five-bit edge labels printed in `README.md` all have
weight two and xor to zero around every vertex.  Reading a coordinate
at a time gives five even edge-subsets covering every edge twice.  So
this same graph has an explicit standard FiveCDC.

The proof is human-checkable by direct finite enumeration; `verify.py`
implements precisely the listed checks in ordinary Python and contains
no SAT solver or probabilistic step.
