# A four-step cycle of dual-obstruction neutralizations

Date: 2026-07-29

Status: **HUMAN-CHECKABLE NO-GO FOR PROPOSITION-5-ONLY
MONOTONICITY / NOT A FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## 1. The reduced state space

Work in \(K=\mathbb F_2^2=\{0,1,2,3\}\), written additively as xor.
The order-fourteen boundary counterstate has component word
```
0123444 | 4413024
```
on two oriented seven-circuits.  After fixing the map of block \(0\),
every integrable component-map tuple is represented by
\[
                 k=(u_1,u_2,u_3,a,b),
\]
where all five entries are nonzero, \(a\ne b\), and
\[
                 b=3+u_1+u_2+u_3.                       \tag{1}
\]
Its transformed derivative words are
\[
\begin{split}
A:&\quad 3,u_1,u_2,u_3,a,b,a,\\
B:&\quad b,a,u_1,u_3,3,u_2,a.                            \tag{2}
\end{split}
\]
There are exactly forty such keys.

For a zero-start integration \(r\), put
\[
 Q_x=\sum_{\pi_i=x}\bigl(q(r_{i-1})+q(r_i)\bigr),
 \qquad q(z_1,z_2)=z_1z_2.                               \tag{3}
\]
These are the five common cut-colour parity bits.  For each block \(x\)
and circuit \(D\), let
\[
                 T_{x,D}=\mathop{\mathbin\oplus}_{i\in D,\ \pi_i=x}t_i.
                                                                    \tag{4}
\]
A subset \(S\) is a dual obstruction when
\[
 \mathop{\mathbin\oplus}_{x\in S}T_{x,D}=0
 \quad\hbox{on both circuits},\qquad
 \mathop{\mathbin\oplus}_{x\in S}Q_x=1.                  \tag{5}
\]

Let \(U=(1\ 2)\), represented on \(0,1,2,3\) by `0213`.  A
Proposition-5 switch applies \(U\) to the component maps in \(S\).
When \(0\in S\), follow it by the common normalization \(U^{-1}=U\);
this does not change the mathematical state.

## 2. The literal four-cycle

The following table contains everything needed to check a directed
cycle.  In the \(T\) column, `33/11/...` lists
\((T_{x,A},T_{x,B})\) for blocks \(x=0,\ldots,4\).

| key | derivative words \(A\mid B\) | integrated words \(A\mid B\) | \(Q_0\cdots Q_4\) | \(T_0/\cdots/T_4\) | \(S\) | target |
|---|---|---|---|---|---|---|
| `11112` | `3111121\|2111311` | `3232310\|2323010` | `00101` | `33/11/11/11/22` | `12` | `22112` |
| `22112` | `3221121\|2121321` | `3132310\|2310310` | `00011` | `33/22/22/11/22` | `013` | `21121` |
| `21121` | `3211212\|1221312` | `3101320\|1310320` | `00101` | `33/22/11/11/11` | `012` | `21212` |
| `21212` | `3212121\|2122311` | `3102310\|2313010` | `00011` | `33/22/11/22/22` | `13` | `11112` |

Here is a direct row-by-row audit.

1. In row one, the \(T\)-sum on \(S=\{1,2\}\) is \(1+1=0\);
   the \(Q\)-sum changes from \(0+1=1\) to \(0+0=0\).
2. In row two, the \(T\)-sum on \(S=\{0,1,3\}\) is
   \(3+2+1=0\); the \(Q\)-sum changes from \(0+0+1=1\) to
   \(0+0+0=0\).
3. In row three, the \(T\)-sum on \(S=\{0,1,2\}\) is
   \(3+2+1=0\); the \(Q\)-sum changes from \(0+0+1=1\) to
   \(0+0+0=0\).
4. In row four, the \(T\)-sum on \(S=\{1,3\}\) is \(2+2=0\);
   the \(Q\)-sum changes from \(0+1=1\) to \(0+0=0\).

The two circuit coordinates of every displayed \(T_x\) agree, so each
calculation checks both circuits at once.  Applying `0213` on the named
blocks, and applying the common `0213` normalization exactly when
block \(0\) was named, changes each derivative word into the next row.
Thus every arrow is a legal integrability-preserving switch and
neutralizes the obstruction that selected it.

The last target is the first source.  Therefore no scalar-valued
potential can strictly decrease on every Proposition-5 neutralization.
This conclusion is entirely finite and can be checked from the table
without trusting a program.

## 3. The full forty-state graph

`analyze_dynamics.py` enumerates the forty keys from (1), every dual
witness (5), and all six choices of \(U\).  It retains precisely the
switches for which the selected obstruction changes from one to zero.
It finds:

- 4 dual witnesses at every state;
- 320 neutralizing switch certificates;
- 136 distinct directed state pairs; and
- one strongly connected component containing all 40 states.

Strong connectivity strengthens the explicit-cycle conclusion.  If a
potential is weakly nonincreasing on **every** legal neutralizing edge,
then paths in both directions force it to have the same value at every
one of the forty states.

`independent_audit.py` reproduces these counts from literal transformed
derivative words.  It enumerates the \(6^4\) normalized component-map
tuples rather than using (1), computes cut-colour parities by literal
four-colour counting rather than formula (3), and checks mutual
reachability rather than using the primary Tarjan implementation.

## 4. Exact audit of the global-minimum escape

The cycle above does **not** settle what happens at a globally minimum
projection.  The displayed simple cubic realization has projection
edges \(0,\ldots,13\), but that projection is not minimum.

The relevant necessary inequality is short.  Let \(h\) be a
cardinality-minimum first-coordinate support, let \(s\) be the two low
coordinates, and put
\[
                         M_c=\{e\in h:s(e)=c\}.
\]
If a binary cycle \(C\) avoids \(M_c\), add the flow value \((1,c)\)
on \(C\).  This remains nowhere-zero.  Its first-coordinate support is
\(h\mathbin\triangle C\), so minimality implies
\[
                         |C\cap h|\le |C-h|.              \tag{6}
\]

For every one of the 40 states and all four relative translations of
the two circuits, the two checkers enumerate the realization's 1,024
binary cycles and find a strict violation of (6).  The best-gain
histogram over the 160 state/translation pairs is
\[
\begin{array}{c|rrrrr}
\max_C\bigl(|C\cap h|-|C-h|\bigr)&3&4&5&6&7\\ \hline
\text{number of pairs}&18&86&40&12&4.
\end{array}
\]
Thus zero of the 160 pairs satisfies all exchange inequalities.

One especially transparent violation occurs at state `21212`.
Its second integrated circuit word is
```
2313010
```
up to an arbitrary translation \(z\).  The graph cycle with edge set
\[
                         \{8,9,10,11,12,13,25,26\}        \tag{7}
\]
uses the last six support edges of that circuit and two complement
edges.  Those six low values are `313010`, which omit colour \(2\);
after translation they omit \(2+z\).  Hence (7) avoids
\(M_{2+z}\) for every \(z\), while
\[
                         |C\cap h|-|C-h|=6-2=4.
\]
This is a human-checkable strict descent from support size fourteen to
ten.

Consequently, the exact neutralization cycle is excluded by the
global-minimum hypothesis in this realization.  It does not refute a
potential that uses the full minimum-projection inequalities.  It proves
the narrower and useful no-go statement: Proposition 5 by itself
cannot supply a termination argument; global minimality must enter
essentially.

## Scope and disclosure

This is a structural negative result about one proposed proof method,
not a proof or disproof of the Five-Cycle-Double-Cover Conjecture.  The
forty-state strong-connectivity claim and the 160 exchange profiles are
exact computational statements with two implementations.  The
four-arrow cycle and the explicit exchange descent above are directly
human-checkable.

OpenAI Codex agents under human direction found the cycle, performed
the exhaustive checks, and prepared this proof package.  No
literature-wide novelty or priority claim is made without a separate
current-primary-source review.
