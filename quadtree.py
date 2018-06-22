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
        self.tm = 0
        # id of node stored
        self.nid = 0

    # Insert a particle into the tree
    def insertNode(self, a):
        if self.n == 0:
            self.n += 1
            self.cx = a.px * a.mass
            self.cy = a.py * a.mass
            self.tm = a.mass
            self.nid = a.id
        else:
            q = getQuadrant(a, self)
            if self.child[q] is None:
                nx, ny = getTopCoordinate(self, q)
                self.child[q] = Treenode(nx, ny, self.w * 2)
            self.n += 1
            self.child[q].insertNode(a)

    # Calculate mass and center of mass
    def calcMass(self):
        if self.n > 1:
            self.tm = 0
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
            tax, tay = getAcceleration(self.cx, self.cy, self.tm, a)
            a.ax += tax
            a.ay += tay
        else:
            for j in range(4):
                if self.child[j] is None:
                    continue
                self.child[j].calcForce(a)

    # Merge particles that are too close
    def checkMerge(self, a, par):
        if self.n == 1:
            if self.nid == par[a].id or par[self.nid].exist == False:
                return
            # If collide, merge and conserve momentum
            if distBetweenPoints(self.cx, self.cy, par[a].px, par[a].py) <= par[a].r + par[self.nid].r:
                par[self.nid].exist = False
                par[a].vx = (par[a].vx * par[a].mass + par[self.nid].vx * par[self.nid].mass) / (par[a].mass + par[self.nid].mass)
                par[a].vy = (par[a].vy * par[a].mass + par[self.nid].vy * par[self.nid].mass) / (par[a].mass + par[self.nid].mass)
                par[a].mass += par[self.nid].mass
            return
        for j in range(4):
            if self.child[j] is None:
                continue
            x1, y1 = getTopCoordinate(self, j)
            w, h = Width / self.w / 2.0, Height / self.w / 2.0
            x2 = x1 + w
            y2 = y1 + h
            if checkCirinRec(par[a].px, par[a].py, par[a].r, x1, x2, y1, y2) or checkRecinCir(par[a].px, par[a].py, par[a].r, x1, x2, y1, y2):
                self.child[j].checkMerge(a, par)
            else:
                for k in range(4):
                    ax = x2 if 1 <= k <= 2 else x1
                    ay = y2 if k >= 2 else y1
                    bx = x2 if 1 <= (k + 1) % 4 <= 2 else x1
                    by = y2 if (k + 1) % 4 >= 2 else y1
                    if disttoLineSeg(ax, ay, bx, by, par[a].px, par[a].py) <= par[a].r:
                        self.child[j].checkMerge(a, par)
                        break
