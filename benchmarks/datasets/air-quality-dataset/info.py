from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['earth and nature', 'health', 'science and technology', 'data analytics', 'weather', 'categorical data']
    license = 'CC0: Public Domain'
    is_open_license = True
    accuracy_functions = [balanced_accuracy_score]
    file = 'data.csv'
    active = True
    target = 'Temperature'
    source = 'https://www.kaggle.com/fedesoriano/air-quality-data-set'
    num_folds = None
    learn_kwargs = {'timeseries_settings': {'order_by': ['CO(GT)'], 
                                            'window': 24,
                                            'nr_predictions': 12,
                                            'use_previous_target': True}, 
                    'advanced_args': {}}
