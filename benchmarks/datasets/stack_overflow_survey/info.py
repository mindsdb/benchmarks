from benchmarks.helpers.accuracy import r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression']
    learn_kwargs = {}
    num_folds = None
    accuracy_functions = [r2_score]
    file = 'data.csv'
    active = True
    target = 'Salary'
    source = 'https://www.kaggle.com/stackoverflow/so-survey-2017'
    license = 'Open Database License (ODbL) 1.0'
    is_open_license = True