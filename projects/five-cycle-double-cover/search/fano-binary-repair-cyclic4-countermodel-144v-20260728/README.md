# Cyclically-4 binary-repair auxiliary countermodel

Date: 2026-07-28

Status: exact finite auxiliary countermodel with 29 dual-checked LRAT
proofs and an explicit standard Five-Cycle Double Cover.

This package does **not** resolve the Five-Cycle Double Cover Conjecture.
It also does not settle the girth-at-least-10 binary-repair branch. The
host below has girth 5.

## Finite result

`countermodel-order144.txt` contains a labelled graph6 record and a
216-entry nowhere-zero \(\mathbb F_2^3\)-flow \(f\) on its edges in
graph6 order. The graph \(G\) is:

- simple, cubic, connected, and bridgeless;
- order 144 and size 216;
- nonplanar (the `planarg` transcript is retained);
- girth 5;
- cyclically 4-edge-connected: exhaustive deletion of every set of one,
  two, or three edges finds no separation with a cycle on both shores;
- not 3-edge-colourable, certified by `tait-coloring.cnf` and LRAT.

Its seven flow-class sizes are
\[
                  33,\ 31,\ 31,\ 33,\ 34,\ 26,\ 28.
\]
All seven value classes fail to pack two disjoint boundary joins.
Moreover, all 21 normalized point-line binary-cycle-repair incidences
fail.

This refutes the **cyclically-4-only** binary packing repair auxiliary
statement. It does not refute the version restricted additionally to
girth at least 10.

## Exact meanings of the formulas

At a cubic vertex, a nowhere-zero \(\mathbb F_2^3\)-flow has three
distinct incident values. Therefore every value class \(M_a=f^{-1}(a)\)
is a matching.

For a fixed value class \(M_a\), the variables \(r_e,d_e\) in
`packing-value-a.cnf` require:

\[
\begin{aligned}
 r_e=d_e&=0 &&(e\in M_a),\\
 \neg r_e\lor\neg d_e&&&(e\notin M_a),\\
 \bigoplus_{e\ni v}r_e
 &=|\delta(v)\cap M_a|\pmod2,\\
 \bigoplus_{e\ni v}d_e
 &=|\delta(v)\cap M_a|\pmod2.
\end{aligned}
\]

Thus a satisfying assignment is exactly two edge-disjoint
\(\partial M_a\)-joins in \(G-M_a\). Conversely, any such pair gives a
satisfying assignment.

For a normalized incidence \((t,b)\), where \(b<b\mathbin\oplus t\),
`repair-tT-bB.cnf` adds switch variables \(x_e\). They require

\[
\begin{aligned}
 \bigoplus_{e\ni v}x_e&=0,&
 x_e&=0\quad(f(e)=t).
\end{aligned}
\]

Hence \(X=\{e:x_e=1\}\) is an arbitrary binary cycle in \(G-M_t\).
After switching, \(f'(e)=f(e)\oplus t x_e\). Its value-\(b\) matching
has indicator

\[
m'_e=
\begin{cases}
1-x_e,&f(e)=b,\\
x_e,&f(e)=b\oplus t,\\
0,&\text{otherwise}.
\end{cases}
\]

The remaining clauses require \(r,d\subseteq G-M'_b\), require them to
be edge-disjoint, and impose
\(\partial r=\partial M'_b=\partial d\). Therefore this CNF is
satisfiable exactly when the named binary-cycle repair exists.

Every XOR above is translated to the complete set of clauses forbidding
assignments of the wrong parity. `verify.py` reconstructs every clause
from these displayed semantics without importing `build_formula.py`.

The 42 ordered choices \((t,b)\), \(b\ne t\), reduce to the 21 retained
representatives. For a paired target \(b\oplus t\), choose a nonzero
linear functional \(\lambda\) with
\(\lambda(t)=0,\lambda(b)=1\). The edge set
\(S=\{e:\lambda(f(e))=1\}\) is an even set avoiding \(M_t\), and
\[
 M_b(f+t1_X)=M_{b\oplus t}(f+t1_{X\mathbin\triangle S}).
\]
Thus \(X\mapsto X\mathbin\triangle S\) is a bijection preserving the
literal target matching and its packing status.

## Certificate inventory

`cnf/` contains:

- 7 individual initial-packing CNFs;
- 21 individual normalized binary-repair CNFs;
- 1 Tait-colouring CNF.

`lrat/` contains one LRAT per CNF. CaDiCaL 3.0.1 generated the proofs.
Every LRAT is accepted independently by:

- the C `lrat-check` program from `drat-trim`; and
- the CakeML-generated verified checker `cake_lpr`.

`proof-manifest.json` records every proof hash and conclusion. The 29
proofs total about 2.82 MB.

`verify_graph_flow.cpp` independently decodes the frozen state, checks
the flow, computes girth, and exhausts every edge deletion set of sizes
1 through 3.

## Explicit Five-Cycle Double Cover

`fivecdc.witness` lists five Eulerian edge subsets with sizes
\[
                       93,\ 96,\ 69,\ 84,\ 90.
\]
`verify_fivecdc.py` checks directly that every vertex has even degree in
each subset and that every one of the 216 edges occurs in exactly two
subsets. This is a short, positive, human-checkable certificate.

Consequently this graph is definitively **not** a counterexample to the
standard Five-Cycle Double Cover Conjecture.

## Reproduction

With the checker paths used in this workspace:

```sh
python3 build_formula.py
python3 prove_all.py --jobs 4

c++ -O3 -std=c++17 verify_graph_flow.cpp -o verify_graph_flow
./verify_graph_flow countermodel-order144.txt

python3 verify.py
python3 verify_fivecdc.py fivecdc.witness countermodel-order144.txt

planarg -u countermodel-order144.g6 /dev/null
shasum -a 256 -c SHA256SUMS
```

`flatten_state.py` is retained only to document the discovery handoff
from `/tmp`; the already flattened `countermodel-order144.txt` is the
self-contained source of truth for verification.

## Scope and publication warning

The result is a finite counterexample to an auxiliary repair strategy,
not to FiveCDC. The graph's girth is 5, so claims about the
girth-at-least-10/minimal-counterexample regime remain open. Novelty has
not been established by specialist literature review. Do not make a
priority or conjecture-resolution claim from this package without
independent human review.

## AI-use disclosure

OpenAI Codex agents using GPT-5-series models, directed by Atharva
Vaidya, performed the search, wrote the encoders and checkers, generated
and checked the LRAT proofs, extracted the FiveCDC witness, and drafted
this account. “Independent checker” here means independent of the
discovery implementation; it does not mean independent of AI. Human
mathematical and software review is required before submission.
