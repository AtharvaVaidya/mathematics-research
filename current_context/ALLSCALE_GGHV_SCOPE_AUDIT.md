# Scope of the all-scale consecutive \((2,3)\) obstruction

Date: 25 July 2026

## Audited conclusion

The all-scale theorem in
`ALLSCALE_MARKED_CUSP_OBSTRUCTION.md` has the following exact consequence
for the public Guccione--Guccione--Horruitiner--Valqui (GGHV) preprint
reduction:

> Both alternatives called **a** and **b** in the proof of GGHV
> Proposition 4.3 are impossible.

Those two alternatives have the same final Newton polygons, and those
polygons become exactly the scale-\(R=4\) consecutive \((2,3)\)
five-block system under a unimodular torus change.  There is no missing
coefficient, vertex, pole, or primitivity hypothesis in this import.

The logically sharp bounded corollary is

\[
\boxed{
\begin{gathered}
(P,Q)\text{ a plane Keller counterexample},\\
\max(\deg P,\deg Q)<125
\end{gathered}
\quad\Longrightarrow\quad
\text{the remaining GGHV normalization is case c}.
}
\tag{S}
\]

Statement (S) is not a proof of \(JC(2)\), and by itself it is not even
the lower bound \(125\): case c must be eliminated independently for
that bounded conclusion.

The phrase **all scale** also has a precise limit.  It means that every
genuine member of the displayed five-block family is excluded for every
radial parameter \(R\).  It does **not** mean that a published reduction
puts every arbitrary-degree plane Keller counterexample into that
family.  No such global exhaustion theorem is known in the sources
audited here.

## 1. Exact import of GGHV Proposition 4.3(2)

The primary source is:

- J. A. Guccione, J. J. Guccione, R. Horruitiner, and C. Valqui,
  *Increasing the degree of a possible counterexample to the Jacobian
  Conjecture from 100 to 108*, arXiv:2204.14178,
  <https://arxiv.org/abs/2204.14178>.

GGHV Proposition 4.3, printed pages 10--12, starts from the remaining
corner \((8,28)\) and produces \(P,Q\in L^{(1)}\) satisfying
\[
[P,Q]_{x,y}=x^2.
\tag{1}
\]
Its alternative (2), obtained from both cases a and b in the proof, has
\[
\begin{aligned}
\Delta_P&=\operatorname{conv}
\{(0,0),(1,0),(8,14),(8,16)\},\\
\Delta_Q&=\operatorname{conv}
\{(0,0),(2,1),(12,21),(12,24)\}.
\end{aligned}
\tag{2}
\]
Equality with these Newton polygons means in particular that every
listed vertex has nonzero coefficient.

Put
\[
z=xy,\qquad h=xy^2.
\tag{3}
\]
Then
\[
x=\frac{z^2}{h},\qquad y=\frac hz,\qquad
x^a y^b=z^{\,2a-b}h^{\,b-a}.
\tag{4}
\]
The exponent map in (4) is unimodular.  It sends all lattice points of
the two polygons in (2) to the following complete block inventories:
\[
\begin{array}{c|c}
P\text{ block}&h\text{-degrees}\\ \hline
z^0&0,\ldots,8\\
z^1&0,\ldots,7\\
z^2&-1,\ldots,6
\end{array}
\qquad
\begin{array}{c|c}
Q\text{ block}&h\text{-degrees}\\ \hline
z^0&0,\ldots,12\\
z^1&0,\ldots,11\\
z^2&0,\ldots,10\\
z^3&-1,\ldots,9.
\end{array}
\tag{5}
\]
Thus
\[
\begin{aligned}
P&=A(h)+zp_1(h)+z^2\frac{U(h)}h,\\
Q&=B(h)+zq_1(h)+z^2q_2(h)+z^3\frac{V(h)}h,
\end{aligned}
\tag{6}
\]
with
\[
\deg A=8,\quad\deg B=12,\quad
\deg U=7,\quad\deg V=10.
\tag{7}
\]
The four outer degrees in (7) are exact because the vertices
\((8,16),(12,24),(8,14),(12,21)\) are present.

The coordinate Jacobian is
\[
\det\frac{\partial(z,h)}{\partial(x,y)}=h.
\tag{8}
\]
Since \(x^2=z^4/h^2\), equations (1) and (8) give
\[
\{P,Q\}_{z,h}=\frac{z^4}{h^3}.
\tag{9}
\]
Let \(\alpha\) and \(\beta\) be the coefficients of \(z^2/h\) and
\(z^3/h\).  The \(z^4/h^3\) coefficient in (9) is \(\alpha\beta\), so
\(\alpha\beta=1\).  Replacing
\[
(P,Q)\longmapsto(\alpha^{-1}P,\alpha Q)
\tag{10}
\]
preserves the bracket and normalizes both fixed-pole coefficients to
one.  Consequently
\[
U(0)=V(0)=1.
\tag{11}
\]
Finally, the \(z^4\) row of (9) is exactly
\[
UV+2hUV'-3hU'V=1.
\tag{12}
\]
Equations (6)--(12) are every support, vertex, pole, and outer-equation
hypothesis of the all-scale theorem with \(R=4\).  Sections 1--5 of
`ALLSCALE_MARKED_CUSP_OBSTRUCTION.md` then exclude the completion,
including nonprimitive boundary parametrizations.  Because GGHV cases a
and b already coincide in (2), both are covered; they are not two
additional subcases requiring separate proofs.

The exact lattice and coordinate audit is executable:

```bash
.venv/bin/python current_context/verify_gghv_allscale_scope.py
```

## 2. What “all scale” proves

For every integer \(R\ge1\), the analogous polygon pair
\[
\begin{aligned}
\Delta_{P,R}
&=\operatorname{conv}
\{(0,0),(1,0),(2R,4R-2),(2R,4R)\},\\
\Delta_{Q,R}
&=\operatorname{conv}
\{(0,0),(2,1),(3R,6R-3),(3R,6R)\}
\end{aligned}
\tag{13}
\]
transforms under (4) into
\[
\begin{array}{c|ccc}
P&z^0:0\ldots2R&z^1:0\ldots2R-1&z^2:-1\ldots2R-2,\\
Q&z^0:0\ldots3R&z^1:0\ldots3R-1&
z^2:0\ldots3R-2&z^3:-1\ldots3R-3.
\end{array}
\tag{14}
\]
Any genuine bracket solution with (13), the required vertices, and the
fixed poles is therefore excluded by the theorem.  This is a real
uniform result: no bound on \(R\) is used.

It is nevertheless a conditional family theorem.  In the primary GGHV
paper, the labels a and b and the exhaustive Proposition 4.3 dichotomy
occur for the specific corner \((8,28)\), hence \(R=4\).  Neither
Proposition 4.3 nor another cited theorem states that every
arbitrary-degree minimal counterexample has polygons (13).  Calling
(13) “a/b-type” at other scales is a useful extrapolated name, not a
published global reduction.

## 3. Why case c is outside the theorem

GGHV Proposition 4.3(1), corresponding to case c in its proof, adds
\[
(0,8)\in\Delta_P,\qquad(0,12)\in\Delta_Q
\tag{15}
\]
to (2).  Under (4), these become
\[
(0,8)\longmapsto(-8,8),\qquad
(0,12)\longmapsto(-12,12).
\tag{16}
\]
The full transformed pair therefore has eleven \(P\)-blocks
\[
z^{-8},z^{-7},\ldots,z^2
\]
and sixteen \(Q\)-blocks
\[
z^{-12},z^{-11},\ldots,z^3.
\]
It is not a five-block completion.

The five nonnegative blocks occurring in (6) remain visible inside case
c, but one cannot delete the negative blocks.  Their brackets with the
positive blocks contribute to the low transverse rows.  Emptiness of
the smaller support is not monotone under enlarging a bilinear
coefficient system.  In particular, the graph identities and the
completed-square root-consumption lemma used in Sections 2 and 5 of the
all-scale proof rely on the complete transverse degree-\((2,3)\) pair
and do not apply to this Laurent pair.

Thus case c survives **this theorem**.  Any separate computational or
structural case-c elimination must be audited on its own and cannot be
silently imported into the scope of the five-block result.

## 4. The exact bounded logical chain

GGHV Theorem 2.1, printed page 2, proves
\[
\text{counterexample}\quad\Longrightarrow\quad
\max(\deg P,\deg Q)\ge125
\quad\text{or}\quad
\{\deg P,\deg Q\}=\{72,108\}.
\tag{17}
\]
The paper's Section 2 table and Sections 3, 5, and 6 eliminate the other
listed configurations below \(125\).  For the remaining
\((72,108)\) configuration, Proposition 4.3 gives the exhaustive
necessary alternatives
\[
\text{case c}\quad\text{or}\quad\text{a/b}.
\tag{18}
\]
The all-scale theorem contradicts a/b.  Combining only the public GGHV
preprint
with the new theorem gives exactly
\[
\text{counterexample with maximum degree below }125
\quad\Longrightarrow\quad\text{case c},
\tag{19}
\]
which is statement (S).

If an independently rigorous argument eliminates case c, then (17)--(19)
give the bounded theorem
\[
\max(\deg P,\deg Q)\ge125.
\tag{20}
\]
Even (20) is only a lower bound and is not \(JC(2)\).

As of the date of this audit, a MathOverflow answer announces a
computer-assisted elimination of both Proposition 4.3 supports and says
that a write-up is in preparation:
<https://mathoverflow.net/questions/513413/the-simplest-case-of-jacobian-conjecture/513458>.
That announcement is consistent with (20), but it does not presently
supply a public proof that can be imported into this scope audit.  In
particular, it does not affect the conclusion that the all-scale theorem
*by itself* leaves case c open.

## 5. Surviving configurations beyond the bounded frontier

The relevant earlier primary source is:

- J. A. Guccione, J. J. Guccione, R. Horruitiner, and C. Valqui,
  *Some algorithms related to the Jacobian Conjecture*,
  arXiv:1708.07936,
  <https://arxiv.org/abs/1708.07936>.

Its Introduction and Section 2 explain the actual minimal-pair
quantifiers.  If \(JC(2)\) is false, one may choose a standard minimal
\((m,n)\)-pair with \(m,n>1\) coprime, rectangular outer support, and
\[
\deg P=m(a+b),\qquad \deg Q=n(a+b).
\tag{21}
\]
The admissible-chain algorithm supplies necessary corner restrictions.
It is an algorithm up to a chosen bound, not a theorem that forces one
fixed pair \((m,n)\) or one fixed chain.

Section 3 explicitly constructs infinite families of possible
\((m,n)\)'s.  Sections 5--6 list the possibilities through the stated
bounds.  Already between \(125\) and \(150\), its tables retain, among
others,
\[
(m,n)=(3,5),(3,4),(2,5),(2,7),(3,7),
\tag{22}
\]
as well as additional \((2,3)\) and \((3,2)\) configurations with
different corner chains.  Concrete entries include:

- family \(F_2\), \((3,5)\), maximum degree \(125\);
- family \(F_{24}\), \((3,4)\), maximum degree \(128\);
- family \(F_{11}\), \((2,5)\), maximum degree \(140\);
- families \(F_7,F_8\), \((2,7),(3,7)\), maximum degree \(147\);
- a \((2,3)\) entry with \(A_0=(7,35)\), maximum degree \(126\);
- \((2,3)\) and \((3,2)\) entries with \(A_0=(9,36)\), maximum
  degree \(135\).

These entries are necessary combinatorial possibilities, not actual
counterexamples.  Their importance for scope is that the known
minimal-counterexample theory has not reduced them to (13).  Some even
retain the transverse ratio \((2,3)\) but have a different Newton-corner
chain, so the words “transverse degree \((2,3)\)” alone are not enough
to invoke the theorem.

The broader shape theorem,

- J. A. Guccione, J. J. Guccione, and C. Valqui,
  *On the shape of possible counterexamples to the Jacobian
  Conjecture*, arXiv:1401.1784,
  <https://arxiv.org/abs/1401.1784>,

proves strong restrictions such as
\(\gcd(\deg P,\deg Q)\ge16\), but its abstract and main reduction do not
claim an upper bound on the degrees or exhaustion by the consecutive
five-block family.

Therefore no existing theorem in this audited chain reduces **all**
plane Keller counterexamples to “a/b or c,” and still less to a/b alone.
The a/b--c dichotomy is exhaustive only at the GGHV \((72,108)\)
frontier.

## 6. The missing bridge to a full proof

There are two very different missing bridges.

### Bounded bridge

For degrees below \(125\), it is enough to eliminate the full case-c
coefficient system of Proposition 4.3(1), with all required vertices.
That would prove (20), not \(JC(2)\).

### Global bridge

To turn the all-scale theorem itself into a proof of \(JC(2)\), one
would need a new uniform exhaustion or descent theorem of the form
\[
\boxed{
\text{any standard minimal Keller counterexample}
\Longrightarrow
\text{a genuine consecutive \((2,3)\) five-block completion}.
}
\tag{23}
\]
Compared with the present literature, (23) must simultaneously prove:

1. **ratio selection:** exclude all coprime terminal ratios other than
   \((2,3)\), up to swapping coordinates;
2. **corner-chain selection:** exclude the other admissible complete
   chains, including the other \((2,3)\) chains;
3. **case-c exclusion:** prevent the extra negative transverse blocks;
4. **global descent:** ensure that the Laurent edge-cutting operations
   lead to an actual five-block solution to which the theorem applies,
   without losing the polynomial Keller problem.

The fourth point is not bookkeeping.  GGHV Proposition 4.3 uses Laurent
automorphisms and finally the involution
\[
x\mapsto x^{-1},\qquad y\mapsto x^4y.
\]
These are valid for deriving necessary normalized equations, but they
are not polynomial automorphisms of \(\mathbb A^2\).  Consequently a
general “repeat the Newton reduction until a five-block appears”
argument needs a genuine polynomiality or minimality theorem at every
step.

A potentially efficient target is therefore a **degree-lowering
minimality lemma**:

> If a standard minimal pair has a terminal corner not of the genuine
> five-block type, then its edge-cutting data construct another
> polynomial Keller pair with strictly smaller
> \(\gcd(\deg P,\deg Q)\).

Such a lemma would use minimality to discard whole infinite families
instead of Gröbner-eliminating them scale by scale.  No audited source
currently proves it; the obstruction is precisely that known
edge-cutting transformations naturally live in Laurent rings.  Until
that polynomial descent gap is closed, the all-scale theorem is a
substantial family obstruction but cannot be promoted to a proof of
\(JC(2)\).

## Scope verdict

\[
\boxed{
\begin{array}{ll}
\text{GGHV a and b at }(72,108):&\textbf{excluded},\\
\text{the same genuine five-block family for every }R:&\textbf{excluded},\\
\text{GGHV case c}:&\textbf{not covered},\\
\text{other corner chains or transverse ratios}:&\textbf{not covered},\\
\text{all plane Keller counterexamples}:&\textbf{not reduced to this class}.
\end{array}}
\]
