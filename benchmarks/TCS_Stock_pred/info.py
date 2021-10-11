from benchmarks.helpers.accuracy import r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression']
    file = 'data.csv'
    active = True
    target = 'concrete_strength'
    accuracy_functions = [r2_score]
    source = 'https://www.kaggle.com/abhimaneukj/tcs-dataset-from-2015-to-2021/version/1'
    license = 'Creative Commons Attribution 4.0 International (CC BY 4.0)'
    is_open_license = True
    learn_kwargs = {}
    num_folds = 5