# A two-lift counterexample to the local minimum-boundary lemma

Date: **2026-07-28**

Status: **HUMAN TWO-LIFT CONSTRUCTION / EXACT CHECKER / NOT A
COUNTEREXAMPLE TO FiveCDC**.

## 1. Statement refuted

For the three factor components through two adjacent edges, it is false
that
\[
                   \min_P |B(P,K_P)|\leq2
\]
always holds.  A connected two-lift gives an order-20 example in which
all three boundary sets have size four.

## 2. The order-10 base

Use the graph

```text
I?Bcu`gM?
```

with labels, in the edge order produced by sorting endpoint pairs,

```text
03 05 06 0a 03 09 09 11 18 09 05 0c 0c 18 14
```

At vertex \(1\), take edges \(3,5\).  The three local factor data are

| \(P\) | \(E(K_P)\) | \(B(P,K_P)\) |
|:---:|:---|:---|
| 01 | 3,5,6,7 | 0,4 |
| 23 | 3,5,6,8,13,14 | 11,12 |
| 34 | 3,5,6,7 | 8,13 |

In particular, all three base boundaries have size two, and all three
factor circuits contain base edge \(3\).

## 3. Lift amplification lemma

Give the base edges voltages in \(\mathbb F_2\), with voltage one only
on edge \(3\).  Form the usual two-lift: a voltage-zero edge joins equal
sheets, while a voltage-one edge joins opposite sheets.  Copy the
\(D_5\) label to both lifts of every edge.

For any base circuit \(K\), its lift is one circuit of twice the length
exactly when the XOR of its edge voltages is one.  This is the standard
path-lifting rule: returning around \(K\) changes sheets by the voltage
sum.  Since all three displayed \(K_P\) contain edge \(3\), all three
lift to connected double circuits through the chosen lifted angle.

The vertex support of such a lifted circuit is the complete inverse
image of \(V(K_P)\).  Therefore an edge has exactly one endpoint in the
lifted support exactly when its base edge has exactly one endpoint in
\(V(K_P)\).  Every base boundary edge has two lifts, so
\[
                         |\widetilde B(P,K_P)|
                         =2|B(P,K_P)|=4
\]
for all three pairs.

The lift is connected because it contains an odd-voltage circuit.  It is
simple and cubic because it covers a simple cubic graph.  It is
bridgeless because every lifted edge lies on a lift of a base circuit:
an even-voltage base circuit lifts to two circuits and an odd-voltage
one to one double circuit.

## 4. Literal lifted witness

Number lifted vertices by \(2v+s\), where \(s\in\{0,1\}\), and list the
sheet-zero then sheet-one lift of each base edge.  At lifted vertex \(2\),
use lifted edges \(6,10\).  The three exact boundary sets are

| \(P\) | lifted \(B(P,K_P)\) | \(\Delta\chi\) |
|:---:|:---|---:|
| 01 | 0,1,8,9 | 0 |
| 23 | 22,23,24,25 | 0 |
| 34 | 16,17,26,27 | 0 |

Thus this refutes the boundary-size lemma but not the surviving sign
target: all three switches happen to be neutral.

## 5. Reproduction

```text
python3 scratch/check_d5_local_minimum_boundary_counterexample.py
```

The checker imports no project code.  It decodes the base graph6 record,
constructs the lift literally, and checks simplicity, cubicity,
connectivity, bridgelessness, all flow equations, the base and lifted
factor components, voltage parity, boundary sets, and surface-Euler
changes.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified the two-lift
amplification, found the base witness by exact enumeration, proved the
lifting statement, wrote the standalone checker, and drafted this note.
The construction and verification require no trust in an AI system.
