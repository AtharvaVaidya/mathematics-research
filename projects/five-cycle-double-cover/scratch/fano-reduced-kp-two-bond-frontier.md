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

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated and corrected the
Knappe--Pitz reduction, found the clean-core countermodel, wrote the
checker, and drafted this note.  An earlier computational read used the
wrong edge ordering and was withdrawn before freezing this package.  The
current checker reconstructs the graph6 bit order explicitly.  This is
not independent human peer review.
