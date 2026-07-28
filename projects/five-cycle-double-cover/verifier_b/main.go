package main

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
)

const version = "verifier-b 0.1.0"

func openGraph(path string) (*Graph, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	return ParseGraph(f)
}

func writeJSON(v any) error {
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	return encoder.Encode(v)
}

func premisesCommand(args []string) int {
	fs := flag.NewFlagSet("premises", flag.ContinueOnError)
	fs.SetOutput(os.Stderr)
	graphPath := fs.String("graph", "", "input multigraph file")
	if err := fs.Parse(args); err != nil || *graphPath == "" || fs.NArg() != 0 {
		if err == nil {
			fmt.Fprintln(os.Stderr, "premises requires -graph FILE")
		}
		return 2
	}
	g, err := openGraph(*graphPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, "invalid graph:", err)
		return 2
	}
	report := g.Report()
	if err := writeJSON(report); err != nil {
		fmt.Fprintln(os.Stderr, err)
		return 2
	}
	if !report.Bridgeless {
		return 1
	}
	return 0
}

func checkCommand(args []string) int {
	fs := flag.NewFlagSet("check", flag.ContinueOnError)
	fs.SetOutput(os.Stderr)
	graphPath := fs.String("graph", "", "input multigraph file")
	assignmentPath := fs.String("assignment", "", "input 5-CDC assignment")
	if err := fs.Parse(args); err != nil || *graphPath == "" || *assignmentPath == "" || fs.NArg() != 0 {
		if err == nil {
			fmt.Fprintln(os.Stderr, "check requires -graph FILE -assignment FILE")
		}
		return 2
	}
	g, err := openGraph(*graphPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, "invalid graph:", err)
		return 2
	}
	f, err := os.Open(*assignmentPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return 2
	}
	a, parseErr := ParseAssignment(f, len(g.Edges))
	closeErr := f.Close()
	if parseErr != nil {
		fmt.Fprintln(os.Stderr, "invalid assignment:", parseErr)
		return 2
	}
	if closeErr != nil {
		fmt.Fprintln(os.Stderr, closeErr)
		return 2
	}
	report, err := CheckAssignment(g, a)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return 2
	}
	if err := writeJSON(report); err != nil {
		fmt.Fprintln(os.Stderr, err)
		return 2
	}
	// An accepted conjecture witness needs both a valid cover and the graph
	// premise. This keeps bridged UNSAT formulas out of counterexample status.
	if !report.Valid || !report.GraphIsBridgeless {
		return 1
	}
	return 0
}

func cnfCommand(args []string) int {
	fs := flag.NewFlagSet("cnf", flag.ContinueOnError)
	fs.SetOutput(os.Stderr)
	graphPath := fs.String("graph", "", "input multigraph file")
	outPath := fs.String("out", "-", "DIMACS output file, or - for stdout")
	maxDegree := fs.Int("max-parity-degree", 20, "largest non-loop vertex degree to truth-table expand")
	if err := fs.Parse(args); err != nil || *graphPath == "" || fs.NArg() != 0 {
		if err == nil {
			fmt.Fprintln(os.Stderr, "cnf requires -graph FILE")
		}
		return 2
	}
	g, err := openGraph(*graphPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, "invalid graph:", err)
		return 2
	}
	cnf, err := GenerateTruthTableCNF(g, *maxDegree)
	if err != nil {
		fmt.Fprintln(os.Stderr, "cannot generate CNF:", err)
		return 2
	}
	var w io.Writer = os.Stdout
	var f *os.File
	if *outPath != "-" {
		f, err = os.Create(*outPath)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			return 2
		}
		w = f
	}
	err = cnf.WriteDIMACS(w)
	if f != nil {
		err = errors.Join(err, f.Close())
	}
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return 2
	}
	return 0
}

func solveCommand(args []string) int {
	fs := flag.NewFlagSet("solve", flag.ContinueOnError)
	fs.SetOutput(os.Stderr)
	graphPath := fs.String("graph", "", "input multigraph file")
	witnessPath := fs.String("witness", "", "write SAT assignment to this file")
	maxNodes := fs.Uint64("max-nodes", 0, "search node limit; 0 is unlimited")
	if err := fs.Parse(args); err != nil || *graphPath == "" || fs.NArg() != 0 {
		if err == nil {
			fmt.Fprintln(os.Stderr, "solve requires -graph FILE")
		}
		return 2
	}
	g, err := openGraph(*graphPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, "invalid graph:", err)
		return 2
	}
	result, err := SolveExactly(g, *maxNodes)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return 2
	}
	if result.Witness != nil {
		report, checkErr := CheckAssignment(g, result.Witness)
		if checkErr != nil || !report.Valid {
			fmt.Fprintln(os.Stderr, "internal witness validation failed")
			return 2
		}
		if *witnessPath != "" {
			f, createErr := os.Create(*witnessPath)
			if createErr != nil {
				fmt.Fprintln(os.Stderr, createErr)
				return 2
			}
			writeErr := result.Witness.Write(f)
			writeErr = errors.Join(writeErr, f.Close())
			if writeErr != nil {
				fmt.Fprintln(os.Stderr, writeErr)
				return 2
			}
		}
	}
	if err := writeJSON(result); err != nil {
		fmt.Fprintln(os.Stderr, err)
		return 2
	}
	if result.Status == "UNKNOWN" {
		return 1
	}
	return 0
}

func usage() {
	fmt.Fprintf(os.Stderr, `%s
Usage:
  verifier-b premises -graph FILE
  verifier-b check -graph FILE -assignment FILE
  verifier-b cnf -graph FILE [-out FILE] [-max-parity-degree N]
  verifier-b solve -graph FILE [-witness FILE] [-max-nodes N]
`, version)
}

func main() {
	if len(os.Args) < 2 {
		usage()
		os.Exit(2)
	}
	var code int
	switch os.Args[1] {
	case "premises":
		code = premisesCommand(os.Args[2:])
	case "check":
		code = checkCommand(os.Args[2:])
	case "cnf":
		code = cnfCommand(os.Args[2:])
	case "solve":
		code = solveCommand(os.Args[2:])
	case "version", "-version", "--version":
		fmt.Println(version)
		code = 0
	default:
		usage()
		code = 2
	}
	os.Exit(code)
}
