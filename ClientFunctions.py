import GlobalVaribles as GV
from UnitDB import UnitDB

def Lerp(a,b,t):
    return a+t*(b-a)

def LerpPoint(a,b,t):
    return (Lerp(a[0],b[0],t),Lerp(a[1],b[1],t))

def intPoint(p):
    return (int(p[0]),int(p[1]))

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