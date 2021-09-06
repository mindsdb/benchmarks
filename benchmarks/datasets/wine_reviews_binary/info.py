from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['text', 'classification']
    learn_kwargs = {}
    num_folds = None
    accuracy_functions = [balanced_accuracy_score]
    file = 'data.csv'
    active = True
    target = 'label'
    source = 'https://www.kaggle.com/zynicide/wine-reviews?select=winemag-data_first150k.csv'
    license = 'Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)'
    is_open_license = True
