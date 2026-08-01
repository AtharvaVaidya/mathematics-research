# Exact minimum-projection audit of the 130-vertex exchange graph

Status: **CERTIFIED FINITE RESULT / NOT A FIVE-CDC RESOLUTION**.

For the retained 130-vertex simple bridgeless cubic graph,

1. the minimum size of an extendable binary projection is exactly \(42\);
2. there are exactly 11,264 minimum projection supports \(h\); and
3. every one of those 11,264 supports is cleanable.

Thus this graph refutes the separate minimum-*value-class* packing route,
but it does **not** refute the minimum-extendable-projection conjecture.
In fact it passes the stronger, graph-specific test that every minimum
projection is cleanable.

## Definitions and exact encoding

Write an \(\mathbb F_2^3\)-flow as

\[
                 f=(h,p,q).
\]

Here \(h,p,q\) are binary cycles.  The binary cycle \(h\) is extendable
exactly when

\[
                 E-h\subseteq p\cup q,
\]

because this says that no edge receives the zero three-bit value.
`projection-at-most-41.cnf` uses three variables per edge, the three
vertex-parity equations, the nowhere-zero clause \(h_e\lor p_e\lor q_e\),
and a forward sequential counter for \(|h|\le41\).

Its LRAT proof is independently accepted by both the C `lrat-check`
program and the verified CakeML `cake_lpr` checker.  Therefore no
extendable projection has fewer than 42 edges.

`minimum-clean-witnesses.json` contains 11,264 triples of 195-bit
hexadecimal masks \((h,p,q)\).  The independent verifier checks directly
that every retained \(h\) has 42 edges, all three masks have even degree
at every vertex, \(E-h\subseteq p\cup q\), and

\[
  |\delta(W)\cap p\cap q|\equiv0\pmod2
\]

for every component \(W\) of \(G-h\).  This last condition is precisely
cleanliness.

To certify completeness, `minimum-projections-exhausted.cnf` starts with
the same full formula at bound 42 and adds one blocking clause for each
retained support \(h\).  Its independently checked LRAT proof is UNSAT.
Consequently there is no omitted minimum projection.  The canonical
SHA-256 of the sorted 11,264 projection masks is

```text
045e75af5313a246d03d2a606cb7da4eb2bd9be4a418dd05a75e7d1b4aaa8f04
```

## The crucial parameter distinction

Let \(\rho_3(G)\) be the minimum size of one designated nonzero value
class over all nowhere-zero \(\mathbb F_2^3\)-flows.  This is not the
minimum size of a coordinate projection.

For this graph,

\[
                         \rho_3(G)=5,\qquad
       \min\{|h|:h\text{ is extendable}\}=42.
\]

`rho3-five-witness.json` gives a nowhere-zero flow whose designated value
class is

\[
                         \{48,95,97,98,148\}.
\]

The verifier checks this witness directly.  The lower bound
\(\rho_3(G)\ge5\) follows from the already retained and independently
checked proof that every \(\mathbb F_2^2\)-flow has at least five zero
edges: quotienting a Fano flow by the line spanned by the designated
value makes exactly that class zero.

The earlier package proves that the minimum packing-certificate parameter
is \(\eta(G)=6\).  Hence no value class of size five packs two disjoint
boundary \(T\)-joins.  This graph therefore refutes the unrestricted
claim that *some globally minimum Fano value class packs*.  It does not
conflict with the minimum-projection conjecture because a clean minimum
projection has four affine classes whose total size is 42; none of those
classes is required to attain the unrelated global minimum \(\rho_3=5\).

## Reproduction

The direct verifier requires only Python plus the two retained proof
checkers:

```sh
python3 verify.py
```

Set `FIVECDC_TOOLS` to the directory containing `cert-checkers/` if the
checkers are not under a discovered repository or project `.tools`
directory:

```sh
FIVECDC_TOOLS=/absolute/path/to/.tools python3 verify.py
```

Regeneration additionally needs `pycryptosat` and CaDiCaL:

```sh
python3 build.py --prove
python3 verify.py
```

## Scope and AI disclosure

This is an exact finite theorem about one graph.  It neither proves nor
disproves the Five-Cycle Double Cover Conjecture.

The encoding, search, certificate generation, verification code, and
documentation were produced with substantial assistance from OpenAI
Codex agents under human direction.  The claims do not require trust in
an AI system: the graph and positive witnesses are explicit, both CNFs
are regenerated independently, and both UNSAT conclusions have
independently checked LRAT certificates.
