# This code is a generated/synthesized SGP model/program
# ============================================

debug = 0

import math

# Input Definition
c0 = None
c1 = None
c2 = None
c3 = None
c4 = None
c5 = None
c6 = None
c7 = None
c8 = None

# Register Definition
a0 = 0
a1 = 0
a2 = 0
a3 = 0
a4 = 0
a5 = 0
a6 = 0
a7 = 0
a8 = 0


# Operator Function Definitions
# returns sum of two given number arguments
def op_sum(a, b):
	return a + b


# returns division of two given number arguments (returns 1 if division by zero)
def op_div(a, b):
	if b == 0:
		return 1
	return a / b


# returns multiplication of two given number arguments
def op_mult(a, b):
	return a * b


# returns subtraction of two given number arguments
def op_minus(a, b):
	return a - b



# Individual Program Definitions
class P0:
	type = 'I'
	return_var = '6'
	complexity = 8
	pos = (-8, -4)
	visit_count = 0

	def p0(self):
		global c0, c1, c2, c3, c4, c5, c6, c7, c8, a0, a1, a2, a3, a4, a5, a6, a7, a8
		a1 = 5
		a2 = a1 - a6
		a4 = 8 + a3
		a2 = 6
		a6 = c7 * c5
		a8 = 0
		a1 = 3 * 4
		return '6'


class P1:
	type = 'O'
	return_var = 'a8'
	complexity = 6
	pos = (-1, -1)
	visit_count = 0

	def p1(self):
		global c0, c1, c2, c3, c4, c5, c6, c7, c8, a0, a1, a2, a3, a4, a5, a6, a7, a8
		a3 = a8 * a5
		a2 = 8 - c8
		a0 = 4 - a2
		a2 = c4 + a7
		a8 = c1 + c0
		return 'a8'


class P2:
	type = 'O'
	return_var = 'a8'
	complexity = 6
	pos = (3, 7)
	visit_count = 0

	def p2(self):
		global c0, c1, c2, c3, c4, c5, c6, c7, c8, a0, a1, a2, a3, a4, a5, a6, a7, a8
		a6 = c3 + 7
		a6 = op_div(c8, 1)
		a3 = a8
		a6 = c4
		a8 = c1 + c0
		return 'a8'


class P3:
	type = 'O'
	return_var = 'a8'
	complexity = 5
	pos = (0, 3)
	visit_count = 0

	def p3(self):
		global c0, c1, c2, c3, c4, c5, c6, c7, c8, a0, a1, a2, a3, a4, a5, a6, a7, a8
		a6 = 2 * a3
		a6 = 1
		a7 = 1
		a8 = c1 + c0
		return 'a8'


class P4:
	type = 'O'
	return_var = 'a8'
	complexity = 10
	pos = (1, 1)
	visit_count = 0

	def p4(self):
		global c0, c1, c2, c3, c4, c5, c6, c7, c8, a0, a1, a2, a3, a4, a5, a6, a7, a8
		a3 = op_div(a8, a0)
		a4 = a5 + c7
		a7 = a5 - c0
		a5 = 6
		a2 = c1 + c3
		a8 = c7
		a0 = 1 * c2
		a4 = c5 + c2
		a8 = c1 + c0
		return 'a8'


# SGP Interpreter
revisit_penalty = 0.01
max_distance = 28.284271247461902
max_complexity = 10
cue_system = 'programmatical'
enable_loops = False
has_output = True

# noinspection PyListCreation
program_objects = []
program_objects.append(P0())
program_objects.append(P1())
program_objects.append(P2())
program_objects.append(P3())
program_objects.append(P4())


def select_program(current_program):
	global program_objects, enable_loops, debug
	if current_program is None:
		source = (0, 0)
	else:
		source = current_program.pos
	selected_program = None
	selected_cost = None
	for program in program_objects:
		dest = program.pos
		program_cost = cost(source, dest, program.complexity, program.return_var, program.visit_count)
		if program_cost == float("inf") or program_cost == float("nan"):
			return None
		if program == current_program:
			continue
		if not enable_loops:
			if program.visit_count > 0:
				continue
		if selected_program is None:
			selected_program = program
			selected_cost = program_cost
			continue
		if program_cost < selected_cost:
			selected_program = program
			selected_cost = program_cost
	if debug == 1:
		print(selected_program.__class__.__name__, "selected")
	if selected_program is not None:
		selected_program.visit_count += 1
	return selected_program


def distance(source, dest):
	return math.sqrt((dest[0] - source[0]) ** 2 + (dest[1] - source[1]) ** 2)


def cost(source, dest, complexity, return_var, visit_count):
	global max_complexity, max_distance, cue_system, enable_loops, revisit_penalty
	dist = distance(source, dest)
	normalized_distance = dist / max_distance
	normalized_complexity = complexity / max_complexity
	if cue_system == "programmatical":
		return_val = eval(return_var)
	elif cue_system == "temporospatial":
		return_val = 0
	else:
		raise "Unknown Cue System"
	cost_value = normalized_complexity + normalized_distance + return_val
	if enable_loops:
		cost_value += (cost_value + 1) * visit_count * revisit_penalty
	return abs(cost_value)


def reset():
	global c0, c1, c2, c3, c4, c5, c6, c7, c8, a0, a1, a2, a3, a4, a5, a6, a7, a8
	for program in program_objects:
		program.visit_count = 0
	a0 = 0
	a1 = 0
	a2 = 0
	a3 = 0
	a4 = 0
	a5 = 0
	a6 = 0
	a7 = 0
	a8 = 0


program_output = None


def run():
	reset()
	global c0, c1, c2, c3, c4, c5, c6, c7, c8, a0, a1, a2, a3, a4, a5, a6, a7, a8, program_output
	# c0 = float(input('Enter c0:'))
	# c1 = float(input('Enter c1:'))
	# c2 = float(input('Enter c2:'))
	# c3 = float(input('Enter c3:'))
	# c4 = float(input('Enter c4:'))
	# c5 = float(input('Enter c5:'))
	# c6 = float(input('Enter c6:'))
	# c7 = float(input('Enter c7:'))
	# c8 = float(input('Enter c8:'))
	current_p = None
	program_output = None
	while True:
		current_p = select_program(current_p)
		if current_p is None:
			break
		function_name = current_p.__class__.__name__.lower()
		program_output = eval("current_p.{}()".format(function_name))
		if current_p.type == "O":
			break
	print('Output:', eval(program_output))

#
# run()
