import random

from eletility import Files
from eletility import Log
from eletility import Times


class SGP:
    def __init__(self, config):
        self.evolver = None
        self.evolver_class = None
        self.fitness_class = None
        self.interpreter_class = None
        self.population_class = None
        self.individual_class = None

        # configuring the program
        self.config = config

        # configure the random seed
        seed = int(config["seed"])
        random.seed(seed)

        # handlers
        self.Files = Files()
        self.Times = Times()
        self.Log = Log(config["output_level"], self.__class__.__name__)

        # initialize the system
        self.init_system(config)

    def init_system(self, config):
        self.Log.D("init_system()")
        # config
        individual = config["individual"]
        population = config["population"]
        interpreter = config["interpreter"]
        fitness = config["fitness"]
        evolver = config["evolver"]

        # Individual
        module = __import__("Individual." + individual)
        self.individual_class = getattr(getattr(module, individual), individual)
        # Population
        module = __import__("Population." + population)
        self.population_class = getattr(getattr(module, population), population)
        # interpreter_obj
        module = __import__("Interpreter." + interpreter)
        self.interpreter_class = getattr(getattr(module, interpreter), interpreter)
        # Fitness

        module = __import__("Fitness." + fitness)
        tokens = fitness.split(".")
        if len(tokens) > 1:
            my_class = tokens[1]
            directory = tokens[0]
            temp_module = getattr(getattr(module, directory), my_class)
            self.fitness_class = getattr(temp_module, my_class)
        else:
            self.fitness_class = getattr(getattr(module, fitness), fitness)

        module = __import__("Evolver." + evolver)
        self.evolver_class = getattr(getattr(module, evolver), evolver)

    # runs the gp until a given condition is met (usually total number of runs is reached)
    def run(self):
        self.Log.D("run()")
        start_time = self.Times.now()

        pop_obj = self.population_class(self.config, self.individual_class)
        fitness_obj = self.fitness_class()
        interpreter_obj = self.interpreter_class(self.config)
        evolver_obj = self.evolver_class(self.config, pop_obj, fitness_obj, interpreter_obj)

        pop_obj.generate_population()
        best_fitness = evolver_obj.run()
        self.evolver = evolver_obj

        end_time = self.Times.now()

        self.Log.Bprint("TotalRuntime:\t\t" + str(self.Times.substract(end_time, start_time)))
        return best_fitness
