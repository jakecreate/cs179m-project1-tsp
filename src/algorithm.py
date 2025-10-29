import numpy as np
import matplotlib.pyplot as plt
import math
import random
import threading
import time
# import keyboard
from pynput import keyboard

# input:
# arr - a numpy array. In main.py, this array is called X. It contains an array of length 2 arrays.
# These are the coords of all the points.
# The first pair of numbers are the coords for the landing pad (aka the starting point).
#
# order - This will be a python array of numbers.
# This set contains the order in which the different points will be visited on this path. The set will
# start with 1 since the starting point will always be the landing pad. The set will also always end with 1
# since we have to end on the landing pad.
#
# output:
# output the total distance of the path the drone will take given this order.
# TODO: possibly replace this with a distance matrix so that we don't have to calculate every time
def find_total_distance(arr, order):
    def distance_between(point_1, point_2):
        x_diff = arr[point_1 - 1][0] - arr[point_2 - 1][0]
        y_diff = arr[point_1 - 1][1] - arr[point_2 - 1][1]
        return math.sqrt(x_diff**2 + y_diff**2)
    
    sum = 0
    for i in range(len(order) - 1):   # goes from the first element to the second to last element
        sum += distance_between(order[i], order[i + 1])
    return sum

# input:
# order - a python array of numbers.
# This set contains the order in which the different points will be visited on this path. The set will
# start with 1 since the starting point will always be the landing pad.The set will also always end with 1
# since we have to end on the landing pad.
# 
# output:
# output a python array of numbers. This array will be a random_neighbor to the set that was inputted.
# To generate this random neighbor, swap the places of 2 random points.
def random_neighbor(order):
    rand_1 = random.randint(1, len(order) - 2)
    rand_2 = random.randint(1, len(order) -2)
    while (rand_1 == rand_2):
        rand_2 = random.randint(2, len(order) - 2)
    order[rand_1], order[rand_2] = order[rand_2], order[rand_1]

# input:
# iteration - the number of the iteration that the algorithm is on
#
# output:
# Output the temperature at that iteration. I chose exponential cooling since it
# allows for a lot of exploration early on and then starts honing in on a solution
# later but still allows for some exploration even after some time. Allowing for
# more exploration early on will help the algorithm find a better solution faster.
# I chose T_start = 0.85 because the cost of choosing a bad option isn't too large.
def temperature_function(iteration):
    # T = T_start * (alpha ** iteration)
    return 0.85 * (0.99999 ** iteration)

# input:
# arr - a numpy array. In main.py, this array is called X. It contains an array of length 2 arrays.
# These are the coords of all the points.
# The first pair of numbers are the coords for the landing pad (aka the starting point).
#
# ouput:
# This function will run the simulated annealing algorithm until it is interupped by the press of the enter key.
# Upon the press of the enter key, return the following:
# distance - an int containing the total distance of the best route we've found so far.
#
# route - an python array of the order in which the points should be visted for the best route we've found
# so far. This array must start and end with 1 since the drone must start and end from the landing pad.
#
# During execution, every time we find a new best route, print the distance to the terminal.
def simulated_annealing(arr):
    num_points = int(arr.size / 2)
    time_dist_list = [] # keep track for graph
    # best_so_far_order = random order
    best_so_far_order = []
    best_so_far_order.append(1)
    while (len(best_so_far_order) != num_points):
        # generate a random number from 2 to the number of elements in arr
        rand = random.randint(2, num_points)
        if (not rand in best_so_far_order):
            best_so_far_order.append(rand)
    best_so_far_order.append(1)

    best_so_far_dist = find_total_distance(arr, best_so_far_order)
    print(f'\t{round(best_so_far_dist, 1)}')
    current_order = best_so_far_order.copy()
    current_dist = best_so_far_dist
    
    time_dist_list.append([0, best_so_far_dist])
    
    enter_key_pressed = False
    def wait_for_enter(key):
        nonlocal enter_key_pressed
        if (key == keyboard.Key.enter):
            enter_key_pressed = True
            return False    # stop the listener

    listener = keyboard.Listener(on_press=wait_for_enter, suppress=True)
    listener.start()


    iteration = 0
    init_time = time.time() # start time
    prev_time = init_time
    while (not enter_key_pressed):
        temperature = temperature_function(iteration)
        if (temperature == 0):
            return best_so_far_dist, best_so_far_order, np.array(time_dist_list)
        candidate_order = current_order.copy()
        random_neighbor(candidate_order)
        candidate_dist = find_total_distance(arr, candidate_order)
        E = current_dist - candidate_dist
        if (E > 0):     # if the candidate is better, take that instead
            current_order = candidate_order.copy()
            current_dist = candidate_dist
            if (current_dist < best_so_far_dist):   # if the current distance is the best we've seen so far  
                best_so_far_order = current_order.copy()
                best_so_far_dist = current_dist
                print(f'\t{round(best_so_far_dist, 1)}')
                
        else:          # if the candidate is worse, have a random chance to take it anyways
            probability = math.e**(E / temperature)
            if (random.random() < probability):
                current_order = candidate_order.copy()
                current_dist = candidate_dist

                # this if condition will probably never run since it'll always be a worse choice
                if (current_dist < best_so_far_dist):   # if the current distance is the best we've seen so far  
                    best_so_far_order = current_order.copy()
                    best_so_far_dist = current_dist
                    print(f'\t{round(best_so_far_dist, 1)}')
        
        present = time.time()
        if (present - prev_time >= 0.5):
            time_dist_list.append([present - init_time, best_so_far_dist])
            prev_time = time.time() 
                 
        iteration += 1
        if (iteration % 250):
            time.sleep(0.001)

    return best_so_far_dist, best_so_far_order, np.array(time_dist_list)

# basline
def random_search(X): 
    # distance matrix
    m = X.shape[0]
    b1, b2 = X[:, np.newaxis, :], X[np.newaxis, :, :] # (m, 1, n), (1, m, n)
    dist_mtx = np.linalg.norm(b1 - b2, axis=2)
    
    # from simulated annealing 
    enter_key_pressed = False
    def wait_for_enter(key):
        nonlocal enter_key_pressed
        if (key == keyboard.Key.enter):
            enter_key_pressed = True
            return False    # stop the listener

    listener = keyboard.Listener(on_press=wait_for_enter, suppress=True)
    listener.start()
    
    min_dist = math.inf
    init_time = time.time() # start time
    prev_time = init_time
    time_dist_list = []
    
    while not enter_key_pressed: 
        
        rand_order = np.hstack([0, np.random.permutation(np.arange(1, X.shape[0])), 0])
        total_dist = 0
        
        for i in range(1, m):
            total_dist+=dist_mtx[rand_order[i], rand_order[i-1]]

        present = time.time()
        if present - prev_time >= 0.5:
            time_dist_list.append([present - init_time, min_dist])
            prev_time = time.time()
            
        if total_dist < min_dist:
            order = rand_order
            min_dist = total_dist
            print(f'\t{round(min_dist,1)}')
               
    return min_dist, order, np.array(time_dist_list)
            
            
        
    
    
        
    
    
    
    