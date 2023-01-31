from Fitness.AbstractFitness import AbstractFitness
from Fitness.ArtificialAnt import ArtificialAnt


class TestProblem(AbstractFitness):

	def __init__(self) -> None:
		super().__init__()

	def preprocess(self, indv):
		return super().preprocess(indv)

	def evaluate(self, individual):
		# in_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		# # inputs = {"x": in_1[6]}
		# # individual.show_execution_flow(inputs)
		# # exit()
		# in_2 = [1, 1, 1, 8, 2, 5, 7, 8, 8, 6, 10]
		# fitness = 0
		# correct_outputs = ['right', 'no_action', 'left', 'right', 'left', 'no_action', 'right', 'right', 'no_action', 'left', 'no_action']
		# outputs = []
		# for i in in_1:
		# 	inputs = {"x": in_1[i], "y": in_2[i]}
		#
		# 	output, registers = individual.individual_eval(inputs)
		# 	# individual.visualize()
		# 	# print(output)
		# 	outputs.append(output)
		# 	with open("anghazi.shayan", "r") as f:
		# 		if f.read() == "1":
		# 			title = str(individual.individual_index) + " attempt " + str(i)
		# 			individual.show_execution_flow(inputs, title=title)
		#
		# for i in range(11):
		# 	if outputs[i] == correct_outputs[i]:
		# 		fitness += 1
		#
		# if [outputs[0]] * 11 == outputs:
		# 	fitness = 0
		#
		# if fitness >= 11:
		# 	print(outputs)
		# if individual.individual_index == 0:
		# 	print(outputs)
		fitness = 0
		return fitness, 0, 0

	def postprocess(self, individual):
		return super().postprocess(individual)
