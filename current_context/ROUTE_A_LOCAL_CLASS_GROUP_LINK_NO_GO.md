# Route A: algebraic local class groups do not kill positive-\(b_1\) links

Date: 25 July 2026

## Outcome

Let
\[
S=\operatorname{Spec}
\mathbf C[u,v,w]/(w^2-u-u^2v)
\subset Y
\]
be the Darboux open subset of a hypothetical finite cubic
normalization
\[
\pi:Y\longrightarrow\mathbf A^2,
\qquad R=Y\setminus S.
\]
The boundary localization sequence gives
\[
0\longrightarrow\mathbf Z^r
\longrightarrow\operatorname{Cl}(Y)
\longrightarrow\mathbf Z/2
\longrightarrow0,
\tag{1}
\]
so \(\operatorname{Cl}(Y)\) is finitely generated.  For every
\(p\in Y\), localization is surjective:
\[
\operatorname{Cl}(Y)\twoheadrightarrow
\operatorname{Cl}(\mathcal O_{Y,p}).
\tag{2}
\]
It is tempting to combine (1)--(2) with positive first Betti number of
the link at a boundary singularity and obtain a contradiction.

That implication is false:

> **Algebraic/analytic local-class no-go.** There are isolated normal
> complex algebraic surface hypersurface singularities \(p\in X\) for
> which
> \[
> b_1(\operatorname{Link}(p,X);\mathbf Q)>0
> \quad\text{but}\quad
> \operatorname{Cl}(\mathcal O_{X,p})=0.
> \tag{3}
> \]
> Their completed, henselian, and analytic local Picard groups are
> nevertheless large.

Thus finite generation of the **algebraic Zariski-local** class group
does not remove the positive-\(b_1\) link correction.  The
rational-homology-manifold balance
\[
r+\chi(\Delta)+N_{\rm tr}=2
\tag{4}
\]
remains conditional.

There is a separate improvement.  Under the hypotheses for which
(4) is valid, the apparent equality case consisting of an irreducible
rational nodal branch with normalization \(\mathbf A^1\) and
transitive inertia at every node is impossible.  This does not make
(4) unconditional, but it closes that equality case within the
smooth/rational-homology-manifold regime.

## 1. Why the global algebraic class group is finitely generated

Assume \(R\) has irreducible divisorial components
\(R_1,\ldots,R_r\).  The divisor localization sequence is
\[
B^\times/\mathcal O(Y)^\times
\longrightarrow
\bigoplus_{i=1}^r\mathbf Z[R_i]
\longrightarrow
\operatorname{Cl}(Y)
\longrightarrow
\operatorname{Cl}(S)
\longrightarrow0.
\tag{5}
\]
Here
\[
B^\times=\mathbf C^\times,\qquad
\operatorname{Cl}(S)=\mathbf Z/2.
\]
Since constants already lie in \(\mathcal O(Y)^\times\), the first
map in (5) has zero source quotient.  This proves (1), in particular
finite generation of \(\operatorname{Cl}(Y)\).

For a normal noetherian domain \(A\), the map
\[
\operatorname{Cl}(A)\longrightarrow\operatorname{Cl}(A_{\mathfrak p})
\]
is surjective: a Weil divisor on the localization is the localization
of the closure of its height-one primes in \(\operatorname{Spec}A\).
This proves (2).  Therefore every algebraic local class group occurring
on this \(Y\) is finitely generated.

The flaw in the proposed contradiction is not here.  It is in silently
identifying this algebraic local group with a completed, henselian, or
analytic local Picard group.

## 2. Four different local Picard groups

For an isolated normal surface singularity \(p\in X\), the ordinary
Zariski-local group is
\[
\operatorname{Pic}_{\rm loc}(p,X)
=\operatorname{Pic}
\bigl(\operatorname{Spec}\mathcal O_{X,p}\setminus\{p\}\bigr)
\simeq\operatorname{Cl}(\mathcal O_{X,p}).
\tag{6}
\]
One must distinguish it from

1. the étale-local or henselian group
   \[
   \operatorname{Pic}
   \bigl(\operatorname{Spec}\mathcal O^h_{X,p}\setminus\{p\}\bigr);
   \]
2. the completed group
   \[
   \operatorname{Cl}(\widehat{\mathcal O}_{X,p});
   \]
3. the Picard group of a punctured analytic neighborhood.

Kollár explicitly warns that the ordinary local group maps to the
étale-local group neither injectively nor surjectively in general, and
that even isolated complex singularities can have ordinary local
Picard group zero while their étale-local Picard group is large.  He
also records that the ordinary group injects into the complex points
of the local Picard scheme but usually does not surject; the
identification with all complex points holds in the henselian or
complete setting.

References:

- J. Kollár, *Maps between local Picard groups*, Algebraic Geometry 3
  (2016), Definition 3.1 and Section 3.5:
  <https://content.algebraicgeometry.nl/2016-4/2016-4-022.pdf>.
- In particular, see pp. 466--468, including the statements
  \(\operatorname{Pic}_{\rm loc}\ne
  \operatorname{Pic}_{\rm et-loc}\) in general and
  \[
  \operatorname{Pic}_{\rm loc}(p,X)
  \hookrightarrow
  \mathbf{Pic}_{\rm loc}(p,X)(\mathbf C).
  \tag{7}
  \]

The local Néron--Severi quotient of the Picard scheme is finitely
generated in characteristic zero.  The non-finite-generation relevant
to positive-\(b_1\) links lies in the positive-dimensional identity
component, not in this discrete quotient.

## 3. Where the large analytic group comes from

Take a good resolution
\[
f:\widetilde X\longrightarrow X
\]
with simple-normal-crossing exceptional curve
\[
E=\bigcup_i E_i
\]
and dual graph \(\Gamma\).  Put \(g_i=g(E_i)\).  The plumbing
calculation gives
\[
b_1(\operatorname{Link}(p,X);\mathbf Q)
=2\sum_i g_i+b_1(\Gamma).
\tag{8}
\]
The generalized Jacobian of the exceptional curve has an exact
sequence
\[
1\longrightarrow(\mathbf C^\times)^{b_1(\Gamma)}
\longrightarrow\operatorname{Pic}^0(E)
\longrightarrow\prod_i\operatorname{Jac}(E_i)
\longrightarrow1.
\tag{9}
\]
Consequently
\[
\dim\operatorname{Pic}^0(E)
=\sum_i g_i+b_1(\Gamma),
\tag{10}
\]
so (8) being positive forces a positive-dimensional generalized
Jacobian.

In the completed or analytic local problem, line bundles on \(E\)
lift through its infinitesimal neighborhoods: the obstruction groups
are \(H^2\) of coherent sheaves on a curve and vanish.  The resolution
description of the local Picard group then quotients by the discrete
lattice generated by the \(E_i\).  Such a lattice cannot kill the
positive-dimensional group (9).  Thus the completed/analytic local
Picard group has a non-finitely-generated group of complex points.

This is precisely the information detected by the link.  It says
nothing by itself about how much of that group is represented by
divisors on one fixed algebraic Zariski neighborhood.

## 4. A citation-grade UFD counterexample

Consider the simple elliptic Hesse cone
\[
X_{\rm H}
=V(z^3+3xyz+x^3+y^3)
\subset\mathbf A^3.
\tag{11}
\]
Its projectivization is a smooth plane cubic \(E\).  The cone is
normal with one isolated singularity at the vertex.  Its link is the
circle bundle of Euler number \(-3\) over \(E\), so the Gysin sequence
gives
\[
b_1(\operatorname{Link}(0,X_{\rm H});\mathbf Q)
=b_1(E;\mathbf Q)=2.
\tag{12}
\]
The completed/analytic local Picard group contains
\(\operatorname{Pic}^0(E)(\mathbf C)\simeq E(\mathbf C)\), hence is not
finitely generated.

Brevik--Nollet prove:

> If
> \[
> A=\mathbf C[[x_1,\ldots,x_n]]/(f),
> \]
> where the polynomial \(f\) defines a variety normal at the origin,
> then there is an algebraic hypersurface \(X\subset\mathbf P^n\) and
> \(p\in X\) such that \(\mathcal O_{X,p}\) is a UFD and
> \[
> \widehat{\mathcal O}_{X,p}\simeq A.
> \tag{13}
> \]

This is Theorem 1.2 of J. Brevik and S. Nollet, *Local Picard Groups*:
<https://arxiv.org/abs/1110.1867>.

Apply the theorem to the Hesse polynomial (11).  The resulting
essentially finite-type complex local hypersurface ring
\[
\mathcal O_{X,p}
\]
is a UFD, hence
\[
\operatorname{Cl}(\mathcal O_{X,p})=0,
\tag{14}
\]
while its completion is the Hesse completion.  For isolated complex
hypersurfaces the formal type is finitely determined; equivalently in
this construction, the Mather--Yau step preserves the analytic
singularity type.  Therefore its link still has \(b_1=2\).

Equations (12)--(14) give (3).  They also exhibit the strongest possible
failure of surjectivity:
\[
0=\operatorname{Cl}(\mathcal O_{X,p})
\longrightarrow
\operatorname{Cl}(\widehat{\mathcal O}_{X,p}),
\]
with a large target.

This counterexample does not assert that the Brevik--Nollet
algebraization is itself finite cubic over a smooth plane.  It proves
that finite generation of the algebraic local class group, by itself,
cannot exclude a positive-\(b_1\) link.  Any successful refinement must
use the special rank-three algebra or branch geometry, not just
localization of divisor classes.

## 5. Rational nodal branch: exact monodromy count

Now assume the smooth or rational-homology-manifold hypotheses under
which (4) is valid.  Let the branch curve \(\Delta\) be irreducible,
rational, nodal, with normalization
\[
\nu:\mathbf A^1\longrightarrow\Delta,
\]
and let it have \(\delta\) ordinary nodes.  Identifying two points of
the normalization at each node gives
\[
\chi(\Delta)=1-\delta.
\tag{15}
\]

At a node \(p\), let \(\tau_p,\sigma_p\in S_3\) be the transpositions
around its two local branches.  There are exactly two cases:

\[
\begin{array}{c|c|c}
\tau_p,\sigma_p&
\langle\tau_p,\sigma_p\rangle&
o_p\\ \hline
\tau_p=\sigma_p&C_2&2,\\
\tau_p\ne\sigma_p&S_3&1.
\end{array}
\tag{16}
\]

Let
\[
k=\#\{p:\tau_p\ne\sigma_p\}.
\]
Then \(N_{\rm tr}=k\), and (4) becomes
\[
r=2-\chi(\Delta)-N_{\rm tr}
=1+\delta-k.
\tag{17}
\]
The coarse inequality is
\[
c(\Delta)+\chi(\Delta)+N_{\rm tr}
=2-\delta+k\le2.
\tag{18}
\]
Equality holds exactly when every node is transitive:
\[
k=\delta.
\tag{19}
\]

## 6. The nodal equality case is conditionally impossible

Assume \(\delta>0\) and (19).  Equation (17) forces
\[
r=1.
\tag{20}
\]
Let \(E_{\rm ram}\) be the unique ramified boundary prime dominating
\(\Delta\).  It is unique because the generic simple branch has one
ramified orbit.  At a smooth point of \(\Delta\), the fiber of
\[
E_{\rm ram}\longrightarrow\Delta
\]
has one point.  At every node, transitivity in (19) says that the
entire normalized cubic fiber has one point, so the ramified boundary
fiber again has one point.  Euler integration by fiber cardinality
therefore gives
\[
\chi(E_{\rm ram})=\chi(\Delta)=1-\delta.
\tag{21}
\]

There are no isolated boundary components.  Indeed, if a normal affine
surface \(Y\) had an affine open \(S\) whose complement had an isolated
point component \(q\), choose an affine neighborhood \(W\) meeting the
complement only at \(q\).  Since \(Y\) is separated, \(W\cap S\) is
affine.  Normality and codimension-two Hartogs extension give
\[
\Gamma(W\setminus\{q\},\mathcal O)=\Gamma(W,\mathcal O),
\]
which is impossible if both are affine and one is a proper open subset
of the other.  Thus the boundary is pure of dimension one.

By (20), the whole boundary is set-theoretically
\[
R=E_{\rm ram}.
\]
Combining (21) with the duality conclusion
\[
\chi(R)=r=1
\]
gives
\[
1-\delta=1,
\]
contrary to \(\delta>0\).

Hence:

> **Conditional nodal exclusion.** If \(Y\) is smooth, or a rational
> homology four-manifold, then an irreducible rational branch with
> normalization \(\mathbf A^1\) cannot have a positive number of nodes
> all carrying distinct-transposition, transitive local inertia.

Nodes with equal local transpositions do not satisfy the equality case:
then \(k<\delta\) and (17) requires extra boundary components.  The
present argument does not exclude those configurations.  More
importantly, it does not exclude the all-transitive nodal configuration
when \(Y\) has positive-\(b_1\) singularity links, because then the
duality identity \(\chi(R)=r\) is exactly what fails.

## 7. Consequence for the research route

The hoped-for implication
\[
\operatorname{Cl}(Y)\ \text{finitely generated}
\quad\Longrightarrow\quad
b_1(\operatorname{Link}(p,Y);\mathbf Q)=0
\]
is false, even after passing to the algebraic local class group.
Therefore the smooth-normalization Euler balance cannot be made
unconditional by a bare class-group argument.

The next viable local direction must exploit structure absent from the
UFD algebraization theorem, for example:

1. classify isolated singularities of **finite flat rank-three**
   algebras over a smooth two-dimensional base and compute whether
   their positive-dimensional completed local Picard subgroup
   algebraizes inside that restricted category;
2. use the two trace-zero generators and Miranda triple-cover equations
   to constrain the resolution graph and its genera;
3. combine the branch conductor with the distinguished open
   \(S\subset Y\), rather than using \(\operatorname{Cl}(Y)\) alone.

This is a no-go result for one proposed shortcut, not a proof of the
Jacobian conjecture and not independently publishable as a new theorem.
