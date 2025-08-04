from enum import Enum
import math
from collections import deque

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

def bfs(current_config, goal_config, hash_row, hash_col):
    frontier = deque()
    visited = set()

    frontier.append(GameSnapshot(hash_row, hash_col, 0, current_config))
    visited.add(tuple(map(tuple, current_config)))

    while frontier:
        current = frontier.popleft()
        #visualize_board(current.board)

        if check_solved(current.board, goal_config): 
            print(current.moves)
            return current
        
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
            


initial_state = input()
goal_state = input()

# map string of init config & goal config to boards
current_board_configuration = [[0, 0, 0], [0, 0, 0], [0, 0,0]]
goal_board_configuration = [[0, 0, 0], [0, 0, 0], [0, 0,0]]
string_to_board(current_board_configuration, initial_state)
string_to_board(goal_board_configuration, goal_state)

# get hash row and col from pos in string
hash_position = initial_state.find("#")
hash_pos_row = math.floor(hash_position / 3)
hash_pos_col = hash_position % 3

bfs(current_board_configuration, goal_board_configuration, hash_pos_row, hash_pos_col)





    