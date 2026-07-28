# Exact \(D_5\) multipole macro-network frontier

## Status

**EXACT SMALL-NETWORK NO-GO / LARGER FRONTIER OPEN / NO FIVECDC
COUNTEREXAMPLE.**

Treating sharp poles as exact boundary constraints does not produce an
obstruction in the first complete macro-network range.  Every connected
bridgeless cubic gluing of

- two \(C_5\) five-poles and no four-pole; or
- two \(C_5\) five-poles and one of the four proper small four-pole
  relations

has a standard five-cycle double cover.

With one four-pole, every such graph is actually Tait-colourable.  With
no four-pole, ten of the 120 labelled terminal pairings are non-Tait, but
all ten still have directly checked standard 5-CDCs.

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

## 3. Exact labelled-pairing theorem

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

This is the sharp exact no-go currently proved:

> No connected bridgeless cubic macro-network made from exactly two
> sharp \(C_5\) five-poles and at most one of the four proper
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
has at least two four-pole atoms, or at least four five-pole atoms.
Labelled pairing enumeration grows too quickly there without quotienting
simultaneously by

- macrograph isomorphism;
- the dihedral terminal action of the \(C_5\) relation;
- the three terminal-order classes of `C]`; and
- the full terminal symmetry of `ECxo`.

No semigroup-wide preserved satisfiability invariant was proved.  In
particular, “all generated graphs are Tait-colourable” is false: the
exact two-\(C_5\) range already contains ten non-Tait pairings, and the
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

The checker compiles
`scratch/search_d5_multipole_macronetwork.cpp` against CaDiCaL, but
directly verifies every returned positive model.

## 7. Scope and AI disclosure

This package supplies a finite no-go and a precise next obstruction.  It
does not cover macro-loops, does not establish satisfiability of the full
generated semigroup, and does not disprove FiveCDC.

OpenAI Codex agents, under human direction, designed the boundary-CSP
search, wrote the programs, ran the enumerations, and drafted this note.
All exact claims reduce to the explicit atoms, finite relation
reconstruction, exhaustive labelled pairing loops, and direct semantic
checking of positive models.  Independent human review remains required
before publication.
