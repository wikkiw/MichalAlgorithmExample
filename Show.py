import os
import sys
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Run_wrapper import get_functions

def show2D(functions):
    f = __import__(functions)

    x = np.linspace(f.get_bounds()[0], f.get_bounds()[1], 1000)
    y = [f.evaluate(np.array(i)) for i in x]

    plt.plot(x, y)  # Plot x vs. y
    plt.title(functions)  # Title of the plot
    plt.xlabel("x")  # Label for the x-axis
    plt.ylabel("cf(x)")  # Label for the y-axis
    plt.grid(True)  # Show grid
    plt.show()  # Display the plot

    pass

def show3D(functions):
    f = __import__(functions)

    x = np.linspace(f.get_bounds()[0], f.get_bounds()[1], 100)
    y = np.linspace(f.get_bounds()[0], f.get_bounds()[1], 100)
    x, y = np.meshgrid(x, y)
    z = np.zeros_like(x)
    # Iterate over the grid to compute z values
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            # Here, we treat each pair (x[i, j], y[i, j]) as a small array to be passed to your custom function
            z[i, j] = f.evaluate(np.array([x[i, j], y[i, j]]))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, z, cmap='viridis')  # You can change 'viridis' to any other colormap

    # Labels and titles
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('cf(x)')
    ax.set_title(functions)

    # Optional: Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

    pass

def main():

    project_home_dir = os.path.dirname(os.path.abspath(__file__))

    functions_directory = os.path.join(project_home_dir, 'Functions')
    sys.path.insert(0, functions_directory)
    functions = get_functions(functions_directory)

    for f in functions:
        show2D(f)
        show3D(f)


if __name__ == '__main__':
    main()