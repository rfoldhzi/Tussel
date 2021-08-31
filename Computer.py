#Attack
#Build
#-Move
#Resources

import random, copy, methods
import numpy as np
from UnitDB import UnitDB

g = None
Grid = []

buildBlackList = ["docks", "wall", 'rocket','radar tower']

def optimizeResources(game, player):
    l = {}
    for u in game.units[player]:
        if ("resources" in u.possibleStates) and (u.state == None or u.state == "resources"):
            l[u] = max(u.resourceGen.values())
    l = {k: v for k, v in sorted(l.items(), key=lambda item: item[1])}
    r = copy.copy(game.resources[player])
    for u in l:
        options = []
        for v in u.resourceGen:
            if u.resourceGen[v] > 0:
                options.append(v)
        print("OPTIONS",options)
        if len(options) == 1:
            u.state = "resources"
            u.stateData = options[0]
            r[options[0]] += u.resourceGen[options[0]]
        elif len(options) > 0:
            choice = None
            if u.resourceGen[options[0]] == u.resourceGen[options[1]]:
                if min(r, key=r.get) in options:
                    print("RIOGHT HERE", player, choice)
                    choice = min(r, key=r.get)
                else:
                    choice = random.choice(options)
            else:
                s = sum(u.resourceGen.values())
                d2 = {k: v/float(s) for k, v in u.resourceGen.items()}
                choice = np.random.choice(list(d2.keys()), p=list(d2.values()))
            u.state = "resources"
            u.stateData = choice
            r[choice] += u.resourceGen[choice]
          
        

def randomizeResources(game, player):
    l = []
    for u in game.units[player]:
        if ("resources" in u.possibleStates) and (u.state == None or u.state == "resources"):
            l.append(u)
    for u in l:
        options = []
        for v in u.resourceGen:
            if u.resourceGen[v] > 0:
                options.append(v)
        u.state = "resources"
        u.stateData = random.choice(options)

def getRangeCircles(unit, anyBlock = False, built = False):#Could be more effiecint
    sp = unit.range
    spaces = []
    for x in range(unit.position[0]-sp, unit.position[0]+1+sp):
        for y in range(unit.position[1]-sp, unit.position[1]+1+sp):
            if x >= 0 and y >= 0 and y<g.height and x<g.width:#If within board:
                if anyBlock or g.getAnyUnitFromPos(x,y) == None:
                    water = Grid[y][x]
                    if built:
                        t = UnitDB[built].get('type') or 0
                        if (water == (t == 'boat')) or t == "aircraft":
                            spaces.append([x,y])
                    else:
                        if anyBlock or (not water):
                            spaces.append([x,y])
    return spaces

def getAttacks(game, unit, player):
    if not 'attack' in unit.possibleStates:
        return []
    spaces = getRangeCircles(unit, True)
    finalTarget = []
    for pos in spaces:
        u = game.getAnyUnitFromPos(pos[0],pos[1])
        if u:
            goodToAdd = True
            if u == unit:
                goodToAdd = False
            if 'onlyHit' in unit.abilities:
                if not (u.type in unit.abilities['onlyHit']):
                    goodToAdd = False
            if goodToAdd and (game.checkFriendlyPlayer(u, player)):
                goodToAdd = False
            if goodToAdd:
                finalTarget.append(u)
    return finalTarget

def randomizeAttacks(game, player):
    for u in game.units[player]:
        targets = getAttacks(game, u, player)
        if len(targets) > 0:
            u.state = "attack"
            u.stateData = random.choice(targets)
        else:
            u.state = None

def randomBuild(game, player):
    resources = copy.copy(game.resources[player])
    for u in game.units[player]:
        if 'build' in u.possibleStates and u.state == None:
            if getattr(u, 'maxPopulation', False):
                if u.population >= u.maxPopulation:
                    continue
            options = []
            for built in UnitDB[u.name]['possibleBuilds']:
                cost = UnitDB[built]['cost']
                good = True
                for v in cost:
                    if resources[v] < cost[v]:
                        good= False
                if not good:
                    continue
                buildHexes = getRangeCircles(u, built = built)
                if len(buildHexes) == 0:
                    continue
                options.append(built)
            if len(options) > 0:
                u.state = "build"
                built = random.choice(options)
                buildHexes = getRangeCircles(u, built = built)
                u.stateData = [random.choice(buildHexes),built]
                for v in cost:
                    resources[v] -= cost[v]

def betterBuild(game, player):
    resources = copy.copy(game.resources[player])

    limitedBuildings = ["mine", "barracks", "power plant","nuclear plant"]
    miniBanList = []
    counts = {}

    usedSpaces = []
    for u in game.units[player]:
        if not u.name in counts:
            counts[u.name] = 0
        counts[u.name] += 1
    for v in limitedBuildings:
        if v in counts and counts[v]>len(game.units[player])/7 + 2:
            miniBanList.append("mine")
    for u in game.units[player]:
        if 'build' in u.possibleStates and u.state == None:
            if getattr(u, 'maxPopulation', False):
                if u.population >= u.maxPopulation:
                    continue
            options = []
            for built in UnitDB[u.name]['possibleBuilds']:
                if built in buildBlackList or built in miniBanList:
                    continue
                cost = UnitDB[built]['cost']
                good = True
                for v in cost:
                    if resources[v] < cost[v]:
                        good= False
                if not good:
                    continue
                buildHexes = getRangeCircles(u, built = built)
                requirement = 1
                t = UnitDB[built].get('type') or 0
                if t == 'building':
                    requirement = 2
                if len(buildHexes) < requirement:
                    continue
                options.append(built)
            if len(options) > 0:
                u.state = "build"
                built = random.choice(options)
                if len(game.units[player]) == 1 and "construction worker" in UnitDB[u.name]['possibleBuilds']:
                    built = "construction worker"
                buildHexes = getRangeCircles(u, built = built)
                pos = random.choice(buildHexes)
                u.stateData = [pos,built]
                usedSpaces.append(pos)
                for v in cost:
                    resources[v] -= cost[v]
    return usedSpaces

def getMoveCircles(unit,usedSpaces = [], openSpaces = []):#Could be more effiecint
    if not 'move' in unit.possibleStates:
        return []
    sp = unit.speed
    spaces = [unit.position]
    #pos = unit.position
    for i in range(sp):
        newSpaces = []
        for pos in spaces:
            for x in range(pos[0]-1, pos[0]+2):
                for y in range(pos[1]-1, pos[1]+2):
                    if ([x,y] not in spaces) and x >= 0 and y >= 0 and y<g.height and x<g.width:#If within board:
                        p = [x,y]
                        if g.getAnyUnitFromPos(x,y) == None or (p in openSpaces):
                            water = Grid[y][x]
                            if (water == (unit.type == 'boat')) or unit.type == "aircraft":
                                if not p in usedSpaces:
                                    newSpaces.append(p)
        spaces += newSpaces
    spaces.pop(0)
    return spaces

def randomMove(game, player):
    for u in game.units[player]:
        if 'move' in u.possibleStates and u.state == None:
            moveCircles = getMoveCircles(u)
            if len(moveCircles) > 0:
                u.state = "move"
                u.stateData = random.choice(moveCircles)
def betterRandomMove(game, player,spaces):
    openSpaces = []
    for u in game.units[player]:
        if 'move' in u.possibleStates and u.state == None:
            moveCircles = getMoveCircles(u,spaces,openSpaces)
            if len(moveCircles) > 0:
                openSpaces.append(u.position)
                u.state = "move"
                u.stateData = random.choice(moveCircles)
                print(player, 'moving to ', u.stateData)

def CurrentAI(game, player):
    betterActions(game, player)

def randomActions(game, player):
    global g, Grid
    g = game
    Grid = methods.intToList(game.intGrid, game.width)
    randomizeAttacks(game, player)
    randomBuild(game, player)
    randomizeResources(game, player)
    randomMove(game, player)


def betterActions(game, player):
    global g, Grid
    g = game
    Grid = methods.intToList(game.intGrid, game.width)
    randomizeAttacks(game, player)
    spaces = betterBuild(game, player)
    print("Spaces buidling at",player,spaces)
    if random.randint(1,2) == 1:
        optimizeResources(game, player)
        betterRandomMove(game, player,spaces)
    else:
        betterRandomMove(game, player,spaces)
        optimizeResources(game, player)

    
