## ADAM ADRIAN-CLAUDIU | 242

import os
from sys import maxsize

# UTIL


def get_path(rel_path):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    return os.path.join(script_dir, rel_path)


def read_planes(fd, n):
    return [[float(elem) for elem in fd.readline().split()] for _ in range(n)]


## Intersection of planes
# O(n)
# return :
#  -1 -> void intersection
#   0 -> unbounded intersection
#   1 -> bounded intersection

## For a, b, c  -  real numbers
# planeN = [a, b, c]     a.i.     a*x + b*y + c <= 0
# planes = [plane0, plane1, ...]


def intersection_of_planes(planes):
    min_x, max_x, min_y, max_y = None, None, None, None
    # if x >= 2 then min_x = 2
    # if x <= 4 then max_x = 4
    # analog y

    for [a, b, c] in planes:
        if a == 0:
            if b > 0:
                sup_y = (-1 * c) / b
                max_y = sup_y if max_y == None else min(sup_y, max_y)
            else:
                inf_y = (-1 * c) / b
                min_y = inf_y if min_y == None else max(inf_y, min_y)
        else:
            if a > 0:
                sup_x = (-1 * c) / a
                max_x = sup_x if max_x == None else min(sup_x, max_x)
            else:
                inf_x = (-1 * c) / a
                min_x = inf_x if min_x == None else max(inf_x, min_x)

    intersect_x = -1
    intersect_y = -1

    if min_x != None and max_x != None and min_x < max_x:
        intersect_x = 1

    if min_y != None and max_y != None and min_y < max_y:
        intersect_y = 1

    return (intersect_x + intersect_y) // 2


## return :
#   1 -> point in plane (even on edge)
#   0 -> point not in plane
def is_point_in_plane(plane, point):
    a, b, c = plane
    x, y = point
    if a == 0:
        if b > 0:
            if y <= (-1 * c) / b:
                return 1
        else:
            if y >= (-1 * c) / b:
                return 1
    else:
        if a > 0:
            if x <= (-1 * c) / a:
                return 1
        else:
            if x >= (-1 * c) / a:
                return 1
    return 0


# O(n)
## return :
#   min_area -> point in rectangle (even on edge)
#   -1 -> point not in rectangle
def get_min_area_of_rectangle_intersection_with_point(planes, point):
    min_x, max_x, min_y, max_y = None, None, None, None
    for plane in planes:
        if is_point_in_plane(plane, point):
            a, b, c = plane
            if a == 0:
                if b > 0:
                    sup_y = (-1 * c) / b
                    max_y = sup_y if max_y == None else min(sup_y, max_y)
                else:
                    inf_y = (-1 * c) / b
                    min_y = inf_y if min_y == None else max(inf_y, min_y)
            else:
                if a > 0:
                    sup_x = (-1 * c) / a
                    max_x = sup_x if max_x == None else min(sup_x, max_x)
                else:
                    inf_x = (-1 * c) / a
                    min_x = inf_x if min_x == None else max(inf_x, min_x)

    if min_x == None or max_x == None or min_y == None or max_y == None:
        return -1

    area = (max_x - min_x) * (max_y - min_y)
    return -1 if area < 0 else area


# SOLVES


def test_ex1(in_path):
    print("EXERCITIUL 1")
    f = open(get_path(in_path), 'r')
    n = int(f.readline().strip())

    for i in range(n):
        m = int(f.readline().strip())
        planes = read_planes(f, m)
        sol = intersection_of_planes(planes)

        print(f"exemplul {i+1}")
        if sol == -1:
            print("intersectie vida")
        if sol == 0:
            print("intersectie nevida, nemarginita")
        if sol == 1:
            print("intersectie nevida, marginita")
        print()

    f.close()


def test_ex2(in_path):
    print("EXERCITIUL 2")
    f = open(get_path(in_path), 'r')
    n = int(f.readline().strip())

    for i in range(n):
        Q = tuple(float(elem) for elem in f.readline().split())
        m = int(f.readline().strip())
        planes = read_planes(f, m)
        sol = get_min_area_of_rectangle_intersection_with_point(planes, Q)

        print(f"exemplul {i+1}")
        if sol == -1:
            print("(a) nu exista un dreptunghi cu proprietatea ceruta")
        else:
            print("(a) exista un dreptunghi cu proprietatea ceruta")
            print(f"(b) ARIA MINIMA ESTE: {sol}")
        print()

    f.close()


if __name__ == '__main__':
    test_ex1('in_out_samples/1_in.txt')
    test_ex2('in_out_samples/2_in.txt')