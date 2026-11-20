from config import terrain_data


class World:
	def __init__(self, terrain_grid):
		if not terrain_grid:
			raise ValueError("terrain_grid must not be empty")

		width = len(terrain_grid[0])
		if width == 0 or any(len(row) != width for row in terrain_grid):
			raise ValueError("terrain_grid must be a non-empty rectangle")

		for row in terrain_grid:
			for terrain in row:
				if terrain not in terrain_data:
					raise ValueError(f"Unknown terrain: {terrain}")

		self.terrain_grid = [list(row) for row in terrain_grid]

	def get_terrain(self, row, col):
		return self.terrain_grid[row][col]
