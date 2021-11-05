# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	
	def __init__(self, recommend = True):
		self.recommend = recommend
		
	def initialize_game(self):
		while(True):
			self.n = int(input('Enter the size n of the board in [3..10]: '))
			if(self.n < 3 or self.n > 10):
				print("Invalid size for the board!")
			else: break

		self.current_state = [['.']*self.n for i in range(self.n)]

		while(True):	
			self.b = int(input(F'Enter the number of blocs b on the board in [0..{2 * self.n}]: '))
			if(self.b < 0 or self.b > 2 * self.n):
				print("Invalid number of blocs!")
			else: break
		
		blocs_positions = []
		blocs_count = 0
		print("Enter the coordinates of the blocs:")
		while(blocs_count < self.b):
			print(F"Bloc {blocs_count + 1}:")
			x = int(input('enter the x coordinate: '))
			y = int(input('enter the y coordinate: '))
			if(self.is_valid(x, y)):
				blocs_positions.append((x,y))
				blocs_count += 1
				self.current_state[x][y] = 'B'
			else:
				print('The position is not valid! Try again.')

		while(True):
			self.s = int(input(F'Enter the winning line-up size s in [3..{self.n}]: '))
			if(self.s < 3 or self.s > self.n):
				print("Invalid winning line-up size!")
			else: break

		while(True):
			print('Enter the maximum depth of the adversarial search for both players in [0..]:')
			self.d1 = int(input('for player 1: '))
			self.d2 = int(input('for player 2: '))
			if(self.d1 < 0 or self.d2 < 0):
				print("One of the maximum depths is invalid! Please try again.")
			else: break

		while(True):
			self.t = int(input('Enter maximum allowed time (in seconds) for the adversarial search in [0..]: '))
			if(self.t < 0):
				print("Invalid time!")
			else: break

		while(True):
			use_alphabeta = input("Enter the desired adversarial search algorithm ('true' = alphabeta, 'false' = minimax) ")
			if(use_alphabeta == 'true'):
				self.use_alphabeta = True
				break
			elif(use_alphabeta == 'false'):
				self.use_alphabeta = False
				break
			else:
				print("Invalid input!")

		while(True):
			print("Enter the desired play mode for each player (H = human, AI = artificial intelligence)")
			mode_1 = input("for player 1: ")
			mode_2 = input("for player 2: ")
			if(mode_1 != 'H' and mode_1 != 'AI' or mode_2 != 'H' and mode_2 != 'AI'):
				print("One of the players has an invalid play mode! Please try again!")
			else:
				self.play_mode = mode_1 + "-" + mode_2 
				break

		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self):
		print()
		for y in range(self.n):
			for x in range(self.n):
				print(F'{self.current_state[x][y]}', end="")
			print()
		print()
		
	def is_valid(self, x, y):
		if x < 0 or x > self.n - 1 or y < 0 or y > self.n - 1:
			return False
		elif self.current_state[x][y] != '.':
			return False
		else:
			return True

	def e1(self):
		max_o_counter = 0
		o_freq_counter = 0
		max_x_counter = 0
		x_freq_counter = 0

		# Horizontal score for O
		for i in range(self.n):			
			for j in range(self.n):
				if j + self.s > self.n: break
				o_counter = 0
				for k in range(j, j + self.s):
					cell = self.current_state[i][k]
					if cell == 'B' or cell == 'X':
						o_counter = 0
						break
					elif cell == 'O':
						o_counter += 1
				if o_counter > max_o_counter:
					max_o_counter = o_counter
					o_freq_counter = 1
				elif o_counter == max_o_counter:
					o_freq_counter += 1

		# Vertical score for O
		for i in range(self.n):			
			for j in range(self.n):
				if j + self.s > self.n: break
				o_counter = 0
				for k in range(j, j + self.s):
					cell = self.current_state[k][i]
					if cell == 'B' or cell == 'X':
						o_counter = 0
						break
					elif cell == 'O':
						o_counter += 1
				if o_counter > max_o_counter:
					max_o_counter = o_counter
					o_freq_counter = 1
				elif o_counter == max_o_counter:
					o_freq_counter += 1

		# Diagonal (\) score for O
		for i in range(self.n):
			if i + self.s > self.n: break		
			for j in range(self.n):
				if j + self.s > self.n: break
				o_counter = 0
				for k in range(self.s):
					cell = self.current_state[i+k][j+k]
					if cell == 'B' or cell == 'X':
						o_counter = 0
						break
					elif cell == 'O':
						o_counter += 1
				if o_counter > max_o_counter:
					max_o_counter = o_counter
					o_freq_counter = 1
				elif o_counter == max_o_counter:
					o_freq_counter += 1

		# Diagonal (/) score for O
		for i in range(self.n):
			if i + self.s > self.n: break		
			for j in range(self.n):
				if j - (self.s - 1) < 0: break
				o_counter = 0
				for k in range(self.s):
					cell = self.current_state[i+k][j-k]
					if cell == 'B' or cell == 'X':
						o_counter = 0
						break
					elif cell == 'O':
						o_counter += 1
				if o_counter > max_o_counter:
					max_o_counter = o_counter
					o_freq_counter = 1
				elif o_counter == max_o_counter:
					o_freq_counter += 1

		# Horizontal score for X
		for i in range(self.n):			
			for j in range(self.n):
				if j + self.s > self.n: break
				x_counter = 0
				for k in range(j, j + self.s):
					cell = self.current_state[i][k]
					if cell == 'B' or cell == 'O':
						x_counter = 0
						break
					elif cell == 'X':
						x_counter += 1
				if x_counter > max_x_counter:
					max_x_counter = x_counter
					x_freq_counter = 1
				elif x_counter == max_x_counter:
					x_freq_counter += 1

		# Vertical score for X
		for i in range(self.n):			
			for j in range(self.n):
				if j + self.s > self.n: break
				x_counter = 0
				for k in range(j, j + self.s):
					cell = self.current_state[k][i]
					if cell == 'B' or cell == 'O':
						x_counter = 0
						break
					elif cell == 'X':
						x_counter += 1
				if x_counter > max_x_counter:
					max_x_counter = x_counter
					x_freq_counter = 1
				elif x_counter == max_x_counter:
					x_freq_counter += 1

		# Diagonal (\) score for X
		for i in range(self.n):
			if i + self.s > self.n: break		
			for j in range(self.n):
				if j + self.s > self.n: break
				o_counter = 0
				for k in range(self.s):
					cell = self.current_state[i+k][j+k]
					if cell == 'B' or cell == 'O':
						o_counter = 0
						break
					elif cell == 'X':
						o_counter += 1
				if o_counter > max_o_counter:
					max_o_counter = o_counter
					o_freq_counter = 1
				elif o_counter == max_o_counter:
					o_freq_counter += 1

		# Diagonal (/) score for X
		for i in range(self.n):
			if i + self.s > self.n: break		
			for j in range(self.n):
				if j - (self.s - 1) < 0: break
				o_counter = 0
				for k in range(self.s):
					cell = self.current_state[i+k][j-k]
					if cell == 'B' or cell == 'O':
						o_counter = 0
						break
					elif cell == 'X':
						o_counter += 1
				if o_counter > max_o_counter:
					max_o_counter = o_counter
					o_freq_counter = 1
				elif o_counter == max_o_counter:
					o_freq_counter += 1

		heuristic_value = max_o_counter - max_x_counter
		if heuristic_value == 0:
			heuristic_value = o_freq_counter - x_freq_counter

		return heuristic_value

	def is_end(self):
		# Horizontal win
		for i in range(self.n):			
			for j in range(self.n):
				if j + self.s > self.n: break
				symbol = self.current_state[i][j]
				if symbol == '.' or symbol == 'B': continue
				symbol_counter = 0
				for k in range(j, j + self.s):
					cell = self.current_state[i][k]
					if cell == symbol:
						symbol_counter += 1
				if symbol_counter == self.s: 
					return symbol

		# Vertical win
		for i in range(self.n):			
			for j in range(self.n):
				if j + self.s > self.n: break
				symbol = self.current_state[j][i]
				if symbol == '.' or symbol == 'B': continue
				symbol_counter = 0
				for k in range(j, j + self.s):
					cell = self.current_state[k][i]
					if cell == symbol:
						symbol_counter += 1
				if symbol_counter == self.s: 
					return symbol

		# Diagonal (\) win
		for i in range(self.n):
			if i + self.s > self.n: break		
			for j in range(self.n):
				if j + self.s > self.n: break
				symbol = self.current_state[i][j]
				if symbol == '.' or symbol == 'B': continue
				symbol_counter = 0
				for k in range(self.s):
					cell = self.current_state[i+k][j+k]
					if cell == symbol:
						symbol_counter += 1
				if symbol_counter == self.s: 
					return symbol

		# Diagonal (/) win
		for i in range(self.n):
			if i + self.s > self.n: break		
			for j in range(self.n):
				if j - (self.s - 1) < 0: break
				symbol = self.current_state[i][j]
				if symbol == '.' or symbol == 'B': continue
				symbol_counter = 0
				for k in range(self.s):
					cell = self.current_state[i+k][j-k]
					if cell == symbol:
						symbol_counter += 1
				if symbol_counter == self.s: 
					return symbol

		# Board not full
		for i in range(self.n):
			for j in range(self.n):
				if (self.current_state[i][j] == '.'):
					return None

		# Tie
		return '.'

	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			self.initialize_game()
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def minimax(self, remainingDepth, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 999 or -999 as worse than the worst case:
		value = 999
		if max:
			value = -999
		x = None
		y = None

		if remainingDepth <= 0:
			return (self.e1(), x, y)

		for i in range(self.n):
			for j in range(self.n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def play(self,algo=None,player_x=None,player_o=None):
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
				else:
					(_, x, y) = self.minimax(max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.current_state[x][y] = self.player_turn
			self.switch_player()

def main():
	g = Game(recommend=True)
	g.initialize_game()
	g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)
	g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)

if __name__ == "__main__":
	main()

