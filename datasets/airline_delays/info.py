from benchmarks.helpers.accuracy import smape
from benchmarks.helpers.confidence import confidence_from_range_v1


file = 'data.json'
speed = 'medium'
active = True
accuracy_function = smape
confidence_function = confidence_from_range_v1
target = 'Statistics.Flights.Delayed'
learn_kwargs = {'timeseries_settings': {'order_by': ['time'], 
                                        'window': 5,
                                        'use_previous_target': True}, 
                'advanced_args': {'disable_column_importance': True}}
