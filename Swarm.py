from Player import Alien
from directionObject import Vector
from itertools import cycle
import random


class Swarm:
    def __init__(self, c, r, startHeight):
        self.C = c
        self.R = r
        self.Field = [
            [
                Alien(Vector(30 + 50 * i, startHeight + 50 * j), Vector(20, 20), 680)
                for i in range(c)
            ]
            for j in range(r)
        ]
        self._March = [Vector(-6, 0) for x in range(4)]
        self._March.append(Vector(0, 10))
        for x in range(9):
            self._March.append(Vector(6, 0))
        self._March.append(Vector(0, 10))
        for x in range(4):
            self._March.append(Vector(-6, 0))
        self.iterator = cycle(self._March)
        self.Timer = 80
        self.Reload = 80

    def isFreeToShoot(self, indexC, indexR):
        if indexR == self.R - 1:
            return True
        for x in range(indexR, self.R - 1):
            if self.Field[x][indexC] != 0:
                return False
        return True

    def fire(self):
        randX, randY = None, None
        while 1:
            randX, randY = random.randint(0, self.C - 1), random.randint(0, self.R - 1)
            if self.isFreeToShoot(randX, randY) and self.Field[randY][randX] != 0:
                break
        self.Field[randY][randX].fire()

    def move(self):
        if self.Timer <= 0:
            self.Timer = self.Reload
            mover = next(self.iterator)
            for i in self.Field:
                for j in i:
                    if j != 0:
                        j.move(mover, True)
        else:
            for i in self.Field:
                for j in i:
                    if j != 0:
                        j.move(Vector(0, 0), False)
            self.Timer -= 1

    def collide(self, player, barriers):
        for i in self.Field:
            for j in i:
                if j != 0:
                    indices = j.shotDetect([player], barriers)
                    for x in indices:
                        if x != -1:
                            return x
        return -1

    def destroy(self, x, y):
        self.Field[y][x] = 0

    def Render(self, screen):
        for i in self.Field:
            for j in i:
                if j != 0:
                    j.Render(screen)
