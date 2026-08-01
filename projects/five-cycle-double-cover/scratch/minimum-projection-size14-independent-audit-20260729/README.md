# Independent audit of the size-fourteen clean-or-delete countermodel

Independent verification package.

Date: 2026-07-29

Status: **exact finite countermodel and simple cubic realization; not a
counterexample to the five-cycle double cover conjecture**.

This package was written independently of the primary search and checker.  It
uses only the Python standard library and hard-codes only the proposed
countermodel and graph.  It therefore checks the mathematical claim by a
second implementation, rather than importing the search code or its output.

## 1. Abstract countermodel

Let \(K=\mathbb F_2^2=\{0,1,2,3\}\), with addition represented by bitwise
xor.  Take two cyclic words and a partition of their fourteen positions:

```text
word       0101023|0101232
partition  01234444413024
```

Both words are proper (cyclic neighbours differ) and use every element of
\(K\).  If \(d_i=c_{i-1}+c_i\) on each circuit, then

```text
d          3111121|2111311
```

and the xor of the \(d_i\) in every one of the five partition blocks is
zero.  The original word has component defect vector
\((1,0,1,0,0)\), so it is dirty.

For each block \(W\), allow an arbitrary linear automorphism
\(L_W\in\operatorname{GL}(2,2)\), replace each \(d_i\) by
\(L_{W(i)}(d_i)\), and require the transformed differences to integrate
around both circuits.  Finally allow an independent translation of either
integrated circuit.  The clean-or-delete assertion would say that some such
choice either makes all five component defects zero or makes an integrated
circuit omit a colour, permitting that circuit to be deleted.

The displayed state violates this assertion.

### Human-scale proof

Common postcomposition lets us fix \(L_0\) to the identity.  Put

\[
u_i=L_i(1)\ (i=1,2,3),\qquad a=L_4(1),\qquad b=L_4(2).
\]

All five quantities are nonzero and \(a\ne b\).  The two circuit-closure
equations reduce to the single condition

\[
b=3+u_1+u_2+u_3. \tag{1}
\]

There are consequently only forty effective choices.  For every one, the
two zero-start integrated walks are

\[
\begin{aligned}
A={}&[3,3+u_1,3+u_1+u_2,b,a+b,a,0],\\
B={}&[b,a+b,3+u_2+u_3+a,3+u_2+a,u_2+a,a,0].
\end{aligned} \tag{2}
\]

Each walk contains \(\{0,a,b,a+b\}=K\); translation cannot make either
walk omit a colour.  Deletion is therefore impossible.

Let \(z\in K\) be the relative translation between the circuits.  Cleanliness
on the four size-two blocks forces \(z\) to lie simultaneously on

\[
\begin{array}{c|c}
W&\text{required affine line}\\ \hline
0&u_2+a+\{0,3\}\\
1&3+a+b+\{0,u_1\}\\
2&3+u_1+u_2+a+\{0,u_2\}\\
3&u_1+u_3+a+\{0,u_3\}.
\end{array} \tag{3}
\]

Write the first condition as \(z=u_2+a+\varepsilon3\).
If \(\varepsilon=1\), the block-2 condition forces \(u_1=u_2\), and block
3 forces \(u_3=3\); then (1) gives \(b=0\), a contradiction.  If
\(\varepsilon=0\), blocks 1 and 3 force \(u_3=u_1\) and \(u_2=u_1\);
block 2 then forces \(u_1=3\), and (1) again gives \(b=0\).  Thus no clean
translation exists.

`verify_abstract.py` independently expands all \(6^5\) map assignments.
It finds 1,920 feasible assignments, or 320 after fixing \(L_0\).  It then
checks all four relative translations, obtains zero clean cases and zero
deletion cases, and prints a complete forty-state reduction grouped into ten
four-element defect cosets.  No coset contains the zero defect.

The separately frozen exact frontier through size thirteen establishes
sharpness within this abstract boundary model: no smaller state survives the
same clean-or-delete alternatives.  That frontier is not reimplemented in
this small audit package.

## 2. Simple bridgeless cubic realization

The realization has vertices \(0,\ldots,17\).  Its two distinguished
7-circuits are

```text
0-1-2-3-4-5-6-0
7-8-9-10-11-12-13-7
```

The remaining edges are

```text
0-11  1-9  2-12  3-10
4-14  5-14  6-15  13-16  8-17  7-17
14-15  15-16  16-17
```

Its canonical graph6 string is

```text
Qs???SC@GS@_CDOoC@@@?O?CO?g
```

`verify_realization.py` directly checks simplicity, connectedness,
cubicity, and connectedness after deleting each edge.  The latter proves
bridgelessness.  It also verifies an explicit nowhere-zero
\(\mathbb F_2^3\)-flow extending the fourteen-edge projection.

The graph is nonplanar: the following nine internally disjoint paths form a
subdivision of \(K_{3,3}\), with branch bipartition
\(\{2,10,16\}\mid\{3,9,12\}\):

```text
2-3              2-1-9          2-12
10-3             10-9           10-11-12
16-15-14-4-3     16-17-8-9      16-13-12
```

The verifier constructs the graph's 10-dimensional binary cycle space,
containing 1,024 cycles.  From every ordered pair \(p,q\) of cycles it forms
the semantic low-flow state \((p\cup q,p\cap q)\), deduplicating to 384,064
states.  For the distinguished projection it finds exactly 15,360 ordered
extensions and no clean extension.

This does **not** disprove FiveCDC or the minimum-extendable-projection
conjecture.  Exhaustive enumeration finds that the graph's global minimum
extendable-projection size is five.  There are four such supports, with
decimal bit masks

```text
50689 83971 164358 199684
```

and every one is cleanable.  The size-fourteen projection is not minimum.
The countermodel instead proves that any surviving proof by minimum
projection must use global minimality more strongly than the local facts
that each circuit uses all four colours and every component has zero charge.

## 3. Reproduction

From this directory:

```sh
python3 verify_abstract.py
python3 verify_realization.py
shasum -a 256 -c SHA256SUMS
```

Both programs are deterministic and dependency-free.

## Scope and AI disclosure

OpenAI Codex agents, directed by a human researcher, found the proposed
state, derived the algebraic proof, constructed the graph realization, wrote
the checkers, and prepared this audit.  The scripts exhaust the finite
claims stated above, and the short proof is intended to be checked without
trusting the programs.  No claim of priority over unpublished work or of a
resolution of the five-cycle double cover conjecture is made.
