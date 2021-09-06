from benchmarks.helpers.accuracy import r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression']
    learn_kwargs = {}
    num_folds = None
    accuracy_functions = [r2_score]
    file = 'data.csv'
    active = True
    target = 'LowQN'
    source = 'https://github.com/amitkaps/weed/blob/master/data/Weed_Price.csv'
    license = 'MIT License'
    is_open_license = True
