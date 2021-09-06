from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification', 'text']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score]
    learn_kwargs = {}
    target = 'Score'
    num_folds = None
    source = 'https://www.kaggle.com/snap/amazon-fine-food-reviews?select=Reviews.csv'
    license = 'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    is_open_license = True