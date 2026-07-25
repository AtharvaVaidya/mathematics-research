# Plane Jacobian conjecture research report

Date: 24 July 2026

> **Current checkpoint.**  See `STATUS_AND_PIVOT_2026-07-24.md` for the
> later adversarial audit, the Davenport--Zannier novelty correction, and
> the pivot from the failed fixed-cusp shortcut to the actual non-cusp
> asymptotic curve and its two boundary clusters.
>
> **25 July checkpoint.**  The Wronskian/radical obstruction now
> eliminates the final a/b \((3,5)\) cell exactly over \(\mathbf Q\).
> The two generic case-c charts are empty at deficit seven.  These
> sharpen the bounded \((72,108)\) elimination but do not change the
> statement below that \(JC(2)\) itself remains unresolved.

## Current assessment

The research is still active.  At this checkpoint neither requested
terminal mathematical result has yet been obtained:

- no explicit \(F=(P,Q):\mathbb C^2\to\mathbb C^2\) with constant nonzero
  Jacobian and an exact collision was found;
- no proof that every plane Keller map is a polynomial automorphism was found.

Every positive claim below has an exact verifier.  Some are all-degree
theorems within a stated construction family; none is promoted to a
resolution of \(JC(2)\).

The strongest new candidate theorem is the complete elimination of both
GGHV reduced systems for the last degree pair \((72,108)\).  Subject to an
independent check of the published reduction and the
tame-specialization/weighted-projective bridge, this would raise the maximum
coordinate-degree lower bound for a counterexample from \(108\) to \(125\).
The proof combines an exact degree-\(21\) Belyi/Hurwitz count with complete
modular algebraic-closure certificates for every lower coefficient, including
the irreducible cubic outer factor.  It does not give an all-degree
reduction.

The main structural advance beyond that bounded result is a uniform
Hamiltonian description of the radial deformation complex.  At every scale
\(k\ge1\), its full linear kernel has weights
\[
(1,1,2,2,3,3,4).
\]
The seven scalar potentials form an explicit graded Hamiltonian Lie algebra,
and their formal flows preserve the bracket exactly.  The remaining
nonlinear equations measure escape from the permitted Newton support.  This
has replaced larger Gröbner searches by a finite support-escape problem in
seven modes.

The publication-readiness review, rejected arguments, verification risks,
and selected next strategy are consolidated in
[`PUBLICATION_STRATEGY_AUDIT.md`](PUBLICATION_STRATEGY_AUDIT.md).

This distinction is especially important in July 2026. The newly announced
three-dimensional map is an exact counterexample to \(JC(3)\), and has
independent formal verification, but the plane problem remains separate. See
the [Archive of Formal Proofs verification](https://isa-afp.org/entries/Jacobian_Counterexample.html)
and the current graded analysis in
[arXiv:2607.20210](https://arxiv.org/abs/2607.20210).

The Danielewski-surface construction has also been closed beyond the
previous equivariant ansatz.  For every Chebyshev étale endomorphism of
degree \(d>1\), no affine-line divisor \(E\) with
\(S\setminus E\simeq\mathbb A^2\) satisfies
\(\Phi_d^{-1}(E)\subseteq E\).  The proof combines the semiconjugacy
\(z\circ\Phi_d=T_d\circ z\) with the exact Picard group of the surface.
It consequently excludes every automorphism conjugate of the Chebyshev
family, not just the explicitly generated shear conjugates.  This is an
all-degree obstruction to Route C, not a proof of \(JC(2)\).

## Route A: pseudo-plane Darboux equation

Let

\[
B=k[u,v,w]/(w^2-u-u^2v)
\]

with the bracket in the brief.

### Exact characteristic-\(3\) construction

Over \(\mathbb F_3\),

\[
P_0=w,\qquad Q_0=-v+uv^2
\]

satisfies \(\{P_0,Q_0\}=1\). Composing with the supplied plane cover gives
the completely explicit characteristic-\(3\) plane map

\[
\begin{aligned}
\widetilde P(x,y)&=x-x^3y,\\
\widetilde Q(x,y)&=-y-x^4y^3+x^6y^4,
\end{aligned}
\]

for which

\[
J(\widetilde P,\widetilde Q)=-1\in\mathbb F_3^\times
\]

and

\[
(1,0)\ne(-1,-1),\qquad
F(1,0)=F(-1,-1)=(1,0).
\]

This is not a complex counterexample. Over the integers the seed has the
exact defect

\[
\{w,-v+uv^2\}=1-3u^2v^2.
\]

### Exact \(3\)-adic tower and its limitation

Put \(s=uv\) and use the homogeneous ansatz

\[
P=w\,a(s),\qquad Q=v\,b(s).
\]

Then

\[
\{P,Q\}
=-\frac1{a(s)}
\frac{d}{ds}\left[s(1+s)a(s)^2b(s)\right].
\]

The characteristic-\(3\) seed is \(a=1,\ b=s-1\). The linearized Hensel
operator at this seed is surjective on \(\mathbb F_3[s]\), so the solution
lifts modulo \(3^N\) for every \(N\) if support is allowed to grow. The
bundled computation verifies 12 stages, through \(3^{13}=1594323\).

The tower cannot have bounded degree. In characteristic zero the Darboux
equation would require

\[
\left[s(1+s)a^2b\right]'=-a.
\]

For nonzero polynomials \(a,b\), the two sides have degrees
\(2\deg a+\deg b+1\) and \(\deg a\), respectively. This is impossible.
A fixed-degree \(3\)-adic tower would converge to polynomials over
\(\mathbb Q_3\), contradicting the same characteristic-zero argument.

The weight-space classification in the Route A memo proves more: every
homogeneous pair with constant bracket reduces to this ansatz. Hence there is
no homogeneous Darboux pair in \(B\) over a characteristic-zero field.

### Further exact obstructions

- No affine-linear Hamiltonian
  \(P=au+bv+cw+d\) has a polynomial slice \(Q\) of any degree.
  The proof splits into a critical-point argument, a generic
  \(\mathbb G_m\)-fiber residue argument for \(P=v\), and a boundary-pole
  argument for \(P=au+cw\).
- More generally, every ordered elementary two-generator Hamiltonian
  \[
  P=cx_i+f(x_j),\qquad c\ne0,\quad
  x_i\ne x_j\in\{u,v,w\},
  \]
  has no polynomial slice of any degree.  This is an all-degree theorem
  within these six nonlinear families, not a classification of arbitrary
  Hamiltonians.  For \(P=cw+f(u)\), Laurent characteristics force
  \(Q=-1/(cu)+h(P)\), and fiber plus boundary regularity is impossible.
  For \(P=cu+f(w)\), the forced rational differential has nonzero residues.
  The other four orientations give differentials \(dx/y\) on explicit
  generic hyperelliptic fibers; these are nonzero holomorphic differentials
  on the smooth projective models and hence cannot be exact.
- The generic-fiber argument extends to every separated three-generator
  Hamiltonian
  \[
  P=a x_i+b x_j+f(x_k),
  \]
  where \((x_i,x_j,x_k)\) is any permutation of \((u,v,w)\) and
  \((a,b)\ne(0,0)\).  Two orientations reduce to explicit hyperelliptic
  differentials.  For \(P=au+bv+f(w)\), the generic fiber is
  \[
  au^3-(P-f(w))u^2-bu+bw^2=0,
  \]
  its Hamiltonian derivation is the curve-Jacobian field, and a mate would
  make \(du/F_w\) exact.  When \(\deg f\ge1\), this is the nonzero
  holomorphic differential associated with the interior lattice point
  \((1,1)\) of the nondegenerate Newton polygon; constant \(f\) is the
  affine case.  This theorem still does not cover Hamiltonians with
  nonlinear mixed terms.
- One substantial mixed-term family also closes.  For
  \[
  P=av+C(u)w+F(u),\qquad a\ne0,
  \]
  put \(Y=2aw+C(u)u^2\).  Its generic fiber is isomorphic to
  \[
  Y^2=4a^2u+4au^2(P-F(u))+C(u)^2u^4,
  \qquad \{P,u\}=Y.
  \]
  A nonsquarefree right side makes the generic fiber singular and is
  immediately incompatible with a slice.  In the squarefree case a mate
  would make \(du/Y\) exact; this differential is nonzero holomorphic when
  the right side has degree at least three, and has nonzero residues at
  infinity in degree two.  Hence this whole family is excluded for
  arbitrary polynomial \(C,F\) and arbitrary mate degree.  This includes
  nonlinear mixed terms \(u^mw\), but is not an arbitrary mixed-support
  classification.
- The other characteristic-\(3\)-inspired mixed seed also has an
  all-degree obstruction.  For
  \(P=cw+\lambda uv\), \(\lambda\ne0\), the function field has the exact
  rational mate
  \[
  Q_0=-\frac{2\lambda w+cu}{2\lambda u(\lambda+P)}.
  \]
  Every rational mate is \(Q_0+h(P)\).  Regularity on the nonboundary
  component of \(P=0\) forces \(h\) to be regular at zero, while \(Q_0\)
  has boundary order \(-1\) along \(D=(u,w)\).  Therefore no polynomial
  mate exists.  In particular \(P=w+uv\), despite occurring in an exact
  characteristic-\(3\) pair, cannot lift to a characteristic-zero
  polynomial pair of any degree.
- This boundary calculation extends to arbitrary \(u\)-tails:
  \[
  P=cw+\lambda uv+F(u),\qquad \lambda\ne0.
  \]
  With \(y=2\lambda w+cu\), the generic fiber is
  \[
  y^2=u\!\left[c^2u+4\lambda(\lambda+P-F(u))\right],
  \qquad \{P,u\}=uy.
  \]
  For \(\deg F\ge2\), a mate would make \(du/(uy)\) exact on a
  positive-genus curve.  This differential has one double pole and no
  others, so its primitive would have one simple pole and induce a
  degree-one map to \(\mathbb P^1\), impossible in positive genus.  For
  affine \(F\), the rational primitive is explicit and its order-\(-1\)
  boundary pole cannot be canceled.  Thus the whole family is excluded
  at every mate degree, including the \(u+w\pm uv\) characteristic-\(3\)
  seeds.
- Allowing an arbitrary \(u\)-dependent coefficient of \(w\) still closes:
  \[
  P=C(u)w+\lambda uv+F(u),\qquad \lambda\ne0.
  \]
  With \(y=2\lambda w+C(u)u\), the generic fiber is
  \[
  y^2=u\!\left[C(u)^2u+
  4\lambda(\lambda+P-F(u))\right],\qquad \{P,u\}=uy.
  \]
  The positive-genus cases are excluded by the same one-double-pole
  argument.  The complete genus-zero locus is
  \(C(u)^2u-4\lambda F(u)\) affine in \(u\); there the rational primitive
  is explicit and again has an uncancelable order-\(-1\) boundary pole.
  This variable-coefficient theorem structurally excludes every one of
  the 17 degree-\((2,5)\) characteristic-\(3\) seed Hamiltonians found by
  the exhaustive search, regardless of prospective characteristic-zero
  mate degree.
- The smallest missing support perturbation of those seeds is a linear
  \(v\)-term.  It leads to a further all-degree family:
  \[
  P=(b+\lambda u)v+C(u)w+F(u),\qquad (b,\lambda)\ne(0,0).
  \]
  With \(A=b+\lambda u\) and \(Y=2Aw+C(u)u^2\), the generic fiber is
  \[
  Y^2=4A^2u+4Au^2(P-F(u))+C(u)^2u^4,\qquad \{P,u\}=Y.
  \]
  For \(b\lambda\ne0\), any repeated root away from \(A=0\) is a critical
  point; at the unique root of \(A\), a simultaneous root is necessarily
  simple because its derivative contains
  \(4\lambda u^2(P-F(u))\).  The transcendental \(P\)-coefficient forces
  degree at least three, so \(du/Y\) is nonzero holomorphic and not exact.
  The cases \(b=0\) and \(\lambda=0\) are exactly the two already-closed
  mixed families.  Hence arbitrary polynomial \(C,F\) and arbitrary mate
  degree are excluded.
- The next absent quadratic support, \(v^2\), also closes.  For
  \[
  P=cw+\lambda uv+\mu v^2,\qquad c\lambda\mu\ne0,
  \]
  the generic fiber in \((v,w)\) is
  \[
  F=(\lambda+2P-2cw-2\mu v^2)^2
    -\lambda^2(1+4vw^2)=0,
  \]
  and \(D_P=(4\lambda)^{-1}(F_w\partial_v-F_v\partial_w)\).
  Its Newton polygon has vertices
  \((0,0),(4,0),(1,2),(0,2)\), with \((1,1)\) strictly interior; the
  four boundary faces are squarefree or binomial over \(\mathbb C(P)\).
  Thus a mate would make the corresponding nonzero holomorphic toric
  residue \(4\lambda\,dv/F_w\) exact, which is impossible.  This is an
  all-mate-degree theorem for the displayed nonzero coefficients.
- In fact the same Newton proof handles every pure \(v\)-tail:
  \[
  P=cw+\lambda uv+G(v),\qquad c\lambda\ne0.
  \]
  For \(n=\deg G\ge2\), the generic Newton polygon has vertices
  \((0,0),(2n,0),(1,2),(0,2)\), still with \((1,1)\) interior.  Its
  bottom face is
  \(4(P-G(v))(\lambda+P-G(v))\), squarefree over \(\mathbb C(P)\);
  the other boundary faces are likewise squarefree or binomial.  Degree
  zero or one is already contained in the affine-\(v\)-coefficient
  theorem.  Thus arbitrary \(G\) and arbitrary mate degree are excluded.
- The complementary quadratic support \(vw\) has a direct rational-fiber
  obstruction.  For
  \[
  P=cw+\lambda uv+\nu vw,\qquad \nu\ne0,
  \]
  use \(s=uv\) and \(vw=s(1+s)/w\).  The generic fiber is the conic
  \[
  F=cw^2+(\lambda s-P)w+\nu s(1+s)=0,
  \]
  with \(D_P=w(F_s\partial_w-F_w\partial_s)\).  The forced differential
  \(-ds/(wF_w)\) has residues \(1/\nu\) and \(-1/\nu\) at the two
  completion points \((s,w)=(0,0),(-1,0)\).  It is therefore not even
  rationally exact, excluding polynomial mates of every degree.
- The apparent \(w^2\)-perturbation reduces to \(u+u^2v\).  It produces
  new exact characteristic-\(3\) pairs; for example
  \[
  P=u+w+uv+u^2v,\qquad
  Q=-v+w-vw+uv^2+v^2w+uv^2w
  \]
  has bracket one over \(\mathbb F_3\).  In characteristic zero it lies
  in a larger excluded family:
  \[
  P=u(b+\kappa u)v+C(u)w+F(u),\qquad b\ne0.
  \]
  With \(y=2(b+\kappa u)w+C(u)u\), its generic fiber is
  \[
  y^2=u\!\left[
  4(b+\kappa u)^2+4(b+\kappa u)(P-F(u))+C(u)^2u
  \right],
  \quad \{P,u\}=uy.
  \]
  In positive genus, the forced \(du/(uy)\) has one double pole, so an
  exact primitive would have one simple pole and force a degree-one map
  to \(\mathbb P^1\).  On the complete genus-zero locus the rational
  primitive is explicit and has an uncancelable order-\(-1\) boundary
  pole.  Thus the entire displayed family is excluded for arbitrary
  \(C,F\) and arbitrary mate degree.  For
  \(P=w+uv+\kappa w^2\), the primitive is
  \[
  -\frac{2(1+\kappa u)w+u}{2u(1+P)}.
  \]
  These new characteristic-\(3\) pairs do not start a Hensel tower.  For
  either sign, write \(\{P_0,Q_0\}=1+3E\) for the displayed integer
  representatives and define, over \(\mathbb F_3\),
  \[
  \ell(R)=[v]R+[uv^2]R.
  \]
  Exact monomial inspection gives
  \[
  \ell(\{A,Q_0\}+\{P_0,B\})=0
  \]
  for arbitrary polynomial corrections \(A,B\), while
  \(\ell(-E)=1\).  Thus the first lifting equation is inconsistent with
  unrestricted support: neither pair lifts modulo \(9\), hence neither
  lifts modulo \(27\).  This modular obstruction is separate from the
  characteristic-zero boundary obstruction above.  By comparison,
  \(P=w\pm u^2\) admits a first mod-\(9\) correction once degree-eight
  support is allowed, whereas the homogeneous \(P=w\) seed has a
  support-expanding tower to every \(3\)-adic order.
- The next reduced degree-three perturbations are \(uv^2\), \(uvw\), and
  \(v^2w\); none of their two signed versions has a characteristic-\(3\)
  mate through degree \(25\).  The middle orbit has an all-degree
  explanation.  Put \(s=uv\).  For
  \[
  P=w+s+\kappa sw=w+uv+\kappa uvw,
  \]
  the generic fiber is \(s=(P-w)/(1+\kappa w)\), and a rational mate
  would force
  \[
  dQ=\frac{dw}{w^2(1+\kappa w)}.
  \]
  Its residues at \(w=0\) and \(w=-1/\kappa\) are
  \(-\kappa\) and \(+\kappa\).  Hence no rational mate exists, in
  characteristic zero or over \(\mathbb F_3\) for \(\kappa=\pm1\).
  The \(uv^2\) orbit has a parallel normalization-residue proof.  In
  \((s,w)\) its generic curve is
  \[
  F=w^3+(s-P)w^2+\kappa s^2(1+s)=0,
  \qquad D_P=F_s\partial_w-F_w\partial_s.
  \]
  Blowing up the missing point \((s,w)=(0,0)\) with \(s=yw\) produces
  two branches \(y=\pm\sqrt{P/\kappa}\).  The forced differential
  \(-ds/F_w\) has residues
  \[
  \pm\frac1{2\sqrt{\kappa P}},
  \]
  both nonzero.  Thus \(w+uv+\kappa uv^2\) has no rational mate in
  characteristic zero or characteristic \(3\).
  The last orbit, \(v^2w\), instead forces a nonzero holomorphic
  differential.  Its generic plane model and forced differential are
  \[
  F=w^4+(s-P)w^3+\kappa s^2(1+s)^2=0,
  \qquad \eta=-\frac{w\,ds}{F_w}.
  \]
  On the normalization, \(\eta\) is regular at the two finite cusps
  \((s,w)=(0,0),(-1,0)\).  At infinity, with \(x=1/s\) and \(t=w/s\),
  it becomes \(t\,dx/\phi_t\), where
  \[
  \phi=t^4+(1-Px)t^3+\kappa(1+x)^2.
  \]
  It is regular at every simple point and also at the only possible
  resonant double point \(t=-3/4,\ \kappa=27/256\), since
  \(\phi_{tt}=9/4\) and
  \(\phi_x=27(2P+1)/128\ne0\) over \(\mathbb C(P)\).
  A nonzero holomorphic differential on a complete smooth curve cannot
  be exact, so \(w+uv+\kappa v^2w\) has no rational mate in
  characteristic zero.
- The first reduced degree-four orbit, \((uv)^2\), is contained in a
  larger all-degree obstruction.  For
  \[
  P=cw+H(s),\qquad s=uv,\quad c\ne0,\quad \deg H\ge2,
  \]
  the generic fiber is \(w=(P-H(s))/c\), and a mate would force
  \[
  dQ=-\frac{c\,ds}{(P-H(s))^2}.
  \]
  At a root \(\alpha\) of \(H(s)-P\), this differential has residue
  \[
  \frac{cH''(\alpha)}{H'(\alpha)^3}.
  \]
  Because \(H(s)-P\) is irreducible over \(\mathbb C(P)\) and
  \(0\ne H''\) has smaller degree, this residue is nonzero.  Hence no
  \(cw+H(uv)\) with nonlinear \(H\) has a rational mate in
  characteristic zero.  For \(H=s+\kappa s^2\), the same residue is
  nonzero in characteristic \(3\), excluding both signed minimal orbits
  there as well; the exact modular search independently finds no mate
  through partner degree \(25\).
- The next orbit \(uv^3\) has one exact characteristic-\(3\) pair:
  \[
  \begin{aligned}
  P={}&w+uv+uv^3,\\
  Q={}&-u-v+w+uv-u^2v+uv^2+uvw+v^2w-u^2v^2+v^3w\\
     &+uv^4+uv^3w-v^4w+uv^4w-u^2v^5-uv^5w+v^6w+uv^7w.
  \end{aligned}
  \]
  The partner degree is nine.  In characteristic zero, however, the
  generic plane model is
  \[
  F=w^5+(s-P)w^4+\kappa s^3(1+s)^2=0,
  \qquad dQ=-\frac{w^2\,ds}{F_w}.
  \]
  The forced differential is regular at the branches over
  \((s,w)=(0,0),(-1,0)\).  At infinity it is
  \(t^2dx/\phi_t\), with
  \[
  \phi=t^5+(1-Px)t^4+\kappa(1+x)^2.
  \]
  The only repeated-root case is
  \(t=-4/5,\ \kappa=-256/3125\); there
  \(\phi_{tt}=-64/25\) and
  \(\phi_x=-256(5P+2)/3125\), so the differential remains regular on
  the normalization.  It is therefore nonzero, holomorphic, and not
  exact, excluding every nonzero \(\kappa\) in characteristic zero.
  The modular pair itself also fails its first unrestricted Hensel
  equation: the functional
  \(\ell(R)=[v^4]R+[uv^5]R\) annihilates every correction column but
  satisfies \(\ell(-E)=1\).  Thus it cannot lift modulo \(9\).
- The four other new degree-four supports are also closed in
  characteristic zero:

  - For \(uv^2w\),
    \[
    F=w^2+(s-P)w+\kappa s^2(1+s),\qquad
    dQ=-\frac{ds}{wF_w}.
    \]
    The branch at \((s,w)=(-1,0)\) has residue \(1/\kappa\), so this
    orbit is excluded in characteristic \(3\) as well.
  - For \(u^2vw\), completing
    \[
    F=(1+s)(w+s-P)+\kappa sw^3
    \]
    gives a squarefree degree-six hyperelliptic model, hence genus two.
    The forced differential has one double pole, at
    \(s=P,w=0\), and is regular everywhere else.  An exact primitive
    would give a degree-one map to \(\mathbb P^1\), impossible.
  - For \(v^3w\),
    \[
    F=w^6+(s-P)w^5+\kappa s^3(1+s)^3,\qquad
    dQ=-\frac{w^3ds}{F_w},
    \]
    and exact normalization calculations show that \(dQ\) is a nonzero
    holomorphic differential.  The sole infinity resonance
    \(t=-5/6,\ \kappa=3125/46656\) is regular.
  - For \(u^3v\),
    \[
    F=(1+s)^2(w+s-P)+\kappa sw^4,\qquad
    dQ=\frac{(1+s)^2dw}{w^2F_s}.
    \]
    Its Newton polygon has four interior points and one
    delta-two tacnode, so the normalization has genus two; again the
    forced differential has exactly one double pole.

  Exact characteristic-\(3\) searches for both signs of the last three
  orbits are negative through partner degree \(25\); no all-degree
  positive-characteristic claim is inferred from those finite searches.
- These calculations are subsumed by a monomial-cone theorem.  In the
  chart \(s=uv\),
  \[
  u^av^bw^c=s^b(1+s)^{b-a}w^{2(a-b)+c},
  \qquad c=0,1.
  \]
  For \(b>a\), put \(r=b-a\) and \(m=2r-c\).  The generic curve and
  forced differential are
  \[
  F=w^{m+1}+(s-P)w^m+\kappa s^b(1+s)^r,\qquad
  \eta=-\frac{w^{m-2}ds}{F_w}.
  \]
  The lattice point of \(\eta\) is interior to the Newton polygon
  exactly when \(m>b\), or \(b>2a+c\); normalization at the two
  degenerate finite groups and the sole possible resonant infinity face
  keeps it holomorphic.  On the wall \(m=b\), it has residues
  \(A/(bP)\), where \(\kappa A^b=P\).  On the adjacent wall \(m=b-1\),
  it has one double pole on a positive-genus normalization, of genus
  \(2(a-1)\) for \(c=0\) and \(2a-1\) for \(c=1\).

  For \(a>b\ge1\), set \(d=a-b,\ e=2d+c\).  Then
  \[
  F=(1+s)^d(w+s-P)+\kappa s^bw^e,\qquad
  \eta=\frac{(1+s)^d\,dw}{w^2F_s}.
  \]
  Pick's theorem and the sole \(z^d+w^e\) boundary singularity give
  \[
  g=e+\frac{b-g_0-g_1-g_2}{2}>0,
  \]
  with \(g_0=\gcd(d,e)\),
  \(g_1=\gcd(|b-d-1|,e)\), and
  \(g_2=\gcd(b,e-1)\).  The differential has exactly one double pole,
  so exactness would force a degree-one map to \(\mathbb P^1\).
  Diagonal monomials are handled by the \(H(uv)\) residue theorem or,
  for \(s^aw\), by residue \(-\kappa aP^{a-1}\).

  Consequently every monomial perturbation with \(a>b\ge1\), every
  non-affine diagonal case, and every
  \(b>a,\ b\ge2a+c-1\) is excluded in characteristic zero.  This
  structurally contains all reduced monomial perturbations through
  generator degree five; the unclosed asymptotic region is the middle
  wedge \(a<b<2a+c-1\), together with already separated pure-tail
  boundaries.
- The middle wedge has two further structural exclusions.  With
  \(m=2(b-a)-c\), \(g=\gcd(m,b)\), \(M=m/g\), and \(B=b/g\), its origin
  branches have
  \[
  s=t^M,\qquad w=A t^B y(t),\qquad A^m=\kappa/P.
  \]
  If \(m\mid b\), direct Puiseux expansion gives
  \[
  \operatorname{res}\eta
  =\frac1{A mP}[t^{b/m-1}]
   (1+t)^{-(b-a)/m}(1-t/P)^{-(m-1)/m},
  \]
  which is nonzero.  Thus this full exponent sublattice is excluded for
  every nonzero coefficient.

  The first residue-zero wall is also excluded for every coefficient.
  If \(b-m=2\), the hypothetical primitive has pole divisor of total
  degree two over the origin.  Explicit toric adjoints give two
  independent canonical jets along that divisor: two branch values when
  \(c=0\), and the value and first jet on the single branch when \(c=1\).
  Riemann--Roch therefore gives \(L(E)=k\), leaving no possible
  nonconstant primitive.

  More generally, the complete canonical space has a row basis
  \[
  s^{i-1}(1+s)^{\lfloor (b-a)(m-j)/m\rfloor}
  w^{j-1}\frac{ds}{F_w}.
  \]
  On the primitive pole divisor, its jet matrix splits into Fourier
  blocks in the \(g=\gcd(m,b)\) origin branches.  This gives an exact
  integer staircase certificate for \(L(E)=k\).  A uniform estimate
  proves the certificate whenever
  \[
  m>(b-m)^2,
  \]
  excluding every fixed nonzero coefficient in that asymptotic region.
  Parity sharpens this to \(m\ge2(b-m)-1\) for \(c=1\), and to
  \(3m>2(b-m)^2\) for \(c=0\) once \(b-m\ge4\).  The same calculation,
  plus explicit low-dimensional \(L(E)\)-generators, excludes the whole
  next two walls \(b-m=3,4\).

  There is also a complete fixed-coefficient theorem in the coprime
  region.  When \(\gcd(m,b-m)=1\), every possible pole order
  \(p\le b-m\) is paired with a complementary canonical adjoint and an
  explicit function
  \(s^\alpha(1+s)^{\lceil\beta(b-a)/m\rceil}/w^\beta\).
  Exactly one member of each pair is regular.  This gives a basis of
  \(L(E)\); its unique possible maximal-pole element is \(vw\), whose
  derivative normalization is incompatible at the origin and at
  \((s,w)=(0,P)\).

  The coprime construction extends character by character to arbitrary
  \(g=\gcd(m,b-m)\).  Each pole order contributes a \(g\)-column Fourier
  block: every column is exactly either a canonical gap or an explicit
  global function.  In the top block only the \(vw\) character can
  match the forced differential.  Its coefficient is fixed by the
  origin principal part, after which evaluation at \((0,P)\) is off by
  the factor \(b-m\).  Consequently the entire former middle wedge is
  excluded for every fixed nonzero coefficient.

  The argument is also facewise stable.  If a middle-wedge monomial is
  exposed after clearing denominators and every other term lies
  strictly behind its origin, \(s=-1\), and slanted-infinity faces, the
  Newton polygon, conductor, Fourier blocks, and comparison point stay
  unchanged.  Such finite nonsparse supports are therefore excluded on
  the Zariski-open coefficient locus with no extra curve singularities.

  Globally, every finite middle-wedge support is classified by three
  rational face signatures
  \(O=b/m,\ Z=(b-a)/m,\ I=(2b-a)/(m+1)\).  A unique term minimizing
  \(O,Z\) and maximizing \(I\) automatically has maximal denominator
  and satisfies the exposed-face inequalities.  All remaining supports
  lie either on an explicit signature-tie locus or in one of four
  separated-extremizer types \(L=Z\ne R\), \(L=R\ne Z\),
  \(Z=R\ne L\), or \(L,Z,R\) all distinct.  This gives a finite
  combinatorial description of the residual nonsparse problem.

  The four separated types and origin-face ties are all excluded by one
  coefficient-uniform first-face calculation.  If
  the primitive edge direction is \((B,-M_0)\), its face equation is
  \(G(s^B/w^{M_0})-P=0\).  The top primitive is governed by the inverse
  \(H_P=(XG')^{-1}\) in \(k(P)[X]/(G-P)\).  Exactness would require
  \(PH_P(0)=B-M_0\), whereas
  \(PH_P(0)\to1/\deg G\) as \(P\to\infty\).  Since
  \(\deg G(B-M_0)\ge2\), this is impossible.  The face polynomial
  \(G-P\) is automatically separable over \(k(P)\).  Degeneracy on a
  later Newton face only refines later boundary valuations, whose
  possible primitive corrections have \(s\)-order at least two and
  hence zero first jet at \((0,P)\).  Thus arbitrary finite
  middle-wedge supports with maximal denominator at least two are
  excluded for every nonzero coefficient vector.

  The remaining horizontal case has maximal denominator \(m=1\).
  Necessarily every term is \(s^b(1+s)/w\), \(b\ge3\), so with
  \(A(s)=(1+s)K(s)\) the cleared curve and forced differential are
  \[
  F=w^2+(s-P)w+A(s),\qquad
  \eta=-\frac{ds}{w(2w+s-P)}.
  \]
  On the curve,
  \[
  \eta-\frac{ds}{A(s)}
  =\frac{ds}{(s-P+w)(s-P+2w)},
  \]
  which is regular at every point above \(w=0\), even when a root of
  \(A\) is multiple.  A reciprocal polynomial differential \(ds/A\)
  has a nonzero residue whenever \(A\) has at least two distinct roots:
  otherwise a rational primitive \(B/C\), with
  \(C=A/\operatorname{rad}(A)\), would satisfy
  \[
  B'C-BC'=C/\operatorname{rad}(A).
  \]
  If \(n=\deg C\), the two sides have degrees at least \(n-1\) and at
  most \(n-2\), respectively.  Here \(A\) is divisible by
  \(s^3(1+s)\), so \(0\) and \(-1\) are distinct roots.  This excludes
  the horizontal case for every coefficient and completes all finite
  middle-wedge supports.

  An earlier generic check, still useful as an independent deformation
  certificate, introduced a parameter \(\tau\).  Around the rational
  fiber at \(\tau=0\),
  \[
  \eta_\tau=-\frac{ds}{(P-s)^2}
  -\tau\kappa(m+2)
   \frac{s^b(1+s)^{b-a}}{(P-s)^{m+3}}\,ds+O(\tau^2).
  \]
  The first-variation residue is
  \[
  \frac{(-1)^m\kappa}{(m+1)!}
  \left.
  \frac{d^{m+2}}{ds^{m+2}}
  \bigl(s^b(1+s)^{b-a}\bigr)
  \right|_{s=P}\ne0.
  \]
  Hence the perturbation is not rationally exact over
  \(\mathbb C(\tau,P)\).  The coefficient-uniform first-face and
  horizontal arguments above now supersede the former exceptional
  fixed-coefficient caveat.
- The strict Newton cone extends to nonsparse supports.  For any finite
  sum of monomials satisfying \(b>2a+c\), clear the largest denominator
  \(w^M\).  A maximum-denominator term already places the forced
  differential's point \((1,M-1)\) strictly inside its Newton polygon;
  adding all other supports preserves interiority.  Therefore every
  such sum is excluded whenever the cleared curve is Newton
  nondegenerate, in particular on a Zariski-open coefficient locus.
  Degenerate initial-form loci are not claimed.
- The degree-five modular hits reveal an infinite exact family rather
  than isolated seeds.  For any zero-constant
  \(H\in B_{\mathbb F_3}\), \(A=1+H^3\) is Poisson central and
  \[
  P=w+Auv,\qquad Q=-v+uv^2+Av^2w
  \]
  has bracket one.  This entire family has the same unrestricted
  first-lift obstruction:
  \[
  \ell(R)=[v]R+[uv^2]R.
  \]
  Frobenius exponent structure shows that only the correction monomials
  \(vw\) and \(v^2\) can reach these coefficients, and each contributes
  a cancelling pair, while exact integer expansion gives
  \(\ell(-E)=1\).  Hence no member lifts modulo \(9\).
- The basic \(u,w\), and \(v\) Hamiltonians are independently excluded by
  Laurent valuation or generic-fiber arguments.
- Exact rational linear algebra found no partner in the documented
  monomial/binomial support searches.
- A full-coefficient search, after the forced \(SL_2\) normalization of
  the linear \((v,w)\)-jets, eliminates every pair for which both reduced
  representatives have generator total degree at most \(4\).  The
  degree-four system has 44 variables and 75 equations; its exact
  Gröbner basis over \(\mathbb Q\) is \([1]\).  This is a bounded theorem,
  not a global obstruction.
- A separate unequal-degree calculation uses two exhaustive
  degree-preserving normalization charts and eliminates every ordered pair
  with
  \[
  \deg P\le2,\qquad \deg Q\le6.
  \]
  The degree-six charts have respectively 53 and 52 variables and 77
  nonzero equations; both exact rational Gröbner bases are \([1]\).
  Swapping the pair gives the corresponding unordered statement.  The
  degree-\((2,7)\) computation did not finish within its time bound, so no
  stronger bounded claim is made.
- Along \(D=(u,w)\), arbitrary nonhomogeneous pairs satisfy the universal
  boundary identity
  \[
  P_0'Q_1-P_1Q_0'=1.
  \]
  The next two boundary recurrences are also explicit and exactly
  verified.  They do not close the problem locally: \(P=v\) has a formal
  slice to every boundary order, but no global polynomial slice.
- The symplectic form is algebraically exact. An explicit polynomial
  primitive is

  \[
  \begin{aligned}
  \beta={}&-4v^2w\,du+w(1-2uv)\,dv\\
  &+2v(1+2uv)\,dw,
  \qquad d\beta=\Omega.
  \end{aligned}
  \]

  Moreover \(H^1_{\mathrm{dR}}(B)=0\), by the grading and an explicit
  weight-zero calculation.  Thus the remaining Pfaff problem is
  genuinely whether this primitive has the special form \(P\,dQ+dh\).
  On the Laurent chart,
  \(\beta=d(rw)+r\,dw\), yielding a useful generic-fiber residue test,
  but not yet a universal obstruction.

Full details:
[Route A memo](</Users/atharva/Documents/Jacobian Conjecture/route_a/ROUTE_A_MEMO.md>).

## Routes B and D: the \((72,108)\) frontier

The workspace did not contain the claimed finite coefficient system. It was
reconstructed from Proposition 4.3 of
[Guccione--Guccione--Horruitiner--Valqui](https://arxiv.org/abs/2204.14178).
There are two reduced branches for \([P,Q]=x^2\):

| branch | \(P\)-support points | \(Q\)-support points | nonzero bracket rows |
|---|---:|---:|---:|
| a/b | 25 | 47 | 92 |
| c | 61 | 125 | 302 |

Proposition 4.3 supplies these branches only after assuming the bounded
\((72,108)\) case (called case \((8,28)\) before the final degree scaling).
The computations below eliminate both branches and therefore rigorously
remove that bounded case, but do not by themselves prove \(JC(2)\).  A full
proof still needs an all-degree infinity argument; the result must not be
mistaken for such a reduction.

The universal equations are the bilinear coefficient equations

\[
\sum (uj-vi)a_{uv}b_{ij}
=\delta_{(r,s),(2,0)}
\]

for matching output exponent \((r,s)=(u+i-1,v+j-1)\).

An exact five-row left-null certificate excludes the whole forced-edge
one-parameter degeneration

\[
P_t=x+y^8(xy-t)^8.
\]

Its target pairing is \(576\), so no \(Q\) in the 125-point case-c support
can satisfy \([P_t,Q]=x^2\), for any \(t\).

This certificate is not universal. Adding \(\varepsilon xy\) produces the
explicit residual \(168\varepsilon\) on the \(Q\)-column \(x^9y^{16}\).
Therefore it does not by itself eliminate the free lower and interior
coefficients.

### a/b branch

The complete a/b branch is eliminated over characteristic zero.

For the outer equation
\[
UV+2wUV'-3wU'V=1,\qquad \deg U=7,\quad\deg V=10,
\]
the function \(R=wV^2/U^3\) satisfies \(R'=V/U^4\).  It is a degree-21
three-point cover with passport
\[
(2^{10},1),\qquad(3^7),\qquad(17,1^4).
\]
An exact Murnaghan--Nakayama evaluation of the Frobenius character formula
gives Hurwitz number five; all triples are transitive and have trivial
automorphism group.

Modulo \(p=32003\), the saturated normalized outer algebra is reduced of
length five.  Its eliminant is squarefree, and the two required outer
vertices \(u_7,v_{10}\) are units.  Over its two rational factors and one
irreducible cubic factor, the complete lower equations have only the affine
origin.  The verifier strengthens this to the projective statement
\[
L^{12}=M^{12}=N_0^2=N_1^2=0
\]
in every lower quotient.

The characteristic-zero bridge is geometric, not an inference from an
isolated finite-field calculation.  A Galois-closure monodromy group is a
subgroup of \(S_{21}\), so \(32003>21\) makes it prime to \(p\), and the
inertia orders \(2,3,17\) are tame.  Grothendieck's prime-to-\(p\) tame
specialization theorem for the constant marked curve
\((\mathbf P^1;0,1,\infty)\) (SGA 1, Exposé XIII, §2.10) identifies the
generic and special permutation triples.  Thus the automorphism-free rigid
Hurwitz scheme is finite étale of degree five over
\(\mathbf Z_{(32003)}\), and the modular \(u_1=1\) chart covers all five
fibers.

The original nonconstant lower blocks carry weights
\[
\operatorname{wt}(a_1,b_2)=1,\qquad
\operatorname{wt}(a_0,b_1)=2,\qquad
\operatorname{wt}(b_0)=3.
\]
Their four equations have weights \(1,2,3,4\), so nonzero lower solutions
form a closed subscheme of a proper weighted-projective bundle over the
Hurwitz scheme.  Any characteristic-zero point would specialize after a
finite valued-field extension, but the exact special fiber is empty.
Therefore no a/b-supported complex solution has all required Newton
vertices.

This is a theorem only for the bounded a/b branch supplied by the
\((72,108)\) reduction.  It is not an all-degree proof of \(JC(2)\).

### case-c branch

Write \(z=xy\) and expand

\[
P=z/y+\sum_{d=0}^{8}y^dp_d(z),\qquad
Q=z^2/y+\sum_{e=0}^{12}y^eq_e(z).
\]

The bracket equation is exactly the 21 graded identities

\[
\sum_{d+e=k}\bigl(e p_d'q_e-dp_dq_e'\bigr)
=\delta_{k,-2}z^2.
\]

The global diagonal exactness condition has the same Hurwitz base as the
a/b outer equation.  If
\[
C(q)=q^7+c_6q^6+\cdots+c_0,\qquad \deg R\le10,
\]
then exactness of the diagonal genus-three differential is equivalent to
\[
2CR'-3C'R=2q^{16}.
\]
With
\[
w=q^{-1},\qquad C=q^7U(w),\qquad R=-2q^{10}V(w),
\]
the left side is exactly
\[
2q^{16}\bigl(UV+2wUV'-3wU'V\bigr).
\]
Thus its scaling quotient is the same five-point degree-21 Hurwitz space.
Coefficient reversal gives
\[
u_i=c_{7-i},\qquad v_j=-\frac12[q^{10-j}]R.
\]
The normalization \(c_0=1\) is \(u_7=1\).  Since \(u_7\) has scaling weight
seven and the Hurwitz covers have no automorphisms, this slice has
\(5\cdot7=35\) geometric points.  This is the finite base for the transverse
elimination.

In radial coordinates
\[
P=\sum_i z^iA_i(w),\qquad Q=\sum_jz^jB_j(w),
\]
the assignments
\[
\operatorname{wt}(A_i)=2-i,\qquad
\operatorname{wt}(B_j)=3-j
\]
make the \(z^k\) bracket row homogeneous of weight \(4-k\).  Over all three
modular outer factors, the descending linear blocks leave only seven
noncentral parameters, of weights
\[
(1,1,2,2,3,3,4);
\]
every later block is uniquely solvable subject to growing consistency
conditions.  The complete 15-block recursion covers all 165 nonouter,
noncentral coefficients and gives 79 weighted-homogeneous consistency
equations.  Over each of the two rational modular outer points and over the
irreducible cubic factor, the exact Gröbner quotient has vector-space
dimension 328 and
\[
X_0^{32}=\cdots=X_6^{32}=0.
\]
Thus every geometric transverse fiber is supported only at the origin and
its weighted Proj is empty.  The cubic-field calculation handles the three
conjugate points simultaneously.

The remaining output rows, of radial degrees \(-12,\ldots,-21\), introduce
no coefficients.  They are logically unnecessary for projective emptiness:
the first 79 equations already have only the origin, and adding equations
cannot enlarge their zero set.  An optional exact check also reduces all
terminal rows over the first rational factor to zero modulo the consistency
ideal.

The computation is made in the \(u_1=1\) chart.  The invertible scaling
\[
(P,Q)(z,w)\mapsto
\bigl(\lambda P(z,\lambda w),\lambda Q(z,\lambda w)\bigr)
\]
transports these fibers to the \(u_7=1\) case-c slice.  Because seventh
powers are bijective in both modular coefficient fields, the checked
representatives cover all 35 normalized geometric points up to the free
\(\mu_7\)-action.

The required coefficients \([w^8]A_0,[w^{12}]B_0\ne0\) would give a nonzero
point of \(\mathbf P(1,1,2,2,3,3,4)\) after the fiberwise recursion.  To
avoid global pivot choices, the specialization argument projectivizes the
original 165 lower coordinates with weights
\(\operatorname{wt}(A_i)=2-i\) and
\(\operatorname{wt}(B_j)=3-j\).  Their bracket equations form a closed
subscheme of a proper weighted-projective bundle over the same finite étale
tame Hurwitz scheme used for a/b; the seven-parameter calculation proves
that its full special fiber is empty.  Hence any characteristic-zero case-c
point would specialize, after a finite valued-field extension, to a
special-fiber point, a contradiction.  Therefore the complete bounded
case-c branch is eliminated over characteristic zero.

Combining the a/b and case-c results eliminates both branches of the bounded
\((72,108)\) reduction.  This is not an all-degree reduction and therefore
is not a proof of \(JC(2)\).

### Universal outer edge

There is nevertheless an all-degree structural reduction at the leading
edge.  For coprime \(m<n\), set
\[
\deg U=mk+1,\qquad \deg V=nk+1,\qquad \delta=n-m.
\]
If
\[
\delta UV+mwUV'-nwU'V=E
\]
is a nonzero constant, then
\[
R=\frac{w^\delta V^m}{U^n},\qquad
\frac{R'}R=\frac{E}{wUV}.
\]
Thus \(R\) is a three-point cover of degree \(n(mk+1)\), with passport
\[
(m^{nk+1},\delta),\qquad
(n^{mk+1}),\qquad
((m+n)k+2,1^\kappa),
\]
where
\[
\kappa=((m-1)(n-1)-1)k+n-2.
\]
A negative \(\kappa\) is already a Riemann--Hurwitz obstruction.  One
normalization caveat is essential: \(E=1\) forces
\(U(0)V(0)=1/(n-m)\); constant terms \(U(0)=V(0)=1\) instead force
\(E=n-m\).

For \((m,n)=(2,3)\), exact character calculations at \(k=1,2,3,4\) give
Hurwitz numbers
\[
1,2,5,14.
\]
The lower linear block at deficit \(d\), with \(F=U/w,\ G=V/w\), is
\[
\mathcal L_d(A,B)
=w((m-d)AG'-nA'G+mFB'-(n-d)F'B).
\]
Putting \(c=m+n-d\) gives the factorization
\[
\frac{\mathcal L_d(A,B)}w
=-nG^{c/n}d(AG^{-(m-d)/n})
+mF^{c/m}d(BF^{-(n-d)/m}),
\]
and \(F^{c/m}/G^{c/n}=R^{-c/(mn)}\).  Hence the all-degree radial
deformation problem is a twisted de Rham complex on a Kummer cover of the
outer Belyi map.  A Riemann--Roch computation of its eigenspace
kernel/cokernel is the natural route to a uniform index theorem.  Such an
index alone does not yet prove that every nonlinear lower weighted fiber is
origin-only; that is the remaining all-degree obstruction.

The formal normal form and its lattice determinant are uniform in the
gcd-reduced pair.  If \(E\) is the outer constant,
\[
N=(m+n)k+2,\quad L=v_q^m/u_p^n,\quad
\sigma=\left(\frac{u_pv_qN}{E}(1-R/L)\right)^{1/N}=t+O(t^2),
\]
then a unique \(H=1+O(\sigma)\), followed by \(\zeta=zH\), gives
\[
P_{\rm out}=u_p\zeta^m\sigma^{-mk},\qquad
Q_{\rm out}=v_q\zeta^n\sigma^{-nk}(1-\sigma^N)^{1/m},
\]
and \(\{\zeta,\sigma\}=-\sigma\) times a unit with constant term one.
More generally, if \(\sigma=at+O(t^2)\), \(H=h+O(\sigma)\), then the
change on a Laurent window \(I\), with \(H\)-power \(e\), is upper
triangular with determinant
\[
a^{\sum_{j\in I}j}h^{e|I|}.
\]
It is unipotent in the canonical normalization.  For the
\((2,3)\), weight-at-most-eight source layers, the unnormalized product is
\[
a^{52k^2+113k+7}h^{76k-32};
\]
after absorbing the bracket unit, the target product is
\[
a^{100k^2+125k+28}h^{-20k-32}.
\]
No discriminant or resultant occurs locally.  Globally the outer ODE
reduces modulo \(U\) and \(V\) to
\(-nwU'V=E\) and \(mwUV'=E\); norming these identities shows that
\(\operatorname{Disc}(U),\operatorname{Disc}(V),\operatorname{Res}(U,V)\)
are already units on the tame Hurwitz locus.

This does not yet make the compatibility matrix a fixed graded module.
The transformed bounded polynomial spaces are outer-dependent lattices.
The individual jet maps are unipotently identified with standard windows,
but the obvious valuation filtration is not known to be strict for the
twisted differential.  Replacing the lattices by naive monomial Laurent
windows gives kernel profiles \((5,5,4,3,2,1,0,0)\),
\((7,7,6,5,4,3,2,1)\), and \((9,9,8,7,6,5,4,3)\) for
\(k=1,2,3\), rather than \((2,2,2,1,0,\ldots)\).  Thus
associated-graded strictness is exactly false for the naive filtration.
A direct polynomial parameterization described below now bypasses this
failure for the linear kernel.  The remaining structural task is to show
that the first 19 nonlinear compatibility rows commute with a
multiplicative filtered base change.  The determinant theorem rules out a
divisor obstruction; the unresolved information is extension data between
filtration grades.

An intrinsic reformulation narrows that gap.  With \(c=m+n-d\),
\(X=AG\), and \(Y=BF\), the linear layer is
\[
\frac{\mathcal L_d}{w}
=-n\left(dX-\frac cnX\,d\log G\right)
{}+m\left(dY-\frac cmY\,d\log F\right).
\]
The two summands are rank-one finite-monodromy Kummer connections.
Their canonical Deligne extensions have strict logarithmic de Rham
filtrations.  The bounded polynomial supports differ from those canonical
lattices by explicit elementary modifications at the roots of \(F,G\)
and at \(0,\infty\).  The modification matrices are root-value or
confluent root-jet evaluations; their possible divisors are precisely
leading coefficients, discriminants, resultants, and scalar residue
factors.  The first three types are units by the outer ODE, while the
residue factors depend only on \((m,n,d)\).  Completing this local
modification count gives one representation-theoretic route to the stable
linear multiplicities.

For \((m,n)=(2,3)\), those multiplicities now have a shorter all-\(k\)
proof.  Set \(c=5-d\).  For \(c\ne0\), every linear kernel pair is
parametrized by one polynomial \(C\):
\[
\begin{aligned}
A_C&=\frac{cwCU'+(d-3)CU-2wC'U}{c},\\
B_C&=\frac{cwCV'+(d-2)CV-3wC'V}{c},
\end{aligned}
\qquad
C=\frac{2UB-3VA}{E}.
\]
The exact identities
\[
\mathcal K_d(A_C,B_C)=wCE',\quad
2UB_C-3VA_C=EC,\quad
\mathcal K_d(2UT,3VT)=cET
\]
prove both directions and uniqueness.  Endpoint support leaves one
low-degree class at each of \(d=1,2,3\), and none at \(d=4\).  Any further
class has the common indicial degree \(ck+1\).  Its existence and
uniqueness follow from the two formal horizontal solutions
\[
u_p^{-c/2}w^{(d-3)/2}U^{c/2},\qquad
v_q^{-c/3}w^{(d-2)/3}V^{c/3}.
\]
Their ratio is \((L/R)^{c/6}=1+O(t^{5k+2})\), while their leading degree is
\(ck+1\); the contact margin is \(dk+1>0\), so their polynomial parts
coincide.  The \(d=5\) equation is an exact derivative, and for \(d\ge6\)
the lower and upper endpoint bounds are incompatible.  Therefore, for
every \(k\ge1\),
\[
\dim\ker\mathcal L_d=(2,2,2,1,0,\ldots).
\]
The seven weights \((1,1,2,2,3,3,4)\) are an all-\(k\) theorem for this
radial support.  Representatives are \(C=1\) and the nonconstant part of
\([u_p^{-2}w^{-1}U^2]_+\) at \(d=1\); \(C=w\) and
\(V-V(0)-V'(0)w\) at \(d=2\); \(C=w\) and
\(U-U(0)-U'(0)w\) at \(d=3\); and the degree-at-least-two part of
\([u_p^{-1/2}(wU)^{1/2}]_+\) at \(d=4\).

These \(C\)-classes also have an exact Hamiltonian interpretation.  After
normalizing \(E=1\),
\[
\Omega=dP_0\wedge dQ_0=\frac{z^4}{w^3}\,dz\wedge dw,\qquad
H_{d,C}=-\frac{z^{5-d}C}{(5-d)w}.
\]
The vector field defined by \(\iota_{X_H}\Omega=dH\) sends
\((P_0,Q_0)\) to the corresponding kernel pair.  Its formal flow preserves
the full bracket exactly.  If \(c=5-d,\ f=5-e,\ g=5-d-e\), the scalar
commutator is
\[
C\star D=-gw\left(
\frac{(wC'-C)D}{c}+\frac{C(D-wD')}{f}
\right).
\]
Thus the multiplicative structure is explicit: the remaining nonlinear
equations measure escape of Hamiltonian flows from the bounded Newton
support.  The sharp next theorem is a triangular first-escape formula in
weights four through eight for the seven displayed potentials.

The leading endpoint alone cannot supply that theorem.  The four high
classes have principal Hamiltonians
\[
-\frac{\xi^4}{4},\quad-\frac{\xi^3}{3},\quad
-\frac{\xi^2}{2},\quad-\xi,\qquad \xi=zw^k,
\]
so their principal brackets all vanish.  For high
\(C=w^{ck+1}+a w^{ck}+\cdots\) and
\(D=w^{fk+1}+b w^{fk}+\cdots\), the first possible bracket coefficient is
the normalized tail mismatch \(b/f-a/c\).  The outer contact identity makes
this vanish as well: through every polynomial term the four high classes
are truncations of \(w\chi^c\) for one common formal coordinate \(\chi\).
Their full brackets vanish identically, so the nonlinear information is
entirely in the discarded boundary tails.  Exact \(k=1,2\) calculation also
shows that the naive filtration by the seven \(C\)-degrees has initial ideal
only \(\langle X_1^4\rangle\), not an irrelevant ideal.  Finally, the
Darboux coordinates \(r=z^5/(5w),s=1/w\) do not give a local-nilpotence
shortcut: \(H=rs\) generates a non-locally-nilpotent scaling flow which
still preserves finite Laurent support.  A uniform proof must use boundary
tails or prove genuine two-boundary extension.

The required boundary rigidity is available conditionally on extension.
The \((2,3)\) outer Belyi map has a unique simple zero and a unique
\((5k+2)\)-ramified point.  Every deck transformation fixes both; its
multiplier at the simple zero is forced to one.  Hence its deck group is
trivial for every \(k\).  The independent orbit-count proof is the Bézout
identity \(3(2k+1)-2(3k+1)=1\).  What remains unproved is precisely the
bridge from a bounded nonlinear completion to an automorphism of this
compactified cover.

Neither trace nor finite Laurent flow supplies that bridge.  The bracket
of the low \(d=1\) and high \(d=4\) modes is
\[
h_D(w)=\frac34D(w)-wD'(w)\ne0.
\]
In the Darboux coordinates it generates a finite translation of \(r\)
while fixing \(s\), hence fixes \(w\) and the Belyi function \(R(w)\)
exactly.  On both rational points of the certified degree-\(21\) fiber
over \(\mathbf F_{32003}\), Newton sums show that
\(\operatorname{Tr}(w^j)\) is constant for \(0\le j\le12\); the trace map
on \(\langle w^{-1},1,\ldots,w^{12}\rangle\) has rank only two.  After
subtracting the constant \(\operatorname{Tr}(h_D)/21\), this same
nonzero flow is trace-zero.  Thus trivial deck group, two bounded
principal parts, trace zero, and finite Darboux support do not force a
Hamiltonian to vanish.

The countermodel fails at exactly the required integrality point.  It
sends \(z^5\) to \(z^5+B(w)\), which is not a fifth power in
\(K(w)(z)\) for \(B\ne0\).  Conversely, any rational symplectomorphism
preserving \(R\) has \(w\) fixed by deck rigidity and hence satisfies
\(\phi(z)^5=z^5+B(w)\); rationality forces \(B=0\), and an identity jet
forces \(\phi(z)=z\).  The useful next invariant is therefore the first
escape from the original fifth-root lattice, not a trace or automorphism
of the outer cover.

There is also a complete conditional target-ring theorem.  If
\(P,Q\in K[P_0,Q_0]\), their \(z\)-bounds force
\[
P=aP_0+c,\qquad Q=bQ_0+\lambda P_0+d.
\]
The fixed edge gives \(a=b=1\), and the forbidden \(w^{-1}\) coefficient
in the \(z^2\)-block of \(Q\) gives \(\lambda=0\).  Thus, after additive
normalization, ring descent forces \(P=P_0,Q=Q_0\).  The open bridge is not
target rigidity but proving this ring descent from the two boundary
conditions.  One cannot infer descent from the trivial deck group:
\(K(t)/K(t^3+t)\) is a degree-three extension with trivial deck group but
\(t\) is not in the base field.

There is now a complementary conditional theorem on the source side.  Let
\(T=(X,Y)\) be the normalized algebraic branch of \(F_0^{-1}\circ F\) in
the original case-c plane.  If both \(X,Y\) are integral over
\(K[x,y]\), its graph is finite.  Away from \(x=0\), divisors with \(X=0\)
are excluded by the zero-dimensional fibers of the étale map \(F\), and
the remaining graph is a base change of the étale locus of \(F_0\).
Purity makes it a finite étale cover of
\(\mathbb G_m\times\mathbb A^1\).  Such a connected cover is Kummer,
\(u^e=x\), but the selected outer valuation has
\[
x=z^2t,\qquad v_t(x)=1
\]
and the normalized branch lies in \(K(z)((t))\); hence \(e=1\).  Thus the
branch is rational and, by normality, polynomial.  The chain rule then
gives
\[
X=cx,\qquad Y=c^{-3}y+h(x).
\]
The identity jet fixes \(c=1\), and the first nonzero term \(a_rx^r\) of
\(h\) creates the forbidden layer
\[
2a_rz^{2r+3}w^{-r-1}U'(w)
\]
in \(P\).  Therefore original-plane integrality of the branch would force
\(T=\mathrm{id}\).

Polynomiality of \(P,Q\) alone does not give this integrality.  The pair
\[
F_0=(x^2,xy),\qquad F=(x^2+(xy)^2,xy)
\]
has polynomial components, the same Jacobian \(2x^2\), and the same
contracted critical line, while its normalized inverse branch is
\[
\left(x\sqrt{1+y^2},\,y/\sqrt{1+y^2}\right).
\]
The second coordinate has a divisor pole.  This exact stress test isolates
properness/finiteness of the selected graph component as the remaining
bridge.

Exact boundary coordinates now expose the first nonlinear square chain.
Set
\[
Y_0=X_0-2X_1,\qquad
Y_2=X_2-\frac23X_3,\qquad
Y_3=X_4-X_5.
\]
They measure the constant or linear pieces discarded from \(U^2/w,V,U\).
For every complete coefficient field at \(k=1,2,3\), weight four contains
\[
\left(Y_2-\frac{(4k+1)^2}{16k}Y_0^2\right)^2,
\]
and on \(Y_0=Y_2=0\), weight six contains a nonzero multiple of \(Y_3^2\).
This is exact finite-scale evidence for an endpoint/BCH identity; the
displayed coefficient has not yet been proved for arbitrary \(k\).
The longer \(k=1\) chain with a common factor \(G\) fails exactly at both
\(k=2\) and \(k=3\), so it is not a universal mechanism.

The first Kummer resonance gives a stronger factorized integrality
obstruction.  The
five nonzero \(d+e=5\) Hamiltonian brackets translate \(z^5\) by five
polynomials \(B_j(w)\).  Those polynomials are independent over the complete
\(k=1,2\) coefficient fields and every \(k=3\) factor, already on the fixed
\(w^4,\ldots,w^8\) coefficient window.  If an exact ordered rational
factorization through weight five isolates the resonant translation,
rationality of that factor therefore forces
\[
X_0X_6=X_1X_6=X_2X_5=X_3X_4=X_3X_5=0.
\]
This does not follow from rationality of the composite time-one map, even
after lower-weight factors have been removed: rationality need not pass to
the flow of the leading logarithmic symbol.
The endpoint determinant is the normalized Wronskian at \(w=0\) of
\(B_j/w^4\).  Its explicit \(5\times5\) jet matrix is universal, but local
ODE data do not force it nonzero; a formal \(u_2=u_3=0\) specialization
kills it.  All-\(k\) nonvanishing still needs a global passport theorem.
Conditionally on exact rational factorization, the displayed product
ideal leaves six coordinate strata for the next descent step.  They are
the combinations of \(X_6=0\) or \(X_0=X_1=0\) with one of
\[
X_4=X_5=0,\qquad X_3=X_5=0,\qquad X_2=X_3=0.
\]
An exact flow audit shows that every one still contains nonzero algebraic
Hamiltonian flows.  The low axes integrate to square or cube roots.  For a
high principal Hamiltonian
\[
H=-a(zw^k)^c/c,\qquad N=5k+2,
\]
the exact flow is
\[
Z=z\left(1-Nat\,\frac{w^{ck+2}}{z^{5-c}}\right)^{k/N},\qquad
W=w\left(1-Nat\,\frac{w^{ck+2}}{z^{5-c}}\right)^{-1/N}.
\]
Its binomial has a simple divisor, so the autonomous flow is not rational.
This is not an obstruction to a general time-one completion, whose higher
Hamiltonians can change the map.

The endpoint equalities have an exact interpretation:
\[
Y_0=0:\ H_1=-(P_0^2-x^2)/4,\quad
Y_2=0:\ H_2=-(Q_0-x^2y)/3,\quad
Y_3=0:\ H_3=-(P_0-x)/2.
\]
The square relations consequently reduce four strata to
\(H_1+H_3\), \(H_2+H_4\), \(H_4\), and \(H_3+H_4\), respectively.
The two \(d=1,d=2\) strata retain the larger graph
\(Y_2=(4k+1)^2Y_0^2/(16k)\).  No unconditional rational-descent identity
currently eliminates these pieces; the source-integrality theorem above
would eliminate all six simultaneously.

Exact \(k=1,2\) reconnaissance changes the expected index pattern.  Both
tiny cases have the same seven kernel weights
\[
(1,1,2,2,3,3,4)
\]
as \(k=3\), and no later kernels.  The earlier guess of two copies of
\(1,\ldots,k\) plus \(k+1\) is therefore false; the stable range follows
\(m+n-d>0\), not \(d\le k+1\).

The full \(k=1,2\) consistency ideals are origin-only, with quotient
dimensions 243 and 225.  More significantly, equations of weights at most
eight already suffice.  Their quotient dimensions are 255 for \(k=1\), 247
for \(k=2\), and 380 for \(k=3\); in the last case the same value occurs over
both rational outer points and the cubic factor.  All seven \(32\)-nd powers
reduce to zero in every prefix ideal.  For \(k\ge2\), this is the same
19-equation finite jet.  A uniform proof would express its weight-descending
pure-power certificates over the universal outer Hurwitz algebra and prove
the relevant determinants are units from the passport.  That symbolic
stabilization, rather than further degree enumeration, is the current
all-degree target.

The top edge has

\[
p_8=a h^8,\qquad q_{12}=b h^{12},\qquad h=z-t,
\]

and exact descent gives \(p_7=h^4r\).  The upper grades
\(E_{12},\ldots,E_{20}\) have now been solved in all parameters.  If
\(A_j=(P^{j/8})_+\), then

\[
Q=\sum_{j=4}^{12}c_jA_j+S_3,\qquad
c_j\in\mathbb C,\quad \deg_yS_3\le3,
\]

with
\[
c_{11}=c_{10}=c_9=c_7=c_6=c_5=0
\]
universally.  The \(c_{10}\) statement follows
from the denominator-free endpoint identity
\[
256r_4E_{14}-512E_{13}
=2688r_4\left(p_{5,7}-\frac{r_4s_3}{2}\right)^2,
\]
together with the required vertex
\([h^8]p_6=r_4^2/4\ne0\).  The remaining lower modes are killed by the
grade-13 \(c_9\) endpoint followed by the \(U,X\) square cascade recorded
in `current_context/CASE_C_UNIVERSAL_FRACTIONAL_DESCENT.md`.  Moreover, for
\(H=A_4=(P^{1/2})_+\),

\[
P-H^2\quad\hbox{has \(y\)-degree at most three}
\]

and the exact three-chart calculation proves

\[
h^4\mid p_6-\frac{r^2}{4a}.
\]

The next middle coefficient is now controlled on all five \(h\)-adic
charts:

\[
h^4\mid p_5-\frac{rs}{2a}
\]

for every \(\operatorname{ord}_h(r)=0,1,2,3,4\).  Consequently the
\(y\)-coefficient of the canonical approximate square root \(H\) is
polynomial universally.  Exact pole witnesses show that the upper grades
alone could not finish this step; the decisive contradictions occur in the
lower equations, as late as grades 9 and 11.

The constant coefficient has now been closed on the charts
\(\operatorname{ord}_h(r)=0,2,3,4\).  In the maximal normalization \(r=h^4\),
put
\[
p_5=h^4(S/2+W),\qquad
D_4=p_4-\frac{S^2}{4}-\frac{h^4W}{2}.
\]
Exact compatibility ideals first contain the fourth power of
\([h^2]D_4\).  After that coefficient vanishes, the three remaining
subcharts contain respectively the third, third, and fifth powers of
\([h^3]D_4\).  Hence
\[
h^4\mid D_4
\]
throughout this chart, and the constant coefficient of \(H\) is polynomial
there.  On the \(r_0\)-unit chart, an endpoint row first gives
\(12w_3^2=0\), after which the last row is
\(-9r_0^2e_3^2/8=0\).  On the \(r_3\)-unit chart, exact radical ideals
contain \(e_2^3,e_2^4\) and then \(e_3^3,e_3^5\) across its subcharts.
Thus the only remaining order for this last divisibility is
\(\operatorname{ord}_h(r)=1\).

On the now-closed \(r_0\)-unit chart, the approximate-root descent also
eliminates every remaining fractional resonance above the degree-three
remainder.  In normalized \(a=b=1\) coordinates, the raw \(q_{10,10}\) and
\(q_{9,9}\) rows become
\[
-\frac{45}{16}r_0^3c_{10}=0,\qquad
-\frac{135}{128}r_0^3c_9=0
\]
after the first equation is imposed.  Keeping the integral parameter
\(c_8\), exact comparison of the \(q_{7,7},q_{6,6},q_{5,5}\) slots with
\(A_{12}+c_8P\) then gives
\[
c_7=c_6=c_5=0.
\]
Thus
\[
\boxed{c_{10}=c_9=c_7=c_6=c_5=0}
\]
on this chart.  All five displayed vanishings are now global by the
required-\(r_4\) endpoint cascade above.  The integral terms \(c_8P,c_4H\)
and the lower cubic remainder remain and require separate analysis.

On this chart the remaining coupled equations can now be written without
the fractional basis.  If
\[
P_+=H^2+R,\qquad
Q_+=H^3+\frac32HR+c_8P_++c_4H+S,
\qquad \deg_yR,\deg_yS\le3,
\]
then the nonlinear upper bracket is exactly
\[
[P_+,Q_+]=[P_+,S]-\left(\frac32R+c_4\right)[H,R].
\]
Together with the two fixed-base cross-terms, this is the reduced system
for \(E_{11},\ldots,E_{-1}\).  No claim that \(R\) or \(S\) vanishes has
yet been established.  Its top row can, however, be solved exactly: if
\(\sigma_3=[y^3]S\), then
\[
\sigma_3(h)=\kappa h^3+\frac32t\,h^4+\frac32h^5.
\]
The free \(\kappa h^3\) is the one-dimensional kernel of the \(E_{11}\)
Euler operator.  The low coefficients of \(E_{10}\) then force
\[
h^2\mid [y^3]R,\qquad \kappa=0
\]
on \(r_0\ne0\).  After the first two coefficients of \([y^2]S\) are
solved, the next endpoint is
\[
[h^3]E_9=\frac{15}{2}r_0\bigl([h^2y^3]R\bigr)^2,
\]
so \(h^3\mid[y^3]R\).  After the resulting \([y^2]S\) resonance is fixed,
the next row is
\[
[h^1]E_8=-\frac{27}{8}r_0^2
\bigl([h^3y^3]R\bigr)^2.
\]
Therefore \(h^4\mid[y^3]R\) on the closed \(r_0\)-unit chart.  This is a
divisibility statement, not yet the vanishing of the cubic remainder.
Writing \([y^3]R=h^4(u_4+u_5h+u_6h^2)\) and
\(a_0=[h^0y^2]R\), the already-solved coefficient
\([h^5y^2]S=3(r_4+u_4u_5)/4\) cancels the apparent next resonance.
The preceding row fixes the constant coefficient of \([y]S\).  Restoring
both solved terms in \(E_8[h^3]\) gives the square
\[
-3(2a_0-r_0u_4)^2=0,
\]
so \(a_0=r_0u_4/2\).  The next row fixes the remaining \([y]S\)
resonance, and the paired \(E_7[h^0]\) residual then vanishes identically.
Restoring all further \(E_{10}\)-solved coefficients of \([y^2]S\) through
\(h^8\), and then the \(E_9\)-solved coefficients of \([y]S\) through
\(h^4\), gives the directly checked lower rows
\[
\begin{aligned}
E_7[h^1]&=\frac9{16}r_0
 (-2a_1+r_0u_5+r_1u_4)^2,\\
E_7[h^2]&=0,\\
E_7[h^3]&=\frac98r_0
 (-2a_2+r_0u_6+r_1u_5+r_2u_4)^2.
\end{aligned}
\]
Hence
\[
a_1=\frac{r_0u_5+r_1u_4}{2},\qquad
a_2=\frac{r_0u_6+r_1u_5+r_2u_4}{2}.
\]
After the next two coefficients of \([y]S\) and the first two nonconstant
coefficients of \([y^0]S\) are solved upstream, the direct full expression
also gives
\[
E_7[h^4]=0,\qquad
E_7[h^5]=\frac38r_0
 (-2a_3+r_1u_6+r_2u_5+r_3u_4)^2.
\]
Thus \(a_3=(r_1u_6+r_2u_5+r_3u_4)/2\).  The four relations obtained so
far are precisely the first four coefficients of
\[
2h^4[y^2]R-r(h)[y^3]R.
\]
This exact coefficient pattern does not yet prove the full polynomial
identity by itself.  The completed finite endpoints are
\[
E_8[h^{15}]=6r_4^2u_6^2,\qquad
E_6[h^{13}]=-\frac{27}{32}r_4^2(2a_5-r_4u_5)^2.
\]
Because \(r_4\ne0\), they give \(u_6=0\) and \(a_5=r_4u_5/2\).  If
\[
d_4=2a_4-r_3u_5-r_4u_4,
\]
the only remaining coefficient of this first defect divided by \(h^4\)
is \(d_4h^4\).  The next exact pair gives
\[
r_0E_7[h^7]-2E_6[h^3]
=\frac34(r_0d_4-4b_0+2s_0u_4)^2,
\]
so \(b_0=r_0d_4/4+s_0u_4/2\).  This is the leading coefficient of
\[
\Delta_1=4h^4[y^1]R-2s[y^3]R-r\Delta_2/h^4.
\]
The following direct square is
\[
6r_0E_5[h^1]-6r_1E_5[h^0]-r_0^2E_6[h^5]
=\frac{27}{32}r_0^2([h^5]\Delta_1)^2,
\]
which fixes
\[
b_1=\frac{r_1d_4+2s_0u_5+2s_1u_4}{4}.
\]

These defects are coefficients of one formal quotient.  For
\[
A(T)=h^4+\frac r2T+\frac s2T^2+\frac w2T^3+H_0T^4,\qquad
B(T)=\rho_3+\rho_2T+\rho_1T^2+\rho_0T^3,
\]
write \(B/A=\sum c_kT^k\).  Direct algebra gives
\[
\Delta_{3-k}=2^kh^8c_k\quad(k=1,2,3).
\]
Thus the structural goal is \(h^8\)-divisibility of the successive
\(\Delta_j\), or equivalently absence of \(h\)-poles in the quotient
coefficients.  The degrees \(6,7\) of \(\Delta_1\) remain to be killed;
degree \(8\) is the permitted constant coefficient.

This recurrence also absorbs the fixed base: since
\(P-H^2=T^{-3}(B+zT^4)\), the next quotient numerator satisfies
\[
\Delta_{-1}
=16h^4z-16H_0\rho_3
-\frac r{h^4}\Delta_0
-\frac{2s}{h^4}\Delta_1
-\frac{4w}{h^4}\Delta_2,
\qquad
c_4=\frac{\Delta_{-1}}{16h^8}.
\]
Hence the base term is part of the same quotient-polynomiality problem.

The solved remainder coefficients also admit one uniform binomial
description.  Put \(C=B_{\rm full}/A\).  Then
\[
P^{3/2}=T^{-12}A^3+\frac32T^{-7}A^2C
+\frac38T^{-2}AC^2+O(T^3),\qquad
P^{1/2}=T^{-4}A+\frac12TC+O(T^6).
\]
Thus the complete \(\sigma_3,\ldots,\sigma_0\) chain is the
nonnegative-\(y\) part of
\(P^{3/2}+c_8P+c_4P^{1/2}\), up to one additive constant.  The fixed
coefficient \(q_{-1}=z^2\) consequently satisfies the exact terminal
identity
\[
z^2=\frac32zH_0+\frac38[T^3](AC^2)+c_8z+\frac{c_4}{2}c_0.
\]
Here
\[
[T^3](AC^2)
=2\rho_0c_0-\frac w2c_0^2+\frac r2c_1^2+2h^4c_1c_2,
\]
which is polynomial under the already-proved defect divisibilities.
The grade-seven equation on the mismatch \(M\) is
\(-8h^7(M+hM')=0\); its Laurent resonance \(1/h\) is excluded by that
polynomiality, so the terminal identity is forced.

More generally, a first mismatch \(n_kh^ky^{-m}\) has multiplier
\(-8(m+k)\).  Its unique Laurent resonance is the leading term of
\(P^{-m/8}\).  Thus, in the completed Laurent field and with
\(S=P^{1/8}\), the formal centralizer is
\(\ker[P,-]=\mathbb C(t)((S^{-1}))\).  Every mate consequently has the formal
normal form
\[
Q=P^{3/2}+c_8P+c_4P^{1/2}+\kappa_0
+W_P+\sum_{m\ge2}\lambda_mP^{-m/8},
\qquad [P,W_P]=z^2y^{-2}.
\]
At the target order \(m=10\), the target is nonresonant and
the leading particular solution is
\[
-\frac1{40}h^{-5}-\frac t{16}h^{-6}
-\frac{t^2}{24}h^{-7}+\lambda_{10}h^{-10}.
\]
After removing \(\lambda_{10}P^{-10/8}\), the next Euler operator has
cokernel \(h^{-4}\), while the complete \(p_7\)-forcing contributes
\[
-\frac38r_0t^2.
\]
Thus the required \(r_0t\ne0\) excludes the entire \(r_0\)-unit chart by a
formal-tail obstruction, independently of the finite descent.

This is a residue statement on the weighted face.  For
\(q=T/h^{4-j}\) and
\(P_{\rm face}=h^{8j-24}q^{-8}a(q)^2\), exactness of the full fiber
differential would force exactness of its first noncentral face
differential.  This follows by taking the first nonzero term in the Rees
filtration of \(dQ\), subtracting functions of the face polynomial whenever
that term is central, and passing to the finite eighth-root extension.
The \(j=0\) residue is \(r_0t^2/64\).  For \(j=2\), with
\(a=1+(r_2/2)q+(s_0/2)q^2\), the cokernel is
\[
\frac5{1024}r_2t^2(r_2^2-16s_0),
\]
which is nonzero on both preceding branches \(s_0=0\) and
\(s_0=r_2^2/8\).

For \(j=1\) the scalar residue vanishes, but the face differential is still
nonexact.  On the cover \(y^2=x^8-1\), Hermite reduction is
\[
\frac{x^{14}dx}{y^5}
=d\left(-\frac{x^7}{12y^3}\right)
+\frac7{12}d\left(-\frac{x^7}{4y}\right)
+\frac7{16}\frac{x^6dx}{y}.
\]
The remaining second-kind differential cannot be exact: involution
averaging would make a primitive \(yB(x)\), whereas
\[
d(yx^n)=((n+4)x^{n+7}-nx^{n-1})dx/y
\]
cannot produce \(x^6dx/y\).

The finite Newton support does not exclude the initial negative formal tail
by itself; the obstruction is its failure to extend one order farther, or
equivalently the nonexact associated-graded fiber differential.
Indeed the terminal equation and every required vertex are compatible with
\(R=0\), \(H_0=2(z-c_8)/3\), and
\(c_8,t,r_0,r_4\ne0\), with the additive constant supplying the
\(Q\)-constant vertex.  This witness has
\(\Delta_2=\Delta_1=\Delta_0=0\) but
\(\Delta_{-1}=16h^4z\), so it is not a full solution.  The remaining
obstruction must control the negative formal tail rather than rely on
terminal matching or vertex nonvanishing alone.  With \(c_4=0\), its first
omitted coefficient is \([y^{-6}]F=3z^2h^{-4}/8\), producing the nonzero
Euler row \(6h^3(2h^2+3th+t^2)\).

Together with the exact order-two constant descent, these weighted-face
arguments exclude \(\operatorname{ord}_h(r)=0,1,2\).  Within this local
method the frontier was reduced to \(\operatorname{ord}_h(r)=3,4\).
Polynomial square-root
descent is already proved on both remaining charts, but the first face
differential there is exact or degenerate.  Normalizing the negative tail
through \(m=14\), with the complete \(p_7,\ldots,p_4\) square-root blocks,
gives vanishing cokernels at \(m=11,12,13\) and the first transverse
condition
\[
-\frac3{16}s_0t(s_0+s_1t)=0.
\]
Thus only the subbranches \(s_0=0\) and \(s_1=-s_0/t\) remain.  At the
next order the genuine cubic-remainder face enters, so a further secondary
Rees obstruction is still required.  Exact continuation through \(m=19\)
currently transfers rather than obstructs: on \(s_0=s_1=0\), the next
cokernels fix \([h]p_3=0\) and then
\([1]p_2=5w_0^2/48\) when \(w_0\ne0\); on
\(s_1=-s_0/t,\ s_0\ne0\), they successively solve the leading
coefficients of \(p_3,p_2,p_1\).  No invariant contradiction is known on
either branch.

The global seven-parameter radial certificate above supersedes this local
frontier and eliminates both of these charts at once.  The local analysis is
retained because it records the approximate-root geometry, not because an
open bounded case remains.

The 2026 graded-plane theorem does not eliminate these systems. It proves
that a plane counterexample cannot carry a nontrivial
\(\mathbb G_m\)-equivariance; the two-dimensional Newton polygons are not
themselves homogeneous for a single weight.

Full details:
[full Route B/D memo](</Users/atharva/Documents/Jacobian Conjecture/ROUTE_B_FULL_MEMO.md>).

## Route C: chart-preserving étale surface maps

On \(S: x^2y=z^2-1\), the following exact families were eliminated.

### Full separated/equivariant ansatz

Every étale endomorphism of the form

\[
(x,y,z)\longmapsto(xA(z),yB(z),R(z))
\]

is, up to scalings and signs, a Chebyshev map

\[
\Phi_d(x,y,z)=\bigl(xU_{d-1}(z),y,T_d(z)\bigr).
\]

For every \(d>1\), an interior critical-level curve
\(C_{r_k}\cong\mathbb G_m\) is sent to one of the deleted boundary lines.
Thus no nontrivial member preserves either affine-plane chart.

### Non-equivariant LND conjugations

For every \(f(x)\in\mathbb C[x]\), conjugating \(\Phi_2\) by

\[
\tau_f(x,y,z)=
\left(x,y+2f(x)z+f(x)^2x^2,z+f(x)x^2\right)
\]

still fails. The explicit curve

\[
(x,y,z)=
\left(s,f(s)^2s^2-s^{-2},-f(s)s^2\right),
\qquad s\in\mathbb C^\times,
\]

lies in the affine-plane chart and maps to the deleted divisor. The induced
chart formula has constant Jacobian on its domain but a genuine pole along
this curve.

The subansatz whose first chart coordinate depends only on \(x\) was also
classified and gives only triangular automorphisms.

Full details:
[Route C memo](</Users/atharva/Documents/Jacobian Conjecture/route_c/ROUTE_C_MEMO.md>).

## Three-dimensional descent and the fixed-plane construction

The July 2026 three-dimensional counterexample has determinant \(-2\) and
three exact rational points in one fiber. Its hyperbolic invariant quotient
has

\[
\operatorname{Jac}(P,Q)=2L^2
\]

and contracts \(L=0\). This is a degenerate quotient map, not a plane Keller
map.

The most direct target slice has inverse image \(xL=0\). On \(x=0\), the
restriction is a triangular plane automorphism. The component \(L=0\) that
contains the other collision points is \(\mathbb G_m\times\mathbb A^1\);
in natural coordinates its map is Laurent and has ordinary Jacobian
\(2/x^4\). Thus the known three-dimensional collision does not restrict to
the required polynomial plane collision.

Full details:
[current-context note](</Users/atharva/Documents/Jacobian Conjecture/current_context/README.md>).

Much stronger no-go results now surround this direct descent:

- every affine target plane in the normalized
  linear-times-degree-\(d\) factorization cover is excluded for every
  \(d\ge2\);
- all linear fibers through the displayed collision are excluded;
- all three triangular target-coordinate orientations through degree four
  are excluded for affine source graphs through a collision pair.
- the cubic discriminant is a genuinely nonlinear target invariant whose
  pullback is a polynomial submersion, but its irreducible level through the
  three collision points has Euler characteristic \(3\), rather than
  \(\chi(\mathbb A^2)=1\).

These are construction-family theorems, not a proof of \(JC(2)\).

### Fixed source plane \(x=1\)

Fixing the source plane rather than the target produces the live ring

\[
R=\mathbb Q[a,b,c]\subset\mathbb Q[t,c],\qquad t=y+1,
\]

with

\[
a=t+t^2-ct^3,\qquad b=2+4t-3ct^2.
\]

It has an exact quadratic-field collision, so any Darboux pair in \(R\)
would immediately be a plane counterexample.  The image relation is

\[
27A^2C^2-18ABC+16A+B^3C-B^2-3BC-2C+4=0.
\]

Its conductor factor and normalization minors satisfy

\[
D=4-3bc-3c,
\qquad
1=\frac c2\{a,b\}+\frac b2\{a,c\}-a\{b,c\}.
\]

Thus module generation is not the obstruction; the problem is exact
decomposability/integrability.

After localizing at \(c\), the same ring has the structural pinch form
\[
\mathbb Q[c^{\pm1},x,y]/\bigl(y^2-x(x-9c)^2\bigr),
\qquad
x=(3ct-2)^2,\quad y=(3ct-2)(x-9c).
\]
Writing \(U=F+yG,\ V=P+yQ\), the constant-bracket equation restricts on
the conductor \(x=9c\) to
\[
F_xP_c-F_cP_x=0,\qquad
G(P_c+9P_x)-Q(F_c+9F_x)=\frac1{54c^2}.
\]
This replaces bounded coefficient searches by an exact parity/Bézout
boundary problem for arbitrary target degrees.

The normalized area form itself is nevertheless exact over the target
ring.  With
\[
p=\frac{27AC^2-15BC+16}{6},\quad
q=\frac{3B^2C-4B-3C}{12},\quad
r=\frac{12AB-B^3+3B+2}{12},
\]
the form \(\alpha=p\,dA+q\,dB+r\,dC\) pulls back to
\(-2c\,dt-t\,dc\), so \(d\alpha=dt\wedge dc\).  Ordinary de Rham
cohomology therefore cannot close this route: the live question is the
stronger factorization \(\alpha+dS=U\,dV\) with \(U,V\in R\).  The same
identity gives
\[
t=\frac{b-2-9ca}{4-3bc-3c},
\]
pinning the failure of the obvious canonical coordinate exactly on the
conductor.

The following exact results now hold:

- no linear target Hamiltonian has a polynomial mate of any degree;
- if \(U=u_2(t)c^2+\cdots\) and \(u_2\) is nonsquare, then \(U\) has no
  polynomial mate of any degree;
- the square-leading submersion family
  \[
  U_r=(b+1)^2+ra
  \]
  has no mate of any degree, by a homogeneous Laurent-Hamiltonian ODE;
- no pair with both target degrees at most two exists.  The complete wedge
  solution forces a Plücker coordinate to be \(9/16\), whereas every actual
  wedge \(u\wedge v\) forces it to vanish.
- no pair of target degrees \((2,3)\) or \((3,2)\) exists.  After the
  all-degree nonsquare reduction, the square-leading locus is covered by
  four normalization charts, and every exact rational Gröbner basis is
  \([1]\).
- if a Hamiltonian \(U\in\mathbb Q[a,b]\) has any polynomial mate, the
  Laurent Hamiltonian equation and the submersion condition force
  \[
  U=C+\gamma a+a^2\Delta K(a,b)
  \quad\hbox{or}\quad
  U=C+\lambda b+a^2\Delta K(a,b),
  \qquad \Delta=(b+1)^2-12a.
  \]
  Submersion alone permits puncture powers \(a(b+1)^m\), but the lowest
  Laurent coefficient of the bracket excludes every \(m\ge1\), including
  arbitrary \(a^2G\) tails.  Exact resultants and saturated coefficient
  ideals then exclude both displayed branches for every affine \(K\), so
  any surviving \(a,b\)-only Hamiltonian requires even \(\deg K\ge4\)
  and square top specialization \(K_k(t,3)\); the primitive-leading
  obstruction excludes every odd degree and every nonsquare even degree.
  Exact target-coordinate resultants and saturated ideals exclude the
  full quadratic square-top locus, including every lower deformation.
  Uniform target-gradient equations also exclude every monomial \(K\) in
  all degrees, and every nonzero univariate tail \(K=K(a)\).  Thus the
  first remaining possibility has even \(\deg K\ge4\), square top
  specialization, and genuinely mixed support involving \(b+1\).
  In both branches, every univariate \(K=K(b+1)\) is excluded as well;
  the \(a\)-branch proof uses an explicit parametrization of the two
  formal Hamiltonian-ODE branches and a root-multiplicity count.  The
  quartic stratum
  \[
  K=M_2(a,b+1)^2+k_0+k_1a+k_2(b+1)
  \]
  is closed for every affine lower deformation.  A degree-four survivor
  must therefore contain genuinely nonlinear lower-degree terms.

The remaining quadratic construction locus has square leading coefficient
and requires a partner of target degree at least four.  Small-coefficient
exact scans find only the already-excluded \(U_r\) submersion family, but
that scan is not itself an all-parameter proof.

Full details:
[fixed-plane memo](</Users/atharva/Documents/Jacobian Conjecture/current_context/FIXED_SOURCE_PLANE_ROUTE.md>).

## Dual ledgers

### Construction ledger

- Exact characteristic-\(3\) plane counterexample from the pseudo-plane.
- Infinite exact Frobenius-central Route A family
  \(P=w+(1+H^3)uv,\ Q=-v+uv^2+(1+H^3)v^2w\) over
  \(\mathbb F_3\); every member is obstructed modulo \(9\).
- Formal \(3\)-adic lifts to every order, with necessarily escaping support.
- Exact three-dimensional characteristic-zero counterexample and quotient
  mechanism, but no valid plane descent.
- Exact noninjective fixed-source-plane target subalgebra, with its Darboux
  equation reduced to a singular-hypersurface Nambu equation.
- Exact nonproper étale Chebyshev surface maps, all failing the chart
  condition.

### Obstruction ledger

- No homogeneous Route A Darboux pair in characteristic zero.
- No affine-linear Route A Hamiltonian admits any polynomial slice.
- No Route A Hamiltonian \(cx_i+f(x_j)\), for distinct generators
  \(x_i,x_j\), admits a polynomial slice of any degree.
- More generally, no separated Route A Hamiltonian
  \(a x_i+b x_j+f(x_k)\) admits a polynomial slice when
  \((a,b)\ne(0,0)\).
- No mixed Route A Hamiltonian \(av+C(u)w+F(u)\), \(a\ne0\), admits a
  polynomial slice, for arbitrary polynomial \(C,F\).
- No bilinear Route A Hamiltonian \(cw+\lambda uv\), \(\lambda\ne0\),
  admits a polynomial slice; this includes the nonhomogeneous
  characteristic-\(3\) seed \(w+uv\).
- More generally, no \(cw+\lambda uv+F(u)\), \(\lambda\ne0\), admits a
  polynomial slice for any \(F\in\mathbb C[u]\).
- No variable-coefficient Hamiltonian
  \(C(u)w+\lambda uv+F(u)\), \(\lambda\ne0\), admits a polynomial slice;
  all 17 low-degree characteristic-\(3\) seed Hamiltonians are covered by
  this or the elementary-family theorem.
- More generally, no
  \((b+\lambda u)v+C(u)w+F(u)\), \((b,\lambda)\ne(0,0)\), admits a
  polynomial slice.
- No \(cw+\lambda uv+\mu v^2\), \(c\lambda\mu\ne0\), admits a polynomial
  slice.
- More generally, no \(cw+\lambda uv+G(v)\), \(c\lambda\ne0\), admits a
  polynomial slice for any \(G\in\mathbb C[v]\).
- No \(cw+\lambda uv+\nu vw\), \(\nu\ne0\), admits even a rational slice.
- Although \(w+uv\pm w^2\) gives new characteristic-\(3\) pairs, no
  \(u(b+\kappa u)v+C(u)w+F(u)\), \(b\ne0\), admits a
  characteristic-zero polynomial slice.
- Both \(w^2\)-perturbed characteristic-\(3\) pairs have an all-support
  two-coefficient obstruction to lifting modulo \(9\).
- No \(w+uv+\kappa uvw\), \(\kappa\ne0\), admits a rational slice; the
  residue proof also applies over \(\mathbb F_3\).
- No \(w+uv+\kappa uv^2\), \(\kappa\ne0\), admits a rational slice in
  characteristic zero or characteristic \(3\).
- No \(w+uv+\kappa v^2w\), \(\kappa\ne0\), admits a rational slice in
  characteristic zero; the characteristic-\(3\) search is negative
  through partner degree \(25\).
- No \(cw+H(uv)\), \(c\ne0\), with nonlinear \(H\), admits a rational
  slice in characteristic zero.  Its minimal quadratic-tail orbit is
  also excluded in characteristic \(3\).
- No \(w+uv+\kappa uv^3\), \(\kappa\ne0\), admits a rational slice in
  characteristic zero.  Its new positive-sign characteristic-\(3\)
  pair has an all-support obstruction modulo \(9\).
- The remaining degree-four orbits \(uv^2w,u^2vw,v^3w,u^3v\) admit no
  rational slice in characteristic zero; the \(uv^2w\) residue proof
  also works in characteristic \(3\).
- The monomial-cone theorem excludes every characteristic-zero
  \(w+uv+\kappa u^av^bw^c\) with \(a>b\ge1\), every non-affine diagonal
  case, and every \(b>a,\ b\ge2a+c-1\).
- In the middle wedge, \(2(b-a)-c\mid b\) is excluded for every
  coefficient, and all remaining exponents are excluded generically in
  the coefficient.
- The first residue-zero middle-wedge wall
  \(2a+c-b=2\) is excluded for every coefficient by a canonical-jet
  computation showing \(L(E)=k\).
- The Fourier canonical-staircase criterion excludes every
  fixed-coefficient middle-wedge monomial with
  \(2(b-a)-c>(2a+c-b)^2\).  Parity improves this region as described
  above, and the entire second and third inner walls
  \(2a+c-b=3,4\) are now excluded as well.
- Every fixed-coefficient middle-wedge monomial with
  \(\gcd(2(b-a)-c,\,2a+c-b)=1\) is excluded by the complementary
  canonical-gap/function-basis theorem.
- The multibranch Fourier extension removes the coprimality restriction:
  every monomial in the former middle wedge is excluded for every
  nonzero coefficient.  Combined with the outer cone theorem, all
  non-affine reduced monomial perturbations with positive \(u\)- and
  \(v\)-exponents are now excluded in characteristic zero.
- Finite nonsparse perturbations strictly behind the three faces of an
  exposed middle-wedge monomial are excluded generically in their
  coefficients by the same Fourier principal-part mismatch.
- The three-signature dichotomy characterizes every support not covered
  by that theorem as a ratio-tie face or one of four
  separated-extremizer configurations.
- The coefficient-uniform global first-face theorem excludes all four
  separated types and every first-face tie whenever the maximal Laurent
  denominator is at least two.  The horizontal denominator-one family
  is excluded for all coefficients by the reciprocal-residue lemma.
  Consequently every nonzero finite middle-wedge sum is now excluded
  in characteristic zero.
- Newton-nondegenerate finite sums supported in \(b>2a+c\) are excluded
  by the same interior differential.
- Every member of the Frobenius-central characteristic-\(3\) family has
  the same all-support \([v]+[uv^2]\) obstruction modulo \(9\).
- No Route A Darboux pair has ordered generator-degree bounds \((2,6)\).
- The symplectic form is exact, so de Rham cohomology is not the obstruction.
- The full bounded a/b branch is eliminated over characteristic zero by
  the exact degree-five Hurwitz count, prime-to-\(32003\) tame
  specialization, and the empty proper weighted-projective lower fiber.
- The full bounded case-c branch is also eliminated over characteristic
  zero.  Its 35-point diagonal locus is the sevenfold slice of the same
  Hurwitz base, and its seven-parameter modular consistency ideals have only
  the affine origin over all five geometric outer points.
- Consequently both branches of the bounded \((72,108)\) reduction are
  closed.  This bounded result is not an all-degree proof of \(JC(2)\).
- The case-c upper grades have a complete approximate-root normal form;
  all five middle-divisibility charts are closed, so the \(y\)-coefficient
  of the approximate square root is polynomial.  The constant coefficient
  is polynomial on the \(\operatorname{ord}_h(r)=0,3,4\) charts; these local
  facts are now supplementary to the global radial obstruction.
- The full separated Route C ansatz and all polynomial LND-shear conjugates
  of \(\Phi_2\) fail chart preservation.
- Every nontrivially \(\mathbb G_m\)-equivariant plane Keller map is an
  automorphism, according to the current graded theorem.
- Every factorization-cover affine-plane descent is excluded in all degrees.
- Every linear fixed-plane Hamiltonian, every nonsquare-leading quadratic
  Hamiltonian, the infinite primitive-leading family \(a(b+1)^m\), and the
  square-leading \(U_r\) family are excluded in all partner degrees.
- Every fixed-plane Hamiltonian in \(\mathbb Q[a,b]\) is confined to the
  two \(a^2\Delta K\) boundary families above, and their full affine-\(K\)
  strata are excluded by exact critical-point resultants.  In higher
  degree, only even \(K\) with square \(K_k(t,3)\) can survive; the
  entire quadratic square-top stratum and every all-degree monomial
  stratum are also closed, as is every univariate \(K(a)\) tail; both
  branches also exclude every univariate \(K(b+1)\), and the
  quartic square-top stratum remains closed after an arbitrary affine
  lower deformation.  A surviving degree-four tail must therefore have
  genuinely nonlinear lower-degree terms.
- The fixed-plane conductor problem is formally unobstructed: an explicit
  logarithmic Darboux pair exists in the completed pinch ring.  Globally,
  however, every conductor-adapted monomial rational chart retains a
  nonzero odd multiple of \(d\log(x/c)\); cancellation would require a
  half-integral valuation.  The remaining gap is to prove the same residue
  parity for arbitrary nonmonomial descended charts.
- In the all-degree finite standard system, the equation-Jacobian has
  exact weight \((m-1)(n-1)\) and is a nonzero constant along a Keller
  section.  Its natural weighted degeneration necessarily escapes every
  affine chart while the determinant vanishes to exactly that order.  If
  \(g=\gcd(m,n)\), the first boundary cone is classified exactly by
  \(C^g=R(x)\), with \(R\) monic of degree \(g\) and zero
  \(x^{g-1}\)-coefficient.  This closes \(g=1\), but for \(g>1\) there are
  coefficient-bound-compatible maximal-slope arcs and the determinant
  order is the largest permitted one.  Thus the remaining invariant is
  transverse contact to this common-root cone, not affine monodromy or a
  larger Groebner calculation.  More precisely, on every actual
  standard-system solution the equation-Jacobian is, up to sign,
  \(\operatorname{Res}_x(P_x,Q_x)\).  At
  \(P_0=R^{n/g},Q_0=R^{m/g}\) its Sylvester corank is
  \(\min(n,m)-1\), and the first transverse term is the resultant of
  \(P_{0,x}\) with the Euclidean remainder of the derivative
  perturbations.  A Hensel factorization distributes the determinant
  order over the roots of \(R\) and \(R'\).  There is no smaller
  Hessian-only upper bound: turning on the single allowed normal
  parameter \(\lambda_{m-1}=L\) gives
  \(\det J=\pm n^{m-1}L^{n-1}\) when \(n<m\), and
  \(L=\lambda_{m-1}\tau^{m-1}\) already saturates
  \((n-1)(m-1)\).  This saturating direction is not tangent to the
  equation fiber.  The full \(n-1\)-dimensional kernel is parametrized
  by arbitrary polynomial variations \(T=\dot P\), while only
  \(T=aR^{a-1}\dot R\) is tangent to the reduced common-root cone.
  For \(P=R^a+\epsilon T\), the first generic normal equation occurs at
  \(\ell_0=\lfloor b/a\rfloor+1\) and is the negative part of
  \(R^{b-a\ell_0}T^{\ell_0}\).  Thus the residual lemma must control a
  genuine nonreduced cancellation cascade and force submaximal contact
  on at least one root or critical-point cluster.  A raw squarefree
  approximate-root induction is false before target normalization:
  \(P=R^a+c\tau^n\), together with
  \(\lambda_{nq}=\binom{b/a}{q}(-c)^q\), makes the whole negative block
  polynomial through order \(m+n-2\).  This is exactly the binomial
  orbit of the removable target translation \(P\mapsto P-c\), and it
  still fails the final \(\tau^{m+n-2}x^{1-n}\) forcing.  Any corrected
  induction must therefore work with invariants of this triangular
  translation action on
  \(\lambda_k,\lambda_{k+n},\lambda_{k+2n},\ldots\).  More strongly,
  the whole \(g\)-multiple sector is a formal approximate-root
  reparametrization gauge: for
  \(P=R^a(1+\kappa(\tau^g/R)^c)\), suitable
  \(\lambda_{gq}\)'s make the second expression equal \(R^b\) through
  order \(N+1\), even when \(c<a\) and the deformation is genuinely
  \(x\)-dependent.  The homogenized Keller identity
  \[
  \tau(P_XQ_\tau-P_\tau Q_X)+nPQ_X-mQP_X=-c\tau^N
  \]
  nevertheless gives an exact invariant.  At a first graded
  deformation of order \(d<N\), with
  \(Z=aV-bU\), it reduces to
  \(gRZ'+dR'Z=0\), so a nonzero rational relative deformation is
  possible only when \(g\mid d\) after choosing the Kummer exponent
  minimally.  The remaining \(Z=0\) case is exactly the nonreduced
  \(n-1\)-dimensional normal kernel, so this congruence does not by
  itself finish the induction.

  Restricting the same identity to an individual normalization branch
  \(\gamma\) of \(P=0\) gives the exact Gelfand--Leray formula
  \[
  d(Q/\tau^m)
  =-c\,\tau^{n-3}\frac{d\tau}{P_X|_\gamma}.
  \]
  Hence, if \(\tau=t^e\), the \(t^{em}\)-coefficient of
  \(\tau^N/P_X|_\gamma\) must vanish.  This condition must be imposed
  branchwise: the sum over all branches is identically zero, and even
  a single boundary cluster can cancel.  The local model
  \(P=s^a+\kappa\tau^{n-2}s\), whose perturbation has order
  \(-2\bmod g\), has a nonzero forbidden coefficient on every branch
  while their sum cancels.  Pure \(g\)-sector branches start instead
  at order \(m+g-2\); they are detected immediately when \(g=2\) and
  are invisible for \(g>2\).  The remaining all-degree lemma is
  therefore precise: after quotienting the \(g\)-sector gauge, the
  final forcing must be shown to create this resonance on at least one
  individual branch.  Proving that the \(Z=0\) nilpotent cascade cannot
  cancel all such branch resonances is the current gap.

  The publication boundary is important here.  Heitmann's Theorem 2.5
  already makes \(JC(2)\) equivalent to exactness of the generic
  Gelfand--Leray differential forcing genus zero, and Friedland develops
  its Gauss--Manin/monodromy form.  The potentially new content above is
  therefore only the explicit finite-standard-system boundary grading,
  resultant/contact formula, reparametrization countermodels, and
  branch-resonance reduction; generic exactness itself is not new.
  A naive local Brieskorn obstruction also fails.  Although the leading
  \(g\)-sector singularity has a nonzero
  \(\zeta^{-2}\)-class represented by
  \(\tau^{n-3}ds\wedge d\tau\), the primitive is meromorphic at infinity.
  In coordinates
  \(\tau=y^{-1}\), \(z=y^{g-1}(x-\alpha y)\), polynomial descent forces
  \(\operatorname{ord}_z p_r,\operatorname{ord}_z q_r
  \ge\lceil r/(g-1)\rceil\) for positive Laurent order \(r\).  Exact
  coefficient extraction shows that the value at \(z=0\) of the
  \(\tau^{g-3}\) bracket coefficient is only
  \[
  p_{-1}(0)q'_{g-1}(0)-p'_{g-1}(0)q_{-1}(0),
  \]
  the negative Jacobian of the affine-linear tails.  Thus the apparent
  local Brieskorn forcing is supplied across the pole filtration by the
  original linear Jacobian; it is not a contradiction.  The most
  promising non-brute-force target is consequently a pole-filtered
  monodromy lemma in the trace-zero \(A_{a-1}\) local system of
  \(\Phi(z)=u\), after quotienting both the \(g\)-sector gauge and this
  endpoint pairing.  That is a strict graded refinement of Heitmann's
  formulation; it remains unproved.

## Reproduction

From the workspace root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python verify_all.py
```

The bundled verification checks:

- the pseudo-plane relation, Poisson brackets, characteristic-\(3\) seed,
  first Hensel lift, primitive, plane pullback factor, and all six
  triangular generic-fiber identities;
- 12 exact \(3\)-adic stages;
- both finite Newton support inventories and the five-row certificate;
- the exact a/b outer Hurwitz character sum and count;
- the universal coprime outer-edge passport and the exact \(k=1,\ldots,4\)
  Catalan counts for the \((2,3)\) family;
- the exact \(k=1,2\) radial rank profiles, nonlinear consistency ideals,
  and origin-only weight-\(\le8\) finite-jet certificates;
- the exact identification of the 35-point normalized case-c diagonal locus
  with the sevenfold slice of the same five-orbit Hurwitz space;
- the complete 165-coefficient case-c radial recursion and the exact
  seven-variable modular projective-emptiness certificate over all five
  outer points;
- the case-c approximate-root identities, pole witnesses, and completed
  valuation charts;
- the Route C surface identities, canonical Jacobians, exceptional curves,
  and generic quadratic-shear specialization;
- the three-dimensional determinant, exact collision, quotient square
  factor, and failed direct slice;
- the all-degree factorization-plane obstruction and the fixed-plane
  normalization, conductor, recurrence, Laurent-ODE, and Plücker
  obstructions;
- the formal fixed-plane conductor solution, its rational residue model,
  and the odd residue lattice for both monomial orientations;
- the standard-system equation weights, determinant weight, complete
  \((n,m)=(2,3)\) toy elimination, and common-root corank/determinant
  saturation for structural \(\gcd=2,3\) examples, together with the
  target-translation and \(g\)-multiple reparametrization
  countermodels, the homogenized mod-\(g\) normal equation, and the
  branchwise Keller-residue resonance and pole-filtered endpoint
  pairing.

All bundled checks pass exactly. This is a research-progress package, not a
proof or counterexample over \(\mathbb C^2\).

The external-Singular unequal-degree certificate is reproduced separately
by:

```sh
.venv/bin/python route_a/unequal_bounded_groebner.py --q-degree 6
```
