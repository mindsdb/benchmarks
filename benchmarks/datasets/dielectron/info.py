from benchmarks.datasets.dataset import DatasetInterface
from benchmarks.helpers.accuracy import r2_score


class Dataset(DatasetInterface):
    tags = ['regression', 'physics']
    file = 'data.csv'
    active = True
    accuracy_functions = [r2_score]
    target = 'M'
    source = 'https://opendata.cern.ch/record/304'
    license = 'Creative Commons CC0 waiver'
    is_open_license = True
    learn_kwargs = {'advanced_args': {'disable_column_importance': True}}
    num_folds = None
