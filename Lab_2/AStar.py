from enum import Enum
from queue import PriorityQueue
import math
from itertools import count

class Move(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class GameSnapshot:
    def __init__(self, row, col, moves, board):
        self.row = row              # position of blank
        self.col = col
        self.moves = moves          # g(n): depth (cost so far)
        self.board = board          # current board config

def string_to_board(board, board_input):
    iterator = 0
    for i in range(3):
        for j in range(3):
            board[i][j] = board_input[iterator]
            iterator += 1

def switch_positions(board, row1, col1, row2, col2):
    board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]

def available_moves(row, col):
    avail_moves = []
    if row != 0: avail_moves.append("UP")
    if row != 2: avail_moves.append("DOWN")
    if col != 0: avail_moves.append("LEFT")
    if col != 2: avail_moves.append("RIGHT")
    return avail_moves

def manhattan_distance(board, goal_board):
    """Heuristic: Manhattan distance between all tiles."""
    dist = 0
    for i in range(3):
        for j in range(3):
            val = board[i][j]
            if val == "#": 
                continue
            # find val in goal board
            for gi in range(3):
                for gj in range(3):
                    if goal_board[gi][gj] == val:
                        dist += abs(i - gi) + abs(j - gj)
                        break
    return dist

def check_solved(current_config, goal_config):
    return current_config == goal_config

def game_solver_astar_solution(current_config, goal_config, hash_row, hash_col):
    frontier = PriorityQueue()
    visited = set()
    counter = count()  # unique increasing numbers

    start_snapshot = GameSnapshot(hash_row, hash_col, 0, current_config)
    h = manhattan_distance(current_config, goal_config)
    frontier.put((h, 0, next(counter), start_snapshot))  # (f, g, counter, state)

    counter_nodes = 0
    while not frontier.empty():
        f, g, _, current = frontier.get()
        state = tuple(map(tuple, current.board))

        if check_solved(current.board, goal_config):
            print(g)
            return

        if state in visited:
            continue
        visited.add(state)

        for move_name in available_moves(current.row, current.col):
            new_row, new_col = Move[move_name].value
            new_row += current.row
            new_col += current.col

            counter_nodes += 1
            print(counter_nodes)
            next_config = [row[:] for row in current.board]
            switch_positions(next_config, current.row, current.col, new_row, new_col)

            g_new = g + 1
            h_new = manhattan_distance(next_config, goal_config)
            frontier.put((g_new + h_new, g_new, next(counter), GameSnapshot(new_row, new_col, g_new, next_config)))

    print("No solution found")

initial_state = input().strip()
goal_state = input().strip()

current_board_configuration = [[0, 0, 0], [0, 0, 0], [0, 0,0]]
goal_board_configuration = [[0, 0, 0], [0, 0, 0], [0, 0,0]]
string_to_board(current_board_configuration, initial_state)
string_to_board(goal_board_configuration, goal_state)

hash_position = initial_state.find("#")
hash_pos_row = math.floor(hash_position / 3)
hash_pos_col = hash_position % 3

game_solver_astar_solution(current_board_configuration, goal_board_configuration, hash_pos_row, hash_pos_col)
