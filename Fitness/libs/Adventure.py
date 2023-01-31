import copy


class Adventure:
	# Observation Space: Two 3-tile rows in front of the agent
	# Action Space: 0 Left, 1 Right, 2 Move
	# Goal: Find the treasure and go back to the end tile
	def __init__(self, adventure_map):
		self.reward = 0
		self.adventure_map = copy.deepcopy(adventure_map)
		self.map = copy.deepcopy(self.adventure_map)
		self.agent_pos = (-1, -1)
		self.done = False
		self.treasure_found = False
		# count the food
		_, _, _ = self.reset()

	def reset(self):
		self.done = False
		self.map = copy.deepcopy(self.adventure_map)
		self.treasure_found = False
		self.agent_pos = (-1, -1)
		self.reward = 0
		for x, rows in enumerate(self.map):
			for y, tile in enumerate(rows):
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
			print("False agent direction", agent_direction)
			exit()
		if self.treasure_found:
			obs.append(1)
		else:
			obs.append(0)
		return obs

	def show_map(self):
		for row in self.map:
			print(row)

	def step(self, action):
		if self.done:
			print("Step after done: ", self.done)
			exit()
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
			# 0 is empty space, 1 is obstacle, 2 is treasure, 7 is end tile, 8 is a trap
			dest = -1
			dest_pos = (-1, -1)
			if current_direction == 3:
				dest = self.map[x-1][y]
				dest_pos = (x-1, y)
			elif current_direction == 4:
				dest = self.map[x][y+1]
				dest_pos = (x, y+1)
			elif current_direction == 5:
				dest = self.map[x+1][y]
				dest_pos = (x+1, y)
			elif current_direction == 6:
				dest = self.map[x][y-1]
				dest_pos = (x, y-1)
			if dest != 1:
				if dest == 2:  # treasure is found
					self.reward += 10  # add to total rewards
					self.treasure_found = True
				elif dest == 8:  # trap found, end
					self.done = True
				if self.treasure_found is True and dest == 7:
					self.done = True
					self.reward += 20

				if self.treasure_found is False and dest == 7:
					pass
				else:
					self.map[dest_pos[0]][dest_pos[1]] = self.map[x][y]  # moves forward 1 tile
					self.map[x][y] = 0  # previous tile is reset
					self.agent_pos = dest_pos  # agent pos is updated
					self.reward += 0.01
		obs = self.get_obs()
		return obs, self.done, self.reward
