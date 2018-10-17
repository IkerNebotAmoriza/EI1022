from algoritmia.datastructures.digraphs import UndirectedGraph
from Utils.labyrinthviewer import LabyrinthViewer
from typing import Tuple, List
from Problemas.P1.s1_p1 import create_labyrinth


def recorrer_aristas_profundidad(lab: UndirectedGraph, v_inicial: "T") -> "T | None":
    def recorrido_desde(u, v):
        seen.add(v)
        aristas.append((u, v))
        for suc in lab.succs(v):
            if suc not in seen:
                recorrido_desde(v, suc)

    aristas = []
    seen = set()
    recorrido_desde(v_inicial, v_inicial)
    return aristas


def path(g: UndirectedGraph, source: Tuple[int, int], target: Tuple[int, int]) -> List[Tuple[int, int]]:
    # obtener aristas por el recorrido en profundidad
    la = recorrer_aristas_profundidad(g, source)
    parent = {}
    for (u, v) in la:
        parent[v] = u

    camino = []

    v = target
    camino.append(v)

    while parent[v] != v:
        v = parent[v]
        camino.append(v)

    return camino


if __name__ == '__main__':
    print("Programa Principal")

    filas = 40
    columnas = 60
    celda_inicial = (0, 0)
    celda_final = (filas - 1, columnas - 1)

    lab = create_labyrinth(filas, columnas)
    camino = recorrer_aristas_profundidad(lab, celda_inicial)
    viewer = LabyrinthViewer(lab, canvas_width=800, canvas_height=500, margin=10)
    viewer.add_path(path(lab, celda_inicial, celda_final))
    viewer.run()