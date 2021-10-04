import pandas as pd
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Consolidate OpenML.')

    parser.add_argument('path', type=str, default='./')
    args = parser.parse_args()

    csvs = [filepath for filepath in os.listdir(args.path) if '.csv' in filepath and 'MindsDB_benchmark_' in filepath]
    dfs = [pd.read_csv(args.path+csv) for csv in csvs]
    df = pd.concat(dfs)
    n_folds = df['fold'].max()+1
    n_folds = [int(n_folds) for _ in range(len(df))]
    df['n_folds'] = n_folds
    
    problematic_datasets = list(df[df['info'] == df['info']]['task'].unique())
    print("Problematic datasets:", problematic_datasets)
    results = df.groupby('task').mean().dropna(subset=['result'])

    results = results.drop(['params', 'models', 'fold', 'result', 'seed'], axis=1)
    results = results.round(4)

    results = results[['acc','auc','logloss','duration','n_folds']]
    results.to_csv(args.path+'consolidated.csv')