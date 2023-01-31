import random
import time

from Fitness.AbstractFitness import AbstractFitness
from Fitness.libs.ObstacleAvoidance import ObstacleAvoidance


class ObstacleAvoidanceProblem(AbstractFitness):

	def __init__(self) -> None:
		super().__init__()
		# 0 is empty space, 1 is obstacle, 2 is treasure, 3 is agent facing north, 4 is agent facing east,
		# 5 is agent facing south, 6 is agent facing west, 7 is end tile, 8 is a trap

		self.task = ObstacleAvoidance()

	def preprocess(self, indv):
		return super().preprocess(indv)

	def evaluate(self, individual):
		fitness = 0
		# obs, done, reward = self.task.reset()
		# self.task.show_map()
		# while not self.task.done:
		# 	action = int(input("enter action: "))
		# 	obs, reward, done = self.task.step(action)
		# 	self.task.show_map()
		# 	print(obs, reward, done)
		# 	if self.task.done:
		# 		exit()
		# obs is the values for the vision cone (two 3-tile rows in front)

		for j in range(5):
			obs, done, reward = self.task.reset()
			for i in range(100):
				input_dict = {"x0": obs[0], "x1": obs[1], "x2": obs[2], "x3": obs[3], "x4": obs[4], "x5": obs[5],
				              "x6": obs[6], "x7": obs[7], "x8": obs[8], "x9": obs[3], "x10": obs[4], "x11": obs[5]}

				output, registers = individual.individual_eval(input_dict)

				action = int(output)

				obs, done, reward = self.task.step(action)
				# if individual.individual_index == 0:
				# 	print("action", action)
				# 	self.task.show_map()
				# 	print("reward", reward)

				if done:
					break
			fitness += reward
		# print("reward: ", reward, individual.individual_index)
		# print("==================")
		return fitness/5, 0, 0

	def postprocess(self, individual):
		return super().postprocess(individual)
