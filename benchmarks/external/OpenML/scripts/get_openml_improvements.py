"""
This script is intended to be used with MindsDB OpenML benchmark results, to report the monthly improvement in those datasets
Example call: `python get_openml_improvements.py ./March2021/consolidated.csv ./June21/consolidated.csv ./June21/`
"""

import argparse
import pandas as pd
import numpy as np

def relative_improvement(old, new):
    if np.isnan(old) or np.isnan(new):
        return None
    else:
        old = old[0]
        new = new[0]
        return (new-old)/old if old != 0 else new-old

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Relative improvements script.')
    parser.add_argument('old_mdb_results', type=str)
    parser.add_argument('new_mdb_results', type=str)
    parser.add_argument('out_path', type=str, default='./')
    args = parser.parse_args()
    
    old_df = pd.read_csv(args.old_mdb_results)
    new_df = pd.read_csv(args.new_mdb_results)

    print(f'Old MDB OpenML results have {old_df.shape[0]} datasets...')
    print(f'New MDB OpenML results have {new_df.shape[0]} datasets...')

    old_datasets = set(old_df['task'].unique())
    new_datasets = set(new_df['task'].unique())

    old_diff = old_datasets.difference(new_datasets)
    new_diff = new_datasets.difference(old_datasets)

    for msg, diff in zip(('new', 'old'), (old_diff, new_diff)):
        if len(diff) > 1:
            print("WARNING: these datasets are not in the new results:")
            for o in old_diff:
                print(f"\t {o}")

    cols = ['duration', 'acc', 'auc', 'logloss']
    improvements = []

    for d in old_datasets.intersection(new_datasets):
        result = [d]
        for col in cols:
            result.append(relative_improvement(old_df[old_df['task']==d][col].values,new_df[new_df['task']==d][col].values))
        improvements.append(result)

    out_cols = [
        'Task', 
        'Duration % change (lower is better)',
        'Acc % change (higher is better)',
        'AUC % change (higher is better)',
        'LogLoss % change (lower is better)'
    ]

    imp_df = pd.DataFrame(improvements, columns=out_cols)
    imp_df = imp_df.round(4)
    imp_df = imp_df.sort_values(by='Task')
    imp_df.to_csv(args.out_path+'incremental_improvement.csv', index=False)
