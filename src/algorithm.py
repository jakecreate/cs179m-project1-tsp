import numpy as np
import matplotlib.pyplot as plt
import math

# input:
# arr - a numpy array. In main.py, this array is called X. It contains an array of length 2 arrays.
# These are the coords of all the points.
# The first pair of numbers are the coords for the landing pad (aka the starting point).
#
# order - This will be a python set of numbers. (sets don't allow duplicate items which is epic.)
# This set contains the order in which the different points will be visited on this path. The set will
# start with 1 since the starting point will always be the landing pad.
#
# output:
# output the total distance of the path the drone will take given this order.
def find_total_distance(arr, order):
    pass

# input:
# order - a python set of numbers. (sets don't allow duplicate items which is epic.)
# This set contains the order in which the different points will be visited on this path. The set will
# start with 1 since the starting point will always be the landing pad.
# 
# output:
# output a python set of numbers. This set will be a random_neighbor to the set that was inputted.
# To generate this random neighbor, swap the places of 2 random points.
def random_neighbor(order):
    pass

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
    # best_so_far_order = random order
    # best_so_far_dist = find_total_distance(best_so_far_order)
    # current_order = best_so_far_order
    # current_dist = best_so_far_dist
    # while (enter key hasn't been pressed):
    #   temperature = whatever scheduled temperature we have for this iteration
    #   if (temperature == 0):
    #       return best_so_far_order, best_so_far_dist
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
    # return best_so_far_order, best_so_far_dist
    
    pass