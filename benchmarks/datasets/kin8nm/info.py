from benchmarks.helpers.accuracy import r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression']
    file = 'data.csv'
    active = True
    target = 'y'
    source = 'https://www.openml.org/d/189'
    license = 'Public Domain Mark 1.0'
    is_open_license = True
    accuracy_functions = [r2_score]
    learn_kwargs = {}
    num_folds = None