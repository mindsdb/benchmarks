from benchmarks.helpers.accuracy import inverse_reverse_smape, array_r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression', 'timeseries']
    file = 'data.csv'
    active = True
    accuracy_functions = [inverse_reverse_smape, array_r2_score]
    target = 'traffic_volume'
    source = 'https://archive-beta.ics.uci.edu/ml/datasets/492'
    license = 'Creative Commons Attribution 4.0 International (CC BY 4.0)'
    is_open_license = True
    learn_kwargs = {'timeseries_settings': {'order_by': ['date_time'], 
                                            'window': 12,  # hours
                                            'nr_predictions': 6,  # hours
                                            'use_previous_target': True}, 
                    'advanced_args': {'disable_column_importance': True}}
    num_folds = None