# The shortest-join dual gives zero price to every rainbow quotient cut

Date: 2026-07-29

Status: **HUMAN-CHECKABLE STRUCTURAL NO-GO / NOT A FIVECDC
RESOLUTION**.

This package derives the four exact shortest-\(T_c\)-join linear
programs attached to a globally minimum extendable projection and audits
their behavior under the six-map witness-neutralization switch.

The main conclusions are:

1. for each low colour \(c\), the standard odd-cut dual has optimum
   \(|h|-|M_c|\);
2. every support edge outside \(M_c\) is tight in every optimal dual;
3. a cut which is a union of components of \(G-h\) is either not
   \(T_c\)-odd, or its displayed optimal join crosses it at least three
   times;
4. consequently every such cut has dual coefficient zero in every
   optimal dual, for every colour;
5. in particular, the common rainbow-odd cut supplied by a failed
   affine-cleaning system has zero price in all four duals;
6. witness neutralization changes that cut from \(T_c\)-odd for all four
   colours to \(T_c\)-even for all four, but removes no positive dual
   mass; and
7. every positive cut in every optimal dual must split the interior of
   at least one component of \(G-h\).

The same argument has a positive global consequence:
\[
             |E-h|\ge |h|-|M_c|\quad\hbox{for every }c,
             \qquad |E-h|\ge \tfrac34|h|.
\]
For a cubic graph this implies the support-density bound
\[
                              |h|\le \tfrac67|V|.
\]

Thus a proof which only contracts the complement components cannot
couple the rainbow obstruction to a positive shortest-join dual
potential.  Any successful LP/T-join argument must use cuts inside the
complement components, equivalently some of their metric or Kempe-path
structure.  The density bound records one exact consequence of that
forced interior dual mass.

`HUMAN-PROOF.md` gives the complete proof, including the exact terminal
and capacity update for all six maps.  The two scripts independently
audit the finite \(\operatorname{GL}(2,2)\) orbit identity used in that
update:

```sh
python3 verify.py
python3 independent_audit.py
shasum -a 256 -c SHA256SUMS
```

The scripts are regression checks for the four-element local algebra.
The universal zero-price theorem itself is proved in
`HUMAN-PROOF.md`; it is not inferred from finite computation.

## Scope and AI-use disclosure

This result closes one natural LP coupling, not the minimum-projection
conjecture and not the Five-Cycle Double Cover Conjecture.  FiveCDC
remains open.

OpenAI Codex agents under Atharva Vaidya's direction derived the result,
wrote the proof, and implemented both audits.  The proof is displayed in
full so that checking it does not require trusting an AI system.  No
literature-wide novelty or priority claim is made.
