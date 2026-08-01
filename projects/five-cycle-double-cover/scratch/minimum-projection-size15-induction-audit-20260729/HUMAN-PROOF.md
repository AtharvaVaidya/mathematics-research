# Human audit of the size-fifteen smoothing induction

Date: 2026-07-29

Status: **EXACT INDUCTION CRITERION AND INDEPENDENT CHECKER / NOT A
FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## 1. The removable repeated-colour lemma

Let \(c_0,\ldots,c_{m-1}\) be a proper cyclic word on four colours,
using all four, with \(m\ge5\).  A position \(i\) is removable if its
colour occurs at least twice and \(c_{i-1}\ne c_{i+1}\).  Deleting such
a position preserves properness and still uses all four colours.

Such a position always exists.  Some colour \(x\) is repeated.  If no
occurrence of a repeated colour were removable, the two neighbours of
every occurrence of \(x\) would be equal, say to \(y\).  The two
displayed occurrences of \(y\) are distinct because \(m\ge5\), so \(y\)
is repeated.  At the next \(y\), the same hypothesis forces the next
colour to be \(x\).  Repeating this argument in both directions makes
the whole cyclic word alternate \(x,y\), contrary to its using four
colours.

Every size-fifteen support shape has a circuit of length at least five,
so the lemma always supplies an abstract smoothing position.

## 2. Exact algebra of smoothing

Write \(K=\mathbb F_2^2\).  Near the deleted support edge, let the three
consecutive support colours be
\[
                         c_-,\ c,\ c_+.
\]
The two old boundary derivatives are
\[
                   a=c_-+c,\qquad b=c+c_+.
\]
After deleting \(c\), the new derivative is
\[
                   r=c_-+c_+=a+b.                       \tag{1}
\]
If the old occurrences belong to complement blocks \(A,B\), the
smoothed partition merges \(A\) and \(B\).  The charge equation is
preserved because the charge of the merged block is the xor of the old
zero charges and (1) replaces \(a,b\) by \(a+b\).

Let a certificate on the smoothed state use the component map \(L\) on
the merged block.  It has a canonical map lift obtained by putting
\(L_A=L_B=L\).  If \(q_-,q_+\) are the adjacent integrated support
colours, the uniquely inserted colour is
\[
                         z=q_-+L(a),
\]
and (1) gives \(q_+=z+L(b)\).

## 3. When direct clean and deletion certificates lift

For a component \(X\), let \(P_X(\gamma)\in\mathbb F_2\) be the parity
of support edges of colour \(\gamma\) crossing its boundary.

If \(A=B\), smoothing has not merged two different parity rows.  Under
the canonical map lift, a direct clean certificate lifts exactly: the
inserted edge is internal to \(A\).

If \(A\ne B\), the smoothed clean equation is only
\[
                         P_A(\gamma)+P_B(\gamma)=0
                         \quad(\gamma\in K).              \tag{2}
\]
The old state is clean exactly when
\[
                         P_A(\gamma)=P_B(\gamma)=0
                         \quad(\gamma\in K).              \tag{3}
\]
Thus a split-block clean certificate lifts if and only if either old
parity row is zero.  Equation (2) says merely that the two rows agree;
the component merge has lost precisely the information needed for
(3).

For deletion, suppose the smoothed integrated word omits a colour
\(\mu\) on the circuit named by the certificate.  If it names a
different circuit, deletion lifts unchanged.  If it names the smoothed
circuit, the lifted certificate works exactly when the inserted value
does not fill the last missing class:
\[
                     |\operatorname{Used}(q)\cup\{z\}|<4. \tag{4}
\]
A certificate naming a particular omitted \(\mu\) therefore lifts when
\(z\ne\mu\).  If the short word uses at most two colours, (4) holds
regardless of \(z\).

These are necessary and sufficient statements for the fixed lifted
component maps and circuit shifts; they do not claim that a failed lift
precludes some unrelated certificate on the original state.

## 4. Exact Kempe lifting criterion

Fix a low-colour pair \(x,y\), put \(\Delta=x+y\), and let
\(\ell:K\to\mathbb F_2\) be one on \(x,y\) and zero on
\(0,\Delta\).  A boundary occurrence is a terminal precisely when
\(\ell(d)=1\).  Equation (1) gives
\[
                         \ell(r)=\ell(a)+\ell(b).          \tag{5}
\]

For a same-block smoothing, every perfect matching \(M\) of the old
terminals collapses to a perfect matching \(\bar M\) of the short
terminals as follows.

* If exactly one of \(a,b\) is a terminal, rename it \(r\).
* If neither is a terminal, change nothing.
* If both are terminals and are paired together, delete their pair.
* If both are paired to \(p,q\), replace the two pairs
  \(ap,bq\) by the single pair \(pq\).

If a short strategy selects a pair of \(\bar M\) inherited from \(M\),
one old path realizes the same switch.  If it selects the artificial
pair \(pq\) in the last case, switching the two actual paths \(ap,bq\)
has the same effect at all short terminals.  It additionally changes
both \(a,b\) by \(\Delta\), hence changes only the inserted support
colour \(z\) by \(\Delta\).

Consequently a short Kempe certificate lifts exactly when, for every
old matching \(M\), its selected inherited path or selected two-path
replacement exists and the resulting old clean/deletion certificate
passes (3) or (4), with the possible change \(z\mapsto z+\Delta\).
This is a finite, realization-independent criterion.  A short
matching-hitting set alone is not sufficient unless this inverse
matching expansion is checked.

For a split-block smoothing, the situation is stricter.  The old paths
are paired separately inside \(A\) and \(B\); the merged short state
allows matchings that forget that separation.  A Kempe row lifts only
if every path it invokes lies in one pre-merge block, robustness is
checked against the matchings of \(A\) and \(B\) separately, circuit
closure is restored, and the final certificate passes (3) or (4).
In particular, a path joining a terminal formerly in \(A\) to one
formerly in \(B\) has no old path justification.

## 5. The literal split-block obstruction and what it does not show

The state

```text
word=01010123|0101232
partition=001234404130002
```

has 320 feasible normalized component-map tuples, no clean tuple, and
no deletion tuple.  Smoothing local position zero of the second circuit
merges blocks 4 and 1 and gives

```text
word=01010123|101232
partition=00123110130002
```

with 56 feasible tuples, 16 clean tuples, and no deletion tuple.  This
is an exact failure of automatic split-block clean lifting.

It is **not** a counterexample to the targeted 6,180-family induction.
Smoothing local position five of its first circuit is same-block and
gives a boundary state canonically equivalent to one of the 224 frozen
size-fourteen residuals.  The independent checker verifies all six
removable positions, both exact classifications, and this canonical
membership.

## 6. Scope of the machine audit

`audit_induction.py` is independent of the primary classifiers: it has
its own derivative, component-map, integration, cleanliness, deletion,
dihedral-action, and canonical-state implementations.

With no arguments it checks all 6,180 targeted residual rows.  When the
full size-fifteen shard files are available, pass them as arguments.  A
successful run proves the finite statement that every emitted residual
has a same-block smoothing equivalent to a frozen size-fourteen
residual.  It does not by itself prove that the primary shard files
exhaust all abstract boundary states; that remains a separate census
claim.

On the completed primary \(7+8\) shard set, the checker reads 6,036
residual rows and covers every one.  Their same-block smoothing counts
are:

```text
3 smoothings:   926 rows
4 smoothings: 4,060 rows
5 smoothings: 1,050 rows.
```

They form 5,200 fully canonical size-fifteen classes, with frozen digest
`f2c0c2b53322c72f00672e3f9c7d807aeb26a6ba771357a673c84c2fdaf96206`.
Thus there is no abstract counterstate to the targeted induction among
the emitted full-census residuals.

The smoothing statements concern the split-occurrence cubic boundary
model.  No arbitrary-degree reduction and no resolution of FiveCDC is
claimed.

OpenAI Codex agents under human direction developed this audit and wrote
the checker and proof.  All conclusions await independent human review.
