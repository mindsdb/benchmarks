import mindsdb
from mindsdb_native import F
from lightwood.mixers import NnMixer
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from math import sqrt


# Ref: https://machinelearningmastery.com/time-series-datasets-for-machine-learning/


def rmse(trues, preds):
    mse = 0
    for t, p in zip(trues, preds):
        try:
            mse += (p - t)**2
        except TypeError:
            mse += (float(p) - float(t))**2
    mse /= len(trues)
    return sqrt(mse)


if __name__ == '__main__':
    path = "data.csv"
    name = 'MelbourneTemps'
    target = 'Temp'
    order_by = ['Date']
    window = 10
    train = True

    data = pd.read_csv(path, index_col=False)
    mdb = mindsdb.Predictor(name=name, log_level=10)

    if train:
        mdb.learn(from_data=data,
                to_predict=target,
                use_gpu=True,
                # stop_training_in_x_seconds=1,
                timeseries_settings={'order_by': order_by,
                                    'window': window,
                                    'nr_predictions': 1,  # 5
                                    'use_previous_target': True,  # False
                                    },
                #advanced_args={'force_predict': True,
                #                'mixer_class': NnMixer}
                )

    r = mdb.predict(when_data=data)

    for t, p in zip(r._data[f'__observed_{target}'], r._data[f'{target}']):
        print(f"real: {t} v/s {p} : pred")

    plt.xlabel(f"Results for {data}")
    plt.plot(r._data[f'__observed_{target}'], label='real')
    plt.plot(r._data[f'{target}'], label='predicted')
    plt.legend(loc='upper left')
    plt.show()

    print(f"RMSE: {rmse(r._data[f'__observed_{target}'], r._data[f'{target}'])}")
    print(f"Confusion Matrix:\n{confusion_matrix(r._data[f'__observed_{target}'], r._data[f'{target}'])}")

