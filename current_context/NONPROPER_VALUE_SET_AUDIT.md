# Nonproper-value-set audit for the fixed-source plane

Date: 24 July 2026

## Conclusion

The finite-cover argument in §1.13 of `FIXED_SOURCE_PLANE_ROUTE.md` is
standard and correct, but a standard dicritical-parametrization theorem
actually decides its displayed alternative more strongly.

Let
\[
e=(U,V):\mathbf A^2_{\mathbf C}\longrightarrow\mathbf A^2_{\mathbf C}
\]
be a hypothetical nonautomorphic Keller map arising from the fixed pinch
ring, let \(S_e\) be its nonproper-value set, and let \(\Gamma\) be the
image of the pinch conductor.  Section 1.12 proves
\[
\widetilde\Gamma\simeq\mathbf G_m.
\]
On the other hand, every irreducible component of \(S_e\) is the image of
a nonconstant polynomial map
\[
\mathbf A^1\longrightarrow\mathbf A^2.
\]
It follows that \(\Gamma\) cannot be a component of \(S_e\).  Consequently
the second alternative in (8cc) is mandatory:
\[
\boxed{\quad S_e\text{ has an irreducible component }\Lambda\ne\Gamma.\quad}
\]
No assumption about \(e^{-1}(\Gamma)\) is needed.

This does not rule out the hypothetical map.  It does remove the ambiguity
between the two proposed continuations: the global route must study the
additional dicritical component(s), not try to prove that the conductor
image is itself the whole nonproper-value set.

## The exact standard inputs

### 1. The finite complement cover

Z. Jelonek, *The set of points at which a polynomial map is not proper*,
Ann. Polon. Math. **58** (1993), 259--266,
DOI [10.4064/ap-58-3-259-266](https://doi.org/10.4064/ap-58-3-259-266).

For a dominant polynomial map \(f:\mathbf C^n\to\mathbf C^n\):

- Proposition 7 identifies the nonproper set \(S_f\) by the leading
  coefficients of the integral equations of the source coordinates and
  proves
  \[
  \mathbf C^n\setminus f^{-1}(S_f)\longrightarrow
  \mathbf C^n\setminus S_f
  \]
  is proper, hence finite.
- Corollary 9 says \(S_f\) is empty or a hypersurface.
- Theorem 15 says a nonempty \(S_f\) is uniruled and gives degree bounds.

For a Keller map, the displayed finite restriction is also étale.  Thus the
pullback-cover construction in §1.13 is standard.  Its specialization to the
explicit conductor curve is project-specific, but the mechanism is not a
new theorem about polynomial maps.

The important caveat is that the standard source complement is
\(\mathbf A^2\setminus e^{-1}(\Gamma)\), not
\(\mathbf A^2\setminus C\).  The latter requires the additional equality
\(e^{-1}(\Gamma)=C\).

### 2. Polynomial parametrization of every plane component

Nguyen Van Chau, *Two remarks on non-zero constant Jacobian polynomial
maps of \(\mathbf C^2\)*, Ann. Polon. Math. **82** (2003), 39--44,
DOI [10.4064/ap82-1-4](https://doi.org/10.4064/ap82-1-4).

The introduction records that a nonempty nonproper set is a curve whose
components are polynomially parametrized.  More precisely, Lemma 5 proves
from dicritical Newton--Puiseux series that
\[
A_f=\bigcup_{\phi\ \mathrm{dicritical}} f_\phi(\mathbf C),
\]
and that every irreducible component \(\ell\) is exactly
\[
\ell=f_\phi(\mathbf C)
\]
for one such nonconstant polynomial map \(f_\phi:\mathbf A^1\to\mathbf
A^2\).

The same fact is stated at the beginning of:

Nguyen Van Chau, *Note on the Jacobian condition and the non-proper value
set*, Ann. Polon. Math. **84** (2004), 203--210,
DOI [10.4064/ap84-3-2](https://doi.org/10.4064/ap84-3-2).

That paper additionally proves that the entire nonproper-value curve of a
nonsingular polynomial self-map, if nonempty, has one point at infinity.
This condition is compatible with several branches or normalization places
lying above the same projective point, so by itself it does not contradict
the two-puncture theorem for \(\Gamma\).

## Why a polynomially parametrized component cannot normalize to
\(\mathbf G_m\)

Suppose an integral affine curve \(L\) with normalization
\(\nu:\mathbf G_m\to L\) admits a nonconstant dominant polynomial
parametrization
\[
p:\mathbf A^1\longrightarrow L.
\]
Since \(\mathbf A^1\) is normal, the universal property of normalization
factors \(p\) through a morphism
\[
\widetilde p:\mathbf A^1\longrightarrow\mathbf G_m.
\]
But such a morphism corresponds to a unit in \(\mathbf C[t]\), and
\[
\mathbf C[t]^\times=\mathbf C^\times.
\]
Thus \(\widetilde p\), hence \(p\), is constant, a contradiction.

Apply this with \(L=\Gamma\).  Since §1.12 proves
\(\widetilde\Gamma\simeq\mathbf G_m\), \(\Gamma\) is not an irreducible
component of \(S_e\).

Finally, \(S_e\) cannot be empty for the hypothetical map.  If it were
empty, Jelonek's properness result would make \(e\) finite; the nonzero
constant Jacobian makes it finite étale.  A finite étale cover of
\(\mathbf A^2_{\mathbf C}\) is trivial, so \(e\) would be an automorphism,
contrary to the verified conductor collision.  Hence \(S_e\) is nonempty,
and any one of its components supplies the required \(\Lambda\ne\Gamma\).

## Effect on novelty and the next direction

The following pieces remain potentially novel as an explicit package:

- the fixed pinch ring and exact Darboux reduction;
- the proof that the conductor image has \(\mathbf G_m\)-normalization;
- the even power-cover and marked cusp-arm data;
- the interaction of those data with a **mandatory different** dicritical
  image.

The fact that a nonproper component is polynomially parametrized is old,
and the complement finite-cover method is old.  A paper should cite these
inputs and state the new conclusion as their application to the explicit
conductor theorem.

The promising continuation is now:

1. Let \(\Lambda\ne\Gamma\) be a mandatory dicritical component.
2. Use Chau's 2004 one-point-at-infinity theorem on the union \(S_e\):
   the projective closures of all its components meet the line at infinity
   at the same single point.
3. Resolve simultaneously the two totally ramified conductor ends
   (types \((2,5)\) and \((2,3)\)) and a polynomially parametrized
   dicritical branch of \(\Lambda\) above that one point.
4. Test the resulting incidence and determinant labels against the
   connected boundary tree and the Borisov
   coexceptional/ample-ramification constraints.

This is a finite combinatorial-geometric compatibility problem after the
local branches are fixed, and is more targeted than further coefficient
brute force.
