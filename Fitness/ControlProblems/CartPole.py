from Fitness.AbstractFitness import AbstractFitness
import gym
import warnings

# warnings.filterwarnings('ignore')


class CartPole(AbstractFitness):

	def __init__(self) -> None:
		super().__init__()

	def preprocess(self, indv):
		return super().preprocess(indv)

	def evaluate(self, individual):
		env = gym.make('CartPole-v1')

		fitness = 0

		# reset the environment and see the initial observation
		obs = env.reset()

		# env.render(mode="human")
		for i in range(501):
			# env.render(mode="human")
			# random_action = env.action_space.sample()
			input_dict = {"cart_pos": obs[0], "cart_velo": obs[1], "pole_angle": obs[2],
			              "pole_velo": obs[3]}
			output, registers = individual.individual_eval(input_dict)
			action = int(output)
			obs, reward, done, info = env.step(action)
			# print("The new observation is {}".format(obs))
			# print("Reward {}".format(reward))
			# print("Done {}".format(done))
			# print("Info {}".format(info))
			fitness += reward
			if done:
				break

		return fitness, 0, 0

	def postprocess(self, individual):
		return super().postprocess(individual)
