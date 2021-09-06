from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['text', 'classification']
    learn_kwargs = {}
    num_folds = None
    accuracy_functions = [balanced_accuracy_score]
    file = 'data.csv'
    active = True
    target = 'Rating'
    source = 'https://www.kaggle.com/andrewmvd/trip-advisor-hotel-reviews'
    license = 'Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)'
    is_open_license = True
