from benchmarks.datasets.dataset import DatasetInterface
from benchmarks.helpers.accuracy import inverse_reverse_smape, array_r2_score


class Dataset(DatasetInterface):
    tags = ['regression', 'timeseries']
    file = 'data.json'
    active = True
    accuracy_functions = [inverse_reverse_smape, array_r2_score]
    target = 'Statistics.Flights.Delayed'
    source = 'https://github.com/RealTimeWeb/datasets/tree/master/datasets/json/airlines'
    license = 'GNU General Public License v2.0'
    is_open_license = True
    learn_kwargs = {'timeseries_settings': {'order_by': ['Time.Label'], 
                                            'window': 6,  # last semester
                                            'nr_predictions': 3,  # next quarter
                                            'use_previous_target': True}, 
                    'advanced_args': {'disable_column_importance': True}}
    num_folds = None