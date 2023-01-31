# from Individual.BaseIndividual import Base
# ToDo:: dynamically import
import math

from compatibility import compatibility_dict

from Interpreter.AbstractInterpreter import AbstractInterpreter
from eletility import Log
import copy


class BaseType:
    INPUT = 0
    OUTPUT = 1
    CONSTANT = 2
    OPERATOR = 3
    STRUCTURAL = 4


class Base:
    pass


class BaseInterpreter(AbstractInterpreter):

    def __init__(self, config) -> None:
        super().__init__()
        self.config = config
        self.L = Log(config["output_level"], self.__class__.__name__)
        self.currRing = 0
        self.currQ = 0
        self.operators = {}
        self.inputs = {}
        self.output_counter = 0
        self.output_history = []
        self.program = ""
        self.demand_queue = []
        self.operator_queue = []
        self.input_queue = []

    def reset_system(self):
        self.currRing = 0
        self.currQ = 0
        self.operators = {}
        self.inputs = {}
        self.output_history = []
        self.output_counter = 0
        self.program = ""
        self.demand_queue = []
        self.operator_queue = []
        self.input_queue = []

    def form_structures(self, indv):
        self.L.D("form_structures()")
        individual = copy.deepcopy(indv)
        self.operators = individual.operators
        self.inputs = individual.inputs
        # opRings = sorted(self.operators.keys())
        # inRings = sorted(self.inputs.keys()) 

    def get_op_rings(self):
        self.L.D("get_op_rings()")
        current_ring = []
        next_ring = []
        top_ring = []
        try:
            current_ring = self.operators[self.currRing][self.currQ]
        except KeyError:
            pass
        try:
            next_ring = self.operators[self.currRing][self.currQ + 1]
        except KeyError:
            pass
        try:
            top_ring = self.operators[self.currRing + 1][self.currQ]
        except KeyError:
            pass
        return current_ring + next_ring + top_ring

    def get_in_rings(self):
        self.L.D("get_in_rings()")
        current_ring = []
        next_ring = []
        top_ring = []
        try:
            current_ring = self.inputs[self.currRing][self.currQ]
        except KeyError:
            pass
        try:
            next_ring = self.inputs[self.currRing][self.currQ + 1]
        except KeyError:
            pass
        try:
            top_ring = self.inputs[self.currRing + 1][self.currQ]
        except KeyError:
            pass
        return current_ring + next_ring + top_ring

    def remove_base(self, base):
        self.L.D("remove_base()")
        base_type = base.type
        if base_type == BaseType.OPERATOR:
            quarter = self.pos2q(base.pos)
            # print("----")
            # print(self.operators[base.ring][quarter])
            # print(base)
            self.operators[base.ring][quarter].remove(base)
            pass
        elif base_type == BaseType.INPUT:
            pass

    # Returns a base that matches the type. 
    def grab_base(self, base_type, demand) -> int:
        # print("demand: ", demand)
        self.L.D("grab_base()")
        # Grabbing Operators ####################################################################
        if base_type == BaseType.OPERATOR:
            eligible_zones = self.get_op_rings()
            for base in eligible_zones:
                if base.explored:
                    continue
                if demand is None:
                    base.explored = True
                    return base
                else:
                    print(demand)
                    self.L.E("demand is not none. looking for a specific operator")
                    base.explored = True
                    return base

        # Grabbing Inputs ####################################################################
        elif base_type == BaseType.INPUT:
            eligible_zones = self.get_in_rings()
            for base in eligible_zones:
                if base.explored:
                    continue
                if demand == [] or demand is None:
                    base.explored = True
                    return base
                else:
                    # productz = base.products[0]
                    # if type(productz) == list:
                    #     productz = productz[0]
                    # print("demand {} base product {} base value {}".format(demand, base.products[0],
                    # base.value))
                    if self.is_compatible(demand, base.products[0]):
                        # print("caught ", base.value)
                        base.explored = True
                        return base
            pass
        elif base_type == BaseType.STRUCTURAL:
            pass
        elif base_type == BaseType.CONSTANT:
            pass
        elif base_type == BaseType.OUTPUT:
            pass

        return None

    def is_compatible(self, demand, product):
        self.L.D("is_compatible()")
        if isinstance(product, list):
            product = product[0]  # code might turn destructive ToDo::
        if product in compatibility_dict[demand]:
            return True
        else:
            return False

    def pos2q(self, pos):
        self.L.D("pos2q()")
        return math.floor(pos / 90)

    def show_queue(self):
        self.L.D("show_queue()")
        print("=============Showing Queue")
        print("ring: ", self.currRing, " q: ", self.currQ)
        print("=====inputs:")
        for inp in self.input_queue:
            if inp.type == BaseType.CONSTANT:
                print(inp.value)
            else:
                print(inp.name)
        print("=====operators:")
        for op in self.operator_queue:
            print(op.operator)
        print("=====demands:")
        for demand in self.demand_queue:
            print(demand)
        print("=============\n")
        pass

    def add_program(self, op, inputs):
        self.L.D("add_program()")

        annotation = op.annotation()

        code = "\"" + annotation + "\".format("
        out_name = "out_" + repr(self.output_counter)
        code += "\"out_" + repr(self.output_counter) + "\", "
        self.output_counter += 1
        for input in inputs:
            if input.name != "":
                code += "\"" + input.name + "\", "
            else:
                code += "\"" + str(input.value) + "\", "

        code = code[:len(code) - 2] + ")"

        self.program += eval(code) + "\n"

        # add output to the system
        base = Base()
        base.type = BaseType.INPUT
        base.pos = self.currQ * 90
        base.value = None
        base.name = out_name
        base.products.append(op.products())
        base.ring = self.currRing
        try:
            self.inputs[self.currRing][self.currQ].insert(0, base)
        except KeyError:
            # print("inputs : {} , currR: {} , currQ: {}".format(self.inputs, self.currRing, self.currQ))
            self.inputs[self.currRing] = {
                0: [],
                1: [],
                2: [],
                3: []
            }
        self.inputs[self.currRing][self.currQ].insert(0, base)
        self.output_history.append(base)

    def extract_statement(self):
        self.L.D("extract_statement()")
        if len(self.operator_queue) > 1:
            base = self.operator_queue[0]
            if len(base.demands) > len(self.input_queue):
                return
            counter = 0
            # if base.value is not None and base.value != "":
            #     print("demands '{}'".format(base.demands))
            #     #     print(current_demand)
            #     exit()

            for index, demand in enumerate(base.demands):
                # if self.input_queue[index].value != "":
                #     print("demand {} queue: {}".format(demand, self.input_queue[index].products[0]))
                #     if self.is_compatible(demand, self.input_queue[index].products[0]):
                #         print("would be")
                #     exit()
                if self.is_compatible(demand, self.input_queue[index].products[0]):
                    counter += 1

            if counter == len(base.demands):
                op = base.operator
                inputs = self.input_queue[:len(base.demands)]
                self.add_program(op, inputs)
                # reset demands
                self.demand_queue = self.demand_queue[len(base.demands) - 1:]
                # remove op base
                self.remove_base(self.operator_queue.pop())
                # remove inp base
                for _ in base.demands:
                    self.remove_base(self.input_queue.pop())

    def modelize(self, individual):
        self.L.D("modelize()")
        self.reset_system()
        self.form_structures(individual)
        individual.outputs = None
        # individual.print_system()
        # self.L.Yprint("===========================================================================\n")

        base_type = BaseType.OPERATOR
        current_demand = None

        self.demand_queue = []
        self.operator_queue = []
        self.input_queue = []

        # individual.print_system()
        # exit()
        while True:
            # print("current demand: ", current_demand, " base_type: ", base_type)
            # self.show_queue()

            base = self.grab_base(base_type, current_demand)

            # if base:
            #     if base.type == BaseType.OPERATOR:
            #         self.L.Yprint(base.operator)
            #     elif base.type == BaseType.INPUT:
            #         self.L.Yprint(base.name)
            #     elif base.type == BaseType.CONSTANT:
            #         self.L.Yprint(base.value)

            # if base:
            #     if base.operator is not None:
            #         print(base.operator)
            #     elif base.name:
            #         print(base.name)
            #     else:
            #         print(base.value)

            # if not base and self.demand_queue is []:
            #     self.L.E("no base found. we have to find the reason and then implement accordingly")

            if base:
                if base.demands or base.demands != []:
                    self.demand_queue += base.demands
                # else:
                #     # self.demands.pop()  # might need an extra check here ToDo::
                #     pass

                if base.type == BaseType.INPUT or base.type == BaseType.CONSTANT:
                    self.input_queue.append(base)
                elif base.type == BaseType.OPERATOR:
                    self.operator_queue.append(base)

                self.extract_statement()

                if len(self.demand_queue) > 0:
                    current_demand = self.demand_queue.pop(0)
                    base_type = BaseType.INPUT
                else:
                    current_demand = None
                    base_type = BaseType.OPERATOR

                self.currQ = self.pos2q(base.pos)
                self.currRing = base.ring

            if not base:
                if len(self.operator_queue) == 0:
                    # Assumed demands will not be other than None when we don't have an operator
                    # Program found!
                    output_code_segment = ""
                    if len(individual.outputsPool) > len(self.output_history):
                        individual.program = ""
                        return
                    self.output_history = reversed(self.output_history)
                    safety_counter = 0

                    for key in individual.outputsPool:
                        for out_n in self.output_history:

                            model_product = out_n.products[0]
                            output_product = eval(individual.outputsPool[key])
                            if self.is_compatible(output_product, model_product):
                                output_code_segment += out_n.name + ", "
                                safety_counter += 1
                                break
                    output_code_segment = output_code_segment[:len(
                        output_code_segment) - 2]

                    if safety_counter != len(individual.outputsPool):
                        individual.program = ""
                        return

                    # for input in individual.inputsPool:

                    individual.outputs = output_code_segment
                    individual.program = self.program

                    # print(individual.program)
                    self.reset_system()
                    return
                else:
                    # useless operator
                    # self.L.Bprint("Reverting")
                    base = self.operator_queue.pop()
                    self.currQ = self.pos2q(base.pos)
                    self.currRing = base.ring
                    self.remove_base(base)
                    for inp in self.input_queue:
                        inp.explored = False
                    self.input_queue = []
                    self.demand_queue = []

    def interpret(self):
        pass
