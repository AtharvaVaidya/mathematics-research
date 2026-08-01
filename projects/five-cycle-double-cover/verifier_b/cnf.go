package main

import (
	"bufio"
	"fmt"
	"io"
	"math/bits"
)

type CNF struct {
	Variables int
	Clauses   [][]int
}

func variable(edgeID, coordinate int) int {
	return 5*edgeID + coordinate + 1
}

// GenerateTruthTableCNF uses no auxiliary variables. For each edge it blocks
// the 22 five-bit rows whose weight is not two. For each (vertex,coordinate)
// it blocks all odd rows on the distinct non-loop incident edges.
func GenerateTruthTableCNF(g *Graph, maxParityDegree int) (*CNF, error) {
	if err := g.Validate(); err != nil {
		return nil, err
	}
	if maxParityDegree < 0 || maxParityDegree > 62 {
		return nil, fmt.Errorf("max parity degree must be in [0,62]")
	}
	cnf := &CNF{Variables: 5 * len(g.Edges)}
	for _, e := range g.Edges {
		for row := 0; row < 32; row++ {
			if bits.OnesCount(uint(row)) == 2 {
				continue
			}
			clause := make([]int, 5)
			for i := 0; i < 5; i++ {
				x := variable(e.ID, i)
				if row&(1<<i) != 0 {
					x = -x
				}
				clause[i] = x
			}
			cnf.Clauses = append(cnf.Clauses, clause)
		}
	}
	incident := nonLoopIncidence(g)
	for v, edgeIDs := range incident {
		d := len(edgeIDs)
		if d > maxParityDegree {
			return nil, fmt.Errorf("vertex %d has non-loop incidence degree %d, above configured truth-table limit %d", v, d, maxParityDegree)
		}
		if d == 0 {
			continue
		}
		rows := uint64(1) << d
		for coordinate := 0; coordinate < 5; coordinate++ {
			for row := uint64(0); row < rows; row++ {
				if bits.OnesCount64(row)%2 == 0 {
					continue
				}
				clause := make([]int, d)
				for j, edgeID := range edgeIDs {
					x := variable(edgeID, coordinate)
					if row&(uint64(1)<<j) != 0 {
						x = -x
					}
					clause[j] = x
				}
				cnf.Clauses = append(cnf.Clauses, clause)
			}
		}
	}
	return cnf, nil
}

func (cnf *CNF) WriteDIMACS(w io.Writer) error {
	bw := bufio.NewWriter(w)
	if _, err := fmt.Fprintln(bw, "c verifier-b direct truth-table encoding, no auxiliary variables"); err != nil {
		return err
	}
	if _, err := fmt.Fprintln(bw, "c variable(edge,coordinate) = 5*edge + coordinate + 1"); err != nil {
		return err
	}
	if _, err := fmt.Fprintf(bw, "p cnf %d %d\n", cnf.Variables, len(cnf.Clauses)); err != nil {
		return err
	}
	for _, clause := range cnf.Clauses {
		for _, literal := range clause {
			if _, err := fmt.Fprintf(bw, "%d ", literal); err != nil {
				return err
			}
		}
		if _, err := fmt.Fprintln(bw, "0"); err != nil {
			return err
		}
	}
	return bw.Flush()
}

func (cnf *CNF) Satisfied(values []bool) bool {
	if len(values) != cnf.Variables {
		return false
	}
	for _, clause := range cnf.Clauses {
		satisfied := false
		for _, literal := range clause {
			value := values[abs(literal)-1]
			if literal < 0 {
				value = !value
			}
			if value {
				satisfied = true
				break
			}
		}
		if !satisfied {
			return false
		}
	}
	return true
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

// FormulaSatisfiedBits is a direct executable form of the SAT/XOR statement,
// independent of the generated clauses. Bit k is variable k+1.
func FormulaSatisfiedBits(g *Graph, bitRow uint64) bool {
	if len(g.Edges) > 12 {
		return false // 5*m would not fit this testing helper's uint64 domain.
	}
	a := &Assignment{Masks: make([]uint8, len(g.Edges))}
	for e := range g.Edges {
		for i := 0; i < 5; i++ {
			if bitRow&(uint64(1)<<uint(variable(e, i)-1)) != 0 {
				a.Masks[e] |= 1 << i
			}
		}
	}
	report, err := CheckAssignment(g, a)
	return err == nil && report.Valid
}
