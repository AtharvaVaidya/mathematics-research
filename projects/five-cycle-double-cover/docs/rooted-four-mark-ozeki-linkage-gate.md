# The rooted four-mark obstruction passes through Ozeki's nice decomposition

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE CONDITIONAL REDUCTION / \(V_8\) ALTERNATIVE
ELIMINATED / NICE DECOMPOSITION AND EVERY WATKINS--MESNER CASE
ELIMINATED BEFORE ONE-TERMINAL REDUCTIONS**.

This note continues `rooted-four-mark-bridgeless-reduction.md`.  It
imports the exact four-terminal noncyclability theorem in Section 4.7
of Kenta Ozeki's dissertation,
[*Structural Characterizations of Rooted Subdivisions on Four
Vertices*](https://repository.dl.itc.u-tokyo.ac.jp/record/2009547/files/A39572.pdf).
It eliminates one of the theorem's two outcomes by an explicit pair of
circuits.  The inherited Tait colouring eliminates the other outcome
when the original subdivided graph is already irreducible.  The same
four private factor-circuits also exclude every Watkins--Mesner
obstruction to triple cyclability in that unreduced setting.

The result remains conditional because triple cyclability and the
forbidden-vertex path condition have not been derived after arbitrary
one-terminal reductions.  No rooted four-mark theorem and no five-cycle
double cover result is claimed.

## 1. Subdivide the four marks

Let \(L\) be a connected simple cubic graph, let
\[
                 S=\{s_1,s_2,s_3,s_4\}
\]
be a four-edge matching, and let \(f\notin S\).  Put \(J=L-f\).
The bridge-elimination theorem in
`rooted-four-mark-bridgeless-reduction.md` proves, in either the
standard rooted setup or the inherited opposite-cap setup, that a
counterexample has \(J\) bridgeless.  Hence \(J\) is 2-connected:
it is connected, subcubic, and has minimum degree two.

Subdivide each \(s_i\) once, and call the new degree-two vertex \(z_i\).
Write
\[
                  \widehat J,\qquad
                  Z=\{z_1,z_2,z_3,z_4\}                \tag{1}
\]
for the resulting graph and terminal set.  Subdivision preserves
2-connectivity.

A circuit of \(\widehat J\) through \(z_i\) uses both edges incident
with \(z_i\), so suppressing \(z_i\) recovers a circuit through \(s_i\).
Consequently:

* a circuit through all of \(Z\) is a closed rooted certificate with
  one four-mark component; and
* two vertex-disjoint circuits which together contain \(Z\), with two
  terminals on each, suppress to a closed rooted certificate with two
  two-mark components.

The second statement uses subcubicity only in the reverse direction:
edge-disjoint circuits in a subcubic graph are vertex-disjoint.  The
circuits constructed below are already vertex-disjoint.

Thus a rooted failure makes \(\widehat J\) \(Z\)-acyclic and forbids
every pair of vertex-disjoint circuits which partitions \(Z\) into
two pairs.

### 1.1 Four private circuits from the inherited colouring

The hypotheses give more than pair cyclability.  Fix the inherited
Tait colouring in which the marks have colour \(c\), and write \(a\)
for the colour of \(f\).  Let \(b\) be the third colour.  The
\(bc\)-coloured subgraph of \(L\) is a disjoint union of circuits and
does not use \(f\).  Universal separation says that each of its circuit
components contains at most one mark.  Hence the four marks belong to
four different components.  After the four marked edges are subdivided,
we obtain four pairwise vertex-disjoint circuits
\[
                  R_1,R_2,R_3,R_4\subseteq\widehat J,
       \qquad z_i\in V(R_i).                            \tag{1a}
\]
Each \(R_i\) contains no other terminal.

This elementary observation is the key extra datum absent from an
arbitrary four-terminal graph.  It uses universal separation only for
the one fixed inherited colouring, although universal separation is
how that colouring and the distinct-component conclusion arise in the
project.

## 2. The exact Ozeki gate

Ozeki calls \((\widehat J,Z)\) **irreducible** when the following
elementary reductions have already been performed:

1. no 2-separation has a nonempty terminal-free proper side;
2. a proper side of a 2-separation containing exactly one terminal is
   just that terminal; and
3. a stated \(1+3\) three-separation is trivial when its lone terminal
   has degree at least three.

Here every member of \(Z\) has degree two, so the third clause is
vacuous.  The first two clauses remove terminal-free and one-terminal
2-separation protrusions while preserving \(Z\)-cyclability.  Their
effect on the stronger two-circuit certificate is settled next.

### 2.1 The two-separation reductions are certificate-safe

> **Irreducible-core lemma.**  Let \(G\) be a 2-connected graph with
> four labelled degree-two terminals \(Z\).  If \(G\) has no circuit
> through all of \(Z\) and no two vertex-disjoint circuits which split
> \(Z\) into two pairs, then the same is true of a smaller
> 2-connected graph \(G'\) on the same four terminal labels which
> satisfies Ozeki's first two irreducibility conditions.

### Proof

Take a 2-separation \((A,B)\), with separator \(\{x,y\}\).

First suppose \(A-B\) is nonempty and contains no terminal.  Choose
vertices \(a\in A-B\) and \(b\in B-A\).  Since \(G\) is 2-connected,
one circuit contains \(a,b\).  Its intersection with \(G[A]\) contains
an \(x\)-to-\(y\) path \(P_A\) through \(A-B\).  Replace the entire
terminal-free side by one edge \(xy\), adding it only if it is not
already present.  If a circuit of the reduced graph uses the replacement
edge, substitute \(P_A\); if it does not, leave it unchanged.  This
lifts both a one-circuit all-terminal certificate and two disjoint
pair-circuits.  The replacement contains no terminal, so it preserves
the marked count of every lifted component.  The standard
two-separation reduction preserves 2-connectivity.

Now suppose \(A-B\) contains exactly one terminal \(z\) and more than
that one vertex.  Choose \(b\in B-A\).  A circuit through \(z,b\)
exists by 2-connectivity.  Its \(A\)-segment is an \(x\)-to-\(y\) path
\(P_z\) through \(z\).  Replace the whole side by a fresh length-two
path
\[
                         xz'y,                         \tag{2a}
\]
and transfer the label \(z\) to the new degree-two vertex \(z'\).
Every circuit containing \(z'\) uses both edges of (2a); replace that
path by \(P_z\).  Other certificate components are vertex-disjoint
from \(x,y\), so the lift is again a valid one- or two-circuit
certificate and preserves the terminal count on each component.

Each operation strictly reduces the order.  Repeating them terminates
with a 2-connected graph satisfying irreducibility clauses 1 and 2.
All terminals still have degree two, so clause 3 is vacuous.  If the
terminal-free replacement edge is already present, retaining the
existing edge rather than adding a parallel copy keeps the graph
simple. \(\square\)

Thus irreducibility is not an inherited-hypothesis obligation: it is a
certificate-preserving topological preprocessing step.  The two
genuine prerequisites at this point are (T3) and (P4) on the resulting
irreducible core.  The first of them is preserved by the preprocessing.

> **Triple-cyclability preservation lemma.**  Suppose the original
> terminal graph is \(Z\)-acyclic and every three members of \(Z\) lie
> on a circuit.  After any sequence of the terminal-free and
> one-terminal reductions in the irreducible-core lemma, either a
> four-terminal circuit has already appeared and lifts to the original
> graph, or every terminal triple still lies on a circuit.

### Proof

Consider one reduction with separator \(\{x,y\}\).  For a
terminal-free side, a circuit through a prescribed terminal triple
either avoids the proper interior or meets it in one \(x\)-to-\(y\)
path.  In the second case replace that segment by the replacement edge
\(xy\).  A simple circuit cannot have two distinct segments through
the same proper side, because it has degree two at \(x\) and \(y\).

Now let the reduced side contain exactly the terminal \(z_i\), and
replace it by \(xz_i'y\).  If the chosen triple contains \(z_i\), its
original circuit also contains terminals outside the side.  Its
intersection with the side is therefore an \(x\)-to-\(y\) path through
\(z_i\); replace that segment by \(xz_i'y\).

If the chosen triple excludes \(z_i\), replace any \(x\)-to-\(y\)
segment through the side by \(xz_i'y\).  The resulting circuit either
still certifies the chosen triple or contains all four reduced
terminals.  In the latter case substitute the fixed
\(x\)-to-\(y\) path through \(z_i\) used to define the reduction.  This
lifts the four-terminal circuit to the original graph, which is already
a closed rooted certificate.

The argument is unchanged when \(x\) or \(y\) is another terminal.
Its two circuit incidences are still used only once, so the displayed
segment replacement remains a simple circuit.  Induction over the
reduction sequence proves the claim. \(\square\)

There is likewise no genuine parallel-edge exception at this stage.
The one-terminal replacement is the simple length-two path
\(xz_i'y\), even if an edge \(xy\) already exists.  Suppressing
\(z_i'\) may *represent* the labelled mark as parallel to that edge,
but Ozeki's theorem is applied before suppression.  Every certificate
component through \(z_i'\) uses both replacement edges and lifts by
substituting the fixed path through \(z_i\).  A second vertex-disjoint
component avoids \(x,y\), so this substitution also preserves a
two-circuit certificate.  Thus parallelism after suppression is a
bookkeeping warning for cubic-core arguments, not a failure of the
topological reduction or its certificate lift.

There is an important limitation.  The reductions are certificate-safe,
but a one-terminal reduction need not preserve the four *pairwise
disjoint* private circuits (1a).  If \(R_i\) lies wholly in the side
being replaced, closing the new path \(xz_i'y\) may require an
\(x\)-to-\(y\) path which meets another \(R_j\).  The replacement may
also display the labelled mark as parallel to an existing edge after
terminal suppression.  The preceding paragraph shows that this does
not obstruct certificate lifting, but it does mean that a later
argument which invokes simplicity of the *suppressed cubic graph*
cannot be silently transferred to an arbitrary reduced core.

The fixed colouring nevertheless localizes the possible loss of the
private circuits.  The following statement is for the standard
marked-cut hypothesis.  It also applies to an inherited opposite-cap
shore whenever the inherited inequality is available on the displayed
shore.

> **Trapped-factor localization lemma.**  Let \((A,B)\) be a
> one-terminal 2-separation used in the irreducible-core reduction, with
> separator \(\{x,y\}\) disjoint from \(Z\) and terminal
> \(z_i\in A-B\).  If the private factor-circuit \(R_i\)
> supplies an \(x\)-to-\(y\) path through the side being replaced, all
> four private circuits survive the reduction.  Otherwise there is a
> shore \(W\), containing \(R_i\), such that:
>
> 1. \(\delta_{\widehat J}(W)\) has size two;
> 2. after suppressing \(z_i\), the corresponding shore of \(L\)
>    contains exactly the mark \(s_i\);
> 3. \(f\) crosses that shore and \(\delta_L(W)\) is a three-edge cut
>    with one edge of each Tait colour; and
> 4. the two non-root cut edges lie on one \(bc\)-factor circuit
>    \(R^\ast\).
>
> If \(R^\ast\) is unmarked, the one-terminal reduction can be chosen so
> that all four private circuits survive.  Therefore the only unresolved
> private-circuit state has \(R^\ast=R_j\) for another marked private
> circuit \(j\ne i\).

### Proof

Assign every separator vertex used by \(R_i\) to the \(A\)-shore.  The
two circuit edges at such a vertex
leave at most one incident edge crossing the resulting shore.  Assign
each remaining separator vertex to the shore which minimizes its
number of crossing incident edges; subcubicity again makes that number
at most one.  Both proper interiors are nonempty, so this gives a
nontrivial edge cut of size at most two.  Since \(\widehat J\) is
bridgeless, its size is exactly two, with one crossing edge at each
separator vertex.

If \(R_i\) supplies an \(x\)-to-\(y\) path through \(z_i\) in the
reduced side, replace that path by the new length-two terminal path.
Pairwise disjointness shows that the other three private circuits are
unaffected.

Suppose no such path is supplied.  The preceding shore contains all of
\(R_i\), so both halves of the subdivided mark are internal and the
shore is cyclic.  Suppress \(z_i\).  No other mark becomes internal:
another subdivided terminal lies outside the proper \(A\)-interior,
and both of its neighbours cannot lie in \(W\), since its two incident
edges would then be the entire cut and would leave the nonempty
\(B\)-interior disconnected.  Thus the corresponding shore in \(L\)
has exactly one internal mark.

If \(f\) did not cross it, its marked cyclic-cut value would be
\[
                         2+1=3,
\]
contrary to the standard inequality.  Hence \(f\) crosses, and the cut
has size three in \(L\).  Tait cut parity makes a three-edge cut contain
one edge of each colour.  Since \(f\) has colour \(a\), the two edges
remaining in \(J\) have colours \(b,c\).

The spanning \(bc\)-factor meets every cut evenly.  Its two cut edges
therefore belong to one factor-circuit \(R^\ast\), different from the
trapped \(R_i\).  If \(R^\ast\) is unmarked, its arc outside the reduced
side is an \(x\)-to-\(y\) path disjoint from all four marked
factor-circuits.  Unite that arc with the replacement path \(xz_i'y\).
The result is a new private circuit for \(z_i'\), while the other three
private circuits remain unchanged.  If \(R^\ast\) is marked, universal
separation for the fixed colouring says it is exactly one \(R_j\), and
its outside arc contains \(z_j\); this is precisely the residual state
in which the construction is not private. \(\square\)

Separations whose boundary itself contains another terminal are not
covered by this localization lemma, but they are no longer a
preservation obligation.  The boundary-terminal lift lemma in
`one-terminal-trace-lift-frontier.md` shows directly that, under (T3),
such a two-separation has a four-terminal circuit: the triple circuit
through the boundary terminal and the two opposite-side terminals can
have its one side-segment replaced by a path through the interior
terminal.

In the residual \(R^\ast=R_j\) case the reduced graph has an exact
replacement for (1a), also proved in that note.  The replacement path
and the outside arc of \(R_j\) form a two-terminal circuit through
\(z_i',z_j\), disjoint from the unchanged private circuits
\(R_k,R_\ell\).  Thus the surviving circuit packet has terminal
partition \(2+1+1\).  The full marked-cut and universal-separation
hypotheses do not exclude this borrower state: an audited compliant
order-56 example realizes it and also has a displayed root-avoiding
four-mark circuit.

Ozeki's two additional hypotheses are:

\[
\begin{array}{ll}
\text{(T3)}&\text{every three members of \(Z\) lie on a circuit;}\\
\text{(P4)}&\text{for every \(w\in V(\widehat J)\setminus Z\), the
graph \(\widehat J-w\) has a path through all of \(Z\).}
\end{array}                                             \tag{2}
\]

Theorem 4.7.2 of the dissertation says that if a 2-connected,
irreducible, \(Z\)-acyclic graph satisfies (T3) and (P4), then exactly
one of the following structural outcomes is present:

1. a **nice decomposition**
   \((X_1,X_2,A,B)\), whose interiors contain the terminals in the
   distribution \(1,1,0,2\); or
2. all terminals have degree two and the graph contains a
   \(V_8\)-subdivision on \(Z\).

All terminals in (1) do have degree two.  The next lemma disposes of
the second outcome without any colouring or cut hypothesis.

## 3. The \(V_8\) frame itself is a certificate

> **\(V_8\)-frame lemma.**  If a graph contains a \(V_8\)-subdivision
> on four terminals \(Z\), then it contains two vertex-disjoint
> circuits, each through two members of \(Z\).

### Proof

Use Ozeki's notation.  The subdivision consists of:

* a rim circuit \(C\) through distinct vertices
  \(u_1,u_2,\ldots,u_8\) in this cyclic order; and
* four mutually disjoint paths \(P_i\), where \(P_i\) joins
  \(u_i\) to \(u_{i+4}\), has no internal vertex on \(C\), and has
  terminal \(z_i\) internally, for \(1\le i\le4\).

Let \(C[u_i,u_{i+1}]\) denote the rim segment between the two
consecutive displayed vertices, with indices read modulo eight.  Then
\[
\begin{aligned}
D_{12}
  &=P_1\cup P_2\cup C[u_1,u_2]\cup C[u_5,u_6],\\
D_{34}
  &=P_3\cup P_4\cup C[u_3,u_4]\cup C[u_7,u_8].
\end{aligned}                                          \tag{3}
\]
Each union in (3) is a circuit.  The four spoke paths are mutually
disjoint, and the four selected rim segments have pairwise disjoint
vertex sets.  Therefore \(D_{12}\) and \(D_{34}\) are vertex-disjoint.
The first contains \(z_1,z_2\), and the second contains \(z_3,z_4\).
\(\square\)

Suppressing the four terminals turns (3) into a closed rooted
certificate in \(J=L-f\).  Thus the \(V_8\) alternative is impossible
in a rooted counterexample.

We obtain the following exact conditional reduction.

> **Ozeki linkage gate.**  Reduce a rooted counterexample by the
> irreducible-core lemma.  If the resulting terminal graph satisfies
> (T3) and (P4), then it has Ozeki's nice decomposition with terminal
> distribution \(1,1,0,2\).

This is a theorem, not a heuristic: apply Ozeki Theorem 4.7.2 and
exclude its \(V_8\) outcome by the displayed lemma.

## 4. The nice case is impossible before one-terminal reduction

The nice decomposition has five distinct boundary vertices
\[
                 a_1,a_2,b_1,b_2,b_3
\]
and parts satisfying
\[
\begin{array}{c|c}
\text{part}&\text{boundary}\\ \hline
X_1&\{a_1,b_1\}\\
X_2&\{a_2,b_2\}\\
A&\{a_1,a_2,b_3\}\\
B&\{b_1,b_2,b_3\}.
\end{array}                                             \tag{4}
\]
The inherited private circuits actually exclude (4), provided that
the graph to which Ozeki is applied is the original subdivided graph
rather than a core changed by a nontrivial one-terminal reduction.

> **Private-circuit exclusion of the nice case.**  Suppose
> \(\widehat J\) itself is Ozeki-irreducible and has the four circuits
> (1a).  Then \(\widehat J\) has no nice decomposition with terminal
> distribution \(1,1,0,2\).

### Proof

Relabel so that \(z_i\in\operatorname{int}X_i\) for \(i=1,2\).
Ozeki irreducibility clause 2 applied to \(X_i\) gives
\[
             \operatorname{int}X_i=\{z_i\}.             \tag{5}
\]
Since \(z_i\) has degree two and \(\operatorname{bd}X_i=\{a_i,b_i\}\),
its neighbours are \(a_i,b_i\).  There is no edge \(a_i b_i\):
suppressing \(z_i\) would make the marked edge \(a_i b_i\) parallel
to it in \(L\), contrary to the assumed simplicity of \(L\).

Delete \(z_1\) from \(R_1\).  What remains is an
\(a_1\)-to-\(b_1\) path outside \(\operatorname{int}X_1\).  In the
incidence pattern (4), every such path passes from the \(A\)-side to
the \(B\)-side either through \(b_3\), or through both boundary
vertices \(a_2,b_2\) of \(X_2\).  The latter is impossible because
\(R_2\) contains \(a_2,z_2,b_2\) and \(R_1,R_2\) are vertex-disjoint.
Therefore \(b_3\in V(R_1)\).  By symmetry
\(b_3\in V(R_2)\), again contradicting disjointness. \(\square\)

Combined with the \(V_8\)-frame lemma, this proves:

> **Unreduced Ozeki closure.**  If the original \(\widehat J\) is
> Ozeki-irreducible and satisfies (T3) and (P4), then it has a closed
> rooted certificate.

This closes both outcomes of Ozeki's theorem in that exact class.  It
does not yet close a graph which reaches irreducibility only after a
one-terminal reduction, because that operation need not preserve (1a).

### 4.1 The majority assignment gives a small paired edge cut

There is also a useful cut consequence of (4).  In any subcubic graph,
let \((U,V)\) be a separation with three-vertex separator \(D\).
Assign the vertices of \(D\) to the two shores so that the number of
crossing edges is minimum.  Flipping one \(d\in D\) changes the cut
size by
\[
                 \deg(d)-2q_d,
\]
where \(q_d\) is the number of its incident crossing edges.  Minimality
therefore gives \(q_d\le1\).  Every crossing edge has an end in \(D\),
so the resulting edge cut has size at most three.

For the nice separation
\[
              (X_1\cup X_2\cup A,\ B)
\]
the *subdivided terminals* remain in a \(2+2\) distribution.  If the
private circuits (1a) are still present, both shores are cyclic: a circuit
crossing the cut uses at least two cut edges, so at most one of the four
pairwise disjoint \(R_i\) crosses a cut of size at most three; at least
one private circuit remains wholly on each \(2\)-terminal shore.
Restoring \(f\) increases the cut size by at most one.

Care is required when the terminals are suppressed.  A boundary vertex
such as \(b_1\) can be assigned opposite \(z_1\), in which case the
original marked edge \(s_1\) itself belongs to the edge cut.  Thus the
majority argument gives a paired terminal cut of size at most three in
\(\widehat J\), or at most four after restoring \(f\), but does not by
itself give an *unmarked* \(2+2\) cut in \(L\).  Nor does it by itself
contradict the marked cyclic-cut inequality: a cyclic shore with two
internal marks is allowed boundary size two.  The marked signature of
this small cut is the remaining issue in the cut-based attack.

## 5. Watkins--Mesner narrows failure of (T3)

The private circuits also sharply restrict the first missing Ozeki
hypothesis when the original \(\widehat J\) is irreducible.

> **Watkins--Mesner residual lemma.**  Suppose the original
> \(\widehat J\) is Ozeki-irreducible and has (1a).  If
> \(z_1,z_2,z_3\) do not lie on one circuit, then their
> Watkins--Mesner \(K_{3,2}\)-decomposition has integral value zero.
> After relabelling, its three terminal parts have total-terminal
> distribution
> \[
>                         2,1,1,                       \tag{6}
> \]
> with \(z_1,z_4\) in the first part and \(z_2,z_3\) alone in the
> other two.

### Proof

The alternative separation of order at most one in Watkins--Mesner
Theorem 4.2.3 is impossible because \(\widehat J\) is 2-connected.
Let
\[
              (X_1,X_2,X_3,Y_1,Y_2)
\]
be the resulting \(K_{3,2}\)-decomposition, and let \(s\in\{0,1,2\}\)
be its integral value.

At least two \(X_i\) have exactly one member of the full four-terminal
set in their interiors.  Irreducibility clause 2 makes each such
interior the singleton \(\{z_i\}\).  If \(s=2\), the two boundary
vertices are common to all three \(X_i\); the private circuits through
two singleton terminals both contain those boundary vertices.  If
\(s=1\), the singleton in the integral part is a common boundary
vertex of all three \(X_i\), and the same two private circuits both
contain it.  Either conclusion contradicts (1a).  Hence \(s=0\).

Write
\[
 X_i\cap Y_j=\{x_{ij}\}\qquad
 (1\le i\le3,\ 1\le j\le2).
\]
If the fourth terminal belonged to no \(\operatorname{int}X_i\), all
three \(X_i\) would have singleton interiors.  Simplicity of \(L\)
forbids an edge \(x_{i1}x_{i2}\), because suppressing \(z_i\) would
then create a parallel edge.  Thus the part of \(R_i-z_i\) from
\(x_{i1}\) to \(x_{i2}\) must pass from \(Y_1\) to \(Y_2\) through
some other part \(X_j\).  It contains both boundary vertices of that
part and therefore meets \(R_j\), contrary to (1a).  The fourth
terminal must consequently lie in one \(\operatorname{int}X_i\).
Relabelling that part as \(X_1\) gives (6). \(\square\)

The last pattern is itself impossible.  The short proof is recorded
separately because it uses the incidence geometry of an integral-zero
\(K_{3,2}\)-decomposition, not merely a separator count.

> **Integral-zero exclusion lemma.**  Under the hypotheses of the
> Watkins--Mesner residual lemma, the distribution (6) cannot occur.
> Consequently every three members of \(Z\) lie on a circuit in the
> original \(\widehat J\); that is, (T3) holds before any nontrivial
> one-terminal reduction.

### Proof

Retain the notation of the residual lemma.  Because \(s=0\), the three
parts \(X_1,X_2,X_3\) are pairwise disjoint, the two parts \(Y_1,Y_2\)
are pairwise disjoint, and
\[
             X_i\cap Y_j=\{x_{ij}\}
             \qquad(1\leq i\leq3,\ 1\leq j\leq2).       \tag{7}
\]
After relabelling as in (6), the interiors of \(X_2\) and \(X_3\)
contain only \(z_2\) and \(z_3\), respectively.  Ozeki irreducibility
clause 2 therefore gives
\[
 X_2=\{x_{21},z_2,x_{22}\},\qquad
 X_3=\{x_{31},z_3,x_{32}\}.                            \tag{8}
\]
The two neighbours of \(z_i\) are \(x_{i1},x_{i2}\).  There is no edge
\(x_{i1}x_{i2}\) for \(i=2,3\), since suppressing \(z_i\) would then
make that edge parallel to the original marked edge in the simple
graph \(L\).

Delete \(z_2\) from its private circuit \(R_2\).  The remainder is an
\(x_{21}\)-to-\(x_{22}\) path.  Its ends lie in the disjoint parts
\(Y_1,Y_2\).  In an integral-zero \(K_{3,2}\)-decomposition every edge
belongs to one of the five parts, so every path from \(Y_1\) to \(Y_2\)
must traverse some \(X_k\) from \(x_{k1}\) to \(x_{k2}\).  It cannot
use \(X_2\): after \(z_2\) is deleted, (8) and the missing edge
\(x_{21}x_{22}\) leave no route across \(X_2\).  It cannot use \(X_3\),
because any route across \(X_3\) contains both \(x_{31},x_{32}\), and
both vertices lie on \(R_3\).  The disjointness of \(R_2,R_3\) therefore
forces the route across \(X_1\), and in particular
\[
                    x_{11},x_{12}\in V(R_2).           \tag{9}
\]

Apply the same argument with indices 2 and 3 interchanged.  The path
\(R_3-z_3\) cannot cross \(X_3\), and it cannot cross \(X_2\) because
both \(x_{21},x_{22}\) lie on \(R_2\).  Hence it must cross \(X_1\), so
\[
                    x_{11},x_{12}\in V(R_3).           \tag{10}
\]
Equations (9) and (10) contradict the pairwise vertex-disjointness of
the private circuits. \(\square\)

Thus (T3) is proved when the original graph is already irreducible.
The preservation lemma shows that once (T3) is established before a
reduction, the reduction does not lose it.  It does not by itself prove
(T3) for a reducible original graph, because the Watkins--Mesner
argument above used irreducibility before the first one-terminal
reduction.  The remaining entry-state issue and the missing (P4)
condition still require their own separator analysis;
\(\widehat J-w\) is connected but need not be 2-connected, so Ozeki's
2-connected path corollary cannot be applied to it without treating the
additional Appendix 4.9 cases.

## 6. Exact P4 boundary: the fixed factor data are not enough

The connected simple cubic graph

```text
SlCGG[_?I?_D??_?_?W?D?_???W?_G?GS
```

has marks
\[
 (0,3),\quad(4,7),\quad(8,9),\quad(14,15)
\]
and root \(f=(9,18)\).  It is a sharp warning about (P4), not a
counterexample to either rooted assertion retained by the project.

Here is a fixed Tait colouring in a compact, directly checkable form.
The \(bc\)-factor consists of the five four-circuits
\[
\begin{split}
 &(0,1,2,3,0),\quad(4,5,6,7,4),\quad
 (8,9,10,11,8),\\
 &(12,13,14,15,12),\quad(16,17,18,19,16).
\end{split}                                             \tag{11}
\]
Colour each displayed circuit alternately, independently choosing the
parity which makes its displayed mark colour \(c\).  The remaining
colour-\(a\) perfect matching is
\[
\begin{split}
\{&(0,13),(1,10),(2,8),(3,4),(5,7),\\
  &(6,16),(9,18),(11,19),(12,14),(15,17)\}.
\end{split}                                             \tag{12}
\]
Thus the four marked \(bc\)-factor circuits are private and
vertex-disjoint, all marks have colour \(c\), and the root has colour
\(a\).  Direct deletion of each edge in turn shows that \(J=L-f\) is
bridgeless.

The exact cycle-space calculation for \(J\) has dimension ten.  Of its
\(2^{10}=1024\) binary cycles, exactly 64 contain all four marks.  Their
marked component profiles are
\[
\begin{array}{c|r}
\text{profile}&\text{number}\\ \hline
(1,1,1,1)&8\\
(1,1,2)&8\\
(1,3)&48 .
\end{array}                                             \tag{13}
\]
Every row has an odd-marked component, so there is no closed rooted
certificate.  Circuit enumeration separately shows that every terminal
triple is cyclable, no circuit contains all four terminals, and no two
vertex-disjoint circuits contain complementary terminal pairs.

Nevertheless (P4) fails.  Subdivide the marks by
\(z_{20},z_{21},z_{22},z_{23}\), respectively.  In
\(\widehat J-0-\{3,6\}\), the terminal-bearing components have terminal
sets
\[
                    \{z_{20}\},\quad
                    \{z_{21}\},\quad
                    \{z_{22},z_{23}\}.                 \tag{14}
\]
The singleton \(z_{20}\) is adjacent only to 3 in \(\widehat J-0\).
The \(z_{21}\)-component attaches to 3 at vertex 4 and to 6 at vertices
5 and 7.  The last component attaches to 3 at vertex 2 and to 6 at
vertex 16.  Inside that last component, the marked block containing
\(z_{22}\) attaches to the rest only at the articulation vertex 11,
while the marked block containing \(z_{23}\) attaches to the rest only
at the articulation vertex 15.  Consequently:

* a path which starts at 16 cannot visit both marked leaf blocks; and
* a path from 2 to 16 cannot visit both marked leaf blocks.

Any path through all four terminals would have to start at \(z_{20}\),
pass through 3, visit the other two terminal-bearing components in one
of the two possible orders through vertex 6, and require exactly one of
those two impossible paths in the last component.  Hence
\(\widehat J-0\) has no path through all four terminals.  The exhaustive
path check gives every nonempty terminal trace except \(1111\).

This graph fails the two hypotheses which remain indispensable in the
project.  First, the four shores
\[
\begin{array}{c|c|c|c}
X&|\delta_L(X)|&|S\cap E(L[X])|&\text{sum}\\ \hline
\{5,6,7\}&3&0&3\\
\{4,5,6,7\}&2&1&3\\
\{12,13,14\}&3&0&3\\
\{12,13,14,15\}&2&1&3
\end{array}                                             \tag{15}
\]
are the exact minimizers of the marked cyclic-cut expression.  Second,
an alternative Tait colouring has the bichromatic circuit
\[
 0,3,4,7,5,6,16,17,15,12,14,13,0,                     \tag{16}
\]
which contains the two marks \((0,3)\) and \((4,7)\); universal
separation therefore fails.

The independent checker
`scratch/verify_rooted_p4_fixed_colouring_boundary.py` locally decodes
the graph6 record, checks both displayed colourings, enumerates all
edges for bridgelessness, all \(2^{20}-2\) vertex shores **without
quotienting by complements**, all 1024 root-avoiding binary cycles,
all circuits, and all simple path traces after deleting vertex 0.
The warning about complements matters: although cut size is
complement-symmetric, the number of marks internal to a shore is not.
An exploratory half-shore calculation incorrectly returned four before
the full audit found (15).

Run:

```text
python3 scratch/verify_rooted_p4_fixed_colouring_boundary.py
```

Thus fixed Tait precolouring, a spanning private factor, bridgeless
root deletion, (T3), and even the absence of a closed certificate do
not imply (P4).  Any proof of (P4) must use the full marked-cut and
universal-separation data, or stronger inherited minimum-counterexample
information.

## 7. Exact boundary example: affine trace and marked cuts are not enough

The connected simple cubic graph

```text
K?ABArOb@WEO
```

has marked edges
\[
 (2,6),\quad(4,7),\quad(0,8),\quad(5,9)
\]
and root
\[
                         f=(1,6).                       \tag{17}
\]
The independent checker
`scratch/verify_rooted_linkage_boundary_example.py` proves:

* deleting \(f\) leaves a bridgeless graph;
* the exact standard marked cyclic-cut inequality has minimum value
  four over **all** vertex shores;
* the graph has two Tait colourings modulo global colour permutation;
* its all-mark affine cycle fibre has eight members;
* the four root-avoiding members all have marked-component profile
  \((1,3)\);
* the four componentwise-even members each form one four-mark circuit
  and all use \(f\).

Thus marked-cut compliance plus affine root avoidance does not imply a
closed rooted certificate.

This graph is outside the intended rooted hypotheses in two independently
checked ways: no Tait colouring makes all four marks one colour and the
root a different colour, and several bichromatic circuits contain two
marks.  It therefore does not refute either the standard rooted assertion
or the inherited six-cut assertion.  Its purpose is to prevent the Tait
and universal-separation data from being silently discarded in the nice
case.

Run:

```text
python3 scratch/verify_rooted_linkage_boundary_example.py
```

## 8. Scope

This note proves:

* the exact translation from marked edges to four degree-two terminals;
* certificate-safe reduction to Ozeki irreducibility;
* localization of private-circuit loss at a terminal-free-boundary
  one-terminal reduction to one marked crossing-factor state;
* the \(V_8\)-frame lemma by two displayed circuits;
* the elimination of the nice-decomposition case when the original
  subdivided graph is already irreducible;
* the majority-assignment conversion of a nice three-separator to an
  paired terminal edge cut of size at most three, together with the
  exact warning that suppression can put marks on that cut; and
* the exclusion of every triple-cycle failure, in that same unreduced
  setting, by reducing to and then contradicting the integral-zero
  Watkins--Mesner distribution (6); and
* an exact countermodel showing that the fixed private-factor data,
  bridgeless root deletion, (T3), and certificate failure do not imply
  (P4), together with its precise marked-cut and universal-separation
  failures.

It does not prove (T3) or (P4) after a nontrivial one-terminal
reduction.  Literal four-private-circuit preservation is false in the
residual marked crossing-factor state; the exact guaranteed replacement
is a \(2+1+1\) circuit packet.  The terminal-on-boundary state is closed
directly by triple cyclability and is no longer residual.  Even in the
unreduced irreducible setting,
(P4) remains open under the full retained hypotheses.  It does not
prove the rooted four-mark assertion or the five-cycle double cover
conjecture.

## AI-use disclosure

OpenAI Codex agents, under human direction, located Ozeki's structural
theorem, recognized that its \(V_8\) alternative contains an immediate
two-circuit certificate, derived the private-circuit obstruction to the
nice case, eliminated the Watkins--Mesner types, found and checked the
finite boundary example, and wrote this reduction.  The
universal arguments are displayed in full for line-by-line human
checking.  The finite example is a diagnostic with an exact executable
checker, not human peer review.
