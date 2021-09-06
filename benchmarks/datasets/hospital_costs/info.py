from benchmarks.helpers.accuracy import r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression']
    file = 'data.csv'
    active = True
    accuracy_functions = [r2_score]
    target = 'TOTCHG'
    source = 'https://www.kaggle.com/vik2012kvs/analyze-the-healthcare-cost-in-wisconsin-hospitals'
    license = 'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    is_open_license = True
    learn_kwargs = {}
    num_folds = 5
