import sys

import numpy as np

from Operators.AbstractOperator import AbstractOperator


def fix_matrix_float_infinite_value(a):
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = fix_float_infinite_value(a[i][j])


def fix_float_infinite_value(a):
    if a == float("inf"):
        return sys.float_info.max
    elif a == float("-inf"):
        return -1 * sys.float_info.max
    return a


class OP_MAT_ADDITION(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        fix_matrix_float_infinite_value(a[0])
        fix_matrix_float_infinite_value(a[1])
        f1 = np.array(a[0])
        f2 = np.array(a[1])
        if f2.shape != f1.shape:
            return np.ones(f1.shape).tolist()
        return np.add(f1, f2).tolist()

    def demands(self):
        return [
            "mat2d",
            "mat2d",
        ]

    @staticmethod
    def op_code():
        code = """
# returns addition of two given 2d matrix arguments
def op_mat_addition(a, b):
\treturn np.add(np.array(a), np.array(b)).tolist()
"""
        return code

    def products(self):
        return ["mat2d"]

    def name(self):
        return "OP_MAT_ADDITION"

    def annotation(self):
        return "{} = op_mat_addition({}, {})"


class OP_MAT_SUBTRACTION(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        fix_matrix_float_infinite_value(a[0])
        fix_matrix_float_infinite_value(a[1])
        f1 = np.array(a[0])
        f2 = np.array(a[1])
        if f2.shape != f1.shape:
            return np.ones(f1.shape).tolist()
        return np.subtract(f1, f2).tolist()

    def demands(self):
        return [
            "mat2d",
            "mat2d",
        ]

    @staticmethod
    def op_code():
        code = """
# returns subtraction of two given 2d matrix arguments
def op_mat_subtraction(a, b):
\treturn np.subtract(np.array(a), np.array(b)).tolist()
"""
        return code

    def products(self):
        return ["mat2d"]

    def name(self):
        return "OP_MAT_SUBTRACTION"

    def annotation(self):
        return "{} = op_mat_subtraction({}, {})"


class OP_MAT_TRANSPOSE(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        fix_matrix_float_infinite_value(a[0])
        return np.transpose(np.array(a[0])).tolist()

    def demands(self):
        return [
            "mat2d",
        ]

    @staticmethod
    def op_code():
        code = """
# returns transpose of a given 2d matrix argument
def op_mat_transpose(a):
\treturn np.transpose(np.array(a)).tolist()
"""
        return code

    def products(self):
        return ["mat2d"]

    def name(self):
        return "OP_MAT_TRANSPOSE"

    def annotation(self):
        return "{} = op_mat_transpose({})"


class OP_MAT_PRODUCT(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        fix_matrix_float_infinite_value(a[0])
        a[1] = fix_float_infinite_value(a[1])
        return (np.array(a[0]) * a[1]).tolist()

    def demands(self):
        return [
            "mat2d",
            "float",
        ]

    @staticmethod
    def op_code():
        code = """
# returns products of a given 2d matrix argument and a number
def op_mat_product(a, b):
\treturn (np.array(a) * b).tolist()
"""
        return code

    def products(self):
        return ["mat2d"]

    def name(self):
        return "OP_MAT_PRODUCT"

    def annotation(self):
        return "{} = op_mat_product({}, {})"


class OP_MAT_DOT_PRODUCT(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        fix_matrix_float_infinite_value(a[0])
        fix_matrix_float_infinite_value(a[1])
        f1 = np.array(a[0])
        f2 = np.array(a[1])
        if f1.shape[1] != f2.shape[0]:
            return np.ones(f1.shape).tolist()
        return np.dot(f1, f2).tolist()

    def demands(self):
        return [
            "mat2d",
            "mat2d",
        ]

    @staticmethod
    def op_code():
        code = """
# returns dot products of two given 2d matrix argument
def op_mat_dot_product(a, b):
\treturn np.dot(np.array(a), np.array(b)).tolist()
"""
        return code

    def products(self):
        return ["mat2d"]

    def name(self):
        return "OP_MAT_DOT_PRODUCT"

    def annotation(self):
        return "{} = op_mat_dot_product({}, {})"


class OP_MAT_DIV(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        fix_matrix_float_infinite_value(a[0])
        a[1] = fix_float_infinite_value(a[1])
        if a[1] == 0:
            return np.ones(np.array(a[0]).shape).tolist()
        return (np.array(a[0]) / a[1]).tolist()

    def demands(self):
        return [
            "mat2d",
            "float",
        ]

    @staticmethod
    def op_code():
        code = """
# returns division of a given 2d matrix argument and a number
def op_mat_div(a, b):
\tif b == 0:
\t\treturn np.ones(np.array(a).shape)
\treturn (np.array(a) / b).tolist()
"""
        return code

    def products(self):
        return ["mat2d"]

    def name(self):
        return "OP_MAT_DIV"

    def annotation(self):
        return "{} = op_mat_div({}, {})"


class OP_MAT_GET(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, a):
        fix_matrix_float_infinite_value(a[0])
        f = np.array(a[0])
        x = a[1]
        y = a[2]
        # if math.isnan(x) or math.isnan(y):
        #     return 0
        if x >= f.shape[0] or x < 0:
            return 0
        if y >= f.shape[1] or y < 0:
            return 0
        return f[int(x)][int(y)]

    def demands(self):
        return [
            "mat2d",
            "float",
            "float",
        ]

    @staticmethod
    def op_code():
        code = """
# returns an element of a given matrix with the given indices
def op_mat_get(a, b, c):
\tf = np.array(a)
\tif b >= f.shape[0] or b < 0:
\t\treturn 0
\tif c >= f.shape[1] or c < 0:
\t\treturn 0
\treturn f[int(b)][int(c)]
"""
        return code

    def products(self):
        return ["float"]

    def name(self):
        return "OP_MAT_GET"

    def annotation(self):
        return "{} = op_mat_get({}, {}, {})"
