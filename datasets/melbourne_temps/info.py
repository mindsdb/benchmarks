from benchmarks.helpers.accuracy import smape
from benchmarks.helpers.confidence import confidence_from_range_v1

# source: https://machinelearningmastery.com/time-series-datasets-for-machine-learning/
file = 'data.csv'
speed = 'medium'
active = True
accuracy_function = smape
confidence_function = confidence_from_range_v1
target = 'Temp'
learn_kwargs = {'timeseries_settings': {'order_by': ['Date'], 
                                        'window': 10,
                                        'use_previous_target': True}}
