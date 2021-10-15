from sklearn.metrics import r2_score
from benchmarks.helpers.confidence import confidence_from_range_v1

file = 'Sunspots.csv'
speed = 'fast'
active = True
accuracy_function = r2_score
confidence_function = confidence_from_range_v1
target = 'Monthly Mean Total Sunspot Number'