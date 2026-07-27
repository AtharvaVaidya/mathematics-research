# Source audit: the GGHV import used in the degree-125 manuscript

Date: 25 July 2026

Source audited: J. A. Guccione, J. J. Guccione, R. Horruitiner, and
C. Valqui, *Increasing the degree of a possible counterexample to the
Jacobian Conjecture from 100 to 108*, arXiv:2204.14178v1 (29 April
2022), 25 pages.  The arXiv record currently contains only v1.

This memo audits only the external implication chain used by
`papers/degree-125-bound/main.tex`.  It does not audit the new
eliminations in that manuscript.

## Verdict

The exact Newton polygons and the equation `[P,Q]=x^2` imported from
GGHV Proposition 4.3 are correct.  The interpretation of the displayed
sets as vertex presentations of the full Newton polygons, followed by
taking every lattice point in their convex hull as an *allowed*
coefficient position, does not strengthen the proposition.  The
unimodular `(x,y)`-exponent to `(z,h)`-exponent map in the manuscript is
also correct.

There is one real citation-level omission in the manuscript's stated
external chain:

- GGHV Theorem 2.1 says that below 125 the only surviving degree pairs
  are `(72,108)` and `(108,72)`.
- The additional assertion that a surviving degree-108 counterexample
  belongs to exactly one of the two corner cases `A_0=(8,28)` and
  `A_0=(9,27)` comes from the exhaustive table on GGHV page 3, not from
  the statement of Theorem 2.1 alone.  GGHV says on pages 2--3 that this
  table is based on the tables in Sections 5 and 6 of its reference
  [5], arXiv:1708.07936.

Thus the intended implication is supported by the public source, but a
publication draft should explicitly import “Theorem 2.1 together with
the complete-case table on page 3 (based on [5])”.  Without that phrase,
the three-item list in the manuscript does not itself state the
degree-pair-to-corner-case exhaustion on which the final proof relies.

## Exact statement audit

### Small-degree exhaustion

- **GGHV Theorem 2.1, PDF page 2:** if `(P,Q)` is a counterexample, then
  either `max(deg P,deg Q) >= 125`, or its degree pair is `(72,108)` or
  `(108,72)`.
- **GGHV complete-case table, PDF page 3:** among the ten small cases,
  exactly two rows have maximum degree 108: `A_0=(8,28)` with
  `(m,n)=(3,2)`, and `A_0=(9,27)` with `(m,n)=(2,3)`.
- The prose on PDF page 2 explicitly says there are two cases with
  degree pair `(72,108)`, and that one is discarded in Section 5 while
  the other is left open in GGHV.

The theorem number in the manuscript, “Theorem 2.1”, is correct.

### Elimination of the `(9,27)` case

- **GGHV Proposition 4.1, PDF page 5:** a counterexample in case
  `(9,27)` yields `P,Q in L^(1)` with `[P,Q]=x` and

  ```
  N(P)={(0,0),(1,1),(6,16),(6,18),(0,18)},
  N(Q)={(0,0),(1,0),(9,24),(9,27),(0,27)}.
  ```

- **GGHV Theorem 5.1, PDF page 14:** rules out a slightly more flexible
  polynomial system with bracket `x+g(y)` and the required two boundary
  ends.
- **GGHV Corollary 5.7, PDF page 20:** rules out exactly the pair of
  Newton polygons produced by Proposition 4.1.  Its proof translates
  `x` and invokes Theorem 5.1.

The numbering and the manuscript's elimination claim are correct.
Corollary 5.7 is the exact terminal statement; Proposition 4.1 is the
normal-form input and Theorem 5.1 is the ingredient used by the
corollary.

### Exact Proposition 4.3 alternatives

**GGHV Proposition 4.3, PDF page 10**, states that a counterexample in
case `(8,28)` yields `P,Q in L^(1)` with `[P,Q]=x^2` and one of exactly
the following alternatives:

1. ```
   N(P)={(0,0),(1,0),(8,14),(8,16),(0,8)},
   N(Q)={(0,0),(2,1),(12,21),(12,24),(0,12)};
   ```
2. ```
   N(P)={(0,0),(1,0),(8,14),(8,16)},
   N(Q)={(0,0),(2,1),(12,21),(12,24)}.
   ```

The proof identifies its preliminary cases a) and b) with alternative
2 and preliminary case c) with alternative 1 (PDF pages 11--12).
Accordingly, the manuscript's labels “a/b alternative” for item 2 and
“case c” for item 1 are accurate.

The last monomial morphism in the GGHV proof is

```
x -> x^(-1),   y -> x^4 y.
```

GGHV records that its Jacobian factor is `-x^2`; a nonzero scalar
rescaling gives the proposition's normalized equation `[P,Q]=x^2`.
Therefore the sign and monomial normalization imported by the
manuscript are legitimate.  The exact statement itself already has
positive `x^2`.

## Newton-polygon notation and the support map

GGHV v1 does not define `N(P)` afresh.  At the end of its introduction
(PDF page 2) it says that it uses the notation and conventions of its
earlier papers.  In Proposition 4.3 and its proof, it repeatedly calls
the displayed objects the “Newton Polygons” and calls the listed points
their corners.  Thus the braces are a vertex-list presentation, not the
claim that the polynomial's support consists only of the listed
vertices.

Under the inherited convention, a Newton polygon is the convex hull of
the actual support.  Consequently:

- every support exponent lies in the displayed convex hull;
- every displayed extreme vertex has a nonzero coefficient;
- an interior or non-extreme lattice coefficient may be zero.

This is exactly what the manuscript needs.  Its 61 and 125 positions are
the complete ambient sets of lattice positions allowed by the two
polygons; its equations do not require every such coefficient to be
nonzero.  The sentence “all displayed vertices have nonzero
coefficients” is correct.

For

```
z=xy,  h=xy^2,
```

the exponent map is

```
(a,b) -> (2a-b,b-a),
```

with determinant 1.  The relevant vertices map as follows:

```
P: (0,0)->(0,0), (1,0)->(2,-1),
   (8,14)->(2,6), (8,16)->(0,8), (0,8)->(-8,8);

Q: (0,0)->(0,0), (2,1)->(3,-1),
   (12,21)->(3,9), (12,24)->(0,12), (0,12)->(-12,12).
```

Hence item 2 has exactly the five consecutive block indices
`P: z^0,z^1,z^2` and `Q: z^0,z^1,z^2,z^3`, while item 1 extends these
to `P: z^(-8),...,z^2` and `Q: z^(-12),...,z^3`.

Also

```
det(d(z,h)/d(x,y))=h,  x^2=z^4/h^2,
```

so `[P,Q]_(x,y)=x^2` is equivalent to
`[P,Q]_(z,h)=z^4/h^3` with the standard bracket orientation.  No
additional support or bracket hypothesis is introduced here.

## Field hypothesis

The arXiv v1 source writes all statements over a symbol `K` but does not
explicitly redeclare `K` in this paper.  It instead says on PDF page 2
that the notation and conventions of references [1], [2], [3], and [5]
are in force.  Reference [1], arXiv:1401.1784 / J. Algebra 471 (2017),
starts with `K` a field of characteristic zero and later states that
`K` is assumed algebraically closed unless otherwise specified.

The new manuscript works over an algebraically closed characteristic-zero
field and first reduces to `C`; this is within the source's intended
scope.  Still, because the field convention is implicit rather than
stated in arXiv:2204.14178 itself, a polished version should say that
the GGHV statements are being used with their inherited
algebraically-closed characteristic-zero convention.

## Recommended manuscript correction

Replace the first two items of the external-chain list by wording of the
following form:

1. “GGHV Theorem 2.1, together with the exhaustive small-case table on
   its page 3 (based on GGHV reference [5]), reduces a counterexample of
   maximum degree below 125, up to exchanging `P,Q`, to degree pair
   `(72,108)` and to one of the two corner cases `(8,28)` and `(9,27)`.”
2. “GGHV Proposition 4.1 and Corollary 5.7 (the latter proved via
   Theorem 5.1) eliminate the `(9,27)` corner case.”

The Proposition 4.3 item can remain as written.
