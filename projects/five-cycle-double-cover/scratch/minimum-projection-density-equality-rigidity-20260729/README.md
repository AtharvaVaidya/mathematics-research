# Rigidity at equality in the minimum-projection density bound

Date: 2026-07-29

Status: **EXACT NECESSARY STRUCTURE / NOT A FIVECDC RESOLUTION**.

Let \(h\) be a globally minimum extendable projection in a finite
loopless cubic graph, and choose optimal odd-cut duals for its four
shortest \(T_c\)-joins.  The already established density bound is
\[
                              |h|\leq\frac67|V|.
\]

This package identifies the complete equality structure forced by those
duals.  Put \(m=|E-h|\) and
\[
                              \sigma=4m-3|h|.
\]
For each colour \(c\), let
\[
\begin{split}
A_c&=\sum_S y_{c,S}\bigl(|\delta_{G-M_c}(S)|-2\bigr),\\
U_c&=\sum_{e\in E-h}(1-\ell_c(e)).
\end{split}
\]
Then
\[
                              \sigma=\sum_c(A_c+U_c).       \tag{1}
\]
Every term is nonnegative.

Consequently, equality \(|h|=6|V|/7\) forces:

- every positive dual cut to have exactly one support edge and one
  complement edge in \(G-M_c\);
- every complement edge to be saturated in all four duals;
- \(G-h\) to be a forest;
- \(|h|\) to be divisible by \(12\);
- \(n=|V|-|h|=|h|/6\) off-support vertices and
  \(5|h|/12\) complement tree components;
- exactly \(|h|/4\) complement edges of each nonzero low colour;
- exactly \(|h|/3\) support-boundary derivatives of each nonzero colour;
  and
- for every balanced affine-cleaning witness shore \(Y\), its three
  selected derivative counts are equal, as are the three outside counts.

Thus an unclean equality-case obstruction, if one exists, has support at
least \(24\): the through-size-fifteen theorem excludes the only smaller
positive multiple \(12\).

The strict-slack case \(\sigma>0\) remains open.  This theorem does not
prove the minimum-projection selection conjecture or FiveCDC.

## Replay

```sh
python3 verify.py
python3 independent_audit.py
shasum -a 256 -c SHA256SUMS
```

The scripts audit the arithmetic consequences and the exact defect
identity on exhaustive bounded integer profiles.  The universal graph
theorem is proved in `HUMAN-PROOF.md`.

## AI-use disclosure

OpenAI Codex agents under Atharva Vaidya's direction derived the slack
identity and equality classification, wrote the proof, and implemented
both audits.  The proof is displayed in full for human checking.  No
literature-wide novelty or priority claim is made.
