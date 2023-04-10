# This code is a generated/synthesized QGP model/program
# ============================================ 

debug = 0

import math

# Input Definition
x0 = None
x1 = None
x2 = None
x3 = None
x4 = None
x5 = None
x6 = None
x7 = None
x8 = None
x9 = None
x10 = None
x11 = None

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
a9 = 0
a10 = 0
a11 = 0
a12 = 0


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



# returns true if a condition is met and false otherwise 
def op_if(a, condition, b):
	if eval('{} {} {}'.format(a, condition, b)):
		return True
	return False


# Individual Program Definitions
class P0:
	discrete_output = 'None'
	type = 'I'
	return_var = """if True:
		return a11
	else:
		return x11
	"""
	complexity = 4
	pos = (1, -9)
	visit_count = 0

	def p0(self):
		global x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12
		if x6 == x0:
			a2 = a3
		a9 = a2 * a8
		if True:
			return a11
		else:
			return x11
		


class P1:
	discrete_output = 'None'
	type = 'I'
	return_var = """if x0 <= 4:
		return x11
	else:
		return x6
	"""
	complexity = 6
	pos = (-5, 1)
	visit_count = 0

	def p1(self):
		global x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12
		a7 = a8
		a3 = a2
		a9 = x9
		a1 = op_div(x8, 6)
		a3 = x8 - x7
		if x0 <= 4:
			return x11
		else:
			return x6
		


class P2:
	discrete_output = 'None'
	type = 'I'
	return_var = """if x3 <= 6:
		return 3
	else:
		return x7
	"""
	complexity = 3
	pos = (-8, -3)
	visit_count = 0

	def p2(self):
		global x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12
		a11 = 6
		a7 = x11 + x10
		if x3 <= 6:
			return 3
		else:
			return x7
		


class P3:
	discrete_output = '0'
	type = 'O'
	return_var = """if a3 > 1:
		return a2
	else:
		return x3
	"""
	complexity = 4
	pos = (-8, 3)
	visit_count = 0

	def p3(self):
		global x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12
		a6 = x3 * 1
		a0 = a4 + x8
		a2 = a4 * x2
		if a3 > 1:
			return a2
		else:
			return x3
		


class P4:
	discrete_output = '1'
	type = 'O'
	return_var = """if x5 <= a1:
		return a0
	else:
		return 3
	"""
	complexity = 6
	pos = (-7, 3)
	visit_count = 0

	def p4(self):
		global x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12
		if 7 == a3:
			a1 = 3 - 7
		a3 = x7
		a2 = op_div(4, 4)
		if a7 < a5:
			pass
		if x5 <= a1:
			return a0
		else:
			return 3
		


class P5:
	discrete_output = '2'
	type = 'O'
	return_var = """if x7 < a3:
		return a12
	else:
		return x10
	"""
	complexity = 3
	pos = (-2, 8)
	visit_count = 0

	def p5(self):
		global x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12
		a7 = x5 * a9
		a4 = op_div(6, x10)
		if x7 < a3:
			return a12
		else:
			return x10
		


# SGP Interpreter
discrete_output = True
revisit_penalty = 0.1
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
program_objects.append(P5())


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


def distance_to_pos(source, dest):
	return math.sqrt((dest[0] - source[0]) ** 2 + (dest[1] - source[1]) ** 2)        


def cost(source, dest, complexity, return_var, visit_count):
	global max_complexity, max_distance, cue_system, enable_loops, revisit_penalty
	distance = distance_to_pos(source, dest)
	normalized_distance = distance / max_distance
	normalized_complexity = complexity / max_complexity
	if cue_system == "programmatical":
		try:
			return_val = eval(return_var)
		except SyntaxError:
			return_var = str(return_var)
			return_var = return_var.replace('\n\t', '\n')
			return_var = return_var.replace("\t\t", "\t")
			return_var = return_var.replace("return ", "program_output = ")
			exec_locals = {}
			exec(return_var, globals(), exec_locals)
			return_val = exec_locals['program_output']
	elif cue_system == "temporospatial":
		return_val = 0
	else:
		raise "Unknown Cue System"
	cost_value = math.log(1+distance) + math.log(1+abs(return_val))
	if enable_loops:
		cost_value += (cost_value + 1) * visit_count * revisit_penalty
	return abs(cost_value)


def reset():
	global x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12
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
	a9 = 0
	a10 = 0
	a11 = 0
	a12 = 0


program_output = None


def run():
	reset()
	global x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, program_output
	x0 = float(input('Enter x0:'))
	x1 = float(input('Enter x1:'))
	x2 = float(input('Enter x2:'))
	x3 = float(input('Enter x3:'))
	x4 = float(input('Enter x4:'))
	x5 = float(input('Enter x5:'))
	x6 = float(input('Enter x6:'))
	x7 = float(input('Enter x7:'))
	x8 = float(input('Enter x8:'))
	x9 = float(input('Enter x9:'))
	x10 = float(input('Enter x10:'))
	x11 = float(input('Enter x11:'))
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
	if discrete_output:
		print(current_p.discrete_output)
	else:
		print('Output:', eval(str(program_output)))


run()
