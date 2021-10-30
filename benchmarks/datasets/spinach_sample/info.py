from benchmarks.helpers.accuracy import balanced_accuracy_score, roc_auc
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score, roc_auc]
    target = 'class'
    source = 'https://www.openml.org/d/1590'
    license = 'Public Domain Mark 1.0'
    is_open_license = True
    sota_accuracy = None
    learn_kwargs = {}
    num_folds = None