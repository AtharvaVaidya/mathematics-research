# Missing rooted base pairs force coordinate-cut certificates

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE NECESSARY CONDITION / NOT AN ELIMINATION**.

This note converts every failure of the rooted three-base-pair target
into an ordinary cut certificate.  It is a structural reduction, not a
proof of universal base-pair closure.

## 1. Setup

Let
\[
 D_5=\{A\subseteq\{0,1,2,3,4\}:|A|=2\},
\]
with addition given by symmetric difference.  A \(D_5\)-labeling of a
cubic three-pole assigns a member of \(D_5\) to every proper edge and
boundary semiedge so that the incident labels sum to zero at every
proper vertex.  Normalize the three ordered boundary labels to
\[
                         01,\quad 02,\quad 12.                 \tag{1}
\]
Let \(r\) be a proper root edge and let
\({\cal R}(Q,r)\subseteq D_5\) be its exact signature.

For a coordinate \(a\), write
\[
 E_{\bar a}(\phi)=
 \{e\in E(Q):a\notin\phi(e)\}.                                \tag{2}
\]
This is a spanning subgraph of the proper core; boundary semiedges are
not included.  Put
\[
                  h_a=\{0,1,2,3,4\}\setminus\{a\}.             \tag{3}
\]

## 2. Complement-cycle switch

> **Lemma 2.1.**  
> Suppose \(a\notin\phi(r)\).  If \(r\) lies on a proper cycle \(C\)
> of \(E_{\bar a}(\phi)\), then
> \[
> \phi'(e)=
> \begin{cases}
>   \phi(e)\mathbin{\triangle}h_a,&e\in C,\\
>   \phi(e),&e\notin C
> \end{cases}                                                  \tag{4}
> \]
> is another \(D_5\)-labeling with the same boundary labels.  In
> particular,
> \[
>             \phi(r)\mathbin{\triangle}h_a
>             \in{\cal R}(Q,r).                               \tag{5}
> \]

### Proof

Every label on \(C\) is a two-subset of the four-set \(h_a\).
Symmetric difference with \(h_a\) replaces it by its complementary
two-subset, so every changed label remains in \(D_5\).  At each vertex
of \(C\), the same vector \(h_a\) is added to exactly two incident
edges and hence cancels over \(\mathbb F_2\).  Other vertices are
unchanged.  Because \(C\) consists only of proper edges, the three
boundary labels (1) are unchanged. \(\square\)

> **Corollary 2.2 (missing mate gives a bridge).**  
> Let \(A=\phi(r)\), with \(a\notin A\), and put
> \(B=A\triangle h_a\).  If \(B\notin{\cal R}(Q,r)\), then \(r\)
> is a bridge of \(E_{\bar a}(\phi)\).

### Proof

In a finite undirected graph an edge is not a bridge exactly when it
lies on a cycle.  Lemma 2.1 would otherwise realize \(B\). \(\square\)

This is stronger than merely saying that one chosen root cycle blocks a
translation: the missing root value forces *every* root cycle to use a
label containing \(a\).

## 3. The three base pairs

The three proposed base pairs are
\[
\begin{aligned}
 P_0&=\{12,03,04\},\\
 P_1&=\{02,13,14\},\\
 P_2&=\{01,23,24\}.                                           \tag{6}
\end{aligned}
\]
The complement switches relating the two parts of each pair are:

```text
12 <-> 03  in the four-set avoiding 4
12 <-> 04  in the four-set avoiding 3
02 <-> 13  in the four-set avoiding 4
02 <-> 14  in the four-set avoiding 3
01 <-> 23  in the four-set avoiding 4
01 <-> 24  in the four-set avoiding 3
```

The exact signature is invariant under the transposition \(3\leftrightarrow
4\), since that transposition fixes all three boundary labels in (1).

> **Theorem 3.1 (base-pair cut certificate).**  
> Suppose \({\cal R}(Q,r)\ne\varnothing\) contains a label other than
> \(34\), but contains none of the three base pairs in (6).  Then there
> is a labeling \(\phi\) and a coordinate
> \(a\in\{3,4\}\) such that \(r\) is a bridge of
> \(E_{\bar a}(\phi)\).
>
> More precisely:
>
> - if an inner label \(12,02,\) or \(01\) occurs without its outer
>   orbit, then in every labeling with that root label, \(r\) is a
>   bridge of both \(E_{\bar3}(\phi)\) and
>   \(E_{\bar4}(\phi)\);
> - if an outer orbit occurs without its corresponding inner label,
>   then a labeling with the member incident to \(3\) makes \(r\) a
>   bridge of \(E_{\bar4}(\phi)\), and its
>   \(3\leftrightarrow4\) image makes \(r\) a bridge of
>   \(E_{\bar3}(\phi)\).

### Proof

Every label other than \(34\) belongs to exactly one of the three sets
in (6).  If it is an inner label, failure to contain its base pair and
the \(3\leftrightarrow4\) invariance exclude both outer mates.  Apply
Corollary 2.2 to the two lines of the table above.  If it is an outer
label, failure of the base pair excludes the inner mate, and the same
corollary applies. \(\square\)

The remaining one-label possibility has a similarly rigid form:

> **Corollary 3.2.**  
> If \({\cal R}(Q,r)=\{34\}\), then in every realizing labeling,
> \(r\) is simultaneously a bridge of
> \[
> E_{\bar0}(\phi),\qquad E_{\bar1}(\phi),\qquad
> E_{\bar2}(\phi).                                             \tag{7}
> \]

### Proof

Complementation in the four-sets avoiding \(0,1,2\) sends \(34\) to
\(12,02,01\), respectively.  All three values are absent, so apply
Corollary 2.2. \(\square\)

## 4. Ordinary cuts

A bridge certificate has an immediate cut form.  If \(r\) is a bridge
of \(E_{\bar a}(\phi)\), one component \(X\) after deleting \(r\)
satisfies
\[
 \delta_Q(X)=\{r\}\mathbin{\dot\cup}F_a,\qquad
 F_a\subseteq\{e:a\in\phi(e)\}.                               \tag{8}
\]
Here and throughout this section, \(\delta_Q(X)\) denotes the edge cut
in the **proper core** of \(Q\); the three boundary semiedges are not
members of this cut.  This is the same convention used in (2), where
only proper edges belong to \(E_{\bar a}(\phi)\).

When \(a=3\) or \(4\), none of the boundary labels (1) uses \(a\).
Consequently the coordinate-\(a\) support on proper edges is Eulerian,
so every proper cut meets it evenly:
\[
                              |F_a|\equiv0\pmod2.              \tag{9}
\]
If \(r\) is a nonbridge of the unlabelled core, \(F_a\ne\varnothing\).
Thus every certificate supplied by Theorem 3.1 is an odd proper cut of
size at least three, containing \(r\), whose other edges all carry one
common outer coordinate.

For the special \(34\) signature, coordinates \(0,1,2\) occur on the
boundary.  Equation (8) still holds, while the parity of \(F_a\) equals
the number modulo two of boundary semiedges containing \(a\) whose
terminal lies in \(X\).

## 5. Consequence for the exceptional cyclic-three fork

The equality-only exceptional four-type orientation requires both
shore signatures to be the same singleton among
\[
                              01,\ 02,\ 12,\ 34.               \tag{10}
\]
For the first three values, Corollary 2.2 supplies two simultaneous
outer-coordinate bridge cuts on each realizing shore.  For \(34\),
Corollary 3.2 supplies three simultaneous inner-coordinate bridge
cuts.  Hence any surviving equality-only cap is not merely
cycle-translation-rigid: it carries this explicit family of ordinary
root cuts.

To finish the cyclic-three branch one would need to show that these
coordinate cuts are reducible under the inherited minimal-cap
hypotheses, or construct a shore realizing them.  Neither step is
proved here.  The cyclically-four-edge-connected cap fork is also
untouched.

## AI-use disclosure

OpenAI Codex agents, under human direction, found and drafted this
reduction.  The proof above is elementary and intended for line-by-line
human checking.  It has not been independently peer reviewed, and no
novelty claim is made.
