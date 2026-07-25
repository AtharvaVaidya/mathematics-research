# Publication and strategy audit

Date: 24 July 2026

> **Later audit notice.**  The current consolidated assessment is
> `STATUS_AND_PIVOT_2026-07-24.md`.  In particular, the outer
> Davenport--Zannier family and Catalan count are classical (Zannier 1995),
> and the fixed-cusp covering pivot proposed below has been superseded:
> cusp-compatible full a/b and case-c strata are now excluded by short
> valuation arguments, so the active route studies the actual non-cusp
> asymptotic curve and its boundary tree.
>
> **25 July update.**  The final a/b \((3,5)\) cell is now empty over
> \(\mathbf Q\) by the exact Wronskian/radical verifier, and the two
> remaining generic case-c charts are empty at deficit seven over the
> complete five-point outer fiber.  See the consolidated status and the
> two new verifier notes for the corrected, smaller proof.

## Bottom line

The plane Jacobian conjecture has **not** been resolved here.  There is
neither a complex counterexample nor a proof of \(JC(2)\).

There is, however, one substantial bounded elimination which appears capable
of becoming a publishable theorem after independent reproduction:

> **Candidate bounded theorem.**  Neither of the two reduced coefficient
> systems attached by Guccione--Guccione--Horruitiner--Valqui to the remaining
> degree pair \((72,108)\) has a point over \(\mathbf C\) with all required
> Newton vertices nonzero.

Taken together with the published reduction in
[GGHV 2022](https://arxiv.org/abs/2204.14178), this would eliminate the last
degree pair below \(125\), so that a complex plane Keller counterexample would
have maximum coordinate degree at least \(125\).  This is the strongest
apparently new result in the workspace.  “Apparently new” is deliberate:
publication requires a complete literature check, independent verification
of the correspondence with the published reduction, and archival exact
certificates.

The best conceptual companion result is a uniform solution of the linear
radial deformation problem.  It replaces scale-by-scale matrix calculations
by a scalar-potential formula and proves the stable seven-mode profile
\[
(1,1,2,2,3,3,4)
\]
at every radial scale.  The remaining obstruction is nonlinear and
finite-dimensional.  This is the main direction selected below.

## 1. Results ranked by publication readiness

### Tier I: a theorem-sized bounded advance

The complete \((72,108)\) elimination in `ROUTE_B_FULL_MEMO.md` has the
following exact structure.

1.  The outer equation is
    \[
    UV+2wUV'-3wU'V=1,\qquad \deg U=7,\quad\deg V=10.
    \]
    It defines degree-\(21\) Belyi maps with passport
    \[
    (2^{10},1),\qquad(3^7),\qquad(17,1^4).
    \]
    An exact Murnaghan--Nakayama character calculation gives Hurwitz number
    five.
2.  Modulo \(32003\), the normalized outer algebra is reduced of length
    five: two rational points and one irreducible cubic factor.  Saturation
    proves this covers every geometric outer point and preserves all required
    vertices.
3.  Over each exact field factor, the full lower a/b system has only its
    affine origin.  This is a \(25+47\)-variable support calculation, not a
    sample of selected leading polynomials.
4.  The full case-c branch is treated independently.  Its outer equation is
    the same Hurwitz problem; all \(165\) lower coefficients reduce exactly
    to seven weighted parameters.  Over all rational and cubic outer factors,
    the modular ideal has only the origin.
5.  Prime-to-\(p\) tame specialization transports the five outer covers, and
    properness of the weighted projectivization prevents a nonzero lower
    solution from disappearing in specialization.

The arithmetic and symbolic verifiers pass, including a direct algebraic
closure run in Singular.  This is much stronger than a heuristic modular
search, but the following external checks are still mandatory before
submission:

- reproduce every computation on a clean machine and archive the Gröbner
  bases, coefficient fields, hashes, and software versions;
- have an independent reader verify that the two implemented supports and
  all “required vertex” localizations are exactly the two alternatives in
  the published reduction;
- rewrite the tame-specialization argument in stack-free or explicitly
  stack-theoretic language, including triviality of automorphisms;
- check the integral weighted-projective closure and the properness
  specialization lemma scheme-theoretically;
- ask the authors of the degree-\(108\) reduction whether the remaining
  system has been eliminated elsewhere or whether any normalization caveat
  is missing.

Subject to those checks, this should be written first as a focused
computational-algebra paper.  It should not be mixed with a claim to settle
\(JC(2)\).

### Tier II: clean structural results

#### Universal outer Belyi/Kummer description

For coprime \(m<n\), \(p=mk+1\), and \(q=nk+1\), the leading equation is
\[
(n-m)UV+mwUV'-nwU'V=E\ne0.
\]
It gives
\[
R=w^{n-m}\frac{V^m}{U^n},\qquad
\frac{R'}R=\frac{E}{wUV},
\]
an explicit three-point-cover passport, an exact all-scale normal form at
infinity, and Kummer logarithmic connections for every lower layer.  This
turns an apparently large coefficient system into a finite Hurwitz problem
plus a filtered deformation problem.  The identities are exact and
reproducible.  Novelty must still be checked against the
Davenport--Zannier, polynomial \(abc\), logarithmic-derivation, and dessin
literatures.

#### Uniform seven-mode linear theorem

For the consecutive \((m,n)=(2,3)\) radial family, let \(d\) be the deficit,
\(c=5-d\), and \(E=UV+2wUV'-3wU'V\).  Every bounded kernel pair is uniquely
represented by
\[
C=\frac{2UB-3VA}{E}.
\]
For \(c\ne0\), an inverse is
\[
\begin{aligned}
A_C&=\frac{cwCU'+(d-3)CU-2wC'U}{c},\\
B_C&=\frac{cwCV'+(d-2)CV-3wC'V}{c}.
\end{aligned}
\]
The key exact identities are
\[
\mathcal K_d(A_C,B_C)=wCE'=0,\qquad
2UB_C-3VA_C=EC,\qquad
\mathcal K_d(2UT,3VT)=cET.
\]
Endpoint and indicial analysis, together with the high-order Belyi contact,
then gives for every \(k\ge1\)
\[
\dim\ker\mathcal L_d=
\begin{cases}
2,&d=1,2,3,\\
1,&d=4,\\
0,&d\ge5.
\end{cases}
\]
This proves, rather than extrapolates, the seven weights
\((1,1,2,2,3,3,4)\).  The proof and symbolic verifier are in
`ROUTE_B_FULL_MEMO.md` and
`route_bd_universal_radial_kernel_theorem.py`.

Independent review should focus on the converse using
\(\gcd(U,V)=1\), the resonant \(d=5\) endpoint, and the support effect of
subtracting the constant or affine part of the common formal polynomial
solution.  This theorem is the cleanest conceptual candidate for a companion
note.

The scalar potential has an exact symplectic meaning, which further improves
the result.  With \(E=1\),
\[
P_0=z^2U/w,\qquad Q_0=z^3V/w,\qquad
dP_0\wedge dQ_0=\frac{z^4}{w^3}\,dz\wedge dw.
\]
For \(c=5-d\), the Hamiltonian
\[
H_{d,C}=-\frac{z^cC(w)}{cw}
\]
generates exactly the kernel deformation \((A_C,B_C)\).  Its formal flow
preserves the full bracket to every order.  Moreover, these potentials form
an explicit graded Lie algebra: if \(f=5-e\) and \(g=5-d-e\), then
\[
C\star D=-gw\left(
\frac{(wC'-C)D}{c}
+\frac{C(D-wD')}{f}
\right).
\]
Thus the nonlinear equations are not mysterious formal
Maurer--Cartan obstructions.  They record the first point at which an exact
Hamiltonian flow escapes the bounded Newton support.  This reframing is both
cleaner and more promising than transporting an abstract filtered
\(L_\infty\) structure.

One important limitation is already rigorous.  The four high principal
Hamiltonians are powers of the same monomial \(\xi=zw^k\), so their leading
brackets vanish.  The outer contact identity makes all their polynomial
terms powers of one common formal coordinate, so even the successive common
tails cancel; the first information lies in the pieces discarded at the
opposite boundary.  Moreover, exact \(k=1,2\) tests show that the naive
filtration by outer \(C\)-degree has initial ideal only
\(\langle X_1^4\rangle\).
Accordingly, no claim of a scale-independent triangular obstruction should
be made until a successive-tail or two-boundary argument is proved.

The outer boundary cover does have trivial deck group for every \(k\) in
the \((2,3)\) family: its unique simple zero and unique high-ramification
point force every deck transformation to be the identity.  This is a useful
rigidity lemma, but it is not yet a nonlinear obstruction because a bounded
completion has not been proved to extend to an automorphism of that cover.
Conditional on the stronger ring descent \(P,Q\in K[P_0,Q_0]\), weighted
degree and one forbidden \(w^{-1}\) endpoint force the normalized pair to
equal \(P_0,Q_0\).  This isolates ring descent as the exact missing theorem.
The standard countermodel \(K(t)/K(t^3+t)\), which has degree three and
trivial deck group, shows why deck rigidity alone cannot establish it.

The most promising new computational invariant is the endpoint mismatch
triple
\[
Y_0=X_0-2X_1,\quad Y_2=X_2-\tfrac23X_3,\quad Y_3=X_4-X_5.
\]
All complete \(k=1,2,3\) fibers contain
\((Y_2-(4k+1)^2Y_0^2/(16k))^2\) at weight four and \(Y_3^2\) on
\(Y_0=Y_2=0\) at weight six.  This should be presented only as an
all-\(k\) conjectural pattern until a symbolic endpoint derivation is
available.  The more elaborate common-\(G\) factorization at \(k=1\)
provably fails at \(k=2,3\).

The \(d+e=5\) Kummer resonance supplies a more robust **conditional**
obstruction.  Its five nonzero translation polynomials have rank five
over every complete \(k=1,2,3\) outer fiber.  If an exact ordered rational
factorization through weight five isolates the resonant translation
factor, rationality of that factor forces
\[
X_0X_6=X_1X_6=X_2X_5=X_3X_4=X_3X_5=0
\]
for that factorized lift past the first resonance.  Rationality of a
composite time-one map does not by itself imply rationality of this
leading logarithmic flow, even after lower-weight factors are rationally
removed.  At the actual \(k=3\)
scale the fixed endpoint determinant is a unit on the localized Hurwitz
algebra, so the rank calculation for the conditional obstruction is
branch-independent in characteristic zero.  The all-\(k\) determinant is
an endpoint jet Wronskian; its nonvanishing is not implied by the local
ODE and remains a global passport problem.

The resulting monomial ideal has six minimal coordinate strata: combine
\(X_6=0\) or \(X_0=X_1=0\) with one of
\[
X_4=X_5=0,\qquad X_3=X_5=0,\qquad X_2=X_3=0.
\]
They should not be attacked by generic elimination.  Each contains exact
algebraic Hamiltonian flows: the low axes give square/cube roots, and the
high principal flow has a \((5k+2)\)-nd-root binomial.  The endpoint
relations identify the matched sectors as
\[
-(P_0^2-x^2)/4,\qquad -(Q_0-x^2y)/3,\qquad -(P_0-x)/2.
\]
This reduces four strata to two-generator matched sectors, but it does not
give an unconditional rational obstruction because higher Hamiltonians can
alter the composite time map.  The source-integrality theorem is stronger:
once graph finiteness is known, it eliminates all six simultaneously.

#### Chebyshev/Danielewski chart obstruction

On \(S:x^2y=z^2-1\), every Chebyshev étale endomorphism of degree \(d>1\)
fails to preserve the complement of every affine-line divisor
\(E\subset S\) for which \(S\setminus E\simeq\mathbf A^2\).  Consequently,
no surface-automorphism conjugate of the Chebyshev family descends to a
polynomial plane Keller map.  The proof uses semiconjugacy in the
\(z\)-coordinate and the exact Picard group of \(S\), rather than testing a
finite automorphism ansatz.  This is a focused all-degree no-go theorem for
one construction architecture, not evidence for all of \(JC(2)\).

### Tier III: useful research infrastructure, not yet a paper headline

- The standard-system equations have an exact weighted compactification.
  Every hypothetical Keller section must escape to weighted infinity with
  equation-Jacobian order \((m-1)(n-1)\), and the first boundary cone is the
  common-root cone \(\Gamma^g=R\).
- The homogenized Keller identity
  \[
  \tau(P_XQ_\tau-P_\tau Q_X)+nPQ_X-mQP_X=-c\tau^{m+n-2}
  \]
  gives an exact branchwise residue condition.  This identifies the missing
  normal-form lemma but does not prove it.
- The fixed-source-plane ring
  \[
  R=\mathbf Q[t+t^2-ct^3,\,2+4t-3ct^2,\,c]
  \]
  has an exact built-in collision.  A Darboux pair in this ring would be a
  plane counterexample.  Its image hypersurface, normalization, conductor,
  Liouville form, and many all-degree Hamiltonian no-go families have been
  determined exactly.
- The characteristic-\(3\) pseudo-plane construction gives an exact
  noninjective Keller pair in characteristic \(3\) and an unbounded
  \(3\)-adic deformation tower, but degree growth prevents this from being a
  characteristic-zero counterexample.

These are valuable constraints and reusable calculations.  None presently
crosses the threshold to a proof or complex counterexample.

The sharp next standard-system question is not another resultant.  It is a
graded local Brieskorn/vanishing-cycle lemma at each
\(A_{a-1}\) common-root cluster: after quotienting the explicit
\(g\)-sector approximate-root gauge, the final order-\(N\) forcing should
have a nonzero class in the leading
\(\Omega^1/(d\mathcal O+\mathcal O\,dP)\) piece.  A naive Milnor quotient
does not suffice—the exact \(g\)-sector countermodels survive there—so the
quotient must remember the coupled \((P,Q)\) deformation or use the
saturated Kummer gauge.  Until that quotient is constructed, this route is
less concrete than the seven-mode Hamiltonian support problem.

## 2. Adversarial review: what was withdrawn or downgraded

The project has deliberately retained countermodels to its own tempting
arguments.

1.  A naive approximate-root induction in the standard system is false.
    Exact \(g\)-multiple reparametrizations reproduce arbitrarily long
    cancellation cascades while respecting the degree bounds.
2.  A monomial associated-graded argument for the radial kernel is false.
    Its kernel dimensions grow with \(k\) and do not equal the true stable
    profile.  Extension data between valuation grades matter.
3.  Conductor parity and a local Bockstein ladder on the fixed source plane
    do not globalize.  Endpoint-preserving perturbations by powers of \(c\)
    can kill the first local cokernel without changing the leading corners.
4.  The generic Gelfand--Leray/exact-differential reformulation is not new.
    It substantially overlaps Heitmann's 1990 equivalence
    ([Journal of Pure and Applied Algebra 64](https://doi.org/10.1016/0022-4049(90)90005-3)).
5.  Small boundary-tree enumeration, bounded sparse searches, and modular
    solutions without a lifting theorem are evidence only.  They are not
    promoted to global statements.
6.  A first check incorrectly suggested that the seven modes were not
    Hamiltonian gauge modes because arbitrary source Hamiltonians change the
    displayed bracket function.  The corrected calculation uses the actual
    symplectic form \(dP_0\wedge dQ_0\): the seven modes are exactly
    Hamiltonian.  Their formal flows solve the bracket equation, but generally
    leave the permitted polynomial support.  The distinction is support
    escape, not formal integrability.
7.  Trivial automorphism group of the outer Belyi cover, even supplemented
    by trace zero, does not force a bounded Hamiltonian to vanish.  The
    bracket of the low \(d=1\) and high \(d=4\) modes is a nonzero
    \(h(w)\); in Darboux coordinates it gives a finite vertical translation
    fixing \(w\) and hence fixing \(R(w)\).  On both rational degree-\(21\)
    outer points, the trace map on
    \(\langle w^{-1},1,\ldots,w^{12}\rangle\) has rank only two, and
    centering \(h\) by its constant trace makes it trace-zero without
    changing the flow.  The flow fails only when one asks for rationality
    in the original Kummer coordinate \(z\).

This negative audit is strategically important: it rules out several
plausible-looking routes to a false proof and prevents further brute-force
expansion of the same dead mechanisms.

## 3. Verification status

`verify_all.py` passes end to end.  The most expensive independent check,
`route_bd_fbar_obstruction.py --run-singular`, verifies the full
algebraic-closure obstruction over the two rational outer factors and the
irreducible cubic factor.  The analogous case-c modular fibers are also
origin-only.  The newly added conductor and universal-kernel verifiers pass
separately and are included in the current verifier inventory.

Passing code is not equivalent to peer review.  The remaining risks are
translation of the published reduction, hidden localizations, specialization
at the weighted boundary, and novelty.  The publication version should be
rebuilt from a small immutable certificate bundle rather than the current
research scripts.

## 4. Chosen pivot: seven-mode nonlinear support escape

The main effort will no longer be a larger Gröbner search.  The exact
Hamiltonian theorem reduces every lower radial deformation to seven scalar
potentials and gives their Lie bracket explicitly.  For \(k=1,2,3\), the
same first \(19\) nonlinear equations of weights at most \(8\) already have
irrelevant radical, with exact pure-power nilpotence certificates.  This
suggests a finite support-escape theorem independent of the radial scale.

The target lemma is:

> **Universal lowest-support-escape lemma.**  Express the quadratic
> Maurer--Cartan bracket in the seven explicit \(C\)-classes.  After ordering
> the modes by endpoint valuation, the first nineteen compatibility
> coefficients in weights \(4,\ldots,8\) force a nonzero endpoint/residue
> coefficient for the highest surviving mode, modulo the earlier modes.
> Iteration forces all seven modes to vanish.

The intended proof has four checkpoints.

1.  Compute the quadratic bracket symbolically in the \(C\)-coordinates,
    using the explicit scalar Lie bracket, the outer ODE, and
    \(\gcd(U,V)=1\).
2.  Identify seven scale-independent endpoint functionals whose coefficient
    matrix is triangular after ordering the modes.
3.  Express each diagonal entry as a product of explicit residues,
    discriminants, and resultants; prove these are units on the tame Hurwitz
    locus.
4.  Recover the observed pure-power eliminations formally, without
    enumerating outer dessins or increasing the Gröbner degree.

The second checkpoint must encode Kummer integrality, not just cover
monodromy or trace.  If a rational symplectomorphism preserves the outer
cover, trivial deck group fixes \(w\); preservation of
\(\Omega=z^4w^{-3}dz\wedge dw\) then gives
\(\phi(z)^5=z^5+B(w)\).  Rationality forces \(B=0\), because
\(z^5+B(w)\) is squarefree when \(B\ne0\).  Thus a promising endpoint
functional must detect the first failure of the formal seven-mode flow to
remain in the original fifth-root lattice.  Finite Laurent support in the
Darboux coordinates is insufficient.

An exact source-integrality theorem now sharpens that checkpoint.  Let
\(T=(X,Y)\) be the normalized algebraic branch of \(F_0^{-1}\circ F\) in
the original case-c coordinates.  If both \(X,Y\) are integral over
\(K[x,y]\), the normalized graph is finite.  Off the contracted critical
line \(x=0\), its projection is unramified in codimension one: a divisor
with \(X=0\) would lie in an origin fiber of the étale map \(F\), and all
other points are a base change of the étale locus of \(F_0\).  Purity makes
this a finite étale cover of \(\mathbb G_m\times\mathbb A^1\), hence a
Kummer cover \(u^e=x\).  The selected outer place has
\(x=z^2t\), so \(v_t(x)=1\), and the branch already lies in
\(K(z)((t))\); this rules out every \(e>1\).  Normality then makes \(T\)
polynomial.  The chain rule classifies it as
\[
X=cx,\qquad Y=c^{-3}y+h(x),
\]
and the identity jet plus the radial \(P\)-cap force \(c=1,h=0\).
Therefore proving original-plane integrality of both branch coordinates
would finish the radial branch outright.

This is not a consequence of polynomiality of \(P,Q\).  The polynomial
target shear
\[
(x^2,xy)\longmapsto(x^2+(xy)^2,xy)
\]
has the same Jacobian and contracted critical line, but its inverse branch
\((x\sqrt{1+y^2},\,y/\sqrt{1+y^2})\) has a pole in the second coordinate.
The actual missing theorem is consequently finiteness/properness of the
selected graph component, not merely regularity of its two output
functions.

Success would turn the observed \(k=1,2,3\) certificates into an all-\(k\)
radial obstruction.  It would still require an all-degree Newton-polygon
reduction before proving \(JC(2)\), but it is the shortest path from a
verified finite result to a reusable structural theorem.

## 5. Independent secondary direction

In parallel, pursue the global geometry forced by the weak-type-\(2\)
alternative for a hypothetical nonautomorphic Keller map, together with
coexceptional-curve and boundary-divisor constraints.  The fixed source
plane remains useful as a counterexample-first test object, but only global
boundary data should be used: local conductor jets are too flexible.

There is already a sharper exact starting point.  The conductor curve is
\(C\simeq\mathbf G_m\), parametrized by \(v\), with
\(c=v^2/9\), and every target-ring function is invariant under
\(v\mapsto-v\) on \(C\).  If a Darboux pair \(e=(U,V)\) existed, its
conductor restrictions \(u,w\in\mathbf Q[c,c^{-1}]\) would obey
\[
\operatorname {Res}_{c=0}(u\,dw)=\frac23.
\]
The normalization of the image curve \(\Gamma=e(C)\) cannot be
\(\mathbf A^1\): a map from \(\mathbf G_m\) to a one-puncture rational
normalization would force both restrictions to be polynomials in one
Laurent monomial and hence give zero residue.  Thus \(\Gamma\) must have
\(\mathbf G_m\)-normalization, and \(C\to\Gamma\) is a finite étale power
cover of even degree \(2\delta\).  This converts a local residue into a
global two-puncture and parity constraint.

For a generic primitive element \(\pi\in R\), the graph hypersurface
\(\overline{(\pi,U,V)(\mathbf A^2)}\) is nonnormal along \(\Gamma\).
The weak-type-\(2\) theorem then requires a genuine saturation failure:
some preimage component of the graph's singular locus must share its image
with a second distinct curve.  The two branches \(v\) and \(-v\) of \(C\)
do not supply this—their union is one irreducible curve—so a new global
collision component is necessary.  What is not yet proved is that this
extra component lies over \(\Gamma\), rather than over another singular
image curve.  That distinction is the immediate global classification
problem.

An exact countermodel prevents a stronger local inference.  On
\(\mathbf G_m^2\), the étale map
\((x,y)\mapsto(x^2,y^2)\) pulls the smooth curve \(XY=1\) back to the two
disjoint curves \(xy=\pm1\); both cover the same image and support nonzero
residues.  Therefore squarefree pullback factorization plus étaleness does
not force an extra component to meet the conductor.  Any attachment or
finiteness theorem must use the global \(\mathbf A^2\) compactification,
cyclic quotient data, or the divisor tree at infinity.  More local conductor
algebra would repeat a mechanism already disproved by this countermodel.

There is nevertheless a global dichotomy that survives the countermodel.
Let \(S_e\) be the nonproper-value curve of a hypothetical fixed-plane
Darboux pair.  If \(e^{-1}(\Gamma)=C\) and \(S_e\subseteq\Gamma\), then
\[
\mathbf A^2\setminus C\longrightarrow\mathbf A^2\setminus\Gamma
\]
is a finite étale cover.  Both complements have compactly supported Euler
characteristic \(1\), so multiplicativity forces the cover to have degree
one, contradicting the verified conductor collision.  Therefore
\[
e^{-1}(\Gamma)\supsetneq C
\quad\text{or}\quad
S_e\text{ has a component }\Lambda\ne\Gamma.
\]
The projective conductor is a rational quartic with two distinct marked
ends: cusp arms of characteristic types \((2,5)\) and \((2,3)\).  The map
to the compactified normalization of \(\Gamma\) is totally ramified of index
\(2\delta\) at both.

The arm-resolution test is now complete and stops this line.  Exact
four- and three-blowup resolutions determine every local self-intersection,
pullback multiplicity, and augmented-canonical label.  Those labels admit a
compatible global skeleton satisfying the known type-\(1\)/type-\(2\)/
type-\(3\) sign and connectedness constraints but containing no type-\(4\)
tail and hence no forced cyclic quotient point.  Borisov's attachment theorem
is therefore vacuous on this skeleton.  It is not a Keller realization, but
it is an exact countermodel to the proposed deduction from the currently
available boundary theorems.  Further expansion of the fixed-plane tree is
not justified without a genuinely new global incidence theorem.

## 6. Revised secondary direction: two-end Hamiltonian reconstruction

The independent secondary effort now supports the primary route from a
different angle.  The seven radial potentials split canonically into three
low-end modes and four high-end modes.  The low-only and high-only
consistency ideals are each already origin-only for \(k=1,2,3\), but mixed
modes can cancel to high order.  This suggests viewing the full lower scheme
as the nonreduced intersection of two opposite Hamiltonian lattices or
parahoric subgroups.

The new structural question is whether a formal symplectomorphism regular in
both endpoint lattices must extend to the compactified degree-\(21\) Belyi
cover and hence be trivial.  The first-symbol shortcut is false: the high
potentials have commuting leading powers of the common coordinate at
infinity, so the naive highest-degree initial ideal is positive-dimensional.
A successful proof must use at least the next Belyi tail, global monodromy,
or a genuine two-end Birkhoff factorization.  Exact rational \(k=1\)
reconstruction is being used only to identify those invariant next-tail
relations, not as a larger search.

## 25 July addendum: what survived adversarial review

The universal depressed-Wronskian bound survives, but a simple
scale-five Hensel countermodel proves that it cannot be the headline
all-scale obstruction by itself.  Its proper role is as the exact
ramification ledger behind the exceptional scale-four calculation.

The stronger candidate for a structural paper is the five-block
discriminant-square theorem
\[
\Phi=3K^2-JL\in\mathbf C[h]^2,
\qquad
\deg\Phi=\deg(B^2-A^3)+8r-10.
\]
It is derived from the fourth transverse row, detects the structure
missed by the Wronskian, and rejects the scale-five Wronskian
countermodel without a coefficient search.  At present it supplies only
the universal parity condition \(\deg(B^2-A^3)\equiv0\pmod2\); the
publishable next theorem would classify its full even divisor together
with the outer \(U,V\) equation.

The exact closure of the bounded \((72,108)\) alternatives remains the
highest-value publication claim.  It should be separated from broader
JC rhetoric, presented as a computer-assisted lower-bound theorem, and
submitted only with:

1. a line-by-line import of the GGHV Proposition 4.3 alternatives;
2. explicit projective good-reduction and chart-exhaustion lemmas for
   case c;
3. the small exact rational Wronskian proof for the final a/b cell;
4. persisted Singular transcripts and independent reruns.

The quadratic-pseudoplane Pfaff, class-group, and \(D+H\) collision
theorems are credible companion material, but they do not yet constitute
a counterexample or a global obstruction.
