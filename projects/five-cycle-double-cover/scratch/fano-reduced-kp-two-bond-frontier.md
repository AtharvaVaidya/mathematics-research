# Reduced Fano one-switch route: the two-bond frontier

Status: **CORRECTED CONDITIONAL REDUCTION / EXACT AUXILIARY
COUNTERMODEL / REDUCED ONE-SWITCH LEMMA OPEN**.

This note isolates the precise point at which the Knappe--Pitz
three-prescribed-edge theorem can help the reduced Fano-flow one-switch
route.  It also gives a 24-vertex countermodel to the tempting global
``clean deleted value'' shortcut.  The countermodel has a one-circuit
repair.  It therefore refutes neither the reduced one-switch lemma nor
FiveCDC.

## 1. The corrected Knappe--Pitz input

Let \(G\) be cubic and
\[
 f:E(G)\longrightarrow\mathbb F_2^3-\{0\}
\]
be a flow.  Put \(M_t=f^{-1}(t)\) and \(H_t=G-M_t\).

For distinct nonzero \(s,t\), let \(S\subseteq M_s\) with
\(|S|\leq3\).  The flow cut equation proves that \(S\) contains no odd
cut of \(H_t\).  Indeed, \(H_t\) has no bridge: a one-edge cut with
edge value \(a\ne t\) would give the \(G\)-cut sum \(a\) or \(a+t\),
never zero.  The only remaining odd cut contained in \(S\) has three
edges, all valued \(s\).  Adding the crossing \(t\)-edges back gives
cut sum \(s\) or \(s+t\), again never zero.

Knappe and Pitz prove \(g(3)=3\): in a 3-edge-connected graph, a
specified set of at most three edges lies on a circuit if and only if
it contains no odd cut.  Consequently:

> **Legal-circuit lemma.**  If the degree-two paths of \(H_t\) can be
> suppressed to a 3-edge-connected core containing the images of \(S\),
> then \(H_t\) has a circuit through \(S\).

Suppression is safe for this conclusion: a core circuit lifts by
expanding every used virtual edge to its whole degree-two path.  Several
members of \(S\) on one path are all recovered.

There is a stronger unconditional statement when \(|S|\le2\).  Every
component of \(H_t\) is bridgeless by the same cut-sum argument.  The
global Knappe--Pitz theorem for \(k=2\) therefore gives:

> **Two-edge escape lemma.**  Any two prescribed edges in one component
> of \(G-M_t\) lie on a common circuit avoiding \(M_t\).

Thus nontrivial two-bonds matter only when the finite graft exchange
really needs three prescribed pieces, or when the desired circuit must
also avoid additional value classes.  Proving that two exchange edges
always suffice would bypass the clean-core problem completely.

This is only a sufficient condition.  The false statement
``\(S\) is cyclable iff every bond meets \(S\) other than once'' must not
be used.  Jaeger's cut condition yields an even subgraph, which may be
disconnected.  Knappe--Pitz supply connectedness under the additional
3-edge-connectivity hypothesis.

## 2. A finite local exchange axiom that would suffice

The remaining odd-\(K_{2,3}\) work can be stated as a finite local
obligation.

> **Three-edge graft exchange axiom.**  For every bad Fano flow \(f\) on
> a simple cyclically 4-edge-connected cubic graph, the seven
> value-class nonpacking certificates admit distinct values \(s,t\) and
> a set \(S\subseteq M_s\), \(1\leq|S|\leq3\), such that:
>
> 1. some circuit of \(H_t\) contains \(S\); and
> 2. switching \(t\) on any such certificate-compatible circuit makes
>    at least one value class pack two edge-disjoint boundary
>    \(T\)-joins.

This axiom immediately implies the reduced one-switch lemma.  The first
part follows from the legal-circuit lemma whenever the prescribed images
lie in a 3-edge-connected suppressed torso.  The second part is the
unproved finite exchange law tying the six pairwise intersections of the
four canonical joins to the seven simultaneous odd-\(K_{2,3}\) graft
obstructions.  A graft minor alone does not preserve enough labeling to
establish it.

The exact avoidance condition is not merely a parity condition:
the circuit must be contained in \(G-M_t\).  Nontrivial two-edge cuts of
\(H_t\) can place prescribed pieces in different suppressed torsos and
prevent the direct \(g(3)=3\) application.

## 3. What a two-bond becomes in the cubic graph

Let \(\delta_{H_t}(X)=\{e_1,e_2\}\) be a nontrivial two-edge cut and put
\[
 r=|\delta_G(X)\cap M_t|.
\]
Then
\[
 \delta_G(X)=\{e_1,e_2\}\mathbin{\dot\cup}
              (\delta_G(X)\cap M_t)
\]
and the flow cut equation gives
\[
 f(e_1)+f(e_2)=(r\bmod2)t.                    \tag{1}
\]
Thus the two bond edges have equal values when \(r\) is even, and values
differing by \(t\) when \(r\) is odd.

If both shores are cyclic, cyclic 4-edge-connectivity gives only
\(r\ge2\).  It does not force \(r=2\), and therefore does not turn every
two-bond into an exact four-edge cut.  Larger cuts of the displayed form
are a genuine residual case.  This is why cyclic 4-edge-connectivity by
itself does not eliminate the deleted-matching two-bonds.

## 4. Exact order-24 countermodel to the global clean-core shortcut

The frozen graph has graph6 record

```text
W??Y@C?OGCCB_AA?p?@?@_G??@WG??a???_????y??CA??D
```

and the edge-ordered flow is retained in
`fano-reduced-kp-core-countermodel-order24.json`.  Direct checking gives:

- 24 vertices, simple, cubic, connected and bridgeless;
- girth five, cyclic edge connectivity four, and nonplanarity;
- all seven value classes fail the two-\(T\)-join packing test;
- for every \(t=1,\ldots,7\), \(G-M_t\) has a displayed nontrivial
  two-bond after the degree-two paths are suppressed.

Hence there is no globally clean value \(t\) to which one can apply
Knappe--Pitz without tracking the location of the exchange set.

Nevertheless, switching value \(1\) on the six-circuit
\[
 \{e_2,e_3,e_4,e_5,e_8,e_9\}
\]
is legal and makes value class \(3\) pack.  This proves that the local
exchange set can escape the global two-bond obstruction.  It also proves
that the graph is positive, not negative, for the reduced one-switch
lemma.

In the initial flow, the circuit contains exactly two value-\(3\) edges,
\(e_3,e_9\), and no value-\(2=3+1\) edge.  Formula (1) of
`docs/fano-flow-one-switch-exchange.md` therefore changes
\[
 M_3\quad\hbox{to}\quad M_3-\{e_3,e_9\}.
\]
This is a literal two-edge escape, explaining why all seven global
two-bond obstructions do not block the actual repair.

The standard-library checker independently:

1. decodes graph6 and verifies the edge order and flow equations;
2. checks every edge removal of size at most three and a displayed
   cyclic four-cut;
3. checks all seven displayed two-bonds and their lifted \(G\)-cuts;
4. enumerates the complete affine \(T\)-join space for every value class;
5. confirms that the initial flow is bad; and
6. confirms the legal connected switch and the resulting packing.

Run:

```bash
python3 scratch/check_fano_reduced_kp_core_countermodel_order24.py
```

The witness was first found at order 24.  The retained complete
cyclic-4 bad-flow census has no such witness through order 14.  Random
sampling found none among 38 bad flows through order 18, 615 bad strict
order-20 samples, and 840 bad strict order-22 samples.  Those sampled
absences do not prove order-minimality.

## 5. Surviving exact obligation

A proof must select the exchange set and the deleted value together.
It is enough to show that the exchange set furnished by the simultaneous
graft algebra lies in one suitable 3-edge-connected torso of \(G-M_t\);
it is not enough to show that some \(G-M_t\) has no two-bond at all.

Equivalently, a counterexample to the surviving local statement must
show, for every certificate-compatible ordered pair \(s,t\) and every
allowed set \(S\subseteq M_s\) of size at most three, either:

1. every circuit through \(S\) meets \(M_t\); or
2. every legal such circuit leaves all seven value classes nonpacking.

No such counterexample is currently known.

## 6. Affine-complement pair exchange

There is a sharper formulation in which the circuit part is completely
solved.

Fix a Fano line
\[
 U=\{0,s,t,s+t\}\leq\mathbb F_2^3
\]
and put
\[
 B_U=f^{-1}(\mathbb F_2^3-U).
\]
At a cubic vertex, the three incident values form a Fano line.  If that
line is \(U\), the vertex has \(B_U\)-degree zero.  Every other Fano line
meets \(U\) in one nonzero point, so exactly two of its points are outside
\(U\); the vertex has \(B_U\)-degree two.  Therefore \(B_U\) is a
vertex-disjoint union of circuits, together with isolated vertices.

For a \(U\)-valued edge \(e=xy\), let
\[
 \tau_U(e)=\{K_x,K_y\}
\]
be the unordered pair, with repetition allowed, of \(B_U\)-components
containing its endpoints.

> **Affine pair-circuit lemma.**  For distinct edges \(p,q\in M_s\),
> there is a circuit \(C\) such that
> \[
> C\cap f^{-1}(U)=\{p,q\}                         \tag{2}
> \]
> if and only if
> \[
> \tau_U(p)=\tau_U(q).                            \tag{3}
> \]

### Proof

Contract every nontrivial \(B_U\)-circuit to one vertex.  The image of a
circuit satisfying (2) is a connected Eulerian multigraph with exactly
the two edges \(p,q\).  It is therefore either two parallel edges between
the same two distinct vertices, or two loops at one vertex.  In both
cases (3) follows.

Conversely, first suppose the common type is \(\{A,D\}\) with
\(A\ne D\).  The \(s\)-matching property makes the endpoints of \(p,q\)
distinct on each component.  Choose either arc of \(A\) between its two
ends and either arc of \(D\) between its two ends.  Together with \(p,q\),
the two arcs form one circuit.

Now suppose the common type is \(\{A,A\}\).  The four chord endpoints are
distinct on the circuit \(A\).  Remove those four endpoints as cyclic
break points.  If their labels alternate \(p,q,p,q\), take either
opposite pair of the four consecutive arcs.  If their labels occur
\(p,p,q,q\), take the two consecutive arcs at which the label changes.
In both cases the chosen arcs pair every \(p\)-end with a \(q\)-end, and
the two chords plus the two arcs form one circuit.  An isolated
\(B_U\)-component cannot occur twice in the common type, because distinct
\(s\)-edges form a matching. \(\square\)

The lemma gives an exact pure-deletion switch.  A circuit in (2) avoids
\(M_t\), so switching \(t\) is nowhere zero.  It also avoids
\(M_{s+t}\) and contains exactly \(p,q\) from \(M_s\).  The switch identity
therefore gives
\[
                         M'_s=M_s-\{p,q\}.             \tag{4}
\]

This proves the following exact conditional resolution statement.

> **Affine pair-exchange axiom (APX).**  Let \(G\) be a simple cyclically
> 4-edge-connected non-3-edge-colourable cubic graph and let \(f\) be a
> bad nowhere-zero \(\mathbb F_2^3\)-flow.  There are a Fano line
> \(U=\{0,s,t,s+t\}\) and distinct \(p,q\in M_s\) such that
> \[
> \tau_U(p)=\tau_U(q)
> \]
> and the matching \(M_s-\{p,q\}\) packs two edge-disjoint boundary
> \(T\)-joins.

If APX holds, the affine pair-circuit lemma and (4) produce a good
one-circuit neighbour.  Hence APX implies the reduced one-switch lemma.
Together with the standard minimum-counterexample reductions and the
8-flow theorem, APX implies standard FiveCDC.

APX is a finite statement on two exact relations.  For each \(s\), let
\[
\begin{split}
 {\cal P}_s&=\bigl\{\{p,q\}\subseteq M_s:
       M_s-\{p,q\}\text{ packs}\bigr\},\\
 {\cal A}_s&=\bigcup_{U\ni s}
       \bigl\{\{p,q\}\subseteq M_s:\tau_U(p)=\tau_U(q)\bigr\}.
\end{split}
\]
The entire unresolved existence claim is
\[
                    {\cal P}_s\cap{\cal A}_s\ne\varnothing
                    \quad\text{for some }s.            \tag{5}
\]

Failure of (5) is stronger than seven original odd-\(K_{2,3}\)
obstructions.  For every affine-compatible pair, the reduced matching is
still contained in a binary cycle (delete \(p,q\) from the original exact
zero matching, which is contained in a functional support).  Thus its
component-parity branch is unavailable, and nonpacking again forces an
odd-\(K_{2,3}\) graft minor.  A counterexample to APX therefore carries
the seven original graft obstructions plus one further labeled graft
obstruction for every pair in every \({\cal A}_s\).

The exact screen in
`scratch/search_fano_reduced_one_switch_binary.cpp` tests (5) by complete
T-join SAT and literal circuit enumeration.  It currently passes:

- 77 sampled bad strict order-22 flows;
- 331 sampled bad strict order-24 flows; and
- 1,527 sampled bad flows on ten strict order-40 graphs.

The weaker assertion \({\cal P}_s\ne\varnothing\) for some \(s\) passed
859, 1,536, and 1,426 sampled bad flows at orders 22, 24, and on the first
order-40 graph, respectively.  These are reconnaissance counts, not a
proof of APX.

In the frozen order-24 example, take
\[
 U=\{0,1,2,3\},\quad s=3,\quad t=1,\quad
 \{p,q\}=\{e_3,e_9\}.
\]
The affine complement has circuit-component vertex sets of sizes
\(10,8,5\), plus one isolated vertex.  Both \(p\) and \(q\) join the
size-10 component to the size-8 component, so their \(\tau_U\)-types
agree.  The retained two-\(T\)-join certificate proves
\(M_3-\{p,q\}\in{\cal P}_3\).

## 7. A proved counting lemma for the affine relation

The affine relation \({\cal A}_s\) itself has a useful exact lower-bound
criterion.  Fix one Fano line \(U\).  Let \(z_U\) be the number of
isolated-vertex components of \(B_U\), and let \(r_U\) be the number of
nontrivial circuit components.

> **Affine-type counting lemma.**  For \(s\in U-\{0\}\), if no two edges
> of \(M_s\) have the same \(\tau_U\)-type, then
> \[
>             |M_s|\le z_U+\binom{r_U+1}{2}.           \tag{6}
> \]
> Consequently, some \(s\in U-\{0\}\) has a repeated type whenever
> \[
>             n>4z_U+3r_U(r_U+1),                     \tag{7}
> \]
> where \(n=|V(G)|\).

### Proof

Split the edges of \(M_s\) into those with an endpoint in an isolated
component of \(B_U\) and those whose endpoints both lie on nontrivial
circuit components.  Since \(M_s\) is a matching, each isolated vertex is
an endpoint of at most one edge of the first kind.  There are therefore at
most \(z_U\) such edges.

There are exactly
\[
                 \binom{r_U+1}{2}
\]
unordered pairs, with repetition allowed, of the \(r_U\) circuit
components.  If \(\tau_U\) has no repeated value on \(M_s\), there is at
most one edge of the second kind for each such pair.  This proves (6).

At an isolated vertex the local Fano line is \(U\), so all three incident
edges are \(U\)-valued.  At every other vertex exactly one incident edge
is \(U\)-valued.  Counting endpoints of the \(U\)-valued edges gives
\[
  2\sum_{s\in U-\{0\}}|M_s|
       =3z_U+(n-z_U)=n+2z_U.                          \tag{8}
\]
If none of the three values has a repeated type, summing (6) and using
(8) gives
\[
 \frac{n+2z_U}{2}
      \le3z_U+3\binom{r_U+1}{2},
\]
which is equivalent to the negation of (7). \(\square\)

If \(G\) has girth \(g\), then every nontrivial component of \(B_U\) is a
circuit of length at least \(g\), so
\[
                         gr_U\le n-z_U.               \tag{9}
\]
Equations (7)--(9) are a genuine finite repeat criterion.  They do not
prove APX: a repeated \(\tau_U\)-type supplies membership in
\({\cal A}_s\), but the same pair must still lie in \({\cal P}_s\).

### A score-one boundary instance

The package
`fano-apx-score1-order24.json` and
`check_fano_apx_score1_order24.py` freezes a strict order-24 bad flow
found by adversarial search.  Complete independent replay gives exactly
one APX witness,
\[
                        (s,\mu,\{p,q\})=(7,6,\{e_1,e_{22}\}),
\]
where \(U=\ker\mu\).  It enumerates all \(4,681\) simple circuits.  Exactly
\(1,371\) legal circuit switches exist; exactly \(180\) leave the flow
bad, and every one of those bad neighbours still has APX score at least
one.  The checker also replays
the displayed ten-edge affine circuit switch by value \(1\), after which
values \(2,5,7\) pack.  Run:

```bash
python3 scratch/check_fano_apx_score1_order24.py
```

This is a locally stable near-state, not a lower-bound theorem.  In
particular, the score-one computation neither proves APX nor rules out a
score-zero bad flow elsewhere.

## 8. A collision-versus-nonpacking criterion

The counting argument can incorporate the packing relation without
assuming that every affine repeat packs.  Fix \(s\ne0\), and put
\[
 q_s=\binom{|M_s|}{2}-|{\cal P}_s|,
\]
the number of pairs whose deletion does not pack.

For a line \(U\ni s\), let \(h_{s,U}\) be the number of \(M_s\)-edges
whose two endpoint components in \(B_U\) are both nontrivial, and put
\[
 N_U=\binom{r_U+1}{2}.
\]
For \(N\ge1\), write \(h=aN+b\), \(0\le b<N\), and define
\[
 L_N(h)=b\binom{a+1}{2}+(N-b)\binom a2.               \tag{10}
\]
Set \(L_0(0)=0\); the case \(N_U=0\) necessarily has
\(h_{s,U}=0\).
This is the minimum number of equal-box pairs obtained by distributing
\(h\) objects among \(N\) boxes as evenly as possible.

> **Packing-intersection criterion.**  If
> \[
>       \sum_{\substack{U\ni s\\ \dim U=2}}
>             L_{N_U}(h_{s,U})>3q_s,                  \tag{11}
> \]
> then \({\cal P}_s\cap{\cal A}_s\ne\varnothing\).

Indeed, types involving an isolated \(B_U\)-component cannot repeat,
because \(M_s\) is a matching.  The remaining \(h_{s,U}\) edges occupy
the \(N_U\) unordered pairs of nontrivial components, so convexity of
\(\binom{x}{2}\) gives at least \(L_{N_U}(h_{s,U})\) compatible-pair
occurrences for this \(U\).  There are exactly three Fano lines through
\(s\), so any fixed unordered pair of \(M_s\)-edges is counted for at
most three choices of \(U\).  If every compatible pair were nonpacking,
the left side of (11) would consequently be at most \(3q_s\), a
contradiction.

One may replace \(h_{s,U}\) by the weaker lower bound
\[
                    h_{s,U}\ge\max(0,|M_s|-z_U),       \tag{12}
\]
because at most \(z_U\) matching edges can touch isolated components.
The resulting condition depends only on
\(|M_s|,z_U,r_U,q_s\).

Criterion (11) is a proved finite obstruction budget.  It still does not
resolve APX: no universal upper bound on \(q_s\) strong enough for (11)
is presently proved.

## 9. Four canonical defect vectors for every nonpacking pair

There is a more structural obstruction budget.  Fix \(s\ne0\) and
\(\nu\in\Lambda_s\), so \(\nu(s)=1\).  Let
\[
 F_\nu=\{e:\nu(f(e))=0\},
\]
and contract each component of \(F_\nu\).  For an edge set \(R\), write
\[
 \partial_\nu R\in\mathbb F_2^{{\cal K}_\nu}
\]
for the odd-degree vector of the image of \(R\) in this quotient.
Section 3 proves that the vector
\[
                  r_\nu=\partial_\nu M_w              \tag{13}
\]
is independent of the choice of \(w\) with \(\nu(w)=1\): its support is
exactly the rainbow-odd components of \(F_\nu\).

For a pair \(p,q\in M_s\), put
\[
 \sigma_\nu(p,q)=\partial_\nu\{p,q\},\qquad
 d_\nu(p,q)=r_\nu+\sigma_\nu(p,q).                    \tag{14}
\]

> **Canonical pair-deletion certificate.**  If
> \(d_\nu(p,q)=0\) for some \(\nu\in\Lambda_s\), then
> \(M_s-\{p,q\}\in{\cal P}_s\).  Consequently, if the pair is
> nonpacking, all four vectors
> \[
>                    d_\nu(p,q)\quad(\nu\in\Lambda_s) \tag{15}
> \]
> are nonzero.

### Proof

Put \(M'=M_s-\{p,q\}\) and \(K'=G-M'\).  For
\(\lambda\in\Lambda_s\), the binary support of \(\lambda\circ f\),
with \(M'\) removed, is a \(\partial M'\)-join
\[
                       J'_\lambda=J_\lambda\cup\{p,q\}.
\]
Fix \(\lambda\ne\nu\), and let \(w\) be the unique value for which the
two original canonical joins meet in \(M_w\).  Then
\[
                  J'_\lambda\cap J'_\nu
                       =M_w\mathbin{\dot\cup}\{p,q\}.  \tag{16}
\]
Holding \(J'_\nu\) fixed and adding a binary cycle \(C\) of \(K'\) to
\(J'_\lambda\) makes the two joins disjoint exactly when
\[
       C\cap J'_\nu=M_w\mathbin{\dot\cup}\{p,q\}.      \tag{17}
\]

The cuts of \(K'\) contained in \(J'_\nu\) are precisely the cuts of
unions of \(F_\nu\)-components.  Cycle--cut orthogonality therefore says
that (17) is solvable exactly when
\[
 \partial_\nu(M_w\mathbin{\dot\cup}\{p,q\})
       =r_\nu+\sigma_\nu(p,q)=0.                      \tag{18}
\]
When it is solvable, the two resulting joins are edge-disjoint, proving
the first assertion.  The second is its contrapositive. \(\square\)

Every nonzero defect vector has even Hamming weight, since it is a graph
boundary vector.  Thus a nonpacking affine repeat carries four explicit
nonempty even sets of odd-factor components, in addition to its
\(\tau_U\)-type and the odd-\(K_{2,3}\) graft obstruction.

This certificate is not an exact characterization of packing: both
canonical joins were restricted to changing only one of them in the
proof.  The unique APX witness in the score-one order-24 package has all
four canonical defect vectors nonzero and nevertheless packs by a
noncanonical pair of joins.  Hence replacing \({\cal P}_s\) by the
zero-defect subset would lose the surviving boundary instance.

## 10. Global seven-line incidence and collision inequality

The seven affine complements are not independent.  At a vertex \(v\),
write \(L(v)\) for its local Fano line.  Thus \(z_U\), as defined above,
is exactly
\[
                        z_U=|\{v:L(v)=U\}|.
\]
Let \(a_U\) count graph edges whose two endpoints both have local line
\(U\), and put \(A=\sum_Ua_U\).

For \(s\in U-\{0\}\), retain \(h_{s,U}\) from Section 8.  Then:
\[
\begin{aligned}
 \sum_U z_U&=n,                                             &(19)\\
 \sum_{U\ni s}z_U&=2|M_s|,                                 &(20)\\
 \sum_{s\in U-\{0\}}|M_s|&=\frac n2+z_U,                   &(21)\\
 \sum_{s\in U-\{0\}}h_{s,U}&=\frac n2-2z_U+a_U,            &(22)\\
 \sum_U\sum_{s\in U-\{0\}}h_{s,U}
     &=\frac{3n}{2}+A.                                     &(23)
\end{aligned}
\]

Equation (20) counts the two endpoints of every \(s\)-edge according to
their local lines; there are three lines through \(s\).  Equation (21)
is the endpoint count (8).  To prove (22), note that the total number of
\(U\)-valued edges is \(n/2+z_U\).  The \(U\)-valued edges touching a
vertex with local line \(U\) number \(3z_U-a_U\): the \(3z_U\) endpoint
incidences double-count exactly the \(a_U\) internal edges.  Deleting
these leaves precisely the edges counted by the left side of (22).
Summing (22), using (19), gives (23).

There is an equivalent seven-vertex skeleton.  Contract each local-line
class
\[
                         V_U=\{v:L(v)=U\}
\]
to one vertex, retaining loops and parallel edge objects.  For a fixed
Fano point \(s\), the matching \(M_s\) becomes a multigraph supported on
the three line-vertices \(U\ni s\), and its degree at \(U\) is exactly
\(z_U\).  Every vertex in \(V_U\) supplies its unique incident
\(s\)-edge.  Thus the seven value classes are seven simultaneous
pairings of the prescribed local-line stub counts.

In particular, (20) and (21) give the exact inversion pair
\[
 z_U=\sum_{s\in U-\{0\}}|M_s|-\frac n2,\qquad
 |M_s|=\frac12\sum_{U\ni s}z_U.                        \tag{20a}
\]
Reducing the second identity modulo two shows that the set of lines with
odd \(z_U\) is either empty or the four-line affine complement of the
three lines through one Fano point.  Indeed, the kernel of the seven
equations
\[
                  \sum_{U\ni s}z_U=0\pmod2
\]
consists of the zero word and the seven words
\[
                  1_{\{U:\,s_0\notin U\}}\quad(s_0\ne0).
\]
With the nonzero binary vectors \(1,\ldots,7\) used to index
\(U_\mu=\ker\mu\), direct elimination leaves \(z_1,z_2,z_4\) free and
gives
\[
 z_3=z_1+z_2,\quad z_5=z_1+z_4,\quad
 z_6=z_2+z_4,\quad z_7=z_1+z_2+z_4,
\]
which proves the stated kernel classification.

These identities yield a global pure-repeat criterion:
\[
 \boxed{\quad
 n+\frac23A>\sum_U r_U(r_U+1)
 \quad\Longrightarrow\quad
 \text{some affine-compatible pair exists.}\quad}          \tag{24}
\]
Indeed, if no type repeated, then
\[
 h_{s,U}\le N_U=\binom{r_U+1}{2}
\]
for all three \(s\in U-\{0\}\).  Summing this inequality and using
(23) gives the negation of (24).

There is also a global packing-intersection inequality.  Let
\[
\begin{split}
 H&=\frac{3n}{2}+A,\\
 B&=3\sum_U\binom{r_U+1}{2},\\
 Q&=\sum_{s\ne0}q_s.
\end{split}
\]
Distribute the \(H\) big--big edge occurrences among the \(B\)
\((s,U,\tau)\)-boxes.  Convexity gives at least \(L_B(H)\) equal-type
pair occurrences.  A fixed unordered pair belongs to at most the three
lines through its value.  Therefore failure of APX implies
\[
                         L_B(H)\le3Q.                    \tag{25}
\]
The sharper non-aggregated lower bound is
\[
 \sum_U\sum_{s\in U-\{0\}}L_{N_U}(h_{s,U})\le3Q.          \tag{26}
\]
Either strict reverse inequality proves APX.

Finally, if \(G\) has girth \(g\), summing (9) over all seven lines gives
\[
                         \sum_U r_U\le\frac{6n}{g}.       \tag{27}
\]
Equations (19)--(27) are a global seven-value constraint, not seven
separate estimates.  They still stop short of resolution: no bound on
the global nonpacking budget \(Q\), or on the distribution of the
\(r_U\), strong enough to reverse (25) or (26) is currently proved.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated and corrected the
Knappe--Pitz reduction, found the clean-core countermodel, wrote the
checker, and drafted this note.  An earlier computational read used the
wrong edge ordering and was withdrawn before freezing this package.  The
current checker reconstructs the graph6 bit order explicitly.  This is
not independent human peer review.
