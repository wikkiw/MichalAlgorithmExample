import numpy as np
import os
import json
import pandas as pd
from pathlib import Path
from scipy.stats import ranksums

def get_results(directory_path):
    """
        Lists all files in the given directory.

        Args:
        - directory_path (str): The path to the directory to list files from.

        Returns:
        - None
    """
    results = []
    if os.path.isdir(directory_path):
        #print(f"Listing all files in directory: {directory_path}")
        # Iterate through all files and directories in the specified directory
        for filename in os.listdir(directory_path):

            # Construct full file path
            file_path = os.path.join(directory_path, filename)
            # Check if it is a file
            if os.path.isfile(file_path) and filename.startswith('R_'):
                results.append(file_path)
    else:
        print(f"The path {directory_path} is not a directory.")

    return results


def organize_results(result_files):
    columns = ['algorithm', 'function', 'dim', 'ofvs', 'params']
    df = pd.DataFrame(columns=columns)
    for result_file in result_files:

        name = Path(result_file).stem
        with open(result_file, 'r') as file:
            data = json.load(file)
            ofvs = [run['fitness'] for run in data]
            params = [run['params'] for run in data]

            name_parts = name.split('_')
            alg = name_parts[2]
            fun = name_parts[4]
            dim = int(name_parts[5])

            new_row = {'algorithm': alg, 'function': fun, 'dim': dim, 'ofvs': ofvs, 'params': params}
            df.loc[len(df)] = new_row

    return df

def get_statistics(df, stats_directory, algorithms=None, dims=None, functions=None, alpha=0.05):

    if algorithms is None:
        algorithms = df['algorithm'].unique()

    if dims is None:
        dims = df['dim'].unique()

    if functions is None:
        functions = df['function'].unique()

    for dim in dims:
        for fun in functions:

            result = pd.DataFrame(index=algorithms, columns=algorithms)
            for row_player in algorithms:
                for col_player in algorithms:
                    if row_player == col_player:
                        df.loc[row_player, col_player] = '0'  # No match against themselves
                    else:
                        # Result
                        rp_result = df[(df['algorithm'] == row_player) & (df['function'] == fun) & (df['dim'] == dim)]['ofvs']
                        cp_result = df[(df['algorithm'] == col_player) & (df['function'] == fun) & (df['dim'] == dim)]['ofvs']

                        stat, p_value = ranksums(rp_result, cp_result)

                        # Interpret the results
                        if p_value < alpha:
                            if stat < 0:
                                sign = '+'
                            else:
                                sign = '-'
                        else:
                            sign = '='

                        result.loc[row_player, col_player] = sign # Random result for illustration

            filename = 'S_F_' + fun + '_D_' + str(dim) + '.csv'
            result.to_csv(os.path.join(stats_directory, filename), index=True)
            print(f'Stats file {filename} created.')



def main():
    # where to look for result files
    project_home_dir = 'C:\\Users\\aviktorin\\PycharmProjects\\MichalAlgorithmExample'
    results_directory = os.path.join(project_home_dir, 'Results')
    # where the stats should be created
    stats_directory = os.path.join(project_home_dir, 'Statistics')

    results = get_results(results_directory)
    df = organize_results(results)

    get_statistics(df, stats_directory)


if __name__ == '__main__':
    main()