# Route A: the singular line image has dicritical index one

Date: 25 July 2026

## Outcome

Let
\[
S=\operatorname {Spec}
\mathbf C[u,v,w]/(w^2-u-u^2v)
\]
and let
\[
\pi_2:\mathbf A^2_{a,b}\longrightarrow S,\qquad
u=a^2,\quad
w=a(1+2a^2b),\quad
v=4b(1+a^2b).
\tag{1}
\]
Suppose that \(e:S\to\mathbf A^2\) is an etale map of geometric
degree three, and put
\[
H=e\circ\pi_2=(H_1,H_2).
\tag{2}
\]
Then \(H\) is a plane Keller map of geometric degree six.  Let
\[
L=V(a),\qquad
\gamma(b)=H(0,b),\qquad
\Gamma=\overline{\gamma(\mathbf A^1)}.
\]
Assume, as established in the collision route, that \(\gamma\) is
finite and birational.

This audit gives three exact conclusions.

1. \(\Gamma\) is itself an irreducible component of the nonproper-value
   set \(A_H\).
2. Its distinguished Newton--Puiseux class has
   \[
   \boxed{m_\varphi=2,\qquad n_\varphi=5,\qquad i_\varphi=1.}
   \tag{3}
   \]
   In particular, the tempting value \(i_\varphi=2\), which would
   strengthen several degree counts, is wrong.
3. If
   \[
   m_i=\deg_bH_i(0,b),\qquad d_i=\deg_{a,b}H_i,
   \]
   then Chau's dicritical degree-ratio theorem and the invariant-ring
   filtration give
   \[
   \boxed{\frac{d_1}{d_2}=\frac{m_1}{m_2},
   \qquad d_i\geq4m_i.}
   \tag{4}
   \]
   Thus \(d_i=\lambda m_i\) for a common rational
   \(\lambda\geq4\).

There is no contradiction with geometric degree six.  Total polynomial
degree \(d_i\), geometric degree \(6\), Puiseux multiplicity
\(m_\varphi=2\), Puiseux index \(i_\varphi=1\), and the degree-one
normalization map \(L\to\Gamma\) are different invariants.  The standard
degree-ratio theorem relates only the two ratios in (4).  The explicit
chart below shows that the distinguished dicritical germ is unramified,
even at a nodal self-identification.  In Orevkov's geometric-degree
defect formula, this class contributes exactly \(1\) to
\(\deg_{\rm geo}H-1=5\); all other dicritical classes must contribute
the remaining \(4\).  Hence the singular case survives this route, but
with a sharp residual budget.

## 1. The deck involution makes \(\Gamma\) nonproper

On \(D(a)\), the quadratic chart (1) has deck involution
\[
\sigma(a,b)=(-a,-b-a^{-2}).
\tag{5}
\]
Direct substitution gives
\[
\pi_2\circ\sigma=\pi_2,
\qquad H\circ\sigma=H.
\tag{6}
\]

Fix \(b_0\in\mathbf C\) and take \(a\to0\) through nonzero values.
Then
\[
\sigma(a,b_0)\longrightarrow\infty,\qquad
H(\sigma(a,b_0))=H(a,b_0)\longrightarrow H(0,b_0).
\]
Therefore every point of \(\gamma(\mathbf A^1)\) is a nonproper value
of \(H\).  Since \(\Gamma\) is an irreducible curve and \(A_H\) is an
algebraic curve,
\[
\boxed{\Gamma\text{ is an irreducible component of }A_H.}
\tag{7}
\]

This justifies applying the nonproper-component theorems directly to
the distinguished line image; it is not merely a curve meeting
\(A_H\) in finitely many points.

## 2. Exact Newton--Puiseux class

For the generic-projection convention, choose
\[
x=-b-\kappa a,\qquad y=a
\]
with generic \(\kappa\).  The kernel direction of \(x\) may then be
chosen away from the zeros of the two top homogeneous coordinate
forms, so the usual monicity convention is available.  Along
\(\sigma(s,b_0)\),
\[
x=s^{-2}+b_0+\kappa s,\qquad y=-s.
\]
Inverting this expansion shows that the relevant branch at infinity
has, up to nonzero rescaling of its free parameter, the truncated
series
\[
y=-x^{-1/2}+\eta x^{-3/2}.
\tag{8}
\]
The fixed term contributed by \(\kappa\) occurs only after the displayed
free-parameter term and does not change \(m_\varphi,n_\varphi\), or
\(i_\varphi\).

For an exact polynomial chart we may set \(\kappa=0\).  With
\(x=t^{-2}\), the original \((a,b)\)-coordinates are then
\[
\Theta(t,\eta)=
\left(-t+\eta t^3,\,-t^{-2}\right).
\tag{9}
\]
The first nonintegral exponent in (8) is \(-1/2=1-3/2\), and the
free parameter occurs at
\(-3/2=1-5/2\).  Hence
\[
m_\varphi=2,\qquad n_\varphi=5.
\]
The zero-parameter series \(\varphi(x,0)=-x^{-1/2}\) still has
multiplicity two.  In Chau's convention,
\[
i_\varphi=
\frac{m_\varphi}{\operatorname {mult}(\varphi(x,0))}
=\frac22=1,
\]
which proves (3).  The class has two conjugate representatives, but
that class size is not the index.

The parameter really is the normalization parameter on \(\Gamma\).
Put \(z=1-\eta t^2\).  Substitution of (9) into the three invariant
generators gives polynomials:
\[
\begin{aligned}
u_\Theta&=t^2z^2,\\
v_\Theta&=-8\eta+4\eta^2t^2,\\
w_\Theta&=tz(2z^2-1).
\end{aligned}
\tag{10}
\]
They satisfy \(w_\Theta^2-u_\Theta-u_\Theta^2v_\Theta=0\).
Consequently
\[
\widehat H(t,\eta)
:=H(\Theta(t,\eta))
=e(u_\Theta,v_\Theta,w_\Theta)
\tag{11}
\]
extends polynomially across \(t=0\), and
\[
\widehat H(0,\eta)
=e(0,-8\eta,0)
=\gamma(-2\eta).
\tag{12}
\]
Thus the dicritical parametrization is birational onto \(\Gamma\), as
is the original map \(L\to\Gamma\).

There is also no hidden ramification in this chart.  On \(t\ne0\),
\[
\det\frac{\partial(-t+\eta t^3,-t^{-2})}
{\partial(t,\eta)}=-2.
\tag{13}
\]
If \(J(H)=c\ne0\), polynomial continuation gives
\[
J(\widehat H)=-2c
\tag{14}
\]
on all of \(\mathbf A^2_{t,\eta}\).  The dicritical germ along \(t=0\)
is therefore etale.

Notice that \(\widehat H\) has geometric degree twelve, not six:
\(\mathbf C(t,\eta)/\mathbf C(a,b)\) defined by (9) has degree two
because \(t^2=-1/b\), and the tower with
\(\mathbf C(a,b)/\mathbf C(H_1,H_2)\) has degree six.  This is a useful
warning against reading the denominator \(m_\varphi=2\) or the chart
(11) as a degree-six contribution formula.

## 3. The exact invariant-ring degree filtration

Every element \(F\in\mathbf C[S]\) has a unique reduced expression
\[
F=A(u,v)+wC(u,v).
\tag{15}
\]
For a monomial in the first summand of (15), its pullback through
\(\pi_2\) has leading ordinary homogeneous monomial
\[
u^iv^j\longmapsto
4^j a^{2i+2j}b^{2j},
\qquad \deg=2i+4j.
\tag{16}
\]
For a monomial in the second summand,
\[
wu^iv^j\longmapsto
2\cdot4^j a^{3+2i+2j}b^{1+2j},
\qquad \deg=4+2i+4j.
\tag{17}
\]
The exponent pairs in each family determine \((i,j)\) uniquely, and
the two families cannot meet because their \(b\)-exponents have
opposite parity.  Hence no leading monomial in (16)--(17) can cancel.
It follows that
\[
\deg_{a,b}\pi_2^*F
=
\max\left\{
2i+4j:a_{ij}\ne0,
\qquad
4+2i+4j:c_{ij}\ne0
\right\}.
\tag{18}
\]

On \(L\), only \(A(0,4b)\) remains.  If its degree is \(m\), the term
\(v^m\) occurs in \(A\), and (18) yields
\[
\deg_{a,b}\pi_2^*F\geq4m.
\tag{19}
\]

By (7), Chau's theorem applies to \(\Gamma\).  The polynomial
parametrization supplied by a dicritical series may cover the
normalization more than once, but that multiplies both coordinate
degrees by the same integer.  Since \(\gamma\) is birational, the ratio
is unchanged, and
\[
\frac{m_1}{m_2}
=\frac{\deg H_1}{\deg H_2}.
\tag{20}
\]
Equations (19)--(20) prove (4).

## 4. Exact geometric-degree defect budget

Chau's 1999 paper records Orevkov's formula, in Newton--Puiseux
notation,
\[
\deg_{\rm geo}H-1
=
\sum_{[\psi]\in\Pi_H}
\frac1{i_\psi}
\left[
\deg_{(0,0)}H_\psi+
\sum_{\substack{d\in E_\psi\\d\ne0}}
\bigl(\deg_{(0,d)}H_\psi-\mu_\psi\bigr)
\right].
\tag{21}
\]
Here \(H_\psi\) is the two-variable polynomial obtained from the
Puiseux chart, \(\mu_\psi\) is its generic local degree along the
dicritical line, and \(E_\psi\) is the exceptional set of the
one-variable parametrization.

For the distinguished class \([\varphi]\), the polynomial \(H_\varphi\)
is exactly \(\widehat H\) in (11), up to the harmless generic linear
choice used before (8).  Equation (14) makes every local degree of
\(\widehat H\) equal to one.  Therefore
\[
i_\varphi=1,\qquad
\deg_{(0,d)}H_\varphi=\mu_\varphi=1
\quad\text{for every }d,
\]
and the entire summand of (21) is
\[
\boxed{1.}
\tag{22}
\]

Since \(\deg_{\rm geo}H=6\), formula (21) now gives the exact residual
condition
\[
\boxed{\quad
\sum_{[\psi]\ne[\varphi]}
\operatorname {defect}([\psi])=4.
\quad}
\tag{23}
\]
In particular, other dicritical classes are mandatory.  They may map
to other components of \(A_H\), or several classes may map to the same
component, so (23) does not by itself count irreducible nonproper
curves.

The numbers are naturally compatible with the tower
\[
\deg_{\rm geo}(\pi_2)=2,\qquad \deg_{\rm geo}(e)=3:
\qquad
6-1=(2-1)+2(3-1)=1+4.
\tag{24}
\]
Equation (24) is only an arithmetic interpretation, not a
componentwise factorization theorem for Orevkov's summands.  It
nevertheless shows why the exact remainder \(4\) is not anomalous.

## 5. Why the hoped-for degree-six contradiction fails

The self-identification forced by Gwozdziewicz gives distinct
\(\eta_1,\eta_2\) with
\[
\widehat H(0,\eta_1)=\widehat H(0,\eta_2).
\]
Equation (14) says that \(\widehat H\) is locally biholomorphic at both
source points.  The two smooth normalization branches form a singular
target germ, and the local inverse of the other target branch supplies
an additional source branch through each point.  This is exactly the
mandatory extra component of \(H^{-1}(\Gamma)\); it is compatible with
local etaleness.

Thus the route does not close:

- the factor \(2\) is the Puiseux multiplicity, not the Puiseux index;
- the index is \(1\), so no extra index divisor enters Chau's ratio;
- (4) constrains total coordinate degrees, not geometric degree;
- the distinguished class consumes only \(1\) of the available
  geometric-degree defect \(5\), leaving the compatible budget (23);
- the explicit dicritical chart is etale and models a nodal
  self-identification without local ramification.

The sharp surviving normal form is (8)--(14).  Any further contradiction
must couple this unramified index-one chart to a genuinely global
invariant: the finite degree-six sheet budget, the full collection of
dicritical components, or the cubic normalization monodromy.  Reusing
the degree ratio or multiplying by \(m_\varphi=2\) cannot do it.

## 6. References and verification

The degree-ratio input is Theorem 4.4(E1), and the defect formula is
equation (4.10), of Nguyen Van Chau,
*Non-zero constant Jacobian polynomial maps of \(\mathbf C^2\)*,
Ann. Polon. Math. **71** (1999), 287--310
([journal PDF](https://matwbn.icm.edu.pl/ksiazki/apm/apm71/apm7135.pdf)).

The definitions
\[
m_\varphi,\quad n_\varphi,\quad
i_\varphi=m_\varphi/\operatorname {mult}(\varphi(x,0))
\]
are those in the same paper.

Run

```sh
.venv/bin/python current_context/verify_route_a_singular_dicritical_index_audit.py
```

for the deck-invariance, polynomial-chart, hypersurface-relation,
Jacobian, restriction, and leading-monomial checks.
