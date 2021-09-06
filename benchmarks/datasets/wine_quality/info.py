from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['text', 'classification']
    learn_kwargs = {}
    num_folds = None
    accuracy_functions = [balanced_accuracy_score]
    file = 'data.csv'
    active = True
    target = 'quality'
    source = 'https://archive-beta.ics.uci.edu/ml/datasets/186'
    license = 'Creative Commons Attribution 4.0 International (CC BY 4.0)'
    is_open_license = True