# A local obstruction in the literal KMNS girth construction

Status: candidate gap report for human audit, 28 July 2026.

This note records a local obstruction found while trying to instantiate the
construction in Theorem 5.1 and Figures 2--4 of:

J. Karabáš, E. Máčajová, R. Nedela, and M. Škoviera, “Girth, oddness, and
colouring defect of snarks,” *Discrete Mathematics* 345 (2022), 113040,
[arXiv:2106.12205](https://arxiv.org/abs/2106.12205),
[doi:10.1016/j.disc.2022.113040](https://doi.org/10.1016/j.disc.2022.113040).

The conclusion established here is deliberately narrow:

> Under the ordinary multipole-gluing convention and the literal \(F_g\) and
> \(Z\) pieces of Figures 3--4, every identification of either pair of
> \(F_g\) connectors with a \(Z\) supervertex creates a cycle of length at
> most \(9\).

Consequently, this literal construction does not produce a graph of girth
\(10\), regardless of the order in which semiedges in those connectors are
identified. This identifies a possible gap in the displayed girth argument.
It does **not** refute the existence theorem stated as Theorem 5.3, does not
exclude a repaired superposition construction, and has no implication for
the Five-Cycle Double Cover Conjecture.

## Figure 2 transcription

The crossings in Figure 2 are not vertices. Number the displayed 6-cycle
\(v_0,\ldots,v_5\) by \(0,\ldots,5\). Number the three branch vertices of
the complementary spanning tree by \(6,7,8\), and its central vertex by
\(9\). The Petersen graph in Figure 2 has edges

```text
01 12 23 34 45 05
06 36 69
17 47 79
28 58 89
```

Thus the outer pairs joined to common branch vertices are
\(\{v_0,v_3\}\), \(\{v_1,v_4\}\), and \(\{v_2,v_5\}\).

This detail mattered computationally. An early experimental transcription
paired \(\{v_0,v_4\}\) and \(\{v_1,v_3\}\); that ten-vertex graph is not the
Petersen graph, because it contains the 4-cycle \(0,5,4,6,0\). The
experimental generator has since been corrected. The checker in this
directory reconstructs the Figure 2 edge set independently and verifies
that it is simple, cubic, connected, and of girth \(5\).

## Multipole convention

Deleting a vertex of a cubic graph retains its three incident edges as
semiedges. Joining two semiedges fuses their free ends to make one ordinary
edge; it does not insert a new 2-valent vertex.

The \((3,3,1)\)-pole \(Z\) in Figure 4 consists of:

- one vertex \(z\), with one incident semiedge in each of the three
  connectors; and
- two isolated edges, each contributing one semiedge to each size-three
  connector.

After the two size-three connectors are joined to connectors of two copies
of \(F_g\), \(z\) is adjacent to one selected terminal in each \(F_g\), and
the two isolated edges pair the two remaining terminals on one side with
the two remaining terminals on the other side. There are
\(3\cdot3\cdot2=18\) such local identifications.

## Human-checkable obstruction

Use the example specified in the proof:

\[
  \{u_i,v_i,w_i\}=\{v_0,v_2,v_4\}.
\]

Focus on \(P_1\), take \(u_1=v_0\), and substitute 5-poles for
\(v_2\) and \(v_4\). After deleting \(u_1\), the three retained endpoints
of the connector are \(v_1,v_5,\) and vertex \(6\). The following paths
avoid \(v_0,v_2,v_4\), so they survive every choice of \(M_g\) and every
permutation used to attach the 5-poles:

```text
v1 - 7 - 9 - 8 - v5       length 4
v1 - 7 - 9 - 6            length 3
v5 - 8 - 9 - 6            length 3
```

Therefore, in each \(F_g\) connector the three terminal-pair distances have
the universal upper bounds \(4,3,3\). Call the terminal opposite the
length-4 pair \(c\).

Now join one connector from each of two copies of \(F_g\) through \(Z\).

- If \(z\) is attached to \(c\) on both sides, use \(z\), either isolated
  edge of \(Z\), and the corresponding length-at-most-3 path in each
  \(F_g\). This is a cycle of length at most
  \(1+3+1+3+1=9\).
- Otherwise, on at least one side the two terminals paired through the
  isolated edges have mutual distance at most \(3\). If this happens on
  both sides, the cycle using both isolated edges has length at most
  \(3+1+3+1=8\). If it happens on exactly one side, the other side has
  mutual distance at most \(4\), giving length at most
  \(3+1+4+1=9\).

These cycles are contained in the two copies of \(F_g\) and their common
copy of \(Z\), so connections to the rest of the superposition cannot
remove them. Hence every literal Figure 4 identification has girth at most
\(9\).

The sentence on page 11 asserting that the absence of short cycles inside
each \(F_g\), together with the decycling set
\(\{v_0,v_1,v_3,v_4\}\), implies \(\operatorname{girth}(\widetilde G)\ge g\)
does not address these cycles: each one enters and leaves an \(F_g\) through
the same connector, so it does not project to a cycle of the Petersen base
graph.

## Independent check

Run:

```sh
shasum -a 256 -c SHA256SUMS
python3 check_connector_obstruction.py > result.json
python3 -m json.tool result.json >/dev/null
```

The standard-library checker:

1. reconstructs the corrected Figure 2 Petersen graph;
2. verifies simplicity, cubicity, connectedness, and girth \(5\);
3. checks the three displayed surviving paths;
4. enumerates all \(18\) possible \(Z\)-connector identifications; and
5. verifies that every case has a displayed local-cycle upper bound at
   most \(9\), with the best achievable bound equal to \(9\).

The calculation uses only path and cycle upper bounds. If an \(F_g\)
contains an even shorter terminal path, the conclusion only becomes
stronger.

## Scope and next checks

Before treating this as a correction to the literature, a human should:

1. verify that the multipole fusion convention above matches the authors’
   convention and Kochol’s cited superposition convention;
2. check whether an unstated restriction or a different \(Z\) multipole was
   intended;
3. ask the authors whether a corrected construction is known; and
4. independently verify whether Theorem 5.3 follows from another published
   construction.

No graph6 witness of girth \(10\) is supplied because the local argument
proves that the literal construction cannot produce one.

## AI-use disclosure

OpenAI Codex, using a GPT model, was used substantively in this investigation:
it inspected the paper figures and text, found and corrected the Figure 2
transcription error in the experimental generator, constructed and tested
candidate port wirings, identified the local \(Z\)-connector obstruction,
and drafted the checker and this note. The finite calculation is reproduced
by the standard-library program, and the mathematical argument above is
intended to be checkable without trusting the model. No claim of novelty or
correctness should be made without independent human review.
