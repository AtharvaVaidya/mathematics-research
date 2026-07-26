# The exceptional four-pole pair is an opposite rooted-packing pair

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE REDUCTIONS / EXACT TEN-STATE ALGEBRA /
EXCEPTIONAL SIGNATURES NOT REALIZED OR REFUTED IN FULL**.

The primary source is E. Máčajová, G. Mazzuoccolo, and G. Tabarelli,
[*Cycle separating cuts in possible counterexamples to the cycle double
cover and the Berge--Fulkerson
conjectures*](https://doi.org/10.26493/1855-3974.3409.c13),
*Ars Mathematica Contemporanea* 26 (2026), #P2.03.  The statements used
below were checked against the version-of-record PDF, not inferred from a
secondary summary.

Their Theorem 3.6 and Remark 3.2 show that the two ordered shore poles of
a cycle-separating four-cut in a minimum CDC or minimum five-CDC
counterexample must have, after naming
\(\{i,j,k\}=\{2,3,4\}\), the two exact signatures
\[
\begin{aligned}
 {\cal E}_4(i;j,k)&=\{AA,AT_j,AT_k,T_jT_k\},\\
 {\cal E}_5(i;j,k)&=\{T_iT_i,T_jT_j,T_kT_k,T_iT_j,T_iT_k\}.
                                                               \tag{1}
\end{aligned}
\]
Their Conjecture 3.7 says that neither signature is realizable by any
four-pole.

This note does **not** prove that conjecture.  It proves three narrower
facts that use structure present in this project.

1. Projection through the distinguished
   \(\mathbb F_2^2\)-flow turns the distinction \(AT_\pi\) versus
   \(T_\pi T_\pi\) into the exact question whether a distinguished
   nonzero cap edge belongs to a two-\(T\)-join packing.
2. A shore containing no internal zero edge always has a packing avoiding
   that cap edge.  Consequently the \({\cal E}_4\) shore in the project's
   \(0,0,b,b\) four-cut must contain at least one internal zero edge.
3. Exact composition of the ten boundary types shows that a
   two-plus-two decomposition cannot create \({\cal E}_4\) without an
   exceptional four-type factor.  For \({\cal E}_5\), the only additional
   factorization allowed by the published switching lemmas uses one
   three-type looped edge and one five-type looped path.

The remaining obstruction is therefore a genuine rooted linkage problem,
not an ambiguity in the ten boundary types.

## 1. A canonical section of the quotient

Write
\[
 E_5=\{x\in\mathbb F_2^5:|x|\equiv0\pmod2\},\qquad
 D_5=\binom{[5]}2\subset E_5.                            \tag{2}
\]
Fix \(A=\{1,2\}\in D_5\), put
\[
 g_1=\mathbf1+e_1,\qquad g_2=\mathbf1+e_2,
\]
and let
\[
 K_A=\langle g_1,g_2\rangle,\qquad
 \rho_A:E_5\longrightarrow E_5/K_A\cong\mathbb F_2^2.  \tag{3}
\]
The only member of \(D_5\) in the zero coset is \(A\).

Let \(W=[5]\setminus A\).  Each nonzero coset of (3) contains exactly
three members of \(D_5\):
\[
       d(q),\qquad d(q)+g_1,\qquad d(q)+g_2,            \tag{4}
\]
where \(d(q)\) is the unique member disjoint from \(A\).  The other two
members meet \(A\) in one point.  The three values \(d(q)\), as \(q\)
runs over the nonzero quotient elements, are the three edges of the
triangle on \(W\).  Notice also that
\[
 d(q)+g_1+g_2=d(q)+A
\]
has weight four and is not in \(D_5\).

These statements are checked by the following literal list when
\(A=\{1,2\}\):
\[
\begin{array}{c|c}
\text{unique disjoint member}&\text{two intersecting members}\\ \hline
\{4,5\}&\{1,3\},\{2,3\}\\
\{3,5\}&\{1,4\},\{2,4\}\\
\{3,4\}&\{1,5\},\{2,5\}.
\end{array}                                             \tag{5}
\]
Relabelling the five coordinates proves the assertion for arbitrary
\(A\).

## 2. Projection-coherent lifts are two rooted \(T\)-joins

Let \(L\) be a finite loopless cubic multigraph and let
\[
 \phi:E(L)\longrightarrow\mathbb F_2^2
\]
be a flow whose exact zero set \(M\) is a matching.  Put
\[
 K=L-M,\qquad T=\partial M.                             \tag{6}
\]

> **Lemma 2.1 (canonical lift with a rooted edge).**
> The \(D_5\)-labellings
> \[
>       y:E(L)\longrightarrow D_5,\qquad
>       \rho_A(y(e))=\phi(e),                           \tag{7}
> \]
> satisfying coordinate parity at every vertex are in bijection with
> ordered pairs of edge-disjoint \(T\)-joins
> \[
>                         (J_1,J_2)
> \quad\text{in }K.                                    \tag{8}
> \]
> Under this bijection, for every nonzero edge \(f\),
> \[
> \begin{array}{c|c}
> \text{membership of \(f\)}&y(f)\text{ relative to }A\\ \hline
> f\notin J_1\cup J_2&y(f)\cap A=\varnothing,\\
> f\in J_1\mathbin{\dot\cup}J_2&|y(f)\cap A|=1.
> \end{array}                                           \tag{9}
> \]

### Proof

Define the base labelling
\[
 y_0(e)=
 \begin{cases}
 A,&\phi(e)=0,\\
 d(\phi(e)),&\phi(e)\ne0.
 \end{cases}                                            \tag{10}
\]
At a vertex outside \(T\), the three quotient values are the three
distinct nonzero elements of \(\mathbb F_2^2\).  The corresponding
three \(d\)-labels are the triangle on \(W\), so their xor is zero.

At a vertex of \(T\), the incident values are \(0,q,q\).  The base xor
is therefore \(A\).  Every lift of a nonzero edge differs from its base
label by exactly one of
\[
                       0,\quad g_1,\quad g_2;           \tag{11}
\]
the fourth kernel element \(g_1+g_2=A\) is forbidden by its weight.
Let \(J_r\) contain the edges corrected by \(g_r\).
The two sets are disjoint.

At a vertex outside \(T\), conservation of the correction is equivalent,
because \(g_1,g_2\) are independent, to each \(J_r\) having even degree.
At a vertex in \(T\), its base defect is
\[
                  A=g_1+g_2,
\]
so each \(J_r\) must have odd degree.  Thus the two correction sets are
edge-disjoint \(T\)-joins.  Conversely any pair (8) corrects (10) at
every vertex and produces a \(D_5\)-labelling.  Formula (9) is exactly
(4). \(\square\)

This is the usual two-\(T\)-join lift written with a fixed quotient
section.  The new point needed here is the last, rooted column (9).

## 3. The exceptional signatures have opposite root polarities

Return to a four-pole whose ordered boundary flow is
\[
                         (0,0,b,b),\qquad b\ne0.        \tag{12}
\]
Join the two zero semiedges to form a zero cap edge \(z\), and join the
two \(b\)-semiedges to form a nonzero cap edge \(f\).  Let \(\pi\) be
the terminal pairing occupied by the two zero positions.

In every projection-coherent lift, \(y(z)=A\).  Cutting the two cap
edges back into semiedges gives the doubled boundary word
\[
                         (A,A,B,B).                    \tag{13}
\]
By (9),
\[
\begin{aligned}
 f\notin J_1\cup J_2
    &\quad\Longleftrightarrow\quad
      A\cap B=\varnothing
    \quad\Longleftrightarrow\quad T_\pi T_\pi,\\
 f\in J_1\mathbin{\dot\cup}J_2
    &\quad\Longleftrightarrow\quad
      |A\cap B|=1
    \quad\Longleftrightarrow\quad AT_\pi.              \tag{14}
\end{aligned}
\]

Consequently:

- a projection-coherent packing on an \({\cal E}_4\) shore can only use
  \(f\), and it can exist only for \(\pi\in\{j,k\}\);
- every projection-coherent packing on an \({\cal E}_5\) shore must
  avoid \(f\).

This is an exact reformulation, not an existence assertion.  In
particular it does not infer that an arbitrary five-coordinate pole
labelling projects to the distinguished flow.

## 4. A zero-free shore always has the avoiding state

The project's four-cut has additional graph structure.  Let \(G\) be
cyclically four-edge-connected and cubic, and let a cycle-separating
four-cut have distinct endpoints on each shore.  Let \(P\) be one
connected shore pole.  Suppose its boundary flow is (12) and that the
shore contains no proper internal zero edge.

Write \(u_1,u_2\) for the endpoints of the zero semiedges and
\(v_1,v_2\) for the endpoints of the nonzero semiedges.  Add the cap
edges
\[
                         z=u_1u_2,\qquad f=v_1v_2.      \tag{15}
\]
The capped flow has exact zero set \(\{z\}\).

> **Lemma 4.1 (zero-free shore avoidance).**
> The capped graph has two edge-disjoint
> \(\{u_1,u_2\}\)-joins which both avoid \(f\).  Hence the four-pole
> signature contains \(T_\pi T_\pi\).

### Proof

It is enough to find two edge-disjoint \(u_1\)-to-\(u_2\) paths in the
proper graph of \(P\), because those paths are the required joins and
do not use the artificial edge \(f\).

Suppose a bridge \(h\) of \(P\) separates \(u_1\) from \(u_2\).  Choose
the component \(Y\) of \(P-h\) containing at most two of the four
original cut endpoints.  It contains at least one, because the two zero
endpoints are separated.  Put \(t=|Y\cap\{u_1,u_2,v_1,v_2\}|\), so
\[
                         1\le t\le2.                  \tag{16}
\]
In the ambient cubic graph,
\[
                         |\delta_G(Y)|=t+1\le3.        \tag{17}
\]

The shore \(Y\) contains a circuit.  Indeed, if it were a tree on \(n\)
vertices, the cubic degree sum, counting its \(t\) original cut edges
and the bridge \(h\), would give
\[
          3n=2(n-1)+(t+1),\qquad\text{hence}\qquad n=t-1. \tag{18}
\]
For \(t=1\) this says \(n=0\).  For \(t=2\) it says \(n=1\), so the one
vertex would be incident with two members of the original four-cut,
contrary to the distinct-endpoint hypothesis.

The complement of \(Y\) contains the cyclic opposite shore of the
original four-cut.  Thus (17) is a cycle-separating cut of size at most
three, contradicting cyclic four-edge-connectivity.  No bridge of \(P\)
separates \(u_1,u_2\).

The edge form of Menger's theorem now supplies two edge-disjoint
\(u_1\)-to-\(u_2\) paths in \(P\).  Lemma 2.1 turns them into a
projection-coherent lift, and (14) gives type \(T_\pi T_\pi\).
\(\square\)

Since \({\cal E}_4\) contains no type \(T_\pi T_\pi\), this proves:

> **Corollary 4.2.**
> In the connected size-four minimum-support branch, if the
> \(0,0,b,b\) cyclic cut has the published exceptional pair, its
> \({\cal E}_4\) shore contains at least one of the two proper internal
> zero edges.

The two proper internal zero counts sum to two.  Therefore the only
remaining distributions, with the \({\cal E}_4\) shore listed first, are
\[
                         (1,1)\quad\text{or}\quad(2,0). \tag{19}
\]
The zero-free \({\cal E}_5\) shore in the second case is consistent with
its required avoiding polarity, so (19) is a reduction rather than a
contradiction.

## 5. Exact two-plus-two composition

Let \(P,Q\) be ordered four-poles.  Join positions \(3,4\) of \(P\) to
positions \(1,2\) of \(Q\), and retain the other four positions in the
order
\[
                  P_1,P_2,Q_3,Q_4.                    \tag{20}
\]
For boundary signatures \({\cal C}(P),{\cal C}(Q)\), exact label
matching at the two joins defines a finite operation
\[
                         {\cal C}(P)\circ{\cal C}(Q).  \tag{21}
\]
Because a pole admits every global \(S_5\)-translate of any admitted
word, the ten orbit types contain all information needed for (21).

The complete singleton table is below.  A cell lists every possible
output type; a blank cell means that no representatives of the two input
orbits agree on both glued positions.

\[
\renewcommand{\arraystretch}{1.15}
\begin{array}{c|cccccccccc}
\circ&AA&AT_2&T_2T_2&AT_3&AT_4&T_2T_3&T_2T_4&T_3T_3&T_3T_4&T_4T_4\\ \hline
AA&AA&AT_2&T_2T_2&&&&&&&\\
AT_2&AT_2&AA,AT_2,T_2T_2&AT_2,T_2T_2&&&&&&&\\
T_2T_2&T_2T_2&AT_2,T_2T_2&AA,AT_2&&&&&&&\\
AT_3&&&&AT_3&AT_4&T_2T_3&T_2T_4&&&\\
AT_4&&&&AT_4&AT_3&T_2T_4&T_2T_3&&&\\
T_2T_3&&&&T_2T_3&T_2T_4&AT_3,T_2T_3&AT_4,T_2T_4&&&\\
T_2T_4&&&&T_2T_4&T_2T_3&AT_4,T_2T_4&AT_3,T_2T_3&&&\\
T_3T_3&&&&&&&&T_3T_3&T_3T_4&T_4T_4\\
T_3T_4&&&&&&&&T_3T_4&T_3T_3,T_3T_4,T_4T_4&T_3T_4\\
T_4T_4&&&&&&&&T_4T_4&T_3T_4&T_3T_3
\end{array}                                             \tag{22}
\]

For arbitrary signatures, distribute (22) over all input pairs and take
the union.  This proves the exact gluing formula
\[
                    {\cal C}(P\circ Q)
                    ={\cal C}(P)\circ{\cal C}(Q).       \tag{23}
\]

The 640 ordered xor-zero boundary words give (22) directly.  The replay
program
`scratch/four_pole_two_plus_two_algebra.py` constructs those words,
quotients by all 120 colour permutations, and regenerates the table.

## 6. Factorization theorem under the published switching lemmas

To avoid assuming graph realizability, filter all \(2^{10}-1\) nonempty
type sets only by the necessary conclusions of Máčajová--Mazzuoccolo--
Tabarelli Lemmas 3.4 and 3.5:

1. the looped \(K_4\) signature graph has no degree-one vertex and no
   isolated loop; and
2. every loop \(XX\) has either
   \[
        XY,YY
   \]
   for some \(Y\ne X\), or
   \[
        XY,XZ,YZ
   \]
   for distinct \(Y,Z\ne X\).

Exactly 259 nonempty masks pass these necessary tests.  Applying (22) to
all \(259^2\) ordered pairs gives the following exact conclusion.

> **Theorem 6.1 (exceptional two-plus-two factorization).**
>
> 1. If the composition of two nonempty lemma-admissible signatures is
>    a member of the four-type family \({\cal E}_4\), one input is itself
>    a member of the \({\cal E}_4\) family.
> 2. If the composition is a member of the five-type family
>    \({\cal E}_5\), then either one input is itself in the
>    \({\cal E}_5\) family, or, up to the compatible names and reversal
>    of the composition, the two input signature graphs are:
>    - one looped edge
>      \[
>                    \{XX,XY,YY\};                    \tag{24}
>      \]
>    - one looped three-vertex path
>      \[
>                    \{UU,UV,VV,VW,WW\}.              \tag{25}
>      \]

This is readily checked by hand from (22): retain only unions equal to
one of the six target rows (1), then apply the two displayed switching
conditions.  The program performs the same finite filtering without a
SAT solver.

In particular, a minimum-vertex \({\cal E}_4\) pole has no proper
two-plus-two decomposition into two positive smaller poles.  A
minimum-vertex \({\cal E}_5\) pole either has no such decomposition or
reduces to the sole unresolved looped-edge/looped-path pattern
(24)--(25).  The program does **not** assert that the looped path (25)
is realizable by a graph pole; no such pole occurs in the project's
complete order-16 census.

## 7. Reproduction and exact boundary of the result

Run

```sh
python3 scratch/four_pole_two_plus_two_algebra.py \
  --output scratch/four-pole-two-plus-two-algebra-result.json
```

The retained hashes are

```text
9469b35d5034b9196d37092a8c701132046d68aee04854deee5f4947f8455661  scratch/four_pole_two_plus_two_algebra.py
e12307cad9a7176dfc8072f9d4052edd148cea5b4d9e11be8617c936a00d65c9  scratch/four-pole-two-plus-two-algebra-result.json
09c36ddf3ec5901e9b8a6a6a051b745bd31b7420fe811b6a098a263503e3faa5  scratch/verify_four_pole_two_plus_two_algebra.mjs
```

The output records all 640 words, the orbit sizes, all 100 cells of
(22), all 259 lemma-admissible masks, and every exceptional
factorization.  The JavaScript verifier is independently structured and
reconstructs the orbits, composition table, published-lemma filter, and
factorization counts without calling the Python implementation.  Its
current output is

```text
{"status":"PASS","words":640,"orbit_sizes":[10,60,30,60,60,120,120,30,120,30],"lemma_admissible_masks":259,"factorization_counts":{"0x119":[6,0],"0x2b":[8,0],"0x53":[8,0],"0x2e4":[10,4],"0x3a4":[12,4],"0x3c4":[12,4]}}
```

What is now proved is sharply scoped:

- the distinguished \(\mathbb F_2^2\)-projection converts the exceptional
  pair into opposite rooted cap-edge requirements;
- a zero-free \({\cal E}_4\) shore is impossible in the actual cyclic
  four-cut branch; and
- a minimal exceptional pole has the restricted decomposition structure
  in Theorem 6.1.

What is **not** proved:

- neither exceptional signature has been realized;
- neither has been ruled out for arbitrary four-poles;
- a general projection-coherent lift need not exist merely because the
  pole has some five-coordinate labelling; and
- the surviving cases (19), especially the rooted four-mark packing
  state, remain open.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified the rooted
projection, derived the zero-free shore argument and the ten-state
composition reduction, wrote the replay program, and drafted this note.
The exceptional signatures, boundary-type framework, and switching
lemmas are prior work of Máčajová, Mazzuoccolo, and Tabarelli and are
explicitly attributed above.  The mathematical arguments and complete
finite table are displayed so they can be checked without trusting an AI
system.  This is not independent human peer review and is not a claim of
resolving five-CDC or Conjecture 3.7.
