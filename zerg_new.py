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
        self.health = 25
        self.moves = (1)
        self.list_of_tupes = []
        self.my_map = {}
        self.list_lists = []
        row = []
        self.move = 0
        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0      

    def action(self, context):
        self.move += 1
        new = randint(0, 3)
        x = context.x
        y = context.y
        print("This is overlord map option -------------------> ", self.overlord.option)
        print("This is map object -------------------------------> ", self.overlord.map_object.map_terrain.items())
        self.list_of_tupes.append(tuple([x, y]))
        print("Zerg id {} on map {} ".format(self.overlord.zerg_id, self.overlord.zerg_to_map[self.overlord.zerg_id]))
        print("This is zerg to map current ", self.overlord.zerg_to_map.items())
        zerg_map_location = self.overlord.zerg_to_map[self.overlord.zerg_id]
        self.overlord.map_object.map_terrain[zerg_map_location].append(tuple([x,y])) 
        #if self.overlord.option in 
        self.overlord.map_object.map_symbols[zerg_map_location] = self.my_map
        print("This is fulll map ------------------------------------------------------------------> ")
        print(self.overlord.map_object.map_symbols[zerg_map_location].items())
        print(self.overlord.map_object.map_symbols.items())
        print("----------------------------------------------------------------------------------------$")

        #self.my_map[self.list
	#if self.moves < 2:
	#	self.my_map[self.list_tuples
        #self.my_map[self.list_of_tupes] = cont
        '''
        for key in self.overlord.maps:
            print("This is map id ") 
            print(key)
        '''
        print("This is list of tupes ---> ")
        print(self.list_of_tupes)
        print(id(self))
        #print("First element in list of tupes ---> ", self.list_of_tupes[0])
       # print("X coordinate of first element ", type(self.list_of_tupes[0][0]))
        #print("Last element in list of tupes ---> ", self.list_of_tupes[-1])
        #print("Last y in last element ", self.list_of_tupes[-1][1])
        #print("This is len of self.list ", len(self.list_of_tupes))
        
        print("First value ", self.list_of_tupes[0])
        self.min_x = min(self.list_of_tupes)[0]
        self.max_x = max(self.list_of_tupes)[0]
        self.min_y = min(self.list_of_tupes, key = lambda tupe_list: tupe_list[1])[1]
        self.max_y = max(self.list_of_tupes, key = lambda tupe_list: tupe_list[1])[1]

        north  = context.y + 1
        x = context.x
        y = context.y
        south = context.y - 1
        self.my_map[(x, north)] = context.north
        self.my_map[(x, south)] = context.south
   
        east = context.x + 1
    
        west = context.x - 1
        self.my_map[(east, y)] = context.east
        self.my_map[(west, y)] = context.west

        #print("These are min and max values")
        #print(self.max_x)
        #print(self.min_x)
        #print(self.max_y)
        #print(self.min_y)

        
       #LOOP
        #print("@" * 30)
        #print(set(self.list_of_tupes))
        #print("@" * 30)
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                symbol = (x, y)
               # print("This is symbol ", symbol)
                #print("This is symbol value", self.my_map.get(symbol, "?"))
                #print("!" * 50)
                #print("Loop symbol {0}  {1} ".format(symbol, self.my_map.get(symbol, "?")))
                print(self.my_map.get(symbol, "?"), end=" ")
            print()			                    


        print("My map  ", self.my_map.items())
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

        for _ in range(1):
            z = Drone(self, self.map_object)
            self.zerg_id = id(z)
            self.zerg[self.zerg_id] = z

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
                if self.zerg_id in self.zerg_to_map:
                     if self.zerg_status[self.zerg_id] == "D":
                         continue
                     else:
                         return 'DEPLOY {} {}'.format(self.zerg_id, self.option)
                else:
                    self.zerg_to_map[self.zerg_id] = self.option
                    self.zerg_status[self.zerg_id] = "D"
                    return 'DEPLOY {} {}'.format(self.zerg_id, self.option)
  

