import random
from config import terrain_data

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

    def update_economy(self, season, world_map):
        if not self.is_alive():
            self.population = 0
            return

        food_income = 0
        gold_income = 0
        wood_income = 0
        stone_income = 0

        for row, col in self.territory:
            biome = world_map.get_terrain(row, col)
            terrain = terrain_data[biome]
            bonus = 1.2 if biome == self.focus_territory else 1.0
            food_income += terrain.food * bonus
            gold_income += terrain.gold * bonus
            wood_income += terrain.wood * bonus
            stone_income += terrain.stone * bonus

        if season == "Winter":
            food_income *= 0.5
            gold_income *= 0.8
            wood_income *= 0.8
            stone_income *= 0.8
        elif season == "Autumn":
            food_income *= 0.8
            gold_income *= 0.9
            wood_income *= 0.9
            stone_income *= 0.9
        elif season == "Spring":
            food_income *= 1.1
            gold_income *= 1.0
            wood_income *= 1.0
            stone_income *= 1.0
        elif season == "Summer":
            food_income *= 1.2
            gold_income *= 1.1
            wood_income *= 1.1
            stone_income *= 1.1

        food_needed = self.population * 0.1
        net_food = food_income - food_needed

        self.resources["gold"] += gold_income
        self.resources["wood"] += wood_income
        self.resources["stone"] += stone_income

        if net_food >= 0:
            self.resources["food"] += net_food
            self.population += net_food * 0.5
        else:
            self.resources["food"] += net_food
            if self.resources["food"] < 0:
                starvation = abs(self.resources["food"]) * 2
                self.population = max(0, self.population - starvation)
                self.resources["food"] = 0