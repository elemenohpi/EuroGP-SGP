from abc import ABC, abstractmethod

class AbstractInterpreter(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def modelize(self, individual):
        pass

    