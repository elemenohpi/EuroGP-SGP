from Operators.AbstractOperator import AbstractOperator
import sys


class OP_IF(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        op1 = a[0]
        conditional = a[1]
        op2 = a[2]

        if op1 == float("inf"):
            op1 = sys.float_info.max
        if op2 == float("inf"):
            op2 = sys.float_info.max
        if op1 == float("-inf"):
            op1 = sys.float_info.max * -1
        if op2 == float("-inf"):
            op2 = sys.float_info.max * -1

        statement = "{} {} {}".format(op1, conditional, op2)

        try:
            ans = eval(statement)
        except NameError:
            print(op1)
            print(conditional)
            print(op2)
            print(statement)
            raise statement + "is invalid"

        if not ans:
            return "skip"
        else:
            return None

    def demands(self):
        return [
            "float",
            "conditional",
            "float",
        ]

    def products(self):
        return ["structural"]

    def name(self):
        return "OP_IF"

    def annotation(self):
        return "if {} {} {}:"

    def op_code(self):
        code = """
# returns true if a condition is met and false otherwise 
def op_if(a, condition, b):
\tif eval('{} {} {}'.format(a, condition, b)):
\t\treturn True
\treturn False
"""
        return code
