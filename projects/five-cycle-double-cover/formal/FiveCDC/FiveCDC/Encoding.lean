import Mathlib.Data.Finset.Card
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
# The fixed-graph five-cycle-double-cover encoding

This file formalizes only the semantic correspondence used by the search
project.  It does not prove that a five-cycle double cover exists.

An undirected multigraph is represented by finite vertex and edge types and
an ordered pair of endpoints for every edge.  The endpoint order has no effect
on any definition below.  Different values of the edge type remain different
parallel edges.  A loop has the same endpoint twice and therefore contributes
two incidences to its vertex degree.
-/

namespace FiveCDC

universe u v

open scoped BigOperators

/-- Finite undirected multigraph data.  Finiteness is supplied by type-class
arguments to the definitions that enumerate vertices or edges. -/
structure MultiGraph (Vertex : Type u) (Edge : Type v) where
  ends : Edge → Vertex × Vertex

variable {Vertex : Type u} {Edge : Type v}

/-- Incidence multiplicity of an edge at a vertex: zero, one, or two. -/
def MultiGraph.incidenceMultiplicity [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) (vertex : Vertex) (edge : Edge) : Nat :=
  (if (G.ends edge).1 = vertex then 1 else 0) +
    (if (G.ends edge).2 = vertex then 1 else 0)

/-- Degree in the spanning subgraph selected by `edges`, counting both
incidences of a loop and treating parallel edge values separately. -/
def MultiGraph.degree [Fintype Edge] [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) (edges : Finset Edge) (vertex : Vertex) : Nat :=
  ∑ edge ∈ edges, G.incidenceMultiplicity vertex edge

/-- An Eulerian/even edge-subset means that every vertex degree is even.
Connectivity and 2-regularity are deliberately not required. -/
def MultiGraph.EvenEdgeSet [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) (edges : Finset Edge) : Prop :=
  ∀ vertex, G.degree edges vertex % 2 = 0

/-- Five indexed edge-subsets.  Repetitions and empty subsets are allowed. -/
abbrev FiveFamily (Edge : Type v) := Fin 5 → Finset Edge

/-- Every indexed member of the family is an even edge-subset. -/
def AllEven [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) (family : FiveFamily Edge) : Prop :=
  ∀ slot, G.EvenEdgeSet (family slot)

/-- Every edge belongs to exactly two of the five indexed coordinates. -/
def FamilyDoubleCovered [Fintype Edge] [DecidableEq Edge]
    (family : FiveFamily Edge) : Prop :=
  ∀ edge, (Finset.univ.filter fun slot => edge ∈ family slot).card = 2

/-- The intended fixed-graph five-cycle-double-cover predicate. -/
def IsFiveCDC [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex]
    [DecidableEq Edge] (G : MultiGraph Vertex Edge)
    (family : FiveFamily Edge) : Prop :=
  AllEven G family ∧ FamilyDoubleCovered family

/-- Boolean variables `x[edge,slot]`. -/
abbrev Assignment (Edge : Type v) := Edge → Fin 5 → Bool

/-- Integer exact-two rows of the SAT encoding. -/
def ExactTwo [Fintype Edge] (x : Assignment Edge) : Prop :=
  ∀ edge, (Finset.univ.filter fun slot => x edge slot = true).card = 2

/-- The incidence sum in one vertex/slot row. -/
def MultiGraph.AssignmentDegree [Fintype Edge] [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) (x : Assignment Edge)
    (vertex : Vertex) (slot : Fin 5) : Nat :=
  ∑ edge, if x edge slot = true then G.incidenceMultiplicity vertex edge else 0

/-- Native-XOR semantics: every incidence row has parity zero.  Because
`incidenceMultiplicity` is two on a loop, a selected loop cancels modulo two. -/
def ParityRows [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) (x : Assignment Edge) : Prop :=
  ∀ vertex slot, G.AssignmentDegree x vertex slot % 2 = 0

/-- The complete fixed-graph SAT/XOR condition. -/
def ValidAssignment [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) (x : Assignment Edge) : Prop :=
  ExactTwo x ∧ ParityRows G x

/-- Read the five Boolean columns as five finite edge sets. -/
def decode [Fintype Edge] [DecidableEq Edge]
    (x : Assignment Edge) : FiveFamily Edge :=
  fun slot => Finset.univ.filter fun edge => x edge slot = true

/-- Take characteristic functions of five indexed edge sets. -/
def encode [DecidableEq Edge] (family : FiveFamily Edge) : Assignment Edge :=
  fun edge slot => decide (edge ∈ family slot)

@[simp]
theorem mem_decode [Fintype Edge] [DecidableEq Edge]
    (x : Assignment Edge) (edge : Edge) (slot : Fin 5) :
    edge ∈ decode x slot ↔ x edge slot = true := by
  simp [decode]

@[simp]
theorem encode_apply [DecidableEq Edge]
    (family : FiveFamily Edge) (edge : Edge) (slot : Fin 5) :
    encode family edge slot = true ↔ edge ∈ family slot := by
  simp [encode]

/-- Encoding after decoding recovers every Boolean variable. -/
@[simp]
theorem encode_decode [Fintype Edge] [DecidableEq Edge]
    (x : Assignment Edge) : encode (decode x) = x := by
  funext edge slot
  cases value : x edge slot <;> simp [encode, decode, value]

/-- Decoding after encoding recovers every indexed edge set. -/
@[simp]
theorem decode_encode [Fintype Edge] [DecidableEq Edge]
    (family : FiveFamily Edge) : decode (encode family) = family := by
  funext slot
  ext edge
  simp

/-- The degree of a decoded edge set is exactly the corresponding incidence
sum used in the XOR row. -/
theorem degree_decode [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) (x : Assignment Edge)
    (vertex : Vertex) (slot : Fin 5) :
    G.degree (decode x slot) vertex = G.AssignmentDegree x vertex slot := by
  simp only [MultiGraph.degree, MultiGraph.AssignmentDegree, decode]
  rw [Finset.sum_filter]

/-- The parity rows preserve and reflect the Eulerian/even-subgraph
conditions of all five decoded coordinates. -/
theorem parityRows_iff_decodedAllEven
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) (x : Assignment Edge) :
    ParityRows G x ↔ AllEven G (decode x) := by
  constructor
  · intro parity slot vertex
    rw [degree_decode]
    exact parity vertex slot
  · intro even vertex slot
    rw [← degree_decode]
    exact even slot vertex

/-- The exact-two rows preserve and reflect indexed double coverage. -/
theorem exactTwo_iff_decodedFamilyDoubleCovered
    [Fintype Edge] [DecidableEq Edge] (x : Assignment Edge) :
    ExactTwo x ↔ FamilyDoubleCovered (decode x) := by
  simp [ExactTwo, FamilyDoubleCovered]

/-- Main semantic theorem: the mandatory SAT/XOR constraints are exactly the
intended five indexed Eulerian edge-subsets with exact double coverage. -/
theorem validAssignment_iff_decodedIsFiveCDC
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) (x : Assignment Edge) :
    ValidAssignment G x ↔ IsFiveCDC G (decode x) := by
  constructor
  · intro valid
    exact ⟨(parityRows_iff_decodedAllEven G x).mp valid.2,
      (exactTwo_iff_decodedFamilyDoubleCovered x).mp valid.1⟩
  · intro cover
    exact ⟨(exactTwo_iff_decodedFamilyDoubleCovered x).mpr cover.2,
      (parityRows_iff_decodedAllEven G x).mpr cover.1⟩

/-- Characteristic functions satisfy the encoding exactly when the original
five indexed edge sets form a five-cycle double cover. -/
theorem validAssignment_encode_iff_isFiveCDC
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) (family : FiveFamily Edge) :
    ValidAssignment G (encode family) ↔ IsFiveCDC G family := by
  rw [validAssignment_iff_decodedIsFiveCDC, decode_encode]

/-- The correspondence is a genuine equivalence of finite witnesses, not
only an equisatisfiability statement. -/
def validAssignmentEquivFiveCDC
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) :
    {x : Assignment Edge // ValidAssignment G x} ≃
      {family : FiveFamily Edge // IsFiveCDC G family} where
  toFun x :=
    ⟨decode x.1, (validAssignment_iff_decodedIsFiveCDC G x.1).mp x.2⟩
  invFun family :=
    ⟨encode family.1,
      (validAssignment_encode_iff_isFiveCDC G family.1).mpr family.2⟩
  left_inv x := by
    apply Subtype.ext
    exact encode_decode x.1
  right_inv family := by
    apply Subtype.ext
    exact decode_encode family.1

/-- A loop contributes exactly two incidences at its endpoint. -/
@[simp]
theorem incidenceMultiplicity_loop [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) (edge : Edge) (vertex : Vertex)
    (isLoop : G.ends edge = (vertex, vertex)) :
    G.incidenceMultiplicity vertex edge = 2 := by
  simp [MultiGraph.incidenceMultiplicity, isLoop]

/-- Consequently any multiple of a loop's incidence contribution is zero
modulo two, while its Boolean membership remains a separate exact-two bit. -/
theorem loop_incidence_cancels [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) (edge : Edge) (vertex : Vertex)
    (isLoop : G.ends edge = (vertex, vertex)) (coefficient : Nat) :
    (coefficient * G.incidenceMultiplicity vertex edge) % 2 = 0 := by
  simp [incidenceMultiplicity_loop G edge vertex isLoop]

/-- Parallel edges are represented by distinct edge values with the same
unordered endpoint pair.  The disjunction makes the definition independent
of the arbitrary order in which each edge's endpoints are stored. -/
def MultiGraph.Parallel (G : MultiGraph Vertex Edge) (first second : Edge) : Prop :=
  first ≠ second ∧
    (G.ends first = G.ends second ∨
      G.ends first = ((G.ends second).2, (G.ends second).1))

/-- Distinct parallel edges occupy two different positions in an edge set. -/
theorem parallel_pair_card [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) (first second : Edge)
    (parallel : G.Parallel first second) :
    ({first, second} : Finset Edge).card = 2 := by
  simp [parallel.1]

end FiveCDC
