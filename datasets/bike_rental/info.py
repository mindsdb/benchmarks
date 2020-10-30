from sklearn.metrics import r2_score
from benchmarks.helpers.confidence import confidence_from_acc_v1

file = 'bike.csv'
speed = 'fast'
active = True
accuracy_function = r2_score
confidence_function = confidence_from_acc_v1
target = 'count'
