from collections import deque
import time
import statistics
import matplotlib.pyplot as plt

def make_grid(grid):
    return [
        [grid[0], grid[1], grid[2]],
        [grid[3], grid[4], grid[5]],
        [grid[6], grid[7], grid[8]],
    ]

def make_string(grid):
    return ''.join(''.join(row) for row in grid)

def find_moves(state):
    grid = make_grid(state)
    for i in range(3):
        for j in range(3):
            if grid[i][j] == '#':
                x, y = i, j
                break

    moves = []
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_grid = [row[:] for row in grid]
            new_grid[x][y], new_grid[nx][ny] = new_grid[nx][ny], new_grid[x][y]
            moves.append(make_string(new_grid))

    return moves

def BFS(init, goal):
    visit = set()
    que = deque([(init, 0)])  # store (state, depth)
    nodes_exp = 0

    while que:
        curr, depth = que.popleft()
        nodes_exp += 1

        if curr == goal:
            return depth, nodes_exp  # return solution length and nodes expanded

        if curr in visit:
            continue

        visit.add(curr)

        for neighbor in find_moves(curr):
            if neighbor not in visit:
                que.append((neighbor, depth + 1))

    return None, nodes_exp  # if goal not found (shouldn't happen)

def generate_board_k_moves_away(init, k):
    visited = {init}
    queue = deque([(init, 0)])
    level_states = []

    while queue:
        state, depth = queue.popleft()

        if depth == k:
            level_states.append(state)
            continue

        for move in find_moves(state):
            if move not in visited:
                visited.add(move)
                queue.append((move, depth + 1))

    return level_states[0] if level_states else None

# Experiment
init = '12345678#'
goal = '12345678#'

ks = list(range(1, 32))  # depths 1 to 31
mean_times = []
std_times = []
mean_nodes = []
std_nodes = []

for depth in ks:
    times = []
    nodes = []

    for _ in range(5):  # repeat 5 times
        generated = generate_board_k_moves_away(init, depth)

        start_time = time.perf_counter()
        length, nodes_expanded = BFS(generated, goal)
        end_time = time.perf_counter()

        times.append(end_time - start_time)
        nodes.append(nodes_expanded)

    mean_times.append(statistics.mean(times))
    std_times.append(2 * statistics.stdev(times) if len(times) > 1 else 0)
    mean_nodes.append(statistics.mean(nodes))
    std_nodes.append(2 * statistics.stdev(nodes) if len(nodes) > 1 else 0)

# Plot time complexity
plt.errorbar(ks, mean_times, yerr=std_times, fmt='-o', capsize=5)
plt.xlabel("Solution Depth (k)")
plt.ylabel("Time (seconds)")
plt.title("BFS Time Complexity vs Solution Depth")
plt.grid(True)
plt.show()

# Plot space complexity
plt.errorbar(ks, mean_nodes, yerr=std_nodes, fmt='-o', capsize=5)
plt.xlabel("Solution Depth (k)")
plt.ylabel("Nodes Expanded")
plt.title("BFS Space Complexity vs Solution Depth")
plt.grid(True)
plt.show()
