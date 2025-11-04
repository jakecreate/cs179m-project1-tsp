import numpy as np
import matplotlib.pyplot as plt
import math
import os
import sys

import algorithm

def generate_solution(X, route, name, distance):
    dpi = 100
    fig, ax = plt.subplots(figsize=(1980/dpi, 1980/dpi), dpi=dpi)
    sort_mask = np.array(route) - 1
    X_sorted = X[sort_mask]
    x, y = X_sorted[:, 0], X_sorted[:, 1]
    
    ax.scatter(x, y)
    ax.plot(x, y)
    
    for i, (x_i, y_i) in enumerate(X):
        ax.annotate(f'{i+1}', xy=(x_i, y_i), color='black', va='bottom', ha='left', fontsize='small')
    
    fig.savefig(f'./output/{name}_SOLUTION_{distance}.png', dpi=dpi)

    
if __name__ == '__main__':
    # INPUT I
    
    FOLDER_PATH = './data/'
    file_name = input('Enter the name of file: ')
    if not os.path.exists(FOLDER_PATH+file_name):
        print(f"The file {FOLDER_PATH+file_name} does not exist.")
        sys.exit(1)
    
    X = np.loadtxt(FOLDER_PATH+file_name)

    if X.shape[0] > 256:
        print("The file contains more than 256 locations.")
    elif X.shape[0] == 0:
        print("The file contains no locations.")
    else:
        print(f'There are {X.shape[0]} nodes, computing route...')
        print(f'\tShortest Route Discovered So Far')
    
    algo_func = algorithm.simulated_annealing
    # START tsp anytime algorithm + input II: interruption key ENTER
    distance, route, time_dist_list = algo_func(X)
    # END algorithm when key ENTER is pressed
    

    # OUTPUT
    if distance > 6000:
        print(f'Warning: Solution is {math.ceil(distance)}, greater than the 6000 - meter constraint')
    
    name = file_name.split('.')[0]
    print(f'Route written to disk as {name}_SOLUTION_{math.ceil(distance)}.txt')
    np.savetxt(f'./output/{name}_SOLUTION_{math.ceil(distance)}.txt', route, fmt='%.0f')
    np.savetxt(f'./experiment/{name}_EXP_{math.ceil(distance)}.txt', time_dist_list, fmt='%.3f')
    generate_solution(X, route, name, math.ceil(distance))
