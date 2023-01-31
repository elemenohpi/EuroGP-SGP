from abc import ABC, abstractmethod


class AbstractOperator(ABC):
    def __init__(self):
        self.ID = 0
        self.operands = []
        self.outputs = []
        pass

    @abstractmethod
    def eval(self, a):
        pass

    @abstractmethod
    def demands(self):
        # For weird demands, hasCondition function of the interpreter should get modified
        pass

    @abstractmethod
    def products(self):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def annotation(self):
        pass

    def annotate(self):
        annotated = self.annotation()
        format_string = annotated
        format_string = "'" + format_string + "'.format("
        for output in self.outputs:
            format_string += "'"+output+"',"
        for operand in self.operands:
            format_string += "'"+operand+"',"
        format_string = format_string[:len(format_string)-1]
        format_string += ")"
        if len(self.operands) == len(self.outputs) == 0:
            return annotated
        return eval(format_string)
