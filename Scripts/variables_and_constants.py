import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GRAVITY=0.75
FPS = 60
font = pygame.font.SysFont("arialblack", 35)
