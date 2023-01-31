from Fitness.AbstractFitness import AbstractFitness
import gym
import warnings

warnings.filterwarnings('ignore')


class MountainCar(AbstractFitness):

	def __init__(self) -> None:
		super().__init__()

	def preprocess(self, indv):
		return super().preprocess(indv)

	def evaluate(self, individual):
		fitness = -0.5
		env = gym.make('MountainCar-v0')
		obs = env.reset()
		pos = obs[0]
		velocity = obs[1]
		input_dict = {"pos": pos, "velocity": velocity}
		steps = 100

		for step in range(steps):
			action, registers = individual.individual_eval(input_dict)
			# print(action)
			action = int(action)
			new_obs, reward, done, info = env.step(action)
			if fitness < new_obs[0]:
				fitness = new_obs[0]
			new_pos = new_obs[0]
			new_velocity = new_obs[1]
			input_dict = {"pos": new_pos, "velocity": new_velocity}
		return fitness, 0, 0

	def postprocess(self, individual):
		return super().postprocess(individual)
