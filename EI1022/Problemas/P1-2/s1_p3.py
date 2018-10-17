from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.digraphs import UndirectedGraph
import random

from algoritmia.datastructures.queues import Fifo

from Utils.labyrinthviewer import LabyrinthViewer


def create_labyrinth_mod(rows: int, cols: int, n=0) -> UndirectedGraph:
    # Paso 1 = Creamos una lista con los vertices de nuestro grafo
    vertices = [(r, c) for r in range(rows) for c in range(cols)]

    # Paso 2 = Creamos un MergeFindSet vacio y le vamos añadiendo UNO A UNO
    # los vertices de la lista creada en el paso 1
    mfs = MergeFindSet()
    for v in vertices:
        mfs.add(v)

    # Paso 3 = Creamos una lista llamada "edges" con los pares de vertices
    # vecinos, y la barajamos
    edges = []
    for (r, c) in vertices:
        if r + 1 < rows:
            edges.append(((r, c), (r + 1, c)))
        if c + 1 < cols:
            edges.append(((r, c), (r, c + 1)))

    random.shuffle(edges)

    # Paso 4 = Creamos una lista vacia que contiene los pasillos del laberinto
    corridors = []
    discarded_edges = []

    # Paso 5 = Recorremos la lista de bordes, y para cada arista (u, v),
    # encuentra la clase a la que pertenece cada uno de los vertices
    # usando "find()". u y v son VERTICES, u = (r,c) y v = (r2,c2)
    for (u, v) in edges:
        if mfs.find(u) != mfs.find(v):
            mfs.merge(u, v)
            corridors.append((u, v))
        else:
            discarded_edges.append((u,v))
    corridors.extend(discarded_edges[:n])

    # Paso 6 = Devolvemos el resultado
    return UndirectedGraph(E=corridors)


def recorredor_aristas_anchura(grafo, v_inicial):
    aristas = []
    queue = Fifo()
    seen = set()
    queue.push((v_inicial, v_inicial))
    seen.add(v_inicial)

    while len(queue)>0:
        u,v=queue.pop()
        aristas.append((u,v))
        for suc in grafo.succs(v):
            if suc not in seen:
                seen.add(suc)
                queue.push((v,suc))
    return aristas


def recuperador_camino(lista_aristas, v):
    bp = {}
    for o,d in lista_aristas:
        bp[d] = o

    camino = []
    camino.append(v)
    while v != bp[v]:
        v = bp[v]
        camino.append(v)
    camino.reverse()
    return camino


if __name__ == '__main__':
    random.seed(42)

    # creamos el laberinto con 'num_paredes_quitadas'
    num_rows = 80
    num_cols = 140
    num_paredes_quitadas = 20
    celda_entrada = (0,0)
    celda_salida = (num_rows-1, num_cols-1)

    lab = create_labyrinth_mod(num_rows,num_cols,num_paredes_quitadas)
    aristas = recorredor_aristas_anchura(lab,celda_entrada)
    camino = recuperador_camino(aristas, celda_salida)
    lv = LabyrinthViewer(lab,canvas_width=800, canvas_height=480, margin=10)
    lv.add_path(camino)
    lv.run()