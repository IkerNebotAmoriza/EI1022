import sys
from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo


########################################################################################################################
########################################################################################################################


def load_lab(fichero):
    fich= open(fichero)

    #Lee la primera linea
    #cols = len de la lista que devuelve split
    cols = len(fich.readline().split(","))

    #Lee el resto de filas
    #rows = num de filas + la leida antes
    rows = len(fich.readlines())+1

    fich.seek(0)
    edges=[]
    for r in range(rows):
        #Vector que guarda cada linea
        row = fich.readline().split(",")
        for c in range(cols):
            column=row[c]
            #Si la celda no tiene pared al norte o al este se añaden los pasillos
            if "s" not in column:
                edges.append(((r,c),(r+1,c)))
            if "e" not in column:
                edges.append(((r,c),(r,c+1)))

    #Devolvemos el grafo construido, junto con sus dimensiones
    return UndirectedGraph (E=edges), rows, cols


########################################################################################################################
########################################################################################################################


def recorredor_anchura(g: UndirectedGraph, source: "T", r: int, c: int  ):
    #Crear e inicializar matriz
    distances = []
    for row in range(r):
        distances.append([0]*c)

    queue = Fifo()
    seen = set()

    #Añadir el punto inicial a la cola
    queue.push((source,source))
    seen.add(source)

    while len(queue) > 0:
        u,v= queue.pop()
        #Miramos los sucesores del elemento extraido de la cola
        for s in g.succs(v):
            #Si no lo hemos visitado ya lo añadimos a los visitados y anotamos en la matriz su distancia al origen
            if s not in seen:
                seen.add(s)
                distances[s[0]][s[1]] = distances[v[0]][v[1]] +1 #En la posición del sucesor el antecesor mas 1
                queue.push((v,s))

    return distances


########################################################################################################################
########################################################################################################################


def getDistances(g: UndirectedGraph, row: int, col: int):
    #Declaramos las celdas de origen y final
    init=(0,0)
    fin = (row-1,col-1)

    #Y mediante una llamada al recorredor de anchura recuperamos la matriz de distancias para cada origen
    inicio_fin = recorredor_anchura(g, init, row, col)
    fin_inicio = recorredor_anchura(g, fin, row, col)

    #Devolvemos las matrices
    return inicio_fin, fin_inicio


########################################################################################################################
########################################################################################################################


def derribar_pared(mInicio, mFinal, rows,cols):
    distMin = ( mInicio[0][0] + mFinal[0][0] )
    pared = ()
    #Recorremos las filas y columnas del laberinto
    for row in range(rows):
        for col in range(cols):
            #Y para cada una de ellas comprobamos la suma minima de distancias para sus celdas este y sur
            if(col != cols-1 and (mInicio[row][col]+mFinal[row][col+1]) < distMin):
                distMin = (mInicio[row][col]+mFinal[row][col+1])
                pared = ((row,col),(row,col+1))

            if(row != rows-1 and (mInicio[row][col] + mFinal [row+1][col]) < distMin):
                distMin = (mInicio[row][col] + mFinal [row+1][col])
                pared = ((row+1,col),(row,col))

    #Devolvemos la pared que consigue la suma minima de distancias, y la longitud de su recorrido
    return pared, distMin+1


########################################################################################################################
########################################################################################################################


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Argumentos invalidos")
        SystemExit

    #Creamos el grafo del laberinto y asignamos los argumentos
    lab = load_lab(sys.argv[1])
    graph=lab[0]
    rows= lab[1]
    columns=lab[2]

    #Creamos las matrices de distancias
    m1,m2= getDistances(graph,rows,columns)

    #Buscamos la pared que consigue el camino mas corto
    pared,distMin = derribar_pared(m1,m2,rows,columns)

    #Mostramos por pantalla el resultado en el orden y formato indicados
    if pared[0] < pared [1]:
        c1 = pared[0]
        c2 = pared[1]
    else:
        c1 = pared[1]
        c2 = pared[0]

    print(c1[0], c1[1], c2[0], c2[1])
    print(m2[0][0])
    print(distMin)