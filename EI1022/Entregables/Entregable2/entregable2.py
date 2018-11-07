from typing import *

Folleto = Tuple[int,int,int]
PosicionFolleto= Tuple[int,int,int,int]


def optimiza_folletos(m: int, folletos: List[Folleto]) -> List[PosicionFolleto]:
    sorted_index= sorted(range(len(folletos)), key = lambda i: -folletos[i][1]) #indices de folleto ordenados
    pags = [[m*[m*[0]]]]    #matriz de posiciones de paginas

    for f in sorted_index:  #recorremos los indices ordenados
        nf = folletos[f][0]
        anchura = folletos[f][1]
        altura = folletos[f][2]




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
