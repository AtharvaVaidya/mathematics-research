package main

import (
	"fmt"
	"math/bits"
)

var twoSubsetMasks = [...]uint8{
	0b00011, // 0,1
	0b00101, // 0,2
	0b01001, // 0,3
	0b10001, // 0,4
	0b00110, // 1,2
	0b01010, // 1,3
	0b10010, // 1,4
	0b01100, // 2,3
	0b10100, // 2,4
	0b11000, // 3,4
}

type SolveResult struct {
	Status     string      `json:"status"`
	Exhaustive bool        `json:"exhaustive"`
	Nodes      uint64      `json:"search_nodes"`
	Witness    *Assignment `json:"-"`
	Note       string      `json:"note"`
}

type searchState struct {
	masks     []int8
	parity    []uint8
	remaining []int
}

func (s *searchState) clone() *searchState {
	return &searchState{
		masks:     append([]int8(nil), s.masks...),
		parity:    append([]uint8(nil), s.parity...),
		remaining: append([]int(nil), s.remaining...),
	}
}

func isTwoSubset(mask uint8) bool {
	return mask < 32 && bits.OnesCount8(mask) == 2
}

func assignMask(g *Graph, s *searchState, edgeID int, mask uint8) bool {
	if !isTwoSubset(mask) {
		return false
	}
	if s.masks[edgeID] >= 0 {
		return uint8(s.masks[edgeID]) == mask
	}
	s.masks[edgeID] = int8(mask)
	e := g.Edges[edgeID]
	if e.U != e.V {
		s.parity[e.U] ^= mask
		s.parity[e.V] ^= mask
		s.remaining[e.U]--
		s.remaining[e.V]--
	}
	return true
}

func propagate(g *Graph, incident [][]int, s *searchState) bool {
	for {
		changed := false
		for v := 0; v < g.N; v++ {
			switch s.remaining[v] {
			case 0:
				if s.parity[v] != 0 {
					return false
				}
			case 1:
				edgeID := -1
				for _, candidate := range incident[v] {
					if s.masks[candidate] < 0 {
						edgeID = candidate
						break
					}
				}
				if edgeID < 0 || !assignMask(g, s, edgeID, s.parity[v]) {
					return false
				}
				changed = true
			}
		}
		if !changed {
			return true
		}
	}
}

func chooseBranchEdge(g *Graph, s *searchState) int {
	bestEdge, bestScore := -1, int(^uint(0)>>1)
	for _, e := range g.Edges {
		if s.masks[e.ID] >= 0 {
			continue
		}
		if e.U == e.V {
			return e.ID
		}
		score := s.remaining[e.U] + s.remaining[e.V]
		if score < bestScore {
			bestEdge, bestScore = e.ID, score
		}
	}
	return bestEdge
}

func nonLoopComponents(g *Graph, incident [][]int) [][]int {
	seenVertex := make([]bool, g.N)
	seenEdge := make([]bool, len(g.Edges))
	var components [][]int
	for root := 0; root < g.N; root++ {
		if seenVertex[root] || len(incident[root]) == 0 {
			continue
		}
		seenVertex[root] = true
		stack := []int{root}
		var edgeIDs []int
		for len(stack) != 0 {
			v := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			for _, edgeID := range incident[v] {
				if !seenEdge[edgeID] {
					seenEdge[edgeID] = true
					edgeIDs = append(edgeIDs, edgeID)
				}
				e := g.Edges[edgeID]
				w := e.U
				if w == v {
					w = e.V
				}
				if !seenVertex[w] {
					seenVertex[w] = true
					stack = append(stack, w)
				}
			}
		}
		components = append(components, edgeIDs)
	}
	return components
}

// SolveExactly performs deterministic exhaustive backtracking over the ten
// two-subsets. It uses parity propagation whenever a vertex has one
// unassigned non-loop incident edge. Coordinate symmetry fixes one edge per
// non-loop connected component to {0,1}; at a 3-non-loop-regular anchor
// vertex, the stabilizer symmetry fixes a second edge to {0,2}.
//
// maxNodes == 0 means unlimited. An UNSAT answer is exhaustive but is not a
// proof certificate and must never be used as a counterexample certificate.
func SolveExactly(g *Graph, maxNodes uint64) (SolveResult, error) {
	if err := g.Validate(); err != nil {
		return SolveResult{}, err
	}
	incident := nonLoopIncidence(g)
	initial := &searchState{
		masks:     make([]int8, len(g.Edges)),
		parity:    make([]uint8, g.N),
		remaining: make([]int, g.N),
	}
	for i := range initial.masks {
		initial.masks[i] = -1
	}
	for v := range incident {
		initial.remaining[v] = len(incident[v])
	}
	// Loops never enter a parity condition, so choose the first label.
	for _, e := range g.Edges {
		if e.U == e.V {
			assignMask(g, initial, e.ID, twoSubsetMasks[0])
		}
	}
	for _, component := range nonLoopComponents(g, incident) {
		anchor := component[0]
		for _, id := range component[1:] {
			if id < anchor {
				anchor = id
			}
		}
		if !assignMask(g, initial, anchor, twoSubsetMasks[0]) {
			return SolveResult{}, fmt.Errorf("internal anchor assignment failure")
		}
		e := g.Edges[anchor]
		anchorVertex := e.U
		if len(incident[anchorVertex]) != 3 && len(incident[e.V]) == 3 {
			anchorVertex = e.V
		}
		if len(incident[anchorVertex]) == 3 {
			second := -1
			for _, id := range incident[anchorVertex] {
				if id != anchor && (second < 0 || id < second) {
					second = id
				}
			}
			if second >= 0 && !assignMask(g, initial, second, twoSubsetMasks[1]) {
				return SolveResult{}, fmt.Errorf("internal cubic symmetry assignment failure")
			}
		}
	}

	var nodes uint64
	limited := false
	var dfs func(*searchState) *Assignment
	dfs = func(s *searchState) *Assignment {
		if maxNodes != 0 && nodes >= maxNodes {
			limited = true
			return nil
		}
		nodes++
		if !propagate(g, incident, s) {
			return nil
		}
		edgeID := chooseBranchEdge(g, s)
		if edgeID < 0 {
			masks := make([]uint8, len(s.masks))
			for i, mask := range s.masks {
				if mask < 0 {
					return nil
				}
				masks[i] = uint8(mask)
			}
			return &Assignment{Masks: masks}
		}
		for _, mask := range twoSubsetMasks {
			child := s.clone()
			if assignMask(g, child, edgeID, mask) {
				if witness := dfs(child); witness != nil {
					return witness
				}
			}
			if limited {
				return nil
			}
		}
		return nil
	}
	witness := dfs(initial)
	if witness != nil {
		return SolveResult{
			Status:     "SAT",
			Exhaustive: false,
			Nodes:      nodes,
			Witness:    witness,
			Note:       "witness checked by direct incidence-parity verifier",
		}, nil
	}
	if limited {
		return SolveResult{
			Status:     "UNKNOWN",
			Exhaustive: false,
			Nodes:      nodes,
			Note:       "node limit reached; no logical conclusion",
		}, nil
	}
	return SolveResult{
		Status:     "UNSAT",
		Exhaustive: true,
		Nodes:      nodes,
		Note:       "exhaustive backtracking result only; NOT a checkable UNSAT certificate",
	}, nil
}
