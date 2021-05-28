## ADAM ADRIAN-CLAUIDU | 242

import os
import numpy as np
import random

# CONSTANTS

EPSILON = 100000

# UTIL


def getPath(rel_path):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    return os.path.join(script_dir, rel_path)


def readPoint(f):
    x, y = f.readline().split()
    return (float(x), float(y))


def readPoints(f, nr=None):
    if nr == None:
        str_coords = [line.split() for line in f.readlines()]
        return list(map(lambda x: (float(x[0]), float(x[1])), str_coords))
    else:
        return [readPoint(f) for _ in range(nr)]


## Orientation test
# return :
#  -1 -> to right (C at right of AB)
#   0 -> colinear (A - B - C)
#   1 -> to left  (C at left of AB)


def orient2d(a, b, c):
    matrix = [[1, 1, 1], [a[0], b[0], c[0]], [a[1], b[1], c[1]]]
    det = np.linalg.det(matrix)
    if det * EPSILON // 1 == 0:
        return 0

    return 1 if det > 0 else -1


def getDistTwoPoints(a, b, dist="l2"):
    ax, ay = a
    bx, by = b
    if dist == "l2":
        return ((ax - bx)**2 + (ay - by)**2) / 2


def getCircumcenter(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c

    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) +
          (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) +
          (cx * cx + cy * cy) * (bx - ax)) / d
    return (ux, uy)


def isPointOnSegment(point, seg):
    if point[0] < min(seg[0][0], seg[1][0]) or point[0] > max(
            seg[0][0], seg[1][0]):
        return False
    if point[1] < min(seg[0][1], seg[1][1]) or point[1] > max(
            seg[0][1], seg[1][1]):
        return False

    return orient2d(seg[0], seg[1], point) == 0


## Intersection of 2 segments
# seg1 = [(x1, y1), (x2, y2)]
# seg2 = [(x3, y3), (x4, y4)]
###
# EX FOR ONE ORIENTATION TEST:
# [(0, 0), (2, 2)], [(2, 3), (4, 1)]
#
# EX FOR BOTH TESTS TO EXEC:
# [(2, 3), (4, 1)], [(0, 0), (2, 2)]
def isSegmentIntersect(seg1, seg2):
    ix1 = [min(seg1[0][0], seg1[1][0]), max(seg1[0][0], seg1[1][0])]
    iy1 = [min(seg1[0][1], seg1[1][1]), max(seg1[0][1], seg1[1][1])]
    ix2 = [min(seg2[0][0], seg2[1][0]), max(seg2[0][0], seg2[1][0])]
    iy2 = [min(seg2[0][1], seg2[1][1]), max(seg2[0][1], seg2[1][1])]
    iax = [max(ix1[0], ix2[0]), min(ix1[1], ix2[1])]
    iay = [max(iy1[0], iy2[0]), min(iy1[1], iy2[1])]

    if iax[0] > iax[1] or iay[0] > iay[1]:
        return False

    if orient2d(seg1[0], seg1[1], seg2[0]) * orient2d(seg1[0], seg1[1],
                                                      seg2[1]) == 1:
        return False

    if orient2d(seg2[0], seg2[1], seg1[0]) * orient2d(seg2[0], seg2[1],
                                                      seg1[1]) == 1:
        return False

    return True


## Test if a polygon is X monotone
# user should assert that polygon
# has at least 3 points
def isXmonotone(polygon):
    changes = 0
    len_polygon = len(polygon)

    direction = np.sign(polygon[1][0] - polygon[0][0])

    for i in range(len_polygon):
        p0 = polygon[i]
        p1 = polygon[(i + 1) % len_polygon]
        if direction == 0:
            return False

        if np.sign(p1[0] - p0[0]) != direction:
            changes += 1

        direction = np.sign(p1[0] - p0[0])

    return changes <= 2


def isYmonotone(polygon):
    changes = 0
    len_polygon = len(polygon)

    direction = np.sign(polygon[1][1] - polygon[0][1])

    for i in range(len_polygon):
        p0 = polygon[i]
        p1 = polygon[(i + 1) % len_polygon]
        if direction == 0:
            return False

        if np.sign(p1[1] - p0[1]) != direction:
            changes += 1

        direction = np.sign(p1[1] - p0[1])

    return changes <= 2


## Get (x_min, x_max), (y_min, y_max) for a polygon
def getPolyLimits(polygon):
    x_min, y_min = polygon[0]
    x_max, y_max = polygon[0]

    for point in polygon:
        if x_min > point[0]:
            x_min = point[0]
        if x_max < point[0]:
            x_max = point[0]
        if y_min > point[1]:
            y_min = point[1]
        if y_max < point[1]:
            y_max = point[1]

    return (x_min, x_max), (y_min, y_max)


## Get a random point
# with x not in x_range
# with y not in y_range
###
# in this case it generates a point
# in a 5x5 squre in top left corner
# of the (min_x, max_y)
def getRandomPointOutside(x_range, y_range):
    x = random.uniform(x_range[0] - 5, x_range[0])
    y = random.uniform(y_range[1] + 5, y_range[1])
    return (x, y)


## Position of a point relative to a polygon => O(n)
# return :
#  -1 -> outside
#   0 -> on edge
#   1 -> inside


def posPointToPolygon(point, polygon):
    x_range, y_range = getPolyLimits(polygon)
    martor = getRandomPointOutside(x_range, y_range)

    len_polygon = len(polygon)
    intersections = 0
    for i in range(len_polygon):
        point0 = polygon[i]
        point1 = polygon[(i + 1) % len_polygon]
        if isPointOnSegment(point, [point0, point1]):
            return 0
        if isSegmentIntersect([martor, point], [point0, point1]):
            intersections += 1

    if intersections % 2 == 0:
        return -1

    return 1


## Position of a point relative to circumcricle formed by a given triangle
# return :
#  -1 -> outside
#   0 -> on edge
#   1 -> inside
def posPointToCircumcircle(point, triangle):
    center = getCircumcenter(triangle[0], triangle[1], triangle[2])
    r = getDistTwoPoints(center, triangle[0])
    dist = getDistTwoPoints(center, point)
    return np.sign(r - dist)


## Rectangle [A, B, C, D]
# where A, B, C, D points in trigonometric order
# return :
#   0 -> no illegal edge
#   1 -> AC illegal edge
#   2 -> BD illegal edge
### Circumcenter version
def getIllegalEdge(rectangle):
    pos = posPointToCircumcircle(rectangle[3], rectangle[:3])
    if pos == 0:
        return 0
    if pos == 1:
        return 1
    if pos == -1:
        return 2


def test_ex1(in_path):
    f = open(getPath(in_path), 'r')
    n = int(f.readline().strip())
    polygon = readPoints(f, n)
    m = int(f.readline().strip())
    test_points = readPoints(f, m)
    f.close()

    for point in test_points:
        position = posPointToPolygon(point, polygon)
        if position == -1:
            print(point, "outside")
        if position == 0:
            print(point, "on edge")
        if position == 1:
            print(point, "inside")


def test_ex2(in_path):
    f = open(getPath(in_path), 'r')
    n = int(f.readline().strip())
    for i in range(n):
        m = int(f.readline().strip())
        polygon = readPoints(f, m)

        print("Poligonul {}:".format(i + 1))
        print("{} X-monoton".format(
            "este" if isXmonotone(polygon) else "nu este"))
        print("{} Y-monoton".format(
            "este" if isYmonotone(polygon) else "nu este"))
        print()

    f.close()


def test_ex3(in_path):
    f = open(getPath(in_path), 'r')
    triangle = readPoints(f, 3)
    n = int(f.readline().strip())
    test_points = readPoints(f, n)
    for point in test_points:
        pos = posPointToCircumcircle(point, triangle)
        print(point)
        if pos == -1:
            print("outside")
        if pos == 0:
            print("on edge")
        if pos == 1:
            print("inside")
    f.close()


def test_ex4():
    ## Assert trigonometric order

    [A, B, C, D] = [(0, 1), (-1, 0), (0, -1), (0, 0.5)]  # AC illegal
    #[A, B, C, D] = [(0, 1), (-1, 0), (0, -1), (0, 1)]   # no illegal
    #[A, B, C, D] = [(0, 1), (-1, 0), (0, -1), (0, 1.5)] # BD illegal

    ## Decomment this for old skool input
    # A = (float(input("ax=")), float(input("ay=")))
    # B = (float(input("bx=")), float(input("by=")))
    # C = (float(input("cx=")), float(input("cy=")))
    # D = (float(input("dx=")), float(input("dy=")))

    res = getIllegalEdge([A, B, C, D])
    if res == 0:
        print("No illegal edge")
    if res == 1:
        print("AC illegal edge")
    if res == 2:
        print("BD illegal edge")


## MAIN ##


def main():
    # test_ex1("in_out_samples/1_in.txt")
    # test_ex2("in_out_samples/2_in.txt")
    # test_ex3("in_out_samples/3_in.txt")
    test_ex4()


if __name__ == "__main__":
    main()
