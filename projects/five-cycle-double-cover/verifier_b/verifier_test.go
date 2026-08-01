package main

import (
	"bytes"
	"fmt"
	"strings"
	"testing"
)

func mustParseGraph(t *testing.T, text string) *Graph {
	t.Helper()
	g, err := ParseGraph(strings.NewReader(text))
	if err != nil {
		t.Fatalf("ParseGraph: %v", err)
	}
	return g
}

func graphFromEdges(n int, endpoints [][2]int) *Graph {
	g := &Graph{N: n, Edges: make([]Edge, len(endpoints))}
	for id, uv := range endpoints {
		g.Edges[id] = Edge{ID: id, U: uv[0], V: uv[1]}
	}
	return g
}

func constantAssignment(m int, mask uint8) *Assignment {
	a := &Assignment{Masks: make([]uint8, m)}
	for i := range a.Masks {
		a.Masks[i] = mask
	}
	return a
}

func TestGraphLoopsParallelAndBridges(t *testing.T) {
	g := mustParseGraph(t, `
		# two parallel edges and a loop
		p mgraph 1 2 3
		e 2 1 1
		e 0 0 1
		e 1 1 0
	`)
	report := g.Report()
	if !report.Bridgeless || report.Simple || report.Loops != 1 || report.ParallelPairs != 1 {
		t.Fatalf("unexpected report: %+v", report)
	}
	if len(report.DegreeSequence) != 2 || report.DegreeSequence[0] != 2 || report.DegreeSequence[1] != 4 {
		t.Fatalf("loop/parallel degree multiplicity wrong: %v", report.DegreeSequence)
	}

	bridge := graphFromEdges(2, [][2]int{{0, 1}})
	if got := bridge.Bridges(); len(got) != 1 || got[0] != 0 {
		t.Fatalf("single edge bridges = %v", got)
	}
	loop := graphFromEdges(1, [][2]int{{0, 0}})
	if got := loop.Bridges(); len(got) != 0 {
		t.Fatalf("loop reported as bridge: %v", got)
	}
	twoLoops := graphFromEdges(1, [][2]int{{0, 0}, {0, 0}})
	if got := twoLoops.Report().ParallelPairs; got != 1 {
		t.Fatalf("parallel loop pairs = %d, want 1", got)
	}
}

func enumerateEndpointSequences(choices [][2]int, length int, visit func([][2]int)) {
	sequence := make([][2]int, length)
	var walk func(int)
	walk = func(position int) {
		if position == length {
			visit(append([][2]int(nil), sequence...))
			return
		}
		for _, endpoints := range choices {
			sequence[position] = endpoints
			walk(position + 1)
		}
	}
	walk(0)
}

func deleteEdge(g *Graph, deleted int) *Graph {
	endpoints := make([][2]int, 0, len(g.Edges)-1)
	for _, e := range g.Edges {
		if e.ID != deleted {
			endpoints = append(endpoints, [2]int{e.U, e.V})
		}
	}
	return graphFromEdges(g.N, endpoints)
}

func TestBridgeDetectionAgainstDeletionDefinitionExhaustiveTiny(t *testing.T) {
	choices := [][2]int{{0, 0}, {0, 1}, {0, 2}, {1, 1}, {1, 2}, {2, 2}}
	for m := 0; m <= 4; m++ {
		enumerateEndpointSequences(choices, m, func(endpoints [][2]int) {
			g := graphFromEdges(3, endpoints)
			got := make(map[int]bool)
			for _, id := range g.Bridges() {
				got[id] = true
			}
			before := g.componentCount()
			for _, e := range g.Edges {
				want := deleteEdge(g, e.ID).componentCount() > before
				if got[e.ID] != want {
					t.Fatalf("edges=%v edge=%d: Tarjan=%v deletion=%v", endpoints, e.ID, got[e.ID], want)
				}
			}
		})
	}
}

func TestMalformedGraphs(t *testing.T) {
	cases := []string{
		"",
		"p graph 1 1 0\n",
		"p mgraph 1 -1 0\n",
		"p mgraph 1 1 1\n",
		"p mgraph 1 1 1\ne 0 0 1\n",
		"p mgraph 1 2 2\ne 0 0 1\ne 0 0 1\n",
		"p mgraph 1 1 0\nextra\n",
		"p mgraph 1 1 1\ne 0 0\n",
	}
	for i, text := range cases {
		if _, err := ParseGraph(strings.NewReader(text)); err == nil {
			t.Errorf("case %d parsed unexpectedly", i)
		}
	}
	inMemory := []*Graph{
		nil,
		{N: -1},
		{N: 1, Edges: []Edge{{ID: 1, U: 0, V: 0}}},
		{N: 2, Edges: []Edge{{ID: 0, U: 0, V: 2}}},
		{N: 1, Edges: []Edge{{ID: 0, U: 0, V: 0}, {ID: 0, U: 0, V: 0}}},
	}
	for i, g := range inMemory {
		if err := g.Validate(); err == nil {
			t.Errorf("in-memory case %d validated unexpectedly", i)
		}
	}
}

func TestAssignmentParsingMalformed(t *testing.T) {
	bad := []string{
		"",
		"p 5cdc 1 2\n",
		"p 5cdc 1 1\na 0 1 1 0 0\n",
		"p 5cdc 1 2\na 0 1 1 0 0 0\na 0 0 0 1 1 0\n",
		"p 5cdc 1 1\na 0 2 0 0 0 0\n",
		"p 5cdc 1 1\na 1 1 1 0 0 0\n",
		"p 5cdc 1 0\ntrailing\n",
	}
	for i, text := range bad {
		if _, err := ParseAssignment(strings.NewReader(text), 1); err == nil {
			t.Errorf("case %d parsed unexpectedly", i)
		}
	}
}

func TestLoopAssignmentAndExactTwo(t *testing.T) {
	g := graphFromEdges(1, [][2]int{{0, 0}})
	valid, err := CheckAssignment(g, &Assignment{Masks: []uint8{0b10100}})
	if err != nil || !valid.Valid {
		t.Fatalf("loop assignment rejected: %+v, %v", valid, err)
	}
	bad, err := CheckAssignment(g, &Assignment{Masks: []uint8{0b00100}})
	if err != nil || bad.Valid || !bad.EvenAtVertices || bad.ExactTwo {
		t.Fatalf("bad loop coverage report: %+v, %v", bad, err)
	}
}

func TestParallelParity(t *testing.T) {
	g := graphFromEdges(2, [][2]int{{0, 1}, {0, 1}})
	valid, _ := CheckAssignment(g, &Assignment{Masks: []uint8{0b00011, 0b00011}})
	if !valid.Valid {
		t.Fatalf("equal parallel labels should cancel: %+v", valid)
	}
	invalid, _ := CheckAssignment(g, &Assignment{Masks: []uint8{0b00011, 0b00101}})
	if invalid.Valid || invalid.ExactTwo != true || invalid.EvenAtVertices {
		t.Fatalf("different parallel labels should leave parity: %+v", invalid)
	}
}

func TestCircuitWitness(t *testing.T) {
	for n := 1; n <= 8; n++ {
		var edges [][2]int
		if n == 1 {
			edges = append(edges, [2]int{0, 0})
		} else if n == 2 {
			edges = append(edges, [2]int{0, 1}, [2]int{0, 1})
		} else {
			for v := 0; v < n; v++ {
				edges = append(edges, [2]int{v, (v + 1) % n})
			}
		}
		g := graphFromEdges(n, edges)
		report, err := CheckAssignment(g, constantAssignment(len(edges), 0b00011))
		if err != nil || !report.Valid || len(g.Bridges()) != 0 {
			t.Fatalf("circuit n=%d failed: %+v %v", n, report, err)
		}
	}
}

func k4() *Graph {
	return graphFromEdges(4, [][2]int{
		{0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3},
	})
}

func petersen() *Graph {
	// Outer 5-cycle, inner pentagram, and five spokes.
	var edges [][2]int
	for i := 0; i < 5; i++ {
		edges = append(edges, [2]int{i, (i + 1) % 5})
	}
	for i := 0; i < 5; i++ {
		edges = append(edges, [2]int{5 + i, 5 + (i+2)%5})
	}
	for i := 0; i < 5; i++ {
		edges = append(edges, [2]int{i, 5 + i})
	}
	return graphFromEdges(10, edges)
}

func TestExactSolverK4AndPetersen(t *testing.T) {
	for name, g := range map[string]*Graph{"K4": k4(), "Petersen": petersen()} {
		t.Run(name, func(t *testing.T) {
			result, err := SolveExactly(g, 0)
			if err != nil {
				t.Fatal(err)
			}
			if result.Status != "SAT" || result.Witness == nil {
				t.Fatalf("result = %+v", result)
			}
			report, err := CheckAssignment(g, result.Witness)
			if err != nil || !report.Valid {
				t.Fatalf("solver witness invalid: %+v %v", report, err)
			}
		})
	}
}

func TestExactSolverExhaustiveUNSATAndLimit(t *testing.T) {
	g := graphFromEdges(2, [][2]int{{0, 1}})
	result, err := SolveExactly(g, 0)
	if err != nil {
		t.Fatal(err)
	}
	if result.Status != "UNSAT" || !result.Exhaustive || result.Witness != nil {
		t.Fatalf("single bridge should be exhaustive UNSAT: %+v", result)
	}

	// This graph needs branching after the symmetry anchor; a one-node limit
	// must say UNKNOWN, never UNSAT.
	path := graphFromEdges(4, [][2]int{{0, 1}, {1, 2}, {2, 3}})
	limited, err := SolveExactly(path, 1)
	if err != nil {
		t.Fatal(err)
	}
	// Propagation can prove this path UNSAT at the root, so use K4 if needed.
	if limited.Status != "UNKNOWN" {
		limited, err = SolveExactly(k4(), 1)
		if err != nil {
			t.Fatal(err)
		}
	}
	if limited.Status != "UNKNOWN" || limited.Exhaustive {
		t.Fatalf("node-limited result = %+v", limited)
	}
}

func valuesFromRow(n int, row uint64) []bool {
	values := make([]bool, n)
	for i := range values {
		values[i] = row&(uint64(1)<<i) != 0
	}
	return values
}

func TestTruthTableCNFExhaustiveAssignments(t *testing.T) {
	graphs := map[string]*Graph{
		"empty":         graphFromEdges(1, nil),
		"loop":          graphFromEdges(1, [][2]int{{0, 0}}),
		"bridge":        graphFromEdges(2, [][2]int{{0, 1}}),
		"parallel":      graphFromEdges(2, [][2]int{{0, 1}, {0, 1}}),
		"loop-parallel": graphFromEdges(2, [][2]int{{0, 0}, {0, 1}, {0, 1}}),
	}
	for name, g := range graphs {
		t.Run(name, func(t *testing.T) {
			cnf, err := GenerateTruthTableCNF(g, 20)
			if err != nil {
				t.Fatal(err)
			}
			if cnf.Variables > 20 {
				t.Fatal("test brute-force domain unexpectedly large")
			}
			rows := uint64(1) << cnf.Variables
			for row := uint64(0); row < rows; row++ {
				got := cnf.Satisfied(valuesFromRow(cnf.Variables, row))
				want := FormulaSatisfiedBits(g, row)
				if got != want {
					t.Fatalf("row %d: CNF=%v direct=%v", row, got, want)
				}
			}
		})
	}
}

func TestCNFAndSolverExhaustiveTwoVertexMultigraphs(t *testing.T) {
	choices := [][2]int{{0, 0}, {0, 1}, {1, 1}}
	for m := 0; m <= 3; m++ {
		enumerateEndpointSequences(choices, m, func(endpoints [][2]int) {
			g := graphFromEdges(2, endpoints)
			cnf, err := GenerateTruthTableCNF(g, 20)
			if err != nil {
				t.Fatal(err)
			}
			cnfSAT := false
			for row := uint64(0); row < uint64(1)<<cnf.Variables; row++ {
				got := cnf.Satisfied(valuesFromRow(cnf.Variables, row))
				want := FormulaSatisfiedBits(g, row)
				if got != want {
					t.Fatalf("edges=%v row=%d: CNF=%v direct=%v", endpoints, row, got, want)
				}
				cnfSAT = cnfSAT || got
			}
			result, err := SolveExactly(g, 0)
			if err != nil {
				t.Fatal(err)
			}
			if (result.Status == "SAT") != cnfSAT || result.Status == "UNKNOWN" {
				t.Fatalf("edges=%v: solver=%s CNF-SAT=%v", endpoints, result.Status, cnfSAT)
			}
		})
	}
}

func cnfHasSolution(cnf *CNF) bool {
	if cnf.Variables > 20 {
		panic("test helper domain too large")
	}
	for row := uint64(0); row < uint64(1)<<cnf.Variables; row++ {
		if cnf.Satisfied(valuesFromRow(cnf.Variables, row)) {
			return true
		}
	}
	return false
}

func TestSolverCrossValidatedByCNFOnTinyInstances(t *testing.T) {
	graphs := []*Graph{
		graphFromEdges(0, nil),
		graphFromEdges(1, nil),
		graphFromEdges(1, [][2]int{{0, 0}}),
		graphFromEdges(2, [][2]int{{0, 1}}),
		graphFromEdges(2, [][2]int{{0, 1}, {0, 1}}),
		graphFromEdges(3, [][2]int{{0, 1}, {1, 2}}),
		graphFromEdges(3, [][2]int{{0, 1}, {1, 2}, {2, 0}}),
		graphFromEdges(4, [][2]int{{0, 1}, {0, 2}, {0, 3}}),
	}
	for i, g := range graphs {
		cnf, err := GenerateTruthTableCNF(g, 20)
		if err != nil {
			t.Fatal(err)
		}
		cnfSAT := cnfHasSolution(cnf)
		result, err := SolveExactly(g, 0)
		if err != nil {
			t.Fatal(err)
		}
		solverSAT := result.Status == "SAT"
		if result.Status == "UNKNOWN" || solverSAT != cnfSAT {
			t.Fatalf("graph %d: solver=%s CNF-SAT=%v", i, result.Status, cnfSAT)
		}
	}
}

func TestCNFClauseCountsAndDeterminism(t *testing.T) {
	loop := graphFromEdges(1, [][2]int{{0, 0}})
	loopCNF, err := GenerateTruthTableCNF(loop, 20)
	if err != nil {
		t.Fatal(err)
	}
	if len(loopCNF.Clauses) != 22 {
		t.Fatalf("loop clauses = %d, want 22", len(loopCNF.Clauses))
	}
	parallel := graphFromEdges(2, [][2]int{{0, 1}, {0, 1}})
	cnf, err := GenerateTruthTableCNF(parallel, 20)
	if err != nil {
		t.Fatal(err)
	}
	// 2*22 exact-two, plus 2 vertices * 5 coordinates * 2 odd rows.
	if got, want := len(cnf.Clauses), 64; got != want {
		t.Fatalf("parallel clauses = %d, want %d", got, want)
	}
	var first, second bytes.Buffer
	if err := cnf.WriteDIMACS(&first); err != nil {
		t.Fatal(err)
	}
	if err := cnf.WriteDIMACS(&second); err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(first.Bytes(), second.Bytes()) {
		t.Fatal("DIMACS output is nondeterministic")
	}
}

func TestCNFHighDegreeRefusal(t *testing.T) {
	g := graphFromEdges(4, [][2]int{{0, 1}, {0, 2}, {0, 3}})
	if _, err := GenerateTruthTableCNF(g, 2); err == nil {
		t.Fatal("expected explicit high-degree refusal")
	}
	if _, err := GenerateTruthTableCNF(g, 3); err != nil {
		t.Fatalf("degree-three generation failed: %v", err)
	}
}

func TestAssignmentRoundTrip(t *testing.T) {
	a := &Assignment{Masks: []uint8{0b00011, 0b10100}}
	var out bytes.Buffer
	if err := a.Write(&out); err != nil {
		t.Fatal(err)
	}
	parsed, err := ParseAssignment(strings.NewReader(out.String()), 2)
	if err != nil {
		t.Fatal(err)
	}
	if fmt.Sprint(parsed.Masks) != fmt.Sprint(a.Masks) {
		t.Fatalf("roundtrip got %v want %v", parsed.Masks, a.Masks)
	}
}
