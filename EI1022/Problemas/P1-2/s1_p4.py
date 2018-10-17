from algoritmia.datastructures.digraphs import UndirectedGraph

from Utils.graph2dviewer import Graph2dViewer
from Problemas.P1.s1_p3 import recorredor_aristas_anchura

def horse_graph(rows, cols):
    edges = []
    saltos = [(1,-2),(2,-1),(2,1),(1,2)]
    for r in range(rows):
        for c in range(cols):
            for (ri,ci) in saltos:
                if r+ri < rows and 0 <= c+ci < cols:
                    edges.append(((r,c),(r+ri,c+ci)))

    return UndirectedGraph(E = edges)


def casillas_alcanzables(grafo, vertice_inicial):
    return len(recorredor_aristas_anchura(grafo,vertice_inicial))

def matriz_saltos(g,num_rows,num_cols):
    m=[] #m es una matriz de distancias, donde cada casilla es la distancia de saltos al origen del caballo
         #porque cada arco del grafo que nos pasa la funcion de matriz de saltos es un salto

    for r in range( num_rows):
        m.append( [0] * num_cols)

    #copiar el codigo del recorredor de aristas en anchura y modificarlo para rellenar a la vez la matriz m
    ################################################################################################################
    #IMPLEMENTAR
    ################################################################################################################
    return m


if __name__ == '__main__':
    num_rows=8
    num_cols=8
    grafo_tablero=horse_graph(num_rows,num_cols)

    print(casillas_alcanzables(grafo_tablero,(0,3)))

    viewer = Graph2dViewer(grafo_tablero, window_size=(600,600), vertexmode=Graph2dViewer.ROW_COL)
    viewer.run()