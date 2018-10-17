from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.digraphs import UndirectedGraph
import random
from Utils.labyrinthviewer import LabyrinthViewer


def create_labyrinth(rows: int, cols: int) -> UndirectedGraph:
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

    # Paso 5 = Recorremos la lista de bordes, y para cada arista (u, v),
    # encuentra la clase a la que pertenece cada uno de los vertices
    # usando "find()". u y v son VERTICES, u = (r,c) y v = (r2,c2)
    for (u, v) in edges:
        if mfs.find(u) != mfs.find(v):
            mfs.merge(u, v)
            corridors.append((u, v))

    # Paso 6 = Devolvemos el resultado
    return UndirectedGraph(E=corridors)


if __name__ == '__main__':
    print('Programa Principal')
    lab = create_labyrinth(40, 60)
    viewer = LabyrinthViewer(lab, canvas_width=800, canvas_height=500, margin=10)
    viewer.run()