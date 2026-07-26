# The \(0,0,b,b\) cyclic four-cut is the published exceptional-signature branch

## Status

Consider the cyclic 4-cut obtained in
`docs/size-four-terminal-gap-cut-reduction.md`.  Two cut edges belong to
the exact-zero matching \(M\), and the other two have one common nonzero
\(\mathbb F_2^2\)-flow value \(b\).  Thus the ordered boundary word is,
up to reordering and a linear permutation of the three nonzero values,
\[
             (0,0,b,b).                                  \tag{1}
\]

This note proves three scoped conclusions.

1. Global cardinal minimality of \(M\) has an exact min-plus expression
   across the cut.  It makes the displayed state locally minimum on each
   shore, but it does not by itself produce a smaller exact-zero matching.
2. The word (1) is strictly coarser than the ten five-coordinate
   four-pole types.  Both an adjacent doubled-pair type \(AT_\pi\) and a
   disjoint doubled-pair type \(T_\pi T_\pi\) project to (1).
3. Those are precisely the kinds of types separated between the two
   exceptional signatures in Theorem 3.6 of Máčajová--Mazzuoccolo--
   Tabarelli.  Hence the present four-cut is not a newly solved
   configuration: it lands in their still-unresolved exceptional-signature
   branch.

An abstract boundary table at the end shows that the minimum-support and
signature data are logically compatible.  It is not claimed realizable by
graph poles.  Proving or disproving graph realizability remains the
published four-pole problem.

## 1. The two shore poles

Let \(G\) be a finite simple cubic graph and let
\[
 \delta_G(X)=\{z_1,z_2,e_1,e_2\}                         \tag{2}
\]
be a cycle-separating 4-cut.  Assume an
\(\mathbb F_2^2\)-flow \(\phi\) has exact zero set \(M\), which is a
matching of size four, and
\[
 \phi(z_1)=\phi(z_2)=0,\qquad
 \phi(e_1)=\phi(e_2)=b\ne0.                              \tag{3}
\]

In the factor-quotient application, all four cut edges belong to the
perfect matching complementary to the chosen two-factor.  Therefore they
have distinct endpoints on either shore.  Cutting the four edges produces
two ordered cubic 4-poles \(P_X,P_{\bar X}\).

The equality of the two nonzero values in (3) is not an extra assumption.
Flow conservation over \(X\) gives
\[
 0+0+\phi(e_1)+\phi(e_2)=0,
\]
and hence \(\phi(e_1)=\phi(e_2)\).

Write \(k_X\) and \(k_{\bar X}\) for the numbers of proper internal edges
of \(M\) on the two shores.  Since precisely two members of \(M\) cross
the cut,
\[
        k_X+k_{\bar X}=2.                               \tag{4}
\]

## 2. The exact \(\mathbb F_2^2\) min-plus boundary calculus

Let
\[
 \Sigma=\{(\sigma_1,\ldots,\sigma_4)\in
          (\mathbb F_2^2)^4:
          \sigma_1+\cdots+\sigma_4=0\}.                 \tag{5}
\]
The equation is the boundary conservation law obtained by summing the
flow equations over one pole.

For a pole \(P\) and \(\sigma\in\Sigma\), define
\[
 f_P(\sigma)\in\mathbb N\cup\{\infty\}                  \tag{6}
\]
as follows.  It is the minimum number of zero-valued proper internal pole
edges over partial flows with ordered boundary word \(\sigma\), subject to:

1. the internal zero edges form a matching; and
2. if \(\sigma_i=0\), no internal zero edge is incident with the internal
   endpoint of the \(i\)-th semiedge.

The second condition says exactly that, after gluing, a zero cut edge is
not adjacent to an internal zero edge.

Let
\[
       z(\sigma)=|\{i:\sigma_i=0\}|.                    \tag{7}
\]

> **Proposition 2.1 (exact cut gluing formula).**
> \[
> r_M(G)=
> \min_{\sigma\in\Sigma}
> \bigl(
> f_{P_X}(\sigma)+f_{P_{\bar X}}(\sigma)+z(\sigma)
> \bigr),                                               \tag{8}
> \]
> where \(r_M(G)\) is the minimum cardinality of an exact zero set that
> is a matching.

### Proof

A matching-supported flow on \(G\) restricts to partial flows on the two
poles with the same ordered boundary word.  Its internal zeros are counted
by the two \(f\)-terms, while every zero boundary position is one zero cut
edge and is counted once by \(z(\sigma)\).  Matching admissibility at the
four cut endpoints is exactly the condition built into (6).  This proves
the lower bound in (8).

Conversely, take partial pole flows attaining the two finite minima for
one common \(\sigma\).  Join corresponding semiedges and give the restored
cut edge the common boundary value.  Conservation holds at every vertex.
The internal zero matchings are disjoint, zero cut edges have distinct
endpoints, and condition 2 prevents adjacency between a zero cut edge and
an internal zero edge.  Thus the glued zero set is a matching of the
displayed size. \(\square\)

This formula is the exact information supplied by global minimum support;
no five-coordinate cover has yet been used.

## 3. What cardinal minimality actually implies

Let
\[
       \sigma_0=(0,0,b,b).                              \tag{9}
\]
The displayed flow proves
\[
 f_{P_X}(\sigma_0)\le k_X,\qquad
 f_{P_{\bar X}}(\sigma_0)\le k_{\bar X}.                \tag{10}
\]

Assume now that \(M\) is globally cardinal-minimum and \(|M|=4\).  By
(8),
\[
 f_{P_X}(\sigma)+f_{P_{\bar X}}(\sigma)+z(\sigma)\ge4
 \qquad(\sigma\in\Sigma).                              \tag{11}
\]
At \(\sigma_0\), equations (4), (10), and (11) force
\[
 f_{P_X}(\sigma_0)=k_X,\qquad
 f_{P_{\bar X}}(\sigma_0)=k_{\bar X}.                  \tag{12}
\]

Thus neither shore can be improved while retaining the same ordered
\(0,0,b,b\) boundary state and leaving the opposite shore fixed.

This is a relative statement, not an absolute minimum theorem for either
shore.  A cheaper partial flow with a different boundary word does not
splice to the unchanged opposite shore.  Two cheaper shore states help
only when they have one common ordered word \(\sigma\) and make the
left-hand side of (11) at most three.

For reference, the xor-zero words in \(\Sigma\), modulo
\(\operatorname{GL}(2,2)\) and terminal order, have the following value
patterns:

- \(0000\);
- \(00aa\), with \(a\ne0\);
- \(0abc\), where \(a,b,c\) are the three distinct nonzero values;
- \(aaaa\), with \(a\ne0\); and
- \(aabb\), with distinct nonzero \(a,b\).

Exactly three zeros are impossible.  The list follows immediately by
checking the parity of the multiplicities of the three nonzero group
elements.

The word (9) is the \(00aa\) case.

## 4. The tempting capping inference and its gap

On one shore, join the two zero boundary terminals by a cap edge of value
zero and join the two \(b\)-terminals by a cap edge of value \(b\).  This
closes the partial flow and gives an exact-zero matching of size
\[
        k_X+1                                             \tag{13}
\]
on the capped shore; similarly the other cap has size
\(k_{\bar X}+1\).  By (4), at least one of these numbers is at most two.

It is tempting to argue that a smaller or five-coverable capped graph must
repair the original cut.  That inference is invalid without a
boundary-preserving theorem.

- A cheaper capped flow whose zero cap becomes nonzero has a different
  four-pole boundary state and need not splice to the other shore.
- A five-cycle double cover of the cap need not project to the particular
  \(\mathbb F_2^2\)-flow in (3).
- A graph may have a standard five-cover even when a specified minimum
  exact-zero matching does not pack two \(T\)-joins.

Equation (8), rather than the unqualified minimum of either capped graph,
is the correct gluing invariant.

## 5. Five-coordinate four-pole types

A standard five-cycle double cover is equivalently a conservative
edge-labeling by the ten two-subsets
\[
       D_5=\binom{[5]}2.                                \tag{14}
\]
At a 4-pole boundary, coordinate parity permits exactly ten ordered types:
\[
 AA,\quad AT_2,AT_3,AT_4,\quad
 T_iT_j\quad(2\le i\le j\le4).                          \tag{15}
\]

This is the notation of Máčajová, Mazzuoccolo, and Tabarelli,
[*Cycle separating cuts in possible counterexamples to the cycle double
cover and the Berge--Fulkerson conjectures*](https://doi.org/10.26493/1855-3974.3409.c13),
Proposition 3.3.

Order the four semiedges so that the two zero positions in (9) are
positions 1 and \(\pi\), where \(\pi\in\{2,3,4\}\).  A doubled-pair
five-coordinate boundary word has the form
\[
       (A,A,B,B)                                        \tag{16}
\]
with the two \(A\)'s at positions \(1,\pi\).  Its type is:

\[
\begin{array}{c|c}
\text{relation between }A,B&\text{four-pole type}\\ \hline
A=B&AA\\
|A\cap B|=1&AT_\pi\\
A\cap B=\varnothing&T_\pi T_\pi.
\end{array}                                             \tag{17}
\]

This is a direct restatement of the type definitions: in the middle row,
the common coordinate occurs on all four semiedges; in the last row, the
two disjoint coordinate pairs induce the same terminal pairing twice.

## 6. Why both \(AT_\pi\) and \(T_\pi T_\pi\) project to \(0,0,b,b\)

For \(A=\{r,s\}\in D_5\), put
\[
 K_A=\langle \mathbf1+e_r,\mathbf1+e_s\rangle
 \le E_5,
\]
where \(E_5\) is the even-weight subspace of \(\mathbb F_2^5\).  Then
\[
        K_A\cap D_5=\{A\}.                              \tag{18}
\]
Consequently the quotient map
\[
        \rho_A:E_5\longrightarrow E_5/K_A
        \cong\mathbb F_2^2                              \tag{19}
\]
sends precisely the label \(A\) among the ten allowed labels to zero.

Apply \(\rho_A\) to (16).  If \(B\ne A\), then
\[
       (A,A,B,B)\longmapsto(0,0,\bar b,\bar b),
       \qquad \bar b=\rho_A(B)\ne0.                     \tag{20}
\]
Thus both rows \(AT_\pi\) and \(T_\pi T_\pi\) in (17) have the same
\(\mathbb F_2^2\) zero/nonzero boundary pattern.  The projection forgets
whether \(A\) and \(B\) intersect.

If \(A=B\), all four boundary values project to zero.  Therefore type
\(AA\) corresponds to \(0000\), not to (1), under this chosen kernel.

Projection also acts on internal edge labels.  Its exact zero set is the
entire \(A\)-label class.  Requiring that class to equal the specified
global matching \(M\) is a substantial coherence condition; it does not
follow merely from the existence of a five-coordinate pole labeling.

## 7. Comparison with the published exceptional signatures

Theorem 3.6 of the cited paper proves that if a minimum CDC counterexample
has a cycle-separating 4-cut, then, after ordering the terminals suitably,
the two pole signatures must be
\[
\begin{aligned}
 {\cal E}_4&=\{AA,AT_k,AT_j,T_kT_j\},\\
 {\cal E}_5&=\{T_iT_i,T_jT_j,T_kT_k,T_iT_k,T_iT_j\},
\end{aligned}                                           \tag{21}
\]
where
\[
       \{i,j,k\}=\{2,3,4\}.                             \tag{22}
\]
The two signatures are disjoint, so their partial covers cannot glue.
Their Conjecture 3.7 states that neither exact signature is realizable by
a 4-pole.

The boundary word (1) is compatible with this exceptional pair:

- \({\cal E}_5\) contains \(T_\pi T_\pi\) for every
  \(\pi\in\{i,j,k\}\);
- \({\cal E}_4\) contains \(AT_\pi\) for
  \(\pi=j\) or \(\pi=k\); and
- by (20), both types project to \(0,0,b,b\).

The types remain different—adjacent doubled pairs on one shore and
disjoint doubled pairs on the other—so they do not glue as a
five-coordinate state.

For the remaining orientation \(\pi=i\), the size-four exceptional
signature contains no \(AT_i\).  Therefore the following stronger,
currently unproved, hypothesis would exclude that orientation:

> each pole has a partial five-coordinate labeling which projects to the
> specified boundary flow (1), with its zero boundary label used as the
> quotient kernel.

Even under that added projection-coherence hypothesis, the two
orientations \(\pi=j,k\) survive exactly as in (21).  Hence projection
coherence alone would not eliminate the cyclic 4-cut.

## 8. A boundary-level countermodel to the naive inference

The compatibility can be displayed without a graph-realizability claim.
Choose \(\pi=j\).  On the first abstract pole retain the exceptional type
\[
       AT_j\in{\cal E}_4,
\]
and on the second retain
\[
       T_jT_j\in{\cal E}_5.
\]
Choose representatives \((A,A,B,B)\) in which:

- \(A,B\) intersect on the first pole;
- \(A,B\) are disjoint on the second pole; and
- \(A\) labels the two designated zero positions.

Quotient each state by its \(K_A\).  Both boundary words become
\(0,0,b,b\), while their five-coordinate types remain different.

Independently choose nonnegative costs \(k_X,k_{\bar X}\) with
\[
       k_X+k_{\bar X}=2
\]
and set
\[
\begin{aligned}
 f_{P_X}(\sigma_0)&=k_X,\\
 f_{P_{\bar X}}(\sigma_0)&=k_{\bar X},\\
 f_{P_X}(\sigma),f_{P_{\bar X}}(\sigma)&=\infty
       \quad(\sigma\ne\sigma_0),
\end{aligned}                                           \tag{23}
\]
together with all images under \(\operatorname{GL}(2,2)\).
Then the min-plus gluing value is exactly
\[
       k_X+k_{\bar X}+2=4,                              \tag{24}
\]
and no smaller common boundary state exists.

This abstract table satisfies the two pieces of information being tested:
the specified \(0,0,b,b\) state is globally minimum, and the
five-coordinate boundary types lie in the two exceptional signatures.
It is **not** asserted to be the signature or cost table of actual graph
poles.  Its purpose is logical: boundary parity plus cardinal minimality
alone cannot contradict the exceptional pair.

## 9. Exact scoped conclusion

> **Theorem 9.1 (cyclic-four-cut scope theorem).**
> In the connected size-four branch, an unavoidable terminal-gap
> obstruction yielding a cyclic cut with boundary flow word
> \(0,0,b,b\) is not eliminated by global minimum exact-zero cardinality
> or by the ten-type four-pole boundary calculus alone.
>
> Global minimality is exactly the family of min-plus inequalities (11).
> In a minimum CDC or five-CDC counterexample, the two shore signatures
> are necessarily the exceptional pair (21).  The word \(0,0,b,b\)
> forgets the distinction between the \(AT_\pi\) and
> \(T_\pi T_\pi\) types, and is compatible with the exceptional pair for
> two of the three terminal pairings.

Therefore a proof must add at least one genuinely stronger ingredient:

1. prove the published exceptional signatures unrealizable;
2. prove a support-preserving projection/coherence theorem and then add a
   further argument for the two surviving pairings;
3. derive a common lower-cost boundary state violating (11); or
4. exploit internal path/circuit topology not recorded by either boundary
   signature.

The existing finite four-pole censuses find no realization of either
exceptional signature, but that is computational evidence rather than the
human proof required here.

## AI-use disclosure

This min-plus formulation, projection comparison, boundary countermodel,
and exposition were developed with substantial assistance from OpenAI
Codex language-model agents under human direction.  The ten-type
four-pole framework, Theorem 3.6, and Conjecture 3.7 are prior work of
Máčajová, Mazzuoccolo, and Tabarelli and are explicitly attributed above.
All new deductions in this note are displayed as finite parity and gluing
arguments so they can be checked without trusting an AI system.
