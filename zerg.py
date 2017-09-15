#!/usr/local/bin/python

from random import randint, choice

class Drone:
    def __init__(self):
        self.health = 20 
        self.moves = randint(1,6)
        self.capacity = 6

    def action(self, context):
        new = randint(0, 3)
        if new == 0:
            return 'NORTH'
        elif new == 1:
            return 'SOUTH'
        elif new == 2:
            return 'EAST'
        elif new == 3:
            return 'WEST'
        else:
            return 'CENTER'

class Overlord:
    def __init__(self, total_ticks, refined_minerals=54):
        self.maps = {}
        self.zerg = {}

        for _ in range(6):
            z = Drone()
            self.zerg[id(z)] = z

    def add_map(self, map_id, summary):
        self.maps[map_id] = summary

    def action(self):
        act = randint(0, 3)
        if act == 0:
            return 'RETURN {}'.format(choice(list(self.zerg.keys())))
        elif act == 1 or act ==2:
            return 'DEPLOY {} {}'.format(choice(list(self.zerg.keys())),
                    choice(list(self.maps.keys())))
        else:
            return 'NONE'

