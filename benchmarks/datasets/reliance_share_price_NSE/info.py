from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['business','finance', 'investing', 'exploratory', 'data analysis', 'regression']
    learn_kwargs = {}
    num_folds = None
    accuracy_functions = [balanced_accuracy_score]
    file = 'data.csv'
    active = True
    target = 'High'
    source = 'https://www.kaggle.com/lazycoder00/tcsdataset'
    license = 'CC0: Public Domain'
    is_open_license = True
