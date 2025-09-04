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

def switch_positions(board, row1, col1, row2, col2):
    board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]

def available_moves(row, col):
    moves = []
    if row != 0: moves.append("UP")
    if row != 2: moves.append("DOWN")
    if col != 0: moves.append("LEFT")
    if col != 2: moves.append("RIGHT")
    return moves

def check_solved(current_config, goal_config):
    return current_config == goal_config

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
            if symbol == '#': continue
            goal_row, goal_col = goal_cell_positions[symbol]
            distance += abs(i - goal_row) + abs(j - goal_col)
    return distance

def game_solver_gbfs_tuple(current_config, goal_config, hash_row, hash_col):
    frontier = PriorityQueue()
    visited = set()
    goal_cell_positions = create_dict(goal_config)

    initial_snapshot = GameSnapshot(hash_row, hash_col, 0, current_config)
    state_tuple = tuple(tuple(row) for row in current_config)
    visited.add(state_tuple)

    # Tie-breaker using board tuple
    frontier.put((manhattan_distance_heuristic(current_config, goal_cell_positions), state_tuple, initial_snapshot))

    while not frontier.empty():
        _, _, current = frontier.get()
        state_tuple = tuple(tuple(row) for row in current.board)

        if check_solved(current.board, goal_config):
            print(current.moves)
            return current

        for move in available_moves(current.row, current.col):
            dr, dc = Move[move].value
            next_row, next_col = current.row + dr, current.col + dc
            next_board = [row[:] for row in current.board]
            switch_positions(next_board, current.row, current.col, next_row, next_col)
            next_state_tuple = tuple(tuple(row) for row in next_board)

            if next_state_tuple not in visited:
                visited.add(next_state_tuple)
                snapshot = GameSnapshot(next_row, next_col, current.moves + 1, next_board)
                h = manhattan_distance_heuristic(next_board, goal_cell_positions)
                frontier.put((h, next_state_tuple, snapshot))

    print("No solution found")
    return None

# Example usage
initial_state = input().strip()
goal_state = input().strip()
current_board = [['' for _ in range(3)] for _ in range(3)]
goal_board = [['' for _ in range(3)] for _ in range(3)]
string_to_board(current_board, initial_state)
string_to_board(goal_board, goal_state)

hash_pos = initial_state.find("#")
game_solver_gbfs_tuple(current_board, goal_board, hash_pos // 3, hash_pos % 3)
