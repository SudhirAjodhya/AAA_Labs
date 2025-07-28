import random
import time
import matplotlib.pyplot as plt

# Implementation

def linearSearch(myList, key):
    for i in range(len(myList)):
        if myList[i] == key: return True
    return False

def generateList(n):
    myList = []
    while len(myList) < n:
        k = random.randint(1, n * 6)
        if (linearSearch(myList, k)) == False:
            myList.append(k)
    return myList


# ----Experimentation----

sizes_of_n = [256,512,1024,2048,4096,8192, 16384, 32768, 65536]#, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216]
timings = {n : [0, 0, 0] for n in sizes_of_n} # [Best, Worst, Average] per size of n

for i, n in enumerate(sizes_of_n):
    
    myList = generateList(n)
    
    # Best:
    best_start = time.time()
    linearSearch(myList, myList[0])
    best_end = time.time()
    timings[n][0] = best_end - best_start
    
    # Worst:
    worst_start = time.time()
    linearSearch(myList, myList[len(myList) - 1])
    worst_end = time.time()
    timings[n][1] = worst_end - worst_start
    
    # Average:
    average_start = time.time()
    linearSearch(myList, myList[random.randint(0, n - 1)])
    average_end = time.time()
    timings[n][2] = average_end - average_start

print("---Timings---")
for n, times in timings.items():
    print(f"{n} : {times}")

# Plot results
plt.figure(figsize=(12, 8))
complexity_cases = ['Best', 'Worst', 'Average']

for i, complexity in enumerate(complexity_cases):
    x = sizes_of_n
    y = [timings[n][i] for n in sizes_of_n]
    plt.plot(x, y, label = complexity)

plt.xlabel('Array Size')
plt.ylabel('Time(seconds)')
plt.title('Linear Search Complexity Timings')
plt.legend()
plt.grid(True)
plt.show()