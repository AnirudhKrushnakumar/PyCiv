class Terrain:
    def __init__(self, food, gold, wood, stone, defense_bonus=1.0):
        self.food = food
        self.gold = gold
        self.wood = wood
        self.stone = stone
        self.defense_bonus = defense_bonus


terrain_data = {
    "plains": Terrain(food=4, gold=1, wood=1, stone=1),
    "forest": Terrain(food=2, gold=1, wood=4, stone=1),
    "mountains": Terrain(
        food=1,
        gold=3,
        wood=1,
        stone=4,
        defense_bonus=1.5,
    ),
}
