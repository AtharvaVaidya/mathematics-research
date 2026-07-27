# All-degree binary maximal-\(x\) and first-lower pole obstruction

Date: 25 July 2026

## Outcome

Let
\[
Q_n(A,B)=\sum_{j=0}^n c_jA^jB^{n-j}
\qquad (n\ge 1)
\tag{1}
\]
be a nonzero homogeneous binary target for the Gallagher weighted
lift, and let
\[
P(t)=\sum_{j=0}^n c_jq_6^jp_5^{n-j}t^j,
\qquad d=\deg P.
\tag{2}
\]
Suppose the graph is nonconstant.  In the Laurent chart
\(t=y+x^{-1}\), let \(I\ge2\) be the maximal \(x\)-power of
\(\gamma\).  The exact maximal-\(x\) equation forces its coefficient
to have the characteristic form
\[
G=cx^It^rP(t)^s,\qquad
r=\frac{5(I-1)}8,\qquad
s=\frac{17I+15}{8n}.
\tag{3}
\]
Every non-top seed term lies at normalized \(x\)-power at most
\(-1\), whereas (3) lies at \(x^I\).  Hence this is an exact
polynomial identity in \(t\), not merely the beginning of a
filtration recurrence.  Since the \(x^I\)-coefficient of a source
polynomial is polynomial in \(t\), a nonpolynomial characteristic
completion is impossible in every degree, regardless of when its
first negative \(t\)-coefficient would occur.

If \(P\) is mixed, then it has a nonzero root over the algebraic
closure.  At every such root the exact first-lower seed forcing has a
double pole.  The top characteristic operator applied to any
polynomial graph correction has at most a simple pole there.
Consequently the normalized \(x^{-1}\) recurrence cannot be solved.

Together with the exact pure numerator and forbidden-descent argument
in `WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_CLOSURE.md`, and the direct
constant-graph calculation in Section 6,
this closes every homogeneous binary target in every degree on every
polynomial graph.  The same \(x\)-layers are unchanged by affine
target additions.

The pole theorem uses polynomiality of the source graph correction;
rational corrections can have their own poles and are outside the
graph problem.

## 1. Exact all-seed separation at \(x=\infty\)

The second-subduction numerator is an exact 77-term polynomial in
\((w,\gamma)\).  For a support monomial \(w^i\gamma^j\), define
\[
A_U=20-i,\qquad B_U=22-i-j.
\tag{S1}
\]
After division by \(x^5\gamma^5\) and substitution \(w=xt\gamma\),
its ratio to the top \(w^{20}\gamma^2\)-term is
\[
x^{-A_U}t^{-A_U}\gamma^{-B_U}.
\tag{S2}
\]
The exact support audit gives
\[
A_U\ge0,\qquad B_U\ge0,
\tag{S3}
\]
with \(B_U=0\) only for the top term.  The unique support point
\((A_U,B_U)=(1,1)\) is \(w^{19}\gamma^2\).

The same description holds for the target seeds.  A \(q_k\)-term of
\(A\) has relative layer
\[
(A_A,B_A)=(6-k,6-k),
\tag{S4}
\]
and a \(p_k\)-term of \(B\) has
\[
(A_B,B_B)=(5-k,5-k).
\tag{S5}
\]
The added \(w\gamma\) and \(\gamma\) terms have layer \((5,4)\).
Layers add in every product \(A^jB^{n-j}\).  Thus every non-top
target component has \(A\ge B\ge1\), and layer \((1,1)\) means
exactly one first-lower \(q_5\)- or \(p_4\)-replacement.

After division by the top Jacobian common factor, a combined layer
\((A,B)\) has the form
\[
x^{-A}t^{-A}\gamma^{-B}\mathcal S(\gamma),
\tag{S6}
\]
where \(\mathcal S\) is linear in
\(\gamma,x\gamma_x,\gamma_t\).  Write the exact Laurent expansion
\[
\gamma=x^I\phi(t)+\text{lower \(x\)-powers},
\qquad \phi(t)\in\mathbb C[t],\quad I\ge2.
\tag{S7}
\]
Its maximal \(x\)-power in (S6) is
\[
\boxed{I(1-B)-A.}
\tag{S8}
\]
The top layer \((0,0)\) is therefore the unique layer at \(x^I\).
Every non-top seed layer is at most \(x^{-1}\), and equality occurs
only for \((A,B)=(1,1)\).  This proves simultaneously that

1. the maximal-\(x\) characteristic equation is exact and receives
   no lower-seed forcing;
2. the normalized \(x^{-1}\) equation contains exactly the first
   lower \(U\)- and target-seed slices;
3. a negative tail in the \(x^I\)-coefficient can never interact
   with a lower seed, even when their scalar graph-weight drops
   happen to agree.

For completeness, the embedding
\[
\mathbb C[x,y]\hookrightarrow\mathbb C[x,x^{-1},t],
\qquad y=t-x^{-1},
\tag{S9}
\]
has polynomial \(t\)-coefficients on every \(x\)-Laurent sector.
Thus (S7) really has \(\phi\in\mathbb C[t]\).  The unique solution of
the top equation is \(t^rP^s\), so it must be polynomial.  This
removes every nonpolynomial completion in all target degrees without
a tail-timing estimate.

The common top Jacobian factor has \(x\)-degree
\[
4n+14+I(4n+16)>1.
\tag{S10}
\]
A nonzero constant Jacobian right side therefore reaches neither
the \(x^I\) nor the \(x^{-1}\) normalized layer.  Also
\[
\deg_xU^{(0)}=15+17I,\quad
\deg_xA^{(0)}=\deg_xB^{(0)}=4+4I,\quad
\deg_xC=1+I.
\tag{S11}
\]
These gaps show that affine additions to either target coordinate
enter strictly below both decisive layers.

The exact support and valuation assertions are checked in
`verify_weighted_lift_all_seed_x_sector_separation.py`.

## 2. Exact first-lower target slice

The first two slices of the second-subduction coordinate are
\[
\begin{aligned}
U^{(0)}&=x^{15}t^{20}\gamma^{17},\\
U^{(1)}&=-\frac{70}{3}x^{14}t^{19}\gamma^{16},
\end{aligned}
\tag{4}
\]
up to one common nonzero scalar.  The exact seed ratios are
\[
\frac{q_5}{q_6}=-\frac{28}{5},
\qquad
\frac{p_4}{p_5}=-\frac{35}{6}.
\tag{5}
\]
Replacing one highest \(A\)- or \(B\)-seed in (1) therefore gives
\[
\begin{aligned}
V^{(0)}
 &=x^{4n}t^{5n}\gamma^{4n}P(t),\\
V^{(1)}
 &=x^{4n-1}t^{5n-1}\gamma^{4n-1}P_1(t),
\end{aligned}
\tag{6}
\]
where
\[
\boxed{
P_1(t)
=-\frac{35n}{6}P(t)+\frac7{30}tP'(t)
=\frac7{30}\bigl(tP'(t)-25nP(t)\bigr).
}
\tag{7}
\]
This identity is coefficientwise: on the \(t^j\)-coefficient the
multiplier is
\[
j\frac{q_5}{q_6}+(n-j)\frac{p_4}{p_5}
=-\frac{35n}{6}+\frac{7j}{30}.
\tag{8}
\]

## 3. The normalized forcing

The top characteristic operator is
\[
\mathcal L_P(\phi)
=x\left(\frac{5n}{t}+17\frac{P'}P\right)\phi_x
-8n\phi_t
+\left(-\frac{5n}{t}+15\frac{P'}P\right)\phi.
\tag{9}
\]
It satisfies \(\mathcal L_P(G)=0\) for (3).  By Section 1, \(G\) is
an honest polynomial \(x^I\)-coefficient.  At normalized \(x\)-power
\(-1\),
divide
\[
J(U^{(1)},V^{(0)})+J(U^{(0)},V^{(1)})
\tag{10}
\]
by the same nonzero top-top common factor used to obtain (9).  Direct
logarithmic differentiation and (3) give
\[
\boxed{
\mathcal R_{n,I,P}
=\frac{7}{120nxt^2P^2}\,\Omega_{n,I,P},
}
\tag{11}
\]
where
\[
\begin{aligned}
\Omega_{n,I,P}={}&
25n^2(1-I)P^2\\
&+4n(17I+15)t^2PP''\\
&+20n(3I+5)tPP'\\
&+(17I+15)(1-4n)t^2(P')^2.
\end{aligned}
\tag{12}
\]
Equivalently, put
\[
z=t\frac{P'}P.
\tag{13}
\]
Then
\[
\mathcal R_{n,I,P}
=\frac{7}{120nxt^2}
\left(
25n^2(1-I)
+4n(17I+15)t z'
+8n(5-I)z
+(17I+15)z^2
\right).
\tag{14}
\]
For \(n=6\), \(P=t+\eta\), and
\(I=48k+33\), formula (11) specializes exactly to
\[
-\frac{7}{15xt^2(t+\eta)^2}
\left(
(900k+600)\eta^2
+(1440k+940)\eta t
+(931k+616)t^2
\right),
\tag{15}
\]
recovering the independently computed degree-six recurrence.

## 4. Root-multiplicity lemma

Let \(\alpha\ne0\) be a root of \(P\) of multiplicity \(e\), and
write
\[
P(t)=(t-\alpha)^eh(t),\qquad h(\alpha)\ne0.
\tag{16}
\]
With \(\tau=t-\alpha\), equation (13) gives
\[
z=\frac{e\alpha}{\tau}+O(1),
\qquad
t z'=-\frac{e\alpha^2}{\tau^2}+O(\tau^{-1}).
\tag{17}
\]
The double-pole coefficient in (14) is therefore
\[
\boxed{
\lim_{t\to\alpha}(t-\alpha)^2\mathcal R_{n,I,P}
=\frac{7(17I+15)e(e-4n)}{120nx}.
}
\tag{18}
\]
For a binary face,
\[
1\le e\le d\le n,\qquad I\ge2,
\tag{19}
\]
so every factor in (18) is nonzero.  In particular, the pole is
genuinely of order two; neither a special position of the root nor
the remaining factor \(h\) changes it.

On the other hand, let \(D(t)\in\mathbb C[t]\) be the coefficient of
the \(x^{-1}\)-sector of \(\gamma\).  The only coefficient of
\(\mathcal L_P(x^{-1}D)\) singular at \(\alpha\) is \(P'/P\), which
has a simple pole.  Differentiating \(D\) creates no pole.  Thus
\[
\operatorname{ord}_\alpha\mathcal L_P(x^{-1}D)\ge-1,
\qquad
\operatorname{ord}_\alpha\mathcal R_{n,I,P}=-2.
\tag{21}
\]
The first-lower equation
\[
\mathcal L_P(x^{-1}D)+\mathcal R_{n,I,P}=0
\tag{22}
\]
is impossible.

The all-seed support lemma proves that no other seed component reaches
this normalized \(x^{-1}\)-sector.  Earlier \(x\)-coefficients belong
to the top operator and are already solved sectorwise; expansion of
the common factor multiplies zero earlier equations and contributes
nothing new here.

## 5. Exhaustion and sharp scope

Over an algebraically closed field, a polynomial whose only root is
zero is a monomial.  Hence exactly one of the following occurs:

1. The characteristic completion is nonpolynomial.  The exact
   maximal-\(x\) equation excludes it, independently of negative-tail
   timing.
2. \(P\) is mixed and the characteristic completion is polynomial.
   Then \(P\) has a nonzero root and (18)--(22) exclude it.
3. \(P\) is a monomial.  This is the pure face
   \(A^dB^{n-d}\), closed by the exact pure first-lower numerator
   classification and its unique forbidden-descent exception in
   `WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_CLOSURE.md`.

The multiplicity coefficient in (18) explains the exact limits of
the local lemma.  Outside the binary-face range \(d\le n\), a formal
factor of multiplicity \(e=4n\) kills its double-pole coefficient.
At the root \(t=0\), the \(t^{-2}\) prefactor and the monomial
characteristic interact differently; for example, for \(P=t^n\)
the first-lower \(t^{-2}\) coefficient vanishes on the resonant
sector \(I=5\), \(J=15\).  These are counterexamples to extending the
nonzero-root pole lemma verbatim, not counterexamples to the
weighted-lift exclusion: this unique zero is exactly the \(A^n\)-ray
whose forced \(1365c\,xy^{11}\) term closes the pure classification.

Thus every homogeneous binary target is excluded in every degree on
every nonconstant graph.

## 6. Constant graphs

Let \(g=c\) be constant.  If \(c\ne0\), then
\[
\gamma=(1-a)+axt+cx^2
\tag{23}
\]
has maximal sector \(cx^2\).  Substitution in the exact top operator
gives
\[
\mathcal L_P(cx^2)
=cx^2\left(\frac{5n}{t}+49\frac{P'}P\right).
\tag{24}
\]
Its vanishing would require
\[
t\frac{P'}P=-\frac{5n}{49},
\tag{25}
\]
which no nonzero polynomial \(P\) satisfies.

If \(c=0\), the maximal sector is \(axt\).  Its equation is
\[
\mathcal L_P(axt)
=ax\left(-8n+32t\frac{P'}P\right).
\tag{26}
\]
It can vanish only if \(n\) is divisible by four and
\[
P=t^{n/4}
\tag{27}
\]
up to scale.  On this pure face, the remaining constant
\((1-a)\)-sector gives
\[
\mathcal L_P(1-a)
=-\frac{5n}{4t}(1-a)
=-\frac{455n}{136t}\ne0,
\tag{28}
\]
because \(a=-57/34\).  The all-seed lemma puts every non-top seed
strictly below this sector, so it cannot be cancelled.

This excludes both constant-graph cases.  The calculation is checked
in `verify_weighted_lift_all_seed_x_sector_separation.py`.

The forcing and root calculation are checked in
`verify_weighted_lift_general_binary_first_lower_pole_obstruction.py`.
