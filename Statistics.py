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

    columns = ['algorithm', 'function', 'dim', 'min', 'max', 'median', 'mean', 'std', 'ranking']
    desc_stats = pd.DataFrame(columns=columns)

    res_columns = np.concatenate((algorithms, ['score', 'ranking']))

    df_rank_all = pd.DataFrame(index=algorithms, columns=['score','ranking'])
    dict_rank_all = {}
    for a in algorithms:
        dict_rank_all[a] = 0

    for dim in dims:

        df_rank_dim = pd.DataFrame(index=algorithms, columns=['score', 'ranking'])
        dict_rank_dim = {}
        for a in algorithms:
            dict_rank_dim[a] = 0

        for fun in functions:

            result = pd.DataFrame(index=algorithms, columns=res_columns)

            for row_player in algorithms:

                rp_result = list(df[(df['algorithm'] == row_player) & (df['function'] == fun) & (df['dim'] == dim)]['ofvs'])[0]

                new_row = {'algorithm': row_player, 'function': fun, 'dim': dim, 'min': min(rp_result),
                           'max': max(rp_result), 'median': np.median(rp_result), 'mean': np.mean(rp_result),
                           'std': np.std(rp_result), 'ranking': 0}

                desc_stats.loc[len(desc_stats)] = new_row
                result.loc[row_player, 'score'] = 0

                for col_player in algorithms:
                    if row_player == col_player:
                        result.loc[row_player, col_player] = '0'  # No match against themselves
                    else:
                        # Result
                        rp_result = list(df[(df['algorithm'] == row_player) & (df['function'] == fun) & (df['dim'] == dim)]['ofvs'])[0]
                        cp_result = list(df[(df['algorithm'] == col_player) & (df['function'] == fun) & (df['dim'] == dim)]['ofvs'])[0]

                        stat, p_value = ranksums(rp_result, cp_result)

                        # Interpret the results
                        if p_value < alpha:
                            if stat < 0:
                                sign = '+'
                                result.loc[row_player, 'score'] += 1
                                dict_rank_all[row_player] += 1
                                dict_rank_dim[row_player] += 1
                            else:
                                sign = '-'
                                result.loc[row_player, 'score'] -= 1
                                dict_rank_all[row_player] -= 1
                                dict_rank_dim[row_player] -= 1
                        else:
                            sign = '='

                        result.loc[row_player, col_player] = sign  # Random result for illustration

            result = result.sort_values(by='score', ascending=False)
            # get algorithm name and its ranking
            rank = 1
            for index, _ in result.iterrows():
                desc_stats.loc[(desc_stats['algorithm'] == index) & (desc_stats['function'] == fun) & (
                        desc_stats['dim'] == dim), 'ranking'] = rank
                result.loc[index,'ranking'] = rank
                rank += 1

            filename = 'S_F_' + fun + '_D_' + str(dim) + '.csv'
            result.to_csv(os.path.join(stats_directory, filename), index=True)
            print(f'Stats file {filename} created.')

        for a in algorithms:
            df_rank_dim.loc[a, 'score'] = dict_rank_dim[a]

        df_rank_dim = df_rank_dim.sort_values(by='score', ascending=False)
        i = 1
        for ind in df_rank_dim.index:
            df_rank_dim['ranking'][ind] = i
            i += 1
        filename = 'S_ranking_D_' + str(dim) + '.csv'
        df_rank_dim.to_csv(os.path.join(stats_directory, filename), index=True)
        print(f'Dim {dim} ranking file {filename} created.')

    filename = 'S_descriptive.csv'
    desc_stats.to_csv(os.path.join(stats_directory, filename), index=False)
    print(f'Descriptive stats file {filename} created.')

    for a in algorithms:
        df_rank_all.loc[a, 'score'] = dict_rank_all[a]

    df_rank_all = df_rank_all.sort_values(by='score', ascending=False)
    i = 1
    for ind in df_rank_all.index:
        df_rank_all['ranking'][ind] = i
        i += 1
    filename = 'S_ranking.csv'
    df_rank_all.to_csv(os.path.join(stats_directory, filename), index=True)
    print(f'Overall ranking file {filename} created.')



def main():
    # where to look for result files
    project_home_dir = os.path.dirname(os.path.abspath(__file__))

    results_directory = os.path.join(project_home_dir, 'Results')
    # where the stats should be created
    stats_directory = os.path.join(project_home_dir, 'Statistics')

    results = get_results(results_directory)
    df = organize_results(results)

    get_statistics(df, stats_directory)


if __name__ == '__main__':
    main()