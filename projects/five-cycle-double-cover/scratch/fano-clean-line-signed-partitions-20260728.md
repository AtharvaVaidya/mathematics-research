# Clean Fano lines have an exact signed-partition cut algebra

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE COMPOSITION THEOREM / NOT A FIVECDC
RESOLUTION**.

## 1. Setup

Let \(G\) be a finite loopless graph with a nowhere-zero
\(\mathbb F_2^3\)-flow \(f\).  Fix a nonzero functional \(\mu\), put

\[
L=\ker\mu-\{0\},
\]

and choose one affine value \(b\) with \(\mu(b)=1\).  Let

\[
K=G[\{e:f(e)\in L\}].
\]

The Hušek--Šámal criterion says that this Fano line is good precisely when
every component \(W\) of \(K\) has

\[
             |\delta_G(W)\cap f^{-1}(b)|\equiv0\pmod2.       \tag{1}
\]

Flow conservation makes the parity in (1) the same for all four affine
values, so the choice of \(b\) is immaterial.

Split \(G\) along an ordered edge cut
\(B=(e_1,\ldots,e_k)\) into shores \(X\) and \(\bar X\).  Parallel cut-edge
objects would remain distinct; the statement below uses edge identities,
not endpoint pairs.

## 2. The shore state

On the \(X\)-shore retain the proper line-valued edges.  Their spanning
subgraph partitions \(X\) into components.  Let

\[
I=\{i:f(e_i)\in L\}.
\]

The line-valued boundary incidences in \(I\) are partitioned by their
shore components; call this partition \(\pi_X\).  Label each block \(A\)
of \(\pi_X\) by

\[
d_X(A)=
 |\delta_G(W_A)\cap f^{-1}(b)|\pmod2,                       \tag{2}
\]

where \(W_A\) is its shore component.  The cut edges in (2) are counted as
ordinary global edges.  Thus an affine \(b\)-valued cut edge contributes
once on each shore, exactly as it does to the two global line components
at its ends.

A shore component meeting no line-valued boundary edge can never merge
with a component on the opposite shore.  Call the shore state
**admissible** when every such closed component has defect zero.
The remaining datum

\[
                         (\pi_X,d_X)                        \tag{3}
\]

is a signed partition of the line-valued terminal set \(I\).

## 3. Exact gluing theorem

Given the two shore states, form a bipartite multigraph \(H_B\).  Its
left vertices are the blocks of \(\pi_X\), its right vertices are the
blocks of \(\pi_{\bar X}\), and every \(i\in I\) supplies one edge between
the two blocks containing \(i\).

> **Signed-partition gluing theorem.**  The fixed line \(L\) is good in
> \(G\) if and only if both shore states are admissible and, in every
> connected component \(Q\) of \(H_B\),
> \[
>       \bigoplus_{A\in V(Q)}d(A)=0.                        \tag{4}
> \]

**Proof.**  A line-valued cut edge joins exactly the two shore components
represented by its endpoints in \(H_B\).  Consequently the global
components of \(K\) that meet the cut are in bijection with the connected
components of \(H_B\).  The remaining global components are exactly the
closed shore components.

Within a joined component, every proper \(b\)-edge contribution is present
in its own shore defect.  Every \(b\)-valued cut edge is affine, so it does
not join line components; it contributes once to the defect of the shore
component at each endpoint.  Hence the defect of a joined global component
is precisely the xor in (4).  The closed components are clean precisely
when both shore states are admissible.  This proves both directions.
\(\square\)

No connectivity, girth, simplicity, or cubicity assumption enters this
composition proof.  Cubicity is needed only when invoking the standard
FiveCDC/Fano-line equivalence.

## 4. Boundary conservation and the small-cut tables

Sum (2) over all shore components.  Every proper \(b\)-valued edge is
counted twice, while every \(b\)-valued boundary edge is counted once.
For an admissible state,

\[
 \bigoplus_{A\in\pi_X}d_X(A)
   =|\{i:f(e_i)=b\}|\pmod2.                               \tag{5}
\]

If \(m=|I|\ge1\), a partition with \(r\) blocks therefore has
\(2^{r-1}\) possible signings.  Summing over the Stirling numbers gives

\[
\begin{array}{c|ccccc}
m&0&1&2&3&4\\ \hline
\text{signed states}&1&1&3&11&47 .
\end{array}                                               \tag{6}
\]

At \(m=0\), the unique empty state exists only when the forced parity in
(5) is zero.  Applying \(\mu\) to the boundary conservation equation shows
\(m\equiv k\pmod2\).  Thus the possible state counts are:

\[
\begin{array}{c|c}
k&\text{possible line-terminal state counts}\\ \hline
2&1,\ 3\\
3&1,\ 11\\
4&1,\ 3,\ 47.
\end{array}                                               \tag{7}
\]

For the same forced parity on both shores, direct evaluation of (4) gives
the following numbers of compatible **ordered** state pairs:

\[
\begin{array}{c|ccccc}
m&0&1&2&3&4\\ \hline
\text{compatible pairs}&1&1&7&79&1283.
\end{array}                                               \tag{8}
\]

The five integers follow by finite evaluation of (4).  The checker
reconstructs them rather than trusting the displayed row.

## 5. What this closes, and what remains

The theorem supplies the exact composition law requested by the
flow-selection formulation.  It confirms:

- affine boundary edges carry parity but never merge line components;
- line boundary edges merge components but carry no \(b\)-defect;
- ordinary boundary words are insufficient, because the connectivity
  partition \(\pi\) is essential; and
- the cyclic four-cut branch already has 47 possible signed connectivity
  states when all four boundary values lie in the line.

Therefore a boundary argument that remembers only the four Fano values, or
only the number of dirty components, cannot be complete.  This is the same
kind of missing internal-topology datum encountered in the existing
four-pole signature frontier, now stated exactly in the Hušek--Šámal
language.

The theorem does **not** prove that the two shores of a cut admit compatible
states after changing the flow.  That selection problem remains the
conjecture-level obligation.  In particular, (7) does not eliminate the
published exceptional four-pole signatures.

## 6. Clean cap flows do not automatically glue

The need to match signed partitions is real already at a two-edge cut.
Let \(Q=K_4-01\), with the \(K_4\) edges ordered as

\[
        01,02,03,12,13,23.
\]

The two literal flows

\[
\begin{aligned}
 f_0&=(2,5,7,7,5,2),\\
 f_1&=(2,1,3,3,1,2)
\end{aligned}                                             \tag{9}
\]

both satisfy the xor equation at every vertex of \(K_4\).  Fix
\(\mu(x)\) to be the low bit of \(x\), take \(b=1\), and designate edge
\(01\), of line value \(2\), as the cap.

The selected line is clean in both capped \(K_4\)'s.  After deleting the
cap, the two boundary vertices are distinct line components.  Their signed
states are respectively

\[
             (0,0)\qquad\text{and}\qquad(1,1).            \tag{10}
\]

Join corresponding cap ends by two new edges, both of value \(2\).  This
gives the simple cubic graph on vertices \(0,\ldots,7\) with edges

\[
\begin{split}
&02,03,12,13,23,\\
&46,47,56,57,67,\\
&04,15 .
\end{split}                                               \tag{11}
\]

The two new line edges pair a zero-defect component with a one-defect
component twice.  Hence the two resulting global components are both
dirty, exactly as (4) predicts.  Thus:

> Two capped shores may each carry a clean selected Fano line while their
> boundary-matched gluing carries a dirty selected line.

This is a no-go only for cap-by-cap fixed-flow induction.  The graph (11)
is bridgeless and Tait-colourable; the checker gives an explicit
three-colouring, hence a standard FiveCDC.  A valid low-cut reduction may
change the shore flows and must align their full signed states.

## 7. Independent replay

Run

```bash
python3 scratch/verify_fano_clean_line_signed_partitions.py
```

The checker uses no third-party package or SAT solver.  It:

1. generates every partition and every parity-compatible signing for
   \(m\le4\);
2. reconstructs the literal bipartite component graph and the compatibility
   counts in (8);
3. independently enumerates every covering three-dimensional binary cycle
   subspace of the Petersen graph; and
4. for every nonzero functional and every Petersen cut of size at most
   four, compares signed-partition gluing with a fresh computation of all
   global line-component defects; then
5. imports the separately written unbounded-component construction and
   checks all 546 flow/functional comparisons on its two-edge diamond
   interfaces through order 322; and
6. verifies both cap flows, the glued graph, its dirty line, bridgelessness,
   and an explicit Tait/FiveCDC witness in (9)--(11).

This is a semantic audit of the theorem, not a solver certificate and not a
counterexample search.

## AI-use disclosure

OpenAI Codex, directed by Atharva Vaidya, derived the signed-partition state
and composition law, wrote the independent replay, and drafted this note.
The Hušek--Šámal Fano-line criterion is cited prior work.  The proof above is
included for line-by-line human checking; AI assistance is not independent
human peer review.
