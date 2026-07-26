# Order-80 vertex-transitive control for the stable-eight branch

Date: **2026-07-26**.

Status: **exact scoped finite result / no five-CDC conclusion**.

This note eliminates the 33 cubic vertex-transitive graphs of order 80
in the Potočnik--Spiga--Verret census from the equality case of the
stable-eight marked-core reduction.  It does not enumerate arbitrary
order-80 cubic graphs.

The reproducible artifacts are:

- `scratch/check_order80_cvt_marked_girth.py`;
- `scratch/order80-cvt-stable8-marked-girth-result.json`;
- `scratch/tait_all_coloring_mark_separation.cpp`.

## 1. Necessary marked-girth condition

Let \(H\) be an order-80 cubic core and let \(S\) be the eight-edge
matching of suppression marks.  Subdividing every edge of \(S\) once
changes a simple cycle \(C\) from length \(|C|\) to
\[
                 |C|+|C\cap S|.
\]
Thus marked-subdivision girth at least ten requires
\[
                 |C\cap S|\ge 10-|C|                 \tag{1}
\]
for every cycle of length below ten.

If \(H\) has girth at most six, a shortest cycle contains at most
\(\lfloor |C|/2\rfloor\) edges of the matching.  Its subdivided length
is consequently at most nine.  Such a graph is impossible.

For each remaining girth-eight census graph, enumerate its eight-cycles.
Summing (1) over them requires two marked-edge incidences per cycle.
On the other hand, count for every edge how many of those cycles use
it.  Even if the matching condition is discarded, eight selected edges
can contribute at most the sum of the eight largest incidence counts.
The exact contradictions are:

| Census index | Eight-cycles | Required incidences | Best eight-edge capacity |
|---:|---:|---:|---:|
| 3 | 40 | 80 | 32 |
| 4 | 40 | 80 | 32 |
| 20 | 10 | 20 | 8 |
| 21 | 10 | 20 | 8 |
| 28 | 20 | 40 | 16 |
| 32 | 80 | 160 | 48 |
| 33 | 40 | 80 | 32 |

This is a direct integer-counting certificate.  A separate binary MILP
with the matching and every constraint (1) gives the same seven
infeasibility results.

The cycle enumerator was compared exactly with NetworkX
`simple_cycles` on all 994 connected simple graphs in the Graph Atlas.

## 2. The sole surviving census graph

Only census graph 30 has ordinary girth ten, so every eight-edge
matching automatically passes the marked-girth condition.  The input
is census line 425, with sparse6 encoding

```text
:~?@O_GA?_WEA_wIB`GUC`WYFaGeE`waHagmKbWiJbGuMbxAPchMSdWyNcHEQcxQTd`w^dpyWHHceeaaZIAe[GHsidaEVIx_aGxcbeaUZHxolfQolfqAaHYOfhae`IikkjrAqLZOvOjWxkRh?mrq}N{DBpCVFQ[hJrCtM
```

Direct checks give 80 vertices, 120 edges, connectedness, simplicity,
cubic degree, and girth ten.  Exhaustive Tait-colouring enumeration
then gives
\[
     426\,256
\]
proper three-edge-colourings modulo global \(S_3\) colour permutation.
Across all of them, the exact mark-profile search finds no universally
separated eight-edge matching; it in fact finds none of size seven.

Exactly 20 normalized colourings have at least two bichromatic factors
consisting entirely of 10-cycles, and the same 20 have all three factors
of that form.  Thus the failure is not explained merely by absence of the
factor profile forced at equality: even those highly structured
colourings do not support a universally separated eight-mark set.

Therefore none of the 33 order-80 vertex-transitive census graphs can
be the core in the equality case of the stable-eight reduction.

## 3. Reproduction

The census conversion is at
<https://github.com/kguo-sagecode/cubic-vertextransitive-graphs>,
commit
`68c592d4790ab1737f04d86d3102c4999bbc6c09`.
The census file SHA-256 is
`4bac89beec1465265318266117c38a2c1680e73a21efd322411207cef5313088`.

Run the marked-girth filter:

```sh
python3 scratch/check_order80_cvt_marked_girth.py \
  tmp/cubic-vertextransitive-graphs/cubicvt4-300g6.txt
```

Convert census line 425 from sparse6 to graph6 and pipe it to the exact
Tait search:

```sh
python3 -c 'import networkx as nx; s=open(
 "tmp/cubic-vertextransitive-graphs/cubicvt4-300g6.txt"
 ).read().splitlines()[424]; g=nx.from_sparse6_bytes(s.encode());
 print(nx.to_graph6_bytes(g,header=False).decode().strip())' |
scratch/tait_all_coloring_mark_separation --target 8 --limit 1 \
  --report-ten-factor-profiles
```

The terminal result is:

```text
FINAL rows=1 tait=1 colourings=426256 witnesses=0 target=8 \
colourings_with_at_least_two_C10_factors=20 \
colourings_with_three_C10_factors=20
```

## 4. Scope

Vertex-transitivity is not a proved property of a minimum counterexample.
Accordingly, this result is a finite control on a natural highly
symmetric family, not a reduction theorem and not evidence that all
order-80 cores have been eliminated.

## AI-use disclosure

The code, computation, and exposition were produced by an OpenAI Codex
agent under human direction.  The counting contradiction is displayed
explicitly, the cycle enumeration has an independent library
cross-check, and exact input encodings and hashes are retained.  No
claim of a five-cycle double cover resolution or human peer review is
made.
