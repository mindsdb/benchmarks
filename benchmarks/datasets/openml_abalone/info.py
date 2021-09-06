from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score]
    target = 'Class_number_of_rings'
    source = 'https://www.openml.org/d/183'
    license = 'Public Domain Mark 1.0'
    is_open_license = True
    learn_kwargs = {}
    num_folds = None
