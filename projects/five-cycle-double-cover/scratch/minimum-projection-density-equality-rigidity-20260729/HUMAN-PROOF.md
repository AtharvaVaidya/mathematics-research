# Equality rigidity for minimum extendable projections

Date: 2026-07-29

Status: **HUMAN-CHECKABLE THEOREM / FIVECDC REMAINS OPEN**.

## 1. Four optimal cut duals

Let \(G=(V,E)\) be a finite loopless cubic graph, let
\(f=(h,s)\) be an extension, and assume that the first-coordinate
support \(h\) has minimum cardinality among all extendable projections.
For \(c\in K=\mathbb F_2^2\), put
\[
 M_c=\{e\in h:s_e=c\},\qquad J_c=h-M_c.
\]
Then \(J_c\) is a shortest \(T_c\)-join in \(G-M_c\), where
\(T_c=\partial M_c\).

Fix any optimal solution \(y_{c,S}\) of the standard odd-cut dual, and
write
\[
 \ell_c(e)=\sum_{\substack{S:\ e\in\delta_G(S)\\S\text{ is }T_c\text{-odd}}}
                  y_{c,S}.                                 \tag{1}
\]
Strong duality and complementary slackness give
\[
\begin{split}
\sum_Sy_{c,S}&=|J_c|,\\
e\in J_c&\Longrightarrow\ell_c(e)=1,\\
y_{c,S}>0&\Longrightarrow|J_c\cap\delta_G(S)|=1.           \tag{2}
\end{split}
\]

The quotient-cut zero-price theorem says every positive dual shore
splits at least one component of \(G-h\).  Hence every positive cut
contains at least one complement edge, and by (2) it contains exactly
one \(J_c\)-edge plus at least one complement edge.  In particular
\[
                      |\delta_{G-M_c}(S)|\geq2
                      \quad\text{when }y_{c,S}>0.           \tag{3}
\]

## 2. Exact slack decomposition

Put
\[
                             m=|E-h|
\]
and define
\[
\begin{split}
 A_c&=\sum_Sy_{c,S}
             \bigl(|\delta_{G-M_c}(S)|-2\bigr),\\
 U_c&=\sum_{e\in E-h}(1-\ell_c(e)).                        \tag{4}
\end{split}
\]
Both quantities are nonnegative by (3) and the unit edge-capacity
constraints.

Double-count cut-edge incidences in two ways:
\[
\begin{split}
\sum_Sy_{c,S}|\delta_{G-M_c}(S)|
 &=2|J_c|+A_c,\\
\sum_{e\in E-M_c}\ell_c(e)
 &=|J_c|+m-U_c.                                            \tag{5}
\end{split}
\]
The two left sides are identical.  Therefore
\[
                            m-|J_c|=A_c+U_c.               \tag{6}
\]
Since the four \(M_c\)'s partition \(h\),
\[
                         \sum_c|J_c|=3|h|.
\]
Summing (6) over \(c\) proves the exact identity
\[
                      4m-3|h|=\sum_c(A_c+U_c).             \tag{7}
\]
It both reproves \(4m\geq3|h|\) and records every source of slack.

## 3. Consequences of equality

Assume
\[
                             4m=3|h|.                      \tag{8}
\]
Every nonnegative term on the right of (7) is zero.

First, \(A_c=0\) says every positive dual cut has exactly two edges in
\(G-M_c\).  By (2), one is its unique \(J_c\)-edge.  The other is
therefore its unique complement edge.

Second, \(U_c=0\) says every complement edge is saturated in every one
of the four duals.  Fix a complement edge \(e\).  In any one dual,
some positive cut crosses \(e\); by the preceding paragraph, \(e\) is
the only complement edge crossing that shore.  An edge on a circuit of
\(G-h\) crosses every shore together with at least one other edge of
that circuit.  Hence \(e\) cannot lie on a complement circuit.  Since
this holds for every complement edge,
\[
                              G-h\text{ is a forest}.       \tag{9}
\]

## 4. Colour and topology counts

Let \(m_t\) be the number of complement edges of nonzero low colour
\(t\in K-\{0\}\).  For the nonzero functional \(\alpha\) whose kernel is
\(\{0,t\}\), the functional half-load theorem gives
\[
                    m-m_t
       =|\{e\in E-h:\alpha(s_e)=1\}|\geq\frac{|h|}{2}.      \tag{10}
\]
Under (8), \(m=3|h|/4\), so \(m_t\leq|h|/4\).  The three \(m_t\)'s sum
to \(m=3|h|/4\).  Therefore
\[
                              m_t=\frac{|h|}{4}
                              \quad(t\ne0).                 \tag{11}
\]

Let \(n=|V|-|h|\) be the number of off-support vertices.  Cubicity and
(8) give
\[
 \frac32|V|-|h|=m=\frac34|h|,
 \qquad\text{hence}\qquad
                              n=\frac{|h|}{6}.              \tag{12}
\]

Let \(k_t\) count support vertices whose unique complement edge has low
colour \(t\).  At every off-support cubic vertex the three incident
nonzero low values are \(1,2,3\), one of each.  Counting colour-\(t\)
incidences in \(G-h\) gives
\[
                              2m_t=n+k_t.                  \tag{13}
\]
Equations (11) and (12) imply
\[
                              k_t=\frac{|h|}{3}
                              \quad(t\ne0).                 \tag{14}
\]
Thus \(|h|\) is divisible by both four and three, hence by twelve.

Finally let \(q\) be the number of components of the forest \(G-h\).
A component with \(k\) support leaves and all other vertices cubic has
\(k-2\) off-support vertices.  Summing over components gives
\[
                         n=|h|-2q.
\]
Using (12),
\[
                              q=\frac{5|h|}{12}.            \tag{15}
\]

## 5. Every affine witness is exactly colour-balanced

Let \(Y\) be a union of complement components on which all six common
\(\operatorname{GL}(2,2)\) postcompositions are integrable; in
particular, take any dual affine-cleaning witness shore.  Write
\[
 a_t=k_t(Y),\qquad k_t(\overline Y)=\frac{|h|}{3}-a_t.
\]
The dynamic boundary colour-load inequality says
\[
        \max_t k_t(Y)+\max_t k_t(\overline Y)\leq2n
                                                  =\frac{|h|}{3}.   \tag{16}
\]
Substituting the displayed outside counts turns (16) into
\[
                         \max_t a_t-\min_t a_t\leq0.
\]
Therefore
\[
                             a_1=a_2=a_3.                  \tag{17}
\]
The outside triple is also equal.  Thus every affine witness at density
equality is exactly derivative-colour-balanced, not merely xor-balanced.

## 6. Remaining scope

The only positive equality support below \(24\) is \(12\).  The theorem
that all globally minimum extendable projections of size at most fifteen
are cleanable excludes an unclean equality obstruction there.  Hence an
unclean equality-case obstruction must have
\[
                              |h|\geq24.                   \tag{18}
\]

Nothing here excludes strict density slack \(4m-3|h|>0\).  Nor does
exact derivative balance in (17) by itself neutralize the quadratic
rainbow bit: the separate six-circuit counterstate shows those two
properties can coexist outside the global-minimum domain.  The equality
classification is a sharp necessary structure, not a resolution.
