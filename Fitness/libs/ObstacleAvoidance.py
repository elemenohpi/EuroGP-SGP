import copy
import random


class ObstacleAvoidance:
	# Observation Space: Three 3-tile rows in front of the agent
	# Action Space: 0 Left, 1 Right, 2 NoAction
	# Goal: Survive the incoming obstacles as long as possible
	def __init__(self):
		self.reward = 0
		self.step_count = 0
		# 3 is the agent
		# 2 is obstacle
		# 1 is road block
		self.inc_patterns = [
			[1, 2, 2, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 2, 0, 2, 0, 1],
			[1, 2, 0, 0, 0, 0, 0, 2, 1],
			[1, 0, 2, 2, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 2, 0, 2, 1],
			[1, 2, 0, 2, 0, 0, 2, 0, 1],
			[1, 2, 0, 0, 2, 0, 0, 2, 1],
			[1, 2, 0, 0, 0, 2, 2, 0, 1],
			[1, 0, 0, 2, 0, 2, 0, 0, 1]
		]
		self.map = [[1, 0, 0, 0, 0, 0, 0, 0, 1],
		            [1, 0, 0, 0, 0, 0, 0, 0, 1],
		            [1, 0, 0, 0, 0, 0, 0, 0, 1],
		            [1, 0, 0, 0, 0, 0, 0, 0, 1],
		            [1, 0, 0, 0, 0, 0, 0, 0, 1],
		            [1, 0, 0, 0, 3, 0, 0, 0, 1]]

		self.agent_pos = (-1, -1)
		self.done = False
		# count the food
		_, _, _ = self.reset()

	def reset(self):
		self.reward = 0
		self.done = False
		self.agent_pos = (5, 4)
		self.map = [[1, 0, 0, 0, 0, 0, 0, 0, 1],
		            [1, 0, 0, 0, 0, 0, 0, 0, 1],
		            [1, 0, 0, 0, 0, 0, 0, 0, 1],
		            [1, 0, 0, 0, 0, 0, 0, 0, 1],
		            [1, 0, 0, 0, 0, 0, 0, 0, 1],
		            [1, 0, 0, 0, 3, 0, 0, 0, 1]]
		obs = self.get_obs()
		return obs, self.done, self.reward

	def get_obs(self):
		x = self.agent_pos[0]
		y = self.agent_pos[1]

		obs = [self.map[x-1][y-1], self.map[x-1][y], self.map[x-1][y+1],
		       self.map[x-2][y-1], self.map[x-2][y], self.map[x-2][y+1],
		       self.map[x-3][y-1], self.map[x-3][y], self.map[x-3][y+1],
		       self.map[x-4][y-1], self.map[x-4][y], self.map[x-4][y+1]
		       ]

		return obs

	def step(self, action):
		# 0 left, 1 right, 2 no action
		x = self.agent_pos[0]
		y = self.agent_pos[1]
		self.step_count += 1

		if action == 0 and self.map[x][y - 1] == 0:
			self.map[x][y - 1] = 3  # agent moves left
			self.map[x][y] = 0
			self.agent_pos = (x, y-1)
		elif action == 1 and self.map[x][y + 1] == 0:
			self.map[x][y + 1] = 3  # agent moves right
			self.map[x][y] = 0
			self.agent_pos = (x, y+1)
		elif action == 2:
			pass
		elif action != 0 and action != 1 and action != 2:
			print("illegal action")
			exit()

		# check end game scenario
		if self.map[x-1][y] == 2:
			self.done = True
		else:
			self.reward += 1

		# update the incoming patterns
		self.update_map()

		obs = self.get_obs()
		return obs, self.done, self.reward

	def update_map(self):
		self.map[-2] = copy.deepcopy(self.map[-3])
		self.map[-3] = copy.deepcopy(self.map[-4])
		self.map[-4] = copy.deepcopy(self.map[-5])
		self.map[-5] = copy.deepcopy(self.map[-6])  # this is self.map[0]
		# if self.step_count % 3 < 2:
		self.map[0] = copy.deepcopy(random.choice(self.inc_patterns))
		# else:
		# 	self.map[0] = [1, 0, 0, 0, 0, 0, 0, 0, 1]

	def show_map(self):
		for row in self.map:
			print(row)
