# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    e1_nodelist = []
    e2_nodelist = []
    e1_node_depths = {}
    e2_node_depths = {}
    e1_total_node_depths = {}
    e2_total_node_depths = {}
    e1_total_states_evaluated = 0
    e2_total_states_evaluated = 0
    e1_total_average_depth = 0
    e2_total_average_depth = 0
    e1_total_evaluation_time = 0
    e2_total_evaluation_time = 0
    e1_total_moves = 0
    e2_total_moves = 0

    def __init__(self, recommend=True):
        self.recommend = recommend

    def initialize_game(self):
        while (True):
            self.n = int(input('Enter the size n of the board in [3..10]: '))
            if (self.n < 3 or self.n > 10):
                print("Invalid size for the board!")
            else:
                break

        self.current_state = [['.'] * self.n for i in range(self.n)]

        while (True):
            self.b = int(input(F'Enter the number of blocs b on the board in [0..{2 * self.n}]: '))
            if (self.b < 0 or self.b > 2 * self.n):
                print("Invalid number of blocs!")
            else:
                break

        blocs_positions = []
        blocs_count = 0
        if blocs_count != 0:
            print("Enter the coordinates of the blocs:")
        while (blocs_count < self.b):
            print(F"Bloc {blocs_count + 1}:")
            x = int(input('enter the x coordinate: '))
            y = int(input('enter the y coordinate: '))
            if (self.is_valid(x, y)):
                blocs_positions.append((x, y))
                blocs_count += 1
                self.current_state[x][y] = 'B'
            else:
                print('The position is not valid! Try again.')
        self.blocs = blocs_positions

        while (True):
            self.s = int(input(F'Enter the winning line-up size s in [3..{self.n}]: '))
            if (self.s < 3 or self.s > self.n):
                print("Invalid winning line-up size!")
            else:
                break

        while (True):
            print('Enter the maximum depth of the adversarial search for both players in [0..]:')
            self.d1 = int(input('for player 1: '))
            self.d2 = int(input('for player 2: '))
            if (self.d1 < 0 or self.d2 < 0):
                print("One of the maximum depths is invalid! Please try again.")
            else:
                for i in range(0, self.d1):
                    self.e1_node_depths[i + 1] = 0
                    self.e1_total_node_depths[i + 1] = 0
                for i in range(0, self.d2):
                    self.e2_node_depths[i + 1] = 0
                    self.e2_total_node_depths[i + 1] = 0
                break

        while (True):
            self.t = int(input('Enter maximum allowed time (in seconds) for the adversarial search in [0..]: '))
            if (self.t < 0):
                print("Invalid time!")
            else:
                break

        while (True):
            use_alphabeta = input(
                "Enter the desired adversarial search algorithm ('true' = alphabeta, 'false' = minimax) ")
            if (use_alphabeta == 'true'):
                self.use_alphabeta = True
                break
            elif (use_alphabeta == 'false'):
                self.use_alphabeta = False
                break
            else:
                print("Invalid input!")

        while (True):
            print("Enter the desired play mode for each player (H = human, AI = artificial intelligence)")
            mode_1 = input("for player 1: ")
            mode_2 = input("for player 2: ")
            if (mode_1 != 'H' and mode_1 != 'AI' or mode_2 != 'H' and mode_2 != 'AI'):
                print("One of the players has an invalid play mode! Please try again!")
            else:
                self.play_mode = mode_1 + "-" + mode_2
                break
        self.p1 = mode_1
        self.p2 = mode_2

        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self, f):
        print()
        f.write("\n")
        for y in range(self.n):
            for x in range(self.n):
                print(F'{self.current_state[x][y]}', end="")
                f.write(F'{self.current_state[x][y]}')
            print()
            f.write("\n")
        print()
        f.write("\n")

    def is_valid(self, x, y):
        if x < 0 or x > self.n - 1 or y < 0 or y > self.n - 1:
            return False
        elif self.current_state[x][y] != '.':
            return False
        else:
            return True

    def is_valid_move(self, px, py):
        x = self.letter_to_int(px)
        y = py
        if x == None or y < 0 or y > self.n - 1:
            return False
        elif self.current_state[x][y] != '.':
            return False
        else:
            return True

    def letter_to_int(self, letter):
        if letter == 'A':
            return 0
        elif letter == 'B':
            return 1
        elif letter == 'C':
            return 2
        elif letter == 'D':
            return 3
        elif letter == 'E':
            return 4
        elif letter == 'F':
            return 5
        elif letter == 'G':
            return 6
        elif letter == 'H':
            return 7
        elif letter == 'I':
            return 8
        elif letter == 'J':
            return 9
        else:
            return None

    def int_to_letter(self, int):
        if int == 0: return 'A'
        if int == 1: return 'B'
        if int == 2: return 'C'
        if int == 3: return 'D'
        if int == 4: return 'E'
        if int == 5: return 'F'
        if int == 6: return 'G'
        if int == 7: return 'H'
        if int == 8: return 'I'
        if int == 9:
            return 'J'
        else:
            return None

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
                    cell = self.current_state[i + k][j + k]
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
                if j - (self.s - 1) < 0: continue
                o_counter = 0
                for k in range(self.s):
                    cell = self.current_state[i + k][j - k]
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
                x_counter = 0
                for k in range(self.s):
                    cell = self.current_state[i + k][j + k]
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

        # Diagonal (/) score for X
        for i in range(self.n):
            if i + self.s > self.n: break
            for j in range(self.n):
                if j - (self.s - 1) < 0: continue
                x_counter = 0
                for k in range(self.s):
                    cell = self.current_state[i + k][j - k]
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

        heuristic_value = max_o_counter - max_x_counter
        if heuristic_value == 0:
            heuristic_value = o_freq_counter - x_freq_counter

        return heuristic_value

    # Calculates the lines that can be formed for both X and O with the open tiles.
    def e2(self):
        heuristic = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    # Left and right move value
                    k = 1
                    consecutive_minus_x = 0
                    consecutive_minus_o = 0

                    while j - k >= 0:
                        if self.current_state[i][j - k] == 'X':
                            if consecutive_minus_o > 0:
                                break
                            consecutive_minus_x += 1
                        elif self.current_state[i][j - k] == 'O':
                            if consecutive_minus_x > 0:
                                break
                            consecutive_minus_o += 1
                        else:
                            break
                        k += 1

                    k = 1
                    consecutive_plus_x = 0
                    consecutive_plus_o = 0
                    while j + k < self.n:
                        if self.current_state[i][j + k] == 'X':
                            if consecutive_plus_o > 0:
                                break
                            consecutive_plus_x += 1
                        elif self.current_state[i][j + k] == 'O':
                            if consecutive_plus_x > 0:
                                break
                            consecutive_plus_o += 1
                        else:
                            break
                        k += 1

                    if consecutive_plus_o == 0 and consecutive_minus_o == 0:
                        move_value = -((consecutive_plus_x + consecutive_minus_x) ^ 2)
                    elif consecutive_plus_x == 0 and consecutive_minus_x == 0:
                        move_value = (consecutive_plus_o + consecutive_minus_o) ^ 2
                    else:
                        move_value = (consecutive_plus_o - consecutive_minus_x) ^ 2

                    heuristic += move_value

                    # Up and down move value
                    k = 1
                    consecutive_minus_x = 0
                    consecutive_minus_o = 0

                    while i - k >= 0:
                        if self.current_state[i - k][j] == 'X':
                            if consecutive_minus_o > 0:
                                break
                            consecutive_minus_x += 1
                        elif self.current_state[i - k][j] == 'O':
                            if consecutive_minus_x > 0:
                                break
                            consecutive_minus_o += 1
                        else:
                            break
                        k += 1

                    k = 1
                    consecutive_plus_x = 0
                    consecutive_plus_o = 0
                    while i + k < self.n:
                        if self.current_state[i + k][j] == 'X':
                            if consecutive_plus_o > 0:
                                break
                            consecutive_plus_x += 1
                        elif self.current_state[i + k][j] == 'O':
                            if consecutive_plus_x > 0:
                                break
                            consecutive_plus_o += 1
                        else:
                            break
                        k += 1

                    if consecutive_plus_o == 0 and consecutive_minus_o == 0:
                        move_value = -((consecutive_plus_x + consecutive_minus_x) ^ 2)
                    elif consecutive_plus_x == 0 and consecutive_minus_x == 0:
                        move_value = (consecutive_plus_o + consecutive_minus_o) ^ 2
                    else:
                        move_value = (consecutive_plus_o - consecutive_minus_x) ^ 2

                    heuristic += move_value

                    # \ Diagonal
                    k = 1
                    consecutive_minus_x = 0
                    consecutive_minus_o = 0

                    while i - k >= 0 and j - k >= 0:
                        if self.current_state[i - k][j - k] == 'X':
                            if consecutive_minus_o > 0:
                                break
                            consecutive_minus_x += 1
                        elif self.current_state[i - k][j - k] == 'O':
                            if consecutive_minus_x > 0:
                                break
                            consecutive_minus_o += 1
                        else:
                            break
                        k += 1

                    k = 1
                    consecutive_plus_x = 0
                    consecutive_plus_o = 0
                    while i + k < self.n and j + k < self.n:
                        if self.current_state[i + k][j + k] == 'X':
                            if consecutive_plus_o > 0:
                                break
                            consecutive_plus_x += 1
                        elif self.current_state[i + k][j + k] == 'O':
                            if consecutive_plus_x > 0:
                                break
                            consecutive_plus_o += 1
                        else:
                            break
                        k += 1

                    if consecutive_plus_o == 0 and consecutive_minus_o == 0:
                        move_value = -((consecutive_plus_x + consecutive_minus_x) ^ 2)
                    elif consecutive_plus_x == 0 and consecutive_minus_x == 0:
                        move_value = (consecutive_plus_o + consecutive_minus_o) ^ 2
                    else:
                        move_value = (consecutive_plus_o - consecutive_minus_x) ^ 2

                    heuristic += move_value

                    # / Diagonal
                    k = 1
                    consecutive_minus_x = 0
                    consecutive_minus_o = 0

                    while i - k >= 0 and j + k < self.n:
                        if self.current_state[i - k][j + k] == 'X':
                            if consecutive_minus_o > 0:
                                break
                            consecutive_minus_x += 1
                        elif self.current_state[i - k][j + k] == 'O':
                            if consecutive_minus_x > 0:
                                break
                            consecutive_minus_o += 1
                        else:
                            break
                        k += 1

                    k = 1
                    consecutive_plus_x = 0
                    consecutive_plus_o = 0
                    while i + k < self.n and j - k >= 0:
                        if self.current_state[i + k][j - k] == 'X':
                            if consecutive_plus_o > 0:
                                break
                            consecutive_plus_x += 1
                        elif self.current_state[i + k][j - k] == 'O':
                            if consecutive_plus_x > 0:
                                break
                            consecutive_plus_o += 1
                        else:
                            break
                        k += 1

                    if consecutive_plus_o == 0 and consecutive_minus_o == 0:
                        move_value = -((consecutive_plus_x + consecutive_minus_x) ^ 2)
                    elif consecutive_plus_x == 0 and consecutive_minus_x == 0:
                        move_value = (consecutive_plus_o + consecutive_minus_o) ^ 2
                    else:
                        move_value = (consecutive_plus_o - consecutive_minus_x) ^ 2

                    heuristic += move_value

        return -1 * heuristic

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
                    cell = self.current_state[i + k][j + k]
                    if cell == symbol:
                        symbol_counter += 1
                if symbol_counter == self.s:
                    return symbol

        # Diagonal (/) win
        for i in range(self.n):
            if i + self.s > self.n: break
            for j in range(self.n):
                if j - (self.s - 1) < 0: continue
                symbol = self.current_state[i][j]
                if symbol == '.' or symbol == 'B': continue
                symbol_counter = 0
                for k in range(self.s):
                    cell = self.current_state[i + k][j - k]
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

    def check_end(self, f):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
                f.write('The winner is X!\n\n')
            elif self.result == 'O':
                print('The winner is O!')
                f.write('The winner is O!\n\n')
            elif self.result == '.':
                print("It's a tie!")
                f.write("It's a tie!\n\n")

            print(F'''Heuristics -- e1:
            Average Evaluation Time Per State: {round(self.e1_total_evaluation_time / self.e1_total_states_evaluated, 10)}s
            Total States Evaluated: {self.e1_total_states_evaluated}
            Average of Per-Move Average Depth: {round(self.e1_total_average_depth / self.e1_total_moves, 10)}
            Total Evaluations at each Depth: {str(self.e1_total_node_depths)}
            Average of Per-Move Average Recursion Depth:
            Total Number of Moves:{self.e1_total_moves}''')

            f.write(F'''Heuristics -- e1:
            Average Evaluation Time Per State: {round(self.e1_total_evaluation_time / self.e1_total_states_evaluated, 10)}s
            Total States Evaluated: {self.e1_total_states_evaluated}
            Average of Per-Move Average Depth: {round(self.e1_total_average_depth / self.e1_total_moves, 10)}
            Total Evaluations at each Depth: {str(self.e1_total_node_depths)}
            Average of Per-Move Average Recursion Depth:
            Total Number of Moves:{self.e1_total_moves}\n\n''')

            print(F'''Heuristics -- e2:
            Average Evaluation Time Per State: {round(self.e2_total_evaluation_time / self.e2_total_states_evaluated, 10)}s
            Total States Evaluated: {self.e2_total_states_evaluated}
            Average of Per-Move Average Depth: {round(self.e2_total_average_depth / self.e2_total_moves, 10)}
            Total Evaluations at each Depth: {str(self.e2_total_node_depths)}
            Average of Per-Move Average Recursion Depth:
            Total Number of Moves:{self.e2_total_moves}''')

            f.write(F'''Heuristics -- e2:
            Average Evaluation Time Per State: {round(self.e2_total_evaluation_time / self.e2_total_states_evaluated, 10)}s
            Total States Evaluated: {self.e2_total_states_evaluated}
            Average of Per-Move Average Depth: {round(self.e2_total_average_depth / self.e2_total_moves, 10)}
            Total Evaluations at each Depth: {str(self.e2_total_node_depths)}
            Average of Per-Move Average Recursion Depth:
            Total Number of Moves:{self.e2_total_moves}\n\n''')

            # self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = input(
                'enter the x coordinate (as a capital letter between A and the nth letter of the english alphabet): ')
            py = int(input('enter the y coordinate in [0..n-1]: '))
            if self.is_valid_move(px, py):
                return (self.letter_to_int(px), py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    def minimax(self, remainingDepth, x, y, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        value = 999
        if max:
            value = -999

        if time.time() - self.start > 0.95 * self.t:
            if time.time() - self.start > 0.99 * self.t:
                return (0, x, y)
            else:
                if (self.player_turn == 'X'):
                    self.e1_nodelist.append(self.d1 - remainingDepth)
                    return (self.e1(), x, y)
                else:
                    self.e2_nodelist.append(self.d2 - remainingDepth)
                    return (self.e2(), x, y)

        result = self.is_end()
        if result == 'X':
            return (-500, x, y)
        elif result == 'O':
            return (500, x, y)
        elif result == '.':
            return (0, x, y)

        if remainingDepth <= 0:
            if (self.player_turn == 'X'):
                self.e1_nodelist.append(self.d1)
                return (self.e1(), x, y)
            else:
                self.e2_nodelist.append(self.d2)
                return (self.e2(), x, y)

        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(remainingDepth - 1, i, j, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(remainingDepth - 1, i, j, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    def alphabeta(self, remainingDepth, x, y, alpha=-999, beta=999, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -500 - win for 'X'
        # 0  - a tie
        # 500  - loss for 'X'
        # We're initially setting it to 999 or -999 as worse than the worst case:
        value = 999
        if max:
            value = -999

        if time.time() - self.start > 0.95 * self.t:
            if time.time() - self.start > 0.99 * self.t:
                return (0, x, y)
            else:
                if (self.player_turn == 'X'):
                    self.e1_nodelist.append(self.d1 - remainingDepth)
                    return (self.e1(), x, y)
                else:
                    self.e2_nodelist.append(self.d2 - remainingDepth)
                    return (self.e2(), x, y)

        result = self.is_end()
        if result == 'X':
            return (-500, x, y)
        elif result == 'O':
            return (500, x, y)
        elif result == '.':
            return (0, x, y)

        if remainingDepth <= 0:
            if (self.player_turn == 'X'):
                self.e1_nodelist.append(self.d1)
                return (self.e1(), x, y)
            else:
                self.e2_nodelist.append(self.d2)
                return (self.e2(), x, y)

        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(remainingDepth - 1, i, j, alpha=alpha, beta=beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(remainingDepth - 1, i, j, alpha=alpha, beta=beta, max=True)
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

    def play(self, f, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board(f)
            if self.check_end(f):
                return
            self.start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(self.d1, None, None, max=False)
                else:
                    (_, x, y) = self.minimax(self.d2, None, None, max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(self.d1, None, None, max=False)
                else:
                    (m, x, y) = self.alphabeta(self.d2, None, None, max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - self.start, 7)}s')
                    print(F'Recommended move: x = {self.int_to_letter(x)}, y = {y}')
                (x, y) = self.input_move()
                f.write(F'Player {self.player_turn} plays: {self.int_to_letter(x)}{y}')
            if (self.player_turn == 'X' and player_x == self.AI):
                self.e1_total_moves += 1
                print(F'Evaluation time: {round(end - self.start, 7)}s')
                self.e1_total_evaluation_time += end - self.start
                f.write(F'Player {self.player_turn} under AI control plays: {self.int_to_letter(x)}{y}\n\n')
                f.write(F'Evaluation time: {round(end - self.start, 7)}s\n')
                print(F'Heuristic evaluations: {str(len(self.e1_nodelist))}')
                f.write(F'Heuristic evaluations: {str(len(self.e1_nodelist))}')
                average_depth = 0
                for node in self.e1_nodelist:
                    self.e1_node_depths[node] += 1
                    average_depth += node
                print(F'Evaluations by depth: {self.e1_node_depths}')
                f.write(F'Evaluations by depth: {self.e1_node_depths}\n')
                if (len(self.e1_nodelist) != 0):
                    average_depth = average_depth / len(self.e1_nodelist)
                    print(F'Average evaluation depth: {round(average_depth, 7)}')
                    f.write(F'Average evaluation depth: {round(average_depth, 7)}\n')
                    self.e1_total_average_depth += average_depth
                else:
                    print(F'Average evaluation depth: NaN')
                    f.write(F'Average evaluation depth: NaN\n')
                f.write("Average recursion depth: " + "\n")
                print(F'Player {self.player_turn} under AI control plays: {self.int_to_letter(x)}{y}')
            elif (self.player_turn == 'O' and player_o == self.AI):
                self.e2_total_moves += 1
                print(F'Evaluation time: {round(end - self.start, 7)}s')
                self.e2_total_evaluation_time += end - self.start
                f.write(F'Player {self.player_turn} under AI control plays: {self.int_to_letter(x)}{y}\n\n')
                f.write(F'Evaluation time: {round(end - self.start, 7)}s\n')
                print(F'Heuristic evaluations: {str(len(self.e2_nodelist))}')
                f.write(F'Heuristic evaluations: {str(len(self.e2_nodelist))}\n')
                average_depth = 0
                for node in self.e2_nodelist:
                    self.e2_node_depths[node] += 1
                    average_depth += node
                print(F'Evaluations by depth: {self.e2_node_depths}')
                f.write(F'Evaluations by depth: {self.e2_node_depths}\n')
                if (len(self.e2_nodelist) != 0):
                    average_depth = average_depth / len(self.e2_nodelist)
                    print(F'Average evaluation depth: {round(average_depth, 7)}')
                    f.write(F'Average evaluation depth: {round(average_depth, 7)}\n')
                    self.e2_total_average_depth += average_depth
                else:
                    print(F'Average evaluation depth: NaN')
                    f.write(F'Average evaluation depth: NaN\n')
                f.write("Average recursion depth: " + "\n")
                print(F'Player {self.player_turn} under AI control plays: {self.int_to_letter(x)}{y}')
            self.e1_total_states_evaluated += len(self.e1_nodelist)
            self.e2_total_states_evaluated += len(self.e2_nodelist)
            self.e1_nodelist.clear()
            self.e2_nodelist.clear()
            for n in range(self.d1):
                self.e1_total_node_depths[n + 1] += self.e1_node_depths[n + 1]
                self.e1_node_depths[n + 1] = 0
            for n in range(self.d2):
                self.e2_total_node_depths[n + 1] += self.e2_node_depths[n + 1]
                self.e2_node_depths[n + 1] = 0

            self.current_state[x][y] = self.player_turn
            self.switch_player()


def main():
    g = Game(recommend=True)
    g.initialize_game()
    trace = "gameTrace-" + str(g.n) + str(g.b) + str(g.s) + str(g.t) + ".txt"
    f = open(trace, "w")
    f.write("n=" + str(g.n) + " b=" + str(g.b) + " s=" + str(g.s) + " t=" + str(g.t))
    f.write("\nBlocs: " + ' '.join(map(str, g.blocs)))
    f.write("\n\nPlayer 1: " + str(g.p1) + " d=" + str(g.d1) + " a=" + str(g.use_alphabeta))
    f.write("\nPlayer 2: " + str(g.p2) + " d=" + str(g.d2) + " a=" + str(g.use_alphabeta) + "\n\n")
    types = player_types_string_to_enum(g.play_mode)
    if (g.use_alphabeta):
        g.play(f, algo=Game.ALPHABETA,player_x=types[0], player_o=types[1])
    else:
        g.play(f, algo=Game.MINIMAX, player_x=types[0], player_o=types[1])
    f.close()


def player_types_string_to_enum(types_string):
    types = types_string.split("-")
    if types[0] == "H":
        types[0] = Game.HUMAN
    elif types[0] == "AI":
        types[0] = Game.AI

    if types[1] == "H":
        types[1] = Game.HUMAN
    elif types[1] == "AI":
        types[1] = Game.AI

    return types


if __name__ == "__main__":
    main()
