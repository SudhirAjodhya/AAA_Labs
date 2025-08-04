from enum import Enum
import math

class Move(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

def string_to_board(board):
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

board_input = input()
move_input = input()

board = [[0, 0, 0], [0, 0, 0], [0, 0,0]]
string_to_board(board)

hash_position = board_input.find("#")
hash_pos_row = math.floor(hash_position / 3)
hash_pos_col = hash_position % 3

implement_move(board, Move[move_input], hash_pos_row, hash_pos_col)

for i in range(3):
    for j in range(3):
        print(board[i][j], end="")





    