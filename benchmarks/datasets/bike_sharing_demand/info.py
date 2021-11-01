from benchmarks.helpers.accuracy import inverse_reverse_smape, array_r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression', 'timeseries']
    file = 'train.csv'
    active = True
    accuracy_functions = [inverse_reverse_smape, array_r2_score]
    target = 'count'
    source = 'https://www.kaggle.com/c/bike-sharing-demand/data'
    license = 'Capital Bikeshare Data License Agreement (https://www.capitalbikeshare.com/data-license-agreement)'
    is_open_license = True
    learn_kwargs = {'timeseries_settings': {'order_by': ['datetime'],
                                            'window': 12,  # hours
                                            'nr_predictions': 6,  # months
                                            'use_previous_target': True}}
    num_folds = None
