# Complementary quotient joins cannot lift in the equality case

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE NO-GO THEOREM FOR ONE QUOTIENT
CONSTRUCTION / FIVE-CDC STILL OPEN**.

This note proves that the especially simple Eulerian-quotient
construction—take one quotient \(T\)-join and its full edge
complement—cannot solve the connected eight-mark size-four branch at
the 88-vertex equality bound.  Any successful pair of quotient joins
in that case must leave at least one quotient edge unused.

The theorem is a limitation of a proof method, not a counterexample to
the five-cycle double cover conjecture.

## 1. Setup

Let \(H\) be the suppressed cubic core in the connected size-four
branch, with universally separated eight-edge matching \(S\).  Give all
marks one Tait colour \(c\), and call the other colours \(a,b\).
Subdivide the marks and delete the four zero edges, obtaining \(K=G-M\).

Lift the \(ac\)-factor to a spanning two-factor \(F\) of \(K\), contract
its circuit components, and retain the complementary \(b\)-edges.  The
result is the connected Eulerian multigraph \(R\) from
`eulerian-factor-quotient-tjoin-reduction.md`.

Choose a quotient \(U\)-join \(J\), where \(U\) is the set of eight
marked factor vertices.  Since \(R\) is Eulerian,
\[
                 J'=E(R)\setminus J
\]
is a second edge-disjoint \(U\)-join.  Thus every quotient edge, and
hence every \(b\)-edge of the core, has exactly one of two colours:
\[
       z(e)=
       \begin{cases}
       0,&e\in J,\\
       1,&e\in J'.
       \end{cases}                                      \tag{1}
\]

## 2. The equations on one marked \(ac\)-circuit

Let \(C\) be an \(ac\)-circuit containing its unique marked edge
\(s=uv\).  List the old core vertices around \(C\).  At every one of
them, the unique incident \(b\)-edge is a selected quotient port.  In
the lifted circuit, the marked edge \(s\) is replaced by the two-edge
path \(u\,t_s\,v\); the terminal \(t_s\) lies in the selected-port gap
between the ports at \(u\) and \(v\).

The exact one-terminal alternating-gap criterion says:

- the two quotient colours flanking the terminal gap must differ; and
- the endpoints of every other gap in the same alternating gap class
  must have equal quotient colours.

The edges of \(C\) alternate \(a,c,a,c,\ldots\).  The terminal gap is
the marked \(c\)-edge, so its alternating gap class consists precisely
of all \(c\)-edges of \(C\).  Therefore a lift of the complementary pair
\((J,J')\) forces
\[
 z(b_x)+z(b_y)=
 \begin{cases}
 1,&xy\in S,\\
 0,&xy\notin S
 \end{cases}
 \pmod2                                             \tag{2}
\]
for every \(c\)-edge \(xy\) on a marked \(ac\)-circuit.  Here \(b_x\)
denotes the unique \(b\)-edge incident with the core vertex \(x\).

Equation (2) is merely the local lift criterion written on the original
Tait-coloured core; it introduces no extra assumption.

## 3. The parity contradiction

Assume that every \(ac\)-circuit is marked.  Universal separation puts
at most one mark on each such circuit, so there are exactly eight of
them and they cover all vertices of \(H\).  Consequently (2) holds at
every \(c\)-edge of \(H\).

Now take any \(bc\)-circuit \(D\) containing a mark.  Such a circuit
exists, and universal separation gives
\[
                     |E(D)\cap S|=1.                  \tag{3}
\]
Sum (2) over the \(c\)-edges of \(D\).  Around the alternating
\(bc\)-circuit, every \(b\)-edge occurs once at the left endpoint of
one \(c\)-edge and once at the right endpoint of the next.  Hence every
variable \(z(b)\) occurs twice and the sum of the left sides is zero.
The sum of the right sides is one by (3).  This gives
\[
                         0=1\pmod2,
\]
a contradiction.

We have proved:

> **Complementary-quotient no-go theorem.**
> If every \(ac\)-factor circuit contains one of the universally
> separated marks, then no quotient \(U\)-join \(J\) and its complement
> \(E(R)\setminus J\) lift to two edge-disjoint \(T\)-joins in \(K\).

The proof is symmetric in the two non-mark colours.

## 4. Why the 88-vertex equality case satisfies the hypothesis

In the minimum-counterexample reduction the ambient graph has girth at
least ten.  Every marked core \(ac\)-circuit has even length, and after
subdividing its unique mark it becomes an odd ambient circuit of length
at least eleven.  Thus its core length is at least ten.

There are eight vertex-disjoint marked \(ac\)-circuits.  If
\(|V(G)|=88\), then suppression gives \(|V(H)|=80\), so their lengths
sum to at least \(8\cdot10=80\).  They therefore all have length ten
and together span \(H\).  No unmarked \(ac\)-circuit remains.

The no-go theorem applies:

> **Connected equality corollary.**
> In the connected eight-mark 88-vertex ambient equality case, no
> complementary quotient pair \(J,E(R)\setminus J\) can lift.  Any
> successful pair of edge-disjoint quotient \(U\)-joins must leave at
> least one edge of \(R\) unused.

This explains why the elementary spanning-tree/complement construction
in the Eulerian quotient is insufficient exactly at the sharp order
bound.  It does not say that noncomplementary quotient joins cannot lift.

## 5. Scope

The conclusion is deliberately narrow:

- it does not refute two-\(T\)-join packing in \(K\);
- it does not apply to an arbitrary pair of edge-disjoint quotient joins
  with unused edges;
- it does not use or prove the global minimum-support exchange step; and
- it does not change the status of five-CDC.

Its value is diagnostic: the equality case cannot be closed by choosing
the canonical tree \(U\)-join and colouring every remaining quotient edge
with the second join.  A proof must exploit unused quotient edges,
another Tait colouring/factor, a cut reduction, or a different route.

## AI-use disclosure

This reduction and exposition were produced by an OpenAI Codex agent
under human direction.  The complete parity proof is displayed above
for direct human checking.  No five-CDC resolution or human peer review
is claimed.
