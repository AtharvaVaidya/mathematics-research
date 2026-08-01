# Fixed-pair interlacement and the closed-cage obstruction

Date: **2026-07-28**

Status: **EXACT REDUCTION AND SHARP NO-GO FOR A FIXED-PAIR
DELTA-MATROID ARGUMENT / NOT A FIVECDC RESOLUTION**.

## 1. Fixed-pair switches as circuit partitions

Let \(G\) be a loopless cubic graph with a \(D_5\)-state
\(\ell:E(G)\to\binom{[5]}2\).  Thus the xor of the three incident
labels is zero at every vertex.  Fix \(Q=\{a,b\}\), and write
\[
 C_i=\{e:i\in\ell(e)\},\qquad
 Y_Q=C_a\mathbin\triangle C_b.
\]

At a cubic vertex the three incident labels have the form
\[
                         ij,\ ik,\ jk                         \tag{1}
\]
for three distinct coordinates \(i,j,k\).  Indeed, if two incident
weight-two vectors are \(p,q\), the third is \(p+q\); its weight is
two only when \(|p\cap q|=1\).  This also proves that the three
labels are distinct.

Consequently the edges labelled exactly \(Q\) form a matching
\(B_Q\).  At each endpoint of an edge in \(B_Q\), the other two
incident edges lie in \(Y_Q\).  Every component of \(Y_Q\) is a
circuit.

Construct a 4-regular multigraph \(F_Q\) as follows.

1. In every \(Y_Q\)-circuit incident with \(B_Q\), suppress every
   vertex not incident with \(B_Q\).
2. Contract every edge in \(B_Q\).
3. Omit a \(Y_Q\)-circuit that has no incidence with \(B_Q\).

The vertices of \(F_Q\) are the \(Q\)-labelled edges.  The omitted
circuits will be called *free*, and their number will be denoted
\(t_Q\).  Loops and parallel edges are allowed in \(F_Q\), even when
\(G\) is simple.

The circuits of \(Y_Q\) give a circuit partition \(P_0\) of \(F_Q\):
at a contracted \(Q\)-edge \(uv\), the two half-edges originally at
\(u\) are paired, as are the two originally at \(v\).

Let \(\mathcal K_Q\) be the set of \(Y_Q\)-components.  For
\(S\subseteq\mathcal K_Q\), switch \(a,b\) on precisely the
components in \(S\), and call the resulting state \(\ell_S\).  At a
vertex of \(F_Q\) coming from \(uv\in B_Q\), pair the two half-edges
whose labels in \(\ell_S\) contain \(a\), and pair the two whose
labels contain \(b\).  These transitions define a circuit partition
\(P_S\) of \(F_Q\).

Every \(C_a(\ell_S)\)- or \(C_b(\ell_S)\)-circuit that uses a
\(Q\)-labelled edge contracts to a circuit of \(P_S\), and the
converse expansion is unique.  A free \(Y_Q\)-circuit is wholly
\(a\)-coloured or wholly \(b\)-coloured and contributes one circuit
before and after every switch.  Hence
\[
       \kappa(C_a(\ell_S))+\kappa(C_b(\ell_S))
                       =t_Q+|P_S|.                            \tag{2}
\]

There is also a useful touch-graph description of the dependence on
\(S\).  The two visits of \(P_0\) at the vertex arising from \(uv\)
belong to components \(K_u,K_v\in\mathcal K_Q\), possibly equal.
The choice between the two non-\(P_0\) transitions in \(P_S\)
depends only on
\[
                     1_{K_u\in S}+1_{K_v\in S}\pmod2.          \tag{3}
\]
Thus the switch vector enters the transition system through the cut
of \(S\) in the touch-graph of \(P_0\).

## 2. Exact principal-submatrix formula

We use one imported theorem.

> **Extended Cohn--Lempel equality** (Traldi, 2009).  Let \(F\) be
> an undirected 4-regular multigraph, \(E\) an Euler system (one
> oriented Euler circuit in each component), and \(P\) a circuit
> partition.  Let \(A(E)\) be the binary interlace matrix indexed by
> \(V(F)\).  Form \(M(E,P)\) by:
>
> * deleting the row and column of a vertex where \(P\) uses the
>   Euler transition;
> * retaining the row and column with diagonal \(0\) where \(P\)
>   uses the other orientation-consistent transition;
> * retaining the row and column and changing its diagonal to \(1\)
>   where \(P\) uses the orientation-inconsistent transition.
>
> Then
> \[
>                          |P|=c(F)+\nu_{\mathbf F_2}M(E,P).
> \]

This is Theorem 4 in Lorenzo Traldi,
[*Binary nullity, Euler circuits and interlace
polynomials*](https://arxiv.org/abs/0903.4405).  The statement above
includes disconnected graphs, loops, and parallel edges, exactly as
needed for \(F_Q\).

Applying it to (2) gives the promised exact translation:
\[
\boxed{\;
 \kappa(C_a(\ell_S))+\kappa(C_b(\ell_S))
 =t_Q+c(F_Q)+\nu_{\mathbf F_2}M(E,P_S).
\;}                                                               \tag{4}
\]
The matrix \(M(E,P_S)\) is a principal submatrix of the fixed
interlace matrix \(A(E)\), with selected retained diagonal entries
toggled.  Equation (3) specifies exactly how the component-switch
variables control those deletions and diagonal toggles.

A \(Q\)-switch changes only \(C_a,C_b\).  Therefore
\[
 \chi(\ell_{S\triangle\{H\}})-\chi(\ell_S)
 =
 \nu M(E,P_{S\triangle\{H\}})
 -
 \nu M(E,P_S).                                                    \tag{5}
\]
Terminality says that the right side is nonpositive for every
factor-component switch at every state in the terminal plateau;
neutrality is equality.

The exact coupling between two coordinate pairs is also elementary,
but it is not contained in one interlace matrix.  If \(R=\{u,v\}\),
\(K\) is a component of \(Y_R(q)\), and \(q'\) is obtained by the
\(R\)-switch on \(K\), then
\[
 C_u(q')=C_u(q)\triangle K,\qquad
 C_v(q')=C_v(q)\triangle K,                                    \tag{6}
\]
with all other coordinate classes unchanged.  Consequently, for
every coordinate pair \(T\),
\[
 Y_T(q')=
 \begin{cases}
  Y_T(q)\triangle K,&|T\cap R|=1,\\
  Y_T(q),&|T\cap R|\in\{0,2\}.
 \end{cases}                                                    \tag{7}
\]
Thus a switch changes exactly six of the ten factors.  If a second
switch is made on an \(H\)-component of \(Y_Q(q')\), its exact
two-step Euler change is
\[
\begin{split}
\chi(q'')-\chi(q)
={}&
\bigl[\kappa(C_u\triangle K)+\kappa(C_v\triangle K)
      -\kappa(C_u)-\kappa(C_v)\bigr]\\
&+
\bigl[\kappa(C_a(q')\triangle H)+\kappa(C_b(q')\triangle H)
      -\kappa(C_a(q'))-\kappa(C_b(q'))\bigr].                  \tag{8}
\end{split}
\]
Equations (4), (7), and (8) are a finite algebraic target for a
cross-pair proof: (4) decides the Euler balance of each move, while
(7) decides how that move rewires the marked factors used by
\(d,b^*\).  The second bracket must be evaluated in the changed
state \(q'\); replacing it by a second nullity calculation in the
original fixed-\(Q\) matrix would be invalid.

For context, a standard binary delta-matroid theorem says that for
a symmetric matrix \(A\), the set system
\[
 \mathcal M_A=\{X\subseteq V:A[X]\text{ is nonsingular}\}
\]
is a delta-matroid, and
\[
 \nu(A[X])=\min_{Z\in\mathcal M_A}|X\mathbin\triangle Z|.
\]
This is stated as the represented-set-system construction and
Theorem 8.1 in Brijder and Hoogeboom,
[*Nullity and Loop Complementation for
Delta-Matroids*](https://arxiv.org/abs/1010.4497).
It controls one principal nullity.  The next section shows why it
does not by itself supply the required exchange theorem for the
coupled fixed-pair objective.

## 3. The smallest binary closed cage

Let
\[
 A=\begin{pmatrix}
 0&1&1\\
 1&0&1\\
 1&1&0
 \end{pmatrix},
 \qquad
 D_S=\operatorname{diag}(1_S),
\]
and define
\[
                     g(S)=\nu(A+D_S)+\nu(A+D_S+I).              \tag{9}
\]
Direct binary row reduction gives
\[
g(S)=
\begin{cases}
3,&S=\varnothing\text{ or }S=\{0,1,2\},\\
1,&\text{otherwise}.
\end{cases}                                                     \tag{10}
\]
Thus the two maximum states are antipodal, and every proper
single-component switch from either one loses two units.  The
maximum family
\[
                         \{\varnothing,\{0,1,2\}\}
\]
fails symmetric exchange: from \(X=\varnothing\), \(Y=\{0,1,2\}\),
and \(e=0\), none of
\(\{0\},\{0,1\},\{0,2\}\) is a maximum.

This is smallest among loopless symmetric binary matrices.  Complete
enumeration gives:
\[
\begin{array}{c|c|c}
n&\text{loopless symmetric matrices}&
\text{matrices whose maximum family fails exchange}\\ \hline
1&1&0\\
2&2&0\\
3&8&4.
\end{array}
\]
The four order-three failures are the three labelled copies of
\(P_3\) and \(K_3\).

The matrix cage occurs in an actual simple bridgeless cubic
\(D_5\)-state.  The graph has graph6 encoding
```
K??FEagT@WB_
```
and, in the edge order
\[
\begin{split}
 &(06),(07),(08),(16),(17),(19),(26),(28),(2\,10),\\
 &(37),(39),(3\,11),(48),(4\,10),(4\,11),(59),(5\,10),(5\,11),
\end{split}
\]
the hexadecimal bit-mask labels are
```
03 05 06 05 09 0c 06 03 05 0c 09 05 05 03 06 05 06 03
```
For \(Q=02\), the three \(Y_Q\)-components are
\[
\begin{split}
H_0&=\{0,2,6,7\},\\
H_1&=\{4,5,9,10\},\\
H_2&=\{13,14,16,17\}.
\end{split}
\]
For the eight switch masks,
\[
\kappa(C_0)+\kappa(C_2)=5,3,3,3,3,3,3,5,
\]
and, exactly,
\[
       \kappa(C_0(\ell_S))+\kappa(C_2(\ell_S))=2+g(S).          \tag{11}
\]

The standalone checker also constructs the six-vertex auxiliary
4-regular graph \(F_{02}\), finds an Euler system, classifies every
transition, builds all eight modified interlace matrices, and checks
(4) directly.  Formula (11) is a smaller, special binary certificate
for the same eight circuit counts.

The state is not merely a local maximum at the displayed pair.
Exhausting its literal equal-\(\chi\) component gives 4,980 states
and 70,800 directed neutral switches, and no boundary switch of
positive \(\chi\).  Hence it is a terminal plateau.  Nevertheless,
the \(02\) face at the displayed state is a strict closed cage:
all three \(02\)-component switches have \(\Delta\chi=-2\).

This refutes any proposed proof that terminality plus a single
fixed-pair delta-matroid exchange law must make the desired
\(Q\)-component switch neutral.

## 4. The marked corner and why the universal target survives

The same state supplies a precise shortest-chain corner.  Take root
edges
\[
                             r=0,\qquad s=10.
\]
Their factor-component distance is \(d=2\).  One shortest ordered
first pair is
\[
\begin{split}
P&=03,&
C&=\{0,1,3,5,9,11,15,17\},\\
Q&=02,&
H&=\{0,2,6,7\},&
D&=\{4,5,9,10\}.
\end{split}
\]
Here \(r\in C\cap H\), \(s\in D\), and \(C\cap D\ne\varnothing\).
In one orientation from \(r\), the edge order around \(C\) is
\[
                       0,3,5,15,17,11,9,1.
\]
The first edge belonging to a \(Q\)-component other than \(H\) is
edge \(5\in D\).  Thus this eligible shortest choice has no foreign
block before \(D\), and consequently \(b^*(q;r,s)=0\).

For \(R=P\mathbin\triangle Q=23\), switching \(Q\) on \(H\) gives
the edgewise first-foreign identity
\[
                         Y_R'=Y_P\mathbin\triangle(Y_Q\setminus H).
                                                                   \tag{12}
\]
The identity follows immediately from
\(Y_R=Y_P\mathbin\triangle Y_Q\) and toggling \(H\).  It proves the
topological nonincrease of the rooted chain in this blocker-free
corner.  In the explicit state the switch indeed has
\[
                         d:2\longmapsto2,
\qquad
                         \Delta\chi=-2.
\]
It cannot be used inside the terminal plateau.

The cage is punctured by a different pair.  Switching \(04\) on
\[
                         K=\{0,1,3,4\}
\]
has \(\Delta\chi=0\) and changes the rooted distance
\[
                         d:2\longmapsto1.
\]
Formula (7) says, in particular,
\[
                  Y_{02}'=Y_{02}\triangle K.
\]
All six changed factors are
\[
                    01,\ 02,\ 03,\ 14,\ 24,\ 34.
\]
After the switch both \(Y_{01}'\) and \(Y_{34}'\) contain the two
root edges in one component.  This is the exact cross-pair
interlacement event hidden from the fixed-\(02\) nullity cube.

So the full fixed-\((d,b^*)\) exit statement succeeds immediately
on this witness, but for a reason invisible to the fixed-\(02\)
matrix.

This is the exact remaining lesson:

* (4) completely solves the fixed-pair Euler-characteristic
  bookkeeping;
* (12) completely solves the blocker-free local splice topology;
* neither theorem couples the nullity of one pair to the marked-root
  component structure of the other nine factors;
* such a cross-pair coupling is essential, already on the smallest
  matrix cage.

The universal claim that every terminal fixed-\((d,b^*)\) subplateau
has a neutral lexicographic exit is therefore neither proved nor
refuted here.  The order-12 and order-14 exhaustive censuses still
support it.  What is ruled out is the cleanest single-pair
delta-matroid proof of that claim.

## 5. Reproduction

```text
python3 scratch/check_d5_fixed_pair_interlacement_closed_cage.py
```

The checker uses only the Python standard library.  It independently
checks graph6 decoding, simplicity, cubicity, bridgelessness, all
local xor equations, the complete auxiliary circuit-nullity cube,
the order-at-most-three binary-matrix census, the 4,980-state
terminal plateau, the marked corner, and the cross-pair neutral exit.

Expected output:

```text
PASS: exact 4-regular circuit-nullity cube; smallest loopless binary cage at order 3; 4,980-state terminal plateau; marked 02 corner exits neutrally only through the checked 04 move
```

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the auxiliary
4-regular reduction, found and checked the binary cage and marked
corner, wrote the standalone replay, and drafted this note.  The two
imported theorems are attributed above.  The new synthesis and finite
claims are not peer reviewed and are not presented as a resolution of
FiveCDC.
