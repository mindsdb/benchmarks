def run(name, df_train, df_test, acc_func, target):
    from sklearn.linear_model import LinearRegression
    from benchmarks.helpers.sklearn_helpers import normalize, to_np

    model = LinearRegression()

    df_train, enc_map = normalize(df_train, target)
    X_train, Y_train = to_np(df_train, target)
    model.fit(X_train, Y_train)

    df_test, _ = normalize(df_test, target, enc_map)
    X_test, Y_test = to_np(df_test, target)
    predictions = model.predict(X_test)
    accuracy = acc_func(predictions, Y_test)

    return accuracy
