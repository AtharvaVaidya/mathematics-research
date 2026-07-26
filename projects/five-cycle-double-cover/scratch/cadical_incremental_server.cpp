#include <cadical.hpp>

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

// Tiny line-oriented incremental CaDiCaL bridge used by the order-100
// discovery solver.  Protocol:
//   add LIT ... 0
//   solve
//   values VAR ... 0
//   quit
// Every command produces one flushed response line.

int main() {
    CaDiCaL::Solver solver;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream input(line);
        std::string command;
        input >> command;
        if (command == "add") {
            int literal = 0;
            bool terminated = false;
            while (input >> literal) {
                solver.add(literal);
                if (literal == 0) {
                    terminated = true;
                    break;
                }
            }
            if (!terminated) {
                std::cerr << "unterminated add command\n";
                return 2;
            }
        } else if (command == "sync") {
            std::cout << "ok\n" << std::flush;
        } else if (command == "solve") {
            const int status = solver.solve();
            if (status == 10) {
                std::cout << "sat\n";
            } else if (status == 20) {
                std::cout << "unsat\n";
            } else {
                std::cout << "unknown\n";
            }
            std::cout << std::flush;
        } else if (command == "values") {
            int variable = 0;
            bool first = true;
            while (input >> variable && variable != 0) {
                if (!first) std::cout << ' ';
                first = false;
                std::cout << (solver.val(variable) > 0 ? 1 : 0);
            }
            std::cout << "\n" << std::flush;
        } else if (command == "quit") {
            std::cout << "bye\n" << std::flush;
            return 0;
        } else {
            std::cerr << "unknown command: " << command << '\n';
            return 2;
        }
    }
    return 0;
}
