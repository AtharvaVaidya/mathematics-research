# A closed complementary-star cage at \(H=0\)

Date: **2026-07-28**

Status: **EXACT MINIMUM-ORDER ENDPOINT NO-GO / NOT A FIVECDC
RESOLUTION**.

## Result

Strict descent of the triangle residual
\[
                         H=K_1\mathbin\triangle K_3
\]
can terminate at \(H=0\).  It is not then guaranteed that a
complementary star triangle rescues the roots or decreases the remaining
support
\[
                         Z=K_1\mathbin\triangle K_2.
\]

The first failure occurs at order 12.  Complete enumeration through
order 10 found 452 all-bad line loops with \(H=0,Z\ne0\); every one had
a complementary-star rescue.  The witness below defeats all four stars
in both operation orders.

## Witness

Use graph

```text
K?ABApoMCWOo
```

with lexicographic label tuple

```text
(01,02,12,23,34,24,34,23,24,24,34,23,23,34,24,04,14,24)
```

and roots \(r=0,s=10\), labeled \(01,34\).  Coordinate \(2\) is the
missing coordinate.  Lift the line triangle
\[
                         01\to02\to12\to01
\]
at \(r\), using switch sequence
\[
                              (12,01,02).
\]
Its circuits are
\[
\begin{aligned}
K_1=K_3&=\{0,1,3,5,7,8,9,11,12,14,16,17\},\\
K_2&=\{0,2,3,5,7,8,9,11,12,14,15,17\}.
\end{aligned}
\]
Thus
\[
                         H=0,\qquad Z=\{1,2,15,16\}.            \tag{1}
\]
All four states on the line lift are root-bad.

The four complementary star sequences at \(s\) are
\[
\begin{gathered}
(03,01,13),\quad(13,01,03),\\
(04,01,14),\quad(14,01,04).
\end{gathered}                                                \tag{2}
\]
Each is a literal identity loop: its three dynamically selected
circuits are equal, so both its residual and support vanish.  The same
is true after the line loop.  Applying any star first leaves the line
loop unchanged, with the same \(H=0\) and the same four-edge \(Z\).
There is no rescue and no strict \((|H|,|Z|)\) descent.

This is an actual component cage, not a hypothetical forbidden circuit
configuration.

## Missing generator and escape

The state is not an orbit obstruction.  It has a two-switch rescue:

1. switch the common-active factor \(04\) on
   \[
                    \{0,1,6,8,13,14,16,17\};
   \]
   this changes the first root label \(01\) to \(14\);
2. switch \(02\), now inactive on both roots, on
   \[
                    \{3,5,6,7\}.
   \]

The resulting \(Y_{04}\)-circuit
\[
                    \{0,1,3,4,7,8,9,10,13,14,16,17\}
\]
contains both roots.

Thus the missing operation is a **change-hidden-pair pivot**: first use
a factor active on both roots to leave the fixed hidden-\(01\) triangle
subsystem, then use a newly exposed inactive handle.  Complementary
triangles with the old hidden pair cannot see the cage (1).

## Reproduction

Run

```text
python3 scratch/check_d5_hzero_complementary_star_cage.py
```

The literal checker verifies every local xor equation, every dynamic
line and star circuit, badness at every intermediate state, the exact
\(H,Z\), identity of all four star loops in both orders, and the
two-switch escape.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated and exhaustively
tested the \(H=0\) endpoint, found the minimum order-12 cage, identified
its missing generator, wrote the literal checker, and drafted this note.
All data are exposed for human verification.  This is not peer review
and is not presented as a resolution of FiveCDC.
