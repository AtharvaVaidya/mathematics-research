# The tensor frontier for one support circuit

Date: 2026-07-29

Status: **UNIVERSAL ABSTRACT TENSOR THEOREM PROVED / EVERY
ONE-SUPPORT-CIRCUIT STATE DIRECTLY CLEANABLE / NOT A
FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## 1. The broad algebraic lemma

Let \(K=\mathbb F_2^2\), with its nondegenerate alternating form
\(B\), and let \({\cal G}=\operatorname{GL}(2,2)\).  On a vertex set
\(V\), fix an arbitrary orientation \((a,b)\) of every unordered pair
\(\{a,b\}\), and give it an arbitrary linear functional
\[
             \phi_{ab}:\operatorname{Mat}_2(\mathbb F_2)\longrightarrow
             \mathbb F_2.
\]
For independently chosen \(L_a\in{\cal G}\), put
\[
             w_{ab}=\phi_{ab}(L_a^{-1}L_b),\qquad
             Q_a=\sum_{b\ne a}w_{ab}.                 \tag{1}
\]
Thus the \(w_{ab}=1\) pairs form a simple graph, and \(Q_a\) is its
degree parity at \(a\).

The theorem proved here is:

> For every finite \(V\) and every family \((\phi_{ab})\), there are
> \(L_a\in\operatorname{GL}(2,2)\) for which all \(Q_a=0\).

Section 3 gives a human-checkable proof with no enumeration.  The SAT
certificates through five vertices are retained as finite
cross-checks.

## 2. Why this contains every one-circuit obstruction

Cut a cyclic support word at any edge.  Let \(\pi_i\in V\) own
occurrence \(i\), let \(d_i\in K-\{0\}\) be its derivative, and assume
the conservation equations
\[
                    \bigoplus_{\pi_i=a}d_i=0
                    \quad(a\in V).                    \tag{2}
\]
Choose local maps \(L_a\), and write \(z_i=L_{\pi_i}d_i\).
For distinct \(a,b\), define
\[
 w_{ab}=\sum_{\substack{j<i\\\pi_j=b,\ \pi_i=a}}
                         B(z_j,z_i).                  \tag{3}
\]
The sum obtained with the reverse ordering has the same value: the
sum of the two expressions is
\[
 B\left(\sum_{\pi_j=b}z_j,\sum_{\pi_i=a}z_i\right)=0
\]
by (2).  Hence (3) supplies one symmetric bit for the unordered pair.
It is also independent of the cut.  Indeed, moving one occurrence
\((a,z)\) across the cut changes its pair bit with \(b\) by
\(B(z,\sum_{\pi_i=b}z_i)=0\); the case of a \(b\)-occurrence is the
same.

Every element of \(\operatorname{GL}(2,2)\) preserves \(B\).  Therefore
\[
 B(L_bd_j,L_ad_i)
 =B(L_a^{-1}L_bd_j,d_i).
\]
For fixed \(a,b\), summing these terms defines a linear functional
\(\phi_{ab}\) of the matrix \(L_a^{-1}L_b\).  Thus (3) has exactly the
form (1).

Let \(r_i\) denote the edge value after occurrence \(i\), so that
\(r_{i-1}+r_i=z_i\), with cyclic indices.  The integrated
boundary-parity calculation gives
\[
                 \text{obstruction at component }a=Q_a.              \tag{4}
\]
For completeness, put \(q(x_1,x_2)=x_1x_2\).  The polarization identity is
\[
              q(x+y)+q(x)+q(y)=B(x,y).                \tag{5}
\]
The parity of any one of the four colours at \(a\) is
\[
 \sum_{\pi_i=a}\bigl(q(r_{i-1})+q(r_i)\bigr);
\]
the constant and linear terms vanish because the degree and both flow
coordinates are even.  Write
\(r_i=r_0+\sum_{j\le i}z_j\), expand with (5), and first use (2) to
cancel the arbitrary-base term.  The remaining \(q(z_i)\)'s and the
terms with two occurrences owned by \(a\) cancel together because
\[
 0=q\left(\sum_{\pi_i=a}z_i\right)
   =\sum_{\pi_i=a}q(z_i)
    +\sum_{\substack{j<i\\\pi_j=\pi_i=a}}B(z_j,z_i).
\]
The terms left are precisely one copy of (3) for every \(b\ne a\).
This proves (4) without appealing to the checker.

Equivalently, contract every complement component to one vertex.
On the blocks met by the support, the support circuit becomes a fixed
Euler tour of a connected Eulerian multigraph; loops are counted twice
in incidence.  The integrated values are four edge colours.  Equation
\(Q_a=0\) says that each of the four colour classes has even degree at
the contracted vertex \(a\).  Hence a tensor solution directly cleans
the one-circuit boundary state.

The tensor model is intentionally broader than is needed: it permits
every one of the \(16\) linear functionals independently on every
pair.  More explicitly, the charge-zero derivative sequence
\[
                 (b,x),(a,y),(b,x),(a,y)
\]
contributes \(B(L_bx,L_ay)=B(L_a^{-1}L_bx,y)\): three identical
ordered cross-pairs occur, hence one remains modulo two.  These are
the rank-one functionals of the matrix \(L_a^{-1}L_b\).  Every
functional on the four-dimensional matrix space is a sum of at most
two such rank-one functionals, and concatenating the gadgets introduces
no cross terms because each gadget has zero charge in both blocks.
Consequently the universal theorem
implies direct cleaning for every one-support-circuit state, without a
bound on the circuit length, number of complement components, or
component degrees.

The same argument gives a slightly stronger useful corollary.  Suppose
there are several support circuits and, on every circuit separately,
every complement block has derivative sum zero:
\[
                    \bigoplus_{\substack{i\in D\\\pi_i=a}}d_i=0
                    \qquad(a\in V,\ D\text{ a support circuit}).
\]
Then every tuple of component maps is integrable on every circuit,
because
\[
 \bigoplus_{i\in D}L_{\pi_i}d_i
 =\bigoplus_{a\in V}L_a
   \left(\bigoplus_{\substack{i\in D\\\pi_i=a}}d_i\right)=0.
\]
Apply the cross-pair
calculation separately to the circuits and xor their pair functionals.
The total obstruction at a block is the degree parity for this summed
tensor family, so the universal theorem again gives a direct cleaning.
There is no conflict from sharing the maps \(L_a\) across circuits:
the theorem is applied once to the sum of all their functionals.
Independent circuit base values and translations disappear from the
calculation because the block charge is zero on each circuit.

## 3. Universal tensor proof

Regard functions \({\cal G}\to\mathbb F_2\) as a six-dimensional
vector space.  Identify
\(1=(1,0)\), \(2=(0,1)\), and \(3=(1,1)\), and order the six maps as
\[
\begin{split}
 &(0123),(0132),(0213),\\
 &(0231),(0312),(0321),
\end{split}
\]
where the string records the images of \(0,1,2,3\).  Define the linear
functional
\[
 \lambda(f)=f(0132)+f(0213)+f(0321).                    \tag{6}
\]
It has the two crucial properties
\[
 \lambda(1)=1,\qquad
 \lambda(M\mapsto M_{ij})=0\quad(1\le i,j\le2).         \tag{7}
\]
The first equality holds because (6) has three summands.  In
column-major order, the flattened matrices of the three maps in (6)
are
\[
 (1,0,1,1),\quad(0,1,1,0),\quad(1,1,0,1),
\]
whose sum is zero.  This proves (7) by inspection.

For a fixed tensor instance, define the Boolean function
\[
                 F((L_a)_{a\in V})
                    =\prod_{a\in V}(1+Q_a).             \tag{8}
\]
It is the indicator of the desired map assignments.  We prove that it
is not the zero function.

Expand every factor of (8).  An expansion choice \(f\) assigns to each
vertex either no edge or one incident edge.  Its term is the product
of the corresponding edge functions \(w_e\).  Since these are
\(\mathbb F_2\)-valued functions, \(w_e^2=w_e\).  Thus terms can be
grouped, including choices in which both endpoints selected the same
edge, by the simple graph \(H_f\) consisting of the distinct chosen
edges.

Apply \(\Lambda=\lambda^{\otimes V}\) to (8).  If a nonempty \(H_f\)
has a vertex of degree one, its grouped monomial depends on the local
map at that vertex through one linear coordinate function.  Indeed
\(w_{ab}=\phi_{ab}(L_a^{-1}L_b)\) is linear in either endpoint map
when the other is fixed: multiplication is linear, and on
\({\cal G}\)
\[
 \begin{pmatrix}p&q\\r&s\end{pmatrix}^{-1}
 =\begin{pmatrix}s&q\\r&p\end{pmatrix}.                 \tag{9}
\]
Equation (7) therefore kills that monomial.

It remains to calculate the coefficient of a graph \(H\) having no
degree-one vertex.  For any expansion choice producing \(H\), let
\(S\) be the vertices at which it selected an edge.  Covering every
edge of \(H\), with one choice per vertex of \(S\), gives
\[
                 |E(H)|\le |S|\le |V(H)|.
\]
Minimum degree at least two gives \(|E(H)|\ge|V(H)|\).
Consequently equality holds throughout: \(H\) is a disjoint union of
cycles, every vertex selects an edge, and every edge is selected
exactly once.  On each cycle there are exactly two such selections,
the two cyclic orientations.  Hence a nonempty union of cycles has
coefficient \(2^{c(H)}=0\) in \(\mathbb F_2\).

Every nonconstant grouped term is therefore killed or cancels.  The
constant term gives
\[
                         \Lambda(F)=\lambda(1)^{|V|}=1.
\]
So \(F\) is nonzero, proving the theorem.

## 4. Exact finite negation and SAT cross-check

A tensor countermodel has four Boolean coefficient variables for every
pair \(ab\).  These specify an arbitrary linear functional on a
four-dimensional matrix space.  Common left multiplication of all
\(L_a\)'s leaves every relative matrix unchanged, so the checker fixes
\(L_0=I\) and enumerates the remaining \(6^{|V|-1}\) map assignments.

For each map assignment it evaluates every \(w_{ab}\) by XOR gates,
forms every degree parity \(Q_a\) by XOR gates, and adds the clause
\[
                         \bigvee_{a\in V}Q_a.           \tag{10}
\]
The conjunction of (10) over all map assignments is exactly the
negation of the theorem: it asks for one tensor family that defeats
every map assignment.

CaDiCaL returns UNSAT for \(3,4,5\) vertices.  It emits a DRAT proof
and checks that proof internally in the same executable.  This is a
proof-producing check, but not an independently implemented proof
checker.  The generator is deterministic and retains the generated
CNF, proof, and solver result so that an external DRAT checker can audit
the artifacts.

## 5. Scope and isotropic-system warning

Bouchet's Eulerian-vector theorem for isotropic systems is suggestive
but is not used here.  A direct identification of solvable anchor
assignments with Eulerian vectors of one fixed isotropic system is
false: the coordinate-fibre parity forced by an isotropic system does
not match the exact small boundary census.  Any future use of that
theory needs an augmentation or projection and a separately proved
obstruction identity.

The theorem proves universal direct cleaning when the support is one
circuit, and also in the circuitwise-balanced several-circuit case
stated above.  A general minimum projection can have several support
circuits with charges that cancel only after the circuits are combined.
Then arbitrary component maps need not preserve circuit integrability,
so the cross-pair reduction does not apply.  Therefore this does not
resolve FiveCDC.

Before the universal proof was found, an ordinary-CNF \(k=6\) attempt
was stopped because the solver reached
about 60 GB of resident memory.  Its partial proof file is not a
certificate and is deliberately excluded from this package's checksum
ledger.  A deterministic heuristic search found no countermodel; its
best sampled tensor family still had 120 clean relative-map
assignments.  These exploratory computations are not used in the
universal proof.

OpenAI Codex agents under human direction derived the tensor reduction,
found and corrected an initial variadic-XOR implementation error, and
wrote the SAT generator and this proof.  The argument and certificates
await independent human review.
