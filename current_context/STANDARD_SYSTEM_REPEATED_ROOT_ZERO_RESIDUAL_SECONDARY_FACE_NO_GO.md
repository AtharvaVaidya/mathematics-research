# Zero-residual secondary faces after a repeated-root Rees chart

Date: 26 July 2026

## Outcome

There is a conditional but exact no-go theorem for the residual root at
zero after the first repeated-root chart.

Let
\[
1<a<b,\qquad \gcd(a,b)=1,\qquad 2\le e\le g,
\]
and suppose a strict first common face is
\[
s^eC\!\left(\frac{\tau^d}{s^h}\right),
\qquad
\gcd(d,h)=1,\qquad
\frac dh<\frac ge.
\tag{1}
\]
Let \(k=\deg C\ge1\), assume the residual zero root persists, and
write
\[
e=kh+f,\qquad f\ge1,
\qquad
G=hg-ed,\qquad
L=g-kd,\qquad S=a+b.
\tag{2}
\]
After
\[
\tau=t^h,\qquad s=t^dy,
\tag{3}
\]
the reversed first-face polynomial has the form
\[
W(y)=y^eC(y^{-h})=y^fU(y^h),\qquad U(0)\ne0.
\tag{4}
\]
Thus zero remains a residual root of multiplicity \(f\).

For an actual secondary face at this root:

1. at a strict secondary slope, the lowest \(Q\)-face is
   automatically the matched face;
2. a matched strict face cannot supply the Keller scalar;
3. a matched resonant face has identically zero bracket;
4. an isolated matched super-slope face cannot supply the scalar,
   because its necessary top coefficient violates the original
   reciprocal degree bound;
5. a direct bracket of a super-slope \(P\)-face with a radial
   \(Q\)-Kummer monomial also cannot supply the scalar.

Items 3--5 do **not** exclude a chain of unmatched faces whose
non-scalar terms cancel successively.  In particular, matchedness is
not automatic at a super slope.  That compensating-chain problem is
the remaining gap.

There is also an essential support convention.  The secondary step
\((D,H)\) below is the **occupied support step**: holes common to the
\(P\)- and \(Q\)-supports have already been divided out.  Using only
the primitive direction of the Newton ray does not justify the
integrality argument in the strict case.

## 1. The transformed operator

Put
\[
n=ag,\qquad m=bg,\qquad N=gS-2,
\]
and use the local homogenized Keller operator
\[
\mathscr K(P,Q)
=\tau(P_sQ_\tau-P_\tau Q_s)+nP Q_s-mQ P_s.
\tag{5}
\]
Factor
\[
P=t^{aed}p,\qquad Q=t^{bed}q
\]
after (3).  A direct chain-rule calculation gives
\[
\boxed{
\mathcal L(p,q)
=t(p_yq_t-p_tq_y)+aG\,p q_y-bG\,q p_y.
}
\tag{6}
\]
More precisely,
\[
\mathscr K(P,Q)
=\frac1h t^{Sed-d}\mathcal L(p,q).
\tag{7}
\]
Consequently the transformed right side has \(t\)-order
\[
\boxed{
N'=hN-Sed+d=SG+d-2h.
}
\tag{8}
\]

Normalize the unit in (4) by the equivariant formal coordinate
\[
z=y\,U(y^h)^{1/f}.
\tag{9}
\]
Then \(W=z^f\).  The coordinate derivative is a unit, so (6) is
multiplied by a unit and the initial right side is still a nonzero
scalar times \(t^{N'}\).  The higher \(z\)-terms of that unit have
strictly higher secondary weight.

## 2. A matched secondary face

Let
\[
\xi=\frac{t^D}{z^H},\qquad D,H>0,
\tag{10}
\]
and consider the matched faces
\[
p_0=z^{af}A(\xi),\qquad
q_0=z^{bf}B(\xi),\qquad A(0)B(0)\ne0.
\tag{11}
\]
The exact face bracket is
\[
\boxed{
\mathcal L(p_0,q_0)
=\left(D-\frac GfH\right)
 z^{fS-1}\xi
\left(af\,AB'-bf\,A'B\right).
}
\tag{12}
\]

Suppose a nonzero term of (12) is the initial scalar
\(c\,t^{N'}\).  If its \(\xi\)-index is \(J\), comparison of
\(z\)- and \(t\)-exponents gives
\[
\boxed{
HJ=fS-1,\qquad DJ=N'.
}
\tag{13}
\]

Polynomiality in \(z\) gives
\[
\deg A\le\left\lfloor\frac{af}{H}\right\rfloor,
\qquad
\deg B\le\left\lfloor\frac{bf}{H}\right\rfloor.
\tag{14}
\]
Since the Wronskian in (12) has degree at most
\(\deg A+\deg B-1\), a scalar at index \(J\) requires
\[
J\le
\left\lfloor\frac{af}{H}\right\rfloor+
\left\lfloor\frac{bf}{H}\right\rfloor.
\tag{15}
\]
Combining (13) and (15) forces
\[
\boxed{
\begin{cases}
af\bmod H=bf\bmod H=0,&H=1,\\
\{af\bmod H,\;bf\bmod H\}=\{0,1\},&H>1.
\end{cases}
}
\tag{16}
\]
For \(H>1\), equality holds in (15), so both top coefficients of
\(A\) and \(B\) are nonzero.  Also (13) implies
\(\gcd(f,H)=1\).  Hence, when \(H>1\),
\[
\boxed{H\mid a\quad\hbox{or}\quad H\mid b.}
\tag{17}
\]
The top Wronskian coefficient does not accidentally cancel.  If
\(H\mid af\), it is
\[
af\frac{bf-1}{H}-bf\frac{af}{H}
=-\frac{af}{H}\ne0,
\tag{18}
\]
and the other case gives \(bf/H\ne0\).

The exceptional case \(H=1\) is different.  Then
\[
J=af+bf-1=\deg A+\deg B-1.
\]
The coefficient of the formally one-degree-higher Wronskian term
cancels because
\[
af(bf)-bf(af)=0.
\]
Every product contributing to the scalar coefficient one degree
below it has indices
\[
(af,bf-1)\quad\hbox{or}\quad(af-1,bf).
\tag{18a}
\]
Thus every such contribution uses at least one top coefficient.

## 3. Equivariance and the second exponent identity

The deck action of (3) is
\[
(t,y)\longmapsto(\omega t,\omega^{-d}y),
\qquad \omega^h=1.
\tag{19}
\]
The coordinate (9) is equivariant:
\(z(\omega^{-d}y)=\omega^{-d}z(y)\).
An occupied face term of index \(i\) therefore requires
\[
h\mid i(D+dH).
\tag{20}
\]

Let \(I\) be the union of the positive indices occupied by \(A\) and
\(B\).  By definition of the occupied support step, \(\gcd I=1\).
Bezout applied to (20) gives
\[
\boxed{
q_*:=\frac{D+dH}{h}\in\mathbf Z_{>0}.
}
\tag{21}
\]
If a primitive ray direction is retained while every occupied index
has a common factor, (21) does not follow.  One must first absorb that
factor into \((D,H)\).

Using \(G+df=hL\), equations (13) now give the second identity
\[
\boxed{
q_*J=SL-2.
}
\tag{22}
\]
Two useful consequences are
\[
\boxed{
\begin{aligned}
(2H-q_*)J&=S(2f-L),\\
J(fD-GH)&=h(L-2f).
\end{aligned}
}
\tag{23}
\]
The sign of the secondary slope defect \(fD-GH\) is therefore exactly
the sign of \(L-2f\).

## 4. Strict, resonant, and super slopes

### Strict slope

Assume \(fD<GH\), equivalently \(L<2f\).  From
\(HJ=fS-1\) one has \(\gcd(S,J)=1\).  The first identity in (23)
therefore gives an integer
\[
r=\frac{2f-L}{J}>0
\]
and
\[
\boxed{q_*=2H-Sr.}
\tag{24}
\]
Since \(q_*>0\),
\[
Sr<2H.
\tag{25}
\]

If \(H=1\), then \(Sr\ge S\ge5>2\), an immediate
contradiction.  Hence \(H>1\), and (17) applies.

If \(H\mid a\), then \(H\le a\), whereas
\(S=a+b>2a\), contradicting (25).  Thus \(H\mid b\).
Because a proper divisor of \(b\) is at most \(b/2<S/2\), (25)
forces
\[
H=b,\qquad r=1.
\tag{26}
\]
Now
\[
J=\frac{fS-1}{b}
=f+\frac{af-1}{b}\ge f+1,
\]
so
\[
L=2f-J<f.
\tag{27}
\]
The first strict face gives
\[
G=hL-fd>0,
\]
hence \(d<h\).  Finally
\[
g-e=(kd+L)-(kh+f)
=L-f-k(h-d)<0,
\tag{28}
\]
contrary to \(e\le g\).  Thus a scalar-producing strict matched face
does not exist.

At a strict secondary slope, matchedness of the actual lowest
\(Q\)-face is automatic.  For this matching argument, first use the
primitive lattice direction of the ray and decompose a putative lower
face into its lattice cosets; only afterward replace the matched
support by the occupied step used in Section 3.  For a lower
\(Q\)-coset
\[
t^u z^vB(\xi)
\]
the constant term of its bracket with \(p_0\) is proportional to
\[
u+\frac Gf v-bG.
\tag{29}
\]
If (29) is nonzero, the lowest bracket has positive \(z\)-order and
cannot equal the scalar.  If it is zero, then \(u=(G/f)(bf-v)\), and
its secondary weight is
\[
Hu+Dv
=bfD+(bf-v)\left(\frac GfH-D\right)\ge bfD,
\tag{30}
\]
contradicting that it was lower.

### Resonant slope

If \(fD=GH\), then \(L=2f\) by (23).  The prefactor in (12) is zero,
so the entire matched bracket vanishes.  It cannot supply a nonzero
scalar.

### Super slope

Assume \(fD>GH\), equivalently \(L>2f\).  If \(H\mid a\), the
necessary top \(A\)-term has index
\[
\alpha=\frac{af}{H}
\]
and, in the original reciprocal polynomial, \(\tau\)-order
\[
akd+q_*\alpha.
\tag{31}
\]
Its local \(s\)-order is zero.  The reciprocal degree bound therefore
requires
\[
q_*\alpha\le a(g-kd)=aL,
\qquad\hbox{hence}\qquad
q_*f\le HL.
\tag{32}
\]
But (23) and \(fD>GH\) give \(q_*f>HL\), a contradiction.  If
\(H\mid b\), the same argument applies to the top \(B\)-term.

For \(H=1\), super slope gives \(q_*f>L\).  The reciprocal bound
therefore excludes both top indices \(af\) and \(bf\).  By (18a),
every possible scalar Wronskian coefficient uses one of those two
top terms, so it vanishes as well.

This proves the super no-go only for an isolated matched face.
Unlike (30), the inequality reverses at a super slope, so lower
zero-radial-defect \(Q\)-cosets can exist and matchedness is not
automatic.

## 5. A direct super-face/Kummer cross term

The simplest unmatched possibility can also be excluded.  Put
\[
c=\gcd(f,G),\qquad f=cf_0,\qquad G=cG_0.
\tag{33}
\]
A radial \(Q\)-Kummer monomial is
\[
q_r=t^{G_0r}z^{bf-f_0r},
\qquad 0\le r\le bc.
\tag{34}
\]
Let
\[
p_{\rm sup}=z^{af}A(\xi),\qquad
\delta=fD-GH>0.
\tag{35}
\]
Direct substitution in (6) gives
\[
\boxed{
\mathcal L(p_{\rm sup},q_r)
=t^{G_0r}z^{af+bf-f_0r-1}
\delta\left(\frac rc-b\right)\xi A'(\xi).
}
\tag{36}
\]

For an \(A_j\xi^j\) term to be scalar in \(z\),
\[
Hj=af+v-1,\qquad v=bf-f_0r.
\tag{37}
\]
Polynomiality gives \(Hj\le af\), so \(v\le1\).
If \(v=0\), then \(r=bc\) and the coefficient in (36) is zero.
Thus \(v=1\).  This forces
\[
f_0=1,\qquad r=bf-1,\qquad Hj=af.
\tag{38}
\]
In particular \(f\mid G\); write
\[
\lambda=\frac Gf.
\]
Equivariance of (34), together with
\(\gcd(bf-1,f)=1\), forces
\[
\lambda+d=q_0h,\qquad q_0=\frac Lf\in\mathbf Z.
\tag{39}
\]

Set \(q=(D+dH)/h\); only \(qj\), not necessarily \(q\), is required
to be integral here.  Equality of the scalar \(t\)-order with (8)
reduces exactly to
\[
\boxed{
j(q-Hq_0)=q_0-2.
}
\tag{40}
\]
The super inequality is \(q>Hq_0\), so (40) would imply
\(q_0\ge3\).  But the original reciprocal degree bound on the top
\(P\)-term is
\[
qj\le aL.
\tag{41}
\]
Since \(j=af/H\) and \(L=fq_0\), (41) gives
\[
q\le Hq_0,
\]
contrary to the super inequality.

This rules out a **direct** scalar term from one super \(P\)-face
against one radial \(Q\)-Kummer monomial.  It does not rule out
additional unmatched \(Q\)-faces that cancel lower bracket terms and
move the terminal to another pair of supports.

## 6. The arbitrary-anchor operator for the open chain

For
\[
p=t^r z^uA(\xi),\qquad
q=t^s z^vB(\xi),\qquad
\xi=t^D/z^H,
\]
the exact bracket is
\[
\boxed{
\begin{aligned}
\mathcal L(p,q)
=t^{r+s}z^{u+v-1}\bigl(
&C_0AB+C_B\xi AB'+C_A\xi A'B
\bigr),
\\
C_0&=u(s-bG)-v(r-aG),\\
C_B&=uD+H(r-aG),\\
C_A&=H(bG-s)-Dv.
\end{aligned}
}
\tag{42}
\]
The mixed \(\xi^2A'B'\) terms cancel identically.  Formula (42), not
the matched Wronskian alone, is the appropriate starting point for
the remaining compensating-chain problem.

## 7. An unconditional terminal endpoint lemma

Although (42) does not exclude a compensating chain, it determines
where any terminal scalar contribution must land.

For arbitrary anchored occupied faces, a scalar term at
\(\xi\)-index \(J\) satisfies
\[
HJ=u+v-1.
\tag{43}
\]
The same degree calculation as in Section 2 shows:

- if \(H>1\), the two contributing monomials have residual
  \(z\)-orders \(0\) and \(1\);
- if \(H=1\), the top-top coefficient has residual orders
  \((0,0)\) but its bracket is zero, and every term one degree below
  it again has residual orders \((0,1)\) or \((1,0)\).

Thus every **nonzero** scalar contribution is the bracket of two
transformed monomials whose local orders are
\[
\{\epsilon_P,\epsilon_Q\}=\{0,1\}.
\tag{44}
\]

Pull those monomials back to the original reciprocal pair and let
their \(\tau\)-indices be \(I\) and \(J_0\).  Equality with the scalar
forcing gives
\[
I+J_0=n+m-2.
\tag{45}
\]
The reciprocal degree bounds give
\[
I+\epsilon_P\le n,\qquad
J_0+\epsilon_Q\le m.
\tag{46}
\]
If \((\epsilon_P,\epsilon_Q)=(0,1)\), the only possibilities are
\[
(I,J_0)=(n,m-2),\quad(n-1,m-1).
\]
If \((\epsilon_P,\epsilon_Q)=(1,0)\), they are
\[
(I,J_0)=(n-2,m),\quad(n-1,m-1).
\]

The bracket coefficient of
\(\tau^Is^{\epsilon_P}\) and
\(\tau^{J_0}s^{\epsilon_Q}\) is
\[
\epsilon_P(J_0-m)+\epsilon_Q(n-I).
\tag{47}
\]
It vanishes at \((n,m-2)\) and \((n-2,m)\).  Therefore
\[
\boxed{
\text{every nonzero terminal scalar contribution has }
I=n-1,\quad J_0=m-1.
}
\tag{48}
\]
So even an unmatched compensating chain must terminate in the
ordinary affine defect-one coefficient pair.  This is a terminal
classification, not a proof that no such chain reaches that pair.

## Scope

The result is local to the zero residual root in (4).  Nonzero roots
of \(U(y^h)\) have unrelated multiplicities and do not obey
\(e=kh+f\) with that local multiplicity.  The result neither proves
the full repeated-root exclusion nor rules out secondary chains with
unmatched anchors.  It does show that the only possible nonzero
terminal of such a chain is the affine defect-one pair (48).

The identities and a bounded arithmetic audit are checked by
`verify_standard_system_repeated_root_zero_residual_secondary_face_no_go.py`.
