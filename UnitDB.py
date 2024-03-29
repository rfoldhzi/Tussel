UnitDB = {
    'soldier':{
        'cost': {'gold':20},
    },
    'scout':{
        'cost': {'gold':30},
        'speed':2,
        'defense':1
    },
    'heavy':{
        'cost': {'gold':50,'metal':25},
        'health': 12,
        'attack':3,
        'resourceGen':{
            "gold": 8,
            "metal": 0,
            "energy": 0
        }
    },
    'defender':{
        'cost': {'gold':20,'metal':10},
        'possibleBuilds': [],
        'possibleStates': ['move','attack','build'],
        'health': 15,
        'defense':3,
    },
    'sniper':{
        'cost': {'gold':125,'metal':20},
        'health': 7,
        'attack':3,
        'defense':1,
        'range':3,
        'abilities':{'onlyHit':['trooper', 'bot']},
    },
    'rocket':{
        'cost': {'gold':60,'metal':40},
        'possibleStates': ['move','attack'],
        'attack':3,
        'range':2,
        'resourceGen':{"gold": 0},
        'abilities':{'onlyHit':['vehicle','aircraft']},
    },
    'brute':{
        'cost': {'gold':50},
        'health': 30,
        'defense':1,
    },
    'medic':{
        'cost': {'gold':50},
        'possibleStates': ['move','heal','resources'],
        'heal':10,
        'abilities':{'onlyHeal':['trooper']},
    },
    'general':{
        'cost': {'gold':300},
        'possibleStates': ['move','attack'],
        'abilities':{'buff':['attack', 1.5]},
    },
    'bot':{
        'cost': {'metal':25,'energy':5},
        'type': 'bot',
        'resourceGen':{
            "gold": 5,
            "metal": 5,
            "energy": 5
        }
    },
    'minibot':{
        'cost': {'metal':8,'energy':2},
        'possibleStates': ['move','attack'],
        'type': 'bot',
        'health': 5,
        'attack':1,
        'defense':1,
        'resourceGen':{
            "gold": 0,
            "metal": 0,
            "energy": 0
        }
    },
    'mech':{
        'cost': {'gold':20,'metal':80,'energy':10},
        'possibleBuilds': ['minibot'],
        'possibleStates': ['move','attack','resources', 'build'],
        'type': 'vehicle',
        'health': 15,
        'defense': 3,
        'population':2,
        'resourceGen':{
            "gold": 4,
            "metal": 5,
            "energy": 0
        }
    },
    'town':{
        'cost': {'gold':150, 'metal':150, 'energy':150},
        'possibleBuilds': ['soldier', 'construction worker','miner', 'electric engineer'],
        'possibleStates': ['resources', 'build','research'],
        'type': 'building',
        'health': 50,
        'population':4,
        'abilities':{'costly':1.75},
        'resourceGen':{
            "gold": 10,
            "metal": 10,
            "energy": 10
        }
    },
    'metropolis':{
        'cost': {'gold':250, 'metal':250, 'energy':250},
        #'possibleBuilds': ['soldier','heavy','construction worker','miner', 'electric engineer','medic', 'agent'],
        'possibleBuilds': ['hall of heroes'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 75,
        'population':5,
        'abilities':{'costly':2},
        'resourceGen':{
            "gold": 25,
            "metal": 25,
            "energy": 25
        }
    },
    'metropolis expansion':{
        'cost': {'gold':150, 'metal':150, 'energy':150},
        #'possibleBuilds': ['soldier','heavy','construction worker','miner', 'electric engineer','medic', 'agent'],
        'possibleBuilds': ['hall of heroes'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 30,
        'population':5,
        'abilities':{'costly':1.5},
        'resourceGen':{
            "gold": 10,
            "metal": 10,
            "energy": 10
        }
    },
    'construction worker':{
        'cost': {'gold':20},
        'possibleBuilds': ['town','barracks','turret','factory','tank factory','docks','wall','radar tower','workshop'],
        'possibleStates': ['move','resources', 'build'],
        'resourceGen':{
            "gold": 4,
            "metal": 8,
            "energy": 0
        }
    },
    'crane':{
        'cost': {'gold':10, 'metal':50, 'energy':10},
        'possibleBuilds': ['town','factory','tank factory','research center','docks','fort','hospital'],
        'possibleStates': ['move','resources', 'build'],
        'type': 'vehicle',
        'health':20,
        'defense':3,
        'resourceGen':{
            "gold": 0,
            "metal": 8,
            "energy": 0
        }
    },
    'mechanic':{
        'cost': {'gold':60, 'energy':5},
        'possibleBuilds': ['bot'],
        'possibleStates': ['move','resources', 'build', 'heal'],
        'population':2,
        'abilities':{'onlyHeal':['vehicle', 'bot']},
        'resourceGen':{
            "gold": 0,
            "metal": 0,
            "energy": 5
        }
    },
    'miner':{
        'cost': {'gold':20},
        'possibleBuilds': ['mine'],
        'possibleStates': ['move','resources', 'build'],
        'resourceGen':{
            "gold": 10,
            "metal": 8,
            "energy": 0
        }
    },
    'mine':{
        'cost': {'gold':20, 'metal':50},
        'possibleStates': ['resources'],
        'type': 'building',
        'health': 15,
        'defense': 1,
        'abilities':{'costly':1.5},
        'resourceGen':{
            "gold": 30,
            "metal": 10,
            "energy": 0
        }
    },
    'mine shaft':{
        'cost': {'gold':20, 'metal':50},
        'possibleStates': ['none'],
        'type': 'building',
        'health': 15,
        'defense': 1,
        'abilities':{'buff':['production',['mine'], 1.5],
                     'costly':1.75},
        'resourceGen':{
            "gold": 0
        }
    },
    'power grid':{
        'cost': {'gold':50, 'metal':50, 'energy':50},
        'possibleStates': ['none'],
        'type': 'building',
        'health': 15,
        'defense': 1,
        'abilities':{'buff':['production',['power plant', 'nuclear plant'], 1.5],
                     'costly':1.75},
        'resourceGen':{
            "gold": 0
        }
    },
    'recycler':{
        'cost': {'gold':20, 'metal':50, 'energy':10},
        'possibleStates': ['none'],
        'type': 'building',
        'health': 15,
        'defense': 1,
        'abilities':{'buff':['production',['factory'], 1.5],
                     'costly':1.75},
        'resourceGen':{
            "gold": 0
        }
    },
    'shield generator':{
        'cost': {'metal':20,'energy':100},
        'possibleStates': ['none'],
        'type': 'building',
        'health': 15,
        'defense': 0.5,
        'abilities':{'buff':['defense', 2]},
        'resourceGen':{
            "gold": 0,
        }
    },
    'turret':{
        'cost': {'metal':100, 'energy':50},
        'possibleStates': ['attack'],
        'type': 'building',
        'attack': 3,
        'range': 2,
        'health': 15,
    },
    'radar tower':{
        'cost': {'gold':10,'metal':30, 'energy':10},
        'possibleStates': ['none'],
        'type': 'building',
        'range': 3,
        'abilities':{'closebuild':1},
        'resourceGen':{
            "gold": 0,
        }
    },
    'fort':{
        'cost': {'gold':100 ,'metal':250, 'energy':100},
        'possibleStates': ['attack','build'],
        'possibleBuilds': ['soldier', 'jeep','medic'],
        'type': 'building',
        'attack': 3,
        'defense': 3,
        'range': 2,
        'health': 30,
        'resourceGen':{
            "metal": 20,
            "energy": 10
        }
    },
    'electric engineer':{
        'cost': {'gold':20},
        'possibleBuilds': ['power plant','nuclear plant'],
        'possibleStates': ['move','resources', 'build'],
        'resourceGen':{
            "gold": 0,
            "metal": 0,
            "energy": 5
        }
    },
    'power plant':{
        'cost': {'gold':10, 'metal':50, 'energy': 20},
        'possibleStates': ['resources'],
        'type': 'building',
        'health': 15,
        'defense': 1,
        'abilities':{'costly':1.5},
        'resourceGen':{
            "gold": 10,
            "metal": 0,
            "energy": 20
        }
    },
    'nuclear plant':{
        'cost': {'gold':100, 'metal':50, 'energy': 50},
        'possibleStates': ['resources'],
        'type': 'building',
        'health': 20,
        'defense': 1,
        'abilities':{'costly':1.75},
        'resourceGen':{
            "gold": 10,
            "metal": 0,
            "energy": 40
        }
    },
    'factory':{
        'cost': {'gold':20, 'metal':50, 'energy':10},
        'possibleBuilds': ['bot','minibot'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 15,
        'abilities':{'costly':1.5},
        'resourceGen':{
            "gold": 0,
            "metal": 30,
            "energy": 0
        }
    },
    'workshop':{
        'cost': {'gold':10, 'metal':100, 'energy':10},
        'possibleBuilds': ['bot','mechanic','mech', 'blob'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 15,
        'defense': 1,
        'abilities':{'costly':1.3},
        'resourceGen':{
            "gold": 0,
            "metal": 8,
            "energy": 5
        }
    },
    'hospital':{
        'cost': {'gold':80, 'metal':50, 'energy':20},
        'possibleBuilds': ['medic'],
        'possibleStates': ['build','heal'],
        'type': 'building',
        'health': 20,
        'defense': 1,
        'heal':15,
        'population':2,
        'abilities':{'onlyHeal':['trooper']},
        'resourceGen':{
            "gold": 0,
        }
    },
    'barracks':{
        'cost': {'gold':100, 'metal':10},
        #'possibleBuilds': ['soldier','scout','heavy','defender','sniper','rocket','brute','medic'],
        'possibleBuilds': ['soldier','scout','heavy','medic'],
        'possibleStates': ['build'],
        'type': 'building',
        'health': 15,
        'abilities':{'costly':1.2},
        'resourceGen':{
            "gold": 0,
        }
    },
    'tank factory':{
        'cost': {'gold':150, 'metal':50, 'energy':10},
        #'possibleBuilds': ['tank','heavy tank','artillery','jeep','crane','mobile fortress'],
        'possibleBuilds': ['tank','jeep','crane'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 20,
        'abilities':{'costly':1.5},
        'resourceGen':{
            "gold": 0,
            "metal": 10,
            "energy": 0
        }
    },
    'tank':{
        'cost': {'gold':70, 'metal':100, 'energy':20},
        'possibleStates': ['move','attack'],
        'type': 'vehicle',
        'health':20,
        'defense':3,
        'resourceGen':{"gold": 0}
    },
    'heavy tank':{
        'cost': {'gold':100, 'metal':200, 'energy':50},
        'possibleStates': ['move','attack'],
        'type': 'vehicle',
        'health':25,
        'attack':2.5,
        'defense':4,
        'resourceGen':{"gold": 0}
    },
    'artillery':{
        'cost': {'gold':120, 'metal':150, 'energy':50},
        'possibleStates': ['move','attack'],
        'type': 'vehicle',
        'attack':3,
        'range':3,
        'defense':1,
        'resourceGen':{"gold": 0},
        'abilities':{'onlyHit':['building']},
    },
    'jeep':{
        'cost': {'gold':20, 'metal':40, 'energy':20},
        'possibleStates': ['move','attack','transport'],
        'type': 'vehicle',
        'speed':2,
        'health':12,
        'population':1,
        'abilities':{'transport':['trooper']},
        'resourceGen':{"gold": 0}
    },
    'mobile fortress':{
        'cost': {'gold':150, 'metal':200, 'energy':100},
        'possibleBuilds': ['soldier','tank'],
        'possibleStates': ['move','attack','resources', 'build'],
        'type': 'vehicle',
        'health': 25,
        'defense': 3,
        'population':3,
        'resourceGen':{
            "gold": 20,
            "metal": 40,
            "energy": 0
        }
    },
    'airport':{
        'cost': {'gold':200, 'metal':70, 'energy':20},
        #'possibleBuilds': ['plane','helicopter','bomber'],
        'possibleBuilds': ['plane'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 15,
        'abilities':{'costly':1.25},
        'resourceGen':{
            "metal": 20,
        }
    },
    'plane':{
        'cost': {'gold':100, 'metal':100, 'energy':20},
        'possibleStates': ['move','attack'],
        'type': 'aircraft',
        'health':15,
        #'speed':3,
        'speed':2,
        'range':2,
        'defense':1,
        'resourceGen':{"gold": 0}
    },
    'helicopter':{
        'cost': {'gold':100, 'metal':50, 'energy':20},
        #'possibleBuilds': ['soldier','construction worker'],
        'possibleStates': ['move','attack','transport'],
        'type': 'aircraft',
        'speed':2,
        'defense':1,
        'attack':1.5,
        'population':1,
        'abilities':{'transport':['trooper','bot']},
        'resourceGen':{"gold": 0}
    },
    'chinook':{
        'cost': {'gold':100, 'metal':100, 'energy':20},
        #'possibleBuilds': ['tank','crane','heavy'],
        'possibleStates': ['move','attack','transport'],
        'type': 'aircraft',
        'speed':2,
        'defense':1.5,
        'attack':2,
        'population':2,
        'abilities':{'transport':['trooper','bot','vehicle']},
        'resourceGen':{"gold": 0}
    },
    'bomber':{
        'cost': {'gold':100, 'metal':150, 'energy':50},
        'possibleStates': ['move','attack'],
        'type': 'aircraft',
        'health':15,
        'speed':2,
        'defense':1,
        'attack':3,
        'resourceGen':{"gold": 0}
    },
    'sea plane':{
        'cost': {'gold':100, 'metal':50, 'energy':20},
        'possibleStates': ['move','attack'],
        'type': 'aircraft',
        'health':15,
        'speed':2,
        'range':2,
        'defense':1.5,
        'attack':3,
        'resourceGen':{"gold": 0},
        'abilities':{'onlyHit':['boat','aircraft']},
    },
    'docks':{
        'cost': {'gold':50, 'metal':100},
        'possibleBuilds': ['boat', 'transport boat'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 15,
        'defense':1,
        'abilities':{'costly':1.2},
        'resourceGen':{
            "gold": 10,
        }
    },
    'boat':{
        'cost': {'gold':20, 'metal':25},
        'possibleStates': ['move','attack'],
        'type': 'boat',
        'resourceGen':{"gold": 0}
    },
    'transport boat':{
        'cost': {'gold':25, 'metal':25},
        'possibleStates': ['move','resources','transport'],
        #'possibleBuilds': ['soldier','construction worker'],
        'type': 'boat',
        'population':2,
        'abilities':{'transport':['trooper','bot']},
        'resourceGen':{"gold": 2}
    },
    'aircraft carrier':{
        'cost': {'gold':50, 'metal':300},
        'possibleBuilds': ['plane'],
        'possibleStates': ['move','attack', 'build'],
        'type': 'boat',
        'health': 25,
        'range':2,
        'defense': 3,
        'population':2,
        'resourceGen':{
            "gold": 0
        }
    },
    'seige boat':{
        'cost': {'gold':100, 'metal':100},
        'possibleBuilds': ['soldier'],
        'possibleStates': ['move', 'build'],
        'type': 'boat',
        'health': 15,
        'defense': 3,
        'population':3,
        'abilities':{'multibuild':4},
        'resourceGen':{
            "gold": 0
        }
    },
    'submarine':{
        'cost': {'gold':50, 'metal':50,'energy':50},
        'possibleStates': ['move','attack'],
        'type': 'boat',
        'attack': 3.5,
        'resourceGen':{"gold": 0},
        'abilities':{'onlyHit':['boat','building']},
    },
    'floating fortress':{
        'cost': {'gold':75, 'metal':350,'energy':150},
        'possibleBuilds': ['boat','transport boat'],
        'possibleStates': ['move','attack', 'build'],
        'type': 'boat',
        'health': 25,
        'defense': 3.5,
        'population':2,
        'resourceGen':{
            "gold": 0
        }
    },
    
    'wall':{
        'cost': {'metal':25},
        'possibleStates': ['none'],
        'type': 'building',
        'health': 20,
        'defense': 3,
        'resourceGen':{
            "gold": 0,
        }
    },
    'blob':{
        'cost': {'energy':20},
        'possibleBuilds': ['blob'],
        'possibleStates': ['move','attack','resources', 'build'],
        'attack':1,
        'defense':1,
        'population':1,
        'resourceGen':{
            "gold": 0,
            "metal": 0,
            "energy": 2
        }
    },
    'slime':{
        'cost': {'energy':25},
        'possibleStates': ['move','attack','resources'],
        'abilities':{'takeover':'slime'},
        'resourceGen':{
            "gold": 0,
            "metal": 0,
            "energy": 3
        }
    },
    'agent':{
        'cost': {'gold':50, 'energy':20},
        #'possibleBuilds': ['experimental facility', 'hall of heroes'],
        'possibleBuilds': ['hall of heroes'],
        'possibleStates': ['attack','move', 'build'],
        'resourceGen':{
            "gold": 0
        }
    },
    'research center':{
        'cost': {'gold':100, 'metal':100, 'energy':100},
        'possibleBuilds': [],
        'possibleStates': ['resources', 'build', 'research'],
        'health':15,
        'type': 'building',
        'population':2,
        'abilities':{'costly':1.4},
        'resourceGen':{
            "energy": 10
        }
    },
    'experimental facility':{
        'cost': {'gold':200, 'metal':100, 'energy':200},
        #'possibleBuilds': ['sonic cannon', 'ultrabot', 'invinsa tank'],
        'possibleBuilds': [],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'defense': 1,
        'population':2,
        'abilities':{'costly':1.5},
        'resourceGen':{
            "energy": 40
        }
    },
    'sonic cannon':{
        'cost': {'gold':100, 'metal':250, 'energy':500},
        'possibleStates': ['move','attack'],
        'type': 'vehicle',
        'health':5,
        'range':2,
        'attack':6,
        'defense':1,
        'resourceGen':{"gold": 0}
    },
    'ultrabot':{
        'cost': {'gold':500,'metal':100,'energy':250},
        'possibleStates': ['move','attack','build'],
        'possibleBuilds': ['bot','minibot'],
        'type': 'vehicle',
        'health': 25,
        'attack': 4,
        'defense': 4,
        'population':2,
        'resourceGen':{
            "gold": 0
        }
    },
    'invinsa tank':{
        'cost': {'gold':250, 'metal':500, 'energy':100},
        'possibleStates': ['move','attack'],
        'type': 'vehicle',
        'health':30,
        'attack':2,
        'defense':6,
        'resourceGen':{"gold": 0}
    },
    'hall of heroes':{
        'cost': {'gold':300, 'metal':50, 'energy':50},
        'possibleBuilds': ['the hunter', 'king blob', 'the recruiter'],
        'possibleStates': ['build'],
        'type': 'building',
        'health':20,
        'population':1,
        'abilities':{'costly':2},
        'resourceGen':{
            "gold": 0
        }
    },
    'the hunter':{
        'cost': {'gold':200,'metal':50},
        'attack':4,
        'defense':1,
        'range':4,
        'abilities':{'onlyHit':['trooper', 'bot']},
        'resourceGen':{
            "gold": 8
        }
    },
    'king blob':{
        'cost': {'energy':100},
        'possibleBuilds': ['blob'],
        'possibleStates': ['move','attack','resources', 'build'],
        'health':20,
        'resourceGen':{
            "gold": 0,
            "metal": 0,
            "energy": 10
        }
    },
    'king of the blob nation of the southeastern blob continent on the blob planet hiding behind jupiter':{
        'cost': {'energy':153},
        'possibleBuilds': ['blob', 'king blob'],
        'possibleStates': ['move','attack','resources', 'build'],
        'health':10,
        'attack':0.5,
        'defense':3.5,
        'range':2,
        'resourceGen':{
            "gold": 0,
            "metal": 0,
            "energy": 20
        }
    },
    'king slime':{
        'cost': {'energy':200},
        'possibleBuilds': ['slime'],
        'possibleStates': ['move','attack','resources', 'build'],
        'health':20,
        'abilities':{'takeover':'slime'},
        'resourceGen':{
            "gold": 0,
            "metal": 0,
            "energy": 10
        }
    },
    'ninja':{
        'cost': {'gold':200,'metal':10},
        'possibleStates': ['move','attack'],
        'attack':3.5,
        'defense':2,
        'speed':2,
    },
    'king':{
        'cost': {'gold':200},
        'possibleBuilds': ['castle'],
        'possibleStates': ['move','attack','resources', 'build'],
        'health':15,
        'population':1,
        'resourceGen':{
            "gold": 20
        }
    },
    'castle':{
        'cost': {'gold':100 ,'metal':100},
        'possibleStates': ['attack','resources','build'],
        'possibleBuilds': ['knight'],
        'type': 'building',
        'defense': 3,
        'health': 20,
        'population':4,
        'resourceGen':{
            "gold": 10,
        }
    },
    'knight':{
        'cost': {'gold':50 ,'metal':50},
        'health': 15,
        'attack':2.5,
        'defense':4,
        'abilities':{'charge':0},
        'resourceGen':{
            "gold": 10
        },
    },
    'calvary':{
        'cost': {'gold':35},
        'speed':2,
        'abilities':{'charge':0},
    },
    'the recruiter':{
        'cost': {'gold':300},
        'possibleBuilds': ['recruited soldier'],
        'possibleStates': ['move','attack','resources', 'build'],
        'population':3,
        'resourceGen':{
            "gold": 8,
            "metal": 0,
            "energy": 0,
        }
    },
    'recruited soldier':{
        'cost': {'gold':0},
        'attack':2.5,
        'defense':2.5,
        'resourceGen':{
            "gold": 0
        }
    },
    'defense platform':{
        'cost': {'gold':50 ,'metal':150, 'energy':150},
        'possibleStates': ['attack','build'],
        'possibleBuilds': [],
        'type': 'building',
        'attack': 1.5,
        'defense': 3,
        'range': 2,
        'health': 20,
        'abilities':{'costly':1.2},
        'resourceGen':{"gold": 0}
    },
    'missile':{
        'cost': {'metal':30, 'energy':5},
        'possibleStates': ['move','attack'],
        'type': 'aircraft',
        'health':3,
        'speed':2,
        'range':1,
        'attack':3.5,
        'defense':1,
        'abilities':{'kamikaze':0,'decay':1},
        'resourceGen':{"gold": 0}
    },

    #Wild Life Faction
    'tree':{
        'cost': {'gold':50, 'metal':50, 'energy':50},
        'possibleBuilds': ['hyena', 'bear','fish'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 25,
        'population':5,
        'resourceGen':{
            "gold": 10,
            "metal": 10,
            "energy": 5
        }
    },
    'hyena':{
        'cost': {'metal':10},
        'health': 8,
    },
    'bear':{
        'cost': {'gold':20},
        'possibleBuilds': ['cave','tree'],
        'possibleStates': ['attack','move','resources', 'build'],
        'health': 12,
        'attack':3,
        'population':2,
        'resourceGen':{
            "gold": 4,
            "metal": 4,
            "energy": 0
        }
    },
    'fish':{
        'cost': {'energy':10},
        'possibleBuilds': ['pond'],
        'possibleStates': ['move','build','resources'],
        'type': 'boat',
        'resourceGen':{"energy": 3}
    },
    'pond':{
        'cost': {'gold':20, 'energy':30},
        'possibleBuilds': ['snake','fish'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'population':3,
        'resourceGen':{
            "gold": 10,
            "metal": 0,
            "energy": 10
        }
    },
    'cave':{
        'cost': {'gold':10, 'metal':30},
        'possibleBuilds': ['hyena', 'bats'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 15,
        'population':2,
        'resourceGen':{
            "gold": 0,
            "metal": 20,
            "energy": 0
        }
    },
    'bats':{
        'cost': {'gold':8},
        'possibleStates': ['move','attack'],
        'type': 'aircraft',
        'health':7,
        'speed':2,
        'defense':1,
        'resourceGen':{"gold": 0}
    },
    'snake':{
        'cost': {'gold':20,'energy':10},
        'possibleStates': ['move','attack'],
        'attack':3.5,
        'abilities':{'onlyHit':['trooper']},
        'resourceGen':{"gold": 8}
    },
    #Bots Faction
    'bot fortress':{
        'cost': {'gold':0, 'metal':150, 'energy':150},
        'possibleBuilds': ['servitor'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 50,
	'defense': 3,
        'population':4,
        'resourceGen':{
            "gold": 0,
            "metal": 20,
            "energy": 20
        }
    },
    'servitor':{
        'cost': {'gold':0, 'metal':40, 'energy':40},
        'possibleBuilds': ['bot defense platform', 'bot factory', 'bot power core'],
        'possibleStates': ['move', 'attack', 'build'],
        'type': 'aircraft',
        'health': 20,
	'defense': 3,
        'resourceGen':{
            "gold": 0
        }
    },
    'bot defense platform':{
        'cost': {'gold':0, 'metal':100, 'energy':60},
        'possibleStates': ['attack', 'resources'],
        'type': 'building',
        'health': 15,
	'range': 3,
	'attack': 3,
	'defense': 3.5,
        'resourceGen':{
            "gold": 10,
            "metal": 0,
            "energy": 10
        }
    },
    'bot power core':{
        'cost': {'gold':0, 'metal':60, 'energy':60},
        'possibleBuilds': ['bot engineer'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 20,
        'population':3,
        'resourceGen':{
            "gold": 0,
            "metal": 10,
            "energy": 50
        }
    },
    'bot engineer':{
        'cost': {'gold':0, 'metal':40, 'energy':40},
        'possibleBuilds': ['bot', 'bot factory', 'bot power station'],
        'possibleStates': ['move', 'resources', 'build'],
        'type': 'bot',
        'health': 10,
        'population':3,
        'resourceGen':{
            "gold": 5,
            "metal": 10,
            "energy": 0
        }
    },
    'bot power station':{
        'cost': {'gold':0, 'metal':40, 'energy':60},
        'possibleStates': ['resources'],
        'type': 'building',
        'health': 20,
        'resourceGen':{
            "gold": 5,
            "metal": 10,
            "energy": 30
        }
    },
    'bot factory':{
        'cost': {'gold':0, 'metal':40, 'energy':40},
        'possibleBuilds': ['bot', 'mech', 'bot engineer'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 17,
        'population':4,
        'abilities':{'costly':1.1},
        'resourceGen':{
            "gold": 10,
            "metal": 30,
            "energy": 5
        }
    },
    #Plant Faction
    'plant base':{
        'cost': {'energy':200},
        'possibleBuilds': ['walking roots'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 8,
        'population':3,
        'abilities':{'deathSpawn':'mad plant base'},
        'resourceGen':{
            "energy": 10
        }
    },
    'mad plant base':{
        'cost': {'gold':0},
        'possibleBuilds': ['seed'],
        'possibleStates': ['build'],
        'type': 'building',
        'health': 16,
        'range': 4,
        'population':8,
        'abilities':{'multibuild':1},
        'resourceGen':{
            "energy": 0
        }
    },
    'seed':{
        'cost': {'energy':0},
        'possibleBuilds': ['plant base'],
        'possibleStates': ['build'],
        'type': 'building',
        'health': 2,
        'population': 1,
        'abilities':{'deathSpawn':'mad seed',
                     'decay':1},
        'resourceGen':{
            "energy": 0
        }
    },
    'mad seed':{
        'cost': {'energy':0},
        'possibleBuilds': ['plant base'],
        'possibleStates': ['move','build'],
        'type': 'building',
        'health': 2,
        'speed': 2,
        'abilities':{'decay':1},
        'resourceGen':{
            "energy": 0
        }
    },
    'walking roots':{
        'cost': {'energy':10},
        'possibleBuilds': ['flower', 'plant house'],
        'possibleStates': ['move', 'resources', 'build'],
        'health': 5,
        'range': 2,
        'population':2,
        'abilities':{'deathSpawn':'mad walking roots'},
        'resourceGen':{
            "gold": 20,
            "metal": 20,
            "energy": 0
        }
    },
    'mad walking roots':{
        'cost': {'gold':0},
        'possibleStates': ['move', 'attack'],
        'population':3,
        'resourceGen':{
            "gold": 0
        }
    },
    'flower':{
        'cost': {'gold':15},
        'possibleStates': ['resources'],
        'type': 'building',
        'health': 4,
        'abilities':{'deathSpawn':'mad flower'},
        'resourceGen':{
            "metal": 1
        }
    },
    'mad flower':{
        'cost': {'gold':0},
        'possibleStates': ['attack'],
        'type': 'building',
    },
    'plant house':{
        'cost': {'metal':30},
        'possibleBuilds': ['phydent', 'jellyfish'],
        'possibleStates': ['build'],
        'type': 'building',
        'health': 6,
        'population':2,
        'abilities':{'deathSpawn':'mad plant house'},
        'resourceGen':{
            "energy": 0
        }
    },
    'mad plant house':{
        'cost': {'metal':0},
        'possibleBuilds': ['spider'],
        'possibleStates': ['build'],
        'type': 'building',
        'health': 8,
        'population':2,
        'resourceGen':{
            "energy": 0
        }
    },
    'phydent':{
        'cost': {'metal':70},
        'possibleStates': ['move'],
        'type': 'monster',
        'health': 6,
        'abilities':{'deathSpawn':'mad phydent'},
        'resourceGen':{
            "metal": 0
        }
    },
    'mad phydent':{
        'cost': {'metal':0},
        'possibleStates': ['move', 'attack'],
        'type': 'monster',
        'health': 18,
        'attack': 3,
        'defense': 3,
        'resourceGen':{
            "metal": 0
        }
    },
    'jellyfish':{
        'cost': {'gold':30},
        'possibleStates': ['move'],
        'type': 'boat',
        'health': 6,
        'abilities':{'deathSpawn':'mad jellyfish'},
        'resourceGen':{
            "metal": 0
        }
    },
    'mad jellyfish':{
        'cost': {'metal':0},
        'possibleStates': ['move', 'attack'],
        'type': 'boat',
        'health': 12,
        'resourceGen':{
            "metal": 0
        }
    },
    'spider':{
        'cost': {'metal':40,'energy':10},
        'possibleStates': ['move'],
        'health': 3,
        'abilities':{'deathSpawn':'mad spider'},
        'resourceGen':{
            "metal": 0
        }
    },
    'mad spider':{
        'cost': {'metal':0},
        'possibleStates': ['move', 'attack'],
        'health': 7,
        'attack': 3.5,
        'defense': 1,
        'resourceGen':{
            "metal": 0
        }
    },
    #Glob Faction
    'mothership':{
        'cost': {'energy':200},
        'possibleBuilds': ['glob lab','alien fighter','alien transport','mining vessel','alien power generator'],
        'possibleStates': ['move','resources', 'build'],
        'type': 'aircraft',
        'health': 50,
        'resourceGen':{
            "energy": 20, 
            "metal": 10, 
        }
    },

    'alien transport':{
        'cost': {'energy':20, 'metal':30},
        'possibleStates': ['move', 'transport'],
        'type': 'aircraft',
        'health': 10,
        'speed':2,
        'abilities':{'default_transport':['cow','alien foot soldier','alien foot soldier']},
        'resourceGen':{
            "gold": 0
        }
    },

    'cow':{
        'cost': {'gold':20},
        'possibleStates': ['move','resources'],
        'health': 12,
        'resourceGen':{
            "gold": 10,
            "metal": 0,
            "energy": 0
        }
    },

    'alien foot soldier':{
        'cost': {'gold':20},
        'resourceGen':{"gold": 0}
        #Maybe multi-attack ability
    },

    'alien fighter':{
        'cost': {'energy':20, 'metal':30},
        'possibleStates': ['move','attack'],
        'type': 'aircraft',
        'health':10,
        'speed':2,
        'range':2,
        'defense':1,
        'resourceGen':{"gold": 0}
    },

    'mining vessel':{
        'cost': {'metal':5, 'energy':50},
        'possibleStates': ['resources'],
        'type': 'building',
        'health': 18,
        'abilities':{'costly':1.1},
        'resourceGen':{
            "metal": 20
        }
    },

    'alien power generator':{
        'cost': {'metal':50, 'energy':5},
        'possibleStates': ['resources'],
        'type': 'aircraft',
        'health': 18,
        'abilities':{'costly':1.1},
        'resourceGen':{
            "energy": 20
        }
    },

    'glob lab':{
        'cost': {'metal':50, 'energy':10},
        'possibleBuilds': ['glob','glob walker', 'glob symbiote'],
        'possibleStates': ['resources', 'build'],
        'type': 'building',
        'health': 15,
        'abilities':{'costly':1.5},
        'resourceGen':{
            "gold": 5,
        }
    },

    'glob':{
        'cost': {'gold':20},
        'possibleStates':['move', 'attack'],
        'health': 5,
        'abilities':{'deathSpawn':'small glob'},
        'resourceGen':{
            "metal": 0
        }
    },
    'small glob':{
        'cost': {'gold':20},
        'possibleStates':['move', 'attack'],
        'health': 3,
        'attack': 1.5,
        'abilities':{'deathSpawn':'baby glob'},
        'resourceGen':{
            "metal": 0
        }
    },
    'baby glob':{
        'cost': {'gold':20},
        'possibleStates':['move', 'attack'],
        'health': 1,
        'attack': 1,
        'resourceGen':{
            "metal": 0
        }
    },

    'glob walker':{
        'cost': {'gold':40},
        'possibleBuilds': ['glob snake'],
        'possibleStates': ['move', 'resources', 'build'],
        'health': 20,
        'population':2,
        'resourceGen':{
            "energy": 2
        }
    },

    'glob snake':{
        'cost': {'gold':20,'energy':10},
        'possibleStates': ['move','attack'],
        'attack':3.5,
        'abilities':{'onlyHit':['trooper']}
    },

    'glob symbiote':{
        'cost': {'energy':100, 'gold':30},
        'possibleStates': ['move','attack'],
        'type': 'aircraft',
        'health':10,
        'attack':5,
        'speed':2,
        'defense':1,
        'abilities':{'onlyHit':['trooper','bot','aircraft','boat','vehicle','monster'],'convert':0,'kamikaze':0,}
    },

}

TechDB = {
    #RED
    'bionics':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['experimental facility','tough skin'],
    },
    'experimental facility':{
        'cost': 20,
        'time': 1,
        #'ability': [['unlock build', 'agent', 'experimental facility']],
        'ability': [['unlock build', 'metropolis', 'experimental facility']],
        'unlocks': ['sonic cannon','ultrabot','invinsa tank'],
        'quote':"For all those expirments that you're doing",
    },
    'sonic cannon':{
        'cost': 20,
        'time': 2,
        'ability': [['unlock build', 'experimental facility', 'sonic cannon']],
        'unlocks': [],
        'quote':"Don't get me wrong, but what about a glass canon?",
    },
    'invinsa tank':{
        'cost': 20,
        'time': 2,
        'ability': [['unlock build', 'experimental facility', 'invinsa tank']],
        'unlocks': [],
        'quote':"It's practically invincible",
    },
    'ultrabot':{
        'cost': 20,
        'time': 2,
        'ability': [['unlock build', 'experimental facility', 'ultrabot']],
        'unlocks': ['harder','better','faster','stronger'],
        'quote':"Look at this absolute bot",
    },
    'harder':{
        'cost': 20,
        'time': 2,
        'ability': [['stat', 'ultrabot', 'defense', 1]],
        'unlocks': [],
        'deny': ['better','faster','stronger'],
        'quote':"HARDER better faster stronger",
    },
    'better':{
        'cost': 20,
        'time': 3,
        'ability': [['stat', 'ultrabot', 'range', 1]],
        'unlocks': [],
        'deny': ['harder','faster','stronger'],
        'quote':"harder BETTER faster stronger",
    },
    'faster':{
        'cost': 20,
        'time': 3,
        'ability': [['stat', 'ultrabot', 'speed', 1]],
        'unlocks': [],
        'deny': ['better','harder','stronger'],
        'quote':"harder better FASTER stronger",
    },
    'stronger':{
        'cost': 20,
        'time': 2,
        'ability': [['stat', 'ultrabot', 'attack', 0.5]],
        'unlocks': [],
        'deny': ['better','faster','harder'],
        'quote':"harder better faster STRONGER",
    },
    'tough skin':{
        'cost': 20,
        'time': 1,
        'ability': [['stat', 'the hunter', 'defense', 0.5],
                    ['stat', 'cyborg', 'defense', 0.5]],
        'unlocks': ['eagle vision','enhanced muscles'],
        'quote':"Ok. That helps. Right?",
    },
    'eagle vision':{
        'cost': 20,
        'time': 1,
        'ability': [['stat', 'the hunter', 'range', 1]],
        'unlocks': ['bulletproof skin'],
        'quote':"So he can fly?",
    },
    'bulletproof skin':{
        'cost': 20,
        'time': 1,
        'ability': [['stat', 'cyborg', 'defense', 0.5]],
        'unlocks': ['xray vision'],
        'quote':"But it isn't really",
    },
    'xray vision':{
        'cost': 20,
        'time': 2,
        'ability': [['stat', 'cyborg', 'range', 1]],
        'unlocks': [],
        'quote':"But he can't see through walls",
    },
    'enhanced muscles':{
        'cost': 50,
        'time': 1,
        'ability': [['stat', 'the hunter', 'attack', 0.5],
                    ['stat', 'cyborg', 'attack', 0.5]],
        'unlocks': [],
        'deny': ['eagle vision','bulletproof skin','xray vision'],
        'quote':"Going to the gym works too...",
    },

    #Blue
    'time travel':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['time of stealth','land of kings','ancient enemy'],
    },
    'time of stealth':{
        'cost': 20,
        'time': 3,
        'ability': [['unlock build', 'hall of heroes', 'ninja']],
        'unlocks': ['weapons','armor','speed'],
        'quote':"Stealth 100",
    },
    'weapons':{
        'cost': 20,
        'time': 2,
        'ability': [['stat', 'ninja', 'attack', 0.5]],
        'unlocks': [],
        'deny': ['armor','speed'],
        'quote':"Attack 100",
    },
    'armor':{
        'cost': 20,
        'time': 1,
        'ability': [['stat', 'ninja', 'defense', 0.5]],
        'unlocks': [],
        'deny': ['weapons','speed'],
        'quote':"Armor 100",
    },
    'speed':{
        'cost': 20,
        'time': 1,
        'ability': [['stat', 'ninja', 'speed', 1]],
        'unlocks': [],
        'deny': ['armor','weapons'],
        'quote':"Speed 100",
    },
    'land of kings':{
        'cost': 20,
        'time': 1,
        'ability': [['unlock build', 'hall of heroes', 'king']],
        'unlocks': ['calvary'],
        'quote':"Knights and Noblemen",
    },
    'calvary':{
        'cost': 20,
        'time': 1,
        'ability': [['unlock build', 'castle', 'calvary']],
        'unlocks': ['knights of old'],
        'quote':"I know we have guns, but, what if we had horses",
    },
    'knights of old':{
        'cost': 50,
        'time': 2,
        'ability': [['stat', 'knight', 'attack', 0.5],
                    ['stat', 'knight', 'defense', 0.5]],
        'unlocks': [],
        'quote':"Knights of the square table",
    },
    'ancient enemy':{
        'cost': 20,
        'time': 2,
        'ability': [['unlock build', 'research center', 'slime']],
        'unlocks': ['hostile takeover','counter measures'],
        'quote':"I fear, an ancient enemy has returned",
    },
    'hostile takeover':{
        'cost': 20,
        'time': 1,
        'ability': [['unlock build', 'workshop', 'slime'],
                    ['lose build', 'workshop', 'blob']],
        'unlocks': ['stronger slimes'],
        'deny': ['counter measures'],
        'quote':"Hey, this is my place now.",
    },
    'stronger slimes':{
        'cost': 75,
        'time': 3,
        'ability': [['stat', 'slime', 'attack', 0.5],],
        'unlocks': ['slimy slimes','negotiations'],
        'quote':"Very stronk slimes",
    },
    'slimy slimes':{
        'cost': 50,
        'time': 3,
        'ability': [['stat', 'slime', 'maxHealth', 2],
                    ['stat', 'slime', 'health', 2]],
        'unlocks': ['usurper'],
        'deny': ['negotiations'],
        'quote':"VERY slimy bois",
    },
    'usurper':{
        'cost': 100,
        'time': 4,
        'ability': [['unlock build', 'hall of heroes', 'king slime'],
                    ['lose build', 'hall of heroes', 'king blob']],
        'unlocks': [],
        'quote':"There's always a bigger fish",
    },
    'negotiations':{
        'cost': 50,
        'time': 4,
        'ability': [['unlock build', 'workshop', 'blob'],
                    ['lose build', 'workshop', 'slime']],
        'unlocks': ['united kingdoms'],
        'deny': ['slimy slimes'],
        'quote':"Ah yes, the negotiator",
    },
    'counter measures':{
        'cost': 20,
        'time': 2,
        'ability': [['gain ability', 'king blob', 'multibuild', 1]],
        'unlocks': ['stronger blobs'],
        'deny': ['hostile takeover'],
        'quote':"Hey no, go back you slimes",
    },
    'stronger blobs':{
        'cost': 50,
        'time': 4,
        'ability': [['stat', 'blob', 'attack', 0.5],],
        'unlocks': ['denser blobs','alignment'],
        'quote':"Wait they have muscles now?",
    },
    'denser blobs':{
        'cost': 50,
        'time': 2,
        'ability': [['stat', 'slime', 'maxHealth', 2],
                    ['stat', 'slime', 'health', 2]],
        'unlocks': ['conquest'],
        'deny': ['alignment'],
        'quote':"Just mix some gold in there...",
    },
    'conquest':{
        'cost': 75,
        'time': 2,
        'ability': [['unlock build', 'research center', 'blob'],
                    ['lose build', 'research center', 'slime']],
        'unlocks': [],
        'quote':"Ah, victory",
    },
    'alignment':{
        'cost': 100,
        'time': 4,
        'ability': [['stat', 'research center', 'maxPopulation', 1]],
        'unlocks': ['united kingdoms'],
        'deny': ['denser blobs'],
        'quote':"Alligning ourselves with the enemy",
    },
    'united kingdoms':{
        'cost': 100,
        'time': 5,
        'ability': [['unlock build', 'king blob', 'slime']],
        'unlocks': ['symbiosis'],
        'quote':"Never thought I'd be fighting alongside a slime",
    },
    'symbiosis':{
        'cost': 100,
        'time': 3,
        'ability': [['unlock build', 'research center', 'blob'],
                    ['unlock build', 'workshop', 'slime']],
        'unlocks': [],
        'quote':"Not a slime, a friend",
    },
    
    #Green
    'recruitment':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['defensive tactics','offensive tactics'],
    },
    'defensive tactics':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['more','defensive recruitment'],
        'deny': ['offensive tactics'],
    },
    'more':{
        'cost': 20,
        'time': 2,
        'ability': [['stat', 'barracks', 'maxPopulation', 1]],
        'unlocks': ['tougher','defenders','anti air'],
    },
    'defenders':{
        'cost': 20,
        'time': 1,
        'ability': [['unlock build', 'barracks', 'defender']],
        'unlocks': ['blockade'],
    },
    'blockade':{
        'cost': 10,
        'time': 3,
        'ability': [['unlock build', 'defender', 'wall']],
        'unlocks': [],
    },
    'tougher':{
        'cost': 20,
        'time': 4,
        'ability': [['typeStat', 'trooper', 'defense', 0.5]],
        'unlocks': ['commanding presence'],
    },
    'anti air':{
        'cost': 20,
        'time': 3,
        'ability': [['unlock build', 'barracks', 'rocket']],
        'unlocks': [],
    },
    'commanding presence':{
        'cost': 50,
        'time': 5,
        'ability': [['unlock build', 'barracks', 'general']],
        'unlocks': [],
    },
    'defensive recruitment':{
        'cost': 20,
        'time': 2,
        'ability': [['stat', 'recruited soldier', 'defense', 0.5]],
        'unlocks': ['reserves'],
    },
    'reserves':{
        'cost': 20,
        'time': 2,
        'ability': [['stat', 'the recruiter', 'maxPopulation', 1]],
        'unlocks': [],
    },
    'offensive tactics':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['charge', 'brute force', 'ranged support'],
        'deny': ['defensive tactics'],
    },
    'brute force':{
        'cost': 30,
        'time': 1,
        'ability': [['unlock build', 'barracks', 'brute']],
        'unlocks': [],
    },
    'ranged support':{
        'cost': 30,
        'time': 3,
        'ability': [['unlock build', 'barracks', 'sniper']],
        'unlocks': [],
    },
    'charge':{
        'cost': 50,
        'time': 6,
        'ability': [['typeAbility', 'trooper', 'charge', 0]],
        'unlocks': ['stronger soldiers'],
    },
    'stronger soldiers':{
        'cost': 50,
        'time': 8,
        'ability': [['typeStat', 'trooper', 'attack', 0.5]],
        'unlocks': [],
    },
    
    
    #Yellow
    'armament':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['heavy weapons','naval warfare'],
    },
    'heavy weapons':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['taking their land','defending our territory'],
    },
    'taking their land':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['artillery','taking land','heavier'],
    },
    'artillery':{
        'cost': 20,
        'time': 2,
        'ability': [['unlock build', 'tank factory', 'artillery']],
        'unlocks': ['seige cannons'],
    },
    'seige cannons':{
        'cost': 50,
        'time': 3,
        'ability': [['stat', 'artillery', 'attack', 0.5]],
        'unlocks': ['stronger hulls'],
    },
    'stronger hulls':{
        'cost': 20,
        'time': 3,
        'ability': [['stat', 'artillery', 'maxHealth', 2],
                    ['stat', 'artillery', 'health', 2]],
        'unlocks': [],
    },
    'taking land':{
        'cost': 50,
        'time': 5,
        'ability': [['typeAbility', 'vehicle', 'charge', 0]],
        'unlocks': ['heavier'],
    },
    'defending our territory':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['mobile fortress','heavier'],
    },
    'mobile fortress':{
        'cost': 20,
        'time': 2,
        'ability': [['unlock build', 'tank factory', 'mobile fortress']],
        'unlocks': [],
    },
    'heavier':{
        'cost': 20,
        'time': 2,
        'ability': [['unlock build', 'tank factory', 'heavy tank']],
        'unlocks': ['heavier weapons','heavier armor'],
    },
    'heavier armor':{
        'cost': 40,
        'time': 2,
        'ability': [['stat', 'heavy tank', 'defense', 0.5]],
        'unlocks': [],
        'deny': ['heavier weapons'],
    },
    'heavier weapons':{
        'cost': 50,
        'time': 3,
        'ability': [['stat', 'heavy tank', 'attack', 0.5]],
        'unlocks': [],
        'deny': ['heavier armor'],
    },
    
    'naval warfare':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['taking their shores', 'defending our water'],
    },
    'taking their shores':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['subs','seige boats'],
    },
    'defending our water':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['floating fortress','backup navy','subs'],
    },
    'floating fortress':{
        'cost': 20,
        'time': 2,
        'ability': [['unlock build', 'docks', 'floating fortress']],
        'unlocks': [],
    },
    'backup navy':{
        'cost': 20,
        'time': 2,
        'ability': [['stat', 'docks', 'maxPopulation', 1]],
        'unlocks': [],
    },
    'subs':{
        'cost': 20,
        'time': 2,
        'ability': [['unlock build', 'docks', 'submarine']],
        'unlocks': [],
    },
    'seige boats':{
        'cost': 20,
        'time': 2,
        'ability': [['unlock build', 'docks', 'seige boat']],
        'unlocks': [],
    },
    #Orange
    'aviation':{
        'cost': 40,
        'time': 2,
        'ability': [],
        'unlocks': ['airport'],
    },
    'airport':{
        'cost': 40,
        'time': 2,
        'ability': [['unlock build', 'crane', 'airport']],
        'unlocks': ['helicopter','water launch','rapid launch','super sonic speed'],
    },
    'helicopter':{
        'cost': 40,
        'time': 5,
        'ability': [['unlock build', 'airport', 'helicopter']],
        'unlocks': ['heavy lifting'],
    },
    'heavy lifting':{
        'cost': 50,
        'time': 5,
        'ability': [['stat', 'helicopter', 'maxPopulation', 1]],
        'unlocks': ['chinook'],
    },
    'chinook':{
        'cost': 100,
        'time': 7,
        'ability': [['unlock build', 'airport', 'chinook']],
        'unlocks': [],
    },
    'water launch':{
        'cost': 80,
        'time': 5,
        'ability': [['unlock build', 'docks', 'aircraft carrier']],
        'unlocks': ['sea plane'],
    },
    'sea plane':{
        'cost': 30,
        'time': 2,
        'ability': [['unlock build', 'aircraft carrier', 'sea plane']],
        'unlocks': ['copter launch'],
    },
    'copter launch':{
        'cost': 40,
        'time': 5,
        'ability': [['unlock build', 'aircraft carrier', 'helicopter']],
        'unlocks': [],
    },
    'rapid launch':{
        'cost': 40,
        'time': 4,
        'ability': [['stat', 'airport', 'range', 1]],
        'unlocks': ['air traffic control'],
    },
    'air traffic control':{
        'cost': 120,
        'time': 2,
        'ability': [['stat', 'airport', 'maxPopulation', 1]],
        'unlocks': ['bombers'],
    },
    'bombers':{
        'cost': 20,
        'time': 4,
        'ability': [['unlock build', 'airport', 'bomber']],
        'unlocks': [],
    },
    'super sonic speed':{
        'cost': 100,
        'time': 5,
        'ability': [['stat', 'plane', 'speed', 1]],
        'unlocks': ['better armor'],
    },
    'better armor':{
        'cost': 40,
        'time': 2,
        'ability': [['typeStat', 'aircraft', 'defense', 0.5]],
        'unlocks': ['better weapons'],
    },
    'better weapons':{
        'cost': 80,
        'time': 4,
        'ability': [['typeStat', 'aircraft', 'attack', 0.5]],
        'unlocks': [],
    },
    
    #Purple
    'improvements':{
        'cost': 20,
        'time': 1,
        'ability': [],
        'unlocks': ['the city', 'miscellaneous upgrades'],
    },
    'the city':{
        'cost': 50,
        'time': 1,
        'ability': [['unlock build', 'crane', 'metropolis']],
        'unlocks': ['bionics','city planning','time travel'],
    },
    'city planning':{
        'cost': 5,
        'time': 2,
        'ability': [],
        'unlocks': ['supply lines','urban expansion','civil fortification'],
    },
    'supply lines':{
        'cost': 20,
        'time': 3,
        'ability': [],
        'unlocks': ['recycling','quarries','power lines'],
    },
    'recycling':{
        'cost': 50,
        'time': 4,
        'ability': [['unlock build', 'metropolis', 'recycler'],
                    ['unlock build', 'metropolis expansion', 'recycler']],
        'unlocks': [],
    },
    'quarries':{
        'cost': 50,
        'time': 4,
        'ability': [['unlock build', 'metropolis', 'mine shaft'],
                    ['unlock build', 'metropolis expansion', 'mine shaft']],
        'unlocks': [],
    },
    'power lines':{
        'cost': 50,
        'time': 4,
        'ability': [['unlock build', 'metropolis', 'power grid'],
                    ['unlock build', 'metropolis expansion', 'power grid']],
        'unlocks': [],
    },
    'urban expansion':{
        'cost': 20,
        'time': 3,
        'ability': [],
        'unlocks': ['suburbs','expanding city limits'],
    },
    'suburbs':{
        'cost': 25,
        'time': 2,
        'ability': [['unlock build', 'metropolis', 'town'],
                    ['unlock build', 'metropolis expansion', 'town']],
        'unlocks': [],
    },
    'expanding city limits':{
        'cost': 35,
        'time': 4,
        'ability': [['unlock build', 'metropolis', 'metropolis expansion']],
        'unlocks': ['indefinite expansion'],
    },
    'indefinite expansion':{
        'cost': 50,
        'time': 7,
        'ability': [['unlock build', 'metropolis expansion', 'metropolis expansion']],
        'unlocks': [],
    },
    'civil fortification':{
        'cost': 40,
        'time': 3,
        'ability': [],
        'unlocks': ['defensive measures','city improvements'],
    },
    'defensive measures':{
        'cost': 45,
        'time': 3,
        'ability': [['unlock build', 'metropolis', 'defense platform'],
                    ['unlock build', 'metropolis expansion', 'defense platform']],
        'unlocks': ['offense platform'],
    },
    'offense platform':{
        'cost': 60,
        'time': 7,
        'ability': [['unlock build', 'defense platform', 'missile']],
        'unlocks': [],
    },
    'city improvements':{
        'cost': 50,
        'time': 2,
        'ability': [],
        'unlocks': ['immigration','resistant structures','taller skyscapers'],
    },
    'immigration':{
        'cost': 250,
        'time': 2,
        'ability': [['gain ability', 'metropolis', 'buff', ['maxPopulation', 1.5]]],
        'unlocks': [],
    },
    'resistant structures':{
        'cost': 50,
        'time': 5,
        'ability': [['stat', 'metropolis', 'defense', 1]],
        'unlocks': [],
    },
    'taller skyscapers':{
        'cost': 50,
        'time': 5,
        'ability': [['stat', 'metropolis', 'maxHealth', 10],
                    ['stat', 'metropolis', 'health', 10]],
        'unlocks': [],
    },
    'miscellaneous upgrades':{
        'cost': 25,
        'time': 1,
        'ability': [],
        'unlocks': ['stronger walls','double time','deflector shields','further dectection'],
    },
    'stronger walls':{
        'cost': 20,
        'time': 4,
        'ability': [['stat', 'wall', 'maxHealth', 5],
                    ['stat', 'wall', 'health', 5]],
        'unlocks': [],
    },
    'double time':{
        'cost': 10,
        'time': 10,
        'ability': [['gain ability', 'research center', 'fast research', 2]],
        'unlocks': [],
    },
    'deflector shields':{
        'cost': 30,
        'time': 7,
        'ability': [['unlock build', 'crane', 'shield generator']],
        'unlocks': [],
    },
    'further dectection':{
        'cost': 20,
        'time': 4,
        'ability': [['stat', 'radar tower', 'range', 1]],
        'unlocks': [],
    },
}







