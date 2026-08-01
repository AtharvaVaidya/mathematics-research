# A 12-vertex obstruction to choosing a shortest Hušek--Šámal projection

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE COUNTEREXAMPLE TO AN EXTREMAL PROJECTION
LEMMA / NOT A FIVECDC COUNTEREXAMPLE**.

## 1. The failed global-selection lemma

After eliminating the basis from the Hušek--Šámal formulation, a natural
global strategy is:

> choose a shortest nonempty binary cycle \(h\), and extend it to a
> nowhere-zero \(\mathbb F_2^3\)-flow.

If the extension existed and the kernel factor \(E-h\) were connected,
the Hušek--Šámal component condition would be automatic.  The graph below
shows that even the extension can fail for every shortest cycle.

The obstruction is global in the relevant sense: it does not fix a
pre-existing Fano flow.  It rules out the chosen binary projection
against **every** possible choice of the other two flow coordinates.

## 2. The graph

Take the Petersen graph and expand one vertex into a triangle, attaching
the three former incident edges to the three different triangle vertices.
In graph6 form one labelling is

```text
K?`@E`gFCKEO
```

Its vertices are \(0,\ldots,11\), and its edges in graph6 order are

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
0&04&1&15&2&26\\
3&07&4&17&5&37\\
6&18&7&28&8&48\\
9&39&10&49&11&59\\
12&0\,10&13&5\,10&14&6\,10\\
15&2\,11&16&3\,11&17&6\,11 .
\end{array}
\]

The unique triangle is
\[
                        C=\{26,2\,11,6\,11\}.              \tag{1}
\]
There is no loop or parallel edge, and the graph is cubic.

Contracting \(C\) to a vertex \(x\) gives the Petersen graph.  For a
literal isomorphism to the standard outer-cycle/inner-star labelling,
map
\[
\begin{array}{c|cccccccccc}
\text{contracted graph}&0&4&8&1&7&10&9&x&5&3\\
\hline
\text{standard Petersen}&0&1&2&3&4&5&6&7&8&9 .
\end{array}                                               \tag{2}
\]

Thus \(C\) is the unique shortest nonempty binary cycle.

## 3. Projection extension forces a small exact-zero set

The following observation is useful beyond the example.

> **Projection--resistance lemma.**  Let \(h\) be a binary cycle of a
> cubic graph \(G\).  If \(h\) is one coordinate of a nowhere-zero
> \(\mathbb F_2^3\)-flow, then \(G\) has an
> \(\mathbb F_2^2\)-flow whose exact zero set is a matching contained in
> \(h\).  Consequently
> \[
>                    r_f(G)\le \nu(h),                       \tag{3}
> \]
> where \(r_f(G)\) is flow resistance and \(\nu(h)\) is the maximum
> matching size in the support of \(h\).

**Proof.**  Write the three-bit flow as
\[
                             f=b\,h+s,
\]
where \(b\) has first coordinate one and
\(s:E(G)\to\mathbb F_2^2\) is the projection onto the other two
coordinates.  Since both \(f\) and \(h\) are flows, so is \(s\).
If \(h(e)=0\), then \(s(e)=f(e)\ne0\), so every zero of \(s\) lies in
\(h\).

At a cubic vertex, \(h\) has degree zero or two.  Two incident zero
values of \(s\) would force the third value of \(s\) to be zero.  The
third edge has \(h=0\) when the first two have \(h=1\), contradicting
the preceding paragraph.  Thus the zero set is a matching contained in
\(h\), proving (3). \(\square\)

For a circuit of length \(\ell\), (3) gives the especially transparent
necessary condition
\[
                         r_f(G)\le\lfloor\ell/2\rfloor.       \tag{4}
\]

## 4. Human proof that the triangle does not extend

For the triangle (1), a matching contained in \(C\) is either empty or
one edge.

An empty exact-zero set would be a nowhere-zero
\(\mathbb F_2^2\)-flow, equivalently a Tait three-edge-colouring.  Such a
colouring of the triangle expansion contracts to a Tait colouring of the
Petersen graph: the three internal triangle edges use the three colours,
and the three external edges use the three corresponding missing
colours.  This is impossible.

Suppose instead that the unique zero is one triangle edge, say \(uv\).
At \(u\), the other two incident edges have the same nonzero
\(\mathbb F_2^2\)-value by flow conservation; the same holds at \(v\).
Delete \(uv\) and suppress the two resulting degree-two vertices,
carrying their common nonzero values onto the two suppressed edges.  The
result is exactly the contracted Petersen graph, now with a nowhere-zero
\(\mathbb F_2^2\)-flow.  That again gives a Tait colouring of Petersen,
a contradiction.

The argument is symmetric in the three triangle edges.  Hence no
\(\mathbb F_2^2\)-flow has exact zero set contained in \(C\).  By the
projection--resistance lemma, \(C\) is not a coordinate of any
nowhere-zero three-bit flow.

Therefore:

> **Shortest-projection obstruction.**  The displayed 12-vertex graph has
> a unique shortest binary cycle, and that cycle cannot be extended to
> any nowhere-zero \(\mathbb F_2^3\)-flow.

## 5. Why this is not a FiveCDC counterexample

The Petersen graph has a standard FiveCDC.  Triangle expansion preserves
one directly.  At the expanded vertex, let the three old incident
two-subset labels be \(A,B,C\).  They have coordinatewise even parity.
Keep them on the three external edges and label each new internal
triangle edge by the old label on the opposite external edge.  At every
new triangle vertex the incident labels are again \(A,B,C\), so the local
parity equations hold and every edge label still has weight two.

Thus the 12-vertex graph has a standard FiveCDC.  A good
Hušek--Šámal projection exists elsewhere; only the rule “choose a shortest
cycle first” is false.

## 6. Stress-test interpretation

The Petersen graph itself does not refute the shortest-cycle rule: some
of its 5-cycles do extend.  Expanding a vertex to a triangle creates a
unique, strictly shorter binary cycle whose contraction remembers the
Petersen Tait obstruction.  This identifies the first irreducible
obligation for any extremal-cycle proof:

> a successful selection rule must control exact-zero matchings contained
> in the chosen cycle, not merely its length, its number of complement
> components, or the connectivity of its complement.

The example contains a triangle and therefore lies outside the usual
girth-at-least-ten minimum-counterexample domain.  It does not refute a
selection theorem using that reduced-domain hypothesis.

## AI-use disclosure

An OpenAI Codex agent, under human direction, found the graph by exact
cycle-space enumeration, recognized it as a Petersen triangle expansion,
derived the human proof above, and drafted this note.  The graph-theoretic
argument is self-contained but has not received independent human review.
No FiveCDC resolution or novelty priority is claimed.
