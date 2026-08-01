# A charge-kernel theorem for direct cleaning

## 1. Boundary data

Put `K = F_2^2`.  Let `C_1,...,C_k` be the support circuits of an
extendable first-coordinate projection.  At every support occurrence `i`,
let `a(i)` be its complement block and let `d_i` be its nonzero low-flow
derivative.  The original extension gives

\[
 \bigoplus_{i\in C_j}d_i=0\quad(j=1,\ldots,k),\qquad
 \bigoplus_{a(i)=a}d_i=0\quad(a\in A).                 \tag{1}
\]

Define the block--circuit charge matrix

\[
 D_{a,j}=\bigoplus_{\substack{i\in C_j\\a(i)=a}}d_i.  \tag{2}
\]

Both its row sums and its column sums are zero.  Its incidence graph is
the bipartite graph on block nodes `A` and circuit nodes `{1,...,k}` with
an edge `aj` exactly when `D[a,j] != 0`.  Isolated block nodes are retained.
An isolated circuit node can be ignored.

For a connected incidence component `Gamma`, let `A_Gamma` and `J_Gamma`
be its block and circuit nodes and define the binary linear map

\[
 \partial_\Gamma:\mathbb F_2^{A_\Gamma}\longrightarrow
 K^{J_\Gamma},\qquad
 (s_a)_a\longmapsto
 \left(\bigoplus_{a\in A_\Gamma}s_aD_{a,j}\right)_{j\in J_\Gamma}.
                                                               \tag{3}
\]

The column equations in (1) show that the all-ones vector
`1_Gamma` belongs to `ker partial_Gamma`.  Call the state
**charge-rigid** when

\[
             \ker\partial_\Gamma=\langle 1_\Gamma\rangle
             \quad\hbox{for every }\Gamma.             \tag{4}
\]

For an isolated block, (3) is the zero map on a one-dimensional domain,
so (4) holds.

## 2. Statement

**Theorem (charge-rigid cleaning).**  Every charge-rigid boundary state
has a directly clean extension.

This is an abstract boundary theorem.  It allows arbitrarily many support
circuits and complement blocks, arbitrary circuit lengths, interaction
loops, and arbitrary occurrence multiplicities.  In a cubic graph, direct
cleaning is exactly the Hušek--Šámal component-parity condition for the
chosen projection and therefore supplies a standard five-cycle double
cover of that graph.  The theorem does not assert that every graph admits
a charge-rigid projection.

## 3. Constant maps on charge components are integrable

Choose one map `L_Gamma in GL(K)` for every charge-incidence component and
give every block `a in A_Gamma` the same map.  Put

\[
                    t_i=L_\Gamma d_i\quad(a(i)\in A_\Gamma). \tag{5}
\]

These transformed derivatives integrate around every support circuit.  To
see this, fix `C_j`.  All nonzero entries `D[a,j]` lie in the unique
incidence component containing the circuit node `j`, and their xor is zero
by (1).  Entries from all other components are zero.  Hence

\[
 \bigoplus_{i\in C_j}t_i
 =L_\Gamma\left(\bigoplus_aD_{a,j}\right)=0.            \tag{6}
\]

Choose any integrated low edge values on each circuit.  Translating all
values on `C_j` by `z_j in K` gives every other integration.

Let `q(x_1,x_2)=x_1x_2` and
`B(x,y)=q(x+y)+q(x)+q(y)`.  The four cut-colour parities of a block are
equal, and their common value is

\[
 Q_a=\sum_{a(i)=a}\bigl(q(r_{i-1})+q(r_i)\bigr).        \tag{7}
\]

Under the circuit translations,

\[
 Q_a(z)=Q_a(0)+\sum_j B(z_j,L_\Gamma D_{a,j}).          \tag{8}
\]

Thus direct cleaning is the consistency of the binary linear system
`Q_a(z)=0` for all blocks `a`.

## 4. The complete dual obstruction is componentwise

A set of block rows, with indicator `s in F_2^A`, is a left dependency of
(8) precisely when, for every circuit `j`,

\[
 \bigoplus_a s_a L_{\Gamma(a)}D_{a,j}=0.                \tag{9}
\]

Circuit nodes belonging to different incidence components are disjoint.
Within one component the same invertible map `L_Gamma` occurs in every
term, so it cancels from (9).  Condition (9) on that component is exactly
`s|A_Gamma in ker partial_Gamma`.  Charge rigidity therefore says that
the full left kernel of (8) is spanned by the disjoint component indicators
`1_{A_Gamma}`.

The standard consistency criterion for a binary linear system now gives:
(8) is solvable if and only if

\[
                  R_\Gamma:=\sum_{a\in A_\Gamma}Q_a(0)=0
                  \quad\hbox{for every }\Gamma.         \tag{10}
\]

No other obstruction remains.

## 5. The tensor theorem kills all component sums simultaneously

Regard each charge-incidence component `Gamma` as one meta-block.  On every
support circuit its transformed derivative sum is zero: this is (6) for
the component containing the circuit node, while every other component has
charge zero on that circuit by definition.

The multi-circuit tensor lemma says the following.  If every meta-block has
zero derivative charge separately on every circuit, then one can choose an
independent map in `GL(K)` for every meta-block so that the total quadratic
obstruction at every meta-block is zero.  Here that total obstruction is
exactly `R_Gamma`: internal edges between constituent blocks contribute
twice and cancel, while every boundary occurrence contributes its summand
from (7).

For completeness, the tensor lemma is elementary.  Cross-pair expansion
on each circuit writes the meta-block obstruction as the degree parity in
a graph whose edge bit between meta-blocks `Gamma` and `Delta` is a linear
functional of `L_Gamma^{-1}L_Delta`.  Let `G0=GL(2,2)` and define, for a
Boolean function on its six elements,

\[
 \lambda(f)=f(0132)+f(0213)+f(0321).                   \tag{11}
\]

Then `lambda(1)=1`, while `lambda` kills every matrix-coordinate function.
Apply `lambda` independently at every meta-block to the indicator

\[
                    \prod_\Gamma(1+R_\Gamma).          \tag{12}
\]

After expansion, a nonconstant edge monomial either has a degree-one
vertex and is killed by (11), or its distinct-edge graph has minimum degree
at least two.  Since the expansion selects at most one incident edge at
each vertex, the latter graph is a disjoint union of cycles; its two cyclic
orientations cancel modulo two.  Only the constant term remains, and its
image is one.  Hence (12) is nonzero for at least one tuple of maps, proving
that all `R_Gamma` can be made zero simultaneously.

With those maps, (10) holds.  The translation system (8) is consistent,
and a solution makes every `Q_a` zero.  By (7), all four cut colours are
even at every complement block.  This proves the theorem.

## 6. Two concrete corollaries

**Corollary 1.**  If the charge-incidence graph has maximum degree at most
two, the state is directly cleanable.

**Proof.**  A node incident with exactly one nonzero charge cannot have
zero charge sum.  Hence every nontrivial connected component is a cycle.
At a degree-two node its two nonzero incident charges are equal.  They are
therefore one common nonzero vector all the way around the cycle.  At a
circuit node, a scalar block dependency must select both adjacent block
rows or neither.  Connectivity forces all block coefficients to agree, so
the kernel is spanned by the all-ones vector.  Isolated blocks also satisfy
(4).  Apply the theorem.  `square`

**Corollary 2.**  A two-support-circuit state is directly cleanable if at
most three blocks have nonzero per-circuit charge.

**Proof.**  For two circuits, every nonzero row has form `(x,x)`.  If there
are two such rows, their charges are the same nonzero vector; the scalar
kernel has dimension one.  If there are three, their charges are the three
distinct nonzero vectors of `K`, again giving a one-dimensional kernel.
Zero or one nonzero rows are impossible except for the all-zero case, in
which every block is isolated.  Apply the theorem.  `square`

The bound three in Corollary 2 cannot simply be removed.  With five
nonzero rows the scalar kernel has dimension at least three.  The Petersen
two-circuit interaction realizes this regime and has no direct cleaning,
although it admits strict circuit deletion and is not a FiveCDC
counterexample.

There is a precise finite consistency check on this boundary.  The 224
direct residuals in the complete support-14 census, the 6,036 direct
residuals in the complete support-15 census, and all eight direct residuals
in the published fixed-word support-16 subcase have exactly one nontrivial
charge component.  In every row it has five block nodes, two circuit nodes,
charge rank two, and kernel dimension three, hence excess nullity two.
`audit_known_residuals.py` derives this from the literal emitted words and
partitions.  This does not prove that all larger residuals have that form;
it shows that the charge theorem pinpoints the same Petersen-type algebraic
core in every currently frozen direct residual.

## 7. Exact logical boundary

The proved implication is

\[
 \text{charge-rigid chosen projection}\Longrightarrow
 \text{clean extension}\Longrightarrow\text{standard FiveCDC}.
\]

Neither converse is asserted.  In particular, no reduction currently
forces a hypothetical smallest FiveCDC counterexample to have a
charge-rigid projection, and no descent theorem is known which always
reduces excess charge-kernel nullity.
