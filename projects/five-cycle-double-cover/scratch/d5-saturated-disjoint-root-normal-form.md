# A saturated disjoint-root normal form for a bad \(D_5\) Kempe orbit

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE GLOBAL REDUCTION / NOT A FIVECDC
RESOLUTION**.

## 1. Statement

Let \(G\) be a connected cubic graph and let
\[
                   q:E(G)\longrightarrow\binom{[5]}2
\]
have xor zero at every vertex.  For \(i\ne j\), put
\[
 Y_{ij}(q)=\{e:|q(e)\cap\{i,j\}|=1\}.
\]
A Kempe switch transposes \(i,j\) on one circuit component of
\(Y_{ij}\).

Fix two root edges \(r,s\).  Call a state **root-good** when some
component of some \(Y_{ij}\) contains both roots.  Call a state
**saturated disjoint-root** when

1. all five coordinates occur on its edge labels; and
2. its two root labels are disjoint.

**Theorem (saturated disjoint-root normal form).**  From every \(D_5\)
state, at most four Kempe switches produce either a root-good state or
a saturated disjoint-root state.

Consequently, if one Kempe orbit fails to rescue \(r,s\), that same
orbit contains a saturated disjoint-root state.  Thus the rooted
Kempe-orbit theorem reduces without loss to states with genuine
five-coordinate support and, after a global permutation,
\[
                         q(r)=01,\qquad q(s)=23.                 \tag{1}
\]
In this normal form the only factors active on both roots are
\[
                         Y_{02},Y_{03},Y_{12},Y_{13},            \tag{2}
\]
and coordinate \(4\) is the unique local mediator.

The switches in this theorem are not asserted to preserve the
surface Euler characteristic.  The theorem is a reduction for the
unrestricted rooted Kempe-orbit problem, not a proof of the stronger
terminal surface-Euler plateau theorem.

## 2. Separating the two root labels

First suppose that the state is root-bad.

If
\[
                q(r)=xy,\qquad q(s)=xz,\qquad y\ne z,
\]
choose a coordinate \(d\notin\{x,y,z\}\).  Both roots are active in
\(Y_{xd}\).  Since the state is root-bad, they lie in distinct
components.  Switch \(x,d\) on the component containing \(r\).  The
root labels become
\[
                              dy,\qquad xz,
\]
which are disjoint.

If \(q(r)=q(s)=xy\), choose distinct
\(a,b\notin\{x,y\}\).  Switch \(x,a\) on the \(Y_{xa}\)-component
containing \(r\).  If this does not already rescue the roots, their
new labels are
\[
                              ay,\qquad xy.
\]
They are active in \(Y_{yb}\) and remain in distinct components, so
switch \(y,b\) on the component containing \(r\).  Their labels become
\[
                              ab,\qquad xy,
\]
which are disjoint.

Thus at most two switches either rescue the roots or make their labels
disjoint.  A disjoint pair of weight-two labels uses at least four
coordinates.  If five coordinates are now used, the theorem is proved.
It remains to handle exactly four-coordinate support.

## 3. The easy four-coordinate escape

Let the used coordinate set be
\[
                         S=L\mathbin{\dot\cup}M,
\qquad q(r)=L,\quad q(s)=M,
\qquad |L|=|M|=2,
\]
and let \(t\) be the missing fifth coordinate.

For \(i\in S\), write
\[
                         C_i=\{e:i\in q(e)\}.
\]
If some \(C_i\) has at least two components, exactly one of the roots
lies in \(C_i\), because \(L,M\) are disjoint and cover \(S\).
Choose a component \(K\) of \(C_i\) containing neither root.  Since
\(C_t=\varnothing\),
\[
                              Y_{it}=C_i.
\]
Switch \(i,t\) on \(K\).  The old coordinate \(i\) remains on the
component containing its root, coordinate \(t\) becomes used on \(K\),
and the other three old coordinates are unchanged.  The new state uses
all five coordinates, while both root labels remain \(L,M\).

We may therefore assume that every \(C_i\), \(i\in S\), is one circuit.

## 4. A support-preserving \(D_4\) cross switch

Write
\[
                              L=\{a,b\},\qquad M=\{c,d\}.
\]
Fix \(a\in L\).  Consider the two factors \(Y_{ac}\) and \(Y_{ad}\).
Both roots are active in both factors.  If either factor component
through \(r\) also contains \(s\), the state is root-good.

Otherwise let \(K_{ac}\) and \(K_{ad}\) be the respective components
through \(r\).  We claim that at least one of the two switches
\[
                       (a,c)\text{ on }K_{ac},\qquad
                       (a,d)\text{ on }K_{ad}                   \tag{3}
\]
leaves coordinate \(a\) in use.

Indeed, switching \(a,m\) on \(K_{am}\) changes
\[
                         C_a\longmapsto C_a\triangle K_{am}.
\]
It deletes coordinate \(a\) exactly when \(K_{am}=C_a\).  If both
switches in (3) deleted \(a\), every edge of \(C_a\) would be active in
both \(Y_{ac}\) and \(Y_{ad}\).  A weight-two label containing \(a\)
and active in both factors can contain neither \(c\) nor \(d\), so it
must be \(ab\).  Hence every edge of \(C_a\) would have label \(ab\).
But \(C_a\) has degree two at every vertex it visits, so two incident
edges at such a cubic vertex would both have label \(ab\).  This is
impossible: the three nonzero weight-two labels at a cubic xor-zero
vertex are the three distinct sides of a coordinate triangle.

Choose \(m\in\{c,d\}\) for which the switch in (3) does not delete
\(a\), and put \(\{n\}=M-\{m\}\).  Coordinate \(m\) also remains in
use, because the untouched root \(s\), which lies outside \(K_{am}\),
has label \(mn\).  The other two coordinates are unchanged.  Thus the
switched state still uses all four coordinates of \(S\).

Its root labels are
\[
                              bm,\qquad mn,                     \tag{4}
\]
and hence share the single coordinate \(m\).

If the roots now lie in one component of \(C_m\), then, because
\(C_t=\varnothing\), that component is a component of
\(Y_{mt}=C_m\), and the state is root-good.

Otherwise switch \(m,t\) on the \(C_m\)-component containing \(r\).
The component containing \(s\) remains in \(C_m\), while \(t\) becomes
used.  Coordinate \(a\) was deliberately preserved by (3), and
coordinates \(b,n\) remain on the root labels.  The resulting state
therefore uses all five coordinates.  The labels in (4) become
\[
                              bt,\qquad mn,
\]
which are disjoint.

The four-coordinate case costs at most two additional switches.  With
the two label-separation switches of Section 2, the total is at most
four. \(\square\)

## 5. What the reduction removes

The theorem eliminates all lower-support phenomena from a prospective
counterexample to rooted orbit reconfiguration:

- a Tait-supported three-coordinate state is not a separate hard case;
- a four-coordinate state with a disconnected coordinate circuit can
  be split into the missing coordinate without moving either root;
- a four-coordinate state whose coordinate circuits are all connected
  has a support-preserving cross switch which either rescues the roots
  or exposes a disconnected common coordinate that can be split into
  the fifth coordinate.

Thus a genuine obstruction must live in the five-coordinate disjoint
gate (1)--(2).  This is exactly the case not controlled by ordinary
Tait Kempe switching or by the four-coordinate circuit-trap theorem.

The reduction does **not** establish that the four factors in (2) can
be reconfigured to join the roots.  Proving that final saturated
disjoint-gate statement would prove the rooted Kempe-orbit theorem;
finding a closed orbit where all four factors keep the roots separated
would refute it.

## 6. Finite algebra replay

Run

```text
python3 scratch/check_d5_saturated_disjoint_root_normal_form.py
```

The checker exhausts every ordered pair of weight-two root labels,
verifies the one- and two-switch separation recipes, enumerates all
four-coordinate complementary root pairs and cross transpositions, and
checks the local triangle contradiction used to choose a
support-preserving cross switch.

## AI-use disclosure

OpenAI Codex agents, under human direction, isolated the saturated
disjoint-root normal form, found the two-cross-switch support argument,
wrote the finite algebra replay, and drafted this proof.  The argument
is fully exposed for human checking.  It is not peer review and is not
presented as a resolution of FiveCDC.
