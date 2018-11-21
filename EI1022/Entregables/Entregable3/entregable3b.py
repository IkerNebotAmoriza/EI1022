import sys
from typing import *

from EI1022.Entregables.Entregable3.brikerdef import Move, Block, Level
from Utils.bt_scheme import PartialSolutionWithOptimization, BacktrackingOptSolver, Solution, State


def bricker_opt_solve(level):
    class BrikerOpt_PS(PartialSolutionWithOptimization):
        def __init__(self, block: Block, decisions: Tuple[Move, ...]):
            self.block = block
            self.decisions = decisions

        def is_solution(self) -> bool:
            return self.block.is_standing_at_pos(level.get_targetpos())

        def get_solution(self) -> Solution:
            return self.decisions

        def successors(self) -> Iterable["BrikerVC_PS"]:
            for movement in self.block.valid_moves(level.is_valid):
                print(self.decisions)
                yield BrikerOpt_PS(self.block.move(movement), self.decisions + (movement, ))

        def state(self) -> State:
            return self.block

        def f(self) -> Union[int, float]:
            return len(self.decisions)

    # TODO: crea initial_ps y llama a BacktrackingOptSolver.solve
    initial_ps = BrikerOpt_PS(Block(level.get_startpos(), level.get_startpos()), ())
    return BacktrackingOptSolver.solve(initial_ps)


if __name__ == '__main__':
    level_filename = "level1.txt" # TODO: Cámbialo por sys.argv[1]

    print("<BEGIN BACKTRACKING>\n")

    # la última solución que devuelva será la más corta
    solutions = list(bricker_opt_solve(Level(level_filename)))

    if len(solutions)==0:
        print("El puzle no tiene solución.")
    else:
        best_solution = solutions[-1]
        string_solution = "".join(best_solution) #convierte la solución de lista  a  string
        print("La solución más corta es: {0} (longitud: {1})".format(string_solution, len(string_solution)))

    print("\n<END BACKTRACKING>")
