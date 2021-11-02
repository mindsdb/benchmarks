from benchmarks.helpers.accuracy import balanced_accuracy_score, roc_auc
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score, roc_auc]
    target = 'DEERNet fit'
    source = 'https://ethz.ch/content/dam/ethz/special-interest/chab/physical-chemistry/epr-dam/documents/software/deer-15-on/DeerAnalysis2021b.zip'
    license = 'Public Domain Mark 1.0'
    is_open_license = True
    sota_accuracy = None
    learn_kwargs = {}
    num_folds = None