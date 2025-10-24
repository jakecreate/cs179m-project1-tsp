import numpy as np
import matplotlib.pyplot as plt
import math
import random
import threading
import time
import keyboard

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
    print("rand_1: ", rand_1, "\trand_2: ", rand_2)
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
    # return T_start * (alpha ** iteration)
    return 0.85 * (0.95 ** iteration)

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
    current_order = best_so_far_order
    current_dist = best_so_far_dist

    enter_key_pressed = False
    def wait_for_enter():
        nonlocal enter_key_pressed
        keyboard.wait('enter', suppress = True)
        enter_key_pressed = True

    enter_key_thread = threading.Thread(target = wait_for_enter, daemon = True)
    enter_key_thread.start()

    iteration = 0
    while (not enter_key_pressed):
        temperature = temperature_function(iteration)
        if (temperature == 0):
            return best_so_far_order, best_so_far_dist
    #   candidate_order = random_neighbor(best_so_far_order)
    #   candidate_dist = find_total_distance(candidate_order)
    #   E = current_dist - candidate_dist
    #   if (E > 0):     // if the candidate is better, take that instead
    #       current_order = candidate_order
    #       current_dist = candidate_dist
    #       if (current_dist < best_so_far_dist):   // if the current distance is the best we've seen so far  
    #           best_so_far_order = current_order
    #           best_so_far_dist = current_dist
    #           print(best_so_far_dist)
    #   else:
    #       probability = math.e**(E / temperature)
    #       if (random() < prob):
    #           current_order = candidate_order
    #           current_dist = candidate_dist
    #           if (current_dist < best_so_far_dist):   // if the current distance is the best we've seen so far  
    #               best_so_far_order = current_order
    #               best_so_far_dist = current_dist
    #               print(best_so_far_dist)
        iteration += 1
    return best_so_far_order, best_so_far_dist