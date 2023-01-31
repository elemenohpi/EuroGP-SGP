from Operators.AbstractOperator import AbstractOperator
from const import MAP
import math

class Pos(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, matrix, a):
        x = int(a[0])
        y = int(a[1])

        return (x, y)

    def demands(self):
        return [
            "number:any",
            "number:any"
        ]
    
    def products(self):
        return "pos:any"
    
    def name(self):
        return self.__class__.__name__

    def annotation(self): 
        return "{} = " + self.name() + "({}, {})"

class PlaceObjAtPos(AbstractOperator): 
    def __init__(self):
        super().__init__()
        pass

    def eval(self, problemMatrix, a):
        matrix = a[0]
        x, y = int(a[1] + 2), int(a[2] + 2)
        obj = a[3]
        lenX = len(matrix)
        lenY = len(matrix[0])
        if x < lenX - 2 and x >= 2 and y < lenY - 2 and y >= 2:  
            if not matrix[x][y] in [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]:
                matrix[x][y] = obj
        return matrix

    def demands(self):
        return [
            "matrix:any",
            "number:any",
            "number:any",
            "obj:any",
        ]
    
    def products(self):
        return "matrix:any"
    
    def name(self):
        return self.__class__.__name__

    def annotation(self): 
        return "{} = " + self.name() + "({}, {}, {})"

class Connect(AbstractOperator):
    def __init__(self):
        super().__init__()
        pass

    def eval(self, matrix , a):
        matrix = a[0]
        x1 = a[1]
        y1 = a[2]
        x2 = a[3]
        y2 = a[4]

        Place = PlaceObjAtPos()

        x1, y1 = y1, x1
        x2, y2 = y2, x2

        while x1 != x2:
            last = 0
            if x1 > x2:
                # belt should go north and it goes north
                matrix = Place.eval(matrix, [matrix, x1, y1, 1])
                x1 -= 1
                last = 1
            elif x2 > x1:
                matrix = Place.eval(matrix, [matrix, x1, y1, 3])
                x1 += 1
                last = 3
            if x1 == x2:
                matrix = Place.eval(matrix, [matrix, x1, y1, last])

        while y1 != y2:
            last = 0
            if y1 > y2:
                # belt should go left and goes left
                matrix = Place.eval(matrix, [matrix, x1, y1, 4])
                y1 -= 1
                last = 4
            elif y2 > y1:
                # belt should go right and goes right
                matrix = Place.eval(matrix, [matrix, x1, y1, 2])
                y1 += 1
                last = 2
            if y1 == y2:
                matrix = Place.eval(matrix, [matrix, x1, y1, last])

        return matrix


    def demands(self):
        return [
            "matrix:any",
            "number:any",
            "number:any",
            "number:any",
            "number:any",
        ]
    
    def products(self):
        return "matrix:any"
    
    def name(self):
        return self.__class__.__name__

    def annotation(self): 
        return "{} = " + self.name() + "({}, {}, {}, {}, {})"

# class North(AbstractOperator):
#     def __init__(self):
#         super().__init__()
#         pass

#     def eval(self, matrix, a):
#         x, y = int(a[0][0]), int(a[0][1])

#         if y - 1 < 0:
#             y = 1

#         return (x, y-1)

#     def demands(self):
#         return [
#             "pos:any",
#         ]
    
#     def products(self):
#         return "pos:any"
    
#     def name(self):
#         return self.__class__.__name__

#     def annotation(self): 
#         return "{} = " + self.name() + "({})"

# class South(AbstractOperator):
#     def __init__(self):
#         super().__init__()
#         pass

#     def eval(self, matrix, a):
#         ylen = len(matrix[0])
#         x, y = int(a[0][0]), int(a[0][1])

#         if y + 1 > ylen - 2:
#             y = ylen - 3

#         return (x, y + 1)

#     def demands(self):
#         return [
#             "pos:any",
#         ]
    
#     def products(self):
#         return "pos:any"
    
#     def name(self):
#         return self.__class__.__name__

#     def annotation(self): 
#         return "{} = " + self.name() + "({})"

# class West(AbstractOperator):
#     def __init__(self):
#         super().__init__()
#         pass

#     def eval(self, matrix, a):
#         x, y = int(a[0][0]), int(a[0][1])

#         if x-1 < 0:
#             x = 1

#         return (x-1, y)

#     def demands(self):
#         return [
#             "pos:any",
#         ]
    
#     def products(self):
#         return "pos:any"
    
#     def name(self):
#         return self.__class__.__name__

#     def annotation(self): 
#         return "{} = " + self.name() + "({})"

# class East(AbstractOperator):
#     def __init__(self):
#         super().__init__()
#         pass

#     def eval(self, matrix, a):
#         lenx = len(matrix)
#         x, y = int(a[0][0]), int(a[0][1])

#         if x + 1 > lenx - 2:
#             x = lenx - 3

#         return (x+1, y)

#     def demands(self):
#         return [
#             "pos:any",
#         ]
    
#     def products(self):
#         return "pos:any"
    
#     def name(self):
#         return self.__class__.__name__

#     def annotation(self): 
#         return "{} = " + self.name() + "({})"


# class GetObjAtPos(AbstractOperator):
#     def __init__(self):
#         super().__init__()
#         pass

#     def eval(self, a):
#         # a[0] = problem matrix
#         matrix = a[0]
#         x, y = int(a[1][0]), int(a[1][1])
#         lenX = len(matrix)
#         lenY = len(matrix[0])
#         if x < lenX and x >= 0 and y < lenY and y >= 0:  
#             return matrix[x][y]
#         else:
#             return -1

#     def demands(self):
#         return [
#             "matrix:any",
#             "pos:any",
#         ]
    
#     def products(self):
#         return "obj:any"
    
#     def name(self):
#         return self.__class__.__name__

#     def annotation(self): 
#         return "{} = " + self.name() + "({}, {})"


# class GetClosestInput(AbstractOperator):
#     def __init__(self):
#         super().__init__()
#         pass

#     # -2 : "inputinserter_north"
# 	# -3 : "inputinserter_east"
# 	# -4 : "inputinserter_south"
# 	# -5 : "inputinserter_west"
# 	# -7 : "inputinserter_north"
# 	# -8 : "inputinserter_east"
# 	# -9 : "inputinserter_south"
# 	# -10 : "inputinserter_west"

#     def eval(self, a):
#         # a[0] = problem matrix
#         matrix = a[0]
#         pos = a[1]

#         gObj = GetObjAtPos()

#         candidates = []

#         for x, row in enumerate(matrix):
#             for y, col in enumerate(row):
#                 if  (col in [-3, -8]  and gObj.eval([matrix, (x, y+1)]) == -6) or \
#                     (col in [-5, -10] and gObj.eval([matrix, (x, y-1)]) == -6) or \
#                     (col in [-2, -7]  and gObj.eval([matrix, (x-1, y)]) == -6) or \
#                     (col in [-4, -9]  and gObj.eval([matrix, (x+1, y)]) == -6) :
#                     # Append the candidate
#                     candidates.append((x, y))
#         # print("candidates", candidates)
        
#         if len(candidates) > 0:
#             return min(candidates,key=lambda point: math.sqrt( abs(math.pow(point[0]-pos[0], 2) - math.pow(point[1]-pos[1], 2)))  )
#         else:
#             raise "No Output"

#     def demands(self):
#         return [
#             "matrix:any",
#             "pos:any",
#         ]
    
#     def products(self):
#         return "pos:any"
    
#     def name(self):
#         return self.__class__.__name__

#     def annotation(self): 
#         return "{} = " + self.name() + "({})"

# class GetClosestOutput(AbstractOperator):
#     def __init__(self):
#         super().__init__()
#         pass

#     # -2 : "inputinserter_north"
# 	# -3 : "inputinserter_east"
# 	# -4 : "inputinserter_south"
# 	# -5 : "inputinserter_west"
# 	# -7 : "inputinserter_north"
# 	# -8 : "inputinserter_east"
# 	# -9 : "inputinserter_south"
# 	# -10 : "inputinserter_west"

#     def eval(self, a):
#         # a[0] = problem matrix
#         matrix = a[0]
#         pos = a[1]

#         gObj = GetObjAtPos()

#         candidates = []

#         for x, row in enumerate(matrix):
#             for y, col in enumerate(row):
#                 if  (col in [-5, -10] and gObj.eval([matrix, (x, y+1)]) == -6) or \
#                     (col in [-3, -8]  and gObj.eval([matrix, (x, y-1)]) == -6) or \
#                     (col in [-4, -9]  and gObj.eval([matrix, (x-1, y)]) == -6) or \
#                     (col in [-2, -7]  and gObj.eval([matrix, (x+1, y)]) == -6) :
#                     # Append the candidate
#                     candidates.append((x, y))
#         # print("candidates", candidates)
#         if len(candidates) > 0:
#             return min(candidates,key=lambda point: math.sqrt( abs(math.pow(point[0]-pos[0], 2) - math.pow(point[1]-pos[1], 2)))  )
#         else:
#             raise "No Output"

#     def demands(self):
#         return [
#             "matrix:any",
#             "pos:any",
#         ]
    
#     def products(self):
#         return "pos:any"
    
#     def name(self):
#         return self.__class__.__name__

#     def annotation(self): 
#         return "{} = " + self.name() + "({})"


# obj = GetClosestOutput()
# matrix = [[-6, -3, 0, 0, -3, -6],\
#           [0, 0, 0, 0, 0, 0],\
#           [-6, -3, 0, 0, -3, -6],\
#           [0, 0, 0, 0, 0, 0],]

# pos1 = (3, 3)

# obj.eval([matrix, pos1])
# print("obj.eval([matrix, pos1])", obj.eval([matrix, pos1]))

