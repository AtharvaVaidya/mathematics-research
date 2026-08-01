# A fixed-pair packing--switch equivalence for nowhere-zero
# \(\mathbb F_2^3\)-flows

Date: **2026-07-28**.

Status: **HUMAN-CHECKABLE EXACT REFORMULATION / NOT A FIVECDC
RESOLUTION**.

## Scope and conventions

Let \(G\) be a finite loopless cubic graph; parallel edges are allowed.
Every edge set is identified with its incidence vector over
\(\mathbb F_2\). Thus \(\partial A\) denotes the set of vertices incident
with an odd number of edges of \(A\), and a **binary cycle** means an edge
set \(X\) with \(\partial X=\varnothing\). A \(T\)-join is an edge set
\(J\) with \(\partial J=T\). No connectedness or bridgelessness hypothesis
is needed for the equivalence below.

Let
\[
 f:E(G)\longrightarrow V-\{0\},\qquad V=\mathbb F_2^3,
\]
be a nowhere-zero flow. Choose a nonzero linear functional
\(\lambda:V\to\mathbb F_2\) and \(a\in V\) such that
\(\lambda(a)=1\). Define
\[
 F=\{e:\lambda(f(e))=1\},\quad
 M=\{e:f(e)=a\},\quad T=\partial M,\quad K=G-M.
\]
The set \(F\) is Eulerian because \(\lambda\circ f\) is a binary flow.
Also \(M\subseteq F\). Put \(J_0=F-M\). Then
\[
 \partial J_0=\partial(F\mathbin\triangle M)=T,
\]
so \(J_0\) is a \(T\)-join in \(K\).

For a binary cycle \(X\), an \(a\)-switch replaces \(f\) by
\[
 f^X(e)=f(e)+a\,1_X(e).
\]
This remains a flow. It is nowhere zero precisely when \(X\cap M\) is
empty, equivalently when \(X\subseteq K\).

## Theorem

The following are equivalent.

1. \(K\) contains two edge-disjoint \(T\)-joins.
2. There is a binary cycle \(X\subseteq K\) such that, after the
   \(a\)-switch, every component of
   \[
   H^X=(V(G),\{e:\lambda(f^X(e))=0\})
   \]
   contains an even number of vertices of \(T\).

The binary cycles \(X\subseteq K\) are in bijection with the \(T\)-joins
\(J_1\subseteq K\) by
\[
                         X=J_0\mathbin\triangle J_1.       \tag{1}
\]
Under this correspondence,
\[
 \{e:\lambda(f^X(e))=1\}=M\cup J_1,\qquad
 H^X=K-J_1.                                               \tag{2}
\]

### Proof

Because \(\partial J_0=T\), equation (1) gives
\[
 \partial X=\partial J_0\mathbin\triangle\partial J_1
            =T\mathbin\triangle T=\varnothing.
\]
Conversely, if \(X\subseteq K\) is a binary cycle, then
\(J_1=J_0\mathbin\triangle X\) has boundary \(T\). This proves the
bijection.

The switch is legal because \(X\cap M=\varnothing\). Since
\(\lambda(a)=1\), switching toggles the scalar support \(F\) exactly on
\(X\). Moreover \(F=M\mathbin{\dot\cup}J_0\), so
\[
\begin{aligned}
 \{e:\lambda(f^X(e))=1\}
 &=F\mathbin\triangle X\\
 &=(M\mathbin{\dot\cup}J_0)
   \mathbin\triangle(J_0\mathbin\triangle J_1)\\
 &=M\cup J_1.
\end{aligned}
\]
Here \(M\cap J_1=\varnothing\) because \(J_1\subseteq K\). Taking the
edge complement proves (2).

An elementary component criterion says that a graph \(L\) contains a
\(T\)-join if and only if every component of \(L\) contains an even
number of vertices of \(T\). Indeed, necessity follows by the
handshaking lemma; for sufficiency, pair the terminals inside each
component and take the symmetric difference of paths joining the pairs.
Consequently the switched component condition holds exactly when
\(K-J_1\) contains a \(T\)-join \(J_2\). This is exactly the assertion
that \(J_1,J_2\) are edge-disjoint \(T\)-joins in \(K\). All steps
reverse, proving the theorem. \(\square\)

## Consequences and limits

- In a cubic graph, \(M\) is automatically a matching: two incident
  \(a\)-edges would force the third incident flow value to be zero.
  Hence \(T\) is the set of endpoints of \(M\).
- The packing property depends on \(f\) and \(a\), but not on the choice
  of \(\lambda\) with \(\lambda(a)=1\). The switch support in (1) does
  depend on \(\lambda\).
- A binary cycle may be disconnected. Decomposing it into circuits
  yields a finite sequence of legal circuit switches, because no
  component meets \(M\). The theorem does **not** promise one connected
  simple-cycle switch.
- If \(M=\varnothing\), the two empty \(T\)-joins give a packing.
- If \(G\) is 3-edge-connected and \(M\) is a singleton \(uv\), then
  \(G-uv\) has two edge-disjoint \(u\)-\(v\) paths, giving a packing.
- This theorem is a fixed-flow reformulation, not a proof that a suitable
  pair \((f,a)\) exists in every bridgeless cubic graph. That remaining
  existential assertion is identified with the Five-Cycle Double Cover
  Conjecture in Hušek--Šámal, Theorem 3.16, Observation 3.15, and
  Conjecture 3.19.

## Relation to five-cycle double covers

The quotient of \(f|_K\) by \(\langle a\rangle\) is a nowhere-zero
\(\mathbb F_2^2\)-flow on \(K\). If \(J_1,J_2\) are a packing, then
\[
 C_1=M\cup J_1,\qquad C_2=M\cup J_2
\]
are Eulerian and \(C_1\cap C_2=M\). Thus the theorem is the switch form
of the matching/two-cycle condition used in the
Hoffmann--Ostenhof-type formulation; it is not a weaker oracle.

## Reference

R. Hušek and R. Šámal, *Exponentially Many Circuit Double Covers*,
arXiv:2607.24724v1 (2026),
[abstract](https://arxiv.org/abs/2607.24724),
[PDF](https://arxiv.org/pdf/2607.24724).

## AI-use disclosure

This note was developed and checked by OpenAI Codex agents using
GPT-5-series models under the direction of Atharva Vaidya. A separately
prompted algebra agent checked the equivalence for hidden connectedness,
simplicity, and support assumptions; that is an AI cross-check, not
independent human review. The proof is included in full so that every step
can be checked independently by a human. Human mathematical review is still
required before citation or publication.
