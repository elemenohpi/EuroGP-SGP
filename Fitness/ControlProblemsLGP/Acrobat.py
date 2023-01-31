from Fitness.AbstractFitness import AbstractFitness
import gym
import warnings

warnings.filterwarnings('ignore')


class Acrobat(AbstractFitness):

	def __init__(self) -> None:
		super().__init__()

	def preprocess(self, indv):
		return super().preprocess(indv)

	def evaluate(self, individual):
		env = gym.make('Acrobot-v1')

		fitness = 0

		# reset the environment and see the initial observation
		obs = env.reset()

		# env.render(mode="human")
		for i in range(200):
			# env.render(mode="human")
			# random_action = env.action_space.sample()
			input_dict = {"cost": obs[0], "sint": obs[1], "cost2": obs[2], "sint2": obs[3], "ang_velo_t1": obs[4],
			              "ang_velo_t2": obs[5]}
			output, registers = individual.individual_eval(input_dict)
			output = int(output)
			# print("output", output)
			if output <= 0:
				output = 0
			elif output >= 2:
				output = 2

			action = output

			# print("action", action)

			obs, reward, done, info = env.step(action)
			# print("The new observation is {}".format(obs))
			# print("Reward {}".format(reward))
			# print("Done {}".format(done))
			# print("Info {}".format(info))
			fitness += reward
			if done:
				break
		# print(individual.individual_index)
		# print(fitness)
		return fitness, 0, 0

	def postprocess(self, individual):
		return super().postprocess(individual)
