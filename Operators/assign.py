from Operators.AbstractOperator import AbstractOperator
import sys


class OP_ASSIGN(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        return a[0]

    def demands(self):
        return [
            "float"
        ]

    def products(self):
        return ["float"]

    def name(self):
        return "OP_ASSIGN"

    def annotation(self):
        return "{} = {}"

    def op_code(self):
        code = """"""
        return code
