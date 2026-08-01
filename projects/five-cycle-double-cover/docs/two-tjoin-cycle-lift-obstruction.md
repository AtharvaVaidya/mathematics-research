# Two disjoint \(T\)-joins do not always lift through contracted circuits

## Status and scope

This note isolates the local problem created when factor circuits are
contracted, two edge-disjoint \(T\)-joins are chosen in the quotient, and
one then tries to lift both joins through the original circuits.

The conclusions are:

1. there is an exact cyclic-word criterion for a fixed pair of quotient
   joins;
2. for two ports of each colour, the obstruction is precisely alternating
   interlacing;
3. a circuit containing one common terminal demand has one distinguished
   exceptional-gap criterion; and
4. changing the quotient joins or the Euler tour does **not** always remove
   the obstruction.

The last assertion is witnessed by a four-vertex, five-edge Eulerian
quotient.  The proof lists all four quotient \(T\)-joins and checks both
possible disjoint pairs.  No solver or search program is needed to verify
it.

This is an obstruction to one quotient-lifting argument.  It is not a
counterexample to the five-cycle-double-cover conjecture.

## 1. Local model

Let \(C\) be a circuit.  Some vertices of \(C\) are **ports**, each carrying
one quotient half-edge.  Their cyclic order is fixed by \(C\).

Let \(R\) and \(B\) be disjoint sets of selected ports.  They are the
half-edges used at this quotient vertex by two edge-disjoint quotient
\(T\)-joins, called red and blue.  Unselected ports may occur between
selected ones.

An **unmarked local lift** is a pair of disjoint edge sets
\[
 X_R,X_B\subseteq E(C)
\]
such that
\[
 \partial_C X_R=R,\qquad \partial_C X_B=B.                 \tag{1}
\]
Here \(\partial_C X\) is the set of vertices having odd incidence in \(X\).
Necessarily \(|R|\) and \(|B|\) are even.

For the marked version, let \(t\) be one distinguished nonport vertex of
\(C\).  Both joins have a terminal demand at \(t\), so the required
boundaries are
\[
 \partial_C X_R=R\mathbin{\triangle}\{t\},\qquad
 \partial_C X_B=B\mathbin{\triangle}\{t\}.                 \tag{2}
\]
Now \(|R|\) and \(|B|\) are odd.  The two lifts may meet at \(t\), but their
edge sets must still be disjoint.

This is exactly the local condition obtained by contracting \(C\):
boundary parity on the quotient records only the parity of the selected
ports, while a lift must realize those boundaries using the actual cyclic
order.

We assume at most one terminal demand on a factor circuit.  Several demands
on one circuit have a similar gap formulation, but are not needed for the
counterexample below.

## 2. The alternating-gap calculation

List all selected ports in cyclic order:
\[
 p_0,p_1,\ldots,p_{2k-1}.
\]
Write \(g_i\) for the open arc from \(p_i\) to \(p_{i+1}\), with indices
modulo \(2k\).  Suppressing unselected ports inside an arc loses no
information, because a lift has constant edge-incidence along that arc
until it encounters a boundary demand.

Put a letter \(R\) or \(B\) at each \(p_i\), according to its selected
join.  This gives the cyclic port word
\[
 w=w_0w_1\cdots w_{2k-1}.                                \tag{3}
\]

To see the governing parity directly, orient \(C\) and let \(x_i,y_i\)
be the indicators that the red and blue lifts use an edge in \(g_i\).
At a selected port,
\[
\begin{aligned}
 x_{i-1}+x_i&=1 &&\text{exactly at an \(R\)-port},\\
 y_{i-1}+y_i&=1 &&\text{exactly at a \(B\)-port},
\end{aligned}                                             \tag{4}
\]
with arithmetic modulo 2.  Let
\[
 z_i=x_i+y_i.
\]
Because the selected port sets are disjoint, \(z\) toggles at every
selected port.  Hence, after choosing its value on one arc, it is 1 on
exactly one of the two alternating classes of gaps
\[
 \{g_0,g_2,\ldots\}\quad\text{or}\quad
 \{g_1,g_3,\ldots\}.                                      \tag{5}
\]

If \(z_i=0\), then \(x_i=y_i\).  Edge-disjointness forces
\[
 x_i=y_i=0.                                               \tag{6}
\]
If \(z_i=1\), exactly one lift uses the arc.  Equations (4)--(6) contain
the whole local problem.

## 3. Exact unmarked criterion

> **Unmarked cycle-lift criterion.**
> Suppose \(|R|\) and \(|B|\) are even.  The two selected port sets have
> an edge-disjoint lift through \(C\) if and only if one of the two
> alternating gap classes in (5) has equal-coloured endpoints on every
> one of its gaps.

Equivalently, one of the two alternating perfect matchings of consecutive
selected ports pairs \(R\)-ports with \(R\)-ports and \(B\)-ports with
\(B\)-ports.

Equivalently again:

> Every maximal monochromatic run in the cyclic word \(w\) has even
> length.                                                       \(\tag{7}\)

The empty selected-port set is feasible by taking both lifts empty.

### Proof

In any feasible lift, take the gaps with \(z_i=1\).  On such a gap exactly
one colour is present.  At each endpoint the corresponding lift must
toggle between that used gap and the adjacent zero gap.  Therefore the
two endpoints have the same colour.

Conversely, suppose one alternating gap class has equal-coloured endpoints.
Use every gap in that class by the colour of its endpoints and leave every
gap in the other class unused.  Each selected port is incident with exactly
one used gap, of its own colour.  This gives (1), and the red and blue edge
sets are disjoint.

Finally, an alternating consecutive-port pairing is monochromatic exactly
when all colour changes occur in the other parity class of gaps.  This is
equivalent to the cyclic distance between successive colour changes being
even, which is exactly (7). \(\square\)

### Interlacing

When \(|R|=|B|=2\), there are only two cyclic patterns up to exchanging
the colours:

\[
 RRBB,\qquad RBRB.
\]

The first is feasible and the second is not.  Thus, for two red and two
blue ports, failure is precisely the usual alternation or interlacing of
the two pairs around the circuit.

For larger port sets, pairwise language is insufficient.  The exact
generalization is the even-run condition (7).

## 4. Exact one-terminal criterion

Assume now that \(t\) is a common terminal demand and that \(|R|\) and
\(|B|\) are odd.  Let \(g_h\) be the unique selected-port gap containing
\(t\).  The terminal may have unselected ports on either side inside that
gap; only its location relative to the selected ports matters.

> **Marked cycle-lift criterion.**
> The boundary demands (2) have edge-disjoint lifts if and only if:
>
> 1. the endpoints of \(g_h\) have different colours; and
> 2. every other gap \(g_i\) with \(i\equiv h\pmod2\) has equal-coloured
>    endpoints.

Equivalently, the terminal gap is a colour-change gap, and every other
colour change lies in the opposite alternating class of gaps.

### Proof

The shared terminal demand cancels in
\[
\partial(X_R\mathbin{\triangle}X_B),
\]
so \(z=x+y\) still toggles exactly at the selected ports.  At \(t\), both
lifts must toggle.  If the terminal gap had \(z=0\), (6) would make both
lifts zero on both sides of \(t\), which is impossible.  Hence \(g_h\)
belongs to the \(z=1\) alternating class.

On every other gap of that class, one colour occupies the whole gap, so
its two endpoint colours must agree, exactly as in the unmarked proof.
On \(g_h\), both lifts toggle at \(t\): one colour runs from one endpoint
to \(t\), and the other runs from \(t\) to the other endpoint.  Its
endpoint colours must therefore be different.

These observations are also a construction.  Leave the opposite gap
class unused, fill each ordinary selected gap with its common endpoint
colour, and split \(g_h\) at \(t\) between its two different endpoint
colours. \(\square\)

The smallest marked pattern has one red and one blue port.  It is always
feasible: choose the alternating class containing \(t\) and split that
gap between the two colours.

## 5. A smallest abstract obstruction to choosing better joins

We now give a connected loopless Eulerian quotient in which:

- every quotient component contains an even number of terminals;
- two edge-disjoint quotient \(T\)-joins exist;
- all possible disjoint pairs can be listed in four lines; but
- no pair lifts through the prescribed factor circuits.

Let the quotient \(Q\) have vertices
\[
 V(Q)=\{0,1,2,3\}
\]
and edges
\[
\begin{array}{c|ccccc}
\text{edge}&a&a'&b&c&d\\ \hline
\text{ends}&03&03&12&13&23 .
\end{array}                                             \tag{8}
\]
Thus \(Q\) is a triangle \(1\,2\,3\,1\) together with a two-edge dipole
between 0 and 3.  Its degrees are
\[
 2,2,2,4,
\]
so it is connected and Eulerian.  Take every quotient vertex to be a
terminal:
\[
 T=\{0,1,2,3\}.                                         \tag{9}
\]

Expand the quotient vertices back to factor circuits with one terminal
demand \(t_i\) on each.  Their cyclic port orders are
\[
\begin{array}{c|l}
0&(t_0,a,a'),\\
1&(t_1,b,c),\\
2&(t_2,b,d),\\
3&(t_3,c,a,a',d).
\end{array}                                             \tag{10}
\]
For example, at vertex 3 the terminal lies in the gap from \(d\) to \(c\).
Each occurrence of an edge name is a distinct port, and equal names in
two rows are joined by the corresponding quotient edge.

This expansion is a completely explicit simple subcubic graft: the factor
circuits have lengths \(3,3,3,5\); their ten port vertices have degree
three; the four vertices \(t_i\) have degree two and form the terminal set.
No drawing is required.

### All quotient \(T\)-joins

At vertex 0 a \(T\)-join must choose exactly one of \(a,a'\).  At vertices
1 and 2, its parity equations are
\[
 b+c=1,\qquad b+d=1.                                   \tag{11}
\]
Thus either it chooses \(b\) and neither of \(c,d\), or it chooses both
\(c,d\) and not \(b\).  The parity equation at vertex 3 is then automatic.
Consequently the complete list of quotient \(T\)-joins is
\[
\begin{array}{c|l}
J_1&\{a,b\},\\
J_2&\{a',b\},\\
J_3&\{a,c,d\},\\
J_4&\{a',c,d\}.
\end{array}                                             \tag{12}
\]

There are exactly two unordered edge-disjoint pairs:
\[
 \{J_1,J_4\},\qquad \{J_2,J_3\}.                        \tag{13}
\]
Both pairs partition all five quotient edges.

### Both pairs fail at the same factor circuit

For \(\{J_1,J_4\}\), colour \(J_1\) red and \(J_4\) blue.  At vertex 3,
the port word in the order \((c,a,a',d)\) is
\[
 B\,R\,B\,B.                                            \tag{14}
\]
The terminal gap is \(d\,t_3\,c\), whose two endpoint ports are both blue.
This violates condition 1 of the marked criterion.

For \(\{J_2,J_3\}\), colour \(J_2\) red and \(J_3\) blue.  The same port
order gives
\[
 B\,B\,R\,B,                                            \tag{15}
\]
and the two endpoints of the terminal gap are again both blue.  Exchanging
the names red and blue changes nothing: the endpoint colours remain equal.

The degree-two quotient vertices cause no hidden failure or escape.  At
each of them, the two incident ports have different colours and the
terminal lies in one of the two gaps, so the smallest marked pattern is
feasible.  The obstruction is exactly the factor circuit at vertex 3.

Every hypothetical packing in the expanded graft contracts to one of the
two pairs in (13), because restriction to the quotient edges preserves the
\(T\)-join parity equations and preserves edge-disjointness.  The local
criterion proves that neither pair can occur.  Hence the expanded graft
does not pack two edge-disjoint \(T\)-joins even though its Eulerian
quotient does.

## 6. Why Euler-tour freedom does not repair the example

A common way to obtain two quotient \(T\)-joins in a connected Eulerian
graph is to choose an Euler tour, designate one visit at each terminal as
a colour switch, and colour the intervening tour segments alternately.
The two colour classes are edge-disjoint \(T\)-joins and partition the
Eulerian edge set.

In the quotient (8), any result of this procedure is still an
edge-disjoint pair of quotient \(T\)-joins.  The parity calculation
(11)--(13) proves that it must be one of the two displayed pairs.
Both pairs fail at the fixed cyclic order (10).  Therefore:

> No choice of quotient \(T\)-joins and no choice of Euler tour avoids the
> local obstruction in this example.

An Euler tour changes transition choices in the quotient; it does not
change the cyclic order inherited from a factor circuit.

## 7. Minimality in the abstract model

The example is smallest first by quotient order and then by edge count
among connected loopless Eulerian quotients with:

- a nonempty even set of marked quotient vertices;
- at most one terminal demand on each expanded factor circuit; and
- arbitrary parallel quotient edges.

Here is a short proof.

With fewer than four quotient vertices, the nonempty terminal set has
size two.  Expanding vertices into circuits preserves bridgelessness:
every internal factor edge lies on its factor circuit, and every quotient
edge lies on a quotient circuit because a connected Eulerian graph has no
bridge; lifting that quotient circuit through the factor circuits gives a
circuit containing the expanded edge.  A connected bridgeless graph has
two edge-disjoint paths between any two vertices.  Those two paths are
two edge-disjoint \(T\)-joins for a two-element terminal set.  Thus no
obstruction has fewer than four quotient vertices.

For four quotient vertices, a connected loopless Eulerian graph has at
least four edges.  If it has exactly four, every degree is two, so the
quotient is a 4-cycle.  The only possible four-element terminal set is all
vertices.  Colour alternate quotient edges red and blue.  At every
quotient vertex the two selected ports have different colours, so the
smallest marked criterion gives a lift regardless of the location of its
terminal gap.

The quotient (8) has four vertices and five edges, so it is minimal.

If quotient simplicity is imposed, the analogous smallest example found
by the same finite analysis has five vertices and six edges: two triangles
sharing one vertex.  Simplicity is not needed for the conclusion because
factor contraction naturally produces quotient parallel edges, while the
expanded graft (10) itself is simple.

## 8. Consequence for quotient-lift arguments

Quotient parity is necessary but not sufficient.  A sound proof using
contracted factor circuits must supply at least one additional ingredient:

1. a theorem selecting two quotient \(T\)-joins whose port words satisfy
   the local criteria at every contracted circuit;
2. a structural reason that the inherited rotations cannot contain the
   marked obstruction above;
3. permission to change the factor itself, and a proof that this can repair
   all cyclic orders simultaneously; or
4. a different lift that is not confined to edge-disjoint subgraphs of the
   individual factor circuits.

The local checks are linear-time once a quotient pair is fixed: suppress
unused ports, read the cyclic red/blue word, and test the two alternating
gap classes.  What fails is the proposed universal existence step, not
the ability to recognize a valid lift.

## AI-use disclosure

This analysis, the finite search used to locate the smallest obstruction,
and the exposition were produced with substantial assistance from OpenAI
Codex language-model agents under human direction.  The search suggested
the example but is not part of its proof.  The graph, the complete list
of four \(T\)-joins, both disjoint pairs, and the local failure are written
out so that the result can be checked without trusting software or an AI
system.
