# Minimum extendable projections through size seven are cleanable

Date: 2026-07-29

Status: **HUMAN-CHECKABLE THEOREM WITH EXHAUSTIVE FINITE BOUNDARY
CLASSIFICATION / NOT A FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## Theorem

Let \(G\) be a finite connected bridgeless loopless cubic graph.  Parallel
edges are allowed.  A binary cycle \(h\) is **extendable** if binary
cycles \(p,q\) exist with
\[
                         E(G)-h\subseteq p\cup q.          \tag{1}
\]
It is **cleanable** if such \(p,q\) can be chosen so that, for every
component \(W\) of \(G-h\),
\[
                   |p\cap q\cap\delta(W)|\equiv0\pmod2.   \tag{2}
\]

> If a cardinality-minimum extendable projection has size at most seven,
> then \(G\) has a clean cardinality-minimum projection.  More precisely,
> on a non-Tait graph every cardinality-minimum extendable projection of
> size at most seven is cleanable; on a Tait graph the zero projection is
> a clean minimum.

This verifies the proposed minimum-projection route only through support
size seven.  It gives no universal bound on the minimum support and does
not resolve FiveCDC.

## 1. Common structural reduction

Fix a non-Tait graph, a cardinality-minimum nonzero extendable \(h\), and
a nowhere-zero extension
\[
                f=(h,s):E(G)\to\mathbb F_2\times\mathbb F_2^2. \tag{3}
\]
For \(c\in\mathbb F_2^2\), put
\[
                         M_c=\{e\in h:s(e)=c\}.            \tag{4}
\]
The minimum-projection exchange theorem makes \(h\) a minimum binary
cycle containing each \(M_c\).  Hence every circuit component of \(h\)
meets all four \(M_c\), and has at least four edges.

For \(|h|\le7\), \(h\) is therefore one ordinary circuit.  Index it as
\[
 v_0,e_0,v_1,e_1,\ldots,v_{n-1},e_{n-1},v_0,\qquad
 e_i=v_iv_{i+1},                                        \tag{5}
\]
with indices modulo \(n=|h|\).  Put \(c_i=s(e_i)\).  Adjacent colours
are distinct, and all four colours occur.

Let \(k_i\) be the unique edge of \(G-h\) at \(v_i\).  Its low value is
\[
                         d_i=s(k_i)=c_{i-1}+c_i\ne0.       \tag{6}
\]
The components of \(G-h\) give a set partition
\(\pi=(\pi_0,\ldots,\pi_{n-1})\) of the circuit vertices.  For each
component, conservation is equivalent to:

- the four parities \(|M_c\cap\delta(W)|\) are equal; and
- \(\sum_{\pi_i=W}d_i=0\).

A component is dirty when those four parities are all one.

## 2. Exact componentwise-linear repair

On each component \(W\) of \(G-h\), apply one independently chosen
\(L_W\in\mathrm{GL}(2,2)\) to every low edge value.  This preserves all
internal equations and nonzeroness.  The new pendant value at \(v_i\)
is
\[
                          g_i=L_{\pi_i}d_i.               \tag{7}
\]
The transformed component values extend to a nowhere-zero
\(\mathbb F_2^2\)-flow on all of \(G\) exactly when nonzero circuit-edge
values \(r_i\) exist with
\[
                          r_{i-1}+r_i=g_i                 \tag{8}
\]
cyclically.

Necessity is the flow equation at \(v_i\).  Conversely, (8) supplies
precisely the missing equations; the \(L_W\)'s preserve the internal
ones.  Thus this is a necessary-and-sufficient test for the modeled
componentwise-\(\mathrm{GL}(2,2)\) repair of the fixed low-flow state.
There are six choices for each \(L_W\) and three choices for a starting
\(r_{n-1}\); the remaining \(r_i\)'s are forced.

If the test succeeds, \(G\) has a nowhere-zero
\(\mathbb F_2^2\)-flow, equivalently a Tait colouring.  It therefore
cannot succeed on the fixed state of a non-Tait graph.

Failure is only failure of this repair class.  A component may have
other low-flow orbits; the test is not an arbitrary Tait-colouring
oracle.

## 3. The two-component cleaning theorem

The bundled `combined-line-span-theorem.md` proves universally that if
the line subgraph \(G-h\) has at most two components, then the fixed
projection is already clean or one valid line-preserving binary-cycle
switch makes it clean.

Here is the final linear deduction.  The combined-line span theorem puts
the rainbow-defect vector \(r\) in the sum of the three initially valid
switch-image spaces.  Every switch image has even weight on the line
components.  For one component this even subspace is zero.  For two
components it is one-dimensional, so if \(r\ne0\), one image space
contains its unique nonzero vector.  One valid switch kills the defect.
Its cycle avoids the cancelling value class, so it creates no zero edge,
and a single switch has no mixed-switch quadratic correction.

The bundled source includes the complete telescoping proof of the
combined-line span theorem, not just this corollary.

## 4. Exact size-six and size-seven classifications

The dependency-free `verify.py` exhausts:

1. every proper cyclic word of length \(n\) on the four affine colours,
   using all four;
2. every set partition of its \(n\) vertices;
3. the conservation and dirty-component conditions above;
4. all six componentwise linear maps on every component; and
5. all three nonzero starting circuit values in (8).

For size six:
\[
\begin{array}{c|c}
\text{valid dirty word/partition pairs}&2712\\
\text{failed componentwise-GL repairs}&432
\end{array}
\]
Every failed repair has exactly two components.  Under the dihedral
action on the six-cycle, the affine action
\(\mathrm{AGL}(2,2)\cong S_4\) on the four colours, and component
relabeling, the failures form three orbits:
\[
\begin{array}{c|c}
010123&001001\\
010232&001010\\
012013&000101
\end{array}                                               \tag{9}
\]
Each orbit has raw size 144.  The separately bundled
`minimum-size6-normal-forms-and-proof.md` gives their metric consequences
and a line-by-line proof of the symmetry and recurrence semantics.

For size seven:
\[
\begin{array}{c|c}
\text{valid dirty word/partition pairs}&26880\\
\text{failed componentwise-GL repairs}&5376\\
\text{failed repairs with three or more components}&0.
\end{array}                                               \tag{10}
\]
Thus there are no residual size-seven boundary normal forms after the
two-component theorem.

These are exhaustive finite classifications of boundary words and set
partitions, not graph sampling.

## 5. Conclusion

Let \(h\) be a minimum projection of size six or seven and fix any dirty
extension.  If its boundary state passes the componentwise-GL test, the
constructed Tait flow contradicts the non-Tait hypothesis.  If it fails,
(9)--(10) say that \(G-h\) has exactly two components, and Section 3
cleans the fixed projection by one valid switch.  Therefore \(h\) is
cleanable.

The size-at-most-five argument is included in
`minimum-through5-theorem.md`; together these prove the stated theorem
through size seven.

## Reproduction and disclosure

Run:

```sh
python3 verify.py
shasum -a 256 -c SHA256SUMS
```

The exhaustive replay takes a few seconds and uses only the Python
standard library.

OpenAI Codex agents under human direction derived the exchange reduction,
finite boundary classifiers, repair recurrence, metric consequences, and
draft.  The full proofs and executable enumeration are included so the
result can be checked without trusting an AI-generated summary.  This has
not received independent human peer review, makes no literature-wide
priority claim, and does not resolve FiveCDC.
