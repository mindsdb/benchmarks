import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, LabelEncoder
from pandas.api.types import is_numeric_dtype
import pandas as pd

def sane_is_nan(x):
    try:
        return np.isnan(x)
    except:
        try:
            return np.isnan(float(x))
        except:
            return False


def normalize(df, target, encoder_map=None):
    if encoder_map is None:
        encoder_map = {}
    for col in df.columns:
        if not is_numeric_dtype(df[col]):
            df[col] = [x if not sane_is_nan(x) else 'None' for x in df[col]]
            if col == target:
                if col not in encoder_map:
                    enc = LabelEncoder()
                    enc.fit(list(df[col]))
                    encoder_map[col] = enc
                else:
                    enc = encoder_map[col]

                encoded = enc.transform([x for x in df[col]])
                df[col] = encoded

            else:
                if (len(df[col]) < 1.01*len(set(df[col]))) or len(set(df[col])) > 4000:
                    del df[col]
                    continue
                if col not in encoder_map:
                    enc = OneHotEncoder(handle_unknown='ignore')
                    enc.fit([[x] for x in df[col]])
                    encoder_map[col] = enc
                else:
                    enc = encoder_map[col]

                encoded = enc.transform([[x] for x in df[col]]).toarray()
                encoded = [list(x) for x in encoded]
                df[col] = encoded
        else:
            df[col] = [x if not sane_is_nan(x) else 0 for x in df[col]]
            if col == target:
                pass
            else:
                enc = MinMaxScaler()
                enc.fit([[x] for x in df[col]])
                encoded = enc.transform([[x] for x in df[col]])
                encoded = [x[0] for x in encoded]
                df[col] = encoded

    return df, encoder_map

def to_np(df, target):
    Y = np.array(df[target])

    X = []
    for i in range(len(df)):
        Xm = []
        for col in df:
            if col == target:
                continue
            try:
                Xm.extend(df.iloc[i][col])
            except:
                Xm.append(df.iloc[i][col])
        X.append(Xm)
    X = np.array(X)
    return X, Y
