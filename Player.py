import pygame
from score import Score
from Laser import *
from directionObject import Vector


class Player:
    def __init__(self, startPos, size, boundX):
        self._bulletSpeed = Vector(0, -10)
        self._bulletSize = Vector(3, 10)
        self._bulletColor = (0, 255, 0)
        self._bodyColor = (255, 0, 0)
        self.Body = pygame.Rect(startPos.X, startPos.Y, size.X, size.Y)
        self.Score = Score()
        self.Speed = Vector(0, 0)
        self.Bullets = []
        self.Bound = boundX

    def fire(self):
        self.Bullets.append(
            playerLaser(
                Vector(self.Body[0] + self.Body[2] / 2, self.Body[1]),
                self._bulletSize,
                self._bulletColor,
                self._bulletSpeed,
            )
        )

    def shotDetect(self, aliens, barriers):
        indices = []
        for x in self.Bullets:
            collisionAliens = x.collide(aliens)
            collisionBarriers = x.collideBarrier(barriers)
            if collisionAliens != -1:
                indices.append(collisionAliens)
                self.Bullets.remove(x)
            elif collisionBarriers != -1:
                self.Bullets.remove(x)
        return indices

    def move(self):
        self.Body = pygame.Rect.move(self.Body, self.Speed.X, self.Speed.Y)
        if self.Body[0] > self.Bound:
            self.Body[0] = self.Bound
        elif self.Body[0] < 0:
            self.Body[0] = 0
        for x in self.Bullets:
            x.move()
            if x.Bullet[1] < 0 or x.Bullet[1] > 600:
                self.Bullets.remove(x)

    def setSpeed(self, speed):
        self.Speed = speed

    def Render(self, screen):
        for x in self.Bullets:
            x.Render(screen)
        pygame.draw.rect(screen, self._bodyColor, self.Body)


class Alien(Player):
    def __init__(self, startPos, size, boundX):
        Player.__init__(self, startPos, size, boundX)
        self.pic = pygame.image.load("Alien.png").convert()
        self.pic = pygame.transform.scale(self.pic, (size.X, size.Y))
        self.Body = self.pic.get_rect()
        self.Body[0] = startPos.X
        self.Body[1] = startPos.Y
        self._bulletSpeed = Vector(0, 10)
        self._bulletSize = Vector(3, 10)
        self._bulletColor = (255, 255, 0)
        self._bodyColor = (0, 255, 255)

    def fire(self):
        self.Bullets.append(
            Laser(
                Vector(self.Body[0] + self.Body[2] / 2, self.Body[1]),
                self._bulletSize,
                self._bulletColor,
                self._bulletSpeed,
            )
        )

    def move(self, mover, bodyMove):
        if bodyMove:
            self.Body = pygame.Rect.move(self.Body, mover.X, mover.Y)
            if self.Body[0] > self.Bound:
                self.Body[0] = self.Bound
            elif self.Body[0] < 0:
                self.Body[0] = 0
        for x in self.Bullets:
            x.move()
            if x.Bullet[1] < 0 or x.Bullet[1] > 600:
                self.Bullets.remove(x)

    def Render(self, screen):
        for x in self.Bullets:
            x.Render(screen)
        screen.blit(self.pic, self.Body)
