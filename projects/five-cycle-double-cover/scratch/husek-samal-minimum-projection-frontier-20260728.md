# Minimum extendable Fano projections: an exchange theorem and finite frontier

Date: **2026-07-28**

Status: **PROVED EXCHANGE THEOREM / EXACT FINITE CENSUS /
UNRESOLVED UNIVERSAL STEP**.

This note develops a possible route from the flow formulation of
Hušek--Šámal, Conjecture 3.19, to the standard five-cycle-double-cover
conjecture.  The exchange theorem below is elementary and complete.  The
finite census is exact and reproducible.  The proposed universal next step
is explicitly a conjecture: this note does **not** resolve Five-CDC and
does not claim priority.

Throughout, a binary cycle means an Eulerian edge set.  All graphs in the
finite census are finite, simple, connected, and cubic.

## 1. Extendable and clean projections

Put \(K=\mathbb F_2^2\).  Write a three-bit flow as
\[
                 f=(h,s):E(G)\longrightarrow\mathbb F_2\times K,
                                                        \tag{1}
\]
where \(h:E(G)\to\mathbb F_2\) and \(s:E(G)\to K\) are
flows.  We identify \(h\) with its support.

Call a nonzero binary cycle \(h\) **extendable** if (1) can be chosen
nowhere zero.  Equivalently, there are two binary cycles \(p,q\) such that
every edge outside \(h\) belongs to \(p\cup q\): take
\(s=(p,q)\).  Notice that this is an existential property of \(h\);
no initially supplied Fano flow is fixed.

For an extension \(f=(h,s)\) and \(c\in K\), put
\[
                         M_c=\{e\in h:s(e)=c\}.        \tag{2}
\]
Every \(M_c\) is a matching.  Indeed, two incident edges of value
\((1,c)\) would force the third incident flow value to be zero.

The projection \(h\) is called **cleanable** if there is an extension
\(s=(p,q)\) for which
\[
 |\,\delta(W)\cap p\cap q\,|\equiv0\pmod2             \tag{3}
\]
for every component \(W\) of \((V(G),E(G)-h)\).
This is the two-cycle form of Hušek--Šámal's component parity criterion.
To see that the affine target is immaterial, flow conservation on
\(\delta(W)\) says that the four multiplicity parities
\[
       |\delta(W)\cap M_c|\pmod2\qquad(c\in K)         \tag{4}
\]
are equal.  Thus they are either all even, when (3) holds, or all odd.
The latter case will be called **rainbow-odd**.

Consequently the Five-CDC conjecture in this language asks for some
extendable cleanable \(h\), with the usual Tait-colourable case allowing
\(h=\varnothing\).

## 2. Exact minimum-support exchange theorem

Assume that \(G\) is not Tait-colourable, so every extendable projection
is nonempty.  Choose \(h\) with minimum cardinality among all extendable
projections, and fix any nowhere-zero extension \(f=(h,s)\).

> **Minimum-projection exchange theorem.**  For every \(c\in K\) and
> every binary cycle \(C\) satisfying \(C\cap M_c=\varnothing\),
> \[
>                       |C\cap h|\le |C-h|.            \tag{5}
> \]
> Equivalently, \(h\) is a minimum-cardinality binary cycle containing
> \(M_c\), simultaneously for all four \(c\in K\).

### Proof

Fix \(c\in K\), and put \(t=(1,c)\).  Add \(t\) to the flow value on
every edge of \(C\):
\[
 f'(e)=
 \begin{cases}
 f(e)+t,&e\in C,\\
 f(e),&e\notin C.
 \end{cases}                                          \tag{6}
\]
Because \(C\) is a binary cycle, the added function is a flow, so \(f'\)
is a flow.  The only edges that could become zero are the edges that had
value \(t\), namely the edges of \(M_c\).  The hypothesis
\(C\cap M_c=\varnothing\) therefore makes \(f'\) nowhere zero.

The first coordinate of \(f'\) is \(h\mathbin\triangle C\).  Hence
\(h\mathbin\triangle C\) is another extendable projection.  Minimality of
\(h\) gives
\[
 |h|\le|h\mathbin\triangle C|
      =|h|+|C-h|-|C\cap h|,
\]
which is exactly (5).

For the equivalent formulation, first note that \(M_c\subseteq h\).
If \(h'\) is any binary cycle containing \(M_c\), rebase the low
coordinates by replacing \(s\) with \(s+ch\).  This is a flow whose exact
zero set is \(M_c\).  Therefore \((h',s+ch)\) is nowhere zero: outside
\(h'\) the only possible zeros would lie in \(M_c\), and those edges are
contained in \(h'\).  Thus \(h'\) is extendable and \(|h|\le|h'|\).

Conversely, apply this minimum-containing property to
\(h'=h\mathbin\triangle C\).  It contains \(M_c\) precisely when
\(C\cap M_c=\varnothing\), and the same cardinality calculation gives
(5). \(\square\)

There is an equivalent ordinary \(T\)-join statement.  Let \(T_c\) be the
set of endpoints of \(M_c\).  Then
\[
                         J_c=h-M_c                    \tag{7}
\]
is a shortest \(T_c\)-join in \(G-M_c\).  This is stronger than choosing
a cardinality-minimum exact-zero matching: it minimizes the whole cycle
\(M_c\cup J_c\), and does so simultaneously for the four affine rebases.
The distinction is essential because the separate conjecture that a
minimum exact-zero matching must pack is false.

Two immediate consequences are useful.

> **Flow-resistance bound.**  If \(r_f(G)\) denotes the minimum number of
> zero edges in an \(\mathbb F_2^2\)-flow on \(G\), then every extendable
> projection satisfies
> \[
>                              |h|\ge4r_f(G).           \tag{8}
> \]

For each \(c\), the rebased low flow \(s+ch\) has exact zero set \(M_c\),
so \(|M_c|\ge r_f(G)\).  The four \(M_c\)'s partition \(h\), and summing
the four inequalities proves (8).  This bound is only a consistency check;
it is not a Five-CDC criterion.

> **Four-colour circuit corollary.**  Every circuit component of \(h\)
> contains an edge of every \(M_c\).

If a circuit component \(D\) omitted \(M_c\), then \(D\) itself would be a
cycle avoiding \(M_c\), while
\(|D\cap h|=|D|>|D-h|=0\), contradicting (5).

> **Rainbow shortcut corollary.**  Every binary cycle \(C\) with
> \(|C\cap h|>|C-h|\) meets all four sets \(M_c\).

This is the contrapositive of (5), applied to any omitted colour.

These statements include disconnected binary cycles and parallel-edge
circuits without change.  Loops require the standard convention that a
loop contributes degree two to parity; the finite census below is simple,
so no loop reduction is used computationally.

## 3. The unresolved universal step

The exact remaining assertion suggested by the data is:

> **Minimum extendable projection conjecture.**  Every bridgeless cubic
> graph has a minimum-cardinality extendable projection that is
> cleanable.

This would imply Five-CDC immediately from the equivalence in Section 1.
A stronger statement saying that every minimum projection is cleanable
also survives the finite census below, but is not needed.

Suppose, toward this step, that a minimum \(h\) is not cleanable.  Every
extension then has a rainbow-odd component \(W\) of \(G-h\): each of the
four \(M_c\) crosses \(\delta(W)\) oddly.  The precise open exchange
obligation is to turn this common four-colour odd cut into either

1. a binary cycle \(C\) avoiding some \(M_c\) with
   \(|C\cap h|>|C-h|\), contradicting (5); or
2. a sequence of support-neutral low-coordinate recolourings followed by
   such a strict exchange.

The word “sequence” cannot presently be removed.  Known order-12 local
switching traps have four disjoint colour classes meeting every immediate
component-reducing cycle; a support-preserving recolouring escapes them.
Likewise, a fixed Fano flow can have every one of its seven projections
dirty.  These examples do not refute the minimum-projection conjecture,
but they invalidate a proof that simply chooses an arbitrary current
flow or assumes one elementary switch always works.

The first irreducible human proof obligation is therefore:

> From a rainbow-odd component of an **uncleanable globally
> minimum-support projection**, derive a negative colour-avoiding cycle
> after allowable neutral recolouring, using all four simultaneous
> shortest-\(T_c\)-join inequalities.

No proof of that statement is supplied here.

## 4. Exact order-18 census

The accompanying checker performs no SAT sampling.  For each canonical
connected cubic graph produced by `nauty-geng`, it checks every edge
deletion for connectivity, tests Tait colourability exactly, enumerates
the full binary cycle space, and quotients pairs of cycles \((p,q)\) by
the exact semantic pair
\[
                         (p\cup q,\ p\cap q).          \tag{9}
\]
For each candidate \(h\), liftability is
\[
                         E-h\subseteq p\cup q,         \tag{10}
\]
and cleanability additionally checks (3) on every component of \(G-h\).
Candidates are processed by increasing \(|h|\).  No graph is discarded
using a snark or cyclic-connectivity reduction.

At order 18 the complete generated population is:

* 41,301 connected simple cubic graphs;
* 39,866 bridgeless graphs;
* 179 bridgeless non-Tait graphs.

Every minimum-cardinality extendable projection on all 179 hard graphs is
cleanable.  This is a finite theorem only.

The exact order-18 minimum-size histogram is
\[
  5:166,\qquad 6:11,\qquad 7:1,\qquad 8:1,
\]
and the canonical hard-record SHA-256 is
`82b01cc2f01d4f50f7745f4bdb1b3dc46ade798d452a9d4f11d4a91d738a7834`.

Run from the repository root:

```sh
python3 scratch/check_husek_samal_minimum_projection_frontier.py --order 18
```

The script requires `geng` on `PATH` and imports the independent graph and
cycle-space primitives from
`scratch/search_fano_all_bad_projection_subspaces.py`.  A typical run
takes about two minutes on an Apple Silicon workstation.  The final
record digest is printed by the checker; it hashes, in canonical graph
order, each hard graph's graph6 string, minimum size, number of minimum
extendable projections, and number cleanable.

## 5. Verification and disclosure

The mathematical proof in Section 2 is short enough to check directly:
the only ingredients are flow addition on a binary cycle, avoidance of the
unique cancelling value, and a cardinality identity for symmetric
difference.  Section 3 is explicitly conjectural.  The census supports
that conjecture but cannot establish it.

This route, checker, experiments, and draft were developed by OpenAI Codex
agents under human direction.  The Hušek--Šámal equivalence and the
standard matching/\(T\)-join formulation are prior work and are not claimed
as new here.  Any public version should retain this AI-use disclosure and
should be reviewed line by line by a human graph theorist before citation.
