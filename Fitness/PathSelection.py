import math
import random

from scipy import stats
import numpy as np
import warnings

warnings.filterwarnings('ignore')

from Fitness.AbstractFitness import AbstractFitness


class PathSelection(AbstractFitness):

    def __init__(self) -> None:
        super().__init__()
        self.max_index = 10
        self.in1 = [random.randint(0, 10) for _ in range(1, self.max_index + 1)]
        self.in2 = [random.randint(0, 10) for _ in range(1, self.max_index + 1)]

    def preprocess(self, indv):
        return super().preprocess(indv)

    def evaluate(self, individual):
        measured = [7, 1, 9]
        predictions = []
        for i in range(3):
            mode = i
            inputs = {"mode": mode}
            output, registers = individual.individual_eval(inputs)
            if i == 0:
                predictions.append(output)
            elif i == 1:
                predictions.append(output)
            elif i == 2:
                predictions.append(output)
            else:
                raise "unreachable statement reached"

        metric = "error"

        if "correl" == metric:
            all_zero = [0] * 3
            if predictions == all_zero:
                r = 0
            else:
                rvalue = stats.pearsonr(predictions, measured)
                if math.isnan(rvalue[0]):
                    r = 0
                else:
                    r = rvalue[0]
            fitness = 1 - r ** 2
        else:
            mse = 0
            for index, val in enumerate(predictions):
                mse += (val - measured[index])**2 / len(predictions)
            rmse = math.sqrt(mse)
            fitness = rmse

        return fitness, "n/a", "n/a"

    def postprocess(self, indv):
        return super().postprocess(indv)
