from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    learn_kwargs = {}
    num_folds = 5
    accuracy_functions = [balanced_accuracy_score]
    file = 'data.csv'
    active = True
    target = 'Status'
    source = 'https://www.kaggle.com/rameessahlu/plantar-fasciitis'
    license = 'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    is_open_license = True
