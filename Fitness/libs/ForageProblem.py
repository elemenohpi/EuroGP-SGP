import copy


class ForageProblem:
	# Observation Space: Two 3-tile rows in front of the agent
	# Action Space: 0 Left, 1 Right, 2 Move
	# Goal: Gather all food in limited steps
	def __init__(self, forage_map):
		self.reward = 0
		self.food_count = 0
		self.forage_map = copy.deepcopy(forage_map)
		self.map = copy.deepcopy(forage_map)
		self.agent_pos = (-1, -1)
		self.done = False
		# count the food
		_, _, _ = self.reset()

	def reset(self):
		self.map = copy.deepcopy(self.forage_map)
		self.agent_pos = (-1, -1)
		self.food_count = 0
		self.reward = 0
		for x, rows in enumerate(self.map):
			for y, tile in enumerate(rows):
				if tile == 2:
					self.food_count += 1
				if tile == 3 or tile == 4 or tile == 5 or tile == 6:
					self.agent_pos = (x, y)
		obs = self.get_obs()
		return obs, self.done, self.reward

	def get_obs(self):
		x = self.agent_pos[0]
		y = self.agent_pos[1]
		agent_direction = self.map[x][y]
		if agent_direction == 3:
			obs = [self.map[x-1][y-1], self.map[x-1][y], self.map[x-1][y+1],
			       self.map[x-2][y-1], self.map[x-2][y], self.map[x-2][y+1]]
		elif agent_direction == 4:
			obs = [self.map[x - 1][y + 1], self.map[x][y + 1], self.map[x + 1][y + 1],
			       self.map[x - 1][y + 2], self.map[x][y + 2], self.map[x + 1][y + 2]]
		elif agent_direction == 5:
			obs = [self.map[x+1][y+1], self.map[x+1][y], self.map[x+1][y-1],
			       self.map[x+2][y+1], self.map[x+2][y], self.map[x+2][y-1]]
		elif agent_direction == 6:
			obs = [self.map[x + 1][y - 1], self.map[x][y - 1], self.map[x - 1][y - 1],
			       self.map[x + 1][y - 2], self.map[x][y - 2], self.map[x - 1][y - 2]]
		else:
			raise "unknown agent direction"
		return obs

	def step(self, action):
		# 0 left, 1 right, 2 move
		x = self.agent_pos[0]
		y = self.agent_pos[1]
		current_direction = self.map[x][y]

		if action == 0:
			new_direction = current_direction - 1
			if new_direction < 3:
				new_direction = 6
			self.map[x][y] = new_direction
		elif action == 1:
			new_direction = current_direction + 1
			if new_direction > 6:
				new_direction = 3
			self.map[x][y] = new_direction
		elif action == 2:
			if current_direction == 3 and self.map[x-1][y] != 1:
				if self.map[x-1][y] == 2:  # reward is found
					self.reward += 1  # add to total rewards
				self.map[x-1][y] = self.map[x][y]  # moves forward 1 tile
				self.map[x][y] = 0  # previous tile is reset
				self.agent_pos = (x-1, y)  # agent pos is updated
			elif current_direction == 4 and self.map[x][y+1] != 1:
				if self.map[x][y+1] == 2:
					self.reward += 1
				self.map[x][y+1] = self.map[x][y]
				self.map[x][y] = 0
				self.agent_pos = (x, y+1)
			elif current_direction == 5 and self.map[x+1][y] != 1:
				if self.map[x+1][y] == 2:
					self.reward += 1
				self.map[x+1][y] = self.map[x][y]
				self.map[x][y] = 0
				self.agent_pos = (x+1, y)
			elif current_direction == 6 and self.map[x][y-1] != 1:
				if self.map[x][y-1] == 2:
					self.reward += 1
				self.map[x][y-1] = self.map[x][y]
				self.map[x][y] = 0
				self.agent_pos = (x, y-1)
		if self.reward == self.food_count:
			self.done = True
		obs = self.get_obs()
		return obs, self.done, self.reward
