from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score]
    target = 'target'
    source = 'https://archive-beta.ics.uci.edu/ml/datasets/52'
    license = 'Creative Commons Attribution 4.0 International (CC BY 4.0)'
    is_open_license = True
    learn_kwargs = {}
    num_folds = 5
