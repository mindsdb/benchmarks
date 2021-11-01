from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score]
    target = 'anomaly'
    source = 'https://github.com/rtu715/NAS-Bench-360'
    license = 'MIT'
    is_open_license = True
    learn_kwargs = {}
    num_folds = None
