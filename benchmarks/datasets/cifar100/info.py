from benchmarks.datasets.dataset import DatasetInterface
from benchmarks.helpers.accuracy import accuracy_score


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [accuracy_score]
    target = 'class'
    source = 'https://www.cs.toronto.edu/~kriz/cifar.html'
    license = 'Unknown/Unlisted but literally everybody and their mom uses and hosts this so we should be fine'
    is_open_license = True
    # Also a good test to see if "time aim" works
    # Note: DO NOT change time aim, otherwise we'll bias the results, also 2 hours seems like a reasonable cap, I wouldn't want any dataset exceeding that
    learn_kwargs = {'advanced_args': {'disable_column_importance': True}, 'time_aim': 7200}
    num_folds = None
