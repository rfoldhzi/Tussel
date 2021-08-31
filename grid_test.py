import pygame, sys, random,math,pathlib,os
os.chdir(os.path.dirname(sys.argv[0]))
from pathlib import Path
from pygame.locals import *
from game import Game

folder = Path(pathlib.Path(__file__).parent.absolute())
game = Game()
player = 0

if True:#Starting board
    import game as gameMod
    game.addPlayer();
    u1 = gameMod.Unit([3,6])
    game.units[0].append(u1);
    u2 = gameMod.Unit([6,3])
    game.units[0].append(u2);
    b = gameMod.Unit([5,5], 'town')
    game.units[0].append(b);
    b.state = 'build'
    b.stateData = [[2,0],'soldier']
    game.resources[0]['gold'] = 2000
    game.resources[0]['metal'] = 2000
    game.resources[0]['energy'] = 2000

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480
pygame.display.set_caption('Hello World!')

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255)
LIGHTGREY = (200, 200, 200)
DARKGREY = (100, 100, 100)

BGCOLOR = LIGHTGREY

StateColors = {
    'attack': (255,0,0),
    'move': (0,255,255),
    'resources': (255,255,0),
    'build':(100,50,0),
    }


#Healthfont = pygame.font.SysFont("arial", 10)


class Button:
    def __init__(self, text, x, y, color,textColor,size = 28,BoxSize = [90,30]):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.textColor = textColor
        self.width = BoxSize[0]
        self.height = BoxSize[1]
        self.size = size
        self.active = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("arial", self.size)
        text = font.render(self.text, 1, self.textColor)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))
        self.active = True

    def deDraw(self, win):
        pygame.draw.rect(win, BGCOLOR, (self.x-1, self.y-1, self.width+2, self.height+2))
        self.active = False

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height and self.active:
            return True
        else:
            return False

def checkRange(a,b):
    if type(b) == list:
        return max(abs(a.position[0]-b[0]), abs(a.position[1]-b[1]))
    return max(abs(a.position[0]-b.position[0]), abs(a.position[1]-b.position[1]))

def randomGreen():
    g = random.randint(150,200)
    return (round(g*random.random()*.5), g, round(g*random.random()*.5))

def gridMouse(x,y,block,offx, offy):
    x = x - offx
    y = y - offy
    return math.floor(x/(block+1)), int(y/(block+1))

def highlightSquare(x,y):
    rect = pygame.Rect(x*(block_size+1)+offset_x-1, y*(block_size+1)+offset_y-1, block_size+2, block_size+2)
    pygame.draw.rect(DISPLAYSURF, (255,255,255), rect)

def getMoveCircles(unit):#Could be more effiecint
    if not 'move' in unit.possibleStates:
        return []
    sp = unit.speed
    spaces = []
    for x in range(unit.position[0]-sp, unit.position[0]+1+sp):
        for y in range(unit.position[1]-sp, unit.position[1]+1+sp):
            if x >= 0 and y >= 0 and y<board_y and x<board_x:#If within board:
                if game.getAnyUnitFromPos(x,y) == None:
                    spaces.append([x,y])
    return spaces
def getRangeCircles(unit):#Could be more effiecint
    sp = unit.range
    spaces = []
    for x in range(unit.position[0]-sp, unit.position[0]+1+sp):
        for y in range(unit.position[1]-sp, unit.position[1]+1+sp):
            if x >= 0 and y >= 0 and y<board_y and x<board_x:#If within board:
                if game.getAnyUnitFromPos(x,y) == None:
                    spaces.append([x,y])
    return spaces

#Get rid of this function later
image = pygame.image.load("assets/%s.png" % "soldier2")
def showUnit(x,y, im = image):
    DISPLAYSURF.blit(im,(x*(block_size+1)+offset_x-1, y*(block_size+1)+offset_y-1))
    
    t = str(random.randint(0,20))#Health Value
    Healthfont = pygame.font.SysFont("arial", 15)
    text = Healthfont.render(t, 1, RED)
    DISPLAYSURF.blit(text, (x*(block_size+1)+offset_x+38-(7*len(t)), y*(block_size+1)+offset_y+23))
    
    rect = pygame.Rect(x*(block_size+1)+offset_x+block_size - 9, y*(block_size+1)+offset_y+4, 5, 5)
    pygame.draw.rect(DISPLAYSURF, (0,255,255), rect)

def showUnitNEW(unit):
    x = unit.position[0]
    y = unit.position[1]
    DISPLAYSURF.blit(pygame.image.load("assets/%s.png" % unit.name),(x*(block_size+1)+offset_x-1, y*(block_size+1)+offset_y-1))
    
    t = str(unit.health)
    Healthfont = pygame.font.SysFont("arial", 15)
    text = Healthfont.render(t, 1, RED)
    DISPLAYSURF.blit(text, (x*(block_size+1)+offset_x+38-(7*len(t)), y*(block_size+1)+offset_y+23))

    #State square
    if unit.state != None:
        rect = pygame.Rect(x*(block_size+1)+offset_x+block_size - 9, y*(block_size+1)+offset_y+4, 5, 5)
        pygame.draw.rect(DISPLAYSURF, StateColors[unit.state], rect)

def drawLine(color,pos1,pos2):
    pygame.draw.line(DISPLAYSURF, color, ((block_size+1)*pos1[0]+offset_x+block_size/2,(block_size+1)*pos1[1]+offset_y+block_size/2),((block_size+1)*pos2[0]+offset_x+block_size/2,(block_size+1)*pos2[1]+offset_y+block_size/2),10)

def drawGrid():
    i = 0
    for y in range(board_y):
        for x in range(board_x):
            rect = pygame.Rect(x*(block_size+1)+offset_x, y*(block_size+1)+offset_y, block_size, block_size)
            pygame.draw.rect(DISPLAYSURF, BoardColors[i], rect)
            i+=1

block_size = 40
offset_x = 115
offset_y = 10

board_x = 10
board_y = 10

highlightSquares = []
BoardColors = []
moveCircles = []
buildHexes = []

blueCircle = pygame.image.load("assets/MoveCircle.png")
OrangeHex = pygame.image.load("assets/BuildHex.png")
print(type(blueCircle))

def drawBoard():
    rect = pygame.Rect(offset_x-1,offset_y-1, 410+offset_x,410+offset_y)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, rect)
    for v in highlightSquares:
        highlightSquare(v[0],v[1])
    drawGrid()
    for u in game.units[player]:
        if u.stateData:#In case target isn't selected yet
            if u.state == 'move':
                if checkRange(u,u.stateData) > u.speed:
                    drawLine((45, 150, 138),u.position,u.stateData)
                else:
                    drawLine((0,255,255),u.position,u.stateData)
            elif u.state == 'attack':
                if checkRange(u,u.stateData.position) > u.range:
                    drawLine((148, 55, 49),u.position,u.stateData.position)
                else:
                    drawLine((255,0,0),u.position,u.stateData.position)
            elif u.state == 'build':
                if len(u.stateData) == 2:
                    if checkRange(u,u.stateData[0]) > u.range:
                        drawLine((110, 106, 46),u.position,u.stateData[0])
                    else:
                        drawLine((255,170,0),u.position,u.stateData[0])
    for i in game.units:
        for u in game.units[i]:
            showUnitNEW(u)
    for pos in moveCircles:
        DISPLAYSURF.blit(blueCircle,(pos[0]*(block_size+1)+offset_x-1, pos[1]*(block_size+1)+offset_y-1))
    for pos in buildHexes:
        DISPLAYSURF.blit(OrangeHex,(pos[0]*(block_size+1)+offset_x-1, pos[1]*(block_size+1)+offset_y-1))

def resources():
    rect = pygame.Rect(0,430, 40,480)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, rect)
    Healthfont = pygame.font.SysFont("arial", 15)
    text = Healthfont.render(str(game.resources[player]['gold']), 1, (255,255,0))
    DISPLAYSURF.blit(text, (0,430))
    text = Healthfont.render(str(game.resources[player]['metal']), 1, (255,255,255))
    DISPLAYSURF.blit(text, (0,445))
    text = Healthfont.render(str(game.resources[player]['energy']), 1, (0,255,255))
    DISPLAYSURF.blit(text, (0,460))

btns = {
    'attack':Button("Attack", 10, 10, (255,0,0), WHITE),
    'move':Button("Move", 10, 60, (0,255,255),BLACK),
    'resources':Button("Resources", 10, 110, (255,255,0),BLACK,19),
    'build':Button("Build", 10, 160, (100,50,0),WHITE),
}
resourceBtns = {
    'gold':Button("Gold", 25, 230, (255,255,50),BLACK,22,(60,20)),
    'metal':Button("Metal", 25, 260, (50,50,50),WHITE,20,(60,20)),
    'energy':Button("Energy", 25, 290, (100,100,255),BLACK,18,(60,20)),
}

selected = None
stateDataMode = None
extraButtons = {}

def cleanUpAfterSelect():
    global highlightSquares, moveCircles, selected,stateDataMode, extraButtons, buildHexes
    selected = None
    print(selected)
    stateDataMode = None
    highlightSquares = []
    moveCircles = []
    buildHexes = []
    for btn in btns:
        btns[btn].deDraw(DISPLAYSURF)
    for v in extraButtons:
        extraButtons[v].deDraw(DISPLAYSURF)

def main():
    global FPSCLOCK, DISPLAYSURF, highlightSquares, moveCircles, selected, stateDataMode, extraButtons, buildHexes
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Blank')

    DISPLAYSURF.fill(BGCOLOR)

    mouseDown = False

    
    image = pygame.image.load(r"C:\Users\reega\Downloads\Python\Game\assets\soldier2.png")
    image2 = pygame.image.load(r"C:\Users\reega\Downloads\Python\Game\assets\town.png")

    for i in range(board_x*board_y):
        BoardColors.append(randomGreen())
        
    drawBoard()
    resources()
    pygame.draw.line(DISPLAYSURF, (0,255,255), (20+offset_x,20+offset_y),(61+offset_x,20+offset_y),10)

    for btn in btns:
        btns[btn].draw(DISPLAYSURF)
    

    

    
            
    while True: # main game loop
        #mouseClicked = False

        #DISPLAYSURF.fill(BGCOLOR)#Draw window
        
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseDown = False  
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                x,y = gridMouse(mousex, mousey, block_size,offset_x,offset_y)
                print(x,y)
                print('datamode', stateDataMode)
                print('selected', selected)
                if stateDataMode == 'move':
                    selected.state = None
                    if x >= 0 and y >= 0 and y<board_y and x<board_x:
                        selected.stateData = [x,y]
                        selected.state = 'move'
                    cleanUpAfterSelect()
                    #Here is to sumbit to server
                    drawBoard()
                if stateDataMode == 'attack':
                    selected.state = None
                    if game.getAnyUnitFromPos(x,y):
                        selected.stateData = game.getAnyUnitFromPos(x,y)
                        selected.state = 'attack'
                    cleanUpAfterSelect()
                    #Here is to sumbit to server
                    drawBoard()
                elif stateDataMode == 'resources':
                    selected.state = None
                    for btn in resourceBtns:
                        if resourceBtns[btn].click(pygame.mouse.get_pos()):#If one of the resources is clicked
                            selected.stateData = btn
                            selected.state = 'resources'
                        resourceBtns[btn].deDraw(DISPLAYSURF)
                    cleanUpAfterSelect()
                    #Here is to sumbit to server
                    drawBoard()
                elif stateDataMode == 'build':
                    offclick = True
                    for btn in extraButtons:
                        if extraButtons[btn].click(pygame.mouse.get_pos()):#If one of the unit options is clicked
                            selected.stateData = [btn]
                            stateDataMode = 'build2'
                            for v in extraButtons:
                                extraButtons[v].deDraw(DISPLAYSURF)
                            extraButtons = {}
                            buildHexes = getRangeCircles(selected)
                            drawBoard()
                            offclick = False
                            break
                    if offclick:
                        selected.state = None
                        cleanUpAfterSelect()
                        for v in extraButtons:
                            extraButtons[v].deDraw(DISPLAYSURF)
                        extraButtons = {}
                        drawBoard()
                elif stateDataMode == 'build2':
                    selected.state = None
                    if x >= 0 and y >= 0 and y<board_y and x<board_x:
                        selected.stateData.insert(0,[x,y])
                        selected.state = 'build'
                    cleanUpAfterSelect()
                    #Here is to sumbit to server
                    drawBoard()
                
                elif selected:
                    for btn in btns:
                        if btns[btn].click(pygame.mouse.get_pos()):#If button clicked, set state of unit
                            selected.state = btn
                            selected.stateData = None
                            stateDataMode = btn
                            for btn2 in btns:
                                if btn2 != btn:
                                    btns[btn2].deDraw(DISPLAYSURF)
                            if stateDataMode == 'resources':
                                for v in resourceBtns:
                                    resourceBtns[v].draw(DISPLAYSURF)
                            if stateDataMode == 'build':
                                i = 0
                                for v in selected.possibleBuilds:
                                    b = Button("", 115+41*i, 430, (230,230,230),BLACK,18,(40,40))
                                    b.draw(DISPLAYSURF)
                                    DISPLAYSURF.blit(pygame.image.load("assets/%s.png" % v),(115+41*i, 430))
                                    extraButtons[v] = b
                                    i+=1
                            drawBoard()
                    if 'build' in selected.possibleStates:#If they are able to build
                        for btn in extraButtons:
                            if extraButtons[btn].click(pygame.mouse.get_pos()):#If one of the unit options is clicked
                                selected.stateData = [btn]
                                stateDataMode = 'build2'
                                for v in extraButtons:
                                    extraButtons[v].deDraw(DISPLAYSURF)
                                extraButtons = {}
                                moveCircles = []
                                buildHexes = getRangeCircles(selected)
                                offclick = False
                                drawBoard()
                                break
                    if x >= 0 and y >= 0 and y<board_y and x<board_x:
                        if [x,y] in moveCircles: #A move was clicked
                            selected.stateData = [x,y]
                            selected.state = 'move'
                            cleanUpAfterSelect()
                            print(selected)
                            #Here is to sumbit to server
                        else: 
                            selected = game.getUnitFromPos(player,x,y)
                            if selected:#Unit is clicked
                                highlightSquares = [[x,y]]
                                moveCircles = getMoveCircles(selected)
                                for btn in btns:
                                    if btn in selected.possibleStates:
                                        btns[btn].draw(DISPLAYSURF)
                                    else:
                                        btns[btn].deDraw(DISPLAYSURF)
                                if 'build' in selected.possibleStates: #Show things on bottom
                                    i = 0
                                    for v in selected.possibleBuilds:
                                        b = Button("", 115+41*i, 430, (230,230,230),BLACK,18,(40,40))
                                        b.draw(DISPLAYSURF)
                                        DISPLAYSURF.blit(pygame.image.load("assets/%s.png" % v),(115+41*i, 430))
                                        extraButtons[v] = b
                                        i+=1
                                else:
                                    for v in extraButtons:
                                        extraButtons[v].deDraw(DISPLAYSURF) 
                            else:
                                cleanUpAfterSelect()
                        drawBoard()
                elif event.button == 1:
                    if x >= 0 and y >= 0 and y<board_y and x<board_x:
                        selected = game.getUnitFromPos(player,x,y)
                        if selected:#When unit clicked
                            highlightSquares = [[x,y]]
                            moveCircles = getMoveCircles(selected)
                            for btn in btns:
                                if btn in selected.possibleStates:
                                    btns[btn].draw(DISPLAYSURF)
                                else:
                                    btns[btn].deDraw(DISPLAYSURF)
                            if 'build' in selected.possibleStates: #Show things on bottom
                                i = 0
                                for v in selected.possibleBuilds:
                                    b = Button("", 115+41*i, 430, (230,230,230),BLACK,18,(40,40))
                                    b.draw(DISPLAYSURF)
                                    DISPLAYSURF.blit(pygame.image.load("assets/%s.png" % v),(115+41*i, 430))
                                    extraButtons[v] = b
                                    i+=1
                        else:
                            for btn in btns:
                                btns[btn].deDraw(DISPLAYSURF)
                        drawBoard()
                elif event.button == 3:
                    if x >= 0 and y >= 0 and y<board_y and x<board_x:
                        showUnit(x,y)
                elif event.button == 2:
                    game.round()
                    resources()
                    drawBoard()
                mouseDown = True
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
