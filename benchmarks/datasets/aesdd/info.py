from benchmarks.datasets.dataset import DatasetInterface
from benchmarks.helpers.accuracy import accuracy_score, balanced_accuracy_score


class Dataset(DatasetInterface):
    tags = ['classification']
    file = 'data.csv'
    active = True
    accuracy_functions = [accuracy_score, balanced_accuracy_score]
    target = 'emotion'
    source = 'http://m3c.web.auth.gr/research/aesdd-speech-emotion-recognition/'
    license = 'No license but says: Aced Emotional Speech Dynamic Database is a Speech Emotion Recognition Dataset publically available for research purposes.'
    is_open_license = True
    learn_kwargs = {'advanced_args': {'disable_column_importance': True}}
    num_folds = None
