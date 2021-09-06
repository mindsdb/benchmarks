from benchmarks.helpers.accuracy import balanced_accuracy_score, log_loss
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    learn_kwargs = {}
    num_folds = 5
    accuracy_functions = [balanced_accuracy_score, log_loss]
    file = 'data.csv'
    active = True
    target = 'Class'
    source = 'https://www.openml.org/d/54'
    license = 'Public Domain Mark 1.0'
    is_open_license = True