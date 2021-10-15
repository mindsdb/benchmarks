import argparse
from benchmarks.datasets.dataset import DatasetInterface
import os
import traceback
import sys
import time
import importlib
from typing import List, Tuple
import pandas as pd
from benchmarks.helpers.db import get_mysql, setup_mysql
from benchmarks.helpers.get_commit import get_commit
from benchmarks.frameworks import Framework_lightwood
from mindsdb_datasources.datasources.file_ds import FileDS
import ray
from sklearn.model_selection import StratifiedKFold, KFold
import numpy as np
from benchmarks.helpers.accuracy import requires_normal_predictions
import torch
import random
import datetime
import json

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
DATASETS_DIR = os.path.join(CURRENT_DIR, os.path.join('benchmarks','datasets'))


def fit_and_infer_w_lightwood(df_train: pd.DataFrame, df_test: pd.DataFrame, problem_definition: object) -> Tuple[list, list, float]:
    import lightwood
    from lightwood import dtype
    from lightwood.api.high_level import predictor_from_problem
    from lightwood import PredictionArguments

    def to_typed_list(lst: List, dtype: type) -> List:
        """
        Cast list of predictions to the specified `dtype`.
        For list of lists, apply the casting on each sublist element.
        """
        lst = list(lst)
        if not isinstance(lst[0], list):
            lst = [dtype(l) for l in lst]
        else:
            lst = [[dtype(l) for l in subl] for subl in lst]
        return lst
    
    started = time.time()
    predictor: lightwood.PredictorInterface = predictor_from_problem(df_train, problem_definition)
    predictor.learn(df_train)
    
    try:
        df_test = df_test[df_test['make_predictions']]
    except KeyError:
        pass

    all_mixer_predictions = predictor.predict(df_test, {'all_mixers': True})
    predictions_per_mixer = {}
    for column in all_mixer_predictions.columns:
        predictions_per_mixer[column.replace('__mdb_mixer_', '')] = list(all_mixer_predictions[column])

    output = predictor.predict(df_test)
    predictions = list(output['prediction'])
    target = problem_definition['target']
    real_values = df_test[target]

    if predictor.dtype_dict[target] in (dtype.categorical, dtype.binary):
        predictions = to_typed_list(predictions, str)
        real_values = to_typed_list(real_values, str)
    elif predictor.dtype_dict[target] in (dtype.integer):
        predictions = to_typed_list(predictions, int)
        real_values = to_typed_list(real_values, int)
    elif predictor.dtype_dict[target] in (dtype.float):
        predictions = to_typed_list(predictions, float)
        real_values = to_typed_list(real_values, float)

    return predictions, predictions_per_mixer, real_values, int(time.time() - started)


def setup_args():
    parser = argparse.ArgumentParser(description='Args for the mindsdb benchmark suite')
    parser.add_argument('--platform', type=str, default='local')
    parser.add_argument('--datasets', type=str, default=None) # comma separated lists of datasets to run | special values: openml runs all openml datasets
    parser.add_argument('--lightwood', type=str, default=None) # env | #latest | branch name | commit hash | None
    parser.add_argument('--use_ray', type=str, default='1') # 1 to use, 0 to not use
    parser.add_argument('--use_db', type=str, default='1') # 1 to use, 0 to not use
    parser.add_argument('--is_dev', type=str, default='1') # 1 to use, 0 to not use

    args, unknown = parser.parse_known_args()
    if len(unknown) > 0:
        print(f'Unknown arguments: {unknown}')
        exit()
    
    false_values = (False, 'false', 'False', 0, '0')

    if args.use_ray in false_values:
        args.use_ray = False
    else:
        args.use_ray = True

    if args.use_db in false_values:
        args.use_db = False
    else:
        args.use_db = True

    if args.is_dev in false_values:
        args.is_dev = False
    else:
        args.is_dev = True

    if args.datasets is not None:
        args.datasets = args.datasets.split(',')

    ds_list: List[DatasetInterface] = []
    for ds_name in os.listdir(DATASETS_DIR):
        if '__' in ds_name or '.py' in ds_name:
            continue
        
        if args.datasets is not None:
            if args.datasets[0] == 'openml':
                if 'openml' not in ds_name:
                    continue
            elif ds_name not in args.datasets:
                continue

        try:
            info = importlib.import_module(f'benchmarks.datasets.{ds_name}.info')
        except ImportError:
            print('[INFO] Dataset {} doesn\'t contain info.py'.format(ds_name))
            continue

        dataset = info.Dataset(DATASETS_DIR, ds_name)
        ds_list.append(dataset)

    args.datasets = ds_list

    if args.platform != 'local':
        raise Exception('Only running locally is supported !')

    return args


def gen_dataframe(ds: DatasetInterface) -> pd.DataFrame:
    file_extension = ds.file.split('.')[-1]

    if file_extension == 'csv':
        df = pd.read_csv(ds.file)
    elif file_extension == 'json':
        df = FileDS(ds.file).df
    else:
        raise Exception('Failed to read dataset "{}"'.format(ds.name))
    
    before_len = len(df)
    df = df.drop_duplicates()
    num_duplicates = before_len - len(df)
    if num_duplicates > 0:
        print(f'Dropped a total of {num_duplicates} duplicate rows (out of {before_len}) for dataset: {ds.name}')
    return df


def ts_ds_to_train_test(ds: DatasetInterface) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = gen_dataframe(ds)
    df = df.sort_values(by=[col for col in ds.learn_kwargs['timeseries_settings']['order_by']])
    group = ds.learn_kwargs['timeseries_settings'].get('group_by', None)  # for now assumes single group column @TODO: generalize
    if group is not None and len(group) > 0:
        df_train = pd.DataFrame(columns=df.columns)
        df_test = pd.DataFrame(columns=df.columns)
        for g in df[group[0]].unique():
            subframe = df[df[group[0]] == g]
            length = subframe.shape[0]
            split_idx = int(0.8 * length)
            df_train = df_train.append(subframe[:split_idx])
            df_test = df_test.append(subframe[split_idx:])
    else:
        split_idx = int(0.8 * len(df))
        df_train = df[:split_idx]
        df_test = df[split_idx:]
    
    return df_train.reset_index(), df_test.reset_index()


def ds_to_folds(ds: DatasetInterface, num_folds: int) -> List[pd.DataFrame]:
    df = gen_dataframe(ds)
    folds = []
    if 'classification' in ds.tags:
        splitter = StratifiedKFold(n_splits=num_folds, random_state=0, shuffle=True)
        '''
        for i in range(num_folds):
            df, fold = train_test_split(
                                    df,
                                    test_size=i+1/num_folds,
                                    random_state=0, 
                                    stratify=df[ds.target]
                                )
            folds.append(fold)
        '''
    else:
        splitter = KFold(n_splits=num_folds, random_state=0, shuffle=True)

    for _, test_indexes in splitter.split(df[ds.target], df[ds.target]):
        folds.append(pd.DataFrame(df.iloc[test_indexes]))

    return folds


def run_dataset(ds: DatasetInterface, lightwood_version: str, accuracy_data: dict, lightwood_commit: str, is_dev: bool, use_db: bool):
    try:
        print('=' * 6 + f'Running for dataset {ds.name}' + '=' * 6)

        if use_db:
            skip = True
            for acc_func in ds.accuracy_functions:
                if acc_func not in requires_normal_predictions:
                    continue
                found = False
                for (ad_dataset_name, ad_accuracy_function), res_arr in accuracy_data.items():
                    if acc_func.__name__ == ad_accuracy_function and ad_dataset_name == ds.name:
                        for res in res_arr:
                            if res['lightwood_commit'] == lightwood_commit and res['lightwood_version'] == lightwood_version:
                                found = True
                if not found:
                    skip = False
        else:
            skip = False

        if skip:
            print(f'\n============\n\nSkipping dataset {ds.name} since it already ran for the same version and commit hash\n===========\n\n')
            return

        if not ds.active:
            print(f'\n============\n\Ignoring dataset {ds.name} since it isn''t marked as active\n===========\n\n')          
            return


        # Otherwise we get pickling errors
        def seed(seed_nr):
            torch.manual_seed(seed_nr)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
            np.random.seed(seed_nr)
            random.seed(seed_nr)
        seed(42)
        problem_definition = ds.learn_kwargs
        problem_definition['target'] = ds.target
        problem_definition['strict_mode'] = ds.strict_mode

        accuracy_map = {}
        accuracy_map_per_fold = {}
        accuracy_per_mixer_map = {}
        accuracy_per_mixer_per_fold_map = {}

        if 'timeseries' in ds.tags:
            df_train, df_test = ts_ds_to_train_test(ds)
            predictions, predictions_per_mixer, real_values, runtime = fit_and_infer_w_lightwood(df_train, df_test, problem_definition)
            for accuracy_function in ds.accuracy_functions:
                if accuracy_function not in requires_normal_predictions:
                    continue
                accuracy_map[accuracy_function.__name__] = accuracy_function(real_values, predictions)
                accuracy_per_mixer_map[accuracy_function.__name__] = {}
                for mixer in predictions_per_mixer:
                    accuracy_per_mixer_map[accuracy_function.__name__][mixer] = accuracy_function(real_values, predictions_per_mixer[mixer])
        
        elif ds.num_folds is None:
            folds = ds_to_folds(ds, 5)
            predictions, predictions_per_mixer, real_values, runtime = fit_and_infer_w_lightwood(pd.concat(folds[:4]), folds[4], problem_definition)
            for accuracy_function in ds.accuracy_functions:
                if accuracy_function not in requires_normal_predictions:
                    continue
                accuracy_map[accuracy_function.__name__] = accuracy_function(real_values, predictions)
                accuracy_per_mixer_map[accuracy_function.__name__] = {}
                for mixer in predictions_per_mixer:
                    accuracy_per_mixer_map[accuracy_function.__name__][mixer] = accuracy_function(real_values, predictions_per_mixer[mixer])
        else:
            folds = ds_to_folds(ds, ds.num_folds)
            for i in range(len(folds)):
                df_test = folds[i]
                df_train = pd.concat(folds[:i] + folds[i+1:])
                predictions, predictions_per_mixer, real_values, runtime = fit_and_infer_w_lightwood(df_train, df_test, problem_definition)
                
                for accuracy_function in ds.accuracy_functions:
                    if accuracy_function not in requires_normal_predictions:
                        continue
                    if accuracy_function.__name__ not in accuracy_map_per_fold:
                        accuracy_map_per_fold[accuracy_function.__name__] = []
                    accuracy_map_per_fold[accuracy_function.__name__].append(accuracy_function(real_values, predictions))

                    if accuracy_function.__name__ not in accuracy_per_mixer_per_fold_map:
                        accuracy_per_mixer_per_fold_map[accuracy_function.__name__] = {}
                        for mixer in predictions_per_mixer:
                            accuracy_per_mixer_per_fold_map[accuracy_function.__name__][mixer] = []
                    for mixer in predictions_per_mixer:
                        accuracy_per_mixer_per_fold_map[accuracy_function.__name__][mixer].append(accuracy_function(real_values, predictions_per_mixer[mixer]))

            for k in accuracy_map_per_fold:
                accuracy_map[k] = np.mean(accuracy_map_per_fold[k])

            for k in accuracy_per_mixer_per_fold_map:
                for mixer in accuracy_per_mixer_per_fold_map[k]:
                    accuracy_per_mixer_map = np.mean(accuracy_per_mixer_per_fold_map[k][mixer])

        for accuracy_function_name in accuracy_map:
            accuracy = accuracy_map[accuracy_function_name]
            accuracy_per_fold = None
            if accuracy_function_name in accuracy_map_per_fold:
                accuracy_per_fold = ','.join([str(x) for x in accuracy_map_per_fold[accuracy_function_name]])

            print(f'\n\nGot accuracy: {accuracy} ({accuracy_function_name}) [per fold: {accuracy_per_fold}] for {ds.name}\n\n')

            insert_map = {
                'dataset': ds.name,
                'accuracy': accuracy,
                'accuracy_function': accuracy_function_name,
                'runtime': runtime,
                'lightwood_version': lightwood_version,
                'lightwood_commit': lightwood_commit,
                'is_dev': is_dev,
                'num_folds': ds.num_folds,
                'accuracy_per_fold': accuracy_per_fold,
                'accuracy_per_mixer': json.dumps(accuracy_per_mixer_map)
            }

            q = f'INSERT INTO benchmarks.v4 ({",".join(list(insert_map.keys()))}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

            if use_db:
                con, cur, _ = get_mysql()
                cur.execute(q, list(insert_map.values()))
                con.commit()
                con.close()
            with open('REPORT.db', 'a') as fp:
                fp.write(json.dumps(insert_map))

            with open('REPORT.md', 'a') as fp:
                fp.write(f'\n\n### {ds.name}  -  {accuracy_function_name}')
                fp.write(f'\nAccuracy: {accuracy}')
                fp.write(f'\nRuntime : {runtime}')
                fp.write(f'\nCommit : {lightwood_commit}')
                fp.write(f'\nVersion : {lightwood_version}')
                fp.write(f'\nNum folds : {ds.num_folds}')
                fp.write(f'\nPer-fold accuracy : {accuracy_per_fold}')
                fp.write(f'\nPredictions per mixer: {accuracy_per_mixer_map}')

        print(f'Inserted results for dataset {ds.name}')
    except Exception as e:
        print(f'Exception {e} | When running dataset {ds.name}')
        print(traceback.format_exc())


@ray.remote(num_gpus=0.5)
def run_datasets_remote(ds, lightwood_version, accuracy_data, lightwood_commit, is_dev, use_db):
    return run_dataset(ds, lightwood_version, accuracy_data, lightwood_commit, is_dev, use_db)


def main():
    args = setup_args()

    if args.use_db:
        setup_mysql()

    with open('REPORT.md', 'w') as fp:
        now = str(datetime.datetime.now()).split('.')[0]   
        fp.write(f'# Benchmark report\n\nRan on: {now}\nDatasets: {[x.name for x in args.datasets]}')

    with open('REPORT.db', 'w') as fp:
        fp.write('')

    print('=' * 20)
    
    print(f'Running benchmarks on {len(args.datasets)} datasets')

    if args.lightwood is None:
        raise Exception('Please specify lightwood version unless comparing!')
    elif args.lightwood == '#env':
        lightwood_commit = get_commit()
    elif args.lightwood == '#latest':
        assert 0 == os.system('pip3 install lightwood')
        lightwood_commit = 'unknown'
    elif args.lightwood is not None:
        assert 0 == os.system('pip3 install git+git://github.com/mindsdb/lightwood.git@{args.lightwood}')
        lightwood_commit = args.lightwood
    else:
        raise Exception('Please specify lightwood version unless comparing!')

    import lightwood
    importlib.reload(lightwood)
    lightwood_version = lightwood.__version__

    accuracy_data = None
    if args.use_db:
        accuracy_data = Framework_lightwood().get_accuracy_groups()

    from lightwood.helpers.device import get_devices
    _, nr_gpus = get_devices()

    if args.use_ray:
        ray.init()
        ray_obj_ids = []
        for i, ds in enumerate(args.datasets):
            if len(ray_obj_ids) > nr_gpus * 2:
                num_ready = i - nr_gpus * 2
                ray.wait(ray_obj_ids, num_returns=num_ready)

            obj_id = run_datasets_remote.remote(ds, lightwood_version, accuracy_data, lightwood_commit, args.is_dev, args.use_db)
            ray_obj_ids.append(obj_id)
        
        for obj_id in ray_obj_ids:
            ray.get(obj_id)
        ray.shutdown()
    else:
        for i, ds in enumerate(args.datasets):
            run_dataset(ds, lightwood_version, accuracy_data, lightwood_commit, args.is_dev, args.use_db)

    print('=' * 20)


if __name__ == '__main__':
    main()
