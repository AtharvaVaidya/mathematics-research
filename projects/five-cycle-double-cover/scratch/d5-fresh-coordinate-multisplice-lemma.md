# The fresh-coordinate multi-splice lemma

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE LOCAL LEMMA / NOT A FIVECDC
RESOLUTION**.

## Statement

Let a cubic graph carry a \(D_5\) state, and write

\[
C_i=\{e:i\in q(e)\},\qquad
Y_{ij}=C_i\mathbin\triangle C_j.
\]

Assume coordinate \(z\) is unused, so \(C_z=\varnothing\).  Let \(L\)
be one circuit component of \(C_x\).  Then:

1. \(L\) is a legal \(Y_{xz}\)-component;
2. switching \(x,z\) on \(L\) preserves
   \(\sum_i\kappa(C_i)\), and hence preserves the normalized surface
   Euler characteristic;
3. for every \(a\notin\{x,z\}\),
   \[
                          Y_{ax}'=Y_{ax}\mathbin\triangle L.    \tag{1}
   \]

Suppose the distinct \(Y_{ax}\)-components meeting \(L\) are
\(K_1,\ldots,K_t\), and each \(L\cap K_i\) is one nonempty proper
edge-path.  Then (1) has a single circuit component containing every
edge in

\[
                         (K_1\cup\cdots\cup K_t)\setminus L.
\]

Consequently, if root edges \(r\in K_i\setminus L\) and
\(s\in K_j\setminus L\), the fresh-coordinate switch puts \(r,s\) on
one factor circuit.

## Proof

Because \(C_z=\varnothing\),

\[
                              Y_{xz}=C_x.
\]

Thus every component \(L\) of \(C_x\) is a legal switch component.
On \(L\), the transposition \(x,z\) removes coordinate \(x\) and adds
coordinate \(z\).  Therefore

\[
 C_x'=C_x\setminus L,\qquad C_z'=L,\qquad C_i'=C_i
 \quad(i\notin\{x,z\}).
\]

If \(C_x\) has \(k\) components, the pair of component counts changes
from \((k,0)\) to \((k-1,1)\), including the case \(k=1\).
Their sum is unchanged.  This proves neutrality.

The pairs \(ax\) and \(xz\) share exactly coordinate \(x\), so the
exact factor law gives (1).

It remains to identify the circuit surgery.  The symmetric difference
of two circuits whose intersection is one nonempty proper path is one
circuit: deleting the common path leaves one complementary
endpoint-to-endpoint path from each circuit, and their union is a
single circuit.

Apply this observation first to \(L,K_1\).  The resulting circuit
still meets \(K_2\) on exactly the original path \(L\cap K_2\),
because the \(K_i\) are distinct factor components and hence
edge-disjoint.  Symmetric difference with \(K_2\) merges it into the
same circuit.  Repeating proves inductively that

\[
                             L\mathbin\triangle K_1
                              \mathbin\triangle\cdots
                              \mathbin\triangle K_t
\]

is one circuit.  All \(Y_{ax}\)-components disjoint from \(L\) remain
unchanged in (1).  Hence the displayed circuit is precisely one
component of \(Y_{ax}'\) and contains every \(K_i\setminus L\), proving
the root conclusion. \(\square\)

## Exact order-14 corollary

In the cyclic-block one-step obstruction on graph6

```text
M??CEB@W_sE_J?F??
```

coordinate \(4\) is unused.  The circuit

\[
                         L=\{6,8,12,13,18,19\}
\]

is a component of \(C_2=Y_{24}\).  The three \(Y_{02}\)-components

\[
\begin{array}{c|l}
H&\{7,8,15,16\}\\
J&\{9,11,12,14\}\\
D&\{0,2,3,5,18,20\}
\end{array}
\]

meet \(L\) in exactly the single edges \(8,12,18\), respectively.
Switching \(24\) on \(L\) is neutral and splices \(H,J,D,L\) into one
\(Y_{02}\)-circuit.  It contains root edge
\(16\in H\setminus L\) and target edge \(3\in D\setminus L\), proving
the exact one-move rescue without a search argument.

The complete replay is

```text
python3 scratch/check_d5_cyclic_block_one_step_no_go_order14.py
```

## Scope

This lemma gives a proof-grade third-pair move whenever an unused
coordinate and the stated single-path intersections exist.  A
universal argument still has to produce such a fresh coordinate or
replace it by a neutral coordinate-transfer sequence in states using
all five coordinates.

## AI-use disclosure

OpenAI Codex agents, under human direction, recognized the fresh
coordinate operation in the exact rescue, formulated the
multi-splice lemma, and drafted the proof.  The argument is fully
exposed for human checking and has not undergone peer review.
