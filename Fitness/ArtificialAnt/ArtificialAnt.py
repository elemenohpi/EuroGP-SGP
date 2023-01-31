import copy
from os import listdir
from os.path import isfile, join


class AntSimulator:
	direction = ["north", "east", "south", "west"]
	dir_row = [1, 0, -1, 0]
	dir_col = [0, 1, 0, -1]

	def __init__(self, max_moves):
		self.matrix_exc = None
		self.matrix_col = None
		self.matrix_row = None
		self.col_start = None
		self.row_start = None
		self.matrix = None
		self.col = None
		self.row = None
		self.dir = None
		self.max_moves = max_moves
		self.moves = 0
		self.eaten = 0
		self.routine = None
		# mypath = "."
		# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

		with open("santafe_trail.txt") as trail_file:
			self.parse_matrix(trail_file)
		self._reset()

	def _reset(self):
		self.row = self.row_start
		self.col = self.col_start
		self.dir = 1
		self.moves = 0
		self.eaten = 0
		self.matrix_exc = copy.deepcopy(self.matrix)

	@property
	def position(self):
		return self.row, self.col, self.direction[self.dir]

	def turn_left(self):
		if self.moves < self.max_moves:
			self.moves += 1
			self.dir = (self.dir - 1) % 4

	def turn_right(self):
		if self.moves < self.max_moves:
			self.moves += 1
			self.dir = (self.dir + 1) % 4

	def move_forward(self):
		if self.moves < self.max_moves:
			self.moves += 1
			self.row = (self.row + self.dir_row[self.dir]) % self.matrix_row
			self.col = (self.col + self.dir_col[self.dir]) % self.matrix_col
			if self.matrix_exc[self.row][self.col] == "food":
				self.eaten += 1
			self.matrix_exc[self.row][self.col] = "passed"

	def sense_food(self):
		ahead_row = (self.row + self.dir_row[self.dir]) % self.matrix_row
		ahead_col = (self.col + self.dir_col[self.dir]) % self.matrix_col
		return self.matrix_exc[ahead_row][ahead_col] == "food"

	# def if_food_ahead(self, out1, out2):
	# 	return partial(if_then_else, self.sense_food, out1, out2)

	def run(self, routine):
		self._reset()
		while self.moves < self.max_moves:
			routine()

	def parse_matrix(self, matrix):
		fds = 0
		self.matrix = list()
		for i, line in enumerate(matrix):
			self.matrix.append(list())
			for j, col in enumerate(line):
				if col == "#":
					self.matrix[-1].append("food")
					fds+=1
				elif col == ".":
					self.matrix[-1].append("empty")
				elif col == "S":
					self.matrix[-1].append("empty")
					self.row_start = self.row = i
					self.col_start = self.col = j
					self.dir = 1
		self.matrix_row = len(self.matrix)
		self.matrix_col = len(self.matrix[0])
		self.matrix_exc = copy.deepcopy(self.matrix)
