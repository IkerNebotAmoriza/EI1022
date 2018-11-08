from typing import *

Folleto = Tuple[int, int, int]
PosicionFolleto = Tuple[int, int, int, int]

def optimiza_folletos(m: int, folletos: List[Folleto]) -> List[PosicionFolleto]:
    lista_sol = []
    indices_ordenados = sorted(range(len(folletos)), key=lambda i: (-folletos[i][2],-folletos[i][1]))
    lista_paginas = [[0, 0, 0]]

    for f in indices_ordenados:
        nFolleto = folletos[f][0]
        anchura = folletos[f][1]
        altura = folletos[f][2]

        for p in range(len(lista_paginas)):
            if lista_paginas[p][0] + anchura <= m and lista_paginas[p][1] + altura <= m:
                lista_sol.append((nFolleto, p+1, lista_paginas[p][0], lista_paginas[p][1]))
                if anchura == 0:
                    lista_paginas[p][2] = lista_paginas[p][1]+altura
                lista_paginas[p][0] += anchura
                break

            elif lista_paginas[p][0] + anchura > m and lista_paginas[p][2] + altura <= m:
                lista_paginas[p][0] = 0
                lista_paginas[p][1] = lista_paginas[p][2]
                lista_paginas[p][2] += altura
                lista_sol.append((nFolleto, p+1, lista_paginas[p][0], lista_paginas[p][1]))
                lista_paginas[p][0] += anchura
                break
        else:
            lista_paginas.append([0, 0, 0])
            lista_sol.append((nFolleto, len(lista_paginas), 0, 0))
            lista_paginas[-1][0] += anchura
            lista_paginas[-1][2] += altura

    return lista_sol

def lee_fichero_imprenta(name: str) -> Tuple[int, List[Folleto]]:
    f = open(name)
    M = f.readline()
    line = f.readline()
    folletos = []

    while line != "":
        info = line.split(" ")
        folletos.append((int(info[0]), int(info[1]), int(info[2])))
        line = f.readline()

    t = [int(M), folletos]
    f.close()
    return t


def muestra_solucion(solucion: List[PosicionFolleto]):
    for s in solucion:
        print(s[0], s[1], s[2], s[3])


def escribe_fichero(solucion):
    f = open("sol.txt", 'w')
    for tupla in solucion:
        cadena = "{} {} {} {}\n".format(tupla[0], tupla[1], tupla[2], tupla[3])
        f.write(cadena)
    f.close()


if __name__ == '__main__':
    m, folletos = lee_fichero_imprenta("problema_imprenta_1.txt")
    solution = optimiza_folletos(m, folletos)
    escribe_fichero(solution)
    muestra_solucion(solution)
