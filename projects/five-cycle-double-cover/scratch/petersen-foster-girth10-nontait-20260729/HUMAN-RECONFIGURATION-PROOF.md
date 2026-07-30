# Human proof of the flow and reconfiguration audit

## Scope and terminology

This note concerns two different move graphs.

A **fixed-value Eulerian-support move** chooses a nonzero
\(a\in\mathbb F_2^3\) and an Eulerian edge-subset \(C\), then replaces
\(f(e)\) by \(f(e)+a\) for \(e\in C\).  The move is legal when no resulting
edge value is zero.  The support can be disconnected.

A **connected simple-cycle move** imposes the additional requirement that
\(C\) be one simple cycle.  This is the move used in the
Cranston--Li--Su--Wang--Xu reconfiguration setting.  These notions are not
interchanged below.

For the two displayed flows, the exact legal Eulerian-support distance is
five.  The five certified supports are disconnected, so this does **not**
prove that the connected-simple-cycle distance is five.  Decomposing the five
supports into their 63 simple-cycle components proves only

\[
  5\ \leq\ d_{\rm connected\ cycle}\ \leq\ 63.
\]

## The two flows

All edge-indexed data use graph6 edge order.  The frozen Jaeger state at
root 0 and seed 211 is a word of length 1,332 over \(\{0,1,2\}\), with 444
occurrences of each symbol.  A symbol \(i\) says that the corresponding
non-root edge is omitted from tree \(T_i\).  Tree \(T_i\) also contains root
spoke \(i\).  Direct reconstruction proves that all three sets are spanning
trees.

For a spanning tree \(T\) on an even number of vertices, let \(K(T)\) contain
the tree edges whose deletion leaves an odd component.  The three frozen
trees have

\[
             (|K(T_0)|,|K(T_1)|,|K(T_2)|)=(506,507,526).
\]

Define

\[
 f(e)=\sum_{\{i:e\notin K(T_i)\}}2^i.
\]

The checker verifies \(f(e)\ne0\) on all 1,335 edges and verifies
\(f(e_1)+f(e_2)+f(e_3)=0\) at every cubic vertex.  Thus \(f\) is a
nowhere-zero \(\mathbb F_2^3\)-flow.  Its value counts are

```text
1:148  2:152  3:226  4:140  5:219  6:214  7:236
```

Its Hušek--Šámal defect profile is

```text
(174,192,138,184,130,140,110).
```

Every entry is positive, so this particular flow is H--S-bad.  The
independent parallel component-span calculation also gives zero successful
flags.

The target flow \(g\) comes directly from the attached FiveCDC.  Assign its
five coordinates the distinct points

```text
(0,1,2,3,4) in F_2^3.
```

An edge with pair label \(\{i,j\}\) receives \(g(e)=p_i+p_j\).  Distinctness
of the points makes every edge value nonzero.  Eulerian parity of each cover
coordinate makes the vertex sums zero.  Direct component counting gives

```text
(142,160,132,0,148,130,150).
```

Hence \(g\) is H--S-good.

## Zero-allowing distance

Put \(h=f+g\), edgewise.  Its values span all of \(\mathbb F_2^3\), so their
rank is three.

If \(k\) fixed-value moves with constants \(a_1,\ldots,a_k\) transform \(f\)
to \(g\), then every \(h(e)\) is a sum of a subset of the \(a_i\).  Thus
\(\operatorname{rank}\{h(e)\}\le k\).  Conversely, for a basis of the
difference-value span, take the edge-set on which each basis coordinate of
\(h\) is one.  Because \(h\) is a flow, each such set is Eulerian.  If zero
intermediate values are allowed, these three moves reach \(g\).

Therefore the zero-allowing fixed-value Eulerian-support distance is exactly
three.

## Why no legal path has three moves

Any three move constants must form an ordered basis of
\(\mathbb F_2^3\).  For a fixed ordered basis, the membership of every edge
in the three supports is the unique coordinate vector of \(h(e)\).  There
are

\[
             |\mathrm{GL}(3,2)|=168
\]

ordered bases.  The verifier exhausts all 168 forced factorizations, checks
their Eulerian supports, and finds that every ordering creates a zero edge at
an intermediate stage.  This covers every possible legal three-move
Eulerian-support path.

## Why no legal path has four moves

The four nonzero constants must still span rank three.  The verifier
exhausts all 1,848 ordered rank-three four-tuples, including repeated
constants.

Fix one tuple and let

\[
 A:\mathbb F_2^4\longrightarrow\mathbb F_2^3,\qquad
 A(z)=\sum_{j=1}^4 z_j a_j.
\]

Its kernel is \(\{0,d\}\) for one nonzero \(d\).  Choose a linear right
inverse \(p\) of \(A\).  For every edge, the only two membership words that
give the required final difference are

\[
                       p(h(e)),\qquad p(h(e))+d.
\]

Write the choice as \(p(h(e))+t_e d\).  Since \(p\) is linear and \(h\) is a
flow, every base coordinate support from \(p(h)\) is Eulerian.  Consequently
all four move supports are Eulerian if and only if

\[
                         T=\{e:t_e=1\}
\]

is Eulerian.  The forward implication uses any coordinate where \(d_j=1\);
the reverse implication is immediate in every coordinate.

Legality along the ordered prefixes is edge-local.  It leaves each \(t_e\)
forced to zero, forced to one, free, or impossible.  If any edge is
impossible, the tuple is blocked.  Otherwise the forced-one edges prescribe
a boundary, and the free edges must contain a join for that boundary.  Such
a join exists exactly when every connected component of the free-edge
subgraph contains an even number of prescribed odd vertices: necessity is
the handshake lemma, and sufficiency follows by solving upward on a spanning
tree of each component.

The exact enumeration finds:

```text
ordered rank-three four-tuples                 1848
tuples having an edge-local blocker            1176
remaining tuples blocked by component parity    672
legal four-move paths                              0
```

This is an exhaustive proof for arbitrary Eulerian supports, not just for
the five supports later displayed.

## The legal five-move path

The constants are

```text
(5,1,6,2,7).
```

The five supports are stored as exact edge bitmasks in
`reconfiguration-certificate.json`.  Their sizes are

```text
(566,608,565,610,604).
```

The verifier checks even degree at every vertex, applies every move, checks
that no intermediate edge is zero, and obtains exactly \(g\).  The
intermediate H--S profiles are

```text
(140,186,144,156,114,180,112)
(148,172,112,158,114,182,136)
(170,132,124,132,180,178,152)
(136,106,186,132,180,164,128)
(142,160,132,  0,148,130,150)
```

The lower bound above and this path prove

\[
 d_{\rm legal,\ Eulerian\ support}(f,g)=5.
\]

The support component counts are \((14,11,10,14,14)\).  Every component is
a simple cycle; their lengths are printed by the verifier.  Since a legal
Eulerian move avoids its switch value on every support edge, its disjoint
cycle components can be applied one at a time without creating zero.  This
gives the separate connected-cycle upper bound 63, but not equality.

## Exact Jaeger neighbourhood

For each pair of coordinates \(i<j\), a reciprocal exchange swaps the omitted
classes of an \(i\)-edge and a \(j\)-edge.  In tree \(T_i\), adding its
currently omitted edge creates a unique fundamental cycle; deleting the
other edge preserves a tree exactly when that other edge lies on the cycle.
The same condition is required reciprocally in \(T_j\).  Rooting each tree
turns membership in a fundamental cycle into the test that the endpoints of
the inserted edge lie on opposite sides of the deleted tree-edge cut.

The standard-library checker applies this cut test to all
\(3\cdot444^2=591{,}408\) candidate pairs.  Exactly 2,640 are legal.  It
recomputes both changed odd kernels and the full seven-entry profile for
every legal neighbour.  Of these, 822 have lexicographically smaller

\[
             \Psi=(d_{\min},|K_0|+|K_1|+|K_2|).
\]

The smallest neighbour potential is \((92,1533)\), first reached by local
swap \((545,1194)\), with profile

```text
(180,184,114,184,130,146,92).
```

The starting state has \(d_{\min}=110>0\) and zero parallel-success flags, so
it is not already terminal.  A lower neighbour exists.  Its exact augmented
escape distance is therefore one.  This is a positive calibration, not a
local trap and not a FiveCDC obstruction.

## Trust boundary

`verify_reconfiguration.py` imports only the adjacent deterministic graph
constructor and the Python standard library.  It does not call Z3, CaDiCaL,
or the discovery program.  It reads the solver-discovered frozen witness,
but does not trust a stored solver verdict: every support and intermediate
flow is checked literally, while short-path nonexistence and all 2,640
neighbour evaluations are recomputed.

OpenAI Codex agents, under human direction, generated the Jaeger state and
five-move witness, designed the finite audits, wrote the checker, and drafted
this proof.  No claim here resolves FiveCDC, and no independent human review
is represented.
