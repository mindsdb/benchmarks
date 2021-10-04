from benchmarks.helpers.accuracy import inverse_reverse_smape, array_r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression', 'timeseries']
    file = 'data.csv'
    active = True
    accuracy_functions = [inverse_reverse_smape, array_r2_score]
    target = 'Sunspots'
    source = 'https://www.kaggle.com/robervalt/sunspots'
    license = 'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    is_open_license = True
    learn_kwargs = {'timeseries_settings': {'order_by': ['Month'], 
                                            'window': 12,  # months
                                            'nr_predictions': 6,  # months
                                            'use_previous_target': True}}
    num_folds = None