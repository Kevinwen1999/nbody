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