# The disjoint-factor mediator distance is not bounded by two

Date: **2026-07-28**

Status: **EXACT PROOF-STRATEGY NO-GO / NOT A FIVECDC
COUNTEREXAMPLE**.

## Result

The promising order-12 pattern

> two intersecting circuits of disjoint factors can have arbitrary
> cross-roots joined after at most two Kempe switches

is false.  A 40-vertex, 3-connected, bipartite cubic graph has a
Tait-derived \(D_5\)-flow and a literal disjoint-factor instance whose
minimum rescue distance is three.

This does not refute orbit-rooted transitivity: the same roots are
rescued by an explicit third switch.

## Witness

The graph has bipartition
\[
                   \{0,\ldots,19\}\ \cup\ \{20,\ldots,39\}
\]
and its complete ordered edge list is embedded in
`scratch/audit_d5_disjoint_two_switch_no_go.py`.  Its graph6 encoding is

```text
g????????????????????????????????GGGO?B?a@?A@A?EC??O_C??_?g?GO_?_g????BA???aG?C??S???E_??AG?O??CCA??SA????GW????H@?????GK???A?GC???
```

Independent graph checks give: simple, connected, cubic, bipartite,
edge-connectivity three, vertex-connectivity three, and nonplanar.

The initial edge labels use only
\[
                              01,\quad02,\quad12,
\]
so they are a Tait colouring embedded in \(D_5\).  In the fixed edge
order, take the disjoint factor pairs
\[
                              P=14,\qquad Q=23.
\]
The \(P\)-circuit is
\[
\begin{split}
A=\{&1,2,3,4,10,11,12,13,28,29,31,32,\\
    &46,47,48,50,51,53\},
\end{split}
\]
and the \(Q\)-circuit is
\[
\begin{split}
B=\{&0,2,4,5,6,7,9,11,12,14,16,17,18,19,21,23,25,26,27,28,\\
    &30,31,33,34,36,38,39,40,43,44,45,47,49,50,51,52,55,56,57,59\}.
\end{split}
\]
They meet in the nine edges
\[
                         2,4,11,12,28,31,47,50,51.
\]
Use roots \(e=29\in A\) and \(g=33\in B\).

## Exact minimum-distance certificate

The standalone checker generates every legal component switch from the
initial state, then every legal second switch.  After duplicate removal
it tests every state at distances zero, one, and two, and finds no
factor circuit containing both roots.

It then replays these three legal component switches:

1. transpose \(0,2\) on the displayed \(A\)-edge set;
2. transpose \(0,1\) on
   \[
   \{0,1,3,5,9,10,16,17,18,19,21,23,30,32,33,34,43,44,45,46,
     48,49,55,56\};
   \]
3. transpose \(0,3\) on
   \[
   \{1,2,3,4,6,8,10,11,12,14,15,17,19,20,21,22,24,26,27,28,
     31,32,40,41,42,44,46,47,48,50,51,52,58,59\}.
   \]

The resulting \(Y_{01}\)-circuit contains both roots.  Thus the minimum
distance is exactly three.

Run

```text
python3 scratch/audit_d5_disjoint_two_switch_no_go.py
```

to replay the local xor checks, exhaustive radius-two search, all three
moves, and final rooted circuit.

## Structural meaning

For disjoint \(P=01,Q=23\), the unused fifth coordinate \(4\) gives the
exact label-region decomposition
\[
\begin{array}{c|c}
({\bf1}_{Y_P},{\bf1}_{Y_Q})&\text{possible labels}\\ \hline
11&P\times Q\\
10&P\times\{4\}\\
01&Q\times\{4\}\\
00&\{P,Q\}.
\end{array}
\]
Also
\[
                           C_4=Y_P\triangle Y_Q
\]
globally, since \(C_0+\cdots+C_4=0\) edgewise.

Those identities explain why the fifth coordinate is the only possible
mediator, but they do not bound the number of component switches.
Multiple common paths and contacts with other \(P\)- and \(Q\)-components
create genuine global interlacement: the 40-vertex witness needs a third
move.

Any surviving proof of orbit-rooted transitivity therefore needs an
unbounded component-chain argument or a monotone global invariant; a
finite two-contact case split cannot suffice.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the witness by an exact
random bipartite-Tait search, minimized the logical claim to Kempe
distance three, independently replayed every radius-two state, and
drafted this note.  The graph, flow, circuits, roots, switches, and
checker are fully exposed.  This is not peer review and is not presented
as a resolution of FiveCDC.
