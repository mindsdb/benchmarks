from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score]
    target = 'insuranceclaim'
    source = 'https://www.kaggle.com/mirichoi0218/insurance'
    license = 'Open Data Commons'
    is_open_license = True
    sota_accuracy = 0.822439024390244
    learn_kwargs = {}
    num_folds = 5
