# Prescribed-factor lift from a Tait colouring

Date: **2026-07-31**

Status: **HUMAN-CHECKABLE THEOREM / GENUINE REDUCTION OF THE ROOTED
FIVECDC PREMISE / NOT A RESOLUTION OF FIVECDC**.

The theorem in `HUMAN-PROOF.md` says that, in a Tait-colourable cubic
graph, every prescribed circuit can be made exactly one `D5` factor.
Consequently every pair of edges in a 2-connected Tait-colourable cubic
graph is root-feasible.  In particular, the narrowed independent-root
premise needed by the edge-elimination induction is automatic whenever
the reduced graph is Tait-colourable; its unresolved domain is reduced
to non-Tait reduced graphs.

This is a direct construction, not a search result.  The two standard-library
programs are supplementary semantic replays written with different graph
representations.  Each verifies every edge pair on several infinite-family
controls and checks the local xor equations, exact factor identity, and the
inverse edge insertion.

Run:

```sh
python3 verify.py
python3 independent_check.py
sh run_all.sh
```

The construction and proof were found and drafted by OpenAI Codex agents
under human direction.  The proof is completely exposed for human checking.
AI-assisted checking is not independent human peer review.

## Priority warning

The existence theorem is **not new**.  Hoffmann-Ostenhof's Lemma 0.2 in
*A note on 5-cycle double covers* (Graphs and Combinatorics 29 (2013),
977--979; arXiv:1209.0096), citing earlier 1995/1997 sources, gives the
stronger statement that every 2-regular subgraph of a cubic graph with a
nowhere-zero 4-flow is contained in a 4-CDC.  A Tait-colourable cubic graph
has such a flow.  The value here is the explicit `D5` labelling formula and
its exact use in the project's two-root edge-insertion reduction, not a
claim of priority.
