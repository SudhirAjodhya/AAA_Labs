from enum import Enum
import math
from collections import deque
import random
import time
import matplotlib.pyplot as plt
import statistics
import numpy as np
from scipy.stats import linregress
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


def reverse_random_solution(goal_state, k_moves, hash_row, hash_col):
    """
    Return a GameSnapshot exactly k moves away from goal_state,
    uniformly sampled using BFS + reservoir sampling.
    """
    start = GameSnapshot(hash_row, hash_col, 0, goal_state)
    frontier = deque([start])
    visited = {tuple(map(tuple, start.board))}

    chosen = None
    seen_at_k = 0

    while frontier:
        current = frontier.popleft()

        # If depth k reached, consider for reservoir
        if current.moves == k_moves:
            seen_at_k += 1
            if random.randint(1, seen_at_k) == 1:
                chosen = current
            continue  # do not expand further

        # Explore children
        moves = available_moves(current.row, current.col)
        random.shuffle(moves)  # randomize order
        for mv in moves:
            dr, dc = Move[mv].value
            nr, nc = current.row + dr, current.col + dc

            next_board = [row[:] for row in current.board]
            switch_positions(next_board, current.row, current.col, nr, nc)

            key = tuple(map(tuple, next_board))
            if key not in visited:
                visited.add(key)
                frontier.append(GameSnapshot(nr, nc, current.moves + 1, next_board))

    if chosen is None:
        raise RuntimeError(f"No state found at depth {k_moves} (should not happen for 8-puzzle).")

    return chosen

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
k = 20
reversed_solution = reverse_random_solution(goal_board_configuration, k, hash_pos_row, hash_pos_col)
print(reversed_solution.board)    

# solve the board to prove its done in k moves
game_solver(reversed_solution.board, goal_board_configuration, reversed_solution.row, reversed_solution.col)



# # =====Time Complexity Experimentation=====

# print()
# print("Running 5 times on different values of k....")

# k = 31
# timings_storage = np.zeros((k, 5))
# timings_average = np.zeros(k)
# timing_deviations = np.zeros(k)
# values_k = np.zeros(k)
# spaces_storage = np.zeros((k, 5))
# spaces_average = np.zeros(k)
# spaces_deviations = np.zeros(k)
# for i in range(k):
#     print()
#     print("Running on k = " + str(i)+":")

#     # repeating 5 times for an average
#     for j in range(5):
#         # reverse solution to k steps
#         reversed_solution = reverse_solution(goal_board_configuration, i, hash_pos_row, hash_pos_col)

#         # Timing the bfs 
#         start_time = time.perf_counter()
#         solution, expanded_nodes = game_solver(reversed_solution.board, goal_board_configuration, reversed_solution.row, reversed_solution.col)
#         end_time = time.perf_counter()

#         print(end_time - start_time)
#         timings_storage[i][j] = end_time - start_time
#         spaces_storage[i][j] = expanded_nodes

#     timings_average[i] = statistics.mean(timings_storage[i]) #sum(timings_storage[i])/5
#     timing_deviations[i] = 2 * statistics.stdev(timings_storage[i])
#     spaces_average[i] = statistics.mean(spaces_storage[i])
#     spaces_deviations[i] = statistics.stdev(spaces_storage[i])
#     values_k[i] = i

#     print(f"Average elapsed time: {timings_average[i]:.6f} seconds")
#     print(f"Expanded nodes: {spaces_average[i]}")


# def fit_multiple_models(k, y):
#     """Try multiple complexity models and compare fits"""
#     results = {}
    
#     # Exponential model (your approach)
#     if len(k) >= 2:
#         try:
#             log_y = np.log(y[y > 0])
#             k_filtered = k[y > 0]
#             slope, intercept, r_value, _, _ = linregress(k_filtered, log_y)
#             results['exponential'] = {
#                 'r2': r_value**2,
#                 'base': math.exp(slope),
#                 'formula': f'O({math.exp(slope):.2f}^k)'
#             }
#         except:
#             pass
    
#     # Also try polynomial fit for comparison
#     try:
#         # Fit quadratic model: O(k^2)
#         coeffs = np.polyfit(k, y, 2)
#         y_pred = np.polyval(coeffs, k)
#         ss_res = np.sum((y - y_pred)**2)
#         ss_tot = np.sum((y - np.mean(y))**2)
#         r2_poly = 1 - (ss_res / ss_tot)
#         results['polynomial'] = {'r2': r2_poly, 'formula': 'O(k^2)'}
#     except:
#         pass
    
#     return results

# # --- Fit models ---
# #a_space, b_space, r2_space = fit_exponential(values_k, spaces_average)
# #a_time, b_time, r2_time = fit_exponential(values_k, timings_average)

# results = fit_multiple_models(values_k, timings_average)
# print(results)

# #print("\n=== Experimental Complexity Estimates ===")
# #print(f"Space: O({b_space:.2f}^k), R² = {r2_space:.4f}")
# #print(f"Time:  O({b_time:.2f}^k), R² = {r2_time:.4f}")


# # # Time Complexity
# # plt.figure(figsize=(8,4))
# # plt.xlabel("Number of moves(depth of tree)")
# # plt.ylabel("Run time(seconds)")
# # plt.title("8-Puzzle solver(BFS) Time complexity complexity analysis")
# # plt.errorbar(
# #     values_k,                 
# #     timings_average,          
# #     yerr=timing_deviations,     
# #     fmt='-o',                  
# #     ecolor='red',           
# #     capsize=5,                  
# #     label='Mean ± 2σ'
# # )
# # plt.show()


# # # Space Complexity
# # plt.figure(figsize=(8,4))
# # plt.xlabel("Number of moves (depth of tree)")
# # plt.ylabel("Number of nodes expanded")
# # plt.title("8-Puzzle solver(BFS) Space complexity analysis")
# # #plt.plot(values_k, spaces)
# # plt.errorbar(
# #     values_k,                   
# #     spaces_average,           
# #     yerr=spaces_deviations,    
# #     fmt='-o',                   
# #     ecolor='red',              
# #     capsize=5,                  
# #     label='Mean ± 2σ'
# # )
# # plt.show()

# # Create one figure with 2 rows, 1 column
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8,6), sharex=True)

# # --- Time Complexity ---
# ax1.errorbar(
#     values_k, timings_average,
#     yerr=timing_deviations,
#     fmt='-o', ecolor='red', capsize=5,
#     label='Mean ± 2σ'
# )
# ax1.set_ylabel("Run time (seconds)")
# ax1.set_title("8-Puzzle solver (BFS) Complexity Analysis")
# ax1.legend()

# # --- Space Complexity ---
# ax2.errorbar(
#     values_k, spaces_average,
#     yerr=spaces_deviations,
#     fmt='-o', ecolor='red', capsize=5,
#     label='Mean ± 2σ'
# )
# ax2.set_xlabel("Number of moves (depth of tree)")
# ax2.set_ylabel("Nodes expanded")
# ax2.legend()

# # Adjust spacing so titles/labels don’t overlap
# plt.tight_layout()
# plt.show()



