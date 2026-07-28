# Exact Fourier/Laplacian count for \(D_5\)-flows

## Status

The Fourier formula below is exact, including for finite multigraphs with
loops.  It was checked independently against direct flow enumeration.

The initially attractive corollary

\[
 \sum_{F\subseteq E}(-1)^{\operatorname{rank}_2 L_{G/F}}\not\equiv0
 \pmod 3
\]

is **false already for \(K_4\)**.  Thus this calculation does not resolve
the Five-Cycle Double Cover Conjecture.

## 1. The group and its Fourier transform

Put

\[
A=\{a\in\mathbb F_2^5:\textstyle\sum_i a_i=0\},\qquad
D=\{e_i+e_j:0\leq i<j<5\}.
\]

Thus \(A\) has order \(16\), and \(D\) is its set of ten weight-two
vectors.  The character group of \(A\) is

\[
B=\mathbb F_2^5/\langle{\bf1}\rangle .
\]

For \(y\in B\), choose either representative in \(\mathbb F_2^5\) and
define

\[
q(y)=\binom{\operatorname{wt}(y)}2\pmod2 .
\]

Replacing a representative of weight \(w\) by its complement of weight
\(5-w\) does not change this value, so \(q\) is well-defined.  If
\(f=1_D\), direct character summation gives

\[
\widehat f(y)
 =\sum_{0\leq i<j<5}(-1)^{y_i+y_j}
 =\frac{(5-2\operatorname{wt}(y))^2-5}{2}.
\]

Consequently the transform takes the values \(10,2,-2\), respectively
on the classes of representative weights \(0\), \(1\), and \(2\).  In
the compact form used below,

\[
\boxed{\widehat f(y)=2(-1)^{q(y)}+8\,1_{\{0\}}(y).}\tag{1}
\]

The polar form

\[
b(x,y)=q(x+y)+q(x)+q(y)
\]

is nonsingular on the four-dimensional space \(B\).  Also \(q\) has six
zeros and ten ones, hence

\[
\sum_{y\in B}(-1)^{q(y)}=-4.\tag{2}
\]

## 2. Expansion over contracted edge sets

Let \(G=(V,E)\) be a finite multigraph.  A loop is incident twice with
its vertex, so it contributes zero to the vertex xor equation and may
receive any of the ten labels in \(D\).

Let \(N_D(G)\) be the number of assignments \(z:E\to D\) whose xor at
every vertex is zero.  Character orthogonality at the vertices gives

\[
N_D(G)=16^{-|V|}
 \sum_{\phi:V\to B}\prod_{uv\in E}\widehat f(\phi(u)+\phi(v)).\tag{3}
\]

Expand (1), choosing on an edge either the quadratic-sign term or the
delta term.  For \(F\subseteq E\), all endpoints of edges in \(F\) are
identified.  Let \(H_F\) have as vertices the connected components of
the spanning subgraph \((V,F)\), and retain every edge of \(E\setminus
F\) after this identification.  Retained edges may become loops.  If
\(k(F)=|V(H_F)|\), then

\[
N_D(G)=2^{|E|}16^{-|V|}
 \sum_{F\subseteq E}4^{|F|}S(H_F),\tag{4}
\]

where

\[
S(H)=\sum_{x:V(H)\to B}
 (-1)^{\sum_{uv\in E(H)}q(x_u+x_v)}.\tag{5}
\]

Selected loops do not identify distinct vertices; they contribute the
factor \(4\).  Unselected loops contribute \(q(0)=0\).  Hence a loop
contributes \(2(1+4)=10\), exactly as it should.

## 3. The binary-Laplacian Gauss sum

Let \(L=L_H\) be the Laplacian of \(H\) over \(\mathbb F_2\): a loop
contributes zero and parallel-edge multiplicities are reduced modulo
two.  Write \(k=|V(H)|\) and \(r=\operatorname{rank}_2L\).  Expanding
\(q(x_u+x_v)\) shows that the exponent in (5) is the quadratic form

\[
Q_L(x_1,\ldots,x_k)
 =\sum_i L_{ii}q(x_i)
  +\sum_{i<j}L_{ij}b(x_i,x_j).\tag{6}
\]

Its polar form is \(L\otimes b\).  Since \(b\) is nonsingular, the
radical is \(\ker L\otimes B\), of dimension \(4(k-r)\).

It is important to check that \(Q_L\) vanishes on this radical; otherwise
the Gauss sum would be zero.  For \(t\in\ker L\) and \(a\in B\),

\[
Q_L(t\otimes a)
 =q(a)\sum_{uv\in E(H)}(t_u+t_v)
 =q(a)t^{\mathsf T}Lt=0.
\]

The restriction of a quadratic form to its polar radical is linear.
Pure tensors \(t\otimes a\) span the radical, so the displayed identity
proves that the restriction is identically zero.

It remains to determine the sign on a nondegenerate complement.
Congruence of \(L\) induces the corresponding change of variables in
(6).  A nonsingular alternating block of \(L\) is a direct sum of
matrices

\[
\begin{pmatrix}0&1\\1&0\end{pmatrix};
\]

each gives the form \(b(x,y)\), whose Gauss sum is \(16\).  A
nonsingular nonalternating block is congruent to an identity matrix;
each diagonal coordinate gives \(q(x)\), whose Gauss sum is \(-4\) by
(2).  These two cases give the same formula (the alternating rank is
even):

\[
\boxed{S(H)=(-1)^r2^{\,4k-2r}.}\tag{7}
\]

Combining (4) and (7) proves the exact integer identity

\[
\boxed{
N_D(G)=2^{|E|-4|V|}\!
\sum_{F\subseteq E}
4^{|F|}(-1)^{r(F)}2^{\,4k(F)-2r(F)},
}\tag{8}
\]

where \(r(F)=\operatorname{rank}_2L_{H_F}\).

No simplicity, connectedness, or bridgelessness assumption was used.

## 4. The mod-3 route fails

Reducing (8) modulo \(3\), all powers of \(4\) become \(1\), every power
\(2^{4k-2r}\) becomes \(1\), and \(16^{-|V|}\) becomes \(1\).  Therefore

\[
N_D(G)\equiv(-1)^{|E|}\!
\sum_{F\subseteq E}(-1)^{r(F)}\pmod3.\tag{9}
\]

Nonvanishing of the signed-rank sum would be a sufficient existence
criterion.  But for \(K_4\),

\[
\sum_{F\subseteq E(K_4)}(-1)^{r(F)}=18\equiv0\pmod3,
\qquad N_D(K_4)=180.
\]

The criterion therefore fails on the first connected bridgeless cubic
simple graph.  The complete census through order \(12\) gives residue
zero for every bridgeless cubic graph tested (1, 2, 5, 18, and 81 graphs
at orders \(4,6,8,10,12\), respectively).  This latter observation is
computational evidence only and is not needed for the \(K_4\) refutation.

## 5. Cubic nullity/bicycle form

Suppose now that \(G\) is connected and cubic, and put \(n=|V(G)|\).
Then \(n\) is even and \(|E(G)|=3n/2\).  For \(F\subseteq E(G)\), let

\[
\eta(F)=|F|-n+k(F)
\]

be the cycle nullity of the spanning subgraph \((V,F)\).  The quotient
\(H_F\) is connected.  Its binary bicycle dimension is

\[
b(H_F)=\dim\bigl(Z(H_F)\cap B(H_F)\bigr)
       =\dim\ker L_{H_F}-1
       =k(F)-1-r(F).\tag{10}
\]

For completeness, if \(M\) is the binary incidence matrix of \(H_F\),
then \(L=MM^{\mathsf T}\).  The map \(x\mapsto M^{\mathsf T}x\) sends
\(\ker L\) onto the intersection of the cut and cycle spaces, and its
kernel has dimension one because \(H_F\) is connected.  This proves
(10), including for parallel edges and loops under the usual binary
incidence convention.

The exponent of two in the \(F\)-summand of (8), including the outer
normalization, is

\[
\begin{aligned}
\frac{3n}{2}-4n+2|F|+4k(F)-2r(F)
 &=2\bigl(\eta(F)+b(H_F)+1\bigr)-\frac n2.
\end{aligned}\tag{11}
\]

Thus, if

\[
A_j(G)=
\sum_{\substack{F\subseteq E(G)\\
 \eta(F)+b(H_F)=j}}(-1)^{r(F)},
\qquad
P_G(z)=\sum_{j\geq0}A_j(G)z^j,
\]

then the exact count has the particularly short form

\[
\boxed{N_D(G)=2^{\,2-n/2}P_G(4).}\tag{12}
\]

There really are terms of degree zero: taking \(F\) to be a spanning
tree gives \(\eta(F)=0\), while \(H_F\) has one vertex and binary
Laplacian zero.  The signed sum \(A_0\), however, could in principle
cancel.

The complete bridgeless cubic simple census through order \(12\) found
no graph with \(A_0=0\).  The numbers of graphs checked at orders
\(4,6,8,10,12\) were \(1,2,5,18,81\).  This is a bounded computation,
not a proof that \(A_0\) is universally nonzero.

### Two naive valuation predictions fail

Keeping only the lowest-degree coefficient does not in general predict
the 2-adic valuation of \(N_D\).  The first census example is
\(K_{3,3}\), graph6 `EFz_`:

\[
P_G(z)=32+60z+36z^2+9z^3+z^4,\qquad
N_D(G)=\frac{P_G(4)}2=840.
\]

The \(A_0\)-term alone has valuation \(4\), while
\(v_2(N_D(G))=3\); the degree-one term has smaller valuation.

Even taking the least valuation among *all* grouped terms can
underestimate the answer when several degrees tie and cancel.  The
first canonical census example is the cube, graph6 `G?zTb_`:

\[
P_G(z)=208+420z+284z^2+83z^3+12z^4+z^5,
\qquad N_D(G)=3960.
\]

Both the degree-zero and degree-one normalized terms have valuation
\(2\), but their leading 2-adic residues cancel.  The exact valuation
is \(3\).

What survives is the standard nonarchimedean statement.  For every
nonzero coefficient define

\[
w_j=2-\frac n2+2j+v_2(A_j).
\]

Then

\[
v_2(N_D(G))\geq\min_j w_j,
\]

with equality whenever the minimum is attained at a unique degree.
This follows immediately from (12); it is exact but does not force
nonvanishing.

There is also an independent, elementary lower bound for connected
loopless cubic graphs:

\[
v_2(N_D(G))\geq2.\tag{13}
\]

Indeed \(S_5\) acts on \(D_5\)-flows by permuting coordinates.  At each
cubic vertex the three incident labels are the three edges of a
three-coordinate triangle.  Connectivity propagates fixed coordinates
from one vertex to the next.  A flow using exactly three coordinates
has stabilizer of order \(2\), permuting the two unused coordinates;
every other flow has trivial stabilizer.  Hence every orbit has size
\(60\) or \(120\), so the total count is divisible by \(60\).  This
orbit lemma is a genuine parity constraint, but of course does not
prove that the count is positive.

## 6. Reproduction

Run:

```sh
python3 scratch/audit_d5_fourier_laplacian_count.py \
  --census-max-order 10
```

For the frozen complete order-12 run (about five minutes on the audit
machine), replace `10` by `12` and optionally pass
`--skip-direct-petersen`.  Its stdout is stored in
`scratch/d5-fourier-laplacian-order12-report.txt`.

The script uses only the Python standard library, except that the census
step calls `geng` from nauty.  It independently:

1. computes all sixteen Fourier coefficients;
2. directly enumerates the Gauss sums of several small graphs, including
   a loop and parallel-edge cases;
3. compares (8) with cotree-based direct \(D_5\)-flow enumeration on
   \(K_4\), \(K_{3,3}\), the cube, the Petersen graph, and multigraph
   examples; and
4. generates and filters the complete connected cubic simple census,
   checking bridgelessness by explicit edge deletion.
