# Publication and route audit: the fixed-source plane

Date: 24 July 2026

## Bottom line

The fixed-source-plane work now contains the core of a potentially
publishable construction/no-go note, but not yet a paper whose main theorem
resolves a recognized open case of the plane Jacobian conjecture.  Its
strongest defensible contribution is an explicit nonnormal plane-section
framework in which a plane Keller counterexample is equivalent to a
polynomial Darboux pair in one concrete pinch ring, together with exact
local/global obstructions and broad all-degree exclusions.

The new global conductor-image theorem materially improves the prospective
paper: a hypothetical pair maps the pinch conductor to a curve with
\(\mathbf G_m\)-normalization by an even-degree power cover, and it must
create either an affine coexceptional component over that curve or a
different dicritical image at infinity.  This is a structural theorem, not
a bounded search.  It still does not exclude either alternative.

## Results that form a coherent paper

1. **Explicit nonnormal target.**  The fixed plane in the verified
   three-dimensional Keller map has target ring
   \[
   R=\mathbf Q[t+t^2-ct^3,\;2+4t-3ct^2,\;c]
   \subset\mathbf Q[t,c],
   \]
   with an exact quadratic-field collision and an explicit hypersurface
   equation.

2. **Pinch normalization and exact Darboux reduction.**  After localizing at
   \(c\), the ring is
   \[
   \mathbf Q[c^{\pm1},x,y]/(y^2-x(x-9c)^2),
   \]
   and a plane counterexample inside this fixed ring is equivalent to one
   exact Nambu/Darboux equation.  The conductor involution, boundary
   equations, target-ring Liouville form, and normalization denominator
   are explicit.

3. **Local obstruction is proved insufficient.**  The conductor completion
   admits an exact formal Darboux pair, and the boundary-filtration map is
   surjective enough to absorb every first Bockstein obstruction.  This is
   valuable negative information: it proves that the problem is genuinely
   global rather than an artifact of an incomplete local calculation.

4. **All-degree no-go theorems.**  Every linear Hamiltonian, every
   primitive-leading family, the square family
   \((b+1)^2+ra\), broad univariate/monomial tail families, and several
   complete exceptional leading strata have no mate.  There are also exact
   complete low-degree exclusions.

5. **Global conductor theorem.**  For a hypothetical pair, the conductor
   image has \(\mathbf G_m\)-normalization, its normalization cover is a
   power map, the original conductor cover has even degree, and the two
   compactified conductor ends are marked cusp arms of types \((2,5)\) and
   \((2,3)\), both totally ramified.  Euler characteristic gives the exact
   alternative
   \[
   e^{-1}(\Gamma)\supsetneq C
   \quad\text{or}\quad
   S_e\text{ has a component different from }\Gamma.
   \]

## Novelty evidence and its limits

- Exact web searches for the defining formulas
  \(t+t^2-ct^3\), \(2+4t-3ct^2\), and the hypersurface relation returned no
  indexed mathematical source.
- The 123-page Borisov--Gabber--Vasiu manuscript and Borisov's
  *Unramified planar self-maps* contain the relevant weak-type and
  coexceptional machinery, but text searches show no pinch/conductor
  treatment of this explicit ring.
- The fixed-plane results are therefore not visibly duplicated by those
  two closest sources.  This is evidence, not a proof of novelty.  A real
  submission still needs MathSciNet/zbMATH and citation-chain searches,
  especially for nonnormal intermediate subalgebras of
  \(\mathbf C[x,y]\), affine modifications, and Danielewski/pseudo-plane
  methods.

## What prevents submission as a major theorem

- The live class of Hamiltonians in the fixed ring remains infinite and is
  not classified.
- The global dichotomy does not prohibit either an affine coexceptional
  curve or a second dicritical image.
- Several impressive exclusions rely on exact Gröbner certificates.  They
  are reproducible, but a paper needs small human-checkable propositions
  around them rather than a catalogue of computations.
- Closing this route would rule out a particular plane descent of the
  three-dimensional example.  It would not prove the plane Jacobian
  conjecture unless an additional universality theorem put every
  hypothetical counterexample into this ring.

## Recommended paper scope

A focused note could be organized around one statement:

> The explicit fixed plane produces a nonnormal pinch target whose
> normalization is noninjective, but any internal plane Keller map is
> forced into a two-puncture, even-degree conductor cover with an affine
> coexceptional/dicritical-image alternative; local conductor obstructions
> alone cannot decide existence.

The all-degree Hamiltonian exclusions should support that statement as
selected examples, not dominate the title or abstract.  The strongest
version worth submitting would add one projective incidence theorem
connecting the two marked cusp arms to Borisov's cyclic quotient
coexceptional point.

## Route comparison

- **Fixed plane / global coexceptional geometry:** best route for a
  publishable explicit case study and possibly for ruling out this descent.
  The next bottleneck is geometrically precise: resolve the two marked cusp
  arms and decide their incidence with the dicritical/coexceptional tree.
- **Standard/Kummer route:** closer to a universal resolution of the plane
  conjecture.  A successful invariant there would apply to every degree
  pair, whereas even a complete fixed-ring theorem is construction-specific.
- **More endpoint, conductor-jet, or bounded \(K\)-search:** poor marginal
  value.  The exact formal solution and filtration-surjectivity theorem
  already show why finite local layers can be adjusted away.

Thus the evidence supports continuing the global coexceptional analysis
for the fixed-plane project, while keeping the standard/Kummer route as the
primary route to the user's full objective.
