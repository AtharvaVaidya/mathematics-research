# Closure of every homogeneous binary second target in every degree

Date: 25 July 2026

## Outcome

Let \(F=(A,B,C)\) be the generic-degree-six Gallagher weighted lift,
and let \(U\) be its second-subduction coordinate.  For every
\(n\ge1\), let
\[
Q_n(A,B)=\sum_{j=0}^n c_jA^jB^{n-j}
\ne0
\tag{1}
\]
be an arbitrary homogeneous binary target.  Let \(R_{\le1}\) and
\(S_{\le1}\) be arbitrary affine target polynomials.  Then no
polynomial graph \(z=g(x,y)\) makes
\[
\left(
(U+R_{\le1})\circ F,\
(Q_n+S_{\le1})\circ F
\right)\big|_{z=g}
\tag{2}
\]
have nonzero constant Jacobian.

This closes every homogeneous binary second target in every degree.
The proof separates three mechanisms:

- the exact maximal-\(x\) filtration isolates the top characteristic
  sector from every lower seed term, so a nonpolynomial
  characteristic is impossible without any tail-timing bound;
- for an honest mixed polynomial completion with
  \(P(0)\ne0\), the first-lower forcing has a nonzero double pole at
  \(t=0\);
- for an honest mixed polynomial completion with \(P(0)=0\), any
  nonzero root of \(P\) supplies a nonzero double pole;
- the characteristic operator applied to a polynomial graph sector
  has only simple poles, so neither double pole can be cancelled;
- on a pure face \(P=t^d\), the exact first-lower numerator is
  nonzero except for the single arithmetic ray
  \((I,J,d)=(5,15,n)\);
- that exceptional \(A^n\)-ray forces the forbidden source monomial
  \(1365c\,xy^{11}\) eight filtration steps below its top, strictly
  before any lower seed or affine perturbation can enter.

The pole obstruction occurs at graph-weight drop \(m+4\).  It is not
the later cleared source-axis residual at \(m+2d+2\), and the two
filtration levels are never combined.  Nor can a sparse negative
tail combine with it: the tail remains in the maximal \(x^I\)-sector,
whereas the first-lower forcing lies in the \(x^{-1}\)-sector.

This is a theorem about the particular weighted lift and its
second-subduction coordinate.  It does not cover arbitrary lower
target-degree terms, targets involving \(C\), or resolve the
Jacobian conjecture.

## 1. The maximal-\(x\) characteristic

Put
\[
u=1+xy,\qquad t=\frac ux,\qquad
\gamma=1-\frac{57}{34}xy+x^2g(x,y).
\tag{3}
\]
Up to nonzero constants, the highest sectors are
\[
\begin{aligned}
U^{(0)}&=\theta x^{15}t^{20}\gamma^{17},\\
A^{(0)}&=q_6x^4t^6\gamma^4,\\
B^{(0)}&=p_5x^4t^5\gamma^4,
\end{aligned}
\tag{4}
\]
where
\[
p_5=-\frac3{46},\qquad q_6=-\frac5{92}.
\tag{5}
\]
Let
\[
d=\max\{j:c_j\ne0\}.
\tag{6}
\]
After absorbing the nonzero seed constants into the coefficients,
the highest sector of \(Q_n\) is
\[
V^{(0)}
=x^{4n}t^{5n}\gamma^{4n}P(t),
\qquad
P(t)=\sum_{j=0}^d p_jt^j,\quad p_d=1.
\tag{7}
\]
The highest Jacobian equation is
\[
\begin{aligned}
\mathcal L_{n,P}(\gamma)={}&
x\left(
\frac{5n}{t}+17\frac{P'}P
\right)\gamma_x
-8n\gamma_t\\
&+\left(
-\frac{5n}{t}+15\frac{P'}P
\right)\gamma=0.
\end{aligned}
\tag{8}
\]
On a fixed \(x\)-Laurent sector it has the unique formal solution
\[
\gamma_I
=c_0x^It^rP(t)^s,
\qquad
r=\frac{5(I-1)}8,\qquad
s=\frac{17I+15}{8n}.
\tag{9}
\]
Its leading \(t\)-degree is
\[
J=r+ds,
\tag{10}
\]
or equivalently
\[
8nJ=(5n+17d)I+15d-5n.
\tag{11}
\]
For a graph monomial of degree \(m\),
\[
m=I+J-2.
\tag{12}
\]

At a fixed \(m\), (11) determines the resonant sector uniquely:
\[
I=\frac{8nm+21n-15d}{13n+17d}.
\tag{13}
\]
Thus two independent characteristic amplitudes cannot occur on the
same highest graph degree.  Since (8) preserves Laurent powers of
\(x\), every other monomial of the same highest homogeneous graph
part is nonresonant and its coefficient is forced to vanish.

The coordinate change \(y=t-x^{-1}\) writes the graph expression as
a finite Laurent polynomial
\[
\gamma(x,t)=\sum_Kx^K\psi_K(t),
\qquad \psi_K(t)\in\mathbb C[t].
\tag{13a}
\]
For a nonconstant graph, let \(I\) be its largest occurring
\(x\)-exponent.  Then \(I\ge2\): if \(x^a\) is the largest
\(x\)-power occurring in \(g\), the coefficient of \(x^{a+2}\) in
\(x^2g(x,t-x^{-1})\) is a nonzero polynomial in \(t\).  Put
\[
\gamma_I=x^I\psi_I(t),\qquad \psi_I\ne0.
\tag{13b}
\]

### 1.1. Exact support separation

The exact second-subduction coordinate has the presentation
\[
U=\frac{\mathcal N(w,\gamma)}{x^5\gamma^5},
\qquad w=xt\gamma.
\tag{13c}
\]
Its top numerator monomial is
\(\theta w^{20}\gamma^2\).  For any numerator monomial
\(w^i\gamma^j\), define its losses from the top by
\[
a=20-i,\qquad b=22-i-j.
\tag{13d}
\]
Thus its ratio to \(U^{(0)}\) is, up to its \(t\)-power,
\[
x^{-a}\gamma^{-b}.
\tag{13e}
\]
The exact 77-term numerator audit gives
\[
a\ge0,\qquad b\ge0,
\tag{13f}
\]
with \((a,b)=(0,0)\) only for the top monomial.  For every
\(I\ge2\), the unique non-top monomial of least maximal-\(x\) loss is
\(w^{19}\gamma^2\), with
\[
(a,b)=(1,1),\qquad a+Ib=I+1.
\tag{13g}
\]
Every other numerator monomial has \(a+Ib>I+1\).

The seed supports obey the same separation.  Relative to
\(q_6w^6\) in \(A\), a term \(q_kw^k\) has
\[
(a,b)=(6-k,6-k),
\]
while the added \(w\gamma\) has \((a,b)=(5,4)\).  Relative to
\(p_5w^5\) in \(B\), a term \(p_kw^k\) has
\((a,b)=(5-k,5-k)\), while the added \(\gamma\) again has
\((a,b)=(5,4)\).  Products forming \(Q_n(A,B)\) add these loss
pairs.  Hence every non-top target term has positive loss, and the
unique first loss \(I+1\) comes from one \(q_5\) or \(p_4\)
replacement.

Indeed, a Jacobian term with combined loss \((a,b)\), divided by the
top common factor, has the form
\[
x^{-a}\gamma^{-b}\mathcal D_{a,b}(\gamma).
\tag{13h}
\]
Here \(\mathcal D_{a,b}\) is linear in \(\gamma,\gamma_x,\gamma_t\).
On (13b), its largest possible Laurent exponent is therefore
\[
I-a-Ib=I(1-b)-a.
\tag{13i}
\]
It equals \(I\) only for the top support \((a,b)=(0,0)\).
Every lower seed term, and every use of a graph sector below
\(x^I\), has smaller maximal \(x\)-degree.

Consequently the coefficient of the largest \(x\)-power in the exact
Jacobian is isolated and is precisely (8) applied to
\(x^I\psi_I(t)\).  The unique solution is (9).  Since
\(\psi_I(t)\) is a polynomial, any nonpolynomial expression
\(t^rP(t)^s\) is impossible immediately.  There is no tail-timing
qualification.

This also resolves the formerly apparent degree-126 timing case.
For
\[
(n,d,I,J)=(126,12,9,7),\qquad
P=t^{12}+6\lambda t^6+15\lambda^2,
\]
one has
\[
t^5P^{1/6}
=t^7+\lambda t-\frac{10}{3}\lambda^3t^{-11}+\cdots.
\tag{13j}
\]
The missing term belongs to the \(x^9\)-sector.  The first-lower
forcing below belongs to the \(x^{-1}\)-sector.  Operator (8)
preserves Laurent powers of \(x\), so the two terms cannot enter one
recurrence or cancel.

## 2. The universal first-lower target polynomial

The exact seed ratios are
\[
\frac{q_5}{q_6}=-\frac{28}{5},
\qquad
\frac{p_4}{p_5}=-\frac{35}{6},
\qquad
\frac{q_5}{q_6}-\frac{p_4}{p_5}=\frac7{30}.
\tag{14}
\]
For the monomial \(A^jB^{n-j}\), a first-lower replacement can occur
in any of its \(j\) copies of \(A\) or \(n-j\) copies of \(B\).
Therefore its coefficient multiplier is
\[
j\frac{q_5}{q_6}
+(n-j)\frac{p_4}{p_5}.
\tag{15}
\]
It follows that the whole first-lower target polynomial is
\[
\boxed{
P_1(t)
=-\frac{35n}{6}P(t)+\frac7{30}tP'(t).
}
\tag{16}
\]
Thus
\[
V^{(1)}
=x^{4n-1}t^{5n-1}\gamma^{4n-1}P_1(t).
\tag{17}
\]

The exact second-subduction numerator has
\[
U^{(1)}
=-\frac{70}{3}\theta x^{14}t^{19}\gamma^{16}
\tag{18}
\]
as its unique first-lower slice.

Equations (17) and (18) contain every term at graph-weight drop
\(m+4\).  Equivalently, on a maximal sector \(x^I\psi_I(t)\), they
are exactly the terms with loss pair \((a,b)=(1,1)\), hence with
maximal-\(x\) loss \(I+1\).  A \(q_4\) or \(p_3\) seed, two
first-lower replacements, the added \(w\gamma,\gamma\) pieces, and
all other monomials in the exact 77-term \(U\)-numerator have
strictly larger maximal-\(x\) loss.

## 3. Normalized first-lower recurrence

In this section and Section 4, assume that the characteristic
solution (9) is an honest polynomial completion.  Nonpolynomial
characteristics in every degree were already excluded by the exact
maximal-\(x\) separation in Section 1.1.

The first-lower equation is obtained from
\[
J(U^{(1)},V^{(0)})+J(U^{(0)},V^{(1)}).
\tag{19}
\]
Divide by the same nonzero common factor used for the top-top
Jacobian.  Each term has a factor
\(x^{-1}t^{-1}\gamma^{-1}\) times a linear operator on \(\gamma\).
After substituting (9), the characteristic amplitude and the
remaining power of \(\gamma\) cancel.  The dependence is only through
\[
\frac{\gamma_x}{\gamma}=\frac Ix,\qquad
\frac{\gamma_t}{\gamma}
=\frac rt+s\frac{P'}P.
\tag{20}
\]
Hence the amplitude \(c_0\) cancels identically; it is not normalized
to one.

Call the resulting inhomogeneous term
\(\mathcal R_{n,I,P}\).  Both product ratios in (19) are
\[
-\frac{70}{3t},
\qquad
\frac{P_1}{tP},
\tag{21}
\]
respectively.  Each logarithmic Jacobian supplies one additional
factor \(x^{-1}\), so
\[
\mathcal R_{n,I,P}=x^{-1}\rho_{n,I,P}(t).
\tag{22}
\]
The first-lower equation is
\[
\mathcal L_{n,P}(\delta\gamma)
+\mathcal R_{n,I,P}=0.
\tag{23}
\]

The nonzero constant on the desired Jacobian cannot enter this
equation.  The top-top factor removed in deriving (8) is, up to
nonzero \(t\)-dependent factors,
\[
x^{4n+14}\gamma^{4n+16}.
\tag{23a}
\]
On the maximal sector (13b), its \(x\)-exponent is
\[
E_{\rm com}=4n+14+(4n+16)I\ge58.
\tag{23b}
\]
Thus a constant Jacobian right side appears after normalization only
in the sector \(x^{-E_{\rm com}}\), strictly below both the top
\(x^I\)-sector and the first-lower \(x^{-1}\)-sector.

The exponent \(-1\) in (22) is decisive.  Operator (8) preserves
Laurent powers of \(x\), so only the total \(x^{-1}\)-coefficient of
\(\delta\gamma\) can affect (23).  Write it as
\[
\delta\gamma=x^{-1}\psi(t).
\tag{24}
\]
The coordinate substitution \(y=t-x^{-1}\) embeds
\(\mathbb C[x,y]\) in
\(\mathbb C[x,x^{-1},t]\).  Therefore every coefficient of a fixed
Laurent power of \(x\) in a polynomial graph is a polynomial in
\(t\).  In particular,
\[
\psi(t)\in\mathbb C[t].
\tag{25}
\]
Denominators in \(\psi\) cannot cancel against another \(x\)-sector.
A simultaneous homogeneous solution on the \(x^{-1}\)-sector also
cannot change the forcing because it lies in the kernel of
\(\mathcal L_{n,P}\).

## 4. The two local double-pole obstructions

### 4.1. Nonzero constant term

Suppose
\[
P(0)\ne0.
\tag{26}
\]
Then \(P'/P\) is regular at \(t=0\), and (16) gives
\[
\frac{P_1(0)}{P(0)}=-\frac{35n}{6}.
\tag{27}
\]
Keeping the \(t^{-1}\) parts of the two logarithmic determinants in
(19) gives
\[
\begin{aligned}
D_{10}&=-n(I+1),\\
D_{01}&=\frac{17I+15}{4}.
\end{aligned}
\tag{28}
\]
The coefficient of \(x^{-1}t^{-2}\) in the forcing is therefore
\[
\begin{aligned}
-\frac{70}{3}D_{10}
-\frac{35n}{6}D_{01}
=-\frac{35}{24}n(I-1).
\end{aligned}
\tag{29}
\]
Since every graph sector has \(I\ge2\), this is nonzero.

### 4.2. A nonzero root

Now suppose
\[
P(0)=0,\qquad P\ne t^d.
\tag{30}
\]
Then \(P\) has a nonzero root \(\alpha\).  Let its multiplicity be
\(q\), so
\[
1\le q\le d\le n.
\tag{31}
\]
With \(z=t-\alpha\), the local expansions are
\[
\frac{P'}P=\frac qz+O(1),
\qquad
\frac{P_1}{P}=\frac{7\alpha q}{30z}+O(1),
\qquad
\frac{P_1'}{P_1}=\frac{q-1}{z}+O(1).
\tag{32}
\]
The \(U^{(1)}V^{(0)}\) term in (19) has only a simple pole at
\(\alpha\).  The \(U^{(0)}V^{(1)}\) logarithmic determinant has
\(z^{-1}/x\)-coefficient
\[
\frac{(17I+15)(q-4n)}{4n}.
\tag{33}
\]
Combining it with \(P_1/(tP)\) gives the double-pole coefficient
\[
\boxed{
\lim_{t\to\alpha}
(t-\alpha)^2x\mathcal R_{n,I,P}
=
\frac{
7q(17I+15)(q-4n)
}{120n}.
}
\tag{34}
\]
It cannot vanish because \(q\le n<4n\).

For polynomial \(\psi\), operator
\(\mathcal L_{n,P}(x^{-1}\psi)\) has rational coefficients generated
only by
\[
\frac1t,\qquad\frac{P'}P.
\tag{35}
\]
At a root of multiplicity \(q\),
\[
\frac{P'}P=\frac q{t-\alpha}+\text{regular},
\tag{36}
\]
which is still a simple pole.  No derivative of \(\psi\) is divided
by \(P\).  Thus the homogeneous operator has at most simple poles
and cannot cancel (29) or (34).

The two cases exhaust every honest mixed polynomial completion:
either \(P(0)\ne0\), or \(P(0)=0\) and a nonpure \(P\) has a nonzero
root.  Therefore every honest mixed polynomial completion fails on
the first-lower slice \(m+4\).

The cleared fixed source-axis term has drop \(m+2d+2\).  It is not
used here.  For \(d\ge2\) it occurs after the pole obstruction; for
\(d=1\) it lies on the same nominal drop, but the local double pole
already proves failure.  No coefficients from distinct filtration
levels are added.

## 5. Pure faces

If
\[
P(t)=t^d,
\tag{37}
\]
the target face is the pure monomial \(A^dB^{n-d}\).  Substitution
in the exact normalized forcing formula gives
\[
\mathcal R_{n,I,t^d}
=
\frac{7K_{n,d,I}}{120n\,x\,t^2},
\tag{38}
\]
where
\[
\boxed{
K_{n,d,I}
=(n+d)\bigl((17d-25n)I+15d+25n\bigr).
}
\tag{39}
\]
The homogeneous operator
\(\mathcal L_{n,t^d}(x^{-1}\psi)\), with
\(\psi\in\mathbb C[t]\), has coefficients generated only by \(1/t\).
It therefore has at most a simple pole at \(t=0\).  Consequently
every pure face with \(K_{n,d,I}\ne0\) is excluded by the nonzero
double pole in (38).

It remains to classify \(K_{n,d,I}=0\).  Because \(n+d>0\), this is
equivalent to
\[
\boxed{
d(17I+15)=25n(I-1).
}
\tag{40}
\]
Combining (40) with the resonance equation (11) gives
\[
\begin{aligned}
8nJ
&=5n(I-1)+d(17I+15)\\
&=30n(I-1),
\end{aligned}
\tag{41}
\]
so
\[
\boxed{
J=\frac{15(I-1)}4.
}
\tag{41a}
\]
Moreover \(0\le d\le n\) and (40) imply
\[
25n(I-1)
=d(17I+15)
\le n(17I+15),
\tag{41b}
\]
and hence \(I\le5\).  Since a nonconstant graph has \(I\ge2\), the
integrality of \(J\) in (41a) forces \(I\equiv1\pmod4\), hence
\[
\boxed{
I=5,\qquad J=15,\qquad d=n.
}
\tag{41c}
\]
Thus the only pure face not already killed by (38) is \(A^n\), and
its maximal characteristic sector is exactly
\[
\gamma_5=cx^5t^{15},\qquad c\ne0.
\tag{41d}
\]

Substitute \(t=y+x^{-1}\).  The term of \(x\)-exponent one and
largest \(y\)-degree in (41d) is
\[
\boxed{
c\binom{15}{4}xy^{11}=1365c\,xy^{11}.
}
\tag{41e}
\]
It cannot occur in
\(\gamma=1-\frac{57}{34}xy+x^2g\).

There is also no hidden same-monomial cancellation.  Before the
first lower seed tier, any other \(x^K\)-sector must solve the same
pure top characteristic equation.  On \(d=n\) its polynomial
solution is a scalar multiple of
\[
x^Kt^{J_K},
\qquad
J_K=\frac{11K+5}{4}.
\tag{41f}
\]
Such a sector can contain \(xy^{11}\) only if
\[
K-J_K+11=1,
\qquad\text{that is,}\qquad J_K=K+10.
\tag{41g}
\]
Equations (41f) and (41g) give \(K=5\).  Hence (41e) comes uniquely
from the already displayed maximal sector and has nonzero
coefficient.

Here \(m=I+J-2=18\).  The forbidden monomial has
ordinary-filtration drop \(2(I-1)=8\), whereas the first lower seed
tier enters only at drop
\[
m+4=22.
\tag{41h}
\]
Thus the exceptional ray fails before the first-lower recurrence is
even reached.  This closes every pure face, including \(d=0\).

## 6. Constant graphs

Let \(g=z_0\).  In the \((x,t)\)-chart,
\[
\gamma
=1-\frac{57}{34}(xt-1)+z_0x^2
=\frac{91}{34}-\frac{57}{34}xt+z_0x^2.
\tag{42}
\]

If \(z_0\ne0\), the maximal Laurent sector is \(z_0x^2\).
Substitution in (8) gives
\[
\mathcal L_{n,P}(z_0x^2)
=z_0x^2
\left(
\frac{5n}{t}+49\frac{P'}P
\right).
\tag{43}
\]
It cannot vanish: it would force
\[
P(t)=c\,t^{-5n/49},
\tag{44}
\]
which is not a nonzero polynomial for \(n\ge1\).

It remains to take \(z_0=0\).  The maximal sector is then
\(-57xt/34\), with \(I=1\).  The unique characteristic (9) can equal
this sector only if
\[
P(t)=c\,t^{n/4}.
\tag{45}
\]
Thus \(4\mid n\) and the binary face is the pure monomial with
\(d=n/4\).  Apply (8) to the next, fixed \(x^0\)-sector \(91/34\):
\[
\mathcal L_{n,t^{n/4}}\left(\frac{91}{34}\right)
=-\frac{455n}{136t}\ne0.
\tag{46}
\]
At \(I=1\), every non-top monomial in the exact \(U,A,B\) supports
has loss at least two, while (46) occurs after loss one.  Lower seed
terms, affine perturbations, and the constant Jacobian right side
therefore cannot reach this sector.  This excludes every constant
graph.

## 7. Affine perturbations and scope

Use the same maximal sector \(x^I\psi_I(t)\), \(I\ge2\), as in
Section 1.  Relative to \(U^{(0)}\), the top \(A,B\)-terms have
maximal-\(x\) loss
\[
\bigl(15+17I\bigr)-\bigl(4+4I\bigr)=11+13I>I+1,
\tag{52}
\]
and \(C=x\gamma\) lies still lower, with loss \(14+16I\).
Thus an affine first-coordinate perturbation cannot enter either the
top equation or the first-lower equation.

For \(n\ge2\), relative to the homogeneous target tier, affine
\(A,B\)-terms have loss
\[
4(n-1)(I+1)>I+1,
\]
while an affine \(C\)-term has loss
\((4n-1)(I+1)>I+1\).  When \(n=1\), the \(A,B\)-part merely changes
\(Q_1\), and the \(C\)-part has loss \(3(I+1)>I+1\).
Constant additions have zero Jacobian.

For completeness, the exceptional ray of Section 5 is protected
from affine terms in the ordinary filtration as well.  There
\(m=18\), and the leading restricted degrees are
\[
\deg U=375,\qquad
\deg A=90,\qquad
\deg B=89,\qquad
\deg C=21.
\tag{52a}
\]
Thus the \(A^n\) top Jacobian has degree \(90n+373\), while its
forbidden defect has degree \(90n+365\).  For \(n\ge2\),
\[
\begin{aligned}
\deg J(U,A)&=463,&
\deg J(U,B)&=462,&
\deg J(U,C)&=394,\\
\deg J(B,A^n)&\le90n+87,&
\deg J(C,A^n)&\le90n+19,
\end{aligned}
\tag{52b}
\]
and every Jacobian between two affine target terms is lower still.
All are strictly below \(90n+365\).  Hence no affine correction can
cancel (41e).

When \(n=1\), combine the binary part of \(Q_1+S_{\le1}\) before
choosing its leading face.  If its full nonconstant linear part in
\(A,B\) is nonzero, the proof above applies to that combined binary
face; a remaining \(C\)-term lies \(3(I+1)\) below it and cannot
reach the top or first-lower obstruction.  If the binary part
vanishes but a \(C\)-term remains, the unconditional \(C\)-pivot
calculation in
`WEIGHTED_LIFT_FIRST_NONLINEAR_CUSP_SUBDUCTION.md` applies.  If the
entire nonconstant second coordinate vanishes, its Jacobian is zero.

Combining Sections 1--7 proves
\[
\boxed{
J_{x,y}\left(
(U+R_{\le1})\circ F|_{z=g},\
(Q_n+S_{\le1})\circ F|_{z=g}
\right)\notin\mathbb C^\times
}
\tag{53}
\]
for every \(n\ge1\), every nonzero homogeneous binary \(Q_n\), every
polynomial graph \(g\), and arbitrary affine \(R_{\le1},S_{\le1}\).

The accompanying exact verifier is
`verify_weighted_lift_all_degree_binary_target_closure.py`.
