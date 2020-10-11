def run(name, df, split_mask, acc_func, conf_func, target, train, learn_kwargs):
    import mindsdb_native
    import numpy as np

    train_indexes = []
    test_indexes = []
    validation_indexes = []
    for i, ele in enumerate(split_mask):
        if ele:
            if np.random.rand() < 0.9:
                train_indexes.append(i)
            else:
                test_indexes.append(i)
        else:
            validation_indexes.append(i)

    predictor = mindsdb_native.Predictor(name=name)
    if train:
        predictor.learn(from_data=df, to_predict=target, advanced_args = {'data_split_indexes': {
            'train_indexes': train_indexes
            ,'test_indexes': test_indexes
            ,'validation_indexes': validation_indexes
        }, 'deduplicate_data': False}, **learn_kwargs)

    df_test = predictor.transaction.input_data.validation_df
    predictions = predictor.predict(when_data=df_test)
    predictions = [x.explanation for x  in predictions]

    accuracy = acc_func([x[target]['predicted_value'] for x in predictions], df_test[target])


    confidence_accuracy = None
    if conf_func is not None:
        try:
            confidence_accuracy = conf_func([x[target] for x in predictions], list(df_test[target]), acc_func)
        except:
            confidence_accuracy = conf_func([x[target] for x in predictions], list(df_test[target]))

    return accuracy, confidence_accuracy
