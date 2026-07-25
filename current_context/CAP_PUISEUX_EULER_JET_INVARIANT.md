# A branchwise Euler invariant for infinitely-near Newton-cap jets

Date: 25 July 2026

## Audited conclusion

There is a finite, non-computational invariant of every successive
infinitely-near cluster above a paired Newton-cap root.  It comes directly
from the full Jacobian equation, not merely from the two face
factorizations.

In a local boundary chart write
\[
 P=u^{-p}F(u,v),\qquad Q=u^{-q}G(u,v),
 \tag{1}
\]
where \(F,G\in k[[u,v]]\), and suppose
\[
 [P,Q]_{u,v}=u^\kappa H(u,v),\qquad H(0,0)\ne0.
 \tag{2}
\]
Put
\[
 N=p+q+1+\kappa.
 \tag{3}
\]
Then (2) is equivalent to
\[
 qF_vG-pFG_v+u(F_uG_v-F_vG_u)=u^N H.
 \tag{4}
\]

Let \(v=\alpha(u)\) be any Puiseux branch of \(F=0\), and set
\[
 e_\alpha=\operatorname{ord}_uF_v(u,\alpha(u)),\qquad
 g_\alpha(u)=G(u,\alpha(u)).
 \tag{5}
\]
Restriction of (4) to this branch gives the exact Euler equation
\[
 F_v(u,\alpha)\bigl(qg_\alpha-u g_\alpha'\bigr)
   =u^NH(u,\alpha),
 \tag{6}
\]
or equivalently
\[
 \boxed{\quad
 \left(\frac{g_\alpha}{u^q}\right)'
 =-\frac{u^{N-q-1}H(u,\alpha)}
          {F_v(u,\alpha)}.
 \quad}
 \tag{7}
\]
Thus every nonresonant jet of \(G\) on the branch is forced.  The only
free branchwise coefficient is the integration constant multiplying
\(u^q\).

In particular, the Puiseux residue
\[
 \boxed{\quad
 \operatorname {Res}_{u=0}
 \frac{u^{N-q-1}H(u,\alpha)}
      {F_v(u,\alpha)}\,du=0
 \quad}
 \tag{8}
\]
is a necessary condition.  Since \(H\) is a unit, (8) immediately gives
the forbidden-contact equality
\[
 \boxed{e_\alpha\ne N-q.}
 \tag{9}
\]
If \(e_\alpha>N-q\), equation (8) is a genuine constraint on a finite
successive jet of the cluster.  It is exactly the obstruction to a
logarithm in the formal primitive in (7).

There is a symmetric statement on every Puiseux branch \(v=\beta(u)\)
of \(G=0\).  With
\[
 f_\beta=F(u,\beta(u)),\qquad
 d_\beta=\operatorname{ord}_uG_v(u,\beta(u)),
\]
one has
\[
 \boxed{\quad
 \left(\frac{f_\beta}{u^p}\right)'
 =\frac{u^{N-p-1}H(u,\beta)}
        {G_v(u,\beta)},\qquad
 \operatorname {Res}_{u=0}
 \frac{u^{N-p-1}H(u,\beta)}
      {G_v(u,\beta)}\,du=0,
 \quad}
 \tag{10}
\]
and hence
\[
 \boxed{d_\beta\ne N-p.}
 \tag{11}
\]

Equations (8) and (10) are the promised finite invariants.  In the
original boundary chart they encode arbitrary finite sequences of point
blowups: the Puiseux contacts and the residue record precisely the
infinitely-near path.  If one changes charts after a blowup, the same
derivation applies again with the transformed values of \(p,q,\kappa\).

## 1. Proof of the branchwise recurrence

Differentiating (1) and extracting \(u^{-p-q-1}\) gives
\[
 [P,Q]_{u,v}
 =u^{-p-q-1}
 \{qF_vG-pFG_v+u(F_uG_v-F_vG_u)\}.
\]
This proves (4).

Along \(F(u,\alpha(u))=0\),
\[
 F_u(u,\alpha)+F_v(u,\alpha)\alpha'=0.
\]
Substitution in (4) gives
\[
\begin{aligned}
u^NH(u,\alpha)
 &=F_v\{qG-u(G_u+\alpha'G_v)\}\\
 &=F_v(qg_\alpha-u g_\alpha'),
\end{aligned}
\]
which is (6).  Dividing and applying
\[
\left(g/u^q\right)'=u^{-q-1}(ug'-qg)
\]
proves (7).

Work in a finite Puiseux extension \(k((u^{1/r}))\).  The image of
\(d/du\) consists exactly of the Puiseux Laurent series whose
\(u^{-1}\)-coefficient is zero.  Since the left side of (7) is a
derivative, its right side has zero residue.  This proves (8).
If \(e_\alpha=N-q\), the right side of (7) has a nonzero leading
\(u^{-1}\)-term because \(H\) is a unit, contradicting (8).  The proof
of (10)--(11) is identical after restricting (4) to \(G=0\).

This proof uses the complete bracket identity but never enumerates the
ambient coefficient scheme.

## 2. The valid trace/gluing consequence

The branch constants are not completely independent.  There is a clean
algebraic formulation of exactly how far they glue.

Let \(K=k((u))\), let \(F^\mathrm W\) be the monic Weierstrass
polynomial generating the same ideal as \(F\), and put
\[
\mathcal A=K[v]/(F^\mathrm W).
\]
Equation (4) implies that \(F\) is separable over \(K\).  The derivation
\(d/du\) has the unique extension
\[
\delta(\bar v)=-\frac{F_u}{F_v}
\tag{12}
\]
to \(\mathcal A\).  Reducing (4) modulo \(F\) gives the single
finite-algebra identity
\[
\boxed{\quad
\delta\left(\frac{\bar G}{u^q}\right)
=-\frac{u^{N-q-1}\bar H}{\overline{F_v}}.
\quad}
\tag{13}
\]

Decompose \(\mathcal A\) into the fields associated with the irreducible
factors of \(F\) over \(K\).  The constant field of each factor is \(k\)
when \(k\) is algebraically closed.  Termwise Puiseux integration with
zero constant commutes with conjugacy.  It follows that:

> all conjugate Puiseux leaves belonging to one irreducible factor of
> \(F\) have the same resonant integration constant \(C\).

There is one such constant per irreducible factor, not one arbitrary
constant per geometric leaf.  If \(F\) splits completely over \(K\),
however, this gives no identification between distinct leaves.  This is
the precise scope of conjugacy gluing.

There is also an exact trace equation.  Let
\[
\mathcal R(u)=\operatorname {Norm}_{\mathcal A/K}(\bar G)
             =\operatorname {Res}_v(F^\mathrm W,G)
\]
and
\[
\mathcal T(u)=\mathcal R(u)\,
\operatorname {Tr}_{\mathcal A/K}
\left(\frac{\bar H}{\overline{F_v}\bar G}\right).
\tag{14}
\]
The expression \(\mathcal T\) is symmetric in the roots; equivalently it
is a subresultant coefficient and is regular whenever \(F,G,H\) are.
Taking the norm derivative in (13) yields
\[
\boxed{\quad
\left(\frac{\mathcal R}{u^{aq}}\right)'
=-u^{N-aq-1}\mathcal T.
\quad}
\tag{15}
\]
Thus the resultant has its own finite no-log residue condition.  This is
a genuine gluing of all \(F\)-branches, but it retains a homogeneous
integration constant.  Neither (13) nor (15) forces that constant to
vanish.  Consequently the trace argument is valid but does not, without
an additional global input, prove support exhaustion or a contradiction.

This limitation is sharp even for an exact monomial bracket.  Fix
integers \(b\ge2\), \(N>b\) and any \(C\in k\), and take
\[
p=1,\qquad q=b,\qquad
F=v,\qquad
G=v^b+C u^b+\frac{u^N}{b-N}.
\tag{16}
\]
A direct calculation gives
\[
qF_vG-pFG_v+u(F_uG_v-F_vG_u)=u^N.
\tag{17}
\]
On the sole \(F\)-branch,
\[
\frac{G(u,0)}{u^b}
=C+\frac{u^{N-b}}{b-N}.
\tag{18}
\]
Thus \(C\) is an arbitrary nonzero resonant constant in a genuine
solution of the complete local bracket equation.  Any theorem killing
the analogous constants in case c must use more than local
differential-algebra or trace gluing.

## 3. Resolution-tree and cross-contact form

Assume that \(F(0,v)\) has order \(a\) and \(G(0,v)\) has order \(b\).
After Weierstrass preparation and passage to a splitting Puiseux field,
write
\[
 F=U_F\prod_{i=1}^a(v-\alpha_i),\qquad
 G=U_G\prod_{j=1}^b(v-\beta_j),
\tag{19}
\]
where the two \(U\)'s are units.  Then
\[
\begin{aligned}
e_i&=\operatorname{ord}_uF_v(u,\alpha_i)
    =\sum_{\ell\ne i}\operatorname{ord}_u(\alpha_i-\alpha_\ell),\\
\tau_i&=\operatorname{ord}_uG(u,\alpha_i)
    =\sum_j\operatorname{ord}_u(\alpha_i-\beta_j).
\end{aligned}
\tag{20}
\]
Thus \(e_i\) is the total same-color contact issuing from the \(i\)-th
leaf of the infinitely-near tree, while \(\tau_i\) is its total
opposite-color contact.

When \(e_i\ne N-q\), integration of (7) gives
\[
G(u,\alpha_i)
=C_i u^q+
\text{a series with nonzero leading exponent }N-e_i.
\tag{21}
\]
Consequently
\[
\boxed{
\begin{array}{ll}
e_i<N-q:&\tau_i\in\{q,N-e_i\},\\[2mm]
e_i>N-q:&\tau_i=N-e_i.
\end{array}}
\tag{22}
\]
In the first line, \(\tau_i=q\) occurs exactly when the resonant constant
\(C_i\) is nonzero; if \(C_i=0\), then \(\tau_i=N-e_i\).
The symmetric formulas are
\[
\boxed{
\begin{array}{ll}
d_j<N-p:&\rho_j\in\{p,N-d_j\},\\[2mm]
d_j>N-p:&\rho_j=N-d_j,
\end{array}}
\qquad
\rho_j=\sum_i\operatorname{ord}_u(\beta_j-\alpha_i).
\tag{23}
\]
As a consistency check,
\[
\sum_i\tau_i=I_0(F,G)=\sum_j\rho_j.
\tag{24}
\]

The data in (20)--(24) are finite tree data.  They can be propagated
along an arbitrary admissible corner chain without introducing the
lower ambient coefficients one at a time.

## 4. Exact case-c thresholds

### The vertical \((2,3)\) cap

Put \(u=x^{-1}\) and \(v=y-s\).  Since the reduced bracket is
\([P,Q]_{x,y}=x^2\),
\[
[P,Q]_{u,v}=-u^{-4}.
\]
The projective local model
\[
[P:Q:1]=[u^4v^2:v^3:u^{12}]
\]
has \(p=8,q=12,\kappa=-4\), hence
\[
N=17.
\tag{25}
\]
For either of the two \(P\)-branches, its contact with the other
\(P\)-branch is \(e_i\), so
\[
\boxed{e_i\ne5,\qquad
\tau_i\in
\begin{cases}
\{12,17-e_i\},&e_i<5,\\
\{17-e_i\},&e_i>5.
\end{cases}}
\tag{26}
\]
The exact successive-jet residue is
\[
\operatorname {Res}_{u=0}
\frac{u^4}{F_v(u,\alpha_i)}\,du=0
\tag{27}
\]
up to a nonzero constant sign.

For a \(Q\)-branch,
\[
\boxed{d_j\ne9,\qquad
\rho_j\in
\begin{cases}
\{8,17-d_j\},&d_j<9,\\
\{17-d_j\},&d_j>9,
\end{cases}}
\tag{28}
\]
and its residue condition is
\[
\operatorname {Res}_{u=0}
\frac{u^8}{G_v(u,\beta_j)}\,du=0.
\tag{29}
\]

### The diagonal \((8,12)\) cap

Put \(u=y^{-1}\) and \(v=xy-t\).  Then
\[
x=(t+v)u,\qquad
\det\frac{\partial(x,y)}{\partial(u,v)}=u^{-1},
\]
so
\[
[P,Q]_{u,v}=(t+v)^2u.
\]
The projective local model
\[
[P:Q:1]=[u^4v^8:v^{12}:u^{12}]
\]
again has \(p=8,q=12\), but now \(\kappa=1\), whence
\[
N=22,\qquad H=(t+v)^2.
\tag{30}
\]
Every \(P\)-leaf and \(Q\)-leaf therefore satisfies respectively
\[
\boxed{e_i\ne10,\qquad
\tau_i\in
\begin{cases}
\{12,22-e_i\},&e_i<10,\\
\{22-e_i\},&e_i>10,
\end{cases}}
\tag{31}
\]
and
\[
\boxed{d_j\ne14,\qquad
\rho_j\in
\begin{cases}
\{8,22-d_j\},&d_j<14,\\
\{22-d_j\},&d_j>14.
\end{cases}}
\tag{32}
\]
The corresponding finite residue tests are
\[
\operatorname {Res}_{u=0}
\frac{u^9(t+\alpha_i)^2}{F_v(u,\alpha_i)}\,du=0,
\qquad
\operatorname {Res}_{u=0}
\frac{u^{13}(t+\beta_j)^2}{G_v(u,\beta_j)}\,du=0.
\tag{33}
\]

## 5. What this proves and what remains

The face data in `CASE_C_CAP_SUPPORT_EXHAUSTION_NO_GO.md` fix only the
numbers of leaves, namely \((2,3)\) and \((8,12)\).  They do not fix the
same-color contact sums \(e_i,d_j\), the cross-contact sums
\(\tau_i,\rho_j\), or the residues (27), (29), and (33).  The bracket
equation does.

The new invariant is therefore strictly deeper than cap
multiplicities:

1. it forbids one exact polar-contact level on every leaf;
2. beyond that level it fixes the entire opposite-color contact sum;
3. it converts every still-deeper infinitely-near path into one finite
   residue equation; and
4. it leaves only one resonant constant per irreducible branch factor
   below the threshold.

It is not by itself a global contradiction.  Section 2 gives the full
conjugacy and trace statement available from the local differential
algebra, and its surviving constants show exactly why that statement
does not close the argument.  The next positive target is therefore
global: relate the surviving constants at the two distinct cap clusters,
or show that the normalized outer sheet fixes one of them.  Either route
would combine the caps without returning to the 165-coordinate
recurrence.
