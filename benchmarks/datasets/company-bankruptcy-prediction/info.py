from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['business', 'classification', 'economics', 'banking', 'categorical data']
    license = 'CC0: Public Domain'
    is_open_license = True
    accuracy_functions = [balanced_accuracy_score]
    file = 'data.csv'
    active = True
    target = 'Category'
    source = 'https://www.kaggle.com/fedesoriano/company-bankruptcy-prediction'
