#!/usr/bin/env python3

from copy import copy
from random import randint
from sys import argv
import timeout
import logging

logging.basicConfig(filename='Dave.log', filemode='w', level=logging.DEBUG)

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Map:
    def __init__(self, x, y):
        """ Instantiates a map with dimensions x, y and populates it with
            a landing zone, minerals, acis and such
        """
        self.__x = x
        self.__y = y
        top_bottom_row = [ '#' for _ in range(x) ]
        self.data = [top_bottom_row]
        for _ in range(y-2):
            wall_edges = ['#']
            wall_edges.extend(' ' for _ in range(x-2))
            wall_edges.append('#')
            self.data.append(wall_edges)
        self.data.append(top_bottom_row)

        self.mineral = []
        for n in range(1,10):
            self.add_mineral(n)

        coordinates = (0,0)
        while self[coordinates] != ' ':
            coordinates = randint(1, self.__x - 2), randint(1, self.__y - 2)
        self[coordinates] = '_'
        self.landing_zone = coordinates

        self.acid = []
        for _ in range(x * y // 15):
            coordinates = (0,0)
            while self[coordinates] != ' ':
                coordinates = randint(1, self.__x - 2), randint(1, self.__y - 2)
            self[coordinates] = '~'
            self.acid.append(coordinates)

        self.zerg = []

    def load_from_file(self, filename):
        data = []
        self.mineral = []
        self.acid = []


# TODO: This could do a much better job of building the summary, by
#       only considering reachable tiles
        with open(filename) as fh:
            for row, line in enumerate(fh):
                d = [char for char in line.rstrip()]
                for column, char in enumerate(d):
                    if char == '~':
                        self.acid.append((column, row))
                    elif char == '_':
                        self.landing_zone = (column, row)
                    elif char in '0123456789':
                        d[column] = '*'
                        ctx = MineralContext(Location(column, row), int(char))
                        self.mineral.append(ctx)

                data.append(d)

        self.__x = column
        self.__y = row
        self.data = data

    def summary(self):
        return sum(m.amt for m in self.mineral) / (self.__x * self.__y)

    def __str__(self):
        return '\n'.join(''.join(row) for row in reversed(self.data))

    def __getitem__(self, key):
        return self.data[key[1]][key[0]]

    def __setitem__(self, key, val):
        self.data[key[1]][key[0]] = val

    def what_is_at(self, key):
        for z in self.zerg:
            if z.location == key:
                return 'Z'
        return self[key]

    def add_mineral(self, amt):
        c = 0,0
        while self[c] != ' ':
            c = randint(1, self.__x - 2), randint(1, self.__y - 2)

        l = Location(c[0], c[1])
        ctx = MineralContext(l, amt)
        self[l.x,l.y] = '*'
        self.mineral.append(ctx)

    def remove_zerg(self, z_id):
        for z in self.zerg:
            if z_id == id(z.zerg) and (z.location.x,z.location.y) == self.landing_zone:
                self[z.location.x, z.location.y] = '_'
                self.zerg.remove(z)
                return z.mineral, z.hp
        return None, None

    def add_zerg(self, z, health):
        c = self.landing_zone
        if self[c] != '_':
            return False

        l = Location(c[0], c[1])
        self.update_location_adjacent(l)

        ctx = DroneContext(l, z, health)
        self[l.x,l.y] = 'Z'
        self.zerg.append(ctx)

        return True

    def update_location_adjacent(self, l):
        l.north = self[l.x, l.y+1]
        l.south = self[l.x, l.y-1]
        l.east = self[l.x+1, l.y]
        l.west = self[l.x-1, l.y]
        return l

    def find_mineralcontext_at(self, pos):
        for z in self.mineral:
            if z.location.x == pos[0] and z.location.y == pos[1]:
                return z

        return None

    def find_zergcontext_at(self, pos):
        for z in self.zerg:
            if z.location.x == pos[0] and z.location.y == pos[1]:
                return z

        return None

    def move_to(self, l, d):
        if d == 'NORTH':
            new_l = (l.x, l.y + 1)
        elif d == 'SOUTH':
            new_l = (l.x, l.y - 1)
        elif d == 'EAST':
            new_l = (l.x + 1, l.y)
        elif d == 'WEST':
            new_l = (l.x - 1, l.y)
        else:
            new_l = (l.x, l.y)

        temp = self[new_l]

        if new_l == (l.x, l.y):
            pass
        elif self[new_l] in ' _~':
            self[l.x, l.y] = ' '
            self.update_tile(l.x, l.y)
            l.x, l.y = new_l[0], new_l[1]
            self[new_l] = 'Z'
            self.update_location_adjacent(l)
        elif self[new_l] == 'Z':
            pass
        elif self[new_l] == '#':
            z = self.find_zergcontext_at( (l.x, l.y) )
            z.zerg.health -= 1
        elif self[new_l] == '*':
            m = self.find_mineralcontext_at( new_l )
            if m.amt > 0:
                m.amt -= 1
                z = self.find_zergcontext_at( (l.x, l.y) )
                z.mineral += 1

                if m.amt <= 0:
                    self[m.location.x, m.location.y] = ' '
                    self.update_tile(m.location.x, m.location.y)
                    self.mineral.remove(m)
        else:
            raise Exception('UNKNOWN TERRAIN')

    def update_tile(self, x, y):
        if (x,y) == self.landing_zone:
            self[ x,y ] = '_'
        elif (x,y) in self.acid:
            self[ x,y ] = '~'


    def tick(self):
# This may be duplicate and unecessary now tha the act of mining
# could remove the minerals.

        for z in self.zerg: 

            d = 'CENTER'
            try:
                
                for _ in range(z.zerg.moves):
                    self.update_location_adjacent(z.location)
                    pos = z.location.x, z.location.y


                    for m in self.mineral:
                        if m.amt <= 0:
                            self[m.location.x, m.location.y] = ' '
                            self.update_tile(m.location.x, m.location.y)
                            self.mineral.remove(m)

                    if (z.location.x, z.location.y) in self.acid:
                        logging.debug("{} has stepped in acid!".format(id(z.zerg)))
                        z.zerg.health -= 3 # Mulitple moves within a tick - necessary to account for here
                    if z.zerg.health <= 0:
                        self[z.location.x, z.location.y] = ' '
                        self.update_tile(z.location.x, z.location.y)
                        if z in self.zerg:
                            self.zerg.remove(z)
                    

                    with timeout.within(1000/z.zerg.moves):
                        #fuck_Dave = copy(z.location)
                        #fuck_Dave.x = id(z.location.x)
                        #fuck_Dave.y = id(z.location.y)
                        #d = z.zerg.action(fuck_Dave)
                        d = z.zerg.action(z.location)
                    logging.debug("{} said '{}'".format(id(z.zerg), d))
# Reset location position so that the zerg cannot track or abuse it
                    z.location = Location(pos[0], pos[1])
                    self.update_location_adjacent(z.location)
                    if z in self.zerg:
                        self.move_to(z.location, d)


                    if z.zerg.health <= 0:
                        logging.debug("{} is ded...".format(id(z.zerg)))
                        break #zerg is dead move on to next

            except timeout.TimeoutError:
                logging.debug("{} TIMEDOUT".format(id(z.zerg)))

    def print_map(self):
        temp_map = self.data[:]
        for mineral in self.mineral:
            temp_map[mineral.location.y][mineral.location.x] = str(mineral.amt)
        print('\n'.join([''.join(i) for i in reversed(temp_map)]))


class MineralContext:
    def __init__(self, l, amt):
        self.location = l
        self.amt = amt

class DroneContext:
    def __init__(self, l, z, hp):
        self.location = l
        self.zerg = z
#TODO: This should be maintained independent of whichever map they are on
        self.hp = hp
        self.mineral = 0

if __name__ == '__main__':
    if len(argv) == 4:
        seed(argv[3])
    if len(argv) >= 3:
        Map(int(argv[1]), int(argv[2])).print_map()
