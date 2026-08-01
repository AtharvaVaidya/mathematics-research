# Realization-sensitive Laplacian obstruction for the Jaeger plateau route

Date: 2026-07-28

Status: **HUMAN FINITE PROOF THAT THE NATURAL DEFECT-SUM
AVERAGING LAW DOES NOT EXIST.  THE FULL PLATEAU-COMPONENT THEOREM
REMAINS OPEN.  THIS IS NOT A FIVE-CYCLE DOUBLE COVER COUNTEREXAMPLE.**

## 1. The proposed averaging step

Let \(\mathcal X\) be a reciprocal-exchange graph of Jaeger star states,
and let
\[
             d(s)=(d_1(s),\ldots,d_7(s)),\qquad
             D(s)=\sum_{h=1}^7 d_h(s).
\]
For a function \(f\) on states, use the unnormalised graph Laplacian
\[
             (\Delta f)(s)=\sum_{t\sim s}(f(t)-f(s)).        \tag{1}
\]

The exact all-seven exchange law writes a fixed-plane update as
\[
 \beta_h'=\beta_h+\partial_hR,\qquad
 d_h'-d_h=|\partial_hR|-2|\partial_hR\cap\beta_h|.           \tag{2}
\]
A tempting next step is to sum (2) over all incident legal exchanges
and hope that the result has a sign, or at least is determined by the
current seven-defect profile.  The literal pair below disproves that
possibility for the most natural symmetric potential \(D\).

## 2. Two adjacent states with the same profile

Use the order-40 graph, root, spoke order, and internal-edge order from
`jaeger-plateau-radius-three-no-go-order40.md`.  The two omitted-mask
triples are

```text
s = (95184251351218348,
     47576007214007363,
      1354929510630160)

t = (95183701612181676,
     47576556953044035,
      1354929510630160).
```

They are adjacent: the exchange swaps graph edges \(27=(20,21)\) and
\(42=(28,29)\) between coordinates zero and one.  Both states have the
same ordered seven-plane profile
\[
                       (8,2,8,8,6,10,10).                  \tag{3}
\]

Complete enumeration gives 65 legal exchange neighbours of \(s\) and
63 of \(t\).  In functional order \(1,\ldots,7\), their coordinate
Laplacians are
\[
\begin{aligned}
 \Delta d(s)&=(-12,140,-6,-6,28,-40,-94),\\
 \Delta d(t)&=(-16,134,-6,-2,34,-58,-100).                 \tag{4}
\end{aligned}
\]
Consequently
\[
                         \Delta D(s)=10,\qquad
                         \Delta D(t)=-14.                   \tag{5}
\]

> **Proposition 2.1 (profile-only Laplacian no-go).**
> There is no function \(F\) of the ordered current defect profile such
> that \(\Delta D(u)=F(d(u))\) for every Jaeger star state \(u\).
> In particular, \(D\) is neither universally subharmonic nor
> universally superharmonic on the reciprocal-exchange graph, even
> after the current ordered profile is fixed.

**Proof.**
Equation (3) gives \(d(s)=d(t)\), while (5) gives
\(\Delta D(s)\ne\Delta D(t)\), with opposite signs.  This contradicts
either a profile-only formula or either universal sign. \(\square\)

The point is not merely that two numerical averages differ.  Equation
(2) predicts exactly why: the profile remembers the sizes of the seven
bad-component sets, but it forgets how the legal fundamental-cycle
boundaries \(\partial_hR\) meet those sets.  Those incidences are
realisation data, and the two states have different realisation data
despite (3).

## 3. What summing over a full plateau actually gives

There is a universal identity, but it is only discrete divergence.
For any finite set \(P\) of states and every \(h\),
\[
 \sum_{s\in P}\Delta d_h(s)
   =\sum_{\substack{s\in P,\ t\notin P\\s\sim t}}
        (d_h(t)-d_h(s)).                                    \tag{6}
\]
Indeed, the two orientations of every internal edge of \(P\) cancel.
If \(P\) is a connected component of a \(d_{\min}=q\) level set, (6)
reduces the desired theorem to the sign of its external boundary.
It does not determine that sign.

Proposition 2.1 shows that substituting the seven current defect counts
into (6) cannot recover the missing sign.  A successful theorem must
retain additional information about fundamental cycles and their
quotient-boundary incidences, or use a different global argument such
as path straightening in the graphic-matroid fibre.

This does **not** refute the full plateau-component statement.  The
two displayed states belong to a level-two component that has a
descending boundary at plateau distance four.  It also says nothing
against FiveCDC itself.

## 4. Reproduction

Run

```sh
python3 scratch/verify_jaeger_plateau_profile_laplacian_no_go.py
```

The derived checker loads only the graph-theoretic primitives from the
standalone standard-library verifier
`verify_jaeger_plateau_escape_radius4_order40.py`.  It independently
reconstructs both complete reciprocal-exchange neighbourhoods, all odd
kernels and exact seven-plane profiles, the 65 and 63 legal degrees,
and every entry of (4).

For a human check, each state partitions the 57 internal edges into
three 19-edge omitted classes.  For each of the
\(3\cdot19^2=1083\) candidate swaps, complement the changed classes,
adjoin the assigned spokes, retain the swap exactly when both changed
sets are spanning trees, recover the unique all-vertices-odd subforest
of each tree by odd subtree sizes, and apply the component parity test.
Summing the resulting neighbour-profile differences gives (4).

## AI-use disclosure

OpenAI Codex agents, under human direction, isolated the equal-profile
adjacent pair, derived the divergence interpretation, wrote the checker,
and drafted this note.  The finite calculation is mechanically
reproducible and has not received independent human peer review.
