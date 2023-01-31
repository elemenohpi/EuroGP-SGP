import random
import math
from Fitness.AbstractFitness import AbstractFitness
from scipy import stats
import numpy as np
import warnings
#
warnings.filterwarnings('ignore')


class E18(AbstractFitness):

    def __init__(self) -> None:
        super().__init__()
        self.data_points = 10
        self.x1_set = [1, 2, 4, 6, 3, 6, 2, 6, 1, 1]
        self.x2_set = [3, 4, 4, 9, 5, 1, 3, 1, 2, 7]
        self.x3_set = [1, 8, 5, 0, 2, 2, 4, 9, 2, 3]
        self.x4_set = [5, 1, 5, 3, 7, 3, 5, 3, 3, 4]
        self.x5_set = [2, 7, 6, 4, 2, 4, 7, 4, 6, 2]
        # self.x5_set = [random.randint(0, 10) for _ in range(self.data_points)]

    def preprocess(self, indv):
        return super().preprocess(indv)

    def evaluate(self, individual):
        measured_values = []
        estimated_values = []
        for i in range(self.data_points):
            x1 = self.x1_set[i]
            x2 = self.x2_set[i]
            x3 = self.x3_set[i]
            x4 = self.x4_set[i]
            x5 = self.x5_set[i]
            inputs_dict = {"x1": x1, "x2": x2, "x3": x3, "x4": x4, "x5": x5}
            measured = x1 * x2 * x3 * x4 * x5
            estimated, registers = individual.individual_eval(inputs_dict)
            measured_values.append(measured)
            # print(registers)
            estimated_values.append(estimated)  # rather than using estimated

        # Correlation
        # try:
        # print(estimated_values)
        if measured_values != estimated_values and estimated_values == [estimated_values[0]] * self.data_points:
            return 1, "inf", 0

        try:
            rvalues = stats.pearsonr(estimated_values, measured_values)
        except ValueError:
            return 1, "inf", 0

        try:
            align = np.polyfit(estimated_values, measured_values, 1)
        except:
            align = [0, 0]

        squared_error = 0
        for index in range(self.data_points):
            squared_error += ((measured_values[index] * align[0] + align[1]) - estimated_values[index]) ** 2
        post_mse = squared_error / self.data_points
        post_rmse = math.sqrt(squared_error / self.data_points)

        fitness = 1 - rvalues[0] ** 2

        return fitness, post_mse, post_rmse

        # squared_error = 0
        # for index in range(self.data_points):
        #     squared_error += (measured_values[index] - estimated_values[index]) ** 2
        # rmse = math.sqrt(squared_error / self.data_points)
        #
        #
        #
        # return rmse, 0, 0

    def postprocess(self, indv):
        return super().postprocess(indv)
