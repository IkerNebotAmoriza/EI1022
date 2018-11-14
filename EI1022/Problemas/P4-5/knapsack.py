from Utils.bt_scheme import PartialSolutionWithOptimization, BacktrackingOptSolver, State, Solution
from typing import *
from random import random, seed


def knapsack_solve(weights, values, capacity):
    class KnapsackPS(PartialSolutionWithOptimization):
        def __init__(self, decisions: Tuple[int, ...], value: int,
                     weight: int):  # IMPLEMENTAR: Añade los parámetros que tú consideres
            self.decisions = decisions
            self.value = value
            self.weight = weight
            self.n = len(decisions)

        def is_solution(self) -> bool:  # IMPLEMENTAR
            return self.n == len(values)

        def get_solution(self) -> Solution:  # IMPLEMENTAR
            return self.decisions, self.value, self.weight

        def successors(self) -> Iterable["KnapsackPS"]:  # Devolvemos los sucesores
            if self.n < len(weights):
                if self.weight + weights[self.n] <= capacity:
                    yield KnapsackPS(self.decisions + (1,), self.value + values[self.n], self.weight + weights[self.n])
                yield KnapsackPS(self.decisions + (0,), self.value, self.weight)

        def state(self) -> State:  # Devolvemos el estado de la PS, que son las decisiones tomadas y lo que pesa
            return (self.n, self.weight)

        def f(self) -> Union[int, float]:  # IMPLEMENTAR
            return -self.value

    initialPS = KnapsackPS((), 0, 0)  # IMPLEMENTAR: Añade los parámetros que tú consideres
    return BacktrackingOptSolver.solve(initialPS)


def create_knapsack_problem(num_objects: int) -> Tuple[Tuple[int, ...], Tuple[int, ...], int]:
    seed(42)
    weights = [int(random() * 1000 + 1) for _ in range(num_objects)]
    values = [int(random() * 1000 + 1) for _ in range(num_objects)]
    capacity = sum(weights) // 2
    return weights, values, capacity


# Programa principal ------------------------------------------
if __name__ == "__main__":
    #W, V, C = [1, 4, 2, 3], [2, 3, 4, 2], 7  # SOLUCIÓN: Weight=7,    Value=9
    W, V, C = create_knapsack_problem(30)     # SOLUCIÓN: Weight=6313, Value=11824
    for sol in knapsack_solve(W, V, C):
        print(sol)
    print("\n<TERMINADO>")
