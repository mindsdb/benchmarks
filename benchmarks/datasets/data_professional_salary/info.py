from benchmarks.helpers.accuracy import r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression']
    file = 'data.csv'
    active = True
    accuracy_functions = [r2_score]
    target = 'SalaryUSD'
    source = 'https://www.brentozar.com/archive/2020/01/the-2020-data-professional-salary-survey-results-are-in/'
    license = 'Unlicense'
    is_open_license = True
    learn_kwargs = {}
    num_folds = None
