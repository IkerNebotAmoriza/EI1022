import sys
from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo
from EI1022.Entregables.Entregable1.labyrinthviewer import LabyrinthViewer


########################################################################################################################
########################################################################################################################

def load_labyrinth(fichero) -> UndirectedGraph:
    # ABRIMOS EL FICHERO
    fich = open(fichero)

    # LEEMOS LA PRIMERA LINEA DEL FICHERO Y CONTAMOS EL NUMERO DE COLUMNAS
    cols = len(fich.readline().split(","))
    # LEEMOS EL RESTO DE LINEAS DEL FICHERO Y CONTAMOS EL NUMERO DE FILAS
    rows = len(fich.readlines()) + 1

    # VOLVEMOS AL INICIOD EL FICHERO Y CREAMOS UNA LISTA DE ARISTAS
    fich.seek(0)
    edges = []

    # PARA CADA CELDA DEL LABERINTO CONSULTAMOS SU INFORMACION EN EL FICHERO
    for r in range(rows):
        # GUARDAMOS EN UNA VECTOR AUXILIAR LOS DATOS PARA CADA FILA
        auxRow = fich.readline().split(",")

        for c in range(cols):
            # GUARDAMOS EN UNA VARIABLE AUXILIAR EL VALOR PARA CADA CELDA DE LA FILA
            auxCell = auxRow[c]
            # AÑADIMOS ARISTAS A LA LISTA DE ARISTAS EN FUNCION A LOS DATOS DE LA CELDA
            # (PARA EVITAR ARISTAS REPETIDAS SOLO EVALUAMOS SI HAY MUROS AL NORTE Y AL ESTE)
            if "n" not in auxCell:
                edges.append(((r, c), (r - 1, c)))
            if "e" not in auxCell:
                edges.append(((r, c), (r, c + 1)))

    # CUANDO TODAS LAS ARISTAS HAN SIDO AÑADIDAS CREAMOS Y DEVOLVEMOS EL GRAFO
    return UndirectedGraph(E=edges), rows, cols


########################################################################################################################
########################################################################################################################


def recorredor_aristas_anchura(grafo, v_inicial):
    # CREAMOS LA LISTA DE ARISTAS, LA COLA Y EL SET QUE VAMOS A UTILIZAR
    aristas = []
    queue = Fifo()
    seen = set()
    # INTRODUCIMOS EN LA COLA LA PRIMERA ARISTA, QUE EMPIEZA Y ACABA SOBRE SI MISMA (ARISTA FANTASMA)
    queue.push((v_inicial, v_inicial))
    # Y LA AÑADIMOS AL SET DE VERTICES VISTOS
    seen.add(v_inicial)

    # CONTINUAMOS MIENTRAS QUEDEN ELEMENTOS EN LA COLA
    while len(queue) > 0:
        u, v = queue.pop()
        aristas.append((u, v))
        # CONSULTAMOS LOS SUCESORES DEL VERTICE QUE SACAMOS DE LA COLA
        for suc in grafo.succs(v):
            # Y SI NO HAN SIDO VISITADOS AÑADIMOS EL VERTICE PADRE AL SET DE VISTOS Y SUS SUCESORES A LA COLA
            if suc not in seen:
                seen.add(suc)
                queue.push((v, suc))

    # DEVOLVEMOS LA LISTA DE ARISTAS DEL RECORRIDO
    return aristas


########################################################################################################################
########################################################################################################################


def recuperador_camino(lista_aristas, v):
    # CREAMOS UN DICCIONARIO DE BACKPOINTERS
    bp = {}
    # Y LO LLENAMOS CON LA LISTA DE ARISTAS
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
    # Y DEVOLVEMOS EL CAMINO
    return camino


########################################################################################################################
########################################################################################################################


def getDistances(lab: UndirectedGraph, rows: int, cols: int):
    # CREAMOS LA MATRIZ DE DISTANCIAS
    distancias = []

    for r in range(rows):
        distancias.append([])
        for c in range(cols):
            # RECORREMOS EL LABERINTO DESDE CADA CELDA DEL MISMO
            aristas = recorredor_aristas_anchura(lab, (r, c))
            # GUARDAMOS LA DISTANCIA HASTA LA ENTRADA
            distEntrada = len(recuperador_camino(aristas, (0, 0)))
            # GUARDAMOS LA DISTANCIA HASTA LA SALIDA
            distSalida = len(recuperador_camino(aristas, (rows - 1, cols - 1)))

            # Y LAS AÑADIMOS A SU CELDA CORRESPONDIENTE EN LA MATRIZ
            distancias[r].append((distEntrada, distSalida))

    # DEVOLVEMOS LA MATRIZ DE DISTANCIAS
    return distancias


########################################################################################################################
########################################################################################################################


if __name__ == '__main__':
    print("Numero de argumentos con los que has llamado al programa", len(sys.argv))
    if len(sys.argv) != 2:
        print("Argumentos invalidos")
        SystemExit
    else:
        print("El nombre del programa:", sys.argv[0])

    lab, rows, cols = load_labyrinth(sys.argv[1])
    celda_final = (rows - 1, cols - 1)
    celda_entrada = (0, 0)

    aristas = recorredor_aristas_anchura(lab, celda_entrada)
    camino = recuperador_camino(aristas, celda_final)

    x = getDistances(lab, rows, cols)

    for r in range(rows):
        fila = []
        for c in range(cols):
            fila.append(x[r][c])
        print(fila)

    viewer = LabyrinthViewer(lab, canvas_width=800, canvas_height=480, margin=10)
    viewer.add_path(camino)
    viewer.run();
