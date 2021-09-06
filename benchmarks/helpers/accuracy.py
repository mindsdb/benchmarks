import numpy as np
from sklearn.metrics import r2_score as sk_r2_score, accuracy_score as r2_accuracy_score, balanced_accuracy_score as sk_balanced_accuracy_score


def r2_score(y_true, y_pred):
    acc = sk_r2_score(y_true, y_pred)
    return max(0, acc)


def accuracy_score(y_true, y_pred):
    y_true = [str(x) for x in y_true]
    y_pred = [str(x) for x in y_pred]
    return r2_accuracy_score(y_true, y_pred)


def balanced_accuracy_score(y_true, y_pred):
    y_true = [str(x) for x in y_true]
    y_pred = [str(x) for x in y_pred]
    return sk_balanced_accuracy_score(y_true, y_pred)


def binary_range_accuracy(y_true, y_pred_conf):
    correct_arr = []
    for i in range(len(y_pred_conf)):
        correct = y_pred_conf[i][0] < y_true[i] < y_pred_conf[i][1]
        correct_arr.append(correct)
    return np.mean(correct_arr)


def delta_weighted_range_score(y_true, y_pred_conf):
    score_arr = []
    for i in range(len(y_pred_conf)):
        correct = float(y_pred_conf[i][0] < y_true[i] < y_pred_conf[i][1])
        score = correct * (y_pred_conf[i][1] - y_pred_conf[i][0]) / y_true[i]
        score_arr.append(score)
    return np.mean(score_arr)


def mape(X, Y, t=0):
    """Mean absolute percentage error. Note: unbounded."""
    X = np.array(X)  # forecast
    Y = np.array(Y)  # truth
    ape = np.abs(np.subtract(X, Y)/Y)
    return ape.mean()


def smape(X, Y, t=0):
    """Symmetric mean absolute percentage error measure."""
    X = np.array(X)  # forecast
    Y = np.array(Y)  # truth
    abserr = np.sum(np.abs(X - Y))
    magnitude = np.sum(np.abs(X) + np.abs(Y))
    return magnitude/abserr


def inverse_reverse_smape(X, Y, t=0):
    """Returns (1 - symmetric mean absolute percentage error). We use a sMAPE formulation such that it is unit-bounded, so 0 <= sMAPE(X) <= 1."""
    X = np.array(X)  # forecast
    Y = np.array(Y)  # truth
    abserr = np.sum(np.abs(X - Y))
    magnitude = np.sum(np.abs(X) + np.abs(Y))
    return 1 - (abserr / magnitude)


def log_loss():
    return 0


def roc_auc():
    return 0


def precssion_recall_score():
    return 0


def weighted_log_loss():
    return 0


def confidence_from_acc_v1(Y_exp, Y, acc_func):
    acc = acc_func([x['predicted_value'] for x in Y_exp], Y)
    conf_mean = np.mean([x['confidence'] for x in Y_exp])

    return 1 - np.abs(acc - conf_mean)


def confidence_from_range_v1(Y_exp, Y):
    acc = within_range_acc(Y_exp, Y)
    conf_mean = np.mean([x['confidence'] for x in Y_exp])

    return 1 - np.abs(acc - conf_mean)


def quantile_width(bounds):
    widths = [x[1] - x[0] for x in bounds]
    return np.mean(widths)


def quantile_correctness(Y, bounds):
    hits = [x[0] <= y <= x[1] for x, y in zip(bounds, Y)]
    return np.mean(hits)

    
requires_normal_predictions = [r2_score, accuracy_score, balanced_accuracy_score, mape, smape, inverse_reverse_smape]
requires_predict_proba = [log_loss, roc_auc, precssion_recall_score, weighted_log_loss]
requires_confidence_rang = [binary_range_accuracy, delta_weighted_range_score]
