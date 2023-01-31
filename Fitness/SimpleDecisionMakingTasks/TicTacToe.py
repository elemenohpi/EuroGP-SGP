import random


class TicTacToe:
	finished = False
	state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
	ai_score = 0.0
	available_moves = list(range(0, 9))

	def __init__(self, multiplayer=False):
		self.reset()
		if multiplayer:
			self.turn = 1

	def play_multi(self, choice):
		row = int(choice / 3)
		column = choice % 3
		if self.state[row][column] == 0:
			self.state[row][column] = self.turn
			self.available_moves.remove(choice)
		else:
			self.finished = True
			print("Game over")
			return
		self.check_end_game()
		if not self.finished:
			if self.turn == 1:
				self.turn = 2
			elif self.turn == 2:
				self.turn = 1
		else:
			print("Game over")

	def is_finished(self):
		return self.finished

	def get_state(self):
		serialized_state = []
		for row in self.state:
			for cell in row:
				serialized_state.append(cell)
		return serialized_state

	def play_turn(self, output):
		row = int(output / 3)
		column = output % 3
		if self.state[row][column] == 0:
			self.state[row][column] = 1
			self.ai_score += 0.1
			self.available_moves.remove(output)
		else:
			self.finished = True
			return
		self.check_end_game()
		if not self.finished:
			self.play_random()

	def play_random(self):
		random_index = random.randint(0, len(self.available_moves)-1)
		row = int(self.available_moves[random_index] / 3)
		column = self.available_moves[random_index] % 3
		if self.state[row][column] != 0:
			raise "totally unexpected error"
		self.state[row][column] = 2
		self.available_moves.remove(self.available_moves[random_index])
		self.check_end_game()

	def check_end_game(self):
		if (self.state[0][0] == self.state[0][1] == self.state[0][2] == 1) or \
				(self.state[1][0] == self.state[1][1] == self.state[1][2] == 1) or \
				(self.state[2][0] == self.state[2][1] == self.state[2][2] == 1) or \
				(self.state[0][0] == self.state[1][0] == self.state[2][0] == 1) or \
				(self.state[0][1] == self.state[1][1] == self.state[2][1] == 1) or \
				(self.state[0][2] == self.state[1][2] == self.state[2][2] == 1) or \
				(self.state[0][0] == self.state[1][1] == self.state[2][2] == 1) or \
				(self.state[2][0] == self.state[1][1] == self.state[0][2] == 1):
			self.finished = True
			self.ai_score += 10
		elif (self.state[0][0] == self.state[0][1] == self.state[0][2] == 2) or \
				(self.state[1][0] == self.state[1][1] == self.state[1][2] == 2) or \
				(self.state[2][0] == self.state[2][1] == self.state[2][2] == 2) or \
				(self.state[0][0] == self.state[1][0] == self.state[2][0] == 2) or \
				(self.state[0][1] == self.state[1][1] == self.state[2][1] == 2) or \
				(self.state[0][2] == self.state[1][2] == self.state[2][2] == 2) or \
				(self.state[0][0] == self.state[1][1] == self.state[2][2] == 2) or \
				(self.state[2][0] == self.state[1][1] == self.state[0][2] == 2):
			self.finished = True
		elif len(self.available_moves) == 0:
			self.finished = True
			self.ai_score += 5

	def reset(self):
		self.finished = False
		self.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
		self.ai_score = 0.0
		self.available_moves = list(range(0, 9))

	def display(self):
		print()
		for row in self.state:
			for cell in row:
				print(cell, end=" ")
			print()
		print()
