import copy
import math
from scipy import stats
import numpy as np
import warnings

warnings.filterwarnings('ignore')

from Fitness.AbstractFitness import AbstractFitness


class Dynaloop(AbstractFitness):

    def __init__(self) -> None:
        super().__init__()

    def preprocess(self, indv):
        return super().preprocess(indv)

    def evaluate(self, individual):
        # c = a^3 + 3 * a^2
        # c = a[index] ** 3 + 3 * a[index] ** 2

        total_error = 0
        # a = list(range(1, 100))
        # b = list(range(1, 100))
        a = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        b = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
        c = []
        # for i in range(10):
        # a.append(i + 1 + 3)
        # b.append(i * 2 + 1)
        # c.append(i * 1.5 + 0)

        predictions = []
        measured = []

        maxindex = 10

        for index in range(maxindex):
            # c = math.factorial(a[index])
            c = 2 ** b[index]
            measured.append(c)
            inputs = {"x": b[index]}
            try:
                c_prime, registers = individual.individual_eval(inputs)
            except TypeError:
                raise "ERROR: Operand name mismatch. Please check the given operand names in the fitness function."
            # total_error += abs(c - c_prime) ** 2
            predictions.append(c_prime)
            if math.isnan(c_prime) or math.isinf(c_prime):
                return 1, 0, float("inf")
            # print(a[index], c_prime)
            # print("=======================================")
        try:
            rvalue = stats.pearsonr(predictions, measured)
            allz = [0] * maxindex
            if predictions == allz:
                return 1, 0, float("inf")
            # print(predictions)
            align = np.polyfit(predictions, measured, 1)
        except:
            return 1, 0, float("inf")

        error_squared_sum = 0
        for index, prediction in enumerate(predictions):
            predictions[index] = prediction * align[0] + align[1]
            error_squared_sum += (predictions[index] - measured[index]) ** 2
        error_squared_sum /= maxindex
        rmse_aligned = math.sqrt(error_squared_sum)

        if math.isnan(rvalue[0]):
            return 1, 0, float("inf")

        return 1 - rvalue[0] ** 2, rvalue[0], rmse_aligned

    def postprocess(self, indv):
        return super().postprocess(indv)
