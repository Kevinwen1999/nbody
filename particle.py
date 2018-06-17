import math
import random
from constants import *


# Particle class
class Particle:
    def __init__(self, mass=0):
        # Position
        self.px = float(random.randint(Width / 3, Width - Width / 3))
        self.py = float(random.randint(Height / 3, Height - Height / 3))
        # Velocity
        self.vx = 0#float(random.randint(-10, 10))
        self.vy = 0#float(random.randint(-10, 10))
        # Acceleration
        self.ax = 0
        self.ay = 0
        # Radius
        self.r = random.randint(10, 20)
        # Boolean to keep track whether the particle still exist
        self.exist = True
        # Randomizing particle color to something visible
        self.color = (random.randint(100, 255) / 255, random.randint(100, 255) / 255, random.randint(100, 255) / 255)
        # Initialize mass
        if mass == 0:
            self.setM()
        else:
            self.mass = mass
            self.setR()

    # A method to manually set position and mass, used for easier force calculations
    def setP(self, x, y, m):
        self.px, self.py, self.mass = x, y, m

    # Calculate new acceleration due to another particle a
    def addA(self, a):
        dx = a.px - self.px
        dy = a.py - self.py
        dist2 = dx * dx + dy * dy
        Gforce = GC * self.mass * a.mass / dist2 if dist2 > 1e-9 else 0.0
        dist = math.sqrt(dist2)
        # Using Gravitational Force Formula for vector quantities
        self.ax += Gforce / dist * dx
        self.ay += Gforce / dist * dy

    # Calculate final position of the particle after checking all other ones
    def updatePV(self):
        self.vx += self.ax * DT
        self.vy += self.ay * DT
        self.px += self.vx * DT
        self.py += self.vy * DT
        # If the particle hits boundary, bounce back and lose a "bit" of energy
        if self.px < 100 or math.fabs(Width - self.px) < 100:
            self.vx = -self.vx * 0.1
        if self.py < 100 or math.fabs(Height - self.py) < 100:
            self.vy = -self.vy * 0.1

    # Set Mass from radius and density
    def setM(self):
        self.mass = Density * 4.0 / 3.0 * self.r ** 3 * math.pi

    # Used to calculate new radius after merging masses
    def setR(self):
        self.r = (self.mass * 3.0 / (Density * 4.0 * math.pi)) ** (0.33333333)

    # Test if two particles collided
    def collide(self, a):
        dx = a.px - self.px
        dy = a.py - self.py
        dist2 = dx * dx + dy * dy
        return dist2 < (self.r + a.r) ** 2
