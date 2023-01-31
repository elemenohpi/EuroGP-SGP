import random
import math
from Fitness.AbstractFitness import AbstractFitness
from scipy import stats
import numpy as np
import warnings
#
warnings.filterwarnings('ignore')


class E19(AbstractFitness):

    def __init__(self) -> None:
        super().__init__()
        self.data_points = 10
        self.x1_set = [random.randint(0, 10) for _ in range(self.data_points)]
        self.x2_set = [random.randint(0, 10) for _ in range(self.data_points)]
        self.x3_set = [random.randint(0, 10) for _ in range(self.data_points)]
        self.x4_set = [random.randint(0, 10) for _ in range(self.data_points)]
        self.x5_set = [random.randint(0, 10) for _ in range(self.data_points)]

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
            measured = 12 - 6 * math.tan(x1) / (math.exp(x2)) * (x3 - math.tan(x4))
            estimated, registers = individual.individual_eval(inputs_dict)
            measured_values.append(measured)
            # print(registers)
            estimated_values.append(registers["a0"])  # rather than using estimated

        # Correlation
        # try:
        # print(estimated_values)
        if measured_values != estimated_values and estimated_values == [estimated_values[0]] * self.data_points:
            return 1, "inf", 0

        try:
            rvalues = stats.pearsonr(estimated_values, measured_values)
        except ValueError:
            return 1, "inf", 0

        align = np.polyfit(estimated_values, measured_values, 1)
        squared_error = 0
        for index in range(self.data_points):
            squared_error += ((measured_values[index] * align[0] + align[1]) - estimated_values[index]) ** 2
        post_mse = squared_error / self.data_points
        post_rmse = math.sqrt(squared_error / self.data_points)

        # squared_error = 0
        # for index in range(self.data_points):
        #     squared_error += (measured_values[index] - estimated_values[index]) ** 2
        # rmse = math.sqrt(squared_error / self.data_points)
        # except:
        #     return 1, 0, 0

        fitness = 1 - rvalues[0] ** 2

        return fitness, post_rmse, post_mse

    def postprocess(self, indv):
        return super().postprocess(indv)
