from contextlib import nullcontext
import  sys, random,math,pathlib,os,pickle,copy,subprocess,signal
os.chdir(os.path.dirname(sys.argv[0]))
from pathlib import Path
from pygame.locals import *
from operator import add
from game import Game, Unit, GameMaker
from network import Network
from UnitDB import UnitDB
from UnitDB import TechDB
import methods
import network


import GlobalVaribles as GV

GV.pygame.mixer.pre_init(44100, -16, 1, 512)

GV.pygame.init()

trooper_affirmative = GV.pygame.mixer.Sound("audio/trooper_affirmative2.wav")

affirmative = {
    "trooper": GV.pygame.mixer.Sound("audio/trooper_affirmative2.wav"),
    "bot": GV.pygame.mixer.Sound("audio/bot_affirmative.wav"),
    "building": GV.pygame.mixer.Sound("audio/building_affirmative.wav"),
    "vehicle": GV.pygame.mixer.Sound("audio/rev.wav"),
    "aircraft": GV.pygame.mixer.Sound("audio/plane_radio.wav"),
} 


attack_audio = {
    #"trooper": GV.pygame.mixer.Sound("audio/trooper_affirmative2.wav"),
    ##"bot": GV.pygame.mixer.Sound("audio/robot_intruder.wav"),
    ##"building": GV.pygame.mixer.Sound("audio/building_attack.wav"),
    #"vehicle": GV.pygame.mixer.Sound("audio/rev.wav"),
    ##"aircraft": GV.pygame.mixer.Sound("audio/target_acquired.wav"),
} 

move_audio = {
    #"trooper": GV.pygame.mixer.Sound("audio/trooper_affirmative2.wav"),
    ##"bot": GV.pygame.mixer.Sound("audio/robot_move.wav"),
    #"vehicle": GV.pygame.mixer.Sound("audio/rev.wav"),
    #"aircraft": GV.pygame.mixer.Sound("audio/target_acquired.wav"),
} 

resource_audio = {
    "gold": GV.pygame.mixer.Sound("audio/coins.wav"),
    "metal": GV.pygame.mixer.Sound("audio/mining.wav"),
    "energy": GV.pygame.mixer.Sound("audio/zap.wav"),
}

construction = GV.pygame.mixer.Sound("audio/construction.wav")     
end_of_round_beeps = GV.pygame.mixer.Sound("audio/end_of_round.wav") 

research_selected_audio = GV.pygame.mixer.Sound("audio/lab_selected.wav")   

imageMani = True
try:
    from PIL import Image
except:
    imageMani = False
    print("No Pillow module found. Please use folling command to install for quality images:")
    print("python3 -m pip install --upgrade Pillow")
folder = Path(pathlib.Path(__file__).parent.absolute())
GV.game = Game(0, False)
GV.player = 0
cloudMode = "halo"#sight, poly, halo, clear

serverprocess = None



FPS = 30 # frames per second, the general speed of the program
GV.pygame.display.set_caption('Hello World!')

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255)
LIGHTGREY = (200, 200, 200)
DARKGREY = (100, 100, 100)
errorColor = (255, 100, 100)
goodColor = (100, 100, 255)
otherColor = (100, 100, 100)

BGCOLOR = LIGHTGREY

GV.StateColors = {
    'attack': (255,0,0),
    'move': (0,255,255),
    'resources': (255,255,0),
    'build':(100,50,0),
    'heal':(255,255,255),
    'research':(66, 135, 245),
    }
GV.resourceColors = {
    'gold': (255,255,0),
    'metal': (100,100,100),
    'energy':(100,100,255),
}


#Healthfont = GV.pygame.font.SysFont("arial", 10)


class Button:
    def __init__(self, text, x, y, color,textColor,size = 28,BoxSize = [90,30],title = False):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.textColor = textColor
        self.width = BoxSize[0]
        self.height = BoxSize[1]
        self.size = size
        self.active = False
        if title:
            self.name = title

    def draw(self, win):
        GV.pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = GV.pygame.font.SysFont("arial", self.size)
        text = font.render(self.text, 1, self.textColor)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))
        self.active = True

    def deDraw(self, win):
        GV.pygame.draw.rect(win, BGCOLOR, (self.x-1, self.y-1, self.width+2, self.height+2))
        self.active = False

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height and self.active:
            return True
        else:
            return False

FONT = GV.pygame.font.SysFont("arial", 14)
COLOR_INACTIVE = GV.pygame.Color('lightskyblue3')
COLOR_ACTIVE = GV.pygame.Color('dodgerblue2')

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = GV.pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == GV.pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == GV.pygame.KEYDOWN:
            if self.active:
                if event.key == GV.pygame.K_RETURN:
                    print(self.text)
                    self.active = False
                    #self.text = ''
                elif event.key == GV.pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, BLACK)

    def update(self):
        # Resize the box if the text is too long.
        width = max(120, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+2))
        # Blit the rect.
        GV.pygame.draw.rect(screen, self.color, self.rect, 2)

def convertToStr(u, state, stateData):#n.send([selected,'move',[x,y]])):
    s = '%s:%s:' % (u.UnitID, state)
    if state == 'move':
        s+= '%s:%s' % tuple(stateData)
    elif state == 'attack':
        s+= stateData.UnitID
    elif state == 'heal':
        s+= stateData.UnitID
    elif state == 'resources':
        s+= stateData
    elif state == 'research':
        s+= stateData
    elif state == 'build':
        s+= '%s:%s:' % tuple(stateData[0])
        s+= stateData[1]
    return s

def PlaySoundByUnit(selected, sound_type):
    sound_dict = None

    if sound_type == "affirmative":
        sound_dict = affirmative
    elif sound_type == "attack":
        sound_dict = attack_audio
    elif sound_type == "move":
        sound_dict = move_audio

    if selected.type in sound_dict:
        sound_dict[selected.type].play()

def checkRange(a,b):
    if type(b) == list:
        return max(abs(a.position[0]-b[0]), abs(a.position[1]-b[1]))
    return max(abs(a.position[0]-b.position[0]), abs(a.position[1]-b.position[1]))

def checkRangePos(a,b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))

def checkRangePosX(a,b):
    return abs(a[0]-b[0])
def checkRangePosY(a,b):
    return abs(a[1]-b[1])

def TotalRange(points):
    total = 0
    X = 0
    Y = 0
    for i in range(len(points)-1):
        for j in range(i+1,len(points)):
            total += checkRangePos(points[i], points[j])
            X += checkRangePosX(points[i], points[j])
            Y += checkRangePosY(points[i], points[j])
    return total,X,Y
def MinRange(points):
    Min = checkRangePos(points[0], points[1])
    for i in range(len(points)-1):
        for j in range(i+1,len(points)):
            if checkRangePos(points[i], points[j]) < Min:
                Min = checkRangePos(points[i], points[j])
    return Min

def randomGreen():
    g = random.randint(150,200)
    return (round(g*random.random()*.5), g, round(g*random.random()*.5))
def randomYellow():
    y = random.randint(175,230)
    return (y, round(y*(random.random()*.15+.65)), round(y*random.random()*.15))

def randomBlue():
    b = random.randint(180,210)
    return (round(b*random.random()*.2), round(b*(random.random()*.25+.5)),b)

def randomGrey():
    g = random.randint(50,100)
    return (g, g, g)

def randomWhite():
    g = random.randint(210,255)
    return (g, g, g)

def randomDark():
    g = random.randint(0,50)
    return (g, g, g)

def gridMouse(x,y,block,offx, offy):
    x = x - offx
    y = y - offy
    return math.floor(x/(block+1)), int(y/(block+1))

def highlightSquare(x,y):
    rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x, y*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
    GV.pygame.draw.rect(GV.DISPLAYSURF, (255,255,255), rect)

def getMoveCircles(unit):#Could be more effiecint
    if not 'move' in unit.possibleStates:
        return []
    sp = unit.speed
    spaces = []
    if unit.type != 'aircraft':
        spaces.append(unit.position)
        #pos = unit.position
        for i in range(sp):
            newSpaces = []
            for pos in spaces:
                for x in range(pos[0]-1, pos[0]+2):
                    for y in range(pos[1]-1, pos[1]+2):
                        if ([x,y] not in spaces) and x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:#If within board:
                            if GV.game.getAnyUnitFromPos(x,y) == None:
                                water = Grid[y][x]
                                if (water == (unit.type == 'boat')) or unit.type == "aircraft":
                                    newSpaces.append([x,y])
            spaces += newSpaces
        spaces.pop(0)
    else:
        for x in range(unit.position[0]-sp, unit.position[0]+1+sp):
            for y in range(unit.position[1]-sp, unit.position[1]+1+sp):
                if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:#If within board:
                    if GV.game.getAnyUnitFromPos(x,y) == None:
                        water = Grid[y][x]
                        if (water == (unit.type == 'boat')) or unit.type == "aircraft":
                            spaces.append([x,y])
    
    
    return spaces

def getRangeCircles(unit, anyBlock = False, built = False):#Could be more effiecint
    sp = unit.range
    spaces = []
    for x in range(unit.position[0]-sp, unit.position[0]+1+sp):
        for y in range(unit.position[1]-sp, unit.position[1]+1+sp):
            if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:#If within board:
                if anyBlock or GV.game.getAnyUnitFromPos(x,y) == None:
                    water = Grid[y][x]
                    if built:
                        t = UnitDB[built].get('type') or 0
                        if (water == (t == 'boat')) or t == "aircraft":
                            spaces.append([x,y])
                    else:
                        if anyBlock or (not water):
                            spaces.append([x,y])
    return spaces
"""
def isNextToWater(pos):
    for x in range(pos[0]-1, pos[0]+2):
        for y in range(pos[1]-1, pos[1]+2):
            if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:
                if Grid[y][x]:
                    return True
    return False
"""
def isNextToWater(pos):
    xs = [1,0,-1,0]
    ys = [0,1,0,-1]
    for i in range(4):
        x = pos[0]+xs[i]
        y = pos[1]+ys[i]
        if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:
                if Grid[y][x]:
                    return True
    return False

"""
x = np.array(g)
b = np.packbits(np.uint8(x))
intToList(b)
"""

def int_to_bool_list(num):
    return [bool(num & (1<<n)) for n in range(8)][::-1]

def intToList(x):
    l = []
    for v in x:
        l+=int_to_bool_list(v)
    l2 = []
    for i in range(len(l)//10):
        l2.append(l[(i*10):((i+1)*10)])
    return l2

def newGrid(x,y):
    g = []
    for i in range(x):
        l = []
        for j in range(y):
            l.append(False)
        g.append(l)
    return g

def pickRandom(g):
    return [random.randint(0,len(g[0])-1),random.randint(0,len(g)-1)]

def getSurround(g,pos):#Could be more effiecint
    spaces = []
    for x in range(pos[0]-1, pos[0]+2):
        for y in range(pos[1]-1, pos[1]+2):
            if x >= 0 and y >= 0 and y<len(g) and x<len(g[0]):#If within board:
                if not g[x][y]:
                    spaces.append([x,y])
    return spaces

def makeAreas(g):
    maxTiles = int(.3*len(g)*len(g[0]))
    spots = random.randint(1,len(g)*len(g[0])//20)
    for i in range(spots):
        pos = pickRandom(g)
        g[pos[0]][pos[1]] = True
    for i in range(maxTiles-spots):
        possible = []
        for x in range(len(g[0])):
            for y in range(len(g)):
                if g[x][y]:
                    possible += getSurround(g,[x,y])
        choice = random.choice(possible)
        g[choice[0]][choice[1]] = True
    return g

def GetIsland(g, pos):
    island = [pos]
    while True:
        done = True
        for p in island:
            for p2 in getSurround(g,p):
                if not p2 in island:
                    done = False
                    island.append(p2)
        if done:
            break
    return island

def findBiggestIsland(g, attempts = 10):
    bestIsland = []
    for i in range(attempts):
        pos = pickRandom(g)
        if not g[pos[0]][pos[1]]:
            island = GetIsland(g, pos)
            if len(island) > len(bestIsland):
                bestIsland = island
    return bestIsland

def smoothIsland(g, island):
    for pos in island:
        s = getSurround(g,pos)
        if len(s) < 3:
            island.remove(pos)
    return island

def findStartSpots(g, n = 2):
    island = findBiggestIsland(g)
    island = smoothIsland(g, island)
    points = []
    for i in range(n):
        pos = random.choice(island)
        points.append(pos)
    print('starting:',points)
    total = n
    good = []
    Attempts = 0
    for i in range(n):
        good.append(True)
    while total > 0 and Attempts < 20:
        Attempts += 1
        #print(Attempts)
        i=0
        for pos in points:
            smallPoints = list(points)
            smallPoints.remove(pos)
            CurrentTotal, Xrange, Yrange = TotalRange(points)
            s = getSurround(g,pos)
            #print(pos, s)
            for pos2 in s:
                newTotal, newX, newY = TotalRange(smallPoints+[pos2])
                if newTotal > CurrentTotal or (newX+newY > Xrange + Yrange):
                    if len(getSurround(g,pos2)) > 3:
                        points[i] = pos2
                        break
                elif newTotal == CurrentTotal:
                    if (newX > Xrange and newY == Yrange) or (newY > Yrange and newX == Xrange):
                        if len(getSurround(g,pos2)) > 3:
                            points[i] = pos2
                            break
            else:
                if good[i]:
                    good[i] = False
                    total-=1
            i+=1
    connections = n*(n-1)/2
    if n > 2:
        if MinRange(points) < TotalRange(points)[0]/(connections+(n-2)*5-4):
            points = findStartSpots(g, n)
    elif n == 2:
        if TotalRange(points)[0] < 5:
            points = findStartSpots(g, n)
    return points

def getAttacks(unit):
    if not 'attack' in unit.possibleStates:
        return []
    spaces = getRangeCircles(unit, True)
    finalSpaces = []
    for pos in spaces:
        u = GV.game.getAnyUnitFromPos(pos[0],pos[1])
        if u:
            goodToAdd = True
            if u == unit:
                goodToAdd = False
            if 'onlyHit' in unit.abilities:
                if not (u.type in unit.abilities['onlyHit']):
                    goodToAdd = False
            if goodToAdd and (GV.game.checkFriendlyPlayer(u, GV.player)):
                goodToAdd = False
            if goodToAdd:
                finalSpaces.append(pos)
    return finalSpaces

def getHeals(unit):
    if not 'heal' in unit.possibleStates:
        return []
    spaces = getRangeCircles(unit, True)
    finalSpaces = []
    for pos in spaces:
        u = GV.game.getAnyUnitFromPos(pos[0],pos[1])
        if u:
            goodToAdd = True
            if u == unit:
                goodToAdd = False
            if 'onlyHeal' in unit.abilities:
                if not (u.type in unit.abilities['onlyHeal']):
                    goodToAdd = False
            if goodToAdd and (not GV.game.checkFriendlyPlayer(u, GV.player)):
                goodToAdd = False
            if u.health == u.maxHealth:
                goodToAdd = False
            if goodToAdd:
                finalSpaces.append(pos)
    return finalSpaces

def roundEnd(g1,g2):
    return g2.turn > g1.turn

def getCount(n):
    count = 0
    for u in GV.game.units[GV.player]:
        if u.name == n:
            count+=1
    return count

#Get rid of this function later
image = GV.pygame.image.load("assets/%s.png" % "soldier")
def showUnit(x,y, im = image):
    GV.DISPLAYSURF.blit(im,(x*(GV.block_size+1)+GV.offset_x-1, y*(GV.block_size+1)+GV.offset_y-1))
    
    t = str(random.randint(0,20))#Health Value
    Healthfont = GV.pygame.font.SysFont("arial", 15)
    text = Healthfont.render(t, 1, RED)
    GV.DISPLAYSURF.blit(text, (x*(GV.block_size+1)+GV.offset_x+38-(7*len(t)), y*(GV.block_size+1)+GV.offset_y+23))
    
    rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x+GV.block_size - 9, y*(GV.block_size+1)+GV.offset_y+4, 5, 5)
    GV.pygame.draw.rect(GV.DISPLAYSURF, (0,255,255), rect)
unitImages = {}
darkunitImages = {}
GV.playerUnitImages = {}
buildUnitImages = {}
#GV.playerColors = [(201, 59, 54,255),(59, 151, 217,255),(117, 69, 143,255),(167, 242, 46,255),(122, 129, 153),(107, 64, 0)]
#GV.playerColors = [(201, 59, 54,255),(167, 242, 46,255), (255, 115, 0,255),(59, 151, 217,255),(117, 69, 143,255),(167, 242, 46,255),(122, 129, 153),(107, 64, 0)]
#GV.playerColors = [(201, 59, 54,255),(150,150,150,255), (255, 115, 0,255),(59, 151, 217,255),(117, 69, 143,255),(167, 242, 46,255),(122, 129, 153),(107, 64, 0)]
#GV.playerColors = [(117, 69, 143,255),(167, 242, 46,255),(122, 129, 153),(107, 64, 0)]
#GV.playerColors = [(201, 59, 54,255),(150,150,150,255),(0, 195, 255,255),(107, 64, 0),(167, 242, 46)]
###GV.playerColors = [(201, 59, 54,255),(0, 195, 255),(255, 136, 0,255),(107, 64, 0),(167, 242, 46)]
#GV.playerColors = [(230,230,230),(0, 195, 255),(255, 136, 0,255),(107, 64, 0),(167, 242, 46)]
AIcolors = [(150,150,150),(50,50,50),(230,230,230), (116, 92, 138), (60, 112, 158),(102, 115, 94),(161, 224, 255) ]
"""
Colors:
Red: (201, 59, 54,255)
Blue: (59, 151, 217,255)
Grey: (150,150,150,255)


Dark Purple: (117, 69, 143,255)
Electric Blue : (0, 195, 255)
Bright Purple: (170, 0, 255)
Lime Green: (167, 242, 46)
bright orange: (255, 136, 0)

"""

#random.shuffle(GV.playerColors)

#GV.changeColor = (233,19,212,255)

#GV.block_size = 40

def getImage(name, p, Pictures = 1, size = False):
    if Pictures == 1:
        Pictures = GV.playerUnitImages
    if not size:
        size = GV.block_size
    if not p in Pictures:
        Pictures[p] = {}
    if not name in Pictures[p]:
        img = Image.open("assets/%s.png" % name)
        pixels = img.load()
        for i in range(img.size[0]): # for every pixel:
            for j in range(img.size[1]):
                if pixels[i,j] == GV.changeColor:
                    pixels[i,j] = GV.playerColors[p]
        img = GV.pygame.image.fromstring(img.tobytes(), img.size, img.mode)
        img = GV.pygame.transform.scale(img, (size, size))
        Pictures[p][name] = img
    return Pictures[p][name]

def showUnitNEW(unit):
    x = unit.position[0]
    y = unit.position[1]
    image = None
    
    for p in GV.game.units:
        if unit in GV.game.units[p]:
            image = getImage(unit.name, p)
            break
    """
    if unit in GV.game.units[GV.player] or (not imageMani):
        if not unit.name in unitImages:
            img = GV.pygame.image.load("assets/%s.png" % unit.name)
            img = GV.pygame.transform.scale(img, (40, 40))
            unitImages[unit.name] = img
        image = unitImages[unit.name]
    else:
        if not unit.name in darkunitImages:
            img = Image.open("assets/%s.png" % unit.name)
            pixels = img.load()
            for i in range(img.size[0]): # for every pixel:
                for j in range(img.size[1]):
                    pixels[i,j] = (int(pixels[i,j][0]/2),int(pixels[i,j][1]/2),int(pixels[i,j][2]/2),pixels[i,j][3])
            img = GV.pygame.image.fromstring(img.tobytes(), img.size, img.mode)
            darkunitImages[unit.name] = GV.pygame.transform.scale(img, (40, 40))
        image = darkunitImages[unit.name]
    """
    GV.DISPLAYSURF.blit(image,(x*(GV.block_size+1)+GV.offset_x-1, y*(GV.block_size+1)+GV.offset_y-1))
    
    t = str(unit.health)
    Healthfont = GV.pygame.font.SysFont("arial", 15)
    text = Healthfont.render(t, 1, WHITE)
    #GV.DISPLAYSURF.blit(text, (x*(GV.block_size+1)+GV.offset_x+38-(7*len(t)), y*(GV.block_size+1)+GV.offset_y+23))
    GV.DISPLAYSURF.blit(text, (x*(GV.block_size+1)+GV.offset_x+(GV.block_size-2)-(7*len(t)), y*(GV.block_size+1)+GV.offset_y+(GV.block_size-17)))

    #State square
    if unit.state != None and unit in GV.game.units[GV.player]:
        #print(vars(unit))
        rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x+GV.block_size - 9, y*(GV.block_size+1)+GV.offset_y+4, 5, 5)
        if unit.state == 'resources':
            if unit.stateData and type(unit.stateData) == str and unit.stateData in GV.resourceColors:
                GV.pygame.draw.rect(GV.DISPLAYSURF, GV.resourceColors[unit.stateData], rect)
        else:
            GV.pygame.draw.rect(GV.DISPLAYSURF, GV.StateColors[unit.state], rect)


def animateUnit(unit1, unit2,t,specfic_player):
    unit = unit1
    if not unit1:
        unit = unit2
    x = unit.position[0]
    y = unit.position[1]
    image = None
    if GV.animateGrid[y][x]:
        return

    image = getImage(unit.name, specfic_player)
    
    default = True
    if not unit1:
        parent = GV.game.getUnitFromID(unit2.parent)
        if parent:
            default = False
            x2,y2 = parent.position
            start = (x2*(GV.block_size+1)+GV.offset_x-1, y2*(GV.block_size+1)+GV.offset_y-1)
            end = (x*(GV.block_size+1)+GV.offset_x-1, y*(GV.block_size+1)+GV.offset_y-1)
            Pos = intPoint(LerpPoint(start, end, t/animateTime))
            GV.DISPLAYSURF.blit(image,Pos)
    elif unit1.position != unit2.position:
        default = False
        start = (x*(GV.block_size+1)+GV.offset_x-1, y*(GV.block_size+1)+GV.offset_y-1)
        end = (unit2.position[0]*(GV.block_size+1)+GV.offset_x-1, unit2.position[1]*(GV.block_size+1)+GV.offset_y-1)
        Pos = intPoint(LerpPoint(start, end, t/animateTime))
        GV.DISPLAYSURF.blit(image,Pos)
    if default:#No move
        GV.DISPLAYSURF.blit(image,(x*(GV.block_size+1)+GV.offset_x-1, y*(GV.block_size+1)+GV.offset_y-1))
        T = str(unit.health)
        Healthfont = GV.pygame.font.SysFont("arial", 15)
        text = Healthfont.render(T, 1, WHITE)
        if unit1 and unit2:
            if unit2.health < unit1.health:
                T = str(int(Lerp(unit1.health, unit2.health, t/animateTime)))
                text = Healthfont.render(T, 1, RED)
            elif unit2.health > unit1.health:
                T = str(int(Lerp(unit1.health, unit2.health, t/animateTime)))
                text = Healthfont.render(T, 1, WHITE)
            elif unit1 == unit2:
                T = str(int(Lerp(unit1.health, 0, t/animateTime)))
                text = Healthfont.render(T, 1, RED)
        GV.DISPLAYSURF.blit(text, (x*(GV.block_size+1)+GV.offset_x+(GV.block_size-2)-(7*len(T)), y*(GV.block_size+1)+GV.offset_y+(GV.block_size-17)))

        #State square
        if unit2:
            unit = unit2
        if unit.state != None and unit1 in GV.game.units[specfic_player]:
            #print(vars(unit))
            rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x+GV.block_size - 9, y*(GV.block_size+1)+GV.offset_y+4, 5, 5)
            if unit.state == 'resources':
                if unit.stateData and type(unit.stateData) == str and unit.stateData in GV.resourceColors:
                    GV.pygame.draw.rect(GV.DISPLAYSURF, GV.resourceColors[unit.stateData], rect)
            else:
                GV.pygame.draw.rect(GV.DISPLAYSURF, GV.StateColors[unit.state], rect)
    if unit1 == unit2:
        GV.DISPLAYSURF.blit(RedX,(x*(GV.block_size+1)+GV.offset_x-1, y*(GV.block_size+1)+GV.offset_y-1))

def drawLine(color,pos1,pos2):
    GV.pygame.draw.line(GV.DISPLAYSURF, color, ((GV.block_size+1)*pos1[0]+GV.offset_x+GV.block_size/2,(GV.block_size+1)*pos1[1]+GV.offset_y+GV.block_size/2),((GV.block_size+1)*pos2[0]+GV.offset_x+GV.block_size/2,(GV.block_size+1)*pos2[1]+GV.offset_y+GV.block_size/2),10)

def drawGrid():
    i = 0
    for y in range(GV.board_y):
        for x in range(GV.board_x):
            rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x, y*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
            GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BoardColors[i], rect)
            i+=1
            
def drawAnimateGrid():
    i = 0
    for y in range(GV.board_y):
        for x in range(GV.board_x):
            rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x, y*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
            if GV.animateGrid[y][x]:
                pass
            else:
                GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BoardColors[i], rect)
            i+=1

def drawGridHighlight():
    i = 0
    for y in range(GV.board_y):
        for x in range(GV.board_x):
            rect = None
            if [x,y] in GV.highlightSquares:
                rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x+1, y*(GV.block_size+1)+GV.offset_y+1, GV.block_size-1, GV.block_size-1)
            else:
                rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x, y*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
            GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BoardColors[i], rect)
            i+=1

animateTime = 20


#GV.offset_x = 115
#GV.offset_y = 10

GV.board_x = 10
GV.board_y = 10

endOfBoard_x = (GV.block_size+1)*GV.board_x+GV.offset_x#525
endOfBoard_y = (GV.block_size+1)*GV.board_y+GV.offset_y#420

WINDOWWIDTH = 640#GV.offset_x*2+(GV.block_size+1)*GV.board_x#640
WINDOWHEIGHT = 480#GV.offset_y+60+(GV.block_size+1)*GV.board_y#480
print('x&y',WINDOWWIDTH,WINDOWHEIGHT)

GV.highlightSquares = []
#GV.BoardColors = []
CloudColors = []
moveCircles = []
possibleAttacks = []
possibleHeals = []
buildHexes = []
Grid = []
cloudGrid = []
explorationGrid = []
GV.animateGrid = []

blueCircle = GV.pygame.image.load("assets/MoveCircle.png")
OrangeHex = GV.pygame.image.load("assets/BuildHex.png")
RedX = GV.pygame.image.load("assets/AttackX.png")
GreenT = GV.pygame.image.load("assets/HealT.png")
Beaker = GV.pygame.image.load("assets/Beaker.png")
print(type(blueCircle))

DoneButton = Button("Done", endOfBoard_x, endOfBoard_y+10, (50,200,50),BLACK,22,(60,40))

#counter = 0

def Lerp(a,b,t):
    return a+t*(b-a)

def LerpPoint(a,b,t):
    return (Lerp(a[0],b[0],t),Lerp(a[1],b[1],t))

def intPoint(p):
    return (int(p[0]),int(p[1]))

def int_to_bool_list(num):
    return [bool(num & (1<<n)) for n in range(8)][::-1]

def intToList(x, width):
    l = []
    for v in x:
        #print(v)
        l+=int_to_bool_list(v)
    l2 = []
    for i in range(len(l)//width):
            l2.append(l[(i*width):((i+1)*width)])
    return l2

def updateCloudCover():
    global cloudGrid,explorationGrid
    if cloudMode == "sight" or cloudMode == "halo":
        cloudGrid = []
        for y in range(GV.board_y):
            l = []
            for x in range(GV.board_x):
                l.append(True)
            cloudGrid.append(l)
    for u in GV.game.units[GV.player]:
        spaces = getRangeCircles(u, True)
        for pos in spaces:
            if cloudGrid[pos[1]][pos[0]]:
                cloudGrid[pos[1]][pos[0]] = False
            if cloudMode == "halo" and explorationGrid[pos[1]][pos[0]]:
                explorationGrid[pos[1]][pos[0]] = False
def drawClouds():
    if cloudMode == "clear":
        return
    i = 0
    for y in range(GV.board_y):
        for x in range(GV.board_x):
            if cloudGrid[y][x] and cloudMode != "halo":
                rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x, y*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
                GV.pygame.draw.rect(GV.DISPLAYSURF, CloudColors[i], rect)
            elif cloudMode == "halo":
                if explorationGrid[y][x]:
                    rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x, y*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
                    GV.pygame.draw.rect(GV.DISPLAYSURF, CloudColors[i], rect)
                elif cloudGrid[y][x]:
                    rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x, y*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
                    #color = list( map(add, CloudColors[i], GV.BoardColors[i]) )
                    color = list( map(add, (0,0,0), GV.BoardColors[i]) )
                    color = [x / 2 for x in color]
                    GV.pygame.draw.rect(GV.DISPLAYSURF, color, rect)
            i+=1

def updateSelf():
    global endOfBoard_x, endOfBoard_y, WINDOWWIDTH, WINDOWHEIGHT, DoneButton, Grid,cloudGrid,explorationGrid,CloudColors,blueCircle,OrangeHex,RedX,GreenT,Beaker,cloudMode,currentTechMenu
    print('blocksize',GV.block_size)
    GV.board_x = GV.game.width
    GV.board_y = GV.game.height
    cloudMode = GV.game.mode

    if GV.game.ai > 0:
        j = 0
        for i in range(len(GV.game.units)-GV.game.ai,len(GV.game.units)):
            GV.playerColors.insert(i, AIcolors[j])
            j+=1
    endOfBoard_x = (GV.block_size+1)*GV.board_x+GV.offset_x#525
    endOfBoard_y = (GV.block_size+1)*GV.board_y+GV.offset_y#420

    WINDOWWIDTH = GV.offset_x*2+(GV.block_size+1)*GV.board_x#640
    WINDOWHEIGHT = GV.offset_y+60+(GV.block_size+1)*GV.board_y

    GV.DISPLAYSURF = GV.pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),RESIZABLE)
    GV.DISPLAYSURF.fill(BGCOLOR)
    DoneButton = Button("Done", endOfBoard_x, endOfBoard_y+10, (50,200,50),BLACK,22,(60,40))

    blueCircle = GV.pygame.image.load("assets/MoveCircle.png")
    OrangeHex = GV.pygame.image.load("assets/BuildHex.png")
    RedX = GV.pygame.image.load("assets/AttackX.png")
    GreenT = GV.pygame.image.load("assets/HealT.png")
    Beaker = GV.pygame.image.load("assets/Beaker.png")
    blueCircle = GV.pygame.transform.scale(blueCircle, (GV.block_size, GV.block_size))
    OrangeHex = GV.pygame.transform.scale(OrangeHex, (GV.block_size, GV.block_size))
    RedX = GV.pygame.transform.scale(RedX, (GV.block_size, GV.block_size))
    GreenT = GV.pygame.transform.scale(GreenT, (GV.block_size, GV.block_size))
    Beaker = GV.pygame.transform.scale(Beaker, (GV.block_size, GV.block_size))

    currentTechMenu = []
    
    Grid = intToList(GV.game.intGrid, GV.board_x)
    print(Grid)
    cloudGrid = []
    for y in range(GV.board_y):
        l = []
        for x in range(GV.board_x):
            l.append(True)
        cloudGrid.append(l)
        
    if cloudMode == "halo": 
        explorationGrid = []
        for y in range(GV.board_y):
            l = []
            for x in range(GV.board_x):
                l.append(True)
            explorationGrid.append(l)
    
    GV.BoardColors = []
    CloudColors = []
    y = 0
    for v in Grid:
        x = 0
        for v2 in v:
            if v2:
                GV.BoardColors.append(randomBlue())
            else:
                #GV.BoardColors.append(randomGreen())
                if isNextToWater([x,y]):
                    #print("YELLOW")
                    GV.BoardColors.append(randomYellow())
                else:
                    #print("GRWEEN")
                    GV.BoardColors.append(randomGreen())
            x+=1
        y+=1
    for v in Grid:
        for v2 in v:
            if cloudMode == "halo": 
                CloudColors.append(randomDark())
            else:
                CloudColors.append(randomWhite())

def animationGrid(g1,g2):
    GV.animateGrid = methods.newGrid2(GV.board_x,GV.board_y)
    l = []
    for i in GV.game.units:
        for u in GV.game.units[i]:
            u2 = g2.getUnitFromID(u.UnitID)
            if u2:#Unit changed
                if u.health != u2.health or u.position != u2.position:
                    l.append([u.position, u2.position])
            else:
                l.append([u.position])#Unit destroyed
    for i in g2.units:
        for u2 in g2.units[i]:
            u = GV.game.getUnitFromID(u2.UnitID)
            if not u:
                parent = GV.game.getUnitFromID(u2.parent)
                if parent:
                    l.append([u2.position, parent.position])
    for v in l:
        if len(v) == 1:
            GV.animateGrid[v[0][1]][v[0][0]] = False
        else:
            a = min(v[0][0], v[1][0])
            b = max(v[0][0], v[1][0])
            c = min(v[0][1], v[1][1])
            d = max(v[0][1], v[1][1])
            for y in range(c,d+1):
                for x in range(a,b+1):
                    GV.animateGrid[y][x] = False

NotAlreadyReady = True

def animateBoard(g1,g2,t):
    #rect = GV.pygame.Rect(GV.offset_x-1,GV.offset_y-1, (GV.block_size+1)*GV.board_x+1,(GV.block_size+1)*GV.board_y+1)#+GV.offset_x,410+GV.offset_y)
    #GV.pygame.draw.rect(GV.DISPLAYSURF, BGCOLOR, rect)
    drawAnimateGrid()#drawGrid()
    resourcesAnimated(g2,t/animateTime)

    techDrawn = []

    for i in g1.units:
        for u in GV.game.units[i]:
            if u.stateData:#In case target isn't selected yet
                #print("Rodeo")
                color = False
                spots = None
                if u.state == 'move':
                    if checkRange(u,u.stateData) > u.speed:
                        color = (45, 150, 138)
                        spots = (u.position,u.stateData)
                        drawLine((45, 150, 138),u.position,u.stateData)
                    else:
                        color = (0,255,255)
                        print("more colro", color)
                        spots = (u.position,u.stateData)
                        drawLine((0,255,255),u.position,u.stateData)
                elif u.state == 'attack':
                    pos = None
                    if type(u.stateData) == dict:
                        pos = u.stateData['position']
                    else:
                        pos = u.stateData.position
                    if checkRange(u,pos) > u.range:
                        color = (148, 55, 49)
                        spots = (u.position,pos)
                        drawLine((148, 55, 49),u.position,pos)
                    else:
                        color = (255,0,0)
                        spots = (u.position,pos)
                        drawLine((255,0,0),u.position,pos)
                elif u.state == 'heal':
                    pos = None
                    if type(u.stateData) == dict:
                        pos = u.stateData['position']
                    else:
                        pos = u.stateData.position
                    if checkRange(u,pos) > u.range:
                        color = (150, 150, 150)
                        spots = (u.position,pos)
                        drawLine((150, 150, 150),u.position,pos)
                    else:
                        color = (255,255,255)
                        spots = (u.position,pos)
                        drawLine((255,255,255),u.position,pos)
                elif u.state == 'build':
                    print('BUILD BUILD BIT')
                    if len(u.stateData) == 2:
                        if checkRange(u,u.stateData[0]) > u.range:
                            color = (110, 106, 46)
                            spots = (u.position,u.stateData[0])
                            drawLine((110, 106, 46),u.position,u.stateData[0])
                        else:
                            color = (255,170,0)
                            print("more colro", color)
                            spots = (u.position,u.stateData[0])
                            drawLine((255,170,0),u.position,u.stateData[0])
                elif u.state == 'research':
                    if g1.checkFriendlyPlayer(u, GV.player) and (not u.stateData in techDrawn) and (u.stateData in g2.tech[GV.player]):
                        img = GV.pygame.image.load("techAssets/%s.png" % u.stateData)
                        img = GV.pygame.transform.scale(img, (40, 40))
                        #img = GV.pygame.image.load("assets/%s.png" % v)
                        #img = GV.pygame.transform.scale(img, (40, 40))
                        GV.DISPLAYSURF.blit(img,(GV.offset_x+(40+1)*len(techDrawn), endOfBoard_y+10))#(115+41*i, 430)
                        techDrawn.append(u.stateData)
                        
                print("COLOR",color, u.state, u.stateData)
                if color:
                    drawLine(color,spots[0],spots[1])
                    
    for i in GV.game.units:
        for u in GV.game.units[i]:
            u2 = g2.getUnitFromID(u.UnitID)
            if u2:
                animateUnit(u,u2,t,i) #Unit changed
            else:
                animateUnit(u,u,t,i)#Unit destroyed
    for i in g2.units:
        for u2 in g2.units[i]:
            u = GV.game.getUnitFromID(u2.UnitID)
            if not u:
                print('here we go')
                animateUnit(None,u2,t,i)#New unit is built
    drawClouds()

def changeAnimateSpeed(g1,g2):
    global animateTime
    units = 0
    for i in GV.game.units:
        for u in GV.game.units[i]:
            u2 = g2.getUnitFromID(u.UnitID)
            if not u2: #Unit died
                units+=1
            elif u.position != u2.position: #Unit moved
                units+=1
            elif u.health != u2.health: #Unit attacked
                units+=1
    for i in g2.units:
        for u2 in g2.units[i]:
            u = GV.game.getUnitFromID(u2.UnitID)
            if not u: #New unit built
                units+=1
    animateTime = min(20,10+units*2)

def GetUnlockedTechs():
    techs = []
    for t in GV.game.tech[GV.player]:
        for t2 in TechDB[t]['unlocks']:
            if (not t2 in techs) and (not t2 in GV.game.tech[GV.player]):
                techs.append(t2)
    starters = ['bionics', 'time travel','recruitment','armament','aviation']
    for t in starters:
        if (not t in techs) and (not t in GV.game.tech[GV.player]):
            techs.append(t)
    toRemove = []
    for t in GV.game.tech[GV.player]:
        if TechDB[t].get('deny'):
            for t2 in TechDB[t].get('deny'):
                if t2 in techs:
                    toRemove.append(t2)
    for t in toRemove:
        techs.remove(t)
    #TODO: Add starter techs {DONE}
    return techs

techSize = 60

def techButtonSize(n):
    global techSize
    width = (GV.block_size+1)*GV.board_x
    height = (GV.block_size+1)*GV.board_y
    if techSize < 60:
        if math.floor(width/(41))*math.floor(height/(41)) >= n:
            techSize = 60
            return
    currentMax = math.floor(width/(techSize+1))*math.floor(height/(techSize+1))
    if currentMax < n:
        techSize = 60
        while math.floor(width/(techSize+1))*math.floor(height/(techSize+1)) < n:
            techSize-=1

def checkTechAffordable(unit, tech):
    cost = TechDB[tech]['cost']
    resource = dict(GV.game.resources[GV.player])["energy"]

    #Account for costs of planned units (and planned research)
    newEnergyCosts = 0
    for u in GV.game.units[GV.player]:
        if u != unit and u.state == 'build' and type(u.stateData) == list:
            cost2 = UnitDB[u.stateData[1]]['cost']
            if 'abilities' in UnitDB[u.stateData[1]] and 'costly' in UnitDB[u.stateData[1]]['abilities']:
                cost2 = copy.copy(cost2)
                count = getCount(u.stateData[1])
                for v in cost2:
                    cost2[v] = cost2[v]*(UnitDB[u.stateData[1]]['abilities']['costly']**count)//5*5
            for v in cost2:
                if v == "energy":
                    newEnergyCosts += cost2[v]
        elif u != unit and u.state == 'research' and type(u.stateData) == str:
            newEnergyCosts += TechDB[u.stateData]["cost"]
    
    for v in newResources:
        if v == "energy":
            resource += newResources[v]
    
    resource -= newEnergyCosts

    if unit.state == 'resources' and type(unit.stateData) == str:
        if unit.stateData == "energy":
            resource -= unit.resourceGen[unit.stateData]
    if resource < cost:
        return False
    return True

currentTechMenu = []
currentTechImages = {}
currentTechButtons = []
currentlyResearch = False
PrevTechHover = False
CurrentTechHover = False
knownTechHover = False

def researchMenu():
    global currentTechMenu,currentTechImages,currentTechButtons,currentlyResearch,knownTechHover
    techs = GetUnlockedTechs()
    if techs == currentTechMenu and currentlyResearch and knownTechHover == CurrentTechHover:
        return
    knownTechHover = CurrentTechHover
    currentlyResearch = True
    currentTechMenu = techs
    print(currentTechMenu)
    size = int(techSize)
    print('tech size', techSize)
    techButtonSize(len(currentTechMenu))
    if size != techSize:
        currentTechImages = {}
    currentTechButtons = []
    w = math.ceil(math.sqrt(len(techs)))#len(techs)//math.ceil(math.sqrt(w)
    #w = math.floor((GV.block_size+1)*GV.board_x/(techSize+1))
    print('w',w)
    #w = len(techs)//math.ceil(math.sqrt(w))
    if w == 0: w = 1;
    print(w)
    if w > math.floor((GV.block_size+1)*GV.board_x/(techSize+1)):
        w = math.floor((GV.block_size+1)*GV.board_x/(techSize+1))
    extraX = ( (GV.block_size+1)*GV.board_x - (w*(techSize+1)) )//2
    #print('(GV.block_size+1)*GV.board_y',(GV.block_size+1)*GV.board_y)
    #print('math.ceil(w/len(techs))',math.ceil(len(techs)/w))
    #print('(math.ceil(w/len(techs))*(techSize+1))',(math.ceil(len(techs)/w)*(techSize+1)))
    #print('all',( (GV.block_size+1)*GV.board_y - (math.ceil(len(techs)/w)*(techSize+1)) )//2)
    extraY = ( (GV.block_size+1)*GV.board_y - (math.ceil(len(techs)/w)*(techSize+1)) )//2
    print('extraY',extraY)
    rect = GV.pygame.Rect(GV.offset_x-1,GV.offset_y-1, (GV.block_size+1)*GV.board_x+1,(GV.block_size+1)*GV.board_y+1)#+GV.offset_x,410+GV.offset_y)
    GV.pygame.draw.rect(GV.DISPLAYSURF, BLACK, rect)

    maybeDeny = []
    if CurrentTechHover:
        maybeDeny = TechDB[CurrentTechHover].get('deny') or []
    
    for i, t in enumerate(currentTechMenu):
        x = i%w
        y = i//w
        b = Button("", x*(techSize+1)+GV.offset_x+1+extraX, y*(techSize+1)+GV.offset_y+1+extraY, BLACK,BLACK,18,(techSize,techSize),t)
        b.active = True
        currentTechButtons.append(b)
        if not t in currentTechImages:
            img = GV.pygame.image.load("techAssets/%s.png" % t)
            img = GV.pygame.transform.scale(img, (techSize, techSize))
            currentTechImages[t] = img
        pos = (x*(techSize+1)+GV.offset_x-1+extraX, y*(techSize+1)+GV.offset_y-1+extraY)
        GV.DISPLAYSURF.blit(currentTechImages[t], pos)
        if t in maybeDeny:
            s = GV.pygame.Surface((techSize, techSize))
            s.set_alpha(128)
            s.fill((0,0,0))
            GV.DISPLAYSURF.blit(s, pos)
        if t == CurrentTechHover:
            s = GV.pygame.Surface((techSize, techSize))
            s.set_alpha(25)
            s.fill((255,255,255))
            GV.DISPLAYSURF.blit(s, pos)
        if TechDB[t]['time'] > 1:
            n = TechDB[t]['time'] 
            if t in GV.game.progress[GV.player]:
                n -= GV.game.progress[GV.player][t]
            if n > 1:
                T = str(n)
                Healthfont = GV.pygame.font.SysFont("arial", 15)
                text = Healthfont.render(T, 1, WHITE)
                GV.DISPLAYSURF.blit(text, pos)
        if not checkTechAffordable(selected, t):
            s = GV.pygame.Surface((techSize, techSize))
            s.set_alpha(160)
            s.fill((0,0,0))
            GV.DISPLAYSURF.blit(s, pos)
        #Make images (similar to getImage) {DONE}
        #Display button with image on top {Done}
        #add buttons to techbuttons {DONE}

def drawBoard():
    print('drawing BOARD')
    global NotAlreadyReady, currentlyResearch
    #print("______________________________")
    #print(vars(GV.game))
    if GV.game.ready:
        if NotAlreadyReady:
            NotAlreadyReady = False
            updateSelf()
        if not GV.game.went[GV.player]:
            allElseWent = True
            for v in GV.game.went:
                if (not GV.game.went[v]) and v != GV.player:
                    allElseWent = False
            if allElseWent and len(GV.game.went) > 1 and (counter%40)//20 == 0:
                DoneButton.color = (255,255,255)
            else:
                DoneButton.color = (50,200,50)
            DoneButton.draw(GV.DISPLAYSURF)
        #print('We are here we are here we are here')
        #print("WENT", GV.game.went)
        #print(vars(GV.game))
        for i in GV.game.went:
            rect = GV.pygame.Rect(endOfBoard_x + 70 + 10 *i, endOfBoard_y+12,8,8)
            if GV.game.went[i]:
                GV.pygame.draw.rect(GV.DISPLAYSURF, GV.playerColors[i], rect)
            else:
                GV.pygame.draw.rect(GV.DISPLAYSURF, BGCOLOR, rect)
        #print('selected',selected)
        #print('stateDataMode',stateDataMode)
        if selected and stateDataMode == 'research':
            print('researching....')
            researchMenu()
            return
        currentlyResearch = False
        rect = GV.pygame.Rect(GV.offset_x-1,GV.offset_y-1, (GV.block_size+1)*GV.board_x+1,(GV.block_size+1)*GV.board_y+1)#+GV.offset_x,410+GV.offset_y)
        GV.pygame.draw.rect(GV.DISPLAYSURF, BGCOLOR, rect)
        for v in GV.highlightSquares:
            highlightSquare(v[0],v[1])
        if len(GV.highlightSquares) > 0:
            drawGridHighlight()
        else:
            drawGrid()
        for u in GV.game.units[GV.player]:
            if u.stateData:#In case target isn't selected yet
                if u.state == 'move' and type(u.stateData) == list and type(u.stateData[0]) == int:
                    if checkRange(u,u.stateData) > u.speed:
                        drawLine((45, 150, 138),u.position,u.stateData)
                    else:
                        drawLine((0,255,255),u.position,u.stateData)
                elif u.state == 'attack':
                    print(u.stateData)
                    pos = None
                    if type(u.stateData) == dict:
                        pos = u.stateData['position']
                    elif isinstance(u.stateData, Unit):
                        pos = u.stateData.position
                    else:
                        continue
                    if type(u.stateData) != list and checkRange(u,pos) > u.range:
                        drawLine((148, 55, 49),u.position,pos)
                    else:
                        drawLine((255,0,0),u.position,pos)
                elif u.state == 'heal':
                    print(u.stateData)
                    pos = None
                    if type(u.stateData) == dict:
                        pos = u.stateData['position']
                    elif isinstance(u.stateData, Unit):
                        pos = u.stateData.position
                    else:
                        continue
                    if type(u.stateData) != list and checkRange(u,pos) > u.range:
                        drawLine((150, 150, 150),u.position,pos)
                    else:
                        drawLine((255,255,255),u.position,pos)
                elif u.state == 'build':
                    if len(u.stateData) == 2:
                        if checkRange(u,u.stateData[0]) > u.range:
                            drawLine((110, 106, 46),u.position,u.stateData[0])
                        else:
                            drawLine((255,170,0),u.position,u.stateData[0])
        for i in GV.game.units:
            for u in GV.game.units[i]:
                showUnitNEW(u)
        for pos in moveCircles:
            GV.DISPLAYSURF.blit(blueCircle,(pos[0]*(GV.block_size+1)+GV.offset_x-1, pos[1]*(GV.block_size+1)+GV.offset_y-1))
        for pos in buildHexes:
            GV.DISPLAYSURF.blit(OrangeHex,(pos[0]*(GV.block_size+1)+GV.offset_x-1, pos[1]*(GV.block_size+1)+GV.offset_y-1))
        for pos in possibleAttacks:
            GV.DISPLAYSURF.blit(RedX,(pos[0]*(GV.block_size+1)+GV.offset_x-1, pos[1]*(GV.block_size+1)+GV.offset_y-1))
        for pos in possibleHeals:
            GV.DISPLAYSURF.blit(GreenT,(pos[0]*(GV.block_size+1)+GV.offset_x-1, pos[1]*(GV.block_size+1)+GV.offset_y-1))
        if selected:
            print('you have someone selected')
            print('posible',selected.possibleStates)
            if 'research' in selected.possibleStates and stateDataMode == None:
                print('yay for research')
                pos = selected.position
                GV.DISPLAYSURF.blit(Beaker,(pos[0]*(GV.block_size+1)+GV.offset_x-1, pos[1]*(GV.block_size+1)+GV.offset_y-1))
        updateCloudCover()
        drawClouds()
    else:
        font = GV.pygame.font.SysFont("arial", 60)
        text = font.render("Waiting...", 1, (255,0,0))
        GV.DISPLAYSURF.blit(text, (200,200))

newResources = {'gold':0,'metal':0,'energy':0}
newCosts = {'gold':0,'metal':0,'energy':0}

def resources():
    global newResources
    res = {
        'gold':0,
        'metal':0,
        'energy':0
    }
    for u in GV.game.units[GV.player]:
        if u.state == 'resources':
            if u.stateData and type(u.stateData) == str and u.stateData in res:
                res[u.stateData] += u.resourceGen[u.stateData]
    newResources = res
    rect = GV.pygame.Rect(2,WINDOWHEIGHT-52, 80,50)#428
    GV.pygame.draw.rect(GV.DISPLAYSURF, (50,50,50), rect)
    Healthfont = GV.pygame.font.SysFont("arial", 15)
    text = Healthfont.render("%s + %s" % (str(GV.game.resources[GV.player]['gold']), res['gold']), 1, (255,255,0))
    GV.DISPLAYSURF.blit(text, (5,WINDOWHEIGHT-50))#430
    text = Healthfont.render("%s + %s" % (str(GV.game.resources[GV.player]['metal']), res['metal']), 1, (255,255,255))
    GV.DISPLAYSURF.blit(text, (5,WINDOWHEIGHT-35))#445
    text = Healthfont.render("%s + %s" % (str(GV.game.resources[GV.player]['energy']), res['energy']), 1, (0,255,255))
    GV.DISPLAYSURF.blit(text, (5,WINDOWHEIGHT-20))#460

def checkIfAffordable(unit, built):
    cost = UnitDB[built]['cost']
    if 'abilities' in UnitDB[built] and 'costly' in UnitDB[built]['abilities']:
        cost = copy.copy(cost)
        count = getCount(built)
        for v in cost:
            cost[v] = cost[v]*(UnitDB[built]['abilities']['costly']**count)//5*5
    resource = dict(GV.game.resources[GV.player])
    
    #Account for costs of planned units (and planned research)
    newCosts = {'gold':0,'metal':0,'energy':0}
    for u in GV.game.units[GV.player]:
        if u != unit and u.state == 'build' and type(u.stateData) == list:
            cost2 = UnitDB[u.stateData[1]]['cost']
            if 'abilities' in UnitDB[u.stateData[1]] and 'costly' in UnitDB[u.stateData[1]]['abilities']:
                cost2 = copy.copy(cost2)
                count = getCount(u.stateData[1])
                for v in cost2:
                    cost2[v] = cost2[v]*(UnitDB[u.stateData[1]]['abilities']['costly']**count)//5*5
            for v in cost2:
                newCosts[v] += cost2[v]
        elif u != unit and u.state == 'research' and type(u.stateData) == str:
            newCosts["energy"] += TechDB[u.stateData]["cost"]
    
    for v in newResources:
        resource[v] += newResources[v]
    for v in newCosts:
        resource[v] -= newCosts[v]
    if unit.state == 'resources' and type(unit.stateData) == str:
        resource[unit.stateData] -= unit.resourceGen[unit.stateData]
    for v in cost:
        if resource[v] < cost[v]:
            return False
    return True

def resourcesAnimated(g2,t=0):
    res = {'gold':0,'metal':0,'energy':0}
    for u in g2.units[GV.player]:
        if u.state == 'resources':
            if u.stateData and type(u.stateData) == str and u.stateData in res:
                res[u.stateData] += u.resourceGen[u.stateData]
    rect = GV.pygame.Rect(2,WINDOWHEIGHT-52, 80,50)#428
    GV.pygame.draw.rect(GV.DISPLAYSURF, (50,50,50), rect)
    Healthfont = GV.pygame.font.SysFont("arial", 15)
    text = Healthfont.render("%s + %s" % (str(int(Lerp(GV.game.resources[GV.player]['gold'],g2.resources[GV.player]['gold'],t))), res['gold']), 1, (255,255,0))
    GV.DISPLAYSURF.blit(text, (5,WINDOWHEIGHT-50))#430
    text = Healthfont.render("%s + %s" % (str(int(Lerp(GV.game.resources[GV.player]['metal'],g2.resources[GV.player]['metal'],t))), res['metal']), 1, (255,255,255))
    GV.DISPLAYSURF.blit(text, (5,WINDOWHEIGHT-35))#445
    text = Healthfont.render("%s + %s" % (str(int(Lerp(GV.game.resources[GV.player]['energy'],g2.resources[GV.player]['energy'],t))), res['energy']), 1, (0,255,255))
    GV.DISPLAYSURF.blit(text, (5,WINDOWHEIGHT-20))#460

currentStatInfo = None

def statInfo(unit):
    global currentStatInfo
    if unit == currentStatInfo:
        return
    currentStatInfo = unit
    if type(unit) == str:
        unit = Unit('',unit)
    rect = GV.pygame.Rect(endOfBoard_x+5, 5, 180,410)#+GV.offset_x,410+GV.offset_y)
    GV.pygame.draw.rect(GV.DISPLAYSURF, BGCOLOR, rect)
    fontsize = 15
    font = GV.pygame.font.SysFont("arial", fontsize)
    text = [
        unit.name.title(),
        '',
        'Health: %s/%s' % (unit.health, unit.maxHealth),
        'Atttack: %s' % unit.attack,
        'Defense: %s' % unit.defense,
        'Speed: %s' % unit.speed,
        'Range: %s' % unit.range,
    ]
    if len(unit.name.title().split()) > 1:
        text.pop(0)
        text = unit.name.title().split() + text
    if getattr(unit, 'maxPopulation', False):
        text.append('Population: %s/%s' % (unit.population, unit.maxPopulation))
    text.append('Generation:')
    for v in unit.resourceGen:
        text.append('  %s %s'%(unit.resourceGen[v],v))
    text.append('cost')
    cost = UnitDB[unit.name]['cost']
    if 'costly' in unit.abilities:
        cost = copy.copy(cost)
        count = getCount(unit.name)
        for v in cost:
            cost[v] = int(cost[v]*(unit.abilities['costly']**count)//5*5)
    for v in UnitDB[unit.name]['cost']:
        text.append('  %s %s'%(cost[v],v))
    #text = Healthfont.render(t, 1, (0,0,0))
    label = []
    for line in text: 
        label.append(font.render(line, True, (0,0,0)))
    for line in range(len(label)):
        GV.DISPLAYSURF.blit(label[line],(endOfBoard_x+5,5+(line*fontsize)+(2*line)))
    del(unit)

def textToLines(t, n = 14):
    text = []
    TT = t.split()
    i = 0
    while i < len(TT):
        x = ''
        while i < len(TT) and len(x)+len(TT[i]) < n:
            x+= TT[i] + " "
            i+=1
        text.append(x)
    return text

def NameTitle(name):
    return name.title().replace('Of', 'of')

def statInfoTech(tech):#a LOT needs to be done here (remake everything)
    global currentStatInfo
    if 'tech'+tech == currentStatInfo:
        return
    currentStatInfo = 'tech'+tech
    rect = GV.pygame.Rect(endOfBoard_x+5, 5, 180,410)#+GV.offset_x,410+GV.offset_y)
    GV.pygame.draw.rect(GV.DISPLAYSURF, BGCOLOR, rect)
    fontsize = 15
    font = GV.pygame.font.SysFont("arial", fontsize)
    text = []
    name = tech.title().split()
    for i, v in enumerate(name):
        if v == 'Of':
            name[i] = 'of'
    """
    i = 0
    while i < len(name):
        x = ''
        while i < len(name) and len(x)+len(name[i]) < 14:
            x+= name[i] + " "
            i+=1
        text.append(x)
    """
    text.extend(textToLines(NameTitle(tech)))
    text.append('')

    T = TechDB[tech]
    progress = GV.game.progress[GV.player].get(tech) or 0
    text.append('Time: %s/%s' % (progress, T['time']))
    text.append('Cost: %s' % T['cost'])
    text.append('')
    d = {}
    for v in T['ability']:
        if v[0] in ['stat','typeStat','gain ability','typeAbility']:
            if not v[1] in d:
                d[v[1]] = []
            stat = v[2]
            
            if stat == 'maxPopulation':
                stat = 'population'
            elif stat == 'maxHealth':
                continue
            """
            elif v[0] in ['gain ability', 'typeAbility']:
                stat = ''
            """

            if v[0] in ['gain ability', 'typeAbility']:
                d[v[1]].append('  +%s' % stat)
            else:
                d[v[1]].append('  +%s %s' % (v[3], stat))
            #text.append('%s: +%s %s' % (v[1].title(), v[3], v[2]))
            #text.append('%s:' % v[1].title())
            #text.append('  +%s %s' % (v[3], v[2]))
        elif v[0] == 'unlock build':
            text.extend(textToLines('Unlocks %s' % NameTitle(v[2])))
            """
            if not v[1] in d:
                d[v[1]] = []
            d[v[1]].append('  unlocks %s' % v[2])
            """
    for V in d:
        text.append('%s:' % V.title())
        for v2 in d[V]:
            text.append(v2)
    if T['ability'] == []:
        text.append('Discovers new')
        text.append('tech')
    """
    text = [
        unit.name.title(),
        '',
        'Health: %s/%s' % (unit.health, unit.maxHealth),
        'Atttack: %s' % unit.attack,
        'Defense: %s' % unit.defense,
        'Speed: %s' % unit.speed,
        'Range: %s' % unit.range,
    ]
    
    if len(unit.name.title().split()) > 1:
        text.pop(0)
        text = unit.name.title().split() + text
    if getattr(unit, 'maxPopulation', False):
        text.append('Population: %s/%s' % (unit.population, unit.maxPopulation))
    text.append('Generation:')
    for v in unit.resourceGen:
        text.append('  %s %s'%(unit.resourceGen[v],v))
    text.append('cost')
    cost = UnitDB[unit.name]['cost']
    if 'costly' in unit.abilities:
        cost = copy.copy(cost)
        count = getCount(unit.name)
        for v in cost:
            cost[v] = int(cost[v]*(unit.abilities['costly']**count)//5*5)
    for v in UnitDB[unit.name]['cost']:
        text.append('  %s %s'%(cost[v],v))
    """
    smallFont = GV.pygame.font.SysFont("arial", 10, bold=False, italic=True)
    
    #text = Healthfont.render(t, 1, (0,0,0))
    label = []
    for line in text: 
        label.append(font.render(line, True, (0,0,0)))
    for line in range(len(label)):
        GV.DISPLAYSURF.blit(label[line],(endOfBoard_x+5,5+(line*fontsize)+(2*line)))

    if T.get('quote'):
        text2 = textToLines(T.get('quote'), 22)
        label2 = []
        for line in text2: 
            label2.append(smallFont.render(line, True, (0,0,0)))
        for line in range(len(label), len(label)+len(label2)):
            GV.DISPLAYSURF.blit(label2[line-len(label)],(endOfBoard_x+5,60+5+(line*10)+(2*line)))
    

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
grid = []

def cleanUpAfterSelect():
    global moveCircles, selected,stateDataMode, extraButtons, buildHexes, possibleAttacks,possibleHeals,PrevTechHover,CurrentTechHover
    selected = None
    print(selected)
    stateDataMode = None
    GV.highlightSquares = []
    moveCircles = []
    buildHexes = []
    possibleAttacks = []
    possibleHeals = []
    rect = GV.pygame.Rect(endOfBoard_x+5, 5, 180,410)
    GV.pygame.draw.rect(GV.DISPLAYSURF, BGCOLOR, rect)
    for btn in btns:
        btns[btn].deDraw(GV.DISPLAYSURF)
    for v in extraButtons:
        extraButtons[v].deDraw(GV.DISPLAYSURF)

def main(playerCount = None):
    global FPSCLOCK, moveCircles, selected, stateDataMode, extraButtons, buildHexes,possibleAttacks,possibleHeals,counter,grid, buildUnitImages,PrevTechHover,CurrentTechHover
    #GV.pygame.init()
    FPSCLOCK = GV.pygame.time.Clock()
    GV.DISPLAYSURF = GV.pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),RESIZABLE)
    
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    GV.pygame.display.set_caption('Blank')

    GV.DISPLAYSURF.fill(BGCOLOR)

    mouseDown = False

    GV.pygame.mixer.music.load("audio/overview_music.wav")
  
    # Setting the volume
    GV.pygame.mixer.music.set_volume(0.3)
    
    # Start playing the song
    GV.pygame.mixer.music.play(-1)

    start_music = 0
    
    #image = GV.pygame.image.load(r"C:\Users\reega\Downloads\Python\Game\assets\soldier2.png")
    #image2 = GV.pygame.image.load(r"C:\Users\reega\Downloads\Python\Game\assets\town.png")
    """
    g = newGrid(GV.board_x,GV.board_y)
    #makeAreas(g)
    stuff = findStartSpots(g,2)
    print(stuff)
    print(g)
    x = 0
    for v in g:
        y = 0
        for v2 in v:
            if [x,y] in stuff:
                 GV.BoardColors.append(randomGrey())
                 y+=1
                 continue
            if v2:
                GV.BoardColors.append(randomBlue())
            else:
                GV.BoardColors.append(randomGreen())
            y+=1
        x+=1
    """
    for i in range(GV.board_x*GV.board_y):
        GV.BoardColors.append(randomGreen())
        
    drawBoard()
    
    #resources()
    #GV.pygame.draw.line(GV.DISPLAYSURF, (0,255,255), (20+GV.offset_x,20+GV.offset_y),(61+GV.offset_x,20+GV.offset_y),10)

    #for btn in btns:
        #btns[btn].draw(GV.DISPLAYSURF)
    
    n = Network()
    GV.player = int(n.getP())
    if playerCount == 1:
        n.send("SOLO")
    
    run = True

    counter = 0

    JustResize = 0
    animateCounter = animateTime*-2
    newGame = None
    
    while run: # main GV.game loop
        #mouseClicked = False

        #GV.DISPLAYSURF.fill(BGCOLOR)#Draw window
        try:
            R = n.send("get")
            if R != "Nothing" and R != None: #and type(r) != str:
                #print("HERE")
                try:
                    print("Collecting:")
                    r = GameMaker(R)
                except Exception as e:
                    print(str(e))
                    
                print("IT WAS DIFFERENT")
                print(vars(r))
                if roundEnd(GV.game,r):
                    print("I think the round ended.....")
                    end_of_round_beeps.play()
                    animateCounter = int(counter)
                    if r:
                        if r.ready:
                            newGame = r
                            changeAnimateSpeed(GV.game,newGame)
                            animationGrid(GV.game,newGame)
                            print(animateTime)
                        else:
                            GV.game = r
                else:
                    #print("stuff", roundEnd(GV.game,r))
                    GV.game = r
                    newGame = r#######
                    #print("GAME", vars(GV.game))
                    #print("newGAME", vars(newGame))
                    #print("R", vars(r))
            elif type(R) == str:
                #print("HERE2", r)
                pass#print(r)
        except Exception as e:
            run = False
            print("Couldn't get GV.game",e)
            break
        
        counter += 1
        if counter-animateCounter <= animateTime:
            animateBoard(GV.game, newGame, counter-animateCounter)
        elif counter%10 == 0:
            #print("MORE ", vars(GV.game))
            if newGame:
                #print("Even MORE", vars(newGame))
                GV.game = newGame
            #print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            #print(vars(GV.game))
            drawBoard()
            resources()
        
        for event in GV.pygame.event.get():
            if counter-animateCounter <= animateTime:#Don't continue to watch events
                break
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                if serverprocess:
                    serverprocess.kill()
                GV.pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == 109: # 'm' Key
                    GV.pygame.mixer.music.pause()
                elif event.key == 110: # 'n' Key
                    GV.pygame.mixer.music.unpause()
            elif event.type == VIDEORESIZE and counter - JustResize > 20:
                JustResize = counter
                if event.w-230 > event.h-65: #Wide rectangle
                    GV.block_size = (event.h-65)//GV.board_y
                else:
                    GV.block_size = (event.w-65)//GV.board_x
                print('blocksize',GV.block_size)
                GV.playerUnitImages = {} #To reset all unit images
                buildUnitImages = {}
                updateSelf()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                if selected and mousey > 410+GV.offset_y and stateDataMode != 'build2':
                    if 'build' in selected.possibleStates:#If they are able to build
                        unfound = True
                        for btn in extraButtons:
                            if extraButtons[btn].click(GV.pygame.mouse.get_pos()):#If one of the unit options is clicked
                                statInfo(btn)
                                unfound = False
                                break
                        if unfound:
                            statInfo(selected)
                if stateDataMode == 'research':
                    unfound = True
                    for btn in currentTechButtons:
                        if btn.click(GV.pygame.mouse.get_pos()):
                            if btn.name != CurrentTechHover:
                                PrevTechHover = str(CurrentTechHover)
                                CurrentTechHover = btn.name
                                drawBoard()
                            statInfoTech(btn.name)
                            unfound = False
                            break
                    if unfound:
                        PrevTechHover = str(CurrentTechHover)
                        CurrentTechHover = False
                        if PrevTechHover != "False":
                            drawBoard()
                            statInfo(selected)
                        
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseDown = False  
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                x,y = gridMouse(mousex, mousey, GV.block_size,GV.offset_x,GV.offset_y)
                print(x,y)
                print('datamode', stateDataMode)
                print('selected', selected)
                if stateDataMode == 'move':
                    selected.state = None
                    if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:

                        PlaySoundByUnit(selected, stateDataMode)

                        n.send(convertToStr(selected,'move',[x,y]))
                        selected.stateData = [x,y]
                        selected.state = 'move'
                    cleanUpAfterSelect()
                    #Here is to sumbit to server
                    drawBoard()
                if stateDataMode == 'attack':
                    selected.state = None
                    if GV.game.getAnyUnitFromPos(x,y):
                        
                        PlaySoundByUnit(selected, stateDataMode)

                        n.send(convertToStr(selected,'attack',GV.game.getAnyUnitFromPos(x,y)))
                        selected.stateData = GV.game.getAnyUnitFromPos(x,y)
                        selected.state = 'attack'
                    cleanUpAfterSelect()
                    #Here is to sumbit to server
                    drawBoard()
                elif stateDataMode == 'resources':
                    selected.state = None
                    for btn in resourceBtns:
                        if resourceBtns[btn].click(GV.pygame.mouse.get_pos()):#If one of the resources is clicked
                            n.send(convertToStr(selected,'resources',btn))
                            selected.stateData = btn
                            selected.state = 'resources'

                            resource_audio[btn].play()

                        resourceBtns[btn].deDraw(GV.DISPLAYSURF)
                    cleanUpAfterSelect()
                    #Here is to sumbit to server
                    drawBoard()
                elif stateDataMode == 'build':
                    offclick = True
                    for btn in extraButtons:
                        if extraButtons[btn].click(GV.pygame.mouse.get_pos()):#If one of the unit options is clicked
                            selected.stateData = [btn]
                            stateDataMode = 'build2'
                            statInfo(btn)
                            for v in extraButtons:
                                extraButtons[v].deDraw(GV.DISPLAYSURF)
                            extraButtons = {}
                            buildHexes = getRangeCircles(selected, built = btn)
                            drawBoard()
                            offclick = False
                            break
                    if offclick:
                        selected.state = None
                        cleanUpAfterSelect()
                        for v in extraButtons:
                            extraButtons[v].deDraw(GV.DISPLAYSURF)
                        extraButtons = {}
                        drawBoard()
                elif stateDataMode == 'build2':
                    selected.state = None
                    if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:
                        construction.play()
                        selected.stateData.insert(0,[x,y])
                        n.send(convertToStr(selected,'build',selected.stateData))
                        selected.state = 'build'
                    cleanUpAfterSelect()
                    #Here is to sumbit to server
                    drawBoard()
                elif stateDataMode == 'research':
                    print('RESEARCH CLICK')
                    selected.state = None

                    play_time = GV.pygame.mixer.music.get_pos()
                    GV.pygame.mixer.music.load("audio/overview_music.mp3")
                    GV.pygame.mixer.music.set_volume(0.3)
                    start_music = (start_music + play_time/1000.0) % 32
                    GV.pygame.mixer.music.play(-1, start_music)


                    print('currentTechButtons',currentTechButtons)
                    for btn in currentTechButtons:
                        if btn.click(GV.pygame.mouse.get_pos()):
                            print('ONE OF THEM WAS CLICKKKEDD!!')

                            research_selected_audio.play()

                            selected.stateData = btn.name
                            n.send(convertToStr(selected,'research',selected.stateData))
                            selected.state = 'research'
                            break
                    cleanUpAfterSelect()
                    drawBoard()   
                elif selected:
                    for btn in btns:
                        if btns[btn].click(GV.pygame.mouse.get_pos()):#If button clicked, set state of unit
                            selected.state = btn
                            selected.stateData = None
                            stateDataMode = btn
                            for btn2 in btns:
                                if btn2 != btn:
                                    btns[btn2].deDraw(GV.DISPLAYSURF)
                            if stateDataMode == 'resources':
                                for v in resourceBtns:
                                    if v in selected.resourceGen:
                                        if selected.resourceGen[v] != 0:
                                            resourceBtns[v].draw(GV.DISPLAYSURF)
                            if stateDataMode == 'build':
                                i = 0
                                posBuilds = getattr(selected,'possiblebuilds',0) or UnitDB[selected.name].get('possibleBuilds') or []
                                for v in posBuilds:
                                    if not checkIfAffordable(selected, v):
                                        btnColor = errorColor
                                    if getattr(selected, 'maxPopulation', False):
                                        if selected.population >= selected.maxPopulation:
                                            btnColor = otherColor
                                    b = Button("", GV.offset_x+(40+1)*i, endOfBoard_y+10, btnColor,BLACK,18,(40,40))
                                    b.draw(GV.DISPLAYSURF)
                                    img = getImage(v, GV.player, buildUnitImages, 40)
                                    #buildUnitImages
                                    #img = GV.pygame.image.load("assets/%s.png" % v)
                                    #img = GV.pygame.transform.scale(img, (40, 40))
                                    GV.DISPLAYSURF.blit(img,(GV.offset_x+(GV.block_size+1)*i, endOfBoard_y+10))
                                    extraButtons[v] = b
                                    i+=1
                            drawBoard()
                    if 'build' in selected.possibleStates:#If they are able to build
                        for btn in extraButtons:
                            if extraButtons[btn].click(GV.pygame.mouse.get_pos()):#If one of the unit options is clicked
                                selected.stateData = [btn]
                                stateDataMode = 'build2'
                                statInfo(btn)
                                for v in extraButtons:
                                    extraButtons[v].deDraw(GV.DISPLAYSURF)
                                extraButtons = {}
                                moveCircles = []
                                possibleAttacks = []
                                possibleHeals = []
                                buildHexes = getRangeCircles(selected, built = btn)
                                offclick = False
                                drawBoard()
                                break
                    if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:
                        if [x,y] in moveCircles: #A move was clicked
                            selected.stateData = [x,y]
                            selected.state = 'move'

                            PlaySoundByUnit(selected, "move")

                            n.send(convertToStr(selected,'move',[x,y]))
                            cleanUpAfterSelect()
                            print(selected)
                            #Here is to sumbit to server
                        elif [x,y] in possibleAttacks:
                            selected.stateData = GV.game.getAnyUnitFromPos(x,y)
                            selected.state = 'attack'

                            PlaySoundByUnit(selected, "attack")

                            n.send(convertToStr(selected,'attack',selected.stateData))
                            cleanUpAfterSelect()
                            #Here is to sumbit to server
                        elif [x,y] in possibleHeals:
                            selected.stateData = GV.game.getAnyUnitFromPos(x,y)
                            selected.state = 'heal'
                            n.send(convertToStr(selected,'heal',selected.stateData))
                            cleanUpAfterSelect()
                        else:
                            newSelected = GV.game.getUnitFromPos(GV.player,x,y)
                            if newSelected == selected:
                                print('the same was clicked')
                                if 'research' in newSelected.possibleStates:
                                    stateDataMode = 'research'

                                    play_time = GV.pygame.mixer.music.get_pos()
                                    GV.pygame.mixer.music.load("audio/lab_music.mp3")
                                    GV.pygame.mixer.music.set_volume(0.3)
                                    start_music = (start_music + play_time/1000.0) % 32
                                    GV.pygame.mixer.music.play(-1, start_music)

                                    drawBoard()
                                    #selected.stateData = GV.game.getAnyUnitFromPos(x,y)
                                    #selected.state = 'attack'
                            #selected = newSelected#GV.game.getUnitFromPos(GV.player,x,y)
                            elif newSelected:#Unit is clicked
                                print('a unit was clicked')
                                selected = newSelected

                                PlaySoundByUnit(selected, "affirmative")

                                GV.highlightSquares = [[x,y]]
                                moveCircles = getMoveCircles(selected)
                                possibleAttacks = getAttacks(selected)
                                possibleHeals = getHeals(selected)
                                statInfo(selected)
                                for btn in btns:
                                    if btn in selected.possibleStates:
                                        btns[btn].draw(GV.DISPLAYSURF)
                                    else:
                                        btns[btn].deDraw(GV.DISPLAYSURF)
                                for v in extraButtons:
                                    extraButtons[v].deDraw(GV.DISPLAYSURF)
                                if 'build' in selected.possibleStates: #Show unit builds on bottom
                                    i = 0
                                    posBuilds = getattr(selected,'possiblebuilds',0) or UnitDB[selected.name].get('possibleBuilds') or []
                                    for v in posBuilds:
                                        btnColor = (230,230,230)
                                        if not checkIfAffordable(selected, v):
                                            btnColor = errorColor
                                        if type(selected.stateData) == list and selected.stateData[1] == v:
                                            btnColor = goodColor
                                        elif getattr(selected, 'maxPopulation', False):
                                            if selected.population >= selected.maxPopulation:
                                                btnColor = otherColor
                                        b = Button("", GV.offset_x+(40+1)*i, endOfBoard_y+10, btnColor,BLACK,18,(40,40))
                                        b.draw(GV.DISPLAYSURF)
                                        img = getImage(v, GV.player, buildUnitImages, 40)
                                        #img = GV.pygame.image.load("assets/%s.png" % v)
                                        #img = GV.pygame.transform.scale(img, (40, 40))
                                        GV.DISPLAYSURF.blit(img,(GV.offset_x+(40+1)*i, endOfBoard_y+10))
                                        extraButtons[v] = b
                                        i+=1
                                     
                            else:
                                cleanUpAfterSelect()
                        drawBoard()
                elif event.button == 1:
                    if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:
                        selected = GV.game.getUnitFromPos(GV.player,x,y)
                        if selected:#When unit clicked
                            
                            PlaySoundByUnit(selected, "affirmative")

                            print(vars(selected))
                            GV.highlightSquares = [[x,y]]
                            moveCircles = getMoveCircles(selected)
                            possibleAttacks = getAttacks(selected)
                            possibleHeals = getHeals(selected)
                            statInfo(selected)
                            for btn in btns:
                                if btn in selected.possibleStates:
                                    btns[btn].draw(GV.DISPLAYSURF)
                                else:
                                    btns[btn].deDraw(GV.DISPLAYSURF)
                            if 'build' in selected.possibleStates: #Show things on bottom
                                i = 0
                                posBuilds = getattr(selected,'possiblebuilds',0) or UnitDB[selected.name].get('possibleBuilds') or []
                                for v in posBuilds:
                                    btnColor = (230,230,230)
                                    if not checkIfAffordable(selected, v):
                                        btnColor = errorColor
                                    if type(selected.stateData) == list and len(selected.stateData) > 1 and selected.stateData[1] == v:
                                        btnColor = goodColor
                                    elif getattr(selected, 'maxPopulation', False):
                                        if selected.population >= selected.maxPopulation:
                                            btnColor = otherColor
                                    b = Button("", GV.offset_x+(40+1)*i, endOfBoard_y+10, btnColor,BLACK,18,(40,40))
                                    b.draw(GV.DISPLAYSURF)
                                    img = getImage(v, GV.player, buildUnitImages, 40)
                                    #img = GV.pygame.image.load("assets/%s.png" % v)
                                    #img = GV.pygame.transform.scale(img, (40, 40))
                                    GV.DISPLAYSURF.blit(img,(GV.offset_x+(40+1)*i, endOfBoard_y+10))#(115+41*i, 430)
                                    extraButtons[v] = b
                                    i+=1
                        else:
                            for btn in btns:
                                btns[btn].deDraw(GV.DISPLAYSURF)
                        drawBoard()
                elif event.button == 3:
                    n.send('done')
                if event.button == 1:
                     if DoneButton.click(GV.pygame.mouse.get_pos()):
                         DoneButton.color = (30,120,30)
                         DoneButton.draw(GV.DISPLAYSURF)
                         n.send('done')
                mouseDown = True
        GV.pygame.display.update()
        FPSCLOCK.tick(FPS)

def menu_screen():
    global serverprocess
    GV.pygame.init()
    run = True
    Cont = True
    clock = GV.pygame.time.Clock()
    GV.DISPLAYSURF = GV.pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    GV.pygame.display.set_caption('Tussel')
    box = InputBox(77, 33, 80, 20)
    font = GV.pygame.font.SysFont("arial", 40)

    launchServer = Button("Start Server", 10, 60, BLACK, WHITE,18,(150,30))
    serverRunning = False
    
    GV.pygame.mixer.music.load("audio/menu_music.mp3")
    GV.pygame.mixer.music.set_volume(0.5)
    GV.pygame.mixer.music.play(-1)

    while run:
        
        GV.DISPLAYSURF.fill((128, 128, 128))
        font = GV.pygame.font.SysFont("arial", 14)
        #text = font.render("Click to Play!", 1, (255,0,0))
        #GV.DISPLAYSURF.blit(text, (200,250))


        solo = Button("Solo", 200, 100, BLACK, WHITE,40,(200,70))
        solo.draw(GV.DISPLAYSURF)
        multiplayer = Button("Multiplayer", 200, 200,  BLACK, WHITE,40,(200,70))
        multiplayer.draw(GV.DISPLAYSURF)
        launchServer.draw(GV.DISPLAYSURF)
        box.update()
        box.draw(GV.DISPLAYSURF)

        line1 = font.render("Current IP: %s" % network.ip, True, (0,0,0))
        GV.DISPLAYSURF.blit(line1,(10,10))
        line1 = font.render("Server IP:", True, (0,0,0))
        GV.DISPLAYSURF.blit(line1,(10,35))


        for event in GV.pygame.event.get():
            box.handle_event(event)
            if event.type == GV.pygame.QUIT:
                if serverprocess:
                    serverprocess.kill()
                GV.pygame.quit()
                run = False
                Cont = False
            if event.type == GV.pygame.MOUSEBUTTONDOWN:
                if multiplayer.click(event.pos):
                    main()
                    run = False
                elif solo.click(event.pos):
                    main(1)
                    run = False
                elif launchServer.click(event.pos):
                    serverRunning = True
                    launchServer.text = "Server Running"
                    serverprocess = subprocess.Popen(['python', 'server.py'])
            if event.type == GV.pygame.KEYDOWN:
                if event.key == GV.pygame.K_RETURN:
                    if network.checkIfIP(box.text):
                        box.color = GREEN
                        network.serverIP = box.text
                    else:
                        box.color = RED

        
        GV.pygame.display.update()
        clock.tick(30)
    return Cont
    
Continue = True

if __name__ == '__main__':
    while Continue:
        Continue = menu_screen()
