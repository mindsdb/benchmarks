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


CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
DATASETS_DIR = os.path.join(CURRENT_DIR, os.path.join('benchmarks','datasets'))


def fit_and_infer_w_native(df_train: pd.DataFrame, df_test: pd.DataFrame, problem_definition: object) -> Tuple[list, list, float]:
    import mindsdb_native
    from mindsdb_native.libs.constants.mindsdb import DATA_TYPES, DATA_SUBTYPES
    
    started = time.time()

    predictor = mindsdb_native.Predictor(name='a_random_name')

    learn_kwargs = {}
    if 'timeseries_settings' in problem_definition:
        learn_kwargs['timeseries_settings'] = problem_definition['timeseries_settings']
    learn_kwargs['advanced_args'] = {}
    learn_kwargs['advanced_args']['deduplicate_data'] = False
    learn_kwargs['advanced_args']['force_predict'] = True
    learn_kwargs['advanced_args']['debug'] = True
    learn_kwargs['advanced_args']['disable_column_importance'] = True

    predictor.learn(from_data=df_train, to_predict=problem_definition['target'], **learn_kwargs)

    target = problem_definition['target']
    try:
        df_test = df_test[df_test['make_predictions']]
    except KeyError:
        pass

    real_values = [x for x in df_test[target]]
        
    raw_predictions = predictor.predict(when_data=df_test)
    predictions = [x.explanation for x in raw_predictions]
    predictions = [x[target]['predicted_value'] for x in predictions]

    if predictor.transaction.lmd['stats_v2'][target]['typing']['data_type'] == DATA_TYPES.CATEGORICAL:
        predictions = [str(x) for x in predictions]
        real_values = [str(x) for x in real_values]
    elif predictor.transaction.lmd['stats_v2'][target]['typing']['data_subtype'] == DATA_SUBTYPES.INT:
        predictions = [int(x) for x in predictions]
        real_values = [int(x) for x in real_values]
    elif predictor.transaction.lmd['stats_v2'][target]['typing']['data_subtype'] == DATA_SUBTYPES.FLOAT:
        predictions = [float(x) for x in predictions]
        real_values = [float(x) for x in real_values]

    return predictions, real_values, int(time.time() - started)


def fit_and_infer_w_lightwood(df_train: pd.DataFrame, df_test: pd.DataFrame, problem_definition: object) -> Tuple[list, list, float]:
    import lightwood
    from lightwood import dtype
    from lightwood.api.high_level import predictor_from_problem
    
    started = time.time()
    predictor: lightwood.PredictorInterface = predictor_from_problem(df_train, problem_definition)
    predictor.learn(df_train)
    
    try:
        df_test = df_test[df_test['make_predictions']]
    except KeyError:
        pass

    output = predictor.predict(df_test)
    predictions = list(output['prediction'])
    target = problem_definition['target']
    real_values = df_test[target]

    if predictor.dtype_dict[target] in (dtype.categorical, dtype.binary):
        predictions = [str(x) for x in predictions]
        real_values = [str(x) for x in real_values]
    elif predictor.dtype_dict[target] in (dtype.integer):
        predictions = [int(x) for x in predictions]
        real_values = [int(x) for x in real_values]
    elif predictor.dtype_dict[target] in (dtype.float):
        predictions = [float(x) for x in predictions]
        real_values = [float(x) for x in real_values]

    return predictions, real_values, int(time.time() - started)


def setup_args():
    parser = argparse.ArgumentParser(description='Args for the mindsdb benchmark suite')
    parser.add_argument('--platform', type=str, default='local')
    parser.add_argument('--datasets', type=str, default=None) # comma separated lists of datasets to run | special values: openml runs all openml datasets
    parser.add_argument('--lightwood', type=str, default=None) # env | #latest | branch name | commit hash | None
    parser.add_argument('--use_ray', type=str, default='1') # 1 to use, 0 to not use
    parser.add_argument('--use_native', type=str, default='0') # 1 to use, 0 to not use

    args, unknown = parser.parse_known_args()
    if len(unknown) > 0:
        print(f'Unknown arguments: {unknown}')
        exit()
    
    if args.use_ray in (False, 'false', 'False', 0, '0'):
        args.use_ray = False
    else:
        args.use_ray = True

    if args.use_native in (False, 'false', 'False', 0, '0'):
        args.use_native = False
    else:
        args.use_native = True

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


def run_dataset(ds: DatasetInterface, lightwood_version: str, accuracy_data: dict, lightwood_commit: str, is_dev: bool, use_native: bool):
    try:
        print('=' * 6 + f'Running for dataset {ds.name}' + '=' * 6)

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
        if use_native:
            fit_and_infer = fit_and_infer_w_native
        else:
            fit_and_infer = fit_and_infer_w_lightwood

        if 'timeseries' in ds.tags:
            df_train, df_test = ts_ds_to_train_test(ds)
            predictions, real_values, runtime = fit_and_infer(df_train, df_test, problem_definition)
            for accuracy_function in ds.accuracy_functions:
                if accuracy_function not in requires_normal_predictions:
                    continue
                accuracy_map[accuracy_function.__name__] = accuracy_function(real_values, predictions)
        
        elif ds.num_folds is None:
            folds = ds_to_folds(ds, 5)
            predictions, real_values, runtime = fit_and_infer(pd.concat(folds[:4]), folds[4], problem_definition)
            for accuracy_function in ds.accuracy_functions:
                if accuracy_function not in requires_normal_predictions:
                    continue
                accuracy_map[accuracy_function.__name__] = accuracy_function(real_values, predictions)

        else:
            folds = ds_to_folds(ds, ds.num_folds)
            for i in range(len(folds)):
                df_test = folds[i]
                df_train = pd.concat(folds[:i] + folds[i+1:])
                predictions, real_values, runtime = fit_and_infer(df_train, df_test, problem_definition)
                
                for accuracy_function in ds.accuracy_functions:
                    if accuracy_function not in requires_normal_predictions:
                        continue
                    if accuracy_function.__name__ not in accuracy_map_per_fold:
                        accuracy_map_per_fold[accuracy_function.__name__] = []
                    accuracy_map_per_fold[accuracy_function.__name__].append(accuracy_function(real_values, predictions))
            
            for k in accuracy_map_per_fold:
                accuracy_map[k] = np.mean(accuracy_map_per_fold[k])
   
        for accuracy_function_name in accuracy_map:
            accuracy = accuracy_map[accuracy_function_name]
            accuracy_per_fold = None
            if accuracy_function_name in accuracy_map_per_fold:
                accuracy_per_fold = ','.join([str(x) for x in accuracy_map_per_fold[accuracy_function_name]])

            print(f'\n\nGot accuracy: {accuracy} ({accuracy_function_name}) [per fold: {accuracy_per_fold}] for {ds.name}\n\n')

            q = 'INSERT INTO benchmarks.v4 (dataset, accuracy, accuracy_function, runtime, lightwood_version, lightwood_commit, is_dev, num_folds, accuracy_per_fold) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'

            con, cur, _ = get_mysql()
            cur.execute(q, (
                ds.name,
                accuracy,
                accuracy_function_name,
                runtime,
                lightwood_version,
                lightwood_commit,
                is_dev,
                ds.num_folds,
                accuracy_per_fold
            ))
            con.commit()
            con.close()

        print(f'Inserted results for dataset {ds.name}')
    except Exception as e:
        print(f'Exception {e} | When running dataset {ds.name}')
        print(traceback.format_exc())


@ray.remote(num_gpus=0.5)
def run_datasets_remote(ds, lightwood_version, accuracy_data, lightwood_commit, is_dev, use_native: bool):
    return run_dataset(ds, lightwood_version, accuracy_data, lightwood_commit, is_dev, use_native)


def main():
    setup_mysql()
    args = setup_args()
    print('=' * 20)
    
    print(f'Running benchmarks on {len(args.datasets)} datasets')

    if args.use_native:
        lightwood_version = 'Native 2.48.0'
        lightwood_commit = 'Native 2.48.0'
        is_dev = False
    else:
        # @TODO: Run lightwood here
        if args.lightwood is None:
            raise Exception('Please specify lightwood version unless comparing!')
        elif args.lightwood == '#env':
            lightwood_commit = get_commit()
            is_dev = True
        elif args.lightwood == '#latest':
            assert 0 == os.system('pip3 install lightwood')
            lightwood_commit = 'unknown'
            is_dev = False
        elif args.lightwood is not None:
            assert 0 == os.system('pip3 install git+git://github.com/mindsdb/lightwood.git@{args.lightwood}')
            lightwood_commit = args.lightwood
            is_dev = True
        else:
            raise Exception('Please specify lightwood version unless comparing!')

        import lightwood
        importlib.reload(lightwood)
        lightwood_version = lightwood.__version__

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

            obj_id = run_datasets_remote.remote(ds, lightwood_version, accuracy_data, lightwood_commit, is_dev, args.use_native)
            ray_obj_ids.append(obj_id)
        
        for obj_id in ray_obj_ids:
            ray.get(obj_id)
        ray.shutdown()
    else:
        for i, ds in enumerate(args.datasets):
            run_dataset(ds, lightwood_version, accuracy_data, lightwood_commit, is_dev, args.use_native)

    print('=' * 20)
    


if __name__ == '__main__':
    main()
