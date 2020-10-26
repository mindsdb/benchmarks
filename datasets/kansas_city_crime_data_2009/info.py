from sklearn.metrics import accuracy_score
from benchmarks.helpers.confidence import confidence_from_acc_v1

file = 'KCPD_Crime_Data.csv'
speed = 'fast'
active = True
accuracy_function = accuracy_score
confidence_function = confidence_from_acc_v1
target = 'Firearm Used Flag'
