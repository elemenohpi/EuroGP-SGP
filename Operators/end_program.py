from Operators.AbstractOperator import AbstractOperator
import sys


class OP_END(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        return "end"

    def demands(self):
        return [
        ]

    def products(self):
        return ["command"]

    def name(self):
        return "OP_RETURN"

    def annotation(self):
        return "return 'end'"

    def op_code(self):
        code = """"""
        return code
