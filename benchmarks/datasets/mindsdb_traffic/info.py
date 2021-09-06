from benchmarks.helpers.accuracy import r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression']
    file = 'data.csv'
    active = True
    accuracy_functions = [r2_score]
    target = 'Github download clicks'
    license = 'Minsdb owned'
    source = 'internal'
    is_open_license = True
    learn_kwargs = {}
    num_folds = None