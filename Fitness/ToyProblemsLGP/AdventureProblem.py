import random
import time

from Fitness.AbstractFitness import AbstractFitness
from Fitness.libs.Adventure import Adventure


class AdventureProblem(AbstractFitness):

	def __init__(self) -> None:
		super().__init__()
		# 0 is empty space, 1 is obstacle, 2 is treasure, 3 is agent facing north, 4 is agent facing east,
		# 5 is agent facing south, 6 is agent facing west, 7 is end tile, 8 is a trap
		adventure_map = [
			[1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 0, 0, 0, 8, 8, 1, 1],
			[1, 1, 2, 8, 0, 0, 0, 1, 1],
			[1, 1, 0, 0, 0, 8, 7, 1, 1],
			[1, 1, 0, 8, 0, 0, 0, 1, 1],
			[1, 1, 8, 0, 3, 0, 8, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1, 1],
		]
		self.task = Adventure(adventure_map)

	def preprocess(self, indv):
		return super().preprocess(indv)

	def evaluate(self, individual):
		fitness = 0
		# obs is the values for the vision cone (two 3-tile rows in front)
		obs, done, reward = self.task.reset()


		# print("=================", individual.individual_index)
		# if individual.individual_index == 67:
		# 	self.task.show_map()
		for i in range(100):

			# print(obs, done, reward)
			input_dict = {"x0": obs[0], "x1": obs[1], "x2": obs[2], "x3": obs[3], "x4": obs[4], "x5": obs[5], "treasure": obs[6]}

			output, registers = individual.individual_eval(input_dict)

			output = int(output)

			if output <= 0:
				output = 0
			elif output >= 2:
				output = 2

			action = output

			# print(obs, done, reward, action)
			obs, done, reward = self.task.step(action)

			# if individual.individual_index == 67:
			# 	print("action", action)
			# 	self.task.show_map()
			# 	print("reward", reward)
			fitness = reward

			if done:
				break

		return fitness, 0, 0

	def postprocess(self, individual):
		return super().postprocess(individual)
