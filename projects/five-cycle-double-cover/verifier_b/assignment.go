package main

import (
	"bufio"
	"fmt"
	"io"
	"math/bits"
	"strings"
)

// Assignment stores the five membership bits for each indexed edge.
type Assignment struct {
	Masks []uint8
}

// ParseAssignment parses:
//
//	p 5cdc 1 <number-of-edges>
//	a <edge-id> <x0> <x1> <x2> <x3> <x4>
func ParseAssignment(r io.Reader, expectedEdges int) (*Assignment, error) {
	scanner := bufio.NewScanner(r)
	scanner.Buffer(make([]byte, 4096), 16*1024*1024)
	line := 0
	header, err := nextRecord(scanner, &line)
	if err != nil {
		return nil, fmt.Errorf("assignment header: %w", err)
	}
	if len(header) != 4 || header[0] != "p" || header[1] != "5cdc" || header[2] != "1" {
		return nil, fmt.Errorf("line %d: expected 'p 5cdc 1 <m>'", line)
	}
	m, err := nonnegativeInt(header[3], "assignment edge count")
	if err != nil {
		return nil, fmt.Errorf("line %d: %w", line, err)
	}
	if m != expectedEdges {
		return nil, fmt.Errorf("assignment has %d edges; graph has %d", m, expectedEdges)
	}
	a := &Assignment{Masks: make([]uint8, m)}
	seen := make([]bool, m)
	for record := 0; record < m; record++ {
		fields, err := nextRecord(scanner, &line)
		if err != nil {
			return nil, fmt.Errorf("assignment record %d: %w", record, err)
		}
		if len(fields) != 7 || fields[0] != "a" {
			return nil, fmt.Errorf("line %d: expected 'a <id> <x0> <x1> <x2> <x3> <x4>'", line)
		}
		id, err := nonnegativeInt(fields[1], "assignment edge ID")
		if err != nil {
			return nil, fmt.Errorf("line %d: %w", line, err)
		}
		if id >= m {
			return nil, fmt.Errorf("line %d: edge ID %d outside [0,%d)", line, id, m)
		}
		if seen[id] {
			return nil, fmt.Errorf("line %d: duplicate edge ID %d", line, id)
		}
		var mask uint8
		for i := 0; i < 5; i++ {
			if fields[i+2] != "0" && fields[i+2] != "1" {
				return nil, fmt.Errorf("line %d: coordinate must be 0 or 1, got %q", line, fields[i+2])
			}
			if fields[i+2] == "1" {
				mask |= 1 << i
			}
		}
		seen[id] = true
		a.Masks[id] = mask
	}
	if fields, err := nextRecord(scanner, &line); err == nil {
		return nil, fmt.Errorf("line %d: unexpected trailing record %q", line, strings.Join(fields, " "))
	} else if err != io.EOF {
		return nil, err
	}
	return a, nil
}

func (a *Assignment) Write(w io.Writer) error {
	if _, err := fmt.Fprintf(w, "p 5cdc 1 %d\n", len(a.Masks)); err != nil {
		return err
	}
	for id, mask := range a.Masks {
		if _, err := fmt.Fprintf(w, "a %d %d %d %d %d %d\n", id,
			(mask>>0)&1, (mask>>1)&1, (mask>>2)&1, (mask>>3)&1, (mask>>4)&1); err != nil {
			return err
		}
	}
	return nil
}

type AssignmentReport struct {
	Valid              bool              `json:"valid"`
	ExactTwo           bool              `json:"exact_two"`
	EvenAtVertices     bool              `json:"even_at_vertices"`
	BadCoverageEdges   []int             `json:"bad_coverage_edge_ids"`
	OddVertexParities  []OddVertexParity `json:"odd_vertex_parities"`
	GraphIsBridgeless  bool              `json:"graph_is_bridgeless"`
	GraphBridgeEdgeIDs []int             `json:"graph_bridge_edge_ids"`
}

type OddVertexParity struct {
	Vertex      int   `json:"vertex"`
	Mask        uint8 `json:"mask"`
	Coordinates []int `json:"coordinates"`
}

// CheckAssignment validates both exact-two coverage and all five incidence
// parities. A loop contributes two incidences at one vertex, hence cancels.
func CheckAssignment(g *Graph, a *Assignment) (AssignmentReport, error) {
	if err := g.Validate(); err != nil {
		return AssignmentReport{}, err
	}
	if a == nil || len(a.Masks) != len(g.Edges) {
		return AssignmentReport{}, fmt.Errorf("assignment length does not match graph")
	}
	bridges := g.Bridges()
	report := AssignmentReport{
		GraphIsBridgeless:  len(bridges) == 0,
		GraphBridgeEdgeIDs: bridges,
	}
	parity := make([]uint8, g.N)
	for _, e := range g.Edges {
		mask := a.Masks[e.ID]
		if mask&^uint8(31) != 0 || bits.OnesCount8(mask) != 2 {
			report.BadCoverageEdges = append(report.BadCoverageEdges, e.ID)
		}
		if e.U != e.V {
			parity[e.U] ^= mask
			parity[e.V] ^= mask
		}
	}
	for v, mask := range parity {
		if mask != 0 {
			odd := OddVertexParity{Vertex: v, Mask: mask}
			for coordinate := 0; coordinate < 5; coordinate++ {
				if mask&(1<<coordinate) != 0 {
					odd.Coordinates = append(odd.Coordinates, coordinate)
				}
			}
			report.OddVertexParities = append(report.OddVertexParities, odd)
		}
	}
	report.ExactTwo = len(report.BadCoverageEdges) == 0
	report.EvenAtVertices = len(report.OddVertexParities) == 0
	report.Valid = report.ExactTwo && report.EvenAtVertices
	return report, nil
}
