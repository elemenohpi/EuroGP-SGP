from abc import ABC, abstractmethod

class AbstractFitness(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def preprocess(self, indv):
        pass
    
    @abstractmethod
    def evaluate(self, indv):
        return -1

    @abstractmethod
    def postprocess(self, indv):
        pass