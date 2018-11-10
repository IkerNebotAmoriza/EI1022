from typing import *

Folleto = Tuple[int,int,int]
PosicionFolleto= Tuple[int,int,int,int]

def optimiza_folletos(m: int, folletos: List[Folleto]) -> List[PosicionFolleto]:
    sorted_index= sorted(range(len(folletos)), key = lambda i: (-folletos[i][2],-folletos[i][1]))
    listMM= [[[0,0]]] #lista de hojas con su anchura y altura en cada momento
    sol = [0] * len(folletos) #lista con las soluciones


    for f in sorted_index:
        folleto = folletos[f]
        num = folleto[0]
        anchura = folleto[1]
        altura = folleto[2]
        añadido = False
        for i in range(len(listMM)):
            if añadido:
                break
            for j in range(len(listMM[i])):
                if (anchura <= m-listMM[i][j][0] and altura<=m-listMM[i][j][1]):
                    print("El folleto cabe en anchura")

                    sol[f]=(num,i+1, listMM[i][j][0], listMM[i][j][1])

                    if(listMM[i][j][0]==0):
                        listMM[i].append([0,listMM[i][j][1]+altura])

                    listMM[i][j][0] += anchura

                    añadido=True
                    break

        if not añadido:
            print("El folleto no cabe")
            sol[f] = (num, i + 2, 0, 0)
            listMM.append([[anchura,0],[0,altura]])

    return sol





def lee_fichero_imprenta(name: str) -> Tuple[int, List[Folleto]]:
    f = open(name)
    M = f.readline()
    line = f.readline()
    folletos = []

    while line != "":
        info = line.split(" ")
        print(info)
        folletos.append((int(info[0]),int(info[1]),int(info[2])))
        line= f.readline()

    t = [int(M),folletos]
    f.close()
    return t


def escribe_fichero(solucion):
    f = open("sol.txt", 'w')
    for tupla in solucion:
        cadena = "{} {} {} {}\n".format(tupla[0], tupla[1], tupla[2], tupla[3])
        print(tupla)
        f.write(cadena)
    f.close()

if __name__ == '__main__':
    m, folletos = lee_fichero_imprenta("problema_imprenta_1.txt")
    solution = optimiza_folletos(m, folletos)
    escribe_fichero(solution)