# Exact algebra for compressing Oum's eight-cover to five coordinates

Date: **2026-07-28**

Status: **EXACT EQUIVALENCE AND MINIMUM SUPPLIED-COVER
COUNTERMODEL / NOT A FIVECDC RESOLUTION**.

## 1. The Oum cover

Let \(G\) be a loopless cubic graph and
\[
                  \phi:E(G)\longrightarrow\Gamma-\{0\},
                  \qquad \Gamma=\mathbf F_2^3,
\]
be a flow.  Thus the three incident values at every vertex xor to
zero.

For every incident vertex-edge pair \((v,e)\), choose one of the
other two incident edges \(f_{v,e}\), and put
\[
                         c_{v,e}=\phi(f_{v,e}).
\]
Changing this choice adds \(\phi(e)\).  For \(e=uv\), define
\[
                         d_e=c_{u,e}+c_{v,e}.
\]
Oum's affine potential system is
\[
             t_u+t_v\in d_e+\langle\phi(e)\rangle
             \qquad(e=uv).                                    \tag{1}
\]
The existence of a solution is the flow-lifting lemma in Sang-il
Oum's exposition,
[*A proof of the cycle double cover conjecture by OpenAI: An
exposition*](https://arxiv.org/abs/2607.16356), arXiv:2607.16356v2.

Given a solution \(t=(t_v)\), put
\[
 x_e=t_u+c_{u,e},\qquad
 P_e=\{x_e,x_e+\phi(e)\}.                                      \tag{2}
\]
Equation (1) says that the same unordered pair is obtained at the
other endpoint.  The eight coordinate classes
\[
                         H_s=\{e:s\in P_e\},
                         \qquad s\in\Gamma,
\]
are Eulerian and cover every edge exactly twice.

Everything below concerns this standard, non-orientable Eulerian
edge-subset cover.

## 2. The exact five-coordinate compression system

Assign a column
\[
                         a_s\in\mathbf F_2^5
                         \qquad(s\in\Gamma)
\]
to each of the eight old coordinates.  On an edge with
\(P_e=\{x,y\}\), define
\[
                              q(e)=a_x+a_y.                    \tag{3}
\]

> **Compression criterion.**  The Oum cover associated with
> \((\phi,t)\) has a binary coordinate-linear compression to a
> five-cycle double cover if and only if there are eight columns
> \(a_s\in\mathbf F_2^5\) satisfying
> \[
>                 \operatorname{wt}
>                 (a_{x_e}+a_{x_e+\phi(e)})=2
>                 \qquad(e\in E(G)).                           \tag{4}
> \]

Here "coordinate-linear" means a binary linear map from the old
coordinate-incidence space \(\mathbf F_2^8\) to
\(\mathbf F_2^5\); its eight columns are the \(a_s\).

To prove sufficiency, let the incident flow values at a vertex be
\(\alpha,\beta,\gamma\), with
\(\alpha+\beta+\gamma=0\).  The three old pair labels are
\[
\{t+\beta,t+\gamma\},\quad
\{t+\alpha,t+\gamma\},\quad
\{t+\alpha,t+\beta\}.
\]
After (3), their xor is zero because every column occurs twice.
Condition (4) says every new edge label has weight two.  Therefore
the five coordinate classes of \(q\) are Eulerian and cover each edge
exactly twice.  Necessity is simply the column description of any
binary linear map.

Thus the exact direct route from Oum's theorem is the mixed system
\[
\boxed{
\begin{aligned}
t_u+t_v&\in d_e+\langle\phi(e)\rangle,\\
\operatorname{wt}\!\left(
a_{t_u+c_{u,e}}+a_{t_u+c_{u,e}+\phi(e)}
\right)&=2
\end{aligned}
\qquad(e=uv).}                                                  \tag{5}
\]
The first line is affine over \(\mathbf F_2\).  The second is the
genuinely additional nonlinear condition not supplied by the
eight-cover theorem.

## 3. Co-occurrence graph formulation

Let \(J(\phi,t)\) be the simple graph on \(\Gamma\) whose edges are
the distinct pairs \(P_e\).  Let \(R_5\) be the graph on
\(\mathbf F_2^5\) in which two words are adjacent when their Hamming
distance is two.  Then (4) is exactly
\[
                         J(\phi,t)\longrightarrow R_5.         \tag{6}
\]
Indeed, \(s\mapsto a_s\) is the required homomorphism.

Pure merging is the special case in which all \(a_s\) are chosen
from a fixed five-clique of \(R_5\).  Such a clique is
\[
                    0,\ 12,\ 13,\ 14,\ 15,
\]
where a pair denotes its weight-two incidence word.  Consequently
\[
                         \chi(J)\le5
                  \quad\Longrightarrow\quad
                         J\longrightarrow R_5.                 \tag{7}
\]

The clique number of \(R_5\) is exactly five.  Translate a clique so
that it contains \(0\).  Every other word then has weight two, and
their supports are pairwise-intersecting two-subsets of \([5]\).
If they have a common point, at most four form a star.  Otherwise,
after taking \(12,13\), a member avoiding \(1\) must be \(23\), and
no fourth two-subset meets all three.  Hence there are at most four
nonzero words.  The displayed star attains the bound.

In particular,
\[
                              K_6\nrightarrow R_5.             \tag{8}
\]

## 4. A still narrower affine map is impossible

One might require the columns to respect the affine structure of
\(\Gamma\):
\[
                              a_s=As+b,
             \qquad A:\mathbf F_2^3\to\mathbf F_2^5\text{ linear}.  \tag{9}
\]
Then the common translate cancels and
\[
                              q(e)=A\phi(e).                   \tag{10}
\]
If \(\phi\) uses all seven nonzero values, this is impossible.

For each nonzero row of \(A\), the corresponding linear functional is
one on exactly four nonzero elements of \(\mathbf F_2^3\).  Therefore
\[
                   \sum_{z\ne0}\operatorname{wt}(Az)
\]
is divisible by four.  If every \(Az\) had weight two, the same sum
would be \(7\cdot2=14\), a contradiction.

So Oum's eight-cover cannot be universally reduced by an affine map of
the Fano coordinate space.  The arbitrary eight columns in (5) are
essentially more general.

## 5. Minimum supplied-cover obstruction on Petersen

Take the following ten triples on coordinates \(0,\ldots,5\):
\[
\begin{array}{ccccc}
012&013&024&035&045\\
125&134&145&234&235.
\end{array}                                                     \tag{11}
\]
Every pair of coordinates occurs in exactly two triples.  Make the
triples the graph vertices.  Join two vertices when their triples
share a pair, and label that graph edge by the shared pair.

The resulting graph is simple, cubic, connected, has girth five, and
has graph6 encoding
```text
IqMA?[aDG
```
It is the Petersen graph.  Its fifteen edge labels are all pairs of
the six coordinates:
\[
                         E(J)=\binom{\{0,\ldots,5\}}2.
\]
Thus its supplied-cover co-occurrence graph is \(K_6\).

At a triple \(abc\), the incident labels are \(ab,ac,bc\), so every
coordinate has even local incidence.  These labels are therefore an
eight-coordinate cycle double cover, with coordinates \(6,7\) empty.

It is also literally an Oum cover.  Put
\[
                         \phi(e)=a+b
\]
on an edge labelled \(ab\), and put
\[
                         t_{abc}=a+b+c
\]
at the vertex \(abc\).  For the edge \(ab\) at that vertex, Oum's
formula gives
\[
 \{t_{abc}+(a+c),t_{abc}+(b+c)\}=\{b,a\}.
\]
The flow uses all seven nonzero values.

By (8), this supplied Oum cover has no binary coordinate-linear
compression to five coordinates.  It also has no affine compression
of the form (9).

This is minimum vertex order for such a supplied-cover obstruction
among loopless cubic graphs.  If a co-occurrence graph \(J\) does not
map to \(R_5\), (7) gives \(\chi(J)\ge6\).  Take a 6-critical subgraph
\(F\).  Every vertex of \(F\) has degree at least five: otherwise a
5-colouring of \(F-v\) extends to \(v\).  Hence
\[
                         |E(J)|\ge|E(F)|\ge15.
\]
Every distinct co-occurrence pair labels at least one graph edge.  A
cubic graph on \(n\) vertices has \(3n/2\) edges, so
\[
                              3n/2\ge15,\qquad n\ge10.
\]
Construction (11) attains equality.

This is a supplied-cover obstruction, not a Petersen-graph obstruction.
For the same fixed flow, the gauged affine system (1) has four
solutions:
\[
\begin{split}
&(0,1,5,5,2,5,5,3,6,7),\\
&(0,1,7,6,4,6,7,4,4,4),\\
&(0,0,5,4,6,5,4,7,0,0),\\
&(0,0,7,7,0,6,6,0,2,3).
\end{split}
\]
The first gives the displayed \(K_6\); the other three give a
\(K_5\).  Thus changing the Oum potential repairs this particular
flow.

## 6. A fixed-flow affine-potential obstruction

Potential flexibility is not universally sufficient.  Consider the
12-vertex graph
```text
K??FEaKR@oE_
```
with edge order
\[
\begin{split}
 &(0,6),(0,7),(0,8),(1,6),(1,7),(1,9),\\
 &(2,6),(2,10),(2,11),(3,7),(3,10),(3,11),\\
 &(4,8),(4,9),(4,10),(5,8),(5,9),(5,11)
\end{split}
\]
and flow values
```text
1 2 3 4 7 3 5 3 6 5 7 2 5 1 4 6 2 4
```
in that order.

With the translation gauge \(t_0=0\), system (1) has exactly one
solution:
```text
0 5 5 1 5 6 7 4 7 3 7 2
```
Every ungauged solution is obtained by adding one common element of
\(\Gamma\) to all twelve potentials: this operation leaves (1)
unchanged, and merely translates all eight coordinate names.
Its eighteen Oum labels are
```text
23 13 12 26 16 12 36 03 06 36 34 46 14 01 04 24 02 04
```
and their distinct pairs are precisely all fifteen pairs on
\[
                              \{0,1,2,3,4,6\}.
\]
Thus every compatible potential, including its seven global
translations, has co-occurrence graph containing \(K_6\).  By (8),
the complete mixed direct-compression system (5) is UNSAT for this
fixed \(\phi\).

This still is not a graph counterexample.  It rules out only:

1. this fixed nowhere-zero \(\mathbf F_2^3\)-flow;
2. direct choice of an Oum-compatible potential for that flow; and
3. binary linear compression of the resulting eight Eulerian
   coordinates.

It does not rule out another flow, a flow switch followed by new
potentials, an edge-dependent nonlinear recolouring, or an unrelated
five-cycle double cover.

## 7. Reproduction

```text
python3 scratch/check_oum_eight_to_five_compression_obstructions.py
```

The standalone standard-library checker verifies:

- the ten-block design and Petersen graph;
- the local parity equations and exact Oum reconstruction;
- all four gauged Petersen potentials;
- all \(2^{15}\) affine maps \(A:\mathbf F_2^3\to\mathbf F_2^5\);
- \(\omega(R_5)=5\) by exact clique search;
- simplicity, cubicity, connectedness, and bridgelessness of both
  displayed graphs;
- the 12-vertex flow equations;
- all \(2^{11}\) spanning-tree potential choices, leaving the unique
  displayed solution; and
- the two \(K_6\) co-occurrence certificates.

Expected output:
```text
PASS: exact Oum compression system controls; no affine all-seven map; omega(R5)=5; minimum-order Petersen supplied K6 obstruction; unique-potential 12-vertex fixed-flow K6
```

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the exact
compression system, found the minimum Petersen design, assembled the
fixed-flow obstruction, wrote the standalone checker, and drafted this
note.  Oum's flow-lifting theorem is cited above.  The compression
countermodels are not peer reviewed and are not presented as a
resolution of FiveCDC.
