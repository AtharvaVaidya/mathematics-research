# Full-flow exchange for minimum extendable projections

Date: 2026-07-29

Status: **EXACT CHARACTERIZATION AND CERTIFICATE / NOT A FIVECDC
RESOLUTION**.

The four familiar shortest-\(T_c\)-join inequalities examine only the
four low flows \(s+c\,h\) attached to one extension \(f=(h,s)\).  This
package gives the exact exchange problem against every nowhere-zero
\(\mathbb F_2^3\)-flow.

For a competing flow \(g=f+d\), write \(d=(a,b)\), where \(a\) is a
binary flow and \(b\) an \(\mathbb F_2^2\)-flow.  Then \(g\) is
nowhere-zero exactly when
\[
                         b_e\ne s_e\quad\text{whenever }a_e=h_e.
\]
Its first-coordinate gain over \(h\) is
\[
                         |a\cap h|-|a-h|.
\]
Thus \(h\) is globally minimum exactly when every admissible pair
\((a,b)\) has nonpositive gain.

Equivalently, choose an arbitrary low flow \(s'=s+b\), let
\(M=Z(s')\) be its exact zero set, and choose a
\(\partial M\)-join \(J\subseteq E-M\).  Then
\[
                         h'=M\mathbin{\dot\cup}J
\]
is an extendable binary projection, and every extendable projection
arises this way.  Hence the exact global optimum is
\[
 \mu(G)=
 \min_{\substack{s'\text{ an }\mathbb F_2^2\text{-flow}\\
                  J\subseteq E-Z(s'),\
                  \partial J=\partial Z(s')}}
       \bigl(|Z(s')|+|J|\bigr).                            \tag{1}
\]
For a feasible cubic instance \(Z(s')\) is automatically a matching.
For fixed \(M\), the inner problem is the ordinary shortest-\(\partial
M\)-join problem in \(G-M\), with its standard odd-cut LP dual.

This is also an exact XOR/pseudo-Boolean master encoding.  It couples
all low-flow values rather than one affine class at a time.

## The 278-vertex static survivor

The package replays the previously frozen metric inflation.  Its
displayed size-fourteen projection satisfies all four static affine
shortest-join inequalities, but a full-flow competitor has:

```text
exact low zero set M = {1,5}
join J                  = {0,2,3,4,6}
projection M union J    = {0,1,2,3,4,5,6}
cost                     = 7
```

In the 27-edge base order, the displayed and competing flows are
```text
f = 7 5 7 3 7 5 1 3 7 5 1 7 5 1 6 2 2 4 4 2 6 4 2 4 6 2 4
g = 3 1 3 7 5 1 5 6 4 6 2 4 6 2 6 2 2 4 2 4 6 4 2 4 6 4 2
```
and their difference is
```text
d = 4 4 4 4 2 4 4 5 3 3 3 3 3 3 0 0 0 0 6 6 0 0 0 0 0 6 6.
```
The difference uses five nonzero values.  Its first coordinate is the
second support 7-circuit, while its low part is
```text
2222122 | 2111111 | 0000330000033.
```
It is therefore outside the four constant-vector switch families.

Both checkers independently lift both flows to the literal 278-vertex,
417-edge graph and verify conservation, nowhere-zeroness, the edgewise
difference condition, and the strict support gain \(14-7=7\).

## Replay

```sh
python3 verify.py
python3 independent_audit.py
shasum -a 256 -c SHA256SUMS
```

The characterization and its relation to the minimum-selection route are
proved in `HUMAN-PROOF.md`.

## Scope and AI-use disclosure

The characterization does not prove that an optimal triple
\((s',M,J)\) has a second \(\partial M\)-join disjoint from \(J\).
That was exactly the minimum-selection route to FiveCDC proposed in this
project.  The later strict parity-lock package refutes it by constructing
a unique optimum with no second join.  Its graph still has an explicit
FiveCDC, so the FiveCDC conjecture itself remains open.

OpenAI Codex agents under Atharva Vaidya's direction derived the
relative and master formulations, identified the survivor's full-flow
certificate, and wrote the proof and checkers.  The proof and literal
data are included for human verification.  No literature-wide novelty
or priority claim is made.
