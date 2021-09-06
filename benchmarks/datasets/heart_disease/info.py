from benchmarks.helpers.accuracy import balanced_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [balanced_accuracy_score]
    target = 'target'
    source = 'https://archive-beta.ics.uci.edu/ml/datasets/45'
    license = 'Creative Commons Attribution 4.0 International (CC BY 4.0)'
    is_open_license = True
    learn_kwargs = {}
    # Used solution: https://www.kaggle.com/ahmadjaved097/classifying-heart-disease-patients 
    # model: LogisticRegression
    # accuracy_score is replaced with balanced_accuracy_score
    sota_accuracy = 0.822439024390244
    num_folds = 5
