# A root-universal terminal plateau with disconnected neutral hypergraphs

Date: **2026-07-28**

Status: **EXACT TERMINAL-PLATEAU NO-GO / ROOT-UNIVERSAL PLATEAU /
NOT A RESOLUTION OF FiveCDC**.

## 1. Result

There is a simple bridgeless cubic graph on 56 vertices with a terminal
surface-\(\chi\) plateau \(T\) such that:

1. \(T\) has 55,652 states modulo the global \(S_5\) action;
2. \(T\) has no \(\chi\)-increasing exit;
3. 1,041 states in \(T\) have a disconnected hypergraph of neutral
   factor components; but
4. \(T\) is root-universal: every pair of graph edges lies together on
   one factor component in at least one state of \(T\).

This refutes the proposed intermediate theorem

> every state in a terminal \(\chi\)-plateau has a connected
> neutral-component hypergraph.

It does **not** refute the terminal-plateau root-universality conjecture.
On the contrary, the complete plateau is an exact order-56 positive
instance of that conjecture.

## 2. Exact graph and starting flow

Start with the 28-vertex graph

```text
[???????????_?O?D??g?__H@?PB??c_?aA?COO?@S??Ag?AE??@H??P?_?AGO??
```

and the labels, in lexicographically sorted endpoint order,

```text
03 09 0a 03 09 0a 0c 14 18 0c 14 18 14 12
06 14 12 06 11 18 09 11 18 09 0c 18 14 0c
18 14 0a 06 0c 0a 06 0c 11 12 11 12 18 18
```

Form a two-lift with voltage one on base edges \(18,36\) and zero on
every other base edge.  Number the lift vertices \(2v+s\).  For base
edge \(e=uv\), list its two lifts consecutively:
\[
 (2u+s,\;2v+s+\sigma(e)),\qquad s=0,1,
\]
where the sheet coordinate is in \(\mathbb F_2\).  Copy the base label
to both lifted edges.  This rule is a complete, unambiguous encoding of
the labelled 56-vertex graph.

For convenience, its graph6 encoding in this vertex numbering is

```text
w??????????????????????????????????????????????_???O???C????_???AG???CO???CO???AG??A?@??GO?_?@@?@??CA?A??GA?I???@?D????OOO???AAA???A?_?O??C@?A???C@?@???A?_?_????Ga?????@CO?????CP??????Ga????G?g?????C?S?????@@@??????GGG????_G?A????@?O?C????@?O@??????_G?_?????
```

The checker independently verifies simplicity, cubicity,
connectedness, bridgelessness, and all five flow-parity equations.

## 3. The local maximum and its exact ascent

The copied lifted flow \(q_{-10}\) has \(\chi=-10\).  Its 48 nonempty
factor-component switches have delta histogram
\[
                 \{-3:2,\ -2:24,\ -1:2,\ 0:20\}.
\]
Thus it is a one-move local maximum.  Its neutral-component hypergraph
has eight classes.  It is not in a terminal plateau.

There is a literal two-switch ascent, both times using pair \(34\):

| step | component edge indices | \(\Delta\chi\) |
|---:|:---|---:|
| 1 | 12,14,18,20,24,26,30,32,48,52,54,58 | 0 |
| 2 | 13,15,19,21,25,27,31,33,49,53,55,59 | \(+2\) |

The first switch stays at \(-10\); in that new state the second
displayed set is a factor component and raises \(\chi\) to \(-8\).
This explicitly records the semantic distinction between a one-move
local maximum and a terminal plateau.

## 4. Exhaustive terminal-plateau certificate

Starting at the resulting \(\chi=-8\) state, the standalone C++ auditor:

1. enumerates every nonempty component of all ten factors;
2. computes every switch by literal coordinate transposition;
3. recomputes \(\chi\) from the five coordinate-circuit counts;
4. traverses every equal-\(\chi\) neighbour;
5. quotients only by the global \(S_5\) action;
6. stops with failure if any state has a positive switch; and
7. records root-pair coverage and neutral-component connectivity.

The exhaustive result is

| quantity | exact value |
|:---|---:|
| plateau \(\chi\) | \(-8\) |
| states modulo \(S_5\) | 55,652 |
| directed neutral switches | 1,022,160 |
| states with disconnected neutral hypergraph | 1,041 |
| uncovered unordered root-edge pairs | **0** |
| positive exits | **0** |

Because every equal-\(\chi\) state was exhausted and no positive exit
exists, this is a terminal plateau, not merely a collection of local
maxima.  “Uncovered root pairs \(=0\)” is exactly root-universality:
for each of the \(\binom{84}{2}=3486\) unordered edge pairs, some
plateau state has one factor circuit containing both edges.

## 5. A literal disconnected state

The frozen report includes the first disconnected state found.  It has
\(\chi=-8\), 34 nonempty switches, and delta histogram
\[
                         \{-3:2,-2:13,-1:1,0:18\}.
\]
Thus it is itself a local maximum.  Its 18 neutral factor components
induce exactly two edge classes:
\[
                         \{75\},\qquad E(G)\setminus\{75\}.
\]
The full 84-label state is in the machine-readable report.  A separate
standard-library Python checker recomputes this state directly and
verifies the graph, flow, every switch delta, and the two neutral
classes without importing project code.

## 6. Reproduction

```text
clang++ -std=c++17 -O3 -DNDEBUG \
  scratch/audit_d5_lift56_equal_chi_plateau.cpp \
  -o /tmp/audit_d5_lift56_equal_chi_plateau

/tmp/audit_d5_lift56_equal_chi_plateau \
  > scratch/d5-lift56-terminal-plateau-report.txt

python3 scratch/check_d5_lift56_disconnected_plateau_state.py
```

Files:

```text
scratch/audit_d5_lift56_equal_chi_plateau.cpp
scratch/d5-lift56-terminal-plateau-report.txt
scratch/check_d5_lift56_disconnected_plateau_state.py
```

The C++ producer is standalone.  The Python checker is independently
written and standard-library only.

Frozen SHA-256 digests:

```text
2f99283cda381b644ae071d61722c3f558ee2c0beba24ae03f88f86895daa3db  scratch/audit_d5_lift56_equal_chi_plateau.cpp
4d1c065f3b51dfb99e1592c30d0fd2f7e12f78a9f04619a9c26dd51f83f3d6ff  scratch/d5-lift56-terminal-plateau-report.txt
6de06c4c49d43a43e3f5056550200faf5ba1832425102c7ee5dac6c55ac1c091  scratch/check_d5_lift56_disconnected_plateau_state.py
```

## 7. Consequence for the proof program

Neutral-component connectivity is not a valid invariant of terminal
plateaus.  Nor can terminal-plateau root-universality be proved by
showing that each adjacent graph-edge pair has a neutral component:
the smaller 28-vertex cover already refutes that local statement.

The surviving fact is genuinely plateau-global.  Neutral moves may
pass through states with disconnected neutral hypergraphs and still
reconfigure the plateau so that every root pair becomes factor-connected.
A proof must therefore track the evolution of factor chains across the
plateau, or use a different \(\chi\)-free reconfiguration argument.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the lift search,
found the voltage assignment, distinguished local maxima from terminal
plateaus, implemented and ran the exhaustive \(S_5\)-quotiented plateau
audit, independently checked the literal disconnected state, and drafted
this note.  These are machine-assisted finite theorems with fully
specified code and witnesses, not peer review and not a resolution of
FiveCDC.
