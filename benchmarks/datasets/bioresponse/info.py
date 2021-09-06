from sklearn.metrics import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score]
    target = 'target'
    source = 'https://datahub.io/machine-learning/bioresponse'
    license = 'Open Data Commons Public Domain Dedication and License (PDDL)'
    is_open_license = True
    strict_mode = False
    learn_kwargs = {}
    num_folds = None