import math
import pygame
import random
import time

from particle import Particle
from quadtree import Treenode
from constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((Width, Height))

    # Initialize particles
    particles = []
    pressed = {pygame.K_i: False, pygame.K_k: False, pygame.K_ESCAPE: False, pygame.K_SPACE: False}

    for i in range(nPar):
        particles.append(Particle())

    # Zoom coefficient
    zoom = 1.0
    # Zoompoint
    zx = Width / 2.0
    zy = Height / 2.0

    # Show/hide Orbits
    showTrail = False

    framecount = 0
    lasttime = 0

    while True:
        # print("zx: %f, zy: %f\n" % (zx, zy))
        # print("px: %f, py: %f\n" % (particles[0].px, particles[0].py))
        # print("%f" % zoom)

        pygame.display.flip()
        if not showTrail:
            screen.fill((0, 0, 0))

        # Remove merged particles
        particles[:] = [x for x in particles if x.exist and (0 <= x.px <= Width and 0 <= x.py <= Height)]

        # Paint all particles
        for i in particles:
            # Scaling: Set zoompoint as origin, then apply zoom factor
            pygame.draw.circle(screen, i.color, (int(round(((i.px - zx) * zoom + zx), 0)), int(round(((i.py - zy) * zoom + zy), 0))), int(i.r * zoom), 0)

        # Check keys
        while True:
            event = pygame.event.poll()
            if event.type == pygame.NOEVENT:
                break
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                pressed[event.key] = event.type == pygame.KEYDOWN


        Quadtree = Treenode(0.0, 0.0, 1.0)
        for i in particles:
            i.ax = i.ay = 0
            Quadtree.insertNode(i)

        Quadtree.calcMass()

        lasttime = time.time()
        for i in particles:
            Quadtree.calcForce(i)
            i.updatePV()

        print("%f" % (time.time() - lasttime))


        # Translate mouse position
        def getMouse(x, y):
            nx, ny = pygame.mouse.get_pos()
            nx = int((nx - x) * zoom + x)
            ny = int((ny - y) * zoom + y)
            return nx, ny

        # Handle input
        if pressed[pygame.K_i]:
            zoom /= 0.99
            zoom = min(zoom, 1.5)
            zx, zy = getMouse(zx, zy)

        if pressed[pygame.K_k]:
            zoom /= 1.01
            zx, zy = getMouse(zx, zy)

        if pressed[pygame.K_SPACE]:
            showTrail = not showTrail

        if pressed[pygame.K_ESCAPE]:
            break

        if event.type == pygame.NOEVENT:
            pygame.time.wait(1)

        """

        print("finished loop %d in %f\n" % (framecount, time.time() - lasttime))
        framecount += 1
        lasttime = time.time()

        print("%f %f" % (particles[1].px, particles[1].py))
        
        """
main()

