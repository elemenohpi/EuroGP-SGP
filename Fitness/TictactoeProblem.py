from Fitness.AbstractFitness import AbstractFitness
from Fitness.SimpleDecisionMakingTasks import TicTacToe


class TictactoeProblem(AbstractFitness):

	def __init__(self) -> None:
		super().__init__()

	def preprocess(self, indv):
		return super().preprocess(indv)

	def evaluate(self, individual):
		game = TicTacToe.TicTacToe()
		total_fitness = 0
		for _ in range(20):
			game.reset()
			while not game.is_finished():
				states = game.get_state()
				inputs = {}
				for index, state in enumerate(states):
					inputs["c" + str(index)] = state
				# individual.reset()
				output, registers = individual.individual_eval(inputs)
				output = int(round(output, 1))
				if output > 8:
					output = 8
				if output < 0:
					output = 0
				game.play_turn(output)
			fitness = round(game.ai_score, 2)
			total_fitness += fitness

		return round(total_fitness, 2), 0, 0

	def postprocess(self, individual):
		return super().postprocess(individual)
