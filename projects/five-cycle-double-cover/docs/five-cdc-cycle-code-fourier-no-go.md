# The four-cycle code and its exact Fourier expansion

Status: **EXACT REFORMULATION / HUMAN FOURIER IDENTITY / BINARY AND
COGRAPHIC GENERALIZATION REFUTED**.

This note gives the exact signed expansion for the most compact cycle-code
form of standard Five-CDC.  Positivity on bridgeless graphic cycle spaces
is exactly the original conjecture, so the expansion is not itself a
resolution.  Two small human-checkable countermodels show that positivity
does not extend to arbitrary coloopless binary or cographic codes.

## 1. Four cycles suffice

Let \(Z(G)\subseteq\mathbb F_2^{E(G)}\) be the binary cycle space and put

\[
 A=\{x\in\mathbb F_2^4:\operatorname{wt}(x)\in\{1,2\}\}.
\]

Four cycles \(C_1,\ldots,C_4\) give each edge the column

\[
 x_e=(1_{C_1}(e),\ldots,1_{C_4}(e)).
\]

If \(x_e\in A\) for every edge, define

\[
 C_5=C_1\triangle C_2\triangle C_3\triangle C_4.
\]

An edge of column weight one lies in \(C_5\), while an edge of weight two
does not.  It is therefore covered exactly twice.  Conversely, deleting
the fifth coordinate from a standard five-cover leaves column weight one
or two.  Thus

> \(G\) has a standard five-cycle double cover if and only if it has an
> \(A\)-valued \(\mathbb F_2^4\)-flow.

## 2. Fourier transform of the allowed set

For \(t\in\mathbb F_2^4\), use the unnormalised transform

\[
 \widehat{1_A}(t)=\sum_{a\in A}(-1)^{t\cdot a}.
\]

It depends only on \(k=\operatorname{wt}(t)\).  The weight-one and
weight-two Krawtchouk sums give

\[
\begin{array}{c|rrrrr}
k&0&1&2&3&4\\ \hline
\widehat{1_A}(t)&10&2&-2&-2&2.
\end{array}                                             \tag{1}
\]

Define the quadratic form

\[
 Q(t)=\sum_{1\le i<j\le4}t_it_j.
\]

Because \(Q(t)=\binom{k}{2}\pmod2\), equation (1) is equivalently

\[
 \widehat{1_A}(t)=
 \begin{cases}
 10,&t=0,\\
 2(-1)^{Q(t)},&t\ne0.
 \end{cases}                                            \tag{2}
\]

## 3. Exact graphic expansion

Let \(G\) have \(n\) vertices, \(m\) edges, and \(c\) connected components.
Fix one root in every component.  For a vertex potential
\(p:V(G)\to\mathbb F_2^4\) which is zero at those roots, put

\[
 z(p)=|\{uv\in E(G):p_u=p_v\}|
\]

and

\[
 q(p)=\sum_{uv\in E(G)}Q(p_u+p_v)\pmod2.
\]

Character orthogonality at every vertex gives the exact number \(N_A(G)\)
of ordered four-cycle witnesses:

\[
\boxed{
 N_A(G)=
 2^{\,m-4(n-c)}
 \sum_{\substack{p:V(G)\to\mathbb F_2^4\\p(\text{roots})=0}}
 5^{z(p)}(-1)^{q(p)}.
}                                                       \tag{3}
\]

Indeed, before fixing roots the orthogonality factor is \(16^{-n}\), and
each edge contributes
\(\widehat{1_A}(p_u+p_v)\).  Constant translation on each component
contributes \(16^c\).  Substituting (2) yields (3).  Loops cause no
exception: their potential difference is zero and their factor is ten.

For a bridgeless graph,

\[
N_A(G)>0
\]

is exactly standard Five-CDC.  Therefore a proof that the signed sum in
(3) is always positive under precisely the bridgeless graphic hypotheses
would resolve the conjecture; it cannot be treated as an already easier
analytic inequality.

## 4. Seven-coordinate binary countermodel

Let \(C\) be the binary simplex code

\[
 C=\{(a\cdot x)_{x\in\mathbb F_2^3-\{0\}}:
 a\in\mathbb F_2^3\}.
\]

Every one of its seven coordinates is nonzero on some codeword, so this
code has no zero coordinate, the direct code analogue of having no bridge.
Suppose four codewords had every column in \(A\).  They define a linear map

\[
 L:\mathbb F_2^3\longrightarrow\mathbb F_2^4
\]

with \(L(x)\in A\) for every \(x\ne0\).  Since \(0\notin A\), the map is
injective.  Its image is a three-dimensional hyperplane
\(W\le\mathbb F_2^4\) with \(W-\{0\}\subseteq A\).

No such hyperplane exists.  Write it as

\[
 W=\{x:h\cdot x=0\},\qquad h\ne0.
\]

If \(\operatorname{wt}(h)=1\), \(W\) contains the weight-three vector on
the other coordinates.  If the weight is two, take both support
coordinates and one outside coordinate.  If it is three, take two support
coordinates and the outside coordinate.  If it is four, \(W\) contains
\(1111\).  In every case \(W\) contains a vector of weight three or four,
contrary to \(W-\{0\}\subseteq A\).

Thus the natural assertion for arbitrary binary coloopless codes is false
already at length seven.

## 5. Cographic countermodel from \(K_6\)

Take the cut space of \(K_6\), equivalently the cycle code of the
cographic matroid \(M^*(K_6)\).  Four cuts assign a label
\(p_v\in\mathbb F_2^4\) to every vertex, and the column on \(uv\) is
\(p_u+p_v\).  An \(A\)-valued witness would therefore give six points of
\(\mathbb F_2^4\) whose pairwise Hamming distances are one or two.

There are at most five such points.  Translate one point to zero.  The
others are one- or two-subsets of \([4]\), and their pairwise symmetric
differences have size at most two.  The two-subsets form an intersecting
family.  With no two-subsets there are at most four singletons.  With one
two-subset, all singletons lie in it.  With at least two two-subsets, they
form a star or a triangle; a star allows only its common singleton and a
triangle allows none.  In every case there are at most four nonzero
points, hence at most five after restoring zero.

So the cographic cut code of the loopless bridgeless graph \(K_6\) has no
four-codeword witness.  This is not a Five-CDC counterexample: the
ordinary graphic cycle space of \(K_6\) is a different code.  It shows
that any positivity proof for (3) must use genuinely graphic structure
and cannot follow from binary or cographic colooplessness alone.

## Executable audit

Run

```sh
python3 scratch/check_cycle_code_fourier_no_go.py
```

The checker recomputes (1), exhausts all linear maps for the simplex code,
and independently finds clique number five in the sixteen-vertex Cayley
graph used in the \(K_6\) argument.

## AI disclosure

The expansion and countermodel search were developed with substantial
assistance from OpenAI Codex agents under human direction.  All proofs
above are self-contained, and the executable audit is supplementary.
