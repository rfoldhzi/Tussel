from contextlib import nullcontext
import  sys, random,math,pathlib,os,pickle,copy,subprocess,signal,time, copy
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
import BoardFunctions as BF

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
tech_error_audio = GV.pygame.mixer.Sound("audio/error_beep.wav")

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
GV.cloudMode = "halo"#sight, poly, halo, clear

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

#GV.BGCOLOR = LIGHTGREY

GV.StateColors = {
    'attack': (255,0,0),
    'move': (0,255,255),
    'resources': (255,255,0),
    'build':(100,50,0),
    'heal':(255,255,255),
    'research':(66, 135, 245),
    'transport':(50,255,50),
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
        GV.pygame.draw.rect(win, GV.BGCOLOR, (self.x-1, self.y-1, self.width+2, self.height+2))
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
    elif state == 'transport':
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

def randomBlueWeighted(x):
    #b = random.randint(180 - x * 10,210 - x * 10)
    #b = max(0,200 - x * 15)
    base = 13
    sub = ((base)*(base+1))/2 - ((base - x)*((base - x) + 1))/2
    print("SUBB",sub,x)
    print("(base)+(base+1))/2",((base)+(base+1))/2,"((base - x)*((base - x) + 1))/2",((base - x)*((base - x) + 1))/2)
    if x > base:
        sub = ((base)*(base+1))/2 + x - base
    sub = int(sub)
    b = max(0,random.randint(180 - sub,180 - sub))
    #b = int (((random.randint(180,210) / x**0.5)+random.randint(180,210))/2)
    #return (int(b*.2), int(b*.625),b)
    return (round(b*random.random()*.1+.1), round(b*(random.random()*.125+.625)),b)

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
                                water = GV.Grid[y][x]
                                if (water == (unit.type == 'boat')) or unit.type == "aircraft":
                                    newSpaces.append([x,y])
            spaces += newSpaces
        spaces.pop(0)
    else:
        for x in range(unit.position[0]-sp, unit.position[0]+1+sp):
            for y in range(unit.position[1]-sp, unit.position[1]+1+sp):
                if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:#If within board:
                    if GV.game.getAnyUnitFromPos(x,y) == None:
                        water = GV.Grid[y][x]
                        if (water == (unit.type == 'boat')) or unit.type == "aircraft":
                            spaces.append([x,y])
    
    return spaces

def getTransportSpots(unit):
    if not 'move' in unit.possibleStates:
        return []
    sp = unit.speed
    spaces = []
    for x in range(unit.position[0]-sp, unit.position[0]+1+sp):
        for y in range(unit.position[1]-sp, unit.position[1]+1+sp):
            if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:#If within board:
                unit2 = GV.game.getUnitFromPos(GV.player,x,y)#Switch to unit on team
                if unit2:
                    if ("transport" in unit2.abilities):
                        if unit.type in unit2.abilities['transport']:
                            if unit2.population >= unit2.maxPopulation:
                                continue
                            #Valid Transport
                            spaces.append([x,y])
    
    return spaces

def getRangeCircles(unit, anyBlock = False, built = False):#Could be more effiecint
    sp = unit.range
    spaces = []
    for x in range(unit.position[0]-sp, unit.position[0]+1+sp):
        for y in range(unit.position[1]-sp, unit.position[1]+1+sp):
            if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:#If within board:
                if anyBlock or GV.game.getAnyUnitFromPos(x,y) == None:
                    water = GV.Grid[y][x]
                    if built:
                        t = UnitDB[built].get('type') or 0
                        if (water == (t == 'boat')) or t == "aircraft":
                            spaces.append([x,y])
                    else:
                        if anyBlock or (not water):
                            spaces.append([x,y])
    return spaces

def isNextToWater(pos):
    xs = [1,0,-1,0]
    ys = [0,1,0,-1]
    for i in range(4):
        x = pos[0]+xs[i]
        y = pos[1]+ys[i]
        if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:
                if GV.Grid[y][x]:
                    return True
    return False

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

AIcolors = [(150,150,150),(50,50,50),(230,230,230),(81, 120, 56), (80, 55, 122), (102, 57, 57),
            (84, 156, 152),(158, 101, 36),(60, 112, 158),(139, 68, 148),(140, 136, 55),(30, 92, 77) ]


def animateUnit(unit1, unit2,t,specfic_player):
    unit = unit1
    if not unit1:
        unit = unit2
    x = unit.position[0]
    y = unit.position[1]
    image = None
    if GV.animateGrid[y][x]:
        return

    image = BF.getImage(unit.name, specfic_player)

    default = True
    if not unit1:
        parent = GV.game.getUnitFromID(unit2.parent)
        if parent:
            default = False
            x2,y2 = parent.position
            start = (x2*(GV.block_size+1)+GV.offset_x-1, y2*(GV.block_size+1)+GV.offset_y-1)
            end = (x*(GV.block_size+1)+GV.offset_x-1, y*(GV.block_size+1)+GV.offset_y-1)
            Pos = intPoint(LerpPoint(start, end, t/GV.animateTime))
            GV.DISPLAYSURF.blit(image,Pos)
    elif unit1.position != unit2.position:
        default = False
        start = (x*(GV.block_size+1)+GV.offset_x-1, y*(GV.block_size+1)+GV.offset_y-1)
        end = (unit2.position[0]*(GV.block_size+1)+GV.offset_x-1, unit2.position[1]*(GV.block_size+1)+GV.offset_y-1)
        Pos = intPoint(LerpPoint(start, end, t/GV.animateTime))
        GV.DISPLAYSURF.blit(image,Pos)
    if default:#No move
        GV.DISPLAYSURF.blit(image,(x*(GV.block_size+1)+GV.offset_x-1, y*(GV.block_size+1)+GV.offset_y-1))
        T = str(unit.health)
        Healthfont = GV.pygame.font.SysFont("arial", 15)
        text = Healthfont.render(T, 1, WHITE)
        if unit1 and unit2:
            if unit2.health < unit1.health:
                T = str(int(Lerp(unit1.health, unit2.health, t/GV.animateTime)))
                text = Healthfont.render(T, 1, RED)
            elif unit2.health > unit1.health:
                T = str(int(Lerp(unit1.health, unit2.health, t/GV.animateTime)))
                text = Healthfont.render(T, 1, WHITE)
            elif unit1 == unit2:
                T = str(int(Lerp(unit1.health, 0, t/GV.animateTime)))
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
        GV.DISPLAYSURF.blit(GV.RedX,(x*(GV.block_size+1)+GV.offset_x-1, y*(GV.block_size+1)+GV.offset_y-1))


GV.animateTime = 20


GV.board_x = 10
GV.board_y = 10

endOfBoard_x = (GV.block_size+1)*GV.board_x+GV.offset_x#525
endOfBoard_y = (GV.block_size+1)*GV.board_y+GV.offset_y#420

WINDOWWIDTH = 640#GV.offset_x*2+(GV.block_size+1)*GV.board_x#640
WINDOWHEIGHT = 480#GV.offset_y+60+(GV.block_size+1)*GV.board_y#480
print('x&y',WINDOWWIDTH,WINDOWHEIGHT)

GV.highlightSquares = []
#GV.BoardColors = []
GV.CloudColors = []
moveCircles = []
transportSpots = []
possibleAttacks = []
possibleHeals = []
buildHexes = []
#GV.Grid = []
GV.cloudGrid = []
GV.explorationGrid = []
GV.animateGrid = []

blueCircle = GV.pygame.image.load("assets/MoveCircle.png")
greenCircle = GV.pygame.image.load("assets/TransportCircle.png")
OrangeHex = GV.pygame.image.load("assets/BuildHex.png")
RedX = GV.RedX#GV.pygame.image.load("assets/AttackX.png")
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


from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT    
import ctypes

def getWindowRectangle(): #Use rect.top, rect.left, rect.bottom, rect.right
        # get our window ID:
    hwnd = GV.pygame.display.get_wm_info()["window"]

    # Jump through all the ctypes hoops:
    prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
    paramflags = (1, "hwnd"), (2, "lprect")

    GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)

    # finally get our data!
    rect = GetWindowRect(hwnd)
    return rect

def getMonitorSize():

    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

    return screensize

from ctypes import windll

def moveWin(x, y):
    # the handle to the window
    hwnd = GV.pygame.display.get_wm_info()['window']

    # user32.MoveWindow also recieves a new size for the window
    w, h = GV.pygame.display.get_surface().get_size()

    windll.user32.MoveWindow(hwnd, x, y, w, h, False)

def updateSelf():
    global endOfBoard_x, endOfBoard_y, WINDOWWIDTH, WINDOWHEIGHT, DoneButton,blueCircle, greenCircle ,OrangeHex,RedX,GreenT,Beaker,currentTechMenu
    print('blocksize',GV.block_size)
    GV.board_x = GV.game.width
    GV.board_y = GV.game.height
    GV.cloudMode = GV.game.mode

    if GV.game.ai > 0:
        j = 0
        for i in range(len(GV.game.units)-GV.game.ai,len(GV.game.units)):
            GV.playerColors.insert(i, AIcolors[j])
            j+=1
    minBoardSize = 7
    endOfBoard_x = (GV.block_size+1)*(max(GV.board_x_end-GV.board_x_start, minBoardSize))+GV.offset_x#525
    endOfBoard_y = (GV.block_size+1)*(max(GV.board_y_end-GV.board_y_start, minBoardSize))+GV.offset_y#420
    #endOfBoard_x = (GV.block_size+1)*(GV.board_x_end-GV.board_x_start)+GV.offset_x#525
    #endOfBoard_y = (GV.block_size+1)*(GV.board_y_end-GV.board_y_start)+GV.offset_y#420

    WINDOWWIDTH = GV.offset_x + endOfBoard_x
    WINDOWHEIGHT = 60 + endOfBoard_y
    #WINDOWWIDTH = GV.offset_x*2+(GV.block_size+1)*(GV.board_x_end-GV.board_x_start)#640
    #WINDOWHEIGHT = GV.offset_y+60+(GV.block_size+1)*(GV.board_y_end-GV.board_y_start)

    monitorSize = getMonitorSize()

    if WINDOWHEIGHT > monitorSize[1] - 70: #If board grows larger than screen, shrink block size so it fits again
        GV.block_size = int((monitorSize[1] - 70 -GV.offset_y-60)/max(GV.board_y_end-GV.board_y_start, minBoardSize)) - 1
        endOfBoard_x = (GV.block_size+1)*(max(GV.board_x_end-GV.board_x_start, minBoardSize))+GV.offset_x#525
        endOfBoard_y = (GV.block_size+1)*(max(GV.board_y_end-GV.board_y_start, minBoardSize))+GV.offset_y#420
        WINDOWWIDTH = GV.offset_x + endOfBoard_x
        WINDOWHEIGHT = 60 + endOfBoard_y
        GV.playerUnitImages = {} #To reset all unit images

    if WINDOWWIDTH > monitorSize[0]: #If board grows larger than screen, shrink block size so it fits again
        GV.block_size = int((monitorSize[0] - GV.offset_x * 2)/max(GV.board_x_end-GV.board_x_start, minBoardSize)) - 1
        endOfBoard_x = (GV.block_size+1)*(max(GV.board_x_end-GV.board_x_start, minBoardSize))+GV.offset_x#525
        endOfBoard_y = (GV.block_size+1)*(max(GV.board_y_end-GV.board_y_start, minBoardSize))+GV.offset_y#420
        WINDOWWIDTH = GV.offset_x + endOfBoard_x
        WINDOWHEIGHT = 60 + endOfBoard_y
        GV.playerUnitImages = {}

    #Ensure the window doesn't grow below bottom of screen
    rect = getWindowRectangle()
    
    if rect.top + WINDOWHEIGHT > monitorSize[1] - 70: # - 70  is for taskbar at bottom of screen
        moveWin(rect.left, monitorSize[1] - WINDOWHEIGHT - 70)
        rect = getWindowRectangle()
        if rect.top < 0:
            moveWin(rect.left, 0)
    
    if rect.right > monitorSize[0]: # - 70  is for taskbar at bottom of screen
        moveWin(monitorSize[0] - WINDOWWIDTH, rect.top)
        rect = getWindowRectangle()
        if rect.left < 0:
            moveWin(0, rect.top)


    print("Window",WINDOWWIDTH,WINDOWWIDTH)

    GV.DISPLAYSURF = GV.pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),RESIZABLE)
    GV.DISPLAYSURF.fill(GV.BGCOLOR)
    DoneButton = Button("Done", endOfBoard_x, endOfBoard_y+10, (50,200,50),BLACK,22,(60,40))

    blueCircle = GV.pygame.image.load("assets/MoveCircle.png")
    greenCircle = GV.pygame.image.load("assets/TransportCircle.png")
    OrangeHex = GV.pygame.image.load("assets/BuildHex.png")
    GV.RedX = GV.pygame.image.load("assets/AttackX.png")
    GreenT = GV.pygame.image.load("assets/HealT.png")
    Beaker = GV.pygame.image.load("assets/Beaker.png")
    blueCircle = GV.pygame.transform.scale(blueCircle, (GV.block_size, GV.block_size))
    greenCircle = GV.pygame.transform.scale(greenCircle, (GV.block_size, GV.block_size))
    OrangeHex = GV.pygame.transform.scale(OrangeHex, (GV.block_size, GV.block_size))
    GV.RedX = GV.pygame.transform.scale(GV.RedX, (GV.block_size, GV.block_size))
    GreenT = GV.pygame.transform.scale(GreenT, (GV.block_size, GV.block_size))
    Beaker = GV.pygame.transform.scale(Beaker, (GV.block_size, GV.block_size))

    currentTechMenu = []
    
    GV.Grid = intToList(GV.game.intGrid, GV.board_x)
    #print(Grid)
    
    if len(GV.cloudGrid) == GV.board_y and len(GV.cloudGrid[0]) == GV.board_x:
        return

    GV.cloudGrid = []
    for y in range(GV.board_y):
        l = []
        for x in range(GV.board_x):
            l.append(True)
        GV.cloudGrid.append(l)
        
    if GV.cloudMode == "halo": 
        GV.explorationGrid = []
        for y in range(GV.board_y):
            l = []
            for x in range(GV.board_x):
                l.append(True)
            GV.explorationGrid.append(l)
    
    #Creates list to store the depth of water. Higher depth values == deeper water
    #Depth is calculated by how far water is to land (doesn't measure corners)
    depthMap = []
    for v in GV.Grid: #This part sets all land to 0 and water to -1
        list = []
        for v2 in v:
            if v2:
                list.append(-1)
            else:
                list.append(0)
        depthMap.append(list)
    
    xList = (-1,1,0,0)
    yList = (0,0,-1,1)
    def lowestNextTo(x,y): #Calculates which adjecent tile has lowest depth value (excludes tiles that are -1)
        lowest = -1
        for i in range(len(xList)):
            if x+xList[i] >= 0 and x+xList[i] < len(depthMap) and y+yList[i] >= 0 and y+yList[i] < len(depthMap[0]):
                if depthMap[x+xList[i]][y+yList[i]] != -1:
                    if depthMap[x+xList[i]][y+yList[i]] < lowest:
                        lowest = depthMap[x+xList[i]][y+yList[i]]
                if lowest == -1:
                    lowest = depthMap[x+xList[i]][y+yList[i]]
        return lowest

    keepGoing = True
    while keepGoing: #Continually loops through until every water tile is assigned a depth value
        print(depthMap)
        keepGoing = False
        x = 0
        newDepthMap = copy.deepcopy(depthMap)
        
        for list in depthMap:
            y = 0
            for n in list:
                if n == -1:
                    keepGoing = True
                    lowest = lowestNextTo(x,y)
                    if lowest != -1:
                        newDepthMap[x][y] = lowest + 1
                y += 1
            x += 1
        depthMap = newDepthMap
    print("The final depthmap",depthMap)

    GV.BoardColors = []
    GV.CloudColors = []
    y = 0
    for v in GV.Grid:
        x = 0
        for v2 in v:
            if v2:
                #GV.BoardColors.append(randomBlue())
                GV.BoardColors.append(randomBlueWeighted(depthMap[y][x]))
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
    for v in GV.Grid:
        for v2 in v:
            if GV.cloudMode == "halo": 
                GV.CloudColors.append(randomDark())
            else:
                GV.CloudColors.append(randomWhite())

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
                if u.state == "move": #This is for when a unit boards a transporter
                    possibleTransport = g2.getUnitFromPos(i,u.stateData[0],u.stateData[1])
                    if possibleTransport:
                        if g2.checkIfUnitTransported(u, possibleTransport):
                            l.append([u.position,possibleTransport.position])
                            continue
                l.append([u.position])#Unit destroyed
    for i in g2.units:
        for u2 in g2.units[i]:
            u = GV.game.getUnitFromID(u2.UnitID)
            if not u:
                parent = GV.game.getUnitFromID(u2.parent)
                if hasattr(u2, "transporter"): #For when a transporter drops off a unit
                    parent = GV.game.getUnitFromID(u2.transporter)
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
    #GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BGCOLOR, rect)
    BF.drawAnimateGrid()#drawGrid()
    resourcesAnimated(g2,t/GV.animateTime)

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
                        #BF.drawLine((45, 150, 138),u.position,u.stateData)
                    else:
                        color = (0,255,255)
                        print("more colro", color)
                        spots = (u.position,u.stateData)
                        #BF.drawLine((0,255,255),u.position,u.stateData)
                elif u.state == 'attack':
                    pos = None
                    if type(u.stateData) == dict:
                        pos = u.stateData['position']
                    else:
                        pos = u.stateData.position
                    if checkRange(u,pos) > u.range:
                        color = (148, 55, 49)
                        spots = (u.position,pos)
                        #BF.drawLine((148, 55, 49),u.position,pos)
                    else:
                        color = (255,0,0)
                        spots = (u.position,pos)
                        #BF.drawLine((255,0,0),u.position,pos)
                elif u.state == 'heal':
                    pos = None
                    if type(u.stateData) == dict:
                        pos = u.stateData['position']
                    else:
                        pos = u.stateData.position
                    if checkRange(u,pos) > u.range:
                        color = (150, 150, 150)
                        spots = (u.position,pos)
                        #BF.drawLine((150, 150, 150),u.position,pos)
                    else:
                        color = (255,255,255)
                        spots = (u.position,pos)
                        #BF.drawLine((255,255,255),u.position,pos)
                elif u.state == 'build':
                    print('BUILD BUILD BIT')
                    if len(u.stateData) == 2:
                        if checkRange(u,u.stateData[0]) > u.range:
                            color = (110, 106, 46)
                            spots = (u.position,u.stateData[0])
                            #BF.drawLine((110, 106, 46),u.position,u.stateData[0])
                        else:
                            color = (255,170,0)
                            print("more colro", color)
                            spots = (u.position,u.stateData[0])
                            #BF.drawLine((255,170,0),u.position,u.stateData[0])
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
                    if spots[0][0] < GV.board_x_start or GV.board_x_end <= spots[0][0] or spots[0][1] < GV.board_y_start or GV.board_y_end <= spots[0][1]:
                        if spots[1][0] < GV.board_x_start or GV.board_x_end <= spots[1][0] or spots[1][1] < GV.board_y_start or GV.board_y_end <= spots[1][1]:
                            continue
                    BF.drawLine(color,spots[0],spots[1])
                    
    for i in GV.game.units:
        for u in GV.game.units[i]:
            u2 = g2.getUnitFromID(u.UnitID)
            if u2:
                BF.animateUnit(u,u2,t,i) #Unit changed
            else:
                if u.state == "move": #Transport units are destroyed, but are actually moving. 
                                      #We make the unit2 equal to transporter to move the unit into it
                    possibleTransport = g2.getUnitFromPos(i,u.stateData[0],u.stateData[1])
                    if possibleTransport:
                        if g2.checkIfUnitTransported(u, possibleTransport):
                            BF.animateUnit(u,possibleTransport,t,i)
                            continue
                BF.animateUnit(u,u,t,i)#Unit destroyed
    for i in g2.units:
        for u2 in g2.units[i]:
            u = GV.game.getUnitFromID(u2.UnitID)
            if not u:
                print('here we go')
                BF.animateUnit(None,u2,t,i)#New unit is built
    BF.drawClouds()

def changeAnimateSpeed(g1,g2):
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
    GV.animateTime = min(20,10+units*2)

starters = ['improvements','recruitment','armament','aviation']

def GetUnlockedTechs():
    techs = []
    for t in GV.game.tech[GV.player]:
        for t2 in TechDB[t]['unlocks']:
            if (not t2 in techs):
                techs.append(t2)

    starters = ['improvements','recruitment','armament','aviation']

    for t in starters:
        if (not t in techs):
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
    board_size_x = max(7, (GV.board_x_end - GV.board_x_start))
    board_size_y = max(7, (GV.board_y_end - GV.board_y_start))

    width_of_techs = [0,0]
    height_of_techs = [0,0]
    i = 0
    for key in treeWidth: #Add up two layers of trees. [0] is the top layer, [1] is the bottom layer
        #if i < len(treeWidth) / 2:
        if i == 0:
            width_of_techs[0] += treeWidth[key]
            height_of_techs[0] = max(height_of_techs[0], treeHeight[key])
        else:
            width_of_techs[1] += treeWidth[key]
            height_of_techs[1] = max(height_of_techs[1], treeHeight[key])
        i += 1
    
    width_of_techs = max(width_of_techs) #Max on width because stacked like hamburger
    height_of_techs = sum(height_of_techs) #Sum on height for same reason

    print("width_of_techs",width_of_techs)
    print("height_of_techs",height_of_techs)

    width = (GV.block_size+1)*board_size_x
    height = (GV.block_size+1)*board_size_y

    techSize = 60
    while width_of_techs * (techSize+1) > width or height_of_techs * (mult*techSize+1) > height:
        techSize-=1
    return

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

#Tree is the tech that starts the tree, key is current tech, and n is layer of tree
def getTreeSizes(tree, key, n = 0):
    global treeSizes, treeOffsets
    if TechDB[key]["unlocks"] == []:
        if len(treeSizes[tree]) <= n:
            while len(treeSizes[tree]) <= n:
                treeSizes[tree].append([])
                treeOffsets[tree].append(0)
        treeSizes[tree][n].append(1)
        return 1
    else:
        total = 0
        if key in GV.game.tech[GV.player] or key in currentTechMenu:
            for subTech in TechDB[key]["unlocks"]:
                if True:#subTech in currentTechMenu:
                    total += getTreeSizes(tree,subTech, n + 1)
        if total == 0:
            if len(treeSizes[tree]) <= n:
                while len(treeSizes[tree]) <= n:
                    treeSizes[tree].append([])
                    treeOffsets[tree].append(0)
            total = 1
        #print("treeSizes", treeSizes[tree])
        #print("key",key,'n',n,'tree',tree)
        treeSizes[tree][n].append(total)
        return total

#Tree is the tech that starts the tree, key is current tech, and n is layer of tree
def placeBoxes(tree,key, n = 0):
    noSubtrees = True
    if key in GV.game.tech[GV.player] or key in currentTechMenu:
        for subTech in TechDB[key]["unlocks"]:
            if True:#subTech in currentTechMenu:
                noSubtrees = False
                placeBoxes(tree, subTech, n + 1)
    boxPlacements[tree].append(((treeOffsets[tree][n] + treeSizes[tree][n][0]/2.0 - 0.5, n), key))
    treeOffsets[tree][n] += treeSizes[tree][n][0]
    if noSubtrees:
        for i in range(n+1, len(treeSizes[tree])):
            treeOffsets[tree][i] += treeSizes[tree][n][0]
    treeSizes[tree][n].pop(0)

mult = 1.5

def drawLinesHelper(key, d,treeXOffset, treeYOffset):
    print("KeY:",key,"Current D+",d)
    extraX = -2
    extraY = -2
    if key in GV.game.tech[GV.player] or key in currentTechMenu:
        for subTech in TechDB[key]["unlocks"]:
            #if subTech in currentTechMenu:
            drawLinesHelper(subTech, d,treeXOffset, treeYOffset)
        for subTech in TechDB[key]["unlocks"]:
            if True:#subTech in currentTechMenu:
                print(key, d[key], d[subTech])
                x1 = d[key][0][0] + treeXOffset
                y1 = d[key][0][1] + treeYOffset
                x2 = d[subTech][0][0] + treeXOffset
                y2 = d[subTech][0][1] + treeYOffset
                (x1+0.5)*(techSize+1)+GV.offset_x+1+extraX
                ColorOfLine = (255,255,255)
                if not (subTech in GV.game.tech[GV.player] or subTech in currentTechMenu):
                    ColorOfLine = (100,100,100)
                GV.pygame.draw.line(GV.DISPLAYSURF, ColorOfLine, 
                        #((int((x1+0.5)*(techSize+1)+GV.offset_x+1+extraX), int((y1+0.5)*(int(mult*techSize)+1)+GV.offset_y+1+extraY))),
                        ((int((x1+0.5)*(techSize+1)+GV.offset_x+1+extraX), int((techSize+1)*(y1*mult + 0.5)+GV.offset_y+1-mult+extraY))),
                        ((int((x2+0.5)*(techSize+1)+GV.offset_x+1+extraX), int((techSize+1)*(y2*mult + 0.5)+GV.offset_y+1-mult+extraY))), 3)
                d[subTech].pop(0)

def drawLines(tree, treeXOffset, treeYOffset):
    d = {}
    for key in boxPlacements[tree]:
        #img = Image.open('techAssets/%s.png' % key[1])
        #blank.paste(img, (int(key[0][0]*20), int(key[0][1]*30)))
        #d[key[1]] = key[0]
        if not (key[1] in d):
            d[key[1]] = []
        d[key[1]].append(key[0])
    drawLinesHelper(tree, d,treeXOffset, treeYOffset)

currentTechMenu = []
currentTechImages = {}
currentTechButtons = []
currentlyResearch = False
PrevTechHover = False
CurrentTechHover = False
knownTechHover = False
treeSizes = {}
treeOffsets = {}
boxPlacements = {}
treeWidth = {}
treeHeight = {}

def researchMenu():
    global currentTechMenu,currentTechImages,currentTechButtons,currentlyResearch,knownTechHover,treeSizes,treeOffsets,boxPlacements,treeWidth, treeHeight
    techs = GetUnlockedTechs()
    if techs == currentTechMenu and currentlyResearch and knownTechHover == CurrentTechHover:
        return
    knownTechHover = CurrentTechHover
    currentlyResearch = True
    currentTechMenu = techs
    print(currentTechMenu)

    #TODO: Show which are unlocked, and prevent their click
    #TODO: Potentially Show future unlocks

    treeSizes = {}
    treeOffsets = {}
    boxPlacements = {}  
    treeWidth = {}
    treeHeight = {}
    for tech in starters:
        treeSizes[tech] = [] #initilize each tree
        treeOffsets[tech] = [] #initilize each tree
        boxPlacements[tech] = [] #initilize each tree
        getTreeSizes(tech, tech)
        treeWidth[tech] = treeSizes[tech][0][0]
        placeBoxes(tech,tech)
        treeHeight[tech] = len(treeSizes[tech])


    print("aviation",boxPlacements["aviation"])
    print("hieght and width", treeHeight, treeWidth)
    print("treeSizes",treeSizes)

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
    board_size_x = max(7, (GV.board_x_end - GV.board_x_start))
    board_size_y = max(7, (GV.board_y_end - GV.board_y_start))
    if w > math.floor((GV.block_size+1)*board_size_x/(techSize+1)):
        w = math.floor((GV.block_size+1)*board_size_y/(techSize+1))
    extraX = 0#( (GV.block_size+1)*board_size_x - (w*(techSize+1)) )//2
    #print('(GV.block_size+1)*GV.board_y',(GV.block_size+1)*GV.board_y)
    #print('math.ceil(w/len(techs))',math.ceil(len(techs)/w))
    #print('(math.ceil(w/len(techs))*(techSize+1))',(math.ceil(len(techs)/w)*(techSize+1)))
    #print('all',( (GV.block_size+1)*GV.board_y - (math.ceil(len(techs)/w)*(techSize+1)) )//2)
    extraY = 0# ( (GV.block_size+1)*board_size_y - (math.ceil(len(techs)/w)*(techSize+1)) )//2
    print('extraY',extraY)
    rect = GV.pygame.Rect(GV.offset_x-1,GV.offset_y-1, (GV.block_size+1)*board_size_x+1,(GV.block_size+1)*board_size_y+1)#+GV.offset_x,410+GV.offset_y)
    GV.pygame.draw.rect(GV.DISPLAYSURF, BLACK, rect)

    maybeDeny = []
    if CurrentTechHover:
        maybeDeny = TechDB[CurrentTechHover].get('deny') or []
    
    treeXOffset = 0
    treeYOffset = 0
    
    print(boxPlacements, "boxPlacements")

    j = 0
    for key in boxPlacements:
        #if j - len(boxPlacements) / 2 == 0 or j - len(boxPlacements) / 2 == 0.5:
        if j == 1:
            print("key is this zone",key)
            treeXOffset = 0
            k = 0
            for key2 in treeWidth: #Add up two layers of trees. [0] is the top layer, [1] is the bottom layer
                #if k < len(treeWidth) / 2:
                if k == 0:
                    treeYOffset = max(treeYOffset, treeHeight[key2])
                else:
                    break
                k += 1
            
        print("We are going at the key: ", key,j)
        print("TREEXoffset",treeXOffset,"TREEYoffset", treeYOffset)

        drawLines(key, treeXOffset, treeYOffset)

        for i, techPlacement in enumerate(boxPlacements[key]):
        #for i, t in enumerate(currentTechMenu):
            #x = i%w
            #y = i//w
            t = techPlacement[1]
            x = techPlacement[0][0] + treeXOffset
            y = techPlacement[0][1] + treeYOffset
            
            b = Button("", x*(techSize+1)+GV.offset_x+1+extraX, y*(int(mult*techSize)+1)+GV.offset_y+1+extraY, BLACK,BLACK,18,(techSize,techSize),t)
            b.active = True
            b.techType = "Good"
            currentTechButtons.append(b)
            if not t in currentTechImages:
                img = GV.pygame.image.load("techAssets/%s.png" % t)
                img = GV.pygame.transform.scale(img, (techSize, techSize))
                currentTechImages[t] = img
            pos = (x*(techSize+1)+GV.offset_x-1+extraX, y*(int(mult*techSize)+1)+GV.offset_y-1+extraY)
            GV.DISPLAYSURF.blit(currentTechImages[t], pos)

            if t in GV.game.tech[GV.player]: #Already own this tech
                b.techType = "Owned"
                rect = GV.pygame.Rect(pos, (techSize+1, techSize+1))#+GV.offset_x,410+GV.offset_y)
                GV.pygame.draw.rect(GV.DISPLAYSURF, (220,220,220), rect, 1)
            elif not checkTechAffordable(selected, t): #This tech is too costly, (also can't be costly and owned)
                b.techType = "Costly"
                s = GV.pygame.Surface((techSize, techSize))
                s.set_alpha(160)
                s.fill((0,0,0))
                GV.DISPLAYSURF.blit(s, pos)

            if t in maybeDeny:
                s = GV.pygame.Surface((techSize, techSize))
                s.set_alpha(128)
                s.fill((0,0,0))
                GV.DISPLAYSURF.blit(s, pos)
            if not (t in GV.game.tech[GV.player] or t in currentTechMenu): #Either denied by other tech or is preview tech
                b.techType = "Dark"
                s = GV.pygame.Surface((techSize, techSize))
                s.set_alpha(170)
                s.fill((20,20,20))
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
            
            #Make images (similar to getImage) {DONE}
            #Display button with image on top {Done}
            #add buttons to techbuttons {DONE}
        
        #if not (j - len(boxPlacements) / 2 == 1 or j - len(boxPlacements) / 2 == 0.5): 
        #    print("key in bottom zone", key)
        treeXOffset += treeWidth[key]
        j+=1

def drawBoard():
    print('drawing BOARD')
    global NotAlreadyReady, currentlyResearch
    #print("______________________________")
    #print(vars(GV.game))
    if GV.game.ready:
        if NotAlreadyReady:
            if len(GV.game.units[GV.player]) == 0:
                return
            NotAlreadyReady = False
            updateSelf()
            BF.updateEdges()
            updateSelf()
            print("We've updated ourself")
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
                GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BGCOLOR, rect)
        #print('selected',selected)
        #print('stateDataMode',stateDataMode)
        if selected and stateDataMode == 'research':
            print('researching....')
            researchMenu()
            return
        currentlyResearch = False
        rect = GV.pygame.Rect(GV.offset_x-1,GV.offset_y-1, (GV.block_size+1)*(GV.board_x_end-GV.board_x_start)+1,(GV.block_size+1)*(GV.board_y_end-GV.board_y_start)+1)#+GV.offset_x,410+GV.offset_y)
        GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BGCOLOR, rect)
        for v in GV.highlightSquares:
            BF.highlightSquare(v[0],v[1])
        if len(GV.highlightSquares) > 0:
            BF.drawGridHighlight()
        else:
            BF.drawGrid()
        for u in GV.game.units[GV.player]:
            if u.stateData:#In case target isn't selected yet
                if u.state == 'move' and type(u.stateData) == list and type(u.stateData[0]) == int:
                    if checkRange(u,u.stateData) > u.speed:
                        BF.drawLine((45, 150, 138),u.position,u.stateData)
                    else:
                        BF.drawLine((0,255,255),u.position,u.stateData)
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
                        BF.drawLine((148, 55, 49),u.position,pos)
                    else:
                        BF.drawLine((255,0,0),u.position,pos)
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
                        BF.drawLine((150, 150, 150),u.position,pos)
                    else:
                        BF.drawLine((255,255,255),u.position,pos)
                elif u.state == 'build':
                    if len(u.stateData) == 2:
                        if checkRange(u,u.stateData[0]) > u.range:
                            BF.drawLine((110, 106, 46),u.position,u.stateData[0])
                        else:
                            BF.drawLine((255,170,0),u.position,u.stateData[0])
                elif u.state == 'transport':
                    if len(u.stateData) == 2:
                        if checkRange(u,u.stateData[0]) > u.range:
                            BF.drawLine((25, 150, 25),u.position,u.stateData[0])
                        else:
                            BF.drawLine((50,255,50),u.position,u.stateData[0])
        for i in GV.game.units:
            for u in GV.game.units[i]:
                BF.showUnitNEW(u)
        for pos in moveCircles:
            if pos in transportSpots:
                BF.drawIcon(greenCircle, pos)
            else:
                BF.drawIcon(blueCircle, pos)
            #GV.DISPLAYSURF.blit(blueCircle,(pos[0]*(GV.block_size+1)+GV.offset_x-1, pos[1]*(GV.block_size+1)+GV.offset_y-1))
        for pos in buildHexes:
            BF.drawIcon(OrangeHex, pos)
            #GV.DISPLAYSURF.blit(OrangeHex,(pos[0]*(GV.block_size+1)+GV.offset_x-1, pos[1]*(GV.block_size+1)+GV.offset_y-1))
        for pos in possibleAttacks:
            BF.drawIcon(GV.RedX, pos)
            #GV.DISPLAYSURF.blit(RedX,(pos[0]*(GV.block_size+1)+GV.offset_x-1, pos[1]*(GV.block_size+1)+GV.offset_y-1))
        for pos in possibleHeals:
            BF.drawIcon(GreenT, pos)
            #GV.DISPLAYSURF.blit(GreenT,(pos[0]*(GV.block_size+1)+GV.offset_x-1, pos[1]*(GV.block_size+1)+GV.offset_y-1))
        if selected:
            print('you have someone selected')
            print('posible',selected.possibleStates)
            if 'research' in selected.possibleStates and stateDataMode == None:
                print('yay for research')
                pos = selected.position
                BF.drawIcon(Beaker, pos)
                #GV.DISPLAYSURF.blit(Beaker,(pos[0]*(GV.block_size+1)+GV.offset_x-1, pos[1]*(GV.block_size+1)+GV.offset_y-1))
        BF.updateCloudCover()
        BF.drawClouds()
    else:
        font = GV.pygame.font.SysFont("arial", 60)
        text = font.render("Waiting...", 1, (255,0,0))
        GV.DISPLAYSURF.blit(text, (200,200))
        #text = font.render("PLAYER %s" % GV.player, 1, (255,0,0))
        #GV.DISPLAYSURF.blit(text, (200,300))

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
    #rect = GV.pygame.Rect(2,WINDOWHEIGHT-52, 80,50)#428
    rect = GV.pygame.Rect(2,WINDOWHEIGHT-67, 80,65)#428
    GV.pygame.draw.rect(GV.DISPLAYSURF, (50,50,50), rect)
    Healthfont = GV.pygame.font.SysFont("arial", 15)
    text = Healthfont.render(str(GV.game.scores[GV.player]), 1, (255,255,255))
    GV.DISPLAYSURF.blit(text, (5,WINDOWHEIGHT-65))#430
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
        pass#return
    currentStatInfo = unit
    if type(unit) == str:
        unit = Unit('',unit)
    rect = GV.pygame.Rect(endOfBoard_x+5, 5, 180,endOfBoard_y)#+GV.offset_x,410+GV.offset_y)
    GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BGCOLOR, rect)
    
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

    fontsize = 15
    if len(text) * (fontsize + 2) + 5 > endOfBoard_y:
        fontsize = int((endOfBoard_y - 5)/len(text) - 2)

    font = GV.pygame.font.SysFont("arial", fontsize)
    
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
    rect = GV.pygame.Rect(endOfBoard_x+5, 5, 180,endOfBoard_y)#+GV.offset_x,410+GV.offset_y)
    GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BGCOLOR, rect)

    text = []
    name = tech.title().split()
    for i, v in enumerate(name):
        if v == 'Of':
            name[i] = 'of'
    text.extend(textToLines(NameTitle(tech)))
    text.append('')

    T = TechDB[tech]
    progress = GV.game.progress[GV.player].get(tech) or 0
    text.append('Time: %s/%s' % (progress, T['time']))
    text.append('Cost: %s energy' % T['cost'])
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
            text.extend(textToLines('Unlocks %s at %s' % (NameTitle(v[2]), NameTitle(v[1]))))
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
    
        
    fontsize = 15
    if len(text) * (fontsize + 2) + 5 > endOfBoard_y:
        fontsize = int((endOfBoard_y - 5)/len(text) - 2)

    font = GV.pygame.font.SysFont("arial", fontsize)

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
extraButtons = []
grid = []

def cleanUpAfterSelect():
    global moveCircles,transportSpots, selected,stateDataMode, extraButtons, buildHexes, possibleAttacks,possibleHeals,PrevTechHover,CurrentTechHover
    selected = None
    print(selected)
    stateDataMode = None
    GV.highlightSquares = []
    moveCircles = []
    transportSpots = []
    buildHexes = []
    possibleAttacks = []
    possibleHeals = []
    rect = GV.pygame.Rect(endOfBoard_x+5, 5, 180,410)
    GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BGCOLOR, rect)
    for btn in btns:
        btns[btn].deDraw(GV.DISPLAYSURF)
    for btn in extraButtons:
        btn.deDraw(GV.DISPLAYSURF)

def main(playerCount = None):
    global FPSCLOCK, moveCircles,transportSpots, selected, stateDataMode, extraButtons, buildHexes,possibleAttacks,possibleHeals,counter,grid, buildUnitImages,PrevTechHover,CurrentTechHover
    #GV.pygame.init()
    FPSCLOCK = GV.pygame.time.Clock()
    GV.DISPLAYSURF = GV.pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),RESIZABLE)
    
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    GV.pygame.display.set_caption('Blank')

    GV.DISPLAYSURF.fill(GV.BGCOLOR)

    mouseDown = False

    GV.pygame.mixer.music.load("audio/overview_music.wav")
  
    # Setting the volume
    GV.pygame.mixer.music.set_volume(0.3)
    
    # Start playing the song
    GV.pygame.mixer.music.play(-1)

    start_music = 0
    
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

    GV.JustResize = 0
    animateCounter = GV.animateTime*-2
    GV.newGame = None
    images = []
    
    while run: # main GV.game loop
        #mouseClicked = False

        #GV.DISPLAYSURF.fill(GV.BGCOLOR)#Draw window
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
                            GV.newGame = r
                            changeAnimateSpeed(GV.game,GV.newGame)
                            animationGrid(GV.game,GV.newGame)
                            print(GV.animateTime)
                        else:
                            GV.game = r
                else:
                    #print("stuff", roundEnd(GV.game,r))
                    GV.game = r
                    GV.newGame = r#######
                    #print("GAME", vars(GV.game))
                    #print("GV.newGame", vars(GV.newGame))
                    #print("R", vars(r))
            elif type(R) == str:
                #print("HERE2", r)
                pass#print(r)
        except Exception as e:
            run = False
            print("Couldn't get GV.game",e)
            break
        
        counter += 1
        if counter-animateCounter <= GV.animateTime:
            print("animateCounter",animateCounter,"counter",counter)
            if animateCounter + 1 == counter:
                print("WE ARE HERE WE ARE HERE WE ARE HERE")
                BF.updateEdges()
                print("THE EDGES",GV.board_x_start,GV.board_x_end,GV.board_y_start,GV.board_y_end)
                updateSelf()
                BF.updateEdges()
                drawBoard()
            animateBoard(GV.game, GV.newGame, counter-animateCounter)
            if counter-animateCounter == GV.animateTime:
                im = Image.new(mode="RGB", size=(GV.board_x, GV.board_y))
                pix = im.load()
                i = 0
                for c in GV.BoardColors:
                    x = i % GV.board_x
                    y = i // GV.board_x
                    pix[x,y] = c
                    i += 1
                for player in GV.game.units:
                    for u in GV.game.units[player]:
                        pix[u.position[0],u.position[1]] = GV.playerColors[player]
                im = im.resize((GV.board_x * 4, GV.board_y * 4))
                images.append(im)
                pass#GV.DISPLAYSURF.fill(GV.BGCOLOR) #Used to clear the board after animating, but blinks when doing so
        elif counter%10 == 0:
            #print("MORE ", vars(GV.game))
            if GV.newGame:
                #print("Even MORE", vars(GV.newGame))
                GV.game = GV.newGame
            #print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            #print(vars(GV.game))
            drawBoard()
            resources()
        
        for event in GV.pygame.event.get():
            if counter-animateCounter <= GV.animateTime:#Don't continue to watch events
                break
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                if serverprocess:
                    serverprocess.kill()
                GV.pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == 109: # 'm' Key
                    GV.board_x_start = 0
                    GV.board_y_start = 0
                    GV.board_x_end = 15
                    GV.board_y_end = 15
                    GV.JustResize = counter
                    updateSelf()
                    #GV.pygame.mixer.music.pause()
                elif event.key == 110: # 'n' Key
                    GV.board_x_start = 3
                    GV.board_y_start = 1
                    GV.board_x_end = 14
                    GV.board_y_end = 14
                    GV.JustResize = counter
                    updateSelf()
                    #GV.pygame.mixer.music.unpause()
                elif event.key == 111: # 'o' Key   
                    images[0].save("the_map.gif", save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0) 
                elif event.key == 112: # 'p' Key    
                    im = Image.new(mode="RGB", size=(GV.board_x, GV.board_y))
                    pix = im.load()
                    i = 0
                    for c in GV.BoardColors:
                        x = i % GV.board_x
                        y = i // GV.board_x
                        pix[x,y] = c
                        i += 1
                    for player in GV.game.units:
                        for u in GV.game.units[player]:
                            pix[u.position[0],u.position[1]] = GV.playerColors[player]
                    im = im.resize((GV.board_x * 4, GV.board_y * 4))
                    im.show()
            elif event.type == VIDEORESIZE and counter - GV.JustResize > 20:
                GV.JustResize = counter
                if event.w-230 > event.h-65: #Wide rectangle
                    GV.block_size = (event.h-65)//max(7, (GV.board_y_end - GV.board_y_start))
                else:
                    GV.block_size = (event.w-65)//max(7, (GV.board_x_end - GV.board_x_start))
                print('blocksize',GV.block_size)
                GV.playerUnitImages = {} #To reset all unit images
                buildUnitImages = {}
                updateSelf()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                if selected and mousey > endOfBoard_y and stateDataMode != 'build2':
                    if 'build' in selected.possibleStates:#If they are able to build
                        unfound = True
                        for btn in extraButtons:
                            if btn.click(GV.pygame.mouse.get_pos()):#If one of the unit options is clicked
                                statInfo(btn.name)
                                unfound = False
                                break
                        if unfound:
                            statInfo(selected)
                    if 'transport' in selected.possibleStates:#If they are able to build
                        unfound = True
                        for btn in extraButtons:
                            if btn.click(GV.pygame.mouse.get_pos()):#If one of the unit options is clicked
                                statInfo(btn.name)
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
                x += GV.board_x_start
                y += GV.board_y_start
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
                        if btn.click(GV.pygame.mouse.get_pos()):#If one of the unit options is clicked
                            selected.stateData = [btn.name]
                            stateDataMode = 'build2'
                            statInfo(btn.name)
                            for btn2 in extraButtons:
                                btn2.deDraw(GV.DISPLAYSURF)
                            extraButtons = []
                            buildHexes = getRangeCircles(selected, built = btn.name)
                            drawBoard()
                            offclick = False
                            break
                    if offclick:
                        selected.state = None
                        cleanUpAfterSelect()
                        for btn in extraButtons:
                           btn.deDraw(GV.DISPLAYSURF)
                        extraButtons = []
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
                elif stateDataMode == 'transport':
                    selected.state = None
                    if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:
                        construction.play()
                        selected.stateData.insert(0,[x,y])
                        n.send(convertToStr(selected,'transport',selected.stateData))
                        selected.state = 'transport'
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

                    CleanUp = True #Only cleanup if player clicked a valid tech or black region
                    
                    for btn in currentTechButtons:
                        if btn.click(GV.pygame.mouse.get_pos()):
                            if btn.techType == "Good":
                                research_selected_audio.play()
                            else:
                                tech_error_audio.play()
                                if btn.techType != "Costly": #If its costly, go through but give error noise
                                    CleanUp = False
                                    break
                            
                            
                            print('ONE OF THEM WAS CLICKKKEDD!!')

                            #research_selected_audio.play()

                            selected.stateData = btn.name
                            n.send(convertToStr(selected,'research',selected.stateData))
                            selected.state = 'research'
                            break
                        
                    if CleanUp:
                        BF.clearGrid()
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
                                    img = BF.getImage(v, GV.player, buildUnitImages, 40)
                                    #buildUnitImages
                                    #img = GV.pygame.image.load("assets/%s.png" % v)
                                    #img = GV.pygame.transform.scale(img, (40, 40))
                                    GV.DISPLAYSURF.blit(img,(GV.offset_x+(GV.block_size+1)*i, endOfBoard_y+10))
                                    b.name = v
                                    extraButtons.append(b)#extraButtons[v] = b
                                    i+=1
                            drawBoard()
                    if 'build' in selected.possibleStates:#If they are able to build
                        for btn in extraButtons:
                            if btn.click(GV.pygame.mouse.get_pos()):#If one of the unit options is clicked
                                selected.stateData = [btn.name]
                                stateDataMode = 'build2'
                                statInfo(btn.name)
                                for btn2 in extraButtons:
                                    btn2.deDraw(GV.DISPLAYSURF)
                                extraButtons = []
                                moveCircles = []
                                transportSpots = []
                                possibleAttacks = []
                                possibleHeals = []
                                buildHexes = getRangeCircles(selected, built = btn.name)
                                offclick = False
                                drawBoard()
                                break
                    if 'transport' in selected.possibleStates:#If they are able to build
                        for btn in extraButtons:
                            if btn.click(GV.pygame.mouse.get_pos()):#If one of the unit options is clicked
                                selected.stateData = [btn.name]
                                stateDataMode = 'transport'
                                statInfo(btn.name)
                                for btn2 in extraButtons:
                                    btn2.deDraw(GV.DISPLAYSURF)
                                extraButtons = []
                                moveCircles = []
                                transportSpots = []
                                possibleAttacks = []
                                possibleHeals = []
                                buildHexes = getRangeCircles(selected, built = btn.name)
                                offclick = False
                                drawBoard()
                                break
                    #if x >= 0 and y >= 0 and y<GV.board_y and x<GV.board_x:
                    if x >= GV.board_x_start and y >= GV.board_y_start and y<GV.board_y_end and x<GV.board_x_end:
                        print("An extra thing")
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
                                transportSpots = getTransportSpots(selected)
                                print("Total transport spots 1", transportSpots)
                                moveCircles += transportSpots
                                possibleAttacks = getAttacks(selected)
                                possibleHeals = getHeals(selected)
                                statInfo(selected)
                                for btn in btns:
                                    if btn in selected.possibleStates:
                                        btns[btn].draw(GV.DISPLAYSURF)
                                    else:
                                        btns[btn].deDraw(GV.DISPLAYSURF)
                                for btn in extraButtons:
                                    btn.deDraw(GV.DISPLAYSURF)
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
                                        img = BF.getImage(v, GV.player, buildUnitImages, 40)
                                        #img = GV.pygame.image.load("assets/%s.png" % v)
                                        #img = GV.pygame.transform.scale(img, (40, 40))
                                        GV.DISPLAYSURF.blit(img,(GV.offset_x+(40+1)*i, endOfBoard_y+10))
                                        b.name = v
                                        extraButtons.append(b)#extraButtons[v] = b
                                        i+=1
                                if 'transport' in selected.possibleStates: #Show things on bottom
                                    if hasattr(selected,"carrying"):
                                        i = 0
                                        posBuilds = selected.carrying
                                        for unit in posBuilds:
                                            unitName = unit['name']
                                            btnColor = (50,230,50)
                                            b = Button("", GV.offset_x+(40+1)*i, endOfBoard_y+10, btnColor,BLACK,18,(40,40))
                                            b.draw(GV.DISPLAYSURF)
                                            img = BF.getImage(unitName, GV.player, buildUnitImages, 40)
                                            #img = GV.pygame.image.load("assets/%s.png" % v)
                                            #img = GV.pygame.transform.scale(img, (40, 40))
                                            GV.DISPLAYSURF.blit(img,(GV.offset_x+(40+1)*i, endOfBoard_y+10))#(115+41*i, 430)
                                            b.name = unitName
                                            extraButtons.append(b)#extraButtons[v] = b
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
                            transportSpots = getTransportSpots(selected)
                            print("Total transport spots 2", transportSpots)
                            moveCircles += transportSpots
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
                                    img = BF.getImage(v, GV.player, buildUnitImages, 40)
                                    #img = GV.pygame.image.load("assets/%s.png" % v)
                                    #img = GV.pygame.transform.scale(img, (40, 40))
                                    GV.DISPLAYSURF.blit(img,(GV.offset_x+(40+1)*i, endOfBoard_y+10))#(115+41*i, 430)
                                    b.name = v
                                    extraButtons.append(b)#extraButtons[v] = b
                                    i+=1
                            if 'transport' in selected.possibleStates: #Show things on bottom
                                if hasattr(selected,"carrying"):
                                    i = 0
                                    posBuilds = selected.carrying
                                    for unit in posBuilds:
                                        unitName = unit['name']
                                        btnColor = (50,230,50)
                                        b = Button("", GV.offset_x+(40+1)*i, endOfBoard_y+10, btnColor,BLACK,18,(40,40))
                                        b.draw(GV.DISPLAYSURF)
                                        img = BF.getImage(unitName, GV.player, buildUnitImages, 40)
                                        #img = GV.pygame.image.load("assets/%s.png" % v)
                                        #img = GV.pygame.transform.scale(img, (40, 40))
                                        GV.DISPLAYSURF.blit(img,(GV.offset_x+(40+1)*i, endOfBoard_y+10))#(115+41*i, 430)
                                        b.name = unitName
                                        extraButtons.append(b)#extraButtons[v] = b
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
