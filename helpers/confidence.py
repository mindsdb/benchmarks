import numpy as np

from benchmarks.helpers.accuracy import within_range_acc


def confidence_from_acc_v1(Y_exp, Y, acc_func):
    acc = acc_func([x['predicted_value'] for x in Y_exp], Y)
    conf_mean = np.mean([x['confidence'] for x in Y_exp])

    return 1 - np.abs(acc - conf_mean)

def confidence_from_range_v1(Y_exp, Y):
    acc = within_range_acc(Y_exp, Y)
    conf_mean = np.mean([x['confidence'] for x in Y_exp])

    return 1 - np.abs(acc - conf_mean)
