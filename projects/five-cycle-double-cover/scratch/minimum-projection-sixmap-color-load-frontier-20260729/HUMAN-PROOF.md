# The six-map colour-load inequality

Date: 2026-07-29

Status: **HUMAN-CHECKABLE DYNAMIC EXCHANGE LEMMA / FIVECDC REMAINS
OPEN**.

## 1. Functional half-load

Let \(G=(V,E)\) be a finite loopless cubic graph and
\[
                         f=(h,s)
\]
a nowhere-zero \(\mathbb F_2\times\mathbb F_2^2\)-flow.  Assume \(h\)
has minimum cardinality among all extendable first-coordinate supports.
Write \(K=\mathbb F_2^2\), and put
\[
                         M_c=\{e\in h:s_e=c\}.
\]

Fix a nonzero linear functional \(\alpha:K\to\mathbb F_2\), and define
the binary cycle
\[
                         C_\alpha=\{e:\alpha(s_e)=1\}.      \tag{1}
\]
It is a binary cycle because \(\alpha\circ s\) is a binary flow.  So is
\[
                         C'_\alpha=h\mathbin\triangle C_\alpha. \tag{2}
\]
Put
\[
\begin{split}
 a_\alpha&=|C_\alpha\cap h|,\\
 m_\alpha&=|C_\alpha-h|
          =|\{e\in E-h:\alpha(s_e)=1\}|.
\end{split}
\]

If \(\alpha(c)=0\), then \(C_\alpha\cap M_c=\varnothing\).  The
minimum-projection exchange inequality applied to \(C_\alpha\) gives
\[
                              a_\alpha\leq m_\alpha.        \tag{3}
\]
If \(\alpha(c)=1\), then \(C'_\alpha\cap M_c=\varnothing\), since its
indicator on a support edge of low colour \(c\) is
\(1+\alpha(c)=0\).  Outside \(h\), the cycles \(C_\alpha\) and
\(C'_\alpha\) agree.  Applying the exchange inequality to
\(C'_\alpha\) gives
\[
                           |h|-a_\alpha\leq m_\alpha.       \tag{4}
\]
Both kinds of \(c\) exist.  Therefore
\[
                             m_\alpha\geq\frac{|h|}{2}.     \tag{5}
\]

This argument is constructive.  If (5) fails, either
\(a_\alpha>m_\alpha\) or
\(|h|-a_\alpha>m_\alpha\).  In the first case \(C_\alpha\) is a strict
exchange avoiding either class in \(\ker\alpha\); in the second case
\(C'_\alpha\) is a strict exchange avoiding either class outside
\(\ker\alpha\).

## 2. Splitting the complement into a switch shore and its exterior

Let \({\cal W}\) be the component partition of \(G-h\).  Let \(Y\) be a
union of members of \({\cal W}\), and suppose that for every
\(U\in\operatorname{GL}(2,2)\), postcomposing \(s\) by \(U\) on the
components inside \(Y\), followed by integration on the support
circuits, gives another extension with first-coordinate support \(h\).

This premise holds for the component union supplied by the dual-cut
feasible-move theorem: its selected derivative xor is zero on every
support circuit, and applying \(U\) preserves zero.

Let
\[
\begin{split}
 N_b&=|\{e\in E-h:e\text{ lies in }Y,\ s_e=b\}|,\\
 O_a&=|\{e\in E-h:e\text{ lies outside }Y,\ s_e=a\}|
\end{split}                                                 \tag{6}
\]
for \(a,b\in K-\{0\}\).  Put
\[
                    N=\sum_bN_b,\quad O=\sum_aO_a,\quad
                    m=N+O=|E-h|.                            \tag{7}
\]

> **Theorem.** Under the preceding hypotheses,
> \[
>                      O_a+N_b\leq m-\frac{|h|}{2}
>                      \qquad(a,b\ne0).                     \tag{8}
> \]
> Equivalently,
> \[
>                  \max_aO_a+\max_bN_b\leq m-\frac{|h|}{2}. \tag{9}
> \]

**Proof.**  Fix \(a,b\ne0\).  There is a unique nonzero functional
\(\alpha\) whose kernel is \(\{0,a\}\).  Choose
\(U\in\operatorname{GL}(2,2)\) with \(U(b)=a\).  Such a \(U\) exists
because the group acts transitively on the three nonzero vectors.

After the postcomposition, an outside complement edge has
\(\alpha(s_e)=0\) exactly when its colour is \(a\), while an inside
complement edge has
\(\alpha(Us_e)=0\) exactly when its old colour is \(b\).  Hence
\[
                         m_\alpha^U
                           =(O-O_a)+(N-N_b)
                           =m-O_a-N_b.                     \tag{10}
\]
The switched state is an extension with the same globally minimum
support \(h\), so (5) applied after the switch gives
\[
                         m-O_a-N_b\geq\frac{|h|}{2}.
\]
This is (8).  Taking the largest \(O_a\) and \(N_b\) gives (9), and
(9) plainly implies every instance of (8). \(\square\)

## 3. Explicit dynamic descent

The contrapositive contains an explicit certificate.  Suppose
\[
                           O_a+N_b>m-\frac{|h|}{2}.         \tag{11}
\]
Choose \(\alpha\) and \(U\) as in the proof.  Equation (10) says
\(m_\alpha^U<|h|/2\).  Let
\[
                 a_\alpha^U=|\{e\in h:\alpha(s_e^U)=1\}|.
\]
If \(a_\alpha^U>|h|/2\), then
\(C_\alpha^U\) has more support than complement edges and avoids the
two support classes in \(\ker\alpha\).  Otherwise
\(|h|-a_\alpha^U\geq|h|/2>m_\alpha^U\), and
\(h\mathbin\triangle C_\alpha^U\) is a strict exchange avoiding the
two support classes outside \(\ker\alpha\).

Thus (11) algorithmically returns a legal six-map recolouring and a
strict colour-avoiding binary-cycle descent.

## 4. Equivalent boundary-occurrence form

The colour-load inequality can be read directly from the derivative
occurrences used by the boundary classifiers.

Let \(n_Y\) be the number of vertices inside \(Y\) which do not lie on
the support \(h\), and let \(k_b(Y)\) be the number of support vertices
inside \(Y\) whose unique incident complement edge has low colour \(b\).
At every off-support cubic vertex the three incident complement values
are the three distinct nonzero elements of \(K\), so exactly one
colour-\(b\) incidence occurs.  At a support vertex there is one such
incidence exactly when its complement edge has colour \(b\).
Double-counting colour-\(b\) incidences inside the complement components
of \(Y\) gives
\[
                             2N_b=n_Y+k_b(Y).               \tag{12}
\]
Similarly, with \(\overline Y\) denoting the union of the other
complement components,
\[
                    2O_a=n_{\overline Y}+k_a(\overline Y). \tag{13}
\]

Because a binary cycle in a cubic graph is 2-regular on its support,
\(h\) has exactly \(|h|\) support vertices.  Put
\[
                   n=n_Y+n_{\overline Y}=|V|-|h|.
\]
The complement degree sum gives
\[
                         m=|E-h|=\frac{3n+|h|}{2}.          \tag{14}
\]
Substituting (12)--(14) into (8) shows that the nine inequalities are
equivalent to
\[
                    k_a(\overline Y)+k_b(Y)\leq2n
                    \qquad(a,b\ne0),                       \tag{15}
\]
or, equivalently,
\[
               \max_a k_a(\overline Y)+\max_b k_b(Y)
                    \leq2(|V|-|h|).                        \tag{16}
\]

Thus violation of (15) is a boundary-count certificate for the explicit
descent in Section 3.  This form also explains the support-density bound:
with \(Y\) equal to all complement components,
\(\max_b k_b(Y)\geq |h|/3\), so (16) implies
\(|h|/3\leq2(|V|-|h|)\), or \(|h|\leq6|V|/7\).

## 5. Exact limitation

Rainbow-oddness is a boundary parity condition.  Inequality (8) concerns
the numbers of all complement edges in the three low colours.  Boundary
parity alone does not presently force one of the nine inequalities (8)
to fail; arbitrary subdivisions or colour-balanced interiors can make
the right side large.

The theorem therefore supplies the requested dynamic recomputation law
and a sufficient descent test, but not a universal descent theorem.
