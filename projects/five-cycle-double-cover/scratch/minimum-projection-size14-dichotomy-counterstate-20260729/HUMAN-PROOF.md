# Human proof for the order-fourteen abstract counterstate

Date: 2026-07-29

Status: **EXACT COUNTERSTATE TO THE UNQUALIFIED ABSTRACT
CLEAN-OR-DELETE DICHOTOMY / NOT A FIVECDC COUNTEREXAMPLE / NOT A
COUNTEREXAMPLE WITH A GLOBALLY MINIMUM PROJECTION**.

## 1. Conventions and the state

Let \(K=\mathbb F_2^2=\{0,1,2,3\}\), with addition written as xor.
Thus the three nonzero elements are \(1,2,3\), and \(1+2=3\).

There are two oriented 7-circuits \(A,B\).  Vertex \(v_i\) lies between
edges \(e_{i-1}\) and \(e_i\), with cyclic indices.  If the low edge
word is \(c_0\cdots c_6\), the boundary derivative at \(v_i\) is
\[
                              d_i=c_{i-1}+c_i.             \tag{1}
\]
The counterstate is
\[
\begin{array}{c|c|c|c}
 &\text{low word }c&\text{derivative word }d&
                         \text{component blocks at }v_i\\ \hline
A&0101023&3111121&0123444\\
B&0101232&2111311&4413024 .
\end{array}                                               \tag{2}
\]
Every adjacent pair of low values differs, and both original circuit
words use all four elements of \(K\).  In every block, the xor of the
displayed derivatives is zero:
\[
\begin{array}{c|cc}
\text{block}&A&B\\ \hline
0&3&3\\
1&1&1\\
2&1&1\\
3&1&1\\
4&1+2+1=2&2+1+1=2 .
\end{array}                                               \tag{3}
\]
Thus (2) is an admissible charged boundary state.

## 2. All integrable component maps

Choose one \(L_i\in\operatorname{GL}(2,2)\) in each block.  Composing
every map and every resulting low value with the same invertible map
does not affect integrability, cleanliness, or the number of colours on
a circuit.  We may therefore normalize
\[
                              L_0=I.                       \tag{4}
\]
Put
\[
 u_i=L_i(1)\quad(i=1,2,3),\qquad
 a=L_4(1),\qquad b=L_4(2).                                \tag{5}
\]
Here \(u_1,u_2,u_3,a,b\) are nonzero and \(a\ne b\).  Conversely, these
conditions determine all boundary-relevant map data; the unused image
in each of blocks \(1,2,3\) has two possible choices.

The transformed derivative words on the two circuits are
\[
\begin{split}
A:&\quad 3,\ u_1,\ u_2,\ u_3,\ a,\ b,\ a,\\
B:&\quad b,\ a,\ u_1,\ u_3,\ 3,\ u_2,\ a.
\end{split}                                               \tag{6}
\]
Their two cyclic xor conditions are the same:
\[
                         b=3+u_1+u_2+u_3.                 \tag{7}
\]
Equations (5) and (7) are therefore an exact, reduced description of
every integrable component-map tuple.  Of the \(3^3=27\) choices of
\((u_1,u_2,u_3)\), exactly seven make the right side of (7) zero; each
of the remaining twenty choices of \(b\) leaves two choices for
\(a\ne b\).  There are therefore 40 reduced tuples, or
\(40\cdot2^3=320\) full tuples after the three irrelevant stabilizer
choices are restored.  The proof below does not enumerate those 40
tuples.

## 3. Deletion is impossible

Integrate (6) with zero start.  Using (7), the circuit-edge values are
\[
\begin{split}
r^A={}&(3,\ 3+u_1,\ 3+u_1+u_2,\ b,\ a+b,\ a,\ 0),\\
r^B={}&(b,\ a+b,\ 3+u_2+u_3+a,\ 3+u_2+a,\
                              u_2+a,\ a,\ 0).
\end{split}                                               \tag{8}
\]
Since \(a,b\) are distinct nonzero elements of the two-dimensional
space \(K\),
\[
                              \{0,a,b,a+b\}=K.             \tag{9}
\]
The four values in (9) occur in each row of (8): in positions
\((6,5,3,4)\) on \(A\) and \((6,5,0,1)\) on \(B\).  Consequently every
integrable map tuple uses all four low colours on both circuits.
Translations merely permute \(K\).  No whole circuit can ever be made
nowhere-zero in the low coordinates, so the proposed deletion branch
never applies.

## 4. Cleaning is impossible

Let \(z\in K\) be the relative translation added to every edge of
circuit \(B\); fix the translation on \(A\) to zero.

Each of blocks \(0,1,2,3\) contains exactly one vertex of \(A\) and one
vertex of \(B\).  In block \(i\), both vertices have the same transformed
derivative \(T_i\).  If \(x\) and \(y\) are the values on the respective
edges immediately preceding those vertices, their two incident-colour
sets are
\[
                         \{x,x+T_i\},\qquad
                         \{y+z,y+z+T_i\}.                 \tag{10}
\]
All four colour multiplicities at this block are even exactly when the
two sets in (10) agree.  Equivalently,
\[
                              z\in x+y+\{0,T_i\}.          \tag{11}
\]

Reading the predecessor values from (8) gives the four necessary
affine-line constraints
\[
\begin{array}{c|c|c}
\text{block}&T_i&\text{allowed relative translations}\\ \hline
0&3   &{\cal L}_0=u_2+a+\{0,3\}\\
1&u_1 &{\cal L}_1=3+a+b+\{0,u_1\}\\
2&u_2 &{\cal L}_2=3+u_1+u_2+a+\{0,u_2\}\\
3&u_3 &{\cal L}_3=u_1+u_3+a+\{0,u_3\}.
\end{array}                                               \tag{12}
\]
We now prove that the four lines have empty intersection.

Suppose first that
\[
                         z=u_2+a+3,                       \tag{13}
\]
the second point of \({\cal L}_0\).  Membership in \({\cal L}_2\)
says
\[
                         u_1\in\{0,u_2\},
\]
so \(u_1=u_2\).  Membership in \({\cal L}_3\) then says
\[
                         3\in\{0,u_3\},
\]
so \(u_3=3\).  Equation (7) now gives
\[
                         b=3+u_1+u_1+3=0,
\]
contrary to \(L_4(2)\ne0\).

It remains to suppose that
\[
                         z=u_2+a,                         \tag{14}
\]
the first point of \({\cal L}_0\).  Using (7), membership in
\({\cal L}_1\) becomes
\[
                         u_1+u_3\in\{0,u_1\}.
\]
Since \(u_3\ne0\), this forces \(u_3=u_1\).  Membership in
\({\cal L}_3\) then gives
\[
                         u_2\in\{0,u_1\}.
\]
Since \(u_2\ne0\), this forces \(u_2=u_1\).  Finally, membership in
\({\cal L}_2\) says
\[
                         u_1+3\in\{0,u_1\},
\]
and hence \(u_1=3\).  Equation (7) again gives
\[
                         b=3+3+3+3=0,
\]
a contradiction.

Thus no \(z\) satisfies even the first four component equations.
Block \(4\) need not be considered: no integrable component maps and
circuit translations clean this state.

Sections 3 and 4 prove, without a finite case table, that (2) has
neither a clean branch nor a deletion branch.

## 5. A simple bridgeless cubic realization

The state is not merely a formal set partition.  The script
`analyze_realization.py` constructs the following graph with edge ids
in the order displayed here.

* Edges \(0,\ldots,6\) form
  \(0\,1\,2\,3\,4\,5\,6\,0\).
* Edges \(7,\ldots,13\) form
  \(7\,8\,9\,10\,11\,12\,13\,7\).
* Edges \(14,\ldots,17\) are
  \(0\!-\!11,1\!-\!9,2\!-\!12,3\!-\!10\), realizing blocks
  \(0,1,2,3\).
* Edges \(18,\ldots,26\) are
  \[
  14\!-\!4,\ 14\!-\!5,\ 14\!-\!15,\ 15\!-\!6,\
  15\!-\!16,\ 16\!-\!13,\ 16\!-\!17,\ 17\!-\!7,\
  17\!-\!8,
  \]
  a cubic tree realizing block \(4\).

This is a simple connected cubic graph on 18 vertices and 27 edges.
The first fourteen edges are the target projection.  Give them the two
words in (2), and give edges \(14,\ldots,26\) the low values
\[
                    3,1,1,1,1,2,3,1,2,1,3,2,1.          \tag{15}
\]
Direct xor at every vertex is zero, and every value outside the target
projection is nonzero.  Thus (15) is an extension of the displayed
projection, and deleting the first fourteen edges produces exactly the
five component blocks in (2).

Every one of the first fourteen edges lies on one of the two displayed
7-circuits.  Every other edge lies on a cycle as well: after its removal,
each resulting piece of its complement component still contains a
terminal on one of the two 7-circuits, and those two circuits together
with any one of edges \(14,\ldots,17\) connect all terminals externally.
Thus the graph is bridgeless.  `analyze_realization.py` independently
checks connectivity after deletion of each of the 27 edges.

Canonical labeling with `labelg` gives
```text
Qs???SC@GS@_CDOoC@@@?O?CO?g
```
and `planarg` reports that the graph is nonplanar.

## 6. The global-minimum escape

The target projection has size 14, but it is **not** a globally minimum
extendable projection of this realization.  In fact, exhaustive
cycle-space enumeration finds 15,360 extensions of this fixed
projection.  None is clean, but 3,840 of them lie outside the
componentwise-\(\operatorname{GL}(2,2)\) orbit studied above and have a
support circuit omitting a low colour (1,920 for each of the two
circuits).  Thus changing to a genuinely different extension already
opens a deletion branch.

The graph has binary cycle space dimension
\[
                              27-18+1=10,
\]
so `analyze_realization.py` explicitly generates all \(2^{10}=1024\)
binary cycles.  It tests every pair \(p,q\) and every possible projection
\(h\), using the exact condition
\[
                              E(G)-h\subseteq p\cup q.     \tag{16}
\]
The resulting minimum is 5.  There are four minimum projections, with
edge sets
\[
\begin{split}
&\{0,9,10,14,15\},\qquad \{0,1,11,14,16\},\\
&\{1,2,9,15,17\},\qquad \{2,10,11,16,17\}.
\end{split}                                               \tag{17}
\]
Every one has 120 extensions, and all 120 are clean.

This exact escape is conceptually essential.  The counterstate proves
that component charge, four-colour occurrence on every support circuit,
and componentwise \(\operatorname{GL}(2,2)\) switching do **not** by
themselves imply clean-or-delete.  It does not disprove a theorem that
uses the full global-minimality inequalities, it does not produce a
globally minimum dirty projection, and it does not resolve FiveCDC.
