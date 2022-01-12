import pygame


class Laser:
    def __init__(self, startPos, size, color, speed):
        self.Bullet = pygame.Rect(startPos.X, startPos.Y, size.X, size.Y)
        self.Color = color
        self.Speed = speed

    def move(self):
        self.Bullet = pygame.Rect.move(self.Bullet, self.Speed.X, self.Speed.Y)

    def collide(self, others):
        for key, rect in enumerate(others):
            if rect != 0:
                if pygame.Rect.colliderect(self.Bullet, rect.Body):
                    return key
        return -1

    def collideBarrier(self, barriers):
        for key, rect in enumerate(barriers):
            if rect != 0:
                if pygame.Rect.colliderect(self.Bullet, rect):
                    return key
        return -1

    def Render(self, screen):
        pygame.draw.rect(screen, self.Color, self.Bullet)


class playerLaser(Laser):
    def __init__(self, startPos, size, color, speed):
        Laser.__init__(self, startPos, size, color, speed)

    def collide(self, others):
        for keyY, i in enumerate(others):
            for keyX, rect in enumerate(i):
                if rect != 0:
                    if pygame.Rect.colliderect(self.Bullet, rect.Body):
                        return (keyX, keyY)

        return -1
