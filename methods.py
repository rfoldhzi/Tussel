import random, math,os,sys
from PIL import Image
#os.chdir(os.path.dirname(sys.argv[0]))

replaceD = {
'null':"N",
'false':"`",
'true':"+",
'"name":':"L",
',"resourceGen":':"R",
',"stateData":':"Q",
'],"state":':"&",
',"UnitID":':"W",
',"position":':"%",
',"maxHealth":':"K",
',"parent":':"^",
',"defense":':"/",
',"maxPopulation"':"@",
',"population":':"V",
',"speed":1':"C",
',"range":1':"Z",
',"attack":':"!",
'"attack"':'>',
'"move"':"<",
'"build"':"Y",
'"trooper"':"T",
'"building"':"B",
',"type":':"|",
',"health":':"J",
'"resources"':"$",
'"gold"':"F",
'"metal"':"M",
'"energy"':"E",
',"possibleStates":':"O",
',"abilities":':"A",
}
def zipper(t):
    for v in replaceD:
        t = t.replace(v,replaceD[v])
    return t

def unzipper(t):
    print("dfhjgffgt")
    for v in replaceD:
        t = t.replace(replaceD[v],v)
    return t

def newGrid(x,y):
    g = []
    for i in range(x):
        l = []
        for j in range(y):
            l.append(False)
        g.append(l)
    return g

def newGrid2(x,y):
    g = []
    for i in range(x):
        l = []
        for j in range(y):
            l.append(True)
        g.append(l)
    return g

def pickRandom(g):
    return [random.randint(0,len(g)-1),random.randint(0,len(g[0])-1)]

def getSurround(g,pos):#Could be more effiecint
    spaces = []
    for x in range(pos[0]-1, pos[0]+2):
        for y in range(pos[1]-1, pos[1]+2):
            if x >= 0 and y >= 0 and y<len(g) and x<len(g[0]):#If within board:
                if not g[y][x]:
                    spaces.append([x,y])
    #print('surround', pos, spaces)
    return spaces

def getSurroundNumber(g,pos, water):#Could be more effiecint
    count = 0
    for x in range(pos[0]-1, pos[0]+2):
        for y in range(pos[1]-1, pos[1]+2):
            if x >= 0 and y >= 0 and y<len(g) and x<len(g[0]):#If within board:
                if water == g[y][x]:
                    count += 1
    #print('surround', pos, spaces)
    return count

def MinRange(points):
    Min = checkRangePos(points[0], points[1])
    for i in range(len(points)-1):
        for j in range(i+1,len(points)):
            if checkRangePos(points[i], points[j]) < Min:
                Min = checkRangePos(points[i], points[j])
    return Min

def smoothAreas(g, cutoff = 7):
    g2 = newGrid(len(g[0]),len(g))
    for y in range(len(g)):
        for x in range(len(g[0])):
            if getSurroundNumber(g,[x,y], not g[y][x]) >= cutoff:
                g2[y][x] = not g[y][x]
            else:
                g2[y][x] = g[y][x]
    return g2

def reduceFlooding(g, cutoff = 5):
    g2 = newGrid(len(g[0]),len(g))
    for y in range(len(g)):
        for x in range(len(g[0])):
            g2[y][x] = g[y][x]
            if g[y][x]:
                if getSurroundNumber(g,[x,y], False) >= cutoff:
                    g2[y][x] = False
            
    return g2

def destroy1block(g,cutoff = 5):
    g2 = newGrid(len(g[0]),len(g))
    for y in range(len(g)):
        for x in range(len(g[0])):
            g2[y][x] = g[y][x]
    y = 0
    for x in range(len(g[0])):
        if getSurroundNumber(g,[x,y], True) >= cutoff:
            g2[y][x] = True
    y = len(g)-1
    for x in range(len(g[0])):
        if getSurroundNumber(g,[x,y], True) >= cutoff:
            g2[y][x] = True
    x = 0
    for x in range(len(g)):
        if getSurroundNumber(g,[x,y], True) >= cutoff:
            g2[y][x] = True
    x = len(g[0])-1
    for x in range(len(g)):
        if getSurroundNumber(g,[x,y], True) >= cutoff:
            g2[y][x] = True
    return g2
    
    
def makeAreas(g):
    totalTiles = len(g)*len(g[0])
    #maxTiles = int(totalTiles*.6/(1+math.e**(-0.02*(totalTiles-100))))
    maxTiles = int(totalTiles*(.1+.4/(1+math.e**(-0.02*(totalTiles-100)))))
    print('total tiles', maxTiles)
    spots = random.randint(1,len(g)*len(g[0])//20)
    print('lakes', spots)
    for i in range(spots):
        pos = pickRandom(g)
        g[pos[0]][pos[1]] = True
    print('tiles made so far',g)
    for i in range(maxTiles-spots):
        possible = []
        for x in range(len(g[0])):
            for y in range(len(g)):
                if g[y][x]:
                    possible += getSurround(g,[x,y])
        print('possible', possible)
        choice = random.choice(possible)
        print(choice)
        g[choice[1]][choice[0]] = True
        print('areasMade',i)
    g = smoothAreas(g)
    g = smoothAreas(g, 6)
    for i in range(3):
        g = smoothAreas(g)
    g = destroy1block(g)
    return g

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
    return total, X, Y

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

def findSecondIsland(g,best,attempts = 10):
    bestIsland = []
    for i in range(attempts):
        pos = pickRandom(g)
        if not g[pos[0]][pos[1]]:
            island = GetIsland(g, pos)
            if len(island) > len(bestIsland) and len(island) < len(best):
                bestIsland = island
    return bestIsland

def smoothIsland(g, island):
    for pos in island:
        s = getSurround(g,pos)
        if len(s) < 3:
            island.remove(pos)
    return island

def flipList(island):
    for i in range(len(island)):
        island[i] = island[i][::-1]
    return island

def findStartSpots(g, n = 2, i = 0):
    if i > 30:
        return "RETRY"
    print(g)
    print(n)
    island = findBiggestIsland(g, 15)
    island2 = findSecondIsland(g, island, 40)
    island = smoothIsland(g, island)
    island2 = smoothIsland(g, island2)
    if len(island) < 4:
        return findStartSpots(g, n, i+1)

    ratio = n
    if len(island2) > 0:
        ratio = len(island)//len(island2)
    NN = n
    N2 = 0
    if ratio < n:
        NN = 0
        #N2 = 0
        i = 0
        while NN+N2 < n:
            if i%ratio == 0 and i!=0:
                N2+=1
                i = 0
            else:
                NN+=1
                i+=1
    
    #island = flipList(island)
    points = []
    for i in range(NN):
        pos = random.choice(island)
        points.append(pos)
    for i in range(N2):
        pos = random.choice(island2)
        points.append(pos)
    print('starting:',points)
    total = n
    good = []
    Attempts = 0
    for i in range(n):
        good.append(True)
    while total > 0 and Attempts < 20:
        Attempts += 1
        print(Attempts)
        i=0
        for pos in points:
            smallPoints = list(points)
            smallPoints.remove(pos)
            CurrentTotal, Xrange, Yrange = TotalRange(points)
            s = getSurround(g,pos)
            print(pos, s)
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
            points = findStartSpots(g, n, i+1)
    elif n == 2:
        if TotalRange(points)[0] < 5:
            points = findStartSpots(g, n, i+1)
    print('final points',points)
    #points = flipList(points)
    return points

def int_to_bool_list(num):
    return [bool(num & (1<<n)) for n in range(8)][::-1]

def intToList(x, width):
    l = []
    for v in x:
        print(v)
        l+=int_to_bool_list(v)
    l2 = []
    for i in range(len(l)//width):
            l2.append(l[(i*width):((i+1)*width)])
    return l2


def generateMapFromImage(MAP):
    im = Image.open(MAP)    
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    grid = []
    for x in range(width):
        l = []
        for y in range(height):
            pixel = pix[y,x]
            if pixel == (0,0,255,255):
                l.append(True)
            else:
                l.append(False)
        grid.append(l)
    return grid

def printGrid(grid):
    for l in grid:
        t = ''
        for c in l:
            if c:
                t += " "
            else:
                t += "X"
        print(t)

def findStartSpotsFromMap(MAP):
    im = Image.open(MAP)    
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    grid = []

    startSpots = []
    
    for x in range(width):
        for y in range(height):
            pixel = pix[y,x]
            if pixel == (255,0,0,255):
                startSpots.append([y,x])
    #For Bots
    for x in range(width):
        for y in range(height):
            pixel = pix[y,x]
            if pixel == (255,255,255,255):
                startSpots.append([y,x])

    print("START SPOTS", startSpots)
    return startSpots

def getAICountFromMap(MAP):
    im = Image.open(MAP)    
    pix = im.load()
    width = im.size[0]
    height = im.size[1]

    AICount = 0
    for x in range(width):
        for y in range(height):
            pixel = pix[y,x]
            if pixel == (255,255,255,255):
                AICount += 1
    return AICount

def getPlayerCountFromMap(MAP):
    im = Image.open(MAP)    
    pix = im.load()
    width = im.size[0]
    height = im.size[1]

    PlayerCount = 0
    for x in range(width):
        for y in range(height):
            pixel = pix[y,x]
            if pixel == (255,0,0,255):
                PlayerCount += 1
    return PlayerCount

def getWidthAndHeight(MAP):
    im = Image.open(MAP) 
    width = im.size[0]
    height = im.size[1]
    return width, height
