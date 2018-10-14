import sys
from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo
from EI1022.Entregables.Entregable1.labyrinthviewer import LabyrinthViewer

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

    print("Longitud filas: ",rows)
    print("Longitud columnas: ",cols)

    fich.seek(0)
    edges=[]
    for r in range(rows):
        #Vector que guarda cada linea
        row = fich.readline().split(",")
        for c in range(cols):
            column=row[c]
            if "n" not in column:
                edges.append(((r,c),(r-1,c)))
            if "e" not in column:
                edges.append(((r,c),(r,c+1)))
    print("Laberinto creado")

    return UndirectedGraph (E=edges), rows, cols


########################################################################################################################
########################################################################################################################


def recorredor_anchura(g: UndirectedGraph, source: "T", r: int, c: int  ):
    aristas = []

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
        aristas.append((u,v))


        for s in g.succs(v):
            if s not in seen:
                seen.add(s)
                distances[s[0]][s[1]] = distances[v[0]][v[1]] +1 #en la posición del sucesor el antecesor mas 1
                queue.push((v,s))

    return aristas, distances


########################################################################################################################
########################################################################################################################


def getDistances(g: UndirectedGraph, row: int, col: int):
    recorrido = []   #lista de vertices
    inicio_fin = []  #matriz longitudes de inicio a fin
    fin_inicio = []  #matriz longitudes de fin a inicio

    init=(0,0)
    fin = (row-1,col-1)

    for r in range(row):
        inicio_fin.append([0] * col)
        fin_inicio.append([0]*col)

    recorrido, inicio_fin = recorredor_anchura(g, init, row, col)
    fin_inicio = recorredor_anchura(g, fin, row, col)[1]


    return inicio_fin, fin_inicio, recorrido


########################################################################################################################
########################################################################################################################


def recuperador_camino(lista_aristas, v):

    # CREAMOS UN DICCIONARIO DE BACKPOINTERS
    bp = {}
    for o, d in lista_aristas:
        bp[d] = o

    camino = []
    camino.append(v)
    # CONTINUAMOS MIENTRAS EL VERTICE ACTUAL NO APUNTE A SI MISMO (ARISTA FANTASMA)
    while v != bp[v]:
        v = bp[v]
        camino.append(v)

    # LE DAMOS LA VUELTA AL CAMINO YA QUE LO HEMOS RECORRIDO EN SENTIDO CONTRARIO
    camino.reverse()
    return camino


########################################################################################################################
########################################################################################################################


def derribar_pared(mInicio, mFinal, aristas,rows,cols):
    distMin = ( mInicio[0][0] + mFinal[0][0] )
    pared = ()
    for row in range(rows-1):
        for col in range(cols-1):
            if((mInicio[row][col] + mFinal[row][col+1]) < distMin):
                distMin = (mInicio[row][col] + mFinal[row][col+1])
                pared = ((row,col),(row,col+1))
            if((mInicio[row][col] + mFinal [row+1][col]) < distMin):
                distMin = (mInicio[row][col] + mFinal[row+1][col])
                pared = ((row+1,col),(row,col))
            print(distMin)
    return pared


########################################################################################################################
########################################################################################################################


if __name__ == '__main__':

    print("Numero de argumentos con los que has llamado al programa", len(sys.argv))
    if len(sys.argv) != 2:
        print("Argumentos invalidos")
        SystemExit
    else:
        print("El nombre del programa:", sys.argv[0])

    lab = load_lab(sys.argv[1])

    graph=lab[0]
    rows= lab[1]
    columns=lab[2]

    m1,m2,recorrido= getDistances(graph,rows,columns)

    print("MATRIZ INICIO A FIN ", m1)
    print("MATRIZ FIN A INICIO ", m2)
    print("RECORRIDO ",recorrido)

    pared = derribar_pared(m1,m2,recorrido,rows,columns)
    print("PARED A DERRIBAR ",pared)


    viewer = LabyrinthViewer(graph, canvas_width=800, canvas_height=480, margin=10)
    viewer.add_marked_cell(pared[0], 'red')
    viewer.add_marked_cell(pared[1], 'red')
    viewer.run()