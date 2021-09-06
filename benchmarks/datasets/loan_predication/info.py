from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score]
    target = 'Loan_Status'
    source = 'https://www.kaggle.com/ninzaami/loan-predication'
    license = 'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    is_open_license = True
    # Used solution: https://www.kaggle.com/bhavik1611/loan-status-predicition
    # model: LogisticRegression
    # f1_score is replaced with balanced_accuracy_score
    sota_accuracy = 0.708224
    learn_kwargs = {}
    num_folds = 5