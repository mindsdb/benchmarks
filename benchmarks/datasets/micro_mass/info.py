from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score]
    target = 'Class'
    source = 'https://archive-beta.ics.uci.edu/ml/datasets/253'
    license = 'Creative Commons Attribution 4.0 International (CC BY 4.0)'
    is_open_license = True

    # Used solution: https://www.openml.org/t/9950
    # model: sklearn.RandomForestClassifier
    sota_accuracy = 0.9177
    learn_kwargs = {}
    num_folds = None