from enum import Enum
import math
from collections import deque
import random
import time
import matplotlib.pyplot as plt
import statistics
import numpy as np

class Move(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class GameSnapshot:
    def __init__(self, row, col, moves, board):
        self.row = row
        self.col = col
        self.moves = moves # depth of the tree
        self.board = board

def string_to_board(board, board_input):
    iterator = 0
    for row in range(3):
        for col in range(3):
            board[row][col] = board_input[iterator]
            iterator+= 1

def implement_move(board, move, row ,col):
    new_row, new_col = move.value
    switch_positions(board, row, col, row + new_row, col + new_col)

def switch_positions(board, row1, col1, row2, col2):
    board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]

def visualize_board(board):
    for i in range(3):
        for j in range(3):
            print(board[i][j] + " ", end="")
        print()

def available_moves(row, col):
    avail_moves = []
     
    if row != 0: avail_moves.append("UP")
    if row != 2: avail_moves.append("DOWN")
    if col != 0: avail_moves.append("LEFT")
    if col != 2: avail_moves.append("RIGHT")
    return avail_moves

def check_solved(current_config, goal_config):
    return current_config == goal_config

def game_solver(current_config, goal_config, hash_row, hash_col):
    frontier = deque()
    visited = set()

    frontier.append(GameSnapshot(hash_row, hash_col, 0, current_config))
    visited.add(tuple(map(tuple, current_config)))

    expanded_nodes = 0
    while frontier:
        current = frontier.popleft()
        expanded_nodes += 1 # for space complexity

        #visualize_board(current.board)
        #print()
        if check_solved(current.board, goal_config): 
            print(current.moves) 
            return current, expanded_nodes
        
        # Choose only valid moves to explore
        available = available_moves(current.row, current.col)
        for i in range(len(available)):
            new_row, new_col = Move[available[i]].value
            new_row += current.row
            new_col += current.col

            next_config = [row[:] for row in current.board]
            switch_positions(next_config, current.row, current.col, new_row, new_col)
            if tuple(map(tuple, next_config)) not in visited:
                visited.add(tuple(map(tuple, next_config)))
                frontier.append(GameSnapshot(new_row, new_col, current.moves + 1, next_config))

    print("No solution found")

# This does not guarantee k steps
def reverse_random_solution(goal_state, k_moves, hash_row, hash_col):
    prev_move = None

    visited = set()
    visited.add(tuple(map(tuple, goal_state)))
    current = GameSnapshot(hash_row, hash_col, 0, [row[:] for row in goal_state])
    move_counter = 0

    while move_counter < k_moves:
        available = available_moves(current.row, current.col)
        random_choice = random.randint(0, len(available) - 1)
        
        # ensure unique choice every time
        while(available[random_choice] == prev_move):
            random_choice = random.randint(0, len(available)- 1)
        
        new_row, new_col = Move[available[random_choice]].value
        new_row += current.row
        new_col += current.col

        next_config = [row[:] for row in current.board]
        switch_positions(next_config, current.row, current.col, new_row, new_col)
        if tuple(map(tuple, next_config)) not in visited:
            visited.add(tuple(map(tuple, next_config)))
            current = GameSnapshot(new_row, new_col, current.moves + 1 ,next_config)
            prev_move = available[random_choice]
            move_counter += 1
    return current

def reverse_solution(goal_state, k_moves, hash_row, hash_col):
    frontier = deque()
    visited = set()

    frontier.append(GameSnapshot(hash_row, hash_col, 0, goal_state))
    visited.add(tuple(map(tuple, goal_state)))

    while frontier:
        current = frontier.popleft()

        if (k_moves == current.moves):
            return current  
        
        available = available_moves(current.row, current.col)
        for i in range(len(available)):
            new_row, new_col = Move[available[i]].value
            new_row += current.row
            new_col += current.col

            next_config = [row[:] for row in current.board]
            switch_positions(next_config, current.row, current.col, new_row, new_col)
            if tuple(map(tuple, next_config)) not in visited:
                visited.add(tuple(map(tuple, next_config)))
                frontier.append(GameSnapshot(new_row, new_col, current.moves + 1, next_config))
    
    print("Could not reverse the solution")
    return None

# map string of init config & goal config to boards
goal_string = "12345678#"

goal_board_configuration = [[0, 0, 0], [0, 0, 0], [0, 0,0]]
string_to_board(goal_board_configuration, goal_string)

# get hash row and col from pos in string
hash_position = goal_string.find("#")
hash_pos_row = math.floor(hash_position / 3)
hash_pos_col = hash_position % 3

# reverse the solution
#k = 31
#reversed_solution = reverse_solution(goal_board_configuration, k, hash_pos_row, hash_pos_col)
#print(reversed_solution.board)    

# solve the board to prove its done in k moves
#game_solver(reversed_solution.board, goal_board_configuration, reversed_solution.row, reversed_solution.col)



# =====Time Complexity Experimentation=====

print()
print("Running 5 times on different values of k....")

k = 31
timings_storage = np.zeros((k, 5))
timings_average = np.zeros(k)
timing_deviations = np.zeros(k)
spaces = []
for i in range(k):
    print()
    print("Running on k = " + str(i)+":")

    # repeating 5 times for an average
    for j in range(5):
        # reverse solution to k steps
        reversed_solution = reverse_solution(goal_board_configuration, i, hash_pos_row, hash_pos_col)

        # Timing the bfs 
        start_time = time.perf_counter()
        solution, expanded_nodes = game_solver(reversed_solution.board, goal_board_configuration, reversed_solution.row, reversed_solution.col)
        end_time = time.perf_counter()

        print(end_time - start_time)
        timings_storage[i][j] = end_time - start_time
        spaces.append(expanded_nodes)

    timings_average[i] = statistics.mean(timings_storage[i]) #sum(timings_storage[i])/5
    timing_deviations[i] = 2 * statistics.stdev(timings_storage[i])
    spaces[i] /= 5
    print(f"Average elapsed time: {timings_average[i]:.6f} seconds")
    print(f"Expanded nodes: {spaces[i]}")
    print(timings_storage)
