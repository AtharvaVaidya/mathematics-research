# Rank-two fixed-value Eulerian moves

Date: **2026-07-29**

Status: **PROVED AUXILIARY NORMAL FORM AND EXACT FINITE
COUNTERMODELS. NOT A PROOF OR DISPROOF OF FIVECDC.**

For nowhere-zero \(\mathbb F_2^3\)-flows, define one fixed-value
Eulerian move to add one nonzero vector to every edge of an arbitrary
Eulerian edge-set.  The Eulerian set may be disconnected.  This package
proves:

1. if zero intermediate flows are allowed, the minimum number of moves
   from \(f\) to \(g\) is
   \[
   \dim\operatorname{span}\{f(e)+g(e):e\in E\};
   \]
2. when this rank is two, the two moves for a chosen ordered basis are
   forced, and their intermediate flow is nowhere-zero exactly when one
   explicit overlap fibre is empty;
3. \(K_{3,3}\) has a pair for which all six basis orders are blocked,
   so the unrestricted distance is two but the nowhere-zero distance is
   exactly three; this is smallest among connected simple cubic graphs;
4. the cube has a stronger pair \(f,g\): \(f\) fails all 28
   Hušek--Šámal component-parity tests, \(g\) passes 16, \(f\) and \(g\)
   share a nonempty binary coordinate cycle, their difference has rank
   two, but every two-move order is blocked.  An exact three-move path is
   included.

The cube result rules out a particular proof shortcut: choosing an
arbitrary component-parity-good flow that shares a coordinate with the
current flow does not guarantee a legal two-move conversion.  It does
not rule out choosing a different good target: for the displayed bad
flow, 992 of the 996 good rank-at-most-two targets are reachable in at
most two fixed-value Eulerian moves.

Both witness graphs are Tait-colourable and have an explicit
five-cycle double cover (three bichromatic cycles plus two empty
cycles).  They are therefore countermodels only to the proposed
switching lemmas, not counterexamples to FiveCDC.

Run the independent standard-library checker:

```sh
python3 verify.py
```

Check frozen bytes:

```sh
shasum -a 256 -c SHA256SUMS
```

See `HUMAN-PROOF.md` for the complete proof, witness tables, literature
boundary, and trust boundary.  `WITNESSES.json` is the machine-readable
certificate and `verification-output.txt` is the retained clean replay.

## Novelty and publication status

The exact rank-two legal-order criterion and the two finite
countermodels were not found in the directly relevant July 2026
literature audit.  The surrounding subject of nowhere-zero flow
reconfiguration is already established, and the unrestricted
decomposition argument is elementary enough that it may be folklore.
Accordingly this package is suitable for public release as an
AI-assisted research note or computational appendix, but it is not
currently justified as a standalone FiveCDC-resolution preprint.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, derived the normal
form, searched the finite examples, wrote and ran the checker, performed
the literature comparison, and drafted this report.  No independent
human peer review has occurred.
