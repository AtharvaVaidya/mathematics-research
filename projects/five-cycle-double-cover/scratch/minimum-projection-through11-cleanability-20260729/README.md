# Minimum extendable projections through size eleven are cleanable

Date: 2026-07-29

Status: **HUMAN-CHECKABLE THEOREM WITH EXACT FINITE CERTIFICATES /
FIRST COUNTERMODEL TO THE DIRECT-REPAIR STRENGTHENING / NOT A
FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## Theorem

Let \(G\) be a finite connected bridgeless loopless cubic graph;
parallel edges are allowed.  A binary cycle \(h\) is **extendable** if
there are binary cycles \(p,q\) with
\[
                         E(G)-h\subseteq p\cup q.          \tag{1}
\]
Equivalently, \(f=(h,s)\), where \(s=(p,q)\), is a nowhere-zero
\(\mathbb F_2\times\mathbb F_2^2\)-flow.

For \(c\in K=\mathbb F_2^2\), put
\[
                         M_c=\{e\in h:s(e)=c\}.            \tag{2}
\]
The extension is **clean** if every component \(W\) of \(G-h\) satisfies
\[
                   |M_c\cap\delta(W)|\equiv0\pmod2
                   \quad(c\in K).                         \tag{3}
\]

> **Theorem.**  Every cardinality-minimum extendable projection of
> size at most eleven is cleanable.

Together with the Hušek--Šámal clean-projection criterion, this proves
FiveCDC for the class in which the minimum extendable-projection size is
at most eleven.  It does not bound the minimum universally and therefore
does not resolve FiveCDC.

## 1. Structural reduction from global minimality

Fix a minimum projection \(h\) and an extension \(f=(h,s)\).  The
minimum-projection exchange theorem says that for every \(c\in K\) and
binary cycle \(C\) avoiding \(M_c\),
\[
                         |C\cap h|\le |C-h|.              \tag{4}
\]
Add the constant flow value \((1,c)\) on \(C\): avoidance keeps the new
flow nowhere zero, its first-coordinate support is
\(h\mathbin\triangle C\), and minimality gives (4).

Every circuit component \(D\) of \(h\) consequently contains all four
sets \(M_c\).  Otherwise \(C=D\) violates (4).  Thus each circuit has at
least four edges.  The support shapes through size eleven are:

- one circuit of length \(4,\ldots,11\);
- two circuits of lengths \(4+4,4+5,4+6,4+7,5+5,\) or \(5+6\).

The zero projection is already clean.  The package
`verify_through10.py` proves the theorem through size ten by direct
boundary cleaning.  Only the three size-eleven shapes \(11\), \(4+7\),
and \(5+6\) are new here.

## 2. Direct componentwise-linear cleaning

Index every circuit of \(h\) cyclically, writing \(c_i=s(e_i)\).
Adjacent values are distinct because the third edge \(k_i\notin h\)
has nonzero low value
\[
                         d_i=s(k_i)=c_{i-1}+c_i.          \tag{5}
\]
The components of \(G-h\) define a set partition \(\pi\) of the circuit
vertices.  Conservation gives, for every block \(a\),
\[
                    \mathop{\mathbin\oplus}_{\pi_i=a}d_i=0, \tag{6}
\]
and makes the four cut-colour parities equal.  A block is dirty when
that common parity is one.

Choose one \(L_a\in\mathrm{GL}(2,2)\) per block and transform every low
value inside that component.  New low values \(r_i\in K\) on \(h\)
must satisfy
\[
                    r_{i-1}+r_i=L_{\pi_i}d_i.             \tag{7}
\]
Independent starting values are allowed on distinct circuit components.
If all resulting cut-colour parities are even, the transformed internal
flows and the \(r_i\)'s give a clean nowhere-zero three-bit flow: an
edge of \(h\) has full value \((1,r_i)\), so \(r_i=0\) is allowed.

The direct repair is constructive, exact, and independent of the
internal graph structure of the components of \(G-h\).

## 3. Exact size-eleven classification

`verify.py` uses only the Python standard library.  It quotients colour
words by the global affine action and the exact dihedral action on each
circuit, but enumerates every set partition for each word orbit.  It
generates exactly the charge-valid partitions (6), tests dirtiness, and
exhausts the six component maps and relative circuit starts in (7).

| support shape | canonical words | charge-valid word/partitions | dirty states | direct-clean failures |
|:---:|---:|---:|---:|---:|
| one 11-cycle | 345 | 1,183,710 | 919,764 | 0 |
| 4-cycle + 7-cycle | 17 | 57,500 | 46,786 | 0 |
| 5-cycle + 6-cycle | 26 | 87,884 | 71,170 | 14 |

The 14 literal failures form 11 orbits after the full dihedral,
affine-colour, and component-renaming action.  Every state and its orbit
membership are frozen in `size11-frontier-certificates.json`.

## 4. Why all 14 failures contradict global minimality

The direct boundary lemma is false at size eleven, but the
global-minimum theorem survives.

For every failed \(5+6\) state, `verify.py` supplies maps \(L_a\), two
circuit starts, and values \(r_i\) satisfying (7) such that every
six-cycle value is nonzero.  Define a new first-coordinate support to
be only the five-cycle:

- on the five-cycle, use full values \((1,r_i)\), which are nonzero
  regardless of the low coordinate;
- on the six-cycle, use \((0,r_i)\), which are nonzero by the
  certificate;
- inside each component of \(G-h\), use the transformed nonzero low
  flow \(L_as\).

Equation (7) verifies conservation at every circuit vertex, and the
component maps preserve every internal equation.  This is a
nowhere-zero three-bit flow whose first-coordinate support has size
five.  Therefore none of the 14 states can come from a globally minimum
size-eleven projection.

It follows that a genuine minimum size-eleven extension must pass the
direct-clean test.  This proves the theorem.

This replacement argument is boundary-universal: it does not assume
short internal paths, minimal multipoles, high cyclic connectivity, or
any particular realization of a component.

## 5. Smallest countermodel to the direct-repair strengthening

Although the 14 states are nonminimal, they are not fictitious.  Replace
every two-vertex partition block by one edge and every three-vertex block
by a claw.  All 14 minimal realizations are isomorphic to the same
12-vertex graph, with canonical graph6 encoding

```text
Kt?G?DIPOqCo
```

It is the triangle-expanded Petersen graph.  The verifier checks:

- finite, simple, connected, cubic, and bridgeless;
- non-Tait-colourable by exhaustive three-edge-colouring;
- nonplanar via an explicitly verified Petersen minor obtained by
  contracting the displayed triangle;
- the target \(5+6\) projection has size 11, is extendable, and is
  **not cleanable**, by exhaustive enumeration of the 128 binary cycles
  and all semantic cycle pairs;
- the minimum extendable-projection size is 5;
- exactly six size-five projections are extendable, and all six are
  cleanable.

Thus the following stronger claim is false:

> Every extendable projection whose every circuit contains all four
> affine classes is directly componentwise-\(\mathrm{GL}(2,2)\)
> cleanable.

The countermodel is sharp in support size for the exact abstract
boundary problem: the through-ten checker finds zero failures.  It is
not a FiveCDC counterexample; its clean minimum projections are explicit
and exactly checked.

## Reproduction

Run:

```sh
python3 verify_through10.py
python3 verify.py
python3 independent_verify_frontier.py
shasum -a 256 -c SHA256SUMS
```

`verify.py` regenerates all size-eleven counts, the 14 literal failures,
the 11 orbit representatives, every size-five replacement, all graph
isomorphisms, and the complete realization metadata, then compares the
result byte for byte with the frozen JSON.

`independent_verify_frontier.py` does not import `verify.py`.  Starting
only from the frozen JSON, it separately implements the dihedral
word/partition action, validates all 14 component-map and recurrence
certificates, decodes the graph6 row, checks every supplied graph
isomorphism, checks simplicity/cubicity/bridgelessness/non-Tait
colourability and the Petersen contraction, and exhausts the
representative graph's 128 binary cycles and all cycle pairs.  It thereby
rechecks the 11 orbit memberships, the uncleanable size-eleven target,
and the six clean minimum projections of size five without trusting the
primary verifier's graph or projection routines.  It does not independently
regenerate the 14 failures from all size-eleven boundary states; that is
the primary verifier's trust boundary.

## Scope and disclosure

The theorem assumes a connected loopless cubic graph.  Parallel edges
are allowed; loops require separate conventions and are outside the
statement.  The finite classifiers are exhaustive boundary proofs, not
graph sampling.  This has not received independent human peer review.

OpenAI Codex agents under human direction discovered the direct repairs
and first failures, derived the size-five replacement, implemented the
independent checkers, and prepared this report.  Complete proof data are
included so the result can be verified without trusting an AI-generated
summary.  No literature-wide priority claim is made, and FiveCDC remains
unresolved.
