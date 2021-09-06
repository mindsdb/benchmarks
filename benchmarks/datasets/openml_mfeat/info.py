from benchmarks.helpers.accuracy import balanced_accuracy_score, log_loss
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    num_folds = None
    accuracy_functions = [balanced_accuracy_score, log_loss]
    file = 'data.csv'
    active = True
    target = 'class'
    source = 'https://www.openml.org/d/12'
    license = 'Public Domain Mark 1.0'
    is_open_license = True
    sota_accuracy = None
    learn_kwargs = {'advanced_args': {'disable_column_importance': True}}
