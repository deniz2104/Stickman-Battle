import pygame
from player import Urzicarius
from Wall import Wall
from enemy import Enemy
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Urzicarius(100, SCREEN_HEIGHT // 1.5, 5)
enemy = Enemy(680, SCREEN_HEIGHT // 1.5, 1, 'Textures/big_boss.png')
wall_left=Wall(0,0,20, SCREEN_WIDTH)
wall_right=Wall(780,0,20, SCREEN_WIDTH)
GRAVITY=0.75