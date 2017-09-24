#!/usr/local/bin/python

from random import randint, choice

class Dashboard():
    def __init__(self, overlord, map_object):
        self.overlord = overlord
        self.my_map = map_object.map_symbols
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0

    
    def dashboard(self):
        '''Dashboard function to print a visual presentation of map'''
        dashboard_output = ""
        #my_map = self.map_object.map_symbols
        map_to_draw = self.overlord.zerg_to_map[self.zerg_id]
        print("This is map_to_draw answer -> ", map_to_draw)
        for key in self.my_map:
            map_to_draw = key    
            if self.my_map.get(map_to_draw, "None"):
                #print(my_map[map_to_draw])
                dashboard_ouput += "=" * 30
                dashboard_output += "This is map for -> {}".format(map_to_draw)
                dashboard_output += "\n"
                self.min_x = min(self.my_map[map_to_draw])[0]
                self.max_x = max(self.my_map[map_to_draw])[0]
                self.min_y = min(self.my_map[map_to_draw], key=lambda map_list: map_list[1])[1]
                self.max_y = max(self.my_map[map_to_draw], key=lambda map_list: map_list[1])[1]
                for y in range(self.min_y, self.max_y + 1):
                    for x in range(self.min_x, self.max_x + 1):
                        symbol = (x, y)
                        dashboard_output = dashboard_output +  self.my_map[map_to_draw].get(symbol, "?")
                      
                    dashboard_output += "\n"

        return(dashboard_output)

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
        self.moves = 1
        self.list_of_tupes = []
        self.list_lists = []
        row = []
        self.move = 0
        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0     
    
     
    
    def action(self, context):
        '''Controls the acionof the Drone class. Decides which direction to go'''
        self.move += 1
        my_map = Map(self.overlord)
        new = randint(0, 3)
        new_x = context.x
        new_y = context.y
        
        id_of_zerg = id(self)
         

        zerg_map_location = self.overlord.zerg_to_map[id_of_zerg] 
        
        self.overlord.map_object.map_terrain[zerg_map_location].append(tuple([new_x, new_y])) 
         
        new_south = context.y - 1
        new_east = context.x + 1
        new_west = context.x - 1
        new_north  = context.y + 1     
        
        if zerg_map_location not in self.my_map: 
            self.my_map[self.overlord.zerg_to_map[id_of_zerg]] = {}
        self.my_map[self.overlord.zerg_to_map[id_of_zerg]][(new_x, new_north)] = context.north
        self.my_map[self.overlord.zerg_to_map[id_of_zerg]][(new_x, new_south)] = context.south
        self.my_map[self.overlord.zerg_to_map[id_of_zerg]][(new_east, new_y)] = context.east
        self.my_map[self.overlord.zerg_to_map[id_of_zerg]][(new_west, new_y)] = context.west
       

     
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

class Miner(Drone):
    def __init__(self, overlord, map_object):
        super().__init__(overlord, map_object)
        self.health = 10
        self.moves = 2
        self.capacity = 20
        self.go_home = []
        self.outbound_journey = []
        self.mined = 0
        self_mission = "M"
        self.target = []
        self.home = []
        self.distance = 0
        self.difference = set()
        self.neighbor_list = {}
        self.check = None
        self.movement = []
        self.total_steps = 0

    def find_neighbors(self, context):
       '''Finds neighbors of current tile in order to find shortest path to end point'''
       zerg_map_location = self.overlord.zerg_to_map[id(self)]
       symbol_map_list = self.overlord.map_object.map_symbols[zerg_map_location]
       
       for x in list(symbol_map_list.keys()):
           self.neighbor_list[x] = []

       for x in self.neighbor_list:
           self.neighbor_list[x].append((x[0], x[1] -1))
           self.neighbor_list[x].append((x[0], x[1] +1))
           self.neighbor_list[x].append((x[0] + 1, x[1]))
           self.neighbor_list[x].append((x[0] - 1, x[1]))

       for x in self.neighbor_list:
           for y in self.neighbor_list[x]:
               if y in list(symbol_map_list.keys()) and symbol_map_list[y] not in "~#Z":
                   continue
               else:
                   self.neighbor_list[x].remove(y)

    
    
    def find_shortest_path(self, start, end, path = []):
        '''Finds shortest path between the start and end. Using the path
           as the list of directions to take'''
        path.append(start)
        if start == end:
            return path
        if start not in self.neighbor_list:
            return None
 
        shortest = None

        for node in self.neighbor_list[start]:
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest 
    
    def compare_move(self, context):
        '''compares the current tile to the next_move tuple in order to return a
           directional command of NORTH, SOUTH, EAST, or WEST or CENTER'''
        current = (context.x, context.y)
        if current == self.outbound_journey[0]:
           self.outbound_journey.pop(0)
           destination = self.outbound_journey[0]
        else:
            destination = self.outbound_journey[0]

        if current[0] == destination[0]:
            if current[1] > destination[1]:
                statement = "NORTH"
                if context.north is "Z":
                    return "CENTER"
            else:
                statement = "SOUTH"
                if context.south is "Z":
                    return "CENTER"
        else:
            if current[0] > destination[0]:
                statement = "EAST"
                if context.east is "Z":
                    return "CENTER"
            else:
                statement = "WEST" 
                if context.west is "Z":
                    return "CENTER"

        return statement   
                             
    def backwards_mine(self, context):
        '''Enables the zerg to mine nearby minerals along their journey to
           the end point.'''
        statement = " "
        if self.mined < self.capacity and context.north in "*":
            statement = 'NORTH'
            self.mined += 1
        
        elif self.mined < self.capacity and context.south in "*":
            statement = 'SOUTH'
            self.mined += 1

        elif self.mined < self.capacity and context.east in "*":
            statement = 'EAST'
            self.mined += 1

        elif self.mined < self.capacity and context.west in "*":
            statement = 'WEST'
            self.mined += 1
     
        elif self.mined == self.capacity:
            start = (context.x, context.y)
            if start == self.home[0]:
                self.overlord.zerg_status[id(self)] = "R"
                self.neighbor_list = {}
                self.go_home = []
                self.target = []
                self.outbound_journey = []
                return "CENTER"
            else:
                self.find_neighbors(context)
                self.find_shortest_path(start, self.home[0])
                statement = self.compare_move(context)
                self.mission = "R"
        else:
            statement = self.compare_move(context)
        
        return statement

    
    def update(self, context):
        '''Updates the tiles in movement'''
        zerg_map_location = self.overlord.zerg_to_map[id(self)]
        if (context.x, context.y) not in self.overlord.map_object.map_terrain[zerg_map_location]:      
            self.overlord.map_object.map_terrain[zerg_map_location].append((context.x, context.y))
        
        if len(self.movement) < 1:
            self.movement.append((context.x, context.y))
        else:
            if self.movement[-1] != (context.x, context.y):
                self.movement.append((context.x, context.y))
                self.total_steps += 1
       
        decision = self.backwards_mine(context)
        return decision
    
    
    def action(self, context):
        '''returns the directional command to move to'''
        new_x = context.x
        new_y = context.y
        new_south = context.y - 1
        new_east = context.x + 1
        new_west = context.x - 1
        new_north  = context.y + 1    
        id_of_zerg = id(self)
        
        if len(self.home) < 1:
            self.home.append((new_x, new_y))
       
        zerg_map_location = self.overlord.zerg_to_map[id_of_zerg]      
        
        if zerg_map_location not in self.overlord.map_object.map_symbols:
            self.overlord.map_object.map_symbols[zerg_map_location] = {}
        
        
        self.overlord.map_object.map_symbols[zerg_map_location][(new_x, new_north)] = context.north
        self.overlord.map_object.map_symbols[zerg_map_location][(new_x, new_south)] = context.south
        self.overlord.map_object.map_symbols[zerg_map_location][(new_east, new_y)] = context.east
        self.overlord.map_object.map_symbols[zerg_map_location][(new_west, new_y)] = context.west
        
        if zerg_map_location not in self.overlord.map_object.map_terrain:
            self.overlord.map_object.map_terrain[zerg_map_location] = []
        
       
        
        if len(self.target) < 1:
            for key, value in self.overlord.map_object.map_symbols[zerg_map_location].items():
                if value is "*":
                    check_x = key[0] - self.home[0][0]
                    check_y = key[1] - self.home[0][1]
                    self.check = abs(check_x) + abs(check_y)
                
                    if self.check > self.distance:
                        self.distance = self.check
                        self.target.append(key)
                        self.difference =  (check_x, check_y)
                
                else:
                    continue
            
            self.find_neighbors(context)
            self.outbound_journey = self.find_shortest_path(self.home[0], self.target[0])
            
                    
        if (new_x, new_y) == self.target[0]:
            self.target = []
 
        decision = self.update(context)
        return(decision)   
    
    def steps():
        '''Returns the total number of steps the zerg has taken since
           starting the game'''
        return self.total_steps

    def get_init_cost():
        health  =  self.health * (1/10)
        moves = self.moves * 3
        capacity = self.capacity * (1/5)
        total = health + moves + capacity
        return total
     
        
class Scout(Drone):
    def __init__(self, overlord, map_object):
        super().__init__(overlord, map_object)   
        self.health = 10
        self.moves = 1
        self.capacity = 15     
        self.movement = []
        self.go_back = 0
        self.mined = 0
        self.updated_moves = []
        self.count = 0
        self.second_move = ""
        self.deployments = 0
        self.total_steps = 0

    def back_track(self, context):
        '''Allows the zerg to step back to find its way home or 
           discover new tiles'''
        zerg_map_location = self.overlord.zerg_to_map[id(self)]      
        next_move = ""
        statement = ''
        current_pos = self.updated_moves[-1]  
        if len(self.second_move) > 0:
            statement = self.second_move
            self.second_move = ""
            self.updated_moves.pop()
            return statement
            
        if len(self.updated_moves) >= 2:
            move_to = self.updated_moves[-2]
            if move_to == current_pos and len(self.updated_moves) > 2:
                move_to = self.updated_moves[-3]
            else:
                None
        if len(self.updated_moves) >= 4:
            repeat2 = self.updated_moves[-4]
            repeat1 = self.updated_moves[-3]
            if current_pos == repeat1 and repeat2 == move_to:
                move_to = repeat2
                if len(self.updated_moves) == 4:
                    self.overlord.zerg_status[id(self)] = "R"
                else:
                    next_move = self.updated_moves[-5]
                self.updated_moves.pop()
                self.updated_moves.pop()
            elif current_pos == repeat1:
                self.updated_moves.pop()
                self.updated_moves.pop() 
        
        if len(self.updated_moves) > 1:
            if move_to[0] == current_pos[0]:
                if move_to[1] > current_pos[1]:
                    statement = "NORTH"
            
                else:
                    statement = "SOUTH"
     
            if move_to[0] > current_pos[0]:
                statement = "EAST"
     
            if move_to[0] < current_pos[0]:
                statement = "WEST"
        
            if len(self.updated_moves) > 1:
                self.updated_moves.pop()
        
        if type(next_move) is not str:
            if move_to[0] == next_move[0]:
                if move_to[1] > next_move[1]:
                    self.second_move = "NORTH"
                else:
                    self.second_move = "SOUTH"
            elif move_to[0] > next_move[0]:
                self.second_move = "EAST"
            else:
                self.second_move = "WEST"    
            next_move = ""
        elif (context.x, context.y) == self.map_object.map_terrain[zerg_map_location][0]:
            print("PICK UP")
            statement = 'CENTER'
            self.overlord.zerg_status[id(self)] = "R"
            self.movement = []
            self.count = 0
            self.mined = 0
            self.deployments += 1
        return statement
 
    def backwards_mine(self, context):
        '''Allows the zerg to mine if it has finished searching a path'''
        statement = " "
        if self.mined < self.capacity and context.north in "*":
            statement = 'NORTH'
            self.mined += 1
        
        elif self.mined < self.capacity and context.south in "*":
            statement = 'SOUTH'
            self.mined += 1

        elif self.mined < self.capacity and context.east in "*":
            statement = 'EAST'
            self.mined += 1

        elif self.mined < self.capacity and context.west in "*":
            statement = 'WEST'
            self.mined += 1
     
        else:
            statement = self.back_track(context)
        return statement
            
        
    
    def scouting(self, context):
        '''determines how the zerg will scout'''
        zerg_map_location = self.overlord.zerg_to_map[id(self)]      
        decision = ""
             
        if (context.x, context.y+1) not in self.movement:
            
            if (context.x, context.y+1) not in self.overlord.map_object.map_terrain[zerg_map_location] and (context.north not in "~#*Z"):
                decision = 'NORTH'
                return decision
   
        if (context.x+1, context.y) not in self.movement:
            if (context.x+1, context.y) not in self.overlord.map_object.map_terrain[zerg_map_location] and (context.east not in "~#*Z"):
                decision = 'EAST'
                return decision
            
        if (context.x, context.y-1) not in self.movement:    
            if (context.x, context.y-1) not in self.overlord.map_object.map_terrain[zerg_map_location]  and (context.south not in "~#*Z"):
                decision = 'SOUTH'
                return decision
            
        if (context.x-1, context.y) not in self.movement:
            if (context.x-1, context.y) not in self.overlord.map_object.map_terrain[zerg_map_location]  and (context.west not in "~#*Z"):
                decision = 'WEST'
                return decision

        if self.count < 30:
            decision = self.backwards_mine(context)
            return decision
        else:
            decision = self.back_track(context)
            return decision
        
        return decision
            
    def update(self, context):
        '''updates the list for the zerg movement'''
        zerg_map_location = self.overlord.zerg_to_map[id(self)]
        if (context.x, context.y) not in self.overlord.map_object.map_terrain[zerg_map_location]:      
            self.overlord.map_object.map_terrain[zerg_map_location].append((context.x, context.y))
        
        if len(self.movement) < 1:
            self.movement.append((context.x, context.y))
            self.updated_moves.append((context.x, context.y))
        else:
            if self.movement[-1] != (context.x, context.y):
                self.movement.append((context.x, context.y))
                self.updated_moves.append((context.x, context.y))
       
        decision = self.scouting(context)
        return decision

    def action(self, context):
       '''returns the directional command to be executed'''
       new_x = context.x
       new_y = context.y
       new_south = context.y - 1
       new_east = context.x + 1
       new_west = context.x - 1
       new_north  = context.y + 1    
       id_of_zerg = id(self)
       self.count += 1
      
       zerg_map_location = self.overlord.zerg_to_map[id_of_zerg]      
       if zerg_map_location not in self.overlord.map_object.map_symbols:
           self.overlord.map_object.map_symbols[zerg_map_location] = {}
       self.overlord.map_object.map_symbols[zerg_map_location][(new_x, new_north)] = context.north
       self.overlord.map_object.map_symbols[zerg_map_location][(new_x, new_south)] = context.south
       self.overlord.map_object.map_symbols[zerg_map_location][(new_east, new_y)] = context.east
       self.overlord.map_object.map_symbols[zerg_map_location][(new_west, new_y)] = context.west
       
       if zerg_map_location not in self.overlord.map_object.map_terrain:
           self.overlord.map_object.map_terrain[zerg_map_location] = []
       decision = self.update(context)
       return(decision)


    def steps():
        '''returns the total number of steps the zerg has taken during game'''
        return self.total_steps

    def get_init_cost():
        '''gives total cost it would take to produce this type of drone'''
        health  =  self.health * (1/10)
        moves = self.moves * 3
        capacity = self.capacity * (1/5)
        total = health + moves + capacity
        return total
   

class Overlord:
    def __init__(self, ticks, refined_minerals):
        self.maps = {}
        self.zerg = {}
        self.map_object = Map(self)
        self.dashboard = Dashboard(self, self.map_object)
        self.option = "None"
        self.zerg_id = -1 
        self.zerg_to_map = {}
        self.zerg_status = {}
        self.test_map = Map(self)
        self.scouted_map = {}
        self.moves = 0
        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0
        self.map_object.map_terrain = {}          
        self.turns = 0        
        self.ticks = ticks

        for _ in range(0):
            z = Drone(self, self.map_object)
            #self.zerg_id = id(z)
            self.zerg[id(z)] = z
        
        for _ in range(1):
            miner = Miner(self, self.map_object)
            self.zerg[id(miner)] = miner
        
        for _ in range(3):
            scout_s = Scout(self, self.map_object)
            self.zerg[id(scout_s)] = scout_s 

    def add_map(self, map_id, summary):
        '''adds a map type to the list of maps'''
        self.maps[map_id] = summary
        self.scouted_map[map_id] = "SCOUT"

    def choose_drone_type(self, map_id):
        '''Chooses drone based on type. If map has not been scouted yet then
           scout must go.  Otherwise a miner will go.  However, 
           if all maps scouted then either can go'''
        status_check = None
        for key, value in self.scouted_map.items():
            if value is "SCOUT":
                status_check = 1
        if self.scouted_map[map_id] is "SCOUT":
            return("SCOUT")
   
        else:
            print("Map is scouted ", self.scouted_map[map_id])
            if not status_check:
                return("BOTH")
            else:
                return("MINE")

    def update_zerg_status(self, key):
        '''updates zerg status among the following options.  H, D or R.  These
           stand for Home, Deployed or Redeploying, respectively'''
        for key, value in self.zerg.items():
            if key not in self.zerg_status:
               self.zerg_status[key] = "H"
    

    def choose_drone(self, zerg_type):
        '''This function will actually choose the drone based on the type
           it is said to choose'''
        for key, value in self.zerg.items():
            self.zerg_status.pop(-1, None)
            print(type(type(value).__name__))
            if zerg_type is "SCOUT":
                if type(value).__name__ is "Scout":
                    self.update_zerg_status(key)
                    print(self.zerg_status[key])
                    if self.zerg_status[key] is "D":
                        continue
                    else:
                        self.zerg_status[key] = "D"
                        return key
               
                else:
                    continue
                    
            elif zerg_type is "MINE":
                if type(value).__name__ is "Miner":
                    if self.zerg_status[key] is "D":
                        continue
                    else:
                        self.zerg_status[key] = "D"
                        return key
                else:
                    continue
            else:
                if self.zerg_status[key] is "D":
                    continue
                
                else:
                    self.zerg_status[key] = "D"
                    return key    
               
        return "NONE" 
           
    def dashboard(self):
        ''' this function will display the dashboard of the current known map'''
        return self.dashboard.dashboard()

    def pickup_zerg(self):
        '''If zerg turns on redeployed flag then he is ready to get picked up.
           This function checks for that.'''
        pickup = None
        for key, value in self.zerg_status.items():
            if value is "R":
                pickup = key
                return pickup

    def action(self, context):
        '''This action decides whether to deploy, return or do nothing as the
           overlord.  If he decides to return he will return the zerg 
           requesting it.  If he decides to do deploy he will deploy based 
           on type, what the map id needs and supply'''
        if self.turns == self.ticks:
           ans = input("do you want to see dashboard, y or no")
           if ans is "y":
                print(dashboard())
        
        statement = " " 
        print("This is beginning of overlord action")
        print()
        status = self.pickup_zerg()
        if self.pickup_zerg():
            statement = 'RETURN {}'.format(status)
            print(statement)
            self.zerg_status[status] = "H"
            map_choice = self.zerg_to_map[status]
            if type(self.zerg[status]).__name__ is "Scout":
                self.scouted_map[map_choice] = "MINE"
            self.zerg_to_map[self.pickup_zerg()] = None
            self.zerg[status].mined = 0
                
        
        else:
            self.option = choice(list(self.maps.keys()))
            zerg_type = self.choose_drone_type(self.option)
            drone_selection = self.choose_drone(zerg_type)
            
            if drone_selection is not "NONE":
                self.zerg_id = drone_selection
                self.zerg_to_map[drone_selection] = self.option
                self.zerg_status[drone_selection] = "D"
                statement = 'DEPLOY {} {}'.format(drone_selection, self.option)
            else:
                statement = "NONE"
        print(self.scouted_map.items())
        return statement
