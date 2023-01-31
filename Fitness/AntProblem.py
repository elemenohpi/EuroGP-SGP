from Fitness.AbstractFitness import AbstractFitness
from Fitness.ArtificialAnt import ArtificialAnt


class AntProblem(AbstractFitness):

	def __init__(self) -> None:
		super().__init__()

	def preprocess(self, indv):
		return super().preprocess(indv)

	def evaluate(self, individual):
		simulator = ArtificialAnt.AntSimulator(600)
		inputs = {"simulator": simulator}
		individual.individual_eval(inputs)
		fitness = simulator.eaten + 0.001 * simulator.moves
		return fitness, simulator.moves, 0

	def postprocess(self, individual):
		return super().postprocess(individual)
