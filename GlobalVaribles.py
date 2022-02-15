import pygame
pygame = pygame

animateTime = 20


offset_x = 115
offset_y = 10

board_x = 10
board_y = 10

block_size = 40
DISPLAYSURF = None
game = None
player = 0

playerUnitImages = {}

changeColor = (233,19,212,255)
playerColors = [(201, 59, 54,255),(0, 195, 255),(255, 136, 0,255),(107, 64, 0),(167, 242, 46)]

StateColors = {
    'attack': (255,0,0),
    'move': (0,255,255),
    'resources': (255,255,0),
    'build':(100,50,0),
    'heal':(255,255,255),
    'research':(66, 135, 245),
}

resourceColors = {
    'gold': (255,255,0),
    'metal': (100,100,100),
    'energy':(100,100,255),
}