# Rank-three four-move normal form

## Scope

Let \(G=(V,E)\) be a finite multigraph and let \(f,g:E\to
\mathbb F_2^3\setminus\{0\}\) be nowhere-zero flows.  A move chooses a fixed
nonzero vector \(a\in\mathbb F_2^3\) and adds \(a\) on an arbitrary Eulerian
edge-set.  The support may be disconnected.  Every flow after a move is
required to remain nowhere-zero.

Thus this is **not** the adjacency relation in which one must switch on one
connected cycle.  It is also not a proof or disproof of the Five-Cycle Double
Cover Conjecture.

Loops are counted twice at their incident vertex and hence vanish in every
incidence sum over \(\mathbb F_2\).  Parallel edges remain separate columns.

## The theorem

Fix an ordered four-tuple
\[
  (a_1,a_2,a_3,a_4)\in
  (\mathbb F_2^3\setminus\{0\})^4
\]
whose span is all of \(\mathbb F_2^3\).  Define
\[
  A:\mathbb F_2^4\longrightarrow\mathbb F_2^3,\qquad
  A z=\sum_{j=1}^4 z_j a_j .
\]
Its kernel has dimension one.  Let \(d\ne0\) be its unique nonzero element.
Put \(h=f+g\).  For every edge \(e\), choose any one preimage
\(z^0(e)\in A^{-1}(h(e))\).

At each vertex define
\[
  p_v=\sum_{e\ni v}z^0(e)\in\mathbb F_2^4,
\]
counting incidences with multiplicity.  Then \(p_v\in\langle d\rangle\), so
there is a unique \(q_v\in\mathbb F_2\) with \(p_v=q_vd\).

For each edge \(e\), define its legal toggle set \(L_e\subseteq\mathbb F_2\)
by declaring \(y\in L_e\) precisely when all four prefix values
\[
 f(e)+\sum_{j=1}^k
 \bigl(z^0_j(e)+y d_j\bigr)a_j,\qquad k=1,2,3,4,
\]
are nonzero.

**Theorem.**  There is a legal realization using the four moves in the
specified order if and only if there are bits \(y_e\in L_e\) satisfying
\[
  B y=q,
\]
where \(B\) is the unoriented vertex-edge incidence matrix over
\(\mathbb F_2\).

Equivalently:

1. if some \(L_e\) is empty, the order is impossible;
2. let \(P=\{e:L_e=\{1\}\}\) and \(F=\{e:L_e=\{0,1\}\}\);
3. put \(q'=q+B{\bf1}_P\);
4. the order is possible if and only if every connected component of the
   spanning subgraph \((V,F)\), isolated vertices included, contains an even
   number of vertices \(v\) with \(q'_v=1\).

Edges with \(L_e=\{0\}\) have no further role.  Free loops cannot change a
boundary and do not join different vertices; forced-one loops contribute
twice and hence contribute zero.

## Proof

Every preimage of \(h(e)\) has the unique form
\[
  z(e)=z^0(e)+y_ed
\]
because \(\ker A=\{0,d\}\).  The \(j\)-th move support is
\(X_j=\{e:z_j(e)=1\}\).

Since \(h\) is a flow,
\[
  A p_v
  =\sum_{e\ni v} A z^0(e)
  =\sum_{e\ni v}h(e)
  =0.
\]
Hence \(p_v\in\ker A=\langle d\rangle\), proving that \(q_v\) is defined.
The four supports are all Eulerian exactly when, at every vertex,
\[
\begin{aligned}
  0
  &=\sum_{e\ni v}z(e)\\
  &=p_v+\left(\sum_{e\ni v}y_e\right)d\\
  &=\left(q_v+(By)_v\right)d .
\end{aligned}
\]
Because \(d\ne0\), this is equivalent to \((By)_v=q_v\).  Independently, the
nowhere-zero condition on edge \(e\) is exactly \(y_e\in L_e\).  This proves
the first characterization in both directions.

After inserting the forced-one variables, the remaining equation is
\[
  B_F y_F=q'.
\]
Every column belonging to a nonloop free edge has two ones, so its boundary
has even parity in its free-edge component; a loop column is zero.  Therefore
even component parity is necessary.  It is sufficient because the incidence
columns of a spanning tree generate every even-parity vector on that
component: root the tree and eliminate nonroot vertices from the leaves
upward, choosing the parent edge exactly when the current leaf demand is one.
The root equation holds because the total demand is even.  This proves the
component criterion.

## Independent finite audit

`verify.py` reconstructs the 890-vertex, 1335-edge Petersen--Foster graph
directly from the Foster LCF string and Petersen substitution, without
importing the source verifier.  It reconstructs:

- the start flow from `bad_flow_digits`;
- the target flow from `fivecdc-labels.txt` and the five point assignments;
- all ordered nonzero four-tuples spanning \(\mathbb F_2^3\).

There are 1,848 such tuples.  One way to check the count is to count
rank-three \(3\times4\) binary matrices and exclude zero columns:
\[
 (15)(14)(12)-4(7)(6)(4)=2520-672=1848.
\]

The audit applies the theorem twice.  The first lift is a canonical linear
section and has \(q=0\).  The second independently toggles the chosen
preimage on a fixed, edge-dependent set; it has 554 odd-demand vertices.
Both give the invariant classification:

- 1,176 tuples have an edge with no legal toggle;
- 672 pass every local edge test but fail free-component parity;
- 0 yield a legal four-move realization.

It also enumerates all 168 ordered rank-three triples and finds none legal.
Finally, it compares the component criterion with brute force on 16,384
small instances containing a loop, parallel edges, and an isolated-vertex
possibility.

The result is an exact lower bound of five moves between these two particular
flows in the arbitrary-Eulerian-support fixed-vector move model.  The source
certificate separately supplies and checks a five-move path.

## AI disclosure and review status

This theorem note and verifier were produced by an OpenAI Codex agent during
an autonomous conjecture-resolution experiment.  The algebraic proof is
written out above for line-by-line human checking.  The artifact has not been
independently peer reviewed by a human and should not be presented as such.
