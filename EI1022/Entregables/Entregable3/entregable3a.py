import sys
from typing import *

from EI1022.Entregables.Entregable3.brikerdef import Move, Block, Level
from Utils.bt_scheme import PartialSolutionWithVisitedControl, Solution, State, BacktrackingVCSolver


def bricker_vc_solve(level: Level):
    class BrikerVC_PS(PartialSolutionWithVisitedControl):
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
                yield BrikerVC_PS(self.block.move(movement), self.decisions + (movement, ))

        def state(self) -> State:
            return self.block

    # TODO: crea initial_ps y llama a BacktrackingVCSolver.solve
    initial_ps = BrikerVC_PS(Block(level.get_startpos(), level.get_startpos()), ())
    return BacktrackingVCSolver.solve(initial_ps)


if __name__ == '__main__':
    level_filename = "level1.txt"  # TODO: Cámbialo por sys.argv[1]

    print("<BEGIN BACKTRACKING>\n")

    for solution in bricker_vc_solve(Level(level_filename)):
        string_solution = "".join(solution)  # convierte la solución de lista a string
        print("La primera solución encontrada es: {0} (longitud: {1})".format(string_solution, len(string_solution)))
        break

    print("\n<END BACKTRACKING>")
