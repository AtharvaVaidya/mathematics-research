# The \(H=0\) endpoint need not be rescued in two root transitions

Date: **2026-07-28**

Status: **MINIMUM-ORDER EXACT NO-GO FOR THE RADIUS-TWO ENDPOINT LEMMA /
NOT A FIVECDC COUNTEREXAMPLE**.

## Claim refuted

Fix a saturated root-bad \(D_5\)-state with disjoint root labels.  Lift
an all-bad line triangle at the first root and suppose its residual is
\[
                             H=K_1+K_3=0.
\]
A **root transition** is a Kempe switch on a factor circuit containing
exactly one root.  The proposed endpoint lemma said that the initial or
final line state is rescued by at most two root transitions.

This is false.  The first failure among biconnected simple cubic graphs
has 14 vertices.

## Literal witness

The graph6 record is

```text
M??CEB@W_sE_J?F??
```

In graph6 bit order, its edges are

```text
(0,6) (0,7) (1,7) (0,8) (1,8) (7,8) (1,9)
(2,9) (6,9) (3,10) (4,10) (6,10) (2,11) (3,11)
(5,11) (2,12) (4,12) (5,12) (3,13) (4,13) (5,13).
```

The labels in this edge order are

```text
01 02 12 12 02 01 01 03 13 04 34 03 04 34 03 34 03 04 03 04 34.
```

Take roots \(r=1,s=20\), labeled \(02,34\).  All five coordinates occur.
Lift at \(r\) the line sequence
\[
                             (01,02,12).
\]
The dynamically selected circuits are
\[
\begin{aligned}
K_1=K_3&=\{1,2,3,4\},\\
K_2&=\{0,1,4,5,6,7,9,11,12,14,16,17,18,19\}.
\end{aligned}
\]
Every line state is root-bad.  Hence
\[
\begin{aligned}
H&=0,\\
Z&=\{0,2,3,5,6,7,9,11,12,14,16,17,18,19\}.
\end{aligned}
\]

An exhaustive breadth-first search over every factor component
containing exactly one root gives distance exactly three from **each**
line endpoint.  From the initial endpoint, one shortest rescue is

\[
\begin{array}{c|c|c|c}
\text{root}&\text{pair}&\text{circuit}&(q(r),q(s))\\ \hline
r&01&\{1,2,3,4\}&(12,34)\\
r&13&\{0,1,4,5,6,7,10,11,15,16\}&(23,34)\\
s&03&\{16,17,19,20\}&(23,04).
\end{array}
\]

The final \(Y_{02}\)-circuit
\[
                 \{0,1,4,5,6,7,9,11,12,14,18,20\}
\]
contains both roots.

From the final line endpoint, another shortest path uses
\[
                       03@r,\quad13@r,\quad23@s
\]
on the same three displayed circuit supports.  It reaches the same
common \(Y_{02}\)-circuit.

## Minimum-order audit

The compiled targeted audit exactly reproduces the earlier independent
Python census through order 12:

```json
{"graphs":107,"flows_mod_s5":27628,
 "saturated_bad_ordered_roots":30394,
 "hzero_loops":22197,"nonempty_support":22197,
 "radius_one":20805,"radius_two":1392,"failures":0}
```

On

```text
geng -Cq -d3 -D3 14
```

the first failure is graph 22, the witness above.  Thus order 14 is
minimum in this graph class.  The audit tests all \(12\) first and all
\(12\) second root transitions from both line endpoints.

## Reproduction

```text
c++ -O3 -std=c++20 scratch/audit_d5_hzero_root_radius2.cpp \
  -o /tmp/audit_d5_hzero_root_radius2

for n in 4 6 8 10 12; do
  /opt/homebrew/bin/geng -Cq -d3 -D3 "$n"
done | /tmp/audit_d5_hzero_root_radius2

python3 scratch/check_d5_hzero_root_radius2_no_go.py
```

The Python checker is an independently written, standard-library
literal replay.  It verifies the graph, bridgelessness, local xor
equations, line lift, complete depth-two failure from both endpoints,
and exact length-three rescues.

## Consequence

Neither complementary-star descent nor any fixed two-transition
endpoint argument can close the residual proof.  A surviving statement
must allow arbitrary transition length and use a well-founded global
potential, or prove that every closed bad rooted orbit forbids
nontrivial \(H=0\) holonomy.  The witness does not refute such an
unbounded statement.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated and implemented
the targeted audit, found and minimized the witness, extracted shortest
paths, wrote an independent checker, and drafted this note.  This is
not peer review and is not a resolution of FiveCDC.
