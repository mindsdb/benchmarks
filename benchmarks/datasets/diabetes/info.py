from benchmarks.helpers.accuracy import r2_accuracy_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ["classification"]
    file = "data.csv"
    active = True
    target = "Outcome"
    accuracy_functions = [r2_accuracy_score]
    source = "https://www.kaggle.com/uciml/pima-indians-diabetes-database"
    license = "CC0: Public Domain"
    is_open_license = True
    learn_kwargs = {}
    num_folds = 5
