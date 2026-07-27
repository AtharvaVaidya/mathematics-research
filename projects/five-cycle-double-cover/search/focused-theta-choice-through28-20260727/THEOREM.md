# Human statement of the finite theorem

Let \({\cal G}_{n}\) be the graph6 stream produced by

```text
snarkhunter n 4 S s C4 o g
```

for even \(10\le n\le28\), using the frozen Snarkhunter 2.0b option
semantics documented by the retained logs.

For every \(G\in{\cal G}_{n}\) and every two vertex-disjoint edges
\(R=\{e,f\}\), set \(U=V(e)\cup V(f)\) and \(H=G-U\).  Then either:

- \(H\) has a perfect matching; or
- \(H\) has a maximum matching \(P\) missing two vertices such that
  \(G-(R\cup P)\) has no bridge.

There are 14,009 input graphs and 10,689,351 such root pairs.  The first
alternative occurs 10,567,773 times and the second 121,578 times.
There is no remaining pair.

## Why the classification has exactly these meanings

The human Tutte--Berge proof in
`../../scratch/prescribed-root-matching-deficiency-frontier.md` gives
\(\operatorname{def}(H)\le2\) for every 3-edge-connected cubic \(G\).
The order of \(H\) is even, so a failed perfect-matching test means
deficiency exactly two.

If \(P\) misses \(a,b\), every vertex of \(G-(R\cup P)\) has degree two
except \(a,b\), which have degree three.  Suppressing degree-two paths in
their component gives either three parallel \(ab\)-edges (a theta) or
one \(ab\)-edge and one loop at each endpoint (a dumbbell).  The first
case is equivalent to absence of a bridge.  It admits a nowhere-zero
\(\mathbb F_2^2\)-flow by assigning the three nonzero values to the
three theta paths; the dumbbell link is forced to zero.

Thus the classifiers use exact matching recurrences and exact bridge
tests.  They do not rely on an optimization heuristic.

## Scope

This is a finite theorem through order 28, conditional on the stated
canonical source provenance.  It neither proves the corresponding
universal perfect-or-theta alternative nor Five-CDC.
