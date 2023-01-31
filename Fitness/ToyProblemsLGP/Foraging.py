import random
import time

from Fitness.AbstractFitness import AbstractFitness
from Fitness.libs.ForageProblem import ForageProblem


class Foraging(AbstractFitness):

	def __init__(self) -> None:
		super().__init__()
		# 0 is empty space, 1 is obstacle, 2 is food, 3 is agent facing north, 4 is agent facing east,
		# 5 is agent facing south, 6 is agent facing west
		forage_map = [
			[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 2, 0, 2, 0, 0, 2, 0, 1, 1, 0, 1, 1],
			[1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 2, 0, 1, 1],
			[1, 1, 0, 2, 0, 0, 1, 0, 2, 2, 0, 0, 1, 1],
			[1, 1, 0, 1, 1, 1, 1, 0, 0, 2, 0, 0, 1, 1],
			[1, 1, 0, 1, 2, 0, 0, 0, 0, 0, 2, 1, 1, 1],
			[1, 1, 0, 0, 0, 0, 2, 0, 1, 1, 0, 0, 1, 1],
			[1, 1, 1, 2, 0, 1, 1, 2, 0, 0, 0, 2, 1, 1],
			[1, 1, 0, 0, 2, 1, 0, 0, 2, 0, 1, 0, 1, 1],
			[1, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1],
			[1, 1, 2, 1, 0, 2, 0, 3, 0, 0, 0, 2, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		]
		self.task = ForageProblem(forage_map)

	def preprocess(self, indv):
		return super().preprocess(indv)

	def evaluate(self, individual):
		fitness = 0
		# obs is the values for the vision cone (two 3-tile rows in front)
		obs, done, reward = self.task.reset()
		for i in range(200):

			# print(obs, done, reward)
			input_dict = {"x0": obs[0], "x1": obs[1], "x2": obs[2], "x3": obs[3], "x4": obs[4], "x5": obs[5]}

			output, registers = individual.individual_eval(input_dict)

			output = int(output)

			if output <= 0:
				output = 0
			elif output >= 2:
				output = 2

			action = output

			obs, done, reward = self.task.step(action)

			fitness = reward
			if done:
				break
		return fitness, 0, 0

	def postprocess(self, individual):
		return super().postprocess(individual)
