#!/usr/bin/env python3
# Alec Battisti
# CPSC 386-01
# 2021-12-13
# alec.battisti@csu.fullerton.edu
# @Alec-Battisti
#
# This is a space invaders clone
#

from Scenes import *
import pygame

def Run(width,height,fps,start_scene):
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    
    current_scene = start_scene
    
    while current_scene != None:
        keys_down = pygame.key.get_pressed()
        
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
            if quit_attempt:
                current_scene.Terminate()
            else:
                filtered_events.append(event)
                
        current_scene.ProcessInput(filtered_events, keys_down)
        current_scene.Update()
        current_scene.Render(screen)
        
        current_scene = current_scene.next
        
        pygame.display.flip()
        clock.tick(fps)

def main():
    Run(700,600,60,Title())

if __name__ == '__main__':
    main()
