import random
from config import terrain_data


class Faction:
    def __init__(
        self,
        name,
        code,
        color,
        description,
        leader=None,
        focus_territory=None,
        is_nomadic=False,
    ):
        self.name = name
        self.code = code
        self.color = color
        self.description = description
        self.leader = leader or {}
        self.focus_territory = focus_territory
        self.is_nomadic = is_nomadic

        self.population = 100
        self.resources = {"gold": 100, "food": 100, "wood": 100, "stone": 100}
        self.capital = None
        self.territory = set()
        self.diplomacy = {}

    def __str__(self):
        leader_display = self.leader.get("name", "None (Decentralized)")
        focus_display = self.focus_territory or (
            "Nomadic (All)" if self.is_nomadic else "None"
        )
        return (
            f"Faction: {self.name} ({self.code})\n"
            f"Description: {self.description}\n"
            f"Type: {'Nomadic' if self.is_nomadic else 'Settled'}\n"
            f"Population: {int(self.population)}\n"
            f"Leader: {leader_display}\n"
            f"Resources: { {k: round(v, 1) for k, v in self.resources.items()} }\n"
            f"Territory: {self.territory}\n"
            f"Focus Territory: {focus_display}\n"
            f"Diplomacy: {self.diplomacy}"
        )

    def is_alive(self):
        if self.is_nomadic:
            return self.population > 0
        return self.population > 0 and len(self.territory) > 0

    def claim_tile(self, coordinates):
        coord = tuple(coordinates)
        if coord not in self.territory:
            self.territory.add(coord)
            if not self.capital and not self.is_nomadic:
                self.capital = coord
            return True
        return False

    def lose_tile(self, coordinates):
        coord = tuple(coordinates)
        if coord in self.territory:
            self.territory.remove(coord)
            if coord == self.capital:
                self.capital = (
                    random.choice(list(self.territory))
                    if self.territory
                    else None
                )
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

        if self.is_nomadic and not self.territory:
            food_income += 15
            gold_income += 2
            wood_income += 3
        else:
            for row, col in self.territory:
                biome = world_map.get_terrain(row, col)
                terrain = terrain_data[biome]
                bonus = (
                    1.2
                    if (
                        self.focus_territory
                        and biome == self.focus_territory
                    )
                    else 1.0
                )
                food_income += terrain.food * bonus
                gold_income += terrain.gold * bonus
                wood_income += terrain.wood * bonus
                stone_income += terrain.stone * bonus

        season_multipliers = {
            "Winter": (0.5, 0.8, 0.8, 0.8),
            "Autumn": (0.8, 0.9, 0.9, 0.9),
            "Spring": (1.1, 1.0, 1.0, 1.0),
            "Summer": (1.2, 1.1, 1.1, 1.1),
        }

        if season in season_multipliers:
            f_mult, g_mult, w_mult, s_mult = season_multipliers[season]
            food_income *= f_mult
            gold_income *= g_mult
            wood_income *= w_mult
            stone_income *= s_mult

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

    def calculate_combat_strength(self, biome, is_attacking):
        base_strength = self.population * random.uniform(0.8, 1.2)

        if self.focus_territory and biome == self.focus_territory:
            base_strength *= 1.25

        if not is_attacking:
            base_strength *= terrain_data[biome].defense_bonus
            if (
                not self.leader
                and self.focus_territory
                and biome == self.focus_territory
            ):
                base_strength *= 1.15

        if self.leader.get("trait") == "Warlord" and is_attacking:
            base_strength *= 1.15

        if self.is_nomadic and is_attacking:
            base_strength *= 1.10

        return base_strength

    def get_relation(self, other_code):
        return self.diplomacy.get(other_code, "Neutral")

    def set_relation(self, other_code, status):
        self.diplomacy[other_code] = status
