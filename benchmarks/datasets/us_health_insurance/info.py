from benchmarks.helpers.accuracy import r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression']
    learn_kwargs = {}
    num_folds = None
    accuracy_functions = [r2_score]
    file = 'data.csv'
    active = True
    target = 'charges'
    source = 'https://www.kaggle.com/teertha/ushealthinsurancedataset'
    license = 'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    is_open_license = True
