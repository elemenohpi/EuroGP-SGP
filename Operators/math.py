import sys
import math

from Operators.AbstractOperator import AbstractOperator


class OP_SUM(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        if a[0] == float("inf"):
            a[0] = sys.float_info.max
        elif a[0] == float("-inf"):
            a[0] = -1 * sys.float_info.max
        if a[1] == float("inf"):
            a[1] = sys.float_info.max
        elif a[1] == float("-inf"):
            a[1] = -1 * sys.float_info.max

        ans = a[0] + a[1]
        if ans == float("inf") or ans == float("-inf"):
            ans = sys.float_info.max

        return ans

    @staticmethod
    def op_code():
        code = """
# returns sum of two given number arguments  
def op_sum(a, b):
\treturn a + b
"""
        return code

    def demands(self):
        return [
            "float",
            "float"
        ]

    def products(self):
        return ["float"]

    def name(self):
        return "OP_SUM"

    def annotation(self):
        return "{} = {} + {}"
        # return "{} = SUM({}, {})"


class OP_SUM3(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        if a[0] == float("inf"):
            a[0] = sys.float_info.max
        elif a[0] == float("-inf"):
            a[0] = -1 * sys.float_info.max
        if a[1] == float("inf"):
            a[1] = sys.float_info.max
        elif a[1] == float("-inf"):
            a[1] = -1 * sys.float_info.max
        if a[2] == float("inf"):
            a[2] = sys.float_info.max
        elif a[2] == float("-inf"):
            a[2] = -1 * sys.float_info.max

        ans = a[0] + a[1] + a[2]
        if ans == float("inf") or ans == float("-inf"):
            ans = sys.float_info.max
        return ans

    @staticmethod
    def op_code():
        code = """
# returns sum of three given number arguments  
def op_sum3(a, b, c):
\treturn a + b + c
"""
        return code

    def demands(self):
        return [
            "float",
            "float",
            "float"
        ]

    def products(self):
        return ["float"]

    def name(self):
        return "OP_SUM3"

    def annotation(self):
        return "{} = {} + {} + {}"
        # return "{} = SUM({}, {})"


#     Protected DIVISION
class OP_DIV(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        if a[0] == float("inf"):
            a[0] = sys.float_info.max
        elif a[0] == float("-inf"):
            a[0] = -1 * sys.float_info.max
        if a[1] == float("inf"):
            a[1] = sys.float_info.max
        elif a[1] == float("-inf"):
            a[1] = -1 * sys.float_info.max
        if a[1] == 0:
            return 1

        ans = a[0] / a[1]
        if ans == float("inf") or ans == float("-inf"):
            ans = sys.float_info.max
        return a[0] / a[1]

    def demands(self):
        return [
            "float",
            "float",
        ]

    @staticmethod
    def op_code():
        code = """
# returns division of two given number arguments (returns 1 if division by zero)
def op_div(a, b):
\tif b == 0:
\t\treturn 1
\treturn a / b
"""
        return code

    def products(self):
        return ["float"]

    def name(self):
        return "OP_DIV"

    def annotation(self):
        return "{} = op_div({}, {})"


class OP_MULT(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        if a[0] == float("inf"):
            a[0] = sys.float_info.max
        elif a[0] == float("-inf"):
            a[0] = -1 * sys.float_info.max
        if a[1] == float("inf"):
            a[1] = sys.float_info.max
        elif a[1] == float("-inf"):
            a[1] = -1 * sys.float_info.max

        ans = a[0] * a[1]
        if ans == float("inf") or ans == float("-inf"):
            ans = sys.float_info.max
        return ans

    def demands(self):
        return [
            "float",
            "float",
        ]

    def products(self):
        return ["float"]

    def name(self):
        return "OP_MULT"

    def annotation(self):
        return "{} = {} * {}"

    @staticmethod
    def op_code():
        code = """
# returns multiplication of two given number arguments  
def op_mult(a, b):
\treturn a * b
"""
        return code


class OP_MINUS(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        if a[0] == float("inf"):
            a[0] = sys.float_info.max
        elif a[0] == float("-inf"):
            a[0] = -1 * sys.float_info.max
        if a[1] == float("inf"):
            a[1] = sys.float_info.max
        elif a[1] == float("-inf"):
            a[1] = -1 * sys.float_info.max

        ans = a[0] - a[1]
        if ans == float("inf") or ans == float("-inf"):
            ans = sys.float_info.max
        return ans

    def demands(self):
        return [
            "float",
            "float",
        ]

    @staticmethod
    def op_code():
        code = """
# returns subtraction of two given number arguments  
def op_minus(a, b):
\treturn a - b
"""
        return code

    def products(self):
        return ["float"]

    def name(self):
        return "OP_MINUS"

    def annotation(self):
        return "{} = {} - {}"


class OP_EXP(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        if a[0] == float("inf"):
            a[0] = sys.float_info.max
        elif a[0] == float("-inf"):
            a[0] = -1 * sys.float_info.max
        try:
            ans = math.exp(a[0])
        except OverflowError:
            ans = sys.float_info.max

        if ans == float("inf") or ans == float("-inf"):
            ans = sys.float_info.max

        return ans

    def demands(self):
        return [
            "float",
        ]

    @staticmethod
    def op_code():
        code = """
# returns exp of the given number
def op_exp(a):
\treturn math.exp(a)
"""
        return code

    def products(self):
        return ["float"]

    def name(self):
        return "OP_EXP"

    def annotation(self):
        return "{} = math.exp({})"


class OP_SIN(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        if a[0] == float("inf"):
            a[0] = sys.float_info.max
        elif a[0] == float("-inf"):
            a[0] = -1 * sys.float_info.max

        ans = math.sin(a[0])
        if ans == float("inf") or ans == float("-inf"):
            ans = sys.float_info.max
        return ans

    def demands(self):
        return [
            "float",
        ]

    @staticmethod
    def op_code():
        code = """
# returns sin of the given number
def op_sin(a):
\treturn math.sin(a)
"""
        return code

    def products(self):
        return ["float"]

    def name(self):
        return "OP_SIN"

    def annotation(self):
        return "{} = math.sin({})"


class OP_COS(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        if a[0] == float("inf"):
            a[0] = sys.float_info.max
        elif a[0] == float("-inf"):
            a[0] = -1 * sys.float_info.max

        ans = math.cos(a[0])
        if ans == float("inf") or ans == float("-inf"):
            ans = sys.float_info.max
        return ans

    def demands(self):
        return [
            "float",
        ]

    @staticmethod
    def op_code():
        code = """
# returns cos of the given number
def op_cos(a):
\treturn math.cos(a)
"""
        return code

    def products(self):
        return ["float"]

    def name(self):
        return "OP_COS"

    def annotation(self):
        return "{} = math.cos({})"


class OP_TANH(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        if a[0] == float("inf"):
            a[0] = sys.float_info.max
        elif a[0] == float("-inf"):
            a[0] = -1 * sys.float_info.max

        ans = math.tanh(a[0])
        if ans == float("inf") or ans == float("-inf"):
            ans = sys.float_info.max
        return ans

    def demands(self):
        return [
            "float",
        ]

    @staticmethod
    def op_code():
        code = """
# returns tanh of the given number
def op_tanh(a):
\treturn math.tanh(a)
"""
        return code

    def products(self):
        return ["float"]

    def name(self):
        return "OP_TANH"

    def annotation(self):
        return "{} = math.tanh({})"


class OP_TAN(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        if a[0] == float("inf"):
            a[0] = sys.float_info.max
        elif a[0] == float("-inf"):
            a[0] = -1 * sys.float_info.max

        ans = math.tan(a[0])
        if ans == float("inf") or ans == float("-inf"):
            ans = sys.float_info.max
        return ans

    def demands(self):
        return [
            "float",
        ]

    @staticmethod
    def op_code():
        code = """
# returns tan of the given number
def op_tan(a):
\treturn math.tan(a)
"""
        return code

    def products(self):
        return ["float"]

    def name(self):
        return "OP_TAN"

    def annotation(self):
        return "{} = math.tan({})"
