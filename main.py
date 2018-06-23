import time
import math
from matplotlib import pyplot as plt
from matplotlib import animation

from particle import Particle
from quadtree import Treenode
from constants import *
from geometry import *

def main():
    '''
    x1 = -4
    y1 = 0
    x2 = 3
    y2 = 1
    px = 0
    py = 0
    r = 2
    for k in range(4):
        ax = x2 if 1 <= k <= 2 else x1
        ay = y2 if k >= 2 else y1
        bx = x2 if 1 <= (k + 1) % 4 <= 2 else x1
        by = y2 if (k + 1) % 4 >= 2 else y1
        print(disttoLineSeg(ax, ay, bx, by, px, py), ax, ay, bx, by)
        if disttoLineSeg(ax, ay, bx, by, px, py) <= r:
            print("Intersect at ", ax, ay, bx, by)
            break

    return'''
    # Initialize particles
    particles = []

    for i in range(nPar):
        particles.append(Particle(i))

    # Calculate new particle position
    def step():
        particles[:] = [x for x in particles if x.exist and (0 <= x.px <= Width and 0 <= x.py <= Height)]
        particles.sort(key=lambda x: x.r, reverse=True)
        for i in range(len(particles)):
            particles[i].id = i
        # Build new quadtree
        mx = 0
        Quadtree = Treenode(0.0, 0.0, 1.0)
        for i in particles:
            i.ax = i.ay = 0
            mx = max(mx, i.r)
            Quadtree.insertNode(i)

        # Calculate mass distributions
        Quadtree.calcMass()

        #lasttime = time.time()
        #print(len(particles), mx)

        # Calculate accelerations and update particle positions
        for i in particles:
            Quadtree.calcForce(i)

        for i in range(len(particles)):
            if particles[i].exist:
                Quadtree.checkMerge(i, particles)
                particles[i].setR()
                particles[i].updatePV()

        #print("%f" % (time.time() - lasttime))

    def visualize(particles):

        fig = plt.figure()
        ax = plt.subplot(111)
        ax.patch.set_facecolor("black")
        line = ax.scatter([], [])
        plt.xlim(0, Width)
        plt.ylim(0, Height)

        def init():
            line = ax.scatter([], [])
            return line,

        def animate(i):
            step()
            X = [x.px for x in particles]
            Y = [x.py for x in particles]
            S = [3.14 * x.r**2 for x in particles]
            C = [x.color for x in particles]
            P = list(zip(X, Y))
            line.set_offsets(P)
            line._sizes = S
            line.set_color(C)
            return line,

        anim = animation.FuncAnimation(fig, animate, init_func = init, blit = True, interval = 10)
        plt.show()

    visualize(particles)

main()

