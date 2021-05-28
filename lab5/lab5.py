# ADAM ADRIAN-CLAUDIU | 242

import os
import numpy as np

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


# EX 1

def orient2d(a, b, c):
    matrix = [[1, 1, 1], [a[0], b[0], c[0]], [a[1], b[1], c[1]]]
    det = np.linalg.det(matrix)
    if det * 100000 // 1 == 0:
        return 0

    return 1 if det > 0 else -1


def printDirection(det):
    if det == 0:
        print("coliniare")
    elif det < 0:
        print("dreapta")
    else:
        print("stanga")


def ex1(input_file):
    print("---- Ex 1 ----")
    input_file = getPath(input_file)
    f = open(input_file, "r")
    x = int(f.readline())
    for _ in range(x):
        points = readPoints(f, 3)
        result = orient2d(points[0], points[1], points[2])
        printDirection(result)
    f.close()


ex1("in_out_samples/1.in")


# EX 2

def getPointIndexByRule(points, rule="minXY"):
    if points == []:
        return None

    selected = points[0]
    index = 0

    if rule == "minXY":
        for i in range(len(points)):
            if selected[0] > points[i][0] or (selected[0] == points[i][0] and selected[1] > points[i][1]):
                selected = points[i]
                index = i

    if rule == "maxXY":
        for i in range(len(points)):
            if selected[0] < points[i][0] or (selected[0] == points[i][0] and selected[1] < points[i][1]):
                selected = points[i]
                index = i

    return index


def addPointToFrontier(frontier, point):
    while(len(frontier) > 1 and orient2d(frontier[-2], frontier[-1], point) <= 0):
        frontier.pop()
    frontier.append(point)


def getFrontier(points, lower=True):
    start_index = getPointIndexByRule(
        points, rule="minXY") if lower else getPointIndexByRule(points, rule="maxXY")

    n = len(points)
    frontier = [points[start_index], points[(start_index + 1) % n]]

    for i in range(n-1):
        addPointToFrontier(frontier, points[(start_index + 2 + i) % n])

    frontier.pop()
    return frontier


def ex2(input_file):
    print("---- Ex 2 ----")
    input_file = getPath(input_file)
    f = open(input_file, "r")

    _ = int(f.readline())

    points = readPoints(f)
    print(getFrontier(points))

    f.close()


ex2("in_out_samples/2.in")

# EX 3

## O(n)
def isPointInPoligon(poligon, point):
    n = len(poligon)
    for i in range(n):
        result = orient2d(poligon[i], poligon[(i + 1) % n], point)
        if result == 0:
            return 0
        if result < 0:
            return -1

    return 1


def getBounds(poligon):
    leftPoint = poligon[0]
    rightPoint = poligon[0]
    left_index , right_index = 0, 0 

    for i in range(len(poligon)):
        if leftPoint[0] > poligon[i][0]:
            leftPoint = poligon[i]
            left_index = i
        if rightPoint[0] < poligon[i][0]:
            rightPoint = poligon[i]
            right_index = i
    
    if left_index < right_index:
        return poligon[left_index : right_index + 1], poligon[right_index:] + poligon[:left_index + 1]
    else:
        return poligon[left_index :] + poligon[ : right_index + 1] , poligon[right_index : left_index + 1]


def binSearchPoint(arr, point, st, dr):
    m = (dr + st) // 2
    if dr - st <= 2:
        return st
    
    if point[0] == arr[m][0]:
        if point[0] == arr[m + 1][0]:
            return m
        if point[0] == arr[m - 1][0]:
            return m - 1

    if point[0] < arr[m][0]:
        return binSearchPoint(arr, point, st, m + 1)
    else:
        return binSearchPoint(arr, point, m, dr)


## O(log(n))
## need ascendent order by X for upper bound
def isInPoligon(l_bound, asc_u_bound, point):
    n1, n2 = len(l_bound), len(asc_u_bound)

    if point[0] < l_bound[0][0] or point[0] > l_bound[-1][0]:
        return -1

    
    index = binSearchPoint(l_bound, point, 0, n1)
    p1, p2 = l_bound[index], l_bound[index + 1]
    lorient = orient2d(p1, p2, point)

    """
    print("LOW")
    print(p1, p2)
    print(lorient)
    """

    index = binSearchPoint(asc_u_bound, point, 0, n2)
    p1, p2 = asc_u_bound[index], asc_u_bound[index + 1]
    uorient = orient2d(p2, p1, point)

    """
    print("UP")
    print(p1, p2)
    print(uorient)
    """

    if lorient == uorient:
        return 1
    elif lorient == 0 or uorient == 0:
        return 0
    else:
        return -1
        
    

def ex3(input_file):
    print("---- Ex 3 ----")
    input_file = getPath(input_file)
    f = open(input_file, "r")

    x = int(f.readline())
    poligon = readPoints(f, x)
    # print("POLIGON : {}".format(poligon))

    x = int(f.readline())
    points_check = readPoints(f, x)
    # print("POINTS TO CHECK : {}".format(points_check))

    
    # for point in points_check:
    #     result = isPointInPoligon(poligon, point)
    #     if result == 1:
    #         print("inside")
    #     if result == 0:
    #         print("on edge")
    #     if result == -1:
    #         print("outside")

    l_bound, u_bound = getBounds(poligon)
    asc_u_bound = u_bound[::-1]
    # print(l_bound, u_bound)

    for point in points_check:  
        result = isInPoligon(l_bound, asc_u_bound, point)

        if result == 1:
            print("inside")
        if result == -1:
            print("outside")
        if result == 0:
            print("on edge")
        

    f.close()


ex3("in_out_samples/3.in")
