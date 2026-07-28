import FiveCDC.Encoding

/-!
# The ten-label `D₅` flow formulation

An exact-two row is equivalently one of the ten two-element subsets of five
coordinates.  Coordinatewise incidence parity is then the conservation law
for this restricted binary flow.  This file proves the witness equivalence.
-/

namespace FiveCDC

universe u v

open scoped BigOperators

variable {Vertex : Type u} {Edge : Type v}

/-- One of the ten weight-two vectors in `𝔽₂⁵`, represented by its support. -/
abbrev D5Label := {support : Finset (Fin 5) // support.card = 2}

/-- A two-element label on every distinct edge. -/
abbrev D5Labeling (Edge : Type v) := Edge → D5Label

/-- Coordinatewise conservation of the weight-two labels at every vertex.
Incidence multiplicity makes loops cancel and preserves distinct parallel
edge contributions. -/
def IsD5Flow [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) (labeling : D5Labeling Edge) : Prop :=
  ∀ vertex coordinate,
    (∑ edge,
      if coordinate ∈ (labeling edge).1
        then G.incidenceMultiplicity vertex edge
        else 0) % 2 = 0

/-- Turn each exact-two Boolean row into its two-element support. -/
def assignmentToD5Labeling [Fintype Edge]
    (x : Assignment Edge) (exact : ExactTwo x) : D5Labeling Edge :=
  fun edge =>
    ⟨Finset.univ.filter fun coordinate => x edge coordinate = true, exact edge⟩

/-- Turn every two-element support into its characteristic Boolean row. -/
def d5LabelingToAssignment (labeling : D5Labeling Edge) : Assignment Edge :=
  fun edge coordinate => decide (coordinate ∈ (labeling edge).1)

@[simp]
theorem mem_assignmentToD5Labeling [Fintype Edge]
    (x : Assignment Edge) (exact : ExactTwo x)
    (edge : Edge) (coordinate : Fin 5) :
    coordinate ∈ (assignmentToD5Labeling x exact edge).1 ↔
      x edge coordinate = true := by
  simp [assignmentToD5Labeling]

@[simp]
theorem d5LabelingToAssignment_apply
    (labeling : D5Labeling Edge) (edge : Edge) (coordinate : Fin 5) :
    d5LabelingToAssignment labeling edge coordinate = true ↔
      coordinate ∈ (labeling edge).1 := by
  simp [d5LabelingToAssignment]

/-- Every D₅ labeling satisfies the exact-two SAT rows after taking
characteristic functions. -/
theorem d5LabelingToAssignment_exactTwo [Fintype Edge]
    (labeling : D5Labeling Edge) :
    ExactTwo (d5LabelingToAssignment labeling) := by
  intro edge
  simpa [d5LabelingToAssignment] using (labeling edge).2

/-- The D₅ conservation law is literally the incidence-XOR family after
conversion to Boolean characteristic functions. -/
theorem d5Flow_iff_assignmentParity
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) (labeling : D5Labeling Edge) :
    IsD5Flow G labeling ↔
      ParityRows G (d5LabelingToAssignment labeling) := by
  simp only [IsD5Flow, ParityRows, MultiGraph.AssignmentDegree,
    d5LabelingToAssignment_apply]

/-- Valid Boolean assignments and restricted `D₅` flows are inverse witness
types. -/
def validAssignmentEquivD5Flow
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) :
    {x : Assignment Edge // ValidAssignment G x} ≃
      {labeling : D5Labeling Edge // IsD5Flow G labeling} where
  toFun x := by
    refine ⟨assignmentToD5Labeling x.1 x.2.1, ?_⟩
    intro vertex coordinate
    simpa [IsD5Flow, assignmentToD5Labeling,
      MultiGraph.AssignmentDegree] using x.2.2 vertex coordinate
  invFun labeling := by
    refine ⟨d5LabelingToAssignment labeling.1, ?_⟩
    exact ⟨d5LabelingToAssignment_exactTwo labeling.1,
      (d5Flow_iff_assignmentParity G labeling.1).mp labeling.2⟩
  left_inv x := by
    apply Subtype.ext
    funext edge coordinate
    cases value : x.1 edge coordinate <;>
      simp [d5LabelingToAssignment, assignmentToD5Labeling, value]
  right_inv labeling := by
    apply Subtype.ext
    funext edge
    apply Subtype.ext
    ext coordinate
    simp [assignmentToD5Labeling, d5LabelingToAssignment]

/-- Consequently the `D₅`-flow witnesses and five-CDC witnesses are exactly
equivalent for every fixed finite multigraph. -/
def d5FlowEquivFiveCDC
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) :
    {labeling : D5Labeling Edge // IsD5Flow G labeling} ≃
      {family : FiveFamily Edge // IsFiveCDC G family} :=
  (validAssignmentEquivD5Flow G).symm.trans (validAssignmentEquivFiveCDC G)

end FiveCDC
