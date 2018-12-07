import statistics as stats
from typing import *
from operator import itemgetter
from EI1022.Entregables.Entregable4.kdtree import KDTree, KDLeaf, Axis, KDNode


def read_points(filename: str) -> List[Tuple[float,float]]:
    fich = open(filename)
    points = []
    for line in fich:
        x,y = line.split(" ")
        points.append((float(x),float(y)))
    return points


def build_kd_tree(points: List[Tuple[float,float]]) -> KDTree:
    def func(conj: List[Tuple[float,float]]):
        if len(conj) == 1:
            return KDLeaf(conj[0])

        # Escojer el eje
        difX = max(conj, key=itemgetter(0))[0] - min(conj, key=itemgetter(0))[0]
        difY = max(conj, key=itemgetter(1))[1] - min(conj, key=itemgetter(1))[1]
        #xlist = []
        #ylist = []

        xOrder = conj[:]
        yOrder = conj[:]
        xOrder.sort(key=lambda x: x[0])
        yOrder.sort(key=lambda y: y[1])

        #for i in range(len(xOrder)):
        #   xlist.append(xOrder[i][0])
        #    ylist.append(yOrder[i][1])

        if difX >= difY:
           axis = Axis.X
           middle, left, right = median(xOrder, 0)

           #med = stats.median(xlist)
           #list_left, list_right = comparation(xOrder,med,0)
           left = func(left)
           right = func(right)

        else:
            axis = Axis.Y
            middle, left, right = median(yOrder, 1)

            #med = stats.median(ylist)
            #list_left, list_right = comparation(yOrder, med, 1)
            left = func(left)
            right = func(right)

        return KDNode(axis,middle,left,right)


    tree = func(points)
    return tree


def median(sorted_points: List[Tuple[float,float]], axis: int):
    mid_point = len(sorted_points)//2
    if len(sorted_points)%2 == 0:
        middle = (sorted_points[mid_point-1][axis]+sorted_points[mid_point][axis])/2
    else:
        middle = sorted_points[mid_point][axis]
    left = sorted_points[0:mid_point-1]
    right = sorted_points[mid_point:]
    return middle, left, right


def comparation(conj: List[Tuple[float,float]], mid: float, axis: int):
    left = []
    right = []
    if(axis==0):
        for i in range(len(conj)):
            if conj[i][0]< mid:
                left.append(conj[i])
            else:
                right.append(conj[i])
    else:
        for i in range(len(conj)):
            if conj[i][1]< mid:
                left.append(conj[i])
            else:
                right.append(conj[i])

    return left,right


if __name__ == '__main__':
    tuple = read_points("points2d_100.txt")
    kdtree = build_kd_tree(tuple)
    print(kdtree.pretty())