from sklearn.metrics import accuracy_score
from benchmarks.helpers.confidence import confidence_from_acc_v1

file = 'wine_reviews.csv'
speed = 'fast'
active = True
accuracy_function = accuracy_score
confidence_function = confidence_from_acc_v1
target = 'points'
