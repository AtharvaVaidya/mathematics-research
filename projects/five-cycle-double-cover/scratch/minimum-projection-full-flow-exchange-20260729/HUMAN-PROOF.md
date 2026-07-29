# The exact full-flow exchange theorem

Date: 2026-07-29

Status: **HUMAN-CHECKABLE CHARACTERIZATION / FIVECDC REMAINS OPEN**.

## 1. Relative difference-flow form

Let \(G=(V,E)\) be a finite loopless cubic graph and let
\[
                         f=(h,s)
\]
be a nowhere-zero
\(\mathbb F_2\times K\)-flow, where \(K=\mathbb F_2^2\).
We identify a binary flow with its edge support.

Every other \(\mathbb F_2^3\)-flow has a unique form
\[
                         g=f+d,\qquad d=(a,b),             \tag{1}
\]
where \(a\) is a binary flow and \(b\) is a \(K\)-flow.  On edge \(e\),
\[
                         g_e=0\quad\Longleftrightarrow\quad
                         d_e=f_e.
\]
Therefore \(g\) is nowhere-zero exactly when
\[
                  (a_e,b_e)\ne(h_e,s_e)\quad(e\in E),     \tag{2}
\]
or equivalently
\[
                         b_e\ne s_e
                         \quad\text{on every edge with }a_e=h_e.    \tag{3}
\]

The first coordinate of \(g\) is
\[
                              h'=h\mathbin\triangle a.     \tag{4}
\]
Consequently
\[
 |h'|-|h|=|a-h|-|a\cap h|.                                \tag{5}
\]

> **Full-flow exchange theorem, relative form.**
> The projection \(h\) has globally minimum cardinality if and only if
> every pair of flows \((a,b)\) satisfying (3) obeys
> \[
>                              |a\cap h|\leq|a-h|.          \tag{6}
> \]

**Proof.**  Equations (1)--(3) are a bijection between admissible pairs
\((a,b)\) and competing nowhere-zero flows \(g\).  Equation (5) says
that (6) is exactly \(|h|\leq|h'|\). \(\square\)

A constant-vector exchange is the special case
\[
                  d=(1,c)\chi_C,\qquad
                  a=\chi_C,\qquad b=c\chi_C,              \tag{7}
\]
where \(C\) is a binary cycle avoiding the old full value \((1,c)\).
The four static exchange families use only (7).  General difference
flows need not be constant on \(a\), need not vanish outside \(a\), and
can use several nonzero values.

## 2. Low-flow plus one-join master form

Put
\[
                         s'=s+b,\qquad M=Z(s')
                              =\{e:s'_e=0\}.               \tag{8}
\]
Condition (3) says precisely
\[
                              M\subseteq h'.               \tag{9}
\]
Indeed \(a_e=h_e\) is equivalent by (4) to \(h'_e=0\), and on such an
edge (3) says \(s'_e=s_e+b_e\ne0\).

Let
\[
                              J=h'-M.                      \tag{10}
\]
The sets are disjoint.  Since \(h'\) is a binary cycle,
\[
                              \partial J=\partial M.       \tag{11}
\]
Conversely, start with any \(K\)-flow \(s'\), its exact zero set \(M\),
and any
\[
                              J\subseteq E-M,\qquad
                              \partial J=\partial M.       \tag{12}
\]
Then \(h'=M\mathbin{\dot\cup}J\) has even degree at every vertex by
(12), so it is a binary flow.  The three-bit flow \((h',s')\) is
nowhere-zero: its low value vanishes exactly on \(M\), where its first
coordinate is one.

This proves a second bijection.

> **Full-flow exchange theorem, master form.**
> The minimum cardinality of an extendable projection is
> \[
> \mu(G)=
> \min_{\substack{s'\text{ a }K\text{-flow}\\
>                  J\subseteq E-Z(s')\\
>                  \partial J=\partial Z(s')}}
>       \bigl(|Z(s')|+|J|\bigr),                           \tag{13}
> \]
> with the value \(+\infty\) when the inner join does not exist.

The equivalent shortest-containing-cycle notation is
\[
                \mu(G)=\min_{s'\text{ a }K\text{-flow}}
                              \tau(Z(s')),                 \tag{14}
\]
where \(\tau(M)\) is the minimum size of a binary cycle containing
\(M\).

## 3. Matching and fixed-zero-set duality

Suppose a zero set \(M=Z(s')\) participates in a feasible triple
\((s',M,J)\).  At a cubic vertex, if two incident low values are zero,
flow conservation makes the third zero as well.  Thus the degree of
\(M\) at a vertex is \(0,1\), or \(3\).  But if it were \(3\), the
disjoint set \(J\) would have degree zero there, contradicting
\(\partial J=\partial M\).  Hence
\[
                              M\text{ is a matching}.       \tag{15}
\]

For a fixed matching \(M\), minimizing \(|J|\) in (13) is the standard
shortest-\(T\)-join problem in \(G-M\), with \(T=\partial M\):
\[
\begin{array}{ll}
\text{minimize}&\displaystyle\sum_{e\in E-M}x_e\\
\text{subject to}&x(\delta_{G-M}(S))\geq1
       \quad(|S\cap T|\text{ odd}),\\
&x_e\geq0.
\end{array}                                                \tag{P_M}
\]
Its odd-cut dual is
\[
\begin{array}{ll}
\text{maximize}&\displaystyle
        \sum_{|S\cap T|\text{ odd}}y_S\\
\text{subject to}&\displaystyle
        \sum_{\substack{S:e\in\delta_G(S)\\|S\cap T|\text{ odd}}}
                  y_S\leq1\quad(e\in E-M),\\
&y_S\geq0.
\end{array}                                                \tag{D_M}
\]
Thus the full problem is a disjunctive master optimization over exact
zero matchings of \(K\)-flows, with an ordinary cut-packing dual in
every fixed-\(M\) branch.

The four affine rebases of the original extension are only
\[
                              s_c=s+c\,h\qquad(c\in K).     \tag{16}
\]
Their exact zero sets are the four classes
\[
                              M_c=\{e\in h:s_e=c\}.         \tag{17}
\]
The four static shortest-join theorems prove optimality only inside
these four branches.  Global minimality requires every low flow \(s'\)
in (13), not merely the affine plane (16).

## 4. Exact XOR/pseudo-Boolean encoding

Use two binary variables \(p_e,q_e\) for \(s'_e\), one zero indicator
\(m_e\), and one join indicator \(j_e\).  Impose:

1. native XOR conservation for \(p\) and \(q\) at every vertex;
2. the exact equivalence
   \[
                m_e=1\quad\Longleftrightarrow\quad
                p_e=q_e=0;                                \tag{18}
   \]
3. disjointness \(m_e+j_e\leq1\);
4. native XOR boundary equality
   \[
                \bigoplus_{e\ni v}m_e
                    =\bigoplus_{e\ni v}j_e
                    \qquad(v\in V);                        \tag{19}
   \]
5. the pseudo-Boolean objective
   \[
                              \min\sum_e(m_e+j_e).          \tag{20}
   \]

For a lower-bound certificate \(\mu(G)>k\), add
\(\sum_e(m_e+j_e)\leq k\) and produce a checkable CNF/PB refutation.
Positive certificates are the literal triple \((s',M,J)\).  Conditions
(18)--(19) prove the bijection above without relying on a solver.

This encoding couples multiple nonzero low-flow values.  It is strictly
stronger than checking four constant-vector cycle switches.

## 5. Cleaning is the missing second join

For a feasible triple put \(h'=M\mathbin{\dot\cup}J_1\).  The extension
\((h',s')\) is clean exactly when every component of \(G-h'\) contains
an even number of terminals in \(T=\partial M\).  Here is the cut-parity
step explicitly.

Fix a component \(W\) of \(G-h'\), and for \(c\in K\) let \(n_c(W)\)
be, modulo two, the number of edges of \(\delta(W)\cap h'\) having low
value \(c\).  Summing low-flow conservation over \(W\) gives
\[
             n_1(W)=n_2(W)=n_3(W).                       \tag{21a}
\]
Since \(h'\) is a binary flow, \(|\delta(W)\cap h'|\) is even.  Together
with (21a), this gives
\[
             n_0(W)=n_1(W)=n_2(W)=n_3(W).                \tag{21b}
\]
The extension is clean at \(W\) exactly when these four parities vanish.
But the zero-valued support edges are exactly \(M\), and the standard
boundary identity gives
\[
 n_0(W)=|M\cap\delta(W)|
       =|W\cap\partial M|\pmod2.                          \tag{21c}
\]
Thus cleanliness is exactly the condition that every component of
\(G-h'\) contains an even number of vertices of \(T\).

The elementary \(T\)-join existence criterion now says this is
equivalent to a second \(T\)-join
\[
                              J_2\subseteq G-h'.          \tag{21d}
\]
Thus \(J_1,J_2\) are edge-disjoint and both avoid \(M\).

The minimum-projection selection conjecture is therefore exactly:

> among the optimum triples in (13), some triple has a second
> \(\partial M\)-join \(J_2\) disjoint from \(M\cup J_1\).

The full-flow characterization makes the remaining obligation precise;
it does not prove it.

## 6. The 278-vertex static survivor

Use the 18-vertex base and edge order from the frozen
rainbow/load/static-exchange survivor.  Its displayed extension has
first-coordinate support \(0,\ldots,13\), low word
\[
        \texttt{3231320|1320320|3112213212312},
\]
and full vector
\[
\begin{split}
f={}&(7,5,7,3,7,5,1,\ 3,7,5,1,7,5,1,\\
    &6,2,2,4,4,2,6,4,2,4,6,2,4).                         \tag{22}
\end{split}
\]
The size-seven competitor is
\[
\begin{split}
g={}&(3,1,3,7,5,1,5,\ 6,4,6,2,4,6,2,\\
    &6,2,2,4,2,4,6,4,2,4,6,4,2).                         \tag{23}
\end{split}
\]
Here the first coordinate is the least significant bit and the low
value is the remaining two-bit integer.

The low flow \(s'\) in (23) is
\[
          \texttt{1013202|3231231|3112123212321}.          \tag{24}
\]
Its exact zero set and one join are
\[
                 M=\{1,5\},\qquad
                 J=\{0,2,3,4,6\}.                         \tag{25}
\]
The set \(M\mathbin{\dot\cup}J=\{0,\ldots,6\}\) is the first
7-circuit.  Hence (25) is a directly checkable master certificate of
cost seven.

Relative to (22), the difference \(d=f+g=(a,b)\) is
\[
\begin{split}
d={}&(4,4,4,4,2,4,4,\ 5,3,3,3,3,3,3,\\
    &0,0,0,0,6,6,0,0,0,0,0,6,6),                         \tag{26}\\
a={}&\texttt{0000000|1111111|0000000000000},\\
b={}&\texttt{2222122|2111111|0000330000033}.              \tag{27}
\end{split}
\]
It uses the five nonzero full values \(2,3,4,5,6\).  In particular,
it is not a constant-vector switch on the second circuit.  Its low
part is also nonzero on the first circuit and on four complement edges.

Every base edge replaced in the 278-vertex inflation has a nonzero low
value in (23).  A chain pole extends any prescribed nonzero terminal
value \(t\): give the two cross pairs the other two nonzero values.
Applying this independently through all five-pole chains lifts (23) to
a nowhere-zero flow on the literal inflated graph without adding any
first-coordinate edge.  Its projection is still the first 7-circuit.

The two bundled checkers construct all \(278\) vertices and \(417\)
edges and verify both lifted flows directly.  The previously frozen
contraction/cycle-space audit proves that seven is not merely an upper
bound but the exact global minimum.

## 7. Exact conclusion

The 278-vertex survivor passes all four affine branches (16)--(17), but
the low flow (24) lies outside that affine plane and has master cost
seven.  This is the precise certificate which the four static duals
cannot see.

A future proof must compare exact-zero matchings belonging to different
low flows, or prove that an optimum master branch in (13) packs the
second join in (21).  No such cross-branch duality or packing theorem is
proved here.
