import os
import sys
from pathlib import Path
import json
import numpy as np


def get_algorihms(directory_path):
    """
        Lists all files in the given directory.

        Args:
        - directory_path (str): The path to the directory to list files from.

        Returns:
        - None
    """
    algorithms = []
    if os.path.isdir(directory_path):
        #print(f"Listing all files in directory: {directory_path}")
        # Iterate through all files and directories in the specified directory
        for filename in os.listdir(directory_path):

            # Construct full file path
            file_path = os.path.join(directory_path, filename)
            # Check if it is a file
            if os.path.isfile(file_path) and filename.startswith('A_'):
                if filename.__contains__('template') == False:
                    algorithms.append(Path(filename).stem)
    else:
        print(f"The path {directory_path} is not a directory.")

    return algorithms

def get_functions(directory_path):
    """
        Lists all files in the given directory.

        Args:
        - directory_path (str): The path to the directory to list files from.

        Returns:
        - None
    """
    functions = []
    if os.path.isdir(directory_path):
        #print(f"Listing all files in directory: {directory_path}")
        # Iterate through all files and directories in the specified directory
        for filename in os.listdir(directory_path):

            # Construct full file path
            file_path = os.path.join(directory_path, filename)
            # Check if it is a file
            if os.path.isfile(file_path) and filename.startswith('F_'):
                if filename.__contains__('template') == False:
                    functions.append(Path(filename).stem)
    else:
        print(f"The path {directory_path} is not a directory.")

    return functions

def run_all(dims, algorithms, functions, runs, max_evals, export_path):

    algs = map(__import__, algorithms)
    funcs = map(__import__, functions)
    funs_list = [fun for fun in funcs]

    for alg in algs:

        for fun in funs_list:

            bounds = fun.get_bounds()
            for dim in dims:
                # Creating an algorithm instance
                a = alg.Algorithm(fun.evaluate, dim, bounds, max_evals)
                export_data = []
                export_name = 'R_' + alg.__name__ + '_' + fun.__name__ + "_" + str(dim) + '.json'
                for run in range(runs):
                    best = a.run()
                    # ndarrays are not JSON serializable!
                    if isinstance(best['params'], np.ndarray):
                        best['params'] = best['params'].tolist()
                    best['run'] = run
                    export_data.append(best)

                with open(os.path.join(export_path, export_name),'w') as file:
                    json.dump(export_data, file, cls=NpEncoder)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def main():

    #project_home_dir = 'C:\\Users\\aviktorin\\PycharmProjects\\MichalAlgorithmExample'
    project_home_dir = 'D:\\WorkBench\\2024_GPTOptimizer\\pythonCodes\\MichalAlgorithmExample'

    algorithms_directory = os.path.join(project_home_dir, 'Algorithms')
    functions_directory = os.path.join(project_home_dir, 'Functions')

    sys.path.insert(0, algorithms_directory)
    sys.path.insert(0, functions_directory)

    algorithms = get_algorihms(algorithms_directory)
    functions = get_functions(functions_directory)

    #func = objective_function  # Objective function
    dims = [5, 10, 20, 30, 50]  # Dimension of the problem
    max_evals = 1000  # Maximum number of evaluations
    runs = 30
    export_path = os.path.join(project_home_dir, 'Results')

    run_all(dims, algorithms, functions, runs, max_evals, export_path)

if __name__ == '__main__':
    main()