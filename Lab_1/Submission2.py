from enum import Enum
import math

def available_moves(row, col):
    avail_moves = []
     
    if row != 0: avail_moves.append("UP")
    if row != 2: avail_moves.append("DOWN")
    if col != 0: avail_moves.append("LEFT")
    if col != 2: avail_moves.append("RIGHT")
    return avail_moves

board_input = input()

hash_position = board_input.find("#")
hash_pos_row = math.floor(hash_position / 3)
hash_pos_col = hash_position % 3

available = available_moves(hash_pos_row, hash_pos_col)
for i in range(len(available)):
    print(available[i])







    