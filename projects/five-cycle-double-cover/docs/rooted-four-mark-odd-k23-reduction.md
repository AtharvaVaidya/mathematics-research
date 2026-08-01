# Rooted four-mark failure forces an odd-\(K_{2,3}\) graft minor

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE REDUCTION / IMPORTED PACKING THEOREM /
ODD-\(K_{2,3}\) EXCLUSION OPEN**.

This note sharpens the cross-intersection obstruction in
`rooted-four-mark-bridgeless-reduction.md`.  Once the forbidden root
edge has been deleted and the four marked edges have been subdivided,
a rooted failure is exactly a failure to pack two edge-disjoint
terminal joins.  The minimum terminal-cut is two.  The theorem of
Codato, Conforti, and Serafini therefore forces an odd-\(K_{2,3}\)
graft minor.

The reduction is universal and short.  It does **not** exclude the
minor, prove the standard rooted assertion, or resolve the
Five-Cycle Double Cover Conjecture.

## 1. Terminal form of the rooted problem

Let \(L\) be a finite connected simple cubic graph, let
\[
                       S=\{s_1,s_2,s_3,s_4\}
\]
be a four-edge matching, and let \(f\in E(L)\setminus S\).  Assume
that a failure of the standard rooted assertion, or of the inherited
opposite-cap assertion, has survived the bridge-elimination lemma in
`rooted-four-mark-bridgeless-reduction.md`.

Put \(J=L-f\), subdivide each \(s_i\) once, and call the new
degree-two vertex \(z_i\).  Write
\[
                  \widehat J,\qquad
                  Z=\{z_1,z_2,z_3,z_4\}.               \tag{1}
\]
The bridge-elimination and subcubic block lemmas say that \(J\), and
hence \(\widehat J\), is 2-connected.

A **\(Z\)-join** is an edge set whose odd-degree vertices are exactly
the members of \(Z\).

> **Terminal packing equivalence.**  The graph \(L\) has a closed
> rooted certificate avoiding \(f\) if and only if \(\widehat J\)
> has two edge-disjoint \(Z\)-joins.

### Proof

Suppose first that \(P_1,P_2\) are edge-disjoint \(Z\)-joins.  At a
terminal \(z_i\), each join has odd degree in a two-edge incidence
set, so each uses exactly one edge and the two joins use different
edges.  At a nonterminal, each join has even degree.  Since
\(\widehat J\) is subcubic and the joins are disjoint, their union
\[
                             Q=P_1\mathbin{\dot\cup}P_2 \tag{2}
\]
has degree zero or two at every vertex.  It is therefore a
vertex-disjoint union of circuits and contains every terminal.

Traverse one component of \(Q\), recording whether its successive
edges belong to \(P_1\) or \(P_2\).  The join colour is unchanged at
a nonterminal and switches at a terminal.  It must return to its
initial colour, so the component contains an even number of
terminals.  Suppressing every \(z_i\) gives a binary cycle of \(L\)
which contains all four marked edges, avoids \(f\), and has an even
number of marks on every component.

Conversely, subdivide the four marked edges in a closed rooted
certificate.  Each resulting circuit component contains an even
number of terminals.  Colour successive arcs alternately by
\(1,2\), switching colour at a terminal and retaining colour at every
other vertex.  Even terminal parity makes this consistent around
each component.  The two colour classes are edge-disjoint
\(Z\)-joins. \(\square\)

This is the four-terminal specialization of the even-marked circuit
criterion in `minimum-zero-tjoin-route.md`.

## 2. The minimum \(Z\)-cut is exactly two

A **\(Z\)-cut** is a cut \(\delta_{\widehat J}(X)\) for which
\(|X\cap Z|\) is odd.  Let
\[
 \tau(\widehat J,Z)=
 \min\{|\delta_{\widehat J}(X)|:|X\cap Z|\text{ is odd}\}. \tag{3}
\]

Because \(\widehat J\) is connected and has four terminals, an empty
cut cannot be a \(Z\)-cut.  Because it is 2-connected, it has no
bridge, so a \(Z\)-cut cannot have size one.  On the other hand, the
singleton shore \(\{z_i\}\) is \(Z\)-odd and has boundary two.
Consequently
\[
                         \tau(\widehat J,Z)=2.          \tag{4}
\]

No marked-cut inequality or colouring argument is hidden in (4).
All the global rooted hypotheses enter through the already proved
fact that deleting \(f\) leaves a bridgeless, hence 2-connected,
subcubic graph.

## 3. The forced graft minor

Codato, Conforti, and Serafini proved that the \(T\)-join clutter has
the max-flow min-cut property in every graft with no
odd-\(K_{2,3}\) graft minor:

P. Codato, M. Conforti, and C. Serafini, “Packing \(T\)-joins,”
*Journal of Graph Theory* **22** (1996), 293--296,
<https://doi.org/10.1002/(SICI)1097-0118(199608)22:4%3C293::AID-JGT2%3E3.0.CO;2-G>.

Their graft contraction convention makes a contracted vertex a
terminal precisely when its branch set contains an odd number of
original terminals.  The odd-\(K_{2,3}\) target has as terminals all
three degree-two vertices and exactly one of the two degree-three
vertices.

> **Rooted odd-\(K_{2,3}\) reduction.**  Every failure of the
> standard rooted assertion, and every failure of the inherited
> opposite-cap assertion after the bridge-elimination step, has an
> odd-\(K_{2,3}\) graft minor in
> \((\widehat J,Z)\).

### Proof

If the graft had no odd-\(K_{2,3}\) graft minor, the imported
max-flow min-cut theorem and (4) would give two edge-disjoint
\(Z\)-joins.  The terminal packing equivalence would then give a
closed rooted certificate, contrary to the assumed failure.
\(\square\)

Since \(|Z|=4\), the four odd branch sets in any such minor model each
carry exactly one original terminal; the fifth branch set carries
none.  The underlying \(K_{2,3}\) minor may be represented
topologically because \(\widehat J\) is subcubic, although extra
edges of \(\widehat J\) need not respect the five-branch interface.
That last qualification is why the marked cyclic-cut inequality does
not immediately eliminate the minor.

## 4. New exact obligation

The surviving rooted task can now be stated without an informal
cross-intersection condition:

> Exclude an odd-\(K_{2,3}\) graft minor from the 2-connected
> subcubic terminal graph \((\widehat J,Z)\) using the simultaneous
> inherited data: four pairwise vertex-disjoint private factor
> circuits, triple cyclability, the marked cyclic-cut inequality,
> the appropriate P4 endpoint condition, and the root-colour trace.

Equivalently, find a graph satisfying all those conditions and the
odd-minor obstruction, then test whether it is a genuine rooted
counterexample.  The minor is necessary, not sufficient, so detecting
one is only a candidate filter.

This formulation suggests two checkable continuations:

1. normalize a minimal odd-\(K_{2,3}\) model and prove that one of its
   three terminal-bearing degree-two branches gives a forbidden
   one-mark cyclic shore; or
2. canonically generate the five branch sets, retain only models
   satisfying all inherited conditions, and independently test the
   two-\(Z\)-join formula.

## 5. Cycle-transparent five-branch models are excluded

The first exact normalization has been exhausted.  Start with the odd
\(K_{2,3}\) whose degree-three vertices are \(X,Y\), whose degree-two
vertices are \(P,Q,R\), and whose terminal set is
\(\{X,P,Q,R\}\).  Replace each terminal branch vertex by a private
cycle containing one degree-two terminal, retain \(Y\) as one cubic
vertex, and add:

* one ordinary extra quotient edge \(E\); and
* one distinguished extra edge \(F\), which is deleted as the root.

Require each of \(P,Q,R\) to meet \(E\) or \(F\).  This is the
branch-level necessity imposed by the one-mark marked-cut inequality:
the underlying \(K_{2,3}\) gives each of those cyclic marked branches
boundary two, and the root can supply only two boundary incidences.

Two versions of the fifth, unmarked branch \(Y\) were checked: a single
cubic vertex and a private cycle with its three base attachments.  In
the second version \(E\) and \(F\) may also meet \(Y\).  Exhausting every
cyclic attachment order, with each terminal position fixed and reversal
identified, gives
\[
\begin{array}{c|r|r}
&Y\text{ a vertex}&Y\text{ a cycle}\\ \hline
\text{quotient placements}&12&18\\
\text{labelled cyclic orders}&3888&5346\\
\text{rows with a closed rooted certificate}&3726&5184\\
\text{certificate-free rows}&162&162\\
\text{certificate-free normalized Tait colourings}&162&162\\
\text{colourings with all four marks one colour}&6&6\\
\text{those with the root a different colour}&0&0.
\end{array}
\]

The last six rows have a short parity explanation.  Up to symmetry,
\(E\) joins \(X\) to \(P\), while the root \(F\) joins \(Q\) to \(R\).
Each low branch has a three-edge boundary, so the three boundary edges
have distinct Tait colours.  The three edges at \(Y\) also have
distinct colours.  Since \(F\) occurs in both the \(Q\)- and
\(R\)-boundaries, its colour must equal the colour of the \(Y\)-to-\(P\)
edge.  In every certificate-free cyclic order with common-colour marks,
the marked edge of the \(P\)-triangle is opposite that \(Y\)-to-\(P\)
edge.  Opposite external and internal edges of a Tait-coloured
triangle have the same colour.  Thus
\[
                         \phi(F)=\phi(s_P),             \tag{5}
\]
contrary to the inherited root-colour hypothesis.

The complete generator, counts, twelve graph6 controls, source hash,
independently written control checker, and scope warning are frozen in
`scratch/odd-k23-cycle-expansion-result.json`.

This excludes only cycle-transparent branch sets.  An arbitrary
odd-\(K_{2,3}\) graft minor may have nontrivial connected branch sets,
deleted cross edges, and local two-join routing failures.  Proving that
the inherited private-circuit/P4 data reduce those branch sets to the
transparent case is the remaining step.

## 6. The first nontransparent chord move is certificate-producing

There is one especially small way to make a transparent branch set
nontransparent while preserving cubicity.  Start with any of the 162
certificate-free rows in either \(Y\)-mode.  In one private cycle
branch, choose two nonadjacent external attachment vertices, remove
their two external edges, join the former attachment vertices by a
chord, subdivide two distinct unmarked internal cycle edges, and
reattach the external edges at the new subdivision vertices.

Every eligible move occurs in the \(X\)-branch: in the certificate-free
base rows the three low branches and the optional \(Y\)-branch are
triangles.  Exhausting both orders of the two chosen internal edges and
deduplicating the resulting marked rooted graphs gives 3,240 variants.
Every one has an explicit closed rooted certificate.  More precisely,
\[
\begin{array}{c|c|c|r}
Y\text{ mode}&|V|&\text{number of certificates}&
                 \text{number of rows}\\ \hline
\text{vertex}&16&1&1350\\
\text{vertex}&16&2&270\\
\text{cycle}&18&2&1350\\
\text{cycle}&18&4&270.
\end{array}
\]

The generator writes one certificate per row.  A separate
standard-library checker decodes every graph6 record and verifies
directly that the displayed edge set is Eulerian, contains all four
marks, avoids the root, and has an even number of marks on every
nonempty component.  The frozen counts, source hashes, 3,240-record
certificate bundle, and exact commands are in
`scratch/odd-k23-one-chord-result.json`.

This is again a finite structured exclusion, not a normalization
theorem.  In particular it does not cover branch sets with two chords,
trees attached to more than one private circuit, or deleted
inter-branch edges.

## 7. Two chord moves expose both global gates

Applying the same chord-relocation move a second time is the first
declared class in which compatible rooted failures appear.  The first
layer has 3,888 labelled branch-decomposition states (3,240 distinct
marked rooted graphs).  After the second layer is deduplicated by the
exact graph6, marks, and root, there are 396,360 graphs.  Both moves
occur in the \(X\)-branch.  The exact filter gives
\[
\begin{array}{l|r}
\text{class}&\text{number}\\ \hline
\text{non-Tait graphs}&2592\\
\text{Tait graphs}&393768\\
\text{graphs with a compatible mark/root colouring}&20306\\
\text{compatible graphs with a closed rooted certificate}&20194\\
\text{compatible certificate-free graphs}&112.
\end{array}
\]

All 112 apparent failures violate universal factor separation.  There
are 56 of order 18 and 56 of order 20.  Each has exactly two normalized
Tait colourings, exactly one compatible colouring, and every one of the
six marked pairs occurs together on a bichromatic factor circuit in
at least one colouring.  They also all violate the marked cyclic-cut
inequality: every row has one cyclic two-cut whose small shore contains
one mark and at least one unmarked cyclic three-cut.  The cycle-\(Y\)
rows have two such three-cuts.

An independently written standard-library checker decodes the 112
controls, enumerates all their normalized Tait colourings and complete
binary cycle spaces, and confirms all three statements: there is no
closed rooted certificate, universal separation fails, and the stated
complete list of low cyclic-cut violations is present.  The controls,
hashes, exact command, counts, and scope warning are frozen in
`scratch/odd-k23-two-chord-result.json`.

The rooted linkage conclusion is therefore false in this small branch
class under compatible colouring alone, but the class does not isolate
which global hypothesis repairs it: universal separation and the
marked-cut inequality both remove every failure.  The next normalization
must permit the one-mark branch to acquire at least two additional
boundary incidences before it can test the genuinely simultaneous case.

## 8. Every direct cubic repair regains a certificate

The one-mark cyclic two-cut can be repaired without adding vertices.
For each of the 112 two-chord failures, choose an unmarked nonroot
internal edge on the bad shore and one on its complement.  Delete both
edges and add either cross pairing of their four ends.  Whenever the
result is simple, this is a cubic 2-switch and raises the displayed
shore boundary from two to four.

Exhausting all such choices and deduplicating the exact marked rooted
graphs gives 15,008 repairs:
\[
\begin{array}{l|r}
\text{class}&\text{number}\\ \hline
\text{non-Tait}&504\\
\text{Tait, but no compatible colouring}&6608\\
\text{compatible common-mark/different-root colouring}&7896.
\end{array}
\]
Every one of the 7,896 compatible repairs has a closed rooted
certificate.  The generator writes one explicit certificate per graph;
a project-independent standard-library checker verifies directly that
each edge set is Eulerian, contains all four marks, avoids the root, and
has even marked parity on every component.

The 2,541,910-byte certificate bundle, hashes, commands, and scope
warning are frozen in
`scratch/odd-k23-two-cut-repair-result.json`.  This does not prove that
every abstract repair of an odd-\(K_{2,3}\) model works.  It does show
that, throughout the first exact failure family, eliminating the actual
one-mark cut restores the desired linkage rather than producing a
hidden full-hypothesis obstruction.

## AI-use disclosure

OpenAI Codex, under human direction, noticed and wrote this application
of the Codato--Conforti--Serafini theorem.  The elementary equivalence,
the terminal-cut calculation, and the contrapositive application are
displayed in full for human checking.  The packing theorem itself is
an imported published result.  No conjecture-resolution claim is made.
