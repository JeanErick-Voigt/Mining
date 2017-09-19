#!/usr/local/bin/python

from random import randint, choice


class Map:
    def __init__(self, overlord):
        self.overlord = overlord
        self.current_map = {}
        self.map_movement = {}
        self.map_terrain = {}
        self.map_symbols = {}

class Drone:
    def __init__(self, overlord, map_object):
        self.map_object = map_object
        self.overlord = overlord 
        self.my_map = map_object.map_symbols
        self.health = 25
        self.moves = (1)
        self.list_of_tupes = []
        #self.my_map = {}
        self.list_lists = []
        row = []
        self.move = 0
        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0      

    def action(self, context):
        print("Beginning of code")
        print()
        print()
        print("This is zerg id ", self.overlord.zerg_id)
        print("*" * 100)
        self.move += 1
        my_map = Map(self.overlord)
        new = randint(0, 3)
        new_x = context.x
        new_y = context.y
        #print("This is overlord map option (number map he is on)-------------------> ", self.overlord.option)
        #print("This is map object (Where he has been, without symbols))-------------------------------> ", self.overlord.map_object.map_terrain.items())
        #self.list_of_tupes.append(tuple([x, y]))
        print("Zerg id {} on map {} ".format(self.overlord.zerg_id, self.overlord.zerg_to_map[self.overlord.zerg_id])) # his id and map number
        #print("This is zerg to map current ", self.overlord.zerg_to_map.items()) # current map location of zerg
         

        zerg_map_location = self.overlord.zerg_to_map[self.overlord.zerg_id] #will give you map location of current zerg
        print("zerg id ", self.overlord.zerg_id)
        print("zerg map location ", zerg_map_location)
        print()
        print()
        self.overlord.map_object.map_terrain[zerg_map_location].append(tuple([new_x, new_y])) # at this current map it will append the current movement of zerg
         
        
        self.min_x = min(self.overlord.map_object.map_terrain[self.overlord.zerg_to_map[self.overlord.zerg_id]])[0]
        self.max_x = max(self.overlord.map_object.map_terrain[self.overlord.zerg_to_map[self.overlord.zerg_id]])[0]
        self.min_y = min(self.overlord.map_object.map_terrain[self.overlord.zerg_to_map[self.overlord.zerg_id]], key = lambda map_list: map_list[1])[1]
        self.max_y = max(self.overlord.map_object.map_terrain[self.overlord.zerg_to_map[self.overlord.zerg_id]], key = lambda map_list: map_list[1])[1]        

        new_north  = context.y + 1
        #new_x = context.x
        #new_y = context.y
        new_south = context.y - 1
        new_east = context.x + 1
        new_west = context.x - 1
        
        print(zerg_map_location)
        print(self.overlord.zerg_id)
        print()
        print()
        print("This is context north ", context.north)
        print("This is context south ", context.south)
        print("This is context east ", context.east)
        print("This is context west ", context.west)
        print("This is context.x ", context.x)
        print("This is context.y ", context.y)
        print()
        print()
        
        
        id_of_zerg = id(self)
        
        if zerg_map_location not in self.my_map: 
            self.my_map[self.overlord.zerg_to_map[id_of_zerg]] = {}
        self.my_map[self.overlord.zerg_to_map[id_of_zerg]][(new_x, new_north)] = context.north
        self.my_map[self.overlord.zerg_to_map[id_of_zerg]][(new_x, new_south)] = context.south
        self.my_map[self.overlord.zerg_to_map[id_of_zerg]][(new_east, new_y)] = context.east
        self.my_map[self.overlord.zerg_to_map[id_of_zerg]][(new_west, new_y)] = context.west
       

        for each_map in self.my_map.items():
            print(each_map)

     
        '''if self.overlord.zerg_to_map[self.overlord.zerg_id] not in my_map:
            my_map[self.overlord.zerg_to_map[self.overlord.zerg_id]] = {}        
            my_map[self.overlord.zerg_to_map[self.overlord.zerg_id]][(x, north)] = context.north
            my_map[self.overlord.zerg_to_map[self.overlord.zerg_id]][(x, south)] = context.south            
            my_map[self.overlord.zerg_to_map[self.overlord.zerg_id]][(east, y)] = context.east
            my_map[self.overlord.zerg_to_map[self.overlord.zerg_id]][(west, y)] = context.west

        else:
            my_map[self.overlord.zerg_to_map[self.overlord.zerg_id]][(x, north)] = context.north
            my_map[self.overlord.zerg_to_map[self.overlord.zerg_id]][(x, south)] = context.south
            my_map[self.overlord.zerg_to_map[self.overlord.zerg_id]][(east, y)] = context.east
            my_map[self.overlord.zerg_to_map[self.overlord.zerg_id]][(west, y)] = context.west
'''
        print("*" * 100)
        #print(self.my_map)        
        #self.my_map[(x, south)] = context.south
   
        #east = context.x + 1
    
        #west = context.x - 1
        #self.my_map[(east, y)] = context.east
        #self.my_map[(west, y)] = context.west

        #print(self.my_map.values()) 
        #self.overlord.map_object.map_symbols[zerg_map_location] = self.my_map
        #print("This is fulll map ------------------------------------------------------------------> ")
        #print(self.overlord.map_object.map_symbols[zerg_map_location].items())
        #print(self.overlord.map_object.map_symbols.items())
        #print("----------------------------------------------------------------------------------------$")



	#print("These are min and max values")
        #print(self.max_x)
        #print(self.min_x)
        #print(self.max_y)
        #print(self.min_y)

        
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                symbol = (x, y)
                print(self.my_map[self.overlord.zerg_to_map[id_of_zerg]].get(symbol, "?"), end=" ")
            print()			                    
       
        print()
        print("End before function return statement")
        print()
        print()
        print()
        print("%" * 100)
     
       # for y in range(self.min_y, self.max_y + 1):
        #    for x in range(self.min_x, self.max_x + 1):
         #       symbol = (x, y)
          #      print(self.my_map.get(symbol, "?"), end=" ")
           # print()

        #print("My map  ", self.my_map.items())
        if new == 0 and context.north in '* ':
            return 'NORTH'
        elif new == 1 and context.south in '* ':
            return 'SOUTH'
        elif new == 2 and context.east in '* ':
            return 'EAST'
        elif new == 3 and context.west in '* ':
            return 'WEST'
        else:
            return 'CENTER'

class Overlord:
    def __init__(self, total_ticks):
        self.maps = {}
        self.zerg = {}
        self.map_object = Map(self)
        self.option = "None"
        self.zerg_id = -1
        self.zerg_to_map = {}
        self.zerg_status = {}
        self.test_map = Map(self)

        for _ in range(2):
            z = Drone(self, self.map_object)
            #self.zerg_id = id(z)
            self.zerg[id(z)] = z

    def add_map(self, map_id, summary):
        self.maps[map_id] = summary
        #print("This is map_id ", map_id)
        self.map_object.map_terrain[map_id] = []

    def action(self):
        act = randint(1, 3)
        if act == 0:
            #print("This is self.maps.keys ", self.maps.keys())
            return 'RETURN {}'.format(choice(list(self.zerg.keys())))
        else:
            while(1):
                self.option = choice(list(self.maps.keys()))
                self.zerg_id = choice(list(self.zerg.keys()))
                print("This is self.zerg_id on overlord class ", self.zerg_id)
                print()
                print()
                if self.zerg_id in self.zerg_to_map:
                     if self.zerg_status[self.zerg_id] == "D":
                         return "NONE"
                   
                     else:
                         return 'DEPLOY {} {}'.format(self.zerg_id, self.option)
                else:
                    self.zerg_to_map[self.zerg_id] = self.option
                    self.zerg_status[self.zerg_id] = "D"
                    return 'DEPLOY {} {}'.format(self.zerg_id, self.option)
  

