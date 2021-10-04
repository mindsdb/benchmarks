"""
As input, the consolidated.csv from MindsDB, and the .csv with results for all other frameworks.
"""

import argparse
import pandas as pd
import numpy as np
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Consolidate OpenML.')

    parser.add_argument('path', type=str, default='./')
    parser.add_argument('others_path', type=str, default='./')
    args = parser.parse_args()

    mdb_path = args.path+'consolidated.csv'
    others = args.others_path+'other_frameworks.csv'

    odf = pd.read_csv(others)
    mdb = pd.read_csv(mdb_path)
    mdb['framework'] = ['MindsDB' for _ in range(len(mdb))]
    mdb = mdb.drop('n_folds', axis=1)
    mdb['task'] = mdb['task'].apply(str.lower)

    odf = pd.concat([odf, mdb])
    
    results = odf.groupby(['task', 'framework']).mean()
    results = results.drop(['fold', 'seed', 'models', 'result', 'score', 'imp_result', 'imp_score', 'norm_score'], axis=1)
    results.to_csv(args.path+'/compared_all.csv')

    final = pd.DataFrame(columns=['task', *[framework for framework in results.reset_index()['framework'].unique()]])
    final['task'] = results.reset_index()['task'].unique()
    final.set_index('task', inplace=True)

    results = results.to_dict()

    for metric, info in results.items():
        out = final.copy()
        for k, v in info.items():
            out.at[k] = v

        out = out.astype(np.float).round(3)
        out.to_csv(args.path+f'{metric}.csv')