# A dynamic six-map colour-load inequality

Date: 2026-07-29

Status: **EXACT NECESSARY CONDITION AND EXPLICIT DESCENT TEST / OPEN
FRONTIER / NOT A FIVECDC RESOLUTION**.

Let \(h\) be a globally minimum extendable projection, let \(s\) be the
low \(\mathbb F_2^2\)-flow, and put \(m=|E-h|\).  For every nonzero
linear functional \(\alpha\) on the low space,
\[
       |\{e\in E-h:\alpha(s_e)=1\}|\geq |h|/2.
\]

More dynamically, let \(Y\) be a union of complement components such
that every common \(U\in\operatorname{GL}(2,2)\) postcomposition on
\(Y\) is integrable.  Write \(N_1,N_2,N_3\) for the three low-colour
counts inside \(Y\), and \(O_1,O_2,O_3\) for those outside.  Then global
minimality forces
\[
             O_a+N_b\leq m-\frac{|h|}{2}
             \quad\hbox{for every }a,b\ne0,                \tag{1}
\]
or equivalently
\[
             \max_a O_a+\max_b N_b\leq m-\frac{|h|}{2}.    \tag{2}
\]

If (1) fails, the proof constructs a legal postcomposition \(U\), a
functional \(\alpha\), and one of the binary cycles
\(\alpha(s^U)\) or \(h+\alpha(s^U)\) which avoids a low-colour class and
uses more support than complement edges.  The minimum-projection
exchange theorem then gives a strict descent.

There is an equivalent boundary form.  Put \(n=|V|-|h|\), the number of
off-support vertices, and let \(k_b(Y)\) count support vertices in \(Y\)
whose unique complement edge has low derivative colour \(b\).  Then (1)
is exactly
\[
                  k_a(\overline Y)+k_b(Y)\leq2n
                  \quad(a,b\ne0).                           \tag{3}
\]
Thus a concentrated derivative-colour profile forces descent unless the
complement has enough internal vertices.

The component union supplied by a failed affine-cleaning system satisfies
the six-map integrability premise.  Thus (1) is an exact coupling between
the witness-neutralization maps and the four dynamically recomputed
exchange inequalities.

What is not proved is that a rainbow-odd witness must violate (1).
Large, colour-balanced complement components can satisfy the inequality.
Accordingly this package does not prove the minimum-projection selection
conjecture or FiveCDC.

Run the finite local audit with:

```sh
python3 verify.py
python3 independent_audit.py
shasum -a 256 -c SHA256SUMS
```

The primary audit checks every integer inside/outside colour profile
through a configurable bound and verifies the equivalence between all
six post-switch functional inequalities and (1).  The independent audit
uses literal binary matrices, checks the constructive strict-descent
dichotomy, and verifies the boundary-incidence form (3).  The universal
theorem is proved in `HUMAN-PROOF.md`, not inferred from finite
computation.

## AI-use disclosure

OpenAI Codex agents under Atharva Vaidya's direction derived the
inequality, wrote the proof, and implemented the audit.  The proof is
displayed in full for human checking.  No novelty or priority claim is
made without specialist review.
