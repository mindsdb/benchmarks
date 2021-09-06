from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    learn_kwargs = {}
    num_folds = None
    accuracy_functions = [balanced_accuracy_score]
    file = 'data.csv'
    active = True
    target = 'Claim'
    source = 'https://www.kaggle.com/mhdzahier/travel-insurance'
    license = 'Open Data Commons Open Database License (ODbL) v1.0'
    is_open_license = True
