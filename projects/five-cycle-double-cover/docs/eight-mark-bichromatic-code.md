# The bichromatic incidence code for the connected eight-mark core

Date: **2026-07-26**.

Status: **human-checkable algebraic reduction**.  This note does not prove
the eight-mark closure and does not resolve the five-cycle double cover
conjecture.  It identifies exactly which part of the problem is linear,
gives an exact signed-graph test for the remaining component condition,
and records how neutral \(\mathbb F_2^2\)-switches move between the
resulting incidence objects.

## 1. Setup and the incidence multigraph

Let \(H\) be a connected simple cubic graph with a proper edge-colouring
\[
 \kappa:E(H)\longrightarrow\{a,b,c\}.
\]
Let \(S\) be a universally separated matching of eight edges.  By the
mark-precolouring lemma in `extremal-marked-core-reduction.md`, the
colouring may be chosen so that every edge of \(S\) has colour \(c\).

Write
\[
 {\cal A}=\pi_0(H[a,c]),\qquad {\cal B}=\pi_0(H[b,c]).
\]
Every member of \({\cal A}\) or \({\cal B}\) is an even circuit.  Define
the **bichromatic incidence multigraph**
\[
 \Gamma=\Gamma(H,\kappa)
\]
as follows:

- its bipartition is \({\cal A}\sqcup{\cal B}\);
- its edge set is the set \(E_c\) of \(c\)-coloured edges of \(H\); and
- a \(c\)-edge \(e\) joins the unique \(ac\)-circuit \(A(e)\) and the
  unique \(bc\)-circuit \(B(e)\) containing it.

Thus \(\Gamma\) is bipartite and loopless, but it can have parallel
edges even though \(H\) is simple.

### Lemma 1.1

\(\Gamma\) is connected.  Moreover,
\[
 \deg_\Gamma(A)=\frac{|E(A)|}{2},\qquad
 \deg_\Gamma(B)=\frac{|E(B)|}{2}.
                                                        \tag{1}
\]
In particular, if \(H\) has girth at least ten, then
\(\delta(\Gamma)\ge5\).  The marked set \(S\), regarded as a subset of
\(E(\Gamma)\), is a matching in \(\Gamma\).

### Proof

Associate to every vertex of \(H\) its incident \(c\)-edge.  Traversing
an \(a\)-edge in \(H\) moves between two \(c\)-edges incident with one
vertex of \({\cal A}\); traversing a \(b\)-edge does the analogous thing
at a vertex of \({\cal B}\); traversing a \(c\)-edge does not change the
associated edge of \(\Gamma\).  A path in \(H\) therefore gives a walk
in \(\Gamma\).  Connectedness of \(H\) gives connectedness of
\(\Gamma\).

An \(ac\)-circuit alternates \(a\)- and \(c\)-edges, proving the first
formula in (1); the other formula is identical.  The girth conclusion
follows.  Finally, two marked \(c\)-edges incident with the same
\({\cal A}\)-vertex would lie on one \(ac\)-circuit, and two incident
with the same \({\cal B}\)-vertex would lie on one \(bc\)-circuit.
Either event contradicts separation in the chosen colouring.
\(\square\)

Universal separation is stronger than the last matching condition: it
requires the analogous condition after every proper three-edge-colouring,
not merely in the one currently represented by \(\Gamma\).

## 2. The exact linear projection

Choose bits
\[
 x_A\in\mathbb F_2\quad(A\in{\cal A}),\qquad
 y_B\in\mathbb F_2\quad(B\in{\cal B})
\]
and put \(z=(x,y)\in\mathbb F_2^{V(\Gamma)}\).  Let
\(\Phi(z)\) be the symmetric difference of the selected bichromatic
circuits:
\[
 \Phi(z)=
 \mathop{\triangle}_{x_A=1} E(A)
 \mathbin\triangle
 \mathop{\triangle}_{y_B=1} E(B).
                                                        \tag{2}
\]
Its edge indicators are exactly
\[
 1_{\Phi(z)}(e)=
 \begin{cases}
  x_{A(e)},&\kappa(e)=a,\\
  y_{B(e)},&\kappa(e)=b,\\
  x_{A(e)}+y_{B(e)},&\kappa(e)=c.
 \end{cases}                                           \tag{3}
\]
At a vertex of \(H\), if \(p=x_{A(e_c)}\) and
\(q=y_{B(e_c)}\) for its incident \(c\)-edge \(e_c\), the local states
are
\[
\begin{array}{c|c}
(p,q)&\hbox{edges of \(\Phi(z)\) at the vertex}\\ \hline
(0,0)&\varnothing\\
(1,0)&a,c\\
(0,1)&b,c\\
(1,1)&a,b .
\end{array}                                             \tag{4}
\]
Thus every vertex has degree zero or two in \(\Phi(z)\).  In particular,
\(\Phi(z)\) is a binary cycle and every nontrivial component is a
circuit.

### Proposition 2.1 (incidence-code theorem)

The map
\[
 \Phi:\mathbb F_2^{V(\Gamma)}
       \longrightarrow Z_1(H;\mathbb F_2)
                                                        \tag{5}
\]
is linear and injective.  Its image is exactly the binary cycles
obtainable as symmetric differences of \(ac\)- and \(bc\)-circuits.
On the \(c\)-edges,
\[
 \Phi(z)|_{E_c}=B_\Gamma^{\,T}z=1_{\delta_\Gamma(U_z)},
                                                        \tag{6}
\]
where \(B_\Gamma\) is the binary vertex-edge incidence matrix and
\(U_z=\{v:z_v=1\}\).

If two members of the image have the same \(c\)-edge trace, their
selectors differ by either \(0\) or the all-one vector.  More explicitly,
\[
 \Phi(z+\mathbf1)=\Phi(z)\mathbin\triangle H[a,b].
                                                        \tag{7}
\]

### Proof

Equations (2)--(3) prove linearity and characterize the image.  If
\(\Phi(z)=0\), an \(a\)-edge on each \(A\in{\cal A}\) forces \(x_A=0\),
and a \(b\)-edge on each \(B\in{\cal B}\) forces \(y_B=0\).  Hence
\(\Phi\) is injective.  Equation (6) is the definition of the incidence
matrix.  Since \(\Gamma\) is connected, the kernel of
\(B_\Gamma^{\,T}\) consists of \(0\) and \(\mathbf1\).  Substituting
\((1,1)\) in the last row of (4) proves (7).
\(\square\)

### Corollary 2.2 (the eight mark equations)

All eight marked edges belong to \(\Phi(z)\) exactly when
\[
 x_{A(e)}+y_{B(e)}=1\qquad(e\in S).                    \tag{8}
\]
Because \(S\) is a matching in \(\Gamma\), these eight equations have
disjoint pairs of variables and rank eight.  Their solution set
\[
 {\cal Z}_S=\{z:S\subseteq\delta_\Gamma(U_z)\}          \tag{9}
\]
is a nonempty affine space of dimension
\[
 |V(\Gamma)|-8.                                        \tag{10}
\]
Complementary selectors \(z,z+\mathbf1\) give the same marked
\(c\)-edge trace and the two cycles in (7).  A search can therefore
inspect \(2^{|V(\Gamma)|-9}\) complementary pairs rather than arbitrary
subsets of all bichromatic circuits.

Equation (8) is the complete **linear** part of the eight-mark problem.
It ensures that every mark is present and, since \(|S|=8\), that the
total number of present marks is even.  It says nothing about how those
eight marks are divided among the circuit components of \(\Phi(z)\).

## 3. The missing topology is signed balance

Put
\[
 s_e=\begin{cases}1,&e\in S,\\0,&e\notin S.\end{cases}
                                                        \tag{11}
\]
For \(z\in{\cal Z}_S\), write \(Q_z=H[\Phi(z)]\), omitting its isolated
vertices.

### Theorem 3.1 (five equivalent exact tests)

For a fixed \(z\in{\cal Z}_S\), the following are equivalent.

1. Every circuit component of \(Q_z\) contains an even number of marks.
2. For every component \(K\) of \(Q_z\),
   \[
    \sum_{e\in E(K)}s_e=0\pmod2.                        \tag{12}
   \]
3. There is a vertex potential \(h:V(H)\to\mathbb F_2\) such that
   \[
    h(u)+h(v)=s_{uv}\qquad(uv\in E(Q_z)).               \tag{13}
   \]
4. The signed graph obtained from \(Q_z\) by declaring precisely the
   marked edges negative is balanced.
5. Give every edge of \(Q_z\) the \(\mathbb F_2\)-voltage \(s_e\).  In
   the derived two-cover, each circuit of \(Q_z\) lifts to two circuits,
   rather than one circuit of twice the length.

### Proof

The equivalence of 1 and 2 is the definition.  Summing (13) around a
circuit cancels every vertex potential twice and gives (12).  Conversely,
if (12) holds, choose \(h\) arbitrarily at one vertex of each circuit
and propagate it using (13); returning to the initial vertex is
consistent exactly because the sum in (12) is zero.  This is the usual
potential characterization of a balanced signed graph.  In a derived
\(\mathbb F_2\)-voltage cover, a closed walk closes in its original
sheet precisely when its total voltage is zero, proving the last
equivalence.
\(\square\)

Thus the componentwise condition is a cohomology condition:
\[
 [s|_{Q_z}]=0\quad\hbox{in }H^1(Q_z;\mathbb F_2).       \tag{14}
\]
For a **fixed** \(Q_z\), the accepted sign patterns form the cut-space
code \(B^1(Q_z;\mathbb F_2)\).  It is a completely linear test.

When \(z\) is also unknown, however, the edge set on which (13) must
hold changes with \(z\).  Combining (3) and (13) gives the exact
quadratic system
\[
\begin{aligned}
 x_{A(e)}\bigl(h(u)+h(v)\bigr)&=0
       &&(e=uv\hbox{ of colour }a),\\
 y_{B(e)}\bigl(h(u)+h(v)\bigr)&=0
       &&(e=uv\hbox{ of colour }b),\\
 \bigl(x_{A(e)}+y_{B(e)}\bigr)
 \bigl(h(u)+h(v)+s_e\bigr)&=0
       &&(e=uv\hbox{ of colour }c),\\
 x_{A(e)}+y_{B(e)}&=1
       &&(e\in S).
\end{aligned}                                          \tag{15}
\]
All equations are over \(\mathbb F_2\).  This is simultaneously:

- an exact signed-graph or voltage-graph formulation;
- an exact homomorphism/potential formulation after \(z\) is fixed; and
- a small XOR-plus-Boolean-implication encoding for SAT.

It is not a pure linear code in the selector variables.  Introducing
product variables can linearize the displayed polynomials syntactically,
but enforcing that those variables really are products restores the
nonlinear constraints.

A useful immediate sufficient condition is:

> If some \(z\in{\cal Z}_S\) makes \(Q_z\) connected, then \(Q_z\)
> satisfies the target condition, because its unique circuit contains
> all eight marks.

The converse is false: a valid \(Q_z\) may have several components, each
containing zero, two, four, six, or eight marks.

## 4. Why the incidence multigraph needs transition data

The plain multigraph \(\Gamma\) determines the membership formula (3),
but not the circuit components of \(Q_z\).  To recover them one must also
remember how the \(c\)-edges occur around every bichromatic circuit and
how their two ends are aligned.

One exact decoration is the following signed rotation datum.  Give the
edges incident with each \(A\in{\cal A}\) a cyclic order \(\rho_A\), and
those incident with each \(B\in{\cal B}\) a cyclic order \(\rho_B\).
For every \(e\in E(\Gamma)\), create two ports \(e^0,e^1\) and record a
bit \(\tau_e\).  After orienting the bichromatic circuits, the coloured
graph is reconstructed by
\[
\begin{array}{rcl}
c\hbox{-edge}&:& e^0e^1,\\
a\hbox{-edge}&:& e^1(\rho_Ae)^0,\\
b\hbox{-edge}&:&
 e^{\,1-\tau_e}(\rho_Be)^{\,\tau_{\rho_Be}}.
\end{array}                                             \tag{16}
\]
Reversing a chosen circuit orientation changes the presentation but not
the reconstructed coloured graph.  Formula (16), followed by the local
table (4), traces every component of \(Q_z\) and its mark parity without
reference to any SAT solver.  This is the precise signed/ribbon-state
version of the incidence object.

Equivalently, put a transition at every port joining the two selected
incident edges from (4).  The orbits of the resulting transition
permutation are the two orientations of the circuit components of
\(Q_z\); the XOR of \(s_e\) on either oriented orbit is the parity in
(12).

## 5. A small explicit nonlinearity witness

The following example is deliberately smaller than the eight-mark target.
Its purpose is to prove that the component test cannot be replaced by
linear equations in \(z\).

Let \(H\) be the connected simple cubic graph with graph6 string

```text
K??FEagT@WB_
```

and the following proper edge-colouring:
\[
\begin{array}{c|l}
c&06,\ 17,\ 28,\ 39,\ 4\,10,\ 5\,11\\
a&07,\ 16,\ 2\,10,\ 3\,11,\ 48,\ 59\\
b&08,\ 19,\ 26,\ 37,\ 4\,11,\ 5\,10 .
\end{array}                                             \tag{17}
\]
The bichromatic circuits have vertex sets
\[
\begin{array}{c|ccc}
{\cal A}&A_0=\{0,1,6,7\}&A_1=\{2,4,8,10\}&
A_2=\{3,5,9,11\}\\
{\cal B}&B_0=\{0,2,6,8\}&B_1=\{1,3,7,9\}&
B_2=\{4,5,10,11\}.
\end{array}                                             \tag{18}
\]
Consequently \(\Gamma\) is the six-cycle with edges
\[
\begin{array}{c|cccccc}
c\hbox{-edge}&06&17&28&39&4\,10&5\,11\\
\Gamma\hbox{-ends}&A_0B_0&A_0B_1&A_1B_0&A_2B_1&
A_1B_2&A_2B_2 .
\end{array}                                             \tag{19}
\]
Take the two marked edges
\[
 S=\{06,39\}.
\]
They form a matching in this \(\Gamma\).  In the coordinate order
\((x_0,x_1,x_2,y_0,y_1,y_2)\), consider
\[
\begin{array}{c|c|c}
z&\hbox{nontrivial component edge sets}&
 \hbox{mark counts}\\ \hline
(1,0,0,0,1,0)&
\{06,07,16,19,37,39\}&(2)\\
(1,1,0,0,1,0)&
\{06,07,16,19,37,39\},\
\{28,2\,10,48,4\,10\}&(2,0)\\
(0,1,1,1,0,1)&
\{06,08,26,2\,10,39,3\,11,48,4\,11,59,5\,10\}&(2)\\
(0,0,1,1,0,1)&
\{06,08,26,28\},\
\{39,3\,11,4\,10,4\,11,59,5\,10\}&(1,1).
\end{array}                                             \tag{20}
\]
All four selectors satisfy the two mark equations (8).  The first three
are good and their affine sum is the fourth:
\[
 (1,0,0,0,1,0)+(1,1,0,0,1,0)+(0,1,1,1,0,1)
 =(0,0,1,1,0,1).                                       \tag{21}
\]
The fourth is bad.  Therefore the good selectors inside the affine
all-mark space are not an affine subspace.  In particular, no system of
linear equations in \(z\), even with existentially quantified linear
auxiliary variables, describes the exact component condition: a linear
projection of an affine space would again be affine.

This is only an algebraic obstruction.  The displayed two marks are not
universally separated.  Section 6 shows exactly how a neutral switch
detects that failure.

## 6. Neutral \(\mathbb F_2^2\)-switches

Identify \(a,b,c\) with the three nonzero elements of
\(\mathbb F_2^2\), with \(a+b=c\).  If \(R\) is a binary cycle and
\(t\ne0\), the switch
\[
 \kappa'(e)=
 \begin{cases}
  \kappa(e)+t,&e\in R,\\
  \kappa(e),&e\notin R
 \end{cases}                                            \tag{22}
\]
is nowhere-zero exactly when \(R\) contains no \(t\)-coloured edge.
In a cubic properly three-edge-coloured graph, the other two colours
form disjoint circuits.  Evenness at each vertex proves:

### Lemma 6.1

Every neutral \(\mathbb F_2^2\)-cycle switch is a simultaneous Kempe
interchange on a collection of whole bichromatic circuits, and every
such interchange is neutral.

Within the fixed incidence code \(\operatorname{im}\Phi\), equations
(3) give a sharper description:

- \(\Phi(x,y)\) avoids colour \(a\) exactly when \(x=0\), so it is a
  union of \(bc\)-circuits and can be switched by \(a\);
- it avoids colour \(b\) exactly when \(y=0\), so it is a union of
  \(ac\)-circuits and can be switched by \(b\); and
- it avoids colour \(c\) exactly when
  \(x_{A(e)}=y_{B(e)}\) on every edge of \(\Gamma\).  Connectedness of
  \(\Gamma\) makes \(z\) constant, so the only possibilities are the
  empty switch and the whole \(ab\)-factor
  \(\Phi(\mathbf1)=H[a,b]\).

An individual proper \(ab\)-circuit is therefore generally **outside**
the fixed incidence code.  Switching on it changes the transition
system from which \({\cal A}\), \({\cal B}\), and \(\Gamma\) are built.
More concretely:

- a switch by \(c\) on an \(ab\)-circuit leaves the \(c\)-matching
  \(E_c=E(\Gamma)\) fixed but flips the \(a/b\) transition at every
  vertex of that circuit; the old \(ac\)- and \(bc\)-circuits can merge
  or split, so the vertices and incidences of \(\Gamma\) change;
- a switch by \(b\) on an \(ac\)-circuit replaces the \(c\)-edges of
  that alternating circuit by its \(a\)-edges, so even the ground edge
  set used for the new incidence graph changes; and
- the analogous statement holds for a switch by \(a\) on a
  \(bc\)-circuit.

Hence neutral reconfiguration is a mutation of the signed rotation
datum, not addition of another selector in one fixed linear code.

For the example in Section 5, switch \(a\) and \(b\) on the \(ab\)-circuit
\[
 07,08,37,3\,11,48,4\,11.                              \tag{23}
\]
The \(c\)-edges remain fixed, but the three old \(ac\)-circuits merge
into one and the three old \(bc\)-circuits merge into one.  The new
incidence multigraph has two vertices joined by all six \(c\)-edges, so
the two marks \(06\) and \(39\) are no longer separated.  The dimension
of the old incidence code is six and that of the new one is two.  This
also gives a literal demonstration that the switch is not an
automorphism of the fixed code.

Universal separation supplies a genuine extra constraint here.  If all
marks are \(c\)-coloured, then after every \(c\)-neutral \(ab\)-Kempe
switch, the marks remain \(c\)-coloured and must still form a matching
in the mutated incidence graph.  After a general neutral switch, one
may use the mark-precolouring lemma again to make all marks \(c\);
universal separation requires a matching in every incidence graph so
obtained.  This Kempe-stability is necessary.  It is not known here to
be sufficient for a good selector, and it must not be silently replaced
by the matching condition in one fixed \(\Gamma\).

## 7. Necessary and sufficient conclusions

For the connected eight-mark branch, the following statements are
**necessary**:

1. \(\Gamma\) is a connected bipartite multigraph, and \(S\) is an
   eight-edge matching in it.
2. The selector lies in the affine cut space \({\cal Z}_S\) of (9).
3. A successful selector must make the fixed sign vector \(s\) a
   coboundary on \(Q_z\), equivalently it must satisfy (15).
4. Universal separation imposes the Kempe-stability condition of
   Section 6 on every reachable signed rotation datum, and in fact on
   every Tait colouring, including other Kempe classes.

The following statement is **necessary and sufficient** for the
bichromatic-symmetric-difference route:

> There is a binary cycle obtained as a symmetric difference of selected
> \(ac\)- and \(bc\)-circuits, containing all eight marks and having an
> even number of marks on every circuit component, if and only if the
> quadratic system (15) has a solution \((x,y,h)\).

Thus the exact residual obstruction is not failure of a cut equation.
It is nontrivial signed holonomy on at least one state circuit for every
selector in \({\cal Z}_S\).  The incidence projection provides a compact
linear search space, while the signed rotation datum and potential
variables retain precisely the component topology that a plain
\(\mathbb F_2\) code forgets.

## AI-use disclosure

This formulation, its proofs, and the explicit nonlinearity witness were
developed by an OpenAI Codex agent under human direction.  The displayed
edge lists, equations, and component traces are included so that every
claim in the note can be checked without trusting the agent or any
unpublished software.
