import pygame
pygame = pygame

animateTime = 20
JustResize = 0
animateTime = 20

offset_x = 115
offset_y = 10

board_x_start = 1
board_y_start = 1
board_x_end = 15
board_y_end = 15


board_x = 10
board_y = 10

block_size = 40
DISPLAYSURF = None
game = None
newGame = None
player = 0
cloudMode = "halo"

highlightSquares = []
BoardColors = []
CloudColors = []
moveCircles = []
possibleAttacks = []
possibleHeals = []
buildHexes = []
Grid = []
cloudGrid = []
explorationGrid = []
animateGrid = []

playerUnitImages = {}

animation = False

RedX = pygame.image.load("assets/AttackX.png")

changeColor = (233,19,212,255)
changeColor2 = (117,10,107,255)
playerColors = [(201, 59, 54,255),(0, 195, 255),(255, 136, 0,255),(41, 61, 148),
(128, 242, 46),(169, 88, 245),(255, 255, 64),(18, 252, 104)]
BGCOLOR = (200,200,200)

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