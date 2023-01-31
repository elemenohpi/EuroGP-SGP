from Population.AbstractPopulation import AbstractPopulation
from eletility import Log



class BasePopulation(AbstractPopulation):

    def __init__(self, config, individual_class) -> None:
        super().__init__()
        self.pop = None
        self.individual_class = individual_class
        self.config = config
        self.L = Log(config["output_level"], self.__class__.__name__)

    def generate_population(self):
        super().generate_population()
        self.L.D("generate_population()")
        pop_size = int(self.config["popsize"])
        self.pop = []
        for i in range(pop_size):
            individual = self.individual_class(self.config)
            individual.init_random()
            individual.individual_index = i
            self.pop.append(individual)

