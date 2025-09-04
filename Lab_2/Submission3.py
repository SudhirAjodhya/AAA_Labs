from enum import Enum
import math
from queue import PriorityQueue

class Move(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class GameSnapshot:
    def __init__(self, row, col, moves, board):
        self.row = row
        self.col = col
        self.moves = moves # depth of tree
        self.board = board

def string_to_board(board, board_input):
    iterator = 0
    for i in range(3):
        for j in range(3):
            board[i][j] = board_input[iterator]
            iterator += 1

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

# symbol: (row, col)
def create_dict_of_symbols(goal_config):
    symbol_map = {}
    for i in range(3):
        for j in range(3):
            symbol = goal_config[i][j]

            if symbol != '#':
                symbol_map[symbol] = (i, j)
    return symbol_map

def manhattan_formula(row1, col1, row2, col2):
    return abs(row1 - row2) + abs(col1 - col2)

def manhattan_heuristic(board, goal_cells):
    distance = 0

    for i in range(3):
        for j in range(3):

            symbol = board[i][j]
            if symbol == '#': continue

            goal_row, goal_col = goal_cells[symbol]
            distance += manhattan_formula(i, j, goal_row, goal_col)
    return distance


def game_solver_AStar(current_config, goal_config, hash_row, hash_col):
    frontier = PriorityQueue()
    visited = {}

    goal_cells = create_dict_of_symbols(goal_config)
    initial = GameSnapshot(hash_row, hash_col, 0, current_config)
    heuristic = manhattan_heuristic(current_config, goal_cells)
    states = tuple(tuple(row) for row in current_config)

    f_cost = initial.moves + heuristic
    frontier.put((f_cost, states, initial))
    visited[states] = 0

    expanded_nodes = 0
    while not frontier.empty():
        _, _, current = frontier.get()
        states = tuple(tuple(row) for row in current.board)
        expanded_nodes += 1

        if check_solved(current.board, goal_config):
            print(current.moves)
            return current, expanded_nodes
        
        available = available_moves(current.row, current.col)
        for i in range(len(available)):
            new_row, new_col = Move[available[i]].value
            new_row += current.row
            new_col += current.col

            next_config = [row[:] for row in current.board]
            switch_positions(next_config, current.row, current.col, new_row, new_col)
            next_state = tuple(tuple(row) for row in next_config)

            g_cost = current.moves + 1
            if next_state not in visited or g_cost < visited[next_state]:
                visited[next_state] = g_cost
                h_cost = manhattan_heuristic(next_config, goal_cells)
                f_cost = h_cost + g_cost
                frontier.put((f_cost, next_state, GameSnapshot(new_row, new_col, g_cost, next_config)))

    print("No Solution found")
    return None


initial_state = input()
goal_state = input()

current_board_configuration = [['', '', ''], ['', '', ''], ['', '', '']]
goal_board_configuration = [['', '', ''], ['', '', ''], ['', '', '']]
string_to_board(current_board_configuration, initial_state)
string_to_board(goal_board_configuration, goal_state)

# get hash row and col from pos in string
hash_position = initial_state.find("#")
hash_pos_row = math.floor(hash_position / 3)
hash_pos_col = hash_position % 3

solution, expanded_nodes = game_solver_AStar(current_board_configuration, goal_board_configuration, hash_pos_row, hash_pos_col)
#print(expanded_nodes)