def run_pycaret(name, df_train, df_test, acc_func, target):
    pycaret_acc_func_str = 'Accuracy'
    for pycaret_metrics in ['Accuracy', 'AUC', 'Recall', 'Precision', 'F1', 'Kappa', 'MCC', 'MAE', 'MSE', 'RMSE', 'R2', 'RMSLE', 'MAPE']:
        if pycaret_metrics.lower() in str(acc_func).lower():
            pycaret_acc_func_str = pycaret_metrics

    import traceback
    task_type = 'classification'
    if pycaret_acc_func_str in ['MAE', 'MSE', 'RMSE', 'R2', 'RMSLE', 'MAPE']:
        task_type = 'regression'
        from pycaret.regression import setup, compare_models, predict_model, blend_models, stack_models, automl, create_model
    else:
        from pycaret.classification import setup, compare_models, predict_model, blend_models, stack_models, automl, create_model

    setup_return = setup(data=df_train, target=target)

    top_models = compare_models(n_select=3, verbose=False, sort=pycaret_acc_func_str, turbo=True, blacklist = ['catboost','xgboost'])

    # Ensemble the top models and optimize the resulting model
    blender = blend_models(estimator_list=top_models, verbose=False)
    stacker = stack_models(estimator_list=top_models, meta_model=top_models[0], verbose=False)
    best_model = automl(optimize=pycaret_acc_func_str)

    df_test_dropped = df_test.drop(columns=[target])

    predictions = predict_model(best_model, data=df_test_dropped)

    try:
        accuracy = acc_func(list(predictions['Label']), list(df_test[target]))
    except Exception as e:
        traceback.print_exc()
        print(f'Exception computing accuracy (1): {e}')
        if task_type == 'classification':
            accuracy = acc_func([str(x) for x in list(predictions['Label'])], [str(x) for x in list(df_test[target])])
        elif task_type == 'regression':
            accuracy = acc_func([float(x) for x in list(predictions['Label'])], [float(x) for x in list(df_test[target])])


    return accuracy
