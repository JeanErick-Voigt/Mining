#!/usr/local/bin/python

from random import randint, choice

class Drone:
    def __init__(self, overlord):
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
        #row = []
        #li = []
        print("This is length of list of tupes --> ", len(self.list_of_tupes))
       # print("This is map_id", Overlord.maps)
        x = context.x
        y = context.y
        self.list_of_tupes.append(tuple([x, y]))

        #self.my_map[self.list
	#if self.moves < 2:
	#	self.my_map[self.list_tuples
        #self.my_map[self.list_of_tupes] = cont
        for key in self.overlord.maps:
            print("This is map id ") 
            print(key)
        print("This is list of tupes ---> ")
        print(self.list_of_tupes)
        print(id(self))
        print("First element in list of tupes ---> ", self.list_of_tupes[0])
       # print("X coordinate of first element ", type(self.list_of_tupes[0][0]))
        print("Last element in list of tupes ---> ", self.list_of_tupes[-1])
        print("Last y in last element ", self.list_of_tupes[-1][1])
            
        #print("This is len of self.list ", len(self.list_of_tupes))
        if(len(self.list_of_tupes) < 2):
       	   # print("DEBUG DEBUG")
            self.my_map[self.list_of_tupes[0]] = "_"
            self.min_x = int(self.list_of_tupes[0][0])
            self.max_x = int(self.list_of_tupes[0][0])
            self.min_y = int(self.list_of_tupes[0][1])
            self.max_y = int(self.list_of_tupes[0][1])
            
            north  = context.x + 1
            x = context.x
            y = context.y
            south = context.x - 1
            self.my_map[(north, y)] = context.north
            self.my_map[(south, y)] = context.south
   
            east = context.y + 1
    
            west = context.y - 1
            self.my_map[(x, east)] = context.east
            self.my_map[(x, west)] = context.west

        else:
            #if tuple(self.list_of_tupes[-1]) in self.my_map:
            north = context.x + 1
            x = context.x
            y = context.y
            south = context.x - 1
            self.my_map[(north, y)] = context.north
            self.my_map[(south, y)] = context.south
            east = context.y + 1
            west = context.y - 1
            self.my_map[(x, east)] = context.east
            self.my_map[(x, west)] = context.west
            print("this is y value from tuple --------------------------------> ", int(self.list_of_tupes[-1][1]))
            if int(self.list_of_tupes[-1][0]) > self.max_x:
                self.max_x = int(self.list_of_tupes[-1][0])
            if int(self.list_of_tupes[-1][0]) < self.min_x:
                self.min_x = int(self.list_of_tupes[-1][0])
            if int(self.list_of_tupes[-1][1]) > self.max_y:
                self.max_y = int(self.list_of_tupes[-1][1])
            if int(self.list_of_tupes[-1][1]) < self.min_y:
                self.min_y = int(self.list_of_tupes[-1][1])

        print("These are min and max values")
        print(self.max_x)
        print(self.min_x)
        print(self.max_y)
        print(self.min_y)

 
       #LOOP
        print("@" * 30)
        print(self.my_map)
        print("@" * 30)
        for x in range(5):
            for y in range(5):
                symbol = (x, y)
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

        for _ in range(1):
            z = Drone(self)
            self.zerg[id(z)] = z

    def add_map(self, map_id, summary):
        self.maps[map_id] = summary

    def action(self):
        act = randint(1, 3)
        if act == 0:
            return 'RETURN {}'.format(choice(list(self.zerg.keys())))
        else:
            return 'DEPLOY {} {}'.format(choice(list(self.zerg.keys())),
                    choice(list(self.maps.keys())))

