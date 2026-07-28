# Root-component switch radius frontier

Date: **2026-07-28**

Status: **EXACT FINITE RECONFIGURATION RESULTS / NOT A FIVECDC
RESOLUTION**.

## Question

Fix two root edges in a root-bad \(D_5\)-flow state.  A
**root-component switch** is a Kempe switch on a factor component
containing exactly one root.  How many such switches are required before
the roots share a factor component?

The exact worst distances found in the complete biconnected simple cubic
census are:

\[
\begin{array}{c|c|c|c}
\text{orders audited}&\text{graphs}&\text{root-bad starts}&
 \text{largest distance}\\ \hline
4,6,8,10&26&5732&2\\
12&81&188496&3\\
\text{order 14}&480&5\,930\,411&4\\
\text{order 16}&3\,874&223\,926\,065&5.
\end{array}
\]

For the complete order-12 census, the distance histogram is
\[
                    (0,179750,8654,92).
\]
The zero entry vanishes because only root-bad starts are counted.

Thus radius two is false first at order 12, radius three is false first
at order 14, and radius four is false first at order 16.  The separate
radius-two witness and its checker are
in:

```text
scratch/d5-two-root-component-switch-no-go.md
scratch/check_d5_two_root_component_switch_no_go.py
```

## Minimum-order radius-three no-go

The first order-14 failure has graph6 encoding

```text
M?AAD@OgPWB_E_Og?
```

In edge order

\[
\begin{split}
 &(05),(07),(09),(16),(18),(1\,13),(27),(29),(2\,10),\\
 &(38),(3\,11),(3\,12),(4\,10),(4\,11),(4\,12),\\
 &(5\,10),(5\,11),(6\,12),(6\,13),(79),(8\,13),
\end{split}
\]
the labels are

\[
\begin{split}
01,02,12,02,12,01,12,02,01,01,12,02,02,01,12,12,02,01,12,01,02.
\end{split}
\]

The roots are edges \(3=(1,6)\) and \(6=(2,7)\), labelled \(02\) and
\(12\).  Every vertex sees \(01,02,12\), so the xor equations hold
directly.  The coordinate-component profile is
\[
                             (2,2,3,0,0).
\]

An exhaustive literal breadth-first search finds no root-good state at
distances zero through three.  A shortest rescue has length four:

\[
\begin{array}{c|c|c}
\text{switch pair}&\text{component edges}&
       (q(r),q(s))\text{ after the move}\\ \hline
01&\{1,2,6,7\}&(02,02)\\
01&\{3,4,18,20\}&(12,02)\\
03&\{0,2,6,8,12,13,16,19\}&(12,23)\\
14&\{3,5,9,10,13,14,17,20\}&(24,23).
\end{array}
\]

The switched components alternate between the two roots.  In the final
state both roots lie in the \(Y_{34}\)-component

\[
       \{0,2,3,5,6,8,9,10,12,14,16,17,19,20\}.
\]

The exact restricted distance is therefore four.  Notice that the final
root labels still intersect.  A root-label relation such as
equal/intersecting/disjoint is consequently not a monotone distance
potential.

The complete audit of all 374624 root-bad starts on this graph has
histogram

\[
                   (0,288912,80320,5312,80),
\]
so 80 starts attain distance four.

## Minimum-order scope

The radius-three search exhausts every normalized \(D_5\)-state and
every unordered root-bad edge pair on all 81 biconnected simple cubic
graphs through order 12.  They all pass.  The displayed graph is graph
352 in

```text
geng -Cq -d3 -D3 14
```

and is the first failure there.  Hence 14 is the minimum order in this
graph class.

## Reproduction

```text
python3 scratch/check_d5_root_component_radius4_no_go.py

c++ -O3 -std=c++20 scratch/search_d5_root_component_radius.cpp \
  -o /tmp/search_d5_root_component_radius
```

The standard-library Python checker independently checks simplicity,
cubicity, bridgelessness, all local xor equations, the displayed
four-switch path, the final factor component, and an exhaustive literal
BFS proving shortest distance four.

## Consequence and limitation

The data rule out any proof asserting a universal radius of two or three
or four for root-component-only Kempe rescue.  They do not refute the unrestricted
rooted Kempe-orbit conjecture: both witnesses have explicit rescues.  They
also do not resolve FiveCDC.

## Minimum-order radius-four no-go and complete order-16 census

The next sharp witness has graph6 encoding

```text
O??CAA_SD@DOB_F?AgAA_
```

It has 16 vertices, 24 edges, and 35008 normalized \(D_5\)-flows.  The
initial flow again uses only \(01,02,12\), has component profile
\((3,2,3,0,0)\), and has roots \(1=(1,7)\) and \(3=(2,8)\), labelled
\(01\) and \(12\).

A literal BFS discovers 6749 states before its first root-good state and
proves that its exact root-component distance is five.  One shortest
root-label path is

\[
(01,12)\to(01,02)\to(01,23)\to(01,12)\to(01,02)\to(01,24).
\]

All five switched components contain the second root.  The explicit
components, full state, graph edge order, and final \(Y_{14}\)-rescue
component are frozen in

```text
scratch/d5-root-component-radius5-no-go.json
scratch/check_d5_root_component_radius5_no_go.py
```

The complete biconnected simple cubic census through order 14 has
maximum distance four, making order 16 minimum in that class.  This third
successive sharp witness led to the capped-ladder family below.

## Unbounded radius is now proved

The capped ladder \(L_m\) has \(2m+10\) vertices and nested two-edge cuts
whose initial label word is the length-\((m+2)\) prefix of

\[
                            01,12,02,01,12,02,\ldots.
\]

A human cut-word argument proves that any root-component rescue between
the two caps requires at least

\[
                         \left\lfloor{m+2\over3}\right\rfloor
\]

switches.  The key points are that one rooted switch transposes a prefix
or suffix of the word, while a final through-factor cannot be active on
three labels whose xor is zero.  Full construction and proof:

```text
scratch/d5-capped-ladder-delay-family.md
scratch/d5-capped-ladder-unbounded-radius-theorem.json
scratch/check_d5_capped_ladder_delay_family.py
```

Thus no universal constant root-component radius exists.  This is a
theorem about the restricted reconfiguration strategy, not a
rooted-orbit or FiveCDC counterexample.

The order-16 census was split into four deterministic `geng` index
classes.  Together they contain 3,874 graphs, 15,187,695 normalized
\(D_5\)-flows, and 223,926,065 initially root-bad state/root pairs.  Every
one is rescued by root-component switches.  The distribution of the
maximum distance of a graph is
\[
 \{0:145,\ 1:966,\ 2:2418,\ 3:325,\ 4:19,\ 5:1\}.
\]
The displayed graph is the unique order-16 graph attaining distance five
in the canonical `geng` order.

### Sound reduced-domain stratification

An exact post-audit of the same 3,874 graph rows retains 607 cyclically
4-edge-connected graphs.  Their graphwise maximum-distance histogram is
\[
                         \{1:23,\ 2:478,\ 3:100,\ 4:6\}.
\]
The six distance-four graphs all have girth four.  Using literal
shortest-cycle computation (not merely a cycle basis), the joint
girth/distance distribution is
\[
\begin{array}{c|rrrr}
&d=1&d=2&d=3&d=4\\ \hline
g=4&15&438&99&6\\
g=5&8&39&1&0\\
g=6&0&1&0&0.
\end{array}
\]
Thus the complete order-16 cyclically 4-edge-connected, girth-at-least-five
subcensus has maximum distance three.  This is a finite stratification,
not a uniform theorem.  The distinction matters because the elementary
minimum-counterexample reduction excludes cyclic cuts of size two or three
and cycles of length at most four.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated and implemented
the radius audit, found and minimized the witnesses, wrote the independent
replays, and drafted this note.  These computations are not peer reviewed.
