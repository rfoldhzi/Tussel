import GlobalVaribles as GV
from operator import add
import ClientFunctions as CF

try:
    from PIL import Image
except:
    imageMani = False
    print("No Pillow module found. Please use folling command to install for quality images:")
    print("python3 -m pip install --upgrade Pillow")


def highlightSquare(x,y):
    rect = GV.pygame.Rect((x-GV.board_x_start)*(GV.block_size+1)+GV.offset_x, (y-GV.board_y_start)*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
    GV.pygame.draw.rect(GV.DISPLAYSURF, (255,255,255), rect)

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
                if pixels[i,j] == GV.changeColor: #Looks for the pink in pictures to change
                    pixels[i,j] = GV.playerColors[p]
        img = GV.pygame.image.fromstring(img.tobytes(), img.size, img.mode)
        img = GV.pygame.transform.scale(img, (size, size))
        Pictures[p][name] = img
    return Pictures[p][name]

def showUnitNEW(unit):
    x = unit.position[0]
    y = unit.position[1]
    image = None
    
    if x < GV.board_x_start or GV.board_x_end <= x or y < GV.board_y_start or GV.board_y_end <= y:
        return

    for p in GV.game.units:
        if unit in GV.game.units[p]:
            image = getImage(unit.name, p)
            break
    
    GV.DISPLAYSURF.blit(image,((x-GV.board_x_start)*(GV.block_size+1)+GV.offset_x-1, (y-GV.board_y_start)*(GV.block_size+1)+GV.offset_y-1))
    
    t = str(unit.health)
    Healthfont = GV.pygame.font.SysFont("arial", 15)
    text = Healthfont.render(t, 1, (255,255,255))
    #GV.DISPLAYSURF.blit(text, (x*(GV.block_size+1)+GV.offset_x+38-(7*len(t)), y*(GV.block_size+1)+GV.offset_y+23))
    GV.DISPLAYSURF.blit(text, ((x-GV.board_x_start)*(GV.block_size+1)+GV.offset_x+(GV.block_size-2)-(7*len(t)), (y-GV.board_y_start)*(GV.block_size+1)+GV.offset_y+(GV.block_size-17)))

    #State square
    if unit.state != None and unit in GV.game.units[GV.player]:
        #print(vars(unit))
        rect = GV.pygame.Rect((x-GV.board_x_start)*(GV.block_size+1)+GV.offset_x+GV.block_size - 9, (y-GV.board_y_start)*(GV.block_size+1)+GV.offset_y+4, 5, 5)
        if unit.state == 'resources':
            if unit.stateData and type(unit.stateData) == str and unit.stateData in GV.resourceColors:
                GV.pygame.draw.rect(GV.DISPLAYSURF, GV.resourceColors[unit.stateData], rect)
        else:
            GV.pygame.draw.rect(GV.DISPLAYSURF, GV.StateColors[unit.state], rect)

def clearGrid():
    board_size_x = max(7, (GV.board_x_end - GV.board_x_start))
    board_size_y = max(7, (GV.board_y_end - GV.board_y_start))
    rect = GV.pygame.Rect(GV.offset_x-1,GV.offset_y-1, (GV.block_size+1)*board_size_x+1,(GV.block_size+1)*board_size_y+1)#+GV.offset_x,410+GV.offset_y)
    GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BGCOLOR, rect)

def drawLine(color,pos1,pos2):
    if pos1[0] < GV.board_x_start or GV.board_x_end <= pos1[0] or pos1[1] < GV.board_y_start or GV.board_y_end <= pos1[1]:
        return
    if pos2[0] < GV.board_x_start or GV.board_x_end <= pos2[0] or pos2[1] < GV.board_y_start or GV.board_y_end <= pos2[1]:
            return
    GV.pygame.draw.line(GV.DISPLAYSURF, color, ((GV.block_size+1)*(pos1[0]-GV.board_x_start)+GV.offset_x+GV.block_size/2,(GV.block_size+1)*(pos1[1]-GV.board_y_start)+GV.offset_y+GV.block_size/2),
                                               ((GV.block_size+1)*(pos2[0]-GV.board_x_start)+GV.offset_x+GV.block_size/2,(GV.block_size+1)*(pos2[1]-GV.board_y_start)+GV.offset_y+GV.block_size/2),10)

def drawGrid():
    for y in range(GV.board_y_start, GV.board_y_end):
        for x in range(GV.board_x_start, GV.board_x_end):
            i = (y*GV.board_x) + x
            rect = GV.pygame.Rect((x-GV.board_x_start)*(GV.block_size+1)+GV.offset_x, (y-GV.board_y_start)*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
            GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BoardColors[i], rect)

def drawAnimateGrid():
    for y in range(GV.board_y_start, GV.board_y_end):
        for x in range(GV.board_x_start, GV.board_x_end):
            if GV.animateGrid[y][x]:
                pass
            else:
                color = GV.BoardColors[(y*GV.board_x) + x]
                rect = GV.pygame.Rect((x-GV.board_x_start)*(GV.block_size+1)+GV.offset_x, (y-GV.board_y_start)*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
                GV.pygame.draw.rect(GV.DISPLAYSURF, color, rect)

def drawGridHighlight():
    for y in range(GV.board_y_start, GV.board_y_end):
        for x in range(GV.board_x_start, GV.board_x_end):
            rect = None
            if [x,y] in GV.highlightSquares:
                rect = GV.pygame.Rect((x-GV.board_x_start)*(GV.block_size+1)+GV.offset_x+1, (y-GV.board_y_start)*(GV.block_size+1)+GV.offset_y+1, GV.block_size-1, GV.block_size-1)
            else:
                rect = GV.pygame.Rect((x-GV.board_x_start)*(GV.block_size+1)+GV.offset_x, (y-GV.board_y_start)*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
            i = (y*GV.board_x) + x
            GV.pygame.draw.rect(GV.DISPLAYSURF, GV.BoardColors[i], rect)

def updateCloudCover(SpecificGame = None):
    if SpecificGame == None:
        SpecificGame = GV.game
    if GV.cloudMode == "sight" or GV.cloudMode == "halo":
        GV.cloudGrid = []
        for y in range(GV.board_y):
            l = []
            for x in range(GV.board_x):
                l.append(True)
            GV.cloudGrid.append(l)
    for u in SpecificGame.units[GV.player]:
        spaces = CF.getRangeCircles(u, True)
        for pos in spaces:
            if GV.cloudGrid[pos[1]][pos[0]]:
                GV.cloudGrid[pos[1]][pos[0]] = False
            if GV.cloudMode == "halo" and GV.explorationGrid[pos[1]][pos[0]]:
                GV.explorationGrid[pos[1]][pos[0]] = False

def drawClouds():
    if GV.cloudMode == "clear":
        return
    for y in range(GV.board_y_start, GV.board_y_end):
        for x in range(GV.board_x_start, GV.board_x_end):
            i = (y*GV.board_x) + x
            if GV.cloudGrid[y][x] and GV.cloudMode != "halo":
                rect = GV.pygame.Rect((x - GV.board_x_start)*(GV.block_size+1)+GV.offset_x, (y-GV.board_y_start)*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
                GV.pygame.draw.rect(GV.DISPLAYSURF, GV.CloudColors[i], rect)
            elif GV.cloudMode == "halo":
                if GV.explorationGrid[y][x]:
                    rect = GV.pygame.Rect((x - GV.board_x_start)*(GV.block_size+1)+GV.offset_x, (y-GV.board_y_start)*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
                    GV.pygame.draw.rect(GV.DISPLAYSURF, GV.CloudColors[i], rect)
                elif GV.cloudGrid[y][x]:
                    rect = GV.pygame.Rect((x - GV.board_x_start)*(GV.block_size+1)+GV.offset_x, (y-GV.board_y_start)*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
                    
                    color = list( map(add, (0,0,0), GV.BoardColors[i]) )
                    color = [x / 2 for x in color]
                    GV.pygame.draw.rect(GV.DISPLAYSURF, color, rect)

def drawIcon(image, pos):
    GV.DISPLAYSURF.blit(image,((pos[0] - GV.board_x_start)*(GV.block_size+1)+GV.offset_x-1, (pos[1]-GV.board_y_start)*(GV.block_size+1)+GV.offset_y-1))

def animateUnit(unit1, unit2,t,specfic_player):
    unit = unit1
    if not unit1:
        unit = unit2
    x = unit.position[0]
    y = unit.position[1]
    image = None
    if GV.animateGrid[y][x]:
        return

    if x < GV.board_x_start or GV.board_x_end <= x or y < GV.board_y_start or GV.board_y_end <= y:
        return
    if unit2.position[0] < GV.board_x_start or GV.board_x_end <= unit2.position[0] or unit2.position[1] < GV.board_y_start or GV.board_y_end <= unit2.position[1]:
        return

    image = getImage(unit.name, specfic_player)
    
    default = True
    if not unit1:
        parent = GV.game.getUnitFromID(unit2.parent)
        if parent:
            default = False
            x2,y2 = parent.position
            if x2 < GV.board_x_start or GV.board_x_end <= x2 or y2 < GV.board_y_start or GV.board_y_end <= y2:
                return
            start = ((x2 - GV.board_x_start)*(GV.block_size+1)+GV.offset_x-1, (y2 - GV.board_y_start)*(GV.block_size+1)+GV.offset_y-1)
            end = ((x - GV.board_x_start)*(GV.block_size+1)+GV.offset_x-1, (y - GV.board_y_start)*(GV.block_size+1)+GV.offset_y-1)
            Pos = CF.intPoint(CF.LerpPoint(start, end, t/GV.animateTime))
            GV.DISPLAYSURF.blit(image,Pos)
    elif unit1.position != unit2.position:
        default = False
        start = ((x - GV.board_x_start)*(GV.block_size+1)+GV.offset_x-1, (y - GV.board_y_start)*(GV.block_size+1)+GV.offset_y-1)
        end = ((unit2.position[0] - GV.board_x_start)*(GV.block_size+1)+GV.offset_x-1, (unit2.position[1] - GV.board_y_start)*(GV.block_size+1)+GV.offset_y-1)
        Pos = CF.intPoint(CF.LerpPoint(start, end, t/GV.animateTime))
        GV.DISPLAYSURF.blit(image,Pos)
    if default:#No move
        GV.DISPLAYSURF.blit(image,((x - GV.board_x_start)*(GV.block_size+1)+GV.offset_x-1, (y - GV.board_y_start)*(GV.block_size+1)+GV.offset_y-1))
        T = str(unit.health)
        Healthfont = GV.pygame.font.SysFont("arial", 15)
        text = Healthfont.render(T, 1, (255,255,255))
        if unit1 and unit2:
            if unit2.health < unit1.health:
                T = str(int(CF.Lerp(unit1.health, unit2.health, t/GV.animateTime)))
                text = Healthfont.render(T, 1, (255,0,0))
            elif unit2.health > unit1.health:
                T = str(int(CF.Lerp(unit1.health, unit2.health, t/GV.animateTime)))
                text = Healthfont.render(T, 1, (255,255,255))
            elif unit1 == unit2:
                T = str(int(CF.Lerp(unit1.health, 0, t/GV.animateTime)))
                text = Healthfont.render(T, 1, (255,0,0))
        GV.DISPLAYSURF.blit(text, ((x - GV.board_x_start)*(GV.block_size+1)+GV.offset_x+(GV.block_size-2)-(7*len(T)), (y - GV.board_y_start)*(GV.block_size+1)+GV.offset_y+(GV.block_size-17)))

        #State square
        if unit2:
            unit = unit2
        if unit.state != None and unit1 in GV.game.units[specfic_player]:
            #print(vars(unit))
            rect = GV.pygame.Rect((x - GV.board_x_start)*(GV.block_size+1)+GV.offset_x+GV.block_size - 9, (y - GV.board_y_start)*(GV.block_size+1)+GV.offset_y+4, 5, 5)
            if unit.state == 'resources':
                if unit.stateData and type(unit.stateData) == str and unit.stateData in GV.resourceColors:
                    GV.pygame.draw.rect(GV.DISPLAYSURF, GV.resourceColors[unit.stateData], rect)
            else:
                GV.pygame.draw.rect(GV.DISPLAYSURF, GV.StateColors[unit.state], rect)
    if unit1 == unit2:
        GV.DISPLAYSURF.blit(GV.RedX,((x - GV.board_x_start)*(GV.block_size+1)+GV.offset_x-1, (y - GV.board_y_start)*(GV.block_size+1)+GV.offset_y-1))


def updateEdges():
    updateCloudCover(GV.newGame)
    if GV.cloudMode == "clear":
        GV.board_x_start = 0
        GV.board_y_start = 0
        GV.board_x_end = GV.board_x
        GV.board_y_end = GV.board_y
        return
    leastX = GV.board_x
    leastY = GV.board_y
    mostX = 0
    mostY = 0
    for y in range(GV.board_y):
        for x in range(GV.board_x):
            if not GV.explorationGrid[y][x]:
                if x - 1 < leastX: # The minus is so you can see so clouds at the edge
                    leastX = x - 1
                elif x + 2 > mostX: # The most needs an extra 1 (off by 1), so plus 2
                    mostX = x + 2
                if y - 1 < leastY:
                    leastY = y - 1
                elif y + 2 > mostY:
                    mostY = y + 2
    GV.board_x_start = max(leastX, 0)
    GV.board_y_start = max(leastY, 0)
    GV.board_x_end = min(mostX, GV.board_x)
    GV.board_y_end = min(mostY, GV.board_y)