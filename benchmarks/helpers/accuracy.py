from typing import List, Tuple

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from sklearn.metrics import r2_score as sk_r2_score, accuracy_score as r2_accuracy_score, balanced_accuracy_score as sk_balanced_accuracy_score


def r2_score(y_true, y_pred) -> float:
    """ Wrapper for sklearn R2 score, lower capped at 0. """
    for arr in (y_true, y_pred):
        for i in range(len(arr)):
            try:
                if arr[i] is None or np.isnan(arr[i]):
                    arr[i] = 0
                if np.isinf(arr[i]):
                    arr[i] = pow(2, 63)
            except Exception as e:
                print(f'Strange value {arr[i]} caused exception: {e}')
                arr[i] = 0
    acc = sk_r2_score(y_true, y_pred)
    return max(0, acc)


def accuracy_score(y_true, y_pred) -> float:
    """ Wrapper for sklearn accuracy_score """
    y_true = [str(x) for x in y_true]
    y_pred = [str(x) for x in y_pred]
    return r2_accuracy_score(y_true, y_pred)


def balanced_accuracy_score(y_true, y_pred) -> float:
    """ Wrapper for sklearn balanced_accuracy_score """
    y_true = [str(x) for x in y_true]
    y_pred = [str(x) for x in y_pred]
    return sk_balanced_accuracy_score(y_true, y_pred)


def binary_range_accuracy(y_true, y_pred_conf) -> float:
    """ Checks if true value is within confidence bounds in regression tasks """
    correct_arr = []
    for i in range(len(y_pred_conf)):
        correct = y_pred_conf[i][0] < y_true[i] < y_pred_conf[i][1]
        correct_arr.append(correct)
    return np.mean(correct_arr)


def delta_weighted_range_score(y_true, y_pred_conf) -> float:
    """
    Similar to binary_range_accuracy, introducing a corrective score
    based on the bound width and the true value magnitude
    """
    score_arr = []
    for i in range(len(y_pred_conf)):
        correct = float(y_pred_conf[i][0] < y_true[i] < y_pred_conf[i][1])
        score = correct * (y_pred_conf[i][1] - y_pred_conf[i][0]) / y_true[i]
        score_arr.append(score)
    return np.mean(score_arr)


def _ts_preprocess(y_true: List, y_pred: List[List]) -> Tuple[np.ndarray, np.ndarray, int]:
    """ Transform into np.ndarrays, get all true target windows, and remove last rows with incomplete target info
    :param y_true: list with `n_rows` data points, representing observed time series
    :param y_pred: list with `n_rows` sublists, each containing a forecast of length `nr_predictions`.
    :returns: true and predicted values reshaped to (n_rows, nr_predictions), as well as the (inferred)
    `nr_predictions` that determines the forecast horizon length.
    """
    if not isinstance(y_pred[0], list):
        y_pred = [[yp] for yp in y_pred]
    nr_preds = len(y_pred[0])

    y_pred = np.array(y_pred).reshape(-1, nr_preds)  # forecast
    y_true = np.array(y_true)  # truth
    y_true = sliding_window_view(y_true, window_shape=nr_preds, axis=0)
    # @TODO: remove rows w/ incomplete historical context
    y_pred = y_pred[:y_true.shape[0], :]  # only use datapoints with full label info

    return y_true, y_pred, nr_preds


def inverse_reverse_smape(y_true: List, y_pred: List) -> float:
    """
    For time series forecasting tasks.
    Returns (1 - symmetric mean absolute percentage error) mean over all timesteps.
    We use a sMAPE formulation such that it is unit-bounded, so 0 <= sMAPE(X) <= 1.
    """
    accs = []
    y_true, y_pred, nr_preds = _ts_preprocess(y_true, y_pred)

    for timestep in range(nr_preds):
        yt = y_true[:, timestep]
        yp = y_pred[:, timestep]
        abserr = np.sum(np.abs(yt - yp))
        magnitude = np.sum(np.abs(yt) + np.abs(yp))
        accs.append(1 - (abserr / magnitude))

    return np.average(accs)


def array_r2_score(y_true: List[List], y_pred: List[List]) -> float:
    """
    For time series forecasting tasks.
    Returns R2 score mean over all timesteps.
    """
    accs = []
    y_true, y_pred, nr_preds = _ts_preprocess(y_true, y_pred)

    for timestep in range(nr_preds):
        yt = y_true[:, timestep]
        yp = y_pred[:, timestep]
        acc = r2_score(yt, yp)
        accs.append(acc)

    return np.average(accs)


def log_loss() -> float:
    return 0.0


def roc_auc() -> float:
    return 0.0


def precssion_recall_score() -> float:
    return 0.0


def weighted_log_loss() -> float:
    return 0.0


def confidence_from_acc_v1(y_pred, y_true, acc_func) -> float:
    """ Computes (classification) model calibration based on comparing accuracy vs mean reported confidence """
    acc = acc_func([x['predicted_value'] for x in y_pred], y_true)
    conf_mean = np.mean([x['confidence'] for x in y_pred])

    return 1.0 - np.abs(acc - conf_mean)


def confidence_from_range_v1(y_pred, y_true) -> float:
    """ Computes (regression) model calibration based on comparing binary range accuracy vs mean reported confidence """
    acc = binary_range_accuracy(y_pred, y_true)
    conf_mean = np.mean([x['confidence'] for x in y_pred])

    return 1.0 - np.abs(acc - conf_mean)


def quantile_width(bounds) -> float:
    """ Returns mean confidence bound width """
    widths = [x[1] - x[0] for x in bounds]
    return np.mean(widths)


def quantile_correctness(y_pred, bounds) -> float:
    """
    Returns mean amount of rows where predicted value falls within predicted confidence bounds.
    Generally speaking, the expectation is for this score to be 1.0
    """
    hits = [x[0] <= y <= x[1] for x, y in zip(bounds, y_pred)]
    return np.mean(hits)


requires_normal_predictions = [r2_score, accuracy_score, balanced_accuracy_score, inverse_reverse_smape, array_r2_score]
requires_predict_proba = [log_loss, roc_auc, precssion_recall_score, weighted_log_loss]
requires_confidence_rang = [binary_range_accuracy, delta_weighted_range_score]
