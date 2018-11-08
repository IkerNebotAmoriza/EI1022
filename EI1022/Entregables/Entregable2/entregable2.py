from typing import *

Folleto = Tuple[int,int,int]
PosicionFolleto= Tuple[int,int,int,int]


def optimiza_folletos(m: int, folletos: List[Folleto]) -> List[PosicionFolleto]:
    sol = []
    # Indices de folleto ordenados
    indices_ordenados= sorted(range(len(folletos)), key = lambda i: (-folletos[i][2], -folletos[i][1]))
    # Lista con la anchura actual, la altura total, y el elemento mas alto de la pagina
    paginas = [[0, 0, 0]]

    # Recorremos todos los folletos
    for indice_folleto in indices_ordenados:
        numero_folleto = folletos[indice_folleto][0]
        anchura_folleto = folletos[indice_folleto][1]
        altura_folleto = folletos[indice_folleto][2]
        # Recorremos todas las paginas
        for indice_pagina in range(len(paginas)):

            # Si el folleto cabe en alguna pagina
            if anchura_folleto + paginas[indice_pagina][0] <= m and altura_folleto + paginas[indice_pagina][2] <= paginas[indice_pagina][1]:

                # Comprobamos si es el folleto mas alto de la pagina
                if altura_folleto > paginas[indice_pagina][2]: paginas[indice_pagina][2] = altura_folleto
                # Anyadimos el folleto
                sol.append((numero_folleto, indice_pagina + 1, paginas[indice_pagina][0], paginas[indice_pagina][1]))
                # Sumamos a la pagina la anchura ocupada por el folleto
                paginas[indice_pagina][0] += anchura_folleto
                break

            # Si el folleto no cabe en el nivel actual, pero cabe en el nivel inferior de la pagina, bajamos de nivel
            if anchura_folleto + paginas[indice_pagina][0] > m and altura_folleto + paginas[indice_pagina][2] <= paginas[indice_pagina][1]:
                # Reiniciamos la anchura de la pagina en el nivel
                paginas[indice_pagina][0] = 0
                # Incrementamos el nivel de la pagina en funcion del folleto mas alto del nivel anterior
                paginas[indice_pagina][1] += paginas[indice_pagina][2]
                # El folleto actual pasa a ser el mas alto del nivel actual
                paginas[indice_pagina][2] = altura_folleto
                # Anyadimos el folleto actual
                sol.append((numero_folleto, indice_pagina + 1, paginas[indice_pagina][0], paginas[indice_pagina][1]))
                # Incrementamos la anchura
                paginas[indice_pagina][0] += anchura_folleto
                break

            # Si el folleto no cabe y nos encontramos en la ultima pagina, anyadimos una nueva pagina
            if anchura_folleto + paginas[indice_pagina][0] > m and altura_folleto + paginas[indice_pagina][1] > m and indice_pagina == len(paginas)-1:
                paginas.append([0, 0, 0])

                # Recorremos todas las paginas hasta el final
                for indice_pagina in range(len(paginas)):
                    # Y comprobamos si podemos anyadir el folleto
                    if anchura_folleto + paginas[indice_pagina][0] <= m:
                        # Si el folleto cabe lo anyadimos
                        sol.append((numero_folleto, indice_pagina + 1, paginas[indice_pagina][0], 0))
                        paginas[indice_pagina][0] += anchura_folleto
                        # Ya que el folleto es el primer elemento de la pagina creada, es el mas alto
                        paginas[indice_pagina][2] = altura_folleto


    return sol


def lee_fichero_imprenta(name: str) -> Tuple[int, List[Folleto]]:
    f = open(name)
    M = f.readline()
    line = f.readline()
    folletos = []

    while line != "":
        info = line.split(" ")
        folletos.append((int(info[0]),int(info[1]),int(info[2])))
        line= f.readline()

    t = [int(M),folletos]
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
