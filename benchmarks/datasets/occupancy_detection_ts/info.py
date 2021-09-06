from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification', 'timeseries']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score]
    target = 'Occupancy'
    source = 'https://archive-beta.ics.uci.edu/ml/datasets/357'
    license = 'Creative Commons Attribution 4.0 International (CC BY 4.0)'
    is_open_license = True
    learn_kwargs = {'timeseries_settings': {'order_by': ['date'],
                                            'window': 5,
                                            'use_previous_target': True}}
    num_folds = None