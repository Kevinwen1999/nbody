import math
from quadtree import *
from constants import *


def distBetweenPoints(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Test if point is inside rectangle
def insideRectangle(x1, x2, y1, y2, xx, yy):
    return (x1 <= xx <= x2) and (y1 <= yy <= y2)


# Get coordinate of top corner of a quadrant
def getTopCoordinate(i, q):
    tx, ty = i.x, i.y
    w, h = Width / i.w / 2, Height / i.w / 2,
    if q > 1:
        tx += w
    if q % 2 != 0:
        ty += h
    return tx, ty


# Get Quadrant of particle
def getQuadrant(a, i):
    tx, ty = i.x, i.y
    w, h = Width / i.w / 2.0, Height / i.w / 2.0
    for j in range(4):
        nx, ny = getTopCoordinate(i, j)
        if insideRectangle(nx, nx + w, ny, ny + h, a.px, a.py):
            return j
    return 0


# Calculate acceleration of particle a due to b
def getAcceleration(bx, by, bm, a):
    dx = bx - a.px
    dy = by - a.py
    dist2 = dx * dx + dy * dy
    gforce = GC * bm * a.mass / dist2 if dist2 > 1e-9 else 0.0
    dist = math.sqrt(dist2)
    if dist == 0.0:
        return 0, 0
    # Using Gravitational Force Formula for vector quantities
    return gforce / dist * dx, gforce / dist * dy

# Determine if a circle is inside a rectangle
def checkCirinRec(cx, cy, r, x1, x2, y1, y2):
    return True if (x1 <= cx - r) and (cx + r <= x2) and (y1 <= cy - r) and (cy + r <= y2) else False


# Determine if a rectangle is inside a circle
def checkRecinCir(cx, cy, r, x1, x2, y1, y2):
    return True if (x1 >= cx - r) and (cx + r >= x2) and (y1 >= cy - r) and (cy + r >= y2) else False


# Convert points to vector
def getVec(ax, ay, bx, by):
    return bx - ax, by - ay


def dot(ax, ay, bx, by):
    return ax * bx + ay * by


def translate(ax, ay, bx, by):
    return ax + bx, ay + by


def scale(ax, ay, f):
    return ax * f, ay * f


def disttoLineSeg(ax, ay, bx, by, px, py):
    apx, apy = getVec(ax, ay, px, py)
    bpx, bpy = getVec(bx, by, px, py)
    u = dot(apx, apy, bpx, bpy) / dot(bx - ax, by - ay, bx - ax, by - ay)
    if u < 0.0:
        return distBetweenPoints(ax, ay, px, py)
    elif u > 1.0:
        return distBetweenPoints(bx, by, px, py)
    else:
        tx, ty = scale(bx - ax, by - ay, u)
        cx, cy = translate(ax, ay, tx, ty)
        return distBetweenPoints(px, py, cx, cy)
