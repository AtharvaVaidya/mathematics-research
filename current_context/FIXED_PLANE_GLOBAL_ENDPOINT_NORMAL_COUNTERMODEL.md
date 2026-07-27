# A globally coupled degree-nine normal-map countermodel

Date: 25 July 2026

## 1. Exact conclusion

The two resolved ends of the conductor image can be coupled through the
same effective pullback divisor, the same pullback-line solution, and one
residual projective bridge without forcing the Poincare-residue exponent
to vanish.

More precisely, the 19-vertex full-effectivity ledger in
`GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md` admits an exact smooth target
curve \(\Gamma\simeq\mathbf G_m\) for which

1. the fixed-source Liouville residue is \(2/3\);
2. the target Poincare-residue exponent is \(j=-1\);
3. the conductor contacts have local cover degree \(2\);
4. the single residual bridge has local cover degree \(1\) at both ends;
5. all four values of \(b,\eta,\kappa\), and \(r\) agree with the two
   resolved target ends coefficient-for-coefficient; and
6. the complete equations \(Qb=y\) and \(Q\eta+z=9y\) hold for one
   common boundary tree.

This is an exact countermodel to any inference from global endpoint
pairing and normal-map gluing alone.  It is **not** a morphism, a
polynomial Darboux pair, or a Keller counterexample.  The boundary ledger
still has six final point-mapping curves, and no two global sections
realizing the numerical data have been constructed.  The calculation
therefore isolates finality/minimality or section-level realization as
the missing input.

## 2. A smooth degree-nine target with \(j=-1\)

Put \(a=2/3\), and on \(\mathbf G_m\) define
\[
X=s^{-2}+a s^{-1},\qquad Y=s+X^4.
\tag{1}
\]
Set
\[
T=Y-X^4
\]
and
\[
\boxed{\qquad
F(X,Y)=X(Y-X^4)^2-a(Y-X^4)-1.
\qquad}
\tag{2}
\]
Then \(T=s\) on the parametrized curve, while (2) gives
\[
T(XT-a)=1.
\tag{3}
\]
Consequently
\[
\mathbf C[X,Y]/(F)
\simeq\mathbf C[T,T^{-1}],
\quad
X=T^{-2}+aT^{-1},
\quad
Y=T+X^4.
\tag{4}
\]
Thus \(F=0\) is a closed smooth embedding of \(\mathbf G_m\) in
\(\mathbf A^2\).  Its degree is nine.

The Liouville residue is exact:
\[
X\,dY=X\,ds+4X^4\,dX,
\]
and the second summand is exact.  Therefore
\[
\boxed{\qquad
\operatorname {Res}_{s=0}(X\,dY)=a=\frac23.
\qquad}
\tag{5}
\]
Moreover,
\[
F_Y=2XT-a,
\qquad
\frac{dX}{F_Y}=-s^{-2}\,ds
             =-s^{-1}\frac{ds}{s}.
\tag{6}
\]
Hence
\[
\boxed{\qquad j=-1.\qquad}
\tag{7}
\]

Both normalization ends map to the same point \([0:1:0]\).  In the
projective chart \(Y=1\), write \(u=X/Y\) and \(z=Z/Y=1/Y\).  At
\(s=0\),
\[
\operatorname {ord}_s(u,z)=(6,8),
\tag{8}
\]
whereas, for \(\tau=s^{-1}\) at the other end,
\[
\operatorname {ord}_\tau(u,z)=(2,1).
\tag{9}
\]
Thus the line-at-infinity multiplicities of the two ends are \(8\) and
\(1\), whose sum is the projective degree \(9\).

## 3. Exact target-resolution triples

Resolve the pair consisting of the projective curve and the line at
infinity at their common point.  The first blowup sees the two distinct
tangent branches of multiplicities \(6\) and \(1\), so the coefficient
of the total curve on the first exceptional divisor is \(7\).  The
smooth \(\tau=0\) branch is already separated there.  Its terminal
triple is
\[
\boxed{\qquad
(M,N,c)_{\infty}=(1,7,1).
\qquad}
\tag{10}
\]
Here \(M\) is the coefficient of the total transform of the target line,
\(N\) is the coefficient of the total transform of the target curve,
and \(c\) is the coefficient of
\(K_Y-\rho^*K_{\mathbf P^2}\).

The \(s=0\) branch continues through the following exceptional
recurrence.  The entry in the fourth column is the multiplicity of the
strict branch at the center creating that row.
\[
\begin{array}{c|c|c|c}
 & (M,N,c) & \text{center} & \text{strict multiplicity}\\ \hline
D_1&(1,7,1)&\text{original point}&7\text{ in total}\\
D_2&(2,9,2)&L\cap D_1&2\\
D_3&(3,18,4)&D_2\cap D_1&2\\
D_4&(4,27,6)&D_3\cap D_1&2\\
D_5&(4,29,7)&\operatorname{gen}(D_4)&2\\
D_6&(4,31,8)&\operatorname{gen}(D_5)&2\\
D_7&(4,33,9)&\operatorname{gen}(D_6)&2\\
D_8&(4,35,10)&\operatorname{gen}(D_7)&2\\
D_9&(4,36,11)&\operatorname{gen}(D_8)&1\\
D_{10}&(8,72,22)&D_8\cap D_9&1
\end{array}
\tag{11}
\]
The transformed parameter-order pairs along this path are
\[
(8,6),(2,6),(2,4),(2,2),(2,9),(2,7),(2,5),(2,3),
(2,1),(1,1).
\tag{12}
\]
After the last crossing blowup the strict branch is smooth and
transverse to \(D_{10}\).  Therefore
\[
\boxed{\qquad
(M,N,c)_0=(8,72,22).
\qquad}
\tag{13}
\]

These numbers independently recover the residue exponent.  Since
\(d=9\),
\[
(d-3)M+c-N=
\begin{cases}
-2=j-1,&s=0,\\
0=-j-1,&s=\infty.
\end{cases}
\tag{14}
\]
The resolved-target slopes are consequently
\[
\boxed{\qquad
\mu_0=\frac{c+1-N}{M}=-\frac{49}{8},
\qquad
\mu_\infty=-5.
\qquad}
\tag{15}
\]

## 4. Matching the globally effective source ledger

Use the exact 19-vertex tree and vectors of Section 5 of
`GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md`.  The conductor \(C\) meets
nodes \(4,7\), and the unique degree-one residual bridge \(H\) meets
nodes \(3,6\).  The strict-incidence vector is
\[
z=\mathbf e_3+\mathbf e_4+\mathbf e_6+\mathbf e_7.
\tag{16}
\]
For these four vertices, the source data are
\[
\begin{array}{c|c|c|c|c|c|c|c}
\text{node}&\text{component/end}&\beta&b&\kappa&\eta&\theta&r\\ \hline
4&C,\ s=0&2&16&-2&147&3&48\\
3&H,\ s=0&1&8&-1&74&2&24\\
7&C,\ s=\infty&2&2&2&15&1&4\\
6&H,\ s=\infty&1&1&1&8&1&2
\end{array}
\tag{17}
\]
Here \(\beta\) is the local cover degree and
\(\theta=\eta-N\beta\).  Every column in (17) is forced by the target
data:
\[
b=M\beta,
\tag{18}
\]
\[
\kappa=
\begin{cases}
\beta j,&s=0,\\
-\beta j,&s=\infty,
\end{cases}
\tag{19}
\]
\[
\eta=N\beta+\theta,
\tag{20}
\]
and
\[
r=c\beta+\beta+\theta-1
 =\eta+\mu b-1
 =a_i-1+3b_i.
\tag{21}
\]
Thus the conductor and residual component see the same target
resolution at each end, with local degrees \(2\) and \(1\),
respectively.

The global source equations are simultaneously exact:
\[
Qb=y,\qquad b^TQb=3,\qquad
Q\eta+z=9y,\qquad \eta^Ty=0.
\tag{22}
\]
The conductor degree and normal degree are
\[
b_4+b_7=18=2\cdot1\cdot9,
\qquad
\eta_4+\eta_7=162=2\cdot1\cdot9^2.
\tag{23}
\]
The residual bridge has
\[
H^2=-1,\qquad
\eta_3+\eta_6-1=81,
\qquad
\kappa_3+\kappa_6=0.
\tag{24}
\]
Its two endpoint charges are therefore paired through one actual
projective component, not assigned independently.

## 5. The exact logical boundary

The construction proves that the following package is consistent:

1. a genuine smooth degree-nine target \(\mathbf G_m\);
2. the exact fixed-source Liouville residue;
3. one common nonzero Poincare exponent \(j=-1\);
4. both complete target resolutions;
5. pointwise tangential-normal determinant gluing at all four marked
   contacts;
6. one conductor and one residual bridge joining the same two target
   ends;
7. effective ramification and component adjunction; and
8. one common integral solution of the full pullback equations.

What is not present is equally precise.  In the 19-vertex boundary tree,
the final exceptional curves are
\[
10,11,12,14,15,16,17,18.
\]
Only \(14\) and \(16\) are dicritical.  The other six,
\[
\boxed{\qquad 10,11,12,15,17,18,\qquad}
\tag{25}
\]
are final point-mapping curves, contrary to the final-boundary theorem
for a minimal Keller resolution.  In addition, an integral divisor
ledger does not construct the two global sections of the line bundle
\(\mathcal O_X(P)\) that would define a morphism.

Accordingly, a proof of \(j=0\) cannot follow from coupling the two
endpoint Green problems only through their common \(Q,b,\eta,z\) data
and their common target normal maps.  It must use at least one
constraint that this model deliberately omits:

* finality/minimality strong enough to exclude the six point-mapping
  final curves; or
* section-level base-point and local-mapping compatibility stronger
  than the divisor intersection equations.

The curve, the resolution recurrence, the four local lifts, the full
19-vertex ledger, and the exact failure set (25) are checked in
`verify_fixed_plane_global_endpoint_normal_countermodel.py`.
