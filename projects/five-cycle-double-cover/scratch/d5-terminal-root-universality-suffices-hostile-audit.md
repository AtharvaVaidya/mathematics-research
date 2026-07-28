# Hostile proof audit: terminal rooted universality implies FiveCDC

Date: **2026-07-28**

Audited file:
`scratch/d5-terminal-root-universality-suffices.md`

Verdict: **THE CONDITIONAL IMPLICATION IS SOUND, BUT THE IMPORTED
MINIMUM-COUNTEREXAMPLE PARAGRAPH IS NOT YET SELF-CONTAINED AND ONE
REFERENCE LOCATION IS WRONG.**

No counterexample was found to either local lemma.  The proof becomes
fully human-checkable after the fixed-five preservation in the standard
reductions is written out, the exact meaning of “snark” is removed from
the logical chain, and the cubic-generation citation is corrected.

This audit concerns the standard, unoriented five-even-subgraph double
cover.  Empty members may be appended, so “five” means “at most five.”

## 1. Dependency graph

The argument has the following logical shape:
\[
\begin{array}{c}
\text{minimum FiveCDC counterexample }G\\
\Downarrow\quad\text{fixed-five reductions}\\
G\text{ simple, cubic, cyclically 4-edge-connected, girth at least }10\\
\Downarrow\quad H=G\div e\\
H\text{ smaller, simple, 3-edge-connected, cubic}\\
\Downarrow\quad\text{minimality}\\
H\text{ has a }D_5\text{-flow}\\
\Downarrow\quad\text{root hypothesis for the new }r,s\\
H\text{ has an }(r,s)\text{-good }D_5\text{-flow}\\
\Downarrow\quad\text{two-root insertion}\\
G\text{ has a }D_5\text{-flow, contradiction.}
\end{array}
\]
The two local downward arrows are valid.  The only imported arrow is
the first one.

## 2. Line-by-line findings

### Lines 10--27: \(D_5\), factors, and roots

**Sound.**  Applying the linear functional
\[
 x\longmapsto |x\cap\{i,j\}|\pmod2
\]
to the xor-zero equation proves that every \(Y_{ij}\) has even degree at
every vertex.  In a loopless cubic graph its degrees are zero or two, so
every nonempty connected component is a circuit.  Parallel edges cause
no problem: a two-edge circuit is allowed.

The later induction uses distinct roots.  If “every pair” in line 27
also includes \(r=s\), that extra case is harmless and unnecessary.

### Lines 33--42: conditional and terminal statements

**Sound, with a domain clarification.**  The theorem only invokes its
hypothesis on the loopless graph \(H\), so “connected bridgeless cubic”
should read “connected loopless bridgeless cubic” to match the definition
in line 14.

The terminal-plateau implication is valid because the state graph is
finite.  From a state, move within its equal-\(\Phi\) component if some
state there has an increasing exit, take such an exit, and repeat.
The integer \(\Phi\) strictly increases only finitely often.  The final
equal-level component is terminal.  Global \(S_5\) normalization does
not affect root-goodness.

### Lines 49--76: two-root insertion

**Sound without an omitted simplicity hypothesis.**  Here is the
complete local check.

Let \(\ell(e)\in D_5\) be active for \(ij\), meaning that it contains
exactly one of \(i,j\).  Transposing \(i,j\) sends
\[
                  \ell(e)\longmapsto\ell(e)+ij,
\]
and the new label still has weight two.  On an open \(u\)-to-\(v\) arc
of the subdivided factor circuit:

* every internal vertex sees either zero or two additions of \(ij\);
* each endpoint \(u,v\) sees exactly one addition of \(ij\);
* adding \(uv\) with label \(ij\in D_5\) cancels that endpoint defect.

All vertex xors are therefore zero.  This remains correct if \(r,s\)
are adjacent or are the two edges of a parallel-edge circuit.  The only
necessary assumptions are precisely the stated ones: the graph is
loopless, \(r\ne s\), and one factor component contains them both.

The argument constructs a standard \(D_5\)-flow only.  It makes no
orientability claim.

### Lines 83--110: existence and simplicity of \(H=G\div e\)

**Sound, but the source pointer is inaccurate.**  If \(G\) is simple
and has girth at least five, then:

1. \(u_1,u_2\) are distinct, as are \(v_1,v_2\);
2. no \(u_i\) equals a \(v_j\), since that would give a triangle through
   \(e\);
3. \(u_1u_2\) is not already an edge, since that would give a triangle
   through \(u\), and similarly at \(v\);
4. the two new edges cannot be equal or parallel.

Thus \(H\) is in fact **simple**, not merely loopless.

The cited paper by Brinkmann, Goedgebeur, and McKay does state the exact
edge-reduction criterion:

> \(e\) is irreducible iff it is a bridge, has an endpoint in a triangle
> not containing \(e\), or has both endpoints in a 4-gon not containing
> \(e\).

However, this sentence occurs immediately **before** Lemma 2.1 in that
paper.  Their Lemma 2.1 is instead the characterization of prime cubic
graphs by bridges and copies of \(K_4-e\).  Lines 171--174 of the audited
note should not attribute the criterion itself to “Lemma 2.1.”

Connectedness can also be proved without importing the criterion.  In a
component of \(H\), the new edge \(r\) keeps \(u_1,u_2\) together and
\(s\) keeps \(v_1,v_2\) together.  If those two pairs were in different
components, \(e\) would be a bridge of \(G\).  A component containing
neither pair would already be disconnected in \(G\).

### Lines 112--128: bridgelessness of \(H\)

**Sound.**  The three cases exhaust all possible bridges.

* If the bridge is \(r\), then \(u_1,u_2\) lie on opposite shores and
  \(v_1,v_2\) lie on one shore.  In \(G\), whichever edge \(uu_i\)
  enters the opposite shore is a bridge.
* The case \(s\) is symmetric.
* If the bridge \(b\) is old, neither new edge crosses its bridge cut.
  Each neighbour pair is therefore contained in one shore.  If the two
  pairs occupy the same shore, \(b\) remains a bridge of \(G\).  If they
  occupy opposite shores, \(\{b,e\}\) is a 2-edge-cut of \(G\).

Both conclusions contradict 3-edge-connectivity.

There is a useful stronger conclusion.  Pasting fixed-five covers across
a nontrivial 3-edge-cut makes the minimum counterexample cyclically
4-edge-connected.  A 2-edge-cut of \(H\) then restores either to a
2-edge-cut of \(G\), or to a cyclic 3-edge-cut when the two root pairs
lie on opposite shores.  Hence the resulting \(H\) is in fact
**3-edge-connected**.

### Lines 132--145: minimum-counterexample step

**Mathematically sound, manuscript gap.**  Huck's published abstract
explicitly states that a smallest counterexample to the 5-CDC conjecture
has girth at least ten.  Melody Chan's survey states the same result.
What the current note does not prove or cite precisely is its preceding
claim that all standard reductions preserve the fixed bound of five.

That fixed-five preservation is true and short:

1. **Components.**  Pad each component cover to five members and union
   members with the same index.
2. **Loops.**  Delete a loop, find a five-cover of the smaller graph,
   and add the loop to any two members.  A loop contributes even degree.
3. **Splitting a high-degree vertex.**  Fleischner's splitting lemma
   supplies incident edges \(va,vb\) whose split-off graph remains
   bridgeless.  If the artificial edge \(ab\) has label \(p\in D_5\),
   replace it by \(av,vb\), both labelled \(p\).  The xor at \(a,b\) is
   unchanged and the two copies cancel at \(v\).  Thus a five-cover
   lifts without adding a member.
4. **Suppressing degree two.**  Replace a degree-two path \(a-v-b\) by
   the edge \(ab\).  A label on \(ab\) lifts to the same label on both
   edges of the path; the two copies cancel at \(v\).  Since a connected
   loopless bridgeless graph has no degree-one vertex, this completes the
   passage from maximum degree three to cubic.
5. **A 2-edge-cut.**  Close each shore by an artificial edge.  The
   artificial edge has a two-coordinate label in each shore's
   \(D_5\)-flow.  A global \(S_5\) permutation makes the two labels
   equal, after which deleting the artificial edges and restoring the
   cut edges pastes the flows.
6. **A nontrivial 3-edge-cut, if cyclic connectivity is desired.**  At
   the contracted cubic vertex, the three weight-two labels with xor
   zero are the three edges of a triangle on three coordinates.  Every
   bijection between two such ordered boundary triangles is induced by
   a coordinate permutation.  The two five-covers therefore paste.
7. **A 3-edge-colourable cubic graph.**  The unions of each two of its
   three perfect-matching colour classes form a three-member double
   cover; append two empty members.

These observations justify taking a smallest counterexample to be
simple, cubic, cyclically 4-edge-connected, and
non-3-edge-colourable.  Huck then supplies girth at least ten.  The word
“snark” should not carry any
logical load because its connectivity and girth conventions vary in the
literature.  Replace “a simple cubic snark, hence 3-edge-connected” by
the exact list of properties.

With those properties established, lines 138--145 are valid:
\(H\) has two fewer vertices, is bridgeless and cubic, so minimality gives
a \(D_5\)-flow; the root hypothesis and Lemma 2.1 reconstruct a flow on
\(G\).

### Lines 147--152: flow-to-cover conversion

**Sound.**  Coordinate projection of the xor equation makes each
\(C_i\) Eulerian, while the weight-two edge label places every edge in
exactly two coordinate sets.  This is precisely an ordered list of at
most five even edge-subsets.

### Lines 169--184: references

**One correction and one addition needed.**

* Correct the location of the edge-reduction criterion as explained
  above.  The stable DOI for the paper is `10.46298/dmtcs.551`.
* Add an exact source for the fixed-five minimum-counterexample
  reduction, or include the six reconstruction bullets above.

Huck's DOI and claimed 5-CDC girth-ten scope are correct:
`10.1016/S0166-218X(99)00126-2`.

## 3. A strictly weaker sufficient hypothesis

The proof does not use Kempe connectivity, does not use every orbit, and
does not even use a preselected flow on \(H\).  It needs only one good
flow for the particular new edges.  This gives the following stronger
conditional theorem (stronger conclusion-to-hypothesis ratio).

> **Independent-pair feasibility theorem.**  Suppose that every simple
> 3-edge-connected cubic graph \(H\), with independent roots \(r,s\),
> girth at least eight, every 8-circuit through both roots, and every
> 9-circuit through at least one root, has the following property: if it
> admits a \(D_5\)-flow, then it admits some \(D_5\)-flow \(q\) (in any
> Kempe orbit) for which one factor component contains both \(r,s\).
> Then every finite bridgeless graph has a standard 5-CDC.

### Proof

Take the minimum counterexample \(G\) above and eliminate any edge
\(e=uv\).  Girth at least five makes the two new edges \(r,s\)
vertex-disjoint, and the strengthened Lemma 3.1 makes \(H\) simple,
cubic, and 3-edge-connected.  Minimality gives a
\(D_5\)-flow on \(H\).

It remains to check the girth.  A circuit of \(H\) using neither new edge
is a circuit of \(G\).  A circuit using one new edge lifts to a circuit
of \(G\) one edge longer.  A circuit using both lifts to a circuit of
\(G\) two edges longer.  Since \(g(G)\ge10\), this proves
\[
                            g(H)\ge8.
\]
It also proves that every 8-circuit uses both roots and every 9-circuit
uses at least one root.
The assumed feasibility supplies a good flow for \(r,s\), and two-root
insertion contradicts the choice of \(G\). \(\square\)

This premise is strictly weaker than “every Kempe orbit is
root-universal”: it allows the good flow to lie in a different orbit and
asks only about independent roots in a structurally restricted graph
class.

An even narrower, but less natural, premise would ask only about pairs
whose inverse insertion is simple, 3-edge-connected, and of girth at
least ten.

## 4. What the order-16 computation does and does not strengthen

The frozen
`scratch/d5-root-component-distance-order16-summary.json` and
`scratch/verify_d5_root_component_distance_order16_summary.py` report:

* all \(3\,874\) biconnected simple cubic graphs of order 16;
* \(15\,187\,695\) normalized \(D_5\)-flows;
* \(223\,926\,065\) initially root-bad state/root pairs;
* zero unrescued pairs using only switches on a factor component
  containing exactly one root;
* maximum such switch distance five.

The verifier was rerun during this audit and printed:

```text
PASS: 3,874 order-16 graphs, 15,187,695 normalized flows,
223,926,065 initially bad pairs, maximum distance five;
607 cyclically-4 graphs match the frozen true-girth stratification
```

Thus the computation supports a statement much stronger than
independent-pair feasibility at order 16: every starting state is
rescued, and remote component switches are unnecessary.

Accepting the complete order-8 through order-16 audits as finite lemmas
(with the order-four and order-six 3-edge-colourable cases checked
directly), one may replace the premise above by:

> every simple 3-edge-connected cubic \(D_5\)-graph of order at least
> 18 with the root-specific short-cycle geometry is independent-pair
> feasible.

This is a legitimate machine-assisted strengthening of the conditional
reduction.  It is not a new universal theorem.

There is an important limitation: the order-16 census contains no graph
of girth eight.  Indeed, the verified girth stratification of its 607
cyclically 4-edge-connected graphs has girths only four, five, and six.
Consequently the order-16 result does **not** directly test the
girth-eight reduction graphs arising from a hypothetical girth-ten
minimum counterexample.  It supports the general reconfiguration
mechanism, not the actual high-girth induction frontier.

## 5. Recommended edits to the audited note

1. Replace the broad sentence at lines 132--136 by an explicit
   fixed-five reduction proposition or cite one at theorem-level
   precision.
2. State the exact properties of \(G\) instead of inferring them from
   the convention-dependent word “snark.”
3. Strengthen Lemma 3.1's conclusion from loopless to simple and
   3-edge-connected, and record the root-specific 8/9-cycle geometry.
4. State the independent-pair feasibility theorem as the logically
   weakest clean remaining hypothesis.
5. Correct the Brinkmann--Goedgebeur--McKay reference location.
6. Keep the order-16 evidence separate from the human implication and
   disclose that it does not reach the high-girth subclass.

## AI-use disclosure

An OpenAI Codex agent, under human direction, performed this adversarial
audit, reconstructed the fixed-five reductions, reran the frozen
order-16 verifier, derived the weaker sufficient hypothesis, and drafted
this note.  The result is a conditional proof audit, not a proof of
FiveCDC and not independent peer review.
