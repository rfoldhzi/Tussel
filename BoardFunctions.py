import GlobalVaribles as GV

try:
    from PIL import Image
except:
    imageMani = False
    print("No Pillow module found. Please use folling command to install for quality images:")
    print("python3 -m pip install --upgrade Pillow")


def highlightSquare(x,y):
    rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x, y*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
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
    
    for p in GV.game.units:
        if unit in GV.game.units[p]:
            image = getImage(unit.name, p)
            break
    
    GV.DISPLAYSURF.blit(image,(x*(GV.block_size+1)+GV.offset_x-1, y*(GV.block_size+1)+GV.offset_y-1))
    
    t = str(unit.health)
    Healthfont = GV.pygame.font.SysFont("arial", 15)
    text = Healthfont.render(t, 1, (255,255,255))
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
            if GV.animateGrid[y][x]:
                pass
            else:
                rect = GV.pygame.Rect(x*(GV.block_size+1)+GV.offset_x, y*(GV.block_size+1)+GV.offset_y, GV.block_size+1, GV.block_size+1)
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