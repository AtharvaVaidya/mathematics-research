# A capped-ladder root-component delay family

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE UNBOUNDED-RADIUS THEOREM / NOT A FIVECDC
RESOLUTION**.

## Recurring extension

The sharp order-14 and order-16 root-component witnesses are consecutive
members of a simple planar family.  Start with two terminal diamonds
\(K_4-e\).  Join their degree-two vertices by a ladder having
\(m+1\) rung edges and \(m\) square cells.  Call the resulting cubic graph
\(L_m\); it has
\[
                       |V(L_m)|=2m+10.
\]

Equivalently, one extension replaces two corresponding rail edges by the
five edges obtained after subdividing both and joining the two new
vertices.  It adds two vertices, one rung, and one square.  It preserves
simplicity, planarity, cubicity, and bridgelessness.

The graph \(L_2\) is isomorphic to the order-14 radius-four witness
`M?AAD@OgPWB_E_Og?`.  The graph \(L_3\) is isomorphic to the order-16
radius-five witness `O??CAA_SD@DOB_F?AgAA_`.

More explicitly, use left-cap vertices \(a,b,p,q\), ladder vertices
\(u_i,v_i\) for \(0\le i\le m\), and right-cap vertices \(c,d,r,s\).
The edges are

\[
\begin{split}
 &ap,aq,bp,bq,pq,\quad au_0,bv_0,\\
 &u_iv_i\quad(0\le i\le m),\\
 &u_iu_{i+1},v_iv_{i+1}\quad(0\le i<m),\\
 &u_mc,v_md,\quad cr,cs,dr,ds,rs.
\end{split}
\]

The missing cap edges are \(ab\) and \(cd\).  This definition makes the
extension and all graph properties directly checkable.

## Canonical Tait-supported state

Write
\[
                A=01,\qquad B=02,\qquad C=12.
\]
Color both rail edges entering the ladder by \(A\), its first rung by
\(B\), and then repeat
\[
             \text{rail-pair }C,\ \text{rung }A,
             \text{rail-pair }B,\ \text{rung }C,
             \text{rail-pair }A,\ \text{rung }B.
\]
The two terminal diamonds have their unique compatible Tait coloring.
Every vertex is incident with \(A,B,C\), so the local \(D_5\) xor equation
is immediate.

Exact literal BFS for selected cross-cap root pairs gives:

\[
\begin{array}{c|c|c|c}
m&|V(L_m)|&\text{selected root edges}&
\text{exact root-component distance}\\ \hline
1&12&(0,13)&3\\
2&14&(0,17)&4\\
3&16&(0,20)&5\\
4&18&(0,22)&6\\
5&20&(1,25)&8\\
6&22&(1,28)&9.
\end{array}
\]

For \(m=1,\ldots,5\), exhaustively testing all 16 pairs consisting of one
noncentral diamond edge in each cap gives maximum distances
\[
                            3,4,5,6,8.
\]

The exact distances are stronger than the general theorem below, but are
not needed to prove unboundedness.

## Unbounded-radius theorem

**Theorem.**  For every \(m\ge1\), choose one root edge inside each cap
of the displayed Tait-supported state.  Any sequence of root-component
switches that makes the roots share a factor component has length at
least

\[
                         \left\lfloor {m+2\over3}\right\rfloor.
\]

Consequently there is no universal constant bound on the number of
root-component switches needed for rescue.

### Proof

For \(0\le j\le m+1\), let \(D_j\) be the two-edge cut between consecutive
pieces of the capped ladder.  In order from left to right these are the
left attachments, the \(m\) rail pairs, and the right attachments.

For any \(D_5\)-flow, the two edges in \(D_j\) have the same label.
Indeed, xor all vertex equations on one side of the cut.  Every internal
edge occurs twice and cancels, leaving the xor of the two cut labels,
which must be zero.  We may therefore represent the state by its
cut-label word

\[
                         \lambda_0\lambda_1\cdots\lambda_{m+1}.
\]

In the initial Tait state this word is the length-\((m+2)\) prefix of

\[
                         A,C,B,A,C,B,\ldots,
\]
and \(A\mathbin\oplus C\mathbin\oplus B=0\).

Consider one factor component \(K\) containing exactly one root.  Since
\(K\) is connected and the cuts \(D_j\) are nested, the cuts met by \(K\)
form a prefix if \(K\) contains the left root, and a suffix if it contains
the right root.  Since \(K\) is Eulerian, it meets every two-edge cut in
an even number of edges; hence it contains either zero or both edges of
each \(D_j\).

A switch with coordinate pair \(k\) applies the coordinate transposition
\(\tau_k\) to the labels on \(K\).  On the cut-label word, one
root-component switch therefore applies one coordinate transposition to
a prefix or a suffix.

After \(t\) switches, their at most \(t\) prefix/suffix boundaries
partition the original word into at most \(t+1\) intervals.  On each
interval the final labels are obtained from the initial labels by one
fixed coordinate permutation: it is the ordered composition of exactly
the switches covering that interval.

Now suppose the final state is root-good through a factor \(Y_h\).
The component of \(Y_h\) containing both roots crosses every \(D_j\).
Thus

\[
                              h\cdot\lambda_j=1
                   \qquad(0\le j\le m+1),
\]

where the dot product is over \(\mathbb F_2\).

Partition the initial word into
\(\lfloor(m+2)/3\rfloor\) disjoint consecutive triples
\((A,C,B)\).  No such triple can remain wholly inside one interval of the
switch-boundary partition.  If it did, one coordinate permutation
\(\pi\) would be applied to all three labels, so

\[
              \pi(A)\mathbin\oplus\pi(C)\mathbin\oplus\pi(B)=0.
\]

Taking dot product with \(h\) would say that the xor of three ones is
zero, a contradiction.

Every disjoint triple must therefore contain a switch boundary in one of
its two internal gaps.  The triples have disjoint internal gaps, so one
boundary can split at most one triple.  Hence

\[
                              t\ge
                    \left\lfloor {m+2\over3}\right\rfloor.
\]

This proves the theorem. \(\square\)

The argument deliberately relaxes the actual move system: it uses only
the necessary prefix/suffix action and ignores further constraints on
which transpositions are legal.  Its lower bound is therefore independent
of the BFS computations.

### Corollary: the \(H=0\) endpoint itself has unbounded delay

For \(m\ge2\), take the left root edge \(0\) and a \(02\)-labeled edge
in the right cap.  From the Tait state, switch \(03\) on
\[
 P=\{0,3,4,5,6,7\}
\]
and then \(24\) on
\[
 Q=\{0,1,2,3\}.
\]
The roots are now labeled \(34,02\).  The all-bad line triangle
\[
                         (13,34,14)
\]
has \(K_1=K_3=Q\), \(K_2=P\), hence
\[
                         H=0,\qquad
                         Z=\{1,2,4,5,6,7\}.
\]
Its two endpoint cut words are
\[
            13,C,B,A,C,B,\ldots\quad\text{and}\quad
            14,C,B,A,C,B,\ldots.
\]
Applying the same boundary proof to the unchanged tail gives a
root-transition lower bound
\[
                         \left\lfloor{m+1\over3}\right\rfloor
\]
from either endpoint.  Thus even the \(H=0\) residual endpoint has
unbounded delay while \(H,Z\), both root labels, and the local cap data
remain fixed.  The full construction and checker are in
`scratch/d5-hzero-capped-ladder-unbounded-delay.md` and
`scratch/check_d5_hzero_capped_ladder_delay_family.py`.

## Two-edge-cut mechanism

Every separation between consecutive ladder columns is a two-edge cut.
For any \(D_5\)-flow, the two labels on such a cut are equal: xor the
vertex equations on either side of the cut.  Thus a state induces a word
of cut labels along the ladder.

A root-component factor circuit crosses a cut in either zero or both
edges.  A rooted switch consequently acts on a prefix or suffix of this
cut-label word.  The zero-xor triple obstruction above is the resulting
word potential.

## Ring closure

Closing the repeating ladder without the two caps gives the circular
ladder, or prism, \(P_n=C_n\square K_2\).  This remains simple cubic and
bridgeless.  The complete dynamic-programming audit over **every**
normalized \(D_5\)-flow and **every** unordered root pair gives:

\[
\begin{array}{c|c|c|c}
n&|V(P_n)|&D_5\text{ flows modulo }S_5&
\text{maximum root-component distance}\\ \hline
3&6&5&0\\
4&8&35&2\\
5&10&121&2\\
6&12&645&3\\
7&14&3171&3\\
8&16&17371&4\\
9&18&96437&4.
\end{array}
\]

No root-local-bad component occurs through \(P_9\).  Instead, the observed
maximum for \(4\le n\le9\) is
\[
                              \lfloor n/2\rfloor.
\]
Thus ring closure currently supports **unbounded finite radius**, not an
actual root-local counterexample.  The fixed-point computation is much
stronger than a bounded search: every bad state/root pair in the stated
scope eventually reaches a good state.

## Reproduction

The capped-family literal checker defaults through \(L_4\); the longer
cases are available explicitly:

```text
python3 scratch/check_d5_capped_ladder_delay_family.py
python3 scratch/check_d5_capped_ladder_delay_family.py --through 6

c++ -O3 -std=c++20 scratch/audit_d5_root_switch_distance.cpp \
  -o /tmp/audit_d5_root_switch_distance
```

The prism output is frozen in
`scratch/d5-prism-root-local-radius-through18.json`.

## Consequence and limitation

The theorem disproves every universal constant-radius root-component
lemma.  It does not disprove the rooted Kempe-orbit conjecture: a state
may require arbitrarily many rooted switches and still always be
rescuable.  The computations explicitly rescue all displayed capped
states and all audited prism states.  This theorem does not resolve
FiveCDC.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified the recurring
extension, generated and audited the family, wrote the independent
checkers, and drafted this note.  These results are not peer reviewed.
