from benchmarks.helpers.accuracy import r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression']
    learn_kwargs = {}
    num_folds = None
    accuracy_functions = [r2_score]
    file = 'data.csv'
    active = True
    target = 'price'
    # file: audi.csv
    source = 'https://www.kaggle.com/adityadesai13/used-car-dataset-ford-and-mercedes'
    license = 'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    is_open_license = True
    # Used solution: https://www.kaggle.com/adityadesai13/audi-car-price-prediction-model-score-0-96
    # model: RandomForestRegressor
    # accuracy function: r2_score
    sota_accuracy = 0.9497231960759135
