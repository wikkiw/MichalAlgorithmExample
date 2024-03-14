'''

TESTED ONLY ON CEC2022!!!!!

'''

import numpy as np
import pandas as pd
import os
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def load_files(path, algname, fmin, fmax, dim, benchname, out):

    clear_algname = algname.replace('_','-')

    for f in range(fmin, fmax+1):
        p = os.path.join(path, f'{algname}_{f}_{dim}.txt')
        df = pd.read_csv(p, header=None, delim_whitespace=True)
        df = df.astype(float)
        results = list(df.iloc[15][:30])

        outlist = []
        for i in range(len(results)):
            outdict = {'params':[]}
            outdict['run'] = i
            outdict['fitness'] = float(results[i])
            outlist.append(outdict)



        with open(os.path.join(out, f'R_A_{clear_algname}_F_{benchname}{f:02d}_{dim}.json'), 'w') as file:
            json.dump(outlist, file, cls=NpEncoder)



def main():

    project_home_dir = os.path.dirname(os.path.abspath(__file__))
    results_directory = os.path.join(project_home_dir, '../Results')
    fmin = 1
    fmax = 2
    dim = 20
    benchmark_name = 'CEC'

    #Example use on CEC 2022
    load_files('C:\\Users\\aviktorin\\Downloads\\2022-SO-BO-main\\Results_and_Ranking\\CEC1230\\Results',
               'NL-SHADE-LBC', fmin, fmax, dim, benchmark_name, results_directory)


    load_files('C:\\Users\\aviktorin\\Downloads\\2022-SO-BO-main\\Results_and_Ranking\\CEC2080\\Results',
               'EA4eigN100_10', fmin, fmax, dim, benchmark_name, results_directory)


    load_files('C:\\Users\\aviktorin\\Downloads\\2022-SO-BO-main\\Results_and_Ranking\\CEC2251\\Results',
               'NL-SHADE-RSP-MID', fmin, fmax, dim, benchmark_name, results_directory)


if __name__ == '__main__':
    main()