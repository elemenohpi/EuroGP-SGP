from Fitness.AbstractFitness import AbstractFitness
import gym
import warnings

warnings.filterwarnings('ignore')


class Pendulum(AbstractFitness):

	def __init__(self) -> None:
		super().__init__()

	def preprocess(self, indv):
		return super().preprocess(indv)

	def evaluate(self, individual):
		env = gym.make('Pendulum-v1', g=9.81)

		fitness = 0

		# reset the environment and see the initial observation
		obs = env.reset()

		# env.render(mode="human")
		for i in range(201):
			# env.render(mode="human")

			input_dict = {"cost": obs[0], "sina": obs[1], "ang_velo": obs[2]}
			output, registers = individual.individual_eval(input_dict)

			if output > 2:
				output = 2
			elif output < -2:
				output = -2

			# print(env.action_space)
			output = [output]
			obs, reward, done, info = env.step(output)
			# print("The new observation is {}".format(obs))
			# print("Reward {}".format(reward))
			# print("Done {}".format(done))
			# print("Info {}".format(info))

			fitness = reward
			if done:
				break

		return fitness, 0, 0

	def postprocess(self, individual):
		return super().postprocess(individual)
