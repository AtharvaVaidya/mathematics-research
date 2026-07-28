# Endpoint rescue for Johnson-labeled transfer trees

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE ABSTRACT TREE THEOREM / GRAPH LIFT REQUIRES
THE TRANSFER-CELL HYPOTHESIS / NOT A FIVECDC RESOLUTION**.

## 1. Tree model

Let \(T\) be a finite tree and
\[
                          \phi:V(T)\longrightarrow J(5,2)
\]
a graph homomorphism.  Thus labels on adjacent tree vertices are
distinct weight-two subsets sharing one coordinate.

Fix two marked vertices \(r,s\).  For a coordinate transposition
\(\tau\), call a tree vertex active when its label contains exactly one
coordinate moved by \(\tau\).

An **endpoint tree move** chooses \(\tau\) active at \(r\) or \(s\),
takes the connected component of active tree vertices containing that
endpoint, and applies \(\tau\) to every label in the component.  This
preserves the homomorphism: \(\tau\) is an automorphism of \(J(5,2)\),
and every label just outside the moved component is inactive and hence
fixed by \(\tau\).

## 2. Path projection

Let
\[
                         P=(v_0=r,v_1,\ldots,v_k=s)
\]
be the unique marked path.

**Path projection lemma.**  The restriction of an \(r\)-move to \(P\)
is the corresponding transposition on the maximal active prefix of
\[
                       \phi(v_0),\phi(v_1),\ldots,\phi(v_k).
\]
The restriction of an \(s\)-move is the maximal active suffix.

**Proof.**  The active component containing \(r\) contains
\(v_0,\ldots,v_j\) exactly until the first inactive path vertex.  It may
also contain active off-path branches, but the tree has no route around
that inactive vertex.  Hence its path intersection is precisely the
maximal active prefix.  The suffix case is symmetric. \(\square\)

The off-path branches therefore never obstruct a prescribed endpoint
move.  They are transposed along with the path component and remain
validly labeled.

## 3. Tree rescue theorem

**Theorem.**  Every finite \(J(5,2)\)-labeled tree with two marked
vertices has an endpoint-move sequence after which one coordinate pair
is active at every vertex of the marked path.

**Proof.**  Apply the Johnson-walk alternation theorem from
`d5-capped-ladder-exact-lifting-and-eventual-rescue.md` to the label
word on \(P\).  Realize each prescribed prefix or suffix move as the
corresponding endpoint tree move.  The path projection lemma guarantees
the same path evolution, regardless of what happens in off-path
branches.

The final path alternates between adjacent labels \(A,B\).  Their
symmetric difference \(A+B\) is a coordinate pair active on both, hence
on every path vertex. \(\square\)

## 4. Transfer-cell reducibility criterion

This abstract theorem lifts to a graph theorem under the following
checkable hypothesis.

Call a two-edge-cut decomposition a **Johnson transfer tree** when:

1. its block incidence graph is a tree;
2. every port consists of a two-edge cut and therefore has one common
   \(D_5\) label;
3. adjacent port/root labels form edges of \(J(5,2)\);
4. for every factor, a rooted factor component traverses exactly the
   connected active port component in the block tree;
5. if one factor is active on every vertex of the marked block-tree
   path, its lifted component contains both graph roots.

**Corollary.**  Every rooted state admitting a Johnson transfer-tree
decomposition is reducible by root-component switches.

For a subcubic transfer tree, condition 4 has a natural local form.  A
three-port cell sees an even number of active ports.  When two are
active, they must be joined by the factor transfer path; an off-path
active pair produces a U-turn into its branch.  Verifying this
two-active-port connectivity for each proposed cell is the remaining
graph-specific obligation.

The capped ladder is the path case, where the cell and cap transfer
lemmas prove conditions 3--5 directly.  The theorem now shows that
branching of the abstract transfer network causes no new word
obstruction.  A genuine counterexample must violate the local transfer
property, contain a cycle of transfer blocks, or lack such a
two-edge-cut decomposition.

## 5. Verification

Run

```text
python3 scratch/check_d5_johnson_transfer_tree_rescue.py
```

The checker enumerates every labeled tree on two through five vertices
using Prüfer codes, fixes the marked vertices to \(0,n-1\), exhausts
every normalized \(J(5,2)\)-homomorphism, lifts the constructive path
plan to active tree components, and verifies the final through-factor.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the tree move,
proved the path projection and rescue theorems, implemented the
exhaustive checker, and isolated the graph-cell transfer hypothesis.
This is not peer review and is not a resolution of FiveCDC.
