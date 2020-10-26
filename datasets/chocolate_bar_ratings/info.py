from sklearn.metrics import accuracy_score
from benchmarks.helpers.confidence import confidence_from_acc_v1

file = 'data.csv'
speed = 'medium'
active = True
accuracy_function = accuracy_score
confidence_function = confidence_from_acc_v1
target = 'Rating'
