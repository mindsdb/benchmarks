import numpy as np


def within_range_acc(Y_exp, Y):
    correct_arr = []
    for i in range(len(Y_exp)):
        correct = Y_exp[i]['confidence_interval'][0] < Y[i] < Y_exp[i]['confidence_interval'][1]
        correct_arr.append(correct)
    return np.mean(correct_arr)
