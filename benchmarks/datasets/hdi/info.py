from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score]
    target = 'Development Index'
    source = 'https://data.humdata.org/dataset/human-development-index-hdi'
    license = 'Creative Commons Attribution for Intergovernmental Organisations'
    is_open_license = True
    learn_kwargs = {}
    num_folds = 5
