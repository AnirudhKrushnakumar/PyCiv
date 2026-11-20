import random
import os
import time

class Faction:
    def __init__(self, name, code, color, description, leader, focus_territory):
        self.name = name
        self.code = code
        self.color = color
        self.description = description
        self.leader = leader
        self.focus_territory = focus_territory

        self.population = 100
        self.resources = {"gold": 100, "food": 100, "wood": 100, "stone": 100}
        self.capital = None
        self.territory = set()
        self.diplomacy = {}

    def __str__(self):
        return f"Faction: {self.name}\nDescription: {self.description}\nPopulation: {self.population}\nLeader: {self.leader}\nResources: {self.resources}\nTerritory: {self.territory}\nFocus Territory: {self.focus_territory}\nDiplomacy: {self.diplomacy}"

    def is_alive(self):
        return self.population > 0 and len(self.territory) > 0

    def claim_tile(self, coordinates):
        coord = tuple(coordinates)
        if coord not in self.territory:
            self.territory.add(coord)
            return True
        return False

    def lose_tile(self, coordinates):
        coord = tuple(coordinates)
        if coord in self.territory:
            self.territory.remove(coord)
            if coord == self.capital:
                self.capital = random.choice(list(self.territory)) if self.territory else None
            return True
        return False