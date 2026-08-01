# The first-foreign-component splice lemma

Date: **2026-07-28**

Status: **HUMAN PROOF OF A LOCAL JOHNSON-LIFTING LEMMA; NOT A
RESOLUTION OF FIVECDC**.

## Definitions

Let a cubic graph carry a \(D_5\) state: every edge is labelled by a
two-subset of \(\{0,1,2,3,4\}\), and the xor of the three labels at
each vertex is zero.  For a coordinate pair \(P\), write

\[
Y_P=\{e:|\ell(e)\cap P|\equiv1\pmod2\}.
\]

Every \(Y_P\) is Eulerian.  In a cubic graph, each nonempty connected
component of \(Y_P\) is a circuit.

Two factor components are adjacent when they share an edge.  A
factor-component chain \(K_1,\ldots,K_d\) from root edge \(r\) to
root edge \(s\) has \(r\in K_1\), \(s\in K_d\), and
\(K_i\cap K_{i+1}\ne\varnothing\).

## The lemma

Let \(P,Q\) be coordinate pairs with \(|P\cap Q|=1\), and put

\[
R=\tau_Q(P)=P\mathbin\triangle Q,
\]

where \(\tau_Q\) is the transposition of the two coordinates in \(Q\).
Suppose:

1. \(K_1=C\) is a \(Y_P\)-component and \(K_2=D\) is a
   \(Y_Q\)-component in a shortest root chain
   \(K_1,\ldots,K_d\), \(d\ge2\);
2. \(H\ne D\) is a \(Y_Q\)-component containing \(r\), and
   \(r\in C\cap H\);
3. in at least one of the two directions around the circuit \(C\),
   starting from the \(C\cap H\) edge-component containing \(r\), the
   first edge of \(C\) belonging to a \(Y_Q\)-component other than
   \(H\) belongs to \(D\).

Switch coordinates \(Q\) on \(H\).  Then in the switched state there
is a \(Y_R\)-component \(C'\) containing \(r\) and sharing an edge
with \(D\).  Moreover

\[
                         C',D,K_3,\ldots,K_d
\]

is a valid root chain.  In particular the factor-chain distance does
not increase.

If \(Y_Q\) has exactly the two components \(H,D\), condition 3 is
automatic.

## Proof

For any edge, membership in \(Y_P\) is the mod-two dot product of its
label with the characteristic vector of \(P\).  Since
\(P\mathbin\triangle R=Q\), edgewise parity gives

\[
                              Y_R=Y_P\mathbin\triangle Y_Q.     \tag{1}
\]

The \(Q\)-switch changes membership in \(Y_R\) precisely on the
switched edge set \(H\), because \(|R\cap Q|=1\).  Therefore

\[
\begin{aligned}
Y_R'
  &=Y_R\mathbin\triangle H\\
  &=Y_P\mathbin\triangle Y_Q\mathbin\triangle H\\
  &=Y_P\mathbin\triangle (Y_Q\setminus H).                     \tag{2}
\end{aligned}
\]

The last equality uses that \(H\) is a whole component, hence an edge
subset, of \(Y_Q\).

Let \(A\) be the edge-component of \(C\cap H\) containing \(r\).
Equation (2) puts every edge of \(A\), including \(r\), in \(Y_R'\):
it belongs to \(Y_P\) and it has been removed from the second term.
Follow \(C\) from \(A\) in the direction supplied by condition 3.
Before the first \(C\cap D\) block, no edge on this portion of \(C\)
belongs to \(Y_Q\setminus H\).  Thus the whole portion belongs to
\(Y_R'\).  Notice the useful point: later intersections with \(H\)
do not interrupt the portion, because all of \(H\) was deleted from
the second term in (2).

Let \(B\) be the first maximal common edge-path of \(C\) and \(D\).
The circuits are distinct.  At either end of \(B\), cubicity forces
one incident continuation edge in \(C\setminus D\) and one in
\(D\setminus C\).  Both continuation edges lie in the symmetric
difference (2), while the common edges of \(B\) do not.  Hence the
\(Y_R'\)-circuit arriving along \(C\) is spliced onto
\(D\setminus C\).  Its component \(C'\) contains \(r\) and shares
edges with \(D\).

It remains to check the suffix.  A switch on a \(Y_Q\)-component
leaves \(Y_Q\), and therefore \(D\), unchanged.  Also \(H\) cannot
meet \(K_j\) for \(j\ge3\): otherwise

\[
                            H,K_j,K_{j+1},\ldots,K_d
\]

would be a shorter root chain.  Two edge-disjoint circuits in a cubic
graph are vertex-disjoint, since two two-edge incidences at one
cubic vertex must share an edge.  Thus toggling edges of \(H\) in any
other factor cannot alter the component \(K_j\).  Every suffix block
\(K_3,\ldots,K_d\) survives, including its root \(s\) and all
successive intersections.  Replacing \(C\) by \(C'\) proves the
displayed chain and the distance bound. \(\square\)

## What the lemma says about self-reentry

The relevant obstruction is not another \(H\cap C\) block.  Formula
(2) shows that the switched \(Y_R\)-circuit follows \(C\) through all
such \(H\)-returns.  It is diverted only by a **foreign**
\(Y_Q\)-component \(J\ne H\).

This exactly separates the small terminal witnesses:

* In graph `K??FEagT@WB_`, state
  `03 05 06 09 11 18 0a 12 18 14 11 05 14 12 06 09 0a 03`,
  the pair \(Q=04\) has only components \(H,D\).  Self-reentry occurs
  before the unique \(D\)-join in both directions, but switching \(H\)
  is neutral and gives \(d:2\to1\) through
  \(R=24=\tau_{04}(02)\).

* In graph `K??FEbGL@WB_`, state
  `03 05 06 05 06 03 06 03 05 03 06 05 05 06 03 05 03 06`,
  the pair \(Q=03\) again has only \(H,D\).  Switching \(H\) is
  neutral and gives \(d:2\to2\).  The new root \(R=13\)-component
  intersects \(D\) on edges \(7,16\), exactly as the lemma predicts.
  This shows that “immediate rescue” is too strong; nonincrease is the
  correct conclusion.

* In the distance-increase witness on `K??FEagT@WB_`, state
  `03 05 06 05 03 06 06 0a 0c 06 0a 0c 0c 0a 06 0c 06 0a`,
  \(P=02,Q=03\).  Besides root component
  \(H=\{0,1,3,4\}\) and target component
  \(D=\{10,11,15,17\}\), \(Y_Q\) has the third component
  \(J=\{7,8,12,13\}\).  On both directions around \(C\), \(J\) is
  encountered before \(D\).  The lemma deliberately makes no claim,
  and the neutral \(H\)-switch can raise \(d:2\to3\).

## Remaining proof target

The shortest-chain endpoint problem is now localized more sharply:
the unresolved case requires at least one foreign \(Q\)-component
between the root \(Q\)-component \(H\) and the target \(Q\)-component
\(D\) in **both** directions around \(K_1\).  A future lexicographic
measure should count or order these foreign blockers; counting
\(H\)-reentries is the wrong statistic.

This lemma is local progress toward a Johnson-lifting proof.  It is
not by itself a proof of FiveCDC.

## AI-use disclosure

OpenAI Codex agents, under human direction, discovered the exact
identity, found and checked the boundary cases, and drafted this
proof.  The argument is presented for direct human verification and
has not undergone independent peer review.
