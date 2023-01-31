import math
import random

from scipy import stats
import numpy as np
import warnings

warnings.filterwarnings('ignore')

from Fitness.AbstractFitness import AbstractFitness


class MultiRegression(AbstractFitness):

    def __init__(self) -> None:
        super().__init__()
        self.max_index = 10
        self.in1 = [random.randint(0, 10) for _ in range(1, self.max_index + 1)]
        self.in2 = [random.randint(0, 10) for _ in range(1, self.max_index + 1)]

    def preprocess(self, indv):
        return super().preprocess(indv)

    def evaluate(self, individual):
        predictions_e1 = []
        predictions_e2 = []
        predictions_e3 = []
        measured_e1 = []
        measured_e2 = []
        measured_e3 = []

        for index in range(self.max_index):
            for i in range(3):
                i = i * 10
                if i == 0:
                    ans = self.in1[index] + self.in2[index]
                    measured_e1.append(ans)
                elif i == 10:
                    ans = self.in1[index] - self.in2[index]
                    measured_e2.append(ans)
                elif i >= 20:
                    ans = self.in1[index] * self.in2[index]
                    measured_e3.append(ans)
                else:
                    raise "unreachable statement reached"

            for i in range(3):
                i = i * 10
                inputs = {"mode": i, "x": self.in1[index], "y": self.in2[index]}
                p_ans, registers = individual.individual_eval(inputs)
                ans = registers["a3"]
                if i == 0:
                    predictions_e1.append(ans)
                elif i == 10:
                    predictions_e2.append(ans)
                elif i >= 20:
                    predictions_e3.append(ans)
                else:
                    raise "unreachable statement reached"

        type = "error"
        if type == "correl":
            all_zero = [0] * self.max_index
            if predictions_e1 == all_zero:
                e1_fitness = 1
            else:
                rvalue = stats.pearsonr(predictions_e1, measured_e1)
                if math.isnan(rvalue[0]):
                    r = 0
                else:
                    r = rvalue[0]
                e1_fitness = 1 - r ** 2

            if predictions_e2 == all_zero:
                e2_fitness = 1
            else:
                rvalue = stats.pearsonr(predictions_e2, measured_e2)
                if math.isnan(rvalue[0]):
                    r = 0
                else:
                    r = rvalue[0]
                e2_fitness = 1 - r ** 2

            if predictions_e3 == all_zero:
                e3_fitness = 1
            else:
                rvalue = stats.pearsonr(predictions_e3, measured_e3)
                if math.isnan(rvalue[0]):
                    r = 0
                else:
                    r = rvalue[0]
                e3_fitness = 1 - r ** 2
            fitness = max(e1_fitness, e2_fitness, e3_fitness)
            logstr = repr(e1_fitness) + "---" + str(e2_fitness) + "---" + str(e3_fitness)
            return fitness, logstr, "n/a"
        else:
            mse_e1 = 0
            for index, value in enumerate(measured_e1):
                mse_e1 += ((value - predictions_e1[index])**2) / len(measured_e1)
            rmse_e1 = math.sqrt(mse_e1)
            mse_e2 = 0
            for index, value in enumerate(measured_e2):
                mse_e2 += ((value - predictions_e2[index]) ** 2) / len(measured_e2)
            rmse_e2 = math.sqrt(mse_e2)
            mse_e3 = 0
            for index, value in enumerate(measured_e3):
                mse_e3 += ((value - predictions_e3[index]) ** 2) / len(measured_e3)
            rmse_e3 = math.sqrt(mse_e3)

            # fitness = max(rmse_e1, rmse_e2, rmse_e3)
            fitness = (rmse_e1 + rmse_e2 + rmse_e3) / 3
            logstr = repr(rmse_e1) + "---" + str(rmse_e2) + "---" + str(rmse_e3)
            return fitness, logstr, "n/a"
        # # y = a x + b
        # align = np.polyfit(predictions, measured, 1)
        # align[0] = round(align[0], 10)
        # align[1] = round(align[1], 10)

        # error_squared_sum = 0
        # for index, prediction in enumerate(predictions):
        #     predictions[index] = prediction * align[0] + align[1]
        #     error_squared_sum += (predictions[index] - measured[index]) ** 2
        # error_squared_sum /= self.max_index
        # rmse_aligned = math.sqrt(error_squared_sum)
        #
        # if math.isnan(rvalue[0]):
        #     return 1, 0, float("inf")

        # fitness = max(e1_fitness, e2_fitness, e3_fitness)


    def postprocess(self, indv):
        return super().postprocess(indv)
