# Exact \(D_5\) multipole macro-network frontier

## Status

**EXACT SMALL-NETWORK NO-GO / LARGER FRONTIER OPEN / NO FIVECDC
COUNTEREXAMPLE.**

Treating sharp poles as exact boundary constraints does not produce an
obstruction in the complete macro-network ranges through four
four-poles.  Every loopless connected bridgeless cubic gluing of

- two \(C_5\) five-poles and no four-pole; or
- two \(C_5\) five-poles and one, two, three, or four of the four proper
  small four-pole relations

has a standard five-cycle double cover.

With one four-pole, every such graph is actually Tait-colourable.  With
no four-pole, ten of the 120 labelled terminal pairings are non-Tait, but
all ten still have directly checked standard 5-CDCs.

With two four-poles, an independent combinatorial count gives 4,466,880
loopless labelled pairing leaves and 4,435,200 connected bridgeless
pairings for each underlying atom-type pattern.  Canonicalization reduces
the three patterns to 1,861 expanded-graph isomorphism classes.  Twelve
are non-Tait; all 1,861 have directly checked standard 5-CDCs.

With three four-poles, exact boundary-relation dynamic programming
reduces the full terminal-order search to 197,568 canonical states.
Every state has nonempty \(D_5\) relation.

With four four-poles, the same exact reduction exhausts 4,293,072
canonical boundary states.  Again, every state has nonempty relation.

No empty exact \(D_5\) relation was found, so there is no graph for which
an UNSAT LRAT should be generated.

## 1. Exact atom relations

Let

\[
                       D_5=\binom{[5]}2.
\]

At every cubic vertex, the three incident labels must xor to zero.  The
independent replay reconstructs each relation directly from its proper
graph; it does not import the large pole census.

### Five-pole atom

The five-pole is a 5-cycle whose five vertices are terminals.  Its exact
relation contains

\[
                         4{,}620
\]

ordered boundary words, forming 46 orbits under the global \(S_5\)
action on cover coordinates.  This is the sharp \(C_5\)-cap relation.

### Four-pole atoms

There are ten four-boundary color orbits.  Through order 14, the four
proper internally bridgeless relations are the masks

\[
             0x3ef,\qquad0x3f7,\qquad0x3fd,\qquad0x3fe.
\]

Each admits nine of the ten orbits.

They require only two underlying proper graphs:

- graph6 `C]`, which is \(K_{2,2}\), realizes the first three masks
  under its three terminal-order classes; and
- graph6 `ECxo` realizes `0x3fe`, invariant under every terminal
  permutation.

The checker enumerates all xor-zero boundary words, solves the internal
edge-label equations by direct propagation and backtracking, and obtains
these masks independently.

## 2. Macro-network model

Take disjoint atom copies.  Pair every terminal with a terminal of a
different atom and add one joining edge per pair.  Retain only pairings
whose macro multigraph is connected and has no bridge.

Because each atom is internally bridgeless, the expanded proper graph is
connected and bridgeless.  Because every terminal is used once and
connections run between distinct atoms, it is also simple and cubic.

A label on a joining edge is the shared CSP variable for its two atom
ports.  The network has a standard 5-CDC exactly when the conjunction of
the atom boundary relations is nonempty.  The search checks the
equivalent fully expanded graph formula:

- five Boolean membership variables per edge;
- exactly two true variables on every edge; and
- even coordinate incidence at every vertex.

Every SAT model is checked directly: every edge has weight two and every
vertex has xor zero.  Tait models are likewise checked edge by edge and
vertex by vertex.  Solver trust is therefore used only to discover
positive assignments, not to validate their semantics.

## 3. Exact pairing theorem

### Two five-poles

Pairing the five ports of one \(C_5\) atom with the five ports of the
other gives

\[
                            5!=120
\]

labelled pairings.  All macrographs are the bridgeless five-edge dipole.
The exact enumeration finds:

\[
\begin{array}{c|r}
\text{outcome}&\text{pairings}\\ \hline
\text{Tait-colourable}&110\\
\text{non-Tait but standard 5-CDC}&10\\
\text{FiveCDC UNSAT}&0.
\end{array}
\]

### Add one four-pole

The only loopless macro multiplicities are three edges between the two
five-poles and two edges from each five-pole to the four-pole.  Exhausting
the labelled port bijections gives 14,400 pairings for either underlying
four-pole atom.

\[
\begin{array}{c|r|r|r}
\text{four-pole atom}&\text{pairings}&\text{non-Tait}&
 \text{FiveCDC UNSAT}\\ \hline
\texttt{C]}&14{,}400&0&0\\
\texttt{ECxo}&14{,}400&0&0.
\end{array}
\]

Port permutations of `C]` cover all three of its proper relation masks;
`ECxo` covers the fourth.  Thus the enumeration includes all four sharp
four-pole constraints, not just two selected terminal orders.

### Add two four-poles

There are 4,466,880 labelled perfect matchings of terminal sets of sizes
\(5,5,4,4\) when same-atom pairs are forbidden.  Solving the six macro
multiplicities subject to row sums \(5,5,4,4\), then deleting a single
edge of each positive type to test for a bridge, gives exactly 12
connected bridgeless macro multiplicity matrices.  Their labelled lifts
sum to

\[
                         4{,}435{,}200.
\]

Both counts are independently recomputed by the Python replay.  The C++
generator expands every accepted labelled pairing, and nauty `shortg`
removes graph isomorphs.  There are three underlying four-pole type
patterns:

\[
\begin{array}{c|r|r|r|r}
\text{four-pole atoms}&\text{labelled pairings}&
\text{graph classes}&\text{non-Tait}&\text{FiveCDC UNSAT}\\ \hline
\texttt{C]}+\texttt{C]}&4{,}435{,}200&252&2&0\\
\texttt{C]}+\texttt{ECxo}&4{,}435{,}200&765&4&0\\
\texttt{ECxo}+\texttt{ECxo}&4{,}435{,}200&844&6&0.
\end{array}
\]

The checker independently parses every canonical graph, verifies
simplicity, cubicity, connectedness, and bridgelessness, then solves the
fully expanded Tait and FiveCDC formulas.  It checks the returned
FiveCDC label on every edge and xors the three labels at every vertex.
Thus the 12 non-Tait classes are not accepted through the Tait
implication; each has an explicit weight-two, vertex-even FiveCDC model.
Their canonical graph6 encodings and edge-label masks are frozen in
`scratch/d5-multipole-macronetwork-frontier2-nontait-witnesses.json`;
the Python replay verifies these witnesses without calling a solver and
separately confirms non-Taitness with an exact three-edge-colouring
backtracker.

The three `C]` masks differ only by a permutation of its four ports.
Relabelling those ports is a bijection of the exhaustive labelled
pairing set.  Consequently the three underlying type patterns cover all
ten unordered choices, with repetition, of two relations from the four
sharp masks.

### Add three four-poles

The degree sequence of the five-atom macrograph is

\[
                          (5,5,4,4,4).
\]

Direct integer enumeration gives 178 labelled connected bridgeless
macro multiplicity matrices.  Quotienting by type-preserving atom
permutations leaves 25 macro classes when all three four-poles have the
same underlying atom type and 56 classes in either mixed type pattern.

The exact ordered boundary relations and their terminal stabilizers are

\[
\begin{array}{c|r|r|r}
\text{atom}&\text{relation words}&\text{stabilizer}&
\text{terminal-bijection orbits}\\ \hline
C_5&4{,}620&10&5!/10=12\\
\texttt{C]}&580&8&4!/8=3\\
\texttt{ECxo}&630&24&4!/24=1.
\end{array}
\]

For each atom, a terminal-to-labelled-half-edge bijection is quotiented
independently by its exact relation stabilizer.  Every original port
assignment is equivalent to exactly one of these local orbits up to
possible harmless duplication from parallel-edge names.  Combining
these local states with the canonical macro matrices gives:

\[
\begin{array}{c|r|r|r}
\text{four-pole mode}&\text{macro classes}&
\text{boundary-CSP states}&\text{empty }D_5\\ \hline
AAA&25&97{,}200&0\\
AAB&56&72{,}576&0\\
ABB&56&24{,}192&0\\
BBB&25&3{,}600&0\\ \hline
\text{total}&&197{,}568&0.
\end{array}
\]

Here \(A=\texttt{C]}\) and \(B=\texttt{ECxo}\).  Each local relation is
stored as a Boolean extension table indexed by an ordered partial
boundary word, using an eleventh value for “unassigned.”  The CSP search
assigns the 11 joining-edge labels and prunes exactly when one incident
partial word has no extension.  A completed state is accepted only when
all five full boundary words belong to their reconstructed exact
relations.

As before, port permutations of \(A\) cover its three sharp masks.
Thus `AAA`, `AAB`, `ABB`, and `BBB` cover every multiset of three
relations from the four sharp masks.  No expanded graph is needed to
justify a positive result: membership in each exact atom relation
supplies compatible internal labels, and the shared joining-edge labels
then give a FiveCDC labeling of the expansion.

### Add four four-poles

For macro degree sequence

\[
                         (5,5,4,4,4,4),
\]

there are 4,222 labelled connected bridgeless multiplicity matrices.
Canonicalization and exact boundary DP give:

\[
\begin{array}{c|r|r|r}
\text{four-pole mode}&\text{macro classes}&
\text{boundary-CSP states}&\text{empty }D_5\\ \hline
AAAA&143&1{,}667{,}952&0\\
AAAB&410&1{,}594{,}080&0\\
AABB&643&833{,}328&0\\
ABBB&410&177{,}120&0\\
BBBB&143&20{,}592&0\\ \hline
\text{total}&&4{,}293{,}072&0.
\end{array}
\]

The five modes cover every multiset of four sharp relations by the same
local port-relabelling argument.  The Python replay independently
reconstructs all 4,222 macro matrices and the five canonical macro
counts before invoking the C++ boundary solver.

This is the sharp exact no-go currently proved:

> No loopless connected bridgeless cubic macro-network made from exactly
> two sharp \(C_5\) five-poles and at most four of the four proper
> order-\(\le14\) four-pole relations has empty exact \(D_5\) relation.

## 4. Larger deterministic diagnostics

Three deterministic discovery runs additionally sampled 27,971 connected
bridgeless macro-networks:

\[
\begin{array}{c|c|r|r}
\text{five-poles}&\text{four-pole range/type}&\text{accepted}&
\text{non-Tait}\\ \hline
2&0\ldots30,\ \text{mixed}&9{,}390&15\\
4&0\ldots30,\ \text{mixed}&8{,}927&2\\
2&1\ldots40,\ \texttt{ECxo}\text{ only}&9{,}654&4.
\end{array}
\]

Every one of the 21 non-Tait graphs in these frozen runs has a directly
checked standard 5-CDC.  These rows are diagnostics, not exhaustive
theorems.

Earlier exploratory seeds examined tens of thousands of further
networks with the same outcome.  They are deliberately excluded from the
formal count above because only the three displayed seeds are frozen.

## 5. Surviving obstruction

Within the loopless macrograph model, the first unresolved exact range
has at least five four-pole atoms, or at least four five-pole atoms.
Labelled pairing enumeration grows too quickly there without quotienting
simultaneously by

- macrograph isomorphism;
- the dihedral terminal action of the \(C_5\) relation;
- the three terminal-order classes of `C]`; and
- the full terminal symmetry of `ECxo`.

No semigroup-wide preserved satisfiability invariant was proved.  In
particular, “all generated graphs are Tait-colourable” is false: the
exact two-\(C_5\) range contains ten non-Tait pairings before four-poles,
the two-four-pole frontier contains 12 non-Tait graph classes, and the
larger diagnostics contain another 21.

The next sound search should canonically enumerate macro multigraphs and
quotient port assignments by these local stabilizers, then run the exact
relation CSP.  If an empty relation appears, the fully expanded graph
must immediately be sent to the standard FiveCDC CNF/XOR encoder and an
independently checked LRAT, as required by the project protocol.

This search also excludes a macro-loop that joins two terminals of the
same atom.  Some such completions can still expand to simple bridgeless
graphs, so allowing macro-loops is a separate unresolved range rather
than a consequence of the theorem above.

## 6. Replay

Run the exact relation reconstruction and labelled-pairing census with:

```sh
python3 scratch/check_d5_multipole_macronetwork_frontier.py
```

Include the three deterministic larger diagnostics with:

```sh
python3 scratch/check_d5_multipole_macronetwork_frontier.py --random
```

Regenerate and verify the complete two-four-pole frontier with:

```sh
python3 scratch/check_d5_multipole_macronetwork_frontier.py --frontier2
```

Reconstruct and exhaust the three-four-pole boundary-DP frontier with:

```sh
python3 scratch/check_d5_multipole_macronetwork_frontier.py --frontier3
```

Run the four-four-pole frontier, with its five atom modes evaluated in
parallel, using:

```sh
python3 scratch/check_d5_multipole_macronetwork_frontier.py --frontier4
```

This longer replay compiles
`scratch/generate_d5_frontier2_graphs.cpp`, canonicalizes its exhaustive
streams with nauty `shortg`, and passes all representatives to
`scratch/check_d5_frontier2_graphs.cpp`.  The latter is linked against
CaDiCaL but directly verifies every returned positive model.  The
emitted non-Tait witnesses must exactly match the frozen witness file.
The three-four-pole replay compiles
`scratch/search_d5_frontier3_boundary.cpp`; Python independently
recomputes the relation stabilizer sizes and the canonical macro counts.
The analogous four-pole program is
`scratch/search_d5_frontier4_boundary.cpp`.
The earlier ranges use `scratch/search_d5_multipole_macronetwork.cpp`.

## 7. Scope and AI disclosure

This package supplies a finite no-go through four sharp four-poles and a
precise next obstruction.  It does not cover macro-loops, does not
establish satisfiability of the full generated semigroup, and does not
disprove FiveCDC.

OpenAI Codex agents, under human direction, designed the boundary-CSP
search, wrote the programs, ran the enumerations, and drafted this note.
All exact claims reduce to the explicit atoms, finite relation
reconstruction, exhaustive labelled pairing loops, and direct semantic
checking of positive models.  Independent human review remains required
before publication.
