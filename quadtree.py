from geometry import *
from particle import *
from constants import *
# Quadtree class


class Treenode:
    def __init__(self, x, y, w):
        # Top corner position of the block
        self.x = x
        self.y = y
        # Dimension factor
        self.w = w
        # Total particles in node
        self.n = 0
        # Pointers to childrens
        self.child = [None] * 4
        # Center of mass position, calculated as weighted means
        self.cx = x
        self.cy = y
        # Total mass
        self.tm = 0,

    # Insert a particle into the tree
    def insertNode(self, a):
        if self.n == 0:
            self.n += 1
            self.cx = a.px * a.mass
            self.cy = a.py * a.mass
            self.tm = a.mass
        else:
            q = getQuadrant(a, self)
            if self.child[q] is None:
                nx, ny = getTopCoordinate(self, q)
                self.child[q] = Treenode(nx, ny, self.w * 2)
            self.n += 1
            self.child[q].insertNode(a)

    # Calculate mass and center of mass
    def calcMass(self):
        for j in range(4):
            if self.child[j] is None:
                continue
            self.child[j].calcMass()
            self.tm += self.child[j].tm
            self.cx += self.child[j].tm * self.child[j].cx
            self.cy += self.child[j].tm * self.child[j].cy
        self.cx /= self.tm
        self.cy /= self.tm

    # Calculate force base on barnes hut optimization
    def calcForce(self, a):
        # Calculate multiple acceptance criterion
        r = distBetweenPoints(self.cx, self.cy, a.px, a.py)
        d = Width / self.w
        if r == 0 or d / r < Theta or self.n == 1:
            tp = Particle()
            tp.setP(self.cx, self.cy, self.tm)
            tax, tay = getAcceleration(self.cx, self.cy, self.tm, a)
            a.ax += tax
            a.ay += tay
        else:
            for j in range(4):
                if self.child[j] is None:
                    continue
                self.child[j].calcForce(a)
