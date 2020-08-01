import pandas as pd
import numpy as np

def data_reader():
    data = pd.read_csv('data.csv')
    array_data = np.array(data)  # df数据转为np.ndarray()
    list_data = array_data.tolist()  # 将np.ndarray()转为列表
    for i in range(len(list_data)):
        list_data[i].remove(list_data[i][0])
    return list_data

if __name__ == '__main__':
    print(data_reader())
