from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['health', 'health conditions', 'public health', 'healthcare', 'binary classification']
    license = 'CC0: Public Domain'
    is_open_license = True
    accuracy_functions = [balanced_accuracy_score]
    file = 'healthcare-dataset-stroke-data.csv'
    active = True
    target = 'stroke'
    source = 'https://www.kaggle.com/fedesoriano/stroke-prediction-dataset'
