from benchmarks.helpers.accuracy import r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression']
    file = 'data.csv'
    active = True
    target = 'concrete_strength'
    accuracy_functions = [r2_score]
    source = 'https://archive-beta.ics.uci.edu/ml/datasets/165'
    license = 'Creative Commons Attribution 4.0 International (CC BY 4.0)'
    is_open_license = True
    learn_kwargs = {}
    num_folds = 5