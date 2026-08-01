# Eight-to-five triangle-state rigidity

Date: **2026-07-31**

Status: **PASS / sharper partial no-go / FiveCDC unresolved**.

This package moves one level beyond a context-free lookup on old
coordinate pairs.  A rule may be chosen for the supplied graph and may
depend on the complete local Oum affine triangle (T_v\), but equal local
states must reuse equal local recolourings.

The new 12-vertex simple bridgeless witness has eleven distinct local
states, with state `012` repeated.  For every old pair, its
state-adjacency graph is connected.  Edge agreement therefore transports
one output label across every occurrence of that pair.  The eleven state
rows have full rank ten in the cycle space of `K6`, forcing a coboundary;
`omega(R5)=5` then rules out weight-two labels on all pairs.

The graph is explicitly 3-edge-colourable.  Its positive FiveCDC uses
different local permutations at the two occurrences of state `012`,
pinpointing the extra vertex context that repairs it.  Allowing arbitrary
vertex-specific local rules is exactly equivalent to FiveCDC, so no
resolution is claimed.

The order 12 is sharp for this connected-state/full-rank mechanism.  An
order-10 candidate would need ten distinct independent state rows and all
fifteen pair columns.  Even pair incidence would then make every pair
occur twice, so the xor of the ten rows would be zero and their rank at
most nine.

## Reproduction

```sh
./run_all.sh
```

The primary checker reconstructs the explicitly labelled cover.  The
independent checker instead decodes graph6, infers labels from block
intersections, uses Tarjan's bridge algorithm, enumerates all scalar
state-rule solutions, exhausts all six-subsets of `R5`, and discovers a
Tait colouring without importing the first implementation.

Both programs use only the Python standard library.  Both are AI-written;
“independent” means independently structured code, not human review.

## Literature and novelty caveat

A bounded primary-source comparison with Oum arXiv:2607.16356v2,
Hušek--Šámal arXiv:2607.24724v1, and Král' et al., *European Journal of
Combinatorics* 30 (2009), found no exact triangle-state transport theorem
or this sharp witness.  Priority is unestablished.  Configuration
homomorphisms and the Desargues/FiveCDC equivalence are established prior
art and are not claimed as new.

## AI-use disclosure

OpenAI Codex agents directed by Atharva Vaidya found the witness, wrote
the proofs and code, ran the checks, and prepared this package.  Human
proof checking and specialist prior-art review remain necessary.
