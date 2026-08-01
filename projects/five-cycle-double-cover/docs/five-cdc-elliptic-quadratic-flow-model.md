# Five-cycle double covers are anisotropic flows in elliptic four-space

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE EXACT REFORMULATION / NOVELTY NOT
ESTABLISHED / NO RESOLUTION**.

This note repackages the mandatory ten-label \(D_5\) encoding as a
quadratic flow problem.  It applies to finite multigraphs, including
parallel edges and loops when a loop is counted twice in vertex
incidence.  The reformulation is exact; it does not make the existence
problem automatically linear.

## 1. The elliptic quadratic space

Let
\[
 V=\left\{x=(x_0,\ldots,x_4)\in{\mathbb F}_2^5:
                       \sum_{i=0}^4x_i=0\right\}.                \tag{1}
\]
This is a four-dimensional vector space.  Define
\[
                         q(x)=\sum_{0\le i<j\le4}x_ix_j.        \tag{2}
\]
For \(x\in V\), its Hamming weight is \(0,2\), or \(4\), and
\[
 q(x)=\binom{|x|}{2}\pmod2.
\]
Consequently
\[
 q(x)=
 \begin{cases}
 1,&|x|=2,\\
 0,&|x|\in\{0,4\}.
 \end{cases}                                                    \tag{3}
\]
Thus the ten anisotropic vectors are exactly
\[
                    q^{-1}(1)=D_5=\binom{[5]}2,                 \tag{4}
\]
while the five nonzero singular vectors are the complements of the
five coordinate singletons.

The polar form of \(q\) is
\[
 B(x,y)=q(x+y)+q(x)+q(y)
       =\sum_{i=0}^4x_iy_i\qquad(x,y\in V).                    \tag{5}
\]
It is nondegenerate on \(V\): if an even vector is orthogonal to every
even vector, all of its coordinates are equal, and the all-one vector
does not belong to \(V\).  Hence \((V,q)\) is the four-dimensional
elliptic quadratic space over \({\mathbb F}_2\).

Coordinate permutations give isometries of \(q\).  Conversely, every
isometry permutes the five nonzero singular vectors.  Those five
vectors span \(V\) and have only the relation that their sum is zero,
so this action is faithful.  Every permutation is already induced by
a coordinate permutation.  Therefore
\[
                             O(V,q)\cong S_5.                   \tag{6}
\]
This identifies the familiar \(S_5\)-action on the ten two-subsets
with the full orthogonal symmetry of the quadratic model.

## 2. Exact equivalence with five Eulerian edge sets

For a finite multigraph \(G\), write each loop twice in the incidence
list of its vertex.  A \(V\)-flow is a map
\[
                         \phi:E(G)\longrightarrow V
\]
such that
\[
                  \sum_{\text{edge-ends incident with }v}
                             \phi(e)=0                         \tag{7}
\]
at every vertex \(v\).  In characteristic two, the two incidences of
a loop cancel, exactly as they do in an even-degree condition.

> **Theorem 2.1 (elliptic-flow equivalence).**  
> The following objects are in bijection:
>
> 1. five Eulerian edge subsets
>    \(C_0,\ldots,C_4\subseteq E(G)\) in which every edge belongs to
>    exactly two of the \(C_i\); and
> 2. \(V\)-flows \(\phi\) satisfying
>    \[
>                              q(\phi(e))=1
>                         \quad\text{for every }e\in E(G).      \tag{8}
>    \]

### Proof

Given the five edge subsets, define
\[
             \phi(e)_i=
             \begin{cases}
             1,&e\in C_i,\\
             0,&e\notin C_i.
             \end{cases}                                       \tag{9}
\]
Every edge lies in exactly two sets, so \(\phi(e)\) has weight two.
It belongs to \(V\) and satisfies (8) by (3).  At a vertex, coordinate
\(i\) of (7) is the degree of that vertex in \(C_i\), modulo two.
Thus the five Eulerian conditions are exactly the flow equations.

Conversely, (8) and (3) say that every \(\phi(e)\) has exactly two
nonzero coordinates.  Put
\[
                         C_i=\{e:\phi(e)_i=1\}.                 \tag{10}
\]
Each edge then belongs to exactly two sets, and coordinate \(i\) of
(7) says that \(C_i\) has even degree at every vertex.  Hence every
\(C_i\) is Eulerian.  The constructions (9) and (10) are inverse.
\(\square\)

Parallel edges are simply distinct variables in this bijection.  A
loop may be selected or omitted independently subject to the
exact-two rule; it contributes degree two to each selected Eulerian
set and therefore no parity obstruction.  This is exactly the
two-incidence convention in (7).

The standard Five-Cycle Double Cover Conjecture can therefore be
stated equivalently as:

> Every finite bridgeless graph has an everywhere-anisotropic flow in
> the elliptic quadratic space \((V,q)\).

Allowing one of the five Eulerian subsets to be empty simply means that
one coordinate of the anisotropic flow is unused.  It does not change
the phrase “at most five”; no orientability constraint is present in
this reformulation.

## 3. The avoided five-circuit formulation

Let
\[
        \Sigma=\{[5]\setminus\{i\}:0\le i<5\}
              =q^{-1}(0)\setminus\{0\}.                        \tag{11}
\]
The five members of \(\Sigma\) sum to zero, and any four form a basis
of \(V\).  Thus \(\Sigma\) is a five-element circuit of the binary
four-space.  Conversely, every five-element circuit has form
\[
                         \{b_1,b_2,b_3,b_4,
                                  b_1+b_2+b_3+b_4\}             \tag{12}
\]
for some basis \(b_1,\ldots,b_4\), so \(GL(4,2)\) acts transitively on
these circuits.

> **Corollary 3.1 (avoided circuit).**  
> A graph \(G\) has a five-cycle double cover if and only if it has a
> nowhere-zero \(V\)-flow \(\psi\) for which the unused value set
> \[
>                    (V\setminus\{0\})\setminus\psi(E(G))
> \]
> contains a five-element circuit.

### Proof

An anisotropic flow from Theorem 2.1 avoids the singular circuit
\(\Sigma\), proving one direction.  Conversely, suppose a nowhere-zero
flow avoids a five-circuit \(S\).  Choose \(T\in GL(4,2)\) with
\(T(S)=\Sigma\).  The transformed flow \(T\psi\) remains nowhere-zero
and avoids \(\Sigma\).  The ten remaining nonzero values are exactly
\(q^{-1}(1)\), so Theorem 2.1 gives a five-cycle double cover.
\(\square\)

There are
\[
                   \frac{|GL(4,2)|}{5\cdot4!}
                   =\frac{20160}{120}=168                       \tag{13}
\]
five-circuits.  The denominator counts the five choices of which
circuit member to omit to obtain a basis and the \(4!\) orders of that
basis.  Thus Corollary 3.1 converts the target into a finite
value-avoidance condition on an otherwise ordinary nowhere-zero
four-bit flow.  Fixing the circuit to \(\Sigma\) recovers the ten-label
SAT encoding, so this is a change of viewpoint, not a relaxation.

## 4. Why the problem remains nonlinear

The conservation laws (7) are linear, but the edge restriction (8) is
quadratic.  Given one anisotropic flow \(\phi\), every other flow with
the same boundary data has form
\[
                              \phi+z,                           \tag{14}
\]
where \(z\) is a \(V\)-valued circulation.  Its edge values remain
anisotropic precisely when
\[
             q(z(e))+B(\phi(e),z(e))=0
                    \qquad(e\in E(G)),                         \tag{15}
\]
because
\[
 q(\phi(e)+z(e))
 =q(\phi(e))+q(z(e))+B(\phi(e),z(e)).                           \tag{16}
\]
Equation (15) is an exact quadratic feasibility system on the
cycle-space variables.  It explains algebraically why solving the
linear parity equations alone is insufficient.

If \(z\) assigns one constant \(h\in V\) to every edge of a proper
cycle and zero elsewhere, (15) becomes
\[
                         q(h)=B(\phi(e),h)
                    \qquad(e\text{ on the cycle}).              \tag{17}
\]
This is the quadratic form of the cycle-translation lemma in
`rooted-cycle-translation-obstruction.md`.

For a weight-two shift \(h\), equation (17) says that every cycle
label meets \(h\) in one coordinate.  For a weight-four shift
\(h=[5]\setminus\{v\}\), it says that every cycle label avoids \(v\).
These are exactly the cut and missing-coordinate alternatives used in
the translation-blocker classification.

## 5. SAT/XOR interpretation

Writing
\[
                          x_{e,i}=\phi(e)_i
\]
turns (9) into the mandatory project encoding:

\[
\sum_{i=0}^4x_{e,i}=2\quad(e\in E(G)),                          \tag{18}
\]
\[
\bigoplus_{\text{edge-ends incident with }v}x_{e,i}=0
            \quad(v\in V(G),\ 0\le i<5).                       \tag{19}
\]

The XOR rows (19) are the linear flow equations.  The exact-cardinality
row (18) is equivalent, on the even subspace, to the anisotropy
equation \(q(\phi(e))=1\).  Thus the native XOR instance, any
certificate-producing CNF or pseudo-Boolean translation of
exactly-two, and the elliptic-flow formulation describe the same
finite object.

## Scope and novelty

The equivalence in Theorem 2.1 is elementary and should be treated as
a reformulation, not as a claimed new theorem.  The orthogonal
language and its use in the rooted cycle-translation obstruction were
developed within this project, but no specialist literature review has
established priority.  The note supplies a compact algebraic target for
future reductions; it is not a proof or disproof of the Five-Cycle
Double Cover Conjecture.

## AI-use disclosure

OpenAI Codex agents, under human direction, recognized the ten
two-subsets as the anisotropic vectors of the elliptic quadratic form,
proved the exact flow equivalence including loops and parallel edges,
derived the quadratic perturbation equations, and drafted this note.
All arguments are displayed for line-by-line human checking.  This is
not independent human review and not a resolution of the conjecture.
