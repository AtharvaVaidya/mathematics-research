package main

import (
	"bufio"
	"fmt"
	"io"
	"strconv"
	"strings"
)

const maxInputObjects = 10_000_000

// Edge is an indexed undirected edge. U == V denotes a loop.
type Edge struct {
	ID int
	U  int
	V  int
}

// Graph is a finite indexed undirected multigraph. Parallel edges are
// represented by different Edge values with different IDs.
type Graph struct {
	N     int
	Edges []Edge
}

func meaningfulFields(line string) []string {
	if i := strings.IndexByte(line, '#'); i >= 0 {
		line = line[:i]
	}
	return strings.Fields(line)
}

func nextRecord(scanner *bufio.Scanner, line *int) ([]string, error) {
	for scanner.Scan() {
		*line++
		fields := meaningfulFields(scanner.Text())
		if len(fields) != 0 {
			return fields, nil
		}
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}
	return nil, io.EOF
}

func nonnegativeInt(s, what string) (int, error) {
	n, err := strconv.Atoi(s)
	if err != nil || n < 0 {
		return 0, fmt.Errorf("%s must be a nonnegative machine integer, got %q", what, s)
	}
	return n, nil
}

// ParseGraph parses:
//
//	p mgraph 1 <number-of-vertices> <number-of-edges>
//	e <edge-id> <endpoint-u> <endpoint-v>
//
// Edge IDs must be a permutation of 0,...,m-1. Blank lines and text following
// '#' are ignored.
func ParseGraph(r io.Reader) (*Graph, error) {
	scanner := bufio.NewScanner(r)
	scanner.Buffer(make([]byte, 4096), 16*1024*1024)
	line := 0
	header, err := nextRecord(scanner, &line)
	if err != nil {
		return nil, fmt.Errorf("graph header: %w", err)
	}
	if len(header) != 5 || header[0] != "p" || header[1] != "mgraph" || header[2] != "1" {
		return nil, fmt.Errorf("line %d: expected 'p mgraph 1 <n> <m>'", line)
	}
	n, err := nonnegativeInt(header[3], "vertex count")
	if err != nil {
		return nil, fmt.Errorf("line %d: %w", line, err)
	}
	m, err := nonnegativeInt(header[4], "edge count")
	if err != nil {
		return nil, fmt.Errorf("line %d: %w", line, err)
	}
	if n > maxInputObjects || m > maxInputObjects {
		return nil, fmt.Errorf("object count exceeds safety limit %d", maxInputObjects)
	}
	g := &Graph{N: n, Edges: make([]Edge, m)}
	seen := make([]bool, m)
	for record := 0; record < m; record++ {
		fields, err := nextRecord(scanner, &line)
		if err != nil {
			return nil, fmt.Errorf("edge record %d: %w", record, err)
		}
		if len(fields) != 4 || fields[0] != "e" {
			return nil, fmt.Errorf("line %d: expected 'e <id> <u> <v>'", line)
		}
		id, err := nonnegativeInt(fields[1], "edge ID")
		if err != nil {
			return nil, fmt.Errorf("line %d: %w", line, err)
		}
		u, err := nonnegativeInt(fields[2], "first endpoint")
		if err != nil {
			return nil, fmt.Errorf("line %d: %w", line, err)
		}
		v, err := nonnegativeInt(fields[3], "second endpoint")
		if err != nil {
			return nil, fmt.Errorf("line %d: %w", line, err)
		}
		if id >= m {
			return nil, fmt.Errorf("line %d: edge ID %d outside [0,%d)", line, id, m)
		}
		if u >= n || v >= n {
			return nil, fmt.Errorf("line %d: endpoint outside [0,%d)", line, n)
		}
		if seen[id] {
			return nil, fmt.Errorf("line %d: duplicate edge ID %d", line, id)
		}
		seen[id] = true
		g.Edges[id] = Edge{ID: id, U: u, V: v}
	}
	if fields, err := nextRecord(scanner, &line); err == nil {
		return nil, fmt.Errorf("line %d: unexpected trailing record %q", line, strings.Join(fields, " "))
	} else if err != io.EOF {
		return nil, err
	}
	if err := g.Validate(); err != nil {
		return nil, err
	}
	return g, nil
}

// Validate checks the in-memory representation independently of the parser.
func (g *Graph) Validate() error {
	if g == nil {
		return fmt.Errorf("nil graph")
	}
	if g.N < 0 || g.N > maxInputObjects {
		return fmt.Errorf("invalid vertex count %d", g.N)
	}
	if len(g.Edges) > maxInputObjects {
		return fmt.Errorf("too many edges")
	}
	seen := make([]bool, len(g.Edges))
	for pos, e := range g.Edges {
		if e.ID < 0 || e.ID >= len(g.Edges) {
			return fmt.Errorf("edge at position %d has invalid ID %d", pos, e.ID)
		}
		if seen[e.ID] {
			return fmt.Errorf("duplicate edge ID %d", e.ID)
		}
		seen[e.ID] = true
		if e.ID != pos {
			return fmt.Errorf("edge ID %d stored at position %d", e.ID, pos)
		}
		if e.U < 0 || e.U >= g.N || e.V < 0 || e.V >= g.N {
			return fmt.Errorf("edge %d has endpoint outside [0,%d)", e.ID, g.N)
		}
	}
	return nil
}

type adjacency struct {
	to     int
	edgeID int
}

// Bridges returns bridge edge IDs in increasing order. Loops are never
// bridges. Edge IDs, rather than parent vertices, distinguish parallel edges.
func (g *Graph) Bridges() []int {
	adj := make([][]adjacency, g.N)
	for _, e := range g.Edges {
		if e.U == e.V {
			continue
		}
		adj[e.U] = append(adj[e.U], adjacency{to: e.V, edgeID: e.ID})
		adj[e.V] = append(adj[e.V], adjacency{to: e.U, edgeID: e.ID})
	}
	discovery := make([]int, g.N)
	low := make([]int, g.N)
	time := 0
	bridges := make([]bool, len(g.Edges))
	var dfs func(int, int)
	dfs = func(v, parentEdge int) {
		time++
		discovery[v] = time
		low[v] = time
		for _, a := range adj[v] {
			if a.edgeID == parentEdge {
				continue
			}
			if discovery[a.to] == 0 {
				dfs(a.to, a.edgeID)
				if low[a.to] < low[v] {
					low[v] = low[a.to]
				}
				if low[a.to] > discovery[v] {
					bridges[a.edgeID] = true
				}
			} else if discovery[a.to] < low[v] {
				low[v] = discovery[a.to]
			}
		}
	}
	for v := 0; v < g.N; v++ {
		if discovery[v] == 0 {
			dfs(v, -1)
		}
	}
	var result []int
	for id, bridge := range bridges {
		if bridge {
			result = append(result, id)
		}
	}
	return result
}

type GraphReport struct {
	Vertices       int   `json:"vertices"`
	Edges          int   `json:"edges"`
	Loops          int   `json:"loops"`
	ParallelPairs  int   `json:"parallel_pairs"`
	Components     int   `json:"components"`
	Simple         bool  `json:"simple"`
	Bridgeless     bool  `json:"bridgeless"`
	BridgeEdgeIDs  []int `json:"bridge_edge_ids"`
	DegreeSequence []int `json:"degree_sequence"`
}

func (g *Graph) Report() GraphReport {
	degree := make([]int, g.N)
	loops := 0
	type pair struct{ a, b int }
	multiplicity := make(map[pair]int)
	for _, e := range g.Edges {
		a, b := e.U, e.V
		if a > b {
			a, b = b, a
		}
		multiplicity[pair{a, b}]++
		if e.U == e.V {
			loops++
			degree[e.U] += 2
			continue
		}
		degree[e.U]++
		degree[e.V]++
	}
	parallelPairs := 0
	for _, k := range multiplicity {
		parallelPairs += k * (k - 1) / 2
	}
	components := g.componentCount()
	bridges := g.Bridges()
	return GraphReport{
		Vertices:       g.N,
		Edges:          len(g.Edges),
		Loops:          loops,
		ParallelPairs:  parallelPairs,
		Components:     components,
		Simple:         loops == 0 && parallelPairs == 0,
		Bridgeless:     len(bridges) == 0,
		BridgeEdgeIDs:  bridges,
		DegreeSequence: degree,
	}
}

func (g *Graph) componentCount() int {
	if g.N == 0 {
		return 0
	}
	adj := make([][]int, g.N)
	for _, e := range g.Edges {
		if e.U != e.V {
			adj[e.U] = append(adj[e.U], e.V)
			adj[e.V] = append(adj[e.V], e.U)
		}
	}
	seen := make([]bool, g.N)
	components := 0
	var stack []int
	for root := 0; root < g.N; root++ {
		if seen[root] {
			continue
		}
		components++
		seen[root] = true
		stack = append(stack[:0], root)
		for len(stack) != 0 {
			v := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			for _, w := range adj[v] {
				if !seen[w] {
					seen[w] = true
					stack = append(stack, w)
				}
			}
		}
	}
	return components
}

func nonLoopIncidence(g *Graph) [][]int {
	incident := make([][]int, g.N)
	for _, e := range g.Edges {
		if e.U == e.V {
			continue
		}
		incident[e.U] = append(incident[e.U], e.ID)
		incident[e.V] = append(incident[e.V], e.ID)
	}
	return incident
}
