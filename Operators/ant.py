import sys

from Operators.AbstractOperator import AbstractOperator


class LEFT(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        sim = a[0]
        if sim.moves > 600:
            return "exit"
        sim.turn_left()
        return None

    @staticmethod
    def op_code():
        code = """
# returns sum of two given number arguments  
def left(sim):
\tif sim.moves > 600:
\t\treturn "exit"
\tsim.turn_left()
"""
        return code

    def demands(self):
        return [
            "object"
        ]

    def products(self):
        return [None]

    def name(self):
        return "LEFT"

    def annotation(self):
        return "left({})"
        # return "{} = SUM({}, {})"


class RIGHT(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        sim = a[0]
        if sim.moves > 600:
            return "exit"
        sim.turn_right()
        return None

    @staticmethod
    def op_code():
        code = """
# returns sum of two given number arguments  
def right(sim):
\tif sim.moves > 600:
\t\treturn "exit"
\tsim.turn_right()
"""
        return code

    def demands(self):
        return [
            "object"
        ]

    def products(self):
        return [None]

    def name(self):
        return "RIGHT"

    def annotation(self):
        return "right({})"
        # return "{} = SUM({}, {})"


class MOVE(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        sim = a[0]
        if sim.moves > 600:
            return "exit"
        sim.move_forward()
        return None

    @staticmethod
    def op_code():
        code = """
# returns sum of two given number arguments  
def move(sim):
\tif sim.moves > 600:
\t\treturn "exit"
\tsim.move_forward()
"""
        return code

    def demands(self):
        return [
            "object"
        ]

    def products(self):
        return [None]

    def name(self):
        return "LEFT"

    def annotation(self):
        return "move({})"
        # return "{} = SUM({}, {})"


class IF_SENSE(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        sim = a[0]
        if sim.moves > 600:
            return "exit"
        if sim.sense_food():
            return None
        return "skip"

    @staticmethod
    def op_code():
        code = """
# returns sum of two given number arguments  
def if(sim):
\tif sim.moves > 600:
\t\treturn "exit"
\tif sim.sense_food():
\t\treturn True
\treturn False
"""
        return code

    def demands(self):
        return [
            "object"
        ]

    def products(self):
        return ["structural"]

    def name(self):
        return "IF_SENSE"

    def annotation(self):
        return "if {}.sense_food():"
        # return "{} = SUM({}, {})"
