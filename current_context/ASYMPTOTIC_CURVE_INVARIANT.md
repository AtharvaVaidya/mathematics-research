# The five-block asymptotic curve: normalization, fifth inertia, and cusp rigidity

Date: 24 July 2026

## Verdict

There is a useful intrinsic theorem, but it is conditional in exactly the
right place.

For the a/b five-block map
\[
\begin{aligned}
P&=\frac{z^2}{w}+a_0(w)+za_1(w)+z^2a_2(w),\\
Q&=\frac{z^3}{w}+b_0(w)+zb_1(w)+z^2b_2(w)+z^3b_3(w),
\end{aligned}
\tag{1}
\]
with
\[
J_{z,w}(P,Q)=\frac{z^4}{w^3},
\tag{2}
\]
the boundary \(z=0\) maps to
\[
\Gamma=\overline{\{(a_0(w),b_0(w))\}}.
\]
If \(\deg a_0=8\) and \(\deg b_0=12\), then:

1. the degree \(\delta\) of the parametrization of \(\Gamma\) is one of
   \(1,2,4\);
2. at a generic smooth point of \(\Gamma\), the transverse local map has
   ramification index \(5\), so its local inertia contains \(\delta\)
   disjoint 5-cycles;
3. if \(\Gamma\) is contained in the fixed cusp
   \(q^2=Lp^3\), then the five-block pole bound at \(w=0\) and (2) force
   \[
   a_0=A w^8,\qquad b_0=B w^{12},\qquad B^2=LA^3.
   \tag{3}
   \]
4. that pure monomial boundary is itself impossible: the coefficient of
   \(z^4\) in \(Q^2-LP^3\) forces a polynomial square to have odd
   \(w\)-adic order seven.

Thus a hypothetical full-vertex a/b solution necessarily has an
asymptotic component different from the fixed cusp.  This conclusion uses
no \(k=3\) coefficient elimination.
What the five bracket equations do **not** do intrinsically is prove cusp
containment.  An exact five-block countermodel below has nonconstant
non-cuspidal \(\Gamma\).

## 1. Polynomial normalization and the three possible degrees

Put
\[
\delta=[\mathbf C(w):\mathbf C(a_0,b_0)].
\]
The polynomial version of Lüroth's theorem (equivalently, normalization of
the polynomially parametrized affine curve) gives a polynomial \(h(w)\)
and coprime polynomials \(A(T),B(T)\) such that
\[
\mathbf C(a_0,b_0)=\mathbf C(h),\qquad
a_0=A(h),\qquad b_0=B(h),\qquad \deg h=\delta.
\tag{4}
\]
Consequently \(\delta\) divides both 8 and 12.  Hence
\[
\boxed{\delta\in\{1,2,4\}},
\tag{5}
\]
and the normalized parametrization has degree pair
\[
\left(\frac8\delta,\frac{12}\delta\right)
=(2m,3m),\qquad m=\frac4\delta.
\tag{6}
\]

The map \(\mathbf A^1_w\to\widetilde\Gamma\simeq\mathbf A^1_h\) is totally
ramified at infinity, as every polynomial map is.  There is no theorem from
the five ODEs saying that it is also totally ramified at \(w=0\).  This is
the exact point at which a tempting two-point-cover shortcut would assume
too much.

The degree alternatives really occur at the level of polynomial
parametrizations.  For
\[
a_0=w^8,\qquad b_0=w^{12}+w^\delta,\qquad \delta=1,2,4,
\tag{7}
\]
the common-fiber gcd is \(v^\delta-w^\delta\), so the parametrization degree
is exactly \(\delta\).  These examples are not asserted to extend to full
five-block solutions with the required outer vertices; they show that
degrees \((8,12)\), one place at infinity, and leading cusp direction alone
do not select \(\delta=4\).

## 2. The local normal form forces fifth-order inertia

Work at a generic point of \(z=0\), so \(w\ne0\), and then over one of the
\(\delta\) branches above the generic point of \(\Gamma\).  Since the
parametrization is generically separable, choose a target parameter \(t\)
along \(\Gamma\) and a transverse equation \(n\) such that
\[
t(P,Q)|_{z=0}=w,\qquad n(P,Q)|_{z=0}=0.
\]
Write
\[
n(P,Q)=z^r u(w)+O(z^{r+1}),\qquad u\ne0.
\]
The target coordinate change has unit Jacobian at the generic point.
Equation (2) and
\[
J_{z,w}(t,n)=-r\,u(w)z^{r-1}+O(z^r)
\]
therefore give
\[
\boxed{r=5}.
\tag{8}
\]
After formal étale coordinate changes the map is
\[
(w,z)\longmapsto(w,z^5).
\tag{9}
\]
Thus a meridian around \(\Gamma\) contributes one 5-cycle for each generic
preimage of its normalization parameter:
\[
\boxed{\text{the boundary }z=0\text{ contributes cycle type }5^\delta.}
\tag{10}
\]
In particular the generic degree is at least \(5\delta\).

This is the genuine monodromy invariant supplied by the exponent four in
the Jacobian.  It is compatible with all three values in (5).  Even if a
separate argument fixed the global degree to 21, the case \(\delta=4\)
would merely give the allowable permutation type \((5^4,1)\); a passport
argument is still needed to show that this inertia cannot coexist with the
outer radial inertia.

## 3. Conditional cusp rigidity

Assume now
\[
b_0^2=La_0^3.
\tag{11}
\]
Unique factorization and the full degrees give
\[
a_0=\alpha h^2,\qquad b_0=\beta h^3,\qquad
\beta^2=L\alpha^3,\qquad \deg h=4.
\tag{12}
\]
On the open set \(PQ\ne0\), introduce
\[
t=\frac{\alpha Q}{\beta P},\qquad n=Q^2-LP^3.
\tag{13}
\]
Along \(z=0\), \(t=h\), and a direct calculation gives
\[
\det\frac{\partial(t,n)}{\partial(P,Q)}
\bigg|_{z=0}
=\frac{\beta}{\alpha}h^2.
\tag{14}
\]
Since (2) holds, if \(n=z^r n_r(w)+\cdots\), comparison of the first
nonzero \(z\)-coefficient yields
\[
r=5,\qquad
-5h'(w)n_5(w)=\frac{\beta}{\alpha}\frac{h(w)^2}{w^3}.
\tag{15}
\]

The five-block caps make this much stronger than the generic local normal
form.  Indeed, with
\[
p_2=a_2+\frac1w,\qquad q_3=b_3+\frac1w,
\]
one has exactly
\[
n_5=2b_2q_3-3L a_1p_2^2,
\tag{16}
\]
and hence
\[
\operatorname{ord}_{w=0}n_5\ge-2.
\tag{17}
\]
If \(h(0)\ne0\), the right side of
\[
n_5=-\frac{\beta}{5\alpha}\frac{h^2}{w^3h'}
\tag{18}
\]
has order at most \(-3\), contradicting (17).  Therefore \(h(0)=0\).

At every nonzero root \(\xi\) of \(h'\), equation (15) forces
\(h(\xi)=0\).  A characteristic-zero polynomial all of whose critical
points are among its roots has only one distinct root: if
\[
h=c\prod_{i=1}^s(w-\xi_i)^{m_i},
\]
then, after removing the factors
\((w-\xi_i)^{m_i-1}\) from \(h'\), the remaining factor has degree \(s-1\)
and is nonzero at every \(\xi_i\).  Hence \(s=1\).  Since the unique root
is zero and \(\deg h=4\),
\[
h=cw^4.
\tag{19}
\]
Substitution into (12) proves (3), and (15) additionally gives
\[
n_5=-\frac{\beta c}{20\alpha}w^2.
\tag{20}
\]

This is the exact a/b analogue of the case-c calculation
\(h'\mid h^2\).  The extra \(w^{-3}\) in (2) initially permits a Laurent
denominator, but the sharper pole bound (17) forces \(h(0)=0\), after
which the same one-root conclusion follows.

## 4. The pure cusp boundary is impossible

The conclusion of the preceding section admits a short contradiction
before the \(n_5\)-equation is reached.  Write
\[
\begin{aligned}
P&=p_0+p_1z+p_2z^2,\\
Q&=q_0+q_1z+q_2z^2+q_3z^3,
\end{aligned}
\]
where
\[
p_0=Aw^8,\qquad q_0=Bw^{12},\qquad
p_2=a_2+\frac1w,\qquad q_0^2=Lp_0^3.
\tag{21}
\]
Since \(n=Q^2-LP^3=z^5(n_5+zn_6)\), its coefficients
\(n_1,n_2,n_3,n_4\) vanish.  The first three solve successively:
\[
\begin{aligned}
q_1&=\frac{3q_0p_1}{2p_0},\\
q_2&=\frac{3q_0p_2}{2p_0}
     +\frac{3q_0p_1^2}{8p_0^2},\\
q_3&=\frac{3q_0p_1p_2}{4p_0^2}
     -\frac{q_0p_1^3}{16p_0^3}.
\end{aligned}
\tag{22}
\]
Substitution in the fourth coefficient gives the exact square
\[
n_4
=-\frac{3q_0^2}{64p_0^4}
\left(4p_0p_2-p_1^2\right)^2.
\tag{23}
\]
Thus \(n_4=0\) implies
\[
a_1^2
=4Aw^8\left(a_2+\frac1w\right)
=4Aw^7(1+wa_2).
\tag{24}
\]
The right side has exact \(w\)-adic order \(7\), because \(A\ne0\) and
\(a_2\in\mathbf C[w]\).  A nonzero polynomial square has even
\(w\)-adic order.  This is impossible.

Therefore:

> **Cusp-exclusion theorem for the full a/b boundary.**  A five-block
> solution with \([w^8]a_0,[w^{12}]b_0\ne0\) cannot satisfy
> \(b_0^2=La_0^3\).

Once cusp containment is assumed, only the two vertical full-degree
vertices and the fixed pole \(z^2/w\) are needed for the contradiction.
The required outer vertices
\([w^6]a_2,[w^9]b_3\ne0\) are not needed.  Their role can only be in a
separate global argument attempting to force cusp containment.

## 5. Exact five-block non-cusp countermodel

The bracket ODEs do not force (11) without the full outer-vertex
conditions.  Let \(\theta\) satisfy
\[
27\theta^2-9\theta+1=0,
\]
and put
\[
d=\frac{9\theta+1}{7},\qquad
e=\frac{3\theta d}{5}.
\]
Then
\[
\begin{aligned}
a_0&=\theta w^3,& a_1&=w,&a_2&=0,\\
b_0&=e w^5,&b_1&=d w^3,&b_2&=w,&b_3&=0
\end{aligned}
\tag{21}
\]
satisfies all five bracket ODEs, equivalently
\[
J_{z,w}(P,Q)=\frac{z^4}{w^3}.
\tag{22}
\]
But
\[
\frac{b_0^2}{a_0^3}
=\frac{e^2}{\theta^3}w
\]
is nonconstant.  Thus neither the order-four Jacobian nor the mere
five-block shape forces the asymptotic image into a fixed cusp.

This example has asymptotic degrees \((3,5)\) and has
\(a_2=b_3=0\), so it misses all four full-vertex requirements
\[
[w^8]a_0,\quad [w^{12}]b_0,\quad [w^6]a_2,\quad [w^9]b_3\ne0.
\]
That limitation is intentional: the complete full-vertex a/b system is
already known to be empty.  The example isolates the logical fact that a
proof of cusp containment must use the full vertex/degree geometry, not
only the local normal form or the five formal identities.

In the conditional cusp theorem, the full vertices enter at two distinct
points and nowhere else:

1. \([w^8]a_0,[w^{12}]b_0\ne0\) turn the UFD factorization (12) into
   \(\deg h=4\);
2. the five-block support caps, including the fixed pole terms
   \(z^2/w,z^3/w\), give the sharp bound
   \(\operatorname{ord}_0 n_5\ge-2\).

The nonzero outer vertices \([w^6]a_2,[w^9]b_3\ne0\) are not used after
cusp containment is assumed.  They remain precisely the plausible global
input for proving cusp containment in the first place.

## 6. Interaction with standard nonproper-set theorems

For fixed \(w\ne0\), the path
\[
x=\frac{z^2}{w}\longrightarrow0,\qquad
y=\frac wz\longrightarrow\infty
\]
shows that \(\Gamma\) is contained in the nonproper-value set of the
auxiliary map.  Since it is a nonconstant irreducible curve, it is an
irreducible component.

The standard theorems for an everywhere nonsingular Keller map do not
close the argument here, because (1) has Jacobian \(x^2\), not a nonzero
constant.  Even after a justified transfer to an original Keller map, the
known degree-ratio constraint on a dicritical component is exactly (6),
and the one-place-at-infinity condition is automatic for a polynomial
parametrization.  Thus these results are consistent with every
\(\delta\in\{1,2,4\}\).

## 7. Exact remaining gap and best continuation

There are now two focused, non-brute-force targets.

1. **Exploit mandatory non-cusp containment.**  Any hypothetical full
   a/b solution has an additional asymptotic curve
   \(\Gamma\not\subset C_L\).  A global theorem relating all asymptotic
   components, or their common point and links at infinity, can now use
   this as a mandatory incidence rather than an unresolved alternative.
2. **Inertia-budget separation.**  Without assuming cusp containment,
   combine the unavoidable \(5^\delta\) inertia of \(\Gamma\) with the
   fixed radial \((17,1^4)\) inertia and a rigorous global-degree formula.
   The current mixed-volume number 45 is only an upper/generic count, and
   the outer degree 21 is not yet known to be the degree of the completed
   map.  Until one of those degrees is fixed and the two peripheral loops
   are related, the fifth-order inertia is not forbidden.

The useful new invariant is therefore not the equation of \(\Gamma\), but
the pair
\[
\boxed{(\delta,\text{ transverse inertia})=(\delta,5^\delta),
\qquad \delta\in\{1,2,4\}.}
\]
Together with the cusp-exclusion theorem, it sharply narrows a geometric
attack to a mandatory extra nonproper component and its fifth-order
inertia.
