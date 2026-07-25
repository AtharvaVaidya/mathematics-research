# Universal radial cusp contact from a homogeneous centralizer

Date: 24 July 2026

## Scope and theorem

This is a theorem about the **radial total-degree boundary at infinity**.
It is not a statement about the separate affine case-c line \(x=0\).

Let \(k\ge1\), put \(r=k+1\), and take the full bounded \((2,3)\) radial
supports used by the universal deformation complex.  In
\[
z=xy,\qquad w=xy^2
\]
coordinates one has
\[
\{z,w\}_{x,y}=w,\qquad
\{P,Q\}_{z,w}=\frac{z^4}{w^3}.
\]
The largest total Laurent degrees are
\[
\deg_{\rm tot}P=2r,\qquad \deg_{\rm tot}Q=3r.
\]
Assume the two endpoints of each leading radial edge are nonzero, as they
are for a full Newton polygon.  Let \(L\) cancel the common leading
square/cube ratio and set
\[
D=Q^2-LP^3.
\]
Then \(D\ne0\), and if \(d=\deg_{\rm tot}D\), one has
\[
\boxed{
d\in\{5r,4r,3r,2r\}\quad\text{or}\quad d\le r+3,
}
\]
where entries in the displayed set that already satisfy \(d\le r+3\)
are simply redundant for small \(r\).

Consequently the radial cusp-contact deficit
\[
c_\infty=6r-\deg_{\rm tot}(Q^2-LP^3)
\]
satisfies
\[
\boxed{c_\infty\ge r=k+1.}
\]
More precisely, the high-degree alternatives give contact
\(r,2r,3r,4r\), while the low alternative gives
\(c_\infty\ge5r-3\).

For \(k=3\), \(r=4\), this specializes to total difference degree
\[
20,16,12,8\quad\text{or}\quad\le7,
\]
which is the same numerical spectrum as the a/b five-block theorem.
The geometric interpretations differ: the a/b theorem can restrict
directly to \(z=0\), whereas the full radial case-c support contains
negative \(z\)-powers.  No conclusion about
\(P(0,y),Q(0,y)\) on the affine critical line should be inferred from
this universal theorem.

## 1. Exact support bookkeeping

The outer \(P\)-block has radial degree two and \(w\)-exponents
\[
-1,\ldots,2k,
\]
while the outer \(Q\)-block has radial degree three and exponents
\[
-1,\ldots,3k.
\]
The lower-support rule with vertical bounds \(2r,3r\) gives:

- for \(P\), only radial degrees \(2,1,0\) reach total degree \(2r\);
- for \(Q\), only radial degrees \(3,2,1,0\) reach total degree \(3r\);
- every negative radial block has strictly smaller total degree.

Thus the leading forms have exactly the shapes
\[
\begin{aligned}
P_{2r}&=A w^{2r}+Czw^{2r-1}+Ez^2w^{2r-2},\\
Q_{3r}&=B w^{3r}+Dzw^{3r-1}
       +Fz^2w^{3r-2}+Gz^3w^{3r-3}.
\end{aligned}
\]
The four endpoint coefficients \(A,E,B,G\) are nonzero.

The coordinate ledger is also exact.  Since
\[
\{z,w\}_{x,y}=w,\qquad x=\frac{z^2}{w},
\]
the equation \(\{P,Q\}_{x,y}=x^2\) becomes
\[
w\{P,Q\}_{z,w}=\frac{z^4}{w^2},
\qquad
\{P,Q\}_{z,w}=\frac{z^4}{w^3}.
\]
The canonical Jacobian on the right has total Laurent degree one,
independently of \(k\).

## 2. Common leading root

The top bracket degree is \(5r-2>1\), so
\[
\{P_{2r},Q_{3r}\}=0.
\]
Euler's identity gives
\[
2P_{2r}\,\mathrm dQ_{3r}
-3Q_{3r}\,\mathrm dP_{2r}=0.
\]
Unique factorization therefore supplies a homogeneous polynomial \(R\)
of degree \(r\) and nonzero constants \(\alpha,\beta\) such that
\[
P_{2r}=\alpha R^2,\qquad
Q_{3r}=\beta R^3,\qquad
L=\frac{\beta^2}{\alpha^3}.
\]
The exact \(z\)-degrees and \(w\)-valuations of the endpoint terms force
\[
\boxed{R=w^{r-1}(uw+vz)=w^k(uw+vz),\qquad uv\ne0.}
\]
It follows that the entire degree-\(6r\) part of \(D\) vanishes.

## 3. Degree bound from one exact identity

The identity
\[
\boxed{\{P,D\}=2Q\{P,Q\}
=2Q\frac{z^4}{w^3}}
\]
has right side of total degree at most \(3r+1\).
Let \(D_d\) be the top nonzero total-homogeneous part of \(D\).  The
top part on the left is
\[
\{P_{2r},D_d\},
\]
of degree \(d+2r-2\).  Hence, whenever
\[
d+2r-2>3r+1,\qquad\text{equivalently }d>r+3,
\]
one must have
\[
\{P_{2r},D_d\}=0,\qquad \{R,D_d\}=0.
\]

For completeness, the homogeneous centralizer argument works in the
rational function field, so the negative radial powers cause no problem.
If a nonzero homogeneous rational function \(H\) of degree \(d\) satisfies
\(\{R,H\}=0\), Euler's identity gives
\[
rR\,\mathrm dH-d\,H\,\mathrm dR=0.
\]
Therefore
\[
\mathrm d(H^r/R^d)=0,\qquad H^r=cR^d.
\]
The valuation along the irreducible factor \(uw+vz\) forces \(r\mid d\),
and then
\[
H=c'R^{d/r}.
\]
Since \(D_{6r}=0\), the only multiples of \(r\) below \(6r\) and above
\(r+3\) are among
\[
5r,4r,3r,2r.
\]
This proves the spectrum and the contact bound.

Finally, \(D\) cannot vanish identically: \(Q^2=LP^3\) would make
\(P,Q\) algebraically dependent and force their Jacobian to be zero,
contrary to \(z^4/w^3\ne0\).

## 4. Verification

Run
```bash
PYTHONPATH=/tmp/codex-mathdeps.IyweI7 \
python3 route_bd_universal_contact_spectrum.py
```
The verifier checks the coordinate change, the precise all-\(k\) support
maxima, the leading-root shape, the Laurent centralizer kernels on a range
of \(r\), and the symbolic degree/contact ledger.
