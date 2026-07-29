# Connected binary-packing-repair countermodel

Date: **2026-07-28**

Status: **EXACT AUXILIARY COUNTERMODEL WITH DUAL-CHECKED LRAT / NOT A
FIVE-CYCLE DOUBLE COVER COUNTEREXAMPLE**.

The standard Five-Cycle Double Cover Conjecture remains open.

## The finite theorem

There is a connected simple bridgeless cubic graph \(G\) of order 108 and
a nowhere-zero \(\mathbb F_2^3\)-flow \(f\) with the following property.
For every distinct nonzero \(t,b\) and every binary cycle
\[
 X\subseteq E(G)-f^{-1}(t),
\]
the value-\(b\) matching of the switched flow \(f+t1_X\) does not pack
two edge-disjoint boundary joins.

Equivalently, all 21 Fano point--line binary-repair incidences fail.
Therefore connectedness alone does not suffice for the binary packing
repair conjecture formulated in
`scratch/fano-binary-packing-repair-frontier-20260728.md`.

The graph has exactly two cyclic 2-edge cuts.  It is not cyclically
4-edge-connected and hence lies outside the sound minimum FiveCDC
counterexample domain.  It has an explicit standard FiveCDC checked by
`verify.py`.

## Construction

Start with three copies of the 36-vertex state
`scratch/fano-binary-repair-score14-order36.txt`.  Relabel their flow
values by the three invertible linear maps whose images on the basis
\((1,2,4)\) are
\[
 (1,2,4),\qquad(3,4,6),\qquad(7,6,2).
\]

In copy/local-edge notation, make crossed cubic 2-sums on
\[
 (0,e_{18})\sim(1,e_{29}),\qquad
 (1,e_{31})\sim(2,e_{34}).
\]
The two removed edges in each sum have equal flow value, so assigning
that value to both new cross edges preserves the flow equation at all
four endpoints.

For the displayed FiveCDC of the base graph, coordinate permutations can
make the removed pair labels equal on both shores.  The new cross edges
receive that common label.  This pastes the three covers into a standard
FiveCDC of the composed graph.  `verify.py` reconstructs both pastings
edge by edge.

The labelled graph6 record and 162 flow values are frozen in
`scratch/fano-binary-repair-connected-countermodel-order108.txt`.

## Exact formula

For one incidence \((t,\{b,b+t\})\), introduce switch variables \(x_e\)
and join variables \(r_e,d_e\).  The switched target matching is
\[
 m'_e=
 \begin{cases}
 1-x_e,&f(e)=b,\\
 x_e,&f(e)=b+t,\\
 0,&\text{otherwise}.
 \end{cases}
\]
The block formula requires
\[
\begin{array}{rl}
\bigoplus_{e\ni v}x_e&=0,\\
x_e&=0\quad(f(e)=t),\\
\neg r_e\vee\neg d_e,&\\
r_e,d_e&\le 1-m'_e,\\
\bigoplus_{e\ni v}(r_e+m'_e)&=0,\\
\bigoplus_{e\ni v}(d_e+m'_e)&=0.
\end{array}
\]
These constraints say exactly that \(X\) is an even support avoiding the
value-\(t\) class and that \(r,d\) are two edge-disjoint
\(\partial M'_b\)-joins in \(G-M'_b\).

`build_formula.py` creates all 21 blocks with selectors.  Every clause of
block \(i\) is gated by \(\neg s_i\), and the final clause is
\[
                         s_1\vee\cdots\vee s_{21}.
\]
Thus the combined CNF is satisfiable exactly when at least one incidence
repairs.  It has 10,227 variables and 51,193 clauses.

CaDiCaL proves this CNF UNSAT.  Its 7.3 MB LRAT is accepted by both the C
`lrat-check` implementation and the CakeML-generated verified checker
`cake_lpr`.  The independently structured `verify.py` reconstructs the
composition, graph metadata, flow, FiveCDC, and every CNF clause before
calling both proof checkers.

## Reproduction

From this directory:

```sh
python3 build_formula.py
cadical --lrat --no-binary \
  all-21-binary-repairs.cnf all-21-binary-repairs.lrat

python3 verify.py \
  --lrat-check /path/to/drat-trim/lrat-check \
  --cake-lpr /path/to/cake_lpr
```

Expected proof-checker conclusions:

```text
c VERIFIED
s VERIFIED UNSAT
```

`verify.py` also reports:

```text
order 108
edges 162
girth 5
cyclic cuts of size 1: 0
cyclic cuts of size 2: 2
explicit standard FiveCDC: true
```

## Scope and novelty

This result closes only a proposed connected binary-repair lemma.  It
does not prove or disprove FiveCDC, and it leaves open the same lemma in
the cyclically 4-edge-connected, girth-at-least-ten minimum-counterexample
class.

The construction and formulation appear plausibly new as of the
AI-assisted search on 2026-07-28, but no priority claim is made without a
specialist literature review.  The mathematical encoding is displayed
above so that a human can check the equivalence without trusting the
search program.

## AI-use disclosure

OpenAI Codex agents using GPT-5-series models, directed by Atharva
Vaidya, formulated the auxiliary conjecture, found the base state and
composition, wrote the encoders and checkers, generated and checked the
LRAT, and drafted this account.  “Independent checker” means independent
of the discovery implementation, not independent of AI.  Human review is
required before scholarly submission.
