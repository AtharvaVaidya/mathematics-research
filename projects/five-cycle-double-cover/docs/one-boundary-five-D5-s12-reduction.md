# The \(D_5\) reduction for \(s=1,2\)

Status: **human-checkable switching and minimality proof plus two
independently implemented boundary-relation solvers over one exact
incidence generator; eliminates every \(s=1\) and \(s=2\) outside in the
one-boundary-five branch; does not resolve Five-CDC**.

## 1. Setup

Assume a standard Five-Cycle Double Cover counterexample exists, and let
\(G\) be one of minimum order among bridgeless cubic multigraphs.  The
elementary [reduction ledger](reductions.md) makes \(G\) simple and
cyclically 4-edge-connected.

In the one-boundary-five Gallai--Edmonds branch, write \(Q\) for the
nontrivial factor-critical shore and \(O=G-Q\).  If \(s=|A|\), then

\[
 |V(O)|=2s+5.
\]

The five cut edges have distinct endpoints in \(Q\): a nontrivial
connected factor-critical graph has no bridge and minimum degree at
least two, while \(G\) is cubic.

A \(D_5\)-labelling assigns to every edge one of the ten two-subsets of
\([5]\).  At every vertex, the symmetric difference of its incident
labels must be empty.  This is equivalent to five Eulerian edge sets
which cover every edge exactly twice.  At a cubic vertex, the three
labels are exactly

\[
                 ab,\quad ac,\quad bc
\]

for three distinct coordinates \(a,b,c\).

Fix the order of the five cut edges.  Let \(\mathcal R_Q\) and
\(\mathcal R_O\) be the corresponding ordered boundary relations,
quotiented by the global \(S_5\) action on coordinates.  Equal orbits
can be made literally equal by one global coordinate permutation, so

\[
       \mathcal R_Q\cap\mathcal R_O\ne\varnothing
\]

is exactly what is needed to glue a \(D_5\)-labelling of \(G\).

## 2. The switching law

For a pair of coordinates \(a,b\), take the edges and semiedges whose
labels contain exactly one of \(a,b\).  Every internal vertex has degree
zero or two in this bichromatic subgraph.  Its boundary therefore has
zero, two, or four ends.

* With two ends, they are joined by one path.  Interchanging \(a,b\)
  along that path gives another state in the same five-pole relation.
* With four ends, the actual labelling pairs them by two paths.  Either
  path can be switched separately, and their union can be switched.
  Thus one of the three pairings has both single-path outputs in the
  relation, and the four-end output is also in the relation.

These are the **elementary path-switching laws**.  For any set
\(S\) of boundary states, repeatedly delete every state which cannot
satisfy one of these laws while staying in \(S\).  The fixed point
\(\operatorname{Core}(S)\) is the greatest switching-closed subset of
\(S\).  Consequently,

\[
\mathcal R_Q\cap\mathcal R_O=\varnothing
\quad\Longrightarrow\quad
\mathcal R_Q\subseteq
\operatorname{Core}(\overline{\mathcal R_O}).       \tag{2.1}
\]

To make the greatest-core implication explicit, let \(S_0=S\) and let
\(S_{k+1}\) be the result of one simultaneous deletion round.  If a
realisable relation \(\mathcal R\) is contained in \(S_k\), the actual
bichromatic paths in a labelling witnessing each state supply every
mandatory output and one complete alternative group, all still in
\(\mathcal R\).  Hence \(\mathcal R\subseteq S_{k+1}\).  Induction gives
\(\mathcal R\subseteq S_k\) for every \(k\); the finite sequence
stabilises at \(\operatorname{Core}(S)\).  Apply this with
\(\mathcal R=\mathcal R_Q\) and
\(S=\overline{\mathcal R_O}\) to obtain (2.1).

This implication is a human proof; the finite computation below only
evaluates the core for the small outside graphs.

## 3. Two smaller caps

Two elementary caps force the boundary information needed below.

### Nonemptiness cap

Join the five terminals of \(Q\) to the five vertices of a new
5-cycle.  The result is a simple bridgeless cubic graph:

* the internal edges of \(Q\) lie on circuits in \(Q\);
* the new cycle edges lie on the cap cycle; and
* every spoke lies on a circuit made from two spokes, a path in
  connected \(Q\), and a path on the cap cycle.

For \(s\ge1\), this graph has

\[
                   |V(Q)|+5<|V(Q)|+2s+5=|V(G)|.
\]

Minimality of \(G\) therefore gives it a Five-CDC, whose restriction
shows

\[
                         \mathcal R_Q\ne\varnothing. \tag{3.1}
\]

### Compatible-pair cap

Choose two specified terminals \(e_i,e_j\).  Add a three-vertex path
\(p_0p_1p_2\).  Join \(e_i,e_j\) to \(p_0\), join one of the remaining
terminals to \(p_1\), and join the last two to \(p_2\).

The resulting graph is again simple, cubic, and bridgeless.  For an
internal path edge, each side of that edge contains at least one spoke;
choose one on each side, join their distinct terminals by a path in
connected \(Q\), and close a circuit through the cap path.  For a spoke,
choose any other spoke and use the path in \(Q\) together with the unique
cap path between their new endpoints.  If the two spokes have the same
new endpoint, the cap path has length zero and the two spokes with the
\(Q\)-path already form a circuit.  The internal \(Q\)-edges retain
their circuits.

This cap has \(|V(Q)|+3<|V(Q)|+2s+5=|V(G)|\) vertices.
Minimality supplies a Five-CDC.  At \(p_0\), the two specified spoke
labels \(A,B\) and the path label form a coordinate triangle.  Hence

\[
                 A\ne B,\qquad |A\cap B|=1,
                 \qquad A\mathbin\triangle B\in D_5.       \tag{3.2}
\]

Thus \(\mathcal R_Q\) contains a state compatible with putting those
two boundary edges at one cubic vertex.

## 4. Exhaustive outside calculation

The one-boundary-five equations give

\[
 |W|=s+4,\qquad |Z|=s+1.
\]

The only edges within \(W\) are the two independent roots.  Every other
proper edge of \(O\) joins a cubic singleton in \(Z\) to \(W\).  The
generator enumerates each \(z\in Z\) by its three-element neighbourhood
in \(W\) and quotients only the permutation of the indistinguishable
\(Z\)-vertices.  It then checks all necessary inherited conditions:

1. cubic degree and exactly five boundary incidences;
2. the strict Gallai--Edmonds Hall inequalities;
3. the bridge-side conditions inherited from bridgeless \(G\);
4. the local cyclic-four cut condition; and
5. attainability for either prescribed root.

This covers the minimum-counterexample outside rather than merely a
chosen subclass.  Label the four root endpoints, label the \(s\)
vertices of \(A\), and forget only the names of the singleton
\(Z\)-components.  The resulting multiset of three-neighbour rows is one
of the generated objects.  The strict Hall test is a
Gallai--Edmonds condition; the component and bridge-side tests are forced
by bridgelessness; every connected cyclic outside subset has cut at least
four because the opposite shore contains the circuit-containing \(Q\);
and the prescribed-edge perfect-matching theorem makes each root
attainable.  Thus none of the filters can discard the outside of \(G\).

For every retained outside, the primary program solves the ten-value
local xor constraints for all 62 ordered boundary-color orbits.  The
independent program instead enumerates all allowed local rows at every
vertex and joins those rows over shared proper edges.  It does not use
the primary finite-domain solver.  It intentionally imports the shared
structural pattern generator, so the independence claim concerns the
\(D_5\) relation and switching-core calculations, not canonical incidence
generation.

Both implementations give:

| \(s\) | boundary multiplicities | \(|\mathcal R_O|\) | \(|\operatorname{Core}(\overline{\mathcal R_O})|\) | patterns |
|---:|---:|---:|---:|---:|
| 1 | \(1+1+1+1+1\) | 58 | 0 | 2 |
| 1 | \(2+1+1+1\) | 36 | 25 | 4 |
| 2 | \(1+1+1+1+1\) | 60 | 0 | 16 |
| 2 | \(1+1+1+1+1\) | 61 | 0 | 8 |
| 2 | \(1+1+1+1+1\) | 62 | 0 | 8 |
| 2 | \(2+1+1+1\) | 36 | 25 | 32 |
| 2 | \(2+1+1+1\) | 37 | 25 | 64 |

There are therefore 6 retained \(s=1\) patterns and 128 retained
\(s=2\) patterns.

For every repeated-endpoint pattern, let positions \(i,j\) be the two
semiedges incident with the same outside vertex.  Both implementations
verify the stronger exact identity

\[
\operatorname{Core}(\overline{\mathcal R_O})
=
\{\,x:\ x_i\mathbin\triangle x_j\notin D_5\,\}.       \tag{4.1}
\]

The right side has 25 coordinate orbits.  It is precisely the local
incompatibility set: the two labels are equal or disjoint, rather than
distinct and meeting in one coordinate.

Reproduction:

```sh
shasum -a 256 -c \
  scratch/one-boundary-five-outside-relations.SHA256SUMS
python3 -B scratch/classify_one_boundary_five_outside_relations.py \
  --output /tmp/one-boundary-five-outside-relations.json
cmp /tmp/one-boundary-five-outside-relations.json \
  scratch/one-boundary-five-outside-relations.json
python3 -B \
  scratch/verify_one_boundary_five_outside_relations_independent.py \
  --output /tmp/one-boundary-five-outside-relations-independent.json
cmp /tmp/one-boundary-five-outside-relations-independent.json \
  scratch/one-boundary-five-outside-relations-independent.json
```

## 5. Elimination theorem

**Theorem.** A minimum standard Five-CDC counterexample cannot have
\(s=1\) or \(s=2\) in the one-boundary-five branch.

**Proof.**  Suppose first that the five boundary incidences of \(O\)
have distinct outside endpoints.  The table gives

\[
       \operatorname{Core}(\overline{\mathcal R_O})=\varnothing.
\]

Equation (3.1) makes \(\mathcal R_Q\) nonempty, while the switching law
makes it switching-closed.  It therefore cannot satisfy (2.1), so it
meets \(\mathcal R_O\).

Now suppose two boundary edges \(e_i,e_j\) have the same outside
endpoint.  The compatible-pair cap gives a state
\(x\in\mathcal R_Q\) with
\[
                 x_i\mathbin\triangle x_j\in D_5.
\]
By (4.1), this state is not in
\(\operatorname{Core}(\overline{\mathcal R_O})\).  Thus (2.1) again
cannot hold, and the two relations intersect.

In either case, align the common boundary orbit by a global coordinate
permutation and glue the two labellings.  This gives a \(D_5\)-labelling,
hence a standard Five-CDC, of \(G\), a contradiction. \(\square\)

The earlier triangle-cut argument excludes \(s=0\).  Combining it with
this theorem leaves only

\[
                              s\ge3
\]

in the one-boundary-five branch.

## 6. Scope and AI-use disclosure

This is a genuine reduction of the minimum-counterexample frontier, not
a resolution of Five-CDC.  It uses a finite exhaustive calculation for
the \(s=1,2\) outside relations.  The switching law, both smaller-cap
arguments, and the final implication are written above as ordinary
human-checkable proofs.

OpenAI Codex, under human direction, found the switching-core identity,
wrote both computations, and drafted this proof.  The result has not
been peer reviewed.  Any publication should rerun the artifacts,
inspect both implementations, and disclose the AI assistance according
to the venue's policy.

The \(D_5\) two-subset language, multipole boundary relations, gluing,
and bichromatic-chain switching are prior machinery; see Máčajová,
Mazzuoccolo, and Trevisan,
[*Cycle double covers of graphs with small oddness*](https://doi.org/10.26493/1855-3974.3409.c13),
Ars Mathematica Contemporanea 26 (2026), article P2.03.  The candidate
contribution here is the greatest-core use, the exact \(s=1,2\) outside
census, and the compatible-pair cap reduction.  That novelty assessment
is provisional pending specialist review.

The standard Five-Cycle Double Cover Conjecture remains open.  The
one-boundary-five branch is reduced only to \(s\ge3\), and no statement
here concerns the orientable variant.
