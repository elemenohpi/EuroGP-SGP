import copy
import importlib
import json
import math
import random
import sys
import time
import matplotlib.pyplot as plt

from Individual.AbstractIndividual import AbstractIndividual
from eletility import Log

# Extra important shared global variables
SHARED_memory = {}


def distance_to_pos(source_pos, pos):
    return math.sqrt((pos[0] - source_pos[0]) ** 2 + (pos[1] - source_pos[1]) ** 2)


# Return condition
class Retcon:

    def __init__(self, condition_count, condition_depth, selection_pool):
        if condition_depth < 1:
            raise "Condition depth should be at least 1 or else should be disabled"
        self.conditionals = [">", "<", "==", "True", "False", "<=", ">="]
        self.connectors = ["and", "or"]
        self.statements = []
        self.condition_count = condition_count
        self.condition_depth = condition_depth
        self.selection_pool = selection_pool
        selection_pool = []
        for key in self.selection_pool:
            selection_pool += self.selection_pool[key]
        self.selection_pool = selection_pool

    def generate(self):

        for i in range(self.condition_depth):
            for j in range(self.condition_count):
                operator = random.choice(self.conditionals)
                if operator == "True" or operator == "False":
                    self.statements.append(operator)
                    if j == self.condition_count - 1:
                        ret_val = random.choice(self.selection_pool)
                        self.statements.append(ret_val)
                else:
                    operand1 = random.choice(self.selection_pool)
                    operand2 = random.choice(self.selection_pool)
                    self.statements += [operand1, operator, operand2]
                    if j == self.condition_count - 1:
                        ret_val = random.choice(self.selection_pool)
                        self.statements.append(ret_val)
                if self.condition_count > 1 and j != self.condition_count - 1:
                    connector = random.choice(self.connectors)
                    self.statements.append(connector)

            if i == self.condition_depth - 1:
                self.statements.append(random.choice(self.selection_pool))
        # print(self.statements)
        # exit()

    def eval(self, shared_memory):
        statement_counter = 0
        condition_string = ""

        for i in range(self.condition_depth):
            condition_string = ""
            j = 0
            while j < self.condition_count:
                candidate = self.statements[statement_counter]
                if candidate in self.selection_pool:
                    op1 = candidate
                    conditional = self.statements[statement_counter+1]
                    op2 = self.statements[statement_counter+2]
                    if op1 in shared_memory.keys():
                        op1 = shared_memory[op1]
                        if op1 == "inf" or op1 == float("inf"):
                            op1 = sys.float_info.max
                        elif op1 == "-inf" or op1 == float("-inf"):
                            op1 = sys.float_info.max * -1
                    if op2 in shared_memory.keys():
                        op2 = shared_memory[op2]
                        if op2 == "inf" or op2 == float("inf"):
                            op2 = sys.float_info.max
                        elif op2 == "-inf" or op2 == float("-inf"):
                            op2 = sys.float_info.max * -1
                    condition_string += " {} {} {}".format(op1, conditional, op2)
                    statement_counter += 3
                elif candidate in self.connectors:
                    condition_string += " " + candidate
                    statement_counter += 1
                    j -= 1
                elif candidate in self.conditionals and (candidate == "True" or candidate == "False"):
                    condition_string += " " + candidate
                    statement_counter += 1
                else:
                    print("unknown candidate: ", candidate)
                    exit()
                j += 1
            # print(shared_memory)
            # print("checking: ", condition_string)
            try:
                if eval(condition_string):
                    ret_val = self.statements[statement_counter]
                    if ret_val in shared_memory.keys():
                        ret_val = shared_memory[ret_val]
                    # print("condition successful, returning: ", ret_val)
                    # exit()
                    return float(ret_val)
                else:
                    # print("condition failed")
                    statement_counter += 1
            except:
                print("condition string error", condition_string)
                exit()
            if i == self.condition_depth - 1:
                ret_val = self.statements[statement_counter]
                if ret_val in shared_memory.keys():
                    ret_val = shared_memory[ret_val]
                # print("else condition, returning: ", ret_val)
                # exit()
                return float(ret_val)
        raise "unreachable statement"

    def mutate(self):
        # print("before", self.statements)
        index = random.randint(0, len(self.statements) - 1)
        candidate = self.statements[index]
        if candidate in self.connectors:
            replacement = random.choice(self.connectors)
        elif candidate in self.selection_pool:
            replacement = random.choice(self.selection_pool)
        elif candidate in self.conditionals:
            replacement = random.choice(self.conditionals)
            if candidate == "True" or candidate == "False":
                if replacement == "True" or replacement == "False":
                    # no change to replacement or the statements list is required because both need same operand count
                    pass
                else:
                    op1 = random.choice(self.selection_pool)
                    op2 = random.choice(self.selection_pool)
                    temp_list = copy.deepcopy(self.statements[:index]) + [op1, replacement, op2] + copy.deepcopy(self.statements[index+1:])
                    self.statements = copy.deepcopy(temp_list)
                    # print("after", self.statements)
                    return
            else:
                if replacement == "True" or replacement == "False":
                    self.statements = self.statements[:index-1] + [replacement] + self.statements[index+2:]
                    # print("after", self.statements)
                    return
                else:
                    # no change to replacement or the statements list is required because both need same operand count
                    pass
        else:
            print(candidate)
            raise "Unknown candidate type"

        self.statements[index] = replacement
        # print("after", self.statements)

    def annotate(self):
        annotation = "if"
        statement_counter = 0
        condition_string = ""
        for i in range(self.condition_depth):
            condition_string = ""
            j = 0
            while j < self.condition_count:
                candidate = self.statements[statement_counter]
                if candidate in self.selection_pool:
                    op1 = candidate
                    conditional = self.statements[statement_counter + 1]
                    op2 = self.statements[statement_counter + 2]
                    condition_string += " {} {} {}".format(op1, conditional, op2)
                    statement_counter += 3
                elif candidate in self.connectors:
                    condition_string += " " + candidate
                    statement_counter += 1
                    j -= 1
                elif candidate in self.conditionals and (candidate == "True" or candidate == "False"):
                    condition_string += " " + candidate
                    statement_counter += 1
                else:
                    print("unknown candidate: ", candidate)
                    exit()
                j += 1

            annotation += condition_string + ":\n\t"
            annotation += "return " + self.statements[statement_counter] + "\n"
            statement_counter += 1

            if statement_counter == len(self.statements) - 1:
                annotation += "else:\n\t" + "return " + self.statements[statement_counter] + "\n"
                return annotation
            else:
                annotation += "elif"
        print(self.statements)
        raise "unreachable statement"


class CueProgram:
    def __init__(self, config, inputs, constants, operators, outputs, registers, has_discrete_output):
        self.has_discrete_output = has_discrete_output
        self.output_selection_pool = None
        self.warning_flag = True
        self.discrete_output = None
        self.selection_pool = None
        self.config = config
        self.dynamic_inputs = self.config["cue_dynamic_inputs"]
        self.random_walk_step_size = int(self.config["random_walk_step_size"])
        self.cue_system = self.config["cue_system"]
        self.cue_init_radius = int(self.config["cue_init_radius"])
        self.lgp_max_size = int(self.config["cue_lgp_size_max"])
        self.revisit_penalty = float(self.config["cue_revisit_penalty"])
        self.inputs = inputs
        self.constants = constants
        self.operators = operators
        self.registers = registers
        self.outputs = outputs
        self.visitable = True
        self.pos = ()
        self.statements = []
        self.visit_count = 0
        self.logged_cost = 0
        self.program_type = "I"  # or O
        self.init_input_selection_pool()
        self.init_lgp_output_selection_pool()
        if self.config["debug"] == "0":
            self.debug = False
        else:
            self.debug = True

    def init_input_selection_pool(self):
        self.selection_pool = copy.deepcopy(self.inputs)
        if "float" not in self.selection_pool.keys():
            self.selection_pool["float"] = []
        for constant in self.constants:
            self.selection_pool["float"].append(constant)

        for register in self.registers:
            self.selection_pool["float"].append(register)

    def init_lgp_output_selection_pool(self):
        self.output_selection_pool = {}
        if self.dynamic_inputs == "True":
            self.output_selection_pool = copy.deepcopy(self.inputs)
        else:
            self.output_selection_pool["float"] = []
        for register in self.registers:
            self.output_selection_pool["float"].append(register)

    def generate_statement(self):
        try:
            random_index = random.randint(0, len(self.operators) - 1)
        except ValueError:
            raise "Empty Operator List. This can be due to unsuitable function set"

        op = None
        while len(self.operators) > 0:
            op = copy.deepcopy(self.operators[random_index])
            success_flag = True
            for demand in op.demands():
                if demand not in self.selection_pool.keys():
                    del self.operators[random_index]
                    success_flag = False
                    break
                operand = random.choice(self.selection_pool[demand])
                op.operands.append(operand)
            if not success_flag:
                continue

            if op.products()[0] is None or op.products()[0] == "command" or op.products()[0] == "structural":
                break
            for product in op.products():
                if product not in self.output_selection_pool.keys():
                    del self.operators[random_index]
                    success_flag = False
                    break
                output = random.choice(self.output_selection_pool[product])
                op.outputs.append(output)
            if success_flag:
                break
        if op is None:
            raise "No suitable function found for the given input set"
        return op

    def generate(self, size):
        for i in range(size):
            op = self.generate_statement()
            self.statements.append(op)
        return_value_selection_pool = {}
        if "float" in self.selection_pool.keys():
            return_value_selection_pool["float"] = copy.deepcopy(self.selection_pool["float"])
        if "int" in self.selection_pool.keys():
            return_value_selection_pool["int"] = copy.deepcopy(self.selection_pool["int"])

        if int(self.config["conditional_return"]) <= 0:
            if "float" in return_value_selection_pool.keys() and len(return_value_selection_pool["float"]) > 0:
                return_var = random.choice(return_value_selection_pool["float"])
            elif "int" in return_value_selection_pool.keys() and len(return_value_selection_pool["int"]) > 0:
                return_var = random.choice(return_value_selection_pool["int"])
            else:
                return_var = "0"
            self.statements.append(return_var)
        else:
            retcon_operator = Retcon(int(self.config["conditional_return"]), int(self.config["conditional_return_depth"]), return_value_selection_pool)
            # print("before\t", retcon_operator.statements)
            retcon_operator.generate()
            # print("after\t", retcon_operator.statements)
            self.statements.append(retcon_operator)

    def add_indent(self, program_txt: str):
        indent = "\t"
        indented_program_txt = program_txt.replace("\n", "\n\t")
        indented_program_txt = indent + indented_program_txt
        return indented_program_txt

    def annotation(self):
        annotation = ""
        indent = "\t"
        for index, statement in enumerate(self.statements):
            if index == len(self.statements) - 1:
                # Return Statement
                indent = "\t"
                if statement.__class__.__name__ == "Retcon":
                    annotation += self.add_indent(statement.annotate())
                else:
                    annotation += indent + "return " + repr(statement)
            else:
                annotation += indent + statement.annotate() + "\n"
                if statement.products()[0] == "structural":
                    indent += "\t"
                elif len(indent) > len("\t"):  # normal instruction
                    indent = "\t"
            # print("decreasing indent")

            if index is len(self.statements) - 2 and statement.products()[0] == "structural":
                annotation += indent + "pass\n"

        return annotation

    def cost(self, source_pos):
        global SHARED_memory

        max_distance = math.sqrt(8 * self.cue_init_radius ** 2)  # math equation for max size
        max_complexity = self.lgp_max_size
        distance = distance_to_pos(source_pos, self.pos)
        if distance > max_distance:
            distance = max_distance
        complexity = len(self.statements)

        if self.cue_system == "programmatical":
            # last element of the statements is the key to the value to be returned
            if self.statements[-1].__class__.__name__ == "Retcon":
                return_val = self.statements[-1].eval(SHARED_memory)
            elif self.statements[-1] == 0:
                return_val = 0
            elif self.statements[-1].isnumeric():
                return_val = float(self.statements[-1])
            else:
                return_val = SHARED_memory[self.statements[-1]]
        elif self.cue_system == "temporospatial":
            return_val = 0
        else:
            raise "Unknown cue_system: {}. Please edit the config file".format(self.cue_system)
        # normalized_distance = distance / max_distance
        # normalized_complexity = complexity / max_complexity
        # ln_normalized_distance = math.log(1+normalized_distance)
        # ln_normalized_complexity = math.log(1+normalized_complexity)
        # ln_return_value = math.log(1+abs(return_val))
        try:
            cost_formula = self.config["cost_formula"]
        except KeyError:
            raise KeyError("Config file does not contain a cost_formula field")

        try:
            cost_value = eval(cost_formula)
        except OverflowError:
            cost_value = float("inf")

        if cost_value < self.logged_cost:
            cost_value = self.logged_cost

        if self.config["cue_enable_loops"] == "True":
            cost_value += (cost_value + 1) * self.visit_count * self.revisit_penalty

        return abs(cost_value)

    def program_eval(self):
        global SHARED_memory
        program_output = None
        skip_next = False
        for statement in self.statements:
            if statement == self.statements[-1]:
                if statement == 0:
                    program_output = 0
                elif statement.__class__.__name__ == "Retcon":
                    program_output = statement.eval(SHARED_memory)
                elif statement.isnumeric():
                    program_output = float(statement)
                else:
                    program_output = SHARED_memory[statement]
                break
            if skip_next:
                skip_next = False
                continue
            input_set = self.construct_op_inputs_from_memory(statement.operands)
            statement_return = statement.eval(input_set)
            # skip is a valid output from operators. skip, skips the execution of the next operator.
            # None or skip does not update the shared memory
            if statement_return == "skip":
                skip_next = True
                continue
            if statement_return is None:
                continue
            if statement_return == "end":
                return "end"
            SHARED_memory[statement.outputs[0]] = statement_return
            pass
        return program_output

    def spatial_mutation(self):
        rand = random.random()
        unattended_chance = 0.5 # I should change this but this is for a later time
        if self.has_discrete_output:
            unattended_chance = 1
        if rand < unattended_chance:
            # change pos with step
            random_step_x = random.randint(-1 * self.random_walk_step_size, self.random_walk_step_size)
            random_step_y = random.randint(-1 * self.random_walk_step_size, self.random_walk_step_size)
            if abs(random_step_x + self.pos[0]) > self.cue_init_radius:
                random_step_x = 0
            if abs(self.pos[1] + random_step_y) > self.cue_init_radius:
                random_step_y = 0
            self.pos = (self.pos[0] + random_step_x, self.pos[1] + random_step_y)
        else:
            # change i/o
            if self.program_type == "O":
                self.program_type = "I"
            else:
                self.program_type = "O"

    def add_lgp_statement_mutation(self):
        if len(self.statements) < self.lgp_max_size:
            statement = self.generate_statement()
            if len(self.statements) < 2:
                random_index = 0
            else:
                random_index = random.randint(0, len(self.statements) - 2)
            self.statements.insert(random_index, statement)

    def remove_lgp_statement_mutation(self):
        if len(self.statements) > 1:
            random_index = random.randint(0, len(self.statements) - 2)
            del self.statements[random_index]

    def mutate_return_value(self):
        if self.statements[-1].__class__.__name__ == "Retcon":
            self.statements[-1].mutate()
        else:
            return_value_selection_pool = copy.deepcopy(self.output_selection_pool)
            for constant in self.constants:
                return_value_selection_pool["float"].append(constant)

            if "float" in return_value_selection_pool.keys() and len(return_value_selection_pool["float"]) > 0:
                return_var = random.choice(return_value_selection_pool["float"])
            elif "int" in return_value_selection_pool.keys() and len(return_value_selection_pool["int"]) > 0:
                return_var = random.choice(return_value_selection_pool["int"])
            else:
                return_var = "0"

            self.statements[-1] = return_var

    def change_operand_mutation(self, random_index):
        random_operand_index = random.randint(0, len(self.statements[random_index].demands()) - 1)
        operand = random.choice(
            self.selection_pool[self.statements[random_index].demands()[random_operand_index]])
        self.statements[random_index].operands[random_operand_index] = operand

    def change_output_mutation(self, random_index):
        if self.statements[random_index].products()[0] == "command" or self.statements[random_index].products()[0] == \
                "structural" or self.statements[random_index].products()[0] is None:
            return
        random_operand_index = random.randint(0, len(self.statements[random_index].products()) - 1)
        output = random.choice(
            self.output_selection_pool[self.statements[random_index].products()[random_operand_index]])
        self.statements[random_index].outputs[random_operand_index] = output

    def lgp_mutation(self):
        # add statement, remove statement, modify statement each have 33% chance
        rand = random.random()
        if rand <= 0.33:
            self.add_lgp_statement_mutation()
        elif rand <= 0.66:
            self.remove_lgp_statement_mutation()
        else:
            random_index = random.randint(0, len(self.statements) - 1)
            if random_index == len(self.statements) - 1:
                self.mutate_return_value()
            else:
                if random.random() < 0.5:
                    # change operand
                    if len(self.statements[random_index].demands()) > 0:
                        self.change_operand_mutation(random_index)
                else:
                    # change output
                    if len(self.statements[random_index].products()) > 0:
                        self.change_output_mutation(random_index)
        rand = random.random()
        ret_mut_chance = float(self.config["return_mutation_rate_increase_handle"])
        if rand < ret_mut_chance:
            self.mutate_return_value()

    @staticmethod
    def construct_op_inputs_from_memory(operands):
        global SHARED_memory
        value_list = []
        for operand in operands:
            if operand.isnumeric():
                value_list.append(float(operand))
            else:
                try:
                    value_list.append(SHARED_memory[operand])
                except KeyError:
                    value_list.append(operand)
        return value_list


def distance_to_center(pos):
    return math.sqrt(pos[0] ** 2 + pos[1] ** 2)


class CueIndividual(AbstractIndividual):
    def __init__(self, config) -> None:
        super().__init__()
        self.has_mem_inited = False
        self.execution_register_flow = None
        self.execution_flow_title = None
        self.execution_flow_plt = None
        self.execution_flow_index = None
        self.execution_flow = None
        self.has_discrete_output = False
        self.individual_index = None
        if config["debug"] == "0":
            self.debug = False
        else:
            self.debug = True

        self.memory = None
        self.programs_destructible_list = None
        self.config = config
        self.output_ratio = float(self.config["cue_output_ratio"])
        if self.config["cue_enable_loops"] == "True":
            self.enable_loops = True
        else:
            self.enable_loops = False
        self.import_set = None
        self.programs: list[CueProgram] = []

        self.L = Log(config["output_level"], self.__class__.__name__)

        self.input_pool = json.loads(self.config["inputs"])  # is a dictionary

        self.operator_pool = self.create_operator_objects()
        if self.config["constants"] != "None":
            self.constant_pool = self.config["constants"].replace(" ", "").split(",")
        else:
            self.constant_pool = []
        try:
            self.output_pool = json.loads(self.config["outputs"])
        except json.decoder.JSONDecodeError:
            self.output_pool = self.config["outputs"].replace(" ", "").split(",")
            self.has_discrete_output = True
        # print(self.config["outputs"])
        # exit()
        # self.output_pool = json.loads(self.config["outputs"])
        # exit()
        self.input_registers = self.config["registers"]
        self.registers = {}
        if self.input_registers != "None":
            tokens = self.input_registers
            tokens = tokens.split("[")

            name = tokens[0]
            size = int(tokens[1][:len(tokens[1]) - 1])
            for i in range(size):
                new_name = name + str(i)
                self.registers[new_name] = 0

        self.reformat_pools()

        if self.config["conditionals"] != "None":
            if "conditional" not in self.input_pool.keys():
                self.input_pool["conditional"] = []
            conditionals: list[str] = self.config["conditionals"].split(",")
            for conditional in conditionals:
                conditional = conditional.strip()
                self.input_pool["conditional"].append(conditional)

        self.cue_init_size_min = int(self.config["cue_init_size_min"])
        self.cue_init_size_max = int(self.config["cue_init_size_max"])
        self.cue_init_lgp_size_min = int(self.config["cue_init_lgp_size_min"])
        self.cue_init_lgp_size_max = int(self.config["cue_init_lgp_size_max"])

        self.make_import_set()

        self.cue_init_radius = int(self.config["cue_init_radius"])

        self.eval_time_limit = int(self.config["cue_max_evaluation_time"].split("ms")[0])

    def init_random(self, init_type="grow"):
        self.L.D("init_random()")
        if init_type == "grow":
            program_count = random.randint(self.cue_init_size_min, self.cue_init_size_max)
        else:
            program_count = self.cue_init_size_max

        for i in range(program_count):
            program = CueProgram(self.config, self.input_pool, self.constant_pool, self.operator_pool, self.output_pool,
                                 self.registers, self.has_discrete_output
                                 )
            if not self.has_discrete_output:
                if random.random() < self.output_ratio:
                    program.program_type = "O"
            program_size = random.randint(self.cue_init_lgp_size_min, self.cue_init_lgp_size_max)
            program.generate(program_size)
            x = random.randint(-1 * self.cue_init_radius, self.cue_init_radius)
            y = random.randint(-1 * self.cue_init_radius, self.cue_init_radius)
            program.pos = (x, y)

            self.programs.append(program)
        if self.has_discrete_output:
            for possible_discrete_output in self.output_pool:
                program = CueProgram(self.config, self.input_pool, self.constant_pool, self.operator_pool,
                                     self.output_pool,
                                     self.registers, self.has_discrete_output
                                     )
                program.program_type = "O"
                program.discrete_output = possible_discrete_output
                program_size = random.randint(self.cue_init_lgp_size_min, self.cue_init_lgp_size_max)
                program.generate(program_size)
                x = random.randint(-1 * self.cue_init_radius, self.cue_init_radius)
                y = random.randint(-1 * self.cue_init_radius, self.cue_init_radius)
                program.pos = (x, y)
                self.programs.append(program)

    def create_operator_objects(self):
        self.L.D("create_operator_objects()")
        operators = []
        try:
            packages = self.config["operators"].split(",")
        except IndexError or KeyError:
            self.L.W("Object type doesn't exist in the config file. Returning an empty list")
            return []

        for package in packages:
            package = package.strip()
            try:
                modules = self.config[package].split(",")
            except IndexError or KeyError:
                self.L.W("Package name doesn't exist in the config file. Returning an empty list")
                return []
            for module in modules:
                module = module.strip()
                imported_class = importlib.import_module("Operators.{}".format(package))
                my_class = getattr(imported_class, module)
                obj = my_class()
                operators.append(obj)
        return operators

    def make_import_set(self):
        self.L.D("make_import_set()")
        self.import_set = ""
        import_string = ""
        for operator in self.operator_pool:
            import_string += operator.op_code() + "\n"
        self.import_set = import_string

    def reformat_pools(self):
        new_input_pool = {}
        for var_name in self.input_pool:
            data_type = self.input_pool[var_name]
            if data_type not in new_input_pool.keys():
                new_input_pool[data_type] = []
            new_input_pool[data_type].append(var_name)

        self.input_pool = new_input_pool

        new_output_pool = {}

        if type(self.output_pool) == dict:
            for var_name in self.output_pool:
                data_type = self.output_pool[var_name]
                if data_type not in new_output_pool.keys():
                    new_output_pool[data_type] = []
                new_output_pool[data_type].append(var_name)

            self.output_pool = new_output_pool
        elif type(self.output_pool) == list:
            pass
        else:
            raise "Unknown output entry"

    def closest_program_to_center(self):
        selected_program = None
        for program in self.programs:
            if selected_program is None:
                selected_program = program
                continue
            if distance_to_center(program.pos) < distance_to_center(selected_program.pos):
                pass

    def show_registers(self):
        global SHARED_memory
        print("Register values:")
        for register in SHARED_memory:
            print(register, SHARED_memory[register])

    def individual_reset(self):
        global SHARED_memory
        SHARED_memory.update(self.registers)

    def individual_eval(self, problem_inputs, return_flow=False):
        self.L.D("eval()")
        # start flow
        # each list inside the flow list is a step to be visualized
        flow = []
        mem_history = []
        # end flow

        global SHARED_memory
        current_program = None
        program_output = None
        discrete_output = None

        SHARED_memory.update(problem_inputs)
        self.programs_destructible_list = copy.deepcopy(self.programs)

        if self.config["memory"] == "False":
            self.individual_reset()
        else:
            # we have memory
            if not self.has_mem_inited:
                self.individual_reset()
                self.has_mem_inited = True

        has_output = False
        for program in self.programs_destructible_list:
            if program.program_type == "O":
                has_output = True
                if self.debug:
                    print("Model has output")

        execution_counter = 0
        execution_limit = 0
        if not has_output:
            execution_limit = len(self.programs_destructible_list)

        # if self.debug:
        # 	self.show_registers()

        start_time = time.time()
        while True:
            if execution_limit > 0:
                if execution_counter > execution_limit:
                    if self.debug:
                        print("Model execution limit passed. Ending")
                    break
                else:
                    execution_counter += 1
            if return_flow:
                current_program, step_flow = self.select_program(current_program, return_flow)
                flow.append(step_flow)
                mem_history.append(copy.deepcopy(SHARED_memory))
            else:
                current_program = self.select_program(current_program)

            if current_program is None:
                if self.debug:
                    print("Current program is None. Ending")
                break

            temp_output = current_program.program_eval()

            # To Do:: end and exit are not implemented in the output program
            if temp_output == "end":
                if self.debug:
                    print("END REACHED. Ending")
                self.programs_destructible_list.remove(current_program)
                continue

            if temp_output == "exit":
                if self.debug:
                    print("Exit signal received. Ending")
                break

            program_output = temp_output

            # if self.debug:
            # 	self.show_registers()

            if self.debug:
                print("Output:", program_output)

            if current_program.program_type == "O":
                if self.debug:
                    print("Current program is Output. Ending")
                discrete_output = current_program.discrete_output
                break
            elapsed_time = (time.time() - start_time) * 1000
            if 0 < self.eval_time_limit < elapsed_time:
                if self.debug:
                    print("Program timeout. Ending")
                program_output = None
                break

        if self.debug:
            # Adds beauty to the beast
            print()

        if return_flow:
            return flow, mem_history
        if program_output is None:
            return 0, SHARED_memory
        # print(debug_counter)

        if self.has_discrete_output:
            program_output = discrete_output

        return program_output, SHARED_memory

    def select_program(self, current_program, return_flow=False):
        step_flow = []
        if current_program is None:
            source_pos = (0, 0)
        else:
            source_pos = current_program.pos
        if return_flow:
            step_flow.append([None, source_pos, None, None])
        selected_program = None
        selected_index = None
        program_costs = []
        current_index = -1
        for index, program in enumerate(self.programs_destructible_list):
            candidate_cost = program.cost(source_pos)
            if candidate_cost == float("inf") or candidate_cost == float("nan"):
                return None
            program_costs.append(candidate_cost)

            if self.config["cue_self_loop"] != "True" and current_program == program:
                current_index = index
                continue
            elif current_program == program:
                current_index = index

            if not self.enable_loops:
                if program.visit_count > 0:
                    continue

            if return_flow:
                p_name = "P" + str(index)
                p_pos = program.pos
                p_type = program.program_type
                p_cost = candidate_cost
                p_output = program.discrete_output
                step_flow.append([p_name, p_pos, p_type, p_cost, p_output])

            if selected_program is None:
                selected_program = program
                selected_index = index
                continue
            if candidate_cost < selected_program.cost(source_pos):
                selected_program = program
                selected_index = index


        if self.config["debug"] == "1":
            for index, cost in enumerate(program_costs):
                if current_index == index:
                    self.L.Bprint("P" + repr(index) + " " + str(round(cost, 2)))
                elif selected_index == index:
                    self.L.Hprint("P" + repr(index) + " " + str(round(cost, 2)))
                else:
                    self.L.Gprint("P" + repr(index) + " " + str(round(cost, 2)))
                if self.programs_destructible_list[index].program_type == "O":
                    print("O", end="")
                self.L.Yprint(" " + str(self.programs_destructible_list[index].visit_count) + " ")
            print()
        # if selected_program is not None and self.debug:
        # 	print(selected_program.annotation())

        if selected_program is not None:
            selected_program.visit_count += 1
            selected_program.logged_cost = abs(selected_program.cost(source_pos))

        if return_flow:
            return selected_program, step_flow
        return selected_program

    def crossover(self, parent_b):
        # self.visualize()
        # parent_b.visualize()
        radius = int(self.cue_init_radius / 2)
        rand_x = random.randint(-1 * radius, radius)
        rand_y = random.randint(-1 * radius, radius)
        a_inside_programs = []
        a_outside_programs = []
        b_inside_programs = []
        b_outside_programs = []
        a_output_programs = []
        b_output_programs = []
        max_program_size = int(self.config["cue_size_max"])
        for program in self.programs:
            if not self.has_discrete_output:
                discrete_output_condition = True
            else:
                discrete_output_condition = not (program.program_type == "O")
                if program.program_type == "O":
                    a_output_programs.append(program)
            if discrete_output_condition:
                if distance_to_pos(program.pos, (rand_x, rand_y)) <= radius:
                    a_inside_programs.append(program)
                else:
                    a_outside_programs.append(program)
        for program in parent_b.programs:
            if not self.has_discrete_output:
                discrete_output_condition = True
            else:
                discrete_output_condition = not (program.program_type == "O")
                if program.program_type == "O":
                    b_output_programs.append(program)
            if discrete_output_condition:
                if distance_to_pos(program.pos, (rand_x, rand_y)) <= radius:
                    b_inside_programs.append(program)
                else:
                    b_outside_programs.append(program)
        offspring_a = CueIndividual(self.config)
        offspring_b = CueIndividual(self.config)

        ab_inside_outside_programs = a_inside_programs + b_outside_programs
        ba_inside_outside_programs = a_outside_programs + b_inside_programs

        if len(ab_inside_outside_programs) > max_program_size:
            ab_inside_outside_programs = copy.deepcopy(ab_inside_outside_programs[:max_program_size-1])

        if len(ba_inside_outside_programs) > max_program_size:
            ba_inside_outside_programs = copy.deepcopy(ba_inside_outside_programs[:max_program_size - 1])

        offspring_a.programs = ab_inside_outside_programs + a_output_programs
        offspring_b.programs = ba_inside_outside_programs + b_output_programs
        offspring_a = copy.deepcopy(offspring_a)
        offspring_b = copy.deepcopy(offspring_b)
        # offspring_a.visualize()
        # offspring_b.visualize()

        return offspring_a, offspring_b

    def add_program(self):
        max_size = int(self.config["cue_size_max"])
        if len(self.programs) >= max_size:
            return
        program = CueProgram(self.config, self.input_pool, self.constant_pool, self.operator_pool, self.output_pool,
                             self.registers, self.has_discrete_output)
        program_size = random.randint(self.cue_init_lgp_size_min, self.cue_init_lgp_size_max)
        program.generate(program_size)
        x = random.randint(-1 * self.cue_init_radius, self.cue_init_radius)
        y = random.randint(-1 * self.cue_init_radius, self.cue_init_radius)
        program.pos = (x, y)
        if not self.has_discrete_output:
            if random.random() < self.output_ratio:
                program.program_type = "O"
        self.programs.append(program)

    def get_full_program_txt(self, index, program, global_txt):
        full_program_txt = ""
        full_program_txt += "def p{}(self):\n".format(index)
        full_program_txt += "\t" + global_txt + "\n"
        full_program_txt += program.annotation()
        return full_program_txt

    def add_indent(self, program_txt: str):
        indent = "\t"
        indented_program_txt = program_txt.replace("\n", "\n\t")
        indented_program_txt = indent + indented_program_txt
        return indented_program_txt

    def generate_method_attribute_text(self, cost: int, pos: tuple, return_var, ptype, discrete_output):
        if return_var.__class__.__name__ == "Retcon":
            return_var = return_var.annotate()
            cost_pos_txt = "discrete_output = '{}'\ntype = '{}'\nreturn_var = \"\"\"{}\"\"\"\ncomplexity = {}\n" \
                           "pos = {}\nvisit_count = 0"\
                .format(discrete_output, ptype, return_var, cost, str(pos))
        else:
            cost_pos_txt = "discrete_output = '{}'\ntype = '{}'\nreturn_var = '{}'\ncomplexity = {}\npos = {}\n" \
                           "visit_count = 0"\
                .format(discrete_output, ptype, return_var, cost, str(pos))
        return cost_pos_txt

    def generate_inputs_txt(self):
        inputs_txt = "# Input Definition\n"
        # exit()
        for item in self.input_pool:
            if not item == "conditional":
                for inp in self.input_pool[item]:
                    inputs_txt += "{} = None\n".format(inp)

        return inputs_txt

    def generate_register_txt(self):
        register_txt = "# Register Definition\n"
        for register in self.registers:
            register_txt += "{} = {}\n".format(register, self.registers[register])
        return register_txt

    def generate_globals_txt(self):
        global_txt = "global "
        for index, item in enumerate(self.input_pool):
            if not item == "conditional":
                for index2, inp in enumerate(self.input_pool[item]):
                    global_txt += inp
                    global_txt += ", "
        if len(self.registers) < 1:
            global_txt = global_txt[:-1]
        for index, register in enumerate(self.registers):
            global_txt += register
            if index != len(self.registers) - 1:
                global_txt += ", "

        return global_txt

    def generate_operators_def_txt(self):
        operators_def_txt = ""
        for operator in self.operator_pool:
            operators_def_txt += operator.op_code() + "\n"
        return operators_def_txt

    def generate_interpreter_helpers_txt(self):
        select_program = ("\n\n"
                          "def select_program(current_program):\n"
                          "\tglobal program_objects, enable_loops, debug\n"
                          "\tif current_program is None:\n"
                          "\t\tsource = (0, 0)\n"
                          "\telse:\n"
                          "\t\tsource = current_program.pos\n"
                          "\tselected_program = None\n"
                          "\tselected_cost = None\n"
                          "\tfor program in program_objects:\n"
                          "\t\tdest = program.pos\n"
                          "\t\tprogram_cost = cost(source, dest, program.complexity, program.return_var, program.visit_count)\n"
                          "\t\tif program_cost == float(\"inf\") or program_cost == float(\"nan\"):\n"
                          "\t\t\treturn None\n"
                          "\t\tif program == current_program:\n"
                          "\t\t\tcontinue\n"
                          "\t\tif not enable_loops:\n"
                          "\t\t\tif program.visit_count > 0:\n"
                          "\t\t\t\tcontinue\n"
                          "\t\tif selected_program is None:\n"
                          "\t\t\tselected_program = program\n"
                          "\t\t\tselected_cost = program_cost\n"
                          "\t\t\tcontinue\n"
                          "\t\tif program_cost < selected_cost:\n"
                          "\t\t\tselected_program = program\n"
                          "\t\t\tselected_cost = program_cost\n"
                          "\tif debug == 1:\n"
                          "\t\tprint(selected_program.__class__.__name__, \"selected\")\n"
                          "\tif selected_program is not None:\n"
                          "\t\tselected_program.visit_count += 1\n"
                          "\treturn selected_program        \n"
                          "")
        distance_function = ("\n\n"
                             "def distance_to_pos(source, dest):\n"
                             "\treturn math.sqrt((dest[0] - source[0]) ** 2 + (dest[1] - source[1]) ** 2)        \n"
                             "")

        cost_formula = self.config["cost_formula"]

        cost_function = (
            "\n\n"
            "def cost(source, dest, complexity, return_var, visit_count):\n"
            "\tglobal max_complexity, max_distance, cue_system, enable_loops, revisit_penalty\n"
            "\tdistance = distance_to_pos(source, dest)\n"
            "\tnormalized_distance = distance / max_distance\n"
            "\tnormalized_complexity = complexity / max_complexity\n"
            "\tif cue_system == \"programmatical\":\n"
            "\t\ttry:\n"
            "\t\t\treturn_val = eval(return_var)\n"
            "\t\texcept SyntaxError:\n"
            "\t\t\treturn_var = str(return_var)\n"
            "\t\t\treturn_var = return_var.replace('\\n\\t', '\\n')\n"
            "\t\t\treturn_var = return_var.replace(\"\\t\\t\", \"\\t\")\n"
            "\t\t\treturn_var = return_var.replace(\"return \", \"program_output = \")\n"
            "\t\t\texec_locals = {}\n"
            "\t\t\texec(return_var, globals(), exec_locals)\n"
            "\t\t\treturn_val = exec_locals['program_output']\n"
            "\telif cue_system == \"temporospatial\":\n"
            "\t\treturn_val = 0\n"
            "\telse:\n"
            "\t\traise \"Unknown Cue System\"\n"
            "\tcost_value = " + cost_formula + "\n"
            "\tif enable_loops:\n"
            "\t\tcost_value += (cost_value + 1) * visit_count * revisit_penalty\n"
            "\treturn abs(cost_value)\n\n"
            ""
        )

        reset_function = self.generate_reset_txt()

        return select_program + distance_function + cost_function + reset_function

    def generate_interpreter_txt(self, globals_txt):
        # Setting up visit counts
        interpreter_txt = ""
        lgp_max_size = int(self.config["cue_lgp_size_max"])
        cue_init_radius = int(self.config["cue_init_radius"])
        max_distance = math.sqrt(8 * cue_init_radius ** 2)  # math equation for max size
        max_complexity = lgp_max_size
        cue_system = self.config["cue_system"]
        enable_loops = self.config["cue_enable_loops"]
        revisit_penalty = self.config["cue_revisit_penalty"]
        has_output = False
        for program in self.programs:
            if program.program_type == "O":
                has_output = True
        program_count = len(self.programs)
        discrete_output = str(self.has_discrete_output)
        interpreter_txt += "discrete_output = {}\nrevisit_penalty = {}\nmax_distance = {}\nmax_complexity = {}\n" \
                           "cue_system = '{}'\nenable_loops = {}\nhas_output = {}\n".format(
                            discrete_output, revisit_penalty, max_distance, max_complexity, cue_system, enable_loops,
                            has_output)

        object_creation_txt = "# noinspection PyListCreation\nprogram_objects = []\n"
        for index, _ in enumerate(self.programs):
            object_creation_txt += "program_objects.append(P{}())\n".format(index)

        interpreter_txt += "\n" + object_creation_txt

        interpreter_txt += self.generate_interpreter_helpers_txt()
        loop_txt = "program_output = None\n\n\n"
        loop_txt += "def run():\n"
        loop_txt += "\treset()\n\t"
        loop_txt += self.generate_globals_txt() + ", program_output\n"
        for item in self.input_pool:
            if not item == "conditional":
                for inp in self.input_pool[item]:
                    loop_txt += "\t{} = {}(input('Enter {}:'))\n".format(inp, item, inp)

        loop_txt += "\tcurrent_p = None\n\tprogram_output = None\n"
        if not has_output:
            loop_txt += "\tfor _ in range({}):".format(program_count)
        else:
            loop_txt += "\twhile True:"
        loop_txt += ("\n"
                     "\t\tcurrent_p = select_program(current_p)\n"
                     "\t\tif current_p is None:\n"
                     "\t\t\tbreak\n"
                     "\t\tfunction_name = current_p.__class__.__name__.lower()\n"
                     "\t\tprogram_output = eval(\"current_p.{}()\".format(function_name))\n"
                     "\t\tif current_p.type == \"O\":\n"
                     "\t\t\tbreak\n"
                     "\tif discrete_output:\n"
                     "\t\tprint(current_p.discrete_output)\n"
                     "\telse:\n"
                     "\t\tprint('Output:', eval(str(program_output)))\n"
                     "")
        interpreter_txt += "\n" + loop_txt
        return interpreter_txt

    def annotate_program(self, print_out=False):
        individual_programs_txt = ""
        import_txt = "debug = 0\n\nimport math\n\n"
        individual_programs_txt += import_txt
        inputs_txt = self.generate_inputs_txt()
        register_txt = self.generate_register_txt()
        individual_programs_txt += inputs_txt + "\n" + register_txt + "\n\n"
        globals_txt = self.generate_globals_txt()

        individual_programs_txt += "# Operator Function Definitions"
        operators_def_txt = self.generate_operators_def_txt()
        individual_programs_txt += operators_def_txt + "\n"

        individual_programs_txt += "# Individual Program Definitions\n"
        for index, program in enumerate(self.programs):
            program_txt = self.get_full_program_txt(index, program, globals_txt)
            class_txt = "class P{}:\n".format(index)
            cost = len(program.statements)
            pos = program.pos
            return_var = program.statements[-1]
            program_type = program.program_type
            discrete_output = program.discrete_output
            cost_pos_txt = self.generate_method_attribute_text(cost, pos, return_var, program_type, discrete_output)
            full_program = class_txt + self.add_indent(cost_pos_txt) + \
                           "\n\n" + self.add_indent(program_txt)
            individual_programs_txt += full_program + "\n\n\n"

        individual_programs_txt += "# SGP Interpreter\n"
        individual_programs_txt += self.generate_interpreter_txt(globals_txt)
        individual_programs_txt += "\n\nrun()\n"
        if print_out:
            print(individual_programs_txt)
            return individual_programs_txt
        else:
            return individual_programs_txt

    def generate_reset_txt(self):
        reset_txt = "\ndef reset():\n"
        global_vars = "\t" + self.generate_globals_txt() + "\n"
        reset_visit_counts = "\tfor program in program_objects:\n" \
                             "\t\tprogram.visit_count = 0"
        reset_registers = "\n"
        for register in self.registers:
            reset_registers += "\t{} = 0\n".format(register)
        reset_txt += global_vars + reset_visit_counts + reset_registers + "\n"
        return reset_txt

    def visualize(self):
        fig = plt.figure()
        fig.set_dpi(100)
        fig.set_size_inches(7, 7)
        axes_size = float(self.config["cue_init_radius"])
        ax = plt.axes(xlim=(-1 * axes_size, axes_size), ylim=(-1 * axes_size, axes_size))
        dotted_line = plt.Line2D((-1 * axes_size, axes_size), (0, 0), lw=1.,
                                 ls=':', marker='.',
                                 alpha=0.5)
        ax.add_line(dotted_line)
        dotted_line = plt.Line2D((0, 0), (-1 * axes_size, axes_size), lw=1.,
                                 ls=':', marker='.',
                                 alpha=0.5)
        ax.add_line(dotted_line)
        for program in self.programs:
            if program.program_type == "I":
                fc = 'y'
            else:
                fc = 'r'
            # noinspection PyTypeChecker
            patch = plt.Circle(program.pos, 0.2, fc=fc)
            patch.center = program.pos
            ax.add_patch(patch)
        plt.show()

    def on_press(self, event):
        if event is None:
            self.execution_flow_index = 0
        elif event.key == "right":
            self.execution_flow_index += 1
            if self.execution_flow_index >= len(self.execution_flow):
                self.execution_flow_index = len(self.execution_flow) - 1
        elif event.key == "left":
            self.execution_flow_index -= 1
            if self.execution_flow_index < 0:
                self.execution_flow_index = 0
        else:
            return
        print(self.execution_register_flow[self.execution_flow_index])
        plt.clf()
        font = {'family': 'DejaVu Sans',
                'weight': 'light',
                'size': 6}
        axes_size = float(self.config["cue_init_radius"]) + 1

        ax = plt.axes(xlim=(-1 * axes_size, axes_size), ylim=(-1 * axes_size, axes_size))
        step = self.execution_flow[self.execution_flow_index]

        plt.title("Individual: " + self.execution_flow_title + " Step " + str(self.execution_flow_index + 1) + "/" +
                  str(len(self.execution_flow)))
        dotted_line = plt.Line2D((-1 * axes_size, axes_size), (0, 0), lw=1.,
                                 ls=':', marker='.',
                                 alpha=0.5)
        ax.add_line(dotted_line)

        dotted_line = plt.Line2D((0, 0), (-1 * axes_size, axes_size), lw=1., ls=':', marker='.', alpha=0.5)
        ax.add_line(dotted_line)
        source_pos = step[0][1]

        lowest_cost = None
        lowest_cost_index = None
        for index, program in enumerate(step):
            if lowest_cost is None:
                lowest_cost_index = index
                lowest_cost = program[3]
                continue
            if program[3] < lowest_cost:
                lowest_cost = program[3]
                lowest_cost_index = index

        for index, program in enumerate(step):
            if index == 0:
                continue
            name = program[0]
            pos = program[1]
            p_type = program[2]
            cost = program[3]
            output = program[4]
            if output is not None:
                name = output
            if p_type == "I":
                fc = "y"
            else:
                fc = "r"
            net_line_width = 0.5
            net_line_alpha = 0.5
            if index == lowest_cost_index:
                net_line_width = 3
                net_line_alpha = 0.8
                fc = "g"
            p_patch = plt.Circle(pos, 0.6, fc=fc)
            p_patch.center = pos
            ax.add_patch(p_patch)

            s_patch = plt.Circle(source_pos, 0.2, fc="g", zorder=5)
            s_patch.center = source_pos
            ax.add_patch(s_patch)

            plt.text(pos[0] - 0.3, pos[1] - 0.15, name)

            net_line = plt.Line2D((source_pos[0], pos[0]), (source_pos[1], pos[1]), lw=net_line_width, marker='.',
                                  alpha=net_line_alpha,
                                  zorder=-1)
            mid_pos = ((source_pos[0] + pos[0]) / 2, (source_pos[1] + pos[1]) / 2)
            plt.text(mid_pos[0] - 0.2, mid_pos[1], round(cost, 2), font)
            ax.add_line(net_line)

            # ax.add_patch(text)

            # if self.execution_flow_index < len(flow) - 1:
            #     plt.clf()
            #     ax = plt.axes(xlim=(-1 * axes_size, axes_size), ylim=(-1 * axes_size, axes_size))
            # plt.clf()
            # plt.close()
        plt.draw()

    def show_execution_flow(self, inputs, title="n/a"):
        self.execution_flow = None
        flow, mem_history = self.individual_eval(inputs, return_flow=True)
        self.execution_flow = flow
        self.execution_register_flow = mem_history
        self.execution_flow_index = 0
        if title == "n/a":
            title = str(self.individual_index)
        self.execution_flow_title = title

        # for step in flow:
        #     for program in step:
        #         print(program)
        #     print("----------")
        # exit()

        fig = plt.figure()
        self.execution_flow_plt = plt
        fig.set_dpi(100)
        fig.set_size_inches(7, 7)

        fig.canvas.mpl_connect('key_press_event', self.on_press)
        self.on_press(None)

        plt.show()
