# An oddness-six one-boundary-five completion

Status: **COMPUTER-CERTIFIED STRUCTURAL COUNTEREXAMPLE TO A PROOF
STRATEGY / HUMAN-AUDITABLE TRANSFER ARGUMENT / POSITIVE FIVE-CDC
INSTANCE / NO CONJECTURE RESOLUTION**.

This package gives a finite simple cubic cyclically
4-edge-connected graph \(G\) of order \(100\) with all of the following
properties.

1. For two displayed independent root edges, deleting their four
   endpoints has the exact one-boundary-five Gallai--Edmonds profile.
   Its nontrivial \(D\)-component is a 93-vertex factor-critical
   five-pole \(Q\), and the other two \(D\)-components are singletons.
2. The vertex resistance of \(G\) is at least \(5\), so its oddness is
   at least \(6\).
3. An explicit perfect matching has a complementary 2-factor with
   exactly six odd circuits.  Hence \(\omega(G)=6\).
4. An explicit \(D_5\) edge labelling is a standard five-cycle double
   cover of \(G\).

Thus the last one-boundary-five branch cannot be closed by proving that
every graph in the branch has oddness at most four.  The specimen is
not a counterexample to Five-CDC; it has a directly checked cover.

## Construction

Use the Petersen-derived four-poles \(N_1,N_2\) of
Lukot'ka--Máčajová--Mazák--Škoviera, *Small snarks with large
oddness*, EJC 22 (2015), P1.51.  Join

\[
                         N_2,N_2,N_2,N_1
\]

cyclically.  The resulting source \(S\) has order \(96\).  Delete the
induced path \(4-0-5\).  Its five outside neighbours are
\(3,7,8,9,12\), and the remaining graph is the factor-critical
93-vertex pole \(Q\).

Attach the five terminals, in that order, to
\(w_0,\ldots,w_4\).  Add roots \(w_0w_1,w_2w_3\), and add

\[
\begin{aligned}
N(z_0)&=\{w_0,w_2,w_4\},\\
N(z_1)&=\{w_1,w_3,w_4\}.
\end{aligned}
\]

For the roots \(R=\{w_0w_1,w_2w_3\}\), delete
\(U=\{w_0,w_1,w_2,w_3\}\).  Taking \(A=\{w_4\}\), deletion of
\(A\) leaves \(Q,\{z_0\},\{z_1\}\), all factor-critical, and \(w_4\)
meets all three components.  This is exactly the advertised
one-boundary-five profile.

## Human resistance-transfer proof

The retained CNF encodes:

> delete at most six vertices from \(S\), then properly 3-edge-colour
> every remaining edge.

It is UNSAT.  Its LRAT is accepted by both `lrat-check` and `cake_lpr`.
Therefore the vertex resistance \(\rho_v(S)\) is at least seven.

The source and completion share \(Q\).  The source cap is the
three-vertex path \(a-v-b\); the completion cap is the displayed
seven-vertex theta outside.  Suppose deleting \(D\) from \(G\) leaves a
properly 3-edge-colourable graph.  Keep only the deleted vertices of
\(D\) that lie in \(Q\), and in the source additionally delete \(a\)
and \(b\).  The colouring on the surviving part of \(Q\) is unchanged.
The only possible surviving cap edge is the fifth boundary edge at
\(v\).  If its colour was not inherited, choose any colour unused at
its endpoint in \(Q\).  This is always possible because that endpoint
has at most two other incident edges.  Hence

\[
                         \rho_v(S)\le \rho_v(G)+2.
\]

It follows that \(\rho_v(G)\ge5\).  If a perfect matching has a
complementary 2-factor with \(k\) odd circuits,
delete one vertex from each odd circuit.  Alternately use two colours on
each surviving path or even circuit and use the third colour on every
surviving matching edge.  This is a proper 3-edge-colouring, so directly
\(\rho_v(G)\le\omega(G)\).  Moreover a cubic graph has even order, and
the parity of the sum of its 2-factor circuit lengths is the parity of
the number of odd circuits.  Hence \(\omega(G)\) is even and
\(\omega(G)\ge6\).  The displayed matching has 2-factor component sizes

```text
5, 5, 8, 9, 9, 9, 9, 10, 12, 12, 12
```

and supplies the reverse inequality.  Therefore \(\omega(G)=6\).

## Reproduction

Quick, standard-library-only semantic audit:

```sh
python3 search/one-boundary-five-oddness6-completion-20260727/verify.py
```

The complete cut audit takes roughly half a minute on the preparation
machine:

```sh
python3 search/one-boundary-five-oddness6-completion-20260727/verify.py \
  --full
```

Check the source-resistance certificate independently:

```sh
.tools/cert-checkers/drat-trim/lrat-check \
  search/one-boundary-five-oddness6-completion-20260727/source96-delete-at-most6.cnf \
  search/one-boundary-five-oddness6-completion-20260727/source96-delete-at-most6.lrat

.tools/cert-checkers/cake_lpr/cake_lpr \
  search/one-boundary-five-oddness6-completion-20260727/source96-delete-at-most6.cnf \
  search/one-boundary-five-oddness6-completion-20260727/source96-delete-at-most6.lrat
```

Check the retained SAT model in the original Five-CDC semantics:

```sh
python3 -m verifier_a check-model \
  search/one-boundary-five-oddness6-completion-20260727/graph.json \
  search/one-boundary-five-oddness6-completion-20260727/fivecdc.model
```

`verify.py` separately checks the compact edge-label cover without
importing Verifier A.

## Trust boundary and AI disclosure

The resistance transfer and Gallai--Edmonds identification are written
out above.  The finite claims have direct witnesses or deterministic
replay.  The two certificate checkers establish UNSAT of the retained
resistance CNF; they do not independently reconstruct that CNF from the
graph.  The displayed resistance encoding and its equivalence to the
source-deletion statement therefore remain in the proof trust boundary.
The explicit matching proves the upper oddness bound; the explicit edge
labels prove Five-CDC for this one graph in a separately replayed
semantics.

This construction, search, proof organization, code, and exposition were
developed with substantial assistance from OpenAI Codex under human
direction.  No bounded computation or AI-generated argument is presented
as a proof of the Five-Cycle Double Cover Conjecture.
