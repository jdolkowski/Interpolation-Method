import random
import math
from itertools import combinations

import numpy as np


class HalfPlane:
    def __init__(self, x, y, direction, b):
        self.x = x
        self.y = y
        self.direction = direction  # up or down
        self.b = b


class Objective:
    def __init__(self, x, y, type):  # max or min
        self.x = x
        self.y = y
        self.type = type
        self.b = 0


def RandomPermute(A):  # a array A[1...n]
    n = len(A)
    k = n - 1
    while k >= 1:
        A[k], A[random.randint(0, k)] = A[random.randint(0, k)], A[k]  # value swap
        k -= 1


def PreProcess(H, c):
    minPhi = angle(H[0], c)
    minI = 0

    for i in range(0, len(H)):
        if angle(H[i], c) < minPhi:
            minPhi = angle(H[i], c)
            minI = i
    if minI is not None:
        H[minI], H[0] = H[0], H[minI]

    return True


def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dotproduct(v, v))


def angle(h, c):
    v1 = [h.x, h.y]
    v2 = [c.x, c.y]
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


def within_borders(h, v):
    if h.direction == 'up':
        if v[0] * h.x + v[1] * h.y >= h.b:
            return True
        else:
            return False
    elif h.direction == 'down':
        if v[0] * h.x + v[1] * h.y <= h.b:
            return True
        else:
            return False


def where_intersect(a, b):
    w = a.x * b.y - b.x * a.y
    wx = a.b * b.y - b.b * a.y
    wy = a.x * b.b - b.x * a.b
    if w != 0:
        return [wx / w, wy / w]
    else:
        return None


def find_optimal(points, obj):
    maximum = [0, 0]
    if obj.type == 'max':
        maximum[0] = points[0][0]
        maximum[1] = points[0][1]
        for p in points[1:]:
            if p[0] * obj.x + p[1] * obj.y > maximum[0] + maximum[1]:
                maximum[0] = p[0]
                maximum[1] = p[1]
        return maximum
    elif obj.type == 'min':
        maximum[0] = points[0][0]
        maximum[1] = points[0][1]
        for p in points[1:]:
            if p[0] * obj.x + p[1] * obj.y < maximum[0] + maximum[1]:
                maximum[0] = p[0]
                maximum[1] = p[1]
        return maximum


def solution(H, c):  # H = { H(0), H(1), … , H(n)} n half-planes, c = objective vector
    if not PreProcess(H, c):
        print('could not resolve')
        return None
    else:
        v = [None] * len(H)

        v[1] = where_intersect(H[0], H[1])

        RandomPermute(H[2:])

        for i in range(2, len(H)-1):
            if within_borders(H[i], v[i - 1]):  # within a halfplane H0
                v[i] = v[i - 1]
            else:
                p = find_optimal(v, c)
                v[i] = p
                if not p:
                    print('could not resolve')

        return v[len(H) - 2]


if __name__ == "__main__":
    objective = Objective(3, 4, 'max')

    constraints = []
    constrain1 = HalfPlane(2, 3, 'down', 4)
    constrain2 = HalfPlane(2, 5, 'down', 5)
    constrain3 = HalfPlane(2, 1, 'down', 3)
    constrain4 = HalfPlane(3, 4, 'down', 2)
    constrain5 = HalfPlane(0, -1, 'down', 0)
    constrain6 = HalfPlane(-1, 0, 'down', 0)
    constraints.append(constrain1)
    constraints.append(constrain2)
    constraints.append(constrain3)
    constraints.append(constrain4)
    constraints.append(constrain5)
    constraints.append(constrain6)

    print(solution(constraints, objective))
