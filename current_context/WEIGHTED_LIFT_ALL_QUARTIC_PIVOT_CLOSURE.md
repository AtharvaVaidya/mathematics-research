# Closure of every quartic second target pivot

Date: 25 July 2026

> **Correction (25 July 2026).**  Section 2.2 uses an invalid
> boundary-Euler separation.  The corrected exact first-lower
> calculation re-closes the pure \(B^4\) and pure linear \(B\) rays,
> but not the \(AB^2C\) and \(A^2C^2\) rays with arbitrary cubic
> lower target terms.  In those two families, normalized \(B^3\) and
> \(ABC\) coefficients respectively can cancel the first-lower double
> pole, and the remaining normalized \(x^{-1}\)-equation admits a
> polynomial coefficient solution.  Therefore the all-quartic
> conclusion, as stated for arbitrary \(Q_{\le3}\), is not currently
> proved.  All descending, negative-tail, nonresonance, interleaving,
> and constant-graph certificates remain valid.  See
> `WEIGHTED_LIFT_ALL_QUARTIC_PURE_FACE_CORRECTION_AUDIT.md`.

## Outcome

Let \(F=(A,B,C)\) be the generic-degree-six Gallagher weighted lift,
and let \(U(A,B,C)\) be the second-subduction polynomial from
`WEIGHTED_LIFT_FIRST_NONLINEAR_CUSP_SUBDUCTION.md`.  Let
\[
V=Q_4(A,B,C)+Q_{\le3}(A,B,C),
\qquad Q_4\ne0,
\tag{1}
\]
where \(Q_4\) is homogeneous quartic and \(Q_{\le3}\) is arbitrary of
target degree at most three.  Let \(R_{\le3}\) be another arbitrary
target polynomial of degree at most three.  Then no polynomial graph
\[
z=g(x,y)
\tag{2}
\]
makes
\[
\left((U+R_{\le3})\circ F,\ V\circ F\right)\big|_{z=g}
\tag{3}
\]
have nonzero constant Jacobian.

The result closes the whole quartic second-coordinate tier.  It is
not a theorem for arbitrary target degree.  The proof has four
structural parts:

- one characteristic equation treats every quartic Newton face;
- the binary and \(C\)-divisible faces reduce to nine integral rays;
- two finite-coefficient recurrences close the mixed quadratic face
  and the unusually close \(A/B\)-versus-\(C^4\) interleaving;
- an exact restricted-degree staircase prevents all remaining target
  and first-coordinate terms from arriving in time.

An independent exact lower-seed recurrence now also closes the
previously exceptional sextic family
\[
B^5(\lambda A+\mu B),\qquad\lambda\mu\ne0.
\tag{4}
\]
Higher binary target
degrees, beginning at degree seven, remain outside the theorem proved
in this note.
Nothing here claims a plane Keller map or resolves the Jacobian
conjecture.

## 1. The characteristic equation

Put
\[
u=1+xy,\qquad t=\frac ux=y+\frac1x,\qquad
\gamma=1+a\,xy+x^2g(x,y),\qquad a=-\frac{57}{34}.
\tag{5}
\]
Up to a nonzero scalar, the highest sector of \(U\) is
\[
M=x^{-5}u^{20}\gamma^{17}
=x^{15}t^{20}\gamma^{17}.
\tag{6}
\]
The highest seed sectors of the target coordinates are
\[
A_{\rm h}=q_6x^4t^6\gamma^4,\qquad
B_{\rm h}=p_5x^4t^5\gamma^4,\qquad
C_{\rm h}=x\gamma,
\tag{7}
\]
where
\[
p_5=-\frac3{46},\qquad q_6=-\frac5{92}.
\tag{8}
\]

Consider a homogeneous target face with \(n\) factors from
\(\{A,B\}\), \(c\) factors \(C\), and \(n+c=4\).  Its combined
highest sector has the form
\[
N=x^{4n+c}t^{5n}\gamma^{4n+c}P(t),
\qquad \deg P\le n.
\tag{9}
\]
Exact logarithmic differentiation gives
\[
\begin{aligned}
x\left(
\frac{5n-20c}{t}+17\frac{P'}P
\right)\gamma_x
{}-(8n+2c)\gamma_t\\
{}+\left(
-\frac{5n+20c}{t}+15\frac{P'}P
\right)\gamma=0
\end{aligned}
\tag{10}
\]
as the necessary and sufficient equation for \(J(M,N)=0\).

The coefficients depend only on \(t\), so each \(x\)-Laurent sector
is preserved.  Substituting
\[
\gamma=x^I\phi(t)
\tag{11}
\]
gives the unique formal solution
\[
\boxed{
\phi(t)=t^rP(t)^s,
}
\qquad
r=\frac{(5n-20c)I-(5n+20c)}{8n+2c},
\qquad
s=\frac{17I+15}{8n+2c}.
\tag{12}
\]
If \(d=\deg P\) and \(t^J\) is the leading term at infinity, then
\[
\boxed{J=r+ds.}
\tag{13}
\]
For a graph monomial \(g_m=c_0x^iy^{m-i}\),
\[
I=i+2,\qquad J=m-i,\qquad m=I+J-2.
\tag{14}
\]
Thus only integral solutions of (13) with \(I\ge2,J\ge0\) can cancel
a highest Jacobian sector.

## 2. Two closure lemmas

### 2.1. Descending and negative-tail obstructions

Normalize the leading coefficient of \(P\).  Formula (12) starts as
\[
x^It^J(1+O(t^{-1})).
\tag{15}
\]
If \(J\ge I+1\), substitution of \(t=y+x^{-1}\) gives the nonzero
term
\[
c_0\binom{J}{I-1}x\,y^{J-I+1}.
\tag{16}
\]
It is forbidden by \(\gamma=1+a xy+x^2g\).  The separate case
\(J=I-1\) gives a nonzero bare \(x\)-term and is forbidden as well.
The case \(J=I\) gives an \(xy\)-term that can meet the fixed boundary
jet and therefore is not covered by this descending argument; it
must be treated by the boundary-jet or negative-tail mechanisms.
Lower \(t\)-powers reach
\(x\)-exponent one with smaller \(y\)-degree, so they cannot cancel
(16).  The filtration drop is \(2(I-1)\).

If (12) has a nonzero negative power of \(t\), it is also impossible:
every coefficient of each \(x\)-power in
\[
\gamma(x,t)=1-a+axt+x^2g(x,t-x^{-1})
\tag{17}
\]
is a polynomial in \(t\).  Different \(x\)-Laurent sectors cannot
cancel such a term because (10) preserves those sectors.  In the two
sparse cases where the location of the first negative coefficient
matters, Sections 4 and 6 prove it by exact recurrences.

### 2.2. Pure monomial boundary jets

Suppose \(P=t^d\) and the characteristic completion
\(x^{I-J}u^J\) is graph-divisible.  Transforming (10) from
\((x,t)\) to \((x,u)\) gives the Euler operator
\[
\begin{aligned}
\mathcal L_{n,c,d}={}&
(5n-20c+17d)x\partial_x\\
&+(17d-3n-22c)u\partial_u
+(15d-5n-20c).
\end{aligned}
\tag{18}
\]
All possible graph corrections on the boundary diagonal have the
form
\[
f(u)=1+a(u-1)+h(u),
\qquad h(u)\in(u-1)^2\mathbb C[u].
\tag{19}
\]
Their necessary diagonal equation is
\[
\left(
(17d-3n-22c)u\partial_u+
(15d-5n-20c)
\right)f=0.
\tag{20}
\]
The two displayed coefficients cannot vanish simultaneously for a
nontrivial nonnegative face.  Indeed,
\[
\begin{aligned}
17(15d-5n-20c)
{}-15(17d-3n-22c)
=-10(4n+c).
\end{aligned}
\tag{21}
\]
If both vanished, nonnegativity would force \(n=c=0\), and then
either equation would give \(d=0\).

If the derivative coefficient in (20) is zero, its constant
coefficient is therefore nonzero and (20) would force \(f=0\),
contrary to \(f(1)=1\).  Otherwise every nonzero polynomial solution
is
\[
f(u)=c_1u^N,
\qquad
N=-\frac{15d-5n-20c}{17d-3n-22c}.
\tag{22}
\]
But (19) fixes
\[
f(1)=1,\qquad f'(1)=a=-\frac{57}{34}.
\tag{23}
\]
Consequently \(c_1=1\) and \(N=a\), impossible for a polynomial
monomial.  This proves a uniform same-diagonal obstruction for every
pure face; it does not rely merely on finding one displayed
coefficient.

## 3. The binary quartic face

Write
\[
Q_{4,AB}=
\alpha_4A^4+\alpha_3A^3B+\alpha_2A^2B^2
+\alpha_1AB^3+\alpha_0B^4.
\tag{24}
\]
After absorbing the nonzero constants \(q_6,p_5\), the corresponding
polynomial \(P_4\) has degree
\[
d=\max\{j:\alpha_j\ne0\}.
\tag{25}
\]
Here \((n,c)=(4,0)\), and (13) gives the complete table
\[
\begin{array}{c|c|c|c}
d&J(I)&(I,J)&m\\ \hline
4&(11I+5)/4&(4k+1,\,11k+4)&15k+3,\ k\ge1\\
3&(71I+25)/32&(32k+1,\,71k+3)&103k+2,\ k\ge1\\
2&(27I+5)/16&(16k+1,\,27k+2)&43k+1,\ k\ge1\\
1&(37I-5)/32&(32k+1,\,37k+1)&69k,\ k\ge1\\
0&5(I-1)/8&(8k+9,\,5k+5)&13k+12,\ k\ge0.
\end{array}
\tag{26}
\]

The first four rows are descending.  They force (16) at respective
filtration drops
\[
8k,\qquad64k,\qquad32k,\qquad64k.
\tag{27}
\]
Each is strictly smaller than the first lower seed drop \(m+4\).
The \(d=0\) row is the pure \(B^4\) ray and is closed by the boundary
jet lemma of Section 2.2.  Its fixed defect appears at drop \(m\),
again before \(m+4\).

Thus every nonzero binary quartic face is excluded, uniformly in all
of its lower \(A/B\)-coefficients.

## 4. The \(C Q_3(A,B)\)-face

For \(C Q_3(A,B)\), one has \((n,c)=(3,1)\).  Formula (13) gives
\[
\begin{array}{c|c|c|c}
d&J(I)&(I,J)&m\\ \hline
3&(23I+5)/13&(13k+6,\,23k+11)&36k+15\\
2&(29I-5)/26&(26k+19,\,29k+21)&55k+38\\
1&(6I-10)/13&(13k+6,\,6k+2)&19k+6\\
0&-(5I+35)/26&\text{none}&\text{none}.
\end{array}
\tag{28}
\]
The \(d=3,2\) rows are descending and force (16) at drops
\[
26k+10,\qquad52k+36.
\tag{29}
\]
The next lower target tier enters at drops \(m+3\) and \(m+2\),
respectively, so it arrives strictly later.

For \(d=1\), normalize
\[
P(t)=t+\eta.
\tag{30}
\]
Equations (12) and (28) give
\[
\phi(t)=
t^{-5(k+1)/2}(t+\eta)^{(17k+9)/2}
=t^{6k+2}(1+\eta/t)^{(17k+9)/2}.
\tag{31}
\]
If \(\eta\ne0\), the coefficient of \(t^{-1}\) is
\[
\binom{(17k+9)/2}{6k+3}\eta^{6k+3}\ne0,
\tag{32}
\]
because
\[
\frac{17k+9}{2}-(6k+2)=\frac{5(k+1)}2>0.
\tag{33}
\]
It appears after \(6k+3\) steps, before the lower target gap
\(m+1=19k+7\).

If \(\eta=0\), the characteristic completion is the honest
graph-divisible polynomial
\[
x^{7k+4}u^{6k+2}.
\tag{34}
\]
It is a pure face and is closed by Section 2.2.  The \(d=0\) face is
nonresonant.  Hence every \(C Q_3(A,B)\) quartic face is closed.

## 5. The \(C^2Q_2(A,B)\)-face

For \(C^2Q_2(A,B)\), one has \((n,c)=(2,2)\).  The degrees
\(d=1,0\) give \(J<0\).  The only resonance is
\[
d=2,\qquad
I=5k+5,\quad J=k,\quad m=6k+3,\qquad k\ge0.
\tag{35}
\]
Normalize
\[
P(t)=t^2+bt+c.
\tag{36}
\]
Then
\[
\phi(t)=t^J F(t^{-1}),\qquad
F(z)=(1+bz+cz^2)^s,\qquad
s=\frac{17k+20}{4}.
\tag{37}
\]
Write \(F(z)=\sum_{q\ge0}a_qz^q\), so \(a_0=1\).  The exact
differential identity
\[
(1+bz+cz^2)F'=s(b+2cz)F
\tag{38}
\]
gives, for \(q\ge0\),
\[
(q+1)a_{q+1}
=b(s-q)a_q+c(2s-q+1)a_{q-1},
\qquad a_{-1}=0.
\tag{39}
\]

If \(c\ne0\) and both \(a_{J+1}\) and \(a_{J+2}\) vanished, (39) at
\(q=J+1\) would force \(a_J=0\).  Descending \(q\) would then force
\[
a_{J-1}=\cdots=a_0=0,
\tag{40}
\]
because every multiplier encountered is at least
\[
2s-J=\frac{15k}{2}+10>0.
\tag{41}
\]
This contradicts \(a_0=1\).  If \(c=0\) but \(b\ne0\), then
\[
a_{J+1}=\binom{s}{J+1}b^{J+1}\ne0,
\tag{42}
\]
since \(s-J=13k/4+5>0\).

Thus every nonpure quadratic \(P\) has a negative \(t\)-coefficient
within \(J+2=k+2\) descending steps.  The next lower target face is
\(C A^2\), at gap
\[
m+3=6k+6>k+2.
\tag{43}
\]
When \(b=c=0\), the completion is pure and Section 2.2 applies.
This closes the last resonant \(C^2Q_2\)-face.

## 6. The \(C^3(A,B)\), \(C^4\), and linear interleaving

For \(C^3(A,B)\), \((n,c)=(1,3)\), and both \(d=1,0\) give
\(J<0\).  For \(C^4\), \((n,c,d)=(0,4,0)\), and
\[
J=-10I-10<0.
\tag{44}
\]
Taken separately, neither face resonates.

There is one important interleaving.  Restricted linear \(A,B\)
terms lie only six and five levels above \(C^4\), so a \(C^4\) term
must be included before using a late linear-pivot defect.  Their
combined highest sector is
\[
N=x^4\gamma^4P(t),\qquad
P(t)=\alpha t^6+\beta t^5+\rho,
\tag{45}
\]
after absorbing \(q_6,p_5\).  Exact differentiation gives
\[
\begin{aligned}
x\left(-\frac{80}{t}+17\frac{P'}P\right)\gamma_x
-8\gamma_t
+\left(-\frac{80}{t}+15\frac{P'}P\right)\gamma=0.
\end{aligned}
\tag{46}
\]

If \(\alpha\ne0\), the resonance is the \(A\)-ray
\[
I=4k+1,\qquad J=11k+4,\qquad m=15k+3,\qquad k\ge1.
\tag{47}
\]
Since \(J-I=7k+3>0\), its leading \(t^J\) term already forces the
forbidden term (16).  For completeness, when \(\rho\ne0\) the whole
sparse completion also has a uniformly short negative tail.  Put
\[
F(z)=(1+bz+cz^6)^s,\qquad s=\frac{17k+8}{2}.
\tag{48}
\]
The identity
\[
(1+bz+cz^6)F'=s(b+6cz^5)F
\tag{49}
\]
gives
\[
(q+1)a_{q+1}
=b(s-q)a_q+c(6s-q+5)a_{q-5}.
\tag{50}
\]
If all six coefficients \(a_{J+1},\ldots,a_{J+6}\) vanished,
(50) at \(q=J+5\), then at descending values of \(q\), would force
all of \(a_J,\ldots,a_0\) to vanish.  This is impossible because
\[
6s-J=40k+20>0,\qquad a_0=1.
\tag{51}
\]
Hence a negative coefficient occurs by \(J+6\), and
\[
J+6<m+4
\tag{52}
\]
because the difference is \(4k-3>0\).

If \(\alpha=0,\beta\ne0,\rho\ne0\), the resonance is the \(B\)-ray
\[
I=8k+9,\qquad J=5k+5,\qquad m=13k+12,\qquad k\ge0.
\tag{53}
\]
Here
\[
F(z)=(1+cz^5)^{17k+21}.
\tag{54}
\]
Its first supported coefficient after \(J=5(k+1)\) is
\[
a_{J+5}=
\binom{17k+21}{k+2}c^{k+2}\ne0.
\tag{55}
\]
It arrives at \(J+5=5k+10<m+4=13k+16\).  If \(\rho=0\), this is the
pure \(B\)-ray; applying the same boundary-jet calculation directly
to (46) gives the operator
\[
5x\partial_x-3u\partial_u-5,
\tag{56}
\]
which closes it.  If
\(\alpha=\beta=0,\rho\ne0\), (44) shows that the pure \(C^4\) face
does not resonate.  These cases exhaust all specializations of
\((\alpha,\beta,\rho)\ne(0,0,0)\).

## 7. Exact composition with arbitrary lower target terms

For a nonconstant graph of degree \(m\), the target monomial degrees
form the following strict staircase:
\[
\begin{array}{c|c}
\text{target faces}&\text{restricted degrees}\\ \hline
A^4,A^3B,A^2B^2,AB^3,B^4&
16m+72,\ldots,16m+68\\
A^3C,A^2BC,AB^2C,B^3C&
13m+57,\ldots,13m+54\\
A^3,A^2B,AB^2,B^3&
12m+54,\ldots,12m+51\\
A^2C^2,ABC^2,B^2C^2&
10m+42,\ldots,10m+40\\
A^2C,ABC,B^2C&
9m+39,\ldots,9m+37\\
A^2,AB,B^2&
8m+36,\ldots,8m+34\\
AC^3,BC^3&
7m+27,\ 7m+26\\
AC^2,BC^2&
6m+24,\ 6m+23\\
AC,BC&
5m+21,\ 5m+20\\
A,B&
4m+18,\ 4m+17\\
C^4,C^3,C^2,C&
4m+12,\ 3m+9,\ 2m+6,\ m+3.
\end{array}
\tag{57}
\]
Every entry exceeds the following entry for \(m\ge1\).  The same
order holds for Jacobians with \(U\), since the common degree
\(\deg U_0-2=17m+67\) is added.

It remains to check that a later face cannot repair the first
obstruction.  The relevant closest gaps are:

- a binary quartic face lies above \(A^3C\) by at least \(3m+11\);
  this exceeds (27) and the pure defect;
- the \(A^3C,A^2BC,AB^2C\) faces lie above the lower binary cubic
  tier by \(m+3,m+2,m+1\), which exceed (29), (32), and the pure
  defect, respectively;
- an \(A^2C^2\) face lies above the lower \(A^2C\) tier by \(m+3\),
  which exceeds the \(k+2\) bound in Section 5;
- if a lower cubic or quadratic face is the first nonzero face, the
  prior cubic and quadratic closure defects occur before the next
  quartic face in (56); the new closest case is a binary cubic above
  \(A^2C^2\), whose gap is at least \(2m+9\);
- the only gap too short for a direct citation is \(A/B\) above
  \(C^4\), and Section 6 treated that combined face exactly.

All \(C^3(A,B)\) quartic faces are nonresonant.  Once the staircase
reaches a polynomial in \(C\) alone, either Section 6 applies or its
Jacobian is a nonzero polynomial multiple of \(J(U,C)\).  Therefore
no quartic or lower second-coordinate term repairs the first
nonzero obstruction.

Finally, adding \(R_{\le3}\) to the first coordinate cannot change
the conclusion.  Its largest restricted degree is
\[
12m+54,
\qquad
\deg U_0=17m+69.
\tag{58}
\]
Thus \(J(R_{\le3},V)\) enters at least
\[
5m+15
\tag{59}
\]
levels after the corresponding \(J(U,V)\) sector, later than every
obstruction above.

## 8. Constant graphs

Let \(g=z_0\), and put
\[
h=ay+z_0x.
\tag{60}
\]
The highest forms are
\[
U_0=\theta x^{32}y^{20}h^{17},\qquad
A_0\sim x^8y^6h^4,\qquad
B_0\sim x^8y^5h^4,\qquad
C_0=x^2h.
\tag{61}
\]
For
\[
R=x^Ay^Bh^C,\qquad S=x^Dy^Eh^F,
\]
direct logarithmic differentiation gives
\[
\frac{J(R,S)}{RS/(xyh)}
=(AE-BD)h+(CE-BF)z_0x+(AF-CD)ay.
\tag{62}
\]
For each of the fifteen quartic target monomials, substitution of
\((A,B,C)=(32,20,17)\) for \(U_0\) and
\[
(D,E,F)=
\bigl(8(a+b)+2c,\ 6a+5b,\ 4(a+b)+c\bigr)
\tag{63}
\]
for \(A^aB^bC^c\), \(a+b+c=4\), gives a nonzero coefficient pair.
Their Jacobian degrees are separated:
\[
\begin{gathered}
139,138,137,136,135,\\
124,123,122,121,\\
109,108,107,\qquad94,93,\qquad79.
\end{gathered}
\tag{64}
\]
For \(z_0\ne0\), every one of these fifteen forms is nonzero.  For
\(z_0=0\), the \(ay\)-coefficient remains nonzero for fourteen
monomials.  The sole exception is \(AB^3\): its degree-\(136\)
Jacobian vanishes because the leading forms of \(U\) and \(AB^3\)
are proportional.

That exceptional cancellation is not left to a numerical sample.
On \(z=0\), put \(v=xy\) and write the exact restricted polynomials
as
\[
U=x^{-5}H(v),\qquad AB^3=x^{-5}K(v).
\tag{65}
\]
Both \(H\) and \(K\) have degree \(37\).  The exact seed and
second-subduction numerator give
\[
\begin{aligned}
H_{37}&=\theta a^{17},&
\frac{H_{36}}{H_{37}}&=\frac{562}{57},\\
K_{37}&=q_6p_5^3a^{16},&
\frac{K_{36}}{K_{37}}&=\frac{653}{57}.
\end{aligned}
\tag{66}
\]
Direct differentiation gives
\[
J(U,AB^3)
=5x^{-10}(H'K-HK').
\tag{67}
\]
Its \(v^{72}\)-coefficient is therefore
\[
5(H_{37}K_{36}-H_{36}K_{37})
=\frac{455}{57}\theta q_6p_5^3a^{33}\ne0.
\tag{68}
\]
This is the nonzero degree-\(134\) term
\(x^{62}y^{72}\).  If \(AB^3\) is the first surviving quartic
monomial and \(B^4\) is also present, the nonzero degree-\(135\)
\(B^4\) top leads instead.  If \(B^4\) is absent, (68) is the
leading term.  Consequently every nonzero \(Q_4\) has either a
nonzero toric top or, in this one specialization, the certified next
diagonal term.  Lower target terms and \(R_{\le3}\) enter later.

## 9. Scope and verification

Combining Sections 3--8 proves
\[
\boxed{
J_{x,y}\left(
(U+R_{\le3})\circ F|_{z=g},\
(Q_4+Q_{\le3})\circ F|_{z=g}
\right)\notin\mathbb C^\times
}
\tag{69}
\]
for every polynomial graph \(g\), every nonzero homogeneous quartic
\(Q_4\), and arbitrary target polynomials \(R_{\le3},Q_{\le3}\) of
degree at most three.

The accompanying exact verifier is
`verify_weighted_lift_all_quartic_pivot_closure.py`.
