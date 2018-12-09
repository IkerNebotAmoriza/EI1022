import statistics as stats
import sys
from typing import *
from EI1022.Entregables.Entregable4.kdtree import KDTree, KDLeaf, Axis, KDNode


def read_points(filename: str) -> List[Tuple[float, float]]:
    file = open(filename)
    points = []
    for line in file:
        x, y = line.split(" ")
        points.append((float(x), float(y)))
    return points


def build_kd_tree(points: List[Tuple[float, float]]) -> KDTree:
    def splitter(p: List[Tuple[float, float]]):  # Recursive function
        if len(p) == 1:  # Returns a KDLeaf if the actual node is a leaf
            return KDLeaf(p[0])

        # Obtains both axis lengths
        x_len = max(p, key=lambda x: x[0])[0] - min(p, key=lambda x: x[0])[0]
        y_len = max(p, key=lambda y: y[1])[1] - min(p, key=lambda y: y[1])[1]

        # Sorts the points according to the largest axis
        sorted_p = p[:]
        if x_len >= y_len:
            n_axis = 0
            axis = Axis.X
            sorted_p.sort(key=lambda x: x[n_axis])
        else:
            n_axis = 1
            axis = Axis.Y
            sorted_p.sort(key=lambda x: x[n_axis])

        # In order to use 'stats.median' creates a list with only the longest axis coordinates
        aux_list = []
        for i in range(len(sorted_p)):
            aux_list.append(sorted_p[i][n_axis])

        # Obtains KDNode parameters
        med = stats.median(aux_list)
        list_left, list_right = get_subtree(sorted_p, med, n_axis)
        left = splitter(list_left)
        right = splitter(list_right)

        return KDNode(axis, med, left, right)

    tree = splitter(points)
    return tree


# Obtains left and right subtrees of a KDNode
def get_subtree(sorted_p: List[Tuple[float, float]], mid: float, axis: int):
    left = []
    right = []

    for i in range(len(sorted_p)):  # If the actual point belongs to the left subtree
        if sorted_p[i][axis] < mid:
            left.append(sorted_p[i])
        else:  # If the actual point belongs to the right subtree
            right.append(sorted_p[i])

    return left, right


if __name__ == '__main__':
    r_points = read_points(sys.argv[1])
    kdt = build_kd_tree(r_points)
    print(kdt.pretty())
