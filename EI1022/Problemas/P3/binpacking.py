from typing import *


def mientras_quepa(W: List[int], C: int) -> List[int]:
    sol = []
    currentContainer = 0
    left = C

    for i in range(len(W)):
        if(W[i] <= left):
            sol.append(currentContainer)
            left -= W[i]
        else:
            currentContainer += 1
            left = C
            sol.append(currentContainer)
            left -= W[i]

    return sol


def primero_que_quepa(W: List[int], C: int) -> List[int]:
    sol = []
    trucks = [C]

    for i in range(len(W)):
        for c in range(len(trucks)):
            if(W[i] <= trucks[c]):
                trucks[c] -= W[i]
                sol.append(c)
                break
        else:
            trucks.append(C-W[i])
            sol.append(c+1)

    return sol

def primero_que_quepa_ordenado(W: List[int], C: int) -> List[int]:
    sol = [-1] * len(W)
    trucks = [C]

    sorted_index = sorted(range(len(W)), key = lambda i:-W[i])

    for i in sorted_index:
        for c in range(len(trucks)):
            if (W[i] <= trucks[c]):
                trucks[c] -= W[i]
                sol[i] = c
                break
        else:
            trucks.append(C - W[i])
            sol[i] = c+1

    return sol


def prueba_binpacking():
    W: List[int] = [1, 2, 8, 7, 8, 3]
    C: int = 10

    for solve in [mientras_quepa, primero_que_quepa, primero_que_quepa_ordenado]:
        sol = solve(W, C)
        print("-" * 40)
        print("Método:", solve.__name__)
        if len(sol) == 0:
            print("No implementado")
        else:
            print("Solución: {}, usados {} contenedores\n".format(sol, 1 + max(sol)))


if __name__ == "__main__":
    prueba_binpacking()