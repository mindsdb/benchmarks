from benchmarks.helpers.accuracy import r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['text', 'regression']
    learn_kwargs = {}
    num_folds = None
    accuracy_functions = [r2_score]
    file = 'data.csv'
    active = True
    target = 'points'
    source = 'https://www.kaggle.com/zynicide/wine-reviews?select=winemag-data_first150k.csv'
    license = 'Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)'
    is_open_license = True
