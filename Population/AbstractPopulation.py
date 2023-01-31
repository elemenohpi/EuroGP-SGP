from abc import ABC, abstractmethod 

class AbstractPopulation(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def generate_population(self):
        pass 