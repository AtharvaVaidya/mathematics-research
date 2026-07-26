# Clean-room audit of the monochromatic-mark girth bound

Date: **2026-07-26**.

Target:
`docs/kempe-transversality-and-eight-mark-girth.md`, Section 3, especially
\[
        |V(G)|\ge 2r\,g_{\rm odd}
\]
and its \(r=4\), girth-at-least-ten consequence \(|V(G)|\ge88\).

This audit reconstructs the argument from the definitions.  It does not
use the finite searches elsewhere in the project.

## 1. Verdict

| Item | Verdict | Reason |
|---|---|---|
| Conditional inequality \(|V(G)|\ge2r g_{\rm odd}\) | **PASS** | Once suppression gives one distinct matching mark for each endpoint of \(M\), universal separation and mark precolouring produce \(2r\) vertex-disjoint odd circuits in \(G\). |
| Application to the extremal exact-zero size-four branch | **PASS** | The earlier marked-core reduction proves the terminal distinctness, valid suppression, Tait colourability, and universal separation required here. |
| Numerical conclusion \(|V(G)|\ge88\) | **PASS** | There are eight lifted odd circuits, and ambient girth at least ten forces each odd circuit to have length at least eleven. |
| Opening formulation for an arbitrary “cubic graph” and matching | **FAIL AS A SELF-CONTAINED FORMULATION; SCOPE REPAIR REQUIRED** | A bare matching in a cubic graph does not ensure that simultaneous suppression produces cubic cores or \(2r\) distinct marked edges forming matchings.  The proof is correct under the explicit suppression hypotheses below, and those hypotheses hold in the intended extremal branch. |

Thus the theorem's substantive conclusion and the order-\(88\) application
pass.  The failure above is a hypothesis/formulation defect, not a
counterexample to the result in its intended minimum-counterexample
domain.

## 2. Precise version audited

The following formulation makes every operation in the proof
unambiguous.

> **Audited proposition.**  Let \(G\) be a finite loopless cubic
> multigraph, let \(M\) be an ordinary matching of \(r\) nonloop edges,
> and let \(T\) be the \(2r\) distinct endpoints of \(M\).  Put
> \(K=G-M\).  Assume that suppressing the vertices of \(T\) has the
> following properties:
>
> 1. it produces loopless cubic multigraph components \(H_j\);
> 2. every terminal \(t\in T\) corresponds to one distinguished edge
>    \(s_t\) in one core, and \(t\mapsto s_t\) is a bijection from \(T\)
>    to the union of marked sets \(S_j\);
> 3. each \(S_j\) is an edge matching;
> 4. every \(H_j\) is Tait-colourable; and
> 5. every \(S_j\) is universally separated in \(H_j\).
>
> Let \(g\) be the girth of \(G\), with loops counted as
> one-circuits and pairs of parallel edges counted as two-circuits, and
> let \(g_{\rm odd}\) be the least odd integer at least \(g\).  Then
> \(G\) contains \(2r\) pairwise vertex-disjoint odd circuits, each of
> length at least \(g_{\rm odd}\).  Consequently
> \[
>             |V(G)|\ge 2r\,g_{\rm odd}.
> \]

Simplicity of the cores is not needed for this proposition.  Properly
edge-coloured parallel edges cause no problem, provided the usual
multigraph convention regards two parallel edges as a circuit of length
two.  Tait colourability itself excludes core loops.

## 3. Clean-room proof

### 3.1 All marks can be given one colour

Fix colours \(a,b,c\).  In each core \(H_j\), start from any proper
three-edge-colouring.  If a marked edge \(s\) currently has colour
\(p\ne c\), interchange \(p\) and \(c\) on the unique
\(pc\)-bichromatic circuit containing \(s\).

Universal separation says that this circuit contains no other marked
edge.  The switch therefore changes the colour of \(s\) without changing
the colour of any other mark.  After the switch the colouring is still
proper, so universal separation remains available for the next mark.
Induction over \(S_j\) makes every mark colour \(c\).  This can be done
independently in every core; no matching edge of \(M\) receives a
nonzero colour.

### 3.2 There are \(2r\) disjoint marked core circuits

For a fixed \(j\), consider the two-colour subgraph
\[
             H_j[a,c].
\]
At every core vertex it has degree two.  Its connected components are
therefore pairwise vertex-disjoint circuits, and their colours alternate,
so every component has even length.

Every \(s\in S_j\) has colour \(c\), hence lies on exactly one such
component; call it \(Q_s\).  If \(Q_s=Q_{s'}\) for two different marks,
that bichromatic circuit would contain two marks, contrary to universal
separation.  Thus
\[
             s\longmapsto Q_s
\]
is injective.  The circuits \(Q_s\), over all marks and all core
components, are pairwise vertex-disjoint.  Their number is
\[
             \sum_j |S_j|=|T|=2r.
\]

Only one bichromatic factor is being counted.  The proof does not add
the analogous \(bc\)-circuits, which can intersect the \(ac\)-circuits
along \(c\)-edges.

### 3.3 Suppression lifts each circuit to an odd circuit

Let \(s_t=uv\) be the marked edge corresponding to terminal \(t\).
Undoing suppression replaces \(uv\) by the two-edge path
\[
             u-t-v.
\]
The core circuit \(Q_{s_t}\) contains exactly one marked edge, namely
\(s_t\).  Its lift \(L_t\) therefore has
\[
             |E(L_t)|=|E(Q_{s_t})|+1.
\]
Since \(Q_{s_t}\) has even length, \(L_t\) has odd length.  It is already
a circuit in \(K=G-M\), hence remains a circuit when the unused matching
edges \(M\) are restored.

Distinct core circuits share no core vertex, and the bijection
\(t\mapsto s_t\) assigns distinct terminals to them.  Consequently the
lifted circuits \(L_t\) remain pairwise vertex-disjoint in \(G\).
Extra edges of \(M\) incident with their terminals do not belong to the
circuits and do not create an intersection.

### 3.4 Girth and vertex counting

Every \(L_t\) is a circuit of \(G\), so \(|L_t|\ge g\).  Its length is
odd, hence in fact
\[
             |L_t|\ge g_{\rm odd}.
\]
Because the \(2r\) circuits are vertex-disjoint,
\[
       |V(G)|
       \ \ge\ \sum_{t\in T}|V(L_t)|
       \ =\ \sum_{t\in T}|E(L_t)|
       \ \ge\ 2r\,g_{\rm odd}.
\]
This proves the audited proposition.

## 4. Suppression, loops, and parallel edges

The sentence “its \(2r\) degree-two vertices are the endpoints of
\(M\)” is valid when \(G\) is loopless and \(M\) is an ordinary
matching.  It is not a safe convention if matching loops are allowed:
one loop has one incident vertex but contributes twice to its degree.
The theorem should therefore say “finite loopless cubic multigraph” (or
simply work with the simple ambient graph in the application).

More importantly, a matching alone does not make the suppressed marks a
matching:

- In \(K_4\), delete one edge \(uv\).  Suppressing \(u\) and \(v\)
  produces the cubic multigraph on the other two vertices with three
  parallel edges.  The two suppressed marks share both endpoints and
  are not a matching.
- In \(K_4\), delete a perfect matching.  The remaining graph is a
  four-cycle all of whose vertices are terminals.  Suppressing all four
  vertices does not produce an ordinary cubic core with four distinct
  marked edges.

These examples do not refute the conditional inequality: they fail its
suppression/matching hypotheses.  They show why those hypotheses cannot
be left implicit in a standalone statement.

In the intended extremal branch, the proof in
`docs/extremal-marked-core-reduction.md` establishes that no two
terminals are adjacent and no two have a common neighbour.  It then
proves that suppression produces connected simple cubic cores and that
the suppressed edges form matchings.  Ambient girth at least ten also
excludes original loops and parallel-edge two-circuits, suppression
loops, and suppression parallelisms of the forbidden short types.
Therefore none of the degeneracies above occurs in the application.

If parallel edges are allowed in an abstract core, the main proof still
works.  An alternating two-circuit is even; subdividing its unique mark
produces a three-circuit in \(G\), which is odd.  This observation relies
on the standard multigraph girth convention.  Under a convention that
ignores two-circuits, the stated girth inference would need to be
reformulated.

## 5. Audit of the order-\(88\) consequence

For the exact-zero size-four extremal branch, the earlier reduction
supplies:

1. \(r=4\), so there are \(2r=8\) terminals and eight marked edges in
   total;
2. either one core has eight marks or two cores have four marks each;
3. all cores are Tait-colourable and their marked matchings are
   universally separated; and
4. the ambient graph has girth at least ten.

The mark-precolouring argument is componentwise, so the \(4+4\) case is
no different from the eight-mark connected case.  Choose the same colour
name \(c\) after independently relabelling the colours in each core.
The audited proposition gives eight vertex-disjoint odd circuits.
An odd circuit in a graph of girth at least ten has length at least
eleven.  Hence
\[
             |V(G)|\ge 8\cdot11=88.
\]

Equivalently, before restoring the eight suppressed vertices, the chosen
marked core circuits have even length at least ten and use at least
\(8\cdot10=80\) core vertices in total.

This is a branch-specific lower bound.  It does **not** say that every
cubic graph of order below \(88\) has a five-cycle double cover, and it
does not close the surviving connected eight-mark obstruction.

## 6. Ledger consistency

The audit initially found stale order-\(68\) summaries and one overbroad
scope sentence.  The publication bundle now records the stronger
conditional bound consistently:

- `docs/current-status.md` states the
  size-four/order-at-least-\(88\) dichotomy and restricts the conclusion
  to a minimum counterexample in the exact-zero size-four extremal branch.
- `README.md` links this audit and states that the suppression hypotheses
  do not follow from an arbitrary matching.
- `docs/proof-obligation-ledger.md` and `docs/experiment-ledger.md`
  already recorded the order-\(88\) bound and its still-open scope
  correctly.

The earlier order-\(68\) theorem in
`docs/flow-resistance-weak-oddness.md` remains a valid but superseded
weaker lemma.

## 7. AI-use disclosure

This clean-room audit was written by an OpenAI Codex agent under human
direction.  The proof above is elementary and fully displayed so that a
human reader can check it without trusting the agent, a SAT solver, or
any computational census.
