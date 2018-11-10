from typing import *

Folleto = Tuple[int, int, int]
PosicionFolleto = Tuple[int, int, int, int]


def optimiza_folletos(m: int, folletos: List[Folleto]) -> List[PosicionFolleto]:
    solucion = []
    # Indices de folleto ordenados
    indices_ordenados= sorted(range(len(folletos)), key=lambda i: (-folletos[i][2], -folletos[i][1]))
    # Lista con la anchura actual, la altura total, y el elemento mas alto de la pagina
    paginas = [[0, 0, 0]]

    # Recorremos todos los folletos
    for indice_folleto in indices_ordenados:
        nFolleto = folletos[indice_folleto][0]; anchura_folleto = folletos[indice_folleto][1]; altura_folleto = folletos[indice_folleto][2]
        # Recorremos todas las paginas

        for indice_pagina in range(len(paginas)):
            # Si el folleto cabe en alguna pagina

            if anchura_folleto + paginas[indice_pagina][0] <= m and altura_folleto + paginas[indice_pagina][1] <= m:
                # Si es el primer elemento añadido, tambien es el mas alto

                if paginas[indice_pagina][0] == 0: paginas[indice_pagina][2] = altura_folleto + paginas[indice_pagina][1]
                # Añadimos el folleto
                solucion.append((nFolleto, indice_pagina + 1, paginas[indice_pagina][0], paginas[indice_pagina][1]))
                # Sumamos a la pagina la anchura ocupada por el folleto
                paginas[indice_pagina][0] += anchura_folleto
                break

            # Si el folleto no cabe en el nivel actual, pero si cabe en el inferior
            elif anchura_folleto + paginas[indice_pagina][0] > m >= altura_folleto + paginas[indice_pagina][2]:
                # Movemos los indices de la pagina al nivel inferior
                paginas[indice_pagina][0] = 0
                paginas[indice_pagina][1] = paginas[indice_pagina][2]
                paginas[indice_pagina][2] += altura_folleto
                # Añadimos el folleto
                solucion.append((nFolleto, indice_pagina+1, paginas[indice_pagina][0], paginas[indice_pagina][1]))
                # Sumamos a la pagina la anchura ocupada por el folleto
                paginas[indice_pagina][0] += anchura_folleto
                break

        else:
            # Si el folleto no ha cabido en ninguna hoja, añadimos una nueva
            paginas.append([0, 0, altura_folleto])
            # Añadimos el folleto
            solucion.append((nFolleto, len(paginas), 0, 0))
            # Sumamos a la pagina la anchura ocupada por el folleto
            paginas[-1][0] += anchura_folleto

    return solucion


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


# Metodo opcional, escribe en un fichero el contenido de una lista solucion.
def escribe_fichero(solucion):
    f = open("sol.txt", 'w')
    for sol in solucion:
        cadena = "{} {} {} {}\n".format(sol[0], sol[1], sol[2], sol[3])
        f.write(cadena)
    f.close()

# Funcion main utilizada para agilizar las pruebas
if __name__ == '__main__':
    m, folletos = lee_fichero_imprenta("problema_imprenta_1.txt")
    solution = optimiza_folletos(m, folletos)
    escribe_fichero(solution)
    muestra_solucion(solution)
