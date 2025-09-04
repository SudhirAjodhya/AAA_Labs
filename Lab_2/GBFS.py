from enum import Enum
from queue import PriorityQueue
import math

class Move(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class GameSnapshot:
    def __init__(self, row, col, moves, board):
        self.row = row
        self.col = col
        self.moves = moves
        self.board = board

def string_to_board(board, board_input):
    iterator = 0
    for i in range(3):
        for j in range(3):
            board[i][j] = board_input[iterator]
            iterator += 1

def board_to_string(board):
    """Convert 2D board to string representation"""
    return ''.join(''.join(row) for row in board)

def switch_positions(board, row1, col1, row2, col2):
    board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]

def available_moves(row, col):
    avail_moves = []
    if row != 0: avail_moves.append("UP")
    if row != 2: avail_moves.append("DOWN")
    if col != 0: avail_moves.append("LEFT")
    if col != 2: avail_moves.append("RIGHT")
    return avail_moves

def check_solved(current_config, goal_config):
    """Compare string representations of boards"""
    return board_to_string(current_config) == board_to_string(goal_config)

def manhattan_distance_formula(row1, col1, row2, col2):
    return abs(row1 - row2) + abs(col1 - col2)

def create_dict(goal_config):
    symbol_to_cell_pos = {}
    for i in range(3):
        for j in range(3):
            symbol = goal_config[i][j]
            if symbol != '#': 
                symbol_to_cell_pos[symbol] = (i, j)
    return symbol_to_cell_pos

def manhattan_distance_heuristic(board, goal_cell_positions):
    distance = 0
    for i in range(3):
        for j in range(3):
            symbol = board[i][j]
            if symbol == '#': 
                continue
            goal_row, goal_col = goal_cell_positions[symbol]
            distance += manhattan_distance_formula(i, j, goal_row, goal_col)
    return distance

def game_solver_gbfs(current_config, goal_config, hash_row, hash_col):
    frontier = PriorityQueue()
    visited = set()

    goal_cell_positions = create_dict(goal_config)
    heuristic = manhattan_distance_heuristic(current_config, goal_cell_positions)

    # Add initial state to visited immediately
    initial_state_str = board_to_string(current_config)
    visited.add(initial_state_str)
    
    # CORRECT ORDER: (heuristic, board_string, snapshot)
    # When heuristic ties, it will compare board strings, not move counts
    frontier.put((heuristic, initial_state_str, GameSnapshot(hash_row, hash_col, 0, current_config)))

    while not frontier.empty():
        _, _, current = frontier.get()

        if check_solved(current.board, goal_config):
            print(current.moves)
            return current

        available = available_moves(current.row, current.col)
        for move in available:
            new_row, new_col = Move[move].value
            next_row = current.row + new_row
            next_col = current.col + new_col

            next_config = [row[:] for row in current.board]
            switch_positions(next_config, current.row, current.col, next_row, next_col)

            next_state_str = board_to_string(next_config)
            
            if next_state_str not in visited:
                visited.add(next_state_str)
                h = manhattan_distance_heuristic(next_config, goal_cell_positions)
                # CORRECT ORDER: (heuristic, board_string, snapshot)
                frontier.put((h, next_state_str, GameSnapshot(next_row, next_col, current.moves + 1, next_config)))

    print("No solution found")
    return None

# Main execution
initial_state = input().strip()
goal_state = input().strip()

current_board_configuration = [['', '', ''], ['', '', ''], ['', '', '']]
goal_board_configuration = [['', '', ''], ['', '', ''], ['', '', '']]

string_to_board(current_board_configuration, initial_state)
string_to_board(goal_board_configuration, goal_state)

hash_position = initial_state.find("#")
hash_pos_row = hash_position // 3
hash_pos_col = hash_position % 3

game_solver_gbfs(current_board_configuration, goal_board_configuration, hash_pos_row, hash_pos_col)