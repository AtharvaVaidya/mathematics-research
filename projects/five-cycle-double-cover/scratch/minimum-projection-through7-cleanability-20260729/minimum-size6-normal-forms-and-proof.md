# Dirty minimum projections of size six: three boundary normal forms

Date: 2026-07-29

Status: **EXACT FINITE NORMAL-FORM THEOREM AND CLEANABILITY COROLLARY
THROUGH SIZE SIX / NOT A FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## Statement

Let \(G\) be a finite connected bridgeless loopless cubic non-Tait graph,
and let \(h\) be a cardinality-minimum extendable binary projection with
\(|h|=6\).  Fix a nowhere-zero extension
\[
                   f=(h,s):E(G)\longrightarrow
                   \mathbb F_2\times\mathbb F_2^2.        \tag{1}
\]
If this extension is dirty, and if it cannot be turned into a
nowhere-zero \(\mathbb F_2^2\)-flow by applying one independent
\(\mathrm{GL}(2,2)\) map to the low values on each component of \(G-h\),
then, up to the equivalences in Section 3, its boundary data is one of
exactly three rows:

| row | affine colours \(c_0\ldots c_5\) on \(h\) | component labels of \(v_0\ldots v_5\) | two-terminal component |
|---:|:---|:---|:---|
| 1 | `010123` | `001001` | \(\{v_2,v_5\}\) |
| 2 | `010232` | `001010` | \(\{v_2,v_4\}\) |
| 3 | `012013` | `000101` | \(\{v_3,v_5\}\) |

Both components are dirty.  Moreover the minimum-projection exchange
theorem forces the distance between the displayed terminals inside
their component of \(G-h\) to be at least \(3,2,2\), respectively.

The rows are survivors of one exact repair class.  They are not graphs,
not uncleanable projections, and not counterexamples to the
minimum-projection conjecture.  In fact, the proved two-component
line-cleaning theorem eliminates all three and gives the following
corollary.

> **Minimum-size-six corollary.**  Every cardinality-minimum extendable
> projection of size at most six in a connected bridgeless loopless cubic
> graph is cleanable (with the zero projection used in the Tait case).

## 1. Why the support is one six-cycle

For \(c\in\mathbb F_2^2\), put
\[
                         M_c=\{e\in h:s(e)=c\}.            \tag{2}
\]
The minimum-projection exchange theorem implies that every circuit
component of \(h\) meets all four \(M_c\).  Every component therefore has
at least four edges.  Since \(|h|=6\), \(h\) is one ordinary six-cycle.

Index it as
\[
 v_0,e_0,v_1,e_1,\ldots,v_5,e_5,v_0,\qquad e_i=v_iv_{i+1}, \tag{3}
\]
with subscripts modulo six, and put \(c_i=s(e_i)\).  Adjacent \(c_i\)'s
are distinct, or the third edge at their common vertex would have low
value zero.  All four affine colours occur.

Let \(k_i\) be the unique edge of \(G-h\) incident with \(v_i\), and put
\[
                         d_i=s(k_i)=c_{i-1}+c_i\ne0.       \tag{4}
\]
Every component of \(G-h\) contains at least one \(v_i\), because \(G\)
is connected.

## 2. Exact boundary constraints

Represent the components of \(G-h\) by a set partition
\(\pi=(\pi_0,\ldots,\pi_5)\), where \(\pi_i\) is the component containing
\(v_i\).

For a component \(W\), conservation gives two equivalent boundary
checks:

1. the four parities
   \[
                  |\delta(W)\cap M_c|\pmod2,\quad c\in\mathbb F_2^2,
                                                               \tag{5}
   \]
   are equal; and
2. the low boundary charges satisfy
   \[
                         \sum_{v_i\in W}d_i=0.             \tag{6}
   \]

A component is dirty when the common parity in (5) is one.  The script
enumerates every proper cyclic four-colour word of length six using all
four colours and every set partition of its six vertices.  It retains
exactly the partitions satisfying (5)--(6) and having at least one dirty
component.

## 3. The exact equivalence action

The finite pairs \((c,\pi)\) are quotiented by:

- the dihedral group of the six-cycle (six rotations and six
  reflections);
- the affine group
  \(\mathrm{AGL}(2,2)\) on the four affine colours; and
- arbitrary renaming of the components of \(G-h\).

Here \(\mathrm{AGL}(2,2)\cong S_4\), so the script may enumerate all 24
permutations of the four colour names.  If
\[
                          c\longmapsto Lc+t,               \tag{7}
\]
then the pendant values in (4) transform as \(d_i\mapsto Ld_i\); the
translation cancels.  Thus (7) preserves the repair question below.
Component labels are put in restricted-growth order, which is a
canonical relabelling rather than an additional assumption.

## 4. Exact componentwise-GL repair test

Fix the low values \(s\) on \(G-h\).  The modeled repair class chooses,
independently for each component \(W\), one
\[
                          L_W\in\mathrm{GL}(2,2)            \tag{8}
\]
and replaces every low edge value in \(W\) by \(L_Ws(e)\).
Internal conservation and nonzeroness are preserved.  At \(v_i\), the
new pendant value is
\[
                          g_i=L_{\pi_i}d_i.                \tag{9}
\]

There is a nowhere-zero \(\mathbb F_2^2\)-flow on all of \(G\) extending
these transformed component values if and only if there are
\[
                          r_i\in\mathbb F_2^2-\{0\}         \tag{10}
\]
on the cycle edges satisfying
\[
                          r_{i-1}+r_i=g_i                  \tag{11}
\]
for every \(i\), cyclically.

This is both necessary and sufficient in the modeled class.  Necessity
is the flow equation at \(v_i\).  Conversely, (11) supplies the missing
cycle-edge equations, while (8) already preserves every internal
equation; (8) and (10) make all values nonzero.  A nowhere-zero
\(\mathbb F_2^2\)-flow on a cubic graph is a Tait colouring.

There are six choices for each \(L_W\).  Once \(r_5\) is chosen among
the three nonzero values, (11) uniquely determines
\(r_0,\ldots,r_4\); the test accepts exactly when no \(r_i\) is zero and
the final value agrees cyclically with \(r_5\).  Thus the script's
enumeration is an exact necessary-and-sufficient decision for
componentwise-GL repair of the fixed state.

This is deliberately narrower than arbitrary Tait recolouring of a
component: a component might admit a different low-flow orbit not
obtained from the supplied \(s\) by one global \(L_W\).  Failure of the
test therefore does not prove that \(G\) is non-Tait or that \(h\) is
uncleanable.

## 5. Exhaustive quotient

Before quotienting, 432 valid dirty pairs fail the repair test.  Under
the action in Section 3 they form exactly three orbits, each of raw size
144, represented by the three displayed rows.  In every survivor the
partition has two blocks, of sizes four and two, and both blocks have
parity vector \((1,1,1,1)\).

Run:

```sh
python3 verify.py
```

The checker uses only the Python standard library.  It regenerates every
word and partition, checks (5)--(6), enumerates all componentwise GL
maps and all nonzero starting values, computes the full equivalence
orbit, and asserts the three representatives and counts above.

## 6. Terminal-distance lower bounds

Let \(B\) be the two-terminal component in one of the three rows, and
let \(P\) be any path inside \(B\) between its displayed terminals.
The union of \(P\) with either corresponding arc of the six-cycle is a
binary cycle.  If that arc omits affine colour \(c\), the binary cycle
avoids \(M_c\).  The minimum-projection exchange inequality therefore
gives
\[
                    |\text{cycle arc}|\le |P|.            \tag{12}
\]

In row 1, the two \(v_2v_5\) arcs have colour words `012` and `301`;
each has length three and omits a colour.  Hence
\[
                           \operatorname{dist}_B(v_2,v_5)\ge3. \tag{13}
\]
In row 2, the short \(v_2v_4\) arc has word `02`, and in row 3 the short
\(v_3v_5\) arc has word `01`.  Each omits two colours, so
\[
 \operatorname{dist}_B(v_2,v_4)\ge2,\qquad
 \operatorname{dist}_B(v_3,v_5)\ge2.                     \tag{14}
\]
The complementary four-edge arcs in rows 2 and 3 use all four colours
and yield no colour-avoiding exchange inequality.

## 7. Elimination of the three survivors

The bundled `combined-line-span-theorem.md` contains a human proof of the
following universal fact for a fixed Fano line.  If its line subgraph has
at most two components, then it is already clean or one valid
line-preserving binary-cycle switch makes it clean.

For completeness, the final deduction is short.  The combined-line span
theorem puts the rainbow-defect vector \(r\) in the sum of the three
initial valid switch-image spaces.  Every switch image has even Hamming
weight on the line components.  With one component, the even-weight
space is zero, so \(r=0\).  With two components, the even-weight space is
one-dimensional.  If \(r\ne0\), at least one of the three image spaces is
nonzero and therefore contains the unique nonzero even vector \(r\).
One initially valid switch then kills the defect.  Its support avoids the
cancelling value class, so it creates no zero edge; because it is a single
switch, there is no mixed-switch quadratic correction.

Now let \(h\) be a minimum extendable projection of size six.  If a dirty
extension passes the componentwise-GL test, Section 4 constructs a
nowhere-zero \(\mathbb F_2^2\)-flow on \(G\), contrary to the non-Tait
hypothesis.  If it fails, Section 5 proves that its boundary data is one
of the three displayed rows.  Every row has exactly two components in
\(G-h\), so the two-component theorem cleans the fixed projection by one
valid switch.  Thus every size-six minimum is cleanable.  The size at
most five cases follow from the same minimum-support circuit argument
and the independently frozen size-five theorem; the Tait case uses the
zero projection.

The dependency is included verbatim from
`projects/five-cycle-double-cover/docs/fano-combined-line-span.md`, with
SHA-256
`c6c7ef87951f9df451c45bcb81f6280c605d90349dcc641af76fbff75e1fc060`.
Its Sections 1--3 give the full telescoping proof of the combined-line
span theorem, rather than treating the two-component corollary as a
black box.

## Scope and disclosure

The normal form assumes a fixed dirty extension of a globally
minimum-cardinality size-six projection in a connected loopless cubic
graph.  It neither constructs such a projection nor proves one
uncleanable.  Parallel edges are allowed by the argument; loops are not.

OpenAI Codex agents under human direction derived the boundary
enumeration, repair criterion, exchange bounds, checker, and report.
The script and complete proof of its semantics are included for
verification without trusting an AI system.  This has not received
independent human peer review, makes no literature-wide priority claim,
and does not resolve FiveCDC.
