# A positive cyclic blocker need not have a fresh coordinate

Date: **2026-07-28**

Status: **EXACT NO-GO FOR UNIVERSAL FRESH-COORDINATE EXISTENCE; THE
MULTI-SPLICE LEMMA ITSELF REMAINS VALID**.

The fresh-coordinate multi-splice lemma has an essential hypothesis:
some coordinate \(z\) is unused.  Positive cyclic-block potential does
not force that hypothesis, even at order 12.

Use graph6

```text
K?ABCiKU@oKO
```

with endpoint-sorted labels

```text
03 05 06 05 14 11 0c 14 18 14 05 11 14 11 05 11 12 09
```

and ordered roots \((3,15)\).  Every coordinate \(0,1,2,3,4\) occurs.
Nevertheless the exact rooted metric is

\[
                              (d,b^*)=(2,1).
\]

There are seven minimizing eligible profiles, all with the required
\(|P\cap Q|=1\).  One is

\[
\begin{array}{c|c|l}
 &\text{pair}&\text{edges}\\ \hline
C&04&\{0,1,3,4,7,8,9,10,12,14,16,17\}\\
H&01&\{3,5,17\}\\
D&01&\{1,2,15,16\}.
\end{array}
\]

The state lies in a genuine terminal equal-\(\chi\) plateau:
\(\chi=1\), the plateau has 72 states modulo global \(S_5\), and all
1,224 directed switches from those states are neutral.

Because all five coordinates occur, no switch can satisfy the
fresh-coordinate hypothesis.  This is a literal counterexample to:

> Every terminal state with \(b^*>0\) has an immediate
> fresh-coordinate rescue.

It is not a counterexample to plateau descent.  In fact switching
pair \(01\) on \(H\) is neutral and immediately gives \(d=1\).

Reproduce with:

```text
python3 scratch/check_d5_no_fresh_coordinate_blocker_order12.py
```

The checker uses only Python's standard library.  It verifies graph6,
bridgelessness, the D5 flow, all seven minimizing profiles and their
shared-coordinate eligibility, \(d,b^*\), coordinate support, the
complete terminal plateau, and the immediate non-fresh rescue.

## AI-use disclosure

OpenAI Codex agents, under human direction, tested the fresh-coordinate
existence claim, found this exact obstruction, independently replayed
it, and drafted the note.  It has not undergone peer review and is not
a resolution of FiveCDC.
