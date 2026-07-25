# Bounded memo: Routes B and D at the \((72,108)\) frontier

Date: 2026-07-24

## Bottom line

No counterexample and no proof of \(JC(2)\) was obtained. The workspace initially
contained no support file, coefficient equations, prior computation, or certificate.
The phrase “the surviving \((72,108)\) reduced system” in the prompt therefore did
not supply a finite system that could simply be solved.

I reconstructed the two exact finite supports from Proposition 4.3 of
Guccione--Guccione--Horruitiner--Valqui (GGHV), expanded the universal bracket
equations conceptually and by a dependency-free verifier, and proved one exact
one-parameter obstruction. The obstruction covers the forced-edge degeneration
\[
P_t=x+y^8(xy-t)^8,
\]
but it does **not** cover the free lower/interior coefficients required by the full
GGHV polygons. That missing simultaneous-coefficient step is the honest gap.

## 1. Known source facts versus reconstruction

### Published source fact

GGHV, Proposition 4.3, states that the \((8,28)\) corner case (which corresponds to
the original degree pair \((72,108)\)) reduces to \(P,Q\in L^{(1)}\) satisfying
\([P,Q]=x^2\) and one of two Newton-polygon alternatives:

\[
\begin{aligned}
\text{case c:}\quad
N(P)&=\operatorname{conv}\{(0,0),(1,0),(8,14),(8,16),(0,8)\},\\
N(Q)&=\operatorname{conv}\{(0,0),(2,1),(12,21),(12,24),(0,12)\};
\end{aligned}
\]

\[
\begin{aligned}
\text{cases a/b:}\quad
N(P)&=\operatorname{conv}\{(0,0),(1,0),(8,14),(8,16)\},\\
N(Q)&=\operatorname{conv}\{(0,0),(2,1),(12,21),(12,24)\}.
\end{aligned}
\]

The labels “a/b” and “c” refer to three pre-inversion shapes in the proof; the first
two acquire the same final polygon. Source:
[arXiv:2204.14178](https://arxiv.org/abs/2204.14178).

### Exact reconstruction

Enumerating all lattice points in the two convex polygons gives:

| reduced branch | \( |S_P| \) | \( |S_Q| \) | possible Jacobian rows | nonzero bilinear terms |
|---|---:|---:|---:|---:|
| a/b | 25 | 47 | 92 | 975 |
| c | 61 | 125 | 302 | 7141 |

These counts are exact and are reproduced by
[`route_bd_verify.py`](./route_bd_verify.py).

Writing
\[
P=\sum_{(u,v)\in S_P}a_{uv}x^uy^v,\qquad
Q=\sum_{(i,j)\in S_Q}b_{ij}x^iy^j,
\]
the complete finite system determined by the polygons alone is
\[
E_{r,s}:=
\sum_{\substack{(u,v)\in S_P,\ (i,j)\in S_Q\\
u+i-1=r,\ v+j-1=s}}
(uj-vi)a_{uv}b_{ij}
-\delta_{(r,s),(2,0)}=0.
\]
Thus it is bilinear in 72 variables for a/b and 186 variables for c, before edge
normalizations and before imposing that every listed polygon vertex has nonzero
coefficient. For fixed \(P\), it is a linear system in the \(Q\)-coefficients.

Every output row obeys \(r-s\le 2\). This is not an additional elimination in the
universal system: it follows immediately from
\(\max_{S_P}(u-v)=\max_{S_Q}(i-j)=1\).

## 2. Exact obstruction obtained

The case-c upper edge \((0,8)\)--\((8,16)\) has the forced form
\(y^8(xy-t)^8\) after the Laurent inversion used by GGHV. Consider the sparse
degeneration
\[
P_t=x+y^8(xy-t)^8.
\]
For any polynomial \(R\), let \([x^ry^s]R\) denote its coefficient. Define
\[
\begin{aligned}
L_t(R)={}&576[x^2]R+24[x^9y^{16}]R+51[x^{16}y^{32}]R\\
&+612t[x^{17}y^{33}]R+4148t^2[x^{18}y^{34}]R.
\end{aligned}
\]
Then, for every \(Q\) supported in the 125-point case-c \(Q\)-polygon,
\[
L_t([P_t,Q])=0
\quad\text{identically in }\mathbb Z[t],
\]
whereas
\[
L_t(x^2)=576.
\]
Hence no such \(Q\) can satisfy \([P_t,Q]=x^2\), for any \(t\).

This certificate is especially small. Only four \(Q\)-columns meet its five rows:

| \(Q\)-monomial | coefficients on the five rows |
|---|---|
| \(x^2y\) | \((1,-24,0,0,0)\) |
| \(x^9y^{17}\) | \((0,17,-8,0,0)\) |
| \(x^{10}y^{18}\) | \((0,0,192t,-16,0)\) |
| \(x^{11}y^{19}\) | \((0,0,-1120t^2,256t,-24)\) |

Their dot products with
\((576,24,51,612t,4148t^2)\) are all zero. The verifier checks all 125 columns,
not just the four displayed nonzero ones.

### Why this is not the full obstruction

The sparse \(P_t\) does not have the full required Newton polygon: in particular,
the required \((8,14)\) vertex and the unrestricted interior coefficients are
absent. The displayed covector is not universal under those perturbations. An
exact witness is:
\[
L_t([xy,x^9y^{16}])=24(16-9)=168\ne0.
\]
So adding an \(\varepsilon xy\) coefficient introduces
\(168\varepsilon b_{9,16}\) into the certificate equation. A corrected covector
may exist for each parameter slice, but proving a single simultaneous certificate
over all 61 \(P\)-coefficients (or proving a finite chart cover) remains undone.

This distinction is decisive: sampled \(P\)'s, one-axis symbolic sweeps, and
certificates on forced-edge families do not prove that the full bilinear variety is
empty.

## 3. Route D: what the infinity/Newton reduction does and does not prove

The GGHV argument is already a substantial infinity reduction. Its Newton
transformations turn the last open low-degree configuration into the two polygons
above. The final inversion
\[
x\mapsto x^{-1},\qquad y\mapsto x^4y
\]
sends exponents \((a,b)\mapsto(-a+4b,b)\) and turns the relevant case-c edge
\[
x^{32}y^8(x^3y-t)^8
\]
into \(y^8(xy-t)^8\).

Two cautions matter:

1. Some transformations occur in a Laurent ring and the final inversion is not a
   polynomial automorphism of \(\mathbb C[x,y]\). Thus a solution of the reduced
   equation \([P,Q]=x^2\) would be a necessary skeleton, not by itself a plane
   Keller counterexample. Every normalization would have to be reversed and the
   resulting polynomial map checked globally.
2. Conversely, eliminating only a degeneration or parameter slice of the reduced
   system does not eliminate the \((72,108)\) case.

The exact finite target for a proof contribution is therefore clear: show that the
coefficient ideal generated by all \(E_{r,s}\), saturated by the required vertex
coefficients and the nonzero edge parameter(s), is the unit ideal in both branches.
No such all-parameter certificate was produced here.

## 4. July 2026 graded obstruction

Shaska proves that every plane Keller map equivariant for a nontrivial algebraic
\(\mathbb G_m\)-action on source and target is a polynomial automorphism, for every
weight signature. Source:
[arXiv:2607.20210](https://arxiv.org/abs/2607.20210), Theorem 3.3 in the v1 source.
Therefore any genuine plane counterexample, including a hypothetical
\((72,108)\) one, must be non-graded (even after polynomial changes that linearize
the actions).

This does **not** eliminate the two GGHV supports. Their required vertices span
two-dimensional polygons, so the displayed coordinates are not homogeneous for a
single nontrivial weight; hidden equivariance after unrelated polynomial
automorphisms is not established either way.

The same paper proves, for the new three-dimensional hyperbolic graded mechanism,
the quotient identity
\[
\operatorname{Jac}_{u,v}(P,Q)=\kappa\Lambda^2.
\]
The reduced GGHV equation \([P,Q]=x^2\) formally has this shape with \(\Lambda=x\).
This is a useful structural analogy, but not an obstruction: the reduced pair has
degenerate Jacobian and is a Laurent-normalized plane problem, while Shaska's plane
theorem concerns constant-Jacobian equivariant maps. A lift would additionally need
the required invariant-theoretic divisibility and weight conditions.

## 5. Reproduction

Run:

```sh
python3 route_bd_verify.py
```

The script uses only the Python standard library. It verifies support counts,
universal row and term counts, the half-plane bound, the symbolic five-row
certificate over \(\mathbb Z[t]\), and the explicit perturbation showing the
generality gap.

## Honest terminal assessment

- Exact plane counterexample: **not obtained**.
- Proof of \(JC(2)\): **not obtained**.
- Exact obstruction certificate: **obtained only for the stated one-parameter
  forced-edge degeneration**.
- Full \((72,108)\) coefficient variety: **unresolved**.
