import pygame
import os
from Player import Player
from directionObject import Vector
from Swarm import Swarm
from leaderBoard import LeaderBoard
import pickle
import random


pygame.font.init()
titleFont = pygame.font.SysFont(None, 190)
title2Font = pygame.font.SysFont(None, 100)
playerFont = pygame.font.SysFont(None, 25)
textFont = pygame.font.SysFont(None, 50)
pygame.mixer.pre_init(44100, 16, 2, 4096)


filename = "scores"
leaderboard = None
try:
    infile = open(filename, "rb")
    leaderboard = pickle.load(infile)
    infile.close()
except:
    leaderboard = LeaderBoard()


class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):
        print("not overridden")

    def Update(self):
        print("not overridden")

    def Render(self, screen):
        print("not overridden")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


class Title(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(Game())

    def Update(self):
        pass

    def Render(self, screen):
        title = titleFont.render("SPACE", True, (255, 255, 255))
        screen.blit(title, (100, 75))
        title2 = titleFont.render("INVADERS", True, (255, 255, 255))
        screen.blit(title2, (15, 175))
        controls = textFont.render(
            "A and D to move, spacebar to shoot", True, (255, 255, 255)
        )
        screen.blit(controls, (30, 300))
        message = textFont.render("Press Enter to Start!", True, (255, 255, 255))
        screen.blit(message, (175, 500))


class gameOver(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(Game())

    def Update(self):
        pass

    def Render(self, screen):
        screen.fill((0, 0, 0))
        title = title2Font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(title, (100, 75))
        for i, v in enumerate(leaderboard.Scores):
            player = playerFont.render(
                str(i + 1)
                + ": "
                + str(v.Points)
                + " Pts. | "
                + str(v.Date)
                + " | "
                + str(v.Time)
                + "ms",
                True,
                (255, 255, 255),
            )
            screen.blit(player, (185, 150 + 30 * (i + 1)))
        message = textFont.render("Press enter to play again", True, (0, 255, 0))
        screen.blit(message, (110, 500))
        pygame.display.update()


class gameWon(SceneBase):
    def __init__(self, player):
        SceneBase.__init__(self)
        self.Player = player

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(Game(self.Player))

    def Update(self):
        pass

    def Render(self, screen):
        screen.fill((0, 0, 0))
        title = title2Font.render("YOU WIN!!", True, (255, 255, 255))
        screen.blit(title, (100, 75))
        message = textFont.render("Press enter to continue", True, (0, 255, 0))
        screen.blit(message, (110, 500))
        pygame.display.update()


class Game(SceneBase):
    def __init__(self, player=Player(Vector(0, 580), Vector(50, 20), 650)):
        SceneBase.__init__(self)
        self.Player = player
        self.Swarm = Swarm(13, 5, 50)
        self.Barriers = [
            pygame.Rect(60, 400, 105, 105),
            pygame.Rect(235, 400, 105, 105),
            pygame.Rect(410, 400, 105, 105),
            pygame.Rect(585, 400, 105, 105),
        ]
        self.fireSignal = 0
        self.fireCoolDown = 0
        self.Lives = 3
        self.startTime = pygame.time.get_ticks()
        self.playerLaser = pygame.mixer.Sound("playerLaser.wav")
        self.alienLaser = pygame.mixer.Sound("alienLaser.wav")
        self.explodeSound = pygame.mixer.Sound("explode.wav")

    def ProcessInput(self, events, pressed_keys):
        move = Vector(0, 0)
        move = (
            move
            + Vector(3 * pressed_keys[pygame.K_d], 0)
            + Vector(-3 * pressed_keys[pygame.K_a], 0)
        )
        self.fireSignal = pressed_keys[pygame.K_SPACE]
        self.Player.setSpeed(move)

    def Update(self):
        if self.fireSignal and self.fireCoolDown == 0:
            self.Player.fire()
            self.playerLaser.play()
            self.fireSignal = 0
            self.fireCoolDown = 30
        else:
            if self.fireCoolDown > 0:
                self.fireCoolDown -= 1

        if random.randint(0, 25) == 3:
            self.Swarm.fire()
            self.alienLaser.play()
        self.Player.move()
        self.Swarm.move()
        playerCollision = self.Swarm.collide(self.Player, self.Barriers)
        if playerCollision != -1:
            self.explodeSound.play()
            self.Lives -= 1
            if self.Lives <= 0:
                self.Player.Score.Time = pygame.time.get_ticks() - self.startTime
                leaderboard.register(self.Player.Score)
                outfile = open(filename, "wb")
                pickle.dump(leaderboard, outfile)
                outfile.close()
                self.SwitchToScene(gameOver())
        alienCollision = self.Player.shotDetect(self.Swarm.Field, self.Barriers)
        for x in alienCollision:
            self.Swarm.destroy(x[0], x[1])
            self.explodeSound.play()
            self.Player.Score.Points += 10
            self.Swarm.Reload -= 1

    def Render(self, screen):
        screen.fill((0, 0, 0))
        self.Player.Render(screen)
        self.Swarm.Render(screen)
        score = textFont.render(
            "Score: " + str(self.Player.Score.Points), True, (255, 255, 255)
        )
        screen.blit(score, (5, 5))
        lives = textFont.render("Lives: " + str(self.Lives), True, (255, 255, 255))
        screen.blit(lives, (400, 5))
        for x in self.Barriers:
            pygame.draw.rect(screen, (255, 255, 255), x)
