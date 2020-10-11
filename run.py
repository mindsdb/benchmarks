import json
import argparse
import os
import sys
import inspect
import time
import random
import importlib
import uuid
from copy import deepcopy
import traceback

import numpy as np
import pandas as pd


sys.path.insert(0,
                os.path.dirname(os.path.join(
                os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
                ))

from benchmarks.helpers.db import get_mysql, setup_mysql


def insert_results(results):
    con, cur, cfg = get_mysql()

    for result in results:
        keys = [k for k in result if k != 'mode']
        values = [result[k] for k in result if k != 'mode']
        ses = ','.join(['%s'] * len(keys))
        keys_str = ','.join(keys)
        table = result['mode']

        q = f"""INSERT INTO benchmarks.{table} ({keys_str}) VALUES ({ses})"""
        cur.execute(q,values)

    con.commit()
    con.close()


def setup_args():
    parser = argparse.ArgumentParser(description='CL argument for mindsdb server')
    parser.add_argument('--speed', type=str, default='fast,medium,slow')
    parser.add_argument('--platform', type=str, default='local')
    parser.add_argument('--modes', type=str, default='mindsdb_dev')
    parser.add_argument('--branch', type=str, default='staging')
    parser.add_argument('--datasets', type=str, default=None)
    parser.add_argument('--ignore_datasets', type=str, default='')
    parser.add_argument('--save', type=str, default='True')

    args, unknown = parser.parse_known_args()
    if len(unknown) > 0:
        print(f'Unknown arguments: {unknown}')
        exit()

    args.speed = args.speed.split(',')
    args.modes = args.modes.split(',')
    if args.datasets is not None:
        args.datasets = args.datasets.split(',')

    if args.save in [0, '0', 'False', 'false']:
        args.save = False
    else:
        args.save = True

    args.ignore_datasets = args.ignore_datasets.split(',')

    supported_modes = ['mindsdb_prod', 'mindsdb_dev', 'sklearn', 'pycaret', 'sota']
    for mode in args.modes:
        if mode not in supported_modes:
            raise Exception(f'Running mode {mode} not in supported running modes: {supported_modes}')

    if args.platform != 'local':
        raise Exception('Running locally is the only supported method at the moment !(Please bother Zoran/backend if you need to run on AWS or GCP or go ahead and implement is, some of the scafolding exists in the `remote_running` dir)')

    return args


def main():
    batch_id = uuid.uuid4().hex
    args = setup_args()
    #if args.save:
        #setup_mysql()

    current_dir = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0]
    dataset_dir = os.path.join(current_dir,'datasets')

    dataset_arr = []
    for name in os.listdir(dataset_dir):
        try:
            info = importlib.import_module(f'datasets.{name}.info')
        except ImportError:
            print('[info] Dataset {} doesn\'t contain info.py'.format(name))
            continue

        file = os.path.join(
            dataset_dir,
            name,
            info.file if hasattr(info, 'file') else 'data.csv'
        )

        if info.speed in args.speed and info.active:
            if (args.datasets is None or name in args.datasets) and name not in args.ignore_datasets:
                dataset_arr.append({
                    'name': name
                    ,'accuracy_function': info.accuracy_function
                    ,'confidence_function': info.confidence_function
                    ,'file': file
                    ,'ignore': info.ignore if hasattr(info, 'ignore') else []
                    ,'target': info.target
                    ,'learn_kwargs': info.learn_kwargs if hasattr(info, 'learn_kwargs') else {}
                    ,'source': info.source if hasattr(info, 'source') else None
                    ,'sota_accuracy': info.sota_accuracy if hasattr(info, 'sota_accuracy') else None
                })

    results = []
    for dataset in dataset_arr:
        print(f'Running for dataset: ' + dataset['name'])

        df = pd.read_csv(dataset['file'])
        df.drop(dataset['ignore'], axis='columns', inplace=True)

        np.random.seed(3532328)
        random.seed(283081)

        split_mask = np.random.rand(len(df)) < 0.9
        df_train = df[split_mask]
        df_test = df[~split_mask]

        for mode in args.modes:
            started_at = time.time()
            dataset_name = dataset['name']

            confidence_accuracy = None
            source = None
            if 'mindsdb' in mode:
                try:
                    from mdb.benchmark import run as run_mindsdb
                    accuracy, confidence_accuracy = run_mindsdb(
                        dataset_name,
                        deepcopy(df),
                        deepcopy(split_mask),
                        dataset['accuracy_function'],
                        dataset['confidence_function'],
                        dataset['target'],
                        train=True,
                        learn_kwargs=dataset['learn_kwargs']
                    )
                    if confidence_accuracy is None:
                        confidence_accuracy = 0
                except Exception as e:
                    traceback.print_exc()
                    print(e)
                    print('\n---------------\n')
                    print(f'Failed to run mindsdb on dataset: {dataset_name}. See exception above.')
                    print('\n---------------\n')
                    continue

            elif mode == 'pycaret':
                try:
                    print(f'Running for dataset {dataset_name}')
                    from benchmarks.alternatives.pycaret.benchmark import run_pycaret
                    accuracy = run_pycaret(
                        dataset_name,
                        deepcopy(df_train),
                        deepcopy(df_test),
                        dataset['accuracy_function'],
                        dataset['target']
                    )
                except:
                    traceback.print_exc()
                    print('\n---------------\n')
                    print(f'Failed to run pycaret on dataset: {dataset_name}. See exception above.')
                    print('\n---------------\n')
                    continue
            elif mode == 'sota':
                try:
                    accuracy = dataset['sota_accuracy']
                    source = dataset['source']
                    assert accuracy != None
                    assert source != None
                except:
                    traceback.print_exc()
                    print('\n---------------\n')
                    print(f'Failed to insert SOTA for dataset: {dataset_name}. See exception above.')
                    print('\n---------------\n')
                    continue
            else:
                try:
                    run = importlib.import_module(f'benchmarks.alternatives.{mode}.{dataset_name}.benchmark').run
                except ImportError:
                    print(f'Dataset {dataset_name} doesn\'t have an implementation for {mode}, if you want one please add it to `alternatives/{mode}/{dataset_name}/benchmark.py`')
                    continue

                try:
                    accuracy = run(
                        dataset_name,
                        deepcopy(df_train),
                        deepcopy(df_test),
                        dataset['accuracy_function'],
                        dataset['target']
                    )
                except Exception as e:
                    traceback.print_exc()
                    print(e)
                    print('\n---------------\n')
                    print(f'Failed to run mindsdb on dataset: {dataset_name}. See exception above.')
                    print('\n---------------\n')
                    continue

            runtime = time.time() - started_at

            try:
                if np.isnan(float(accuracy)):
                    accuracy = 0
            except:
                print(f'Malformed accuracy: {accuracy}')
                accuracy = 0

            result = {
                'runtime': runtime
                ,'batch_id': batch_id
                ,'mode': mode
                ,'dataset': dataset['name']
                ,'accuracy': accuracy
                ,'accuracy_function': dataset['accuracy_function'].__name__
            }

            if confidence_accuracy is not None:
                result['confidence_accuracy'] = confidence_accuracy
                result['confidence_accuracy_function'] = dataset['confidence_function'].__name__

            if source is not None:
                result['source'] = source

            if 'mindsdb' in mode:
                import lightwood
                import mindsdb_native

                result['native_version'] = mindsdb_native.__version__
                result['lightwood_version'] = lightwood.__version__

            if mode == 'mindsdb_dev':
                result['branch'] = args.branch

            if 'sklearn' in mode:
                import sklearn
                result['sklearn_version'] = sklearn.__version__

            if 'pycaret' in mode:
                import pycaret
                result['sklearn_version'] = pycaret.__version__

            print(f'\n\nIntermediary results: {results}\n\n')
            print('Legth of intermediary results: ' + str(len(results)))
            print('\n---------------------------------\n')

            results.append(result)
            if args.save:
                insert_results([results[-1]])
            else:
                print('Not inserting the results into the database')


    print(f'Results: \n------------\n{results}\n------------\n')


if __name__ == '__main__':
    main()
