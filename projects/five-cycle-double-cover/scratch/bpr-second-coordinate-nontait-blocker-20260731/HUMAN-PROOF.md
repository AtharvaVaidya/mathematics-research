# A vertex-minimal non-Tait blocker for the refined second-coordinate gate

Date: **2026-07-31**

Status: **EXACT OBSTRUCTION TO ONE BPR DESCENT MECHANISM / VERTEX-MINIMAL
IN THE STATED HOST DOMAIN / NOT BPR / NOT FIVECDC**.

## 1. Statement

There is a simple bridgeless cyclically four-edge-connected cubic graph
\(G\), a nowhere-zero \(\mathbb F_2^3\)-flow \(f\), a nonzero target value
\(b\), and an optimal first join \(J\) with the following property.

Let \(M=f^{-1}(b)\), \(F=M\mathbin{\dot\cup}J\), and let \(Q\) be one
component of \(G-F\).  Then

\[
 \Psi(M,J)=(0,8),\qquad
 (|\delta_{G-M}(Q)|,|\delta_M(Q)|)=(3,3),
\]

but every partner-free direction on the \((G-M)\)-cut of \(Q\) fails the
reduced even-four-cut parity gate.  In fact the same is true for the other
old odd residual component, whose profile is \((5,1)\).  Thus this optimal
state has no old odd component at which the partner-free, all-in,
fixed-\(F\) gate can start while keeping the first coordinate zero.

The host is the first 18-vertex Blanuša snark in the frozen census.  It is
non-3-edge-colourable.  Moreover, order 18 is smallest possible among
simple cyclically four-edge-connected non-Tait cubic hosts for this exact
kind of optimal-state blocker: the Petersen graph is the only such host on
fewer than 18 vertices, and an exhaustive flow/join computation shows that
it has no optimal state whose first coordinate is zero and whose second
coordinate is positive.

This settles a structural question about the proposed descent mechanism.
It does **not** disprove BPR and does **not** prove or disprove the
five-cycle-double-cover conjecture.  The host has girth five, so it is also
outside the girth-at-least-ten domain of the full BPR conjecture.

## 2. Frozen graph and state

The labelled graph6 record is

```text
Q???C@?GCoOoDO[?CcAO_?k?J??
```

Nauty's `labelg` gives canonical graph6 record

```text
Qs??GODB?E@OOGG@G@@?_C?cO@_
```

Here is the complete labelled edge/flow table; an entry is
`edge:endpoints/value`.

```text
0:0-7/6   1:1-8/6   2:2-9/6   3:0-10/2  4:3-10/3
5:4-10/1  6:0-11/4  7:5-11/5  8:6-11/1  9:3-12/5
10:5-12/2 11:7-12/7 12:1-13/3 13:2-13/5 14:3-13/6
15:2-14/3 16:5-14/7 17:8-14/4 18:1-15/5 19:4-15/4
20:9-15/1 21:6-16/5 22:8-16/2 23:9-16/7 24:4-17/5
25:6-17/4 26:7-17/1
```

At every vertex the three displayed values XOR to zero, and every value is
nonzero, so this is a directly checkable nowhere-zero flow.  Take \(b=1\).
Then

\[
 M=\{5,8,20,26\},
\]

and take

\[
 J=\{4,7,10,11,12,14,18,21,23,24\}.
\]

The boundary of each of \(M\) and \(J\) is

\[
 T=\{4,6,7,9,10,11,15,17\}.
\]

Thus \(J\subseteq E(G)-M\) is a \(T\)-join and \(F=M\dot\cup J\) is
Eulerian.

The residual components and their profiles \((k,q)\) are:

| component | vertex shore | cut edges | \((k,q)\) |
|---|---|---|---|
| \(Q=C_0\) | 0, 7, 10, 11 | 4, 5, 7, 8, 11, 26 | (3,3) |
| \(C_1\) | 1, 2, 5, 8, 9, 13, 14, 16 | 7, 10, 14, 18, 20, 21 | (5,1) |
| \(C_2\) | 3, 12 | 4, 10, 11, 14 | (4,0) |
| \(C_3\) | 4, 15 | 5, 18, 20, 24 | (2,2) |
| \(C_4\) | 6, 17 | 8, 21, 24, 26 | (2,2) |

The odd components are \(C_0,C_1\); neither has total cut size four, and
their \(k\)-sum is \(3+5=8\).  Hence \(\Psi(M,J)=(0,8)\).

For optimality, \(H=G-M\) is connected and has binary cycle rank six.
One \(T\)-join plus its six-dimensional cycle space gives all \(2^6=64\)
possible \(T\)-joins in \(H\).  Their exact potential distribution is

```text
(0,8):3  (0,10):1  (1,6):9  (1,8):3  (1,10):1
(2,6):13 (2,14):1  (2,16):1 (3,12):1 (3,14):10
(3,16):5 (4,12):11 (4,22):1 (5,20):2 (5,22):1 (6,18):1
```

The entries total 64 and have lexicographic minimum \((0,8)\), proving
that the displayed \(J\) realizes \(\Psi^*(M)\).  The independent checker
constructs a fundamental-cycle basis and verifies every one of these 64
joins directly.

## 3. Six cut-space certificates: the entire state is blocked

On the \(H\)-cut of \(Q\), the three edges are

\[
 4,7,11\quad\hbox{with values}\quad3,5,7.
\]

Their partners under XOR with \(b=1\), namely \(2,4,6\), do not occur on
that cut.  The partner-free directions are therefore exactly
\(t=3,5,7\).

For a direction \(t\), put

\[
 L_t=G-\bigl(M_t\cup(M_{1+t}-J)\bigr),
 \qquad
 a_C=(M_1\cup M_{1+t})\cap E(L_t)\cap\delta(C).
\]

The protected old even four-cut components are exactly
\(C_2,C_3,C_4\).  A legal cycle \(X\in Z_1(L_t;\mathbb F_2)\) passes the
reduced gate precisely when

\[
 \langle a_Q,X\rangle=1,
 \qquad
 \langle a_{C_i},X\rangle=0\quad(i=2,3,4).
\tag{1}
\]

The complete dual certificates are:

| \(t\) | \(a_Q\) | nonempty protected rows | exact cut-space identity in \(L_t\) |
|---|---|---|---|
| 3 | 5, 8, 26 | \(a_{C_2}=\{10\}\), \(a_{C_3}=\{5,20\}\), \(a_{C_4}=\{8,26\}\) | \(a_Q\triangle a_{C_4}=\{5\}=\delta_{L_3}(\{10\})\) |
| 5 | 5, 8, 26 | \(a_{C_3}=\{5,20\}\), \(a_{C_4}=\{8,26\}\) | \(a_Q=\delta_{L_5}(\{4,11,17\})\) |
| 7 | 5, 8, 26 | \(a_{C_2}=\{14\}\), \(a_{C_3}=\{5,20\}\), \(a_{C_4}=\{8,26\}\) | \(a_Q\triangle a_{C_2}=\{5,8,14,26\}=\delta_{L_7}(W)\), where \(W=\{1,2,4,6,8,9,13,14,15,16,17\}\) |

These three displayed identities are short human-checkable proofs of
infeasibility.  Every binary cycle has even intersection with every cut.
For \(t=5\), this forces \(\langle a_Q,X\rangle=0\).  For \(t=3\), a
cycle with \(\langle a_Q,X\rangle=1\) must also have
\(\langle a_{C_4},X\rangle=1\).  For \(t=7\), it must instead have
\(\langle a_{C_2},X\rangle=1\).  Each case contradicts (1).

For an additional primal check, the dimensions of
\(Z_1(L_3),Z_1(L_5),Z_1(L_7)\) are respectively \(5,1,4\).  Direct
enumeration checks 32, 2, and 16 cycles.  The counts of cycles flipping
\(Q\) are 16, 0, and 8, and zero cycles pass all protected rows in every
case.

The other odd component is \(C_1\), of profile \((5,1)\).  Its
\(H\)-cut values have support \(\{2,5,6\}\), while the respective partners
\(3,4,7\) do not occur.  Its partner-free directions and certificates are:

| \(t\) | \(a_{C_1}\) | nonempty protected rows | exact cut-space identity in \(L_t\) |
|---|---|---|---|
| 2 | 20 | \(a_{C_2}=\{4\}\), \(a_{C_3}=\{5,20\}\), \(a_{C_4}=\{8,26\}\) | \(a_{C_1}\triangle a_{C_2}\triangle a_{C_3}=\{4,5\}=\delta_{L_2}(\{10\})\) |
| 5 | 20 | \(a_{C_3}=\{5,20\}\), \(a_{C_4}=\{8,26\}\) | \(a_{C_1}=\delta_{L_5}(\{15\})\) |
| 6 | 20 | \(a_{C_2}=\{11\}\), \(a_{C_3}=\{5,20\}\), \(a_{C_4}=\{8,26\}\) | \(a_{C_1}\triangle a_{C_3}\triangle a_{C_4}=\{5,8,26\}=\delta_{L_6}(W)\), for the same \(W\) as above |

The identical cycle-cut orthogonality argument proves all three systems
infeasible.  The corresponding cycle-space dimensions are \(6,1,5\); the
checker enumerates 64, 2, and 32 cycles, of which 32, 0, and 16 flip
\(C_1\), and again none pass every protected row.  Thus the displayed
optimal state is blocked at **both** of its old odd components, not merely
at a specially chosen one.

This obstruction depends on the choice of optimal join.  There are three
joins attaining \((0,8)\).  The other two are

\[
 \{2,4,7,9,11,15,16,19,25\},
 \qquad
 \{2,4,7,10,11,13,14,19,25\}.
\]

For each of them, the direction-3 cycle

\[
 X=\{0,2,6,8,9,11,13,14,21,23\}
\]

is all-in, protects every old even four-cut, and changes the fixed-residual
potential to \((0,0)\).  The checker verifies these two escapes directly.
Thus the example refutes an assertion that an **arbitrary** optimal
representative must admit the local move; it does not refute a strategy
that chooses a favourable optimum among all minimizers.

## 4. The host really is non-Tait and cyclically four-connected

The checker verifies simplicity, connectedness, cubicity, bridgelessness,
and girth five directly.  It examines every vertex shore (quotiented by
complementation) and finds minimum cyclic cut size four.  Thus the host
answers the present non-Tait/cyclically-four question but not the stronger
girth-ten question in the full BPR domain.

For a cubic graph, a Tait colouring exists if and only if some perfect
matching has an even-cycle complement: one colour is a perfect matching
and the other two alternate on the complementary cycles, and conversely.
The host has exactly 20 perfect matchings.  Sixteen have complementary
cycle lengths \((5,13)\), and four have lengths \((9,9)\).  Every
complement therefore contains odd cycles, proving that the host is not
3-edge-colourable.  `certificate-output.txt` lists all 20 perfect
matchings, so this finite proof can be checked without trusting the
summary.

## 5. Vertex minimality in the stated domain

The optional census checker invokes nauty `geng` to generate every
connected simple cubic graph of even order at most 16.  It independently
tests Tait colourability as above and deletes every one-, two-, and
three-edge set to test cyclic edge connectivity.  Its counts are:

| order | connected cubic | non-Tait | cyclically-4 non-Tait |
|---:|---:|---:|---:|
| 4 | 1 | 0 | 0 |
| 6 | 2 | 0 | 0 |
| 8 | 5 | 0 | 0 |
| 10 | 19 | 2 | 1 |
| 12 | 85 | 5 | 0 |
| 14 | 509 | 34 | 0 |
| 16 | 4060 | 212 | 0 |

The unique qualifying record below order 18 is the Petersen graph,
`ICOf@pSb?`.

The Petersen checker constructs its full six-dimensional binary flow
space and enumerates all \(64^3\) coordinate triples.  Exactly 28,560 are
nowhere-zero \(\mathbb F_2^3\)-flows.  Fixing \(b=1\) is without loss of
generality because \(GL(3,2)\) is transitive on nonzero values.  Across
all flows there are 295 distinct target classes.  For each, the checker
enumerates every \((\partial M)\)-join and computes \(\Psi^*(M)\).  The
flow-weighted optimum distribution is

```text
(0,0):18240  (1,6):4320  (1,8):5760  (3,12):240.
```

Thus the Petersen graph has no optimal state with first coordinate zero
and positive second coordinate; there is no blocker of the present kind.
Together with the complete host census, this proves vertex minimality.

## 6. Reproduction and scope

Run:

```sh
python3 -B verify_certificate.py
python3 -B search_petersen.py
python3 -B verify_small_order_census.py  # requires nauty geng
```

`verify_certificate.py` is a standard-library-only implementation written
separately from the Z3-assisted discovery program `search_snarks18.py`.  It
reconstructs the graph, flow, joins, potentials, all cycle spaces, dual
cut witnesses, graph connectivity, and non-Tait certificate from the
frozen data.

What fails here is a specific simultaneous coordination claim: non-Tait
and cyclically four-connected structure does not ensure that some
partner-free direction can flip an old odd residual component while
protecting all old even four-cuts in an all-in fixed-\(F\) switch.  In this
state every such direction at both old odd components is blocked.
Indeed, the two other optimal joins for the same target admit an immediate
descent to \((0,0)\).  Non-all-in rerouting, a different target, and global
reoptimization after a different switch also remain available.
Accordingly, this is not a counterexample to BPR and has no direct
counterexample status for FiveCDC.

All theorem statements, prose, code, and certificate packaging here were
produced by OpenAI Codex under human direction.  The results have not yet
received independent human peer review.
