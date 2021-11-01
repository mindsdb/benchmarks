import numpy as np
with open('data.csv', 'w') as fp:
    fp.write('ecg_readings,anomaly')
    data = np.load('challenge2017.pkl', allow_pickle=True)
    for i in range(len(data['label'])):
        str_array = ' '.join([str(x) for x in data["data"][i]])
        fp.write(f'\n{str_array},{data["label"][i]}')
