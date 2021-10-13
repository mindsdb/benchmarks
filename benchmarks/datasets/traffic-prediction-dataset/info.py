from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['social science', 'automobiles and vehicles', 'transportation', 'time series analysis', 'pollution']
    license = 'CC0: Public Domain'
    is_open_license = True
    accuracy_functions = [balanced_accuracy_score]
    file = 'data.csv'
    active = True
    target = 'Junction'
    source = 'https://www.kaggle.com/fedesoriano/traffic-prediction-dataset'
    learn_kwargs = {'timeseries_settings': {'order_by': ['DateTime'], 
                                            'window': 24,
                                            'nr_predictions': 12,
                                            'use_previous_target': True}, 
                    'advanced_args': {} }
    num_folds = None
