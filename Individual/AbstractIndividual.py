from abc import ABC, abstractmethod

class AbstractIndividual(ABC):
    def __init__(self) -> None:
        self.fitness = 0
        pass

    @abstractmethod
    def init_random(self, init_type):
        pass
    pass

    @abstractmethod
    def individual_eval(self, inputs):
        pass
    pass