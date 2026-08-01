# Strict Oum one-switch audit, 2026-07-28

## Result

The unrestricted one-circuit countermodel does **not** survive the retained
cyclically \(4\)-edge-connected tests.

On all seven retained order-34 strong snarks, the seeded sampler accepted
500 distinct nowhere-zero \(\mathbb F_2^3\)-flows per graph.  Of the 3,500
flows, 1,528 admit no Oum-compatible eight-cover whose coordinate
co-occurrence graph is five-colourable.  Every one of those 1,528 flows has
a legal connected-circuit switch after which some compatible cover is
five-colourable.

This is exact for every sampled flow: a negative starting decision exhausts
the full affine potential space, and the repair search tests elementary
circuits until it finds and checks a witness.  It is **not** an exact flow
census, because the 500 flows per graph were sampled.

The frozen files are:

- `fixed-fano-pure-merge-strong34-sample500-20260728.json`, the discovery
  output;
- `audit_strict_oum_one_switch_20260728.py`, the replay checker; and
- `strict-oum-order34-one-switch-replay-20260728.json`, its checked report.

The replay also directly verifies that all seven graph6 records are simple,
cubic, connected, girth five, and have no cyclic edge cut of size below
four.  It checks the retained source-list SHA-256
`2f087d5cbd1e97b1e10e7a5a064fe83d037872f838372e4d317c9d3f912fbf1f`.
The source-list assertion that these are the seven order-34 strong snarks is
provenance from the House of Graphs list, not independently reproved here.

The first bad flow retained on each graph has respectively
\(8,4,4,2,2,4,1\) gauged compatible covers.  Every one of these 25 covers
contains a coordinate \(K_6\), so none maps to \(R_5\).  The displayed
repairs use circuits of lengths \(5,5,13,13,5,5,17\), and each repaired
flow has an explicitly checked five-colourable compatible cover.

Three additional House of Graphs girth-at-least-six snarks, the unique
retained records of orders 28, 30, and 36, were then sampled at 500 flows
each.  Their 182, 263, and 272 merge-bad flows are all one-circuit
repairable.  Thus the combined new frontier is 5,000 sampled flows, 2,245
merge-bad flows, and no local countermodel.  The three additional frozen
outputs are
`fixed-fano-pure-merge-girth6-order{28,30,36}-sample500-20260728.json`.
Again, the potential and circuit decisions are exact for each sampled flow,
but the flow selection is not exhaustive.

## Eight-coordinate \(R_5\) equivalence

The apparently broader \(R_5\)-compression option gives no additional
freedom when the old cover has only eight coordinates.

> **Lemma.**  If \(H\) is a graph on at most eight vertices, then
> \[
> H\longrightarrow R_5
> \quad\Longleftrightarrow\quad
> \chi(H)\le 5,
> \]
> where \(R_5\) is the graph on \(\mathbb F_2^5\) joining words at Hamming
> distance two.

The reverse implication is immediate because \(R_5\) contains a \(K_5\):
take \(0\) and the four weight-two words whose supports form a four-edge
star.

For the forward implication, it is enough to prove the following small
critical-graph dichotomy.

> **Eight-vertex dichotomy.**  Every graph on at most eight vertices with
> chromatic number at least six contains \(K_6\) or
> \(K_3\mathbin{\vee}C_5\) as a subgraph.

Take a 6-critical subgraph \(F\).  Then \(\delta(F)\ge5\).  For six
vertices this forces \(K_6\).  For seven vertices the complement is a
matching.  If it has at least two edges, pairing the endpoints of two
missing edges gives a five-colouring; otherwise \(F\) contains \(K_6\).

It remains to consider \(|V(F)|=8\).  Put \(D=\overline F\).  Then
\(\Delta(D)\le2\), so every component of \(D\) is a path or a cycle.
Moreover
\[
\chi(F)=\theta(D)=6,
\]
where \(\theta\) is the minimum number of cliques partitioning \(V(D)\).
Thus a clique partition of \(D\) saves exactly two parts compared with
eight singletons.  If \(\alpha(D)\ge6\), then \(F\) contains \(K_6\).
Otherwise the path/cycle component possibilities with total saving two
leave only
\[
D=C_5+3K_1.
\]
Indeed, a triangle plus five isolates has independence number six; a
single matching-number-two component other than \(C_5\), or two
matching-number-one components, also has independence number at least six.
Consequently
\[
F=\overline{C_5+3K_1}=K_3\mathbin{\vee}C_5.
\]

Neither critical graph maps to \(R_5\).  For completeness,
\(\omega(R_5)=5\): translate a clique so that it contains \(0\).  Every
other word then has weight two, and any two of their supports must
intersect.  A pairwise-intersecting family of two-subsets is either
contained in a star, and hence has size at most four, or is the three-edge
triangle.  Thus the whole clique has size at most five, with equality from
\(0\) and a four-edge star.  This excludes \(K_6\).

For \(K_3\mathbin{\vee}C_5\), translate and permute
coordinates so that the triangle maps to
\[
0,\quad \{1,2\},\quad \{1,3\}.
\]
The common neighbourhood of these three vertices in \(R_5\) is
\[
\bigl\{\{2,3\},\{1,4\},\{1,5\}\bigr\}.
\]
Its induced graph is \(K_1+K_2\).  The joined \(C_5\) would have to map
into this common neighbourhood.  Since it is connected and has edges, its
image must lie in the \(K_2\), impossible for an odd cycle.  This proves
the lemma.

For an Oum-compatible eight-cover, therefore, general binary XOR
compression to five coordinates exists exactly when pure merging exists.
The surviving reduced conjecture can be stated without an \(R_5\)
alternative.

## Structural reason the 46-vertex composition does not transfer

There is also a clean topological lemma eliminating the exact
noncyclable-triple mechanism used in the unrestricted 46-vertex
countermodel.

> **Equal-value triple lemma.**  Let \(G\) be a cyclically
> \(4\)-edge-connected cubic graph and let
> \(\phi:E(G)\to\mathbb F_2^3-\{0\}\) be a flow.  Any set of at most three
> edges having one common \(\phi\)-value lies on a common circuit.

Knappe--Pitz's \(g(3)=3\) theorem says that at most three prescribed edges
of a 3-edge-connected graph lie on a circuit exactly when they contain no
odd edge cut.  Here an odd cut contained in the prescribed set has size one
or three.  Size one would be a bridge.  In a cyclically
\(4\)-edge-connected cubic graph every three-edge cut is a vertex star:
one shore must be acyclic, and the cubic cut formula for a forest shore
forces that shore to be one vertex.  But the three edges at a cubic vertex
cannot have one common nonzero flow value, because their sum would be that
same nonzero value rather than zero.  No odd cut is possible, so the common
circuit exists.

This lemma removes the precise device used in the 46-vertex construction:
three same-flow attachment edges that no connected circuit meets
simultaneously.  It does not finish the reduced conjecture.  A legal switch
by \(t\) requires the chosen circuit to avoid every edge currently valued
\(t\); the prescribed-edge theorem alone does not provide that avoidance.

The cited result is P. Knappe and M. Pitz, *Circuits through Prescribed
Edges*, Journal of Graph Theory 93 (2020), 470--482, Fact 5.4,
<https://doi.org/10.1002/jgt.22497>; the open preprint is
<https://arxiv.org/abs/1810.09323>.

## High-girth boundary

No tractable girth-at-least-ten strict snark was available in the retained
corpora.  The local candidate inventory contains a 30,450-vertex simple
cubic girth-ten non-Tait graph, but its cyclic edge connectivity is not
certified and exhaustive connected-circuit quantification is far beyond
the current enumerator.  The extra tests on the unique retained
girth-at-least-six snarks of orders 28, 30, and 36 also pass, but do not
reach the requested girth-ten frontier.

## Exact scope

What is established:

1. \(R_5\)-compression and five-colour pure merging are equivalent for
   every eight-coordinate co-occurrence graph.
2. The noncyclable same-value triple obstruction cannot occur in a
   cyclically \(4\)-edge-connected cubic graph.
3. All 2,245 merge-bad flows among the 5,000 new order-28--36 strict-snark
   samples have a checked one-circuit repair.

What remains open:

1. whether every fixed nowhere-zero \(\mathbb F_2^3\)-flow on every simple
   cyclically \(4\)-edge-connected non-Tait cubic graph has such a repair;
2. whether a smallest five-CDC counterexample, if one exists, can always be
   put in this fixed-flow/Oum-potential framework with the needed switch;
   and
3. the girth-at-least-ten strict-snark test.

None of these computations proves or disproves the Five-Cycle Double Cover
Conjecture.
