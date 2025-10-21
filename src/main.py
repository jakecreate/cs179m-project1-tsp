import numpy as np
import matplotlib.pyplot as plt
import math

def generate_image(X, route, name, distance):
    dpi = 100
    fig, ax = plt.subplots(figsize=(1980/dpi, 1980/dpi), dpi=dpi)
    sort_mask = np.array(route) - 1
    X_sorted = X[sort_mask]
    x, y = X_sorted[:, 0], X_sorted[:, 1]
    
    ax.scatter(x, y)
    ax.plot(x, y)
    
    for i, (x_i, y_i) in enumerate(X):
        ax.annotate(f'{i+1}', xy=(x_i, y_i), color='black', va='bottom', ha='left', fontsize='small')
    
    fig.savefig(f'../output/{name}_SOLUTION_{distance}.png', dpi=dpi)
    
if __name__ == '__main__':
    # INPUT I
    
    FOLDER_PATH = '../data/'
    file_name = input('Enter the name of file: ')
    
    X = np.loadtxt(FOLDER_PATH+file_name)
    print(f'There are {X.shape[0]} nodes, computing route...')
    print(f'\t Shortest Route Discovered So Far')
    # START tsp anytime algorithm + input II: interruption key ENTER
    
    

    # END algorithm when key ENTER is pressed
    temp_list = [i + 1 for i in range(X.shape[0])]
    
    distance, route = (1234, temp_list) # algorithm output
    
    # OUTPUT
    if distance > 6000:
        print(f'Warning: Solution is {math.ceil(distance)}, greater than the 6000 - meter constraint')
        
    print(f'total distance: {math.ceil(distance)}')
    
    route.append(route[0])
    name = file_name.split('.')[0]
    np.savetxt(f'../output/{name}_SOLUTION_{distance}.txt', route, fmt='%.0f')
    
    generate_image(X, route, name, distance)
