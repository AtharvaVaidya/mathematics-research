import FiveCDC.Encoding

/-!
# Padding an at-most-five cover

The literature's "at most five" convention is represented here by an indexed
family with index type `Fin k` and a proof that `k ≤ 5`.  This file proves
that extending such a family by empty even edge-subsets gives exactly five
coordinates without changing any edge's coverage count.
-/

namespace FiveCDC

universe u v

open scoped BigOperators

variable {Vertex : Type u} {Edge : Type v}

/-- An indexed family with exactly `k` available coordinates. -/
abbrev KFamily (k : Nat) (Edge : Type v) := Fin k → Finset Edge

/-- Every member of a `k`-indexed family is even. -/
def AllEvenK [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex]
    (G : MultiGraph Vertex Edge) {k : Nat} (family : KFamily k Edge) : Prop :=
  ∀ slot, G.EvenEdgeSet (family slot)

/-- Every edge occurs in exactly two of the `k` indexed members. -/
def FamilyDoubleCoveredK [Fintype Edge] [DecidableEq Edge]
    {k : Nat} (family : KFamily k Edge) : Prop :=
  ∀ edge, (Finset.univ.filter fun slot => edge ∈ family slot).card = 2

/-- A `k`-coordinate Eulerian double cover.  This definition is meaningful
for every `k`; for `k < 2` it is simply uninhabited when the graph has edges. -/
def IsKCDC [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex]
    [DecidableEq Edge] (G : MultiGraph Vertex Edge)
    {k : Nat} (family : KFamily k Edge) : Prop :=
  AllEvenK G family ∧ FamilyDoubleCoveredK family

/-- The standard "at most five" formulation using an explicitly indexed
family.  Repeated members remain distinguishable by their indices. -/
def HasAtMostFiveCDC [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex]
    [DecidableEq Edge] (G : MultiGraph Vertex Edge) : Prop :=
  ∃ k : Nat, ∃ _bound : k ≤ 5, ∃ family : KFamily k Edge, IsKCDC G family

/-- The exactly-five-coordinate existential formulation. -/
def HasFiveCDC [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex]
    [DecidableEq Edge] (G : MultiGraph Vertex Edge) : Prop :=
  ∃ family : FiveFamily Edge, IsFiveCDC G family

/-- The order-preserving embedding of the first `k` indices into `Fin n`. -/
def finCastEmbedding {k n : Nat} (bound : k ≤ n) : Fin k ↪ Fin n where
  toFun slot := ⟨slot.val, lt_of_lt_of_le slot.isLt bound⟩
  inj' := by
    intro first second equal
    apply Fin.ext
    exact congrArg (fun slot : Fin n => slot.val) equal

/-- Pad a `k`-coordinate family to five coordinates with empty edge sets. -/
def padFamily {k : Nat} (_bound : k ≤ 5)
    (family : KFamily k Edge) : FiveFamily Edge :=
  fun slot =>
    if inRange : slot.val < k
      then family ⟨slot.val, inRange⟩
      else ∅

@[simp]
theorem padFamily_inRange {k : Nat} (bound : k ≤ 5)
    (family : KFamily k Edge) (slot : Fin k) :
    padFamily bound family (finCastEmbedding bound slot) = family slot := by
  simp [padFamily, finCastEmbedding]

/-- Padding preserves every Eulerian/even-subgraph condition. -/
theorem allEven_padFamily
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) {k : Nat} (bound : k ≤ 5)
    (family : KFamily k Edge) (allEven : AllEvenK G family) :
    AllEven G (padFamily bound family) := by
  intro slot
  by_cases inRange : slot.val < k
  · simpa [padFamily, inRange] using allEven ⟨slot.val, inRange⟩
  · intro vertex
    simp [padFamily, inRange, MultiGraph.degree]

/-- The selected padded slots are exactly the embedded selected original
slots.  This is the cardinality bridge used by the exact-two proof. -/
theorem filter_padFamily_eq_map
    [Fintype Edge] [DecidableEq Edge]
    {k : Nat} (bound : k ≤ 5) (family : KFamily k Edge) (edge : Edge) :
    (Finset.univ.filter fun slot : Fin 5 => edge ∈ padFamily bound family slot) =
      (Finset.univ.filter fun slot : Fin k => edge ∈ family slot).map
        (finCastEmbedding bound) := by
  apply Finset.ext
  intro slot
  simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_map]
  by_cases inRange : slot.val < k
  · let small : Fin k := ⟨slot.val, inRange⟩
    have mapped : finCastEmbedding bound small = slot := Fin.ext rfl
    constructor
    · intro selected
      exact ⟨small, by simpa [padFamily, inRange, small] using selected, mapped⟩
    · rintro ⟨original, selected, originalMapped⟩
      have values : original.val = slot.val :=
        congrArg (fun index : Fin 5 => index.val) originalMapped
      have originalSmall : original = small := Fin.ext values
      simpa [padFamily, inRange, small, originalSmall] using selected
  · constructor
    · intro selected
      simp [padFamily, inRange] at selected
    · intro mapped
      obtain ⟨small, _, equal⟩ := mapped
      have values : small.val = slot.val := congrArg Fin.val equal
      exact (inRange (values ▸ small.isLt)).elim

/-- Padding preserves exact double coverage edge by edge. -/
theorem doubleCovered_padFamily
    [Fintype Edge] [DecidableEq Edge]
    {k : Nat} (bound : k ≤ 5) (family : KFamily k Edge)
    (doubleCovered : FamilyDoubleCoveredK family) :
    FamilyDoubleCovered (padFamily bound family) := by
  intro edge
  rw [filter_padFamily_eq_map bound family edge, Finset.card_map]
  exact doubleCovered edge

/-- An at-most-five cover pads to a valid exactly-five-coordinate cover. -/
theorem isKCDC_padFamily
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) {k : Nat} (bound : k ≤ 5)
    (family : KFamily k Edge) (cover : IsKCDC G family) :
    IsFiveCDC G (padFamily bound family) :=
  ⟨allEven_padFamily G bound family cover.1,
    doubleCovered_padFamily bound family cover.2⟩

/-- "At most five" implies the five-coordinate formulation by empty padding. -/
theorem hasAtMostFiveCDC_implies_hasFiveCDC
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) :
    HasAtMostFiveCDC G → HasFiveCDC G := by
  rintro ⟨k, bound, family, cover⟩
  exact ⟨padFamily bound family, isKCDC_padFamily G bound family cover⟩

/-- Five coordinates are already an at-most-five indexed family. -/
theorem hasFiveCDC_implies_hasAtMostFiveCDC
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) :
    HasFiveCDC G → HasAtMostFiveCDC G := by
  rintro ⟨family, cover⟩
  exact ⟨5, le_rfl, family, cover⟩

/-- Machine-checked justification for treating "five" as "at most five". -/
theorem hasAtMostFiveCDC_iff_hasFiveCDC
    [Fintype Vertex] [Fintype Edge] [DecidableEq Vertex] [DecidableEq Edge]
    (G : MultiGraph Vertex Edge) :
    HasAtMostFiveCDC G ↔ HasFiveCDC G :=
  ⟨hasAtMostFiveCDC_implies_hasFiveCDC G,
    hasFiveCDC_implies_hasAtMostFiveCDC G⟩

end FiveCDC
