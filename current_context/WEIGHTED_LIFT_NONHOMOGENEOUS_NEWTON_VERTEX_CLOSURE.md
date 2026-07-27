# A Newton-vertex closure for nonhomogeneous weighted-lift targets

Date: 25 July 2026

## Outcome

Let \(F=(A,B,C)\) be the Gallagher weighted lift and let \(U\) be
the exact second-subduction coordinate.  The homogeneous
minimal-boundary proof extends to an arbitrary nonhomogeneous target
as soon as the first Newton vertex on its globally earliest boundary
face does not undergo the primitive cusp cancellation.

This gives a conceptual, all-degree closure of every isolated
remove-one-\(C\) chain
\[
\boxed{
A^aB^bC^c+\lambda A^{a-1}B^{b+1}C^{c-1},
\qquad a,c\ge1,
}
\tag{1}
\]
for arbitrary \(\lambda\).  In particular it closes the four
previously open target chains
\[
AC+\lambda B,\quad
ABC+\lambda B^2,\quad
AB^2C+\lambda B^3,\quad
A^2C^2+\lambda ABC.
\tag{2}
\]
The proof does not use the invalid boundary-Euler separation and
does not solve a coefficient recurrence.

There is also an immediate bounded-degree theorem substantially
stronger than the four-chain application:
\[
\boxed{
\deg_{\!A,B,C}Q\le8,\quad Q\notin\mathbf C
\quad\Longrightarrow\quad
J_{x,y}(U+R_{\le2},Q)\notin\mathbf C^\times
}
\tag{2a}
\]
on every polynomial graph.  No homogeneity hypothesis is imposed on
\(Q\).  More generally the same conclusion holds in every degree
when the support of \(Q\) contains no two exponent triples differing
by a nonzero multiple of (3), with the same first-coordinate scope
\(U+R_{\le2}\).  Degree nine is the first degree at which the
criterion can fail, through the binomial (4).

The sole ambiguity in the first two steps of the relevant Newton
filtration is the primitive lattice direction
\[
(5,-6,4),
\tag{3}
\]
which is exactly the leading cusp relation
\[
p_5^6A^5C^4-q_6^5B^6.
\tag{4}
\]
Thus the reason that a lower target degree can feed a later jet of a
higher-degree face is precise: different target degrees can represent
the same boundary initial monomial along (3).  The known
subductions \(T\) and \(U\) begin resolving this ambiguity, but a
terminating SAGBI normal-form theorem modulo \(\mathbf C[U]\) is not
proved here.

For first-coordinate perturbations the result directly applies when
every perturbing monomial is later than \(U\) in the boundary
valuation.  This includes arbitrary perturbations of target degree at
most two, and hence the quadratic and cubic scopes.  The two cubic
first-coordinate monomials that need additional care in the quartic
scope are \(A^3\), which precedes \(U\), and \(A^2B\), which ties it.
A short bifiltration calculation in Section 5 closes both
possibilities on all four chains (2).

Consequently, when combined with the surviving cases in the exact
quadratic, cubic, and quartic correction audits, this restores those
three bounded target-tier theorems in their original
first-coordinate scopes.  This conclusion depends on those prior
case exhaustions; the Newton-vertex theorem by itself is not an
arbitrary-quartic classification.

## 1. Exact boundary data

Put
\[
u=1+xy,\qquad
\gamma=1-\frac{57}{34}(u-1)
  +x^2g\left(x,\frac{u-1}{x}\right)
=\sum_{j=\rho}^{M}x^jf_j(u),
\tag{5}
\]
with \(f=f_\rho\ne0\).  As in the homogeneous proof,
\(\rho\le0\).  The exact boundary templates have unique top terms
\[
\begin{aligned}
\mathsf A&=q_6u^6\gamma^4+\cdots,\\
\mathsf B&=p_5u^5\gamma^4+\cdots,\\
\mathsf H&=\theta u^{20}\gamma^{17}+\cdots,
\end{aligned}
\qquad q_6p_5\theta\ne0,
\tag{6}
\]
and
\[
A=x^{-2}\mathsf A,\quad
B=x^{-1}\mathsf B,\quad
C=x\gamma,\quad
U=x^{-5}\mathsf H.
\tag{7}
\]
For \(\rho=0\), every non-top term in (6), after
\(\gamma=f\), loses at least \(L+1\) in \(u\)-degree, where
\[
L=\deg f\ge1,\qquad
f(1)=1,\qquad f'(1)=-\frac{57}{34}.
\tag{8}
\]
For \(\rho<0\), every non-top term in (6) has strictly later
\(x\)-order.  Moreover
\[
\nu=\operatorname{ord}_{u=1}f\ge2-\rho,\qquad
L+\rho+1\ge3.
\tag{9}
\]

Adding a constant to \(Q\) does not change the Jacobian, so discard
its constant term and write
\[
Q-Q(0)=
\sum_{\substack{a,b,c\ge0\\a+b+c>0}}
\lambda_{abc}A^aB^bC^c.
\tag{10}
\]
For an exponent triple define
\[
\begin{aligned}
\beta&=-2a-b+c,\\
h&=6a+5b,\\
q&=4a+4b+c=h+\beta.
\end{aligned}
\tag{11}
\]

## 2. Regular-boundary vertex theorem

Suppose \(\rho=0\).  Let \(\beta_0\) be the minimum \(\beta\)
in the support of \(Q\), and let \(h_0\) be the maximum \(h\) among
the support terms with \(\beta=\beta_0\).  Define the aggregated
vertex coefficient
\[
\Lambda_0=
\sum_{\substack{\lambda_{abc}\ne0\\
                 \beta=\beta_0,\ h=h_0}}
\lambda_{abc}q_6^ap_5^b.
\tag{12}
\]

> **Regular Newton-vertex theorem.**
> If \(\Lambda_0\ne0\), then
> \[
> J_{x,y}(U,Q)\notin\mathbf C^\times.
> \tag{13}
> \]
> The same holds with \(U\) replaced by \(U+R\) whenever every
> nonconstant monomial of \(R\) has boundary order greater than
> \(-5\).

Indeed, the top boundary term of \(A^aB^bC^c\) is
\[
q_6^ap_5^b u^h f^q.
\tag{14}
\]
On a fixed \(\beta\)-face its \(u\)-degree is
\[
h+qL=h+(h+\beta)L.
\tag{15}
\]
Thus decreasing \(h\) by \(r\ge1\) costs exactly
\[
r(L+1).
\tag{16}
\]
Equation (12) therefore gives a nonzero unique aggregate leading
term, and every other target contribution or non-top seed term starts
after a drop of at least \(L+1\).

The coefficient at the globally earliest Jacobian order
\(x^{\beta_0-5}\) is
\[
\mathcal W=-5\mathsf H\mathsf V'
           -\beta_0\mathsf H'\mathsf V.
\tag{17}
\]
For any exponent triple at the vertex, its leading \(u\)-coefficient
is the nonzero seed-and-target scalar times
\[
B_*L+C_*,
\tag{18}
\]
where
\[
B_*=-5q-17\beta=14a-3b-22c,\qquad
C_*=-5h-20\beta=10a-5b-20c.
\tag{19}
\]
If (18) is nonzero, then \(\mathcal W\ne0\).

If (18) vanishes, the identity
\[
17C_*-15B_*=-10q
\tag{20}
\]
and \(q>0\) show that \(B_*\ne0\).  The fixed jets (8) imply that
\(f\) is not a pure monomial.  Hence
\[
f=du^L+eu^{L-\delta}+\cdots,
\qquad d e\ne0,\quad1\le\delta\le L.
\tag{21}
\]
After the leading cancellation, the top terms in (17) have a
nonzero coefficient proportional to
\[
-B_*\delta e
\tag{22}
\]
at degree drop \(\delta\le L\).  By (16) and the exact seed gap,
nothing else can reach this coefficient.  This proves (13).

For completeness, the earliest Jacobian term has \(x\)-order
\(\beta_0-5\).  If that order is nonzero, it cannot belong to a
nonzero constant Jacobian.  If it is zero, the coefficient just
isolated is still nonconstant in \(u\): before a leading cancellation
its degree is
\[
20+17L+h_0+q_0L-1>0,
\]
and after the deviation (22) the degree drops by only
\(\delta\le L\), so it remains positive.

If the earliest \(x\)-exponent happens to be zero, the coefficient
just found still cannot be a nonzero constant.  Without leading
cancellation its \(u\)-degree is
\[
(20+17L)+(h+qL)-1>0;
\]
after (21) it drops by at most \(L\), and remains positive.

## 3. Pole-boundary vertex theorem

Suppose \(\rho<0\).  Put
\[
E=\beta+\rho q,\qquad
\alpha=-5+17\rho.
\tag{23}
\]
Let \(E_0\) be the minimum \(E\) in the support.  At \(x^{E_0}\),
group the top target terms by \(q\) and put
\[
\Lambda_q=
\sum_{\substack{\lambda_{abc}\ne0\\
                 E=E_0,\ q(a,b,c)=q}}
\lambda_{abc}q_6^ap_5^b.
\tag{24}
\]
Assume that at least one \(\Lambda_q\) is nonzero, and let
\(q_{\min}\) and \(q_{\max}\) be the smallest and largest such
indices.

> **Polar Newton-vertex theorem.**
> Under this assumption,
> \[
> J_{x,y}(U,Q)\notin\mathbf C^\times.
> \tag{25}
> \]

At fixed \(E_0\), the top monomial for the \(q\)-group is a
nonzero multiple of
\[
u^s f^q,\qquad
s=(1+\rho)q-E_0.
\tag{26}
\]
At \(u=1\), the \(q_{\min}\)-group uniquely has the least vanishing
order.  Its \(f'\)-coefficient in the Wronskian is
\[
\alpha q_{\min}-17E_0.
\tag{27}
\]
If this is nonzero, its order at \(u=1\) is
\[
(17+q_{\min})\nu-1.
\tag{27a}
\]
The corresponding order for every larger \(q\) is at least
\((17+q)\nu-1\), so (9) separates the \(q_{\min}\)-group.

Suppose instead that (27) vanishes, so
\[
E_0=\frac{\alpha q_{\min}}{17}.
\tag{28}
\]
At \(u=\infty\), the \(q_{\max}\)-group uniquely dominates because
\(L+\rho+1>0\).  Its Wronskian degree is
\[
20+17L+(L+\rho+1)q_{\max}-E_0-1,
\tag{28a}
\]
and its leading coefficient becomes
\[
\alpha\left(
(L+\rho+1)(q_{\max}-q_{\min})
+\frac{2q_{\min}}{17}
\right),
\tag{29}
\]
which is nonzero.  This proves (25).  Since every non-top seed term
has later \(x\)-order when \(\rho<0\), no hidden seed contribution
can enter this coefficient.

Again, a nonzero earliest term rules out a constant unless its
\(x\)-order is zero.  In that exceptional order, (27a) is positive
because \(\nu\ge3\), while in the second endpoint case (28a) is
positive because \(E_0\le0\), \(L+\rho+1\ge3\), and
\(\deg\mathsf H=20+17L\).  Thus the isolated coefficient is not a
nonzero constant in either case.

The nonzero coefficient cannot be a constant when its \(x\)-order is
zero: every Wronskian term vanishes at \(u=1\) to positive order,
because \(q_{\min}\ge1\) and \(\nu\ge3\).

## 4. The exact remove-one-\(C\) filtration

Let
\[
M=A^aB^bC^c,\qquad
M_-=A^{a-1}B^{b+1}C^{c-1},
\qquad a,c\ge1.
\tag{30}
\]
Their exponent difference, from \(M\) to \(M_-\), is
\[
(-1,1,-1).
\tag{31}
\]
Consequently
\[
\beta(M_-)=\beta(M),\qquad
h(M_-)=h(M)-1,\qquad
q(M_-)=q(M)-1.
\tag{32}
\]

For a regular boundary, (15) says that \(M_-\) begins exactly
\(L+1\) degrees after \(M\).  The coefficient of \(M\) is therefore
the uncancelled Newton vertex, independently of the coefficient of
\(M_-\).  For a pole boundary,
\[
E(M_-)-E(M)=-\rho>0,
\tag{33}
\]
so \(M_-\) is not even on the globally earliest \(x\)-face.
This proves (1).

For the four chains in (2), the regular leading factors (18) are,
respectively,
\[
-8L-10,\qquad
-11L-15,\qquad
-14L-20,\qquad
-16L-20.
\tag{34}
\]
They are already nonzero for every \(L\ge1\); the deviation argument
is not needed in these four cases.  At a pole boundary their local
\(f'\)-coefficients, equivalently (27), are
\[
-8,\qquad-11,\qquad-14,\qquad-16,
\tag{35}
\]
again nonzero.

### 4.1. Arbitrary nonhomogeneous targets through degree eight

If two distinct nonnegative exponent triples differ by
\(k(5,-6,4)\), assume after exchanging them that \(k>0\).  The triple
on the negative-\(B\) side must have \(b\ge6k\), so its target degree
is at least \(6k\).  The other triple has target degree larger by
\(3k\), hence at least \(9k\).  Therefore no such pair occurs when
every target monomial has degree at most eight.

It follows that the aggregate vertex (12) is a single nonzero target
coefficient at every regular boundary.  The same kernel calculation
for \((E,q)\) proves the polar assertion.  Finally, every
first-coordinate monomial of degree at most two is later than \(U\):
at a regular boundary its order is at least \(-4>-5\).  At a pole
boundary, \(\beta\ge-4\) and \(q\le8\), so
\[
(\beta+\rho q)-(-5+17\rho)
=(\beta+5)+\rho(q-17)>0.
\]
This proves (2a).

## 5. Cubic first-coordinate perturbations

It remains to check that the target-chain argument is compatible with
the arbitrary \(R_{\le3}\) allowed in the quartic theorem.

At a pole boundary every monomial of target degree at most three has
strictly later \(x\)-order than \(U\).  Indeed, for such a monomial
\(q\le12\), \(\beta\ge-6\), and
\[
E_R-\alpha=(\beta+5)+\rho(q-17)>0
\qquad(\rho<0).
\tag{36}
\]

At a regular boundary, the relevant order table is
\[
\begin{array}{c|c|c}
\text{part of }R_{\le3}&\text{smallest }\beta&
\text{comparison with }\beta(U)=-5\\ \hline
R_{\le1}&-2&\text{later}\\
R_2&-4&\text{later}\\
A^3&-6&\text{earlier}\\
A^2B&-5&\text{tied}\\
\text{other cubic monomials}&\ge-4&\text{later}.
\end{array}
\tag{37}
\]

If the \(A^3\)-coefficient is nonzero, its leading boundary term is
a nonzero multiple of
\[
x^{-6}u^{18}f^{12}.
\tag{38}
\]
For the leading monomials
\[
AC,\quad ABC,\quad AB^2C,\quad A^2C^2,
\tag{39}
\]
the leading Wronskian coefficients of \(A^3\) with the target are,
respectively,
\[
-18(L+1),\quad-30(L+1),\quad
-42(L+1),\quad-36(L+1).
\tag{40}
\]
They are nonzero.  The remove-one-\(C\) target term and every non-top
seed term begin at least \(L+1\) degrees later, so they cannot alter
these coefficients whenever the displayed monomial is the leading
target-chain monomial.

If the \(A^3\)-coefficient is zero, no first-coordinate term precedes
\(U\).  The only possible tie is \(A^2B\), whose leading \(u\)-degree
is
\[
17+12L.
\tag{41}
\]
The leading \(u\)-degree of \(U\) is \(20+17L\), a gap of
\[
3+5L>L.
\tag{42}
\]
Thus \(A^2B\) cannot reach either the leading \(U\)-Wronskian
coefficient or the fixed-\(f\) deviation at drop at most \(L\).
This closes the cubic first-coordinate perturbation on all four
chains.

## 6. The primitive obstruction to a global induction

Two exponent triples have the same pair \((\beta,h)\) if and only if
their difference is
\[
k(5,-6,4),\qquad k\in\mathbf Z.
\tag{43}
\]
Likewise, for fixed \(\rho<0\), equality of both \((E,q)\) has the
same kernel.  The primitive positive and negative parts of (43) give
\[
A^5C^4\quad\hbox{and}\quad B^6.
\tag{44}
\]
Their boundary top forms are proportional, and the normalized
binomial (4) cancels them exactly.

This also explains the apparent cross-degree failure of a degree
induction: (44) compares target degrees nine and six, yet both terms
occupy the same first Newton block.  Its exact subduction produces
the new generator \(T\); the next relation between \(T C\) and
\(B^5\) produces \(U\).  Since
\[
J(U,Q+H(U))=J(U,Q)
\tag{45}
\]
for every polynomial \(H\), an eventual normal-form theorem should
work modulo \(\mathbf C[U]\), not by target degree.

What is still missing is a proof that all subsequent toric
relations subduct and terminate using a finite set of generators.
Without that SAGBI/normal-form statement, cancellation of
\(\Lambda_0\) in (12) is a genuine obstruction to extending the
Newton-vertex theorem to every nonhomogeneous target.

## 7. Restored scope and remaining caution

The new vertex theorem supplies the missing argument for the
\(AC+B\) and \(ABC+B^2\) chains.  Since first-coordinate
perturbations of target degree at most two are later than \(U\) at
both regular and pole boundaries, it closes the only two gaps listed
in the quadratic and cubic correction audit.  Together with the
surviving cases there, this restores
\[
\begin{aligned}
&J(U+R_{\le1},Q_2+Q_{\le1})\notin\mathbf C^\times,
&&Q_2\ne0,\\
&J(U+R_{\le2},Q_3+Q_{\le2})\notin\mathbf C^\times,
&&Q_3\ne0.
\end{aligned}
\tag{46}
\]

The two genuinely quartic target gaps were \(AB^2C+B^3\) and
\(A^2C^2+ABC\); the quartic staircase also inherited the two lower
chains.  Section 5 shows that arbitrary \(R_{\le3}\) cannot repair
any of the four.  Therefore, together with the surviving descending,
negative-tail, nonresonance, interleaving, and constant-graph cases
in the quartic correction audit, this restores
\[
J(U+R_{\le3},Q_4+Q_{\le3})\notin\mathbf C^\times,
\qquad Q_4\ne0.
\tag{47}
\]

No claim is made here for arbitrary nonhomogeneous target degree.
When the aggregate vertex coefficient (12) cancels in the cusp
direction, the missing SAGBI termination problem remains.

The accompanying symbolic verifier is
`verify_weighted_lift_nonhomogeneous_newton_vertex_closure.py`.
The exact 77-term seed-support and gap assertions used here are
checked independently by
`verify_weighted_lift_global_minimal_boundary_face_closure.py`.
