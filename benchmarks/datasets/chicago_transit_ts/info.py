from benchmarks.helpers.accuracy import inverse_reverse_smape, array_r2_score
from benchmarks.datasets.dataset import DatasetInterface


class Dataset(DatasetInterface):
    tags = ['regression', 'timeseries']
    file = 'CTA_2019_2020.csv'
    active = True
    accuracy_functions = [inverse_reverse_smape, array_r2_score]
    target = 'RIDES'
    source = 'https://data.cityofchicago.org/Transportation/CTA-Ridership-Bus-Routes-Daily-Totals-by-Route/jyb9-n7fm'
    license = 'Exact type TBD'
    is_open_license = True
    learn_kwargs = {'timeseries_settings': {'order_by': ['DATE'],
                                            'group_by': ['ROUTE'],
                                            'window': 14,  # three years
                                            'nr_predictions': 7,  # next year
                                            'use_previous_target': True}}
    num_folds = None
